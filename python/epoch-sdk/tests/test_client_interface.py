"""Shared public behavior: SDK and MCP choose the same workflow, never a second agent."""

from __future__ import annotations

import asyncio

import httpx
import pytest
from mcp import Client
from stratifyx import DatePeriodConfig
from test_operation_reconnect import Service
from test_research import REQUEST
from test_session import StreamService
from test_supervisor import THREAD, job

from epoch_sdk import EpochError, RunRequest
from epoch_sdk.supervisor import SavedStudy
from epoch_sdk.workflow_mcp import create_server


def test_sdk_task_fields_and_mcp_have_identical_requests_results_and_session_behavior():
    async def scenario():
        request = RunRequest.model_validate(REQUEST)
        results = []
        accepted = []
        for mode in ("sdk", "mcp"):
            service = StreamService()
            async with service.client() as client:
                if mode == "sdk":
                    events = []

                    async def observe(event, events=events):
                        events.append(event)

                    value = await client.run(
                        task=request.task,
                        context=request.context,
                        outputs=request.outputs,
                        parameters=request.parameters,
                        thread_id=THREAD,
                        operation_id="shared-interface",
                        interface="headless",
                        on_event=observe,
                    )
                    results.append(value.to_wire())
                    assert events[-1].event == "completed"
                else:
                    async with Client(create_server(client)) as mcp:
                        value = await mcp.call_tool(
                            "epoch_run",
                            {
                                **REQUEST,
                                "operation_id": "shared-interface",
                                "thread_id": THREAD,
                            },
                        )
                        assert not value.is_error
                        results.append(value.structured_content)
                accepted.append(service.record["request"])
                assert service.submissions == service.streams == 1
        assert results[0] == results[1] and accepted[0] == accepted[1]

    asyncio.run(scenario())


@pytest.mark.parametrize("operation", ["run", "execute"])
@pytest.mark.parametrize("handle", ["", " spaced "])
def test_blank_or_padded_explicit_ids_never_turn_into_new_operations(operation, handle):
    async def scenario():
        service = StreamService()
        async with service.client() as client:
            with pytest.raises(ValueError):
                if operation == "run":
                    await client.run(REQUEST["task"], operation_id=handle, interface="headless")
                else:
                    await client.execute(
                        "saved", period=DatePeriodConfig(start="2025-01-01"), operation_id=handle
                    )
            assert service.record is None and service.jobs == 0 and service.graph_calls == []

    asyncio.run(scenario())


def test_typed_request_fields_cannot_be_silently_overridden():
    async def scenario():
        service = StreamService()
        async with service.client() as client:
            with pytest.raises(ValueError, match="RunRequest"):
                await client.run(
                    RunRequest.model_validate(REQUEST), context=["Changed"], interface="headless"
                )
            assert service.record is None and service.graph_calls == []

    asyncio.run(scenario())


def test_execute_waits_for_backend_completion_without_resubmitting_or_calling_graph():
    async def scenario():
        service = Service()
        calls = []
        remaining = ["queued", "completed"]

        def backend(request):
            calls.append(request.method)
            if request.url.path == "/api/v1/studies/executions/repeat-one":
                return httpx.Response(200, json=job("repeat-one", status=remaining.pop(0)))
            return service.backend(request)

        service.backend_handler = backend
        async with service.client() as client:
            result = await asyncio.wait_for(
                client.execute(
                    SavedStudy(study_id="study-one", source_execution_id="new"),
                    period=DatePeriodConfig(start="2025-01-01"),
                    operation_id="prepared",
                ),
                4,
            )
            assert result.execution.status.value == "completed"
            assert service.jobs == 1 and service.graph_calls == [] and calls.count("POST") == 1

    asyncio.run(scenario())


@pytest.mark.parametrize("state", ["failed", "cancelled"])
def test_execute_does_not_report_a_failed_or_cancelled_job_as_an_answer(state):
    async def scenario():
        from epoch_sdk.supervisor import SavedStudy

        service = Service()

        def backend(request):
            if request.url.path == "/api/v1/studies/executions/repeat-one":
                return httpx.Response(200, json=job("repeat-one", status=state))
            return service.backend(request)

        service.backend_handler = backend
        async with service.client() as client:
            with pytest.raises(EpochError) as error:
                await client.execute(
                    SavedStudy(study_id="study-one", source_execution_id="new"),
                    period=DatePeriodConfig(start="2025-01-01"),
                    operation_id="failed",
                )
            assert error.value.error.code == "EXECUTION_FAILED"
            assert error.value.execution_id == "repeat-one"
            assert service.jobs == 1 and service.graph_calls == []

    asyncio.run(scenario())


def test_answer_reads_do_not_silently_ignore_table_paging_arguments():
    async def scenario():
        service = Service()
        async with service.client() as client:
            with pytest.raises(ValueError, match="table name"):
                await client.read("saved", offset=10)
            assert service.record is None and service.graph_calls == []

    asyncio.run(scenario())


def test_cancelling_execute_only_detaches_the_observer():
    async def scenario():
        service = Service()
        reached = asyncio.Event()
        methods = []

        def backend(request):
            methods.append((request.method, request.url.path))
            if request.url.path == "/api/v1/studies/executions/repeat-one":
                reached.set()
                return httpx.Response(200, json=job("repeat-one", status="queued"))
            return service.backend(request)

        service.backend_handler = backend
        async with service.client() as client:
            observer = asyncio.create_task(
                client.execute(
                    SavedStudy(study_id="study-one", source_execution_id="new"),
                    period=DatePeriodConfig(start="2025-01-01"),
                    operation_id="kept-execution",
                )
            )
            await asyncio.wait_for(reached.wait(), 3)
            observer.cancel()
            with pytest.raises(asyncio.CancelledError):
                await observer
            current = await client.status("kept-execution", kind="execute")
            assert current.execution.status.value == "queued"
            assert service.jobs == 1 and service.graph_calls == []
            assert all(method != "DELETE" and "/cancel" not in path for method, path in methods)
            assert sum(method == "POST" for method, path in methods) == 1

    asyncio.run(scenario())


def test_legacy_typed_request_keyword_still_uses_the_shared_session():
    async def scenario():
        service = StreamService()
        async with service.client() as client:
            result = await client.run(
                request=RunRequest.model_validate(REQUEST),
                operation_id="legacy-keyword",
                interface="headless",
            )
            assert result.status == "succeeded" and service.submissions == service.streams == 1

    asyncio.run(scenario())
