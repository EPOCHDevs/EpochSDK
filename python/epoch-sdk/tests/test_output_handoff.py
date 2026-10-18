from __future__ import annotations

import copy

import pytest
from stratifyx.types.dashboard_schema import DashboardSchema
from test_saved_outputs import dashboard, manifest

from epoch_sdk import EpochError
from epoch_sdk.output_handoff import output_manifest


def named_schema() -> dict:
    value = dashboard()
    value["tables"][0]["id"] = "sales"
    value["tables"][0]["columns"][0]["name"] = "year"
    value["tables"][0]["columns"][1]["name"] = "sales"
    value["content"]["markdown"][0]["id"] = "totals"
    value["content"]["markdown"][1]["id"] = "report"
    return value


def test_stable_native_ids_create_the_explicit_mapping_without_title_inference() -> None:
    result = output_manifest(
        DashboardSchema.model_validate(named_schema()),
        execution_id="run-one",
        study_id="study-one",
        declarations=manifest().declarations,
    )
    assert result.to_wire()["bindings"] == [
        {
            "name": "sales",
            "type": "table",
            "category": "ALL",
            "table_index": 3,
            "field_ids": ["native-year", "native-value"],
        },
        {"name": "totals", "type": "json", "category": "ALL", "markdown_id": "totals"},
        {
            "name": "report",
            "type": "text",
            "category": "ALL",
            "markdown_id": "report",
            "format": "markdown",
        },
    ]


@pytest.mark.parametrize(
    "change", ["missing-id", "duplicate-id", "column-label", "missing-text", "category"]
)
def test_missing_or_ambiguous_output_identity_is_a_defined_failure(change: str) -> None:
    value = named_schema()
    if change == "missing-id":
        value["tables"][0]["id"] = "different"
        value["tables"][0]["title"] = "sales"
    if change == "duplicate-id":
        value["tables"].append(copy.deepcopy(value["tables"][0]))
    if change == "column-label":
        value["tables"][0]["columns"][0]["name"] = "Different meaning"
    if change == "missing-text":
        value["content"]["markdown"] = []
    if change == "category":
        value["tables"][0]["category"] = "OTHER"
    with pytest.raises(EpochError) as error:
        output_manifest(
            DashboardSchema.model_validate(value),
            execution_id="run-one",
            study_id="study-one",
            declarations=manifest().declarations,
        )
    assert error.value.error.code == "OUTPUT_VALIDATION_FAILED"
    assert error.value.execution_id == "run-one"
