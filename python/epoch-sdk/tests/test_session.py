"""Native client/SSE boundary proofs. These are not live market-data acceptance."""

from __future__ import annotations

import asyncio
import copy
import json
import sys
from pathlib import Path

import httpx
import pytest
from mcp import Client
from pydantic import TypeAdapter, ValidationError
from test_operation_reconnect import Service
from test_research import REQUEST, REQUEST_ID
from test_supervisor import INTERRUPT, RUN

from epoch_sdk import RunRequest
from epoch_sdk.mcp import create_server
from epoch_sdk.presentation import question_answer
from epoch_sdk.research import ResearchCompleted, ResearchError
from epoch_sdk.session import (
    SessionCompleted,
    SessionEvent,
    SessionUI,
    SessionUIRemoved,
)
from epoch_sdk.supervisor import Answer, Answers, NeedsInput

RESUMED_RUN = "01900000-0000-7000-8000-000000000002"


def ui(status="active", *, id="phase-one", merge=False):
    return {
        "type": "ui",
        "id": id,
        "name": "build_study_phase",
        "props": {"phase": "building", "status": status, "label": "Build study"},
        "metadata": {"message_id": "bot-one", "merge": merge},
    }


class NativeRunStream(httpx.AsyncByteStream):
    def __init__(self, service):
        self.service = service

    async def __aiter__(self):
        self.service.waiting.set()
        self.service.streams += 1
        if self.service.hold:
            await self.service.release.wait()
        for kind, data in self.service.frames:
            yield ("event: " + kind + "\ndata: " + json.dumps(data) + "\n\n").encode()
        if self.service.transport_error:
            raise httpx.ReadTimeout("Fixture observation ended")
        if self.service.terminal_error:
            self.service.graph_status = "error"
            yield b'event: error\ndata: {"message":"Native execution failed"}\n\n'
            return
        if self.service.questions and self.service.resumes == 0:
            self.service.snapshot["interrupts"] = [copy.deepcopy(INTERRUPT)]
            self.service.graph_status = "interrupted"
        else:
            self.service.complete()
        yield b"event: end\ndata: {}\n\n"

    async def aclose(self):
        self.service.closed_streams += 1


class StreamService(Service):
    def __init__(self, *, questions=False, hold=False):
        super().__init__()
        self.questions = questions
        self.hold = hold
        self.resumes = 0
        self.streams = 0
        self.closed_streams = 0
        self.transport_error = False
        self.terminal_error = False
        self.frames = []
        self.snapshot["values"].update(
            messages=[{"role": "user", "id": REQUEST_ID}, {"type": "ai", "id": "bot-one"}],
            ui=[],
        )

    def complete(self):
        self.response["thread_id"] = self.record["runtime"]["thread_id"]
        super().complete()

    async def graph(self, request):
        path = request.url.path
        if path.endswith("/stream"):
            self.graph_calls.append(request)
            assert request.url.params["cancel_on_disconnect"] == "false"
            return httpx.Response(
                200, headers={"content-type": "text/event-stream"}, stream=NativeRunStream(self)
            )
        if path.endswith("/runs") and request.method == "POST":
            body = json.loads(request.content)
            assert body["stream_mode"] == ["values", "custom"]
            assert body["stream_subgraphs"] is True
            assert body["stream_resumable"] is True
            if "command" in body:
                self.graph_calls.append(request)
                assert "input" not in body
                submitted = Answers.model_validate(body["command"]["resume"][INTERRUPT["id"]])
                assert submitted.answers == [Answer(question_index=0, selected_indices=[0])]
                self.resumes += 1
                self.graph_status = "running"
                self.record["phase"] = "active"
                self.record["graph_run_id"] = RESUMED_RUN
                self.snapshot["interrupts"] = []
                return httpx.Response(
                    200,
                    json={"run_id": RESUMED_RUN, "thread_id": self.record["runtime"]["thread_id"]},
                )
        if path.endswith("/history"):
            self.graph_calls.append(request)
            body = json.loads(request.content)
            assert body["metadata"] == {
                "epoch_sdk_request_id": REQUEST_ID,
                "epoch_sdk_run_id": self.record["graph_run_id"],
            }
            return httpx.Response(200, json=[self.snapshot])
        return await super().graph(request)


