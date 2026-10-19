"""Build standalone, case-specific notebooks from the canonical desk requests.

Only local files are read or written. No services, vendors or models are called.
Run with --check to verify the committed examples without changing them.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from pprint import pformat

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


def cell(kind: str, source: str, *, hidden: bool = False) -> dict:
    result = {
        "cell_type": kind,
        "id": hashlib.sha256((kind + source).encode()).hexdigest()[:12],
        "metadata": {"jupyter": {"source_hidden": True}} if hidden else {},
        "source": source.rstrip().splitlines(keepends=True),
    }
    if kind == "code":
        result.update(execution_count=None, outputs=[])
    return result


def setup_cells() -> list[dict]:
    return [
        cell(
            "markdown",
            """## Connect

Select a Python kernel with `epoch-sdk[notebook]` installed. On the prepared
server, choose **Epoch SDK (local prototype)**.

The notebook needs only your Epoch login and the two service addresses. The
collapsed helper below obtains a current identity token from the environment's
configured Epoch login command, or uses `EPOCH_TOKEN`. It prints no credentials
and reads no service configuration files. On another machine, supply your own
`EPOCH_TOKEN`, `EPOCH_BACKEND_URL` and `EPOCH_GRAPH_URL`.

The next cell prepares the client and checks both services. It starts no research.
""",
        ),
        cell("code", (NOTEBOOKS / "notebook_identity.py").read_text(), hidden=True),
        cell(
            "code",
            """import importlib.metadata
import httpx
from IPython.display import JSON, display
from epoch_sdk import RunRequest
from epoch_sdk.research import EpochClient, ResearchCompleted

# Connect to Epoch using your login, not vendor or model credentials.
_epoch_token = identity_token()
epoch = EpochClient.connect(
    graph_url=os.environ["EPOCH_GRAPH_URL"],
    backend_url=os.environ["EPOCH_BACKEND_URL"],
    token=_epoch_token,
)

print("Epoch SDK:", importlib.metadata.version("epoch-sdk"))
print("Native SDK:", importlib.metadata.version("stratifyx"))
async with httpx.AsyncClient(
    headers={"Authorization": "Bearer " + _epoch_token}, timeout=20,
) as health:
    for name, origin, route in [
        ("Backend", os.environ["EPOCH_BACKEND_URL"], "/api/v1/health"),
        ("EpochAI", os.environ["EPOCH_GRAPH_URL"], "/health/custom"),
    ]:
        response = await health.get(origin.rstrip("/") + route)
        response.raise_for_status()
        print(name + ": ready")
del _epoch_token
""",
        ),
    ]


def table_read_cell(variable: str, destination: str) -> str:
    return f"""# Read every page; a page size does not limit the total table size.
{destination} = {{}}
for part in {variable}.response.content.outputs:
    if part.type != "table":
        continue
    rows = []
    async for page in epoch.iter_response_table(
        {variable}.response.response_id,
        part.name,
        version={variable}.response.version,
        page_size=1000,
    ):
        names = [column.name for column in page.columns]
        rows.extend(dict(zip(names, row, strict=True)) for row in page.rows)
    assert len(rows) == part.source.row_count
    {destination}[part.name] = rows
"""


def make_notebook(entry: dict, request: dict) -> dict:
    key = entry["id"]
    variant = entry["kind"] == "output_variant"
    context = "\n".join("- " + item for item in request["context"])
    formats = ", ".join(
        output["name"] + " (" + output.get("format", output["type"]) + ")"
        for output in request["outputs"]
    )
    introduction = (
        f"# {entry['title']}\n\n{request['task']}\n\n"
        f"**Data and assumptions**\n\n{context}\n\n"
        f"**Requested answer:** {formats}.\n\n"
        "This notebook contains its complete request and setup. Share this file; "
        "no local case JSON or helper module is required. It contains no "
        "pre-filled market results.\n"
    )
    if variant:
        prerequisite = FILENAMES[entry["source_case"]]
        introduction += (
            f"\nFirst complete [{prerequisite}]({prerequisite}). This follow-up reads "
            "that saved operation and uses the same execution. It does not start "
            "the prerequisite automatically.\n"
        )
    if entry["kind"] == "clarification":
        introduction += (
            "\nThis example deliberately asks for a fiscal/calendar-year check. "
            "Answer in the session cell. To try reconnecting, choose **Leave waiting**, "
            "then rerun the same cell with the same ID and answer there.\n"
        )
    cells = [cell("markdown", introduction), *setup_cells()]
    cells += [
        cell(
            "markdown",
            """## The request

