"""Shared native SDK/MCP lifecycle over captured C++ publication records.

HTTP is controlled. The input metadata and authored source below are synthetic
transport controls; no numerical, provider or live client acceptance is claimed.
"""
import asyncio
import copy
import json
from pathlib import Path

import httpx
import pyarrow as pa
import pytest
from langgraph_sdk.client import LangGraphClient
from mcp import Client
from stratifyx import AsyncStratifyX
from stratifyx.types import CreateSdkExecutionRequest, NamedExecutionInputSelection
from test_agent_tools import CATALOG

from epoch_sdk.agent_tools import AgentToolsClient
from epoch_sdk.mcp import create_server
from epoch_sdk.research import EpochClient
from epoch_sdk.responses import SavedResearchResponse
from epoch_sdk.supervisor import SupervisorClient

ROOT = Path(__file__).parent / "fixtures/execution_extensions"
load = lambda name: json.loads((ROOT / name).read_text())
REQUEST = load("execution-request.json")
RECORD = load("execution-record.json")
ANSWER = load("response-v1.json")
DASHBOARD = load("dashboard-v0.json")
PIN = RECORD["extension_outputs"]["dashboards"][0]["presentation"]
SOURCE = "# Synthetic authored-source transport control; no engine runs in this test."
CATALOGUE = {
    "source": {"execution_id": "original", "study_id": "original-study", "family": "research", "source": "retained_fixture()"},
    "tables": [{"table": "orders", "reference": "ExecutionTable.Orders", "field_enum": "ExecutionTableOrders", "row_count": 6,
                "fields": [{"name": "quantity", "reference": "ExecutionTableOrders.Quantity", "arrow_type": "double", "nullable": False}]}],
}


class Service:
    def __init__(self):
        self.calls = []
        self.graph_calls = []

    def graph(self, request):
        self.graph_calls.append(request)
        assert request.method == "GET" and request.url.path == "/api/v1/agent-tools"
        return httpx.Response(200, json=CATALOG)

    def backend(self, request):
        self.calls.append(request)
        assert request.headers["Authorization"] == "Bearer fixture"
        path = request.url.path
        if path == "/api/v1/studies/executions/original/inputs":
            assert request.method == "POST" and json.loads(request.content) == {"tables": ["orders"]}
            return httpx.Response(200, json=CATALOGUE)
        if path == "/api/v1/agents/threads/native-scope/studies/definitions":
            assert json.loads(request.content) == {
                "name": "Order review", "description": "Controlled source save", "source": SOURCE,
                "study_type": "research", "data": {"assets": []},
                "execution_input": {"source_execution_id": "original", "tables": ["orders"]},
            }
            return httpx.Response(201, json={"id": "extension-study", "message": "Controlled definition saved"})
        if path == "/api/v1/integration/execution-requests":
            assert request.method == "POST" and json.loads(request.content) == REQUEST
            return httpx.Response(200, json=RECORD)
        if path == "/api/v1/integration/execution-requests/by-handle/presentation-test":
            assert request.method == "GET"
            return httpx.Response(200, json=RECORD)
        if path == f"/api/v1/contexts/publications/{PIN['publication_id']}/presentation":
            assert request.method == "GET" and request.url.params["edit_version"] == "0"
            return httpx.Response(200, json={**PIN, "dashboard": DASHBOARD, "editable_fields": []})
        if path == f"/api/v1/studies/executions/{RECORD['execution_id']}/response-tables":
            # An empty typed end-page is a transport control, not invented
            # financial rows. Full nonempty paging has its own shared tests.
            part = next(item for item in ANSWER["content"]["outputs"] if item["type"] == "table")
            body = json.loads(request.content)
            assert body["table"] == part["source"]["table"]
            assert body["field_ids"] == part["source"]["field_ids"]
            assert body["offset"] == part["source"]["row_count"]
            kinds = {"string": pa.string(), "int64": pa.int64(), "float64": pa.float64()}
            table = pa.Table.from_arrays(
                [pa.array([], type=kinds[column["type"]]) for column in part["schema"]],
                names=part["source"]["field_ids"],
            )
            sink = pa.BufferOutputStream()
            with pa.ipc.new_stream(sink, table.schema) as writer:
                writer.write_table(table)
            return httpx.Response(200, content=sink.getvalue().to_pybytes(), headers={
                "X-Arrow-Total-Rows": str(part["source"]["row_count"]),
                "X-Arrow-Returned-Rows": "0", "X-Arrow-Row-Offset": str(body["offset"]),
            })
        assert path == f"/api/v1/research/responses/{ANSWER['response_id']}"
        assert request.method == "GET" and request.url.params["version"] == "1"
        return httpx.Response(200, json=ANSWER)


