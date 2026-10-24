from __future__ import annotations

import asyncio
import copy
import json
from contextlib import asynccontextmanager
from datetime import date
from pathlib import Path

import httpx
import pytest
from jsonschema import Draft202012Validator
from langgraph_sdk.client import LangGraphClient
from stratifyx import AsyncStratifyX, DatePeriodConfig
from stratifyx.core.api_error import ApiError

from epoch_sdk.supervisor import (
    Answer,
    Answers,
    AskUser,
    InProgress,
    NeedsInput,
    NoExecution,
    PublishedAnswer,
    SavedStudy,
    SupervisorClient,
)

ROOT = Path(__file__).resolve().parents[3]

THREAD = "11111111-1111-4111-8111-111111111111"
RUN = "22222222-2222-4222-8222-222222222222"
INTERRUPT = {
    "id": "interrupt-one",
    "value": {
        "type": "ask_user",
        "tool_call_id": "ask-one",
        "questions": [
            {
                "question": "Which period?",
                "description": "Choose the analysis window.",
                "multi_select": False,
                "options": [
                    {"label": "2024", "recommended": True},
                    {"label": "2025", "recommended": False},
                ],
            }
        ],
    },
}


def test_sdk_interrupt_and_answer_models_agree_with_the_supervisors_owned_wire() -> None:
    snapshot = json.loads((ROOT / "contracts/supervisor-native.schema.json").read_text())

    def shape(node: object, root: dict) -> object:
        if isinstance(node, list):
            return [shape(value, root) for value in node]
        if not isinstance(node, dict):
            return node
        if "$ref" in node:
            return shape(root["$defs"][node["$ref"].rsplit("/", 1)[-1]], root)
        # Titles/default annotations are language-specific. The SDK is deliberately
        # closed even where the supervisor's output TypedDict permits extensions.
        return {
            key: {name: shape(field, root) for name, field in value.items()}
            if key == "properties"
            else shape(value, root)
            for key, value in node.items()
            if key not in {"$defs", "title", "description", "default", "additionalProperties"}
        }

    for model, name in [(AskUser, "AskUser"), (Answers, "Answers")]:
        owned = snapshot["schemas"][name]
        local = model.model_json_schema()
        assert shape(local, local) == shape(owned, owned)
    Draft202012Validator(snapshot["schemas"]["AskUser"]).validate(
        AskUser.model_validate(INTERRUPT["value"]).model_dump(mode="json")
    )
    Draft202012Validator(snapshot["schemas"]["Answers"]).validate(
        Answers(answers=[Answer(question_index=0, free_form_input="Use 2025")]).model_dump(
            mode="json"
        )
    )


def test_feedback_includes_the_question_context_options_and_conversation_link() -> None:
    async def scenario() -> None:
        async with clients([{"__interrupt__": [INTERRUPT]}]) as (client, _, _):
            waiting = await client.run("Compare sales")
            assert isinstance(waiting, NeedsInput)
            assert waiting.feedback() == (
                "The workflow is waiting for input.\nWhich period?\n"
                "Choose the analysis window.\n1. 2024 (recommended)\n2. 2025\n"
                f"Continue: https://epoch.invalid/?tab=chat&threadId={THREAD}"
            )

    asyncio.run(scenario())


def test_missing_answer_rows_are_rejected_before_the_native_resume_call() -> None:
    async def scenario() -> None:
        async with clients([{"__interrupt__": [INTERRUPT]}]) as (client, calls, _):
            waiting = await client.run("Compare sales")
            assert isinstance(waiting, NeedsInput)
            count = len(calls)
            with pytest.raises(ValueError, match="every question"):
                await client.resume(waiting, {"interrupt-one": Answers(answers=[])})
            assert len(calls) == count

    asyncio.run(scenario())


def job(identifier: str, *, status: str = "completed", definition_id: str = "study-one") -> dict:
    return {
        "id": identifier,
        "definition_id": definition_id,
        "created_at": 1,
        "execution_type": "research",
        "status": status,
        "thread_id": THREAD,
    }


