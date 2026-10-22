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


def test_composable_mcp_preserves_native_failure_without_retry_or_fallback():
    from epoch_sdk.mcp import _call
    from stratifyx.core.api_error import ApiError

    async def scenario():
        calls = 0
        async def rejected():
            nonlocal calls
            calls += 1
            raise ApiError(status_code=503, headers={"private-header": "must-not-leak"}, body={
                "error": "ServiceUnavailable", "message": "Macrobond metadata search is at capacity",
                "timestamp": "2026-10-22T12:00:00Z", "additionalContext": {"request_id": "macro-test"},
                "private_extra": "must-not-leak",
            })
        result = await _call(rejected())
        assert result.is_error and calls == 1
        assert result.structured_content == {
            "http_status": 503, "backend_error": {
                "error": "ServiceUnavailable", "message": "Macrobond metadata search is at capacity",
                "timestamp": "2026-10-22T12:00:00Z", "additionalContext": {"request_id": "macro-test"},
            },
        }
        assert "Macrobond" in result.content[0].text
        assert "must-not-leak" not in result.model_dump_json()
        async def malformed():
            raise ApiError(status_code=502, body={"raw_internal": "must-not-leak"})
        invalid = await _call(malformed())
        assert invalid.is_error
        assert "without a valid native error" in invalid.content[0].text
        assert "must-not-leak" not in invalid.model_dump_json()
    asyncio.run(scenario())
