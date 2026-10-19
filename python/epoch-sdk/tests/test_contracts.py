from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker
from pydantic import ValidationError
from stratifyx import DatePeriodConfig, ExecutionOptions

from epoch_sdk import (
    Acknowledgement,
    DomainError,
    EpochError,
    ErrorResponse,
    IngestRequest,
    JsonOutputRequest,
    RefreshRequest,
    RunRequest,
    TableOutputRequest,
    parse_fetch,
)
from epoch_sdk.parsing import parse_request

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT.parents[1] / "contracts/openapi.json"


def table() -> dict:
    return {
        "name": "sales",
        "type": "table",
        "schema": [
            {"name": "year", "type": "int64", "description": "Calendar year"},
            {"name": "sales", "type": "float64", "unit": "USD", "nullable": True},
        ],
    }


def request() -> dict:
    return {"task": "Compare annual sales", "outputs": [table()]}


def clarification() -> dict:
    return {
        "code": "CLARIFICATION_REQUIRED",
        "message": "Choose a period",
        "retryable": False,
        "gaps": [{"field": "/task", "description": "Missing period"}],
        "questions": [
            {"question": "Which period?", "options": ["2024", "2025"], "recommended_option": "2025"}
        ],
        "recommended_task": "Compare annual sales in [chosen year]",
    }


def wire_validator(name: str) -> Draft202012Validator:
    schemas = json.loads(CONTRACT.read_text())["components"]["schemas"]
    return Draft202012Validator(
        {"$ref": f"#/components/schemas/{name}", "components": {"schemas": schemas}},
        format_checker=FormatChecker(),
    )


def test_run_preserves_descriptions_and_native_parameter_types() -> None:
    wire = {
        **request(),
        "source_execution_id": "engine_original",
        "parameters": {
            "period": {"start": "2024-01-01", "end": "2024-12-31"},
            "execution": {"cash": 10000},
        },
    }
    parsed = parse_request(RunRequest, json.dumps(wire))
    assert parsed.to_wire() == wire
    assert parsed.parameters is not None
    assert isinstance(parsed.parameters.period, DatePeriodConfig)
    assert isinstance(parsed.parameters.execution, ExecutionOptions)
    assert isinstance(parsed.outputs[0], TableOutputRequest)
    assert parsed.outputs[0].columns[0].description == "Calendar year"
    wire_validator("RunRequest").validate(wire)


@pytest.mark.parametrize(
    "patch",
    [
        {"task": "   "},
        {"task": 12},
        {"auto_ingest": "false"},
        {"context": None},
        {"outputs": []},
        {"unexpected": 1},
        {"task": None},
        {"study_id": "study_a", "source_execution_id": "exec_a"},
        {"parameters": {"period": {"start": "2024-13-01"}}},
        {"parameters": {"execution": {"cash": True}}},
        {"parameters": {"execution": {"cash": "10000"}}},
        {"parameters": {"execution": {"made_up": 10}}},
        {"parameters": {"study_id": "hidden_rebinding"}},
    ],
)
def test_bad_run_inputs_fail_before_service_calls(patch: dict) -> None:
    wire = {**request(), **patch}
    with pytest.raises(ValidationError):
        RunRequest.model_validate(wire)
    assert not wire_validator("RunRequest").is_valid(wire)
    assert not Draft202012Validator(
        RunRequest.model_json_schema(), format_checker=FormatChecker()
    ).is_valid(wire)


def test_reversed_period_is_a_semantic_error() -> None:
    with pytest.raises(ValidationError, match="must not follow"):
        RunRequest.model_validate(
            {
                **request(),
                "parameters": {
                    "period": {
                        "start": "2025-01-01",
                        "end": "2024-01-01",
                    }
                },
            }
        )


def test_duplicate_output_and_column_names_fail() -> None:
    with pytest.raises(ValidationError, match="Output names"):
        RunRequest.model_validate({**request(), "outputs": [table(), table()]})
    duplicate = table()
    duplicate["schema"].append(copy.deepcopy(duplicate["schema"][0]))
    with pytest.raises(ValidationError, match="column names"):
        RunRequest.model_validate({**request(), "outputs": [duplicate]})


