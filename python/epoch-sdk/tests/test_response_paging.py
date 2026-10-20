from __future__ import annotations

import asyncio
import json
from contextlib import asynccontextmanager
from pathlib import Path

import httpx
import pyarrow as pa
import pytest
from langgraph_sdk.client import LangGraphClient
from mcp import Client
from stratifyx import AsyncStratifyX

from epoch_sdk import EpochError
from epoch_sdk.mcp import create_server
from epoch_sdk.responses import SavedResearchResponse, read_response_table_page
from epoch_sdk.supervisor import SupervisorClient

ROOT = Path(__file__).resolve().parents[3]


def example():
    return json.loads((ROOT / "contracts/research-response-reference.example.json").read_text())


@asynccontextmanager
async def clients(*, wrong_count=False, wrong_offset=False):
    calls = []
    order = [i for parity in (0, 1) for i in range(parity, 25003, 2)]
    table = pa.table(
        {
            "label": ["A" if i % 2 == 0 else "B" for i in order],
            "value": pa.array(order, type=pa.int64()),
        }
    )

    def respond(request):
        calls.append(request)
        if request.method == "GET":
            return httpx.Response(200, json=example())
        assert request.url.path == "/api/v1/studies/executions/example_execution/response-tables"
        body = json.loads(request.content)
        assert set(body) == {"table", "field_ids", "offset", "page_size", "order_by"}
        assert body["table"] == "computed_results" and body["field_ids"] == ["label", "value"]
        rows = table.slice(body["offset"], body["page_size"])
        sink = pa.BufferOutputStream()
        with pa.ipc.new_stream(sink, rows.schema) as writer:
            writer.write_table(rows)
        return httpx.Response(
            200,
            content=sink.getvalue().to_pybytes(),
            headers={
                "X-Arrow-Total-Rows": "25002" if wrong_count else "25003",
                "X-Arrow-Returned-Rows": str(rows.num_rows),
                "X-Arrow-Row-Offset": str(body["offset"] + int(wrong_offset)),
            },
        )

    def no_graph(request):
        raise AssertionError("Table paging must not invoke an agent")

    async with (
        httpx.AsyncClient(transport=httpx.MockTransport(respond)) as http,
        httpx.AsyncClient(transport=httpx.MockTransport(no_graph)) as graph,
    ):
        yield (
            SupervisorClient(
                LangGraphClient(graph),
                AsyncStratifyX(
                    base_url="https://backend.invalid", token="fixture", httpx_client=http
                ),
            ),
            calls,
            order,
        )


def test_complete_traversal_exceeds_10000_rows_and_pins_the_answer_once():
    async def scenario():
        async with clients() as (sdk, calls, expected):
            actual = []
            async for page in sdk.iter_response_table(
                example()["response_id"], "results", page_size=5000
            ):
                assert page.total_rows == 25003 and page.version == 1
                assert len(page.rows) <= 5000
                actual.extend(int(row[1]) for row in page.rows)
            assert actual == expected
            assert len([call for call in calls if call.method == "GET"]) == 1
            assert [
                json.loads(call.content)["offset"] for call in calls if call.method == "POST"
            ] == [0, 5000, 10000, 15000, 20000, 25000]
            assert "rows" not in example()["content"]["outputs"][0]
            assert len(json.dumps(example())) < 4096

    asyncio.run(scenario())


def test_mcp_returns_explicit_page_metadata_and_an_empty_end_page():
    async def scenario():
        async with clients() as (sdk, _, _), Client(create_server(sdk)) as mcp:
            page = await mcp.call_tool(
                "epoch_read",
                {
                    "response_id": example()["response_id"],
                    "table": "results",
                    "version": 1,
                    "offset": 25000,
                    "page_size": 1000,
                },
            )
            assert not page.is_error
            result = page.structured_content
            assert result["total_rows"] == 25003 and len(result["rows"]) == 3
            assert result["next_offset"] is None
            empty = await sdk.response_table(example()["response_id"], "results", offset=25003)
            assert empty.rows == [] and empty.next_offset is None

    asyncio.run(scenario())


@pytest.mark.parametrize(
    "wrong_count,wrong_offset,code",
    [(True, False, "INVALID_STATE"), (False, True, "OUTPUT_VALIDATION_FAILED")],
)
def test_changed_sources_and_inconsistent_page_metadata_fail(wrong_count, wrong_offset, code):
    async def scenario():
        async with clients(wrong_count=wrong_count, wrong_offset=wrong_offset) as (sdk, _, _):
            with pytest.raises(EpochError) as error:
                await sdk.response_table(example()["response_id"], "results")
            assert error.value.error.code == code

    asyncio.run(scenario())


def test_legacy_inline_answers_page_without_a_native_table_read():
    async def scenario():
        saved = json.loads((ROOT / "contracts/research-response.example.json").read_text())
        async with clients() as (sdk, calls, _):
            page = await read_response_table_page(
                sdk.backend, SavedResearchResponse.model_validate(saved), "screen", page_size=1
            )
            assert page.total_rows == 1 and page.rows == [["EXAMPLE", 18.2]]
            assert calls == []

    asyncio.run(scenario())
