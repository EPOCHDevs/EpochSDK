"""Research completes when the agent's turn ends, with the answer the turn ended with; no live services."""
import asyncio
import time
from copy import deepcopy

import httpx
import pytest
from test_ordinary_native_completion import OPERATION, RESEARCH, client, records

from epoch_sdk.contracts import RunRequest
from epoch_sdk.errors import EpochError
from epoch_sdk.research import TURN_END_LIMIT_MS, ResearchCompleted
from epoch_sdk.supervisor import InProgress

RUN = "run-1"
EDIT = "req_" + "e" * 32


def recorded(*, age_ms: int = 1_000):
    """A research whose outcome Backend recorded age_ms ago, with the native run's original answer."""
    research, native, answer = records()
    research["graph_run_id"] = RUN
    research["updated_at_ms"] = int(time.time() * 1000) - age_ms
    native["output_revision"] = {"execution_id": "ordinary", "version": 1, "sha256": "4" * 64}
    return research, native, answer


def revise(native, answer):
    """The agent's in-turn output edit: revision 2 publishes its answer under the edit's request."""
    revised = deepcopy(answer)
    revised.update(response_id="revised", request_id=EDIT)
    revised["content"]["outputs"][0]["value"] = 8
    native["output_revision"] = {"execution_id": "ordinary", "version": 2, "sha256": "5" * 64}
    native["response_id"] = native["extension_outputs"]["response_id"] = "revised"
    return revised


def serve_backend(research, native, answers, reads):
    def serve(request):
        reads.append(request.url.path)
        assert request.method == "GET"
        mapping = {
            f"/api/v1/integration/requests/{RESEARCH}": research,
            f"/api/v1/integration/execution-requests/{OPERATION}": native,
            **{f"/api/v1/research/responses/{item['response_id']}": item for item in answers},
        }
        return httpx.Response(200, json=mapping[request.url.path])
    return serve


def run_record(status, request_id=RESEARCH):
    return {"run_id": RUN, "thread_id": "thread", "assistant_id": "epoch-ai", "status": status,
            "metadata": {"epoch_sdk_request_id": request_id}, "created_at": "2026-11-19T00:00:00Z",
            "updated_at": "2026-11-19T00:00:00Z", "kwargs": {}, "multitask_strategy": "reject"}


def serve_graph(statuses):
    """A graph whose run reports each status in turn (the last one repeats)."""
    def serve(request):
        assert request.method == "GET" and request.url.path == f"/threads/thread/runs/{RUN}"
        status = statuses.pop(0) if len(statuses) > 1 else statuses[0]
        if status == 404:
            return httpx.Response(404, json={"detail": "Thread not found"})
        return httpx.Response(200, json=run_record(status))
    return serve


async def status(research, native, answers, graph_statuses):
    reads: list[str] = []
    async with httpx.AsyncClient(transport=httpx.MockTransport(
            serve_backend(research, native, answers, reads))) as http, httpx.AsyncClient(
            base_url="https://graph.invalid", transport=httpx.MockTransport(serve_graph(graph_statuses))) as graph:
        return await client(http, graph).research_status(RESEARCH), reads


@pytest.mark.parametrize("run_status", ["pending", "running"])
def test_recorded_outcome_stays_running_until_the_turn_ends(run_status):
    research, native, answer = recorded()
    result, reads = asyncio.run(status(research, native, [answer], [run_status]))
    assert isinstance(result, InProgress)
    assert result.handle.run_id == RUN and result.handle.request_id == RESEARCH
    assert not any("/research/responses/" in path for path in reads)  # No answer is read mid-turn.


@pytest.mark.parametrize("run_status", ["success", "error", "timeout", "interrupted", 404])
def test_an_ended_or_vanished_turn_completes_with_the_answer_it_ended_with(run_status):
    research, native, answer = recorded()
    result, _ = asyncio.run(status(research, native, [answer], [run_status]))
    assert isinstance(result, ResearchCompleted)
    assert result.response.to_wire() == answer


