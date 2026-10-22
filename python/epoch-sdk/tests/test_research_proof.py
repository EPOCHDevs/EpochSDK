import asyncio
import importlib.util
import json
import os
import subprocess
import sys
from contextlib import asynccontextmanager
from pathlib import Path

import httpx
import pytest

from epoch_sdk import EpochError
from epoch_sdk.contracts import DomainError
from epoch_sdk.output_validation import TableReference, TableValue
from epoch_sdk.research import ResearchCompleted
from epoch_sdk.responses import ResponseTablePage

ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location(
    "research_service_proof", ROOT / "tools/verify_research_services.py"
)
assert SPEC is not None and SPEC.loader is not None
proof = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = proof
SPEC.loader.exec_module(proof)
CASE = ROOT / "examples/research-service-proof.case.json"


def test_mcp_cleanup_preserves_the_domain_error_for_the_receipt(monkeypatch):
    class GroupingClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, kind, error, traceback):
            if error is not None:
                raise ExceptionGroup("MCP cleanup", [error])

    monkeypatch.setattr(proof, "Client", lambda *args, **kwargs: GroupingClient())
    failure = EpochError(
        DomainError(
            code="TEMPORARILY_UNAVAILABLE",
            message="Model unavailable",
            retryable=True,
        )
    )

    async def scenario():
        async with proof.mcp_client("https://graph.invalid", "https://backend.invalid", "fixture"):
            raise failure

    with pytest.raises(EpochError) as caught:
        asyncio.run(scenario())
    assert caught.value is failure


def completed(case):
    return ResearchCompleted.model_validate(
        {
            "status": "succeeded",
            "request_id": "request-one",
            "reusable_study": {
                "study_id": "study-one",
                "source_execution_id": "execution-one",
                "thread_id": "thread-one",
            },
            "response": {
                "response_id": "rsp_" + "1" * 64,
                "request_id": "request-one",
                "thread_id": "thread-one",
                "primary_execution_id": "execution-one",
                "study_id": "study-one",
                "version": 1,
                "published_at_ms": 1,
                "content": {
                    "declarations": [item.to_wire() for item in case.request.outputs],
                    "outputs": [
                        case.expected_table.model_dump(
                            mode="json", by_alias=True, exclude_unset=True
                        ),
                        case.expected_json.model_dump(mode="json"),
                        {
                            "name": "explanation",
                            "type": "text",
                            "format": "plain",
                            "value": "Synthetic annual sales total 25 USD.",
                        },
                    ],
                },
            },
        }
    )


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


@pytest.mark.parametrize("mode", ["sdk", "mcp"])
@pytest.mark.parametrize("wrong_revision", [False, True])
def test_referenced_case_checks_every_pinned_page(monkeypatch, mode, wrong_revision):
    case = proof.load_case(CASE)
    result = completed(case)
    expected = case.expected_table
    result.response.content.outputs[0] = TableValue(
        name=expected.name,
        type="table",
        schema=expected.columns,
        source=TableReference(
            execution_id="execution-one",
            table="computed_sales",
            field_ids=[column.name for column in expected.columns],
            row_count=len(expected.rows),
        ),
    )
    with pytest.raises(AssertionError, match="Read all referenced"):
        proof.verify_values(case, result)
    calls = []

    def page(offset):
        return ResponseTablePage(
            response_id=result.response.response_id,
            version=2 if wrong_revision else result.response.version,
            name=expected.name,
            type="table",
            schema=expected.columns,
            rows=expected.rows[offset : offset + 1],
            offset=offset,
            total_rows=len(expected.rows),
            next_offset=offset + 1 if offset + 1 < len(expected.rows) else None,
        )

    class Sdk:
        async def iter_response_table(self, response_id, name, *, version):
            assert response_id == result.response.response_id
            assert name == expected.name and version == 1
            for offset in range(len(expected.rows)):
                calls.append(offset)
                yield page(offset)

        async def aclose(self):
            pass

    def connect(graph, backend, token):
        assert graph == "http://127.0.0.1:1"
        return Sdk()

    @asynccontextmanager
    async def mcp_client(graph, backend, token):
        assert graph == "http://127.0.0.1:1"
        yield object()

    async def mcp_call(client, name, arguments):
        assert name == "epoch_read"
        assert arguments["response_id"] == result.response.response_id
        assert arguments["table"] == expected.name and arguments["version"] == 1
        offset = arguments["offset"]
        calls.append(offset)
        return page(offset).to_wire()

    monkeypatch.setattr(proof, "connect", connect)
    monkeypatch.setattr(proof, "mcp_client", mcp_client)
    monkeypatch.setattr(proof, "mcp_call", mcp_call)
    if wrong_revision:
        with pytest.raises(AssertionError, match="saved source"):
            asyncio.run(
                proof.read_case_table(mode, "https://backend.invalid", "fixture", case, result)
            )
    else:
        actual = asyncio.run(
            proof.read_case_table(mode, "https://backend.invalid", "fixture", case, result)
        )
        assert calls == list(range(len(expected.rows)))
        proof.verify_values(case, result, table=actual)


