from __future__ import annotations

import asyncio
import copy
import json
from contextlib import asynccontextmanager

import httpx
import pytest
from langgraph_sdk.client import LangGraphClient
from mcp import Client
from stratifyx import AsyncStratifyX
from test_supervisor import INTERRUPT, RUN, THREAD, job

from epoch_sdk import RunRequest
from epoch_sdk.mcp import create_server
from epoch_sdk.research import EpochClient, ResearchCompleted, ResearchError
from epoch_sdk.supervisor import Answer, Answers, NeedsInput, SupervisorClient

REQUEST_ID = "req_" + "1" * 32
REQUEST = {
    "task": "Compare sales",
    "context": ["Annual values"],
    "outputs": [
        {
            "name": "answer",
            "type": "json",
            "schema": {
                "type": "object",
                "properties": {"rows": {"type": "integer", "description": "Row count"}},
                "required": ["rows"],
                "additionalProperties": False,
            },
        }
    ],
    "parameters": {"period": {"start": "2024-01-01", "end": "2024-12-31"}},
}


def saved_response():
    return {
        "response_id": "rsp_" + "1" * 64,
        "request_id": REQUEST_ID,
        "thread_id": THREAD,
        "primary_execution_id": "new",
        "study_id": "study-one",
        "version": 1,
        "published_at_ms": 1,
        "content": {
            "declarations": REQUEST["outputs"],
            "outputs": [
                {"name": "answer", "type": "json", "value": {"rows": 2}},
            ],
        },
    }


@asynccontextmanager
async def clients(
    *,
    interrupt=False,
    missing_response=False,
    terminal_failure=False,
    no_execution=False,
    publication_error=None,
):
    def answer():
        value = saved_response()
        if no_execution:
            value.pop("primary_execution_id")
            value.pop("study_id")
        return value

    records = {}
    graph_calls = []
    backend_calls = []
    waits = 0

    def backend(request):
        backend_calls.append(request)
        path = request.url.path
        assert request.headers["Authorization"] == "Bearer fixture"
        if path == "/api/v1/integration/requests" and request.method == "POST":
            accepted = json.loads(request.content)["request"]
            records.update(
                {
                    "request_id": REQUEST_ID,
                    "version": 0,
                    "created_at_ms": 1,
                    "updated_at_ms": 1,
                    "phase": "accepted",
                    "request": accepted,
                }
            )
            return httpx.Response(200, json=copy.deepcopy(records))
        if path == "/api/v1/integration/requests/" + REQUEST_ID:
            if request.method == "PATCH":
                body = json.loads(request.content)
                assert body.pop("expected_version") == records["version"]
                records.update(body)
                records["version"] += 1
                if "runtime" in body:
                    records["phase"] = "active"
                if "response_version" in body:
                    records["phase"] = "outputs_recorded"
                if "error" in body:
                    records["phase"] = "failed"
            else:
                assert request.method == "GET"
            return httpx.Response(200, json=copy.deepcopy(records))
        if path == "/api/v1/research/responses/" + saved_response()["response_id"]:
            if missing_response:
                return httpx.Response(
                    404,
                    json={
                        "error": "DataNotFound",
                        "message": "No response",
                        "timestamp": "2026-10-18T00:00:00Z",
                    },
                )
            if "version" in request.url.params:
                assert request.url.params["version"] == "1"
            return httpx.Response(200, json=answer())
        if path == "/api/v1/studies/executions/new":
            return httpx.Response(
                200, json=job("new", status="failed" if terminal_failure else "completed")
            )
        raise AssertionError(f"Unexpected native call: {request.method} {path}")

    def graph(request):
        nonlocal waits
        graph_calls.append(request)
        if request.method == "POST" and request.url.path == "/threads":
            return httpx.Response(200, json={"thread_id": THREAD})
        if request.method == "POST" and request.url.path == f"/threads/{THREAD}/runs/wait":
            # Backend accepted the full request/runtime before agent submission.
            assert records["runtime"]["thread_id"] == THREAD
            body = json.loads(request.content)
            waits += 1
            if waits == 1:
                assert body["input"]["sdk_request_id"] == REQUEST_ID
                assert body["input"]["messages"][0]["id"] == REQUEST_ID
                assert "Row count" in body["input"]["messages"][0]["content"]
            else:
                assert "input" not in body and "resume" in body["command"]
            assert body["durability"] == "sync"
            reference = {
                key: value
                for key, value in answer().items()
                if key not in {"content", "published_at_ms"}
            }
            result = {
                "authority_turn_id": "user-turn:" + REQUEST_ID,
                "execution_ids": ["new"],
                "published_response": reference,
            }
            if terminal_failure:
                result.pop("published_response")
                result["next_action_outcomes"] = {
                    "failed": {
                        "tool_call_id": "failed-call",
                        "tool_name": "run_study",
                        "subject": "sales",
                        "status": "failed",
                        "detail": "The selected execution failed.",
                        "execution_id": "new",
                    }
                }
            if publication_error is not None:
                result.pop("published_response")
                result["publication_error"] = {
                    **publication_error,
                    "gaps": None,
                    "questions": None,
                    "recommended_task": None,
                    "data_requirements": None,
                    "access_requirements": None,
                }
            if interrupt and waits == 1:
                result = {
                    "authority_turn_id": "user-turn:" + REQUEST_ID,
                    "__interrupt__": [INTERRUPT],
                }
            return httpx.Response(
                200,
                json=result,
                headers={
                    "Content-Location": f"/threads/{THREAD}/runs/{RUN}",
                },
            )
        raise AssertionError(f"Unexpected graph call: {request.method} {request.url.path}")

    async with (
        httpx.AsyncClient(
            base_url="https://graph.invalid", transport=httpx.MockTransport(graph)
        ) as graph_http,
        httpx.AsyncClient(transport=httpx.MockTransport(backend)) as backend_http,
    ):
        supervisor = SupervisorClient(
            LangGraphClient(graph_http),
            AsyncStratifyX(
                base_url="https://backend.invalid", token="fixture", httpx_client=backend_http
            ),
        )
        yield EpochClient(supervisor), records, graph_calls, backend_calls


