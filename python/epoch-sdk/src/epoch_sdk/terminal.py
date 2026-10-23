"""Rich progress and prompt_toolkit input over the shared session core."""

from __future__ import annotations

import json

from prompt_toolkit import PromptSession
from rich.console import Console, Group
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .output_validation import JsonValueOutput, TextValue
from .presentation import question_answer, ui_text
from .research import ResearchCompleted
from .session import (
    EventHandler,
    ResearchSession,
    SessionEvent,
    SessionQuestions,
    SessionStatus,
    SessionUI,
    SessionUIRemoved,
)
from .supervisor import Answer, Answers, NeedsInput


class TerminalView:
    def __init__(self, session: ResearchSession, *, console: Console | None = None) -> None:
        self.session = session
        self.console = console or Console()
        self.rows: dict[str, str] = {}
        self.status = "Connecting"
        self.live = Live(console=self.console, auto_refresh=False, vertical_overflow="visible")

    def _refresh(self) -> None:
        lines = [Text(self.status, style="bold cyan")]
        lines.extend(Text(value) for value in self.rows.values())
        self.live.update(
            Panel(Group(*lines), title="Epoch · " + self.session.operation_id), refresh=True
        )

    async def update(self, event: SessionEvent) -> None:
        if isinstance(event, SessionStatus):
            self.status = "Research in progress" if event.status == "in_progress" else "Accepted"
        elif isinstance(event, SessionUI):
            text = ui_text(event.message)
            if text:
                self.rows[event.message.id] = text
            else:
                self.rows.pop(event.message.id, None)
        elif isinstance(event, SessionUIRemoved):
            self.rows.pop(event.id, None)
        elif isinstance(event, SessionQuestions):
            self.status = "Waiting for your reply"
        else:
            self.status = "Answer published"
        self._refresh()

    async def ask(self, waiting: NeedsInput) -> dict[str, Answers] | None:
        self.live.stop()
        prompt = PromptSession[str]()
        replies: dict[str, Answers] = {}
        try:
            for interrupt in waiting.interrupts:
                if (
                    not isinstance(interrupt.value, dict)
                    or interrupt.value.get("type") != "ask_user"
                ):
                    self.console.print(Text(waiting.feedback()))
                    return None
                answers: list[Answer] = []
                for index, question in enumerate(interrupt.ask_user().questions):
                    self.console.print(
                        Panel(
                            Text(question.question + "\n" + question.description),
                            title="Your input",
                        )
                    )
                    for number, option in enumerate(question.options, 1):
                        recommended = " (recommended)" if option.recommended else ""
                        self.console.print(Text(f"  {number}. {option.label}{recommended}"))
                    hint = (
                        "Numbers separated by commas, or your reply"
                        if question.multi_select
                        else ("Option number, or your reply")
                    )
                    self.console.print(
                        Text(
                            "/leave keeps the server waiting; /skip explicitly skips.", style="dim"
                        )
                    )
                    while True:
                        reply = await prompt.prompt_async(hint + ": ")
                        if reply.strip() == "/leave":
                            return None
                        try:
                            answer = question_answer(question, index, reply)
                        except ValueError as error:
                            self.console.print(Text(str(error), style="yellow"))
                        else:
                            answers.append(answer)
                            break
                replies[interrupt.id] = Answers(answers=answers)
        except (EOFError, KeyboardInterrupt):
            return None
        finally:
            self.live.start()
        return replies

    async def _answer(self, result: ResearchCompleted) -> None:
        saved = result.response
        self.console.print(Text(f"Saved answer · revision {saved.version}", style="bold green"))
        for qualification in saved.content.qualifications:
            self.console.print(Panel(
                Text(json.dumps(qualification.value, ensure_ascii=False, indent=2)),
                title=Text(qualification.description),
            ))
        for part in saved.content.outputs:
            if isinstance(part, TextValue):
                value = Markdown(part.value) if part.format == "markdown" else Text(part.value)
                self.console.print(Panel(value, title=part.name))
            elif isinstance(part, JsonValueOutput):
                self.console.print(
                    Panel(
                        Text(json.dumps(part.value, ensure_ascii=False, indent=2)), title=part.name
                    )
                )
            else:
                page = await self.session.client.response_table(
                    saved.response_id, part.name, version=saved.version, page_size=25
                )
                table = Table(title=part.name)
                for column in page.columns:
                    table.add_column(column.name + (f" ({column.unit})" if column.unit else ""))
                for row in page.rows:
                    table.add_row(*(Text("—" if cell is None else str(cell)) for cell in row))
                self.console.print(table)
                if page.next_offset is not None:
                    self.console.print(
                        Text(
                            f"Preview: {len(page.rows)} of {page.total_rows} rows. "
                            "Use iter_response_table(...) for every row of this saved revision.",
                            style="dim",
                        )
                    )
        self.console.print(
            Text(
                f"{saved.response_id} · source {saved.primary_execution_id or 'no engine run'}",
                style="dim",
            )
        )

    async def run(self, *, on_event: EventHandler | None = None) -> ResearchCompleted | NeedsInput:
        async def update(event: SessionEvent) -> None:
            await self.update(event)
            if on_event is not None:
                await on_event(event)

        self.live.start()
        try:
            result = await self.session.run(on_event=update, on_question=self.ask)
        finally:
            self.live.stop()
        if isinstance(result, ResearchCompleted):
            await self._answer(result)
        else:
            self.console.print(
                Text("Waiting on the server. Reuse this operation ID to continue.", style="yellow")
            )
        return result
