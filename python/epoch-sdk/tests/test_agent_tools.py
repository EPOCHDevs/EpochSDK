"""Real native clients and MCP protocol over controlled service transports."""

import asyncio
import copy
import json
from contextlib import asynccontextmanager
from pathlib import Path

import httpx
import pytest
from jsonschema import Draft202012Validator
from langgraph_sdk.client import LangGraphClient
from mcp import Client
from stratifyx import AsyncStratifyX
from stratifyx.core.api_error import ApiError
from test_supervisor import INTERRUPT

from epoch_sdk.agent_tools import AgentToolsClient
from epoch_sdk.mcp import create_server

CATALOG = json.loads(
    (Path(__file__).resolve().parents[3] / "contracts/agent-tools-native.json").read_text()
)["catalog"]
WORKSPACE = "11111111-1111-4111-8111-111111111111"
RUN = "22222222-2222-4222-8222-222222222222"
STUDY = {
    "name": "Saved fixture",
    "description": "Explicit test data",
    "source": "fixture source",
    "data": {"assets": []},
    "authoring_origin": "agent",
}
ARGS = {
    "needs": [{"kind": "market", "description": "AAPL daily-price metadata"}],
    "history_scope": "metadata_only",
}
BUILD_ARGS = {"studies": [{"operation": "create", "slot_id": "aapl_review", "name": "AAPL Review",
    "form": "research", "authoring_brief": "Use the selected source.", "data_refs": [], "decision_refs": []}]}


class Service:
    def __init__(self):
        self.graph_calls = []
        self.backend_calls = []
        self.native_status = "running"
        self.messages = []
        self.metadata = {}
        self.study_registry = {}
        self.owner_denied = False

    def graph(self, request):
        self.graph_calls.append(request)
        path = request.url.path
        if path == "/api/v1/agent-tools":
            return httpx.Response(200, json=CATALOG)
        if path == "/threads" and request.method == "POST":
            assert json.loads(request.content)["metadata"] == {"epoch_tool_workspace": "v1"}
            return httpx.Response(200, json={"thread_id": WORKSPACE})
        if path == f"/threads/{WORKSPACE}" and request.method == "GET":
            return httpx.Response(
                200, json={"thread_id": WORKSPACE, "metadata": {"epoch_tool_workspace": "v1"}}
            )
        if path == f"/threads/{WORKSPACE}/runs" and request.method == "POST":
            data = json.loads(request.content)
            assert data["assistant_id"] == "epoch-tools"
            assert data["durability"] == "sync" and data["multitask_strategy"] == "reject"
            assert data["on_completion"] == "keep"
            assert set(data["input"]) == {"messages"}
            self.messages = data["input"]["messages"]
            assert len(self.messages[-1]["tool_calls"]) == 1
            assert "sdk_request_id" not in data["input"]
            self.metadata = data["metadata"]
            return httpx.Response(200, json={"run_id": RUN, "status": "running"})
        if path == f"/threads/{WORKSPACE}/runs/{RUN}":
            return httpx.Response(
                200, json={"run_id": RUN, "status": self.native_status, "metadata": self.metadata}
            )
        if path == f"/threads/{WORKSPACE}/state":
            call = self.messages[-1]["tool_calls"][0]
            return httpx.Response(
                200,
                json={
                    "values": {
                        "messages": [
                            *self.messages,
                            {
                                "type": "tool",
                                "tool_call_id": call["id"],
                                "name": call["name"],
                                "content": "Retained exact source references",
                                "artifact": {"saved": "native proof"},
                                "status": "success",
                            },
                        ],
                        "study_name_to_id": self.study_registry,
                        "run_name_to_id": {},
                    },
                    "interrupts": [],
                    "next": [],
                },
            )
        if path == "/threads/search":
            assert json.loads(request.content)["metadata"] == {"epoch_tool_workspace": "v1"}
            return httpx.Response(200, json=[{"thread_id": WORKSPACE}])
        raise AssertionError(f"Unexpected graph request: {request.method} {path}")

    def backend(self, request):
        self.backend_calls.append(request)
        path = request.url.path
        assert request.headers["Authorization"] == "Bearer fixture"
        if path == "/api/v1/studies/definitions/study-one":
            return httpx.Response(200, json=STUDY)
        if path == "/api/v1/studies/definitions":
            return httpx.Response(200, json=["study-one", "study-two"])
        if path == "/api/v1/studies/executions" and request.method == "GET":
            return httpx.Response(200, json=["execution-one"])
        if path == "/api/v1/studies/executions" and request.method == "POST":
            body = json.loads(request.content)
            assert body["id"] == "study-one" and body["period"]["start"] == "2024-01-01"
            assert "response_plan" not in body
            return httpx.Response(
                200, json={"id": "execution-one", "message": "Execution accepted"}
            )
        if path == "/api/v1/studies/executions/execution-one/study":
            if self.owner_denied:
                return httpx.Response(
                    404,
                    json={
                        "error": "DataNotFound",
                        "message": "Unavailable",
                        "timestamp": "2026-10-20T00:00:00Z",
                    },
                )
            return httpx.Response(
                200,
                json={
                    "execution_id": "execution-one",
                    "definition_id": "study-one",
                    "captured_at": 1,
                    "study": STUDY,
                },
            )
        if path == "/api/v1/studies/executions/execution-one":
            return httpx.Response(
                200,
                json={
                    "id": "execution-one",
                    "definition_id": "study-one",
                    "created_at": 1,
                    "execution_type": "research",
                    "status": "completed",
                },
            )
        raise AssertionError(f"Unexpected Backend request: {request.method} {path}")

    @asynccontextmanager
    async def client(self):
        async with (
            httpx.AsyncClient(
                base_url="https://graph.invalid", transport=httpx.MockTransport(self.graph)
            ) as graph_http,
            httpx.AsyncClient(transport=httpx.MockTransport(self.backend)) as backend_http,
        ):
            yield AgentToolsClient(
                LangGraphClient(graph_http),
                AsyncStratifyX(
                    base_url="https://backend.invalid",
                    token="fixture",
                    httpx_client=backend_http,
                ),
                graph_http,
            )


