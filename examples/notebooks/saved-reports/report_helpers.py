"""Small presentation/read helpers over the ordinary SDK; no server state.

Only Epoch identity and service URLs come from the environment. Vendor/model
credentials, source data, operation persistence and computation stay in services.
"""

from __future__ import annotations

import asyncio
import html
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Literal
from urllib.parse import quote, urlsplit

from epoch_sdk import RunRequest
from epoch_sdk.notebook import display_answer
from epoch_sdk.output_validation import Cell, JsonValueOutput, TableValue, TextValue
from epoch_sdk.research import EpochClient, ResearchCompleted
from epoch_sdk.responses import ResponseReference
from epoch_sdk.supervisor import NeedsInput
from IPython.display import HTML, JSON, display
from notebook_identity import identity_token
from pydantic import BaseModel, ConfigDict, JsonValue
from stratifyx import SdkExecutionRecord, SdkRequestPhase

type CaseName = Literal["msft_annual_figures", "aapl_order_activity"]
_FILES: dict[CaseName, str] = {
    "msft_annual_figures": "msft_annual_figures.json",
    "aapl_order_activity": "aapl_order_activity.json",
}


class _Case(BaseModel):
    model_config = ConfigDict(extra="forbid")
    source_environment: Literal["EPOCH_MSFT_EXECUTION_ID", "EPOCH_AAPL_EXECUTION_ID"]
    request: RunRequest


@dataclass(frozen=True)
class Task:
    name: CaseName
    request: RunRequest
    source_execution_id: str
    operation_id: str


@dataclass(frozen=True, repr=False)
class Answer:
    reference: ResponseReference
    # Output/column names belong to the caller's request, so these maps are open.
    tables: dict[str, list[dict[str, Cell]]]
    json: dict[str, JsonValue]
    text: dict[str, str]

    def __repr__(self) -> str:
        rows = {name: len(values) for name, values in self.tables.items()}
        return (
            f"Answer(tables={rows}, json={list(self.json)}, text={list(self.text)}, "
            f"version={self.reference.version})"
        )


def connect() -> EpochClient:
    """Prepare access; this starts no research, execution or vendor request."""
    return EpochClient.connect(
        graph_url=os.environ["EPOCH_GRAPH_URL"],
        backend_url=os.environ["EPOCH_BACKEND_URL"],
        token=identity_token(),
    )


def task(
    name: CaseName, *, attempt: str = "demo-01", source_execution_id: str | None = None
) -> Task:
    """Read a local question/output contract and select an existing source.

    Matching attempts reconnect. Use a new attempt for intentionally changed
    inputs; the server refuses a changed request under an existing operation ID.
    """
    definition = _Case.model_validate_json(
        (Path(__file__).parent / "cases" / _FILES[name]).read_text()
    )
    if source_execution_id is None:
        source_execution_id = os.environ[definition.source_environment]
    if (
        not source_execution_id.strip()
        or source_execution_id != source_execution_id.strip()
    ):
        raise ValueError("Choose the exact completed source execution ID.")
    if not attempt.strip() or attempt != attempt.strip():
        raise ValueError("Choose a nonblank attempt; keep it to reconnect.")
    context = [
        (
            f"Use completed source execution {source_execution_id} without refreshing its data "
            "or rerunning the original study."
        ),
        *definition.request.context,
    ]
    request = definition.request.model_copy(update={"context": context})
    prefix = os.environ.get("EPOCH_NOTEBOOK_PREFIX", "epoch-reports")
    return Task(name, request, source_execution_id, f"{prefix}-{name}-{attempt}")


def display_request(review: Task) -> None:
    """Show the selected source, stable operation ID and exact request."""
    print("Operation:", review.operation_id)
    print("Completed source:", review.source_execution_id)
    display(JSON(review.request.to_wire(), expanded=False))


async def run(epoch: EpochClient, review: Task) -> ResearchCompleted | NeedsInput:
    """Use the SDK's normal live notebook/terminal session and question controls."""
    return await epoch.run(review.request, operation_id=review.operation_id)