def test_research_admits_the_full_contract_and_returns_a_pinned_response():
    async def scenario():
        async with clients() as (sdk, records, _, _):
            result = await sdk.research(RunRequest.model_validate(REQUEST))
            assert isinstance(result, ResearchCompleted)
            assert result.to_wire()["status"] == "succeeded"
            assert result.response.to_wire() == saved_response()
            assert result.request_id == REQUEST_ID
            assert records["request"] == REQUEST
            assert records["current_execution_id"] == "new" and records["response_version"] == 1

    asyncio.run(scenario())


def test_a_fresh_client_reads_completion_without_any_graph_request():
    async def scenario():
        async with clients() as (sdk, _, graph_calls, backend_calls):
            first = await sdk.research(RunRequest.model_validate(REQUEST))
            graph_calls.clear()
            backend_calls.clear()
            fresh = EpochClient(sdk.supervisor)
            read = await fresh.research_status(REQUEST_ID)
            assert first == read and graph_calls == []
            assert all(call.method == "GET" for call in backend_calls)
            assert backend_calls[-1].url.params["version"] == "1"

    asyncio.run(scenario())


def test_research_clarification_resumes_the_same_accepted_request_and_thread():
    async def scenario():
        async with clients(interrupt=True) as (sdk, records, graph_calls, _):
            waiting = await sdk.research(RunRequest.model_validate(REQUEST))
            assert isinstance(waiting, NeedsInput) and records["phase"] == "needs_input"
            fresh = EpochClient(sdk.supervisor)
            result = await fresh.resume_research(
                waiting,
                {
                    "interrupt-one": Answers(
                        answers=[
                            Answer(question_index=0, selected_indices=[0]),
                        ]
                    )
                },
            )
            assert isinstance(result, ResearchCompleted)
            assert result.request_id == waiting.handle.request_id == REQUEST_ID
            assert len([call for call in graph_calls if call.url.path == "/threads"]) == 1
            assert not any(call.method == "DELETE" for call in graph_calls)

    asyncio.run(scenario())