The task and context are the desk request shown above. The collapsed output
schema declares the requested fields, formats and units; expand it to inspect
or change them. It contains no result values.

Keep the attempt unchanged to reconnect, including after a kernel restart.
Choose a new attempt when intentionally changing the request or refreshing data.
""",
        ),
        cell(
            "code",
            "OUTPUTS = " + pformat(request["outputs"], width=100, sort_dicts=False),
            hidden=True,
        ),
    ]
    request_code = (
        "TASK = " + repr(request["task"]) + "\n"
        "CONTEXT = " + pformat(request["context"], width=100) + "\n\n"
        'PREFIX = os.environ.get("EPOCH_NOTEBOOK_PREFIX", "notebook-demo")\n'
    )
    if variant:
        request_code += (
            'BASE_ATTEMPT = "desk-v2-01"\n'
            'FOLLOWUP_ATTEMPT = "01"\n'
            f'SOURCE_RESEARCH_ID = f"{{PREFIX}}-{entry["source_case"]}-{{BASE_ATTEMPT}}-research"\n'
            f'RESEARCH_ID = f"{{PREFIX}}-{key}-{{BASE_ATTEMPT}}-{{FOLLOWUP_ATTEMPT}}-research"\n\n'
            "# Read the exact completed base answer; this starts no new work.\n"
            "source = await epoch.research_status(operation_id=SOURCE_RESEARCH_ID)\n"
            'assert isinstance(source, ResearchCompleted), "Complete the base notebook first."\n'
            "ref = source.response\n"
            "assert ref.study_id and ref.primary_execution_id\n"
            "source_context = (\n"
            '    "Authorized saved evidence for this output-only follow-up: "\n'
            '    f"study_id={ref.study_id}; execution_id={ref.primary_execution_id}; "\n'
            '    f"source_response_id={ref.response_id}; source_response_version={ref.version}; "\n'
            '    f"thread_id={ref.thread_id}. Select this exact existing execution as the "\n'
            '    "primary source. Read its persisted data; create no discovery or execution job."\n'
            ")\n"
            "request = RunRequest.model_validate({\n"
            '    "task": TASK, "context": [*CONTEXT, source_context], "outputs": OUTPUTS,\n'
            "})\n"
        )
    else:
        request_code += (
            'ATTEMPT = "desk-v2-01"\n'
            f'RESEARCH_ID = f"{{PREFIX}}-{key}-{{ATTEMPT}}-research"\n'
            "PARAMETERS = "
            + pformat(request["parameters"], width=100, sort_dicts=False)
            + "\n"
            "request = RunRequest.model_validate({\n"
            '    "task": TASK, "context": CONTEXT, "parameters": PARAMETERS, "outputs": OUTPUTS,\n'
            "})\n"
        )
    request_code += 'print("Research ID:", RESEARCH_ID)\ndisplay(JSON(request.to_wire(), expanded=False))\n'
    cells += [cell("code", request_code)]
    cells += [
        cell(
            "markdown",
            """## Run the session

This is the cell that starts research or reconnects to the same operation. It
shows live activity and the published answer. If Epoch asks a question, choose
an option or write a reply and press **Send reply** inside the cell.

Nothing is selected automatically. If you leave a question waiting, rerun this
cell with the same research ID before continuing to the result cells.
""",
        )
    ]
    thread_argument = "    thread_id=source.response.thread_id,\n" if variant else ""
    cells += [
        cell(
            "code",
            "# The SDK owns streaming, questions and resume.\n"
            "result = await epoch.run(\n    request,\n    operation_id=RESEARCH_ID,\n"
            + thread_argument
            + ")\n",
        )
    ]
    cells += [
        cell(
            "markdown",
            """## Use the result in Python

