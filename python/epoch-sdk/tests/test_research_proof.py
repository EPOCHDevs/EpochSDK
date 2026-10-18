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
