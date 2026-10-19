"""Presentation/input component proofs; real-kernel/live acceptance is separate."""

from __future__ import annotations

import asyncio
from io import StringIO

import ipywidgets as widgets
import pytest
from prompt_toolkit.application import create_app_session
from prompt_toolkit.input import create_pipe_input
from prompt_toolkit.output import DummyOutput
from rich.console import Console
from test_session import StreamService
from test_supervisor import INTERRUPT

from epoch_sdk.notebook import NotebookView
from epoch_sdk.research import ResearchCompleted
from epoch_sdk.supervisor import GraphInterrupt, NeedsInput, WorkflowHandle
from epoch_sdk.terminal import TerminalView


def pending():
    return NeedsInput(
        handle=WorkflowHandle(
            thread_id="thread",
            request_id="request",
            assistant_id="epoch-ai",
            operation_id="questions",
        ),
        interrupts=[GraphInterrupt.model_validate(INTERRUPT)],
    )


def test_notebook_requires_explicit_submit_and_keeps_event_loop_responsive():
    async def scenario():
        service = StreamService()
        async with service.client() as client:
            view = NotebookView(client.session(operation_id="questions"))
            question = asyncio.create_task(view.ask(pending()))
            await asyncio.sleep(0)
            choices = view.questions.children[0].children[1]
            assert isinstance(choices, widgets.RadioButtons) and choices.value is None
            assert view.submit is not None
            view.submit.click()  # Blank is an error, never a recommendation vote.
            await asyncio.sleep(0)
            assert not question.done()
            choices.value = 0
            assert not question.done()  # Merely selecting does not submit either.
            view.submit.click()
            responses = await asyncio.wait_for(question, 2)
            assert responses[INTERRUPT["id"]].answers[0].selected_indices == [0]
            assert view.submit.disabled and view.leave.disabled
            assert service.resumes == service.submissions == 0

    asyncio.run(scenario())


def test_notebook_leave_waiting_and_cell_cancel_send_no_answer():
    async def scenario():
        service = StreamService()
        async with service.client() as client:
            view = NotebookView(client.session(operation_id="questions"))
            task = asyncio.create_task(view.ask(pending()))
            await asyncio.sleep(0)
            view.leave.click()
            assert await task is None
            task = asyncio.create_task(view.ask(pending()))
            await asyncio.sleep(0)
            task.cancel()
            with pytest.raises(asyncio.CancelledError):
                await task
            assert view.submit.disabled and view.leave.disabled
            assert service.submissions == service.resumes == 0

    asyncio.run(scenario())


def test_notebook_single_call_displays_progress_questions_resumes_and_returns_saved_answer():
    from test_research import REQUEST

    from epoch_sdk import RunRequest

    async def scenario():
        service = StreamService(questions=True)
        async with service.client() as client:
            view = NotebookView(
                client.session(RunRequest.model_validate(REQUEST), operation_id="notebook-one-call")
            )
            running = asyncio.create_task(view.run())
            async with asyncio.timeout(3):
                while view.pending_reply is None:
                    await asyncio.sleep(0)
            assert "Waiting for your reply" in view.progress.value
            view.questions.children[0].children[1].value = 0
            view.submit.click()
            result = await asyncio.wait_for(running, 3)
            assert isinstance(result, ResearchCompleted)
            assert result.response.version == 1 and view.status == "Answer published"
            assert service.submissions == service.resumes == 1

    asyncio.run(scenario())


def test_terminal_uses_async_coding_agent_choices_and_native_answer_indices():
    async def scenario():
        service = StreamService()
        output = StringIO()
        with create_pipe_input() as pipe, create_app_session(input=pipe, output=DummyOutput()):
            pipe.send_text("1\n")
            async with service.client() as client:
                view = TerminalView(
                    client.session(operation_id="questions"),
                    console=Console(file=output, width=100),
                )
                try:
                    responses = await view.ask(pending())
                finally:
                    view.live.stop()
            assert responses[INTERRUPT["id"]].answers[0].selected_indices == [0]
            assert pending().interrupts[0].ask_user().questions[0].question in output.getvalue()
            assert service.submissions == service.resumes == 0

    asyncio.run(scenario())


def test_high_level_headless_run_never_imports_human_views(monkeypatch):
    import sys

    from test_research import REQUEST

    from epoch_sdk import RunRequest

    monkeypatch.setitem(sys.modules, "epoch_sdk.notebook", None)
    monkeypatch.setitem(sys.modules, "epoch_sdk.terminal", None)

    async def scenario():
        service = StreamService(questions=True)
        async with service.client() as client:
            result = await client.run(
                RunRequest.model_validate(REQUEST), operation_id="headless", interface="headless"
            )
            assert isinstance(result, NeedsInput)
            assert service.resumes == 0

    asyncio.run(scenario())
