from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from epoch_sdk import EpochError
from epoch_sdk.responses import ResponseTablePage, SavedResearchResponse

ROOT = Path(__file__).resolve().parents[3]


def example() -> dict:
    return json.loads((ROOT / "contracts/research-response.example.json").read_text())


def test_one_saved_response_contains_all_requested_parts_and_annotations() -> None:
    response = SavedResearchResponse.model_validate(example())
    assert response.to_wire() == example()
    assert [item.name for item in response.content.outputs] == ["screen", "summary", "explanation"]


def test_computed_qualifications_survive_saved_reads_outside_accepted_output_parts():
    value = example()
    declarations = copy.deepcopy(value["content"]["declarations"])
    outputs = copy.deepcopy(value["content"]["outputs"])
    value["response_plan"] = {"plan_id": "rpl_" + "a" * 64, "version": 1}
    value["content"]["qualifications"] = [{"name": "statement_coverage",
        "description": "Annual statement coverage of the selected cohort",
        "value": {"observed": 7, "expected": 8, "missing": ["unobserved_source"], "basis": None}}]
    saved = SavedResearchResponse.model_validate(value)
    assert saved.to_wire() == value
    assert saved.to_wire()["content"]["declarations"] == declarations
    assert saved.to_wire()["content"]["outputs"] == outputs


@pytest.mark.parametrize("change", ["duplicate", "too_many", "oversize", "nonfinite"])
def test_qualification_payload_bounds_and_finite_values_are_checked(change):
    value = example()
    value["response_plan"] = {"plan_id": "rpl_" + "a" * 64, "version": 1}
    qualification = {"name": "coverage", "description": "Observed coverage", "value": {"observed": 1}}
    value["content"]["qualifications"] = [qualification]
    SavedResearchResponse.model_validate(value)
    if change == "duplicate": value["content"]["qualifications"].append(copy.deepcopy(qualification))
    elif change == "too_many": value["content"]["qualifications"] = [{**qualification, "name": "q" + str(i)} for i in range(17)]
    elif change == "oversize": qualification["value"] = {"message": "x" * 65536}
    else: qualification["value"] = {"nested": [float("inf")]}
    expected = {"duplicate": "names must be unique", "too_many": "at most 16",
                "oversize": "exceed 64 KiB", "nonfinite": "finite"}[change]
    with pytest.raises(ValidationError, match=expected): SavedResearchResponse.model_validate(value)


def test_qualifications_cannot_claim_computed_provenance_without_a_plan():
    value = example()
    value["content"]["qualifications"] = [{"name": "coverage", "description": "Observed coverage", "value": {"observed": 7}}]
    with pytest.raises(ValidationError, match="source-backed response plan"):
        SavedResearchResponse.model_validate(value)


@pytest.mark.parametrize("change", ["json-type", "table-value", "column-meaning", "missing-part"])
def test_publication_content_validates_values_not_only_response_metadata(change: str) -> None:
    value = example()
    content = value["content"]
    if change == "json-type":
        content["outputs"][1]["value"]["matches"] = "one"
    if change == "table-value":
        content["outputs"][0]["rows"][0][1] = "18.2"
    if change == "column-meaning":
        content["outputs"][0]["schema"][0]["description"] = "Different column meaning"
    if change == "missing-part":
        content["outputs"].pop()
    with pytest.raises(EpochError) as error:
        SavedResearchResponse.model_validate(value)
    assert error.value.error.code == "OUTPUT_VALIDATION_FAILED"


def test_null_is_data_in_a_nullable_json_response() -> None:
    value = example()
    declaration = value["content"]["declarations"][1]
    declaration["schema"] = {"type": ["object", "null"]}
    value["content"]["outputs"][1]["value"] = None
    response = SavedResearchResponse.model_validate(value)
    assert response.to_wire()["content"]["outputs"][1]["value"] is None


def test_reference_answers_keep_large_row_counts_and_reject_mismatched_execution() -> None:
    value = json.loads((ROOT / "contracts/research-response-reference.example.json").read_text())
    saved = SavedResearchResponse.model_validate(value)
    assert saved.to_wire() == value
    assert value["content"]["outputs"][0]["source"]["row_count"] == 25003
    assert "rows" not in saved.to_wire()["content"]["outputs"][0]
    value["content"]["outputs"][0]["source"]["execution_id"] = "another-execution"
    with pytest.raises(ValueError):
        SavedResearchResponse.model_validate(value)


def test_a_table_cannot_mix_inline_rows_and_a_reference() -> None:
    value = json.loads((ROOT / "contracts/research-response-reference.example.json").read_text())
    value["content"]["outputs"][0]["rows"] = []
    with pytest.raises(ValueError):
        SavedResearchResponse.model_validate(value)


def test_a_terminal_page_requires_an_explicit_null_continuation() -> None:
    value = {
        "response_id": "answer",
        "version": 1,
        "name": "results",
        "type": "table",
        "schema": [{"name": "label", "type": "string"}],
        "rows": [],
        "offset": 0,
        "total_rows": 0,
        "next_offset": None,
    }
    page = ResponseTablePage.model_validate(value)
    assert page.to_wire()["next_offset"] is None
    schema = ResponseTablePage.model_json_schema()
    assert "next_offset" in schema["required"]
    assert {"type": "null"} in schema["properties"]["next_offset"]["anyOf"]
    del value["next_offset"]
    with pytest.raises(ValueError):
        ResponseTablePage.model_validate(value)


def test_an_answer_revision_does_not_change_the_native_execution_reference() -> None:
    first = SavedResearchResponse.model_validate(example())
    value = copy.deepcopy(example())
    value["version"] = 2
    value["content"]["outputs"][2]["value"] = "Revised interpretation."
    second = SavedResearchResponse.model_validate(value)
    assert first.primary_execution_id == second.primary_execution_id
    assert first.content.outputs[2] != second.content.outputs[2]
