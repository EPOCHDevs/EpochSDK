"""Generated-client transport controls for one authored ordinary study; no live services."""
import asyncio
from copy import deepcopy
from datetime import date
import json

import httpx
from langgraph_sdk.client import LangGraphClient
import pytest
from stratifyx import AsyncStratifyX, DatePeriodConfig, ExecutionOptions

from epoch_sdk.errors import EpochError
from epoch_sdk.research import EpochClient, ExecutionAccepted, ResearchCompleted
from epoch_sdk.supervisor import ChosenExecution, SavedStudy, SupervisorClient

RESEARCH = "req_" + "b" * 32
OPERATION = "req_" + "a" * 32
BINDINGS = {"threshold": {"type": "Integer", "value": "7"}}
PERIOD = {"start": "2024-01-01", "end": "2024-12-31"}
COST = {"default_model": {"type": "None", "args": {}},
        "asset_class_overrides": {}, "symbol_overrides": {}}
TRADING = {"cash": 123456, "currency": "USD",
           "commission": {**COST, "default_model": {"type": "Bps", "args": {"bps": 10}}}, "slippage": COST,
           "futures_tick_snapshot": {"rules": [], "snapshot_id": "0" * 64, "working_orders_on_change": "Reject"}}


def records():
    provenance = {"execution_id": "ordinary", "study_id": "study", "source_execution_id": "",
        "compiled_schema_version": 77, "config_sha256": "1" * 64,
        "input_snapshot_sha256": "2" * 64, "output_declarations_sha256": "3" * 64,
        "execution_parameter_bindings": BINDINGS, "inputs": [], "commentary": []}
    declarations = [{"name": "measurement", "type": "json", "schema": {"type": "integer"}}]
    answer = {"response_id": "answer", "version": 1, "request_id": OPERATION,
        "thread_id": "thread", "primary_execution_id": "ordinary", "study_id": "study",
        "published_at_ms": 1, "extension": provenance,
        "content": {"declarations": declarations,
                    "outputs": [{"name": "measurement", "type": "json", "value": 7}]}}
    native = {"request_id": OPERATION, "execution_id": "ordinary", "created_at_ms": 1,
        "phase": "active", "execution_status": "Completed", "response_phase": "outputs_recorded",
        "response_id": "answer", "response_version": 1,
        "request": {"operation_id": "original", "study_id": "study", "thread_id": "thread",
                    "research_request_id": RESEARCH, "parameters": {"period": PERIOD},
                    "execution_parameter_bindings": BINDINGS},
        "extension_outputs": {"provenance": provenance, "dashboards": [],
            "response_id": "answer", "response_version": 1,
            "text": [{"producer_id": "llm_brief", "value": "Seven observations."}],
            "dashboard_prose": "Computed observations: 7."}}
    research = {"request_id": RESEARCH, "operation_id": "question", "version": 3,
        "created_at_ms": 1, "updated_at_ms": 2, "phase": "outputs_recorded",
        "request": {"task": "Measure observations", "outputs": declarations},
        "runtime": {"thread_id": "thread", "assistant_id": "epoch-ai",
                    "execution_ids_before": [], "outcome_ids_before": []},
        "current_execution_id": "ordinary", "native_execution_request_id": OPERATION,
        "response_id": "answer", "response_version": 1}
    return research, native, answer


def job(identifier="ordinary"):
    return {"id": identifier, "definition_id": "study", "created_at": 1,
        "execution_type": "backtest", "status": "completed", "thread_id": "thread",
        "period": PERIOD, "trading": TRADING}


def snapshot(identifier="ordinary"):
    return {"execution_id": identifier, "definition_id": "study", "captured_at": 1,
        "execution_parameter_bindings": BINDINGS,
        "study": {"name": "Owned original", "description": "Transport control", "source": "fixture()",
                  "data": {"assets": []}, "authoring_origin": "agent"}}


def client(native_http, graph_http):
    return EpochClient(SupervisorClient(LangGraphClient(graph_http), AsyncStratifyX(
        base_url="https://native.invalid", token="fixture", httpx_client=native_http)))


def no_graph(request):
    raise AssertionError("Prepared ordinary work must not invoke a supervisor")


