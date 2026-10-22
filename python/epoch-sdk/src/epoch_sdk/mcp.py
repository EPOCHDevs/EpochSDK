"""Composable Epoch tools: the calling coding agent is the supervisor."""

from __future__ import annotations

import asyncio
import inspect
import os
from collections.abc import Awaitable
from copy import deepcopy
from importlib.resources import files
from typing import Annotated, Literal, cast

import httpx
from jsonschema.exceptions import ValidationError as SchemaValidationError
from mcp.server import MCPServer
from mcp.server.context import CallNext, HandlerResult, ServerRequestContext
from mcp.shared.exceptions import MCPError
from mcp.types import CallToolResult, ListToolsResult, TextContent, Tool
from pydantic import BaseModel, Field, JsonValue, ValidationError
from stratifyx import DatePeriodConfig, ExecutionOptions
from stratifyx.core.api_error import ApiError
from stratifyx.types import DatasetSearchQuery, ScreenAssetsRequest
from stratifyx.types.error_response import ErrorResponse as NativeErrorResponse

from .agent_tools import AgentToolsClient
from .agent_tools_contract import MCP_TOOL_NAMES, AgentToolHandle
from .supervisor import Answers

# Old handles remain readable through AgentToolsClient. New MCP discovery is
# native Backend lookup; the legacy Discovery LLM is never advertised/invoked.
_SPECIALIST_NAMES = {name: public for name, public in MCP_TOOL_NAMES.items() if name != "discovery"}


def _value(value: BaseModel) -> CallToolResult:
    return CallToolResult(
        content=[TextContent(type="text", text=value.model_dump_json(by_alias=True, exclude_unset=True))],
        structured_content=value.model_dump(mode="json", by_alias=True, exclude_unset=True),
    )


def _failure(message: str) -> CallToolResult:
    return CallToolResult(is_error=True, content=[TextContent(type="text", text=message)])


async def _call(operation: Awaitable[BaseModel]) -> CallToolResult:
    try:
        return _value(await operation)
    except SchemaValidationError as error:
        return _failure("Invalid tool input: " + error.message)
    except (ValueError, ValidationError) as error:
        return _failure(str(error))
    except ApiError as error:
        try:
            native = NativeErrorResponse.model_validate(error.body, strict=True)
        except ValidationError:
            return _failure(
                f"Backend returned HTTP {error.status_code} without a valid native error response."
            )
        # Preserve the native cause through MCP, using only the source-owned
        # error contract. Headers and arbitrary error-body extras stay private.
        payload = native.model_dump(
            mode="json", by_alias=True,
            include={"error", "message", "timestamp", "additional_context"},
            exclude_none=True,
        )
        return CallToolResult(
            is_error=True,
            content=[TextContent(
                type="text", text=f"Backend returned HTTP {error.status_code}: {native.message}"
            )],
            structured_content={"http_status": error.status_code, "backend_error": payload},
        )
    except httpx.HTTPStatusError as error:
        return _failure(f"Epoch tools service returned HTTP {error.response.status_code}.")
    except httpx.HTTPError:
        return _failure(
            "The Epoch service could not be reached; retain any accepted handle before reconnecting."
        )


