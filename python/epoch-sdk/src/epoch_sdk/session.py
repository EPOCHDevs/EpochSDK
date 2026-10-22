"""One headless session over native operation records and the Epoch UI stream.

This module owns observation and input mapping, never a workflow or durable
state store. Renderers and MCP consume the same finite session event variants.
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator, Awaitable, Callable
from contextlib import aclosing
from typing import Annotated, Literal, cast

import httpx
from pydantic import BaseModel, ConfigDict, Field, JsonValue, TypeAdapter

from .contracts import DomainError, RunRequest
from .research import (
    EpochClient,
    ResearchAccepted,
    ResearchCompleted,
    ResearchError,
    ResearchFailure,
    ResearchResult,
)
from .supervisor import Answers, InProgress, NeedsInput, WorkflowHandle


class _Closed(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)


class NativeUIMessage(_Closed):
    """Source envelope: langgraph.graph.ui.UIMessage.

    Component names/props and metadata extensions are deliberately service-owned
    extension points, as in Portal's UIMessage registry. They remain JSON here;
    SDK session events themselves have closed, validated outer shapes.
    """

    type: Literal["ui"]
    id: str
    name: str
    props: dict[str, JsonValue]
    metadata: dict[str, JsonValue] = Field(default_factory=dict)


class _RemoveUI(_Closed):
    type: Literal["remove-ui"]
    id: str


_ui_adapter = TypeAdapter(NativeUIMessage | _RemoveUI)
_stream_data: TypeAdapter[JsonValue] = TypeAdapter(JsonValue)


class SessionStatus(_Closed):
    event: Literal["status"]
    operation_id: str
    status: Literal["accepted", "in_progress"]
    handle: WorkflowHandle | None = None


class SessionUI(_Closed):
    event: Literal["ui"]
    handle: WorkflowHandle
    message: NativeUIMessage


class SessionUIRemoved(_Closed):
    event: Literal["ui_removed"]
    handle: WorkflowHandle
    id: str


class SessionQuestions(_Closed):
    event: Literal["questions"]
    waiting: NeedsInput


class SessionCompleted(_Closed):
    event: Literal["completed"]
    result: ResearchCompleted


type SessionEvent = Annotated[
    SessionStatus | SessionUI | SessionUIRemoved | SessionQuestions | SessionCompleted,
    Field(discriminator="event"),
]
type EventHandler = Callable[[SessionEvent], Awaitable[None]]
type QuestionHandler = Callable[[NeedsInput], Awaitable[dict[str, Answers] | None]]


class _ToolCall(BaseModel):
    model_config = ConfigDict(extra="ignore", strict=True)
    id: str | None = None


class _Message(BaseModel):
    model_config = ConfigDict(extra="ignore", strict=True)
    id: str | None = None
    type: str | None = None
    role: str | None = None
    tool_calls: list[_ToolCall] = Field(default_factory=list[_ToolCall])


class _UIState(BaseModel):
    """Read-only projection of the server checkpoint; never written back."""

    model_config = ConfigDict(extra="ignore", strict=True)
    ui: list[NativeUIMessage | _RemoveUI] = Field(default_factory=list[NativeUIMessage | _RemoveUI])
    messages: list[_Message] = Field(default_factory=list[_Message])
    authority_turn_id: str | None = None


class _RunMetadata(BaseModel):
    model_config = ConfigDict(extra="ignore", strict=True)
    epoch_sdk_request_id: str | None = None
    epoch_sdk_ui_stream: str | None = None


class ResearchSession:
    def __init__(
        self,
        client: EpochClient,
        request: RunRequest | None,
        *,
        operation_id: str,
        thread_id: str | None = None,
    ) -> None:
        if not operation_id.strip() or operation_id != operation_id.strip():
            raise ValueError("Provide an exact nonblank operation_id")
        if request is None and thread_id is not None:
            raise ValueError("Reconnect by operation_id; its server record owns the thread")
        self.client = client
        self.request = request
        self.operation_id = operation_id
        self.thread_id = thread_id
        self._current: ResearchResult | None = None
        # Ephemeral display reducer only. Fresh clients hydrate from the server.
        self._ui: dict[str, NativeUIMessage] = {}

    def _reduce_ui(
        self, value: NativeUIMessage | _RemoveUI, handle: WorkflowHandle
    ) -> SessionUI | SessionUIRemoved | None:
        if isinstance(value, _RemoveUI):
            if self._ui.pop(value.id, None) is not None:
                return SessionUIRemoved(event="ui_removed", handle=handle, id=value.id)
            return None
        previous = self._ui.get(value.id)
        merge = value.metadata.get("merge", False)
        if not isinstance(merge, bool):
            raise TypeError("Native UI merge must be boolean")
        if merge and previous is not None:
            value = value.model_copy(update={"props": {**previous.props, **value.props}})
        if previous == value:
            return None
        self._ui[value.id] = value
        return SessionUI(event="ui", handle=handle, message=value)

    def _state_ui(self, raw: object, handle: WorkflowHandle) -> list[SessionUI | SessionUIRemoved]:
        state = _UIState.model_validate(raw)
        if state.authority_turn_id not in (None, "user-turn:" + handle.request_id):
            return []  # A later query's live thread is not this operation's UI.
        owned_messages: set[str] = set()
        owned_calls: set[str] = set()
        in_turn = False
        for message in state.messages:
            if message.type == "human" or message.role == "user":
                in_turn = message.id == handle.request_id
            if in_turn:
                if message.id is not None:
                    owned_messages.add(message.id)
                owned_calls.update(call.id for call in message.tool_calls if call.id is not None)
        events: list[SessionUI | SessionUIRemoved] = []
        for message in state.ui:
            message_id = (
                message.metadata.get("message_id") if isinstance(message, NativeUIMessage) else None
            )
            call_id = (
                message.metadata.get("tool_call_id")
                if isinstance(message, NativeUIMessage)
                else None
            )
            if isinstance(message, NativeUIMessage) and not (
                (isinstance(message_id, str) and message_id in owned_messages)
                or (isinstance(call_id, str) and call_id in owned_calls)
                or (handle.run_id is not None and message.props.get("parent_id") == handle.run_id)
                or message.id in self._ui
            ):
                continue
            event = self._reduce_ui(message, handle)
            if event is not None:
                events.append(event)
        return events

    async def _observe(
        self, handle: WorkflowHandle
    ) -> AsyncGenerator[SessionUI | SessionUIRemoved]:
        if handle.run_id is None:
            return
        native = await self.client.supervisor.graph.runs.get(handle.thread_id, handle.run_id)
        metadata = _RunMetadata.model_validate(native["metadata"] or {})
        if metadata.epoch_sdk_request_id != handle.request_id:
            raise ValueError("The native stream belongs to another operation")
        buffered = metadata.epoch_sdk_ui_stream == "v1"
        if not buffered:
            # Pre-session native runs did not retain an SSE buffer. Hydrate
            # their current UI, then observe live events without replay.
            snapshot = await self.client.supervisor.graph.threads.get_state(handle.thread_id)
            for event in self._state_ui(cast(object, snapshot["values"]) or {}, handle):
                yield event
        # Native buffered observation only: disconnecting this iterator never
        # cancels, restarts, retries or re-plans the underlying graph run.
        stream = self.client.supervisor.graph.runs.join_stream(
            handle.thread_id,
            handle.run_id,
            cancel_on_disconnect=False,
            stream_mode=["values", "custom"],
            last_event_id="0" if buffered else None,
        )
        try:
            async for part in stream:
                kind = part.event.split("|", 1)[0]
                # LangGraph streams arbitrary configured graph data. Validate
                # JSON at this boundary before decoding the finite UI shape.
                data = _stream_data.validate_python(cast(object, part[1]))
                if kind == "error":
                    # The operation/run record owns the terminal outcome. Read
                    # it after closing this stream rather than inferring it
                    # from an observation event or persisting a guessed error.
                    return
                if (
                    kind == "custom"
                    and isinstance(data, dict)
                    and data.get("type") in {"ui", "remove-ui"}
                ):
                    event = self._reduce_ui(_ui_adapter.validate_python(data), handle)
                    if event is not None:
                        yield event
                elif kind == "values" and "|" not in part.event:
                    for event in self._state_ui(data, handle):
                        yield event
                # Only UI/custom/value modes are requested. Raw draft model tokens
                # are not another answer; final parts come from saved publication.
        finally:
            if isinstance(stream, AsyncGenerator):
                await stream.aclose()

    async def events(self) -> AsyncGenerator[SessionEvent]:
        """Stream to a question or saved answer. Never choose a reply implicitly."""
        if self._current is None:
            if self.request is None:
                self._current = await self.client.research_status(operation_id=self.operation_id)
            else:
                self._current = await self.client.research(
                    self.request,
                    operation_id=self.operation_id,
                    thread_id=self.thread_id,
                    wait=False,
                )
        previous_status: SessionStatus | None = None
        while True:
            current = self._current
            if isinstance(current, ResearchCompleted):
                yield SessionCompleted(event="completed", result=current)
                return
            if isinstance(current, NeedsInput):
                yield SessionQuestions(event="questions", waiting=current)
                return
            status = SessionStatus(
                event="status",
                operation_id=self.operation_id,
                status=current.status,
                handle=current.handle if isinstance(current, InProgress) else None,
            )
            if status != previous_status:
                yield status
                previous_status = status
            if isinstance(current, InProgress):
                try:
                    async with aclosing(self._observe(current.handle)) as stream:
                        async for event in stream:
                            yield event
                except httpx.HTTPError as error:
                    raise ResearchError(
                        ResearchFailure(
                            request_id=current.handle.request_id,
                            error=DomainError(
                                code="TEMPORARILY_UNAVAILABLE",
                                message=(
                                    "The stream connection ended. Reconnect with the same operation_id; "
                                    "the server-owned research has not been cancelled."
                                ),
                                retryable=True,
                            ),
                        )
                    ) from error
                except (ValueError, TypeError) as error:
                    raise ResearchError(
                        ResearchFailure(
                            request_id=current.handle.request_id,
                            error=DomainError(
                                code="INVALID_STATE",
                                message="The native UI stream did not match its operation or event contract.",
                                retryable=False,
                            ),
                        )
                    ) from error
            self._current = await self.client.research_status(operation_id=self.operation_id)
            if isinstance(self._current, (ResearchAccepted, InProgress)):
                # Admission/checkpoint publication can settle after the SSE end.
                # Reading status here starts no new work and creates no local registry.
                await asyncio.sleep(0.25)

    async def resume(self, waiting: NeedsInput, responses: dict[str, Answers]) -> None:
        if waiting.handle.operation_id != self.operation_id:
            raise ValueError("The pending question belongs to a different operation")
        self._current = await self.client.resume_research(waiting, responses, wait=False)

    async def run(
        self,
        *,
        on_event: EventHandler | None = None,
        on_question: QuestionHandler | None = None,
    ) -> ResearchCompleted | NeedsInput:
        """Shared flow for terminal, notebook and structured MCP callers."""
        while True:
            async with aclosing(self.events()) as events:
                async for event in events:
                    if on_event is not None:
                        await on_event(event)
                    if isinstance(event, SessionCompleted):
                        return event.result
                    if isinstance(event, SessionQuestions):
                        responses = (
                            None if on_question is None else await on_question(event.waiting)
                        )
                        if responses is None:
                            return event.waiting
                        await self.resume(event.waiting, responses)
                        break
