"""Thin walkthrough helpers over the ordinary Epoch SDK.

Share this folder, including cases/ and the two support modules. These helpers
own no server state, graph, retry policy, vendor access or model credentials.
"""

from __future__ import annotations

import asyncio
import html
import importlib.metadata
import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Literal
from urllib.parse import quote, urlsplit

import httpx
from case_support import (
    check_case_answer,
    check_variant_source,
    load_case,
    read_case_tables,
)
from epoch_sdk import RunParameters, RunRequest, date_range
from epoch_sdk.research import EpochClient, ExecutionAccepted, ResearchCompleted
from epoch_sdk.responses import ResponseReference
from epoch_sdk.supervisor import ChosenExecution, NeedsInput
from IPython.display import HTML, JSON, display
from notebook_identity import identity_token
from pydantic import JsonValue
from stratifyx import DatePeriodConfig, SdkExecutionRecord

CASES = Path(__file__).resolve().parent / "cases"
__all__ = [
    "Answer",
    "Task",
    "check_services",
    "connect",
    "dashboard",
    "date_range",
    "display_request",
    "execute",
    "read",
    "run",
    "task",
]


@dataclass(frozen=True)
class Task:
    """One desk request and its stable server-owned operation handles."""

    case: str
    request: RunRequest
    operation_id: str
    execution_id: str | None
    source_operation_id: str | None = None


@dataclass(frozen=True, repr=False)
class Answer:
    """Complete saved values for Python use; the session already showed them."""

    reference: ResponseReference
    tables: dict[str, list[dict]]
    json: dict[str, JsonValue]
    text: dict[str, str]

    def __repr__(self) -> str:
        rows = {name: len(values) for name, values in self.tables.items()}
        return (
            f"Answer(tables={rows}, json={list(self.json)}, text={list(self.text)}, "
            f"version={self.reference.version})"
        )


def connect() -> EpochClient:
    """Prepare a client from the environment's Epoch login and service URLs."""
    return EpochClient.connect(
        graph_url=os.environ["EPOCH_GRAPH_URL"],
        backend_url=os.environ["EPOCH_BACKEND_URL"],
        token=identity_token(),
    )


async def check_services() -> None:
    """Check access to both services; start no research or execution."""
    async with httpx.AsyncClient(
        headers={"Authorization": "Bearer " + identity_token()}, timeout=20
    ) as client:
        for name, key, route in [
            ("Backend", "EPOCH_BACKEND_URL", "/api/v1/health"),
            ("EpochAI", "EPOCH_GRAPH_URL", "/health/custom"),
        ]:
            response = await client.get(os.environ[key].rstrip("/") + route)
            if response.status_code == 401:
                raise RuntimeError(
                    f"{name} rejected the Epoch login. Refresh your login and rerun "
                    "setup; keep the same task ID to reconnect."
                )
            response.raise_for_status()
    print(f"Epoch ready · SDK {importlib.metadata.version('epoch-sdk')}")


def task(
    case: str,
    *,
    attempt: str = "desk-v2-01",
    followup_attempt: str = "01",
) -> Task:
    """Load a local desk request without contacting a service.

    Keep the same attempt to reconnect. Use a new attempt for changed inputs or
    an intentional refresh. For a follow-up, attempt identifies its base case.
    The ordinary RunRequest remains available as ``review.request``.
    """
    entries = json.loads((CASES / "index.json").read_text())["cases"]
    entry = next((entry for entry in entries if entry["id"] == case), None)
    if entry is None:
        raise ValueError(f"Unknown desk case {case!r}; see cases/index.json.")
    if not attempt.strip() or not followup_attempt.strip():
        raise ValueError("Attempts must be nonempty readable labels.")
    prefix = os.environ.get("EPOCH_NOTEBOOK_PREFIX", "notebook-demo")
    operation = f"{prefix}-{case}-{attempt}"
    request = RunRequest.model_validate(json.loads((CASES / entry["file"]).read_text()))
    if entry["kind"] == "output_variant":
        return Task(
            case=case,
            request=request,
            operation_id=f"{operation}-{followup_attempt}-research",
            execution_id=None,
            source_operation_id=f"{prefix}-{entry['source_case']}-{attempt}-research",
        )
    return Task(case, request, f"{operation}-research", f"{operation}-execute")


def display_request(review: Task, *, period: DatePeriodConfig | None = None) -> None:
    """Show parameters/dates before submission, with an expandable full request.

    Supply period to preview the separate saved-study execution, rather than
    the research request. The execution keeps the task's original cost settings.
    """
    if period is not None:
        parameters, operation_id = _execution_inputs(review, period)
        print("Execution ID:", operation_id)
        display(JSON(parameters.to_wire(), expanded=True))
    else:
        print("Task ID:", review.operation_id)
        if review.source_operation_id is not None:
            print("Saved source:", review.source_operation_id)
        if review.request.parameters is not None:
            display(JSON(review.request.parameters.to_wire(), expanded=True))
        display(JSON(review.request.to_wire(), expanded=False))


