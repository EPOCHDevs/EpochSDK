"""Prove readable-ID reconnect through real services and normally built clients.

Uses the registered supplied-data case. No vendor credential enters a client.
"""

from __future__ import annotations

import argparse
import asyncio
import importlib.metadata
import json
import os
import time
from contextlib import asynccontextmanager, suppress
from pathlib import Path
from uuid import uuid4
from typing import Literal, TypedDict

from pydantic import TypeAdapter
from stratifyx.core.api_error import ApiError
from stratifyx._release import SDK_RELEASE

from epoch_sdk.research import (
    EpochClient,
    ExecutionAccepted,
    ResearchCompleted,
    ResearchResult,
)
from epoch_sdk.supervisor import Answer, Answers, ChosenExecution, NeedsInput
from epoch_sdk.output_validation import TableValue
from verify_research_services import (
    capture_trace,
    connect,
    load_case,
    mcp_call,
    mcp_client,
    preflight,
    read_case_table,
    revision_content,
    verify_trace,
    verify_values,
    TraceEvidence,
)

RESULT = TypeAdapter(ResearchResult)
EXECUTION = TypeAdapter(ChosenExecution | ExecutionAccepted)


class NativeSdkProvenance(TypedDict):
    backend_git_sha: str
    backend_worktree_dirty: bool
    distribution: str
    openapi_digest: str
    schema_version: int
    source_tree_digest: str
    source_tree_digest_algorithm: str
    version: str


class ProofReceipt(TypedDict, total=False):
    scope: Literal["real-sdk-mcp-readable-reconnect"]
    mode: Literal["sdk", "mcp"]
    native_sdk: NativeSdkProvenance
    epoch_sdk_version: str
    langgraph_sdk_version: str
    backend_git_sha: str
    agent_git_sha: str
    accepted_task: str
    operation_id: str
    initial_observer_cancelled: bool
    request_id: str
    thread_id: str
    initial_graph_run_id: str
    pending_interrupt_ids: list[str]
    resume_observer_cancelled_before_finish: bool
    resumed_graph_run_id: str
    server_pinned_without_client_finish: bool
    trace: TraceEvidence
    later_conversation_run_id: str
    original_pin_after_conversation_and_revision: bool
    no_duplicate_research_turn_or_job: bool
    execution_observer_cancelled: bool
    prepared_execution_id: str
    execution_operation_id: str
    prepared_execution_one_job_without_graph: bool
    completed: ResearchCompleted
    table: TableValue
    real_analysis_proven: bool
    status: Literal["passed", "failed"]
    error_type: str
    error: str
    plan: str


RECEIPT = TypeAdapter(ProofReceipt)


@asynccontextmanager
async def connection(mode, graph_url, backend_url, token):
    if mode == "sdk":
        client = connect(graph_url, backend_url, token)
        try:
            yield client
        finally:
            await client.aclose()
    else:
        async with mcp_client(graph_url, backend_url, token) as client:
            yield client


async def research(client, mode, request, operation_id):
    if mode == "sdk":
        return await client.research(request, operation_id=operation_id)
    return RESULT.validate_python(
        await mcp_call(
            client,
            "epoch_research",
            {"request": request.to_wire(), "operation_id": operation_id},
        )
    )


async def status(client, mode, operation_id):
    if mode == "sdk":
        return await client.research_status(operation_id=operation_id)
    return RESULT.validate_python(
        await mcp_call(client, "epoch_research_status", {"operation_id": operation_id})
    )


async def resume(client, mode, waiting, answers):
    if mode == "sdk":
        return await client.resume_research(waiting, answers)
    return RESULT.validate_python(
        await mcp_call(
            client,
            "epoch_resume_research",
            {
                "waiting": waiting.model_dump(mode="json"),
                "responses": {
                    key: value.model_dump(mode="json") for key, value in answers.items()
                },
            },
        )
    )


async def cancel_observer(task):
    if task.done():
        result = task.result()
        if isinstance(result, ResearchCompleted):
            raise AssertionError(
                "Original observer completed before the registered disconnect point"
            )
        return False
    task.cancel()
    with suppress(asyncio.CancelledError):
        await task
    return True


