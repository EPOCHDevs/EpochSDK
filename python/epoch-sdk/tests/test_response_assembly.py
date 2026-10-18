from __future__ import annotations

import asyncio

import pytest
from test_saved_outputs import dashboard, manifest, native_backend

from epoch_sdk import EpochError
from epoch_sdk.output_validation import JsonValueOutput, TableValue, TextValue
from epoch_sdk.responses import assemble_response


def interpreted():
    return [
        JsonValueOutput(name="totals", type="json", value={"total": 12.5}),
        TextValue(name="report", type="text", format="markdown", value="Sales were USD 12.5."),
    ]


def native_schema():
    result = dashboard()
    result["tables"][0]["id"] = "sales"
    result["tables"][0]["columns"][0]["name"] = "year"
    result["tables"][0]["columns"][1]["name"] = "sales"
    # Interpretation need not be embedded in a native Markdown block.
    result["content"] = None
    return result


def test_assembly_reads_complete_native_table_and_preserves_interpreted_parts():
    async def scenario():
        async with native_backend(schema=native_schema()) as (backend, calls):
            result = await assemble_response(
                backend, "run-one", "study-one", manifest().declarations, interpreted(),
            )
        table = result.outputs[0]
        assert isinstance(table, TableValue)
        assert table.rows == [["9007199254740993", 12.5], ["2025", None]]
        assert table.columns[0].description == "Calendar year"
        assert result.outputs[1:] == interpreted()
        assert all(item.method == "GET" for item in calls)

    asyncio.run(scenario())


@pytest.mark.parametrize("parts", [[], interpreted()[:1], interpreted() * 2])
def test_missing_or_duplicate_interpretations_fail_before_native_io(parts):
    async def scenario():
        async with native_backend() as (backend, calls):
            with pytest.raises(EpochError):
                await assemble_response(
                    backend, "run-one", "study-one", manifest().declarations, parts,
                )
            assert not calls

    asyncio.run(scenario())


def test_wrong_native_exhibit_cannot_be_published_under_a_requested_table_name():
    async def scenario():
        async with native_backend(schema=dashboard()) as (backend, calls):
            with pytest.raises(EpochError) as error:
                await assemble_response(
                    backend, "run-one", "study-one", manifest().declarations, interpreted(),
                )
            assert error.value.error.code == "OUTPUT_VALIDATION_FAILED"
            assert not any("/dashboard/data/" in item.url.path for item in calls)

    asyncio.run(scenario())
