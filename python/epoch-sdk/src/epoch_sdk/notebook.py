"""Asynchronous notebook widgets over the same headless research session."""

from __future__ import annotations

import asyncio
import html
import json
from dataclasses import dataclass
from typing import cast

import ipywidgets as widgets  # pyright: ignore[reportMissingTypeStubs]
from IPython.display import HTML, JSON, display  # pyright: ignore[reportUnknownVariableType]
from markdown_it import MarkdownIt
from pydantic import TypeAdapter

from .errors import EpochError
from .output_validation import JsonValueOutput, TableValue
from .presentation import ui_text
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
from .supervisor import Answer, Answers, NeedsInput, Question

type _WidgetSelection = int | tuple[int, ...] | None
_selection: TypeAdapter[_WidgetSelection] = TypeAdapter(_WidgetSelection)
_markdown = MarkdownIt("commonmark", {"html": False}).enable("table")


def _markdown_view(value: str) -> widgets.HTML:
    # A normal HTML widget does not opt into HTMLMath/MathJax. Financial prose
    # such as "$87 billion to $136 billion" must remain literal currency while
    # headings, emphasis, links, code and tables retain Markdown formatting.
    rendered = widgets.HTML(value=_markdown.render(value))
    rendered.add_class("jp-RenderedHTMLCommon")  # pyright: ignore[reportUnknownMemberType]
    return rendered


@dataclass
class _QuestionControl:
    interrupt_id: str
    index: int
    question: Question
    choices: widgets.RadioButtons | widgets.SelectMultiple
    reply: widgets.Textarea
    skip: widgets.Checkbox

    def answer(self) -> Answer:
        # ipywidgets exposes traitlets without type stubs. Validate the UI
        # value at this narrow boundary, preserving native integer indices.
        raw = cast(object, self.choices.value)  # pyright: ignore[reportUnknownMemberType]
        selected = _selection.validate_python(raw)
        indices = (
            list(selected)
            if isinstance(selected, tuple)
            else ([] if selected is None else [selected])
        )
        text = self.reply.value.strip()
        if self.skip.value:
            if indices or text:
                raise ValueError(
                    "Clear the reply and choices before explicitly skipping a question"
                )
            return Answer(question_index=self.index)
        if not indices and not text:
            raise ValueError("Choose an option or enter a reply. Recommendations are not selected.")
        if not self.question.multi_select and indices and text:
            raise ValueError("Choose one option or write your own reply for this question")
        return Answer(
            question_index=self.index,
            selected_indices=indices,
            free_form_input=text or None,
        )