@pytest.mark.parametrize(
    "option,code",
    [
        ("missing_response", "OUTPUT_VALIDATION_FAILED"),
        ("terminal_failure", "EXECUTION_FAILED"),
    ],
)
def test_engine_completion_alone_cannot_certify_response_success(option, code):
    async def scenario():
        async with clients(**{option: True}) as (sdk, records, graph_calls, _):
            with pytest.raises(ResearchError) as error:
                await sdk.research(RunRequest.model_validate(REQUEST))
            assert error.value.request_id == REQUEST_ID
            assert error.value.execution_id == "new" and error.value.error.code == code
            assert records["phase"] == "failed" and "response_version" not in records
            graph_calls.clear()
            with pytest.raises(ResearchError) as reopened:
                await EpochClient(sdk.supervisor).research_status(REQUEST_ID)
            assert reopened.value.response == error.value.response
            assert graph_calls == []

    asyncio.run(scenario())


@pytest.mark.parametrize("mode", ["sdk", "mcp"])
def test_publication_service_failure_keeps_its_code_in_fresh_request_reads(mode):
    failure = {
        "code": "TEMPORARILY_UNAVAILABLE",
        "message": "Epoch could not confirm the saved answer.",
        "retryable": False,
    }

    async def scenario():
        async with clients(publication_error=failure) as (sdk, records, graph_calls, _):
            if mode == "sdk":
                with pytest.raises(ResearchError) as raised:
                    await sdk.research(RunRequest.model_validate(REQUEST))
                assert raised.value.error.to_wire() == failure
            else:
                async with Client(create_server(sdk.supervisor)) as mcp:
                    result = await mcp.call_tool("epoch_research", {"request": REQUEST})
                    assert result.structured_content["error"] == failure
                    assert result.structured_content["request_id"] == REQUEST_ID
            assert records["phase"] == "failed"
            assert records["error"]["error"] == failure
            assert "response_version" not in records
            graph_calls.clear()
            with pytest.raises(ResearchError) as reopened:
                await EpochClient(sdk.supervisor).research_status(REQUEST_ID)
            assert reopened.value.error.to_wire() == failure
            assert graph_calls == []

    asyncio.run(scenario())


def test_prepared_work_is_explicitly_separate_from_research():
    async def scenario():
        async with clients() as (sdk, _, graph_calls, backend_calls):
            request = RunRequest.model_validate({**REQUEST, "study_id": "study-one"})
            with pytest.raises(ValueError, match="separate"):
                await sdk.research(request)
            assert not graph_calls and not backend_calls

    asyncio.run(scenario())


def test_mcp_research_uses_the_same_completion_and_fresh_status_path():
    async def scenario():
        async with (
            clients() as (sdk, _, graph_calls, _),
            Client(create_server(sdk.supervisor)) as mcp,
        ):
            result = await mcp.call_tool("epoch_research", {"request": REQUEST})
            assert not result.is_error and result.structured_content["status"] == "succeeded"
            assert result.structured_content["response"] == saved_response()
            graph_calls.clear()
            fresh = await mcp.call_tool("epoch_research_status", {"request_id": REQUEST_ID})
            assert not fresh.is_error and fresh.structured_content == result.structured_content
            assert graph_calls == []

    asyncio.run(scenario())


def test_sdk_can_complete_a_published_answer_without_starting_an_execution():
    async def scenario():
        request = {key: value for key, value in REQUEST.items() if key != "parameters"}
        async with clients(no_execution=True) as (sdk, records, _, calls):
            result = await sdk.research(RunRequest.model_validate(request))
            assert isinstance(result, ResearchCompleted)
            assert result.reusable_study is None
            assert result.response.primary_execution_id is None
            assert records["response_id"] == result.response.response_id
            assert not any("/studies/executions/" in call.url.path for call in calls)

    asyncio.run(scenario())
