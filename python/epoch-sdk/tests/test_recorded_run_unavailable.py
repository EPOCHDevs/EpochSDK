"""A missing recorded graph run is a read failure, not an active operation."""

from __future__ import annotations

import asyncio
import copy
import time

import httpx
import pytest
from test_operation_reconnect import Service
from test_research import REQUEST, REQUEST_ID
from test_supervisor import RUN, THREAD

from epoch_sdk import EpochError, RunRequest
from epoch_sdk.research import ResearchCompleted, ResearchError
from epoch_sdk.supervisor import InProgress, NoExecution


class MissingRunService(Service):
    def __init__(self):
        super().__init__()
        self.missing_run = False
        self.complete_during_read = False
        self.backend_calls = []

    def backend(self, request):
        self.backend_calls.append(request)
        return super().backend(request)

    async def graph(self, request):
        if self.missing_run and request.url.path == f"/threads/{THREAD}/runs/{RUN}":
            self.graph_calls.append(request)
            if self.complete_during_read:
                self.complete()
            return httpx.Response(404, json={"detail": "Run not found"})
        return await super().graph(request)


async def accepted(service, sdk):
    result = await sdk.research(
        RunRequest.model_validate(REQUEST),
        operation_id="recorded-run-status",
        thread_id=THREAD,
        wait=False,
    )
    assert isinstance(result, InProgress)
    assert service.submissions == 1
    service.graph_calls.clear()
    service.backend_calls.clear()


def assert_read_only(service):
    assert service.submissions == 1
    assert service.jobs == 0
    assert all(call.method == "GET" for call in service.graph_calls + service.backend_calls)


async def unavailable(sdk):
    with pytest.raises(ResearchError) as failure:
        await sdk.research_status(REQUEST_ID)
    error = failure.value.response.error
    assert failure.value.response.request_id == REQUEST_ID
    assert error.code == "TEMPORARILY_UNAVAILABLE"
    assert error.retryable is True
    assert "outcome is unknown" in error.message
    assert "do not resubmit" in error.message


def test_missing_recorded_run_never_claims_running_or_persists_a_terminal_failure():
    async def scenario():
        service = MissingRunService()
        async with service.client() as sdk:
            await accepted(service, sdk)
            service.missing_run = True
            before = copy.deepcopy(service.record)
            await unavailable(sdk)
            assert service.record == before
            assert [(call.method, call.url.path) for call in service.graph_calls] == [
                ("GET", f"/threads/{THREAD}/runs/{RUN}")
            ]
            assert_read_only(service)

    asyncio.run(scenario())


@pytest.mark.parametrize("status", ["pending", "running"])
def test_present_pending_and_running_records_remain_in_progress(status):
    async def scenario():
        service = MissingRunService()
        async with service.client() as sdk:
            await accepted(service, sdk)
            service.graph_status = status
            before = copy.deepcopy(service.record)
            result = await sdk.research_status(REQUEST_ID)
            assert isinstance(result, InProgress)
            assert service.record == before
            assert_read_only(service)

    asyncio.run(scenario())


@pytest.mark.parametrize("during_read", [False, True])
@pytest.mark.parametrize("fresh_answer", [False, True])
def test_later_durable_answer_wins_without_recreating_the_missing_run(during_read, fresh_answer):
    async def scenario():
        service = MissingRunService()
        async with service.client() as sdk:
            await accepted(service, sdk)
            service.missing_run = True
            service.complete_during_read = during_read
            await unavailable(sdk)
            if not during_read:
                service.complete()
            if fresh_answer:
                service.record["updated_at_ms"] = int(time.time() * 1000)
            before = copy.deepcopy(service.record)
            service.graph_calls.clear()
            result = await sdk.research_status(REQUEST_ID)
            assert isinstance(result, ResearchCompleted)
            assert result.response.response_id == service.response["response_id"]
            assert service.record == before
            # Preserve the existing turn-end check for a recently published
            # answer. Its missing run establishes turn end, not answer failure.
            assert len(service.graph_calls) == int(fresh_answer)
            assert_read_only(service)

    asyncio.run(scenario())


@pytest.mark.parametrize("by", ["request", "operation", "supervisor"])
def test_missing_run_preserves_the_real_exception_boundary_and_original_cause(by):
    async def scenario():
        service = MissingRunService()
        async with service.client() as sdk:
            await accepted(service, sdk)
            service.missing_run = True
            expected = ResearchError if by == "request" else EpochError
            with pytest.raises(expected) as caught:
                if by == "request":
                    await sdk.research_status(REQUEST_ID)
                elif by == "operation":
                    await sdk.research_status(operation_id="recorded-run-status")
                else:
                    from epoch_sdk.research_operations import ResearchRecord

                    await sdk.supervisor.status(sdk._handle(ResearchRecord.model_validate(service.record)))
            error = caught.value.__cause__ if by in {"request", "operation"} else caught.value
            assert isinstance(error, EpochError)
            assert error.error.code == "TEMPORARILY_UNAVAILABLE"
            assert isinstance(error.__cause__, httpx.HTTPStatusError)
            assert error.__cause__.response.status_code == 404
            assert_read_only(service)

    asyncio.run(scenario())


@pytest.mark.parametrize("status", ["error", "timeout"])
def test_actual_terminal_graph_errors_remain_distinct_from_missing_runs(status):
    async def scenario():
        from epoch_sdk.research_operations import ResearchRecord

        service = MissingRunService()
        async with service.client() as sdk:
            await accepted(service, sdk)
            service.graph_status = status
            result = await sdk.supervisor.status(sdk._handle(ResearchRecord.model_validate(service.record)))
            assert isinstance(result, NoExecution)
            assert result.reason == "The accepted native graph run failed."
            assert_read_only(service)

    asyncio.run(scenario())


def test_later_durable_error_wins_without_graph_access_or_research_mutation():
    async def scenario():
        service = MissingRunService()
        async with service.client() as sdk:
            await accepted(service, sdk)
            service.missing_run = True
            await unavailable(sdk)
            service.record.update(
                phase="failed",
                error={"error": {
                    "code": "INVALID_REQUEST", "message": "Native build failed.", "retryable": False
                }},
            )
            before = copy.deepcopy(service.record)
            service.graph_calls.clear()
            with pytest.raises(ResearchError) as failure:
                await sdk.research_status(REQUEST_ID)
            assert failure.value.response.error.code == "INVALID_REQUEST"
            assert failure.value.response.error.retryable is False
            assert service.record == before
            assert service.graph_calls == []
            assert_read_only(service)

    asyncio.run(scenario())