def test_default_catalogue_is_composable_and_preserves_native_nested_schemas():
    async def scenario():
        service = Service()
        async with service.client() as client, Client(create_server(client)) as mcp:
            tools = {tool.name: tool for tool in (await mcp.list_tools()).tools}
            assert set(tools) == {
                "epoch_dataset_catalog",
                "epoch_search_dataset",
                "epoch_screen_assets",
                "epoch_inspect_source",
                "epoch_build_study",
                "epoch_audit_run",
                "epoch_execute",
                "epoch_extension_inputs",
                "epoch_save_extension",
                "epoch_execute_extension",
                "epoch_status",
                "epoch_resume",
                "epoch_read",
                "epoch_find",
            }
            for source in CATALOG["tools"]:
                if source["name"] == "discovery":
                    continue
                mapping = {
                    "discovery": "epoch_discover",
                    "inspect_source": "epoch_inspect_source",
                    "build_study": "epoch_build_study",
                    "audit_run": "epoch_audit_run",
                }
                schema = tools[mapping[source["name"]]].input_schema
                Draft202012Validator.check_schema(schema)
                assert schema.get("$defs") == source["parameters"].get("$defs")
                for name, prop in source["parameters"]["properties"].items():
                    assert schema["properties"][name] == prop
                assert "task" in schema["required"]
                assert not {"runtime", "state", "tool_call_id"} & set(schema["properties"])
            assert all(t.input_schema["additionalProperties"] is False for t in tools.values())
            assert not service.backend_calls
            assert [r.url.path for r in service.graph_calls] == ["/api/v1/agent-tools"]

    asyncio.run(scenario())


