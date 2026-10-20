"""Offline helper checks; all values here are fixtures, not financial observations."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest
from stratifyx import SdkContractRunRequest

from epoch_sdk import RunRequest
from epoch_sdk.research import ResearchCompleted

NOTEBOOKS = Path(__file__).resolve().parents[3] / "examples/notebooks"
sys.path.insert(0, str(NOTEBOOKS))

from case_support import (
    case_info,
    check_case_answer,
    check_variant_source,
    load_case,
)

ENTRIES = json.loads((NOTEBOOKS / "cases/index.json").read_text())["cases"]


def request_for(key):
    return RunRequest.model_validate(
        json.loads((NOTEBOOKS / "cases" / (key + ".json")).read_text())
    )


def completed_for(key, tables, *, json_values=None, response_id="fixture-source"):
    """Build only an in-memory typed answer; no clients or services are called."""
    request = request_for(key)
    outputs = []
    for declaration in request.to_wire()["outputs"]:
        name, kind = declaration["name"], declaration["type"]
        if kind == "table":
            outputs.append(
                {
                    "name": name,
                    "type": kind,
                    "schema": declaration["schema"],
                    "rows": [
                        [row[column["name"]] for column in declaration["schema"]]
                        for row in tables[name]
                    ],
                }
            )
        elif kind == "json":
            outputs.append({"name": name, "type": kind, "value": json_values[name]})
        else:
            outputs.append(
                {
                    "name": name,
                    "type": kind,
                    "format": declaration["format"],
                    "value": "Unit-test fixture text; no market result is claimed.",
                }
            )
    return ResearchCompleted.model_validate(
        {
            "request_id": "fixture-request",
            "response": {
                "response_id": response_id,
                "request_id": "fixture-request",
                "thread_id": "fixture-thread",
                "primary_execution_id": "fixture-execution",
                "study_id": "fixture-study",
                "version": 1,
                "published_at_ms": 1,
                "content": {"declarations": request.to_wire()["outputs"], "outputs": outputs},
            },
        }
    )


def fundamentals():
    rows = []
    for year, revenue in [(2023, 100.0), (2024, 120.0), (2025, 144.0)]:
        rows.append(
            {
                "fiscal_year": f"FY{year}",
                "period_end": f"{year}-06-30",
                "revenue": revenue,
                "revenue_growth": 0.2,
                "operating_income": revenue * 0.3,
                "operating_margin": 0.3,
                "net_income": 20.0,
                "operating_cash_flow": 30.0,
                "capex": 10.0,
                "free_cash_flow": 20.0,
                "free_cash_flow_margin": 20.0 / revenue,
                "cash_conversion": 1.5,
            }
        )
    return {"msft_fundamentals": rows}


def screener():
    rows = [
        {
            "rank": str(rank),
            "ticker": ticker,
            "company": "Fixture " + ticker,
            "sector": "Fixture sector",
            "as_of": "2026-10-16",
            "momentum_12_1": score,
            "return_3m": 0.05,
            "distance_to_sma_200": 0.1,
            "average_dollar_volume_20": 1.0,
        }
        for rank, ticker, score in [(1, "AAA", 0.3), (2, "BBB", 0.3)]
    ]
    return {
        "shortlist": rows,
        "screening_coverage": [
            {
                "as_of": "2026-10-16",
                "membership_snapshot_at": "2026-10-19T15:00:00Z",
                "universe_count": "5",
                "excluded_missing_data_count": "1",
                "eligible_count": "2",
                "returned_count": "2",
            }
        ],
    }


@pytest.mark.parametrize("entry", ENTRIES, ids=lambda entry: entry["id"])
def test_cases_match_sdk_and_native_models(entry):
    request = request_for(entry["id"])
    SdkContractRunRequest.model_validate(request.to_wire())
    assert all(
        column.description
        for output in request.outputs
        if output.type == "table"
        for column in output.columns
    )


def test_output_variant_requires_the_completed_source_and_exact_identity():
    with pytest.raises(ValueError, match="Complete msft_fundamentals first"):
        load_case("msft_fundamentals_plain.json")
    source = completed_for("msft_fundamentals", fundamentals())
    request = load_case("msft_fundamentals_plain.json", source=source)
    assert "execution_id=fixture-execution" in request.context[-1]
    assert "source_response_id=fixture-source" in request.context[-1]
    assert "source_execution_id" not in request.to_wire()
    source.response.content.declarations[0].description = "Different source contract"
    with pytest.raises(ValueError, match="declared outputs of the source case"):
        load_case("msft_fundamentals_plain.json", source=source)


def test_fundamentals_checks_calculation_and_fiscal_order():
    key = "msft_fundamentals"
    tables = fundamentals()
    result = completed_for(key, tables)
    check_case_answer(key + ".json", request_for(key), result, tables)
    wrong = copy.deepcopy(tables)
    wrong[key][0]["free_cash_flow"] = 40.0  # Wrong capex sign.
    with pytest.raises(ValueError, match="FCF differs"):
        check_case_answer(key + ".json", request_for(key), result, wrong)
    with pytest.raises(ValueError, match="fiscal years"):
        check_case_answer(
            key + ".json", request_for(key), result, {key: list(reversed(tables[key]))}
        )


def test_screener_checks_tie_order_and_never_silently_truncates():
    key = "sp500_momentum_screener"
    tables = screener()
    result = completed_for(key, tables)
    check_case_answer(key + ".json", request_for(key), result, tables)
    wrong = copy.deepcopy(tables)
    wrong["shortlist"][0]["ticker"], wrong["shortlist"][1]["ticker"] = "BBB", "AAA"
    with pytest.raises(ValueError, match="tie-break"):
        check_case_answer(key + ".json", request_for(key), result, wrong)
    wrong = copy.deepcopy(tables)
    wrong["shortlist"].pop()
    with pytest.raises(ValueError, match="truncated or padded"):
        check_case_answer(key + ".json", request_for(key), result, wrong)


def test_json_screener_preserves_all_values_order_and_native_integer_conversion():
    tables = screener()
    source = completed_for("sp500_momentum_screener", tables)
    value = {
        "coverage": {
            key: int(value) if key.endswith("count") else value
            for key, value in tables["screening_coverage"][0].items()
        },
        "shortlist": [{**row, "rank": int(row["rank"])} for row in tables["shortlist"]],
    }
    answer = completed_for(
        "sp500_momentum_json",
        {},
        json_values={"screener_json": value},
        response_id="fixture-follow-up",
    )
    check_variant_source("sp500_momentum_json.json", source, answer, tables)
    answer.response.content.outputs[0].value["shortlist"][1]["return_3m"] = 0.9
    with pytest.raises(ValueError, match="values/order"):
        check_variant_source("sp500_momentum_json.json", source, answer, tables)


def test_variant_rejects_a_different_primary_execution():
    source = completed_for("msft_fundamentals", fundamentals())
    answer = completed_for("msft_fundamentals_plain", {}, response_id="fixture-follow-up")
    answer.response.primary_execution_id = "different-execution"
    with pytest.raises(ValueError, match="exact original execution"):
        check_variant_source("msft_fundamentals_plain.json", source, answer, fundamentals())


def test_catalogue_looks_up_the_file_next_to_the_notebooks():
    assert case_info(Path("cases/aapl_trend_strategy.json"))["family"] == "single_asset_strategy"
