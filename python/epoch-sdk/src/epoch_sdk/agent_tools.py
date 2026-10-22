"""Composable Epoch capabilities for an external coding-agent supervisor.

Graph specialists run only when explicitly selected. Execution and persisted
reads use the generated Backend client directly; no response is published.
"""

from __future__ import annotations

import json
from typing import Literal, Protocol, TypedDict, cast
from uuid import uuid4

import httpx
from jsonschema import Draft202012Validator
from langgraph_sdk.client import LangGraphClient
from langgraph_sdk.schema import Command, Run, RunStatus, StreamMode
from pydantic import BaseModel, ConfigDict, Field, JsonValue
from stratifyx import AsyncStratifyX, DatePeriodConfig, ExecutionOptions
from stratifyx.types import DashboardSchema, JobListItem, StudyDefinition, TearSheetMetadataResponse

from .agent_tools_contract import (
    MAX_TOOL_ARGUMENT_BYTES,
    TOOLS_ASSISTANT_ID,
    AgentToolHandle,
    AgentToolName,
    AgentToolsCatalog,
    ToolContract,
    ToolWorkspace,
)
from .datasets import DatasetClient
from .json_schema import validate_schema
from .supervisor import (
    Answers,
    GraphInterrupt,
    NeedsInput,
    SupervisorClient,
    WorkflowHandle,
    api_url,
)


class _ToolRunMetadata(TypedDict):
    epoch_tool_call_id: str
    epoch_tool_name: AgentToolName


class _ExternalTaskMessage(TypedDict):
    role: Literal["user"]
    id: str
    content: str


class _SelectedToolCall(TypedDict):
    id: str
    name: AgentToolName
    # Parameter keys are supplied by the source-owned runtime tool schema.
    args: dict[str, JsonValue]
    type: Literal["tool_call"]


class _SelectedToolMessage(TypedDict):
    role: Literal["assistant"]
    id: str
    content: Literal[""]
    tool_calls: list[_SelectedToolCall]


class _ToolGraphInput(TypedDict):
    messages: list[_ExternalTaskMessage | _SelectedToolMessage]


class _ExecutionOverrides(TypedDict, total=False):
    execution: ExecutionOptions
    execution_id: str
    thread_id: str


class _JsonValidator(Protocol):
    def validate(self, instance: JsonValue) -> None: ...


class _ToolRuns(Protocol):
    # The installed native implementation accepts durability for create(), but
    # its overload declarations omit it. Keep this verified transport seam
    # narrow; the returned Run remains the SDK's own closed type.
    async def create(
        self,
        thread_id: str,
        assistant_id: str,
        *,
        input: _ToolGraphInput | None = None,
        command: Command | None = None,
        metadata: _ToolRunMetadata,
        durability: Literal["sync"],
        multitask_strategy: Literal["reject"],
        on_completion: Literal["keep"],
        stream_mode: list[StreamMode] | None = None,
        stream_subgraphs: bool = False,
        stream_resumable: bool = False,
    ) -> Run: ...


class AgentToolOperation(ToolContract):
    status: Literal["in_progress", "completed", "failed", "needs_input"]
    handle: AgentToolHandle
    native_status: RunStatus
    output: JsonValue = None
    tool_status: Literal["success", "error"] | None = None
    interrupts: list[GraphInterrupt] = Field(default_factory=list[GraphInterrupt])
    workspace: ToolWorkspace | None = None
    artifact: JsonValue = None


class _ToolMessage(BaseModel):
    model_config = ConfigDict(extra="ignore", strict=True)
    tool_call_id: str | None = None
    # These are native LangChain content/artifact envelopes, owned by the
    # registered tool. They are transported/displayed, never parsed for facts.
    content: JsonValue = None
    artifact: JsonValue = None
    status: Literal["success", "error"] = "success"


class _WorkspaceState(BaseModel):
    model_config = ConfigDict(extra="ignore", strict=True)
    messages: list[_ToolMessage] = Field(default_factory=list[_ToolMessage])
    study_name_to_id: dict[str, str] = Field(default_factory=dict)
    run_name_to_id: dict[str, str] = Field(default_factory=dict)

    def view(self, identifier: str) -> ToolWorkspace:
        return ToolWorkspace(
            workspace_id=identifier, studies=self.study_name_to_id, executions=self.run_name_to_id
        )


