"""Run a reviewed research case through the real SDK or MCP process.

Without --execute this validates and describes the case without opening a
connection. Receipts are local evidence, not a published research dataset.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import importlib.metadata
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
from epoch_sdk.supervisor import Answers, ChosenExecution, InProgress, NeedsInput
from mcp import Client, StdioServerParameters
from pydantic import BaseModel, ConfigDict, TypeAdapter, model_validator
from stratifyx._release import SDK_RELEASE


class Case(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    name: str
    request: RunRequest
    expected_table: TableValue
    expected_json: JsonValueOutput

    @model_validator(mode="after")
    def expected_values(self):
        text = [item for item in self.request.outputs if item.type == "text"]
        if len(text) != 1 or len(self.request.outputs) != 3:
            raise ValueError("A proof case requires one table, one JSON and one text part")
        validate_outputs(self.request.outputs, [
            self.expected_table, self.expected_json,
            TextValue(name=text[0].name, type="text", format=text[0].format, value="Expected text"),
        ])
        if self.request.parameters is None or self.request.parameters.period is None:
            raise ValueError("Provide an explicit native period for the saved-study reuse check")
        return self


class Receipt(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    scope: Literal["real-services-sdk-mcp-research"] = "real-services-sdk-mcp-research"
    mode: Literal["sdk", "mcp"]
    case_sha256: str
    recorded_at: str
    result: ResearchResult | ResearchFailure | None = None
    reused_execution: ChosenExecution | None = None
    checks: list[str]
    epoch_sdk_version: str
    langgraph_sdk_version: str
    stratifyx_version: str
    native_sdk_backend_sha: str
    native_sdk_openapi_digest: str
    backend_git_sha: str | None = None
    agent_git_sha: str | None = None
    error: ErrorResponse | None = None
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


def load_case(path: Path) -> Case:
    return Case.model_validate(parse_json(path.read_text()))


def verify_values(case: Case, result: ResearchCompleted) -> None:
    response = result.response
    if response.content.declarations != case.request.outputs:
        raise AssertionError("The completed answer changed the accepted declarations")
    values = {item.name: item for item in response.content.outputs}
    if values[case.expected_table.name] != case.expected_table:
        raise AssertionError("Actual saved table values differ from the registered case")
    if values[case.expected_json.name] != case.expected_json:
        raise AssertionError("Actual JSON values differ from the registered case")
    texts = [item for item in values.values() if isinstance(item, TextValue)]
    if len(texts) != 1 or not texts[0].value.strip():
        raise AssertionError("The requested explanation is missing")
    if (
        result.reusable_study.study_id != response.study_id
        or result.reusable_study.source_execution_id != response.execution_id
    ):
        raise AssertionError("Reusable study and saved answer refer to different executions")


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
    async with Client(server, read_timeout_seconds=None) as client:
        yield client


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


async def reuse(
    mode: str, case: Case, backend_url: str, token: str, completed: ResearchCompleted,
    timeout_seconds: float, receipt: Receipt,
) -> ChosenExecution:
    assert case.request.parameters is not None and case.request.parameters.period is not None
    graph_url = "http://127.0.0.1:1"
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
        or selected.execution.id == completed.response.execution_id
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
    answers: dict[str, Answers] = {}
    if args.resume_from:
        previous = Receipt.model_validate_json(args.resume_from.read_text())
        if previous.case_sha256 != receipt.case_sha256 or not isinstance(previous.result, NeedsInput):
            raise ValueError("Resume the same registered case with a needs_input receipt")
        if args.answers is None:
            raise ValueError("Provide explicit native answers; recommendations are not auto-selected")
        waiting = previous.result
        answers = TypeAdapter(dict[str, Answers]).validate_python(parse_json(args.answers.read_text()))
    result = await research(args.mode, case, graph_url, backend_url, token, waiting, answers)
    receipt.result = result
    if isinstance(result, NeedsInput):
        print(result.feedback())
        receipt.checks.append("native-clarification-retained")
        return
    if isinstance(result, InProgress):
        print("The research is still running; preserve this request handle.")
        return
    if not isinstance(result, ResearchCompleted):
        raise TypeError("The research request has no completed saved response")
    verify_values(case, result)
    receipt.checks.extend(["actual-values", "exact-execution-linkage"])
    await fresh_read(args.mode, backend_url, token, result)
    receipt.checks.append("fresh-read-without-graph")
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
