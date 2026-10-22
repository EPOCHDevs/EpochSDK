"""Shared SDK/MCP native data calls with controlled HTTP and no graph run.

Response fixtures were captured from EpochBackend's native [dataset_clients]
test. Paging variants below are explicitly synthetic metadata transport cases.
"""
import asyncio
import json
from pathlib import Path

import httpx
import pytest
from langgraph_sdk.client import LangGraphClient
from mcp import Client
from stratifyx import AsyncStratifyX
from stratifyx.core.api_error import ApiError
from stratifyx.types import DatasetSearchQuery

from epoch_sdk.agent_tools import AgentToolsClient
from epoch_sdk.mcp import create_server
from epoch_sdk.research import EpochClient
from epoch_sdk.supervisor import SupervisorClient
from test_agent_tools import CATALOG

FIXTURES = Path(__file__).parent / 'fixtures/dataset_search'
QUERY = {"request_id": "company", "subjects": [{"kind": "asset_name", "name": "Apple"}]}


def fixture(name):
    return json.loads((FIXTURES / (name + '.response.json')).read_text())


class MetadataService:
    def __init__(self, inline):
        self.inline = inline
        self.calls = []
        self.search = fixture('search')
        self.rows = [dict(self.search['records'][0], record_ref=f'fixture-record-{i}') for i in range(15)]
        if not inline:
            self.search['records'] = []
            self.search['records_complete'] = False
            self.search['counts']['stored_records'] = 15
            self.search['counts']['candidates'] = 15

    def transport(self, request):
        self.calls.append(request)
        body = json.loads(request.content)
        assert request.headers['Authorization'] == 'Bearer fixture'
        if request.url.path == '/api/v1/discovery/catalog':
            assert body['include_details'] is True
            return httpx.Response(200, json=fixture('catalog'))
        if request.url.path == '/api/v1/discovery/datasets/search':
            assert body['requests'][0] == QUERY
            return httpx.Response(200, json=self.search)
        if request.url.path == '/api/v1/discovery/assets/screen':
            assert body == {'kind': 'saved', 'universe_ref': 'owned-cohort'}
            return httpx.Response(200, json=fixture('screen'))
        if request.url.path == '/api/v1/discovery/query-stored':
            assert body['operation'] == {'kind': 'read'}
            assert body['result_refs'] == [self.search['receipt']['result_ref']]
            assert body['limit'] == 10
            after = body.get('cursor')
            assert after in (None, 'fixture-continuation')
            records = self.rows[:10] if after is None else self.rows[10:]
            return httpx.Response(200, json={
                'columns': [], 'rows': [], 'records': records, 'result_refs': body['result_refs'],
                'original_receipts': [self.search['receipt']], 'receipts': [self.search['receipt']],
                'returned': len(records), 'total_matching': 15, 'total_stored': 15,
                'has_more': after is None,
                **({'next_cursor': 'fixture-continuation'} if after is None else {}),
            })
        raise AssertionError(request.url)


@pytest.mark.parametrize('inline', [False, True])
def test_sdk_and_mcp_share_native_contracts_and_bound_first_page_without_research(inline):
    async def scenario():
        service = MetadataService(inline)
        graph_calls = []
        def no_graph(request):
            graph_calls.append(request)
            if request.method == 'GET' and request.url.path == '/api/v1/agent-tools':
                return httpx.Response(200, json=CATALOG)
            raise AssertionError('Native metadata must not contact EpochAI')
        async with (
            httpx.AsyncClient(transport=httpx.MockTransport(service.transport)) as backend_http,
            httpx.AsyncClient(base_url='https://graph.invalid', transport=httpx.MockTransport(no_graph)) as graph_http,
        ):
            backend = AsyncStratifyX(base_url='https://backend.invalid', token='fixture', httpx_client=backend_http)
            graph = LangGraphClient(graph_http)
            tools = AgentToolsClient(graph, backend, graph_http)
            # The same methods are available to the notebook/application client.
            epoch = EpochClient(SupervisorClient(graph, backend))
            catalog = await epoch.dataset_catalog(include_details=True)
            assert catalog.model_dump(mode='json', by_alias=True, exclude_unset=True) == fixture('catalog')
            assert catalog.registry_version != catalog.loader_registry_version
            query = DatasetSearchQuery.model_validate(QUERY)
            result = await epoch.search_dataset([query])
            assert result.result.model_dump(mode='json', by_alias=True, exclude_unset=True) == service.search
            assert result.result.records_complete is inline
            if inline:
                assert result.page is None
                assert len(service.calls) == 2
            else:
                assert result.page.returned == 10 and result.page.has_more
                assert len(service.calls) == 3
                later = await tools.read_dataset_search(result.result.receipt.result_ref, cursor=result.page.next_cursor)
                assert len(later.records) == 5 and not later.has_more
                assert {r.record_ref for r in result.page.records}.isdisjoint(r.record_ref for r in later.records)

            assert not graph_calls
            async with Client(create_server(tools)) as mcp:
                searched = await mcp.call_tool('epoch_search_dataset', {'requests': [QUERY]})
                assert not searched.is_error
                assert searched.structured_content['result'] == result.result.model_dump(mode='json', by_alias=True, exclude_unset=True)
                screen = await mcp.call_tool('epoch_screen_assets', {'request': {'kind': 'saved', 'universe_ref': 'owned-cohort'}})
                assert not screen.is_error
                assert screen.structured_content['definition']['membership_screen']['index_membership_mode'] == 'PointInTime'
                if not inline:
                    page = await mcp.call_tool('epoch_read', {'kind': 'dataset_search', 'identifier': result.result.receipt.result_ref, 'cursor': result.page.next_cursor})
                    assert not page.is_error and page.structured_content['returned'] == 5
                before = len(service.calls)
                invalid = await mcp.call_tool('epoch_screen_assets', {'request': {'kind': 'invented'}})
                assert invalid.is_error and len(service.calls) == before
            assert sum(r.url.path.endswith('/datasets/search') for r in service.calls) == 2
            assert all(r.method == 'GET' and r.url.path == '/api/v1/agent-tools' for r in graph_calls)
    asyncio.run(scenario())


def test_a_failed_page_read_remains_an_error_instead_of_an_empty_or_complete_result():
    async def scenario():
        service = MetadataService(False)
        def transport(request):
            if request.url.path.endswith('/query-stored'):
                return httpx.Response(403, json={'error': 'Forbidden', 'message': 'Not owned', 'timestamp': '2026-10-21T00:00:00Z'})
            return service.transport(request)
        async with httpx.AsyncClient(transport=httpx.MockTransport(transport)) as http:
            # Only the native Backend is used by DatasetClient methods.
            from epoch_sdk.datasets import DatasetClient
            client = DatasetClient()
            client.backend = AsyncStratifyX(base_url='https://backend.invalid', token='fixture', httpx_client=http)
            with pytest.raises(ApiError) as error:
                await client.search_dataset([DatasetSearchQuery.model_validate(QUERY)])
            assert error.value.status_code == 403
            assert len(service.calls) == 1
    asyncio.run(scenario())
