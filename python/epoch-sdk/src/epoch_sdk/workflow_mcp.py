"""Five MCP operations over the same public EpochClient used by SDK callers."""

from __future__ import annotations

import asyncio
import inspect
import os
from collections.abc import Mapping
from typing import Literal, cast
from urllib.parse import quote

import httpx
from mcp.server import MCPServer
from mcp.server.context import CallNext, HandlerResult, ServerRequestContext
from mcp.server.mcpserver import Context
from mcp.shared.exceptions import MCPError
from mcp.types import CallToolResult, ListToolsResult, ResourceLink, TextContent
from pydantic import JsonValue
from stratifyx import DatePeriodConfig, ExecutionOptions
from stratifyx.core.api_error import ApiError

from .contracts import ErrorResponse, OutputRequest, RunParameters
from .errors import EpochError
from .research import (
    EpochClient,
    ExecutionAccepted,
    ResearchAccepted,
    ResearchCompleted,
    ResearchError,
    ResearchResult,
)
from .responses import ResponseTablePage, SavedResearchResponse
from .session import EventHandler, SessionCompleted, SessionEvent, SessionQuestions
from .supervisor import (
    ChosenExecution,
    InProgress,
    InterruptResponse,
    NeedsInput,
    NoExecution,
    PublishedAnswer,
    SavedStudy,
    SupervisorClient,
    SupervisorResult,
)


def _result(value: SupervisorResult) -> CallToolResult:
    if isinstance(value, NeedsInput):
        text = value.feedback()
    elif isinstance(value, ChosenExecution):
        text = (
            "Answer ready."
            if value.response is not None
            else f"Execution is {value.execution.status.value}."
        )
    elif isinstance(value, PublishedAnswer):
        text = "Answer ready."
    elif isinstance(value, InProgress):
        text = "Still running. Reconnect with epoch_status using the same operation ID."
    else:
        text = value.reply or value.reason
    wire = value.model_dump(mode="json", by_alias=True)
    if isinstance(value, PublishedAnswer):
        wire["response"] = value.response.to_wire()
    elif isinstance(value, ChosenExecution):
        response = value.response
        if response is not None:
            wire["response"] = response.to_wire()
    elif isinstance(value, NoExecution) and value.publication_error is not None:
        wire["publication_error"] = value.publication_error.to_wire()
    return CallToolResult(content=[TextContent(type="text", text=text)], structured_content=wire)


def _value(
    value: ResearchResult
    | ChosenExecution
    | ExecutionAccepted
    | SavedResearchResponse
    | ResponseTablePage,
) -> CallToolResult:
    if isinstance(value, ResearchCompleted):
        text = "Answer ready."
    elif isinstance(value, ResearchAccepted):
        text = "Research accepted. Read epoch_status with kind=run and the same operation ID."
    elif isinstance(value, ExecutionAccepted):
        text = "Execution accepted. Read epoch_status with kind=execute and the same operation ID."
    elif isinstance(value, ResponseTablePage):
        text = "Table page ready. Follow next_offset using this version until it is null."
    elif isinstance(value, SavedResearchResponse):
        text = "Answer ready."
    else:
        return _result(value)
    return CallToolResult(
        content=[TextContent(type="text", text=text)],
        structured_content=value.to_wire(),
    )


def _error(error: EpochError) -> CallToolResult:
    response = (
        error.response
        if isinstance(error, ResearchError)
        else ErrorResponse(
            error=error.error,
            **({"execution_id": error.execution_id} if error.execution_id else {}),
        )
    )
    return CallToolResult(
        content=[TextContent(type="text", text=str(error))],
        structured_content=response.to_wire(),
    )


