"""The research log: the lines wait() and the CLI print, from a real research's events."""

import io
import json
from pathlib import Path

import httpx
import pytest

from epoch_sdk import Epoch
from epoch_sdk import api as api_module
from epoch_sdk.research_log import ResearchLog, research_log

CAPTURE = json.loads(
    (Path(__file__).parent / "fixtures/research_log/msft_spy_volatility.json").read_text()
)
KEY = "epk_test_0123456789abcdef_" + "a" * 64


class Clock:
    def __init__(self) -> None:
        self.now = 0.0

    def __call__(self) -> float:
        return self.now


def replay_research(log: ResearchLog, clock: Clock) -> None:
    log.begin_research(CAPTURE["research_id"])
    for item in CAPTURE["events"]:
        clock.now = item["t"]
        log.research_event(item["data"])


def screen(text: str) -> list[str]:
    """What a terminal shows after this output. The log always erases before it redraws, so a
    carriage return here starts the line again."""
    lines, current = [], ""
    for char in text.replace("\x1b[2K", ""):
        if char == "\n":
            lines.append(current.rstrip())
            current = ""
        elif char == "\r":
            current = ""
        else:
            current += char
    return lines + [current.rstrip()]


def test_a_research_reads_as_one_line_per_finished_step():
    out, clock = io.StringIO(), Clock()
    replay_research(ResearchLog(out, clock=clock, tick=None), clock)
    assert out.getvalue().splitlines() == [
        f"research · {CAPTURE['research_id']}",
        "00:00  ✓  Question received",
        "00:04  ✓  Search dataset",
        "00:50  ✓  Built MSFT and SPY volatility in 2025                           38.0s",
        "01:12  ✓  Ran MSFT and SPY volatility in 2025                             18.1s",
        "01:14  ✓  Answer saved · rsp_cbf5d11e1eb4 · version 1",
        "          Finished in 1 min 15 s",
    ]


def test_internal_names_never_reach_the_log():
    out, clock = io.StringIO(), Clock()
    replay_research(ResearchLog(out, clock=clock, tick=None), clock)
    text = out.getvalue().lower()
    for internal in ("model status", "model_status", "trail", "open artifact", "build study phase"):
        assert internal not in text
    assert "thinking" not in text  # Only ever the live line, never kept.


def test_a_run_reads_from_its_status():
    out, clock = io.StringIO(), Clock()
    log = ResearchLog(out, clock=clock, tick=None)
    log.begin_run(CAPTURE["execution_id"])
    for item in CAPTURE["run"]:
        clock.now = item["t"]
        log.run_read(item["data"])
    assert out.getvalue().splitlines() == [
        f"run · {CAPTURE['execution_id']}",
        "00:00  ✓  Run accepted",
        "00:05  ✓  Queued                                                           5.4s",
        "00:07  ✓  Executing Study                                                  2.1s",
        "00:11  ✓  Answer saved · rsp_da2b8c5f06c5 · version 1                      4.2s",
        "          Finished in 12 s",
    ]


def test_in_a_terminal_the_step_in_progress_is_one_line_drawn_again_in_place():
    out, clock = io.StringIO(), Clock()
    log = ResearchLog(out, live=True, clock=clock, tick=None, width=80)
    log.begin_research("req_1")
    clock.now = 1
    log.ui("model_status", "model_status:1", {"state": "started", "optional": False})
    assert screen(out.getvalue())[-1].startswith("00:01  ›  Thinking…")
    clock.now = 3
    log.progress({"kind": "step_started", "label": "Building New Study"})
    assert screen(out.getvalue())[-1].startswith("00:03  ›  Building New Study")
    clock.now = 40
    log.progress({"kind": "step_completed", "label": "Built the study"})
    log.ui("model_status", "model_status:1", {"state": "recovered", "optional": False})
    lines = [line for line in screen(out.getvalue()) if line]
    assert lines[-1].startswith("00:40  ✓  Built the study") and lines[-1].endswith("37.0s")
    assert not any("Thinking" in line or "Building New" in line for line in lines)


