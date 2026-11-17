"""SDK/MCP transport over captured native records; no provider or graph run.

The first page and answer revisions come from the C++ service. End-page and
malformed variants are explicit synthetic paging controls, not acquisitions.
"""

import asyncio
import copy
import json
from pathlib import Path

import httpx
import pytest
from langgraph_sdk.client import LangGraphClient
from mcp import Client
from stratifyx import AsyncStratifyX

from epoch_sdk.errors import EpochError
from epoch_sdk.research import EpochClient
from epoch_sdk.supervisor import SupervisorClient

FIXTURES = Path(__file__).parent / "fixtures/acquisition_provenance"
ANSWER = json.loads((FIXTURES / "response-v1.json").read_text())
REVISION = json.loads((FIXTURES / "response-v2.json").read_text())
PAGE = json.loads((FIXTURES / "provenance-page.json").read_text())
CATALOGUE = json.loads((FIXTURES / "input-catalog.response.json").read_text())
SHA = PAGE["reference"]["sha256"]


class Service:
    def __init__(self, page=None, status=200):
        self.calls = []
        self.graph_calls = []
        self.page = page
        self.status = status

    def graph(self, request):
        self.graph_calls.append(request)
        assert request.method == "GET" and request.url.path == "/api/v1/agent-tools"
        raise AssertionError("Native operation must not use the retired tools graph")

    def backend(self, request):
        self.calls.append(request)
        assert request.headers["Authorization"] == "Bearer fixture"
        if request.url.path.endswith("/acquisition-provenance"):
            assert request.method == "GET"
            if self.status != 200:
                return httpx.Response(self.status, json={"message": "Snapshot differs"})
            if self.page is not None:
                return httpx.Response(200, json=self.page)
            offset = int(request.url.params["offset"])
            if offset == 0:
                return httpx.Response(200, json=PAGE)
            # Explicit synthetic end-page control. Native first-page identity
            # and source/acquisition facts remain untouched.
            assert offset == 1
            return httpx.Response(200, json={
                "reference": PAGE["reference"], "offset": 1,
                "records": [{"execution_id": "older-legacy-input", "status": "not_recorded"}],
            })
        if request.url.path.endswith("/inputs"):
            return httpx.Response(200, json=CATALOGUE)
        assert request.url.path == f"/api/v1/research/responses/{ANSWER['response_id']}"
        return httpx.Response(200, json=REVISION if request.url.params["version"] == "2" else ANSWER)


async def scenario(operation, *, client_kind="application", service=None):
    service = service or Service()
    async with (
        httpx.AsyncClient(transport=httpx.MockTransport(service.backend)) as native_http,
        httpx.AsyncClient(base_url="https://graph.invalid", transport=httpx.MockTransport(service.graph)) as graph_http,
    ):
        native = AsyncStratifyX(base_url="https://backend.invalid", token="fixture", httpx_client=native_http)
        graph = LangGraphClient(graph_http)
        client = EpochClient(SupervisorClient(graph, native, document_http=graph_http))
        await operation(client, service)


@pytest.mark.parametrize("client_kind", ["application"])
def test_frozen_reference_and_exact_acquisition_clocks_survive_both_clients(client_kind):
    async def check(client, service):
        first = await client.response(ANSWER["response_id"], version=1)
        second = await client.response(ANSWER["response_id"], version=2)
        assert first.to_wire() == ANSWER and second.to_wire() == REVISION
        assert first.reference().acquisition_provenance == second.reference().acquisition_provenance
        page = await client.response_provenance(ANSWER["response_id"], version=1, page_size=1)
        assert page.reference == first.acquisition_provenance and page.next_offset == 1
        receipt = page.records[0].source.acquisitions[0]
        assert receipt.payload_id == "immutable-payload"
        assert receipt.origin.value == "cache_hit"
        assert receipt.acquired_at == "2026-10-27T09:00:00Z"
        assert receipt.read_completed_at == "2026-10-28T10:00:00Z"
        last = await client.response_provenance(ANSWER["response_id"], version=1, offset=1, page_size=1)
        assert last.next_offset is None and last.records[0].status.value == "not_recorded"
        execution = await client.execution_provenance("execution-one", expected_sha256=SHA, page_size=1)
        assert execution.reference == page.reference
        assert service.calls[-1].url.params["expected_sha256"] == SHA
        assert not service.graph_calls
    asyncio.run(scenario(check, client_kind=client_kind))




@pytest.mark.parametrize("arguments", [
    {"offset": True}, {"offset": -1}, {"offset": 9007199254740992},
    {"page_size": True}, {"page_size": 0}, {"page_size": 1001},
])
def test_invalid_paging_never_reaches_backend(arguments):
    async def check(client, service):
        with pytest.raises(ValueError):
            await client.execution_provenance("execution-one", **arguments)
        assert not service.calls
    asyncio.run(scenario(check))


@pytest.mark.parametrize("change", [
    {"offset": 1}, {"records": []}, {"next_offset": None},
    {"records": PAGE["records"] * 2, "next_offset": None},
])
def test_inconsistent_pages_fail_without_repair(change):
    async def check(client, service):
        with pytest.raises(ValueError, match="paging"):
            await client.execution_provenance("execution-one", page_size=1)
        assert len(service.calls) == 1
    asyncio.run(scenario(check, service=Service({**copy.deepcopy(PAGE), **change})))


def test_snapshot_change_fails_explicitly_without_retry():
    async def check(client, service):
        with pytest.raises(EpochError):
            await client.execution_provenance("execution-one", expected_sha256=SHA)
        assert len(service.calls) == 1
    asyncio.run(scenario(check, service=Service(status=409)))


def test_wrong_snapshot_is_not_accepted_even_after_successful_http():
    async def check(client, service):
        with pytest.raises(ValueError, match="different acquisition"):
            await client.execution_provenance("execution-one", expected_sha256="f" * 64)
    asyncio.run(scenario(check))