def test_session_uses_native_ui_replacement_merge_removal_and_nested_events():
    async def scenario():
        service = StreamService()
        active = ui()
        service.snapshot["values"]["ui"] = [active]
        merged = ui("completed", merge=True)
        merged["props"] = {"status": "completed"}
        extension = {
            "type": "ui",
            "id": "source",
            "name": "source_coverage",
            "props": {"labels": ["MSFT"], "rows": 3},
            "metadata": {},
        }
        service.frames = [
            ("custom", active),
            ("values", copy.deepcopy(service.snapshot["values"])),
            ("custom|delegate:one", active),
            ("custom", merged),
            ("custom|delegate:one", extension),
            ("custom", {"type": "remove-ui", "id": "source"}),
            ("messages-tuple", [{"type": "AIMessageChunk", "content": "Unpublished draft"}, {}]),
        ]
        async with service.client() as client:
            events = [
                event
                async for event in client.session(
                    RunRequest.model_validate(REQUEST), operation_id="same-research"
                ).events()
            ]
        phase = [
            event
            for event in events
            if isinstance(event, SessionUI) and event.message.id == "phase-one"
        ]
        assert len(phase) == 2
        assert phase[-1].message.props == {**active["props"], "status": "completed"}
        assert [
            event.message.props
            for event in events
            if isinstance(event, SessionUI) and event.message.id == "source"
        ] == [extension["props"]]
        assert len([event for event in events if isinstance(event, SessionUIRemoved)]) == 1
        assert isinstance(events[-1], SessionCompleted)
        assert events[-1].result.response.version == 1
        assert "Unpublished draft" not in repr(events)
        assert service.submissions == 1 and service.closed_streams == 1

    asyncio.run(scenario())


@pytest.mark.parametrize("mcp", [False, True])
def test_questions_remain_structured_and_explicit_replies_resume_same_operation(mcp):
    async def scenario():
        service = StreamService(questions=True)
        async with service.client() as client:
            if mcp:
                async with Client(create_server(client.supervisor)) as caller:
                    pending = await caller.call_tool(
                        "epoch_research", {"request": REQUEST, "operation_id": "question-one"}
                    )
                    assert not pending.is_error
                    waiting = NeedsInput.model_validate(pending.structured_content)
                    assert service.resumes == 0
                    completed = await caller.call_tool(
                        "epoch_resume_research",
                        {
                            "waiting": waiting.model_dump(mode="json"),
                            "responses": {
                                INTERRUPT["id"]: {
                                    "answers": [{"question_index": 0, "selected_indices": [0]}]
                                }
                            },
                        },
                    )
                    assert not completed.is_error
                    result = ResearchCompleted.model_validate(completed.structured_content)
            else:
                session = client.session(
                    RunRequest.model_validate(REQUEST), operation_id="question-one"
                )
                waiting = await session.run()
                assert isinstance(waiting, NeedsInput) and service.resumes == 0
                await session.resume(
                    waiting,
                    {
                        INTERRUPT["id"]: Answers(
                            answers=[Answer(question_index=0, selected_indices=[0])]
                        )
                    },
                )
                result = await session.run()
            assert isinstance(result, ResearchCompleted)
            assert result.operation_id == "question-one"
            assert service.submissions == service.resumes == 1
            # Fresh clients read the exact pinned saved answer, with no new run.
            calls = len(service.graph_calls)
            again = await client.session(operation_id="question-one").run()
            assert again == result and len(service.graph_calls) == calls

    asyncio.run(scenario())


def test_mcp_reports_structured_progress_without_importing_human_renderers(monkeypatch):
    async def scenario():
        service = StreamService()
        service.frames = [("custom", ui())]
        progress = []

        async def notify(value, total, message):
            progress.append((value, total, json.loads(message)))

        # A headless MCP installation must not need either human UI dependency.
        monkeypatch.setitem(sys.modules, "epoch_sdk.notebook", None)
        monkeypatch.setitem(sys.modules, "epoch_sdk.terminal", None)
        async with service.client() as client, Client(create_server(client.supervisor)) as caller:
            tools = await caller.list_tools()
            assert (
                "ctx"
                not in next(
                    tool for tool in tools.tools if tool.name == "epoch_research"
                ).input_schema["properties"]
            )
            result = await caller.call_tool(
                "epoch_research",
                {"request": REQUEST, "operation_id": "mcp-stream"},
                progress_callback=notify,
            )
        assert not result.is_error
        assert [item[2]["event"] for item in progress] == ["status", "ui"]
        assert progress[-1][2]["message"]["id"] == "phase-one"
        assert all(item[1] is None for item in progress)
        assert "\x1b" not in result.content[0].text
        assert service.submissions == 1

    asyncio.run(scenario())