def test_colour_and_the_live_line_only_where_someone_is_watching():
    plain = io.StringIO()
    log = ResearchLog(plain, tick=None)
    log.begin_research("req_1")
    log.progress({"kind": "step_started", "label": "Building New Study"})
    assert "\x1b" not in plain.getvalue() and "\r" not in plain.getvalue()
    coloured = io.StringIO()
    ResearchLog(coloured, live=True, color=True, tick=None).begin_research("req_1")
    assert "\x1b[32m✓\x1b[0m" in coloured.getvalue()


def test_a_notebook_keeps_carriage_returns_but_never_terminal_erase_codes():
    out = io.StringIO()
    log = ResearchLog(out, live=True, notebook=True, tick=None)
    log.begin_research("req_1")
    log.progress({"kind": "step_started", "label": "Building New Study"})
    log.progress({"kind": "step_completed", "label": "Built the study"})
    assert "\x1b[2K" not in out.getvalue() and "\r" in out.getvalue()


def test_questions_and_failures_end_the_log_with_what_happened():
    out, clock = io.StringIO(), Clock()
    log = ResearchLog(out, clock=clock, tick=None)
    clock.now = 125
    log.research_settled(
        {
            "status": "needs_input",
            "questions": [
                {
                    "id": "q-1",
                    "kind": "ask_user",
                    "questions": [
                        {"question": "Which prices should volatility use?"},
                        {"question": "Which year?"},
                    ],
                }
            ],
        }
    )
    clock.now = 220
    log.research_settled({"status": "failed", "error": {"title": "The study failed to run"}})
    assert out.getvalue().splitlines() == [
        "02:05  ?  Epoch asks: Which prices should volatility use? (+1 more)",
        "          Waiting for your answer · 2 min 5 s so far",
        "03:40  ✗  The study failed to run",
        "          Stopped after 3 min 40 s",
    ]


def test_a_failed_tool_is_one_failed_line():
    out, clock = io.StringIO(), Clock()
    log = ResearchLog(out, clock=clock, tick=None)
    log.ui("call_1", "call_1", {"status": "processing", "tool_name": "search_dataset"})
    clock.now = 2
    log.ui(
        "call_1",
        "call_1",
        {"status": "error", "tool_name": "search_dataset", "error_message": "No data"},
    )
    [line] = out.getvalue().splitlines()
    assert line.startswith("00:02  ✗  Search dataset · No data ") and line.endswith(" 2.0s")


def test_marks_fall_back_where_the_output_cannot_write_them():
    raw = io.BytesIO()
    out = io.TextIOWrapper(raw, encoding="ascii")
    ResearchLog(out, tick=None).begin_research("req_1")
    out.flush()
    assert raw.getvalue().decode().splitlines() == [
        "research - req_1",
        "00:00  +  Question received",
    ]


def test_the_log_is_written_only_where_asked():
    import sys

    assert research_log(False) is None
    assert research_log(None) is None  # pytest's stderr is not a terminal
    target = io.StringIO()
    to_target, to_stderr = research_log(target), research_log(True)
    assert to_target is not None and to_target._stream is target
    assert to_stderr is not None and to_stderr._stream is sys.stderr


def test_ctrl_c_says_the_work_keeps_going():
    out = io.StringIO()
    with pytest.raises(KeyboardInterrupt), ResearchLog(out, tick=None) as log:
        log.begin_research("req_1")
        raise KeyboardInterrupt
    assert out.getvalue().splitlines()[-1].strip() == (
        "Stopped watching. The work keeps going; wait() again to follow it."
    )


# ---------------------------------------------------------------------- wait()
def client(handler) -> Epoch:
    return Epoch(
        KEY,
        api_url="https://api.test.epoch.trade",
        http=httpx.Client(transport=httpx.MockTransport(handler)),
        max_retries=0,
    )


@pytest.fixture(autouse=True)
def no_sleep(monkeypatch):
    monkeypatch.setattr(api_module.time, "sleep", lambda seconds: None)


def research(status: str) -> dict:
    final = CAPTURE["events"][-1]["data"]["research"]
    return {**final, "status": status, "result": final["result"] if status == "completed" else None}