async def read(
    epoch: EpochClient,
    result: ResearchCompleted | SdkExecutionRecord,
    *,
    show: bool = False,
) -> Answer:
    """Read every saved table page; optionally use the ordinary answer renderer.

    A run session already displayed its answer. Keep show=False there to avoid
    duplicate prose. Direct native execution can use show=True for the same view.
    """
    if isinstance(result, ResearchCompleted):
        saved = result.response
    else:
        outputs = result.extension_outputs
        if (
            outputs is None
            or outputs.response_id is None
            or outputs.response_version is None
        ):
            raise ValueError("This operation has no confirmed saved answer to read.")
        saved = await epoch.response(
            outputs.response_id, version=outputs.response_version
        )
    tables: dict[str, list[dict[str, Cell]]] = {}
    json_values: dict[str, JsonValue] = {}
    text: dict[str, str] = {}
    for part in saved.content.outputs:
        if isinstance(part, TableValue):
            rows: list[dict[str, Cell]] = []
            total: int | None = None
            async for page in epoch.iter_response_table(
                saved.response_id, part.name, version=saved.version, page_size=100
            ):
                total = page.total_rows
                rows.extend(
                    dict(zip([column.name for column in page.columns], row))
                    for row in page.rows
                )
            if total is None or len(rows) != total:
                raise ValueError("The complete saved table was not read.")
            tables[part.name] = rows
        elif isinstance(part, JsonValueOutput):
            json_values[part.name] = part.value
        elif isinstance(part, TextValue):
            text[part.name] = part.value
    if show:
        await display_answer(epoch, saved)
    return Answer(saved.reference(), tables, json_values, text)


async def native_operation(
    epoch: EpochClient, result: ResearchCompleted
) -> SdkExecutionRecord:
    """Read the exact native operation linked by this accepted research request."""
    accepted = await epoch.backend.sdk_requests.get_sdk_request(result.request_id)
    if accepted.native_execution_request_id is None:
        raise ValueError(
            "This answer was not produced by a native execution extension."
        )
    return await epoch.backend.sdk_requests.get_sdk_execution_request(
        accepted.native_execution_request_id
    )


def dashboard(record: SdkExecutionRecord) -> str | None:
    """Link the exact saved operation only when it published a dashboard."""
    if record.extension_outputs is None or not record.extension_outputs.dashboards:
        return None
    origin = os.environ.get("EPOCH_PORTAL_URL")
    if not origin:
        print("Saved dashboard operation:", record.request.operation_id)
        print("Supply your Portal address in EPOCH_PORTAL_URL to open it.")
        return None
    parsed = urlsplit(origin)
    if (
        parsed.scheme not in {"http", "https"}
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError(
            "Use your public Portal base URL without credentials or query parameters."
        )
    url = (
        origin.rstrip("/")
        + "/execution-extensions/"
        + quote(record.request.operation_id, safe="")
    )
    display(
        HTML(
            '<a target="_blank" rel="noopener noreferrer" href="'
            + html.escape(url, quote=True)
            + '">Open saved dashboard</a>'
        )
    )
    return url


async def execute(
    epoch: EpochClient, original: SdkExecutionRecord, *, operation_id: str
) -> SdkExecutionRecord:
    """Run the same prepared report with a new idempotent operation ID.

    Source, tables, immutable definition and parameters stay exact. The original
    research link belongs to its first operation, so this standalone replay omits
    that link. It starts no supervisor, discovery or authoring process.
    """
    if original.request.input_tables is None:
        raise ValueError("Choose a prepared execution-extension operation.")
    request = original.request.model_copy(
        update={"operation_id": operation_id, "research_request_id": None}
    )
    record = await epoch.execute_extension(request)
    deadline = time.monotonic() + 300
    while True:
        if (
            record.error is not None
            or record.phase == SdkRequestPhase.FAILED
            or record.response_phase == SdkRequestPhase.FAILED
        ):
            raise RuntimeError(
                f"Report stopped. Inspect operation {operation_id}; do not resubmit changed inputs."
            )
        if record.response_phase == SdkRequestPhase.OUTPUTS_RECORDED:
            if record.extension_outputs is None:
                raise ValueError(
                    "Recorded outputs are missing their confirmed references."
                )
            return record
        if time.monotonic() >= deadline:
            raise TimeoutError(f"Still pending. Reconnect to operation {operation_id}.")
        await asyncio.sleep(1)
        record = await epoch.extension_status(operation_id)