def outcome(identifier: str | None, status: str = "completed", tool: str = "run_study") -> dict:
    return {
        "tool_call_id": "tool-one",
        "tool_name": tool,
        "subject": "sales",
        "status": status,
        "detail": "Selected outcome",
        "execution_id": identifier,
    }


def published(execution: str, request_id: str = "$current") -> dict:
    return {
        "response_id": "rsp_" + "1" * 64,
        "request_id": request_id,
        "thread_id": THREAD,
        "version": 1,
        "primary_execution_id": execution,
        "study_id": "study-one",
    }


@asynccontextmanager
async def clients(
    replies: list[dict],
    *,
    before: dict | None = None,
    backend_jobs: dict | None = None,
    origin: str = "agent",
    backend_study_status: int = 200,
    observed: dict | None = None,
    thread_status: str = "idle",
    pending_nodes: list[str] | None = None,
):
    """Actual native clients over simulated transports; no sockets or agent calls."""
    graph_calls: list[httpx.Request] = []
    backend_calls: list[httpx.Request] = []
    pending = copy.deepcopy(replies)
    jobs = backend_jobs or {}
    active_request = ""

    def graph(request: httpx.Request) -> httpx.Response:
        nonlocal active_request
        graph_calls.append(request)
        if request.method == "POST" and request.url.path == "/threads":
            return httpx.Response(200, json={"thread_id": THREAD})
        if request.method == "GET" and request.url.path == f"/threads/{THREAD}/state":
            return httpx.Response(
                200,
                json={
                    "values": observed if observed is not None else before or {},
                    "interrupts": (observed or {}).get("__interrupt__", []),
                    "next": pending_nodes or [],
                },
            )
        if request.method == "GET" and request.url.path == f"/threads/{THREAD}":
            return httpx.Response(200, json={"thread_id": THREAD, "status": thread_status})
        if request.method == "POST" and request.url.path == f"/threads/{THREAD}/runs/wait":
            body = json.loads(request.content)
            if "input" in body:
                active_request = body["input"]["messages"][0]["id"]
            reply = pending.pop(0)
            if reply.get("published_response", {}).get("request_id") == "$current":
                reply["published_response"]["request_id"] = active_request
            return httpx.Response(
                200,
                json=reply,
                headers={"Content-Location": f"/threads/{THREAD}/runs/{RUN}"},
            )
        raise AssertionError(f"Unexpected graph call: {request.method} {request.url.path}")

    def backend(request: httpx.Request) -> httpx.Response:
        backend_calls.append(request)
        path = request.url.path
        if request.method == "GET" and path.startswith("/api/v1/studies/executions/"):
            identifier = path.rsplit("/", 1)[-1]
            return httpx.Response(200, json=jobs.get(identifier, job(identifier)))
        if request.method == "GET" and path == "/api/v1/studies/definitions/study-one":
            if backend_study_status != 200:
                return httpx.Response(
                    backend_study_status,
                    json={
                        "error": "DataNotFound",
                        "message": "Not found",
                        "timestamp": "2026-10-18T00:00:00Z",
                    },
                )
            return httpx.Response(
                200,
                json={
                    "name": "Saved analysis",
                    "description": "Approved task",
                    "source": "immutable study source",
                    "data": {"assets": []},
                    "authoring_origin": origin,
                },
            )
        if request.method == "POST" and path == "/api/v1/studies/executions":
            return httpx.Response(
                200, json={"id": "fresh-execution", "message": "Execution accepted"}
            )
        raise AssertionError(f"Unexpected Backend call: {request.method} {path}")

    async with (
        httpx.AsyncClient(
            base_url="https://graph.invalid", transport=httpx.MockTransport(graph)
        ) as graph_http,
        httpx.AsyncClient(transport=httpx.MockTransport(backend)) as backend_http,
    ):
        client = SupervisorClient(
            LangGraphClient(graph_http),
            AsyncStratifyX(
                base_url="https://backend.invalid",
                token="fixture-only",
                httpx_client=backend_http,
            ),
            ui_url="https://epoch.invalid/?tab=chat",
        )
        yield client, graph_calls, backend_calls