def test_false_and_annotated_json_schemas_are_supported() -> None:
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "$defs": {"amount": {"type": "number", "description": "USD amount"}},
        "properties": {"sales": {"$ref": "#/$defs/amount"}, "$ref": {"type": "string"}},
        "examples": [{"$ref": "https://example.com/this-is-example-data"}],
    }
    parsed = JsonOutputRequest.model_validate({"name": "summary", "type": "json", "schema": schema})
    assert parsed.to_wire()["schema"] == schema
    assert (
        JsonOutputRequest.model_validate(
            {"name": "none", "type": "json", "schema": False}
        ).json_schema
        is False
    )


@pytest.mark.parametrize(
    "schema",
    [
        {"type": "imaginary"},
        {"$ref": "https://example.com/schema"},
        {"$defs": {"unused": {"$ref": "file:///private/schema.json"}}},
        {"$dynamicRef": "https://example.com/dynamic"},
        {"$ref": "#/$defs/missing"},
        {"$ref": "#/description", "description": "not a schema"},
        {"$schema": "http://json-schema.org/draft-07/schema#"},
    ],
)
def test_invalid_or_external_json_schema_fails_without_fetching(schema: dict) -> None:
    with pytest.raises(ValidationError):
        JsonOutputRequest.model_validate({"name": "summary", "type": "json", "schema": schema})


def test_recursive_and_anchored_local_schemas() -> None:
    for schema in [
        {
            "$defs": {
                "node": {"type": "object", "properties": {"child": {"$ref": "#/$defs/node"}}}
            },
            "$ref": "#/$defs/node",
        },
        {
            "$id": "https://example.com/root",
            "$defs": {"amount": {"$anchor": "amount", "type": "number"}},
            "$ref": "#amount",
        },
    ]:
        assert (
            JsonOutputRequest.model_validate(
                {"name": "summary", "type": "json", "schema": schema}
            ).json_schema
            == schema
        )


def test_nested_resource_ids_keep_local_reference_scope() -> None:
    schema = {
        "$id": "https://example.com/root",
        "$defs": {
            "child": {
                "$id": "child",
                "$defs": {"value": {"type": "number"}},
                "$ref": "#/$defs/value",
            }
        },
    }
    assert (
        JsonOutputRequest.model_validate(
            {"name": "nested", "type": "json", "schema": schema}
        ).json_schema
        == schema
    )


def test_ingestion_requires_a_table_and_keeps_its_full_contract() -> None:
    wire = {"task": "Prepare sales data", "outputs": [table()]}
    assert IngestRequest.model_validate(wire).to_wire() == wire
    wire_validator("IngestRequest").validate(wire)
    invalid = {
        "task": "Prepare sales data",
        "outputs": [{"name": "notes", "type": "text", "instructions": "Describe the source"}],
    }
    with pytest.raises(ValidationError, match="table"):
        IngestRequest.model_validate(invalid)
    assert not wire_validator("IngestRequest").is_valid(invalid)
    assert not Draft202012Validator(IngestRequest.model_json_schema()).is_valid(invalid)


def test_fetch_question_and_cursor_are_distinct() -> None:
    assert parse_fetch({"task": "Show the latest five rows"}).to_wire() == {
        "task": "Show the latest five rows"
    }
    assert parse_fetch({"cursor": "opaque_page"}).to_wire() == {"cursor": "opaque_page"}
    for invalid in [
        {"cursor": "page", "task": "change selection"},
        {"task": "Show rows", "page_size": 0},
        {"task": "Show rows", "page_size": True},
    ]:
        with pytest.raises(ValidationError):
            parse_fetch(invalid)


def test_refresh_parameters_use_the_same_native_types() -> None:
    r = RefreshRequest.model_validate({"parameters": {"period": {"start": "2024-01-01"}}})
    assert r.parameters and isinstance(r.parameters.period, DatePeriodConfig)


def test_clarification_guidance_round_trips_through_error_envelope() -> None:
    error = clarification()
    parsed = ErrorResponse.model_validate({"error": error})
    assert parsed.to_wire() == {"error": error}
    wire_validator("ErrorResponse").validate(parsed.to_wire())
    accepted_error = {"error": error, "execution_id": "exec_existing"}
    assert ErrorResponse.model_validate(accepted_error).to_wire() == accepted_error
    raised = EpochError.from_response(ErrorResponse.model_validate(accepted_error))
    assert raised.execution_id == "exec_existing"
    display = str(EpochError(parsed.error))
    assert "Which period? Options: 2024; 2025" in display
    assert parsed.error.recommended_task in display