def test_describe_is_offline_and_cannot_claim_real_analysis(tmp_path):
    output = tmp_path / "plan.json"
    env = os.environ.copy()
    for key in ("EPOCH_GRAPH_URL", "EPOCH_BACKEND_URL", "EPOCH_TOKEN"):
        env.pop(key, None)
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools/verify_research_services.py"),
            "--case",
            str(CASE),
            "--mode",
            "sdk",
            "--output",
            str(output),
        ],
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
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
        return httpx.Response(
            200,
            json={
                "status": "healthy",
                "deployment": {"git_sha": "3" * 40 if mismatch == "agent-sha" else agent_sha},
                "build_study": {
                    "ready": mismatch != "not-ready",
                    "backend_url": "https://different.invalid"
                    if mismatch == "backend-pair"
                    else "https://backend.invalid",
                },
            },
        )

    client = httpx.AsyncClient
    monkeypatch.setattr(
        proof.httpx,
        "AsyncClient",
        lambda **kwargs: client(
            transport=httpx.MockTransport(respond),
            **kwargs,
        ),
    )
    with pytest.raises(RuntimeError):
        asyncio.run(
            proof.preflight(
                "https://graph.invalid",
                "https://backend.invalid",
                "fixture",
                backend_sha,
                agent_sha,
            )
        )
    assert len(calls) == 2


def native_thread():
    policy = {
        "run_id": "model-one",
        "model": "provider-model-one",
        "model_identity_source": "provider_response",
        "model_role": "supervisor",
        "receipt_source": "production_policy",
    }
    return {
        "sdk_request_id": "request-one",
        "authority_turn_id": "user-turn:request-one",
        "messages": [
            {"id": "earlier-task", "type": "human", "content": "Old task"},
            {"type": "ai", "tool_calls": [{"id": "old-call", "name": "discovery"}]},
            {"id": "request-one", "type": "human", "content": "private-user-content"},
            {
                "type": "ai",
                "response_metadata": {"epoch_model_call": policy},
                "usage_metadata": {"input_tokens": 10, "output_tokens": 4, "total_tokens": 14},
                "tool_calls": [
                    {
                        "id": "build-one",
                        "name": "build_study",
                        "args": {"private-tool-args": "omit"},
                    }
                ],
            },
            {"type": "ai", "tool_calls": [{"id": "run-one", "name": "run_study"}]},
            {"type": "ai", "tool_calls": [{"id": "publish-one", "name": "publish_response"}]},
        ],
        "next_action_outcomes": {
            "build-one:build_study:study": {
                "tool_call_id": "build-one",
                "tool_name": "build_study",
                "status": "saved",
            },
            "run-one:run_study:run": {
                "tool_call_id": "run-one",
                "tool_name": "run_study",
                "status": "completed",
                "execution_id": "execution-one",
            },
        },
    }


def test_native_trace_records_current_calls_usage_and_chosen_execution(monkeypatch):
    state = native_thread()

    def respond(request):
        assert request.url.path == "/threads/thread-one/state"
        assert request.headers["Authorization"] == "Bearer fixture"
        return httpx.Response(200, json={"values": state, "next": [], "interrupts": []})

    client = httpx.AsyncClient
    monkeypatch.setattr(
        proof.httpx,
        "AsyncClient",
        lambda **kwargs: client(
            transport=httpx.MockTransport(respond),
            **kwargs,
        ),
    )
    trace = asyncio.run(
        proof.capture_trace("https://graph.invalid", "fixture", "thread-one", "request-one")
    )
    result = completed(proof.load_case(CASE))
    proof.verify_trace(trace, result)
    assert [call.name for call in trace.tool_calls] == [
        "build_study",
        "run_study",
        "publish_response",
    ]
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
    repeated = trace.model_copy(
        update={
            "tool_calls": [*trace.tool_calls, proof.ToolCall(id="new-discovery", name="discovery")]
        }
    )
    with pytest.raises(AssertionError, match="Discovery repeated"):
        proof.verify_resume_trace(before, repeated, no_new_discovery=True)


def test_native_trace_rejects_an_unrelated_current_user_turn(monkeypatch):
    state = native_thread()
    state["authority_turn_id"] = "user-turn:another-request"
    client = httpx.AsyncClient
    monkeypatch.setattr(
        proof.httpx,
        "AsyncClient",
        lambda **kwargs: client(
            transport=httpx.MockTransport(lambda _: httpx.Response(200, json={"values": state})),
            **kwargs,
        ),
    )
    with pytest.raises(AssertionError, match="different current request"):
        asyncio.run(
            proof.capture_trace("https://graph.invalid", "fixture", "thread-one", "request-one")
        )


