"""Asynchronous notebook widgets over the same headless research session."""

from __future__ import annotations

import asyncio
import html
import json
from dataclasses import dataclass
from typing import Literal, cast

import ipywidgets as widgets  # pyright: ignore[reportMissingTypeStubs]
from IPython.display import HTML, JSON, display  # pyright: ignore[reportUnknownVariableType]
from markdown_it import MarkdownIt
from pydantic import JsonValue, TypeAdapter
from stratifyx.types import DatasetSchemaChoice_Provided

from .dataset_reviews import DatasetConfigureInterrupt, dataset_response
from .errors import EpochError
from .output_validation import JsonValueOutput, TableValue
from .presentation import ui_text
from .research import EpochClient, ResearchCompleted
from .responses import SavedResearchResponse
from .session import (
    EventHandler,
    ResearchSession,
    SessionCompleted,
    SessionEvent,
    SessionProgress,
    SessionQuestions,
    SessionStatus,
    SessionUI,
    SessionUIRemoved,
)
from .supervisor import Answer, Answers, InterruptResponse, NeedsInput, Question

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


async def display_answer(client: EpochClient, saved: SavedResearchResponse) -> None:
    """Display an already saved answer with the ordinary notebook renderer.

    This reads bounded table previews from Backend. It starts no research,
    numerical execution or model call; use iter_response_table for all rows.
    """
    output = widgets.Output()
    display(output)
    await _render_saved_answer(client, saved, output)


