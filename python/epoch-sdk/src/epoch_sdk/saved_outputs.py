"""Read explicit saved-artifact bindings through the native Backend client.

Bindings/declarations must come from the accepted request's saved manifest.
This component does not discover bindings, persist that manifest, execute a
study, or infer named outputs from assistant prose or presentation titles.
"""

from __future__ import annotations

from collections.abc import Iterator
from datetime import date, datetime
from importlib import import_module
from typing import Annotated, Literal, Protocol, cast

from pydantic import ConfigDict, Field
from stratifyx import AsyncStratifyX
from stratifyx.types.dashboard_schema import DashboardSchema

from .contracts import (
    Column,
    Contract,
    DomainError,
    ExecutionId,
    JsonOutputRequest,
    NonBlank,
    OutputName,
    OutputRequest,
    TableOutputRequest,
    TextOutputRequest,
)
from .errors import EpochError
from .output_validation import (
    Cell,
    JsonValueOutput,
    OutputValue,
    TableValue,
    TextValue,
    validate_outputs,
)
from .parsing import parse_json


class TableBinding(Contract):
    name: OutputName
    type: Literal["table"]
    category: NonBlank
    table_index: Annotated[int, Field(ge=0)]
    # Exact physical Arrow field ids, in requested output-column order. These
    # allow explicit aliases without SQL or guessing from presentation titles.
    field_ids: Annotated[list[NonBlank], Field(min_length=1)]


class JsonBinding(Contract):
    name: OutputName
    type: Literal["json"]
    category: NonBlank
    markdown_id: NonBlank


class TextBinding(Contract):
    name: OutputName
    type: Literal["text"]
    category: NonBlank
    markdown_id: NonBlank
    format: Literal["plain", "markdown"]


type OutputBinding = Annotated[
    TableBinding | JsonBinding | TextBinding, Field(discriminator="type")
]


class SavedOutputManifest(Contract):
    """Explicit per-execution read plan; persistence is owned by Backend."""

    execution_id: ExecutionId
    study_id: NonBlank
    declarations: Annotated[list[OutputRequest], Field(min_length=1)]
    bindings: Annotated[list[OutputBinding], Field(min_length=1)]


class ValidatedSavedOutputs(Contract):
    model_config = ConfigDict(extra="forbid", strict=True)
    execution_id: str
    study_id: str
    declarations: list[OutputRequest]
    outputs: list[OutputValue]


class _Field(Protocol):
    name: str
    type: object


class _Schema(Protocol):
    names: list[str]

    def field(self, index: int) -> _Field: ...


class _Array(Protocol):
    def to_pylist(self) -> list[object]: ...
    def cast(self, target_type: object) -> _Array: ...


class _Arrow(Protocol):
    def string(self) -> object: ...


class _Batch(Protocol):
    schema: _Schema
    num_rows: int
    nbytes: int

    def column(self, index: int) -> _Array: ...


class _FileReader(Protocol):
    schema: _Schema
    num_record_batches: int

    def get_batch(self, index: int) -> _Batch: ...


class _StreamReader(Protocol):
    schema: _Schema

    def __iter__(self) -> Iterator[_Batch]: ...


class _IPC(Protocol):
    def open_file(self, source: bytes) -> _FileReader: ...
    def open_stream(self, source: bytes) -> _StreamReader: ...


class _Types(Protocol):
    def is_integer(self, value: object) -> bool: ...
    def is_floating(self, value: object) -> bool: ...
    def is_boolean(self, value: object) -> bool: ...
    def is_string(self, value: object) -> bool: ...
    def is_large_string(self, value: object) -> bool: ...
    def is_string_view(self, value: object) -> bool: ...
    def is_dictionary(self, value: object) -> bool: ...
    def is_date(self, value: object) -> bool: ...
    def is_timestamp(self, value: object) -> bool: ...


class _DictionaryType(Protocol):
    value_type: object


class _TimestampType(Protocol):
    tz: str | None


def _failure(
    code: Literal[
        "OUTPUT_VALIDATION_FAILED",
        "EXECUTION_NOT_READY",
        "EXECUTION_FAILED",
        "FETCH_LIMIT_EXCEEDED",
    ],
    message: str,
    execution_id: str,
) -> EpochError:
    return EpochError(
        DomainError(code=code, message=message, retryable=code == "EXECUTION_NOT_READY"),
        execution_id=execution_id,
    )


def _invalid(message: str, execution_id: str) -> EpochError:
    return _failure("OUTPUT_VALIDATION_FAILED", message, execution_id)