@pytest.mark.parametrize("change", [None, "source", "bindings", "answer"])
def test_ordinary_research_read_retains_one_study_and_rejects_changed_native_pins(change):
    async def scenario():
        research, native, answer = records()
        if change == "source":
            research["source_execution_id"] = "invented-original"
        if change == "bindings":
            native["request"]["execution_parameter_bindings"] = {"threshold": {"type": "Integer", "value": "8"}}
        if change == "answer":
            answer["primary_execution_id"] = "another-job"
        calls = []
        def serve(request):
            calls.append(request)
            assert request.method == "GET"
            mapping = {
                f"/api/v1/integration/requests/{RESEARCH}": research,
                f"/api/v1/integration/execution-requests/{OPERATION}": native,
                "/api/v1/research/responses/answer": answer,
            }
            return httpx.Response(200, json=mapping[request.url.path])
        async with httpx.AsyncClient(transport=httpx.MockTransport(serve)) as http, httpx.AsyncClient(
            base_url="https://graph.invalid", transport=httpx.MockTransport(no_graph)) as graph:
            owner = client(http, graph)
            if change:
                with pytest.raises((EpochError, ValueError)):
                    await owner.research_status(RESEARCH)
            else:
                result = await owner.research_status(RESEARCH)
                assert isinstance(result, ResearchCompleted)
                assert result.response.to_wire() == answer
                assert result.reusable_study == SavedStudy(study_id="study", source_execution_id="ordinary", thread_id="thread")
                assert result.reusable_study.report_template is None
            assert all(request.method == "GET" for request in calls)
    asyncio.run(scenario())


@pytest.mark.parametrize("source_state", ["missing", "drifted"])
def test_fresh_ordinary_admission_requires_its_actual_owned_source_snapshot(source_state):
    async def scenario():
        calls = []
        def serve(request):
            calls.append(request)
            assert request.method == "GET", "An unverified fresh source must not launch work"
            if "by-handle" in request.url.path or (source_state == "missing" and request.url.path.endswith("/ordinary")):
                return httpx.Response(404, json={"error":"DataNotFound", "message":"Source unavailable",
                    "timestamp":"2026-10-27T00:00:00Z"})
            if request.url.path.endswith("/study"):
                return httpx.Response(200, json={**snapshot(), "definition_id":"another-study"})
            return httpx.Response(200, json=job())
        async with httpx.AsyncClient(transport=httpx.MockTransport(serve)) as http, httpx.AsyncClient(
            base_url="https://graph.invalid", transport=httpx.MockTransport(no_graph)) as graph:
            with pytest.raises(EpochError):
                await client(http, graph).execute_saved(SavedStudy(study_id="study",
                    source_execution_id="ordinary", thread_id="thread"),
                    period=DatePeriodConfig(start=date(2025, 1, 1)), operation_id="fresh")
        assert all(request.method == "GET" for request in calls)
    asyncio.run(scenario())


def test_string_reference_reconnect_uses_retained_identity_without_reopening_the_original():
    async def scenario():
        research, original, answer = records()
        later = deepcopy(original)
        later_answer = deepcopy(answer)
        later_id = "req_" + "c" * 32
        later.update(request_id=later_id, execution_id="later-execution", response_id="later-answer")
        later["request"].pop("research_request_id")
        later["request"].update(operation_id="later", source_execution_id="ordinary",
            parameters={"period":{"start":"2025-01-01"}})
        later["extension_outputs"]["response_id"] = "later-answer"
        later["extension_outputs"]["provenance"].update(execution_id="later-execution",source_execution_id="ordinary")
        later_answer.update(response_id="later-answer",request_id=later_id,primary_execution_id="later-execution",
            extension=deepcopy(later["extension_outputs"]["provenance"]))
        calls = []
        def serve(request):
            calls.append(request)
            path = request.url.path
            assert path not in {"/api/v1/studies/executions/ordinary", "/api/v1/studies/executions/ordinary/study"}
            if request.method == "POST":
                assert json.loads(request.content) == later["request"]
                return httpx.Response(200,json=later)
            mapping = {
                "/api/v1/integration/requests/by-handle/question":research,
                f"/api/v1/integration/execution-requests/{OPERATION}":original,
                "/api/v1/research/responses/answer":answer,
                "/api/v1/integration/execution-requests/by-handle/later":later,
                "/api/v1/studies/executions/later-execution":job("later-execution"),
                "/api/v1/research/responses/later-answer":later_answer,
            }
            return httpx.Response(200,json=mapping[path])
        async with httpx.AsyncClient(transport=httpx.MockTransport(serve)) as http, httpx.AsyncClient(
            base_url="https://graph.invalid", transport=httpx.MockTransport(no_graph)) as graph:
            result = await client(http,graph).execute_saved("question", period=DatePeriodConfig(start=date(2025,1,1)),operation_id="later")
            assert isinstance(result,ChosenExecution) and result.response.to_wire() == later_answer
        assert sum(request.method == "POST" for request in calls) == 1
    asyncio.run(scenario())