class AgentToolsClient(DatasetClient):
    def __init__(
        self, graph: LangGraphClient, backend: AsyncStratifyX, graph_http: httpx.AsyncClient
    ):
        self.graph = graph
        self.backend = backend
        self.graph_http = graph_http
        self._catalog: AgentToolsCatalog | None = None
        self._owned_http: list[httpx.AsyncClient] = []

    @classmethod
    def connect(cls, *, graph_url: str, backend_url: str, token: str) -> AgentToolsClient:
        graph_http = httpx.AsyncClient(
            base_url=api_url(graph_url), headers={"Authorization": f"Bearer {token}"}, timeout=30.0
        )
        backend_http = httpx.AsyncClient(timeout=30.0)
        client = cls(
            LangGraphClient(graph_http),
            AsyncStratifyX(base_url=api_url(backend_url), token=token, httpx_client=backend_http),
            graph_http,
        )
        client._owned_http = [graph_http, backend_http]
        return client

    async def aclose(self) -> None:
        for client in self._owned_http:
            await client.aclose()

    async def catalog(self) -> AgentToolsCatalog:
        if self._catalog is None:
            response = await self.graph_http.get("/api/v1/agent-tools")
            response.raise_for_status()
            catalog = AgentToolsCatalog.model_validate_json(response.content)
            for tool in catalog.tools:
                validate_schema(tool.parameters)
            self._catalog = catalog
        return self._catalog

    async def _workspace(self, identifier: str) -> None:
        thread = await self.graph.threads.get(identifier)
        if (thread.get("metadata") or {}).get("epoch_tool_workspace") != "v1":
            raise ValueError("Select an Epoch tools workspace, not a supervisor conversation")

    async def invoke(
        self,
        tool: AgentToolName,
        arguments: dict[str, JsonValue],
        *,
        task: str,
        workspace_id: str | None = None,
    ) -> AgentToolOperation:
        if not task.strip():
            raise ValueError("The external task must not be blank")
        definition = next((row for row in (await self.catalog()).tools if row.name == tool), None)
        if definition is None:
            raise ValueError("Unknown Epoch specialist tool")
        cast(_JsonValidator, Draft202012Validator(definition.parameters)).validate(arguments)
        if (
            len(json.dumps(arguments, ensure_ascii=False, allow_nan=False).encode())
            > MAX_TOOL_ARGUMENT_BYTES
        ):
            raise ValueError("Tool arguments exceed 128 KiB; pass saved references")
        if workspace_id is None:
            thread = await self.graph.threads.create(metadata={"epoch_tool_workspace": "v1"})
            workspace_id = thread["thread_id"]
        else:
            await self._workspace(workspace_id)
        call_id, request_id = str(uuid4()), str(uuid4())
        run = await cast(_ToolRuns, self.graph.runs).create(
            workspace_id,
            TOOLS_ASSISTANT_ID,
            input={
                "messages": [
                    {"role": "user", "id": request_id, "content": task},
                    {
                        "role": "assistant",
                        "id": "tool-request:" + call_id,
                        "content": "",
                        "tool_calls": [
                            {"id": call_id, "name": tool, "args": arguments, "type": "tool_call"},
                        ],
                    },
                ]
            },
            durability="sync",
            multitask_strategy="reject",
            on_completion="keep",
            metadata={"epoch_tool_call_id": call_id, "epoch_tool_name": tool},
            stream_mode=["values", "custom"],
            stream_subgraphs=True,
            stream_resumable=True,
        )
        return AgentToolOperation(
            status="in_progress",
            native_status=run["status"],
            handle=AgentToolHandle(
                workspace_id=workspace_id, run_id=run["run_id"], tool_call_id=call_id, tool=tool
            ),
        )

    async def status(
        self, handle: AgentToolHandle, *, include_artifact: bool = False
    ) -> AgentToolOperation:
        await self._workspace(handle.workspace_id)
        run = await self.graph.runs.get(handle.workspace_id, handle.run_id)
        metadata = run.get("metadata") or {}
        if (
            metadata.get("epoch_tool_call_id") != handle.tool_call_id
            or metadata.get("epoch_tool_name") != handle.tool
        ):
            raise ValueError("The handle differs from its native tool operation")
        native = run["status"]
        if native in {"pending", "running"}:
            return AgentToolOperation(status="in_progress", native_status=native, handle=handle)
        if native == "interrupted":
            # Thread state is the latest checkpoint, not a run-scoped read.
            # A reused workspace or resumed continuation must not lend its
            # current questions to an older operation handle.
            latest = await self.graph.runs.list(handle.workspace_id, limit=1)
            if not latest or latest[0]["run_id"] != handle.run_id:
                raise ValueError(
                    "This interrupted handle is stale; the workspace has advanced. "
                    "Use the current operation or continuation handle."
                )
        snapshot = await self.graph.threads.get_state(handle.workspace_id)
        state = _WorkspaceState.model_validate(snapshot["values"] or {})
        interrupts = [GraphInterrupt.model_validate(row) for row in snapshot["interrupts"]]
        if native == "interrupted" and interrupts:
            return AgentToolOperation(
                status="needs_input", native_status=native, handle=handle, interrupts=interrupts
            )
        result = next(
            (row for row in state.messages if row.tool_call_id == handle.tool_call_id), None
        )
        if native != "success" or result is None:
            return AgentToolOperation(
                status="failed",
                native_status=native,
                handle=handle,
                workspace=state.view(handle.workspace_id),
            )
        return AgentToolOperation(
            status="completed" if result.status == "success" else "failed",
            native_status=native,
            handle=handle,
            output=result.content,
            tool_status=result.status,
            artifact=result.artifact if include_artifact else None,
            workspace=state.view(handle.workspace_id),
        )

    async def resume(
        self, handle: AgentToolHandle, responses: dict[str, Answers]
    ) -> AgentToolOperation:
        waiting = await self.status(handle)
        if waiting.status != "needs_input":
            raise ValueError("This tool operation is not waiting for input")
        native = NeedsInput(
            handle=WorkflowHandle(
                thread_id=handle.workspace_id,
                request_id=handle.tool_call_id,
                assistant_id=TOOLS_ASSISTANT_ID,
                run_id=handle.run_id,
            ),
            interrupts=waiting.interrupts,
        )
        command = SupervisorClient.resume_command(native, responses)
        run = await cast(_ToolRuns, self.graph.runs).create(
            handle.workspace_id,
            TOOLS_ASSISTANT_ID,
            command=command,
            durability="sync",
            multitask_strategy="reject",
            on_completion="keep",
            metadata={"epoch_tool_call_id": handle.tool_call_id, "epoch_tool_name": handle.tool},
        )
        return AgentToolOperation(
            status="in_progress",
            native_status=run["status"],
            handle=handle.model_copy(update={"run_id": run["run_id"]}),
        )

    async def workspace(self, workspace_id: str) -> ToolWorkspace:
        await self._workspace(workspace_id)
        snapshot = await self.graph.threads.get_state(workspace_id)
        return _WorkspaceState.model_validate(snapshot["values"] or {}).view(workspace_id)

    async def find(
        self,
        *,
        kind: Literal["workspaces", "studies", "executions"],
        limit: int = 20,
        offset: int = 0,
    ) -> list[str]:
        if not 1 <= limit <= 100 or offset < 0:
            raise ValueError("Use a limit of 1–100 and a nonnegative offset")
        if kind == "studies":
            ids = await self.backend.studies_definitions.list_study_definitions(
                request_options={"max_retries": 0}
            )
            return ids[offset : offset + limit]
        if kind == "executions":
            ids = await self.backend.studies_executions.list_executions(
                request_options={"max_retries": 0}
            )
            return ids[offset : offset + limit]
        threads = await self.graph.threads.search(
            metadata={"epoch_tool_workspace": "v1"},
            limit=limit,
            offset=offset,
            # The service's owner response filter needs metadata even though
            # this public method returns IDs only.
            select=["thread_id", "metadata"],
        )
        return [thread["thread_id"] for thread in threads]

    async def study(self, study_id: str) -> StudyDefinition:
        return await self.backend.studies_definitions.get_a_study_definition_by_id(
            study_id, request_options={"max_retries": 0}
        )

    async def execution(self, execution_id: str) -> JobListItem:
        snapshot = await self.backend.studies_executions.get_the_per_execution_study_snapshot_as_run_source_assets_screen(
            execution_id, request_options={"max_retries": 0}
        )
        job = await self.backend.studies_executions.get_execution_by_id(
            execution_id, request_options={"max_retries": 0}
        )
        if (
            snapshot.execution_id != execution_id
            or job.id != execution_id
            or job.definition_id != snapshot.definition_id
        ):
            raise ValueError("The execution differs from its owned snapshot")
        return job

    async def dashboard(self, execution_id: str, *, category: str = "ALL") -> DashboardSchema:
        """Read native dashboard values without involving an analysis model."""
        await self.execution(execution_id)
        return await self.backend.studies_dashboard.get_dashboard_schema_chart_specs_table_specs_card_values(
            execution_id, category=category, request_options={"max_retries": 0}
        )

    async def dashboard_metadata(self, execution_id: str) -> TearSheetMetadataResponse:
        await self.execution(execution_id)
        return await self.backend.studies_performance.get_performance_metadata(
            execution_id, request_options={"max_retries": 0}
        )

    async def execute(
        self,
        study_id: str,
        *,
        period: DatePeriodConfig,
        execution: ExecutionOptions | None = None,
        execution_id: str | None = None,
        workspace_id: str | None = None,
    ) -> JobListItem:
        if workspace_id is not None:
            await self._workspace(workspace_id)
        await self.study(study_id)
        # This is the maintained native execution API, not saved-answer replay.
        # Backend owns execution_id validation/deduplication; there is no retry.
        options: _ExecutionOverrides = {}
        if execution is not None:
            options["execution"] = execution
        if execution_id is not None:
            options["execution_id"] = execution_id
        if workspace_id is not None:
            options["thread_id"] = workspace_id
        accepted = await self.backend.studies_executions.start_execute_a_study(
            id=study_id, period=period, **options, request_options={"max_retries": 0}
        )
        job = await self.execution(accepted.id)
        if job.definition_id != study_id:
            raise ValueError("Backend executed a different study")
        return job