def create_server(client: AgentToolsClient) -> MCPServer:
    arguments: dict[str, set[str]] = {}

    async def dispatch(
        ctx: ServerRequestContext[object, object], call_next: CallNext
    ) -> HandlerResult:
        name = ctx.params.get("name") if ctx.params is not None else None
        if ctx.method == "tools/list" or (
            ctx.method == "tools/call" and name in _SPECIALIST_NAMES.values()
        ):
            catalog = await client.catalog()
        elif ctx.method == "tools/call":
            catalog = None
        else:
            return await call_next(ctx)
        if ctx.method == "tools/call" and ctx.params is not None:
            name, supplied = ctx.params.get("name"), ctx.params.get("arguments", {})
            if not isinstance(supplied, dict):
                raise ValueError("Tool arguments must be an object")
            for tool in catalog.tools if catalog is not None else []:
                if tool.name not in _SPECIALIST_NAMES:
                    continue
                if name != MCP_TOOL_NAMES[tool.name]:
                    continue
                values = dict(cast(dict[str, JsonValue], supplied))
                task = values.pop("task", None)
                workspace_id = values.pop("workspace_id", None)
                if not isinstance(task, str) or (
                    workspace_id is not None and not isinstance(workspace_id, str)
                ):
                    raise ValueError("Supply task and an optional workspace_id")
                return await _call(
                    client.invoke(
                        tool.name,
                        values,
                        task=task,
                        workspace_id=workspace_id,
                    )
                )
            if isinstance(name, str) and name in arguments:
                extra = cast(dict[str, JsonValue], supplied).keys() - arguments[name]
                if extra:
                    return CallToolResult(
                        is_error=True,
                        content=[
                            TextContent(
                                type="text", text="Unknown arguments: " + ", ".join(sorted(extra))
                            )
                        ],
                    )
        result = await call_next(ctx)
        if ctx.method == "tools/list" and result is not None:
            if catalog is None:
                raise ValueError("The specialist catalogue is unavailable")
            listing = ListToolsResult.model_validate(result)
            for tool in listing.tools:
                tool.input_schema["additionalProperties"] = False
            for definition in catalog.tools:
                if definition.name not in _SPECIALIST_NAMES:
                    continue
                schema = deepcopy(definition.parameters)
                properties, required = schema.get("properties", {}), schema.get("required", [])
                if not isinstance(properties, dict) or not isinstance(required, list):
                    raise TypeError("Invalid source-owned tool schema")
                if {"task", "workspace_id"} & properties.keys():
                    raise ValueError("A source tool conflicts with the MCP transport fields")
                schema["properties"] = {
                    **properties,
                    "task": {
                        "type": "string",
                        "minLength": 1,
                        "description": "The user's current task and approved context, retained as the source authority for this operation.",
                    },
                    "workspace_id": {
                        "anyOf": [{"type": "string"}, {"type": "null"}],
                        "description": "Reuse a returned tools workspace to retain discovery and study references across calls.",
                    },
                }
                schema["required"] = ["task", *required]
                schema["additionalProperties"] = False
                listing.tools.append(
                    Tool(
                        name=MCP_TOOL_NAMES[definition.name],
                        description=definition.description
                        + "\n"
                        + (
                            "Can use the existing specialist LLM; no Epoch supervisor is invoked. "
                            if definition.llm == "specialist"
                            else "Makes no LLM call. "
                        )
                        + "Returns a background-operation handle; use epoch_status. Publication is not required.",
                        input_schema=schema,
                    )
                )
            return listing
        return result

    async def checked_dispatch(
        ctx: ServerRequestContext[object, object], call_next: CallNext
    ) -> HandlerResult:
        try:
            return await dispatch(ctx, call_next)
        except (ValueError, ValidationError) as error:
            if ctx.method == "tools/list":
                raise MCPError(-32603, "The Epoch tools catalogue is invalid; check its service version.") from None
            return _failure(str(error))
        except httpx.HTTPStatusError as error:
            message = f"Epoch tools catalogue is unavailable (HTTP {error.response.status_code}). Deploy the epoch-tools graph before connecting this MCP."
            if ctx.method == "tools/list":
                raise MCPError(-32603, message) from None
            return _failure(message)

    server = MCPServer(
        "Epoch",
        instructions=(
            "Read epoch_read(kind=guide) for workflow guidance. You are the supervisor. Read epoch_dataset_catalog for datasets/options, epoch_search_dataset for identities, and epoch_screen_assets for whole cohorts. "
            "These data tools call Backend directly without a Discovery agent or generative LLM. Reuse exact source_refs across study builds. "
            "Do not launch epoch-ai or publish merely to finish; explain results directly. "
            "Specialist operations return handles; poll epoch_status rather than resubmitting. "
            "Execution and reads use Backend directly. Only explicitly selected study authoring and auditing use specialist LLMs."
        ),
        middleware=[checked_dispatch],
    )

    async def execute(
        study_id: str,
        period: DatePeriodConfig,
        execution: ExecutionOptions | None = None,
        execution_id: str | None = None,
        workspace_id: str | None = None,
    ) -> CallToolResult:
        """Execute a saved study through Backend, without a supervisor or publication.
        Returns the native execution ID/status. Observe with epoch_status using
        kind=execution; pass completed execution_ids to epoch_audit_run. Optional
        execution_id is Backend's caller-selected ID. Never retry an uncertain
        submission blindly: retain and read its accepted ID.
        """
        return await _call(
            client.execute(
                study_id,
                period=period,
                execution=execution,
                execution_id=execution_id,
                workspace_id=workspace_id,
            )
        )

    async def dataset_catalog(
        source_ids: list[str] | None = None,
        include_details: bool = False,
        include_saved: bool = True,
        saved_cursor: str | None = None,
        saved_limit: int = 100,
    ) -> CallToolResult:
        """Read Backend's dataset directory and shared source guidance, without an LLM.
        Request details for all supported loader options, including available
        vintage/revision selectors. Saved datasets are caller-owned. Metadata
        describes source capabilities; it does not prove access or data coverage.
        """
        return await _call(client.dataset_catalog(
            source_ids=source_ids or [], include_details=include_details,
            include_saved=include_saved, saved_cursor=saved_cursor, saved_limit=saved_limit,
        ))

    async def search_dataset(
        requests: list[DatasetSearchQuery], candidate_limit: int | None = None,
    ) -> CallToolResult:
        """Find assets/series by name, concept or exact native address through Backend.
        No Discovery agent or generative LLM is invoked. Reuse exact returned
        result_ref/record_ref in build_study source_refs; never invent identifiers.
        Result retains original search facts. If inline records were omitted,
        page contains the first saved page; continue with epoch_read(kind=dataset_search).
        This is ranked identity lookup; use epoch_screen_assets for a whole cohort.
        """
        return await _call(client.search_dataset(requests, candidate_limit=candidate_limit))

    async def screen_assets(request: ScreenAssetsRequest) -> CallToolResult:
        """Create or reuse a complete saved asset universe through Backend, without an LLM.
        Use explicit membership mode and a window for historical membership.
        No relevance limit is applied. Keep qualifications/integrity visible;
        pass universe_ref plus the desired dataset to build_study source_refs.
        A missing universe_ref means no usable complete universe was established.
        """
        return await _call(client.screen_assets(request))

    async def status(
        kind: Literal["tool", "execution"],
        handle: AgentToolHandle | None = None,
        execution_id: str | None = None,
    ) -> CallToolResult:
        """Observe existing work only. Tool operations require their complete handle;
        Backend executions require execution_id. No work is resubmitted or published.
        """
        if kind == "tool" and handle is not None and execution_id is None:
            return await _call(client.status(handle))
        if kind == "execution" and execution_id is not None and handle is None:
            return await _call(client.execution(execution_id))
        return _failure("Supply only the handle or execution_id required by kind")

    async def resume(handle: AgentToolHandle, responses: dict[str, Answers]) -> CallToolResult:
        """Explicitly answer pending specialist questions and continue that operation.
        Copy returned interrupt/question/option IDs. Recommendations are never
        selected automatically. Completed operations cannot be resumed.
        """
        if handle.tool == "discovery":
            return _failure(
                "Legacy Discovery handles are read-only in the default MCP. "
                "Use the explicit compatibility client to continue the original legacy operation."
            )
        return await _call(client.resume(handle, responses))

    async def read(
        kind: Literal[
            "workspace", "study", "execution", "tool", "dashboard", "dashboard_metadata", "guide",
            "dataset_search"
        ],
        identifier: str | None = None,
        handle: AgentToolHandle | None = None,
        category: str = "ALL",
        cursor: str | None = None,
        limit: Annotated[int, Field(ge=1, le=10, strict=True)] = 10,
    ) -> CallToolResult:
        """Read owned saved work without a model call or publication.
        Workspace returns study/execution registries; study returns the native
        definition; execution returns status. Tool reads require a handle and
        include the original saved artifact when available.
        Dataset-search pages contain 1..10 records and retain native cursors.
        """
        if kind == "guide":
            if identifier is not None or handle is not None:
                return _failure("Guide reads do not take an identifier or handle")
            guide = files("epoch_sdk").joinpath("data/agent-tools-guide.md").read_text()
            return CallToolResult(content=[TextContent(type="text", text=guide)])
        if kind == "tool" and handle is not None and identifier is None:
            return await _call(client.status(handle, include_artifact=True))
        if identifier is None or handle is not None:
            return _failure("Supply identifier, or a tool handle for kind=tool")
        if kind == "dataset_search":
            return await _call(client.read_dataset_search(identifier, cursor=cursor, limit=limit))
        if cursor is not None or limit != 10:
            return _failure("Cursor and limit apply only to dataset_search reads")
        if kind == "workspace":
            return await _call(client.workspace(identifier))
        if kind == "study":
            return await _call(client.study(identifier))
        if kind == "execution":
            return await _call(client.execution(identifier))
        if kind == "dashboard":
            return await _call(client.dashboard(identifier, category=category))
        if kind == "dashboard_metadata":
            return await _call(client.dashboard_metadata(identifier))
        return _failure("Tool reads require their handle")

    async def find(
        kind: Literal["workspaces", "studies", "executions"], limit: int = 20, offset: int = 0
    ) -> CallToolResult:
        """List owned reusable workspace or study IDs, paged by offset.
        Read selected IDs to inspect them. Listing makes no vendor/model call.
        """
        ids = await client.find(kind=kind, limit=limit, offset=offset)
        return CallToolResult(
            content=[TextContent(type="text", text="Saved IDs ready.")],
            structured_content={"kind": kind, "ids": ids, "offset": offset},
        )

    for name, function in (
        ("epoch_dataset_catalog", dataset_catalog),
        ("epoch_search_dataset", search_dataset),
        ("epoch_screen_assets", screen_assets),
        ("epoch_execute", execute),
        ("epoch_status", status),
        ("epoch_resume", resume),
        ("epoch_read", read),
        ("epoch_find", find),
    ):
        arguments[name] = set(inspect.signature(function).parameters)
        server.tool(name=name, structured_output=True)(function)
    return server


async def _stdio() -> None:
    client = AgentToolsClient.connect(
        graph_url=os.environ.get("EPOCH_MCP_GRAPH_URL") or os.environ["EPOCH_GRAPH_URL"],
        backend_url=os.environ["EPOCH_BACKEND_URL"],
        token=os.environ["EPOCH_TOKEN"],
    )
    try:
        await create_server(client).run_stdio_async()
    finally:
        await client.aclose()


def main() -> None:
    asyncio.run(_stdio())


if __name__ == "__main__":
    main()
