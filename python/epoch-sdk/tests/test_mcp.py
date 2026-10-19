from __future__ import annotations

import asyncio

from mcp import Client
from test_supervisor import INTERRUPT, THREAD, clients, job

from epoch_sdk.mcp import create_server


def test_mcp_round_trip_keeps_the_pending_thread_and_resumes_via_the_sdk() -> None:
    async def scenario() -> None:
        replies = [
            {"execution_ids": ["old"], "__interrupt__": [INTERRUPT]},
            {"execution_ids": ["old", "new"]},
        ]
        async with (
            clients(replies, before={"execution_ids": ["old"]}) as (sdk, graph_calls, _),
            Client(create_server(sdk)) as mcp,
        ):
            tools = await mcp.list_tools()
            assert {tool.name for tool in tools.tools} == {
                "epoch_run",
                "epoch_resume",
                "epoch_execute_saved",
                "epoch_status",
                "epoch_outputs",
                "epoch_response",
                "epoch_publish_response",
                "epoch_response_table",
            }
            waiting = await mcp.call_tool(
                "epoch_run", {"task": "Compare sales", "thread_id": THREAD}
            )
            assert not waiting.is_error
            assert waiting.structured_content is not None
            assert waiting.structured_content["status"] == "needs_input"
            assert waiting.structured_content["handle"]["thread_id"] == THREAD
            feedback = "\n".join(item.text for item in waiting.content if item.type == "text")
            assert "Which period?" in feedback and "2024 (recommended)" in feedback
            result = await mcp.call_tool(
                "epoch_resume",
                {
                    "waiting": waiting.structured_content,
                    "responses": {
                        "interrupt-one": {
                            "answers": [{"question_index": 0, "selected_indices": [1]}]
                        }
                    },
                },
            )
            assert not result.is_error
            assert result.structured_content is not None
            assert result.structured_content["execution"]["id"] == "new"
            assert not any(call.method == "DELETE" for call in graph_calls)

    asyncio.run(scenario())


def test_mcp_reuses_a_saved_study_without_calling_the_supervisor() -> None:
    async def scenario() -> None:
        async with (
            clients(
                [], backend_jobs={"fresh-execution": job("fresh-execution", status="queued")}
            ) as (sdk, graph_calls, _),
            Client(create_server(sdk)) as mcp,
        ):
            result = await mcp.call_tool(
                "epoch_execute_saved",
                {
                    "reference": {
                        "study_id": "study-one",
                        "source_execution_id": "old",
                        "thread_id": THREAD,
                    },
                    "parameters": {"period": {"start": "2024-01-01", "end": "2024-12-31"}},
                },
            )
            assert not result.is_error
            assert result.structured_content is not None
            assert result.structured_content["execution"]["id"] == "fresh-execution"
            assert result.structured_content["execution"]["status"] == "queued"
            assert graph_calls == []

    asyncio.run(scenario())


def test_mcp_invalid_resume_is_a_tool_error_and_keeps_the_checkpoint() -> None:
    async def scenario() -> None:
        async with (
            clients([{"__interrupt__": [INTERRUPT]}]) as (sdk, graph_calls, _),
            Client(create_server(sdk)) as mcp,
        ):
            waiting = await mcp.call_tool("epoch_run", {"task": "Compare sales"})
            before = len(graph_calls)
            result = await mcp.call_tool(
                "epoch_resume",
                {
                    "waiting": waiting.structured_content,
                    "responses": {
                        "interrupt-one": {
                            "answers": [{"question_index": 0, "selected_indices": [99]}]
                        }
                    },
                },
            )
            assert result.is_error
            assert len(graph_calls) == before

    asyncio.run(scenario())


def test_mcp_reads_the_result_after_the_human_ui_resume_without_starting_a_run() -> None:
    async def scenario() -> None:
        async with (
            clients([{"__interrupt__": [INTERRUPT]}]) as (sdk, _, _),
            Client(create_server(sdk)) as first,
        ):
            waiting = await first.call_tool("epoch_run", {"task": "Compare sales"})
            assert waiting.structured_content is not None
            handle = waiting.structured_content["handle"]
        async with (
            clients([], observed={"execution_ids": ["from-ui"]}) as (sdk, calls, _),
            Client(create_server(sdk)) as second,
        ):
            result = await second.call_tool("epoch_status", {"handle": handle})
            assert not result.is_error
            assert result.structured_content is not None
            assert result.structured_content["execution"]["id"] == "from-ui"
            assert all(call.method == "GET" for call in calls)

    asyncio.run(scenario())
