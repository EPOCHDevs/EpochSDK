"""Client-boundary cases; real native acceptance/service proof is separate."""

from __future__ import annotations

import asyncio
import copy
import json
from contextlib import asynccontextmanager

import httpx
import pytest
from langgraph_sdk.client import LangGraphClient
from mcp import Client
from stratifyx import AsyncStratifyX, DatePeriodConfig
from test_research import REQUEST, REQUEST_ID, saved_response
from test_supervisor import INTERRUPT, RUN, THREAD, job

from epoch_sdk import EpochError, RunRequest
from epoch_sdk.mcp import create_server
from epoch_sdk.research import EpochClient, ExecutionAccepted, ResearchCompleted, ResearchError
from epoch_sdk.response_plans import ResponsePlanReference
from epoch_sdk.supervisor import (
    ChosenExecution,
    InProgress,
    NeedsInput,
    NoExecution,
    SavedStudy,
    SupervisorClient,
    WorkflowHandle,
)


class ObservedRunStream(httpx.AsyncByteStream):
    def __init__(self, service):
        self.service = service

    async def __aiter__(self):
        self.service.waiting.set()
        await self.service.release.wait()
        yield b"event: end\ndata: {}\n\n"


class Service:
    def __init__(self):
        self.record = None
        self.submissions = 0
        self.waiting = asyncio.Event()
        self.release = asyncio.Event()
        self.response = saved_response()
        self.graph_status = "running"
        self.snapshot = {
            "values": {"authority_turn_id": "user-turn:" + REQUEST_ID},
            "next": [],
            "interrupts": [],
        }
        self.graph_calls = []
        self.execution_record = None
        self.jobs = 0
        self.stale_admission = False
        self.stale_reads = 0
        self.backend_handler = None

    def stale(self):
        result = copy.deepcopy(self.record)
        result.pop("runtime", None)
        result.pop("graph_run_id", None)
        result.update(phase="accepted", version=0)
        return result

    def complete(self):
        # Models the SERVER publication path, without EpochClient._finish.
        self.record.update(
            phase="outputs_recorded",
            response_id=self.response["response_id"],
            response_version=1,
            current_execution_id="new",
        )
        self.graph_status = "success"
        self.release.set()

    def backend(self, request):
        path = request.url.path
        if path == "/api/v1/integration/requests" and request.method == "POST":
            body = json.loads(request.content)
            if self.record is None:
                self.record = {
                    "request_id": REQUEST_ID,
                    "version": 0,
                    "phase": "accepted",
                    "created_at_ms": 1,
                    "updated_at_ms": 1,
                    **body,
                }
            elif (
                body["request"] != self.record["request"] or body["launch"] != self.record["launch"]
            ):
                return httpx.Response(409, json={"message": "Changed inputs"})
            if self.stale_admission:
                self.stale_admission = False
                return httpx.Response(200, json=self.stale())
            return httpx.Response(200, json=self.record)
        if path.startswith("/api/v1/integration/requests/"):
            if request.method == "GET" and self.stale_reads:
                self.stale_reads -= 1
                return httpx.Response(200, json=self.stale())
            if request.method == "PATCH":
                patch = json.loads(request.content)
                if patch.pop("expected_version") != self.record["version"]:
                    return httpx.Response(409, json={"message": "Version changed"})
                self.record.update(patch)
                self.record["version"] += 1
                if "runtime" in patch:
                    self.record["phase"] = "active"
                if "error" in patch:
                    self.record["phase"] = "failed"
            return httpx.Response(200, json=self.record)
        if path.startswith("/api/v1/research/responses/"):
            assert request.url.params["version"] == "1"
            response = copy.deepcopy(self.response)
            response["content"]["declarations"] = self.record["request"]["outputs"]
            return httpx.Response(200, json=response)
        if path == "/api/v1/integration/execution-requests":
            body = json.loads(request.content)
            if self.execution_record is None:
                self.execution_record = {
                    "request_id": REQUEST_ID,
                    "execution_id": "repeat-one",
                    "request": body,
                    "phase": "active",
                    "created_at_ms": 1,
                }
                self.jobs += 1
            elif self.execution_record["request"] != body:
                return httpx.Response(409, json={"message": "Changed execution"})
            return httpx.Response(200, json=self.execution_record)
        if path.startswith("/api/v1/integration/execution-requests/"):
            return httpx.Response(200, json=self.execution_record)
        if path == "/api/v1/studies/executions/repeat-one":
            return httpx.Response(200, json=job("repeat-one"))
        raise AssertionError((request.method, path))

    async def graph(self, request):
        self.graph_calls.append(request)
        path = request.url.path
        if path.endswith("/stream"):
            assert request.url.params["cancel_on_disconnect"] == "false"
            return httpx.Response(
                200, headers={"content-type": "text/event-stream"}, stream=ObservedRunStream(self)
            )
        if path == "/threads":
            return httpx.Response(200, json={"thread_id": THREAD})
        if path.endswith("/state"):
            return httpx.Response(200, json=self.snapshot)
        if path.endswith("/runs") and request.method == "POST":
            self.submissions += 1
            assert self.record["runtime"]["thread_id"] == path.split("/")[2]
            body = json.loads(request.content)
            assert body["input"]["messages"][0]["id"] == REQUEST_ID
            assert body["input"]["messages"][0]["content"] == REQUEST["task"]
            assert body["durability"] == "sync" and body["on_completion"] == "keep"
            # Native auth records this before the native create response returns.
            self.record["graph_run_id"] = RUN
            return httpx.Response(
                200, json={"run_id": RUN, "thread_id": self.record["runtime"]["thread_id"]}
            )
        if path.endswith("/join"):
            self.waiting.set()
            await self.release.wait()
            return httpx.Response(200, json={"authority_turn_id": "user-turn:later-query"})
        current_run = self.record.get("graph_run_id", RUN) if self.record else RUN
        if path.endswith("/runs/" + current_run):
            return httpx.Response(
                200,
                json={
                    "run_id": current_run,
                    "status": self.graph_status,
                    "metadata": {"epoch_sdk_request_id": REQUEST_ID},
                },
            )
        if path.endswith("/history"):
            body = json.loads(request.content)
            assert body["metadata"] == {"epoch_sdk_request_id": REQUEST_ID, "epoch_sdk_run_id": RUN}
            return httpx.Response(200, json=[self.snapshot])
        raise AssertionError((request.method, path))

    @asynccontextmanager
    async def client(self):
        async with (
            httpx.AsyncClient(
                transport=httpx.MockTransport(self.backend_handler or self.backend)
            ) as backend_http,
            httpx.AsyncClient(
                base_url="https://graph.invalid", transport=httpx.MockTransport(self.graph)
            ) as graph_http,
        ):
            supervisor = SupervisorClient(
                LangGraphClient(graph_http),
                AsyncStratifyX(
                    base_url="https://backend.invalid", token="fixture", httpx_client=backend_http
                ),
            )
            yield EpochClient(supervisor)