@pytest.mark.parametrize("override", [False, True])
@pytest.mark.parametrize("operation_id", [None, "later"])
@pytest.mark.parametrize("source_status", ["running", "completed"])
def test_later_period_reuses_actual_settings_and_bindings_without_a_report_or_agent(override, operation_id, source_status):
    async def scenario():
        _, native, answer = records()
        answer["thread_id"] = "later-thread"
        native["request"].pop("research_request_id")
        native["request"].update(operation_id="later", source_execution_id="ordinary-source",
            parameters={"period": {"start": "2025-01-01", "end": "2025-12-31"}})
        native["extension_outputs"]["provenance"]["source_execution_id"] = "ordinary-source"
        calls = []
        def serve(request):
            calls.append(request)
            path = request.url.path
            if path == "/api/v1/integration/execution-requests/by-handle/later":
                return httpx.Response(404, json={"error": "DataNotFound", "message": "New operation",
                    "timestamp": "2026-10-27T00:00:00Z"})
            if request.method == "POST":
                assert path == "/api/v1/integration/execution-requests"
                body = json.loads(request.content)
                assert body["source_execution_id"] == "ordinary-source"
                assert body["thread_id"] == "later-thread"
                assert body["parameters"]["period"] == {"start": "2025-01-01", "end": "2025-12-31"}
                assert body["parameters"]["execution"]["cash"] == (999999 if override else 123456)
                if not override:
                    assert body["parameters"]["execution"]["commission"] == TRADING["commission"]
                    assert body["parameters"]["execution"]["futures_tick_snapshot"] == TRADING["futures_tick_snapshot"]
                assert body["execution_parameter_bindings"] == BINDINGS
                assert "input_tables" not in body and "report_template" not in body
                native["request"] = body
                return httpx.Response(200, json=native)
            mapping = {"/api/v1/studies/executions/ordinary-source": {**job("ordinary-source"), "status": source_status},
                "/api/v1/studies/executions/ordinary-source/study": snapshot("ordinary-source"),
                "/api/v1/studies/executions/ordinary": {**job(), "thread_id": "later-thread"},
                "/api/v1/research/responses/answer": answer}
            return httpx.Response(200, json=mapping[path])
        async with httpx.AsyncClient(transport=httpx.MockTransport(serve)) as http, httpx.AsyncClient(
            base_url="https://graph.invalid", transport=httpx.MockTransport(no_graph)) as graph:
            result = await client(http, graph).execute(SavedStudy(study_id="study",
                source_execution_id="ordinary-source", thread_id="later-thread"),
                period=DatePeriodConfig(start=date(2025, 1, 1), end=date(2025, 12, 31)),
                execution=ExecutionOptions(cash=999999) if override else None, operation_id=operation_id)
            assert isinstance(result, ChosenExecution)
            assert result.response.to_wire() == answer and result.report is None
            assert result.reusable_study.source_execution_id == "ordinary"
        assert sum(request.method == "POST" for request in calls) == 1
        assert any("by-handle" in request.url.path for request in calls) == (operation_id is not None)
    asyncio.run(scenario())


