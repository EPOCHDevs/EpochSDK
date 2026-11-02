"""Human adapters leave reviews pending until an explicit choice."""

from __future__ import annotations

import asyncio
from io import StringIO
from types import SimpleNamespace

import ipywidgets as widgets
import pytest
from rich.console import Console
from test_dataset_reviews import BUILD, waiting

from epoch_sdk.dataset_reviews import DatasetConfigureInterrupt, dataset_response
from epoch_sdk.notebook import NotebookView
from epoch_sdk.supervisor import GraphInterrupt, NeedsInput
from epoch_sdk.terminal import TerminalView


def buttons(root):
    if isinstance(root, widgets.Button):
        yield root
    for child in getattr(root, "children", ()):
        yield from buttons(child)


def test_notebook_review_never_defaults_to_save_and_edit_requires_build():
    async def scenario():
        pending = waiting()
        view = NotebookView(SimpleNamespace(operation_id="review-only"))
        task = asyncio.create_task(view.ask(pending))
        await asyncio.sleep(0)
        assert not task.done()
        controls = {button.description: button for button in buttons(view.questions)}
        assert {"Save dataset", "Don’t save", "Edit fields", "Leave waiting"} <= controls.keys()
        controls["Edit fields"].click()
        assert not task.done()
        controls["Build preview"].click()
        result = await task
        response = result["review-one"]
        assert response.action == "edit" and response.request is not None
        assert (
            response.request.preparation.schema_choice
            == pending.interrupts[0].dataset_review().operation.request.preparation.schema_choice
        )
        assert all(button.disabled for button in controls.values())

    asyncio.run(scenario())


def test_notebook_leave_keeps_the_native_decision_unanswered():
    async def scenario():
        view = NotebookView(SimpleNamespace(operation_id="leave-review"))
        task = asyncio.create_task(view.ask(waiting()))
        await asyncio.sleep(0)
        next(
            button for button in buttons(view.questions) if button.description == "Leave waiting"
        ).click()
        assert await task is None

    asyncio.run(scenario())


def test_notebook_configuration_needs_explicit_build_and_disables_controls_afterward():
    async def scenario():
        payload = DatasetConfigureInterrupt(
            tool_call_id="configure",
            proposal_ref="proposal:" + "a" * 64,
            preparation_ref=BUILD["preparation_ref"],
            request=waiting().interrupts[0].dataset_review().operation.request,
        )
        pending = NeedsInput(
            handle=waiting().handle,
            interrupts=[
                GraphInterrupt(
                    id="configure-one", value=payload.model_dump(mode="json", by_alias=True)
                )
            ],
        )
        view = NotebookView(SimpleNamespace(operation_id="configure-only"))
        task = asyncio.create_task(view.ask(pending))
        await asyncio.sleep(0)
        assert not task.done()
        next(button for button in buttons(view.questions) if button.description == "Cancel").click()
        result = await task
        assert result["configure-one"] == dataset_response(payload, "cancel")

    asyncio.run(scenario())


class Prompt:
    def __init__(self, replies):
        self.replies = iter(replies)
        self.calls = []

    async def prompt_async(self, label):
        self.calls.append(label)
        return next(self.replies)


@pytest.mark.parametrize(
    "choice,expected", [("/save", "save"), ("/decline", "decline"), ("/leave", None)]
)
def test_terminal_requires_an_explicit_available_result_choice(choice, expected):
    async def scenario():
        payload = waiting().interrupts[0].dataset_review()
        view = TerminalView(
            SimpleNamespace(operation_id="terminal-review"), console=Console(file=StringIO())
        )
        prompt = Prompt(["", choice])
        result = await view._dataset_reply(payload, prompt)
        assert (result.action if result else None) == expected
        assert len(prompt.calls) == 2

    asyncio.run(scenario())


def test_terminal_invalid_schema_retains_edits_and_requires_a_corrected_build():
    async def scenario():
        payload = waiting().interrupts[0].dataset_review()
        out = StringIO()
        view = TerminalView(SimpleNamespace(operation_id="invalid-edit"), console=Console(file=out))
        schema = payload.operation.request.preparation.schema_choice.json_schema_text
        prompt = Prompt(
            [
                "/edit",
                "Local name",
                "Local instructions",
                "{broken",
                "/build",
                "/edit",
                "",
                "",
                schema,
                "/build",
            ]
        )
        response = await view._dataset_reply(payload, prompt)
        assert response.action == "edit" and response.request.name == "Local name"
        assert response.request.preparation.instruction == "Local instructions"
        assert response.request.preparation.schema_choice.json_schema_text == schema
        assert "not valid JSON" in out.getvalue() and "Nothing was submitted" in out.getvalue()
        assert len(prompt.calls) == 10

    asyncio.run(scenario())
