"""A research's or a run's progress as log lines, the same in a terminal, a notebook and the CLI.

    research · req_7b375f4da93c
    00:00  ✓  Question received
    00:04  ✓  Search dataset                                      0.1s
    00:50  ✓  Built MSFT and SPY volatility in 2025              37.9s
    01:12  ✓  Ran MSFT and SPY volatility in 2025                18.0s
    01:15  ✓  Answer saved · rsp_cbf5d11e1eb4 · version 1
              Finished in 1 min 15 s

The lines come from the research's own events: its progress steps, which are stable (ENG-2513),
and the tools the Terminal shows as activity. A run has no event stream, so its lines come from
reading it. A finished step adds one line that is never rewritten. In a terminal or a notebook the
step in progress is one more line at the bottom, with a running timer, drawn again in place;
"Thinking…" only ever appears there. Anywhere else only finished lines are written.

Only the standard library is used, so the log works with the base install.
"""

from __future__ import annotations

import os
import shutil
import sys
import threading
import time
from collections.abc import Callable, Mapping
from types import TracebackType
from typing import IO, Any, Literal, Self, cast

type Tone = Literal["done", "live", "ask", "fail", "note"]
type LogTarget = bool | IO[str] | None

_MARKS: dict[str, str] = {"done": "✓", "live": "›", "ask": "?", "fail": "✗", "note": " "}
_PLAIN_MARKS: dict[str, str] = {"done": "+", "live": ">", "ask": "?", "fail": "x", "note": " "}
_COLORS: dict[str, str] = {"done": "32", "live": "36", "ask": "33", "fail": "31"}
_PLAIN_TEXT = str.maketrans({"·": "-", "…": "...", "→": "->", "›": ">", "✓": "+", "✗": "x"})
# Tools whose work the progress steps already report: their activity would repeat those lines.
_STEP_TOOLS = frozenset(
    {"build_study", "run_study", "fast_path_study", "run_monte_carlo", "tune_study"}
)
_THINKING = {"started": "Thinking…", "waiting": "Thinking…", "streaming": "Thinking…"}
_TOOL_LABELS = {
    "discovery": "Discover data",
    "build_study": "Build study",
    "run_study": "Run study",
}


def research_log(log: LogTarget) -> ResearchLog | None:
    """The log a wait() call writes, or None for no log.

    None (the default) logs only when someone is watching: to stderr in a terminal, or to the
    cell's output in a notebook. True logs anywhere: without a terminal, only finished lines,
    uncoloured. False never logs. A file object receives the log instead.
    """
    if log is False:
        return None
    notebook = _in_notebook()
    if log is None:
        if _isatty(sys.stderr):
            stream: IO[str] = sys.stderr
        elif notebook:
            stream = sys.stdout
        else:
            return None
    elif log is True:
        stream = sys.stdout if notebook else sys.stderr
    else:
        stream = log
    in_notebook = notebook and stream is sys.stdout
    live = in_notebook or _isatty(stream)
    return ResearchLog(
        stream,
        live=live,
        color=live and "NO_COLOR" not in os.environ,
        notebook=in_notebook,
    )


