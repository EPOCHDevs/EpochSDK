"""Small notebook views over ordinary SDK methods; no server or vendor logic."""
from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path

import httpx
from epoch_sdk import RunRequest
from epoch_sdk.datasets import DatasetSearchResult
from epoch_sdk.output_validation import Cell, TableValue
from epoch_sdk.research import EpochClient, ResearchCompleted
from epoch_sdk.supervisor import ChosenExecution, NeedsInput
from IPython.display import JSON, display
from stratifyx import DatePeriodConfig
from stratifyx.types import DiscoverySourceAddress
from notebook_identity import identity_token


def connect() -> EpochClient:
    """Use only the Epoch identity and service URLs supplied to this kernel."""
    return EpochClient.connect(graph_url=os.environ["EPOCH_GRAPH_URL"],
        backend_url=os.environ["EPOCH_BACKEND_URL"], token=identity_token())


async def check_services() -> None:
    """Health reads only; this starts no research, vendor call or execution."""
    async with httpx.AsyncClient(headers={"Authorization": "Bearer " + identity_token()}, timeout=20) as http:
        for name, key, route in [("Backend", "EPOCH_BACKEND_URL", "/api/v1/health"),
                                 ("EpochAI", "EPOCH_GRAPH_URL", "/health/custom")]:
            response = await http.get(os.environ[key].rstrip("/") + route)
            response.raise_for_status()
            print(name, "ready at", os.environ[key])


@dataclass(frozen=True)
class Task:
    name: str
    request: RunRequest
    operation_id: str


def task(name: str, *, attempt: str = "01") -> Task:
    """Read a local question/output contract. Keep the ID to reconnect."""
    request = RunRequest.model_validate_json(
        (Path(__file__).parent / "cases" / f"{name}.json").read_text())
    return Task(name, request, f"native-discovery-{name}-{attempt}")


def display_request(review: Task) -> None:
    print("Task ID:", review.operation_id)
    print(review.request.task)
    display(JSON(review.request.to_wire(), expanded=False))


async def run(epoch: EpochClient, review: Task) -> ResearchCompleted | NeedsInput:
    """The standard SDK session owns live progress, questions and reconnection."""
    return await epoch.run(review.request, operation_id=review.operation_id)


async def read(epoch: EpochClient, result: ResearchCompleted | NeedsInput) -> dict[str, list[dict[str, Cell]]]:
    """Read every native saved table page. This starts no agent or execution."""
    if not isinstance(result, ResearchCompleted):
        raise RuntimeError("Answer the pending question in the run cell before reading results.")
    # Column names belong to each caller's declared table schema and are
    # intentionally dynamic; the native cell value vocabulary stays closed.
    tables: dict[str, list[dict[str, Cell]]] = {}
    for output in result.response.content.outputs:
        if not isinstance(output, TableValue):
            continue
        rows: list[dict[str, Cell]] = []
        total = None
        async for page in epoch.iter_response_table(result.response.response_id, output.name,
                                                    version=result.response.version):
            if total is not None and page.total_rows != total:
                raise ValueError("Saved table size changed while reading a pinned revision.")
            total = page.total_rows
            names = [column.name for column in page.columns]
            rows.extend(dict(zip(names, row, strict=True)) for row in page.rows)
        if total is None or len(rows) != total:
            raise ValueError("The complete saved table was not read.")
        tables[output.name] = rows
    print("Saved answer:", result.response.response_id, "revision", result.response.version)
    print("Rows:", {name: len(rows) for name, rows in tables.items()})
    return tables


async def execute(epoch: EpochClient, review: Task, result: ResearchCompleted,
                  *, period: DatePeriodConfig) -> ChosenExecution:
    """Reuse the saved study/plan for an explicit period; no supervisor run."""
    if result.reusable_study is None:
        raise ValueError("This answer did not return a reusable saved study.")
    suffix = f"{period.start}-{period.end}"
    return await epoch.execute(result.reusable_study, period=period,
                               operation_id=f"{review.operation_id}-execute-{suffix}")


def identities(result: DatasetSearchResult) -> list[DiscoverySourceAddress]:
    """A concise display of source-owned identities, retaining the original DTO."""
    records = result.result.records if result.page is None else result.page.records
    return [record.identity
            for record in records if record.identity is not None]