def test_interrupt_answers_resume_the_same_thread_without_repeating_the_task() -> None:
    async def scenario() -> None:
        replies = [
            {"execution_ids": ["old"], "__interrupt__": [INTERRUPT]},
            {"execution_ids": ["old", "new"], "published_response": published("new")},
        ]
        async with clients(replies, before={"execution_ids": ["old"]}) as (
            client,
            graph_calls,
            backend_calls,
        ):
            waiting = await client.run("Compare sales", thread_id=THREAD)
            assert isinstance(waiting, NeedsInput)
            assert waiting.handle.run_id == RUN
            assert waiting.conversation_url == f"https://epoch.invalid/?tab=chat&threadId={THREAD}"
            assert backend_calls == []
            assert waiting.interrupts[0].ask_user().questions[0].options[0].recommended
            final = await client.resume(
                waiting,
                {
                    "interrupt-one": Answers(
                        answers=[Answer(question_index=0, selected_indices=[1])]
                    )
                },
            )
            assert isinstance(final, PublishedAnswer)
            assert final.response.primary_execution_id == "new"
            assert final.handle is not None
            assert final.handle.request_id == waiting.handle.request_id
            assert final.response.study_id == "study-one"
            waits = [
                json.loads(call.content)
                for call in graph_calls
                if call.url.path.endswith("/runs/wait")
            ]
            assert waits[0]["input"]["messages"][0]["content"] == "Compare sales"
            assert "input" not in waits[1]
            assert waits[1]["command"]["resume"] == {
                "interrupt-one": {"answers": [{"question_index": 0, "selected_indices": [1]}]}
            }
            assert all(call["durability"] == "sync" for call in waits)
            assert not any(call.method == "DELETE" for call in graph_calls)

    asyncio.run(scenario())


def test_execution_order_alone_never_selects_a_primary_answer() -> None:
    async def scenario() -> None:
        async with clients([{"execution_ids": ["first", "last"]}]) as (
            client,
            graph_calls,
            backend_calls,
        ):
            result = await client.run("Build the requested study")
            assert isinstance(result, NoExecution)
            assert result.publication_failed
            assert len([call for call in graph_calls if call.url.path == "/threads"]) == 1
            assert len(backend_calls) == 0

    asyncio.run(scenario())


def test_checkpoint_default_null_reference_fields_allow_an_execution_free_answer() -> None:
    async def scenario() -> None:
        reference = {**published("unused"), "primary_execution_id": None, "study_id": None}
        async with clients([{"published_response": reference}]) as (client, _, backend_calls):
            result = await client.run("A brief explanation")
            assert isinstance(result, PublishedAnswer)
            assert result.response.primary_execution_id is None
            assert result.response.study_id is None
            assert not backend_calls

    asyncio.run(scenario())


@pytest.mark.parametrize("invalid", [{"response_id": None}, {"study_id": "study-one"}])
def test_checkpoint_null_normalization_keeps_required_and_paired_source_validation(invalid) -> None:
    async def scenario() -> None:
        reference = {
            **published("unused"),
            "primary_execution_id": None,
            "study_id": None,
            **invalid,
        }
        async with clients([{"published_response": reference}]) as (client, _, _):
            with pytest.raises(ValueError):
                await client.run("A brief explanation")

    asyncio.run(scenario())