async def started(service, task):
    waiting = asyncio.create_task(service.waiting.wait())
    done, _ = await asyncio.wait({task, waiting}, timeout=5, return_when=asyncio.FIRST_COMPLETED)
    if task in done:
        task.result()  # expose admission failures instead of hanging on a fixture event
    assert waiting in done, "The operation did not reach its native join"


@pytest.mark.parametrize("mode", ["sdk", "mcp"])
def test_fresh_client_reattaches_after_original_wait_is_cancelled_and_conversation_advances(mode):
    async def scenario():
        service = Service()
        async with service.client() as sdk:
            if mode == "sdk":
                original = asyncio.create_task(
                    sdk.research(
                        RunRequest.model_validate(REQUEST),
                        operation_id="screen-sp500",
                        thread_id=THREAD,
                    )
                )
                await started(service, original)
                original.cancel()
                with pytest.raises(asyncio.CancelledError):
                    await original
            else:
                async with Client(create_server(sdk.supervisor)) as mcp:
                    original = asyncio.create_task(
                        mcp.call_tool(
                            "epoch_run",
                            {
                                **REQUEST,
                                "operation_id": "screen-sp500",
                                "thread_id": THREAD,
                            },
                        )
                    )
                    await started(service, original)
                    original.cancel()
                    with pytest.raises(asyncio.CancelledError):
                        await original
        assert "response_version" not in service.record
        service.complete()
        service.snapshot["values"] = {"authority_turn_id": "user-turn:later-query"}
        service.graph_calls.clear()
        async with service.client() as sdk:
            if mode == "sdk":
                result = await sdk.research(
                    RunRequest.model_validate(REQUEST),
                    operation_id="screen-sp500",
                    thread_id=THREAD,
                )
                assert isinstance(result, ResearchCompleted) and result.response.version == 1
            else:
                async with Client(create_server(sdk.supervisor)) as mcp:
                    result = await mcp.call_tool(
                        "epoch_run",
                        {**REQUEST, "operation_id": "screen-sp500", "thread_id": THREAD},
                    )
                    assert result.structured_content["response"]["version"] == 1
        assert service.submissions == 1 and service.graph_calls == []

    asyncio.run(scenario())


