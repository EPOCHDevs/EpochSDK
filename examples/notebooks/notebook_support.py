"""Presentation and polling helpers for the local SDK walkthroughs.

Authentication is supplied by the notebook environment. This module reads no
service .env files, vendor credentials or model credentials.
"""

from __future__ import annotations

import asyncio
import html
import importlib.metadata
import json
import os
import time
from pathlib import Path

import httpx
from IPython.display import HTML, JSON, Markdown, display
from epoch_sdk import RunRequest
from epoch_sdk.errors import EpochError
from epoch_sdk.output_validation import Cell, JsonValueOutput, TableValue, TextValue
from epoch_sdk.research import EpochClient, ExecutionAccepted, ResearchCompleted, ResearchResult
from epoch_sdk.responses import ResponseTablePage
from epoch_sdk.supervisor import ChosenExecution, InProgress, NeedsInput


def connect() -> EpochClient:
    token = os.environ.get("EPOCH_TOKEN")
    if not token:
        raise RuntimeError(
            "Set EPOCH_TOKEN to your Epoch identity token, or use the prepared local "
            "notebook server, which supplies authentication to its kernels."
        )
    return EpochClient.connect(
        graph_url=os.environ["EPOCH_GRAPH_URL"],
        backend_url=os.environ["EPOCH_BACKEND_URL"],
        token=token,
    )


async def check_services() -> None:
    print("Workflow SDK:", importlib.metadata.version("epoch-sdk"))
    print("Native SDK:", importlib.metadata.version("stratifyx"))
    async with httpx.AsyncClient(
        headers={"Authorization": "Bearer " + os.environ["EPOCH_TOKEN"]}, timeout=20
    ) as http:
        for name, origin, route in [
            ("Backend", os.environ["EPOCH_BACKEND_URL"], "/api/v1/health"),
            ("EpochAI", os.environ["EPOCH_GRAPH_URL"], "/health/custom"),
        ]:
            response = await http.get(origin.rstrip("/") + route)
            response.raise_for_status()
            print(f"{name}: HTTP {response.status_code} at {origin}")


def operation_name(suffix: str) -> str:
    return os.environ.get("EPOCH_NOTEBOOK_PREFIX", "notebook-demo") + "-" + suffix


def demo_request(*, confirmation: bool = False) -> RunRequest:
    case_path = Path(__file__).resolve().parents[1] / "research-service-proof.case.json"
    request = RunRequest.model_validate(json.loads(case_path.read_text())["request"])
    if confirmation:
        request.task = (
            "Before building, ask me once to confirm that you should use exactly the two "
            "supplied years (2024 and 2025). Wait for my confirmation using ask_user. "
            "After I confirm, " + request.task
        )
    return request


async def wait_research(
    epoch: EpochClient, operation_id: str, *, timeout_seconds: float = 900
) -> ResearchCompleted | NeedsInput:
    deadline = time.monotonic() + timeout_seconds
    previous = ""
    while time.monotonic() < deadline:
        result = await epoch.research_status(operation_id=operation_id)
        if isinstance(result, (ResearchCompleted, NeedsInput)):
            return result
        if result.status != previous:
            print("Research:", result.status)
            previous = result.status
        await asyncio.sleep(1)
    raise TimeoutError("Still running. Re-run the status cell with the same operation ID.")


async def wait_execution(
    epoch: EpochClient, operation_id: str, *, timeout_seconds: float = 300
) -> ChosenExecution:
    deadline = time.monotonic() + timeout_seconds
    previous = ""
    while time.monotonic() < deadline:
        result = await epoch.execution_operation(operation_id)
        state = "accepted" if isinstance(result, ExecutionAccepted) else result.execution.status.value
        if state != previous:
            print("Execution:", state)
            previous = state
        if isinstance(result, ChosenExecution) and state == "completed":
            return result
        if state in {"failed", "cancelled"}:
            raise RuntimeError(f"Execution ended as {state}; inspect the recorded job.")
        await asyncio.sleep(1)
    raise TimeoutError("Still running. Read the same execution operation again.")


async def wait_until_admitted(
    epoch: EpochClient,
    operation_id: str,
    observer: asyncio.Task[ResearchResult],
    *,
    previous_run_id: str | None = None,
) -> ResearchResult:
    """Wait for server admission before disconnecting the local observer."""
    deadline = time.monotonic() + 90
    while time.monotonic() < deadline:
        try:
            result = await epoch.research_status(operation_id=operation_id)
        except EpochError as error:
            if error.error.code != "NOT_FOUND":
                raise
        else:
            if isinstance(result, ResearchCompleted):
                return result
            if (
                isinstance(result, (InProgress, NeedsInput))
                and result.handle.run_id is not None
                and result.handle.run_id != previous_run_id
            ):
                return result
        if observer.done():
            return await observer
        await asyncio.sleep(0.05)
    raise TimeoutError("No server admission yet; inspect the same operation ID.")


async def stop_local_observer(observer: asyncio.Task[ResearchResult]) -> bool:
    """Cancel only this Python wait; never call native server cancellation."""
    if observer.done():
        await observer
        return False
    observer.cancel()
    try:
        await observer
    except asyncio.CancelledError:
        pass
    return True


def show_table(page: ResponseTablePage) -> None:
    header = "".join("<th>" + html.escape(column.name) + "</th>" for column in page.columns)
    rows = "".join(
        "<tr>" + "".join("<td>" + html.escape(str(value)) + "</td>" for value in row) + "</tr>"
        for row in page.rows
    )
    display(HTML("<table><thead><tr>" + header + "</tr></thead><tbody>" + rows + "</tbody></table>"))
    print(f"Showing {len(page.rows)} of {page.total_rows} rows; offset {page.offset}.")


async def show_answer(epoch: EpochClient, completed: ResearchCompleted) -> None:
    print("Saved answer and source identities:")
    display(JSON(completed.response.reference().to_wire(), expanded=False))
    for part in completed.response.content.outputs:
        display(Markdown("### " + part.name))
        if isinstance(part, TableValue):
            page = await epoch.response_table(
                completed.response.response_id,
                part.name,
                version=completed.response.version,
                page_size=1000,
            )
            show_table(page)
        elif isinstance(part, JsonValueOutput):
            display(JSON(part.value, expanded=True))
        elif isinstance(part, TextValue):
            if part.format == "markdown":
                display(Markdown(part.value))
            else:
                display(HTML("<pre>" + html.escape(part.value) + "</pre>"))


def check_demo_values(completed: ResearchCompleted, rows: list[list[Cell]]) -> None:
    assert rows == [["2024", 10.0], ["2025", 15.0]], rows
    metrics = next(
        part for part in completed.response.content.outputs
        if isinstance(part, JsonValueOutput) and part.name == "metrics"
    )
    assert metrics.value == {"row_count": 2, "total_sales": 25}, metrics.value
    print("Verified: two annual rows, row_count = 2, total_sales = 25.")


def show_research(result: ResearchResult) -> None:
    if isinstance(result, NeedsInput):
        print(result.feedback())
    else:
        print("Research:", result.status)
