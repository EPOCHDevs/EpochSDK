"""Stateful communication with the existing supervisor through the native SDKs.

This adapter does not define a new agent, checkpoint store, or execution registry.
Selecting an engine execution is separate from validating its requested outputs.
"""

from __future__ import annotations

from collections.abc import AsyncIterator, Callable, Mapping
from typing import Literal, NotRequired, Protocol, TypedDict, cast
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from uuid import NAMESPACE_URL, uuid4, uuid5

import httpx
from epoch_sources.client import AsyncSourcesClient
from langgraph_sdk.client import LangGraphClient
from langgraph_sdk.schema import Command, Run, RunCreateMetadata, StreamMode
from pydantic import BaseModel, ConfigDict, Field, JsonValue, field_validator, model_validator
from stratifyx import (
    AsyncStratifyX,
    DatePeriodConfig,
    ExecutionOptions,
    ExecutionReportReference,
    SdkExecutionRecord,
)
from stratifyx.core.api_error import ApiError
from stratifyx.types.job_list_item import JobListItem

from .contracts import DomainError
from .credentials import Token, http_clients
from .dataset_reviews import (
    DatasetConfigureInterrupt,
    DatasetConfigureResponse,
    DatasetResultInterrupt,
    DatasetResultResponse,
    DatasetWorkflowInterrupt,
    interrupt_adapter,
)
from .responses import (
    ResearchResponseContent,
    ResponsePlanReference,
    ResponseReference,
    ResponseTablePage,
    SavedResearchResponse,
    publish_response,
    read_response,
    read_response_table_page,
)
from .saved_outputs import SavedOutputManifest, ValidatedSavedOutputs, read_saved_outputs


class Closed(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)


class QuestionOption(Closed):
    label: str
    recommended: bool


class Question(Closed):
    question: str
    description: str
    options: list[QuestionOption]
    multi_select: bool


class AskUser(Closed):
    """Source wire: EpochAI agent_src/common/ask_user.py::AskUserInterruptPayload."""

    type: Literal["ask_user"]
    questions: list[Question]
    tool_call_id: str


class GraphInterrupt(Closed):
    # Configured LangGraph assistants own arbitrary interrupt values. Recognized
    # Epoch ask_user values are decoded into the closed model by ask_user().
    id: str
    value: JsonValue
    response_schema: dict[str, JsonValue] | None = None

    def ask_user(self) -> AskUser:
        return AskUser.model_validate(self.value)

    def dataset_review(self) -> DatasetWorkflowInterrupt:
        return interrupt_adapter.validate_python(self.value)


class Answer(Closed):
    question_index: int
    selected_indices: list[int] = Field(default_factory=list[int])
    free_form_input: str | None = None


class Answers(Closed):
    """Source wire: EpochAI agent_src/common/ask_user.py::AskUserResponse."""

    answers: list[Answer]


type InterruptResponse = Answers | DatasetConfigureResponse | DatasetResultResponse


class WorkflowHandle(Closed):
    thread_id: str
    request_id: str
    assistant_id: str
    run_id: str | None = None
    operation_id: str | None = None
    execution_ids_before: list[str] = Field(default_factory=list)
    outcome_ids_before: list[str] = Field(default_factory=list)


class NeedsInput(Closed):
    status: Literal["needs_input"] = "needs_input"
    handle: WorkflowHandle
    interrupts: list[GraphInterrupt]
    conversation_url: str | None = None

    def feedback(self) -> str:
        lines = ["The workflow is waiting for input."]
        for item in self.interrupts:
            if isinstance(item.value, dict) and item.value.get("type") == "dataset_review":
                review = item.dataset_review()
                if isinstance(review, DatasetConfigureInterrupt):
                    lines.extend(
                        [
                            f"Review dataset fields: {review.request.name}",
                            review.request.preparation.schema_choice.model_dump_json(by_alias=True),
                            "Choose Build preview or Cancel explicitly. No processing has started.",
                        ]
                    )
                else:
                    lines.extend(
                        [
                            f"Review dataset preview: {review.operation.request.name}",
                            review.operation.message,
                            f"Operation: {review.operation.preparation_ref}",
                            "Choose an available explicit action; no decision is selected automatically.",
                        ]
                    )
                    if review.preview is not None:
                        lines.append(
                            review.preview.model_dump_json(by_alias=True, exclude_none=True)
                        )
                    lines.append(review.operation.coverage.model_dump_json(by_alias=True))
                    allowed = (
                        review.operation.review.allowed_actions if review.operation.review else []
                    )
                    labels = [
                        label
                        for action, label in (
                            ("save", "Save dataset"),
                            ("save_available", "Save available data"),
                            ("retry_save", "Retry saving"),
                            ("discard", "Don't save"),
                        )
                        if action in allowed
                    ]
                    if review.can_edit:
                        labels.append("Edit then Build preview")
                    if review.operation.state.value in {"saved", "discarded", "expired", "stopped"}:
                        labels.append("Continue conversation")
                    lines.append("Available: " + ", ".join(labels))
                    lines.extend(review.operation.limitations)
                continue
            if not isinstance(item.value, dict) or item.value.get("type") != "ask_user":
                lines.append("Open the conversation to respond to this interrupt.")
                continue
            for question in item.ask_user().questions:
                lines.append(question.question)
                if question.description:
                    lines.append(question.description)
                for index, option in enumerate(question.options):
                    suffix = " (recommended)" if option.recommended else ""
                    lines.append(f"{index + 1}. {option.label}{suffix}")
        if self.conversation_url:
            lines.append(f"Continue: {self.conversation_url}")
        return "\n".join(lines)