def test_wait_follows_the_events_prints_the_log_and_returns_the_research():
    frames = "".join(
        f"id: {index}-0\ndata: {json.dumps(item['data'])}\n\n"
        for index, item in enumerate(CAPTURE["events"])
    )

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/events"):
            return httpx.Response(
                200, content=frames.encode(), headers={"Content-Type": "text/event-stream"}
            )
        return httpx.Response(200, json=research("running"))

    out = io.StringIO()
    result = client(handler).research.wait(CAPTURE["research_id"], log=out)
    assert result.status == "completed"
    assert result.result is not None and result.result.response.version == 1
    lines = out.getvalue().splitlines()
    assert lines[0] == f"research · {CAPTURE['research_id']}"
    assert [line[10:].split("  ")[0] for line in lines[1:-1]] == [
        "Question received",
        "Search dataset",
        "Built MSFT and SPY volatility in 2025",
        "Ran MSFT and SPY volatility in 2025",
        "Answer saved · rsp_cbf5d11e1eb4 · version 1",
    ]


def test_wait_without_a_log_never_opens_the_event_stream():
    def handler(request: httpx.Request) -> httpx.Response:
        assert not request.url.path.endswith("/events")
        return httpx.Response(200, json=research("completed"))

    assert client(handler).research.wait(CAPTURE["research_id"], log=False).status == "completed"


def test_wait_keeps_logging_by_reading_when_the_stream_keeps_dropping():
    busy = {"title": "Busy", "status": 503, "code": "TEMPORARILY_UNAVAILABLE", "retryable": True}
    reads = iter(["running", "running", "completed"])

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/events"):
            return httpx.Response(503, json=busy)
        return httpx.Response(200, json=research(next(reads)))

    out = io.StringIO()
    assert client(handler).research.wait(CAPTURE["research_id"], log=out).status == "completed"
    assert "Answer saved · rsp_cbf5d11e1eb4 · version 1" in out.getvalue()


def test_wait_gives_up_at_its_deadline_while_following_events():
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/events"):
            return httpx.Response(
                200, content=b": keep-alive\n\n", headers={"Content-Type": "text/event-stream"}
            )
        return httpx.Response(200, json=research("running"))

    with pytest.raises(TimeoutError, match="still running"):
        client(handler).research.wait(CAPTURE["research_id"], log=io.StringIO(), timeout=0)


def test_a_run_wait_logs_from_reading_the_run():
    reads = iter(item["data"] for item in CAPTURE["run"])

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=next(reads))

    out = io.StringIO()
    run = client(handler).executions.wait(CAPTURE["execution_id"], log=out)
    assert run.status == "completed"
    lines = out.getvalue().splitlines()
    assert lines[1].endswith("Run accepted")
    assert "Executing Study" in out.getvalue()
    assert lines[-2].startswith("00:00  ✓  Answer saved · rsp_da2b8c5f06c5 · version 1")


# ---------------------------------------------------------------------- the CLI
def test_the_cli_prints_the_same_lines():
    pytest.importorskip("rich")
    import asyncio
    from types import SimpleNamespace

    from rich.console import Console

    from epoch_sdk.session import (
        NativeUIMessage,
        ResearchProgress,
        SessionProgress,
        SessionStatus,
        SessionUI,
    )
    from epoch_sdk.supervisor import WorkflowHandle
    from epoch_sdk.terminal import TerminalView

    out = io.StringIO()
    view = TerminalView(SimpleNamespace(operation_id="op-1"), console=Console(file=out))  # type: ignore[arg-type]
    handle = WorkflowHandle(thread_id="thread", request_id="req_1", assistant_id="epoch-ai")

    async def scenario():
        await view.update(SessionStatus(event="status", operation_id="op-1", status="in_progress"))
        await view.update(
            SessionUI(
                event="ui",
                handle=handle,
                message=NativeUIMessage(
                    type="ui",
                    id="call_1",
                    name="search_dataset",
                    props={"status": "success", "tool_name": "search_dataset"},
                ),
            )
        )
        await view.update(
            SessionProgress(
                event="progress",
                handle=handle,
                progress=ResearchProgress(kind="step_completed", label="Built the study"),
            )
        )

    asyncio.run(scenario())
    assert [line[10:].rstrip() for line in out.getvalue().splitlines()[1:]] == [
        "Question received",
        "Search dataset",
        "Built the study",
    ]
    assert view.status == "Research in progress"
