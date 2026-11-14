"""The v1 API client (ENG-2520): one URL and one API key, methods one-to-one with the contract."""

import hashlib
import json

import httpx
import pytest

from epoch_sdk import Epoch, EpochApiError, EpochError
from epoch_sdk import api as api_module

KEY = "epk_test_0123456789abcdef_" + "a" * 64
RESEARCH = {
    "id": "req_1",
    "object": "research",
    "status": "queued",
    "operation_id": "op-1",
    "thread_id": None,
    "created_at": "2026-11-11T10:00:00Z",
    "updated_at": "2026-11-11T10:00:00Z",
    "questions": [],
    "result": None,
    "error": None,
    "links": {"self": "/v1/research/req_1", "events": "/v1/research/req_1/events"},
}
OUTPUT = {"name": "summary", "type": "text", "format": "markdown", "instructions": "Explain it."}


def client(handler, **kwargs) -> Epoch:
    return Epoch(
        KEY,
        api_url="https://api.test.epoch.trade",
        http=httpx.Client(transport=httpx.MockTransport(handler)),
        **kwargs,
    )


@pytest.fixture(autouse=True)
def no_sleep(monkeypatch):
    slept: list[float] = []
    monkeypatch.setattr(api_module.time, "sleep", slept.append)
    return slept


def test_the_key_and_url_come_from_the_environment(monkeypatch):
    monkeypatch.setenv("EPOCH_API_KEY", KEY)
    monkeypatch.setenv("EPOCH_API_URL", "https://api.dev.epoch.trade/")
    epoch = Epoch()
    assert epoch.api_url == "https://api.dev.epoch.trade"
    assert KEY not in repr(epoch)


def test_a_key_is_required(monkeypatch, tmp_path):
    monkeypatch.delenv("EPOCH_API_KEY", raising=False)
    # Without a key the client looks for a browser sign-in; keep that lookup off the real home.
    monkeypatch.setenv("EPOCH_CREDENTIAL_STORE", "file")
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    with pytest.raises(ValueError, match="EPOCH_API_KEY"):
        Epoch()


def test_starting_research_sends_the_request_with_an_idempotency_key():
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(202, json=RESEARCH)

    research = client(handler).research.create(
        "Compare MSFT and SPY volatility in 2025.",
        context=["Use daily returns in USD."],
        outputs=[OUTPUT],
    )
    assert research.id == "req_1" and research.status == "queued"
    assert research.links.self_ == "/v1/research/req_1"
    [request] = seen
    assert request.url == "https://api.test.epoch.trade/v1/research"
    assert request.headers["Authorization"] == f"Bearer {KEY}"
    assert request.headers["Idempotency-Key"]
    assert json.loads(request.content) == {
        "request": {
            "task": "Compare MSFT and SPY volatility in 2025.",
            "context": ["Use daily returns in USD."],
            "outputs": [OUTPUT],
        }
    }


def test_an_invalid_request_fails_before_any_call():
    with pytest.raises(ValueError):
        client(lambda r: httpx.Response(202, json=RESEARCH)).research.create("Task", outputs=[])


def test_an_outage_is_retried_with_the_same_idempotency_key(no_sleep):
    keys: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        keys.append(request.headers["Idempotency-Key"])
        if len(keys) == 1:
            return httpx.Response(
                503,
                headers={"Retry-After": "2"},
                json={
                    "title": "Service unavailable",
                    "status": 503,
                    "code": "TEMPORARILY_UNAVAILABLE",
                    "retryable": True,
                },
            )
        return httpx.Response(202, json=RESEARCH)

    client(handler).research.create("Task", outputs=[OUTPUT], idempotency_key="mine")
    assert keys == ["mine", "mine"]
    assert no_sleep == [2.0]


def test_a_problem_raises_an_epoch_error_with_its_details():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            409,
            json={
                "type": "about:blank",
                "title": "Conflict",
                "status": 409,
                "code": "IDEMPOTENCY_CONFLICT",
                "retryable": False,
                "detail": "This operation ID already has different accepted inputs.",
                "request_id": "r-9",
            },
        )

    with pytest.raises(EpochApiError) as failure:
        client(handler).research.create("Task", outputs=[OUTPUT])
    error = failure.value
    assert isinstance(error, EpochError)
    assert (error.status, error.request_id, error.error.code) == (
        409,
        "r-9",
        "IDEMPOTENCY_CONFLICT",
    )
    assert "different accepted inputs" in str(error)


def test_wait_reads_until_research_finishes_or_asks(no_sleep):
    states = iter(["queued", "running", "needs_input"])

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={**RESEARCH, "status": next(states)})

    research = client(handler).research.wait("req_1", poll_interval=5)
    assert research.status == "needs_input"
    assert no_sleep == [5, 5]