The session has already displayed the answer. These cells read its typed parts
for further analysis without printing the same narrative again. Table reads
retrieve every page; JSON and text are already in the saved answer.
""",
        ),
        cell(
            "code",
            'assert isinstance(result, ResearchCompleted), "Resume the session above first."\n'
            "answer = result.response\n"
            'json_answers = {part.name: part.value for part in answer.content.outputs if part.type == "json"}\n'
            'text_answers = {part.name: part.value for part in answer.content.outputs if part.type == "text"}\n'
            + table_read_cell("result", "tables")
            + 'print("Saved answer:", answer.response_id, "revision", answer.version)\n'
            + 'print("Complete table rows:", {name: len(rows) for name, rows in tables.items()})\n',
        ),
    ]
    if variant:
        checks = (
            "assert answer.primary_execution_id == source.response.primary_execution_id\n"
            "assert answer.study_id == source.response.study_id\n"
            "assert answer.response_id != source.response.response_id\n"
            "original = await epoch.research_status(operation_id=SOURCE_RESEARCH_ID)\n"
            "assert isinstance(original, ResearchCompleted)\n"
            "assert original.response == source.response\n"
        )
        if key == "sp500_momentum_json":
            checks += table_read_cell("source", "source_tables")
            checks += (
                'value = json_answers["screener_json"]\n'
                'expected_rows = [{**row, "rank": int(row["rank"])} for row in source_tables["shortlist"]]\n'
                'expected_coverage = {name: int(value) if name.endswith("count") else value\n'
                '                     for name, value in source_tables["screening_coverage"][0].items()}\n'
                'assert value["shortlist"] == expected_rows\n'
                'assert value["coverage"] == expected_coverage\n'
            )
        checks += (
            'print("Same source execution; the original saved answer is unchanged.")\n'
        )
        cells += [
            cell(
                "markdown",
                "## Check reuse\n\nThe new answer must use the original execution and preserve its answer revision.",
            ),
            cell("code", checks),
        ]
    elif entry["kind"] == "research":
        cells += [
            cell(
                "markdown",
                """## Optional: execute the saved study again

This separate action creates a new Backend execution of the saved study using
the same period and costs. It does not rediscover data, rebuild the study,
refresh a saved roster or publish a new interpretation. It currently returns
execution status; response-plan replay remains separate work.

The execution ID below is independent of the research ID. Repeating the call
with the same ID attaches to the same execution.
""",
            ),
            cell(
                "code",
                f'EXECUTION_ID = f"{{PREFIX}}-{key}-{{ATTEMPT}}-execute"\n'
                "assert result.reusable_study is not None\n"
                "execution = await epoch.execute_saved(\n"
                "    result.reusable_study,\n"
                "    period=request.parameters.period,\n"
                "    execution=request.parameters.execution,\n"
                "    operation_id=EXECUTION_ID,\n"
                ")\n"
                'print("Execution operation:", EXECUTION_ID)\n'
                "# Read this same ID later to get its current native status.\n"
                "execution_status = await epoch.execution_operation(EXECUTION_ID)\n",
            ),
        ]
    cells += [
        cell(
            "markdown",
            "## Close this client\n\nSaved work remains on the services. Keep the readable research ID to reconnect.",
        ),
        cell("code", "await epoch.aclose()\n"),
    ]
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Epoch SDK (local prototype)",
                "language": "python",
                "name": "epoch-sdk-prototype",
            },
            "language_info": {"name": "python", "version": "3.12"},
            "epoch_example": {
                "case": key,
                "request_revision": "desk-v2",
                "self_contained": True,
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
    DESTINATION.mkdir(exist_ok=True)
    for entry in entries:
        request = json.loads((NOTEBOOKS / "cases" / entry["file"]).read_text())
        text = (
            json.dumps(make_notebook(entry, request), indent=1, ensure_ascii=False)
            + "\n"
        )
        destination = DESTINATION / FILENAMES[entry["id"]]
        if args.check:
            if not destination.is_file() or destination.read_text() != text:
                raise SystemExit(f"Regenerate the standalone example: {destination}")
        else:
            destination.write_text(text)
    print(
        f"{'Checked' if args.check else 'Generated'} {len(entries)} standalone case notebooks."
    )


if __name__ == "__main__":
    main()