@pytest.mark.parametrize("field", ["gaps", "questions", "recommended_task"])
def test_clarification_without_guidance_is_invalid(field: str) -> None:
    wire = clarification()
    wire.pop(field)
    with pytest.raises(ValidationError):
        DomainError.model_validate(wire)
    assert not wire_validator("Error").is_valid(wire)
    assert not Draft202012Validator(DomainError.model_json_schema()).is_valid(wire)


def test_clarification_cannot_be_retryable_or_invent_an_option() -> None:
    with pytest.raises(ValidationError):
        DomainError.model_validate({**clarification(), "retryable": True})
    wire = clarification()
    wire["questions"][0]["recommended_option"] = "unoffered"
    with pytest.raises(ValidationError, match="one of options"):
        DomainError.model_validate(wire)


@pytest.mark.parametrize("code", ["DATA_REQUIRED", "ACCESS_REQUIRED"])
def test_data_and_access_errors_need_their_requirements(code: str) -> None:
    with pytest.raises(ValidationError):
        DomainError.model_validate(
            {"code": code, "message": "Missing permission/data", "retryable": False}
        )


def test_acknowledgement_is_exactly_the_persisted_handle_and_status() -> None:
    value = {"execution_id": "exec_123", "status": "queued"}
    assert Acknowledgement.model_validate(value).to_wire() == value
    for invalid in [{**value, "study_id": "internal"}, {**value, "status": "running"}]:
        with pytest.raises(ValidationError):
            Acknowledgement.model_validate(invalid)


@pytest.mark.parametrize(
    "payload",
    [
        '{"task":"one","task":"two","outputs":[]}',
        '{"task":"one","parameters":{"execution":{"cash":NaN}},"outputs":[]}',
    ],
)
def test_wire_parser_rejects_ambiguous_json(payload: str) -> None:
    with pytest.raises(ValueError):
        parse_request(RunRequest, payload)


def test_openapi_has_no_unresolved_internal_references() -> None:
    document = json.loads(CONTRACT.read_text())

    def walk(node: object) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if key == "$ref" and isinstance(value, str) and value.startswith("#/"):
                    target = document
                    for part in value[2:].split("/"):
                        target = target[part.replace("~1", "/").replace("~0", "~")]
                else:
                    walk(value)
        elif isinstance(node, list):
            for child in node:
                walk(child)

    walk(document)
    for schema in document["components"]["schemas"].values():
        Draft202012Validator.check_schema(schema)


def test_documented_wire_examples_agree_with_shared_contract() -> None:
    document = json.loads(CONTRACT.read_text())
    covered = set()
    for methods in document["paths"].values():
        for operation in methods.values():
            if not isinstance(operation, dict) or "operationId" not in operation:
                continue
            cases = [("request", operation.get("requestBody", {}))]
            cases.extend((str(code), response) for code, response in operation["responses"].items())
            for role, container in cases:
                for content in container.get("content", {}).values():
                    schema = content.get("schema")
                    if not schema:
                        continue
                    for example in content.get("examples", {}).values():
                        if "value" not in example:
                            continue
                        value = example["value"]
                        Draft202012Validator(
                            {"allOf": [schema], "components": document["components"]},
                            format_checker=FormatChecker(),
                        ).validate(value)
                        covered.add(operation["operationId"])
                        if role == "request":
                            model = {
                                "run": RunRequest,
                                "ingest": IngestRequest,
                                "refresh": RefreshRequest,
                            }.get(operation["operationId"])
                            if model:
                                model.model_validate(value)
                            elif operation["operationId"] == "fetch":
                                parse_fetch(value)
                        elif schema.get("$ref") == "#/components/schemas/ErrorResponse":
                            ErrorResponse.model_validate(value)
                        elif schema.get("$ref") == "#/components/schemas/Acknowledgement":
                            Acknowledgement.model_validate(value)
    assert covered == {
        operation["operationId"]
        for methods in document["paths"].values()
        for operation in methods.values()
        if isinstance(operation, dict) and "operationId" in operation
    }


def test_language_neutral_validation_fixtures() -> None:
    cases = json.loads((CONTRACT.parent / "validation-cases.json").read_text())["cases"]
    models = {"RunRequest": RunRequest, "IngestRequest": IngestRequest,
              "RefreshRequest": RefreshRequest, "ErrorResponse": ErrorResponse,
              "Acknowledgement": Acknowledgement}
    for case in cases:
        try:
            if case["schema"] == "FetchRequest":
                parse_fetch(case["value"])
            else:
                models[case["schema"]].model_validate(case["value"])
        except ValidationError:
            assert not case["valid"], case["name"]
        else:
            assert case["valid"], case["name"]
