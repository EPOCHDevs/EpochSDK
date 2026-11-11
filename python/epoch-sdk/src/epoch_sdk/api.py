"""Epoch's public v1 API with one URL and one API key (ENG-2520).

    from epoch_sdk import Epoch

    epoch = Epoch()  # Reads EPOCH_API_KEY, and EPOCH_API_URL when set.
    research = epoch.research.create(
        task="Compare MSFT and SPY volatility in 2025.",
        outputs=[{"name": "summary", "type": "text", "instructions": "Explain it briefly."}],
    )
    research = epoch.research.wait(research.id)
    answer = epoch.responses.get(research.result.response.id)

Each method is one v1 operation (contracts/public-v1.openapi.json), plus `wait` and `rows`, which
repeat reads for you. Calls that start work send an Idempotency-Key, so a retried call attaches to
the work it already started instead of starting it twice. Failures raise EpochApiError.

The direct clients (EpochClient over Backend and LangGraph) remain for Epoch's own apps.
"""

from __future__ import annotations

import hashlib
import json
import os
import time
import uuid
from collections.abc import Callable, Iterator, Mapping, Sequence
from datetime import datetime
from pathlib import Path
from typing import Any, Literal, Self
from urllib.parse import quote

import httpx
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from .contracts import DomainError, OutputRequest, RunRequest
from .errors import EpochError
from .responses import ResponseTablePage, SavedResearchResponse

DEFAULT_API_URL = "https://api.epoch.trade"
RETRYABLE = frozenset({429, 502, 503, 504})
FINISHED = frozenset({"completed", "failed", "cancelled", "needs_input"})
FINAL_EVENTS = frozenset({"questions", "completed", "failed"})

type Status = Literal["queued", "running", "needs_input", "completed", "failed", "cancelled"]


class EpochApiError(EpochError):
    """A v1 problem response, with the API's own words and stable code."""

    def __init__(self, problem: Problem) -> None:
        self.problem = problem
        self.status = problem.status
        self.request_id = problem.request_id
        message = problem.detail or problem.title
        try:
            error = DomainError.model_validate(
                {"code": problem.code, "message": message, "retryable": problem.retryable}
            )
        except ValidationError:
            error = DomainError(
                code="TEMPORARILY_UNAVAILABLE" if problem.status >= 500 else "INVALID_REQUEST",
                message=message,
                retryable=problem.retryable,
            )
        super().__init__(error)


class _Reply(BaseModel):
    # Replies may gain fields; older clients keep working.
    model_config = ConfigDict(extra="ignore", populate_by_name=True)


class Problem(_Reply):
    title: str
    status: int
    code: str
    retryable: bool = False
    detail: str | None = None
    request_id: str | None = None


class ResponseRef(_Reply):
    id: str
    version: int


class Links(_Reply):
    self_: str = Field(alias="self")
    events: str | None = None
    app: str | None = Field(default=None, description="Opens the same work in the Epoch Terminal.")
    response: str | None = None


class SavedStudy(BaseModel):
    """A study to run again. Pass it back unchanged to executions.create(study=...)."""

    model_config = ConfigDict(extra="allow")
    study_id: str
    source_execution_id: str
    thread_id: str | None = None


class ResearchResult(_Reply):
    response: ResponseRef
    reusable_study: SavedStudy | None = None
    source_execution_id: str | None = None


class Option(_Reply):
    label: str
    recommended: bool = False


class Question(_Reply):
    question: str
    description: str = ""
    options: list[Option] = Field(default_factory=list[Option])
    multi_select: bool = False


class PendingQuestion(_Reply):
    """A question Epoch is waiting on: answer it by `id` with research.answer."""

    id: str
    kind: Literal["ask_user", "dataset_review"]
    questions: list[Question] = Field(default_factory=list[Question])
    review: dict[str, Any] | None = None


class Research(_Reply):
    id: str
    status: Status
    operation_id: str
    thread_id: str | None = None
    created_at: datetime
    updated_at: datetime
    questions: list[PendingQuestion] = Field(default_factory=list[PendingQuestion])
    result: ResearchResult | None = None
    error: Problem | None = None
    links: Links


class ExecutionProgress(_Reply):
    phase: str | None = None
    percent: float | None = None
    current: int | None = None
    total: int | None = None
    unit: str | None = None


class ExecutionAnswer(_Reply):
    status: Status
    response: ResponseRef | None = None