def create_server(client: SupervisorClient | EpochClient) -> MCPServer:
    arguments: dict[str, set[str]] = {}

    async def closed_arguments(
        ctx: ServerRequestContext[object, object], call_next: CallNext
    ) -> HandlerResult:
        # MCP's function argument models otherwise silently discard extra keys.
        if ctx.method == "tools/call" and ctx.params is not None:
            name = ctx.params.get("name")
            supplied = ctx.params.get("arguments")
            if isinstance(name, str) and name in arguments and isinstance(supplied, dict):
                extra = cast(dict[str, JsonValue], supplied).keys() - arguments[name]
                if extra:
                    return CallToolResult(
                        is_error=True,
                        content=[
                            TextContent(
                                type="text",
                                text="Unknown arguments: " + ", ".join(sorted(extra)),
                            )
                        ],
                    )
        result = await call_next(ctx)
        if ctx.method == "tools/list" and result is not None:
            result = ListToolsResult.model_validate(result)
            for tool in result.tools:
                tool.input_schema["additionalProperties"] = False
        return result

    server = MCPServer("Epoch", middleware=[closed_arguments])
    epoch = client if isinstance(client, EpochClient) else EpochClient(client)

    def draft_identity(draft_ref: str, digest: str) -> None:
        if not draft_ref.startswith("draft:") or len(draft_ref) > 256:
            raise ValueError("Use the exact retained draft_ref from the review")
        if len(digest) != 64 or any(char not in "0123456789abcdef" for char in digest):
            raise ValueError("Use the exact draft descriptor content_sha256 from the review")

    async def draft_bytes(
        draft_ref: str, digest: str, output_format: Literal["json", "table"]
    ) -> bytes:
        try:
            draft_identity(draft_ref, digest)
            preview = await epoch.preview_dataset(draft_ref, limit=1)
            if preview.content.format != output_format:
                raise ValueError("The draft resource has a different content format")
            return await epoch.download_dataset(draft_ref, expected_sha256=digest)
        except (ApiError, httpx.HTTPError, ValueError):
            raise MCPError(
                -32001,
                "This draft content could not be authorized or verified. Reopen its exact review.",
            ) from None

    @server.resource(
        "epoch://review-json/{draft_ref}/{digest}",
        mime_type="application/json",
        description="Complete owner-checked retained JSON/text/scalar draft, pinned to its content digest.",
    )
    async def draft_json(draft_ref: str, digest: str) -> str:
        try:
            return (await draft_bytes(draft_ref, digest, "json")).decode("utf-8")
        except UnicodeError:
            raise MCPError(-32001, "The retained JSON draft is not valid UTF-8.") from None

    @server.resource(
        "epoch://review-arrow/{draft_ref}/{digest}",
        mime_type="application/vnd.apache.arrow.file",
        description="Complete owner-checked retained Arrow draft, pinned to its content digest.",
    )
    async def draft_arrow(draft_ref: str, digest: str) -> bytes:
        return await draft_bytes(draft_ref, digest, "table")

    def progress(context: Context[object, object]) -> EventHandler:
        count = 0

        async def update(event: SessionEvent) -> None:
            nonlocal count
            if isinstance(event, (SessionQuestions, SessionCompleted)):
                return  # Questions and the saved answer are the structured tool result.
            count += 1
            await context.report_progress(
                float(count), message=event.model_dump_json(exclude_none=True)
            )

        return update

    async def run(
        task: str,
        ctx: Context[object, object],
        context: list[str] | None = None,
        outputs: list[OutputRequest] | None = None,
        parameters: RunParameters | None = None,
        operation_id: str | None = None,
        thread_id: str | None = None,
        auto_ingest: bool = False,
    ) -> CallToolResult:
        """Submit a task through the shared SDK workflow and receive its saved answer.
        Context, output declarations and parameters are optional; the default answer
        is concise Markdown. Reuse operation_id with identical inputs to reconnect.
        Structured questions return without choosing an answer; use epoch_resume.
        Discovery, study building, validation and publication are handled by Epoch.
        """
        try:
            return _value(
                await epoch.run(
                    task,
                    context=context,
                    outputs=outputs,
                    parameters=parameters,
                    operation_id=operation_id,
                    thread_id=thread_id,
                    auto_ingest=auto_ingest,
                    interface="headless",
                    on_event=progress(ctx),
                )
            )
        except EpochError as error:
            return _error(error)

    async def execute(
        reference: SavedStudy | str,
        period: DatePeriodConfig,
        execution: ExecutionOptions | None = None,
        operation_id: str | None = None,
    ) -> CallToolResult:
        """Execute prepared work and wait for completion, without a supervisor.
        A verified response plan also publishes its saved answer before returning.
        Reference is the completed research operation ID or its returned reusable_study.
        Supply a separate operation_id to reconnect to this execution. A different
        period must be allowed by the saved plan. This does not rebuild the study.
        """
        try:
            return _value(
                await epoch.execute(
                    reference,
                    period=period,
                    execution=execution,
                    operation_id=operation_id,
                )
            )
        except EpochError as error:
            return _error(error)

    async def resume(
        operation_id: str,
        responses: Mapping[str, InterruptResponse],
        ctx: Context[object, object],
    ) -> CallToolResult:
        """Respond to current questions or dataset reviews in the same operation.
        Copy the exact interrupt IDs from needs_input. Questions use zero-based
        indices; dataset reviews use the displayed proposal/result identity and
        an explicit Build preview, Save, Edit or decline action. Native dataset
        decisions are confirmed before conversation delivery; retrying delivery
        never extracts or saves a second result. No choice is selected by default.
        """
        try:
            return _value(
                await epoch.resume(
                    operation_id,
                    responses,
                    interface="headless",
                    on_event=progress(ctx),
                )
            )
        except EpochError as error:
            return _error(error)

    async def status(
        operation_id: str,
        kind: Literal["run", "execute"] = "run",
    ) -> CallToolResult:
        """Read an existing operation's status, questions or pinned saved answer.
        Use kind=run for research and kind=execute for a prepared execution.
        This never submits work, resumes a question or starts a replacement job.
        """
        try:
            return _value(await epoch.status(operation_id, kind=kind))
        except EpochError as error:
            return _error(error)

    async def read(
        response_id: str | None = None,
        table: str | None = None,
        version: int | None = None,
        offset: int = 0,
        page_size: int | None = None,
        draft_ref: str | None = None,
        full_content: bool = False,
        expected_sha256: str | None = None,
    ) -> CallToolResult:
        """Read a saved answer/table or inspect a retained pending dataset draft.
        Pin the returned version for subsequent pages and follow next_offset until
        null. For a pending review, supply draft_ref instead of response_id. Draft
        pages use offset/page_size (default 100, maximum 100); follow next_cursor.
        full_content returns an exact JSON/Arrow resource link and requires the
        review draft descriptor's content_sha256 as expected_sha256. Read that
        resource to inspect all values, including JSON requires_download. Resource
        reads recheck native ownership and digest. Nothing is saved by reading.
        Reads call Backend only and never start a study or model call.
        """
        try:
            if (response_id is None) == (draft_ref is None):
                raise ValueError("Choose exactly one saved response_id or pending draft_ref")
            if draft_ref is not None:
                if table is not None or version is not None:
                    raise ValueError("Answer table/version settings do not apply to a draft")
                if not draft_ref.startswith("draft:") or len(draft_ref) > 256:
                    raise ValueError("Use the retained draft_ref from the dataset review")
                if full_content:
                    if expected_sha256 is None or offset != 0 or page_size is not None:
                        raise ValueError(
                            "Full draft content requires its exact content digest and no paging"
                        )
                    draft_identity(draft_ref, expected_sha256)
                    preview = await epoch.preview_dataset(draft_ref, limit=1)
                    is_json = preview.content.format == "json"
                    return CallToolResult(
                        content=[
                            ResourceLink(
                                name=draft_ref + (".json" if is_json else ".arrow"),
                                uri=("epoch://review-json/" if is_json else "epoch://review-arrow/")
                                + quote(draft_ref, safe="")
                                + "/"
                                + expected_sha256,
                                mime_type="application/json"
                                if is_json
                                else "application/vnd.apache.arrow.file",
                            )
                        ]
                    )
                if expected_sha256 is not None:
                    raise ValueError("The content digest applies to full_content resource reads")
                preview = await epoch.preview_dataset(
                    draft_ref, offset=offset, limit=100 if page_size is None else page_size
                )
                return CallToolResult(
                    content=[
                        TextContent(
                            type="text",
                            text="Retained draft preview; follow next_cursor for table continuation, or full_content for all JSON/Arrow bytes.",
                        )
                    ],
                    structured_content=preview.model_dump(
                        mode="json", by_alias=True, exclude_none=True
                    ),
                )
            if full_content or expected_sha256 is not None:
                raise ValueError("Draft content settings require draft_ref")
            assert response_id is not None
            return _value(
                await epoch.read(
                    response_id,
                    table=table,
                    version=version,
                    offset=offset,
                    page_size=1000 if page_size is None else page_size,
                )
            )
        except EpochError as error:
            return _error(error)

    for name, function in (
        ("epoch_run", run),
        ("epoch_execute", execute),
        ("epoch_resume", resume),
        ("epoch_status", status),
        ("epoch_read", read),
    ):
        arguments[name] = set(inspect.signature(function).parameters) - {"ctx"}
        server.tool(name=name, structured_output=True)(function)
    return server


async def _stdio() -> None:
    client = SupervisorClient.connect(
        graph_url=os.environ["EPOCH_GRAPH_URL"],
        backend_url=os.environ["EPOCH_BACKEND_URL"],
        token=os.environ["EPOCH_TOKEN"],
        assistant_id=os.environ.get("EPOCH_ASSISTANT_ID", "epoch-ai"),
        ui_url=os.environ.get("EPOCH_UI_URL"),
    )
    try:
        await create_server(client).run_stdio_async()
    finally:
        await client.aclose()


def main() -> None:
    asyncio.run(_stdio())


if __name__ == "__main__":
    main()
