"""Composable Epoch tools: the calling coding agent is the supervisor."""

from __future__ import annotations

import asyncio
import base64
import binascii
import inspect
import os
from collections.abc import Awaitable
from copy import deepcopy
from importlib.resources import files
from typing import Annotated, Literal, cast
from urllib.parse import quote, unquote

import httpx
from jsonschema.exceptions import SchemaError
from jsonschema.exceptions import ValidationError as SchemaValidationError
from mcp.server import MCPServer
from mcp.server.context import CallNext, HandlerResult, ServerRequestContext
from mcp.shared.exceptions import MCPError
from mcp.types import CallToolResult, ListToolsResult, ResourceLink, TextContent, Tool
from pydantic import BaseModel, ConfigDict, Field, JsonValue, ValidationError
from stratifyx import DatePeriodConfig, ExecutionOptions
from stratifyx.core.api_error import ApiError
from stratifyx.types import (
    CreateSdkExecutionRequest,
    DatasetCatalogResponse,
    DatasetReviewRequest,
    DatasetSearchQuery,
    DatasetSearchRequest,
    ExecutionPresentationPin,
    NamedExecutionInputSelection,
    ReferenceLibraryResponse,
    ScreenAssetsRequest,
    SdkExecutionRecord,
    SpaceResourceRef,
    StructuredImportRequest,
)
from stratifyx.types.error_response import ErrorResponse as NativeErrorResponse

from .agent_tools import AgentToolsClient
from .agent_tools_contract import MCP_TOOL_NAMES, AgentToolHandle
from .errors import EpochError
from .supervisor import Answers

# Old handles remain readable through AgentToolsClient. New MCP discovery is
# native Backend lookup; the legacy Discovery LLM is never advertised/invoked.
_SPECIALIST_NAMES = dict(MCP_TOOL_NAMES)

# Reuse the native request fields, including strictness and source-owned bounds.
# Plain int/bool annotations would coerce values before SDK validation sees them.
_CandidateLimit = Annotated[int | None, DatasetSearchRequest.model_fields["candidate_limit"]]


class _ExtensionExecutionRequest(CreateSdkExecutionRequest):
    """The native input shape is closed; read-side SDK extensions stay intact."""

    model_config = ConfigDict(extra="forbid")


def _value(value: BaseModel) -> CallToolResult:
    return CallToolResult(
        is_error=isinstance(value, SdkExecutionRecord) and value.error is not None,
        content=[TextContent(type="text", text=value.model_dump_json(by_alias=True, exclude_unset=True))],
        structured_content=value.model_dump(mode="json", by_alias=True, exclude_unset=True),
    )


def _failure(message: str) -> CallToolResult:
    return CallToolResult(is_error=True, content=[TextContent(type="text", text=message)])


def _compose_native_guide(
    workflow: str, catalog: DatasetCatalogResponse, library: ReferenceLibraryResponse
) -> str:
    """Present only coherent Backend guidance for tools this MCP mounts."""
    if catalog.loader_registry_version != library.version:
        raise ValueError("Backend dataset catalogue and planner reference versions differ")
    planning = library.planner_guidance

    def guide(name: str) -> str:
        content = planning.get(name) if planning is not None else None
        if not isinstance(content, str) or not content.strip():
            raise ValueError("Backend planner guidance is unavailable or incomplete")
        return content

    sections = [workflow, "<data>\n" + catalog.overview + "\n</data>"]
    sections.append("<compute>\n" + guide("compute") + "\n</compute>")
    sections.append("<epoch_execute>\n" + guide("run_study") + "\n</epoch_execute>")
    sections.append("<native_reports>\n" + guide("native_reports") + "\n</native_reports>")
    sections.append("<execution_cost_models>\n" + guide("cost_models") +
                    "\n</execution_cost_models>")
    return "\n\n".join(sections)


