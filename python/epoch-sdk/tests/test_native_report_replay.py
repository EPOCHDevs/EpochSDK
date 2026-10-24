"""Real generated SDK/MCP over controlled native replay records.

These checks exercise transport and identity validation, not a live engine/model.
The child fixture originates in the native exporter; replay envelopes are controls.
"""

import asyncio
import copy
import json

import httpx
import pytest
from langgraph_sdk.client import LangGraphClient
from mcp import Client
from stratifyx import AsyncStratifyX
from test_agent_tools import CATALOG
from test_execution_extensions import ANSWER, PIN, RECORD

from epoch_sdk.agent_tools import AgentToolsClient
from epoch_sdk.errors import EpochError
from epoch_sdk.mcp import create_server
from epoch_sdk.research import EpochClient
from epoch_sdk.supervisor import ChosenExecution, SupervisorClient


def replay(*, answer=True):
    child = copy.deepcopy(RECORD)
    child["request"]["source_execution_id"] = "new-original"
    child["request"]["thread_id"] = ANSWER["thread_id"]
    child["extension_outputs"]["provenance"]["source_execution_id"] = "new-original"
    child["request"]["base_presentation"] = copy.deepcopy(PIN)
    child["extension_outputs"]["provenance"]["base_presentation"] = copy.deepcopy(PIN)
    response = copy.deepcopy(ANSWER)
    response["extension"] = copy.deepcopy(child["extension_outputs"]["provenance"])
    parent = {
        "request_id": "req_" + "c" * 32,
        "execution_id": "new-original",
        "request": {
            "operation_id": "source-with-report",
            "study_id": "original-study",
            "source_execution_id": "original",
            "parameters": {"period": {"start": "2024-01-01", "end": "2024-12-31"}},
            "report_template": {"request_id": "req_" + "d" * 32},
        },
        "phase": "active",
        "created_at_ms": 1,
        "response_phase": "outputs_recorded",
        "report_request_id": child["request_id"],
        "report_request": copy.deepcopy(child["request"]),
        "response_id": child["response_id"],
        "response_version": child["response_version"],
    }
    if not answer:
        for record in (parent, child, child["extension_outputs"]):
            record.pop("response_id", None)
            record.pop("response_version", None)
    return parent, child, response


class ReplayService:
    def __init__(self, parent, child, response):
        self.parent, self.child, self.response = parent, child, response
        self.calls, self.graph_calls = [], []

    def graph(self, request):
        self.graph_calls.append(request)
        assert request.method == "GET" and request.url.path == "/api/v1/agent-tools"
        return httpx.Response(200, json=CATALOG)

    def backend(self, request):
        self.calls.append(request)
        path = request.url.path
        if path == "/api/v1/integration/execution-requests":
            assert request.method == "POST"
            assert json.loads(request.content) == self.parent["request"]
            return httpx.Response(200, json=self.parent)
        assert request.method == "GET"
        if path == "/api/v1/integration/execution-requests/by-handle/source-with-report":
            return httpx.Response(200, json=self.parent)
        if path == f"/api/v1/integration/execution-requests/{self.child['request_id']}":
            return httpx.Response(200, json=self.child)
        if path == "/api/v1/studies/executions/new-original":
            return httpx.Response(
                200,
                json={
                    "id": "new-original",
                    "definition_id": "original-study",
                    "created_at": 1,
                    "execution_type": "research",
                    "status": "completed",
                },
            )
        assert path == f"/api/v1/research/responses/{self.response['response_id']}"
        assert request.url.params["version"] == "1"
        return httpx.Response(200, json=self.response)


@pytest.mark.parametrize("answer", [True, False])
def test_reconnect_preserves_separate_source_report_and_optional_answer_pins(answer):
    async def scenario():
        service = ReplayService(*replay(answer=answer))
        async with (
            httpx.AsyncClient(transport=httpx.MockTransport(service.backend)) as http,
            httpx.AsyncClient(
                base_url="https://graph.invalid", transport=httpx.MockTransport(service.graph)
            ) as graph_http,
        ):
            native = AsyncStratifyX(
                base_url="https://backend.invalid", token="fixture", httpx_client=http
            )
            client = EpochClient(SupervisorClient(LangGraphClient(graph_http), native))
            result = await client.execution_operation("source-with-report")
            assert isinstance(result, ChosenExecution)
            assert result.execution.id == "new-original" != result.report.execution_id
            assert result.report.extension_outputs.dashboards[0].presentation.edit_version == 0
            assert result.report.request == result.report.request.model_validate(
                service.parent["report_request"]
            )
            assert (result.response is not None) == answer
            assert result.reusable_study.source_execution_id == "new-original"
            assert result.reusable_study.report_template.request_id == "req_" + "d" * 32
            assert await client.execution_operation("source-with-report") == result
            assert all(request.method == "GET" for request in service.calls)
            assert not service.graph_calls

    asyncio.run(scenario())