def _execution_inputs(
    review: Task, period: DatePeriodConfig | None
) -> tuple[RunParameters, str]:
    if (
        review.execution_id is None
        or review.request.parameters is None
        or review.request.parameters.period is None
    ):
        raise ValueError("This output-only task has no prepared execution parameters.")
    original = review.request.parameters
    parameters = RunParameters.model_validate(original.to_wire())
    operation_id = review.execution_id
    if period is not None:
        parameters = RunParameters.model_validate(
            {
                **original.to_wire(),
                "period": period.model_dump(mode="json", exclude_unset=True),
            }
        )
        if parameters.period != original.period:
            if period.start is None or period.end is None:
                raise ValueError("Use explicit resolved start/end dates for execution.")
            operation_id += f"-{period.start.isoformat()}-{period.end.isoformat()}"
    return parameters, operation_id


async def _source(epoch: EpochClient, review: Task) -> ResearchCompleted:
    if review.source_operation_id is None:
        raise ValueError("This task does not name a saved source.")
    result = await epoch.research_status(operation_id=review.source_operation_id)
    if not isinstance(result, ResearchCompleted):
        raise RuntimeError(  # noqa: TRY004 - a valid workflow can still be waiting.
            f"Complete the base task {review.source_operation_id!r} first. "
            "This helper does not start it automatically."
        )
    return result


async def run(
    epoch: EpochClient,
    review: Task,
    *,
    interface: Literal["auto", "notebook", "terminal", "headless"] = "auto",
) -> ResearchCompleted | NeedsInput:
    """Start or reconnect; let the SDK stream, ask questions and show the answer.

    A saved-output follow-up reads the completed base, validates its declarations,
    and supplies its exact identities on the same thread. It starts no base job.
    """
    if review.source_operation_id is None:
        return await epoch.run(
            review.request, operation_id=review.operation_id, interface=interface
        )
    source = await _source(epoch, review)
    request = load_case(review.case + ".json", source=source)
    result = await epoch.run(
        request,
        operation_id=review.operation_id,
        thread_id=source.response.thread_id,
        interface=interface,
    )
    if isinstance(result, ResearchCompleted):
        if (
            result.response.primary_execution_id != source.response.primary_execution_id
            or result.response.study_id != source.response.study_id
            or result.response.thread_id != source.response.thread_id
            or result.response.response_id == source.response.response_id
        ):
            raise ValueError("The follow-up did not preserve its exact saved source.")
        original = await _source(epoch, review)
        if original.response != source.response:
            raise ValueError("The original saved answer revision changed.")
    return result


def _completed(
    review: Task, result: ResearchCompleted | NeedsInput
) -> ResearchCompleted:
    if not isinstance(result, ResearchCompleted):
        raise RuntimeError(  # noqa: TRY004 - a valid workflow can still be waiting.
            "Answer the pending question in the run cell first. "
            f"Rerun it with the same task ID: {review.operation_id}."
        )
    if result.operation_id != review.operation_id:
        raise ValueError("This result belongs to a different task ID.")
    return result


async def read(
    epoch: EpochClient,
    review: Task,
    result: ResearchCompleted | NeedsInput,
    *,
    page_size: int = 1000,
) -> Answer:
    """Read every table page and check declared output shape/consistency.

    JSON/text already belong to the saved answer. Reading starts no agent or job
    and does not display the narrative again. This is not a vendor-source audit.
    """
    completed = _completed(review, result)
    tables = await read_case_tables(
        epoch, completed, page_size=page_size, verbose=False
    )
    check_case_answer(
        review.case + ".json", review.request, completed, tables, verbose=False
    )
    if review.source_operation_id is not None:
        source = await _source(epoch, review)
        source_tables = (
            await read_case_tables(epoch, source, page_size=page_size, verbose=False)
            if review.case == "sp500_momentum_json"
            else {}
        )
        check_variant_source(
            review.case + ".json", source, completed, source_tables, verbose=False
        )
    return Answer(
        reference=completed.response.reference(),
        tables=tables,
        json={
            part.name: part.value
            for part in completed.response.content.outputs
            if part.type == "json"
        },
        text={
            part.name: part.value
            for part in completed.response.content.outputs
            if part.type == "text"
        },
    )