@pytest.mark.parametrize("mode", ["sdk", "mcp"])
@pytest.mark.parametrize("fault", [None, "mutable-pin", "new-answer"])
def test_revision_proof_uses_native_clients_and_detects_broken_identity_or_pins(
    monkeypatch, mode, fault
):
    """Exercise the verifier over actual generated HTTP and MCP clients."""
    import copy
    from contextlib import asynccontextmanager

    from langgraph_sdk.client import LangGraphClient
    from mcp import Client
    from stratifyx import AsyncStratifyX

    from epoch_sdk.research import EpochClient
    from epoch_sdk.supervisor import SupervisorClient
    from epoch_sdk.workflow_mcp import create_server

    case = proof.load_case(CASE)
    original = completed(case)
    saved = original.response.to_wire()
    versions = {1: copy.deepcopy(saved)}
    calls = []
    expected_thread = saved["thread_id"]
    request_record = {
        "request_id": original.request_id,
        "version": 2,
        "created_at_ms": 1,
        "updated_at_ms": 1,
        "phase": "outputs_recorded",
        "request": case.request.to_wire(),
        "runtime": {
            "thread_id": expected_thread,
            "assistant_id": "epoch-ai",
            "execution_ids_before": [],
            "outcome_ids_before": [],
        },
        "current_execution_id": saved["primary_execution_id"],
        "response_id": saved["response_id"],
        "response_version": 1,
    }

    def backend(request):
        calls.append(request)
        assert request.headers["Authorization"] == "Bearer fixture"
        if request.method == "POST":
            assert request.url.path == "/api/v1/research/requests/request-one/response"
            body = json.loads(request.content)
            assert body["expected_version"] == 1
            assert body["thread_id"] == expected_thread
            assert body["primary_execution_id"] == saved["primary_execution_id"]
            updated = copy.deepcopy(saved)
            updated.update(version=2, published_at_ms=2, content=body["content"])
            if fault == "new-answer":
                updated["response_id"] = "rsp_" + "2" * 64
            versions[2] = updated
            return httpx.Response(200, json=updated)
        if request.url.path == "/api/v1/integration/requests/request-one":
            result = copy.deepcopy(request_record)
            if fault == "mutable-pin":
                result["response_version"] = 2
            return httpx.Response(200, json=result)
        assert request.url.path == "/api/v1/research/responses/" + saved["response_id"]
        version = (
            int(request.url.params["version"]) if "version" in request.url.params else max(versions)
        )
        return httpx.Response(200, json=versions[version])

    def no_graph(request):
        raise AssertionError("Answer revision/pinned reads must not invoke LangGraph")

    async def scenario():
        async with (
            httpx.AsyncClient(transport=httpx.MockTransport(backend)) as native_http,
            httpx.AsyncClient(transport=httpx.MockTransport(no_graph)) as graph_http,
        ):
            native = AsyncStratifyX(
                base_url="https://backend.invalid", token="fixture", httpx_client=native_http
            )
            supervisor = SupervisorClient(LangGraphClient(graph_http), native)
            client = EpochClient(supervisor)

            def connect(graph_url, backend_url, token):
                assert graph_url == "http://127.0.0.1:1"
                return client

            @asynccontextmanager
            async def mcp_client(graph_url, backend_url, token):
                assert graph_url == "http://127.0.0.1:1"
                async with Client(create_server(supervisor)) as mcp:
                    yield mcp

            monkeypatch.setattr(proof, "connect", connect)
            monkeypatch.setattr(proof, "mcp_client", mcp_client)
            receipt = proof.Receipt(
                mode=mode,
                case_sha256="1" * 64,
                recorded_at="2026-10-18T00:00:00Z",
                checks=[],
                epoch_sdk_version="fixture",
                langgraph_sdk_version="fixture",
                stratifyx_version="fixture",
                native_sdk_backend_sha="2" * 40,
                native_sdk_openapi_digest="sha256:" + "3" * 64,
            )
            if fault:
                with pytest.raises((AssertionError, ExceptionGroup)) as failure:
                    await proof.revise_and_verify(
                        mode, "https://backend.invalid", "fixture", original, receipt
                    )
                error = failure.value
                if isinstance(error, ExceptionGroup):
                    matched, unrelated = error.split(AssertionError)
                    assert matched is not None and unrelated is None
                    message = repr(matched)
                else:
                    message = str(error)
                assert "identity" in message or "pinned" in message
                assert not receipt.real_analysis_proven
            else:
                await proof.revise_and_verify(
                    mode, "https://backend.invalid", "fixture", original, receipt
                )
                assert receipt.revised_response.response_id == original.response.response_id
                assert receipt.revised_response.version == 2
                assert len(receipt.revised_content_sha256) == 64
                assert receipt.checks == [
                    "post-analysis-revision-without-graph",
                    "original-request-still-pinned-after-edit",
                ]
                assert versions[2]["content"]["outputs"][:2] == saved["content"]["outputs"][:2]
                assert sum(request.method == "POST" for request in calls) == 1

    asyncio.run(scenario())