@pytest.mark.parametrize(
    "change",
    [
        "child-pin",
        "parent-pin",
        "extension-only-pin",
        "version",
        "same-job",
        "source",
        "body",
        "base",
        "bindings",
        "recursive",
    ],
)
def test_report_read_rejects_corrupt_native_pins_including_dashboard_only(change):
    async def scenario():
        parent, child, response = replay(answer=change not in {"child-pin", "parent-pin", "extension-only-pin"})
        if change == "child-pin":
            child["response_id"] = ANSWER["response_id"]
        if change == "parent-pin":
            parent["response_id"] = ANSWER["response_id"]
        if change == "extension-only-pin":
            child["extension_outputs"].update(response_id=ANSWER["response_id"], response_version=1)
        if change == "version":
            child["extension_outputs"]["response_version"] = 2
        if change == "same-job":
            child["execution_id"] = parent["execution_id"]
            child["extension_outputs"]["provenance"]["execution_id"] = parent["execution_id"]
            response["primary_execution_id"] = parent["execution_id"]
            response["extension"]["execution_id"] = parent["execution_id"]
            for part in response["content"]["outputs"]:
                if part["type"] == "table":
                    part["source"]["execution_id"] = parent["execution_id"]
        if change == "source":
            child["extension_outputs"]["provenance"]["source_execution_id"] = "wrong"
        if change == "body":
            parent["report_request"]["study_id"] = "wrong"
        if change == "base":
            child["extension_outputs"]["provenance"]["base_presentation"]["edit_version"] = 1
        if change == "bindings":
            child["request"]["execution_parameter_bindings"] = {
                "threshold": {"type": "Integer", "value": "2"}
            }
            parent["report_request"] = copy.deepcopy(child["request"])
        if change == "recursive":
            child["request"]["report_template"] = {"request_id": "recursive"}
            parent["report_request"] = copy.deepcopy(child["request"])
        service = ReplayService(parent, child, response)
        async with (
            httpx.AsyncClient(transport=httpx.MockTransport(service.backend)) as http,
            httpx.AsyncClient(
                base_url="https://graph.invalid", transport=httpx.MockTransport(service.graph)
            ) as graph_http,
        ):
            client = EpochClient(
                SupervisorClient(
                    LangGraphClient(graph_http),
                    AsyncStratifyX(
                        base_url="https://backend.invalid", token="fixture", httpx_client=http
                    ),
                )
            )
            with pytest.raises(EpochError, match="report|Report"):
                await client.execution_operation("source-with-report")
            assert (
                all(request.method == "GET" for request in service.calls)
                and not service.graph_calls
            )

    asyncio.run(scenario())


def test_mcp_reuses_existing_execute_extension_contract_for_native_report_replay():
    async def scenario():
        service = ReplayService(*replay())
        async with (
            httpx.AsyncClient(transport=httpx.MockTransport(service.backend)) as http,
            httpx.AsyncClient(
                base_url="https://graph.invalid", transport=httpx.MockTransport(service.graph)
            ) as graph_http,
        ):
            tools = AgentToolsClient(
                LangGraphClient(graph_http),
                AsyncStratifyX(
                    base_url="https://backend.invalid", token="fixture", httpx_client=http
                ),
                graph_http,
            )
            async with Client(create_server(tools)) as mcp:
                listed = {tool.name for tool in (await mcp.list_tools()).tools}
                assert (
                    not {
                        "epoch_audit_run",
                        "epoch_publish_response",
                        "epoch_inspect_response_sources",
                        "epoch_edit_dashboard",
                    }
                    & listed
                )
                output = await mcp.call_tool(
                    "epoch_execute_extension", {"request": service.parent["request"]}
                )
                assert not output.is_error
                assert output.structured_content == service.parent
            assert sum(request.method == "POST" for request in service.calls) == 1
            assert all(request.method == "GET" for request in service.graph_calls)

    asyncio.run(scenario())