def _compatible(kind: object, column: Column, types: _Types) -> bool:
    if types.is_dictionary(kind):
        kind = cast(_DictionaryType, kind).value_type
    string = types.is_string(kind) or types.is_large_string(kind) or types.is_string_view(kind)
    if column.type == "string":
        return string
    if column.type == "boolean":
        return types.is_boolean(kind)
    if column.type == "int64":
        return types.is_integer(kind) or string
    if column.type == "float64":
        return types.is_floating(kind) or types.is_integer(kind)
    if column.type == "date":
        return types.is_date(kind) or string
    return string or (types.is_timestamp(kind) and cast(_TimestampType, kind).tz is not None)


def _cell(value: object, column: Column, execution_id: str) -> Cell:
    if value is None:
        return None
    if column.type == "int64" and type(value) is int:
        return str(value)
    if column.type == "date" and type(value) is date:
        return value.isoformat()
    if column.type == "datetime" and isinstance(value, datetime):
        return value.isoformat()
    if type(value) in (str, int, float, bool):
        return cast(Cell, value)
    raise _invalid(f"Output column {column.name} has an unsupported stored value.", execution_id)


def _table(
    data: bytes,
    declaration: TableOutputRequest,
    binding: TableBinding,
    execution_id: str,
    *,
    max_rows: int,
    max_bytes: int,
) -> tuple[TableValue, int]:
    # PyArrow 26 has no bundled type stubs. Keep a narrow typed interface to its
    # actual IPC API; Arrow fields/batches never become untyped business state.
    ipc = cast(_IPC, import_module("pyarrow.ipc"))
    types = cast(_Types, import_module("pyarrow.types"))
    arrow = cast(_Arrow, import_module("pyarrow"))
    file = ipc.open_file(data) if data.startswith(b"ARROW1") else None
    stream = ipc.open_stream(data) if file is None else None
    assert file is not None or stream is not None
    schema = file.schema if file is not None else cast(_StreamReader, stream).schema
    if len(binding.field_ids) != len(declaration.columns):
        raise _invalid("Table binding must identify each output column exactly once.", execution_id)
    positions: list[int] = []
    for field_id, column in zip(binding.field_ids, declaration.columns, strict=True):
        if schema.names.count(field_id) != 1:
            raise _invalid(f"Stored field {field_id} is missing or duplicated.", execution_id)
        index = schema.names.index(field_id)
        if not _compatible(schema.field(index).type, column, types):
            raise _invalid(f"Stored field {field_id} has an incompatible Arrow type.", execution_id)
        positions.append(index)
    batches = (
        (file.get_batch(i) for i in range(file.num_record_batches))
        if file is not None
        else iter(cast(_StreamReader, stream))
    )
    rows: list[list[Cell]] = []
    expanded = 0
    for batch in batches:
        expanded += batch.nbytes
        if len(rows) + batch.num_rows > max_rows or expanded > max_bytes:
            raise _failure(
                "FETCH_LIMIT_EXCEEDED", "Complete saved table exceeds the read limit.", execution_id
            )
        columns: list[list[object]] = []
        for index, column in zip(positions, declaration.columns, strict=True):
            array = batch.column(index)
            kind = schema.field(index).type
            if types.is_dictionary(kind):
                kind = cast(_DictionaryType, kind).value_type
            if column.type == "datetime" and types.is_timestamp(kind):
                # Arrow's string cast retains nanoseconds; Python datetime can
                # reduce precision or require the optional pandas dependency.
                columns.append(
                    [
                        item.replace(" ", "T", 1) if isinstance(item, str) else item
                        for item in array.cast(arrow.string()).to_pylist()
                    ]
                )
            else:
                columns.append(array.to_pylist())
        for row in zip(*columns, strict=True):
            rows.append(
                [
                    _cell(value, column, execution_id)
                    for value, column in zip(row, declaration.columns, strict=True)
                ]
            )
    return TableValue(
        name=declaration.name, type="table", schema=declaration.columns, rows=rows
    ), expanded