class SavedStudy(Closed):
    study_id: str
    source_execution_id: str
    thread_id: str | None = None
    response_plan: ResponsePlanReference | None = None
    report_template: ExecutionReportReference | None = None

    @model_validator(mode="after")
    def one_output_program(self) -> SavedStudy:
        if self.report_template is not None and (
            self.response_plan is not None or self.report_template.model_extra
        ):
            raise ValueError("Choose one exact native report or historical response plan")
        return self


class ChosenExecution(Closed):
    # Engine completion does not certify requested output schemas or correctness.
    status: Literal["execution_selected"] = "execution_selected"
    handle: WorkflowHandle | None = None
    execution: JobListItem
    reusable_study: SavedStudy
    reply: str = ""
    operation_id: str | None = None
    request_id: str | None = None
    response: SavedResearchResponse | None = None
    # The original engine job remains execution; this is its separate native
    # report, including exact dashboard/answer publication pins.
    report: SdkExecutionRecord | None = None


class PublishedAnswer(Closed):
    status: Literal["response_published"] = "response_published"
    handle: WorkflowHandle
    response: ResponseReference


class NoExecution(Closed):
    status: Literal["no_execution"] = "no_execution"
    handle: WorkflowHandle
    reason: str
    publication_failed: bool = False
    publication_error: DomainError | None = None
    execution_id: str | None = None
    reply: str = ""


class InProgress(Closed):
    status: Literal["in_progress"] = "in_progress"
    handle: WorkflowHandle


type SupervisorResult = NeedsInput | PublishedAnswer | ChosenExecution | NoExecution | InProgress


class _Outcome(BaseModel):
    """Read-only projection of EpochAI's next_action_evidence owner contract."""

    model_config = ConfigDict(extra="ignore", strict=True)
    tool_call_id: str
    tool_name: Literal["build_study", "run_study", "run_monte_carlo", "tune_study"]
    subject: str | None
    status: Literal[
        "saved", "completed", "failed", "cancelled", "not_started", "infeasible", "unknown"
    ]
    detail: str
    execution_id: str | None = None


class _MessageToolCall(BaseModel):
    """Consumer projection; the registered tool owns its unused argument shape."""

    model_config = ConfigDict(extra="ignore", strict=True)
    id: str
    name: str


class _Message(BaseModel):
    model_config = ConfigDict(extra="ignore", strict=True)
    type: str | None = None
    role: str | None = None
    # Model providers own rich/multimodal content; only text is displayed here.
    content: JsonValue = ""
    tool_calls: list[_MessageToolCall] = Field(default_factory=list[_MessageToolCall])


class _State(BaseModel):
    """Finite consumer projection; unused native state is never rewritten."""

    model_config = ConfigDict(extra="ignore", strict=True, populate_by_name=True)
    execution_ids: list[str] = Field(default_factory=list)
    next_action_outcomes: dict[str, _Outcome] = Field(default_factory=dict)
    messages: list[_Message] = Field(default_factory=list[_Message])
    published_response: ResponseReference | None = None
    publication_error: DomainError | None = None
    authority_turn_id: str | None = None
    interrupts: list[GraphInterrupt] = Field(
        default_factory=list[GraphInterrupt], alias="__interrupt__"
    )

    @field_validator("published_response", mode="before")
    @classmethod
    def checkpoint_response(cls, value: object) -> ResponseReference | None:
        if value is None:
            return None
        if isinstance(value, dict):
            # Native checkpoint serialization includes default null metadata.
            # Normalize only the known optional reference fields at this boundary.
            raw = cast(dict[str, object], value)
            value = {
                key: item
                for key, item in raw.items()
                if key not in {"primary_execution_id", "study_id"} or item is not None
            }
        return ResponseReference.model_validate(value)

    @field_validator("publication_error", mode="before")
    @classmethod
    def checkpoint_error(cls, value: object) -> DomainError | None:
        if value is None:
            return None
        if isinstance(value, dict):
            raw = cast(dict[str, object], value)
            optional = {
                "gaps",
                "questions",
                "recommended_task",
                "data_requirements",
                "access_requirements",
            }
            value = {
                key: item for key, item in raw.items() if key not in optional or item is not None
            }
        return DomainError.model_validate(value)

    def reply(self) -> str:
        for message in reversed(self.messages):
            if message.type in {"human", "user"} or message.role == "user":
                return ""
            if message.type != "ai" and message.role != "assistant":
                continue
            if message.tool_calls:
                continue
            if isinstance(message.content, str):
                return message.content
            if isinstance(message.content, list):
                texts: list[str] = []
                for block in message.content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        text = block.get("text")
                        if isinstance(text, str):
                            texts.append(text)
                return "\n".join(texts)
        return ""


