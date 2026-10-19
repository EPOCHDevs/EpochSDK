"""Run a reviewed research case through the real SDK or MCP process.

Without --execute this validates and describes the case without opening a
connection. Receipts are local evidence, not a published research dataset.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import importlib.metadata
import json
import os
import sys
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal
from urllib.parse import urlsplit

import httpx
from epoch_sdk import EpochError, ErrorResponse, RunRequest
from epoch_sdk.output_validation import (
    Cell,
    JsonValueOutput,
    TableValue,
    TextValue,
    validate_outputs,
)
from epoch_sdk.parsing import parse_json
from epoch_sdk.research import (
    EpochClient,
    ResearchCompleted,
    ResearchError,
    ResearchFailure,
    ResearchResult,
)
from epoch_sdk.responses import (
    ResearchResponseContent,
    ResponseReference,
    ResponseTablePage,
    SavedResearchResponse,
)
from epoch_sdk.supervisor import Answers, ChosenExecution, InProgress, NeedsInput
from langgraph_sdk.client import LangGraphClient
from mcp import Client, StdioServerParameters
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    TypeAdapter,
    model_validator,
)
from stratifyx._release import SDK_RELEASE


class Case(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    name: str
    request: RunRequest
    expected_table: TableValue
    expected_json: JsonValueOutput
    requires_discovery: bool = False
    require_discovery_before_clarification: bool = False
    no_new_discovery_on_resume: bool = False

    @model_validator(mode="after")
    def expected_values(self):
        text = [item for item in self.request.outputs if item.type == "text"]
        if len(text) != 1 or len(self.request.outputs) != 3:
            raise ValueError("A proof case requires one table, one JSON and one text part")
        validate_outputs(self.request.outputs, [
            self.expected_table, self.expected_json,
            TextValue(name=text[0].name, type="text", format=text[0].format, value="Expected text"),
        ])
        if self.expected_table.rows is None:
            raise ValueError("A proof case must register complete expected table rows")
        if self.request.parameters is None or self.request.parameters.period is None:
            raise ValueError("Provide an explicit native period for the saved-study reuse check")
        return self


class ModelPolicy(BaseModel):
    """Read-only projection of EpochAI's ModelCallReceipt owner contract."""
    model_config = ConfigDict(extra="ignore", strict=True)
    run_id: str
    model: str
    model_identity_source: str
    model_role: str
    receipt_source: str


class ResponseMetadata(BaseModel):
    model_config = ConfigDict(extra="ignore", strict=True)
    epoch_model_call: ModelPolicy | None = None


class Usage(BaseModel):
    model_config = ConfigDict(extra="ignore", strict=True)
    input_tokens: int
    output_tokens: int
    total_tokens: int


class ToolCall(BaseModel):
    model_config = ConfigDict(extra="ignore", strict=True)
    id: str
    name: str


class Message(BaseModel):
    """Only identity, calls and usage are read; conversation content is omitted."""
    model_config = ConfigDict(extra="ignore", strict=True)
    id: str | None = None
    type: str | None = None
    role: str | None = None
    tool_calls: list[ToolCall] = Field(default_factory=list)
    response_metadata: ResponseMetadata = Field(default_factory=ResponseMetadata)
    usage_metadata: Usage | None = None


class Outcome(BaseModel):
    model_config = ConfigDict(extra="ignore", strict=True)
    tool_call_id: str
    tool_name: Literal["build_study", "run_study", "run_monte_carlo", "tune_study"]
    status: Literal["saved", "completed", "failed", "cancelled", "not_started", "infeasible", "unknown"]
    execution_id: str | None = None


class ThreadState(BaseModel):
    model_config = ConfigDict(extra="ignore", strict=True)
    sdk_request_id: str
    authority_turn_id: str
    messages: list[Message]
    # Native tool-call IDs own these map keys; outcome values stay closed.
    next_action_outcomes: dict[str, Outcome] = Field(default_factory=dict)


