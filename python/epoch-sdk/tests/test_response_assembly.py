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

    def respond(request):
        calls.append(request)
        assert request.url.path == "/api/v1/studies/executions/run-one/response-tables"
        assert request.method == "POST"
        assert json.loads(request.content) == {
            "table": "computed_sales",
            "field_ids": ["year", "sales"],
            "offset": 0,
            "page_size": 1,
            "order_by": [],
        }
        if denied:
            return httpx.Response(404, json={"message": "Not found"})
        sink = pa.BufferOutputStream()
        with pa.ipc.new_stream(sink, table.schema) as writer:
            writer.write_table(table.slice(0, 1))
        return httpx.Response(
            200,
            content=sink.getvalue().to_pybytes(),
            headers={
                "X-Arrow-Total-Rows": "2",
                "X-Arrow-Returned-Rows": "1",
                "X-Arrow-Row-Offset": "0",
            },
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as http:
        yield (
            AsyncStratifyX(base_url="https://backend.invalid", token="fixture", httpx_client=http),
            calls,
        )


def test_reference_does_not_copy_the_complete_relation_or_require_a_dashboard_exhibit():
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
            output = result.to_wire()["outputs"][0]
            assert "rows" not in output
            assert output["source"] == {
                "execution_id": "run-one",
                "table": "computed_sales",
                "field_ids": ["year", "sales"],
                "row_count": 2,
            }
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


def test_native_table_access_failure_keeps_its_domain_error():
    async def scenario():
        async with backend(denied=True) as (native, _):
            with pytest.raises(EpochError) as error:
                await assemble_response(
                    native,
                    "run-one",
                    "study-one",
                    manifest().declarations,
                    parts(),
                    table_sources=[source()],
                )
            assert error.value.error.code == "NOT_FOUND"
            assert error.value.execution_id == "run-one"

    asyncio.run(scenario())
