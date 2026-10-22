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
from pydantic import TypeAdapter
from stratifyx import AsyncStratifyX
from stratifyx.core.api_error import ApiError
from stratifyx.types import DatasetSearchQuery, ScreenAssetsRequest
from test_agent_tools import CATALOG

from epoch_sdk.agent_tools import AgentToolsClient
from epoch_sdk.mcp import create_server
from epoch_sdk.research import EpochClient
from epoch_sdk.supervisor import SupervisorClient

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


def test_customer_table_snapshot_fits_the_owner_scoped_catalog_in_sdk_and_mcp():
    """Schema/transport fixture, not a production database connector or auth test.

    Native catalog/Files tests own authorization. This checks that neither client
    invents a database-specific tool or drops the existing schema/clock contract.
    """
    from stratifyx.types import SavedDataset

    def saved(owner):
        return SavedDataset.model_validate({
            'dataset_ref': f'dataset:{owner}-signal@1', 'name': 'Internal revision signal',
            'source_ref': f'source:{owner}-signal@1', 'saved_at': '2026-10-21T12:00:00Z',
            'archived': False,
            'descriptor': {
                'content_sha256': 'a' * 64, 'schema_sha256': 'b' * 64,
                'sources': [{'kind': 'dataset', 'dataset_ref': f'dataset:{owner}-export@1'}],
                'limitations': ['Fixture database export snapshot; no live connector is installed.'],
                'preparation': {
                    'origin': 'derived', 'purpose': 'study_source', 'enrichment': 'user_defined',
                    'implementation_version': 'fixture-sql-export-v1',
                    'instruction': 'Preserve the supplied signal and its publication clock.',
                    'schema_choice': {'mode': 'imported'},
                },
                'shape': {'format': 'table', 'coverage': {
                    'row_count': 2, 'first_timestamp': '2026-10-21T12:00:00Z',
                    'last_timestamp': '2026-10-21T12:01:00Z',
                }, 'schema': {
                    'frame_schema': {'columns': [
                        {'name': 'known_at', 'dtype': 'timestamp[ns,UTC]', 'nullable': False, 'is_index': True, 'semantic': 'Timestamp'},
                        {'name': 'issuer', 'dtype': 'string', 'nullable': False},
                        {'name': 'revision_signal', 'dtype': 'float64', 'nullable': True, 'unit': 'fraction'},
                    ], 'transforms': [{'kind': 'PromoteIndex'}]},
                    'dataframe_metadata': {
                        'data_type': 'user_dataset', 'description': 'Internal revision signal snapshot',
                        'foundation': 'Nanosecond', 'entity_columns': ['issuer'],
                        'source_capabilities': {
                            'range': 'FullPayloadLocalSlice', 'future_rows': 'PastOrPresentOnly',
                            'predecessor': 'Unsupported', 'availability_axis': 'None',
                        },
                    },
                    'key_fields': ['issuer'], 'asset_field': 'issuer',
                    'time_axis': {'meaning': 'publication', 'source_precision': 'nanosecond',
                                  'source_timezone': 'UTC', 'assumed': False},
                }},
            },
        })

    async def scenario():
        seen = []
        for owner in ('alice', 'bob'):
            def backend(request, owner=owner):
                assert request.url.path == '/api/v1/discovery/catalog'
                assert request.headers['Authorization'] == f'Bearer fixture-{owner}'
                assert json.loads(request.content)['include_saved'] is True
                seen.append(owner)
                result = fixture('catalog')
                result['saved'] = {'items': [saved(owner).model_dump(mode='json', by_alias=True, exclude_unset=True)]}
                return httpx.Response(200, json=result)

            def graph(request):
                assert request.method == 'GET' and request.url.path == '/api/v1/agent-tools'
                return httpx.Response(200, json=CATALOG)

            async with (
                httpx.AsyncClient(transport=httpx.MockTransport(backend)) as native_http,
                httpx.AsyncClient(base_url='https://graph.invalid', transport=httpx.MockTransport(graph)) as graph_http,
            ):
                native = AsyncStratifyX(base_url='https://backend.invalid', token=f'fixture-{owner}', httpx_client=native_http)
                tools = AgentToolsClient(LangGraphClient(graph_http), native, graph_http)
                expected = await tools.dataset_catalog()
                assert expected.saved.items == [saved(owner)]
                assert owner not in expected.overview
                async with Client(create_server(tools)) as mcp:
                    actual = await mcp.call_tool('epoch_dataset_catalog', {})
                    assert not actual.is_error
                    assert actual.structured_content == expected.model_dump(mode='json', by_alias=True, exclude_unset=True)
        assert seen == ['alice', 'alice', 'bob', 'bob']
    asyncio.run(scenario())


@pytest.mark.parametrize('limit', [0, 11, 100, True, 1.5, '10'])
def test_metadata_page_bounds_reject_before_native_transport_and_match_mcp_schema(limit):
    async def scenario():
        from epoch_sdk.datasets import DatasetClient
        def no_backend(request):
            if request.method == 'GET' and request.url.path == '/api/v1/agent-tools':
                return httpx.Response(200, json=CATALOG)
            pytest.fail('An invalid metadata page must not reach Backend')
        async with httpx.AsyncClient(base_url='https://graph.invalid', transport=httpx.MockTransport(no_backend)) as http:
            backend = AsyncStratifyX(base_url='https://backend.invalid', token='fixture', httpx_client=http)
            client = DatasetClient()
            client.backend = backend
            with pytest.raises(ValueError, match='integer in 1..10'):
                await client.read_dataset_search('owned-result', limit=limit)
            tools = AgentToolsClient(LangGraphClient(http), backend, http)
            async with Client(create_server(tools)) as mcp:
                listed = await mcp.list_tools()
                read = next(tool for tool in listed.tools if tool.name == 'epoch_read')
                assert read.input_schema['properties']['limit']['minimum'] == 1
                assert read.input_schema['properties']['limit']['maximum'] == 10
                result = await mcp.call_tool('epoch_read', {
                    'kind': 'dataset_search', 'identifier': 'owned-result', 'limit': limit,
                })
                assert result.is_error
    asyncio.run(scenario())


