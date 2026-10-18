"""Thin MCP tools over the same stateful SDK adapter."""

from __future__ import annotations

import asyncio
import os

from mcp.server import MCPServer
from mcp.types import CallToolResult, TextContent

from .contracts import ErrorResponse, RunParameters
from .errors import EpochError
from .responses import ResearchResponseContent
from .saved_outputs import SavedOutputManifest
from .supervisor import (
    Answers,
    ChosenExecution,
    InProgress,
    NeedsInput,
    SavedStudy,
    SupervisorClient,
    SupervisorResult,
    WorkflowHandle,
)


def _result(value: SupervisorResult) -> CallToolResult:
    if isinstance(value, NeedsInput):
        text = value.feedback()
    elif isinstance(value, ChosenExecution):
        text = f"Selected Backend execution {value.execution.id}: {value.execution.status.value}."
        if value.reply:
            text += "\n" + value.reply
    elif isinstance(value, InProgress):
        text = "The supervisor is still running. Read epoch_status again using the same handle."
    else:
        text = value.reply or value.reason
    return CallToolResult(
        content=[TextContent(type="text", text=text)],
        structured_content=value.model_dump(mode="json", by_alias=True),
    )


def create_server(client: SupervisorClient) -> MCPServer:
    server = MCPServer("Epoch")

    async def run(task: str, thread_id: str | None = None) -> CallToolResult:
        """Communicate with Epoch's existing supervisor. A needs_input result retains
        the thread and contains questions; answer them with epoch_resume or open
        its conversation URL. Execution selection is not output certification.
        """
        return _result(await client.run(task, thread_id=thread_id))

    async def resume(waiting: NeedsInput, responses: dict[str, Answers]) -> CallToolResult:
        """Answer pending interrupts and continue the same checkpointed task.
        Use interrupt ids and zero-based question/option indices from needs_input.
        Recommendations are advice; this tool never selects answers automatically.
        """
        return _result(await client.resume(waiting, responses))

    async def execute_saved(reference: SavedStudy, parameters: RunParameters) -> CallToolResult:
        """Execute a saved immutable study directly through Backend using an explicit
        period and optional execution overrides. Makes no discovery or supervisor call.
        The returned engine status may still be queued or running.
        """
        if parameters.period is None:
            raise ValueError("Provide parameters.period for the saved-study execution")
        return _result(
            await client.execute_saved(
                reference, period=parameters.period, execution=parameters.execution
            )
        )

    async def status(handle: WorkflowHandle) -> CallToolResult:
        """Read the same request after it continues in Epoch's UI. Starts no graph run
        and never resubmits the task. Returns pending questions or the current result.
        """
        return _result(await client.status(handle))

    async def outputs(manifest: SavedOutputManifest) -> CallToolResult:
        """Read complete bounded saved outputs through Backend and validate their
        actual values. Supply the saved receipt from the workflow/Backend owner;
        binding publication is still being integrated. Do not guess bindings from
        presentation titles. This starts no agent/job and does not certify research.
        """
        try:
            result = await client.outputs(manifest)
        except EpochError as error:
            response = ErrorResponse(error=error.error, execution_id=manifest.execution_id)
            return CallToolResult(
                content=[TextContent(type="text", text=str(error))],
                structured_content=response.to_wire(),
            )
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"Validated {len(result.outputs)} saved outputs for execution {result.execution_id}.",
                )
            ],
            structured_content=result.to_wire(),
        )

    server.tool(name="epoch_run", structured_output=True)(run)
    server.tool(name="epoch_resume", structured_output=True)(resume)
    server.tool(name="epoch_execute_saved", structured_output=True)(execute_saved)
    server.tool(name="epoch_status", structured_output=True)(status)
    server.tool(name="epoch_outputs", structured_output=True)(outputs)

    async def response(response_id: str, version: int | None = None) -> CallToolResult:
        """Read a published answer by its own identity and optional immutable revision."""
        try:
            saved = await client.response(response_id, version=version)
        except EpochError as error:
            return CallToolResult(
                content=[TextContent(type="text", text=str(error))],
                structured_content=ErrorResponse(error=error.error).to_wire(),
            )
        return CallToolResult(
            content=[TextContent(type="text", text="Answer ready.")],
            structured_content=saved.to_wire(),
        )

    async def publish(
        request_id: str,
        thread_id: str,
        content: ResearchResponseContent,
        primary_execution_id: str | None = None,
        expected_version: int = 0,
    ) -> CallToolResult:
        """Publish one answer for this query. Different queries may use the same run.
        Values must be complete. Edits retain the original query/thread and use
        its expected revision; no new agent or engine work is started.
        """
        try:
            saved = await client.publish_response(
                request_id,
                content,
                thread_id=thread_id,
                primary_execution_id=primary_execution_id,
                expected_version=expected_version,
            )
        except EpochError as error:
            return CallToolResult(
                content=[TextContent(type="text", text=str(error))],
                structured_content=ErrorResponse(error=error.error).to_wire(),
            )
        return CallToolResult(
            content=[TextContent(type="text", text="Answer ready.")],
            structured_content=saved.to_wire(),
        )

    server.tool(name="epoch_response", structured_output=True)(response)
    server.tool(name="epoch_publish_response", structured_output=True)(publish)
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