class NotebookView:
    def __init__(self, session: ResearchSession) -> None:
        self.session = session
        self.status = "Connecting"
        self.rows: dict[str, str] = {}
        self.progress = widgets.HTML()
        self.questions = widgets.VBox()
        self.answer_output = widgets.Output()
        self.root = widgets.VBox([self.progress, self.questions, self.answer_output])
        self.pending_reply: asyncio.Future[dict[str, Answers] | None] | None = None
        self.submit: widgets.Button | None = None
        self.leave: widgets.Button | None = None

    def _refresh(self) -> None:
        activity = "".join(
            '<div style="padding:7px 0;border-top:1px solid #d8e0e8;white-space:pre-wrap">'
            + html.escape(value)
            + "</div>"
            for value in self.rows.values()
        )
        self.progress.value = (
            '<section style="font-family:system-ui;border:1px solid #c7d2de;border-radius:12px;'
            'padding:16px 20px;max-height:420px;overflow:auto">'
            '<div style="font-size:12px;color:#567;letter-spacing:.05em">EPOCH · '
            + html.escape(self.session.operation_id)
            + '</div><strong style="display:block;'
            'font-size:17px;margin:6px 0 12px">'
            + html.escape(self.status)
            + "</strong>"
            + activity
            + "</section>"
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
        controls: list[_QuestionControl] = []
        parts: list[widgets.Widget] = []
        for interrupt in waiting.interrupts:
            if not isinstance(interrupt.value, dict) or interrupt.value.get("type") != "ask_user":
                self.questions.children = (
                    widgets.HTML("<pre>" + html.escape(waiting.feedback()) + "</pre>"),
                )
                return None
            for index, question in enumerate(interrupt.ask_user().questions):
                options = [
                    (option.label + (" (recommended)" if option.recommended else ""), i)
                    for i, option in enumerate(question.options)
                ]
                choices = (
                    widgets.SelectMultiple(options=options, value=())
                    if question.multi_select
                    else widgets.RadioButtons(options=options, index=None)
                )
                choices.layout = widgets.Layout(width="100%")
                reply = widgets.Textarea(
                    placeholder="Or reply in your own words",
                    layout=widgets.Layout(width="100%", height="72px"),
                )
                skip = widgets.Checkbox(value=False, description="Explicitly skip this question")
                controls.append(
                    _QuestionControl(interrupt.id, index, question, choices, reply, skip)
                )
                parts.append(
                    widgets.VBox(
                        [
                            widgets.HTML(
                                "<h4>"
                                + html.escape(question.question)
                                + "</h4><p>"
                                + html.escape(question.description)
                                + "</p>"
                            ),
                            choices,
                            reply,
                            skip,
                        ],
                        layout=widgets.Layout(padding="8px 0"),
                    )
                )
        error = widgets.HTML()
        self.submit = widgets.Button(description="Send reply", button_style="primary", icon="send")
        self.leave = widgets.Button(description="Leave waiting", icon="pause")
        future: asyncio.Future[dict[str, Answers] | None] = (
            asyncio.get_running_loop().create_future()
        )
        self.pending_reply = future

        def submit(_button: widgets.Button) -> None:
            if future.done():
                return
            answers: dict[str, list[Answer]] = {}
            try:
                for control in controls:
                    answers.setdefault(control.interrupt_id, []).append(control.answer())
            except ValueError as problem:
                error.value = '<p style="color:#b44">' + html.escape(str(problem)) + "</p>"
                return
            error.value = ""
            future.set_result({key: Answers(answers=value) for key, value in answers.items()})

        def leave(_button: widgets.Button) -> None:
            if not future.done():
                future.set_result(None)

        # ipywidgets callback registration has no shipped type annotations.
        self.submit.on_click(submit)  # pyright: ignore[reportUnknownMemberType]
        self.leave.on_click(leave)  # pyright: ignore[reportUnknownMemberType]
        parts.extend(
            [
                error,
                widgets.HBox([self.submit, self.leave]),
                widgets.HTML(
                    "<small>Only Send reply resumes the server. No option is selected automatically. "
                    "Stopping this cell leaves the operation available under the same ID.</small>"
                ),
            ]
        )
        self.questions.children = tuple(parts)
        try:
            # Await a comm callback, not blocking input(): the kernel stays able
            # to process widget messages while this one cell owns the session.
            return await future
        finally:
            self.submit.disabled = True
            self.leave.disabled = True
            for control in controls:
                control.choices.disabled = True
                control.reply.disabled = True
                control.skip.disabled = True
            self.pending_reply = None

    async def _answer(self, result: ResearchCompleted) -> None:
        saved = result.response
        with self.answer_output:
            display(
                HTML(
                    "<p><strong>Saved answer · revision "
                    + str(saved.version)
                    + "</strong></p><details><summary>Answer and source identities</summary><pre>"
                    + html.escape(saved.reference().model_dump_json(indent=2))
                    + "</pre></details>"
                )
            )
        for part in saved.content.outputs:
            with self.answer_output:
                display(HTML("<h4>" + html.escape(part.name) + "</h4>"))
            if isinstance(part, TableValue):
                page = await self.session.client.response_table(
                    saved.response_id, part.name, version=saved.version, page_size=100
                )
                headers = "".join(
                    '<th title="'
                    + html.escape(column.description or "", quote=True)
                    + '">'
                    + html.escape(column.name + (f" ({column.unit})" if column.unit else ""))
                    + "</th>"
                    for column in page.columns
                )
                rows = "".join(
                    "<tr>"
                    + "".join(
                        "<td>" + html.escape("—" if cell is None else str(cell)) + "</td>"
                        for cell in row
                    )
                    + "</tr>"
                    for row in page.rows
                )
                with self.answer_output:
                    display(
                        HTML(
                            '<div style="overflow:auto;max-height:480px"><table><thead><tr>'
                            + headers
                            + "</tr></thead><tbody>"
                            + rows
                            + "</tbody></table></div>"
                        )
                    )
                    if page.next_offset is not None:
                        display(
                            HTML(
                                f"<p>Preview: {len(page.rows)} of {page.total_rows} rows. "
                                "Use <code>iter_response_table(...)</code> to read every row "
                                "of this saved revision.</p>"
                            )
                        )
            elif isinstance(part, JsonValueOutput):
                with self.answer_output:
                    if isinstance(part.value, (dict, list)):
                        display(JSON(part.value, expanded=True))
                    else:
                        display(HTML("<pre>" + html.escape(json.dumps(part.value)) + "</pre>"))
            else:
                with self.answer_output:
                    display(
                        _markdown_view(part.value)
                        if part.format == "markdown"
                        else HTML(
                            '<pre style="white-space:pre-wrap">'
                            + html.escape(part.value)
                            + "</pre>"
                        )
                    )

    async def run(self, *, on_event: EventHandler | None = None) -> ResearchCompleted | NeedsInput:
        async def update(event: SessionEvent) -> None:
            await self.update(event)
            if on_event is not None:
                await on_event(event)

        self._refresh()
        display(self.root)
        try:
            result = await self.session.run(on_event=update, on_question=self.ask)
        except EpochError as error:
            self.status = "Research stopped · " + error.error.code
            self._refresh()
            raise
        except BaseException:
            self.status = "Local session stopped · reconnect using the same operation ID"
            self._refresh()
            raise
        if isinstance(result, ResearchCompleted):
            await self._answer(result)
        return result