def test_default_mcp_never_invokes_the_legacy_discovery_llm_and_accepts_catalog_v2():
    class VersionTwo(Service):
        def graph(self, request):
            if request.url.path == '/api/v1/agent-tools':
                self.graph_calls.append(request)
                catalog = copy.deepcopy(CATALOG)
                catalog['version'] = 2
                catalog['tools'] = [tool for tool in catalog['tools'] if tool['name'] != 'discovery']
                return httpx.Response(200, json=catalog)
            return super().graph(request)

    async def scenario():
        for service in (Service(), VersionTwo()):
            async with service.client() as client, Client(create_server(client)) as mcp:
                names = {tool.name for tool in (await mcp.list_tools()).tools}
                assert 'epoch_discover' not in names
                assert {'epoch_search_dataset', 'epoch_screen_assets', 'epoch_build_study'} <= names
                rejected = await mcp.call_tool('epoch_discover', {'task': 'Find metadata', **ARGS})
                assert rejected.is_error
                assert not any(row.method == 'POST' for row in service.graph_calls)
    asyncio.run(scenario())


def test_default_mcp_cannot_resume_an_existing_interrupted_legacy_discovery():
    async def scenario():
        service = Service()
        async with service.client() as client:
            accepted = await client.invoke('discovery', ARGS, task='Existing legacy work')
            service.native_status = 'interrupted'
            handle = accepted.handle.model_dump(mode='json')
            service.graph_calls.clear()
            async with Client(create_server(client)) as mcp:
                result = await mcp.call_tool('epoch_resume', {'handle': handle, 'responses': {}})
                assert result.is_error and 'read-only' in result.content[0].text
            assert not any(row.method == 'POST' for row in service.graph_calls)
    asyncio.run(scenario())


def test_submit_reconnect_and_read_keep_the_same_native_operation_and_artifact():
    async def scenario():
        service = Service()
        async with service.client() as client, Client(create_server(client)) as mcp:
            submitted = await mcp.call_tool(
                "epoch_build_study", {"task": "Build the AAPL review", **BUILD_ARGS}
            )
            assert not submitted.is_error
            handle = submitted.structured_content["handle"]
            assert submitted.structured_content["status"] == "in_progress"
            service.native_status = "success"
            for _ in range(2):
                status = await mcp.call_tool("epoch_status", {"kind": "tool", "handle": handle})
                assert status.structured_content["status"] == "completed"
                assert status.structured_content["output"] == "Retained exact source references"
                assert status.structured_content["artifact"] is None
            read = await mcp.call_tool("epoch_read", {"kind": "tool", "handle": handle})
            assert read.structured_content["artifact"] == {"saved": "native proof"}
            creates = [
                r
                for r in service.graph_calls
                if r.method == "POST" and r.url.path.endswith("/runs")
            ]
            assert len(creates) == 1 and not service.backend_calls

    asyncio.run(scenario())


def test_execution_and_reads_use_backend_without_a_graph_run_or_published_answer():
    async def scenario():
        service = Service()
        async with service.client() as client, Client(create_server(client)) as mcp:
            executed = await mcp.call_tool(
                "epoch_execute",
                {"study_id": "study-one", "period": {"start": "2024-01-01", "end": "2024-12-31"}},
            )
            assert not executed.is_error
            assert executed.structured_content["id"] == "execution-one"
            read = await mcp.call_tool(
                "epoch_read", {"kind": "execution", "identifier": "execution-one"}
            )
            assert read.structured_content["status"] == "completed"
            assert [r.url.path for r in service.graph_calls] == ["/api/v1/agent-tools"]
            assert len([r for r in service.backend_calls if r.method == "POST"]) == 1

    asyncio.run(scenario())