def _header_from_auth_flow() -> str:
    # AsyncSourcesClient writes "Bearer <this>"; with a provider, the auth flow replaces it.
    return ""


def api_url(value: str) -> str:
    parsed = urlsplit(value)
    if (
        parsed.scheme not in ("http", "https")
        or not parsed.hostname
        or parsed.username
        or parsed.password
    ):
        raise ValueError("Provide an HTTP(S) endpoint without URL credentials")
    if parsed.query or parsed.fragment:
        raise ValueError("API endpoints must not contain query strings or fragments")
    return value.rstrip("/")


class _UserMessage(TypedDict):
    role: Literal["user"]
    id: str
    content: str


class _SupervisorInput(TypedDict):
    messages: list[_UserMessage]
    sdk_request_id: NotRequired[str]


class _RunsWait(Protocol):
    # langgraph-sdk 0.4.4 implements durability at runtime, but omits it from
    # wait()'s overload declarations. Keep this narrow native-boundary shim.
    async def wait(
        self,
        thread_id: str,
        assistant_id: str,
        *,
        input: _SupervisorInput | None,
        command: Command | None,
        metadata: dict[str, str],
        durability: Literal["sync"],
        on_disconnect: Literal["continue"],
        multitask_strategy: Literal["reject"],
        on_run_created: Callable[[RunCreateMetadata], None],
    ) -> object: ...


class _RunsAdmission(Protocol):
    # Native SDK runtime options; its pinned overloads omit durability on create.
    async def create(
        self,
        thread_id: str,
        assistant_id: str,
        *,
        input: _SupervisorInput | None = None,
        command: Command | None = None,
        metadata: dict[str, str],
        durability: Literal["sync"],
        multitask_strategy: Literal["reject"],
        on_completion: Literal["keep"],
        stream_mode: list[StreamMode] = ...,
        stream_subgraphs: bool = ...,
        stream_resumable: bool = ...,
    ) -> Run: ...

    # The configured graph owns join values; this caller discards them and reads
    # the operation's checkpoint through the existing finite state projection.
    async def join(self, thread_id: str, run_id: str) -> object: ...