async def record(observer: EpochClient, operation_id):
    try:
        return await observer.backend.sdk_requests.get_sdk_request_by_handle(
            operation_id, request_options={"max_retries": 0}
        )
    except ApiError as error:
        if error.status_code != 404:
            raise
        return None


async def wait_claim(observer, operation_id, task, previous=None):
    deadline = time.monotonic() + 90
    while time.monotonic() < deadline:
        accepted = await record(observer, operation_id)
        if accepted is not None:
            if accepted.error is not None:
                raise AssertionError(accepted.error.model_dump_json(exclude_unset=True))
            if accepted.graph_run_id is not None and accepted.graph_run_id != previous:
                return accepted
        if task.done():
            task.result()
        await asyncio.sleep(0.1)
    raise TimeoutError("Native run admission")


async def execute(args, receipt: ProofReceipt):
    if (
        receipt["epoch_sdk_version"] != "0.1.0a4"
        or receipt["native_sdk"]["backend_worktree_dirty"]
        or receipt["native_sdk"]["backend_git_sha"] != args.expected_backend_sha
    ):
        raise RuntimeError(
            "Use the matching normally built SDK and clean-source native preview archives"
        )
    graph_url, backend_url, token = (
        os.environ[key]
        for key in ("EPOCH_GRAPH_URL", "EPOCH_BACKEND_URL", "EPOCH_TOKEN")
    )
    receipt["backend_git_sha"], receipt["agent_git_sha"] = await preflight(
        graph_url,
        backend_url,
        token,
        args.expected_backend_sha,
        args.expected_agent_sha,
    )
    case = load_case(args.case)
    case.request.task = (
        "Before building, ask me once to confirm that you should use exactly the two supplied "
        "years (2024 and 2025). Wait for my confirmation using ask_user. After I confirm, "
        + case.request.task
    )
    receipt["accepted_task"] = case.request.task
    receipt["operation_id"] = args.operation_id
    observer = connect(graph_url, backend_url, token)
    try:
        async with connection(args.mode, graph_url, backend_url, token) as original:
            task = asyncio.create_task(
                research(original, args.mode, case.request, args.operation_id)
            )
            accepted = await wait_claim(observer, args.operation_id, task)
            receipt["initial_observer_cancelled"] = await cancel_observer(task)
        receipt.update(
            request_id=accepted.request_id,
            thread_id=accepted.runtime.thread_id,
            initial_graph_run_id=accepted.graph_run_id,
        )
        assert accepted.response_version is None
        deadline = time.monotonic() + args.timeout_seconds
        async with connection(args.mode, graph_url, backend_url, token) as fresh:
            while True:
                pending = await status(fresh, args.mode, args.operation_id)
                if isinstance(pending, NeedsInput):
                    break
                assert not isinstance(pending, ResearchCompleted), (
                    "The explicit confirmation was skipped"
                )
                assert time.monotonic() < deadline, "Clarification timeout"
                await asyncio.sleep(1)
        assert pending.handle.run_id == accepted.graph_run_id
        receipt["pending_interrupt_ids"] = [item.id for item in pending.interrupts]
        answers = {}
        for item in pending.interrupts:
            rows = []
            for index, question in enumerate(item.ask_user().questions):
                recommended = next(
                    (
                        i
                        for i, option in enumerate(question.options)
                        if option.recommended
                    ),
                    None,
                )
                rows.append(
                    Answer(question_index=index, selected_indices=[recommended])
                    if recommended is not None
                    else Answer(
                        question_index=index,
                        free_form_input="Yes, use both supplied years: 2024 and 2025.",
                    )
                )
            answers[item.id] = Answers(answers=rows)
        async with connection(args.mode, graph_url, backend_url, token) as resuming:
            task = asyncio.create_task(resume(resuming, args.mode, pending, answers))
            resumed = await wait_claim(
                observer, args.operation_id, task, previous=accepted.graph_run_id
            )
            receipt["resume_observer_cancelled_before_finish"] = await cancel_observer(
                task
            )
        assert receipt["resume_observer_cancelled_before_finish"]
        receipt["resumed_graph_run_id"] = resumed.graph_run_id
        # Poll ONLY native Backend records, without EpochClient._finish. Server publication
        # must pin the answer with both original/resume clients gone.
        while True:
            saved = await record(observer, args.operation_id)
            assert saved is not None
            if saved.error is not None:
                raise AssertionError(saved.error.model_dump_json(exclude_unset=True))
            if saved.response_version is not None:
                break
            assert time.monotonic() < deadline, "Server-owned publication timeout"
            run = await observer.supervisor.graph.runs.get(
                saved.runtime.thread_id, saved.graph_run_id
            )
            if run["status"] in {"error", "timeout"}:
                raise AssertionError("Native graph failed before server publication")
            await asyncio.sleep(1)
        receipt["server_pinned_without_client_finish"] = True
        await observer.supervisor.graph.runs.join(
            saved.runtime.thread_id, saved.graph_run_id
        )
        # Read before advancing only to verify actual model/build/execution evidence.
        completed = await observer.research_status(operation_id=args.operation_id)
        assert (
            isinstance(completed, ResearchCompleted) and completed.response.version == 1
        )
        trace = await capture_trace(
            graph_url, token, saved.runtime.thread_id, saved.request_id
        )
        verify_trace(trace, completed)
        receipt["trace"] = trace
        table = await read_case_table(args.mode, backend_url, token, case, completed)
        verify_values(case, completed, table=table)
        original_runs = [
            item["run_id"]
            for item in await observer.supervisor.graph.runs.list(
                saved.runtime.thread_id, limit=100
            )
            if (item["metadata"] or {}).get("epoch_sdk_request_id") == saved.request_id
        ]
        assert set(original_runs) == {accepted.graph_run_id, resumed.graph_run_id}
        jobs_before = await observer.backend.studies_executions.list_executions(
            request_options={"max_retries": 0}
        )
        # An ordinary subsequent conversation turn publishes its own answer.
        later_id = "followup-" + str(uuid4())
        later = await observer.supervisor.graph.runs.create(
            saved.runtime.thread_id,
            "epoch-ai",
            input={
                "messages": [
                    {
                        "role": "user",
                        "id": later_id,
                        "content": "Explain the completed supplied-sales study in one short sentence. Reuse the same results and publish the answer. Do not build or execute any study.",
                    }
                ]
            },
            durability="sync",
            on_completion="keep",
            multitask_strategy="reject",
        )
        await observer.supervisor.graph.runs.join(
            saved.runtime.thread_id, later["run_id"]
        )
        snapshot = await observer.supervisor.graph.threads.get_state(
            saved.runtime.thread_id
        )
        assert snapshot["values"]["authority_turn_id"] == "user-turn:" + later_id
        assert snapshot["values"]["published_response"]["request_id"] == later_id
        jobs_after = await observer.backend.studies_executions.list_executions(
            request_options={"max_retries": 0}
        )
        assert sorted(jobs_before) == sorted(jobs_after), (
            "Conversation follow-up launched another job"
        )
        receipt["later_conversation_run_id"] = later["run_id"]
        # A later saved revision also must not replace the operation's original pin.
        revision = await observer.supervisor.publish_response(
            saved.request_id,
            revision_content(completed.response),
            thread_id=saved.runtime.thread_id,
            primary_execution_id=completed.response.primary_execution_id,
            expected_version=1,
        )
        assert revision.version == 2
        async with connection(args.mode, graph_url, backend_url, token) as fresh:
            attached = await research(fresh, args.mode, case.request, args.operation_id)
        assert isinstance(attached, ResearchCompleted)
        assert (
            attached.response == completed.response and attached.response.version == 1
        )
        final_runs = [
            item["run_id"]
            for item in await observer.supervisor.graph.runs.list(
                saved.runtime.thread_id, limit=100
            )
            if (item["metadata"] or {}).get("epoch_sdk_request_id") == saved.request_id
        ]
        assert sorted(final_runs) == sorted(original_runs)
        receipt["original_pin_after_conversation_and_revision"] = True
        receipt["no_duplicate_research_turn_or_job"] = True
        assert (
            case.request.parameters is not None
            and case.request.parameters.period is not None
        )
        execution_handle = args.operation_id + "-execute"
        async with connection(args.mode, graph_url, backend_url, token) as executor:
            if args.mode == "sdk":
                task = asyncio.create_task(
                    executor.execute_saved(
                        args.operation_id,
                        period=case.request.parameters.period,
                        operation_id=execution_handle,
                    )
                )
            else:
                task = asyncio.create_task(
                    mcp_call(
                        executor,
                        "epoch_execute_saved",
                        {
                            "reference": args.operation_id,
                            "parameters": case.request.parameters.to_wire(),
                            "operation_id": execution_handle,
                        },
                    )
                )
            while True:
                try:
                    execution_record = await observer.backend.sdk_requests.get_sdk_execution_request_by_handle(
                        execution_handle, request_options={"max_retries": 0}
                    )
                    break
                except ApiError as error:
                    if error.status_code != 404:
                        raise
                if task.done():
                    task.result()
                await asyncio.sleep(0.01)
            if not task.done():
                task.cancel()
                with suppress(asyncio.CancelledError):
                    await task
                receipt["execution_observer_cancelled"] = True
            else:
                task.result()
                receipt["execution_observer_cancelled"] = False
        async with connection(
            args.mode, "http://127.0.0.1:1", backend_url, token
        ) as fresh:
            while True:
                if args.mode == "sdk":
                    selected = await fresh.execute_saved(
                        completed.reusable_study,
                        period=case.request.parameters.period,
                        operation_id=execution_handle,
                    )
                else:
                    selected = EXECUTION.validate_python(
                        await mcp_call(
                            fresh,
                            "epoch_execute_saved",
                            {
                                "reference": completed.reusable_study.model_dump(
                                    mode="json"
                                ),
                                "parameters": case.request.parameters.to_wire(),
                                "operation_id": execution_handle,
                            },
                        )
                    )
                if (
                    isinstance(selected, ChosenExecution)
                    and selected.execution.status.value == "completed"
                ):
                    break
                assert time.monotonic() < deadline, "Prepared execution timeout"
                if isinstance(selected, ChosenExecution):
                    assert selected.execution.status.value in {
                        "pending",
                        "queued",
                        "running",
                    }
                await asyncio.sleep(1)
        assert selected.execution.id == execution_record.execution_id
        assert selected.execution.definition_id == completed.response.study_id
        jobs_final = await observer.backend.studies_executions.list_executions(
            request_options={"max_retries": 0}
        )
        assert set(jobs_final) - set(jobs_after) == {selected.execution.id}
        receipt.update(
            prepared_execution_id=selected.execution.id,
            execution_operation_id=execution_handle,
            prepared_execution_one_job_without_graph=True,
            completed=completed,
            table=table,
            real_analysis_proven=True,
            status="passed",
        )
    finally:
        await observer.aclose()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["sdk", "mcp"], required=True)
    parser.add_argument("--operation-id", required=True)
    parser.add_argument(
        "--case", type=Path, default=Path("examples/research-service-proof.case.json")
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--expected-backend-sha", required=True)
    parser.add_argument("--expected-agent-sha", required=True)
    parser.add_argument("--timeout-seconds", type=float, default=900)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    receipt: ProofReceipt = {
        "scope": "real-sdk-mcp-readable-reconnect",
        "mode": args.mode,
        "native_sdk": TypeAdapter(NativeSdkProvenance).validate_python(SDK_RELEASE),
        "epoch_sdk_version": importlib.metadata.version("epoch-sdk"),
        "langgraph_sdk_version": importlib.metadata.version("langgraph-sdk"),
        "real_analysis_proven": False,
    }
    if not args.execute:
        print(
            json.dumps(
                receipt
                | {
                    "plan": "Synthetic two-row confirmation/build/execute/publish; disconnect both observers; advance conversation; fresh attach original pin; direct prepared execution."
                },
                indent=2,
            )
        )
        return
    try:
        asyncio.run(execute(args, receipt))
    except BaseException as error:
        receipt.update(
            status="failed", error_type=type(error).__name__, error=str(error)
        )
        raise
    finally:
        args.output.write_bytes(
            RECEIPT.dump_json(RECEIPT.validate_python(receipt), indent=2) + b"\n"
        )


if __name__ == "__main__":
    main()