def test_unknown_nested_fields_fail_before_any_thread_or_job_is_created():
    async def scenario():
        service = Service()
        async with service.client() as client, Client(create_server(client)) as mcp:
            invalid = copy.deepcopy(BUILD_ARGS)
            invalid["studies"][0]["runtime"] = {"authorization": "not-a-client-field"}
            result = await mcp.call_tool("epoch_build_study", {"task": "Build the review", **invalid})
            assert result.is_error
            assert [r.url.path for r in service.graph_calls] == ["/api/v1/agent-tools"]
            assert not service.backend_calls

    asyncio.run(scenario())


def test_forged_operation_handle_and_unowned_execution_are_not_accepted():
    async def scenario():
        service = Service()
        async with service.client() as client:
            submitted = await client.invoke("discovery", ARGS, task="Find metadata")
            forged = submitted.handle.model_copy(update={"tool_call_id": "different"})
            with pytest.raises(ValueError, match="handle differs"):
                await client.status(forged)
            service.owner_denied = True
            with pytest.raises(ApiError):
                await client.execution("execution-one")
            assert service.backend_calls[-1].url.path.endswith("/study")

    asyncio.run(scenario())


def test_completed_operations_do_not_resume_and_find_is_read_only():
    async def scenario():
        service = Service()
        async with service.client() as client:
            accepted = await client.invoke("discovery", ARGS, task="Find metadata")
            service.native_status = "success"
            with pytest.raises(ValueError, match="not waiting"):
                await client.resume(accepted.handle, {})
            assert await client.find(kind="workspaces") == [WORKSPACE]
            assert await client.find(kind="executions") == ["execution-one"]
            assert await client.find(kind="studies", limit=1, offset=1) == ["study-two"]
            assert (
                len(
                    [
                        r
                        for r in service.graph_calls
                        if r.method == "POST" and r.url.path.endswith("/runs")
                    ]
                )
                == 1
            )

    asyncio.run(scenario())


@pytest.mark.parametrize("continuation", [False, True])
def test_stale_interrupted_handle_cannot_read_or_answer_a_newer_workspace_question(continuation):
    class ReusedService(Service):
        newest_run = RUN

        def graph(self, request):
            if request.method == "GET" and request.url.path == f"/threads/{WORKSPACE}/runs":
                self.graph_calls.append(request)
                return httpx.Response(200, json=[{
                    "run_id": self.newest_run,
                    "status": "interrupted",
                    "metadata": self.metadata if continuation else {"epoch_tool_call_id": "newer-call"},
                }])
            if request.url.path == f"/threads/{WORKSPACE}/state":
                self.graph_calls.append(request)
                return httpx.Response(200, json={"values": {}, "interrupts": [INTERRUPT], "next": []})
            return super().graph(request)

    async def scenario():
        service = ReusedService()
        async with service.client() as client:
            accepted = await client.invoke("discovery", ARGS, task="Find metadata")
            service.native_status = "interrupted"
            current = await client.status(accepted.handle)
            assert current.status == "needs_input" and len(current.interrupts) == 1
            service.newest_run = "33333333-3333-4333-8333-333333333333"
            service.graph_calls.clear()
            with pytest.raises(ValueError, match="stale"):
                await client.status(accepted.handle)
            with pytest.raises(ValueError, match="stale"):
                await client.resume(accepted.handle, {})
            assert not any(r.url.path.endswith("/state") for r in service.graph_calls)
            assert not any(r.method == "POST" for r in service.graph_calls)

    asyncio.run(scenario())


def test_stdio_accepts_tools_url_without_unused_base_graph_url(monkeypatch):
    from epoch_sdk import mcp as module

    captured = {}

    class Client:
        closed = False

        async def aclose(self):
            self.closed = True

    class Server:
        ran = False

        async def run_stdio_async(self):
            self.ran = True

    client, server = Client(), Server()

    def connect(**arguments):
        captured.update(arguments)
        return client

    monkeypatch.delenv("EPOCH_GRAPH_URL", raising=False)
    monkeypatch.setenv("EPOCH_MCP_GRAPH_URL", "http://tools.invalid")
    monkeypatch.setenv("EPOCH_BACKEND_URL", "http://backend.invalid")
    monkeypatch.setenv("EPOCH_TOKEN", "fixture")
    monkeypatch.setattr(module.AgentToolsClient, "connect", connect)
    monkeypatch.setattr(module, "create_server", lambda _: server)
    asyncio.run(module._stdio())
    assert captured["graph_url"] == "http://tools.invalid"
    assert server.ran and client.closed


