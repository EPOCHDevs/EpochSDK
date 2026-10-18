from __future__ import annotations

import asyncio
import json
from contextlib import asynccontextmanager

import httpx
import pytest
from langgraph_sdk.client import LangGraphClient
from mcp import Client
from stratifyx import AsyncStratifyX
from test_responses import example

from epoch_sdk import EpochError
from epoch_sdk.mcp import create_server
from epoch_sdk.responses import ResearchResponseContent, publish_response, read_response
from epoch_sdk.supervisor import SupervisorClient


@asynccontextmanager
async def clients(*, wrong_identity: bool = False, denied: bool = False):
    calls: list[httpx.Request] = []
    record = example()
    if wrong_identity:
        record["execution_id"] = "another-execution"

    def respond(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        assert request.url.path == "/api/v1/studies/executions/example_execution/response"
        assert request.headers["Authorization"] == "Bearer fixture"
        if denied:
            return httpx.Response(
                403,
                json={
                    "error": "Forbidden",
                    "message": "Access denied",
                    "timestamp": "2026-10-18T00:00:00Z",
                },
            )
        if request.method == "POST":
            assert json.loads(request.content) == {
                "expected_version": 0,
                "content": example()["content"],
            }
        else:
            assert request.method == "GET"
        return httpx.Response(200, json=record)

    def no_graph(request: httpx.Request) -> httpx.Response:
        raise AssertionError("Response publication/reading must not invoke the supervisor")

    async with (
        httpx.AsyncClient(transport=httpx.MockTransport(respond)) as http,
        httpx.AsyncClient(transport=httpx.MockTransport(no_graph)) as graph_http,
    ):
        backend = AsyncStratifyX(
            base_url="https://backend.invalid", token="fixture", httpx_client=http
        )
        yield SupervisorClient(LangGraphClient(graph_http), backend), calls


def test_notebook_publication_and_read_use_the_generated_native_client() -> None:
    async def scenario() -> None:
        async with clients() as (sdk, calls):
            content = ResearchResponseContent.model_validate(example()["content"])
            published = await publish_response(sdk.backend, "example_execution", content)
            read = await read_response(sdk.backend, "example_execution", version=1)
            assert published == read
            assert published.to_wire() == example()
            assert [item.method for item in calls] == ["POST", "GET"]
            assert calls[-1].url.params["version"] == "1"

    asyncio.run(scenario())


def test_mcp_publishes_and_reads_the_same_typed_response_without_an_agent_run() -> None:
    async def scenario() -> None:
        async with clients() as (sdk, _), Client(create_server(sdk)) as mcp:
            published = await mcp.call_tool(
                "epoch_publish_response",
                {
                    "execution_id": "example_execution",
                    "content": example()["content"],
                },
            )
            assert not published.is_error
            assert published.structured_content == example()
            read = await mcp.call_tool("epoch_response", {"execution_id": "example_execution"})
            assert not read.is_error
            assert read.structured_content == published.structured_content

    asyncio.run(scenario())


def test_another_execution_cannot_be_returned_as_the_requested_response() -> None:
    async def scenario() -> None:
        async with clients(wrong_identity=True) as (sdk, _):
            with pytest.raises(EpochError) as error:
                await sdk.response("example_execution")
            assert error.value.error.code == "INVALID_STATE"
            assert error.value.execution_id == "example_execution"

    asyncio.run(scenario())


def test_mcp_keeps_access_failure_separate_from_protocol_failure() -> None:
    async def scenario() -> None:
        async with clients(denied=True) as (sdk, _), Client(create_server(sdk)) as mcp:
            result = await mcp.call_tool("epoch_response", {"execution_id": "example_execution"})
            assert not result.is_error
            assert result.structured_content["error"]["code"] == "FORBIDDEN"
            assert result.structured_content["execution_id"] == "example_execution"

    asyncio.run(scenario())