def test_a_turn_that_never_ends_completes_after_the_limit():
    research, native, answer = recorded(age_ms=TURN_END_LIMIT_MS + 1)
    result, _ = asyncio.run(status(research, native, [answer], ["running"]))
    assert isinstance(result, ResearchCompleted)
    assert result.response.to_wire() == answer


def test_another_requests_run_cannot_hold_back_the_outcome():
    research, native, answer = recorded()

    def other(request):
        return httpx.Response(200, json=run_record("running", request_id="req_" + "f" * 32))

    async def scenario():
        reads: list[str] = []
        async with httpx.AsyncClient(transport=httpx.MockTransport(
                serve_backend(research, native, [answer], reads))) as http, httpx.AsyncClient(
                base_url="https://graph.invalid", transport=httpx.MockTransport(other)) as graph:
            return await client(http, graph).research_status(RESEARCH)
    assert isinstance(asyncio.run(scenario()), ResearchCompleted)


def test_the_agents_in_turn_revision_is_the_answer():
    research, native, answer = recorded()
    revised = revise(native, answer)
    result, reads = asyncio.run(status(research, native, [answer, revised], ["success"]))
    assert isinstance(result, ResearchCompleted)
    assert result.response.to_wire() == revised
    assert result.response.response_id == "revised"
    assert "/api/v1/research/responses/answer" not in reads  # The superseded answer is not read.


def test_a_revision_that_drops_the_answer_is_an_output_failure():
    research, native, answer = recorded()
    revise(native, answer)
    native["response_id"] = native["response_version"] = None
    native["extension_outputs"]["response_id"] = native["extension_outputs"]["response_version"] = None
    with pytest.raises(EpochError) as raised:
        asyncio.run(status(research, native, [answer], ["success"]))
    assert raised.value.error.code == "OUTPUT_VALIDATION_FAILED"


@pytest.mark.parametrize("change", ["provenance", "execution", "thread"])
def test_a_revised_answer_must_still_belong_to_the_run(change):
    research, native, answer = recorded()
    revised = revise(native, answer)
    if change == "provenance":
        revised["extension"] = {**revised["extension"], "config_sha256": "9" * 64}
    if change == "execution":
        revised["primary_execution_id"] = "another-job"
    if change == "thread":
        revised["thread_id"] = "another-thread"
    with pytest.raises((EpochError, ValueError)):
        asyncio.run(status(research, native, [answer, revised], ["success"]))


def test_waiting_reattach_follows_the_turn_to_its_revised_answer():
    research, native, answer = recorded()
    research["operation_id"] = "question"
    research["request"] = {**research["request"], "context": [], "auto_ingest": False}
    revised = deepcopy(answer)
    joined = []

    def backend(request):
        if request.method == "POST":
            assert request.url.path == "/api/v1/integration/requests"
            return httpx.Response(200, json=research)
        mapping = {
            f"/api/v1/integration/requests/{RESEARCH}": research,
            f"/api/v1/integration/execution-requests/{OPERATION}": native,
            "/api/v1/research/responses/answer": answer,
            "/api/v1/research/responses/revised": revised,
        }
        return httpx.Response(200, json=mapping[request.url.path])

    def graph(request):
        if request.url.path.endswith("/join"):
            # The agent revises its answer, then the turn ends.
            joined.append(request.url.path)
            revised.update(revise(native, answer))
            return httpx.Response(200, json={})
        assert request.url.path == f"/threads/thread/runs/{RUN}"
        return httpx.Response(200, json=run_record("success" if joined else "running"))

    async def scenario():
        async with httpx.AsyncClient(transport=httpx.MockTransport(backend)) as http, httpx.AsyncClient(
                base_url="https://graph.invalid", transport=httpx.MockTransport(graph)) as graph_http:
            return await client(http, graph_http).research(
                RunRequest.model_validate(research["request"]), operation_id="question", wait=True)
    result = asyncio.run(scenario())
    assert joined == [f"/threads/thread/runs/{RUN}/join"]
    assert isinstance(result, ResearchCompleted)
    assert result.response.response_id == "revised"