def test_a_second_clarification_round_preserves_its_updated_questions_and_request() -> None:
    async def scenario() -> None:
        second_interrupt = copy.deepcopy(INTERRUPT)
        second_interrupt["value"]["tool_call_id"] = "ask-two"
        second_interrupt["value"]["questions"][0]["question"] = "Which comparison?"
        second_interrupt["value"]["questions"][0]["options"] = [
            {"label": "Revenue", "recommended": False},
            {"label": "Margin", "recommended": True},
        ]
        replies = [
            {"__interrupt__": [INTERRUPT]},
            {"__interrupt__": [second_interrupt]},
            {"execution_ids": ["final"], "published_response": published("final")},
        ]
        async with clients(replies) as (client, calls, _):
            first = await client.run("Compare sales")
            assert isinstance(first, NeedsInput)
            second = await client.resume(
                first,
                {
                    "interrupt-one": Answers(
                        answers=[Answer(question_index=0, selected_indices=[0])]
                    )
                },
            )
            assert isinstance(second, NeedsInput)
            assert "Which comparison?" in second.feedback()
            assert "Margin (recommended)" in second.feedback()
            assert second.handle.request_id == first.handle.request_id
            # Do not deduplicate a later round merely because an interrupt ID
            # repeats. Resume the currently returned questions and checkpoint.
            restored = NeedsInput.model_validate_json(second.model_dump_json())
            result = await client.resume(
                restored,
                {
                    "interrupt-one": Answers(
                        answers=[Answer(question_index=0, selected_indices=[1])]
                    )
                },
            )
            assert isinstance(result, PublishedAnswer)
            assert result.response.primary_execution_id == "final"
            submissions = [json.loads(call.content) for call in calls if call.method == "POST"]
            assert len([item for item in submissions if "input" in item]) == 1
            assert len([item for item in submissions if "command" in item]) == 2

    asyncio.run(scenario())


def test_no_new_execution_never_returns_an_old_success() -> None:
    async def scenario() -> None:
        async with clients(
            [
                {
                    "execution_ids": ["old"],
                    "messages": [{"role": "assistant", "content": "Data is unavailable."}],
                }
            ],
            before={"execution_ids": ["old"]},
        ) as (client, _, backend_calls):
            result = await client.run("A new task", thread_id=THREAD)
            assert isinstance(result, NoExecution)
            assert not result.publication_failed
            assert result.reply == "Data is unavailable." and result.execution_id is None
            assert backend_calls == []

    asyncio.run(scenario())


def test_fresh_client_reads_the_result_after_a_human_resumes_in_the_ui() -> None:
    async def scenario() -> None:
        async with clients([{"execution_ids": ["old"], "__interrupt__": [INTERRUPT]}]) as (
            first,
            _,
            _,
        ):
            waiting = await first.run("Compare sales")
            assert isinstance(waiting, NeedsInput)
            saved_handle = waiting.handle.model_dump_json()
        async with clients(
            [],
            observed={
                "execution_ids": ["old", "new"],
                "published_response": published("new", waiting.handle.request_id),
            },
        ) as (
            second,
            calls,
            _,
        ):
            result = await second.status(waiting.handle.model_validate_json(saved_handle))
            assert isinstance(result, PublishedAnswer)
            assert result.response.primary_execution_id == "new"
            assert all(call.method == "GET" for call in calls)
            # Read status first so completion between these reads cannot pair an
            # old partial checkpoint with a freshly idle thread status.
            assert [call.url.path for call in calls] == [
                f"/threads/{THREAD}",
                f"/threads/{THREAD}/state",
            ]

    asyncio.run(scenario())


@pytest.mark.parametrize("thread_status,pending_nodes", [("busy", []), ("idle", ["tools"])])
def test_status_does_not_select_partial_results_while_the_supervisor_is_running(
    thread_status: str, pending_nodes: list[str]
) -> None:
    async def scenario() -> None:
        async with clients([{"__interrupt__": [INTERRUPT]}]) as (first, _, _):
            waiting = await first.run("Compare sales")
            assert isinstance(waiting, NeedsInput)
        async with clients(
            [],
            observed={"execution_ids": ["partial"]},
            thread_status=thread_status,
            pending_nodes=pending_nodes,
        ) as (second, calls, backend_calls):
            result = await second.status(waiting.handle)
            assert isinstance(result, InProgress)
            assert backend_calls == []
            assert all(call.method == "GET" for call in calls)

    asyncio.run(scenario())