class Execution(_Reply):
    id: str
    status: Status
    operation_id: str | None = None
    study_id: str
    created_at: datetime
    progress: ExecutionProgress | None = None
    answer: ExecutionAnswer | None = None
    reusable_study: SavedStudy | None = None
    error: Problem | None = None
    links: Links


class _Resource:
    def __init__(self, client: Epoch) -> None:
        self._client = client


class ResearchApi(_Resource):
    def create(
        self,
        task: str | RunRequest,
        *,
        context: Sequence[str] = (),
        outputs: Sequence[OutputRequest | Mapping[str, Any]] = (),
        thread_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> Research:
        """Starts research and returns at once. Follow it with wait, events or get."""
        if isinstance(task, RunRequest):
            request = task.to_wire()
        else:
            request = RunRequest.model_validate(
                {
                    "task": task,
                    "context": list(context),
                    "outputs": [
                        o.to_wire() if isinstance(o, BaseModel) else dict(o) for o in outputs
                    ],  # type: ignore[union-attr]
                }
            ).to_wire()
        body: dict[str, Any] = {"request": request}
        if thread_id is not None:
            body["thread_id"] = thread_id
        reply = self._client.request(
            "POST", "/v1/research", json=body, idempotency_key=idempotency_key
        )
        return Research.model_validate(reply)

    def get(self, research_id: str) -> Research:
        """The research now. Reading never starts or resumes work."""
        return Research.model_validate(
            self._client.request("GET", f"/v1/research/{_path(research_id)}")
        )

    def answer(self, research_id: str, answers: Mapping[str, Any]) -> Research:
        """Answers every pending question by its id; the research continues from the same point.

        An ask_user answer is {"answers": [{"question_index": 0, "selected_indices": [0]}]}, with
        free_form_input for your own words.
        """
        reply = self._client.request(
            "POST", f"/v1/research/{_path(research_id)}/answers", json={"answers": dict(answers)}
        )
        return Research.model_validate(reply)

    def wait(
        self, research_id: str, *, poll_interval: float = 10.0, timeout: float | None = None
    ) -> Research:
        """Reads the research until it finishes, stops, or asks a question."""
        deadline = None if timeout is None else time.monotonic() + timeout
        while True:
            research = self._client.retrying(lambda: self.get(research_id))
            if research is not None and research.status in FINISHED:
                return research
            if deadline is not None and time.monotonic() + poll_interval > deadline:
                state = research.status if research else "unread"
                raise TimeoutError(f"Research {research_id} is still {state}")
            time.sleep(poll_interval)

    def events(
        self, research_id: str, *, last_event_id: str | None = None
    ) -> Iterator[dict[str, Any]]:
        """Each event as it happens, until a question, the answer or a failure.

        A dropped connection reconnects after the last event received. Stopping early never
        cancels the research.
        """
        last = last_event_id
        attempt = 0
        while True:
            try:
                for event_id, data in self._client.stream(
                    f"/v1/research/{_path(research_id)}/events", last
                ):
                    attempt = 0
                    if event_id:
                        last = event_id
                    yield data
                    if data.get("event") in FINAL_EVENTS:
                        return
            except httpx.TransportError:
                pass
            attempt += 1
            if attempt > self._client.max_retries:
                raise EpochApiError(
                    Problem(
                        title="The event stream kept dropping",
                        status=503,
                        code="TEMPORARILY_UNAVAILABLE",
                        retryable=True,
                    )
                )
            time.sleep(min(8.0, 0.5 * 2**attempt))


class ExecutionsApi(_Resource):
    def create(
        self,
        research_id: str | None = None,
        *,
        study: SavedStudy | Mapping[str, Any] | None = None,
        start: str | None = None,
        end: str | None = None,
        idempotency_key: str | None = None,
    ) -> Execution:
        """Runs a finished research's study again, for new dates. Pass research_id or study."""
        if (research_id is None) == (study is None):
            raise ValueError("Pass exactly one of research_id or study")
        period = {key: value for key, value in (("start", start), ("end", end)) if value}
        body: dict[str, Any] = {"parameters": {"period": period} if period else {}}
        if research_id is not None:
            body["research_id"] = research_id
        else:
            body["study"] = (
                study.model_dump(mode="json", exclude_none=True)
                if isinstance(study, BaseModel)
                else dict(study or {})
            )
        reply = self._client.request(
            "POST", "/v1/executions", json=body, idempotency_key=idempotency_key
        )
        return Execution.model_validate(reply)

    def get(self, execution_id: str) -> Execution:
        return Execution.model_validate(
            self._client.request("GET", f"/v1/executions/{_path(execution_id)}")
        )

    def wait(
        self, execution_id: str, *, poll_interval: float = 10.0, timeout: float | None = None
    ) -> Execution:
        """Reads the run until it finishes and its answer is saved, or it stops."""
        deadline = None if timeout is None else time.monotonic() + timeout
        while True:
            execution = self._client.retrying(lambda: self.get(execution_id))
            writing = (
                execution is not None
                and execution.status == "completed"
                and execution.answer is not None
                and execution.answer.status in ("queued", "running")
            )
            if execution is not None and execution.status in FINISHED and not writing:
                return execution
            if deadline is not None and time.monotonic() + poll_interval > deadline:
                state = execution.status if execution else "unread"
                raise TimeoutError(f"Run {execution_id} is still {state}")
            time.sleep(poll_interval)


class ResponsesApi(_Resource):
    def get(self, response_id: str, *, version: int | None = None) -> SavedResearchResponse:
        """A saved answer; the latest version unless you pin one."""
        reply = self._client.request(
            "GET", f"/v1/responses/{_path(response_id)}", params={"version": version}
        )
        return SavedResearchResponse.model_validate(reply)

    def table(
        self,
        response_id: str,
        name: str,
        *,
        version: int | None = None,
        offset: int = 0,
        page_size: int = 1000,
    ) -> ResponseTablePage:
        """One page of an answer's table. Follow next_offset, with the page's version."""
        reply = self._client.request(
            "GET",
            f"/v1/responses/{_path(response_id)}/tables/{_path(name)}",
            params={"version": version, "offset": offset, "page_size": page_size},
        )
        return ResponseTablePage.model_validate(reply)

    def rows(self, response_id: str, name: str, *, version: int | None = None) -> list[list[Any]]:
        """Every row of an answer's table, reading page after page of the same version."""
        rows: list[list[Any]] = []
        offset: int | None = 0
        while offset is not None:
            page = self.table(response_id, name, version=version, offset=offset)
            version = page.version
            rows.extend(page.rows)
            offset = page.next_offset
        return rows


class FilesApi(_Resource):
    def upload(
        self, file: str | Path | bytes, *, name: str | None = None, media_type: str | None = None
    ) -> dict[str, Any]:
        """Uploads one file. The same content uploaded again returns the same file."""
        if isinstance(file, bytes):
            if not name:
                raise ValueError("Name the file you upload from bytes")
            content = file
        else:
            path = Path(file)
            content = path.read_bytes()
            name = name or path.name
        params = {
            "name": name,
            "media_type": media_type or _media_type(name),
            "content_sha256": hashlib.sha256(content).hexdigest(),
        }
        return self._client.request(
            "POST",
            "/v1/files",
            params=params,
            content=content,
            headers={"Content-Type": "application/octet-stream"},
        )


class DatasetsApi(_Resource):
    def prepare(
        self,
        file_ref: str,
        *,
        name: str,
        columns: Sequence[Mapping[str, Any]],
        delimiter: str = ",",
        header: bool = True,
        null_values: Sequence[str] = ("",),
        request_id: str | None = None,
    ) -> dict[str, Any]:
        """Prepares a dataset from an uploaded CSV file and returns a preview. Nothing is saved yet."""
        body = {
            "file_ref": file_ref,
            "request_id": request_id or uuid.uuid4().hex,
            "name": name,
            "options": {
                "format": "csv",
                "delimiter": delimiter,
                "header": header,
                "null_values": list(null_values),
                "columns": [dict(c) for c in columns],
            },
        }
        return self._client.request("POST", "/v1/datasets", json=body)

    def save(self, draft_ref: str, *, name: str) -> dict[str, Any]:
        """Saves a prepared dataset; research can then find and use it."""
        body = {"decisions": [{"action": "save", "draft_ref": draft_ref, "name": name}]}
        return self._client.request("POST", "/v1/datasets/reviews", json=body)


class Epoch:
    """A v1 API client. Close it when done, or use it in a `with` block."""

    def __init__(
        self,
        api_key: str | None = None,
        *,
        api_url: str | None = None,
        timeout: float = 30.0,
        max_retries: int = 2,
        http: httpx.Client | None = None,
    ) -> None:
        key = api_key or os.environ.get("EPOCH_API_KEY")
        if not key:
            raise ValueError("Pass api_key or set EPOCH_API_KEY")
        self.api_url = (api_url or os.environ.get("EPOCH_API_URL") or DEFAULT_API_URL).rstrip("/")
        self.max_retries = max_retries
        self._http = http or httpx.Client(timeout=timeout)
        self._headers = {"Authorization": f"Bearer {key}", "User-Agent": "epoch-sdk-python"}
        self.research = ResearchApi(self)
        self.executions = ExecutionsApi(self)
        self.responses = ResponsesApi(self)
        self.files = FilesApi(self)
        self.datasets = DatasetsApi(self)

    def __repr__(self) -> str:  # Never shows the key.
        return f"Epoch(api_url={self.api_url!r})"

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def request(
        self,
        method: str,
        path: str,
        *,
        json: Any = None,
        params: Mapping[str, Any] | None = None,
        content: bytes | None = None,
        headers: Mapping[str, str] | None = None,
        idempotency_key: str | None = None,
    ) -> Any:
        """One call, retried on rate limits and outages. Starting work reuses one Idempotency-Key."""
        sent = {**self._headers, **(headers or {})}
        if method == "POST":
            sent["Idempotency-Key"] = idempotency_key or uuid.uuid4().hex
        query = {k: v for k, v in (params or {}).items() if v is not None}
        for attempt in range(self.max_retries + 1):
            last = attempt == self.max_retries
            try:
                response = self._http.request(
                    method,
                    self.api_url + path,
                    json=json,
                    params=query,
                    content=content,
                    headers=sent,
                )
            except httpx.TransportError:
                if last:
                    raise
                time.sleep(min(8.0, 0.5 * 2**attempt))
                continue
            if response.status_code in RETRYABLE and not last:
                time.sleep(_retry_after(response, attempt))
                continue
            if response.is_success:
                return response.json()
            raise EpochApiError(_problem(response))
        raise AssertionError("unreachable")

    def retrying[T](self, read: Callable[[], T]) -> T | None:
        """A read inside a wait loop: a passing outage means "not yet", not a failure."""
        try:
            return read()
        except EpochApiError as error:
            if not error.problem.retryable:
                raise
            return None
        except httpx.TransportError:
            return None

    def stream(
        self, path: str, last_event_id: str | None
    ) -> Iterator[tuple[str | None, dict[str, Any]]]:
        headers = {**self._headers, "Accept": "text/event-stream"}
        if last_event_id:
            headers["Last-Event-ID"] = last_event_id
        # The server sends a comment every 15 seconds, so a minute without bytes is a dead connection.
        with self._http.stream(
            "GET", self.api_url + path, headers=headers, timeout=httpx.Timeout(30.0, read=60.0)
        ) as response:
            if not response.is_success:
                response.read()
                raise EpochApiError(_problem(response))
            event_id: str | None = None
            data: list[str] = []
            for line in response.iter_lines():
                if not line:
                    if data:
                        yield event_id, json.loads("\n".join(data))
                    event_id, data = None, []
                elif not line.startswith(":"):
                    field, _, value = line.partition(":")
                    value = value.removeprefix(" ")
                    if field == "data":
                        data.append(value)
                    elif field == "id":
                        event_id = value


def _path(value: str) -> str:
    return quote(value, safe="")


def _media_type(name: str) -> str:
    suffix = name.lower().rsplit(".", 1)[-1] if "." in name else ""
    return {
        "csv": "text/csv",
        "tsv": "text/tab-separated-values",
        "json": "application/json",
        "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "pdf": "application/pdf",
    }.get(suffix, "application/octet-stream")


def _retry_after(response: httpx.Response, attempt: int) -> float:
    try:
        return min(30.0, float(response.headers["Retry-After"]))
    except (KeyError, ValueError):
        return min(8.0, 0.5 * 2**attempt)


def _problem(response: httpx.Response) -> Problem:
    try:
        return Problem.model_validate(response.json())
    except (ValueError, ValidationError):
        return Problem(
            title=response.reason_phrase or "Request failed",
            status=response.status_code,
            code="TEMPORARILY_UNAVAILABLE" if response.status_code >= 500 else "INVALID_REQUEST",
            retryable=response.status_code in RETRYABLE,
        )