async def read_saved_outputs(
    backend: AsyncStratifyX,
    manifest: SavedOutputManifest,
    *,
    max_bytes: int = 8 * 1024 * 1024,
    max_rows: int = 10_000,
) -> ValidatedSavedOutputs:
    """Read complete bounded values and validate them; launch no agent or job.

    Declarations preserve the accepted semantic descriptions/units. Explicit
    bindings identify the physical sources; presentation titles are not inferred
    to be output names. This does not certify analytical correctness.
    """
    execution_id = manifest.execution_id
    if max_bytes <= 0 or max_rows < 0:
        raise ValueError("Read limits must be positive (zero rows permits empty tables)")
    declarations = {item.name: item for item in manifest.declarations}
    bindings = {item.name: item for item in manifest.bindings}
    if (
        len(declarations) != len(manifest.declarations)
        or len(bindings) != len(manifest.bindings)
        or declarations.keys() != bindings.keys()
    ):
        raise _invalid("Bindings must match every declared output exactly once.", execution_id)
    job = await backend.studies_executions.get_execution_by_id(
        execution_id, request_options={"max_retries": 0}
    )
    if job.id != execution_id or job.definition_id != manifest.study_id:
        raise _invalid(
            "Saved output manifest does not match the Backend execution/study.", execution_id
        )
    # Owner-scoped definition read before returning any data, including for
    # legacy execution-read endpoints whose ownership audit is separate.
    await backend.studies_definitions.get_a_study_definition_by_id(
        manifest.study_id, request_options={"max_retries": 0}
    )
    if job.status.value != "completed":
        raise _failure(
            "EXECUTION_FAILED"
            if job.status.value in ("failed", "cancelled")
            else "EXECUTION_NOT_READY",
            f"Execution is {job.status.value}; saved outputs are not ready.",
            execution_id,
        )
    schemas: dict[str, DashboardSchema] = {}
    values: list[OutputValue] = []
    used_bytes = 0
    expanded_bytes = 0
    for declaration in manifest.declarations:
        binding = bindings[declaration.name]
        if binding.type != declaration.type:
            raise _invalid("Binding type differs from the declared output type.", execution_id)
        if binding.category not in schemas:
            schemas[
                binding.category
            ] = await backend.studies_dashboard.get_dashboard_schema_chart_specs_table_specs_card_values(
                execution_id, category=binding.category, request_options={"max_retries": 0}
            )
        schema = schemas[binding.category]
        if isinstance(binding, TableBinding) and isinstance(declaration, TableOutputRequest):
            tables = [
                table
                for table in schema.tables
                if table.index == binding.table_index and table.category == binding.category
            ]
            if len(tables) != 1 or not tables[0].data_id:
                raise _invalid(
                    "The exact saved table binding is missing or ambiguous.", execution_id
                )
            data = bytearray()
            async with (
                backend.studies_dashboard.with_raw_response.get_chart_table_data_as_arrow_ipc(
                    execution_id,
                    tables[0].data_id,
                    category=binding.category,
                    request_options={"max_retries": 0},
                ) as response
            ):
                async for chunk in response.data:
                    used_bytes += len(chunk)
                    if used_bytes > max_bytes:
                        raise _failure(
                            "FETCH_LIMIT_EXCEEDED",
                            "Complete saved outputs exceed the byte limit.",
                            execution_id,
                        )
                    data.extend(chunk)
            try:
                value, expanded = _table(
                    bytes(data),
                    declaration,
                    binding,
                    execution_id,
                    max_rows=max_rows,
                    max_bytes=max_bytes - expanded_bytes,
                )
                expanded_bytes += expanded
            except EpochError:
                raise
            except (ValueError, TypeError, OSError) as error:
                raise _invalid(
                    "Stored table is not a supported Arrow IPC file/stream.", execution_id
                ) from error
            values.append(value)
        else:
            if not isinstance(binding, (JsonBinding, TextBinding)):
                raise _invalid("Unsupported saved output binding.", execution_id)
            markdown = schema.content.markdown if schema.content is not None else []
            if schema.content is None or binding.category not in {
                item.native_category or item.id for item in schema.content.categories
            }:
                raise _invalid(
                    "The requested saved Markdown category is unavailable.", execution_id
                )
            matches = [item for item in markdown if item.id == binding.markdown_id]
            if len(matches) != 1:
                raise _invalid(
                    "The exact saved Markdown binding is missing or ambiguous.", execution_id
                )
            text = matches[0].markdown
            used_bytes += len(text.encode("utf-8"))
            expanded_bytes += len(text.encode("utf-8"))
            if used_bytes > max_bytes or expanded_bytes > max_bytes:
                raise _failure(
                    "FETCH_LIMIT_EXCEEDED",
                    "Complete saved outputs exceed the byte limit.",
                    execution_id,
                )
            if isinstance(binding, JsonBinding) and isinstance(declaration, JsonOutputRequest):
                try:
                    values.append(
                        JsonValueOutput.model_validate(
                            {"name": binding.name, "type": "json", "value": parse_json(text)}
                        )
                    )
                except (ValueError, TypeError) as error:
                    raise _invalid(
                        "Stored JSON output is not strict, finite JSON.", execution_id
                    ) from error
            elif isinstance(binding, TextBinding) and isinstance(declaration, TextOutputRequest):
                values.append(
                    TextValue(name=binding.name, type="text", format=binding.format, value=text)
                )
            else:
                raise _invalid("Unsupported saved output binding.", execution_id)
    return ValidatedSavedOutputs(
        execution_id=execution_id,
        study_id=manifest.study_id,
        declarations=manifest.declarations,
        outputs=validate_outputs(manifest.declarations, values, execution_id=execution_id),
    )
