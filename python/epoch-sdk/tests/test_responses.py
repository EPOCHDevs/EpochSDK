from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from epoch_sdk import EpochError
from epoch_sdk.responses import SavedResearchResponse

ROOT = Path(__file__).resolve().parents[3]


def example() -> dict:
    return json.loads((ROOT / "contracts/research-response.example.json").read_text())


def test_one_saved_response_contains_all_requested_parts_and_annotations() -> None:
    response = SavedResearchResponse.model_validate(example())
    assert response.to_wire() == example()
    assert [item.name for item in response.content.outputs] == ["screen", "summary", "explanation"]


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


def test_an_answer_revision_does_not_change_the_native_execution_reference() -> None:
    first = SavedResearchResponse.model_validate(example())
    value = copy.deepcopy(example())
    value["version"] = 2
    value["content"]["outputs"][2]["value"] = "Revised interpretation."
    second = SavedResearchResponse.model_validate(value)
    assert first.primary_execution_id == second.primary_execution_id
    assert first.content.outputs[2] != second.content.outputs[2]
