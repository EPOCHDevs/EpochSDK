import asyncio
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import httpx
import pytest

from epoch_sdk.research import ResearchCompleted

ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location("research_service_proof", ROOT / "tools/verify_research_services.py")
assert SPEC is not None and SPEC.loader is not None
proof = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = proof
SPEC.loader.exec_module(proof)
CASE = ROOT / "examples/research-service-proof.case.json"


def completed(case):
    return ResearchCompleted.model_validate({
        "status": "succeeded", "request_id": "request-one",
        "reusable_study": {"study_id": "study-one", "source_execution_id": "execution-one"},
        "response": {"execution_id": "execution-one", "study_id": "study-one", "version": 1,
                     "published_at_ms": 1, "content": {
                         "declarations": [item.to_wire() for item in case.request.outputs],
                         "outputs": [
                             case.expected_table.model_dump(mode="json", by_alias=True, exclude_unset=True),
                             case.expected_json.model_dump(mode="json"),
                             {"name": "explanation", "type": "text", "format": "plain",
                              "value": "Synthetic annual sales total 25 USD."},
                         ],
                     }},
    })


def test_registered_case_checks_actual_values_and_native_identity():
    case = proof.load_case(CASE)
    result = completed(case)
    proof.verify_values(case, result)
    bad = result.model_copy(deep=True)
    bad.response.content.outputs[0].rows[0][1] = 999.0
    with pytest.raises(AssertionError, match="table values"):
        proof.verify_values(case, bad)
    bad = result.model_copy(deep=True)
    bad.reusable_study = bad.reusable_study.model_copy(update={"study_id": "another-study"})
    with pytest.raises(AssertionError, match="different executions"):
        proof.verify_values(case, bad)


def test_describe_is_offline_and_cannot_claim_real_analysis(tmp_path):
    output = tmp_path / "plan.json"
    env = os.environ.copy()
    for key in ("EPOCH_GRAPH_URL", "EPOCH_BACKEND_URL", "EPOCH_TOKEN"):
        env.pop(key, None)
    result = subprocess.run([
        sys.executable, str(ROOT / "tools/verify_research_services.py"),
        "--case", str(CASE), "--mode", "sdk", "--output", str(output),
    ], env=env, capture_output=True, text=True, check=True)
    assert "no service connection" in result.stdout
    receipt = json.loads(output.read_text())
    assert receipt["real_analysis_proven"] is False
    assert receipt["checks"] == ["registered-case-valid"]
    assert "result" not in receipt


@pytest.mark.parametrize("mismatch", ["agent-sha", "backend-pair", "not-ready"])
def test_service_pairing_fails_before_a_model_call(monkeypatch, mismatch):
    calls = []
    backend_sha, agent_sha = "1" * 40, "2" * 40

    def respond(request):
        calls.append(request)
        assert request.method == "GET"
        assert request.headers["Authorization"] == "Bearer fixture"
        if request.url.path == "/api/v1/health":
            return httpx.Response(200, json={"git_sha": backend_sha})
        assert request.url.path == "/health/custom"
        return httpx.Response(200, json={
            "status": "healthy", "deployment": {"git_sha": "3" * 40 if mismatch == "agent-sha" else agent_sha},
            "build_study": {"ready": mismatch != "not-ready", "backend_url":
                "https://different.invalid" if mismatch == "backend-pair" else "https://backend.invalid"},
        })

    client = httpx.AsyncClient
    monkeypatch.setattr(proof.httpx, "AsyncClient", lambda **kwargs: client(
        transport=httpx.MockTransport(respond), **kwargs,
    ))
    with pytest.raises(RuntimeError):
        asyncio.run(proof.preflight(
            "https://graph.invalid", "https://backend.invalid", "fixture", backend_sha, agent_sha,
        ))
    assert len(calls) == 2


def native_thread():
    policy = {"run_id": "model-one", "model": "provider-model-one",
              "model_identity_source": "provider_response", "model_role": "supervisor",
              "receipt_source": "production_policy"}
    return {
        "sdk_request_id": "request-one", "authority_turn_id": "user-turn:request-one",
        "messages": [
            {"id": "earlier-task", "type": "human", "content": "Old task"},
            {"type": "ai", "tool_calls": [{"id": "old-call", "name": "discovery"}]},
            {"id": "request-one", "type": "human", "content": "private-user-content"},
            {"type": "ai", "response_metadata": {"epoch_model_call": policy},
             "usage_metadata": {"input_tokens": 10, "output_tokens": 4, "total_tokens": 14},
             "tool_calls": [{"id": "build-one", "name": "build_study", "args": {"private-tool-args": "omit"}}]},
            {"type": "ai", "tool_calls": [{"id": "run-one", "name": "run_study"}]},
            {"type": "ai", "tool_calls": [{"id": "publish-one", "name": "publish_response"}]},
        ],
        "next_action_outcomes": {
            "build-one:build_study:study": {"tool_call_id": "build-one", "tool_name": "build_study", "status": "saved"},
            "run-one:run_study:run": {"tool_call_id": "run-one", "tool_name": "run_study", "status": "completed", "execution_id": "execution-one"},
        },
    }


def test_native_trace_records_current_calls_usage_and_chosen_execution(monkeypatch):
    state = native_thread()

    def respond(request):
        assert request.url.path == "/threads/thread-one/state"
        assert request.headers["Authorization"] == "Bearer fixture"
        return httpx.Response(200, json={"values": state, "next": [], "interrupts": []})

    client = httpx.AsyncClient
    monkeypatch.setattr(proof.httpx, "AsyncClient", lambda **kwargs: client(
        transport=httpx.MockTransport(respond), **kwargs,
    ))
    trace = asyncio.run(proof.capture_trace("https://graph.invalid", "fixture", "thread-one", "request-one"))
    result = completed(proof.load_case(CASE))
    proof.verify_trace(trace, result)
    assert [call.name for call in trace.tool_calls] == ["build_study", "run_study", "publish_response"]
    assert trace.model_calls[0].usage.total_tokens == 14
    assert "private-user-content" not in trace.model_dump_json()
    assert "private-tool-args" not in trace.model_dump_json()
    with pytest.raises(AssertionError, match="real-model proof"):
        proof.verify_trace(trace.model_copy(update={"model_calls": []}), result)
    changed = trace.model_copy(deep=True)
    changed.outcomes["run-one:run_study:run"].execution_id = "another-execution"
    with pytest.raises(AssertionError, match="completed-run outcome"):
        proof.verify_trace(changed, result)
    with pytest.raises(AssertionError, match="did not discover"):
        proof.verify_trace(trace, result, requires_discovery=True)
    before = trace.model_copy(update={"tool_calls": trace.tool_calls[:1]})
    proof.verify_resume_trace(before, trace, no_new_discovery=True)
    repeated = trace.model_copy(update={"tool_calls": [*trace.tool_calls, proof.ToolCall(id="new-discovery", name="discovery")]})
    with pytest.raises(AssertionError, match="Discovery repeated"):
        proof.verify_resume_trace(before, repeated, no_new_discovery=True)


def test_native_trace_rejects_an_unrelated_current_user_turn(monkeypatch):
    state = native_thread()
    state["authority_turn_id"] = "user-turn:another-request"
    client = httpx.AsyncClient
    monkeypatch.setattr(proof.httpx, "AsyncClient", lambda **kwargs: client(
        transport=httpx.MockTransport(lambda _: httpx.Response(200, json={"values": state})), **kwargs,
    ))
    with pytest.raises(AssertionError, match="different current request"):
        asyncio.run(proof.capture_trace("https://graph.invalid", "fixture", "thread-one", "request-one"))
