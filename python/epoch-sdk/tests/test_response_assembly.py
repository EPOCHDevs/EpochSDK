from __future__ import annotations

import asyncio
import json
from contextlib import asynccontextmanager

import httpx
import pyarrow as pa
import pytest
from stratifyx import AsyncStratifyX
from test_saved_outputs import manifest

from epoch_sdk import EpochError
from epoch_sdk.output_validation import JsonValueOutput, TextValue
from epoch_sdk.responses import ResponseTableSource, assemble_response


def parts():
    return [
        JsonValueOutput(name="totals", type="json", value={"total": 12.5}),
        TextValue(name="report", type="text", format="markdown", value="Sales were USD 12.5."),
    ]


def source():
    return ResponseTableSource(name="sales", table="computed_sales", field_ids=["year", "sales"])


@asynccontextmanager
async def backend(*, denied=False, bad_type=False):
    calls = []
    table = pa.table(
        {
            "year": pa.array([9007199254740993, 2025], type=pa.int64()),
            "sales": pa.array(["bad", None])
            if bad_type
            else pa.array([12.5, None], type=pa.float64()),
        }
    )
    sink = pa.BufferOutputStream()
    with pa.ipc.new_stream(sink, table.schema) as writer:
        writer.write_table(table)

    def respond(request):
        calls.append(request)
        assert request.url.path == "/api/v1/studies/executions/run-one/response-tables"
        assert request.method == "POST"
        assert json.loads(request.content) == {
            "table": "computed_sales",
            "field_ids": ["year", "sales"],
        }
        if denied:
            return httpx.Response(404, json={"message": "Not found"})
        return httpx.Response(200, content=sink.getvalue().to_pybytes())

    async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as http:
        yield (
            AsyncStratifyX(base_url="https://backend.invalid", token="fixture", httpx_client=http),
            calls,
        )


def test_complete_relation_does_not_require_any_dashboard_exhibit():
    async def scenario():
        async with backend() as (native, calls):
            result = await assemble_response(
                native,
                "run-one",
                "study-one",
                manifest().declarations,
                parts(),
                table_sources=[source()],
            )
            assert result.outputs[0].to_wire()["rows"] == [
                ["9007199254740993", 12.5],
                ["2025", None],
            ]
            assert len(calls) == 1

    asyncio.run(scenario())


@pytest.mark.parametrize("sources", [[], [source(), source()]])
def test_missing_or_duplicate_table_sources_fail_before_io(sources):
    async def scenario():
        async with backend() as (native, calls):
            with pytest.raises(ValueError):
                await assemble_response(
                    native,
                    "run-one",
                    "study-one",
                    manifest().declarations,
                    parts(),
                    table_sources=sources,
                )
            assert not calls

    asyncio.run(scenario())


def test_native_physical_types_are_checked():
    async def scenario():
        async with backend(bad_type=True) as (native, _):
            with pytest.raises(EpochError):
                await assemble_response(
                    native,
                    "run-one",
                    "study-one",
                    manifest().declarations,
                    parts(),
                    table_sources=[source()],
                )

    asyncio.run(scenario())