@pytest.mark.parametrize("mismatch", [False, True])
def test_same_operation_reconnect_uses_frozen_settings_when_the_original_is_unavailable(mismatch):
    async def scenario():
        _, native, answer = records()
        native["request"].pop("research_request_id")
        native["request"].update(operation_id="later", source_execution_id="removed-source")
        native["request"]["parameters"]["execution"] = TRADING
        native["extension_outputs"]["provenance"]["source_execution_id"] = "removed-source"
        calls = []
        def serve(request):
            calls.append(request)
            path = request.url.path
            assert "removed-source" not in path, "Reconnect must not reopen the original snapshot"
            if "by-handle/later" in path:
                return httpx.Response(200, json=native)
            if request.method == "POST":
                body = json.loads(request.content)
                if mismatch:
                    assert body["parameters"]["period"]["end"] == "2025-12-31"
                    return httpx.Response(409, json={"error": "InvalidState", "message": "Different accepted inputs"})
                assert body == native["request"]
                return httpx.Response(200, json=native)
            return httpx.Response(200, json=answer if "responses" in path else job())
        async with httpx.AsyncClient(transport=httpx.MockTransport(serve)) as http, httpx.AsyncClient(
            base_url="https://graph.invalid", transport=httpx.MockTransport(no_graph)) as graph:
            call = client(http, graph).execute_saved(SavedStudy(study_id="study",
                source_execution_id="removed-source", thread_id="thread"),
                period=DatePeriodConfig(start=date(2024, 1, 1),
                    end=date(2025 if mismatch else 2024, 12, 31)), operation_id="later")
            if mismatch:
                with pytest.raises(EpochError) as caught:
                    await call
                assert caught.value.error.code == "IDEMPOTENCY_CONFLICT"
            else:
                result = await call
                assert isinstance(result, ChosenExecution) and result.response.to_wire() == answer
        assert sum(request.method == "POST" for request in calls) == 1
    asyncio.run(scenario())


@pytest.mark.parametrize("phase", ["active", "outputs_recorded", "failed"])
@pytest.mark.parametrize("answer_pin", [False, True])
def test_ordinary_required_output_stage_controls_completion_and_optional_answer(phase, answer_pin):
    async def scenario():
        _, native, answer = records()
        native["request"].pop("research_request_id")
        native["response_phase"] = phase
        if not answer_pin:
            for value in (native, native["extension_outputs"]):
                value.pop("response_id")
                value.pop("response_version")
        def serve(request):
            assert request.method == "GET"
            if "by-handle" in request.url.path:
                return httpx.Response(200, json=native)
            if request.url.path.endswith("/ordinary"):
                # Deliberately completed numerics while delivery is still active.
                return httpx.Response(200, json=job())
            return httpx.Response(200, json=answer)
        async with httpx.AsyncClient(transport=httpx.MockTransport(serve)) as http, httpx.AsyncClient(
            base_url="https://graph.invalid", transport=httpx.MockTransport(no_graph)) as graph:
            owner = client(http, graph)
            if phase == "failed":
                with pytest.raises(EpochError, match="required study outputs"):
                    await owner.execution_operation("original")
            else:
                result = await owner.execution_operation("original")
                if phase == "active":
                    assert isinstance(result, ExecutionAccepted)
                else:
                    assert isinstance(result, ChosenExecution)
                    assert (result.response is not None) == answer_pin
    asyncio.run(scenario())


@pytest.mark.parametrize("numeric_status", ["Failed", "Cancelled"])
def test_execute_terminates_on_native_numerical_failure_before_output_acknowledgment(numeric_status):
    async def scenario():
        _, native, _ = records()
        native["request"].pop("research_request_id")
        native["request"].update(operation_id="later", source_execution_id="earlier")
        native.update(execution_status=numeric_status, response_phase="active")
        calls = []
        def serve(request):
            calls.append(request)
            assert "earlier" not in request.url.path
            if request.method == "POST":
                assert json.loads(request.content) == native["request"]
            else:
                assert request.url.path.endswith("by-handle/later")
            return httpx.Response(200, json=native)
        async with httpx.AsyncClient(transport=httpx.MockTransport(serve)) as http, httpx.AsyncClient(
            base_url="https://graph.invalid", transport=httpx.MockTransport(no_graph)) as graph:
            with pytest.raises(EpochError) as failure:
                await asyncio.wait_for(client(http, graph).execute(SavedStudy(study_id="study",
                    source_execution_id="earlier", thread_id="thread"),
                    period=DatePeriodConfig(start=date(2024, 1, 1), end=date(2024, 12, 31)),
                    operation_id="later"), timeout=.5)
            assert failure.value.error.code == "EXECUTION_FAILED"
            assert numeric_status.lower() in failure.value.error.message
        assert [request.method for request in calls] == ["GET", "POST"]
    asyncio.run(scenario())