async def _render_saved_answer(
    client: EpochClient, saved: SavedResearchResponse, output: widgets.Output
) -> None:
    with output:
        display(
            HTML(
                "<p><strong>Saved answer · revision "
                + str(saved.version)
                + "</strong></p><details><summary>Answer and source identities</summary><pre>"
                + html.escape(saved.reference().model_dump_json(indent=2))
                + "</pre></details>"
            )
        )
    for qualification in saved.content.qualifications:
        with output:
            display(HTML("<h4>" + html.escape(qualification.description) + "</h4>"))
            if isinstance(qualification.value, (dict, list)):
                display(JSON(qualification.value, expanded=True))
            else:
                display(HTML("<pre>" + html.escape(json.dumps(qualification.value)) + "</pre>"))
    for part in saved.content.outputs:
        with output:
            display(HTML("<h4>" + html.escape(part.name) + "</h4>"))
        if isinstance(part, TableValue):
            page = await client.response_table(
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
            with output:
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
            with output:
                if isinstance(part.value, (dict, list)):
                    display(JSON(part.value, expanded=True))
                else:
                    display(HTML("<pre>" + html.escape(json.dumps(part.value)) + "</pre>"))
        else:
            with output:
                display(
                    _markdown_view(part.value)
                    if part.format == "markdown"
                    else HTML(
                        '<pre style="white-space:pre-wrap">' + html.escape(part.value) + "</pre>"
                    )
                )


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


def _visible(widget: widgets.DOMWidget, visible: bool) -> None:
    # ipywidgets ships no layout annotation. This is a native widget property,
    # not a transport or application-state escape hatch.
    layout = cast(widgets.Layout, cast(object, widget.layout))  # pyright: ignore[reportUnknownMemberType]
    layout.display = "" if visible else "none"


class NotebookView:
    def __init__(self, session: ResearchSession) -> None:
        self.session = session
        self.status = "Connecting"
        self.rows: dict[str, str] = {}
        self.progress = widgets.HTML()
        self.questions = widgets.VBox()
        self.answer_output = widgets.Output()
        self.root = widgets.VBox([self.progress, self.questions, self.answer_output])
        self.pending_reply: asyncio.Future[dict[str, InterruptResponse] | None] | None = None
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
        elif isinstance(event, SessionCompleted):
            self.status = "Answer published"
        elif isinstance(event, SessionProgress):
            return  # The UI rows already show each step; progress carries ids for API callers.
        self._refresh()

    async def _ask_dataset(self, waiting: NeedsInput) -> dict[str, InterruptResponse] | None:
        # One native workflow owns this form. Concurrent heterogeneous interrupts
        # remain fully structured for the explicit headless resume API.
        if len(waiting.interrupts) != 1:
            self.questions.children = (
                widgets.HTML(
                    "<pre>"
                    + html.escape(waiting.feedback())
                    + "</pre><p>Use the SDK resume method to supply explicit choices for every pending interrupt.</p>"
                ),
            )
            return None
        item = waiting.interrupts[0]
        payload = item.dataset_review()
        request = (
            payload.request
            if isinstance(payload, DatasetConfigureInterrupt)
            else payload.operation.request
        )
        schema = request.preparation.schema_choice
        supplied = schema.json_schema_text if schema.mode == "provided" else ""
        parsed = TypeAdapter(JsonValue).validate_json(supplied) if supplied else None
        root_type = parsed.get("type") if isinstance(parsed, dict) else None
        primitive = isinstance(root_type, str) and root_type in {
            "string",
            "integer",
            "number",
            "boolean",
        }
        name = widgets.Text(
            value=request.name, description="Name", layout=widgets.Layout(width="100%")
        )
        instructions = widgets.Textarea(
            value=request.preparation.instruction,
            description="Instructions",
            layout=widgets.Layout(width="100%", height="80px"),
        )
        structure = widgets.Textarea(
            value=supplied,
            description="Structure",
            disabled=primitive,
            layout=widgets.Layout(width="100%", height="160px"),
        )
        form = widgets.VBox([name, instructions, structure])
        error = widgets.HTML()
        parts: list[widgets.Widget] = [
            widgets.HTML(
                '<pre style="white-space:pre-wrap">' + html.escape(waiting.feedback()) + "</pre>"
            )
        ]
        submit = widgets.Button(description="Build preview", button_style="primary")
        self.submit = submit
        leave = widgets.Button(description="Leave waiting", icon="pause")
        self.leave = leave
        cancel = widgets.Button(
            description="Cancel"
            if isinstance(payload, DatasetConfigureInterrupt)
            else "Cancel edit"
        )
        future: asyncio.Future[dict[str, InterruptResponse] | None] = (
            asyncio.get_running_loop().create_future()
        )
        self.pending_reply = future
        text = TypeAdapter(str)

        def choose(action: Literal["build", "cancel", "save", "decline", "continue"]) -> None:
            if future.done():
                return
            try:
                if action == "build":
                    chosen_schema = schema
                    if schema.mode == "provided" and not primitive:
                        exact = text.validate_python(cast(object, structure.value))  # pyright: ignore[reportUnknownMemberType]
                        json.loads(exact)
                        chosen_schema = DatasetSchemaChoice_Provided(
                            mode="provided", json_schema_text=exact
                        )
                    candidate = request.model_copy(
                        update={
                            "name": text.validate_python(cast(object, name.value)),  # pyright: ignore[reportUnknownMemberType]
                            "preparation": request.preparation.model_copy(
                                update={
                                    "instruction": text.validate_python(
                                        cast(object, instructions.value)
                                    ),  # pyright: ignore[reportUnknownMemberType]
                                    "schema_choice": chosen_schema,
                                }
                            ),
                        }
                    )
                    response = dataset_response(
                        payload,
                        "build_preview"
                        if isinstance(payload, DatasetConfigureInterrupt)
                        else "edit",
                        candidate,
                    )
                elif action == "cancel":
                    response = dataset_response(payload, "cancel")
                elif action == "save":
                    assert not isinstance(payload, DatasetConfigureInterrupt)
                    response = dataset_response(
                        payload,
                        "save_available"
                        if payload.operation.review
                        and "save_available" in payload.operation.review.allowed_actions
                        else "save",
                    )
                elif action == "decline":
                    response = dataset_response(payload, "decline")
                else:
                    response = dataset_response(payload, "continue")
                future.set_result({item.id: response})
            except (ValueError, TypeError) as problem:
                error.value = "<p>" + html.escape(str(problem)) + "</p>"

        def bind(
            button: widgets.Button,
            action: Literal["build", "cancel", "save", "decline", "continue"],
        ) -> None:
            def click(_button: widgets.Button) -> None:
                choose(action)

            button.on_click(click)  # pyright: ignore[reportUnknownMemberType]

        def leave_waiting(_button: widgets.Button) -> None:
            if not future.done():
                future.set_result(None)

        actions: list[widgets.Button] = []
        if isinstance(payload, DatasetConfigureInterrupt):
            parts.extend(
                [form, widgets.HTML("<p>Build prepares a preview. It does not save a dataset.</p>")]
            )
            actions.extend([cancel, submit])
            bind(cancel, "cancel")
        else:
            _visible(form, False)
            _visible(submit, False)
            _visible(cancel, False)
            parts.append(form)
            allowed = payload.operation.review.allowed_actions if payload.operation.review else []
            if "discard" in allowed:
                decline = widgets.Button(description="Don’t save")
                bind(decline, "decline")
                actions.append(decline)
            if payload.can_edit:
                edit = widgets.Button(
                    description="Edit instructions" if primitive else "Edit fields"
                )

                def editing(_button: widgets.Button) -> None:
                    _visible(form, True)
                    _visible(submit, True)
                    _visible(cancel, True)
                    for button in actions:
                        _visible(button, False)
                    _visible(cancel, True)
                    _visible(submit, True)

                def cancel_edit(_button: widgets.Button) -> None:
                    _visible(form, False)
                    _visible(submit, False)
                    _visible(cancel, False)
                    for button in actions:
                        _visible(button, True)

                edit.on_click(editing)  # pyright: ignore[reportUnknownMemberType]
                cancel.on_click(cancel_edit)  # pyright: ignore[reportUnknownMemberType]
                actions.append(edit)
            if any(action in allowed for action in ("save", "save_available", "retry_save")):
                save = widgets.Button(
                    description="Save available data"
                    if "save_available" in allowed
                    else "Retry saving"
                    if "retry_save" in allowed
                    else "Save dataset",
                    button_style="primary",
                )
                bind(save, "save")
                actions.append(save)
            if payload.operation.state.value in {"saved", "discarded", "expired", "stopped"}:
                proceed = widgets.Button(
                    description="Continue conversation", button_style="primary"
                )
                bind(proceed, "continue")
                actions.append(proceed)
        bind(submit, "build")
        leave.on_click(leave_waiting)  # pyright: ignore[reportUnknownMemberType]
        parts.extend(
            [
                error,
                widgets.HBox(actions + [cancel, submit, leave])
                if not isinstance(payload, DatasetConfigureInterrupt)
                else widgets.HBox(actions + [leave]),
                widgets.HTML(
                    "<small>Only an explicit choice resumes the server. Closing this cell leaves the operation waiting.</small>"
                ),
            ]
        )
        self.questions.children = tuple(parts)
        try:
            return await future
        finally:
            submit.disabled = True
            leave.disabled = True
            for button in actions:
                button.disabled = True
            cancel.disabled = True
            name.disabled = True
            instructions.disabled = True
            structure.disabled = True
            self.pending_reply = None

    async def ask(self, waiting: NeedsInput) -> dict[str, InterruptResponse] | None:
        if any(
            isinstance(item.value, dict) and item.value.get("type") == "dataset_review"
            for item in waiting.interrupts
        ):
            return await self._ask_dataset(waiting)
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
        send_button = widgets.Button(description="Send reply", button_style="primary", icon="send")
        self.submit = send_button
        leave_button = widgets.Button(description="Leave waiting", icon="pause")
        self.leave = leave_button
        future: asyncio.Future[dict[str, InterruptResponse] | None] = (
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
        send_button.on_click(submit)  # pyright: ignore[reportUnknownMemberType]
        leave_button.on_click(leave)  # pyright: ignore[reportUnknownMemberType]
        parts.extend(
            [
                error,
                widgets.HBox([send_button, leave_button]),
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
            send_button.disabled = True
            leave_button.disabled = True
            for control in controls:
                control.choices.disabled = True
                control.reply.disabled = True
                control.skip.disabled = True
            self.pending_reply = None

    async def _answer(self, result: ResearchCompleted) -> None:
        await _render_saved_answer(self.session.client, result.response, self.answer_output)

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