def test_status_returns_pending_questions_and_never_restarts_the_thread() -> None:
    async def scenario() -> None:
        async with clients([{"__interrupt__": [INTERRUPT]}]) as (first, _, _):
            waiting = await first.run("Compare sales")
            assert isinstance(waiting, NeedsInput)
        async with clients(
            [], observed={"__interrupt__": [INTERRUPT]}, thread_status="interrupted"
        ) as (second, calls, backend_calls):
            result = await second.status(waiting.handle)
            assert isinstance(result, NeedsInput)
            assert result.interrupts == waiting.interrupts
            assert backend_calls == []
            assert all(call.method == "GET" for call in calls)

    asyncio.run(scenario())


def test_status_does_not_present_a_graph_failure_as_a_successful_request() -> None:
    async def scenario() -> None:
        async with clients([{"__interrupt__": [INTERRUPT]}]) as (first, _, _):
            waiting = await first.run("Compare sales")
            assert isinstance(waiting, NeedsInput)
        async with clients([], observed={"execution_ids": ["earlier"]}, thread_status="error") as (
            second,
            _,
            backend_calls,
        ):
            result = await second.status(waiting.handle)
            assert isinstance(result, NoExecution)
            assert "failed" in result.reason
            assert backend_calls == []

    asyncio.run(scenario())


def test_status_rejects_a_handle_when_the_ui_has_moved_to_an_unrelated_task() -> None:
    async def scenario() -> None:
        async with clients([{"__interrupt__": [INTERRUPT]}]) as (first, _, _):
            waiting = await first.run("Compare sales")
            assert isinstance(waiting, NeedsInput)
        async with clients(
            [],
            observed={"execution_ids": ["unrelated"], "authority_turn_id": "user-turn:other"},
        ) as (second, calls, backend_calls):
            with pytest.raises(ValueError, match="another request"):
                await second.status(waiting.handle)
            assert backend_calls == []
            assert all(call.method == "GET" for call in calls)

    asyncio.run(scenario())


def test_latest_run_failure_without_an_execution_does_not_fall_back_to_earlier_run() -> None:
    async def scenario() -> None:
        values = {
            "execution_ids": ["earlier"],
            "next_action_outcomes": {
                "first": outcome("earlier"),
                "last": outcome(None, "not_started"),
            },
        }
        async with clients([values]) as (client, _, backend_calls):
            result = await client.run("Compare two studies")
            assert isinstance(result, NoExecution)
            assert backend_calls == []

    asyncio.run(scenario())


def test_latest_failed_execution_is_returned_with_its_actual_backend_status() -> None:
    async def scenario() -> None:
        values = {
            "execution_ids": ["earlier", "failed"],
            "next_action_outcomes": {
                "first": outcome("earlier"),
                "last": outcome("failed", "failed"),
            },
        }
        async with clients([values], backend_jobs={"failed": job("failed", status="failed")}) as (
            client,
            _,
            _,
        ):
            result = await client.run("Build and run")
            assert isinstance(result, NoExecution)
            assert result.execution_id == "failed"

    asyncio.run(scenario())


def test_reconnected_execution_can_be_chosen_from_current_outcomes() -> None:
    async def scenario() -> None:
        values = {
            "execution_ids": ["existing"],
            "next_action_outcomes": {"current": outcome("existing")},
            "published_response": published("existing"),
        }
        async with clients([values], before={"execution_ids": ["existing"]}) as (client, _, _):
            result = await client.run("Check the current execution", thread_id=THREAD)
            assert (
                isinstance(result, PublishedAnswer)
                and result.response.primary_execution_id == "existing"
            )

    asyncio.run(scenario())


def test_invalid_answers_do_not_change_the_pending_checkpoint() -> None:
    async def scenario() -> None:
        async with clients([{"__interrupt__": [INTERRUPT]}]) as (client, graph_calls, _):
            waiting = await client.run("Compare sales")
            assert isinstance(waiting, NeedsInput)
            count = len(graph_calls)
            for answers in [
                Answers(answers=[Answer(question_index=0, selected_indices=[9])]),
                Answers(answers=[Answer(question_index=0, selected_indices=[0, 1])]),
                Answers(answers=[Answer(question_index=2, selected_indices=[0])]),
                Answers(
                    answers=[Answer(question_index=0, selected_indices=[0], free_form_input="2025")]
                ),
            ]:
                with pytest.raises(ValueError):
                    await client.resume(waiting, {"interrupt-one": answers})
            with pytest.raises(ValueError):
                await client.resume(waiting, {})
            assert len(graph_calls) == count

    asyncio.run(scenario())


