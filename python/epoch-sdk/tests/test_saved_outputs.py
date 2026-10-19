from __future__ import annotations

import asyncio
import copy
import json
from contextlib import asynccontextmanager
from datetime import date
from pathlib import Path

import httpx
import pyarrow as pa
import pytest
from jsonschema import Draft202012Validator
from pyarrow import ipc
from pydantic import ValidationError
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012
from stratifyx import AsyncStratifyX
from stratifyx.core.api_error import ApiError

from epoch_sdk import EpochError
from epoch_sdk.output_validation import JsonValueOutput, TableValue, TextValue
from epoch_sdk.saved_outputs import SavedOutputManifest, ValidatedSavedOutputs, read_saved_outputs

ROOT = Path(__file__).resolve().parents[3]


def manifest() -> SavedOutputManifest:
    return SavedOutputManifest.model_validate(
        {
            "execution_id": "run-one",
            "study_id": "study-one",
            "declarations": [
                {
                    "name": "sales",
                    "type": "table",
                    "schema": [
                        {"name": "year", "type": "int64", "description": "Calendar year"},
                        {"name": "sales", "type": "float64", "unit": "USD", "nullable": True},
                    ],
                },
                {
                    "name": "totals",
                    "type": "json",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "total": {"type": "number", "description": "Total sales in USD"}
                        },
                        "required": ["total"],
                        "additionalProperties": False,
                    },
                },
                {
                    "name": "report",
                    "type": "text",
                    "format": "markdown",
                    "instructions": "Report sales",
                },
            ],
            "bindings": [
                {
                    "name": "sales",
                    "type": "table",
                    "category": "ALL",
                    "table_index": 3,
                    "field_ids": ["native-year", "native-value"],
                },
                {"name": "totals", "type": "json", "category": "ALL", "markdown_id": "json-one"},
                {
                    "name": "report",
                    "type": "text",
                    "category": "ALL",
                    "markdown_id": "text-one",
                    "format": "markdown",
                },
            ],
        }
    )


def dashboard() -> dict:
    return {
        "charts": [],
        "event_marker_notes": {},
        "tables": [
            {
                "index": 3,
                "order": 0,
                "category": "ALL",
                "data_id": "native-data",
                "title": "A presentation title is not the requested output name",
                "table_name": "chart_all_native_data",
                "cards": [],
                "flavor": "Detailed",
                "columns": [
                    {"id": "native-year", "name": "Year label"},
                    {"id": "native-value", "name": "Revenue label"},
                ],
            }
        ],
        "content": {
            "categories": [{"id": "all", "native_category": "ALL", "title": "All"}],
            "graphs": [],
            "sections": [],
            "shared_parts": [],
            "studies": [],
            "markdown": [
                {"id": "json-one", "markdown": '{"total":12.5}'},
                {"id": "text-one", "markdown": "# Sales\nRevenue was USD 12.5."},
            ],
        },
    }


def arrow_bytes(
    table: pa.Table | None = None,
    *,
    stream: bool = False,
    chunksize: int = 1000,
    compression: str | None = None,
) -> bytes:
    if table is None:
        table = pa.table(
            {
                "native-year": pa.array([9007199254740993, 2025], type=pa.int64()),
                "native-value": pa.array([12.5, None], type=pa.float64()),
            }
        )
    sink = pa.BufferOutputStream()
    writer = ipc.new_stream if stream else ipc.new_file
    with writer(sink, table.schema, options=ipc.IpcWriteOptions(compression=compression)) as output:
        output.write_table(table, max_chunksize=chunksize)
    return sink.getvalue().to_pybytes()


