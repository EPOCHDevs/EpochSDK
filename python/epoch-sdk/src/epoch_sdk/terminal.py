"""Rich progress and prompt_toolkit input over the shared session core."""

from __future__ import annotations

import json

from prompt_toolkit import PromptSession
from pydantic import JsonValue, TypeAdapter
from rich.console import Console, Group
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from stratifyx.types import DatasetBuildRequest, DatasetSchemaChoice_Provided

from .dataset_reviews import DatasetConfigureInterrupt, DatasetWorkflowInterrupt, dataset_response
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
from .supervisor import Answer, Answers, InterruptResponse, NeedsInput


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

    async def _dataset_reply(
        self, payload: DatasetWorkflowInterrupt, prompt: PromptSession[str]
    ) -> InterruptResponse | None:
        request = (
            payload.request
            if isinstance(payload, DatasetConfigureInterrupt)
            else payload.operation.request
        )
        self.console.print(Panel(Text(request.name), title="Dataset review"))
        if isinstance(payload, DatasetConfigureInterrupt):
            self.console.print(
                Text("Review the fields before paid preparation. /build, /edit, /cancel or /leave.")
            )
        else:
            self.console.print(Text(payload.operation.message))
            if payload.preview is not None:
                self.console.print(
                    Text(payload.preview.model_dump_json(by_alias=True, exclude_none=True))
                )
            for limitation in payload.operation.limitations:
                self.console.print(Text(limitation, style="yellow"))
            self.console.print(
                Text(
                    "/save, /edit, /decline or /leave. Terminal outcomes use /continue; no new native decision is sent."
                )
            )
        if request.preparation.schema_choice.mode == "provided":
            self.console.print(Text(request.preparation.schema_choice.json_schema_text))
        edited: DatasetBuildRequest | None = None
        while True:
            choice = (await prompt.prompt_async("Dataset choice: ")).strip().casefold()
            if choice == "/leave":
                return None
            if choice == "/cancel" and isinstance(payload, DatasetConfigureInterrupt):
                return dataset_response(payload, "cancel")
            if choice == "/build" and (
                isinstance(payload, DatasetConfigureInterrupt) or edited is not None
            ):
                candidate = edited or request
                schema = candidate.preparation.schema_choice
                if schema.mode == "provided":
                    try:
                        TypeAdapter(JsonValue).validate_json(schema.json_schema_text)
                    except ValueError:
                        self.console.print(
                            Text(
                                "The edited schema is not valid JSON. Use /edit to correct it; your local name and instructions are retained.",
                                style="yellow",
                            )
                        )
                        continue
                return dataset_response(
                    payload,
                    "build_preview" if isinstance(payload, DatasetConfigureInterrupt) else "edit",
                    candidate,
                )
            if (
                choice == "/continue"
                and not isinstance(payload, DatasetConfigureInterrupt)
                and payload.operation.state.value in {"saved", "discarded", "expired", "stopped"}
            ):
                return dataset_response(payload, "continue")
            if choice == "/save" and not isinstance(payload, DatasetConfigureInterrupt):
                actions = (
                    payload.operation.review.allowed_actions if payload.operation.review else []
                )
                if "save_available" in actions:
                    return dataset_response(payload, "save_available")
                if "save" in actions or "retry_save" in actions:
                    return dataset_response(payload, "save")
            if (
                choice == "/decline"
                and not isinstance(payload, DatasetConfigureInterrupt)
                and payload.operation.review
                and "discard" in payload.operation.review.allowed_actions
            ):
                return dataset_response(payload, "decline")
            if choice == "/edit" and (
                isinstance(payload, DatasetConfigureInterrupt) or payload.can_edit
            ):
                name = await prompt.prompt_async("Dataset name (Enter keeps it): ")
                instruction = await prompt.prompt_async(
                    "Extraction instructions (Enter keeps them): "
                )
                base = edited or request
                schema = base.preparation.schema_choice
                if schema.mode == "provided":
                    original_schema = request.preparation.schema_choice
                    assert original_schema.mode == "provided"
                    parsed = TypeAdapter(JsonValue).validate_json(original_schema.json_schema_text)
                    root_type = parsed.get("type") if isinstance(parsed, dict) else None
                    primitive = isinstance(root_type, str) and root_type in {
                        "string",
                        "integer",
                        "number",
                        "boolean",
                    }
                    if not primitive:
                        raw = await prompt.prompt_async(
                            "Exact JSON Schema on one line (Enter keeps it): "
                        )
                        if raw.strip():
                            schema = DatasetSchemaChoice_Provided(mode="provided", json_schema_text=raw)
                edited = base.model_copy(
                    update={
                        "name": name.strip() or base.name,
                        "preparation": base.preparation.model_copy(
                            update={
                                "instruction": instruction.strip() or base.preparation.instruction,
                                "schema_choice": schema,
                            }
                        ),
                    }
                )
                if schema.mode == "provided":
                    try:
                        TypeAdapter(JsonValue).validate_json(schema.json_schema_text)
                    except ValueError:
                        self.console.print(
                            Text(
                                "The edited schema is not valid JSON. Your edit is retained locally; use /edit to correct it. Nothing was submitted.",
                                style="yellow",
                            )
                        )
                        continue
                self.console.print(
                    Text(
                        "Edits have not started processing. Choose /build to prepare the new preview, or /leave to keep waiting."
                    )
                )
                continue
            self.console.print(
                Text(
                    "Choose an available explicit action. Nothing is selected automatically.",
                    style="yellow",
                )
            )

    async def ask(self, waiting: NeedsInput) -> dict[str, InterruptResponse] | None:
        self.live.stop()
        prompt = PromptSession[str]()
        replies: dict[str, InterruptResponse] = {}
        try:
            for interrupt in waiting.interrupts:
                if (
                    isinstance(interrupt.value, dict)
                    and interrupt.value.get("type") == "dataset_review"
                ):
                    response = await self._dataset_reply(interrupt.dataset_review(), prompt)
                    if response is None:
                        return None
                    replies[interrupt.id] = response
                    continue
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
            self.console.print(
                Panel(
                    Text(json.dumps(qualification.value, ensure_ascii=False, indent=2)),
                    title=Text(qualification.description),
                )
            )
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