def test_saved_study_execution_uses_backend_without_any_supervisor_or_discovery_call() -> None:
    async def scenario() -> None:
        async with clients(
            [], backend_jobs={"fresh-execution": job("fresh-execution", status="queued")}
        ) as (client, graph_calls, backend_calls):
            result = await client.execute_saved(
                SavedStudy(study_id="study-one", source_execution_id="prior", thread_id=THREAD),
                period=DatePeriodConfig(start=date(2024, 1, 1), end=date(2024, 12, 31)),
            )
            assert graph_calls == []
            assert result.execution.id == "fresh-execution"
            assert result.execution.status.value == "queued"
            submitted = next(call for call in backend_calls if call.method == "POST")
            assert json.loads(submitted.content) == {
                "id": "study-one",
                "period": {"start": "2024-01-01", "end": "2024-12-31"},
                "thread_id": THREAD,
            }

    asyncio.run(scenario())


def test_mutable_saved_definition_is_not_silently_reused_as_the_frozen_version() -> None:
    async def scenario() -> None:
        async with clients([], origin="manual") as (client, graph_calls, backend_calls):
            with pytest.raises(ValueError, match="immutable"):
                await client.execute_saved(
                    SavedStudy(study_id="study-one", source_execution_id="prior"),
                    period=DatePeriodConfig(),
                )
            assert graph_calls == []
            assert not any(call.method == "POST" for call in backend_calls)

    asyncio.run(scenario())


def test_saved_study_owner_rejection_prevents_execution_submission() -> None:
    async def scenario() -> None:
        async with clients([], backend_study_status=404) as (client, graph_calls, backend_calls):
            with pytest.raises(ApiError) as failure:
                await client.execute_saved(
                    SavedStudy(study_id="study-one", source_execution_id="prior"),
                    period=DatePeriodConfig(),
                )
            assert failure.value.status_code == 404
            assert graph_calls == []
            assert not any(call.method == "POST" for call in backend_calls)

    asyncio.run(scenario())


def test_later_diagnostic_execution_does_not_replace_the_explicit_primary():
    async def scenario():
        async with clients(
            [{"execution_ids": ["main", "diagnostic"], "published_response": published("main")}]
        ) as (client, _, calls):
            result = await client.run("Explain the main result")
            assert isinstance(result, PublishedAnswer)
            assert result.response.primary_execution_id == "main"
            assert calls == []

    asyncio.run(scenario())


@pytest.mark.parametrize("content", ["The retained source uses annual statements.", [{"type": "text", "text": "The retained source uses annual statements."}]])
def test_normal_contextual_reply_does_not_require_an_execution_or_publication(content):
    async def scenario():
        async with clients([{"messages": [{"type": "human", "content": "Which source?"}, {"type": "ai", "content": content}]}]) as (client, _, backend_calls):
            result = await client.run("Which source?")
            assert isinstance(result, NoExecution)
            assert not result.publication_failed
            assert result.reply == "The retained source uses annual statements."
            assert not backend_calls
    asyncio.run(scenario())


def test_previous_turn_and_tool_call_prose_are_not_a_current_contextual_answer():
    async def scenario():
        async with clients([{"messages": [{"type": "ai", "content": "Old answer"}, {"type": "human", "content": "New question"},
                {"type": "ai", "content": "Calling a tool", "tool_calls": [{"id": "call", "name": "build_study", "args": {}}]}]}]) as (client, _, backend_calls):
            result = await client.run("New question")
            assert isinstance(result, NoExecution) and result.publication_failed
            assert not result.reply and not backend_calls
    asyncio.run(scenario())
