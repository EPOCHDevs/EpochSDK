"""Local case loading and result checks for the US equities desk notebooks.

These helpers start no research. The notebook makes every service call explicitly.
Checks cover shape and internal consistency, not an independent market-data audit.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from epoch_sdk import RunRequest
from epoch_sdk.output_validation import JsonValueOutput, TableValue, validate_outputs
from epoch_sdk.research import EpochClient, ResearchCompleted

CASES = Path(__file__).resolve().parent / "cases"


def case_info(filename: str | Path) -> dict:
    """Find the local catalogue entry; its metadata is not sent to Epoch."""
    name = Path(filename).name
    entries = json.loads((CASES / "index.json").read_text())["cases"]
    for entry in entries:
        if entry["file"] == name:
            return entry
    raise ValueError(
        f"Unknown case {name!r}; see cases/index.json and cases/README.md."
    )


def list_cases() -> None:
    """Print the cases available in the folder beside the notebooks."""
    for entry in json.loads((CASES / "index.json").read_text())["cases"]:
        print(f"{entry['file']}: {entry['title']} ({entry['kind']})")


def load_case(
    filename: str | Path, *, source: ResearchCompleted | None = None
) -> RunRequest:
    """Validate a request; output variants also require the completed source case.

    Exact saved identities go into the agent's context. They are not passed as a
    prepared-execution selector: this is a new answer-producing research turn.
    The notebook attaches that turn to the original thread and checks that the
    primary execution remains the same.
    """
    entry = case_info(filename)
    request = RunRequest.model_validate(json.loads((CASES / entry["file"]).read_text()))
    if entry["kind"] != "output_variant":
        if source is not None:
            raise ValueError("Only an output variant takes a completed source case.")
        return request
    if source is None:
        raise ValueError(
            f"Complete {entry['source_case']} first, then use notebook 03."
        )
    reference = source.response
    if not reference.study_id or not reference.primary_execution_id:
        raise ValueError(
            "The source answer must identify its saved study and execution."
        )
    base = load_case(entry["source_case"] + ".json")
    if [output.to_wire() for output in reference.content.declarations] != [
        output.to_wire() for output in base.outputs
    ]:
        raise ValueError(
            "This answer does not have the declared outputs of the source case."
        )
    wire = request.to_wire()
    wire["context"] = [
        *request.context,
        (
            "Authorized saved evidence for this output-only follow-up: "
            f"study_id={reference.study_id}; execution_id={reference.primary_execution_id}; "
            f"source_response_id={reference.response_id}; source_response_version={reference.version}; "
            f"thread_id={reference.thread_id}. Select this exact existing execution as the "
            "primary source. Read its persisted data; create no discovery or execution job."
        ),
    ]
    return RunRequest.model_validate(wire)


async def read_case_tables(
    epoch: EpochClient, completed: ResearchCompleted, *, page_size: int = 1000
) -> dict[str, list[dict]]:
    """Fetch every page of each table; JSON/text-only answers need no table call."""
    tables = {}
    for output in completed.response.content.outputs:
        if not isinstance(output, TableValue):
            continue
        rows = []
        total = None
        async for page in epoch.iter_response_table(
            completed.response.response_id,
            output.name,
            version=completed.response.version,
            page_size=page_size,
        ):
            if total is not None and page.total_rows != total:
                raise ValueError("The table's row count changed during the saved read.")
            total = page.total_rows
            names = [column.name for column in page.columns]
            rows.extend(dict(zip(names, row, strict=True)) for row in page.rows)
            print(f"{output.name}: offset {page.offset}, next {page.next_offset}")
        if total is None or len(rows) != total:
            raise ValueError(f"Did not read the complete {output.name} table.")
        tables[output.name] = rows
    if not tables:
        print("This answer requests JSON/text only; no table retrieval is needed.")
    return tables


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _equal(actual: float, expected: float, label: str) -> None:
    _require(
        math.isclose(actual, expected, rel_tol=1e-8, abs_tol=1e-10),
        f"{label} differs: {actual!r} versus {expected!r}.",
    )


def _json_output(completed: ResearchCompleted, name: str) -> dict:
    for output in completed.response.content.outputs:
        if isinstance(output, JsonValueOutput) and output.name == name:
            return output.value
    raise ValueError(f"The answer has no JSON output named {name}.")


def check_case_answer(
    filename: str | Path,
    request: RunRequest,
    completed: ResearchCompleted,
    tables: dict[str, list[dict]],
) -> None:
    """Check the declared answer and case-specific arithmetic/ordering invariants.

    Financial values are not hardcoded. Independent source reconciliation and
    inspection of actual strategy fills still belong to the live case review.
    """
    validate_outputs(request.outputs, completed.response.content.outputs)
    _require(
        [output.to_wire() for output in completed.response.content.declarations]
        == [output.to_wire() for output in request.outputs],
        "The saved answer declarations differ from the requested outputs.",
    )
    expected_tables = {
        output.name for output in request.outputs if output.type == "table"
    }
    _require(
        set(tables) == expected_tables, "Read every requested table before checking it."
    )
    key = case_info(filename)["id"]
    if key in {"msft_fundamentals", "msft_fundamentals_confirmation"}:
        rows = tables["msft_fundamentals"]
        _require(
            [row["fiscal_year"] for row in rows] == ["FY2023", "FY2024", "FY2025"],
            "Expected the three distinct fiscal years in ascending order.",
        )
        for index, row in enumerate(rows):
            _require(
                row["revenue"] > 0 and row["capex"] >= 0, "Check revenue/capex sign."
            )
            _equal(
                row["free_cash_flow"], row["operating_cash_flow"] - row["capex"], "FCF"
            )
            _equal(
                row["operating_margin"],
                row["operating_income"] / row["revenue"],
                "Margin",
            )
            _equal(
                row["free_cash_flow_margin"],
                row["free_cash_flow"] / row["revenue"],
                "FCF margin",
            )
            if row["net_income"] == 0:
                _require(
                    row["cash_conversion"] is None,
                    "Zero net income requires null conversion.",
                )
            else:
                _equal(
                    row["cash_conversion"],
                    row["operating_cash_flow"] / row["net_income"],
                    "Conversion",
                )
            if index:
                _equal(
                    row["revenue_growth"],
                    row["revenue"] / rows[index - 1]["revenue"] - 1,
                    "Growth",
                )
    elif key == "msft_risk_json":
        value = _json_output(completed, "risk_summary")
        _require(
            [row["year"] for row in value["annual_returns"]] == list(range(2021, 2026)),
            "Check annual return years/order.",
        )
        _require(
            sorted(row["ticker"] for row in value["assets"]) == ["MSFT", "SPY"],
            "Expected one asset summary each.",
        )
        for row in [*value["annual_returns"], value["msft_worst_drawdown"]]:
            _equal(
                row["active_return"],
                row["msft_return"] - row["spy_return"],
                "Active return",
            )
        drawdown = value["msft_worst_drawdown"]
        _require(
            "2021-01-01"
            <= drawdown["peak_date"]
            <= drawdown["trough_date"]
            <= "2025-12-31",
            "Drawdown dates are out of order/range.",
        )
        if drawdown["recovery_date"] is not None:
            _require(
                drawdown["trough_date"] <= drawdown["recovery_date"] <= "2025-12-31",
                "Check recovery date.",
            )
        msft = next(row for row in value["assets"] if row["ticker"] == "MSFT")
        _equal(drawdown["msft_return"], msft["maximum_drawdown"], "Worst drawdown")
    elif key == "aapl_trend_strategy":
        rows = tables["performance"]
        _require(
            [row["variant"] for row in rows] == ["trend_filter", "buy_and_hold"],
            "Expected the two comparison rows.",
        )
        summary = _json_output(completed, "strategy_summary")
        for row, name in zip(rows, ["strategy", "benchmark"], strict=True):
            _require(
                row["annualized_volatility"] >= 0
                and -1 <= row["maximum_drawdown"] <= 0,
                "Check volatility/drawdown sign.",
            )
            for metric in summary[name]:
                _equal(
                    row[metric], summary[name][metric], f"{name}.{metric} table/JSON"
                )
    elif key == "sp500_momentum_screener":
        rows, coverage = tables["shortlist"], tables["screening_coverage"]
        _require(len(coverage) == 1, "Expected one coverage record.")
        counts = {
            key: int(coverage[0][key])
            for key in [
                "universe_count",
                "excluded_missing_data_count",
                "eligible_count",
                "returned_count",
            ]
        }
        _require(
            counts["universe_count"] > 0
            and 0 <= counts["excluded_missing_data_count"] <= counts["universe_count"],
            "Invalid universe/exclusion counts.",
        )
        _require(
            0
            <= counts["eligible_count"]
            <= counts["universe_count"] - counts["excluded_missing_data_count"],
            "Invalid eligible count.",
        )
        _require(
            len(rows) == counts["returned_count"] == min(20, counts["eligible_count"]),
            "Shortlist is truncated or padded.",
        )
        _require(
            [int(row["rank"]) for row in rows] == list(range(1, len(rows) + 1)),
            "Ranks must be contiguous.",
        )
        _require(len({row["ticker"] for row in rows}) == len(rows), "Duplicate ticker.")
        _require(
            rows
            == sorted(rows, key=lambda row: (-row["momentum_12_1"], row["ticker"])),
            "Ranking/tie-break order differs.",
        )
        _require(coverage[0]["as_of"] == "2026-10-16", "Wrong screening price cutoff.")
        for row in rows:
            _require(
                row["as_of"] == "2026-10-16"
                and row["distance_to_sma_200"] > 0
                and row["average_dollar_volume_20"] >= 0,
                "A shortlist row fails the screen or has invalid units.",
            )
    elif key == "qqq_treasury_regimes":
        rows = tables["rate_regimes"]
        _require(
            [row["regime"] for row in rows]
            == ["yields_up_25bp", "yields_down_25bp", "other"],
            "Expected the three labelled regimes.",
        )
        _require(
            0 < sum(int(row["month_count"]) for row in rows) <= 120,
            "Invalid number of paired evaluation months.",
        )
        for row in rows:
            count = int(row["month_count"])
            values = [
                value
                for name, value in row.items()
                if name not in {"regime", "month_count"}
            ]
            _require(
                count >= 0 and all((value is None) == (count == 0) for value in values),
                "Null metrics are valid only for an empty regime.",
            )
            if count:
                _equal(
                    row["active_mean_return"],
                    row["qqq_mean_return"] - row["spy_mean_return"],
                    "Mean paired active return",
                )
                for asset in ["qqq", "spy", "active"]:
                    _require(
                        row[f"{asset}_worst_return"] <= row[f"{asset}_mean_return"]
                        and row[f"{asset}_worst_return"]
                        <= row[f"{asset}_median_return"],
                        "Worst return exceeds the mean or median.",
                    )
    print(
        "Passed requested-output and internal-consistency checks; market-source accuracy still needs live review."
    )


def check_variant_source(
    filename: str | Path,
    source: ResearchCompleted,
    completed: ResearchCompleted,
    source_tables: dict[str, list[dict]],
) -> None:
    """Require the original execution; compare every screener JSON cell to it."""
    original, answer = source.response, completed.response
    _require(
        answer.primary_execution_id == original.primary_execution_id
        and answer.study_id == original.study_id,
        "The output variant must reuse the exact original execution/study.",
    )
    _require(
        answer.response_id != original.response_id,
        "A new query needs its own answer identity.",
    )
    if case_info(filename)["id"] == "sp500_momentum_json":
        value = _json_output(completed, "screener_json")
        expected = {}
        for output in original.content.outputs:
            if isinstance(output, TableValue):
                expected[output.name] = [
                    {
                        column.name: int(row[column.name])
                        if column.type == "int64"
                        else row[column.name]
                        for column in output.columns
                    }
                    for row in source_tables[output.name]
                ]
        _require(
            value["coverage"] == expected["screening_coverage"][0],
            "JSON coverage differs from the original saved row.",
        )
        _require(
            value["shortlist"] == expected["shortlist"],
            "JSON values/order differ from the original saved table.",
        )
    print("Verified the same execution/study and a distinct saved answer.")