async def execute(
    epoch: EpochClient,
    review: Task,
    result: ResearchCompleted | NeedsInput,
    *,
    period: DatePeriodConfig | None = None,
    timeout_seconds: float = 300,
) -> ChosenExecution:
    """Execute the saved study with the task's period/costs and wait for its job.

    Repeating the call attaches to the same native operation. Only that operation
    is polled; timeout/cell cancellation does not cancel or restart server work.
    Without an output program this returns native engine status. A saved native
    report or historical response plan also supplies its new answer under .response;
    a native child report remains available separately under .report.
    """
    completed = _completed(review, result)
    parameters, operation_id = _execution_inputs(review, period)
    if completed.reusable_study is None:
        raise ValueError("The saved answer has no reusable study.")
    if timeout_seconds <= 0:
        raise ValueError("The observation timeout must be positive.")
    current: ChosenExecution | ExecutionAccepted = await epoch.execute_saved(
        completed.reusable_study,
        period=parameters.period,
        execution=parameters.execution,
        operation_id=operation_id,
    )
    deadline = time.monotonic() + timeout_seconds
    previous = ""
    while True:
        status = (
            current.execution.status.value
            if isinstance(current, ChosenExecution)
            else "accepted"
        )
        if status != previous:
            print("Execution:", status, "·", operation_id)
            previous = status
        if status == "completed" and isinstance(current, ChosenExecution):
            return current
        if status in {"failed", "cancelled"}:
            raise RuntimeError(f"Execution {operation_id} {status}.")
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError(
                f"Still running: {operation_id}. Rerun execute with the same "
                "task to reconnect; no replacement job was submitted."
            )
        await asyncio.sleep(min(1, remaining))
        current = await epoch.execution_operation(operation_id)


async def dashboard(
    epoch: EpochClient,
    result: ResearchCompleted | NeedsInput | ChosenExecution,
    *,
    portal_url: str | None = None,
) -> str | None:
    """Link the exact execution only when native dashboard content exists.

    Configure your Portal origin with EPOCH_PORTAL_URL or portal_url. No dashboard
    is built by this read, and an empty response-only dashboard gets no link.
    """
    if isinstance(result, NeedsInput):
        raise RuntimeError("Answer the pending question before opening a dashboard.")  # noqa: TRY004
    report: SdkExecutionRecord | None = None
    if isinstance(result, ChosenExecution):
        report = result.report
    elif result.response.extension is not None:
        accepted = await epoch.backend.sdk_requests.get_sdk_request(result.request_id)
        if accepted.native_execution_request_id is None:
            raise ValueError("The saved report has no exact native operation link.")
        report = await epoch.backend.sdk_requests.get_sdk_execution_request(accepted.native_execution_request_id)
        if report.execution_id != result.response.primary_execution_id or report.extension_outputs is None or report.extension_outputs.provenance != result.response.extension:
            raise ValueError("The saved dashboard differs from the exact report outcome.")
    if report is not None:
        if report.extension_outputs is None or not report.extension_outputs.dashboards:
            print("Response only · no dashboard content.")
            return None
        path = "/execution-extensions/" + quote(report.request.operation_id, safe="")
    else:
        if isinstance(result, ResearchCompleted):
            execution_id, study_id = (
                result.response.primary_execution_id,
                result.response.study_id,
            )
        else:
            execution_id, study_id = result.execution.id, result.execution.definition_id
        if execution_id is None or study_id is None:
            print("This answer has no execution dashboard.")
            return None
        # Keep the ownership boundary even on older execution-read routes.
        await epoch.backend.studies_definitions.get_a_study_definition_by_id(
            study_id, request_options={"max_retries": 0}
        )
        job = await epoch.execution(execution_id)
        if job.id != execution_id or job.definition_id != study_id:
            raise ValueError("The dashboard execution differs from the saved answer.")
        metadata = await epoch.backend.studies_performance.get_performance_metadata(
            execution_id, request_options={"max_retries": 0}
        )
        populated = any(
            marker.row_count > 0
            for markers in (metadata.event_markers_metadata or {}).values()
            for marker in markers or []
        )
        # Response-only studies have no categories. Discover the actual categories
        # first, as EpochAI does; never guess ALL/GLOBAL or translate a 404 to empty.
        for category in sorted(metadata.tearsheet_metadata):
            schema = await epoch.backend.studies_dashboard.get_dashboard_schema_chart_specs_table_specs_card_values(
                execution_id, category=category, request_options={"max_retries": 0}
            )
            populated |= bool(schema.charts or schema.tables or schema.snapshot_cards)
            for content in (schema.content, schema.context):
                if content is not None:
                    populated |= bool(
                        content.graphs
                        or content.markdown
                        or content.studies
                        or content.shared_parts
                    )
            if populated:
                break
        if not populated:
            print("Response only · no dashboard content.")
            return None
        path = "/dashboard/" + quote(execution_id, safe="")
    origin = portal_url or os.environ.get("EPOCH_PORTAL_URL")
    if not origin:
        print("Dashboard content is available. Set EPOCH_PORTAL_URL to show its link.")
        return None
    parsed = urlsplit(origin)
    if (
        parsed.scheme not in {"http", "https"}
        or not parsed.netloc
        or parsed.username is not None
        or parsed.password is not None
        or parsed.path not in {"", "/"}
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError(
            "Use your Portal HTTP(S) origin, without credentials or a path."
        )
    url = origin.rstrip("/") + path
    display(
        HTML(
            '<a href="'
            + html.escape(url, quote=True)
            + '" target="_blank" rel="noopener noreferrer">Open dashboard ↗</a>'
        )
    )
    return url