def test_pending_questions_and_original_failure_are_read_from_the_recorded_run():
    async def scenario():
        service = Service()
        async with service.client() as sdk:
            task = asyncio.create_task(
                sdk.research(
                    RunRequest.model_validate(REQUEST),
                    operation_id="screen-sp500",
                    thread_id=THREAD,
                )
            )
            await started(service, task)
            task.cancel()
            with pytest.raises(asyncio.CancelledError):
                await task
        service.graph_status = "interrupted"
        service.snapshot.update(interrupts=[INTERRUPT])
        async with service.client() as sdk:
            pending = await sdk.research_status(operation_id="screen-sp500")
            assert isinstance(pending, NeedsInput)
            assert pending.handle.run_id == RUN and pending.handle.operation_id == "screen-sp500"
            assert "Which period?" in pending.feedback()
        service.graph_status = "error"
        service.snapshot["values"] = {"authority_turn_id": "user-turn:later-query"}
        async with service.client() as sdk:
            with pytest.raises(ResearchError) as failure:
                await sdk.research_status(operation_id="screen-sp500")
            assert failure.value.error.code == "EXECUTION_FAILED"
        service.graph_calls.clear()
        async with service.client() as sdk:
            with pytest.raises(ResearchError):
                await sdk.research_status(operation_id="screen-sp500")
        assert service.graph_calls == [] and service.submissions == 1

    asyncio.run(scenario())


def test_changed_input_conflicts_and_prepared_execution_reconnect_does_not_call_graph():
    async def scenario():
        service = Service()
        async with service.client() as sdk:
            task = asyncio.create_task(
                sdk.research(
                    RunRequest.model_validate(REQUEST),
                    operation_id="screen-sp500",
                    thread_id=THREAD,
                )
            )
            await started(service, task)
            task.cancel()
            with pytest.raises(asyncio.CancelledError):
                await task
            with pytest.raises(EpochError) as conflict:
                await sdk.research(
                    RunRequest.model_validate({**REQUEST, "task": "Different task"}),
                    operation_id="screen-sp500",
                    thread_id=THREAD,
                )
            assert conflict.value.error.code == "IDEMPOTENCY_CONFLICT"
            service.complete()
            service.graph_calls.clear()
            first = await sdk.execute_saved(
                "screen-sp500",
                period=DatePeriodConfig(start="2025-01-01"),
                operation_id="refresh-sp500",
            )
        async with service.client() as fresh:
            second = await fresh.execute_saved(
                SavedStudy(study_id="study-one", source_execution_id="new", thread_id=THREAD),
                period=DatePeriodConfig(start="2025-01-01"),
                operation_id="refresh-sp500",
            )
            assert first.execution.id == second.execution.id == "repeat-one"
            assert service.jobs == 1 and service.graph_calls == []

    asyncio.run(scenario())


def test_optional_launch_and_execution_metadata_are_omitted_from_native_wire():
    async def scenario():
        service = Service()
        async with service.client() as sdk:
            task = asyncio.create_task(
                sdk.research(RunRequest.model_validate(REQUEST), operation_id="screen-sp500")
            )
            await started(service, task)
            assert "thread_id" not in service.record["launch"]
            task.cancel()
            with pytest.raises(asyncio.CancelledError):
                await task
            await sdk.execute_saved(
                SavedStudy(study_id="study-one", source_execution_id="new"),
                period=DatePeriodConfig(start="2025-01-01"),
                operation_id="refresh-one",
            )
            assert "thread_id" not in service.execution_record["request"]

    asyncio.run(scenario())