class ModelEvidence(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    policy: ModelPolicy
    usage: Usage | None


class TraceEvidence(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    thread_id: str
    request_id: str
    tool_calls: list[ToolCall]
    model_calls: list[ModelEvidence]
    # Map keys are protocol-owned native tool-call identities.
    outcomes: dict[str, Outcome]


class Receipt(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    scope: Literal["real-services-sdk-mcp-research"] = "real-services-sdk-mcp-research"
    mode: Literal["sdk", "mcp"]
    case_sha256: str
    recorded_at: str
    result: ResearchResult | ResearchFailure | None = None
    reused_execution: ChosenExecution | None = None
    revised_response: ResponseReference | None = None
    revised_content_sha256: str | None = None
    checks: list[str]
    epoch_sdk_version: str
    langgraph_sdk_version: str
    stratifyx_version: str
    native_sdk_backend_sha: str
    native_sdk_openapi_digest: str
    backend_git_sha: str | None = None
    agent_git_sha: str | None = None
    error: ErrorResponse | None = None
    trace: TraceEvidence | None = None
    real_analysis_proven: bool = False


RESULT = TypeAdapter(ResearchResult | ResearchFailure)
ERROR = TypeAdapter(ResearchFailure | ErrorResponse)


class Deployment(BaseModel):
    model_config = ConfigDict(extra="ignore", strict=True)
    git_sha: str


class BuildReadiness(BaseModel):
    model_config = ConfigDict(extra="ignore", strict=True)
    ready: bool
    backend_url: str


class AgentHealth(BaseModel):
    """Read-only projection of the service-owned custom health receipt."""
    model_config = ConfigDict(extra="ignore", strict=True)
    status: str
    deployment: Deployment
    build_study: BuildReadiness


class BackendHealth(BaseModel):
    model_config = ConfigDict(extra="ignore", strict=True)
    git_sha: str


async def preflight(
    graph_url: str, backend_url: str, token: str, backend_sha: str, agent_sha: str,
) -> tuple[str, str]:
    for endpoint in (graph_url, backend_url):
        url = urlsplit(endpoint)
        if (
            url.scheme not in {"http", "https"} or not url.hostname
            or url.username or url.password or url.query or url.fragment
        ):
            raise ValueError("Provide HTTP service URLs without credentials, queries or fragments")
    if len(backend_sha) != 40 or len(agent_sha) != 40:
        raise ValueError("Provide the exact expected Backend and agent commit SHAs")
    async with httpx.AsyncClient(headers={"Authorization": f"Bearer {token}"}, timeout=30) as http:
        backend = await http.get(backend_url.rstrip("/") + "/api/v1/health")
        backend.raise_for_status()
        graph = await http.get(graph_url.rstrip("/") + "/health/custom")
        graph.raise_for_status()
    native = BackendHealth.model_validate(backend.json())
    agent = AgentHealth.model_validate(graph.json())
    if native.git_sha != backend_sha or agent.deployment.git_sha != agent_sha:
        raise RuntimeError("The running services do not match the reviewed source revisions")
    if (
        agent.status != "healthy" or not agent.build_study.ready
        or agent.build_study.backend_url.rstrip("/") != backend_url.rstrip("/")
    ):
        raise RuntimeError("The agent is not ready against the selected Backend")
    return native.git_sha, agent.deployment.git_sha


async def capture_trace(
    graph_url: str, token: str, thread_id: str, request_id: str,
) -> TraceEvidence:
    async with httpx.AsyncClient(
        base_url=graph_url, headers={"Authorization": f"Bearer {token}"}, timeout=30,
    ) as http:
        snapshot = await LangGraphClient(http).threads.get_state(thread_id)
    state = ThreadState.model_validate(snapshot["values"])
    if state.sdk_request_id != request_id or state.authority_turn_id != "user-turn:" + request_id:
        raise AssertionError("The retained thread belongs to a different current request")
    anchor = next((index for index, message in enumerate(state.messages)
                   if message.id == request_id and (message.type == "human" or message.role == "user")), None)
    if anchor is None:
        raise AssertionError("The accepted user-turn identity is absent from the thread")
    messages = state.messages[anchor:]
    calls = [call for message in messages for call in message.tool_calls]
    call_ids = {call.id for call in calls}
    return TraceEvidence(
        thread_id=thread_id, request_id=request_id, tool_calls=calls,
        model_calls=[ModelEvidence(policy=message.response_metadata.epoch_model_call,
                                   usage=message.usage_metadata)
                     for message in messages if message.response_metadata.epoch_model_call is not None],
        outcomes={key: value for key, value in state.next_action_outcomes.items()
                  if value.tool_call_id in call_ids},
    )


def verify_trace(trace: TraceEvidence, completed: ResearchCompleted, *, requires_discovery: bool = False) -> None:
    if not trace.model_calls or not any(
        call.policy.model not in {"", "?"} and call.usage is not None and call.usage.total_tokens > 0
        for call in trace.model_calls
    ):
        raise AssertionError("A real-model proof needs source-owned model identity and token usage")
    chosen_calls = {outcome.tool_call_id for outcome in trace.outcomes.values()
                    if outcome.tool_name == "run_study" and outcome.status == "completed"
                    and outcome.execution_id == completed.response.primary_execution_id}
    if not chosen_calls:
        raise AssertionError("No native completed-run outcome identifies the saved answer's execution")
    run = next((index for index, call in enumerate(trace.tool_calls)
                if call.id in chosen_calls and call.name == "run_study"), None)
    saved_builds = {outcome.tool_call_id for outcome in trace.outcomes.values()
                    if outcome.tool_name == "build_study" and outcome.status == "saved"}
    build = next((index for index, call in enumerate(trace.tool_calls)
                  if call.id in saved_builds and call.name == "build_study"), None)
    if run is None or build is None or build >= run or not any(
        call.name == "publish_response" for call in trace.tool_calls[run + 1:]
    ):
        raise AssertionError("The thread does not show build -> chosen execution -> publish")
    if requires_discovery and not any(call.name == "discovery" for call in trace.tool_calls[:build]):
        raise AssertionError("The registered discovery case did not discover before building")


def verify_resume_trace(before: TraceEvidence, after: TraceEvidence, *, no_new_discovery: bool) -> None:
    if before.thread_id != after.thread_id or before.request_id != after.request_id:
        raise AssertionError("Clarification moved to a different thread or request")
    if after.tool_calls[:len(before.tool_calls)] != before.tool_calls:
        raise AssertionError("The resumed tool history does not retain its prior prefix")
    if no_new_discovery and any(call.name == "discovery" for call in after.tool_calls[len(before.tool_calls):]):
        raise AssertionError("Discovery repeated after the registered clarification point")


def load_case(path: Path) -> Case:
    return Case.model_validate(parse_json(path.read_text()))


def verify_values(
    case: Case,
    result: ResearchCompleted,
    *,
    table: TableValue | None = None,
) -> None:
    response = result.response
    if response.content.declarations != case.request.outputs:
        raise AssertionError("The completed answer changed the accepted declarations")
    values = {item.name: item for item in response.content.outputs}
    actual_table = values[case.expected_table.name]
    if isinstance(actual_table, TableValue) and actual_table.source is not None:
        if table is None:
            raise AssertionError(
                "Read all referenced table pages before checking actual values"
            )
        actual_table = table
    if actual_table != case.expected_table:
        raise AssertionError(
            "Actual saved table values differ from the registered case"
        )
    if values[case.expected_json.name] != case.expected_json:
        raise AssertionError("Actual JSON values differ from the registered case")
    texts = [item for item in values.values() if isinstance(item, TextValue)]
    if len(texts) != 1 or not texts[0].value.strip():
        raise AssertionError("The requested explanation is missing")
    if (
        result.reusable_study is None
        or result.reusable_study.study_id != response.study_id
        or result.reusable_study.source_execution_id != response.primary_execution_id
    ):
        raise AssertionError(
            "Reusable study and saved answer refer to different executions"
        )


def connect(graph_url: str, backend_url: str, token: str) -> EpochClient:
    return EpochClient.connect(
        graph_url=graph_url, backend_url=backend_url, token=token,
        assistant_id=os.environ.get("EPOCH_ASSISTANT_ID", "epoch-ai"),
        ui_url=os.environ.get("EPOCH_UI_URL"),
    )


@asynccontextmanager
async def mcp_client(graph_url: str, backend_url: str, token: str) -> AsyncIterator[Client]:
    env = {
        "EPOCH_GRAPH_URL": graph_url, "EPOCH_BACKEND_URL": backend_url, "EPOCH_TOKEN": token,
    }
    for key in ("EPOCH_ASSISTANT_ID", "EPOCH_UI_URL"):
        if value := os.environ.get(key):
            env[key] = value
    server = StdioServerParameters(
        command=sys.executable, args=["-m", "epoch_sdk.mcp"], env=env,
    )
    failure: EpochError | None = None
    async with Client(server, read_timeout_seconds=None) as client:
        try:
            yield client
        except EpochError as error:
            # AnyIO groups an exception crossing MCP cleanup. Close the client
            # normally, then preserve the domain failure for the proof receipt.
            failure = error
    if failure is not None:
        raise failure


async def mcp_call(client: Client, name: str, arguments: dict):
    result = await client.call_tool(name, arguments)
    if result.is_error or result.structured_content is None:
        raise RuntimeError(f"MCP protocol/tool failure for {name}")
    data = result.structured_content
    if "error" in data:
        error = ERROR.validate_python(data)
        if isinstance(error, ResearchFailure):
            raise ResearchError(error)
        raise EpochError(error.error, execution_id=error.execution_id)
    return data


async def read_case_table(
    mode: str,
    backend_url: str,
    token: str,
    case: Case,
    result: ResearchCompleted,
) -> TableValue:
    """Read every pinned table page; a reference or preview is not value proof."""
    saved = result.response
    table = next(
        part for part in saved.content.outputs if part.name == case.expected_table.name
    )
    if not isinstance(table, TableValue):
        raise TypeError("The requested table was not published")
    if table.source is None:
        return table
    source = table.source
    rows: list[list[Cell]] = []

    def accept(page: ResponseTablePage) -> None:
        if (
            page.response_id != saved.response_id
            or page.version != saved.version
            or page.name != table.name
            or page.columns != table.columns
            or page.total_rows != source.row_count
            or page.offset != len(rows)
        ):
            raise AssertionError(
                "A table page differs from its saved source or continuation"
            )
        rows.extend(page.rows)

    graph_url = "http://127.0.0.1:1"
    if mode == "sdk":
        client = connect(graph_url, backend_url, token)
        try:
            async for page in client.iter_response_table(
                saved.response_id,
                table.name,
                version=saved.version,
            ):
                accept(page)
        finally:
            await client.aclose()
    else:
        async with mcp_client(graph_url, backend_url, token) as client:
            offset = 0
            while True:
                page = ResponseTablePage.model_validate(
                    await mcp_call(
                        client,
                        "epoch_response_table",
                        {
                            "response_id": saved.response_id,
                            "name": table.name,
                            "version": saved.version,
                            "offset": offset,
                            "page_size": 1000,
                        },
                    )
                )
                accept(page)
                if page.next_offset is None:
                    break
                offset = page.next_offset
    if len(rows) != source.row_count:
        raise AssertionError("The proof did not read the complete referenced table")
    return TableValue(name=table.name, type="table", schema=table.columns, rows=rows)


async def research(
    mode: str, case: Case, graph_url: str, backend_url: str, token: str,
    waiting: NeedsInput | None, answers: dict[str, Answers],
) -> ResearchResult:
    if mode == "sdk":
        client = connect(graph_url, backend_url, token)
        try:
            return await client.resume_research(waiting, answers) if waiting else (
                await client.research(case.request)
            )
        finally:
            await client.aclose()
    async with mcp_client(graph_url, backend_url, token) as client:
        arguments = {"waiting": waiting.model_dump(mode="json"),
                     "responses": {key: value.model_dump(mode="json", exclude_unset=True)
                                   for key, value in answers.items()}} if waiting else {
            "request": case.request.to_wire(),
        }
        payload = await mcp_call(
            client, "epoch_resume_research" if waiting else "epoch_research", arguments,
        )
        parsed = RESULT.validate_python(payload)
        if isinstance(parsed, ResearchFailure):
            raise ResearchError(parsed)
        return parsed


async def fresh_read(
    mode: str, backend_url: str, token: str, completed: ResearchCompleted,
) -> None:
    # An unreachable graph URL proves this read cannot silently start an agent.
    graph_url = "http://127.0.0.1:1"
    if mode == "sdk":
        fresh = connect(graph_url, backend_url, token)
        try:
            actual = await fresh.research_status(completed.request_id)
        finally:
            await fresh.aclose()
    else:
        async with mcp_client(graph_url, backend_url, token) as client:
            actual = RESULT.validate_python(await mcp_call(
                client, "epoch_research_status", {"request_id": completed.request_id},
            ))
    if actual != completed:
        raise AssertionError("A fresh client did not return the same pinned answer")


def revision_content(saved: SavedResearchResponse) -> ResearchResponseContent:
    """Edit only the explanation, preserving the computed parts and declarations."""
    texts = [part for part in saved.content.outputs if isinstance(part, TextValue)]
    if len(texts) != 1:
        raise AssertionError("The registered revision proof requires one explanation")
    original = texts[0]
    changed = original.model_copy(
        update={
            "value": original.value
            + "\n\nPublication check: this revision changes only the explanation, not the computed values."
        }
    )
    return ResearchResponseContent(
        declarations=saved.content.declarations,
        outputs=[
            changed if part.name == original.name else part
            for part in saved.content.outputs
        ],
    )


def verify_revision(
    before: SavedResearchResponse,
    after: SavedResearchResponse,
    content: ResearchResponseContent,
) -> None:
    if (
        after.response_id != before.response_id
        or after.request_id != before.request_id
        or after.thread_id != before.thread_id
        or after.primary_execution_id != before.primary_execution_id
        or after.study_id != before.study_id
        or after.version != before.version + 1
        or after.content != content
    ):
        raise AssertionError(
            "The revision changed answer identity, source or accepted values"
        )


class PublishArguments(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    request_id: str
    thread_id: str
    content: ResearchResponseContent
    expected_version: int
    primary_execution_id: str | None = None


async def revise_and_verify(
    mode: str,
    backend_url: str,
    token: str,
    completed: ResearchCompleted,
    receipt: Receipt,
) -> None:
    """Use actual publication/read clients with an unreachable graph endpoint."""
    before = completed.response
    content = revision_content(before)
    graph_url = "http://127.0.0.1:1"
    if mode == "sdk":
        client = connect(graph_url, backend_url, token)
        try:
            latest = await client.supervisor.response(before.response_id)
            if latest != before:
                raise AssertionError("The answer changed before the registered edit")
            after = await client.supervisor.publish_response(
                before.request_id,
                content,
                thread_id=before.thread_id,
                primary_execution_id=before.primary_execution_id,
                expected_version=before.version,
            )
            receipt.revised_response = after.reference()
            verify_revision(before, after, content)
            latest = await client.supervisor.response(before.response_id)
            original = await client.supervisor.response(
                before.response_id, version=before.version
            )
        finally:
            await client.aclose()
    else:
        async with mcp_client(graph_url, backend_url, token) as client:
            latest = SavedResearchResponse.model_validate(
                await mcp_call(
                    client,
                    "epoch_response",
                    {"response_id": before.response_id},
                )
            )
            if latest != before:
                raise AssertionError("The answer changed before the registered edit")
            arguments = PublishArguments(
                request_id=before.request_id,
                thread_id=before.thread_id,
                content=content,
                expected_version=before.version,
            )
            if before.primary_execution_id is not None:
                arguments.primary_execution_id = before.primary_execution_id
            after = SavedResearchResponse.model_validate(
                await mcp_call(
                    client,
                    "epoch_publish_response",
                    arguments.model_dump(mode="json", by_alias=True, exclude_unset=True),
                )
            )
            receipt.revised_response = after.reference()
            verify_revision(before, after, content)
            latest = SavedResearchResponse.model_validate(
                await mcp_call(
                    client,
                    "epoch_response",
                    {"response_id": before.response_id},
                )
            )
            original = SavedResearchResponse.model_validate(
                await mcp_call(
                    client,
                    "epoch_response",
                    {"response_id": before.response_id, "version": before.version},
                )
            )
    if latest != after or original != before:
        raise AssertionError(
            "Latest or immutable original answer read differs after editing"
        )
    receipt.revised_content_sha256 = hashlib.sha256(
        json.dumps(
            after.content.to_wire(),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode()
    ).hexdigest()
    await fresh_read(mode, backend_url, token, completed)
    receipt.checks.extend(
        [
            "post-analysis-revision-without-graph",
            "original-request-still-pinned-after-edit",
        ]
    )


async def reuse(
    mode: str, case: Case, backend_url: str, token: str, completed: ResearchCompleted,
    timeout_seconds: float, receipt: Receipt,
) -> ChosenExecution:
    assert case.request.parameters is not None and case.request.parameters.period is not None
    graph_url = "http://127.0.0.1:1"
    if completed.reusable_study is None:
        raise AssertionError("Prepared execution requires an execution-backed answer")
    if mode == "sdk":
        client = connect(graph_url, backend_url, token)
        try:
            selected = await client.execute_saved(
                completed.reusable_study, period=case.request.parameters.period,
                execution=case.request.parameters.execution,
            )
            receipt.reused_execution = selected
            async with asyncio.timeout(timeout_seconds):
                while selected.execution.status.value in {"pending", "queued", "running"}:
                    await asyncio.sleep(1)
                    selected = selected.model_copy(update={
                        "execution": await client.execution(selected.execution.id),
                    })
                    receipt.reused_execution = selected
        finally:
            await client.aclose()
    else:
        async with mcp_client(graph_url, backend_url, token) as client:
            selected = ChosenExecution.model_validate(await mcp_call(
                client, "epoch_execute_saved", {
                    "reference": completed.reusable_study.model_dump(mode="json"),
                    "parameters": case.request.parameters.to_wire(),
                },
            ))
            receipt.reused_execution = selected
            async with asyncio.timeout(timeout_seconds):
                while selected.execution.status.value in {"pending", "queued", "running"}:
                    await asyncio.sleep(1)
                    from stratifyx.types.job_list_item import JobListItem
                    selected = selected.model_copy(update={
                        "execution": JobListItem.model_validate(await mcp_call(
                            client, "epoch_execution", {"execution_id": selected.execution.id},
                        )),
                    })
                    receipt.reused_execution = selected
    if (
        selected.execution.status.value != "completed"
        or selected.execution.id == completed.response.primary_execution_id
        or selected.execution.definition_id != completed.response.study_id
    ):
        raise AssertionError("Saved-study execution failed or changed its study identity")
    return selected


async def execute(args: argparse.Namespace, case: Case, receipt: Receipt) -> None:
    token = os.environ["EPOCH_TOKEN"]
    graph_url, backend_url = os.environ["EPOCH_GRAPH_URL"], os.environ["EPOCH_BACKEND_URL"]
    receipt.backend_git_sha, receipt.agent_git_sha = await preflight(
        graph_url, backend_url, token, args.expected_backend_sha or "", args.expected_agent_sha or "",
    )
    receipt.checks.append("reviewed-services-paired-and-ready")
    waiting = None
    previous_trace = None
    answers: dict[str, Answers] = {}
    if args.resume_from:
        previous = Receipt.model_validate_json(args.resume_from.read_text())
        if previous.case_sha256 != receipt.case_sha256 or not isinstance(previous.result, NeedsInput):
            raise ValueError("Resume the same registered case with a needs_input receipt")
        if args.answers is None:
            raise ValueError("Provide explicit native answers; recommendations are not auto-selected")
        waiting = previous.result
        previous_trace = previous.trace
        answers = TypeAdapter(dict[str, Answers]).validate_python(parse_json(args.answers.read_text()))
    result = await research(args.mode, case, graph_url, backend_url, token, waiting, answers)
    receipt.result = result
    if isinstance(result, NeedsInput):
        receipt.trace = await capture_trace(graph_url, token, result.handle.thread_id, result.handle.request_id)
        if case.require_discovery_before_clarification and not any(
            call.name == "discovery" for call in receipt.trace.tool_calls
        ):
            raise AssertionError("The registered clarification case did not first load discovery")
        print(result.feedback())
        receipt.checks.append("native-clarification-retained")
        return
    if isinstance(result, InProgress):
        print("The research is still running; preserve this request handle.")
        return
    if not isinstance(result, ResearchCompleted):
        raise TypeError("The research request has no completed saved response")
    if result.reusable_study is None:
        raise AssertionError("This registered engine case requires a reusable study")
    thread_id = result.reusable_study.thread_id
    if thread_id is None:
        raise AssertionError("The completed research response has no native thread reference")
    receipt.trace = await capture_trace(graph_url, token, thread_id, result.request_id)
    verify_trace(receipt.trace, result, requires_discovery=case.requires_discovery)
    if previous_trace is not None:
        verify_resume_trace(previous_trace, receipt.trace, no_new_discovery=case.no_new_discovery_on_resume)
        receipt.checks.append("clarification-retains-thread-and-tool-history")
    receipt.checks.append("native-tool-sequence-and-model-usage")
    table = await read_case_table(args.mode, backend_url, token, case, result)
    verify_values(case, result, table=table)
    receipt.checks.append("complete-table-values-read")
    receipt.checks.extend(["actual-values", "exact-execution-linkage"])
    await fresh_read(args.mode, backend_url, token, result)
    receipt.checks.append("fresh-read-without-graph")
    await revise_and_verify(args.mode, backend_url, token, result, receipt)
    receipt.reused_execution = await reuse(
        args.mode, case, backend_url, token, result, args.execution_timeout, receipt,
    )
    receipt.checks.append("direct-repeat-without-graph")
    receipt.real_analysis_proven = True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", type=Path, required=True)
    parser.add_argument("--mode", choices=["sdk", "mcp"], required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--expected-backend-sha")
    parser.add_argument("--expected-agent-sha")
    parser.add_argument("--resume-from", type=Path)
    parser.add_argument("--answers", type=Path)
    parser.add_argument("--execution-timeout", type=float, default=300)
    args = parser.parse_args()
    case = load_case(args.case)
    receipt = Receipt(
        mode=args.mode, case_sha256=hashlib.sha256(args.case.read_bytes()).hexdigest(),
        recorded_at=datetime.now(UTC).isoformat(), checks=["registered-case-valid"],
        epoch_sdk_version=importlib.metadata.version("epoch-sdk"),
        langgraph_sdk_version=importlib.metadata.version("langgraph-sdk"),
        stratifyx_version=importlib.metadata.version("stratifyx"),
        native_sdk_backend_sha=SDK_RELEASE["backend_git_sha"],
        native_sdk_openapi_digest=SDK_RELEASE["openapi_digest"],
    )
    try:
        if args.execute:
            asyncio.run(execute(args, case, receipt))
        else:
            print(case.request.model_dump_json(by_alias=True, exclude_unset=True, indent=2))
            print("Validated only; no service connection, study or model call was made.")
    except ResearchError as error:
        receipt.result = error.response
        raise
    except EpochError as error:
        receipt.error = ErrorResponse.model_validate({
            "error": error.error.to_wire(),
            **({"execution_id": error.execution_id} if error.execution_id else {}),
        })
        raise
    finally:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(receipt.model_dump_json(exclude_none=True, indent=2) + "\n")


if __name__ == "__main__":
    main()
