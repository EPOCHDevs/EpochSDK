"""Generated-client transport controls; native/provider acceptance is separate."""

import asyncio
import copy
import json
from unittest.mock import AsyncMock

import httpx
import pytest
from langgraph_sdk.client import LangGraphClient
from stratifyx import AsyncStratifyX
from test_execution_extensions import ANSWER, RECORD

from epoch_sdk.contracts import RunRequest
from epoch_sdk.errors import EpochError
from epoch_sdk.research import EpochClient, ResearchCompleted, ResearchError
from epoch_sdk.supervisor import InProgress, PublishedAnswer, SupervisorClient, WorkflowHandle

RESEARCH_ID = "req_" + "b" * 32


def records():
    native = copy.deepcopy(RECORD)
    answer = copy.deepcopy(ANSWER)
    # Synthetic research transport envelope around the existing captured output.
    native["request"]["thread_id"] = answer["thread_id"]
    requested = copy.deepcopy(answer["content"]["declarations"])
    for part in requested:
        if part["type"] == "table":
            for column in part["schema"]:
                if column.get("nullable") is False:
                    column.pop("nullable")
        if part["type"] == "text" and part.get("format") == "plain":
            part.pop("format")
    research = {
        "request_id": RESEARCH_ID,
        "operation_id": "saved-order-review",
        "version": 3,
        "created_at_ms": 1,
        "updated_at_ms": 2,
        "phase": "outputs_recorded",
        "request": {
            "task": "Review the recorded orders in this saved result.",
            "outputs": requested,
        },
        "runtime": {
            "thread_id": answer["thread_id"],
            "assistant_id": "epoch-ai",
            "execution_ids_before": [],
            "outcome_ids_before": [],
        },
        "current_execution_id": native["execution_id"],
        "native_execution_request_id": native["request_id"],
        "response_id": answer["response_id"],
        "response_version": 1,
    }
    return research, native, answer


@pytest.mark.parametrize("phase", ["pending", "complete", "failed"])
def test_research_reconnect_uses_only_backend_pins_and_never_the_latest_graph_turn(phase):
    async def scenario():
        research, native, answer = records()
        if phase != "complete":
            research.pop("response_id")
            research.pop("response_version")
            research["phase"] = "active"
        if phase == "failed":
            research["phase"] = "failed"
            research["error"] = {
                "error": {
                    "code": "EXECUTION_FAILED",
                    "message": "Declared output failed.",
                    "retryable": False,
                }
            }
        calls = []

        def backend(request):
            calls.append(request)
            assert request.method == "GET"
            assert request.headers["Authorization"] == "Bearer fixture"
            if request.url.path == f"/api/v1/integration/requests/{RESEARCH_ID}":
                return httpx.Response(200, json=research)
            if request.url.path == f"/api/v1/integration/execution-requests/{native['request_id']}":
                return httpx.Response(200, json=native)
            assert request.url.path == f"/api/v1/research/responses/{answer['response_id']}"
            assert request.url.params["version"] == "1"
            return httpx.Response(200, json=answer)

        def graph(request):
            raise AssertionError("Research reconnect must not depend on the current conversation")

        async with (
            httpx.AsyncClient(transport=httpx.MockTransport(backend)) as native_http,
            httpx.AsyncClient(
                base_url="https://graph.invalid", transport=httpx.MockTransport(graph)
            ) as graph_http,
        ):
            client = EpochClient(
                SupervisorClient(
                    LangGraphClient(graph_http),
                    AsyncStratifyX(
                        base_url="https://backend.invalid",
                        token="fixture",
                        httpx_client=native_http,
                    ),
                )
            )
            if phase == "failed":
                with pytest.raises(ResearchError) as failure:
                    await client.research_status(RESEARCH_ID)
                assert failure.value.request_id == RESEARCH_ID
                assert failure.value.error.code == "EXECUTION_FAILED"
            else:
                result = await client.research_status(RESEARCH_ID)
                if phase == "pending":
                    assert isinstance(result, InProgress)
                    assert result.handle.request_id == RESEARCH_ID
                    assert len(calls) == 1
                else:
                    assert isinstance(result, ResearchCompleted)
                    assert result.request_id == RESEARCH_ID != result.response.request_id
                    assert result.response.request_id == native["request_id"]
                    assert result.response.to_wire() == answer
                    assert result.reusable_study is None
                    reconnected = await client.research_status(RESEARCH_ID)
                    assert isinstance(reconnected, ResearchCompleted)
                    assert reconnected.response == result.response

    asyncio.run(scenario())


