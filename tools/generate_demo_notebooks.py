"""Build client-readable notebooks and a portable folder of shared helpers.

Only local files are read/written. No service, vendor or model is called.
Run --check to verify committed notebooks and bundled canonical support files.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT / "examples/notebooks"
DESTINATION = NOTEBOOKS / "demos"
FILENAMES = {
    "msft_fundamentals": "01_msft_financial_quality.ipynb",
    "msft_risk_json": "02_msft_risk_vs_spy.ipynb",
    "aapl_trend_strategy": "03_aapl_trend_strategy.ipynb",
    "sp500_momentum_screener": "04_sp500_momentum_screen.ipynb",
    "qqq_treasury_regimes": "05_qqq_treasury_regimes.ipynb",
    "msft_fundamentals_plain": "06_msft_plain_text_followup.ipynb",
    "sp500_momentum_json": "07_sp500_json_followup.ipynb",
    "msft_fundamentals_confirmation": "08_clarification_and_reconnect.ipynb",
}


def cell(kind: str, source: str, *, tags: tuple[str, ...] = ()) -> dict:
    result = {
        "cell_type": kind,
        "id": hashlib.sha256((kind + source).encode()).hexdigest()[:12],
        "metadata": {"tags": list(tags)} if tags else {},
        "source": source.rstrip().splitlines(keepends=True),
    }
    if kind == "code":
        result.update(execution_count=None, outputs=[])
    return result


def make_notebook(entry: dict, request: dict) -> dict:
    key, variant = entry["id"], entry["kind"] == "output_variant"
    context = "\n".join("- " + item for item in request["context"])
    formats = ", ".join(
        output["name"] + " (" + output.get("format", output["type"]) + ")"
        for output in request["outputs"]
    )
    introduction = (
        f"# {entry['title']}\n\n{request['task']}\n\n"
        f"**Data and assumptions**\n\n{context}\n\n"
        f"**Requested answer:** {formats}.\n\n"
        "Run the short cells below. The shared helpers live beside this notebook; "
        "share the complete **demos** folder, including **cases**. No market "
        "results or credentials are stored in these source notebooks.\n"
    )
    if variant:
        source = FILENAMES[entry["source_case"]]
        introduction += (
            f"\nFirst complete [{source}]({source}). This follow-up reads that saved "
            "answer and attaches to its thread. It never starts the base case automatically.\n"
        )
    if entry["kind"] == "clarification":
        introduction += (
            "\nThis example deliberately requests a fiscal/calendar-year check. "
            "Answer in the run cell. To try reconnecting, choose **Leave waiting**, "
            "then rerun that cell with the same task ID.\n"
        )
    imports = [
        "connect",
        "check_services",
        "task",
        "display_request",
        "run",
        "read",
        "dashboard",
    ]
    if entry["kind"] == "research":
        imports += ["execute", "date_range"]
    import_lines = "".join(f"    {name},\n" for name in sorted(imports))
    cells = [
        cell("markdown", introduction),
        cell(
            "markdown",
            "## 1. Connect\n\n`connect()` prepares the ordinary SDK client using your "
            "Epoch login and service URLs. The health check confirms access; neither starts research. "
            "Choose a kernel with `epoch-sdk[notebook]` 0.1.0a6 or later installed.",
        ),
        cell(
            "code",
            f"from demo_helpers import (\n{import_lines})\n\n"
            "epoch = connect()\nawait check_services()\n",
        ),
        cell(
            "markdown",
            "## 2. Review the request\n\nThe resolved parameters are shown first; expand "
            "the full request to inspect the task, context, columns and output formats. "
            "Keep the attempt unchanged to reconnect. Change it for changed inputs or a deliberate refresh.",
        ),
        cell(
            "code",
            f'review = task("{key}", attempt="desk-v2-01")\ndisplay_request(review)\n',
        ),
        cell(
            "markdown",
            "## 3. Run\n\nOne call shows live activity, collects any explicit replies "
            "inside the cell and displays the saved answer. Rerunning it with the same "
            "task ID reconnects. Answer a pending question before proceeding.",
        ),
        cell("code", "result = await run(epoch, review)\n"),
        cell(
            "markdown",
            "## 4. Use the answer\n\nRead complete table rows, JSON and text for Python "
            "use. The helper checks requested output shape and internal consistency; "
            "it does not print the narrative again or start another run.",
        ),
        cell("code", "answer = await read(epoch, review, result)\nanswer\n"),
        cell(
            "markdown",
            "## 5. Open the dashboard, when available\n\nA response-only study can have "
            "no dashboard. This read shows a link only when the exact execution has "
            "dashboard content. Set `EPOCH_PORTAL_URL` to your Portal origin to enable the link.",
        ),
        cell("code", "dashboard_url = await dashboard(epoch, result)\n"),
    ]
    if entry["kind"] == "research":
        cells += [
            cell(
                "markdown",
                "## Optional: execute the saved study\n\nThis is a separate Backend "
                "execution with the original period and costs. It starts no supervisor "
                "or new discovery. Repeating it attaches to the same execution. "
                "It currently returns engine status; saved-answer replay is still being built.",
            ),
            cell(
                "code",
                "execution = await execute(epoch, review, result)\n"
                "execution_dashboard_url = await dashboard(epoch, execution)\n",
                tags=("optional-execution",),
            ),
            cell(
                "markdown",
                "### Optional: a later execution period\n\nThe research above uses historical "
                "dates. Preview a later engine window before executing it. This pinned "
                "example resolves **year to date** through 16 October 2026. You can also use "
                '`date_range("last year", as_of="2026-10-16")`, `"last month"`, or '
                '`date_range(months=3, as_of="2026-10-16")` for a rolling lookback. '
                "Previous-year/month presets mean complete calendar periods.\n\n"
                "Changing the engine period does not rewrite fixed fiscal labels, SQL date "
                "filters or a saved screener roster. A rolling application needs a study "
                "whose data and calculations support the later window. No future data is assumed.",
            ),
            cell(
                "code",
                'later_period = date_range("year to date", as_of="2026-10-16")\n'
                "display_request(review, period=later_period)\n",
            ),
            cell(
                "code",
                "later_execution = await execute(epoch, review, result, period=later_period)\n"
                "later_dashboard_url = await dashboard(epoch, later_execution)\n",
                tags=("optional-execution",),
            ),
        ]
    cells += [
        cell(
            "markdown",
            "## Close this client\n\nSaved work stays on the services. Keep the task ID to reconnect.",
        ),
        cell("code", "await epoch.aclose()\n"),
    ]
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3 (ipykernel)",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "version": "3.12"},
            "epoch_example": {
                "case": key,
                "request_revision": "desk-v2",
                "shared_helpers": True,
                "self_contained": False,
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    entries = json.loads((NOTEBOOKS / "cases/index.json").read_text())["cases"]
    files = {
        DESTINATION / name: (NOTEBOOKS / name).read_bytes()
        for name in ("case_support.py", "notebook_identity.py")
    }
    for source in (NOTEBOOKS / "cases").iterdir():
        if source.is_file():
            files[DESTINATION / "cases" / source.name] = source.read_bytes()
    for entry in entries:
        request = json.loads((NOTEBOOKS / "cases" / entry["file"]).read_text())
        files[DESTINATION / FILENAMES[entry["id"]]] = (
            json.dumps(make_notebook(entry, request), indent=1, ensure_ascii=False)
            + "\n"
        ).encode()
    for destination, content in files.items():
        if args.check:
            if not destination.is_file() or destination.read_bytes() != content:
                raise SystemExit(f"Regenerate the demo bundle: {destination}")
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)
    print(
        f"{'Checked' if args.check else 'Generated'} {len(entries)} case notebooks and their shared support bundle."
    )


if __name__ == "__main__":
    main()
