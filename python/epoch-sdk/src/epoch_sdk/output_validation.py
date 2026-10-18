"""Validate materialized named outputs before declaring an analysis successful."""

from __future__ import annotations

import math
import re
from datetime import date, datetime
from typing import Annotated, Literal

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError as JsonValidationError
from pydantic import BaseModel, ConfigDict, Field, JsonValue, TypeAdapter, field_validator
from referencing import Registry

from .contracts import (
    Column,
    DomainError,
    JsonOutputRequest,
    OutputName,
    OutputRequest,
    TableOutputRequest,
    TextOutputRequest,
)
from .errors import EpochError


class MaterializedOutput(BaseModel):
    """Closed result boundary; arbitrary JSON is confined to a JSON output value."""

    model_config = ConfigDict(extra="forbid", strict=True, allow_inf_nan=False)
    name: OutputName


type Cell = str | int | float | bool | None


class TableValue(MaterializedOutput):
    type: Literal["table"]
    columns: list[Column] = Field(alias="schema")
    rows: list[list[Cell]]


class JsonValueOutput(MaterializedOutput):
    type: Literal["json"]
    value: JsonValue

    @field_validator("value")
    @classmethod
    def finite_json(cls, value: JsonValue) -> JsonValue:
        def check(item: JsonValue) -> None:
            if isinstance(item, float) and not math.isfinite(item):
                raise ValueError("JSON numbers must be finite")
            if isinstance(item, list):
                for child in item:
                    check(child)
            elif isinstance(item, dict):
                for child in item.values():
                    check(child)

        check(value)
        return value


class TextValue(MaterializedOutput):
    type: Literal["text"]
    format: Literal["plain", "markdown"]
    value: str


type OutputValue = Annotated[TableValue | JsonValueOutput | TextValue, Field(discriminator="type")]
OUTPUT_VALUES = TypeAdapter(list[OutputValue])


def _fail(message: str, execution_id: str | None) -> EpochError:
    return EpochError(
        DomainError(code="OUTPUT_VALIDATION_FAILED", message=message, retryable=False),
        execution_id=execution_id,
    )


def _valid_cell(column: Column, value: Cell) -> bool:
    if value is None:
        return column.nullable
    if column.type == "string":
        return type(value) is str
    if column.type == "boolean":
        return type(value) is bool
    if column.type == "float64":
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            return False
        try:
            return math.isfinite(value)
        except OverflowError:
            return False
    if not isinstance(value, str):
        return False
    if column.type == "int64":
        return (
            len(value) <= 20
            and bool(re.fullmatch(r"-?(0|[1-9][0-9]*)", value))
            and -(2**63) <= int(value) < 2**63
        )
    try:
        if column.type == "date":
            return bool(re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value)) and bool(
                date.fromisoformat(value)
            )
        if not re.fullmatch(
            r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}"
            r"(?:\.[0-9]+)?(?:Z|[+-][0-9]{2}:[0-9]{2})",
            value,
        ):
            return False
        return datetime.fromisoformat(value).utcoffset() is not None
    except ValueError:
        return False


def validate_outputs(
    declarations: list[OutputRequest],
    values: list[OutputValue],
    *,
    execution_id: str | None = None,
) -> list[OutputValue]:
    """Require every named output and validate the actual values, not a preview.

    Readers must materialize the complete bounded result or report a limit/error;
    passing a preview here cannot certify an unavailable remainder.
    """
    expected = {output.name: output for output in declarations}
    actual = {output.name: output for output in values}
    if (
        len(expected) != len(declarations)
        or len(actual) != len(values)
        or expected.keys() != actual.keys()
    ):
        raise _fail(
            "Returned output names must match every requested name exactly once.", execution_id
        )
    for name, declaration in expected.items():
        value = actual[name]
        if isinstance(declaration, TableOutputRequest) and isinstance(value, TableValue):
            if [
                column.model_dump(by_alias=True, exclude_none=True)
                for column in declaration.columns
            ] != [column.model_dump(by_alias=True, exclude_none=True) for column in value.columns]:
                raise _fail(f"Output {name}: ordered columns and annotations differ.", execution_id)
            for index, row in enumerate(value.rows):
                if len(row) != len(declaration.columns) or any(
                    not _valid_cell(column, cell)
                    for column, cell in zip(declaration.columns, row, strict=False)
                ):
                    raise _fail(
                        f"Output {name}: row {index} violates its declared schema.", execution_id
                    )
        elif isinstance(declaration, JsonOutputRequest) and isinstance(value, JsonValueOutput):
            validator = Draft202012Validator(
                declaration.json_schema,
                registry=Registry(),
                format_checker=FormatChecker(),
            )
            try:
                # jsonschema leaves its public validate(*args, **kwargs) untyped.
                validator.validate(value.value)  # pyright: ignore[reportUnknownMemberType]
            except JsonValidationError as error:
                path = "/".join(str(item) for item in error.absolute_path)
                raise _fail(
                    f"Output {name}: JSON value fails its schema at /{path}.", execution_id
                ) from error
        elif isinstance(declaration, TextOutputRequest) and isinstance(value, TextValue):
            if declaration.format != value.format:
                raise _fail(f"Output {name}: text format differs from the request.", execution_id)
        else:
            raise _fail(f"Output {name}: result type differs from the request.", execution_id)
    return [actual[output.name] for output in declarations]