@pytest.mark.parametrize(
    "change", ["answer-id", "version", "provenance", "thread", "missing-outputs", "native-pin"]
)
def test_adoption_does_not_relax_exact_native_answer_validation(change):
    async def scenario():
        research, native, answer = records()
        if change == "answer-id":
            answer["request_id"] = RESEARCH_ID
        if change == "version":
            answer["version"] = 2
        if change == "provenance":
            answer["extension"]["config_sha256"] = "f" * 64
        if change == "thread":
            native["request"]["thread_id"] = "another-thread"
        if change == "missing-outputs":
            native.pop("extension_outputs")
        if change == "native-pin":
            native["response_version"] = 2

        def backend(request):
            assert request.method == "GET"
            if "/research/responses/" in request.url.path:
                return httpx.Response(200, json=answer)
            return httpx.Response(
                200, json=native if "/execution-requests/" in request.url.path else research
            )

        async with (
            httpx.AsyncClient(transport=httpx.MockTransport(backend)) as native_http,
            httpx.AsyncClient(
                base_url="https://graph.invalid",
                transport=httpx.MockTransport(
                    lambda request: pytest.fail("No graph call is allowed")
                ),
            ) as graph_http,
        ):
            client = EpochClient(
                SupervisorClient(
                    LangGraphClient(graph_http),
                    AsyncStratifyX(
                        base_url="https://backend.invalid",
                        token="fixture",
                        httpx_client=native_http,
                    ),
                )
            )
            with pytest.raises(ResearchError):
                await client.research_status(RESEARCH_ID)

    asyncio.run(scenario())


def test_supervisor_terminal_selection_accepts_the_linked_original_request_identity():
    async def scenario():
        research, native, answer = records()
        thread = answer["thread_id"]

        def graph(request):
            raise AssertionError(
                "A later or failed graph turn cannot hide the linked native result"
            )

        def backend(request):
            assert request.method == "GET"
            return httpx.Response(
                200, json=answer if "/responses/" in request.url.path else research
            )

        async with (
            httpx.AsyncClient(transport=httpx.MockTransport(backend)) as native_http,
            httpx.AsyncClient(
                base_url="https://graph.invalid", transport=httpx.MockTransport(graph)
            ) as graph_http,
        ):
            supervisor = SupervisorClient(
                LangGraphClient(graph_http),
                AsyncStratifyX(
                    base_url="https://backend.invalid", token="fixture", httpx_client=native_http
                ),
            )
            result = await supervisor.status(
                WorkflowHandle(
                    thread_id=thread,
                    request_id=RESEARCH_ID,
                    assistant_id="epoch-ai",
                    operation_id="saved-order-review",
                    run_id="later-graph-run",
                )
            )
            assert isinstance(result, PublishedAnswer)
            assert result.handle.request_id == RESEARCH_ID
            assert result.response.request_id == native["request_id"]

    asyncio.run(scenario())


