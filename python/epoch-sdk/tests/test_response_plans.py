"""Replay-definition contracts; these do not claim native replay is implemented."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from epoch_sdk import RunRequest
from epoch_sdk.response_plans import ResponsePlanDefinition, SavedResponsePlan

ROOT = Path(__file__).resolve().parents[3]


def aapl_plan() -> dict:
    request = RunRequest.model_validate_json(
        (ROOT / "examples/notebooks/cases/aapl_trend_strategy.json").read_text()
    )
    declarations = request.outputs
    assert declarations[0].type == "table"
    assert declarations[2].type == "text"
    metrics = [column.name for column in declarations[0].columns[1:]]
    fields = {name: {"field_id": name} for name in metrics}
    constants = ["asset", "sma_sessions", "trade_timing", "cash_interest_rate", "benchmark_basis"]
    return {
        "format_version": 1,
        "study_id": "study-aapl",
        "captured_parameters": request.parameters.to_wire(),
        "declarations": [item.to_wire() for item in declarations],
        "queries": [
            {"kind": "recorded_sql", "name": name, "query_ref": "rqr_" + digit * 64}
            for name, digit in [("strategy", "1"), ("benchmark", "2")]
        ],
        "outputs": [
            {"name": "performance", "type": "table", "projections": [
                {"query": query, "field_ids": ["variant", *metrics]}
                for query in ["strategy", "benchmark"]
            ]},
            {"name": "strategy_summary", "type": "json", "value": {
                "kind": "object", "fields": {
                    **{name: {"kind": "schema_constant"} for name in constants},
                    "transaction_cost_bps": {"kind": "parameter", "pointer": "/execution/commission/model/args/bps"},
                    "strategy": {"kind": "row", "query": "strategy", "fields": fields},
                    "benchmark": {"kind": "row", "query": "benchmark", "fields": fields},
                },
            }},
            {"name": "trader_conclusion", "type": "text",
             "model_policy": "response_interpretation.v1",
             "instructions": declarations[2].instructions,
             "inputs": {
                 "strategy": {"kind": "row", "query": "strategy", "fields": fields},
                 "benchmark": {"kind": "row", "query": "benchmark", "fields": fields},
                 "execution_parameters": {"kind": "parameter", "pointer": "/execution"},
             }},
        ],
    }


def test_fixed_strategy_plan_preserves_the_real_request_and_round_trips():
    value = aapl_plan()
    plan = ResponsePlanDefinition.model_validate(value)
    assert ResponsePlanDefinition.model_validate_json(json.dumps(plan.to_wire())) == plan
    assert plan.allow_period_override is False
    assert plan.declarations[0].type == "table"
    assert plan.declarations[0].columns[1].unit == "fraction"
    assert "session/auction basis" in plan.outputs[2].instructions
    assert [(item.name, item.type) for item in plan.outputs] == [
        ("performance", "table"), ("strategy_summary", "json"), ("trader_conclusion", "text")
    ]


def test_plan_contract_reuses_canonical_native_extension_provenance():
    from tools.sync_response_plan_contract import schemas

    schema = schemas()["response-plan.schema.json"]
    assert "ExecutionExtensionProvenance" not in schema["$defs"]
    assert "openapi.json#/components/schemas/Native_ExecutionExtensionProvenance" in json.dumps(schema)


def test_computed_only_plan_contains_no_model_or_prompt_step():
    value = aapl_plan()
    value["outputs"].pop()
    value["declarations"].pop()
    plan = ResponsePlanDefinition.model_validate(value)
    assert all(output.type in {"table", "json"} for output in plan.outputs)
    wire = json.dumps(plan.to_wire())
    assert "model_policy" not in wire and "instructions" not in wire


@pytest.mark.parametrize("change", ["missing_query", "duplicate_query", "renamed_output", "reordered_outputs", "missing_column"])
def test_replay_mapping_must_preserve_exact_queries_and_output_contract(change):
    value = aapl_plan()
    if change == "missing_query": value["outputs"][0]["projections"][0]["query"] = "unrecorded"
    elif change == "duplicate_query": value["queries"].append(copy.deepcopy(value["queries"][0]))
    elif change == "renamed_output": value["outputs"][0]["name"] = "another_answer"
    elif change == "reordered_outputs": value["outputs"].reverse()
    else: value["outputs"][0]["projections"][0]["field_ids"].pop()
    with pytest.raises(ValidationError): ResponsePlanDefinition.model_validate(value)


@pytest.mark.parametrize("branch", ["query_sql", "table_rows", "literal_fact", "supervisor_fallback", "bad_pointer"])
def test_plan_draft_does_not_accept_unrecorded_sql_transcribed_cells_or_hidden_fallbacks(branch):
    value = aapl_plan()
    if branch == "query_sql": value["queries"][0]["sql"] = "SELECT 0.5 AS total_return"
    elif branch == "table_rows": value["outputs"][0]["rows"] = [["trend_filter", 0.5, 0.1, 0.2, -0.1]]
    elif branch == "literal_fact": value["outputs"][1]["value"]["fields"]["asset"]["value"] = "invented"
    elif branch == "supervisor_fallback": value["fallback_to_supervisor"] = True
    else: value["outputs"][2]["inputs"]["execution_parameters"]["pointer"] = "execution~2bad"
    with pytest.raises(ValidationError): ResponsePlanDefinition.model_validate(value)


def test_schema_constants_are_not_arbitrary_text_inputs():
    value = aapl_plan()
    value["outputs"][2]["inputs"]["invented_fact"] = {"kind": "schema_constant"}
    with pytest.raises(ValidationError, match="no output JSON Schema constant"):
        ResponsePlanDefinition.model_validate(value)


def test_qualification_facts_reuse_bindings_without_changing_outputs():
    value = aapl_plan()
    value["qualifications"] = [{"name": "coverage", "description": "Observed source coverage",
        "value": {"kind": "object", "fields": {
            "observed": {"kind": "column_array", "query": "strategy", "field": {"field_id": "count"}},
            "period_end": {"kind": "parameter", "pointer": "/period/end"},
        }}}]
    plan = ResponsePlanDefinition.model_validate(value)
    assert plan.to_wire()["outputs"] == value["outputs"]
    assert plan.to_wire()["declarations"] == value["declarations"]
    assert len(plan.qualifications) == 1
    assert "model_policy" not in json.dumps(plan.qualifications[0].to_wire())


@pytest.mark.parametrize("change", ["missing_query", "schema_constant", "duplicate", "too_many"])
def test_qualification_bindings_are_required_and_cannot_invent_schema_constants(change):
    value = aapl_plan()
    qualification = {"name": "coverage", "description": "Observed coverage", "value": {
        "kind": "object", "fields": {"observed": {
            "kind": "cell", "query": "strategy", "field": {"field_id": "count"},
        }}}}
    value["qualifications"] = [qualification]
    if change == "missing_query": qualification["value"]["fields"]["observed"]["query"] = "unrecorded"
    elif change == "schema_constant": qualification["value"]["fields"]["observed"] = {"kind": "schema_constant"}
    elif change == "duplicate": value["qualifications"].append(copy.deepcopy(qualification))
    else: value["qualifications"] = [{**qualification, "name": "q" + str(i)} for i in range(17)]
    with pytest.raises(ValidationError): ResponsePlanDefinition.model_validate(value)


def published_plan() -> dict:
    return {
        "plan_id": "rpl_" + "3" * 64, "version": 1, "request_id": "original-query",
        "thread_id": "research-thread", "source_execution_id": "original-execution",
        "created_at_ms": 1, "phase": "outputs_recorded", "definition": aapl_plan(),
        "text_settings": {"trader_conclusion": {"model_policy": "response_interpretation.v1",
            "model_id": "fixture-model-v1", "prompt_version": "grounded-response.v1",
            "max_output_tokens": 2000, "reasoning_effort": "medium"}},
        "verified_response": {"response_id": "original-answer", "request_id": "original-query",
            "response_plan": {"plan_id": "rpl_" + "3" * 64, "version": 1},
            "thread_id": "research-thread", "version": 1,
            "primary_execution_id": "original-execution", "study_id": "study-aapl"},
    }


def test_published_plan_keeps_the_original_verified_answer_pin():
    plan = SavedResponsePlan.model_validate(published_plan())
    assert SavedResponsePlan.model_validate_json(json.dumps(plan.to_wire())) == plan
    assert plan.verified_response.primary_execution_id == "original-execution"


@pytest.mark.parametrize("field", ["request_id", "thread_id", "primary_execution_id", "study_id"])
def test_published_plan_rejects_an_unrelated_verification_answer(field):
    value = published_plan()
    value["verified_response"][field] = "another-source"
    with pytest.raises(ValidationError, match="exact original answer/source"):
        SavedResponsePlan.model_validate(value)


def test_failed_plan_does_not_claim_a_verified_answer():
    value = published_plan()
    value.update(phase="failed", error={"code": "OUTPUT_VALIDATION_FAILED", "message": "A required computed field is missing.", "retryable": False})
    with pytest.raises(ValidationError, match="Only a fully published plan"):
        SavedResponsePlan.model_validate(value)
    del value["verified_response"]
    failed = SavedResponsePlan.model_validate(value)
    assert failed.error.message == "A required computed field is missing."


@pytest.mark.parametrize("change", ["missing", "wrong_policy", "credential"])
def test_published_text_steps_retain_exact_non_secret_model_settings(change):
    value = published_plan()
    if change == "missing": value["text_settings"] = {}
    elif change == "wrong_policy": value["text_settings"]["trader_conclusion"]["model_policy"] = "another-policy"
    else: value["text_settings"]["trader_conclusion"]["api_key"] = "must-not-be-a-plan-field"
    with pytest.raises(ValidationError): SavedResponsePlan.model_validate(value)