def test_wait_keeps_reading_through_a_passing_outage():
    busy = {"title": "Busy", "status": 503, "code": "TEMPORARILY_UNAVAILABLE", "retryable": True}
    replies = iter(
        [
            httpx.Response(503, json=busy),
            httpx.Response(503, json=busy),
            httpx.Response(200, json={**RESEARCH, "status": "completed"}),
        ]
    )
    epoch = client(lambda request: next(replies), max_retries=0)
    assert epoch.research.wait("req_1", poll_interval=1).status == "completed"


def sse(*frames: str) -> bytes:
    return "".join(frames).encode()


def test_events_resume_after_the_last_event_and_stop_at_the_answer():
    calls: list[str | None] = []
    completed = {"event": "completed", "research": {**RESEARCH, "status": "completed"}}

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request.headers.get("Last-Event-ID"))
        if len(calls) == 1:  # The connection drops after one event.
            body = sse(
                'data: {"event": "status", "research_id": "req_1", "status": "running"}\n\n',
                ": keep-alive\n\n",
                'id: 1-0\ndata: {"event": "ui", "research_id": "req_1", "message": {}}\n\n',
            )
        else:
            body = sse(f"id: 2-0\ndata: {json.dumps(completed)}\n\n")
        return httpx.Response(200, content=body, headers={"Content-Type": "text/event-stream"})

    events = list(client(handler).research.events("req_1"))
    assert [e["event"] for e in events] == ["status", "ui", "completed"]
    assert calls == [None, "1-0"]


def test_answers_are_sent_by_question_id():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/research/req_1/answers"
        assert json.loads(request.content) == {
            "answers": {"q-1": {"answers": [{"question_index": 0, "selected_indices": [0]}]}}
        }
        return httpx.Response(202, json={**RESEARCH, "status": "running"})

    assert (
        client(handler)
        .research.answer(
            "req_1", {"q-1": {"answers": [{"question_index": 0, "selected_indices": [0]}]}}
        )
        .status
        == "running"
    )


def test_rows_reads_every_page_of_the_same_version():
    asked: list[dict] = []

    def handler(request: httpx.Request) -> httpx.Response:
        asked.append(dict(request.url.params))
        offset = int(request.url.params["offset"])
        return httpx.Response(
            200,
            json={
                "response_id": "rsp_1",
                "version": 3,
                "name": "volatility",
                "type": "table",
                "schema": [{"name": "symbol", "type": "string"}],
                "rows": [[f"S{offset}"]],
                "offset": offset,
                "total_rows": 2,
                "next_offset": 1 if offset == 0 else None,
            },
        )

    rows = client(handler).responses.rows("rsp_1", "volatility")
    assert rows == [["S0"], ["S1"]]
    assert asked == [
        {"offset": "0", "page_size": "1000"},
        {"version": "3", "offset": "1", "page_size": "1000"},
    ]


def test_a_run_needs_exactly_one_source_and_sends_its_dates():
    def handler(request: httpx.Request) -> httpx.Response:
        assert json.loads(request.content) == {
            "research_id": "req_1",
            "parameters": {"period": {"start": "2026-01-01", "end": "2026-10-31"}},
        }
        return httpx.Response(
            202,
            json={
                "id": "job_1",
                "status": "running",
                "study_id": "std_1",
                "created_at": "2026-11-11T10:00:00Z",
                "progress": {"phase": "simulating", "percent": 42.0},
                "links": {"self": "/v1/executions/job_1"},
            },
        )

    epoch = client(handler)
    assert (
        epoch.executions.create("req_1", start="2026-01-01", end="2026-10-31").progress.percent
        == 42.0
    )  # type: ignore[union-attr]
    with pytest.raises(ValueError):
        epoch.executions.create()


def test_upload_sends_the_exact_bytes_and_their_digest(tmp_path):
    path = tmp_path / "q3-sales.csv"
    path.write_bytes(b"date,revenue\n2026-07-01,1\n")

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["Content-Type"] == "application/octet-stream"
        assert request.url.params["name"] == "q3-sales.csv"
        assert request.url.params["media_type"] == "text/csv"
        assert request.url.params["content_sha256"] == hashlib.sha256(path.read_bytes()).hexdigest()
        assert request.content == path.read_bytes()
        return httpx.Response(200, json={"file_ref": "file_1", "name": "q3-sales.csv"})

    assert client(handler).files.upload(path)["file_ref"] == "file_1"


def problem(status: int, code: str, *, retryable: bool, title: str = "Problem") -> dict:
    return {"title": title, "status": status, "code": code, "retryable": retryable}