def test_stopping_the_observer_does_not_cancel_native_work_and_fresh_client_reconnects():
    async def scenario():
        service = StreamService(hold=True)
        async with service.client() as client:
            observer = asyncio.create_task(
                client.session(
                    RunRequest.model_validate(REQUEST), operation_id="notebook-disconnected"
                ).run()
            )
            await asyncio.wait_for(service.waiting.wait(), 3)
            observer.cancel()
            with pytest.raises(asyncio.CancelledError):
                await observer
        assert service.closed_streams == 1
        assert all(
            "/cancel" not in str(call.url) and call.method != "DELETE"
            for call in service.graph_calls
        )
        service.complete()
        async with service.client() as fresh:
            result = await fresh.session(operation_id="notebook-disconnected").run()
        assert isinstance(result, ResearchCompleted) and service.submissions == 1

    asyncio.run(scenario())


@pytest.mark.parametrize(
    "reply,indices,text",
    [
        ("1", [0], None),
        (
            "Use fiscal years and keep the original sources",
            [],
            "Use fiscal years and keep the original sources",
        ),
        ("/skip", [], None),
    ],
)
def test_human_replies_use_native_indices_or_plain_language(reply, indices, text):
    from epoch_sdk.supervisor import GraphInterrupt

    question = GraphInterrupt.model_validate(INTERRUPT).ask_user().questions[0]
    result = question_answer(question, 0, reply)
    assert result.selected_indices == indices and result.free_form_input == text


@pytest.mark.parametrize("reply", ["", "  ", "0", "999", "1,1"])
def test_human_reply_does_not_silently_select_recommendations(reply):
    from epoch_sdk.supervisor import GraphInterrupt

    question = GraphInterrupt.model_validate(INTERRUPT).ask_user().questions[0]
    with pytest.raises(ValueError):
        question_answer(question, 0, reply)


def test_later_query_ui_does_not_leak_into_an_earlier_session():
    from epoch_sdk.supervisor import WorkflowHandle

    async def scenario():
        service = StreamService()
        async with service.client() as client:
            session = client.session(operation_id="earlier")
            raw = {"authority_turn_id": "user-turn:later", "ui": [ui()]}
            handle = WorkflowHandle(
                thread_id="thread", request_id=REQUEST_ID, assistant_id="epoch-ai", run_id=RUN
            )
            assert session._state_ui(raw, handle) == []

    asyncio.run(scenario())


def test_stream_observation_failure_preserves_live_operation_and_request_identity():
    async def scenario():
        service = StreamService()
        service.transport_error = True
        async with service.client() as client:
            with pytest.raises(ResearchError) as raised:
                await client.session(
                    RunRequest.model_validate(REQUEST), operation_id="interrupted-view"
                ).run()
            assert raised.value.request_id == REQUEST_ID
            assert raised.value.error.code == "TEMPORARILY_UNAVAILABLE"
            assert service.graph_status == "running" and "error" not in service.record
        service.complete()
        async with service.client() as client:
            assert isinstance(
                await client.session(operation_id="interrupted-view").run(), ResearchCompleted
            )
        assert service.submissions == 1

    asyncio.run(scenario())


def test_native_run_record_owns_the_terminal_failure_after_an_sse_error():
    async def scenario():
        service = StreamService()
        service.terminal_error = True
        async with service.client() as client:
            with pytest.raises(ResearchError) as raised:
                await client.session(
                    RunRequest.model_validate(REQUEST), operation_id="failed-run"
                ).run()
            assert raised.value.error.code == "EXECUTION_FAILED"
            assert service.record["phase"] == "failed"
            assert "response_version" not in service.record
            assert any(call.url.path.endswith("/runs/" + RUN) for call in service.graph_calls)
        assert service.submissions == 1

    asyncio.run(scenario())


@pytest.mark.parametrize(
    "fixture",
    json.loads(
        (Path(__file__).resolve().parents[3] / "contracts/research-session.cases.json").read_text()
    ),
    ids=lambda fixture: fixture["name"],
)
def test_python_session_events_match_language_neutral_fixtures(fixture):
    adapter = TypeAdapter(SessionEvent)
    if fixture["valid"]:
        adapter.validate_python(fixture["value"])
    else:
        with pytest.raises(ValidationError):
            adapter.validate_python(fixture["value"])