@pytest.mark.parametrize("mode", ["sdk", "mcp"])
def test_rejected_plan_period_is_not_reported_as_a_duplicate_operation(mode):
    async def scenario():
        service = Service()
        calls = []
        reason = "This verified plan does not allow a different period."

        def backend(request):
            calls.append((request.method, request.url.path))
            if request.method == "POST":
                assert request.url.path == "/api/v1/integration/execution-requests"
                return httpx.Response(
                    409,
                    json={
                        "error": "Conflict",
                        "message": reason,
                        "timestamp": "2026-10-19T00:00:00Z",
                    },
                )
            assert request.method == "GET" and request.url.path.endswith("/by-handle/later-period")
            return httpx.Response(
                404,
                json={
                    "error": "NotFound",
                    "message": "Execution operation not found.",
                    "timestamp": "2026-10-19T00:00:00Z",
                },
            )

        service.backend_handler = backend
        source = SavedStudy(
            study_id="study-one",
            source_execution_id="new",
            thread_id=THREAD,
            response_plan=ResponsePlanReference(plan_id="rpl_" + "a" * 64, version=1),
        )
        async with service.client() as sdk:
            if mode == "sdk":
                with pytest.raises(EpochError) as failure:
                    await sdk.execute_saved(
                        source,
                        period=DatePeriodConfig(start="2026-01-01"),
                        operation_id="later-period",
                    )
                detail = failure.value.error
            else:
                async with Client(create_server(sdk.supervisor)) as client:
                    response = await client.call_tool(
                        "epoch_execute",
                        {
                            "reference": source.model_dump(mode="json", exclude_none=True),
                            "period": {"start": "2026-01-01"},
                            "operation_id": "later-period",
                        },
                    )
                from epoch_sdk.contracts import DomainError

                detail = DomainError.model_validate(response.structured_content["error"])
        assert detail.code == "INVALID_STATE" and detail.message == reason
        assert detail.retryable is False
        assert [method for method, _ in calls] == ["POST", "GET"]
        assert service.jobs == 0 and service.graph_calls == []

    asyncio.run(scenario())


def test_existing_execution_operation_with_changed_inputs_remains_a_conflict():
    async def scenario():
        service = Service()
        source = SavedStudy(study_id="study-one", source_execution_id="new")
        async with service.client() as sdk:
            await sdk.execute_saved(
                source, period=DatePeriodConfig(start="2025-01-01"), operation_id="refresh-one"
            )
            with pytest.raises(EpochError) as failure:
                await sdk.execute_saved(
                    source, period=DatePeriodConfig(start="2026-01-01"), operation_id="refresh-one"
                )
        assert failure.value.error.code == "IDEMPOTENCY_CONFLICT"
        assert service.jobs == 1 and service.graph_calls == []

    asyncio.run(scenario())


def test_prepared_execution_waits_for_its_answer_and_reconnects_without_a_graph_call():
    async def scenario():
        service = Service()
        service.record = {"request": REQUEST}
        plan = ResponsePlanReference(plan_id="rpl_" + "a" * 64, version=1)
        source = SavedStudy(
            study_id="study-one",
            source_execution_id="new",
            thread_id=THREAD,
            response_plan=plan,
        )
        async with service.client() as sdk:
            waiting = await sdk.execute_saved(
                source, period=DatePeriodConfig(start="2025-01-01"), operation_id="prepared-one"
            )
            # The engine is already complete, but native publication has not finished.
            assert isinstance(waiting, ExecutionAccepted)
            assert service.execution_record["request"]["response_plan"] == plan.to_wire()
        service.response.update(primary_execution_id="repeat-one", response_plan=plan.to_wire())
        service.execution_record.update(
            response_phase="outputs_recorded",
            response_id=service.response["response_id"],
            response_version=1,
        )
        async with service.client() as fresh:
            finished = await fresh.execution_operation("prepared-one")
            repeated = await fresh.execute_saved(
                source, period=DatePeriodConfig(start="2025-01-01"), operation_id="prepared-one"
            )
            assert isinstance(finished, ChosenExecution) and finished.response is not None
            assert finished.response.primary_execution_id == finished.execution.id == "repeat-one"
            assert finished.reusable_study.response_plan == plan
            assert repeated == finished
            assert service.jobs == 1 and service.graph_calls == []
            # MCP must preserve the same closed saved-answer contract, while
            # retaining explicit nulls in the user's JSON response data.
            service.record["request"] = copy.deepcopy(REQUEST)
            schema = service.record["request"]["outputs"][0]["schema"]
            schema["properties"]["optional"] = {"type": ["string", "null"]}
            service.response["content"]["outputs"][0]["value"]["optional"] = None
            async with Client(create_server(fresh.supervisor)) as mcp:
                wire = await mcp.call_tool(
                    "epoch_status", {"operation_id": "prepared-one", "kind": "execute"}
                )
                assert not wire.is_error
                parsed = ChosenExecution.model_validate(wire.structured_content)
                assert parsed.response is not None
                assert parsed.response.content.outputs[0].value["optional"] is None
                assert (
                    "description"
                    not in wire.structured_content["response"]["content"]["declarations"][0]
                )

    asyncio.run(scenario())


