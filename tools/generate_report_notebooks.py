"""Build portable saved-result walkthroughs; --check makes no service calls."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from generate_demo_notebooks import cell

ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / "examples/notebooks/saved-reports"


def notebook(cells: list[dict]) -> str:
    return (
        json.dumps(
            {
                "cells": cells,
                "metadata": {
                    "kernelspec": {
                        "display_name": "Python 3 (Epoch SDK)",
                        "language": "python",
                        "name": "python3",
                    },
                    "language_info": {"name": "python"},
                },
                "nbformat": 4,
                "nbformat_minor": 5,
            },
            indent=1,
            ensure_ascii=False,
        )
        + "\n"
    )


def research_case(name: str, title: str, checks: str) -> str:
    imports = "connect, task, display_request, run, read"
    if name == "aapl_order_activity":
        imports += ", native_operation, dashboard"
    cells = [
        cell(
            "markdown",
            f"# {title}\n\nUse an existing completed result. This question does not ask for a saved or reusable report: Epoch chooses the supported native path. No financial values are prefilled. Share this folder with its helpers and cases. See [README](README.md) for login, service URLs and source IDs.",
        ),
        cell(
            "markdown",
            "## 1. Connect\n\nThis prepares the ordinary SDK client. It does not start work. Use `epoch-sdk[notebook]` 0.1.0a25 or later and native SDK 3.3.0rc19 or later.",
        ),
        cell(
            "code",
            f"from report_helpers import {imports}\nfrom epoch_sdk.research import ResearchCompleted\n\nepoch = connect()",
        ),
        cell(
            "markdown",
            "## 2. Review the question and outputs\n\nThe source ID comes from your prepared environment. Keep the attempt to reconnect; change it for intentionally changed inputs. The case JSON beside the notebook contains the exact task, context and output contract.",
        ),
        cell(
            "code",
            f'review = task("{name}", attempt="demo-01")\ndisplay_request(review)',
        ),
        cell(
            "markdown",
            "## 3. Run\n\nThe SDK shows real activity and any questions here. Nothing selects a recommended reply automatically. Stopping this cell ends the local wait; keep its operation ID to reconnect.",
        ),
        cell(
            "code",
            "result = await run(epoch, review)\nassert isinstance(result, ResearchCompleted), 'Answer or resume the pending question first.'",
        ),
        cell(
            "markdown",
            "## 4. Read the complete answer\n\nThe session already displayed it. This cell reads every table page for Python use and checks the selected source and requested formats without printing a second report.",
        ),
        cell(
            "code",
            "answer = await read(epoch, result)\nassert answer.reference.extension is not None\nassert answer.reference.extension.source_execution_id == review.source_execution_id\nassert result.response.content.declarations == review.request.outputs\n"
            + checks
            + "\nanswer",
        ),
        cell(
            "markdown",
            f"## {6 if name == 'aapl_order_activity' else 5}. Reconnect\n\nA fresh client reads the same operation and saved answer. This does not submit a new research request.",
        ),
        cell(
            "code",
            "await epoch.aclose()\nepoch = connect()\nreconnected = await epoch.research_status(operation_id=review.operation_id)\nassert isinstance(reconnected, ResearchCompleted)\nassert reconnected.response == result.response\nawait epoch.aclose()",
        ),
    ]
    if name == "aapl_order_activity":
        cells[9:9] = [
            cell(
                "markdown",
                "## 5. Open the requested dashboard\n\nOnly the side-mix chart belongs on this dashboard. The table and note stay in the answer. The prepared environment supplies EPOCH_PORTAL_URL; this link selects the exact saved operation.",
            ),
            cell(
                "code",
                "report = await native_operation(epoch, result)\ndashboard_url = dashboard(report)",
            ),
        ]
    return notebook(cells)


def files() -> dict[str, str]:
    return {
        "01_msft_annual_figures.ipynb": research_case(
            "msft_annual_figures",
            "Microsoft: annual figures from existing results",
            'assert answer.json["annual_json"] == {"rows": answer.tables["annual_table"]}\n'
            'years = [row["fiscal_year"] for row in answer.tables["annual_table"]]\n'
            "assert years == sorted(years) and len(set(years)) == len(years)",
        ),
        "02_aapl_order_activity.ipynb": research_case(
            "aapl_order_activity",
            "AAPL: recorded order activity",
            'rows = answer.tables["orders_by_side"]\n'
            'assert len({row["side"] for row in rows}) == len(rows)\n'
            'assert all(int(row["orders"]) >= 0 for row in rows)\n'
            'assert len(answer.text["desk_note"].split()) <= 110',
        ),
        "03_reexecute_and_reuse_text.ipynb": notebook(
            [
                cell(
                    "markdown",
                    "# Rerun the prepared report and inspect text reuse\n\nFirst complete [02](02_aapl_order_activity.ipynb). This notebook reads its immutable report definition and runs that definition again against the same source. It uses no supervisor or study author. Matching facts, instructions and model settings should reuse persisted text; provider traces, rather than matching text alone, establish zero new inference.",
                ),
                cell(
                    "code",
                    "from report_helpers import connect, task, native_operation, execute, read, dashboard\nfrom epoch_sdk.research import ResearchCompleted\n\nepoch = connect()\nreview = task('aapl_order_activity', attempt='demo-01')",
                ),
                cell(
                    "markdown",
                    "## 1. Read the prepared report\n\nThis reads the completed operation from notebook 02. It never starts that notebook automatically.",
                ),
                cell(
                    "code",
                    "source = await epoch.research_status(operation_id=review.operation_id)\nassert isinstance(source, ResearchCompleted), 'Complete notebook 02 first.'\noriginal = await native_operation(epoch, source)\nprint('Original report execution:', original.execution_id)",
                ),
                cell(
                    "markdown",
                    "## 2. Execute\n\nA different operation ID creates a new report execution with the same definition, source, tables and parameters. Reusing this ID reconnects to that execution. This is a direct Backend operation; it does not run the original backtest.",
                ),
                cell(
                    "code",
                    "rerun = await execute(epoch, original, operation_id=review.operation_id + '-cache-01')\nassert rerun.execution_id != original.execution_id\nanswer = await read(epoch, rerun, show=True)\ndashboard_url = dashboard(rerun)",
                ),
                cell(
                    "markdown",
                    "## 3. Compare the saved outputs\n\nRead all table rows and compare the exact retained text and provenance. The renderer is the same one used by the ordinary SDK session. A policy/facts change is a different cache input and must not be reported as a hit.",
                ),
                cell(
                    "code",
                    "base = await read(epoch, source)\nassert answer.tables == base.tables and answer.text == base.text\nassert source.response.extension is not None and answer.reference.extension is not None\nassert answer.reference.extension.source_execution_id == source.response.extension.source_execution_id\nassert answer.reference.extension.commentary == source.response.extension.commentary\nassert answer.reference.response_id != base.reference.response_id\nreconnected = await epoch.research_status(operation_id=review.operation_id)\nassert isinstance(reconnected, ResearchCompleted) and reconnected.response == source.response\nanswer",
                ),
                cell(
                    "markdown",
                    "## 4. Close this client\n\nKeep both operation IDs for later reads. The server retains the source, report and answers.",
                ),
                cell("code", "await epoch.aclose()"),
            ]
        ),
        "04_unavailable_input.ipynb": notebook(
            [
                cell(
                    "markdown",
                    "# An unavailable input stays visible\n\nThis uses an existing owned AAPL execution and deliberately requests an unavailable table from its metadata endpoint. Nothing is authored, executed or substituted. For interactive question/reconnect controls, see the existing [clarification walkthrough](../demos/08_clarification_and_reconnect.ipynb).",
                ),
                cell(
                    "code",
                    "from report_helpers import connect, task\nfrom stratifyx.core.api_error import ApiError\n\nepoch = connect()\nreview = task('aapl_order_activity', attempt='demo-01')",
                ),
                cell(
                    "markdown",
                    "## 1. Inspect supported inputs\n\nAn empty selection only discovers the actual table names. It does not bind every table or execute work.",
                ),
                cell(
                    "code",
                    "catalogue = await epoch.extension_inputs(review.source_execution_id, tables=[])\nprint('Available tables:', [table.table for table in catalogue.tables])",
                ),
                cell(
                    "markdown",
                    "## 2. Observe an explicit refusal\n\nThe following name is intentionally invalid for this case. A permission, login or network error is not accepted as the expected unavailable-table outcome.",
                ),
                cell(
                    "code",
                    "try:\n    await epoch.extension_inputs(review.source_execution_id, tables=['__not_a_source_table__'])\nexcept ApiError as error:\n    assert error.status_code == 400, 'Inspect the actual service error; do not treat it as missing data.'\n    print('Expected unavailable-table refusal: HTTP', error.status_code)\nelse:\n    raise AssertionError('The deliberately unavailable table was unexpectedly accepted.')",
                ),
                cell(
                    "markdown",
                    "## 3. Close this client\n\nNo alternative source or made-up result was used.",
                ),
                cell("code", "await epoch.aclose()"),
            ]
        ),
        "notebook_identity.py": (
            ROOT / "examples/notebooks/notebook_identity.py"
        ).read_text(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    for name, text in files().items():
        path = DESTINATION / name
        if args.check:
            if not path.is_file() or path.read_text() != text:
                raise SystemExit(f"Regenerate {path.relative_to(ROOT)}")
        else:
            path.write_text(text)
    print(
        "Saved-report notebooks and canonical login helper match."
        if args.check
        else "Generated four saved-report notebooks."
    )


if __name__ == "__main__":
    main()