async def _call(operation: Awaitable[BaseModel | CallToolResult]) -> CallToolResult:
    try:
        value = await operation
        return value if isinstance(value, CallToolResult) else _value(value)
    except SchemaValidationError as error:
        return _failure("Invalid tool input: " + error.message)
    except (ValueError, ValidationError) as error:
        return _failure(str(error))
    except EpochError as error:
        return CallToolResult(
            is_error=True,
            content=[TextContent(type="text", text=error.error.message)],
            structured_content={"error": error.error.to_wire(), "execution_id": error.execution_id},
        )
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
            try:
                catalog = await client.catalog()
            except httpx.HTTPStatusError as error:
                raise MCPError(code=-32603, message=
                    f"Epoch tools catalog returned HTTP {error.response.status_code}; no tool list was substituted.") from None
            except httpx.HTTPError:
                raise MCPError(code=-32603, message=
                    "Epoch tools service is unreachable; the required tool catalog could not be loaded.") from None
            except (ValueError, SchemaError):
                raise MCPError(code=-32603, message=
                    "Epoch tools service returned an invalid tool catalog.") from None
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
            "Read epoch_read(kind=guide) for workflow guidance. You are the supervisor. The guide includes version-matched Backend dataset, compute, execution and cost guidance. Use epoch_search_dataset for identities or caller-owned saved datasets, and epoch_screen_assets for whole cohorts. "
            "These data tools call Backend directly without a Discovery agent or generative LLM. Reuse exact source_refs across study builds. "
            "Do not launch epoch-ai or publish merely to finish; explain results directly. "
            "Specialist operations return handles; poll epoch_status rather than resubmitting. "
            "Execution and reads use Backend directly. Specialist LLMs run only for explicitly selected study authoring or a program's declared llm_call."
            " For a supported completed result, use epoch_extension_inputs, epoch_save_extension and epoch_execute_extension to author/reuse an execution-input program. "
            "Its deterministic tables/JSON and native reporters need no inner LLM; only an explicit llm_call declaration may use the cached text model. "
            "Read exact answer or presentation pins from extension_outputs; source_execution_id is not the derived execution_id."
            " Files and Space persist independently of conversations. Use epoch_upload_file, epoch_prepare_dataset and epoch_review_datasets for imports. "
            "Use returned dataset_ref/source_ref exactly; knowledge datasets do not automatically become study sources. "
            "epoch_dataset_content returns a resource link to the complete prepared Arrow IPC file; read that resource when preview requires_download is true. "
            "Space folder and placement operations preserve existing resource references."
        ),
        middleware=[checked_dispatch],
    )

    @server.resource(
        "epoch://prepared-datasets/{dataset_ref}", name="prepared_dataset",
        description="Complete owner-authorized prepared Arrow IPC file, for an exact draft or saved dataset.",
        mime_type="application/vnd.apache.arrow.file",
    )
    async def prepared_dataset(dataset_ref: str) -> bytes:
        try:
            return await client.download_dataset(unquote(dataset_ref))
        except ApiError as error:
            try:
                native = NativeErrorResponse.model_validate(error.body, strict=True)
                message = native.message
            except ValidationError:
                message = "Prepared dataset is unavailable; verify its reference and ownership."
            raise MCPError(-32001, f"Backend returned HTTP {error.status_code}: {message}") from None
        except httpx.HTTPError:
            raise MCPError(-32001, "The prepared dataset service could not be reached.") from None

    async def upload_file(name: str, media_type: str, content_base64: str) -> CallToolResult:
        """Upload exact base64-encoded file bytes in verified native chunks.
        Backend owns content identity and safe replay. Files persist across chats.
        This transfers a file; preparation and explicit draft review are separate operations.
        """
        try:
            content = base64.b64decode(content_base64, validate=True)
        except (binascii.Error, ValueError):
            return _failure("content_base64 must be valid base64 file bytes")
        return await _call(client.upload_file(content, name=name, media_type=media_type))

    async def list_files(
        query: str | None = None, cursor: str | None = None,
        limit: Annotated[int, Field(strict=True, ge=1, le=1000)] = 100,
    ) -> CallToolResult:
        """Discover this owner's saved original files across conversations."""
        return await _call(client.list_files(query=query, cursor=cursor, limit=limit))

    async def inspect_file(file_ref: str, format: str) -> CallToolResult:
        """Inspect a structured file's sheets/record selections before preparing it."""
        return await _call(client.inspect_file(file_ref, format=format))

    async def prepare_dataset(request: StructuredImportRequest) -> CallToolResult:
        """Prepare an inspectable draft from an uploaded file, using deterministic readers.
        Retain request_id when retrying. Use purpose=study_source only with an explicit
        valid time mapping; knowledge data remains a useful saved dataset without source_ref.
        """
        return await _call(client.prepare_dataset(request))

    async def review_datasets(request: DatasetReviewRequest) -> CallToolResult:
        """Accept/name or reject each exact prepared draft; repeats do not publish duplicates."""
        return await _call(client.review_datasets(request))

    async def list_datasets(
        query: str | None = None, cursor: str | None = None,
        limit: Annotated[int, Field(strict=True, ge=1, le=100)] = 100,
    ) -> CallToolResult:
        """Find this owner's accepted datasets and exact eligible source references."""
        return await _call(client.list_datasets(query=query, cursor=cursor, limit=limit))

    async def preview_dataset(
        dataset_ref: str, offset: Annotated[int, Field(strict=True, ge=0)] = 0,
        limit: Annotated[int, Field(strict=True, ge=1, le=100)] = 100,
    ) -> CallToolResult:
        """Inspect an immutable draft/saved table. Follow next_cursor as an offset.
        If requires_download is true, read epoch_dataset_content's resource instead;
        no row values have been truncated and no zero-progress cursor is supplied.
        """
        return await _call(client.preview_dataset(dataset_ref, offset=offset, limit=limit))

    async def dataset_content(dataset_ref: str) -> CallToolResult:
        """Get a resource link for complete prepared data, beyond preview limits.
        Read the returned resource to fetch the owner-authorized Arrow IPC file.
        A link alone does not read the data or grant access to another owner.
        """
        return CallToolResult(content=[ResourceLink(
            name=dataset_ref + ".arrow",
            uri="epoch://prepared-datasets/" + quote(dataset_ref, safe=""),
            mime_type="application/vnd.apache.arrow.file",
        )])

    async def browse_space(
        folder_ref: str | None = None,
        recursive: Annotated[bool, Field(strict=True)] = False,
        query: str | None = None, cursor: str | None = None,
        limit: Annotated[int, Field(strict=True, ge=1, le=100)] = 100,
    ) -> CallToolResult:
        """Browse/search folders and explicitly placed resources in a selected hierarchy.
        Omit folder_ref for root. Null resource names mean obsolete/unavailable references.
        """
        return await _call(client.browse_space(
            folder_ref=folder_ref, recursive=recursive, query=query, cursor=cursor, limit=limit,
        ))

    async def create_folder(name: str, parent_folder_ref: str | None = None) -> CallToolResult:
        """Create a nested folder. Equal retries reuse the same sibling identity."""
        return await _call(client.create_folder(name, parent_folder_ref=parent_folder_ref))

    async def update_folder(
        folder_ref: str, name: str, parent_folder_ref: str | None = None,
    ) -> CallToolResult:
        """Rename/move a folder without changing its reference or descendants.
        Supply its current parent to rename in place; null parent moves it to root.
        """
        return await _call(client.update_folder(
            folder_ref, name=name, parent_folder_ref=parent_folder_ref,
        ))

    async def delete_folder(folder_ref: str) -> CallToolResult:
        """Delete an empty folder. Move/unplace contents first; resources remain saved."""
        async def remove() -> CallToolResult:
            await client.delete_folder(folder_ref)
            return CallToolResult(content=[TextContent(type="text", text="Empty folder deleted.")],
                                  structured_content={"folder_ref": folder_ref})
        return await _call(remove())

    async def place_resource(
        resource: SpaceResourceRef, folder_ref: str | None = None, name: str | None = None,
    ) -> CallToolResult:
        """Place/move an existing authorized file, dataset, model or study.
        Optional name is its Space display name. Resource/source references remain exact.
        """
        return await _call(client.place_resource(resource, folder_ref=folder_ref, name=name))

    async def unplace_resource(resource: SpaceResourceRef) -> CallToolResult:
        """Remove organization metadata only, including obsolete references."""
        return await _call(client.unplace_resource(resource))

    async def execute(
        study_id: str,
        period: DatePeriodConfig,
        execution: ExecutionOptions | None = None,
        execution_id: str | None = None,
        workspace_id: str | None = None,
    ) -> CallToolResult:
        """Execute a saved study through Backend, without a supervisor or publication.
        Returns the native execution ID/status. Observe with epoch_status using
        kind=execution. Use a native extension for new supported single-source
        calculations. Existing context answers source questions directly. Optional
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

    async def search_dataset(
        requests: list[DatasetSearchQuery], candidate_limit: _CandidateLimit = None,
        saved_query: str | None = None,
    ) -> CallToolResult:
        """Find assets/series by name, concept or exact native address through Backend.
        No Discovery agent or generative LLM is invoked. Reuse exact returned
        result_ref/record_ref in build_study source_refs; never invent identifiers.
        The first response contains ranked candidates per requested subject/product,
        with definitions and qualifications. Do not browse collected candidate
        pages. saved_query finds caller-owned datasets by name, description or
        exact returned dataset/source reference; use requests=[] for saved-only.
        This is ranked identity lookup; use epoch_screen_assets for a whole cohort.
        Preserve the returned asset class with each identity. Futures-root history
        bounds and their provenance describe the root, not one dated contract or
        every continuous construction. Root-coverage lookup does not require a
        continuous-construction choice.
        """
        return await _call(client.search_dataset(requests, candidate_limit=candidate_limit, saved_query=saved_query))

    async def screen_assets(request: ScreenAssetsRequest) -> CallToolResult:
        """Create or reuse a complete saved asset universe through Backend, without an LLM.
        Use explicit membership mode and a window for historical membership.
        No relevance limit is applied. Keep qualifications/integrity visible;
        pass universe_ref plus the desired dataset to build_study source_refs.
        A missing universe_ref means no usable complete universe was established.
        Listing location and company domicile are different filters. Current
        roster freshness does not establish historical identity, lineage or
        effective-date completeness.
        """
        return await _call(client.screen_assets(request))

    async def status(
        kind: Literal["tool", "execution", "extension"],
        handle: AgentToolHandle | None = None,
        execution_id: str | None = None,
        operation_id: str | None = None,
    ) -> CallToolResult:
        """Observe existing work only. Tool operations require their complete handle;
        Backend executions require execution_id; extensions require operation_id.
        Extension records separate native computation from saved output completion
        and retain exact publication/answer revisions. Check error/response_phase;
        outputs_recorded with extension_outputs confirms publication. Admission
        phase may remain active; kind=execution reads numerical job status.
        No work is resubmitted.
        """
        if kind == "tool" and handle is not None and execution_id is None and operation_id is None:
            return await _call(client.status(handle))
        if kind == "execution" and execution_id is not None and handle is None and operation_id is None:
            return await _call(client.execution(execution_id))
        if kind == "extension" and operation_id is not None and handle is None and execution_id is None:
            return await _call(client.extension_status(operation_id))
        return _failure("Supply only the handle, execution_id or operation_id required by kind")

    async def extension_inputs(
        execution_id: str, tables: list[str],
        additional_sources: list[NamedExecutionInputSelection] | None = None,
    ) -> CallToolResult:
        """Read selected retained tables' exact types, flat enum refs and frozen code.
        Backend owner-checks the completed source and rejects unsupported inputs.
        Pass tables=[] to discover native table names, then select an explicit
        subset when saving a program. This inspection does not bind every table.
        It reads metadata, without sample rows, vendor discovery or a model call. Reuse the
        source for multiple programs; do not embed its execution ID in EpochScript.
        """
        return await _call(client.extension_inputs(execution_id, tables=tables,
            additional_sources=additional_sources))

    async def save_extension(
        thread_id: str, source_execution_id: str, tables: list[str], source: str,
        name: str, description: str, parent_definition_id: str | None = None,
        additional_sources: list[NamedExecutionInputSelection] | None = None,
    ) -> CallToolResult:
        """Compile and save supplied EpochScript over an explicit execution_input.
        Use the returned catalog's flat ExecutionTable/field enum refs. Declare
        response_table/response_json and/or native reporters independently. Text
        uses an explicit llm_call result with response_text, Markdown or summary
        consumers. This saves an immutable definition, uses no authoring LLM and
        runs no study. Keep the returned ID.
        """
        return await _call(client.save_extension(
            thread_id,source_execution_id=source_execution_id,tables=tables,source=source,
            name=name,description=description,parent_definition_id=parent_definition_id,
            additional_sources=additional_sources,
        ))

    async def execute_extension(request: _ExtensionExecutionRequest) -> CallToolResult:
        """Start or attach one saved-execution extension through Backend.
        study_id is the saved extension, source_execution_id is the original owned
        result, input_tables selects its data and parameters may be empty. Supply
        additional_sources to select named completed runs for one comparison.
        Every source is retained in the output provenance. Reuse
        operation_id for identical accepted inputs; changed inputs conflict. It
        never reruns the original study or launches a supervisor. Only explicitly
        declared llm_call may call the bounded cached text model. Read epoch_status
        with kind=extension and operation_id for exact completed output pins.
        """
        return await _call(client.execute_extension(request))

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
            "response", "presentation"
        ],
        identifier: str | None = None,
        handle: AgentToolHandle | None = None,
        category: str = "ALL",
        version: Annotated[int, Field(ge=1, strict=True)] | None = None,
        table: str | None = None,
        offset: Annotated[int, Field(ge=0, strict=True)] = 0,
        page_size: Annotated[int, Field(ge=1, le=10000, strict=True)] = 1000,
        presentation: ExecutionPresentationPin | None = None,
    ) -> CallToolResult:
        """Read owned saved work without a model call or publication.
        Workspace returns study/execution registries; study returns the native
        definition; execution returns status. Tool reads require a handle and
        include the original saved artifact when available.
        Response reads accept a pinned version; table selects one paged named
        table using offset/page_size. Page size never caps the full result.
        Presentation reads require the exact publication/catalog/edit pin from
        extension_outputs; edit zero is a real version, not a latest lookup.
        """
        if kind == "presentation":
            if (presentation is None or identifier is not None or handle is not None
                    or version is not None
                    or table is not None or offset != 0 or page_size != 1000):
                return _failure("Presentation reads require only their exact pin and optional category")
            return await _call(client.extension_presentation(
                presentation, category=None if category == "ALL" else category,
            ))
        if presentation is not None:
            return _failure("Presentation pins apply only to presentation reads")
        if kind != "response" and (
            version is not None or table is not None or offset != 0 or page_size != 1000
        ):
            return _failure("Version, table, offset and page_size apply only to response reads")
        if kind == "guide":
            if identifier is not None or handle is not None:
                return _failure("Guide reads do not take an identifier or handle")
            guide = files("epoch_sdk").joinpath("data/agent-tools-guide.md").read_text()
            catalog = await _call(client.dataset_catalog(include_saved=False))
            if catalog.is_error:
                return catalog
            dataset_catalog = DatasetCatalogResponse.model_validate(catalog.structured_content)
            reference = await _call(client.backend.agents.get_the_agent_reference_library())
            if reference.is_error:
                return reference
            try:
                library = ReferenceLibraryResponse.model_validate(reference.structured_content)
            except ValidationError as error:
                return _failure("Backend planner reference is invalid: " + str(error))
            try:
                briefing = _compose_native_guide(guide, dataset_catalog, library)
            except ValueError as error:
                return _failure(str(error))
            return CallToolResult(content=[TextContent(type="text", text=briefing)])
        if kind == "tool" and handle is not None and identifier is None:
            return await _call(client.status(handle, include_artifact=True))
        if identifier is None or handle is not None:
            return _failure("Supply identifier, or a tool handle for kind=tool")
        if kind == "response":
            if table is not None:
                return await _call(client.response_table(identifier, table, version=version, offset=offset, page_size=page_size))
            if offset != 0 or page_size != 1000:
                return _failure("Response paging requires a table name")
            return await _call(client.response(identifier, version=version))
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
        ("epoch_upload_file", upload_file),
        ("epoch_list_files", list_files),
        ("epoch_inspect_file", inspect_file),
        ("epoch_prepare_dataset", prepare_dataset),
        ("epoch_review_datasets", review_datasets),
        ("epoch_list_datasets", list_datasets),
        ("epoch_preview_dataset", preview_dataset),
        ("epoch_dataset_content", dataset_content),
        ("epoch_space_browse", browse_space),
        ("epoch_space_create_folder", create_folder),
        ("epoch_space_update_folder", update_folder),
        ("epoch_space_delete_folder", delete_folder),
        ("epoch_space_place_resource", place_resource),
        ("epoch_space_unplace_resource", unplace_resource),
        ("epoch_search_dataset", search_dataset),
        ("epoch_screen_assets", screen_assets),
        ("epoch_execute", execute),
        ("epoch_extension_inputs", extension_inputs),
        ("epoch_save_extension", save_extension),
        ("epoch_execute_extension", execute_extension),
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