@pytest.mark.parametrize("client_kind", ["application", "coding_agent"])
def test_both_clients_share_native_lifecycle_and_preserve_source_and_zero_edit_pin(client_kind):
    async def scenario():
        service = Service()
        async with (
            httpx.AsyncClient(transport=httpx.MockTransport(service.backend)) as native_http,
            httpx.AsyncClient(base_url="https://graph.invalid", transport=httpx.MockTransport(service.graph)) as graph_http,
        ):
            native = AsyncStratifyX(base_url="https://backend.invalid", token="fixture", httpx_client=native_http)
            graph = LangGraphClient(graph_http)
            client = (EpochClient(SupervisorClient(graph, native)) if client_kind == "application"
                      else AgentToolsClient(graph, native, graph_http))
            inputs = await client.extension_inputs("original", tables=["orders"])
            assert inputs.source.execution_id == "original"
            assert inputs.tables[0].fields[0].reference == "ExecutionTableOrders.Quantity"
            definition = await client.save_extension("native-scope", source_execution_id="original", tables=["orders"],
                                                     source=SOURCE, name="Order review", description="Controlled source save")
            assert definition.id == "extension-study"
            accepted = await client.execute_extension(CreateSdkExecutionRequest.model_validate(REQUEST))
            observed = await client.extension_status("presentation-test")
            assert accepted == observed and observed.response_phase.value == "outputs_recorded"
            assert observed.extension_outputs.provenance.source_execution_id == "original"
            assert observed.extension_outputs.provenance.execution_id != "original"
            assert observed.extension_outputs.dashboards[0].presentation.edit_version == 0
            view = await client.extension_presentation(observed.extension_outputs.dashboards[0].presentation)
            assert view.publication_id == PIN["publication_id"] and view.edit_version == 0
            assert view.dashboard.model_dump(mode="json", by_alias=True, exclude_unset=True) == DASHBOARD
            answer = await client.response(ANSWER["response_id"], version=1)
            assert answer.to_wire() == ANSWER
            assert answer.reference().extension == observed.extension_outputs.provenance
            assert len(service.calls) == 6 and not service.graph_calls
    asyncio.run(scenario())


def test_mcp_uses_the_same_methods_and_returns_machine_readable_pins_without_graph_runs():
    async def scenario():
        service = Service()
        async with (
            httpx.AsyncClient(transport=httpx.MockTransport(service.backend)) as native_http,
            httpx.AsyncClient(base_url="https://graph.invalid", transport=httpx.MockTransport(service.graph)) as graph_http,
        ):
            tools = AgentToolsClient(LangGraphClient(graph_http), AsyncStratifyX(base_url="https://backend.invalid", token="fixture", httpx_client=native_http), graph_http)
            async with Client(create_server(tools)) as mcp:
                listed = {tool.name for tool in (await mcp.list_tools()).tools}
                assert {"epoch_extension_inputs", "epoch_save_extension", "epoch_execute_extension"} <= listed
                assert not (await mcp.call_tool("epoch_extension_inputs", {"execution_id": "original", "tables": ["orders"]})).is_error
                assert not (await mcp.call_tool("epoch_save_extension", {"thread_id": "native-scope", "source_execution_id": "original", "tables": ["orders"], "source": SOURCE, "name": "Order review", "description": "Controlled source save"})).is_error
                executed = await mcp.call_tool("epoch_execute_extension", {"request": REQUEST})
                assert not executed.is_error and executed.structured_content == RECORD
                status = await mcp.call_tool("epoch_status", {"kind": "extension", "operation_id": "presentation-test"})
                assert not status.is_error and status.structured_content == RECORD
                view = await mcp.call_tool("epoch_read", {"kind": "presentation", "presentation": PIN})
                assert not view.is_error and view.structured_content["edit_version"] == 0
                assert view.structured_content["dashboard"] == DASHBOARD
                answer = await mcp.call_tool("epoch_read", {"kind": "response", "identifier": ANSWER["response_id"], "version": 1})
                assert not answer.is_error and answer.structured_content == ANSWER
                part = next(item for item in ANSWER["content"]["outputs"] if item["type"] == "table")
                page = await mcp.call_tool("epoch_read", {"kind": "response", "identifier": ANSWER["response_id"], "version": 1,
                                                        "table": part["name"], "offset": part["source"]["row_count"]})
                assert not page.is_error and page.structured_content["rows"] == []
                assert page.structured_content["total_rows"] == part["source"]["row_count"]
                assert page.structured_content["next_offset"] is None
                calls = len(service.calls)
                invalid = await mcp.call_tool("epoch_execute_extension", {"request": {**REQUEST, "owner": "forged"}})
                assert invalid.is_error and len(service.calls) == calls
                wrong = await mcp.call_tool("epoch_status", {"kind": "extension", "operation_id": "presentation-test", "execution_id": "wrong"})
                assert wrong.is_error and len(service.calls) == calls
                paging = await mcp.call_tool("epoch_read", {"kind": "response", "identifier": ANSWER["response_id"], "offset": 1})
                assert paging.is_error and len(service.calls) == calls
            assert all(call.url.path == "/api/v1/agent-tools" for call in service.graph_calls)
    asyncio.run(scenario())


def test_saved_answer_rejects_mismatched_extension_identity_and_old_answers_remain_valid():
    changed = copy.deepcopy(ANSWER)
    changed["extension"]["execution_id"] = "wrong-derived-execution"
    with pytest.raises(ValueError, match="attribution"):
        SavedResearchResponse.model_validate(changed)
    legacy = {key: value for key, value in ANSWER.items() if key != "extension"}
    assert SavedResearchResponse.model_validate(legacy).extension is None


