"""Public MCP/SDK parity over native admission, streaming and saved operations."""

from __future__ import annotations

import asyncio
import copy

import pytest
from mcp import Client
from test_operation_reconnect import Service
from test_research import REQUEST
from test_session import StreamService
from test_supervisor import INTERRUPT, clients, published

from epoch_sdk.mcp import _result, create_server
from epoch_sdk.supervisor import NoExecution, PublishedAnswer


def test_public_surface_has_five_tools_and_task_is_the_only_required_run_field():
    async def scenario():
        service = StreamService()
        async with service.client() as sdk, Client(create_server(sdk)) as mcp:
            tools = {tool.name: tool for tool in (await mcp.list_tools()).tools}
            assert set(tools) == {
                "epoch_run",
                "epoch_execute",
                "epoch_resume",
                "epoch_status",
                "epoch_read",
            }
            assert tools["epoch_run"].input_schema["required"] == ["task"]
            assert all(
                tool.input_schema["additionalProperties"] is False for tool in tools.values()
            )
            assert "ctx" not in tools["epoch_run"].input_schema["properties"]
            assert service.submissions == service.jobs == 0

    asyncio.run(scenario())


def test_unknown_task_fields_fail_before_any_service_work():
    async def scenario():
        service = StreamService()
        async with service.client() as sdk, Client(create_server(sdk)) as mcp:
            result = await mcp.call_tool("epoch_run", {"task": "Compare sales", "output": "json"})
            assert result.is_error
            assert "Unknown arguments: output" in result.content[0].text
            assert service.record is None and service.submissions == 0 and service.graph_calls == []

    asyncio.run(scenario())


@pytest.mark.parametrize("keyed", [False, True])
def test_task_only_run_always_uses_the_published_session_path(keyed):
    async def scenario():
        service = StreamService()
        service.response["content"]["outputs"] = [
            {"name": "answer", "type": "text", "format": "markdown", "value": "The saved answer."}
        ]
        args = {"task": REQUEST["task"]}
        if keyed:
            args["operation_id"] = "task-only"
        async with service.client() as sdk, Client(create_server(sdk)) as mcp:
            result = await mcp.call_tool("epoch_run", args)
            assert not result.is_error
            wire = result.structured_content
            assert wire["status"] == "succeeded" and wire["operation_id"]
            assert wire["response"]["content"]["outputs"][0]["value"] == "The saved answer."
            assert service.record["request"]["outputs"][0]["type"] == "text"
            assert service.record["request"]["outputs"][0]["format"] == "markdown"
            assert service.streams == service.submissions == 1
            before = len(service.graph_calls)
            observed = await mcp.call_tool("epoch_status", {"operation_id": wire["operation_id"]})
            assert observed.structured_content == wire
            assert len(service.graph_calls) == before

    asyncio.run(scenario())


def test_run_reconnects_with_the_same_inputs_and_preserves_named_json_outputs():
    async def scenario():
        service = StreamService()
        async with service.client() as sdk, Client(create_server(sdk)) as mcp:
            args = {**REQUEST, "operation_id": "same-operation"}
            first = await mcp.call_tool("epoch_run", args)
            again = await mcp.call_tool("epoch_run", args)
            assert not first.is_error and again.structured_content == first.structured_content
            assert first.structured_content["response"]["content"]["outputs"][0]["value"] == {
                "rows": 2
            }
            assert service.submissions == 1
            changed = await mcp.call_tool("epoch_run", {**args, "task": "Different task"})
            assert changed.structured_content["error"]["code"] == "IDEMPOTENCY_CONFLICT"
            assert service.submissions == 1

    asyncio.run(scenario())