class ResearchLog:
    """Writes log lines; feed it research events, or the run each time it is read."""

    def __init__(
        self,
        stream: IO[str],
        *,
        live: bool = False,
        color: bool = False,
        notebook: bool = False,
        width: int | None = None,
        clock: Callable[[], float] = time.monotonic,
        tick: float | None = 1.0,
    ) -> None:
        self._stream = stream
        self._live = live
        self._color = color
        self._notebook = notebook
        self._clock = clock
        self._tick = tick if live else None
        self._width = width or _width(stream, live=live, notebook=notebook)
        # An output that cannot write these (an ASCII console) gets plain marks and separators.
        self._encoding = getattr(stream, "encoding", None) or "utf-8"
        self._unicode = _can_write(stream, "✓›✗…→·")
        self._marks = _MARKS if self._unicode else _PLAIN_MARKS
        self._lock = threading.RLock()
        self._stop = threading.Event()
        self._ticker: threading.Thread | None = None
        self._start = clock()
        self._drawn = 0  # Characters of the live line now on screen.
        self._paused = False
        # How to pick the work up again, said when someone stops watching (Ctrl-C).
        self.reattach = "wait() again to follow it."
        # What is in progress; the live line shows the most specific.
        self._queued = False
        self._step: tuple[str, float] | None = None
        self._tools: dict[str, tuple[str, float]] = {}
        self._thinking: dict[str, float] = {}
        self._thinking_text = "Thinking…"
        # A run, between reads.
        self._phase: tuple[str, float] | None = None
        self._phase_text = ""
        self._run_status: str | None = None
        self._saving: float | None = None
        self._ended = False

    # ------------------------------------------------------------------ lifecycle
    def __enter__(self) -> Self:
        if self._tick and self._ticker is None:
            self._ticker = threading.Thread(target=self._redraw_every_tick, daemon=True)
            self._ticker.start()
        return self

    def __exit__(
        self,
        kind: type[BaseException] | None,
        error: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if kind is KeyboardInterrupt and not self._ended:
            self.note(f"Stopped watching. The work keeps going; {self.reattach}")
        self.close()

    def close(self) -> None:
        self._stop.set()
        if self._ticker is not None and self._ticker is not threading.current_thread():
            self._ticker.join(timeout=2)
        with self._lock:
            self._erase()
            self._flush()

    def pause(self) -> None:
        """Takes the live line away, e.g. while the CLI prompts; resume() brings it back."""
        with self._lock:
            self._paused = True
            self._erase()
            self._flush()

    def resume(self) -> None:
        with self._lock:
            self._paused = False
            self._draw()

    # ------------------------------------------------------------------ lines
    def header(self, text: str) -> None:
        with self._lock:
            self._write(self._paint(text, "2"))

    def line(self, text: str, *, tone: Tone = "done", took: float | None = None) -> None:
        """A finished line, at the time since the log started."""
        with self._lock:
            self._write(self._format(self._elapsed(), tone, text, _duration(took)))

    def note(self, text: str) -> None:
        with self._lock:
            self._write(self._format(None, "note", text, ""))

    # ------------------------------------------------------------------ research
    def begin_research(self, research_id: str, *, link: str | None = None) -> None:
        self.header(" · ".join(part for part in ("research", research_id, link) if part))
        self.line("Question received")

    def research_event(self, event: Mapping[str, Any]) -> None:
        """One /v1/research/{id}/events event."""
        kind = event.get("event")
        if kind == "status":
            self.status(str(event.get("status")))
        elif kind == "ui":
            message = _mapping(event.get("message"))
            self.ui(
                str(message.get("name", "")),
                str(message.get("id", "")),
                _mapping(message.get("props")),
            )
        elif kind == "ui_removed":
            self.ui_removed(str(event.get("id", "")))
        elif kind == "progress":
            self.progress(_mapping(event.get("progress")))
        elif kind in ("questions", "completed", "failed"):
            self.research_settled(_mapping(event.get("research")))

    def research_settled(self, research: Mapping[str, Any]) -> None:
        """The last lines: what was saved, what Epoch asks, or why the research stopped."""
        status = research.get("status")
        if status == "needs_input":
            pending = _mappings(research.get("questions"))
            asked = [
                str(question.get("question", ""))
                for item in pending
                for question in _mappings(item.get("questions"))
            ]
            reviews = sum(1 for item in pending if item.get("kind") == "dataset_review")
            self.questions(asked, reviews=reviews)
        elif status == "completed":
            answer = _mapping(_mapping(research.get("result")).get("response"))
            self.answer_saved(answer.get("id"), answer.get("version"))
        elif status in ("failed", "cancelled"):
            error = _mapping(research.get("error"))
            self.stopped(str(error.get("detail") or error.get("title") or "Research stopped"))

    def status(self, status: str) -> None:
        with self._lock:
            self._queued = status == "queued"
            self._draw()

    def ui(self, name: str, message_id: str, props: Mapping[str, Any]) -> None:
        """A Terminal UI message: tool activity becomes a line; the model's work, the live line."""
        with self._lock:
            if name == "model_status":
                state = props.get("state")
                if props.get("optional") is True:
                    return
                if state in _THINKING or state == "retrying":
                    self._thinking.setdefault(message_id, self._clock())
                    self._thinking_text = (
                        "Waiting for the model service…" if state == "retrying" else "Thinking…"
                    )
                else:
                    self._thinking.pop(message_id, None)
                self._draw()
                return
            tool = props.get("tool_name")
            status = props.get("status")
            if not isinstance(tool, str) or tool in _STEP_TOOLS or name in _STEP_TOOLS:
                return
            label = _tool_label(tool)
            if status == "processing":
                self._tools.setdefault(message_id, (label, self._clock()))
                self._draw()
            elif status in ("success", "error"):
                started = self._tools.pop(message_id, (label, self._clock()))[1]
                took = self._clock() - started
                if status == "success":
                    self.line(label, took=took)
                else:
                    reason = _short(str(props.get("error_message") or "it failed"))
                    self.line(f"{label} · {reason}", tone="fail", took=took)

    def ui_removed(self, message_id: str) -> None:
        with self._lock:
            self._tools.pop(message_id, None)
            self._thinking.pop(message_id, None)
            self._draw()

    def progress(self, progress: Mapping[str, Any]) -> None:
        """A stable research step: step_started and step_completed carry the step's own words."""
        kind = progress.get("kind")
        label = str(progress.get("label") or "")
        with self._lock:
            if kind == "step_started" and label:
                self._step = (label, self._clock())
                self._draw()
            elif kind == "step_completed":
                started = self._step[1] if self._step else None
                self._step = None
                self.line(
                    label or "Step finished",
                    took=None if started is None else self._clock() - started,
                )

    def questions(self, asked: list[str], *, reviews: int = 0) -> None:
        with self._lock:
            self._clear_work()
            first = next((text for text in asked if text), "")
            if first:
                more = len(asked) - 1
                self.line(
                    f"Epoch asks: {first}" + (f" (+{more} more)" if more > 0 else ""), tone="ask"
                )
            if reviews:
                self.line("Epoch asks you to review a dataset", tone="ask")
            if not first and not reviews:
                self.line("Epoch asks a question", tone="ask")
            self.note(f"Waiting for your answer · {_spoken(self._elapsed())} so far")
            self._ended = True

    def answer_saved(self, response_id: object, version: object) -> None:
        with self._lock:
            saving = self._saving
            self._clear_work()
            parts = ["Answer saved"]
            if response_id:
                parts.append(_short_id(str(response_id)))
            if version is not None:
                parts.append(f"version {version}")
            self.line(" · ".join(parts), took=None if saving is None else self._clock() - saving)
            self.note(f"Finished in {_spoken(self._elapsed())}")
            self._ended = True

    def stopped(self, reason: str) -> None:
        with self._lock:
            self._clear_work()
            self.line(_short(reason, 120), tone="fail")
            self.note(f"Stopped after {_spoken(self._elapsed())}")
            self._ended = True

    # ------------------------------------------------------------------ run
    def begin_run(self, execution_id: str, *, link: str | None = None) -> None:
        self.header(" · ".join(part for part in ("run", execution_id, link) if part))
        self.line("Run accepted")

    def run_read(self, execution: Mapping[str, Any]) -> None:
        """The run, each time it is read: its queue, its phases and its answer become lines."""
        status = str(execution.get("status"))
        progress = _mapping(execution.get("progress"))
        answer = _mapping(execution.get("answer"))
        now = self._clock()
        with self._lock:
            previous, self._run_status = self._run_status, status
            if previous == "queued" and status != "queued" and now - self._start > 1.5:
                self.line("Queued", took=now - self._start)
            self._queued = status == "queued"
            phase = progress.get("phase")
            if isinstance(phase, str) and phase and phase != "queued":
                if self._phase is None or self._phase[0] != phase:
                    self._finish_phase(now)
                    self._phase = (phase, now)
                current, total = progress.get("current"), progress.get("total")
                self._phase_text = phase + (
                    f" {current}/{total}" if current is not None and total else ""
                )
            elif status != "queued":
                self._finish_phase(now)
            if status == "running" and self._phase is None and answer.get("status") == "running":
                self._saving = self._saving or now
            if status == "completed" and answer.get("status") not in ("queued", "running"):
                self._finish_phase(now)
                response = _mapping(answer.get("response"))
                if response:
                    self.answer_saved(response.get("id"), response.get("version"))
                else:
                    self.line("Run finished")
                    self.note(f"Finished in {_spoken(self._elapsed())}")
                    self._ended = True
            elif status in ("failed", "cancelled"):
                error = _mapping(execution.get("error"))
                self.stopped(str(error.get("detail") or error.get("title") or f"Run {status}"))
            else:
                self._draw()

    def _finish_phase(self, now: float) -> None:
        if self._phase is not None:
            # The counter shown while it ran was its last reading, not its end: name the phase.
            phase, started = self._phase
            self.line(phase, took=now - started)
            self._phase, self._phase_text = None, ""

    # ------------------------------------------------------------------ drawing
    def _clear_work(self) -> None:
        self._queued = False
        self._step = None
        self._tools.clear()
        self._thinking.clear()
        self._phase, self._phase_text, self._saving = None, "", None

    def _live_text(self) -> tuple[str, float] | None:
        if self._step:
            return self._step
        if self._tools:
            return next(reversed(self._tools.values()))
        if self._phase:
            return (self._phase_text or self._phase[0], self._phase[1])
        if self._saving is not None:
            return ("Saving the answer", self._saving)
        if self._thinking:
            return (self._thinking_text, min(self._thinking.values()))
        if self._queued:
            return ("Queued", self._start)
        return None

    def _redraw_every_tick(self) -> None:
        assert self._tick is not None
        while not self._stop.wait(self._tick):
            with self._lock:
                self._draw()

    def _draw(self) -> None:
        if not self._live or self._paused:
            return
        current = self._live_text()
        self._erase()
        if current is None:
            self._flush()
            return
        text, since = current
        rendered = self._safe(
            self._format(self._elapsed(), "live", text, _duration(self._clock() - since))
        )
        self._stream.write(rendered)
        self._drawn = len(_visible(rendered))
        self._flush()

    def _erase(self) -> None:
        if not self._drawn:
            return
        if self._notebook:  # A notebook keeps carriage returns but not terminal erase codes.
            self._stream.write("\r" + " " * self._drawn + "\r")
        else:
            self._stream.write("\r\x1b[2K")
        self._drawn = 0

    def _safe(self, text: str) -> str:
        if self._unicode:
            return text
        text = text.translate(_PLAIN_TEXT)
        return text.encode(self._encoding, "replace").decode(self._encoding)

    def _write(self, text: str) -> None:
        self._erase()
        self._stream.write(self._safe(text) + "\n")
        if self._live:
            self._draw()
        else:
            self._flush()

    def _flush(self) -> None:
        try:
            self._stream.flush()
        except (OSError, ValueError):
            pass

    def _elapsed(self) -> float:
        return self._clock() - self._start

    def _format(self, at: float | None, tone: Tone, text: str, took: str) -> str:
        stamp = _stamp(at) if at is not None else " " * 5
        mark = self._marks[tone]
        body = f"{stamp}  {mark}  "
        room = self._width - len(body) - (len(took) + 2 if took else 0) - 1
        text = text if len(text) <= room else text[: max(1, room - 1)] + "…"
        tail = (" " * (room - len(text) + 2) + took) if took else ""
        if not self._color:
            return body + text + tail
        painted_text = self._paint(
            text, "31" if tone == "fail" else ("2" if tone == "note" else "")
        )
        return (
            self._paint(stamp, "2")
            + "  "
            + self._paint(mark, _COLORS.get(tone, ""))
            + "  "
            + painted_text
            + self._paint(tail, "2")
        )

    def _paint(self, text: str, code: str) -> str:
        if not self._color or not code or not text:
            return text
        return f"\x1b[{code}m{text}\x1b[0m"


# ---------------------------------------------------------------------- helpers
def _mapping(value: object) -> Mapping[str, Any]:
    return cast(Mapping[str, Any], value) if isinstance(value, Mapping) else {}


def _mappings(value: object) -> list[Mapping[str, Any]]:
    items = cast(list[object], value) if isinstance(value, list) else []
    return [_mapping(item) for item in items]


def _tool_label(name: str) -> str:
    return _TOOL_LABELS.get(name, name.replace("_", " ").strip().capitalize() or "Tool")


def _stamp(seconds: float) -> str:
    seconds = max(0, int(seconds))
    hours, rest = divmod(seconds, 3600)
    minutes, secs = divmod(rest, 60)
    return f"{hours}:{minutes:02d}:{secs:02d}" if hours else f"{minutes:02d}:{secs:02d}"


def _duration(seconds: float | None) -> str:
    # Under half a second is not worth a column of noise.
    if seconds is None or seconds < 0.5:
        return ""
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes, secs = divmod(int(seconds), 60)
    return f"{minutes}m {secs:02d}s"


def _spoken(seconds: float) -> str:
    seconds = max(0, round(seconds))
    minutes, secs = divmod(seconds, 60)
    if not minutes:
        return f"{secs} s"
    return f"{minutes} min {secs} s" if secs else f"{minutes} min"


def _short(text: str, limit: int = 90) -> str:
    text = " ".join(text.split())
    return text if len(text) <= limit else text[: limit - 1] + "…"


def _short_id(value: str) -> str:
    """Response ids are long hashes; the start is enough to recognise one in a log."""
    prefix, _, rest = value.partition("_")
    return f"{prefix}_{rest[:12]}" if rest and len(rest) > 16 else value


def _visible(text: str) -> str:
    out: list[str] = []
    skip = False
    for char in text:
        if char == "\x1b":
            skip = True
        elif skip and char == "m":
            skip = False
        elif not skip:
            out.append(char)
    return "".join(out)


def _isatty(stream: object) -> bool:
    try:
        return bool(stream.isatty())  # type: ignore[attr-defined]
    except (AttributeError, OSError, ValueError):
        return False


def _can_write(stream: IO[str], sample: str) -> bool:
    encoding = getattr(stream, "encoding", None) or "utf-8"
    try:
        sample.encode(encoding)
    except (LookupError, UnicodeEncodeError):
        return False
    return True


def _width(stream: IO[str], *, live: bool, notebook: bool) -> int:
    if notebook:
        return 96
    if live:
        return max(60, min(100, shutil.get_terminal_size((100, 24)).columns))
    return 80


def _in_notebook() -> bool:
    if "IPython" not in sys.modules:
        return False
    try:
        from IPython import get_ipython  # type: ignore[import-not-found]
    except ImportError:
        return False
    shell = get_ipython()
    return shell is not None and type(shell).__name__ == "ZMQInteractiveShell"