@pytest.mark.parametrize('limit', [1, 10])
def test_metadata_page_minimum_and_maximum_reach_native_unchanged(limit):
    async def scenario():
        from epoch_sdk.datasets import DatasetClient
        search = fixture('search')
        seen = []
        def read(request):
            body = json.loads(request.content)
            assert body['limit'] == limit
            assert body['cursor'] == 'native-cursor'
            assert body['result_refs'] == ['owned-result']
            seen.append(request)
            return httpx.Response(200, json={
                'columns': [], 'rows': [], 'records': [], 'result_refs': ['owned-result'],
                'original_receipts': [search['receipt']], 'receipts': [search['receipt']],
                'returned': 0, 'total_matching': 0, 'total_stored': 0, 'has_more': False,
            })
        async with httpx.AsyncClient(transport=httpx.MockTransport(read)) as http:
            client = DatasetClient()
            client.backend = AsyncStratifyX(base_url='https://backend.invalid', token='fixture', httpx_client=http)
            await client.read_dataset_search('owned-result', cursor='native-cursor', limit=limit)
            assert len(seen) == 1
    asyncio.run(scenario())


@pytest.mark.parametrize('status', [400, 401, 403, 404, 409, 410, 413, 422, 429, 502, 503, 504])
@pytest.mark.parametrize('route', ['search', 'catalog', 'read', 'screen'])
def test_native_discovery_failure_reaches_sdk_and_mcp_without_retry_or_replacement(status, route):
    """Transport contract cases, not live auth/expiry/provider-fault evidence.

    Owner, expiry, wrong-kind and cursor semantics belong to native store/HTTP
    tests. Both clients must preserve their rejection instead of retrying,
    rescreening, replacing a result or converting it into an empty response.
    """
    async def scenario():
        calls = []
        failure = {
            'error': 'MetadataProviderFailure',
            'message': f'{route}: owner, expiry, cursor or provider rejection remains visible',
            'timestamp': '2026-10-22T12:00:00Z',
        }
        def native(request):
            expected = {
                'search': '/api/v1/discovery/datasets/search',
                'catalog': '/api/v1/discovery/catalog',
                'read': '/api/v1/discovery/query-stored',
                'screen': '/api/v1/discovery/assets/screen',
            }
            assert request.method == 'POST' and request.url.path == expected[route]
            body = json.loads(request.content)
            if route == 'search':
                assert body['requests'] == [QUERY]
            elif route == 'read':
                assert body['result_refs'] == ['owned-result']
                assert body['cursor'] == 'native-cursor'
                assert body['limit'] == 1
            elif route == 'screen':
                assert body == {'kind': 'saved', 'universe_ref': 'owned-cohort'}
            calls.append(request)
            return httpx.Response(status, json=failure)
        def graph(request):
            assert request.method == 'GET' and request.url.path == '/api/v1/agent-tools'
            return httpx.Response(200, json=CATALOG)
        async with (
            httpx.AsyncClient(transport=httpx.MockTransport(native)) as native_http,
            httpx.AsyncClient(base_url='https://graph.invalid', transport=httpx.MockTransport(graph)) as graph_http,
        ):
            backend = AsyncStratifyX(base_url='https://backend.invalid', token='fixture', httpx_client=native_http)
            tools = AgentToolsClient(LangGraphClient(graph_http), backend, graph_http)
            with pytest.raises(ApiError) as rejected:
                if route == 'search':
                    await tools.search_dataset([DatasetSearchQuery.model_validate(QUERY)])
                elif route == 'catalog':
                    await tools.dataset_catalog(include_saved=True, saved_cursor='native-cursor')
                elif route == 'read':
                    await tools.read_dataset_search('owned-result', cursor='native-cursor', limit=1)
                else:
                    await tools.screen_assets(TypeAdapter(ScreenAssetsRequest).validate_python({
                        'kind': 'saved', 'universe_ref': 'owned-cohort',
                    }))
            assert rejected.value.status_code == status
            from stratifyx.types.error_response import ErrorResponse as NativeErrorResponse
            body = rejected.value.body
            if isinstance(body, NativeErrorResponse):
                body = body.model_dump(mode='json', by_alias=True, exclude_unset=True)
            assert body == failure
            assert len(calls) == 1
            async with Client(create_server(tools)) as mcp:
                if route == 'search':
                    result = await mcp.call_tool('epoch_search_dataset', {'requests': [QUERY]})
                elif route == 'catalog':
                    result = await mcp.call_tool('epoch_dataset_catalog', {
                        'include_saved': True, 'saved_cursor': 'native-cursor',
                    })
                elif route == 'read':
                    result = await mcp.call_tool('epoch_read', {
                        'kind': 'dataset_search', 'identifier': 'owned-result',
                        'cursor': 'native-cursor', 'limit': 1,
                    })
                else:
                    result = await mcp.call_tool('epoch_screen_assets', {
                        'request': {'kind': 'saved', 'universe_ref': 'owned-cohort'},
                    })
                assert result.is_error
                assert result.structured_content == {'http_status': status, 'backend_error': failure}
                assert failure['message'] in result.content[0].text
            assert len(calls) == 2
    asyncio.run(scenario())