def test_fresh_mcp_resumes_by_operation_id_without_copying_the_checkpoint():
    async def scenario():
        service = StreamService(questions=True)
        async with service.client() as sdk, Client(create_server(sdk)) as first:
            pending = await first.call_tool("epoch_run", {**REQUEST, "operation_id": "questions"})
            assert pending.structured_content["status"] == "needs_input"
            thread = pending.structured_content["handle"]["thread_id"]
            assert service.resumes == 0
        async with service.client() as sdk, Client(create_server(sdk)) as second:
            invalid = await second.call_tool(
                "epoch_resume",
                {
                    "operation_id": "questions",
                    "responses": {
                        INTERRUPT["id"]: {
                            "answers": [{"question_index": 0, "selected_indices": [99]}]
                        }
                    },
                },
            )
            assert invalid.structured_content["error"]["code"] == "INVALID_STATE"
            assert service.resumes == 0
            complete = await second.call_tool(
                "epoch_resume",
                {
                    "operation_id": "questions",
                    "responses": {
                        INTERRUPT["id"]: {
                            "answers": [{"question_index": 0, "selected_indices": [0]}]
                        }
                    },
                },
            )
            assert not complete.is_error and complete.structured_content["status"] == "succeeded"
            assert complete.structured_content["response"]["thread_id"] == thread
            assert service.resumes == service.submissions == 1

    asyncio.run(scenario())


def test_execute_and_its_status_use_backend_without_a_supervisor():
    async def scenario():
        service = Service()
        async with service.client() as sdk, Client(create_server(sdk)) as mcp:
            value = await mcp.call_tool(
                "epoch_execute",
                {
                    "reference": {"study_id": "study-one", "source_execution_id": "new"},
                    "period": {"start": "2025-01-01", "end": "2025-12-31"},
                    "operation_id": "prepared",
                },
            )
            assert not value.is_error
            assert value.structured_content["execution"]["status"] == "completed"
            status = await mcp.call_tool(
                "epoch_status", {"operation_id": "prepared", "kind": "execute"}
            )
            assert status.structured_content == value.structured_content
            assert service.jobs == 1 and service.graph_calls == []

    asyncio.run(scenario())


@pytest.mark.parametrize(
    "name",
    [
        "epoch_research",
        "epoch_research_status",
        "epoch_resume_research",
        "epoch_execute_saved",
        "epoch_execution",
        "epoch_execution_operation",
        "epoch_outputs",
        "epoch_publish_response",
        "epoch_response",
        "epoch_response_table",
    ],
)
def test_retired_tools_are_not_callable(name):
    async def scenario():
        service = StreamService()
        async with service.client() as sdk, Client(create_server(sdk)) as mcp:
            result = await mcp.call_tool(name, {})
            assert result.is_error
            assert service.submissions == service.jobs == 0 and service.graph_calls == []

    asyncio.run(scenario())


@pytest.mark.parametrize("kind", ["execution-free-answer", "publication-error"])
def test_transport_preserves_closed_publication_metadata_without_checkpoint_nulls(kind):
    async def scenario():
        state = (
            {
                "published_response": {
                    **published("unused"),
                    "primary_execution_id": None,
                    "study_id": None,
                }
            }
            if kind == "execution-free-answer"
            else {
                "publication_error": {
                    "code": "TEMPORARILY_UNAVAILABLE",
                    "message": "Publication was not confirmed.",
                    "retryable": False,
                    "gaps": None,
                    "questions": None,
                }
            }
        )
        async with clients([copy.deepcopy(state)]) as (sdk, _, _):
            wire = _result(await sdk.run("A brief answer")).structured_content
            if kind == "execution-free-answer":
                parsed = PublishedAnswer.model_validate(wire)
                assert parsed.response.primary_execution_id is None
                assert (
                    "primary_execution_id" not in wire["response"]
                    and "study_id" not in wire["response"]
                )
            else:
                parsed = NoExecution.model_validate(wire)
                assert parsed.publication_error.code == "TEMPORARILY_UNAVAILABLE"
                assert "gaps" not in wire["publication_error"]

    asyncio.run(scenario())