class SupervisorClient:
    def __init__(
        self,
        graph: LangGraphClient,
        backend: AsyncStratifyX,
        *,
        assistant_id: str = "epoch-ai",
        ui_url: str | None = None,
        source_connections: AsyncSourcesClient | None = None,
        document_http: httpx.AsyncClient | None = None,
    ) -> None:
        self.graph = graph
        self.backend = backend
        self.assistant_id = assistant_id
        self.ui_url = ui_url
        self.source_connections = source_connections
        self.document_http = document_http
        self._owned_http: list[httpx.AsyncClient] = []

    @classmethod
    def connect(
        cls,
        *,
        graph_url: str,
        backend_url: str,
        token: Token,
        assistant_id: str = "epoch-ai",
        ui_url: str | None = None,
    ) -> SupervisorClient:
        """Connect with a token string, or a provider that every request awaits for its token.

        A provider is for a server acting for one user with renewing tokens (see
        ``epoch_sdk.credentials``). Connect once per user and request.
        """
        return cls._connect(
            graph_url=graph_url,
            backend_url=backend_url,
            token=token,
            assistant_id=assistant_id,
            ui_url=ui_url,
        )

    @classmethod
    def _connect(
        cls,
        *,
        graph_url: str,
        backend_url: str,
        token: Token,
        assistant_id: str = "epoch-ai",
        ui_url: str | None = None,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> SupervisorClient:
        graph_url = api_url(graph_url)
        backend_url = api_url(backend_url)
        graph_http, backend_http = http_clients(
            graph_url=graph_url, backend_url=backend_url, token=token, transport=transport
        )
        fixed = token if isinstance(token, str) else None
        client = cls(
            LangGraphClient(graph_http),
            # With a provider, the auth flow on backend_http sets the header for every request.
            AsyncStratifyX(base_url=backend_url, token=fixed, httpx_client=backend_http),
            assistant_id=assistant_id,
            ui_url=ui_url,
            source_connections=AsyncSourcesClient(
                base_url=backend_url,
                token=fixed if fixed is not None else _header_from_auth_flow,
                http=backend_http,
            ),
            document_http=graph_http,
        )
        client._owned_http = [graph_http, backend_http]
        return client

    async def aclose(self) -> None:
        for http in self._owned_http:
            await http.aclose()

    async def outputs(self, manifest: SavedOutputManifest) -> ValidatedSavedOutputs:
        """Read and validate an explicit saved receipt directly through Backend."""
        return await read_saved_outputs(self.backend, manifest)

    async def publish_response(
        self,
        request_id: str,
        content: ResearchResponseContent,
        *,
        thread_id: str,
        primary_execution_id: str | None = None,
        expected_version: int = 0,
    ) -> SavedResearchResponse:
        """Publish one query's answer without starting an agent or execution."""
        return await publish_response(
            self.backend,
            request_id,
            content,
            thread_id=thread_id,
            primary_execution_id=primary_execution_id,
            expected_version=expected_version,
        )

    async def response(
        self, response_id: str, *, version: int | None = None
    ) -> SavedResearchResponse:
        return await read_response(self.backend, response_id, version=version)

    async def execution(self, execution_id: str) -> JobListItem:
        """Read a native execution, including jobs started without a graph handle."""
        if not execution_id.strip() or execution_id != execution_id.strip():
            raise ValueError("Provide an exact nonblank execution identity")
        job = await self.backend.studies_executions.get_execution_by_id(
            execution_id,
            request_options={"max_retries": 0},
        )
        if job.id != execution_id:
            raise ValueError("Backend returned a different execution identity")
        return job

    async def response_table(
        self,
        response_id: str,
        name: str,
        *,
        version: int | None = None,
        offset: int = 0,
        page_size: int = 1000,
    ) -> ResponseTablePage:
        """Read one page of an answer's table directly from Backend."""
        saved = await self.response(response_id, version=version)
        return await read_response_table_page(
            self.backend, saved, name, offset=offset, page_size=page_size
        )

    async def iter_response_table(
        self,
        response_id: str,
        name: str,
        *,
        version: int | None = None,
        page_size: int = 1000,
    ) -> AsyncIterator[ResponseTablePage]:
        """Pin the answer revision once and traverse its complete table."""
        saved = await self.response(response_id, version=version)
        offset = 0
        while True:
            page = await read_response_table_page(
                self.backend, saved, name, offset=offset, page_size=page_size
            )
            yield page
            if page.next_offset is None:
                break
            offset = page.next_offset

    def conversation_url(self, thread_id: str) -> str | None:
        if self.ui_url is None:
            return None
        parsed = urlsplit(self.ui_url)
        if (
            parsed.scheme not in ("http", "https")
            or not parsed.hostname
            or parsed.username
            or parsed.password
        ):
            raise ValueError("Provide a UI URL without embedded credentials")
        query = dict(parse_qsl(parsed.query, keep_blank_values=True))
        query["threadId"] = thread_id  # EpochPortal's existing route parameter.
        return urlunsplit(
            (parsed.scheme, parsed.netloc, parsed.path, urlencode(query), parsed.fragment)
        )

    async def run(self, task: str, *, thread_id: str | None = None) -> SupervisorResult:
        if not task.strip():
            raise ValueError("Task must not be blank")
        handle = await self.prepare(thread_id)
        return await self._wait(handle, task=task)

    async def prepare(
        self,
        thread_id: str | None,
        *,
        request_id: str | None = None,
    ) -> WorkflowHandle:
        """Resolve a native thread before attaching the accepted Backend record."""
        if thread_id is None:
            thread = await self.graph.threads.create()
            thread_id = thread["thread_id"]
            before = _State()
        else:
            snapshot = await self.graph.threads.get_state(thread_id)
            before = _State.model_validate(snapshot["values"] or {})
            if snapshot["interrupts"] or before.interrupts:
                raise ValueError("This thread is waiting for input; resume its existing handle")
        return WorkflowHandle(
            thread_id=thread_id,
            request_id=request_id or str(uuid4()),
            assistant_id=self.assistant_id,
            execution_ids_before=before.execution_ids,
            outcome_ids_before=list(before.next_action_outcomes),
        )

    async def submit(
        self,
        handle: WorkflowHandle,
        task: str,
        *,
        sdk_request_id: str | None = None,
    ) -> SupervisorResult:
        """Submit a prepared turn after its owning request/runtime is persisted."""
        if not task.strip():
            raise ValueError("Task must not be blank")
        return await self._wait(handle, task=task, sdk_request_id=sdk_request_id)

    async def prepare_operation(self, request_id: str, thread_id: str | None) -> WorkflowHandle:
        """Create/attach the operation's thread before the native admission gate."""
        if thread_id is None:
            thread_id = str(uuid5(NAMESPACE_URL, "epoch:research:" + request_id))
            await self.graph.threads.create(thread_id=thread_id, if_exists="do_nothing")
        return await self.prepare(thread_id, request_id=request_id)

    async def start_operation(self, handle: WorkflowHandle, task: str) -> None:
        """Create a native background run; server admission durably records its ID."""
        await cast(_RunsAdmission, self.graph.runs).create(
            handle.thread_id,
            handle.assistant_id,
            input={
                "messages": [{"role": "user", "id": handle.request_id, "content": task}],
                "sdk_request_id": handle.request_id,
            },
            metadata={"epoch_sdk_request_id": handle.request_id, "epoch_sdk_ui_stream": "v1"},
            durability="sync",
            multitask_strategy="reject",
            on_completion="keep",
            stream_mode=["values", "custom"],
            stream_subgraphs=True,
            stream_resumable=True,
        )

    async def join_operation(self, handle: WorkflowHandle) -> SupervisorResult:
        if handle.run_id is None:
            return InProgress(handle=handle)
        # Joining observes existing native work. Closing this wait never cancels it.
        try:
            await cast(_RunsAdmission, self.graph.runs).join(handle.thread_id, handle.run_id)
        except httpx.HTTPStatusError as error:
            if error.response.status_code == 404:
                # The server recorded admission before publishing the native run.
                return InProgress(handle=handle)
            raise
        return await self.status(handle)

    @staticmethod
    def resume_command(waiting: NeedsInput, responses: Mapping[str, InterruptResponse]) -> Command:
        expected = {item.id for item in waiting.interrupts}
        if not expected:
            raise ValueError("There are no pending interrupts to resume")
        if set(responses) != expected:
            raise ValueError("Provide answers for exactly the pending interrupt ids")
        resume: dict[str, JsonValue] = {}
        for item in waiting.interrupts:
            answer = responses[item.id]
            if isinstance(item.value, dict) and item.value.get("type") == "dataset_review":
                review = item.dataset_review()
                if isinstance(review, DatasetConfigureInterrupt):
                    if (
                        not isinstance(answer, DatasetConfigureResponse)
                        or answer.proposal_ref != review.proposal_ref
                    ):
                        raise ValueError("Provide the exact dataset configuration decision")
                else:
                    operation = review.operation
                    identity = operation.review
                    if (
                        not isinstance(answer, DatasetResultResponse)
                        or identity is None
                        or (
                            answer.preparation_ref != operation.preparation_ref
                            or answer.attempt != operation.attempt
                            or answer.review_ref != identity.review_ref
                            or answer.result_sha256 != operation.result_sha256
                            or answer.schema_sha256 != identity.schema_sha256
                        )
                    ):
                        raise ValueError(
                            "Provide a decision for the exact displayed dataset result"
                        )
                    if answer.action == "continue":
                        if operation.state.value not in {
                            "saved",
                            "discarded",
                            "expired",
                            "stopped",
                        }:
                            raise ValueError(
                                "Continue can only deliver a confirmed terminal dataset outcome"
                            )
                    elif answer.action == "edit":
                        if not review.can_edit:
                            raise ValueError("This dataset review cannot be edited")
                    elif (
                        not (
                            operation.state.value == "saved"
                            and answer.action in {"save", "save_available"}
                            or operation.state.value == "discarded"
                            and answer.action == "decline"
                            or operation.state.value == "save_failed"
                            and "retry_save" in identity.allowed_actions
                            and answer.action in {"save", "save_available"}
                        )
                        and ("discard" if answer.action == "decline" else answer.action)
                        not in identity.allowed_actions
                    ):
                        raise ValueError(
                            "This action is unavailable for the current dataset review"
                        )
                resume[item.id] = answer.model_dump(mode="json", by_alias=True, exclude_none=True)
                continue
            if not isinstance(answer, Answers):
                raise TypeError("A question interrupt requires structured answers")
            questions = item.ask_user().questions
            answers = answer
            used: set[int] = set()
            for answer in answers.answers:
                index = answer.question_index
                if index in used or index < 0 or index >= len(questions):
                    raise ValueError("Question index is duplicated or out of range")
                used.add(index)
                question = questions[index]
                selected = answer.selected_indices
                if len(set(selected)) != len(selected) or any(
                    i < 0 or i >= len(question.options) for i in selected
                ):
                    raise ValueError("Option index is duplicated or out of range")
                if not question.multi_select and (
                    len(selected) > 1 or (selected and answer.free_form_input)
                ):
                    raise ValueError("Single-select answers accept one option or free-form input")
                if answer.free_form_input and (
                    not answer.free_form_input.strip()
                    or answer.free_form_input != answer.free_form_input.strip()
                ):
                    raise ValueError("Free-form input must be exact and non-blank")
            if used != set(range(len(questions))):
                raise ValueError("Provide an answer row for every question; an empty row skips it")
            resume[item.id] = answers.model_dump(mode="json", exclude_unset=True)
        return Command(resume=resume)

    async def _prepare_resume(
        self, waiting: NeedsInput, responses: Mapping[str, InterruptResponse]
    ) -> Command:
        command = self.resume_command(waiting, responses)
        if all(isinstance(answer, Answers) for answer in responses.values()):
            return command
        current = await self.status(waiting.handle)
        if not isinstance(current, NeedsInput) or {i.id for i in current.interrupts} != {
            i.id for i in waiting.interrupts
        }:
            raise ValueError("The pending interrupt changed; reopen the current workflow")
        for old in waiting.interrupts:
            fresh = next(item for item in current.interrupts if item.id == old.id)
            if isinstance(old.value, dict) and old.value.get("type") == "dataset_review":
                old_review, fresh_review = old.dataset_review(), fresh.dataset_review()
                if isinstance(old_review, DatasetConfigureInterrupt):
                    if (
                        not isinstance(fresh_review, DatasetConfigureInterrupt)
                        or old_review.proposal_ref != fresh_review.proposal_ref
                    ):
                        raise ValueError("The current dataset proposal changed")
                elif isinstance(fresh_review, DatasetConfigureInterrupt) or (
                    old_review.operation.preparation_ref != fresh_review.operation.preparation_ref
                    or old_review.operation.attempt != fresh_review.operation.attempt
                    or old_review.operation.result_sha256 != fresh_review.operation.result_sha256
                    or old_review.operation.review is None
                    or fresh_review.operation.review is None
                    or old_review.operation.review.review_ref
                    != fresh_review.operation.review.review_ref
                ):
                    raise ValueError("The current dataset review changed")
            elif old.value != fresh.value:
                raise ValueError("The pending question changed")
        for item in waiting.interrupts:
            answer = responses[item.id]
            if not isinstance(answer, DatasetResultResponse) or answer.action == "edit":
                continue
            native = await self.backend.user_files.get_dataset_preparation(
                answer.preparation_ref,
                request_options={"max_retries": 0},
            )
            identity = native.review
            if (
                identity is None
                or native.attempt != answer.attempt
                or (
                    identity.review_ref != answer.review_ref
                    or native.result_sha256 != answer.result_sha256
                    or identity.schema_sha256 != answer.schema_sha256
                )
            ):
                raise ValueError("The native dataset review changed; reopen it before deciding")
            if native.state.value == "saving":
                raise ValueError(
                    "Save is not yet confirmed. Reconcile this operation; the agent remains paused."
                )
            if answer.action == "continue":
                if native.state.value not in {"saved", "discarded", "expired", "stopped"}:
                    raise ValueError("The terminal dataset outcome is not confirmed")
                continue
            terminal = "discarded" if answer.action == "decline" else "saved"
            if native.state.value != terminal:
                action = "discard" if answer.action == "decline" else answer.action
                if native.state.value == "save_failed" and answer.action != "decline":
                    action = "retry_save"
                from stratifyx.types import DatasetBuildActionRequest

                decision = DatasetBuildActionRequest.model_validate(
                    {
                        "action": action,
                        "attempt": answer.attempt,
                        "result_sha256": answer.result_sha256,
                        "review_ref": answer.review_ref,
                        "schema_sha256": answer.schema_sha256,
                    }
                )
                native = await self.backend.user_files.act_on_dataset_preparation(
                    answer.preparation_ref,
                    action=decision.action,
                    attempt=decision.attempt,
                    result_sha256=decision.result_sha256,
                    review_ref=decision.review_ref,
                    schema_sha256=decision.schema_sha256,
                    request_options={"max_retries": 0},
                )
            if native.state.value != terminal:
                raise ValueError(
                    "The dataset decision is not confirmed. Reopen the same operation; the agent remains paused."
                )
        return command

    async def start_resume(
        self, waiting: NeedsInput, responses: Mapping[str, InterruptResponse]
    ) -> None:
        """Resume the exact native interrupt in a kept background run."""
        command = await self._prepare_resume(waiting, responses)
        await cast(_RunsAdmission, self.graph.runs).create(
            waiting.handle.thread_id,
            waiting.handle.assistant_id,
            command=command,
            metadata={
                "epoch_sdk_request_id": waiting.handle.request_id,
                "epoch_sdk_ui_stream": "v1",
            },
            durability="sync",
            multitask_strategy="reject",
            on_completion="keep",
            stream_mode=["values", "custom"],
            stream_subgraphs=True,
            stream_resumable=True,
        )

    async def resume(
        self, waiting: NeedsInput, responses: Mapping[str, InterruptResponse]
    ) -> SupervisorResult:
        return await self._wait(
            waiting.handle, command=await self._prepare_resume(waiting, responses)
        )

    async def _wait(
        self,
        handle: WorkflowHandle,
        *,
        task: str | None = None,
        command: Command | None = None,
        sdk_request_id: str | None = None,
    ) -> SupervisorResult:
        current = handle

        def created(metadata: RunCreateMetadata) -> None:
            nonlocal current
            current = current.model_copy(update={"run_id": metadata["run_id"]})

        graph_input: _SupervisorInput | None = None
        if task is not None:
            graph_input = {"messages": [{"role": "user", "id": handle.request_id, "content": task}]}
            if sdk_request_id is not None:
                graph_input["sdk_request_id"] = sdk_request_id

        # Input/command belong to the native LangGraph transport. User prose is
        # supplied once; a resume sends only the pending answer command.
        state = _State.model_validate(
            await cast(_RunsWait, self.graph.runs).wait(
                handle.thread_id,
                handle.assistant_id,
                input=graph_input,
                command=command,
                metadata={"epoch_sdk_request_id": handle.request_id},
                durability="sync",
                on_disconnect="continue",
                multitask_strategy="reject",
                on_run_created=created,
            )
        )
        return await self._select(current, state)

    async def status(self, handle: WorkflowHandle) -> SupervisorResult:
        """Read this request after a human resumes in the UI; start no graph run."""
        native = await self._native_research_outcome(handle)
        if native is not None:
            return native
        if handle.operation_id is not None and handle.run_id is None:
            return InProgress(handle=handle)
        if handle.run_id is not None and handle.operation_id is not None:
            try:
                run = await self.graph.runs.get(handle.thread_id, handle.run_id)
            except httpx.HTTPStatusError as error:
                if error.response.status_code == 404:
                    return InProgress(handle=handle)
                raise
            if (run["metadata"] or {}).get("epoch_sdk_request_id") != handle.request_id:
                raise ValueError("The recorded native run belongs to another operation")
            if run["status"] in {"pending", "running"}:
                return InProgress(handle=handle)
            if run["status"] in {"error", "timeout"}:
                return NoExecution(handle=handle, reason="The accepted native graph run failed.")
            history = await self.graph.threads.get_history(
                handle.thread_id,
                limit=1,
                metadata={
                    "epoch_sdk_request_id": handle.request_id,
                    "epoch_sdk_run_id": handle.run_id,
                },
            )
            if history:
                snapshot = history[0]
                state = _State.model_validate(snapshot["values"] or {})
                if snapshot["interrupts"]:
                    state = state.model_copy(
                        update={
                            "interrupts": [
                                GraphInterrupt.model_validate(item)
                                for item in snapshot["interrupts"]
                            ]
                        }
                    )
                if run["status"] == "interrupted" and not state.interrupts:
                    return NoExecution(
                        handle=handle,
                        reason="The accepted native run was cancelled or interrupted.",
                    )
                return await self._select(handle, state)
            return NoExecution(
                handle=handle,
                reason="The accepted native run ended without a saved result checkpoint.",
            )
        thread = await self.graph.threads.get(handle.thread_id)
        if thread["status"] == "busy":
            return InProgress(handle=handle)
        snapshot = await self.graph.threads.get_state(handle.thread_id)
        state = _State.model_validate(snapshot["values"] or {})
        if snapshot["interrupts"]:
            state = state.model_copy(
                update={
                    "interrupts": [
                        GraphInterrupt.model_validate(item) for item in snapshot["interrupts"]
                    ]
                }
            )
        self._check_request(handle, state)
        if thread["status"] == "error":
            return NoExecution(
                handle=handle,
                reason="The graph run failed; no completed supervisor result is available.",
                reply=state.reply(),
            )
        if snapshot["next"] and not state.interrupts:
            return InProgress(handle=handle)
        return await self._select(handle, state)

    @staticmethod
    def _check_request(handle: WorkflowHandle, state: _State) -> None:
        # EpochAI's owner middleware stamps the stable HumanMessage identity.
        # A retained handle must not silently read a later, unrelated UI task.
        if state.authority_turn_id not in (None, f"user-turn:{handle.request_id}"):
            raise ValueError("This thread has moved to another request; use its current handle")

    async def _native_research_outcome(self, handle: WorkflowHandle) -> SupervisorResult | None:
        identifier = handle.request_id
        if (
            len(identifier) != 36
            or not identifier.startswith("req_")
            or any(char not in "0123456789abcdef" for char in identifier[4:])
        ):
            return None
        try:
            record = await self.backend.sdk_requests.get_sdk_request(
                identifier, request_options={"max_retries": 0}
            )
        except ApiError as error:
            if error.status_code == 404:
                return None  # A generic graph handle is not a Backend research record.
            raise
        if record.native_execution_request_id is None:
            return None
        if (
            record.request_id != handle.request_id
            or record.runtime is None
            or record.runtime.thread_id != handle.thread_id
            or record.runtime.assistant_id != handle.assistant_id
            or (handle.operation_id is not None and record.operation_id != handle.operation_id)
        ):
            raise ValueError(
                "The native research operation belongs to another request or conversation"
            )
        if record.error is not None:
            error = DomainError.model_validate_json(record.error.error.model_dump_json())
            return NoExecution(
                handle=handle,
                reason=error.message,
                publication_failed=True,
                publication_error=error,
                execution_id=record.error.execution_id,
            )
        if record.response_id is None or record.response_version is None:
            return InProgress(handle=handle)
        answer = await self.response(record.response_id, version=record.response_version)
        if (
            answer.request_id != record.native_execution_request_id
            or answer.thread_id != handle.thread_id
            or answer.primary_execution_id != record.current_execution_id
            or answer.version != record.response_version
            or answer.extension is None
        ):
            raise ValueError("The answer differs from the linked native research operation")
        return PublishedAnswer(handle=handle, response=answer.reference())

    async def _review_interrupts(self, items: list[GraphInterrupt]) -> list[GraphInterrupt]:
        """An explicit native edit may have happened through another client.

        Keep the real graph interrupt ID and follow only its native replacement
        chain. This is observation; it never prepares, saves or resumes anything.
        """
        result: list[GraphInterrupt] = []
        for item in items:
            if not isinstance(item.value, dict) or item.value.get("type") != "dataset_review":
                result.append(item)
                continue
            payload = item.dataset_review()
            if isinstance(payload, DatasetConfigureInterrupt):
                result.append(item)
                continue
            operation = await self.backend.user_files.get_dataset_preparation(
                payload.operation.preparation_ref,
                request_options={"max_retries": 0},
            )
            seen: set[str] = set()
            while operation.replaced_by is not None:
                if operation.preparation_ref in seen or len(seen) >= 32:
                    raise ValueError("Invalid dataset review replacement chain")
                seen.add(operation.preparation_ref)
                child = await self.backend.user_files.get_dataset_preparation(
                    operation.replaced_by,
                    request_options={"max_retries": 0},
                )
                if (
                    child.request.replaces is None
                    or child.request.replaces.preparation_ref != operation.preparation_ref
                ):
                    raise ValueError("Dataset replacement does not belong to this workflow")
                operation = child
            preview = None
            if operation.draft_ref is not None and operation.state.value in {
                "pending_review",
                "incomplete",
                "save_failed",
                "saved",
            }:
                preview = await self.backend.user_files.preview_saved_dataset(
                    operation.draft_ref,
                    offset=0,
                    limit=5,
                    request_options={"max_retries": 0},
                )
            projected = DatasetResultInterrupt(
                tool_call_id=payload.tool_call_id,
                operation=operation,
                preview=preview,
                can_edit=operation.state.value in {"pending_review", "incomplete"},
            )
            result.append(
                GraphInterrupt.model_validate(
                    {
                        "id": item.id,
                        "value": projected.model_dump(
                            mode="json", by_alias=True, exclude_none=True
                        ),
                        "response_schema": item.response_schema,
                    }
                )
            )
        return result

    async def _select(self, handle: WorkflowHandle, state: _State) -> SupervisorResult:
        native = await self._native_research_outcome(handle)
        if native is not None:
            return native
        self._check_request(handle, state)
        if state.interrupts:
            return NeedsInput(
                handle=handle,
                interrupts=await self._review_interrupts(state.interrupts),
                conversation_url=self.conversation_url(handle.thread_id),
            )
        reference = state.published_response
        if reference is not None:
            if reference.request_id != handle.request_id or reference.thread_id != handle.thread_id:
                raise ValueError("The published answer belongs to another query or thread")
            return PublishedAnswer(handle=handle, response=reference)
        if state.publication_error is not None:
            return NoExecution(
                handle=handle,
                reason=state.publication_error.message,
                publication_failed=True,
                publication_error=state.publication_error,
            )
        outcomes = [
            value
            for key, value in state.next_action_outcomes.items()
            if key not in handle.outcome_ids_before
        ]
        failed = [
            value
            for value in outcomes
            if value.status in {"failed", "cancelled", "infeasible", "not_started"}
        ]
        return NoExecution(
            handle=handle,
            reason=failed[-1].detail
            if failed
            else "Conversation completed without an engine execution."
            if state.reply().strip()
            else "The supervisor finished without delivering an answer for this query.",
            publication_failed=not bool(failed) and not bool(state.reply().strip()),
            execution_id=failed[-1].execution_id if failed else None,
            reply=state.reply() if not failed else "",
        )

    async def execute_saved(
        self,
        reference: SavedStudy,
        *,
        period: DatePeriodConfig,
        execution: ExecutionOptions | None = None,
    ) -> ChosenExecution:
        if reference.response_plan is not None or reference.report_template is not None:
            raise ValueError(
                "Use EpochClient.execute_saved for a prepared response plan so its "
                "outputs are replayed and published with the new execution."
            )
        definition = await self.backend.studies_definitions.get_a_study_definition_by_id(
            reference.study_id, request_options={"max_retries": 0}
        )
        if definition.authoring_origin.value != "agent":
            raise ValueError("Workflow reuse requires an immutable agent-authored study")
        if execution is None:
            accepted = await self.backend.studies_executions.start_execute_a_study(
                id=reference.study_id,
                period=period,
                thread_id=reference.thread_id,
                request_options={"max_retries": 0},
            )
        else:
            accepted = await self.backend.studies_executions.start_execute_a_study(
                id=reference.study_id,
                period=period,
                execution=execution,
                thread_id=reference.thread_id,
                request_options={"max_retries": 0},
            )
        result = await self.backend.studies_executions.get_execution_by_id(
            accepted.id, request_options={"max_retries": 0}
        )
        if result.id != accepted.id or result.definition_id != reference.study_id:
            raise ValueError("Backend execution does not match the saved study")
        return ChosenExecution(
            execution=result,
            reusable_study=SavedStudy(
                study_id=reference.study_id,
                source_execution_id=result.id,
                thread_id=reference.thread_id,
            ),
        )