def test_a_table_page_as_the_server_sends_it_parses():
    # The v1 server leaves out a column's absent description and unit; null would be refused.
    page = {
        "response_id": "rsp_1", "version": 1, "name": "results", "type": "table",
        "schema": [{"name": "ticker", "type": "string", "nullable": False},
                   {"name": "volatility", "type": "float64", "nullable": True, "unit": "percent"}],
        "rows": [["MSFT", 21.4], ["SPY", None]], "offset": 0, "total_rows": 2, "next_offset": None,
    }
    epoch = client(lambda request: httpx.Response(200, json=page))
    assert epoch.responses.rows("rsp_1", "results") == [["MSFT", 21.4], ["SPY", None]]


def test_an_answer_is_sent_once_after_an_outage(no_sleep):
    calls: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        return httpx.Response(503, json=problem(503, "TEMPORARILY_UNAVAILABLE", retryable=True))

    with pytest.raises(EpochApiError):
        client(handler).research.answer("req_1", {"q-1": {"answers": []}})
    assert len(calls) == 1 and "Idempotency-Key" not in calls[0].headers


def test_an_answer_is_sent_once_after_a_lost_connection():
    calls: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        raise httpx.ReadError("reset", request=request)

    with pytest.raises(httpx.ReadError):
        client(handler).datasets.save("drf_1", name="Sales")
    assert len(calls) == 1


def test_an_answer_refused_by_a_rate_limit_is_sent_again(no_sleep):
    replies = iter([
        httpx.Response(429, json=problem(429, "RATE_LIMITED", retryable=True), headers={"Retry-After": "-5"}),
        httpx.Response(202, json={**RESEARCH, "status": "running"}),
    ])
    epoch = client(lambda request: next(replies))
    assert epoch.research.answer("req_1", {"q-1": {"answers": []}}).status == "running"
    assert no_sleep == [0.0]  # A negative Retry-After waits no time.


def test_retries_follow_the_servers_retryable_flag(no_sleep):
    replies = iter([
        httpx.Response(500, json=problem(500, "INTERNAL_ERROR", retryable=True)),
        httpx.Response(200, json=RESEARCH),
    ])
    assert client(lambda request: next(replies)).research.get("req_1").id == "req_1"
    lasting = client(lambda request: httpx.Response(
        503, json=problem(503, "TEMPORARILY_UNAVAILABLE", retryable=False)))
    with pytest.raises(EpochApiError):
        lasting.research.get("req_1")


def test_an_api_error_keeps_the_servers_code():
    reply = {**problem(422, "DATA_REQUIRED", retryable=False, title=""), "detail": "Upload the sales file."}
    with pytest.raises(EpochApiError) as failure:
        client(lambda request: httpx.Response(422, json=reply)).research.get("req_1")
    error = failure.value
    assert (error.code, error.error.code, error.retryable) == ("DATA_REQUIRED", "DATA_REQUIRED", False)
    assert str(error) == "Upload the sales file."


def test_wait_reads_once_more_at_its_deadline(monkeypatch):
    now = [0.0]
    reads: list[float] = []
    monkeypatch.setattr(api_module.time, "monotonic", lambda: now[0])
    monkeypatch.setattr(api_module.time, "sleep", lambda seconds: now.__setitem__(0, now[0] + seconds))

    def handler(request: httpx.Request) -> httpx.Response:
        reads.append(now[0])
        return httpx.Response(200, json={**RESEARCH, "status": "running"})

    with pytest.raises(TimeoutError, match="still running"):
        client(handler).research.wait("req_1", poll_interval=5, timeout=12)
    assert reads == [0.0, 5.0, 10.0, 12.0]


def test_events_reconnect_after_a_brief_outage(no_sleep):
    calls: list[str | None] = []
    completed = {"event": "completed", "research": {**RESEARCH, "status": "completed"}}

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request.headers.get("Last-Event-ID"))
        if len(calls) == 1:
            return httpx.Response(503, json=problem(503, "TEMPORARILY_UNAVAILABLE", retryable=True),
                                  headers={"Retry-After": "2"})
        return httpx.Response(200, content=sse(f"id: 2-0\ndata: {json.dumps(completed)}\n\n"),
                              headers={"Content-Type": "text/event-stream"})

    events = list(client(handler).research.events("req_1", last_event_id="1-0"))
    assert [e["event"] for e in events] == ["completed"]
    assert calls == ["1-0", "1-0"] and no_sleep == [2.0]


def test_events_stop_at_a_lasting_refusal():
    epoch = client(lambda request: httpx.Response(404, json=problem(404, "NOT_FOUND", retryable=False)))
    with pytest.raises(EpochApiError) as failure:
        list(epoch.research.events("req_other"))
    assert failure.value.code == "NOT_FOUND"