def test_native_contract_refs_and_discriminator_targets_resolve_to_the_same_owned_projection():
    contract = json.loads((ROOT.parents[4] / "contracts/openapi.json").read_text())
    schemas = contract["components"]["schemas"]
    def visit(node):
        if isinstance(node, dict):
            for key, value in node.items():
                if key == "$ref" and value.startswith("#/components/schemas/"):
                    assert value.removeprefix("#/components/schemas/") in schemas
                if key == "discriminator":
                    for target in value.get("mapping", {}).values():
                        assert target.startswith("#/components/schemas/Native_")
                        assert target.removeprefix("#/components/schemas/") in schemas
                visit(value)
        elif isinstance(node, list):
            for value in node:
                visit(value)
    for name in contract["x-epoch-native-operations"]["schemas"]:
        visit(schemas[name])


@pytest.mark.parametrize("interface", ["sdk", "mcp"])
def test_named_sources_cross_the_existing_catalog_save_and_execute_interfaces(interface):
    """Controlled transport checks; the native worker owns numeric parity."""
    async def scenario():
        extra = {"alias": "candidate", "source_execution_id": "candidate-source", "tables": ["orders"]}
        request_wire = {**REQUEST, "additional_sources": [extra]}
        record_wire = copy.deepcopy(RECORD)
        record_wire["request"] = request_wire
        record_wire["extension_outputs"]["provenance"]["additional_sources"] = [extra]
        catalogue_wire = copy.deepcopy(CATALOGUE)
        catalogue_wire["additional_sources"] = [{"alias": "candidate", "execution_id": "candidate-source",
            "study_id": "candidate-study", "family": "backtest", "source": "candidate_fixture()"}]
        candidate = copy.deepcopy(CATALOGUE["tables"][0])
        candidate.update(source_alias="candidate", reference="ExecutionSourceCandidateTable.Orders",
            field_enum="ExecutionSourceCandidateTableOrders")
        candidate["fields"][0]["reference"] = "ExecutionSourceCandidateTableOrders.Quantity"
        catalogue_wire["tables"].append(candidate)
        calls = []
        graph_calls = []

        def graph(request):
            graph_calls.append(request)
            assert request.method == "GET" and request.url.path == "/api/v1/agent-tools"
            return httpx.Response(200, json=CATALOG)

        def backend(request):
            body = json.loads(request.content)
            calls.append((request.url.path, body))
            if request.url.path.endswith("/inputs"):
                assert body == {"tables": ["orders"], "additional_sources": [extra]}
                return httpx.Response(200, json=catalogue_wire)
            if request.url.path.endswith("/studies/definitions"):
                assert body["execution_input"] == {"source_execution_id": "original",
                    "tables": ["orders"], "additional_sources": [extra]}
                return httpx.Response(201, json={"id": "extension-study", "message": "Saved"})
            assert request.url.path == "/api/v1/integration/execution-requests"
            assert body == request_wire
            return httpx.Response(200, json=record_wire)

        async with (
            httpx.AsyncClient(transport=httpx.MockTransport(backend)) as native_http,
            httpx.AsyncClient(base_url="https://graph.invalid",
                transport=httpx.MockTransport(graph)) as graph_http,
        ):
            client = AgentToolsClient(LangGraphClient(graph_http),
                AsyncStratifyX(base_url="https://backend.invalid", token="fixture", httpx_client=native_http), graph_http)
            if interface == "sdk":
                sources = [NamedExecutionInputSelection.model_validate(extra)]
                metadata = await client.extension_inputs("original", tables=["orders"], additional_sources=sources)
                assert metadata.additional_sources is not None
                assert metadata.additional_sources[0].execution_id == "candidate-source"
                await client.save_extension("native-scope", source_execution_id="original", tables=["orders"],
                    additional_sources=sources, source=SOURCE, name="Comparison", description="Saved comparison")
                result = await client.execute_extension(CreateSdkExecutionRequest.model_validate(request_wire))
                assert result.extension_outputs is not None
                assert result.extension_outputs.provenance.additional_sources == sources
            else:
                async with Client(create_server(client)) as mcp:
                    result = await mcp.call_tool("epoch_extension_inputs", {"execution_id": "original",
                        "tables": ["orders"], "additional_sources": [extra]})
                    assert not result.is_error
                    assert result.structured_content["additional_sources"][0]["execution_id"] == "candidate-source"
                    saved = await mcp.call_tool("epoch_save_extension", {"thread_id": "native-scope",
                        "source_execution_id": "original", "tables": ["orders"], "additional_sources": [extra],
                        "source": SOURCE, "name": "Comparison", "description": "Saved comparison"})
                    assert not saved.is_error
                    executed = await mcp.call_tool("epoch_execute_extension", {"request": request_wire})
                    assert not executed.is_error
                    assert executed.structured_content["extension_outputs"]["provenance"]["additional_sources"] == [extra]
            assert len(calls) == 3
            assert len(graph_calls) == (1 if interface == "mcp" else 0)
    asyncio.run(scenario())