def test_concurrent_native_link_after_runtime_cas_conflict_never_starts_a_graph(monkeypatch):
    async def scenario():
        research, native, answer = records()
        for field in [
            "runtime",
            "native_execution_request_id",
            "current_execution_id",
            "response_id",
            "response_version",
        ]:
            research.pop(field)
        research["phase"] = "accepted"
        patches = []

        def backend(request):
            if request.method == "PATCH":
                patches.append(json.loads(request.content))
                research.update(
                    phase="active",
                    version=5,
                    runtime={
                        "thread_id": answer["thread_id"],
                        "assistant_id": "epoch-ai",
                        "execution_ids_before": [],
                        "outcome_ids_before": [],
                    },
                    native_execution_request_id=native["request_id"],
                    current_execution_id=native["execution_id"],
                )
                return httpx.Response(
                    409, json={"message": "A concurrent native admission retained the runtime"}
                )
            assert request.method in {"POST", "GET"}
            return httpx.Response(200, json=copy.deepcopy(research))

        async with (
            httpx.AsyncClient(transport=httpx.MockTransport(backend)) as native_http,
            httpx.AsyncClient(
                base_url="https://graph.invalid",
                transport=httpx.MockTransport(
                    lambda request: pytest.fail(
                        "No graph transport is allowed after the native link"
                    )
                ),
            ) as graph_http,
        ):
            supervisor = SupervisorClient(
                LangGraphClient(graph_http),
                AsyncStratifyX(
                    base_url="https://backend.invalid", token="fixture", httpx_client=native_http
                ),
            )
            prepare = AsyncMock(
                return_value=WorkflowHandle(
                    thread_id=answer["thread_id"], request_id=RESEARCH_ID, assistant_id="epoch-ai"
                )
            )
            start = AsyncMock(
                side_effect=AssertionError("A linked native operation must not start a graph")
            )
            monkeypatch.setattr(supervisor, "prepare_operation", prepare)
            monkeypatch.setattr(supervisor, "start_operation", start)
            result = await EpochClient(supervisor).research(
                RunRequest.model_validate(research["request"]), operation_id="saved-order-review"
            )
            assert isinstance(result, InProgress)
            assert result.handle.request_id == RESEARCH_ID
            assert len(patches) == 1
            start.assert_not_called()

    asyncio.run(scenario())


@pytest.mark.parametrize("missing", [None, "job", "snapshot", "denied", "wrong-identity"])
def test_first_study_report_retains_original_replay_and_survives_missing_optional_source(missing):
    async def scenario():
        research, native, answer = records()
        research["source_execution_id"] = native["request"]["source_execution_id"]
        original_id = research["source_execution_id"]
        calls = []
        def backend(request):
            calls.append(request)
            path = request.url.path
            assert request.method == "GET"
            if path == f"/api/v1/integration/requests/{RESEARCH_ID}":
                return httpx.Response(200, json=research)
            if path == f"/api/v1/integration/execution-requests/{native['request_id']}":
                return httpx.Response(200, json=native)
            if path == f"/api/v1/research/responses/{answer['response_id']}":
                return httpx.Response(200, json=answer)
            kind = "snapshot" if path.endswith("/study") else "job"
            assert path in {f"/api/v1/studies/executions/{original_id}", f"/api/v1/studies/executions/{original_id}/study"}
            if kind == missing:
                return httpx.Response(404, json={"error": "DataNotFound", "message": "Removed original metadata", "timestamp": "2026-10-23T00:00:00Z"})
            if kind == "job" and missing == "denied":
                return httpx.Response(403, json={"error": "Forbidden", "message": "Not owned", "timestamp": "2026-10-23T00:00:00Z"})
            if kind == "job":
                return httpx.Response(200, json={"id": original_id, "definition_id": "original-study", "created_at": 1, "execution_type": "research", "status": "completed"})
            return httpx.Response(200, json={"execution_id": "wrong" if missing == "wrong-identity" else original_id, "definition_id": "original-study", "captured_at": 1,
                "study": {"name": "Original", "description": "Transport control", "source": "retained_fixture()", "data": {"assets": []}, "authoring_origin": "agent"}})
        def graph(request):
            raise AssertionError("Saved research read must not run a supervisor")
        async with httpx.AsyncClient(transport=httpx.MockTransport(backend)) as http, httpx.AsyncClient(base_url="https://graph.invalid", transport=httpx.MockTransport(graph)) as graph_http:
            client = EpochClient(SupervisorClient(LangGraphClient(graph_http), AsyncStratifyX(base_url="https://backend.invalid", token="fixture", httpx_client=http)))
            if missing in {"denied", "wrong-identity"}:
                with pytest.raises(EpochError):
                    await client.research_status(RESEARCH_ID)
                return
            result = await client.research_status(RESEARCH_ID)
            assert isinstance(result, ResearchCompleted) and result.response.to_wire() == answer
            if missing:
                assert result.reusable_study is None
            else:
                assert result.reusable_study.source_execution_id == original_id
                assert result.reusable_study.study_id == "original-study"
                assert result.reusable_study.report_template.request_id == native["request_id"]
                assert result.reusable_study.response_plan is None
            assert all(request.method == "GET" for request in calls)
    asyncio.run(scenario())
