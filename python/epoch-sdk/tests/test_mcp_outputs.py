"""Advanced manifest reads remain SDK-only; MCP consumes published answers."""

from __future__ import annotations

import asyncio

import httpx
import pytest
from langgraph_sdk.client import LangGraphClient
from pydantic import ValidationError
from test_saved_outputs import dashboard, manifest, native_backend

from epoch_sdk.errors import EpochError
from epoch_sdk.saved_outputs import SavedOutputManifest
from epoch_sdk.supervisor import SupervisorClient


def test_sdk_manifest_reader_keeps_native_values_without_a_graph_call():
    async def scenario():
        def no_graph(request):
            raise AssertionError("Saved reads must not invoke the supervisor")

        async with (
            native_backend() as (backend, calls),
            httpx.AsyncClient(
                base_url="https://graph.invalid", transport=httpx.MockTransport(no_graph)
            ) as graph,
        ):
            sdk = SupervisorClient(LangGraphClient(graph), backend)
            result = (await sdk.outputs(manifest())).to_wire()
            assert result["outputs"][0]["rows"] == [["9007199254740993", 12.5], ["2025", None]]
            assert (
                result["declarations"][1]["schema"]["properties"]["total"]["description"]
                == "Total sales in USD"
            )
            assert all(call.method == "GET" for call in calls)

    asyncio.run(scenario())


def test_normal_ended_refusal_preserves_its_terminal_payload_in_the_active_mcp_surface():
    from test_supervisor import clients
    from epoch_sdk import UsageLimitReached
    from epoch_sdk.workflow_mcp import _error

    async def scenario():
        marker = {"meter": "assistant", "state": "reached", "resets_at": "2099-11-23T00:00:00Z"}
        async with clients([{"usage_limit": marker}]) as (client, graph_calls, backend_calls):
            with pytest.raises(UsageLimitReached) as raised:
                await client.run("Question stopped before its model")
            result = _error(raised.value)
            assert result.is_error
            assert result.structured_content["error"]["code"] == "USAGE_LIMIT_REACHED"
            assert result.structured_content["error"]["retryable"] is False
            assert result.structured_content["error"]["meter"] == "assistant"
            assert result.structured_content["error"]["resets_at"] == marker["resets_at"]
            assert len([r for r in graph_calls if r.method == "POST" and r.url.path.endswith("/runs/wait")]) == 1
            assert not [r for r in backend_calls if r.method in {"POST", "PATCH"}]
    asyncio.run(scenario())


def test_workflow_refusal_is_an_mcp_error_with_reset_guidance():
    from epoch_sdk.api import Problem, UsageLimitReached
    from epoch_sdk.workflow_mcp import _error

    result = _error(UsageLimitReached(Problem(
        title="Weekly usage limit reached", status=403, code="USAGE_LIMIT_REACHED",
        meter="assistant", resets_at="2099-11-23T00:00:00Z",
    )))
    assert result.is_error
    assert result.structured_content["error"]["code"] == "USAGE_LIMIT_REACHED"
    assert result.structured_content["error"]["retryable"] is False
    assert result.structured_content["error"]["resets_at"] == "2099-11-23T00:00:00Z"


def test_sdk_manifest_failure_retains_execution_identity():
    async def scenario():
        schema = dashboard()
        schema["content"]["markdown"][0]["markdown"] = '{"total":"wrong-type"}'
        async with (
            native_backend(schema=schema) as (backend, _),
            httpx.AsyncClient(base_url="https://graph.invalid") as graph,
        ):
            sdk = SupervisorClient(LangGraphClient(graph), backend)
            with pytest.raises(EpochError) as failure:
                await sdk.outputs(manifest())
            assert failure.value.error.code == "OUTPUT_VALIDATION_FAILED"
            assert failure.value.execution_id == "run-one"

    asyncio.run(scenario())


def test_malformed_manifest_is_rejected_before_it_can_be_sent():
    value = manifest().to_wire()
    value["bindings"][0]["unexpected"] = "invalid"
    with pytest.raises(ValidationError):
        SavedOutputManifest.model_validate(value)
