"""Five MCP operations over the same public EpochClient used by SDK callers."""

from __future__ import annotations

import asyncio
import inspect
import os
from typing import Literal

from mcp.server import MCPServer
from mcp.server.context import CallNext, HandlerResult, ServerRequestContext
from mcp.server.mcpserver import Context
from mcp.types import CallToolResult, ListToolsResult, TextContent
from stratifyx import DatePeriodConfig, ExecutionOptions

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
    Answers,
    ChosenExecution,
    InProgress,
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
    elif isinstance(value, ChosenExecution) and value.response is not None:
        wire["response"] = value.response.to_wire()
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
                extra = supplied.keys() - arguments[name]
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
        responses: dict[str, Answers],
        ctx: Context[object, object],
    ) -> CallToolResult:
        """Answer the current questions and continue the same operation to its answer.
        Copy interrupt IDs and zero-based question/option indices from needs_input.
        Explicit user/agent answers are required; recommendations are never selected.
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
        response_id: str,
        table: str | None = None,
        version: int | None = None,
        offset: int = 0,
        page_size: int = 1000,
    ) -> CallToolResult:
        """Read a saved answer, or one table page when table is supplied.
        Pin the returned version for subsequent pages and follow next_offset until
        null. Page size limits one transfer; there is no total table row ceiling.
        Reads call Backend only and never start a study or model call.
        """
        try:
            return _value(
                await epoch.read(
                    response_id,
                    table=table,
                    version=version,
                    offset=offset,
                    page_size=page_size,
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