@asynccontextmanager
async def native_backend(
    *,
    data: bytes | None = None,
    schema: dict | None = None,
    status: str = "completed",
    owner_status: int = 200,
    definition_id: str = "study-one",
    source_stream: httpx.AsyncByteStream | None = None,
):
    calls: list[httpx.Request] = []
    source = arrow_bytes() if data is None else data

    def respond(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        assert request.method == "GET", "A saved-output read must not submit work"
        if request.url.path == "/api/v1/studies/executions/run-one":
            return httpx.Response(
                200,
                json={
                    "id": "run-one",
                    "definition_id": definition_id,
                    "created_at": 1,
                    "execution_type": "research",
                    "status": status,
                },
            )
        if request.url.path == "/api/v1/studies/definitions/study-one":
            if owner_status != 200:
                return httpx.Response(
                    owner_status,
                    json={
                        "error": "DataNotFound",
                        "message": "Not found",
                        "timestamp": "2026-10-18T00:00:00Z",
                    },
                )
            return httpx.Response(
                200,
                json={
                    "name": "Saved study",
                    "description": "Fixture",
                    "source": "immutable saved source",
                    "authoring_origin": "agent",
                    "data": {"assets": []},
                },
            )
        if request.url.path == "/api/v1/studies/executions/run-one/dashboard/schema":
            assert request.url.params["category"] == "ALL"
            return httpx.Response(200, json=dashboard() if schema is None else schema)
        if request.url.path == "/api/v1/studies/executions/run-one/dashboard/data/native-data":
            if source_stream is not None:
                return httpx.Response(200, stream=source_stream)
            return httpx.Response(
                200, content=source, headers={"Content-Type": "application/vnd.apache.arrow.file"}
            )
        raise AssertionError(f"Unexpected native request: {request.url.path}")

    async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as http:
        yield (
            AsyncStratifyX(
                base_url="https://backend.invalid", token="fixture-only", httpx_client=http
            ),
            calls,
        )


@pytest.mark.parametrize("stream", [False, True])
def test_reads_saved_table_json_and_text_with_exact_values_and_annotations(stream: bool) -> None:
    async def scenario() -> None:
        reference = SavedOutputManifest.model_validate_json(
            manifest().model_dump_json(by_alias=True, exclude_unset=True)
        )
        async with native_backend(data=arrow_bytes(stream=stream, chunksize=1)) as (backend, calls):
            result = await read_saved_outputs(backend, reference)
        assert result.execution_id == "run-one" and result.study_id == "study-one"
        table, total, report = result.outputs
        assert isinstance(table, TableValue) and table.rows == [
            ["9007199254740993", 12.5],
            ["2025", None],
        ]
        assert table.columns[0].description == "Calendar year" and table.columns[1].unit == "USD"
        assert isinstance(total, JsonValueOutput) and total.value == {"total": 12.5}
        assert isinstance(report, TextValue) and report.value == "# Sales\nRevenue was USD 12.5."
        assert (
            result.declarations[1].to_wire()["schema"]["properties"]["total"]["description"]
            == "Total sales in USD"
        )
        assert len([call for call in calls if call.url.path.endswith("/dashboard/schema")]) == 1
        assert all(call.method == "GET" for call in calls)
        restored = ValidatedSavedOutputs.model_validate_json(json.dumps(result.to_wire()))
        assert restored.to_wire() == result.to_wire()

    asyncio.run(scenario())


def only_table(reference: SavedOutputManifest | None = None) -> SavedOutputManifest:
    value = (reference or manifest()).to_wire()
    value["declarations"] = value["declarations"][:1]
    value["bindings"] = value["bindings"][:1]
    return SavedOutputManifest.model_validate(value)


def test_nanosecond_timestamp_and_date_values_are_not_rounded_or_assigned_a_timezone() -> None:
    async def scenario() -> None:
        value = only_table().to_wire()
        value["declarations"][0]["schema"] = [
            {"name": "day", "type": "date"},
            {"name": "stamp", "type": "datetime"},
        ]
        value["bindings"][0]["field_ids"] = ["native-day", "native-stamp"]
        table = pa.table(
            {
                "native-day": pa.array([date(2024, 1, 1)], type=pa.date32()),
                "native-stamp": pa.array([1700000000000000123], type=pa.timestamp("ns", tz="UTC")),
            }
        )
        async with native_backend(data=arrow_bytes(table)) as (backend, _):
            result = await read_saved_outputs(backend, SavedOutputManifest.model_validate(value))
        assert isinstance(result.outputs[0], TableValue)
        assert result.outputs[0].rows == [["2024-01-01", "2023-11-14T22:13:20.000000123Z"]]

    asyncio.run(scenario())


def test_complete_later_batches_are_validated_instead_of_certifying_a_preview() -> None:
    async def scenario() -> None:
        table = pa.table({"native-year": ["2024", "not-an-integer"], "native-value": [12.5, 20.0]})
        async with native_backend(data=arrow_bytes(table, stream=True, chunksize=1)) as (
            backend,
            _,
        ):
            with pytest.raises(EpochError) as error:
                await read_saved_outputs(backend, only_table())
        assert error.value.error.code == "OUTPUT_VALIDATION_FAILED"
        assert error.value.execution_id == "run-one"

    asyncio.run(scenario())


@pytest.mark.parametrize(
    "text",
    [
        '{"total":"wrong-type"}',
        '{"total":1,"total":2}',
        '{"total":NaN}',
        '```json\n{"total":1}\n```',
    ],
)
def test_saved_json_must_be_exact_finite_json_and_satisfy_its_declared_schema(text: str) -> None:
    async def scenario() -> None:
        schema = dashboard()
        schema["content"]["markdown"][0]["markdown"] = text
        async with native_backend(schema=schema) as (backend, _):
            with pytest.raises(EpochError) as error:
                await read_saved_outputs(backend, manifest())
        assert error.value.error.code == "OUTPUT_VALIDATION_FAILED"
        assert error.value.execution_id == "run-one"

    asyncio.run(scenario())


@pytest.mark.parametrize(
    "status,code,retryable",
    [
        ("queued", "EXECUTION_NOT_READY", True),
        ("failed", "EXECUTION_FAILED", False),
        ("cancelled", "EXECUTION_FAILED", False),
    ],
)
def test_noncompleted_job_does_not_return_saved_outputs(
    status: str, code: str, retryable: bool
) -> None:
    async def scenario() -> None:
        async with native_backend(status=status) as (backend, calls):
            with pytest.raises(EpochError) as error:
                await read_saved_outputs(backend, manifest())
        assert error.value.error.code == code and error.value.error.retryable is retryable
        assert not any("/dashboard/" in call.url.path for call in calls)

    asyncio.run(scenario())


def test_owner_rejection_prevents_all_saved_artifact_reads() -> None:
    async def scenario() -> None:
        async with native_backend(owner_status=404) as (backend, calls):
            with pytest.raises(ApiError) as error:
                await read_saved_outputs(backend, manifest())
        assert error.value.status_code == 404
        assert not any("/dashboard/" in call.url.path for call in calls)

    asyncio.run(scenario())


def test_manifest_study_mismatch_cannot_read_another_jobs_artifacts() -> None:
    async def scenario() -> None:
        async with native_backend(definition_id="other-study") as (backend, calls):
            with pytest.raises(EpochError):
                await read_saved_outputs(backend, manifest())
        assert len(calls) == 1

    asyncio.run(scenario())


@pytest.mark.parametrize("max_bytes,max_rows", [(100, 1000), (8 * 1024 * 1024, 1)])
def test_complete_result_limits_fail_instead_of_returning_partial_rows(
    max_bytes: int, max_rows: int
) -> None:
    async def scenario() -> None:
        async with native_backend(data=arrow_bytes(chunksize=1)) as (backend, _):
            with pytest.raises(EpochError) as error:
                await read_saved_outputs(
                    backend, only_table(), max_bytes=max_bytes, max_rows=max_rows
                )
        assert error.value.error.code == "FETCH_LIMIT_EXCEEDED"

    asyncio.run(scenario())


def test_native_http_stream_is_closed_immediately_when_a_byte_limit_stops_the_read() -> None:
    class Stream(httpx.AsyncByteStream):
        closed = False

        async def __aiter__(self):
            yield b"x" * 1024
            yield b"unread remainder"

        async def aclose(self):
            self.closed = True

    async def scenario() -> None:
        stream = Stream()
        async with native_backend(source_stream=stream) as (backend, _):
            with pytest.raises(EpochError) as error:
                await read_saved_outputs(backend, only_table(), max_bytes=100)
            assert error.value.error.code == "FETCH_LIMIT_EXCEEDED"
            assert stream.closed

    asyncio.run(scenario())


def test_empty_table_still_checks_physical_types() -> None:
    async def scenario() -> None:
        good = pa.table(
            {
                "native-year": pa.array([], type=pa.int64()),
                "native-value": pa.array([], type=pa.float64()),
            }
        )
        bad = pa.table(
            {
                "native-year": pa.array([], type=pa.bool_()),
                "native-value": pa.array([], type=pa.float64()),
            }
        )
        async with native_backend(data=arrow_bytes(good)) as (backend, _):
            result = await read_saved_outputs(backend, only_table(), max_rows=0)
            assert isinstance(result.outputs[0], TableValue) and result.outputs[0].rows == []
        async with native_backend(data=arrow_bytes(bad)) as (backend, _):
            with pytest.raises(EpochError):
                await read_saved_outputs(backend, only_table())

    asyncio.run(scenario())


@pytest.mark.parametrize(
    "change",
    [
        "table-category",
        "markdown-category",
        "missing-markdown",
        "duplicate-markdown",
        "missing-data",
        "wrong-format",
    ],
)
def test_exact_source_bindings_are_required(change: str) -> None:
    async def scenario() -> None:
        schema = copy.deepcopy(dashboard())
        reference = manifest().to_wire()
        if change == "table-category":
            schema["tables"][0]["category"] = "OTHER"
        if change == "markdown-category":
            schema["content"]["categories"][0]["native_category"] = "OTHER"
        if change == "missing-markdown":
            schema["content"]["markdown"] = []
        if change == "duplicate-markdown":
            schema["content"]["markdown"].append(copy.deepcopy(schema["content"]["markdown"][0]))
        if change == "missing-data":
            schema["tables"][0]["data_id"] = ""
        if change == "wrong-format":
            reference["bindings"][2]["format"] = "plain"
        async with native_backend(schema=schema) as (backend, _):
            with pytest.raises(EpochError) as error:
                await read_saved_outputs(backend, SavedOutputManifest.model_validate(reference))
        assert error.value.error.code == "OUTPUT_VALIDATION_FAILED"

    asyncio.run(scenario())


def test_corrupt_native_arrow_payload_is_a_defined_output_failure() -> None:
    async def scenario() -> None:
        async with native_backend(data=b"invalid arrow") as (backend, _):
            with pytest.raises(EpochError) as error:
                await read_saved_outputs(backend, only_table())
        assert error.value.error.code == "OUTPUT_VALIDATION_FAILED"

    asyncio.run(scenario())


def test_dictionary_strings_and_boolean_nulls_preserve_their_native_values() -> None:
    async def scenario() -> None:
        value = only_table().to_wire()
        value["declarations"][0]["schema"] = [
            {"name": "label", "type": "string", "nullable": True},
            {"name": "enabled", "type": "boolean", "nullable": True},
        ]
        value["bindings"][0]["field_ids"] = ["labels", "booleans"]
        table = pa.table(
            {
                "labels": pa.DictionaryArray.from_arrays(
                    pa.array([0, 1, None]), pa.array(["A", "B"])
                ),
                "booleans": pa.array([True, False, None]),
            }
        )
        async with native_backend(data=arrow_bytes(table)) as (backend, _):
            result = await read_saved_outputs(backend, SavedOutputManifest.model_validate(value))
        assert isinstance(result.outputs[0], TableValue)
        assert result.outputs[0].rows == [["A", True], ["B", False], [None, None]]

    asyncio.run(scenario())


def test_a_naive_timestamp_does_not_acquire_an_invented_timezone() -> None:
    async def scenario() -> None:
        value = only_table().to_wire()
        value["declarations"][0]["schema"] = [{"name": "stamp", "type": "datetime"}]
        value["bindings"][0]["field_ids"] = ["stamp"]
        table = pa.table({"stamp": pa.array([1700000000000000123], type=pa.timestamp("ns"))})
        async with native_backend(data=arrow_bytes(table)) as (backend, _):
            with pytest.raises(EpochError):
                await read_saved_outputs(backend, SavedOutputManifest.model_validate(value))

    asyncio.run(scenario())


def test_compressed_ipc_is_limited_by_its_decoded_values_too() -> None:
    async def scenario() -> None:
        table = pa.table({"native-year": [2024] * 1000, "native-value": [12.5] * 1000})
        compressed = arrow_bytes(table, compression="lz4")
        assert len(compressed) < 10_000
        async with native_backend(data=compressed) as (backend, _):
            with pytest.raises(EpochError) as error:
                await read_saved_outputs(backend, only_table(), max_bytes=10_000)
        assert error.value.error.code == "FETCH_LIMIT_EXCEEDED"

    asyncio.run(scenario())


def test_unmatched_binding_names_are_rejected_before_native_calls() -> None:
    async def scenario() -> None:
        value = only_table().to_wire()
        value["bindings"][0]["name"] = "other"
        async with native_backend() as (backend, calls):
            with pytest.raises(EpochError):
                await read_saved_outputs(backend, SavedOutputManifest.model_validate(value))
        assert calls == []

    asyncio.run(scenario())


def test_decoded_byte_limit_applies_across_multiple_named_outputs() -> None:
    async def scenario() -> None:
        value = only_table().to_wire()
        second = copy.deepcopy(value["declarations"][0])
        second["name"] = "another_table"
        binding = copy.deepcopy(value["bindings"][0])
        binding["name"] = "another_table"
        value["declarations"].append(second)
        value["bindings"].append(binding)
        table = pa.table({"native-year": [2024] * 1000, "native-value": [12.5] * 1000})
        compressed = arrow_bytes(table, compression="lz4")
        assert len(compressed) * 2 < 30_000
        async with native_backend(data=compressed) as (backend, _):
            with pytest.raises(EpochError) as error:
                await read_saved_outputs(
                    backend, SavedOutputManifest.model_validate(value), max_bytes=30_000
                )
        assert error.value.error.code == "FETCH_LIMIT_EXCEEDED"

    asyncio.run(scenario())


@pytest.mark.parametrize("bad", [None, "unknown_field", "bad_index", "null_category"])
def test_manifest_example_and_python_wire_agree_with_the_shared_schema(bad: str | None) -> None:
    path = ROOT / "contracts/saved-output-manifest.schema.json"
    core = ROOT / "contracts/openapi.json"
    registry = Registry().with_resources(
        [
            (
                path.as_uri(),
                Resource.from_contents(
                    json.loads(path.read_text()), default_specification=DRAFT202012
                ),
            ),
            (
                core.as_uri(),
                Resource.from_contents(
                    json.loads(core.read_text()), default_specification=DRAFT202012
                ),
            ),
        ]
    )
    validator = Draft202012Validator({"$ref": path.as_uri()}, registry=registry)
    value = json.loads((ROOT / "contracts/saved-output-manifest.example.json").read_text())
    if bad == "unknown_field":
        value["bindings"][0]["query"] = "Unexpected input"
    if bad == "bad_index":
        value["bindings"][0]["table_index"] = True
    if bad == "null_category":
        value["bindings"][0]["category"] = None
    if bad is None:
        parsed = SavedOutputManifest.model_validate(value)
        validator.validate(parsed.to_wire())
        assert parsed.to_wire() == value
    else:
        assert not validator.is_valid(value)
        with pytest.raises(ValidationError):
            SavedOutputManifest.model_validate(value)