@pytest.mark.parametrize(
    "change",
    [
        {"primary_execution_id": "another-job"},
        {"response_plan": {"plan_id": "rpl_" + "b" * 64, "version": 1}},
        {"thread_id": "another-thread"},
    ],
)
def test_prepared_execution_rejects_a_published_answer_from_another_source(change):
    async def scenario():
        service = Service()
        service.record = {"request": REQUEST}
        plan = ResponsePlanReference(plan_id="rpl_" + "a" * 64, version=1)
        async with service.client() as sdk:
            await sdk.execute_saved(
                SavedStudy(
                    study_id="study-one",
                    source_execution_id="new",
                    thread_id=THREAD,
                    response_plan=plan,
                ),
                period=DatePeriodConfig(start="2025-01-01"),
                operation_id="prepared-one",
            )
            service.response.update(primary_execution_id="repeat-one", response_plan=plan.to_wire())
            service.response.update(change)
            service.execution_record.update(
                response_phase="outputs_recorded",
                response_id=service.response["response_id"],
                response_version=1,
            )
            with pytest.raises(EpochError, match="exact admitted plan/source") as mismatch:
                await sdk.execution_operation("prepared-one")
            assert mismatch.value.error.code == "INVALID_STATE"
            assert service.jobs == 1 and service.graph_calls == []

    asyncio.run(scenario())


def test_lower_level_supervisor_execution_cannot_skip_a_prepared_response_plan():
    async def scenario():
        service = Service()
        async with service.client() as sdk:
            with pytest.raises(ValueError, match="EpochClient.execute_saved"):
                await sdk.supervisor.execute_saved(
                    SavedStudy(
                        study_id="study-one",
                        source_execution_id="new",
                        response_plan=ResponsePlanReference(plan_id="rpl_" + "a" * 64, version=1),
                    ),
                    period=DatePeriodConfig(start="2025-01-01"),
                )
            assert service.jobs == 0 and service.graph_calls == []

    asyncio.run(scenario())


async def admitted(service):
    async with service.client() as sdk:
        task = asyncio.create_task(
            sdk.research(
                RunRequest.model_validate(REQUEST), operation_id="screen-sp500", thread_id=THREAD
            )
        )
        await started(service, task)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task


def test_stale_admission_reattaches_when_the_winner_has_already_reached_clarification():
    async def scenario():
        service = Service()
        await admitted(service)
        service.graph_status = "interrupted"
        service.snapshot["interrupts"] = [INTERRUPT]
        service.stale_admission = True
        service.stale_reads = 1
        service.release.set()
        async with service.client() as fresh:
            result = await fresh.research(
                RunRequest.model_validate(REQUEST), operation_id="screen-sp500", thread_id=THREAD
            )
        assert isinstance(result, NeedsInput) and service.submissions == 1

    asyncio.run(scenario())


def test_duplicate_question_observers_converge_when_one_phase_hint_loses_the_cas():
    async def scenario():
        service = Service()
        await admitted(service)
        service.graph_status = "interrupted"
        service.snapshot["interrupts"] = [INTERRUPT]
        barrier = asyncio.Event()
        reads = 0

        async def backend(request):
            nonlocal reads
            response = service.backend(request)
            if (
                request.method == "GET"
                and request.url.path.endswith("/requests/" + REQUEST_ID)
                and reads < 2
            ):
                reads += 1
                if reads == 2:
                    barrier.set()
                await asyncio.wait_for(barrier.wait(), timeout=5)
            return response

        service.backend_handler = backend
        async with service.client() as first, service.client() as second:
            results = await asyncio.gather(
                first.research_status(operation_id="screen-sp500"),
                second.research_status(operation_id="screen-sp500"),
            )
        assert all(isinstance(result, NeedsInput) for result in results)
        assert results[0] == results[1] and service.record["phase"] == "needs_input"
        assert service.submissions == 1

    asyncio.run(scenario())


@pytest.mark.parametrize("outcome_kind", ["needs_input", "failure"])
def test_old_run_observation_cannot_change_a_resumed_runs_phase_or_failure(outcome_kind):
    async def scenario():
        service = Service()
        await admitted(service)
        handle = WorkflowHandle(
            thread_id=THREAD,
            request_id=REQUEST_ID,
            assistant_id="epoch-ai",
            run_id=RUN,
            operation_id="screen-sp500",
        )
        outcome = (
            NeedsInput(handle=handle, interrupts=[INTERRUPT])
            if outcome_kind == "needs_input"
            else NoExecution(handle=handle, reason="Old cancelled run")
        )
        service.record["graph_run_id"] = "33333333-3333-4333-8333-333333333333"
        version = service.record["version"]
        async with service.client() as fresh:
            result = await fresh._finish(REQUEST_ID, outcome)
        assert isinstance(result, InProgress)
        assert service.record["phase"] == "active" and "error" not in service.record
        assert service.record["version"] == version and service.submissions == 1

    asyncio.run(scenario())
