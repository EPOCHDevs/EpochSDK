"""The research log, rich answers and prompt_toolkit input over the shared session core."""

from __future__ import annotations

import json

from prompt_toolkit import PromptSession
from pydantic import JsonValue, TypeAdapter
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .dataset_reviews import DatasetConfigureInterrupt, DatasetWorkflowInterrupt, dataset_response
from .files_api.types import DatasetBuildRequest, DatasetSchemaChoice_Provided
from .output_validation import JsonValueOutput, TextValue
from .presentation import question_answer
from .research import ResearchCompleted
from .research_log import ResearchLog
from .session import (
    EventHandler,
    ResearchSession,
    SessionEvent,
    SessionProgress,
    SessionQuestions,
    SessionStatus,
    SessionUI,
    SessionUIRemoved,
)
from .supervisor import Answer, Answers, InterruptResponse, NeedsInput


class TerminalView:
    def __init__(
        self,
        session: ResearchSession,
        *,
        console: Console | None = None,
        log: ResearchLog | None = None,
    ) -> None:
        self.session = session
        self.console = console or Console()
        self.status = "Connecting"
        # The same lines epoch.research.wait() prints, on the console's own output.
        self.log = log or ResearchLog(
            self.console.file,
            live=self.console.is_terminal,
            color=self.console.is_terminal and not self.console.no_color,
        )
        self.log.reattach = "run the same command to follow it."
        self._begun = False

    async def update(self, event: SessionEvent) -> None:
        if not self._begun:
            self._begun = True
            self.log.begin_research(self.session.operation_id)
        if isinstance(event, SessionStatus):
            self.status = "Research in progress" if event.status == "in_progress" else "Accepted"
            self.log.status("running" if event.status == "in_progress" else "queued")
        elif isinstance(event, SessionUI):
            self.log.ui(event.message.name, event.message.id, event.message.props)
        elif isinstance(event, SessionUIRemoved):
            self.log.ui_removed(event.id)
        elif isinstance(event, SessionProgress):
            self.log.progress(event.progress.model_dump())
        elif isinstance(event, SessionQuestions):
            self.status = "Waiting for your reply"
            asked, reviews = _asked(event.waiting)
            self.log.questions(asked, reviews=reviews)
        else:  # SessionCompleted
            self.status = "Answer published"
            saved = event.result.response
            self.log.answer_saved(saved.response_id, saved.version)

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
        self.log.pause()
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
            self.log.resume()
        return replies

    async def _answer(self, result: ResearchCompleted) -> None:
        saved = result.response  # The log has already said it was saved, and which version.
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
                        Text(part.unavailable_reason or json.dumps(part.value, ensure_ascii=False, indent=2)), title=part.name
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

        with self.log:
            result = await self.session.run(on_event=update, on_question=self.ask)
        if isinstance(result, ResearchCompleted):
            await self._answer(result)
        else:
            self.console.print(
                Text("Waiting on the server. Reuse this operation ID to continue.", style="yellow")
            )
        return result


def _asked(waiting: NeedsInput) -> tuple[list[str], int]:
    """The questions Epoch asks, in order, and how many datasets it asks you to review."""
    asked: list[str] = []
    reviews = 0
    for interrupt in waiting.interrupts:
        kind = interrupt.value.get("type") if isinstance(interrupt.value, dict) else None
        if kind == "dataset_review":
            reviews += 1
        elif kind == "ask_user":
            asked.extend(question.question for question in interrupt.ask_user().questions)
    return asked, reviews