def test_workspace_find_retains_metadata_required_by_the_service_owner_filter():
    async def scenario():
        service = Service()
        original_graph = service.graph
        def projected_search(request):
            if request.url.path != '/threads/search':
                return original_graph(request)
            body = json.loads(request.content)
            assert body['metadata'] == {'epoch_tool_workspace': 'v1'}
            original = {'thread_id': WORKSPACE, 'metadata': {'owner': 'fixture-owner', 'epoch_tool_workspace': 'v1'}}
            projected = {name: original[name] for name in body['select']}
            # The actual EpochAI response filter drops rows whose projected
            # metadata cannot establish ownership. Keep that enforcement.
            rows = [projected] if projected.get('metadata', {}).get('owner') == 'fixture-owner' else []
            return httpx.Response(200, json=rows)
        service.graph = projected_search
        async with service.client() as client, Client(create_server(client)) as mcp:
            assert await client.find(kind='workspaces') == [WORKSPACE]
            result = await mcp.call_tool('epoch_find', {'kind': 'workspaces'})
            assert not result.is_error
            assert result.structured_content['ids'] == [WORKSPACE]
            assert set(result.structured_content) == {'kind', 'ids', 'offset'}
    asyncio.run(scenario())


@pytest.mark.parametrize("failure", ["connect", "timeout", "status", "invalid", "schema"])
def test_mcp_catalog_listing_reports_required_service_failure_without_partial_tools(failure):
    from mcp.shared.exceptions import MCPError

    async def scenario():
        calls = []
        def rejected(request):
            calls.append(request)
            if failure == "connect":
                raise httpx.ConnectError("private transport details", request=request)
            if failure == "timeout":
                raise httpx.ReadTimeout("private transport details", request=request)
            if failure == "status":
                return httpx.Response(503, json={"private": "must-not-leak"})
            if failure == "schema":
                catalog = copy.deepcopy(CATALOG)
                catalog["tools"][0]["parameters"] = {"type": "must-not-leak"}
                return httpx.Response(200, json=catalog)
            return httpx.Response(200, json={"private": "must-not-leak"})
        async with httpx.AsyncClient(base_url="https://graph.invalid",
                transport=httpx.MockTransport(rejected)) as http:
            client = AgentToolsClient(LangGraphClient(http), AsyncStratifyX(base_url="https://backend.invalid"),
                                      graph_http=http)
            try:
                async with Client(create_server(client)) as mcp:
                    with pytest.raises(MCPError) as caught:
                        await mcp.list_tools()
                    assert caught.value.code == -32603
                    message = str(caught.value)
                    assert "Epoch tools" in message and "catalog" in message
                    assert "must-not-leak" not in message and "private transport" not in message
                    assert "Internal server error" not in message
                    assert len(calls) == 1 and client._catalog is None
                    # A rejected schema/body must not be cached and served by
                    # a later listing after the first error was reported.
                    with pytest.raises(MCPError):
                        await mcp.list_tools()
                    with pytest.raises(MCPError) as specialist:
                        await mcp.call_tool("epoch_build_study", {"task": "Do not run with an invalid catalog"})
                    assert "must-not-leak" not in str(specialist.value)
                    assert "private transport" not in str(specialist.value)
                    assert "Epoch tools" in str(specialist.value)
                assert len(calls) == 3
                assert client._catalog is None
            finally:
                await client.aclose()
    asyncio.run(scenario())
