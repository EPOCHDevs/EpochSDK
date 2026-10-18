from __future__ import annotations

import pytest
from pydantic import ValidationError

from epoch_sdk.contracts import Column, JsonOutputRequest, TableOutputRequest, TextOutputRequest
from epoch_sdk.errors import EpochError
from epoch_sdk.output_validation import (
    OUTPUT_VALUES,
    JsonValueOutput,
    TableValue,
    TextValue,
    validate_outputs,
)


def table(column_type: str = "float64", nullable: bool = False) -> TableOutputRequest:
    return TableOutputRequest.model_validate(
        {
            "name": "sales",
            "type": "table",
            "schema": [
                {
                    "name": "value",
                    "type": column_type,
                    "description": "Approved sales",
                    "nullable": nullable,
                }
            ],
        }
    )


@pytest.mark.parametrize(
    ("kind", "valid", "invalid"),
    [
        ("string", "revenue", 5),
        ("int64", "9223372036854775807", "9223372036854775808"),
        ("int64", "-9223372036854775808", "-9223372036854775809"),
        ("int64", "1", 1),
        ("int64", "0", "01"),
        ("float64", 123.5, True),
        ("float64", 123, "123"),
        ("boolean", False, 0),
        ("date", "2024-02-29", "2023-02-29"),
        ("date", "2024-01-01", "20240101"),
        ("datetime", "2024-01-01T12:00:00Z", "2024-01-01T12:00:00"),
        ("datetime", "2024-01-01T12:00:00+01:00", "2024-13-01T12:00:00Z"),
    ],
)
def test_actual_table_values_obey_declared_types(kind: str, valid: object, invalid: object) -> None:
    declaration = table(kind)
    accepted = TableValue.model_validate(
        {
            "name": "sales",
            "type": "table",
            "schema": [c.to_wire() for c in declaration.columns],
            "rows": [[valid]],
        }
    )
    assert validate_outputs([declaration], [accepted]) == [accepted]
    rejected = TableValue.model_validate(
        {**accepted.model_dump(by_alias=True, exclude_none=True), "rows": [[invalid]]}
    )
    with pytest.raises(EpochError) as failure:
        validate_outputs([declaration], [rejected], execution_id="exec_accepted")
    assert failure.value.error.code == "OUTPUT_VALIDATION_FAILED"
    assert failure.value.execution_id == "exec_accepted"


@pytest.mark.parametrize("rows", [[[None]], [[1, 2]], [[]]])
def test_nullability_and_row_width(rows: list) -> None:
    declaration = table()
    value = TableValue.model_validate(
        {
            "name": "sales",
            "type": "table",
            "schema": [c.to_wire() for c in declaration.columns],
            "rows": rows,
        }
    )
    with pytest.raises(EpochError):
        validate_outputs([declaration], [value])


def test_nullable_values_and_empty_tables_are_valid() -> None:
    declaration = table(nullable=True)
    for rows in [[], [[None]]]:
        value = TableValue(name="sales", type="table", schema=declaration.columns, rows=rows)
        assert validate_outputs([declaration], [value]) == [value]


def test_all_named_outputs_are_required_and_return_in_declaration_order() -> None:
    sales = table()
    notes = TextOutputRequest(
        name="notes", type="text", instructions="Describe the result", format="markdown"
    )
    values = [
        TextValue(name="notes", type="text", format="markdown", value="**Sales**"),
        TableValue(name="sales", type="table", schema=sales.columns, rows=[[1.0]]),
    ]
    assert [value.name for value in validate_outputs([sales, notes], values)] == ["sales", "notes"]
    for invalid in [
        values[:1],
        values + values[:1],
        [values[0].model_copy(update={"name": "wrong"}), values[1]],
    ]:
        with pytest.raises(EpochError):
            validate_outputs([sales, notes], invalid)


def test_changed_columns_annotations_and_format_are_rejected() -> None:
    declaration = table()
    value = TableValue(
        name="sales",
        type="table",
        schema=[Column(name="value", type="float64", description="A different meaning")],
        rows=[[1]],
    )
    with pytest.raises(EpochError):
        validate_outputs([declaration], [value])
    text = TextOutputRequest(name="notes", type="text", instructions="Summarize", format="markdown")
    with pytest.raises(EpochError):
        validate_outputs(
            [text], [TextValue(name="notes", type="text", format="plain", value="Summary")]
        )


def test_json_values_obey_nested_local_schema_and_format() -> None:
    declaration = JsonOutputRequest.model_validate(
        {
            "name": "detail",
            "type": "json",
            "schema": {
                "$defs": {"date": {"type": "string", "format": "date"}},
                "type": "object",
                "required": ["as_of"],
                "additionalProperties": False,
                "properties": {
                    "as_of": {"$ref": "#/$defs/date", "description": "Date of the source"}
                },
            },
        }
    )
    valid = JsonValueOutput(name="detail", type="json", value={"as_of": "2024-02-29"})
    assert validate_outputs([declaration], [valid]) == [valid]
    for raw in [{"as_of": "2023-02-29"}, {}, {"as_of": "2024-01-01", "extra": True}, None]:
        with pytest.raises(EpochError):
            validate_outputs(
                [declaration], [JsonValueOutput(name="detail", type="json", value=raw)]
            )
    null_schema = JsonOutputRequest.model_validate(
        {"name": "detail", "type": "json", "schema": {"type": "null"}}
    )
    assert validate_outputs(
        [null_schema], [JsonValueOutput(name="detail", type="json", value=None)]
    )


@pytest.mark.parametrize(
    "wire",
    [
        [{"name": "sales", "type": "table", "schema": [], "rows": [[float("nan")]]}],
        [{"name": "detail", "type": "json", "value": {"nested": [float("inf")]}}],
        [{"name": "detail", "type": "json", "value": {}, "extra": "ignored"}],
    ],
)
def test_untrusted_materialized_values_are_closed_and_finite(wire: object) -> None:
    with pytest.raises(ValidationError):
        OUTPUT_VALUES.validate_python(wire)
