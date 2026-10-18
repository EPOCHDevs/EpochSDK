from __future__ import annotations

import asyncio

import httpx
from langgraph_sdk.client import LangGraphClient
from mcp import Client
from test_saved_outputs import dashboard, manifest, native_backend

from epoch_sdk.mcp import create_server
from epoch_sdk.supervisor import SupervisorClient


def test_mcp_reads_and_validates_native_saved_values_without_a_graph_call() -> None:
    async def scenario() -> None:
        def no_graph(request: httpx.Request) -> httpx.Response:
            raise AssertionError("Saved result reads must not invoke the supervisor")

        async with (
            native_backend() as (backend, calls),
            httpx.AsyncClient(
                base_url="https://graph.invalid", transport=httpx.MockTransport(no_graph)
            ) as graph,
            Client(create_server(SupervisorClient(LangGraphClient(graph), backend))) as mcp,
        ):
            result = await mcp.call_tool("epoch_outputs", {"manifest": manifest().to_wire()})
            assert not result.is_error and result.structured_content is not None
            assert result.structured_content["outputs"][0]["rows"] == [
                ["9007199254740993", 12.5],
                ["2025", None],
            ]
            assert (
                result.structured_content["declarations"][1]["schema"]["properties"]["total"][
                    "description"
                ]
                == "Total sales in USD"
            )
            assert all(call.method == "GET" for call in calls)

    asyncio.run(scenario())


def test_mcp_reports_a_typed_output_failure_with_execution_identity() -> None:
    async def scenario() -> None:
        schema = dashboard()
        schema["content"]["markdown"][0]["markdown"] = '{"total":"wrong-type"}'
        async with (
            native_backend(schema=schema) as (backend, _),
            httpx.AsyncClient(base_url="https://graph.invalid") as graph,
            Client(create_server(SupervisorClient(LangGraphClient(graph), backend))) as mcp,
        ):
            result = await mcp.call_tool("epoch_outputs", {"manifest": manifest().to_wire()})
            assert not result.is_error and result.structured_content is not None
            assert result.structured_content["error"]["code"] == "OUTPUT_VALIDATION_FAILED"
            assert result.structured_content["execution_id"] == "run-one"

    asyncio.run(scenario())


def test_malformed_manifest_is_a_tool_error_before_any_backend_call() -> None:
    async def scenario() -> None:
        value = manifest().to_wire()
        value["bindings"][0]["unexpected"] = "invalid"
        async with (
            native_backend() as (backend, calls),
            httpx.AsyncClient(base_url="https://graph.invalid") as graph,
            Client(create_server(SupervisorClient(LangGraphClient(graph), backend))) as mcp,
        ):
            result = await mcp.call_tool("epoch_outputs", {"manifest": value})
            assert result.is_error
            assert calls == []

    asyncio.run(scenario())
