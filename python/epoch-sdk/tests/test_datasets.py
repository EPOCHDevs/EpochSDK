"""Direct SDK data-contract checks; the retired composable MCP is not mounted."""
import asyncio
import json
from copy import deepcopy
from pathlib import Path
import httpx
import pytest
from pydantic import ValidationError
from stratifyx import AsyncStratifyX
from stratifyx.core.api_error import ApiError
from epoch_sdk.datasets import DatasetClient
from epoch_sdk.catalogue import CatalogueClient, CatalogueHTTPError
from epoch_sdk.discovery_types import DiscoveryQuery
FIXTURES=Path(__file__).parent/'fixtures/dataset_search'
QUERY={"id":"company","query":"Apple","mode":"discover"}
def fixture(name):return json.loads((FIXTURES/(name+'.response.json')).read_text())

def malformed_inputs():
    for name, values in {
        'candidate_limit': (True, 1.0, '2', 0, 26),
    }.items():
        for value in values:
            yield 'search', {'requests': [QUERY], name: value}
    for name, values in {
        'saved_limit': (None, True, 1.0, '2', 0, 101),
        'include_saved': (None, 0, 1, 'true', 'false'),
        'include_details': (None, 0, 1, 'true', 'false'),
        'source_ids': (False, '', 'cash_flow', 0),
    }.items():
        for value in values:
            yield 'catalog', {name: value}
    vintage = {
        'request_id': 'macro',
        'subjects': [{'kind': 'macro_concept', 'concept': 'Real US GDP'}],
        'datasets': [{'category': 'MacrobondVintageData',
                      'selectors': {'kind': 'vintage', 'revision': 'NthFromLast', 'nth': 2}}],
    }
    for name, values in {
        'nth': (True, 1.0, '2'), 'full_tape': (0, 1, 'true', 'false'),
    }.items():
        for value in values:
            query = deepcopy(vintage)
            query['datasets'][0]['selectors'][name] = value
            yield 'search', {'requests': [query]}
    for name in ('include_discontinued', 'must_have_revisions'):
        for value in (0, 1, 'false', 'true'):
            query = deepcopy(vintage)
            query['subjects'][0]['macrobond'] = {
                'category': [], 'currency': [], 'data_type': [], 'exchange': [],
                'frequency': [], 'klass': [], name: value,
            }
            yield 'search', {'requests': [query]}
    for name, values in {
        'ipo_shares_min': (True, 1.0, 2), 'ipo_shares_max': (True, 1.0, 2),
        'max_assets': (True, 1.0, '2'),
        'ipo_price_min': (True, '2', float('inf'), float('-inf'), float('nan')),
        'ipo_price_max': (True, '2', float('inf'), float('-inf'), float('nan')),
        'ipo_market_cap_min': (True, '2', float('inf'), float('-inf'), float('nan')),
        'ipo_market_cap_max': (True, '2', float('inf'), float('-inf'), float('nan')),
    }.items():
        for value in values:
            screen = {'all_of': [], 'any_of': [], name: value}
            # A nested "not" exercises the foreign recursive request component.
            yield 'screen', {'request': {'kind': 'screen', 'screen': {
                'all_of': [], 'any_of': [], 'not': screen,
            }}}
    for request in ({'kind': 'saved', 'universe_ref': 'owned-cohort'},
                    {'kind': 'screen', 'screen': {'all_of': [], 'any_of': []}}):
        for name in ('current_cap_min_exclusive', 'current_cap_max_exclusive'):
            for value in (True, '2', float('inf'), float('-inf'), float('nan')):
                yield 'screen', {'request': {**request, name: value}}

@pytest.mark.parametrize('route,arguments',[(route,args) for route,args in malformed_inputs() if route!='search'])
def test_existing_catalogue_and_screen_reject_coercion_before_transport(route,arguments):
    async def run():
        def denied(_):pytest.fail('Invalid input reached transport')
        async with httpx.AsyncClient(transport=httpx.MockTransport(denied)) as http:
            client=DatasetClient();client.backend=AsyncStratifyX(base_url='https://backend.invalid',token='fixture',httpx_client=http);client.catalogue=CatalogueClient('https://platform.invalid','fixture',http=http)
            with pytest.raises(ValidationError):
                if route=='catalog':await client.dataset_catalog(**arguments)
                else:await client.screen_assets(**arguments)
    asyncio.run(run())

@pytest.mark.parametrize('limit',[None,0,11,100,True,1.0,1.5,'10'])
def test_historical_metadata_page_bound_is_enforced_before_transport(limit):
    async def run():
        async with httpx.AsyncClient(transport=httpx.MockTransport(lambda _:pytest.fail('Invalid page reached transport'))) as http:
            client=DatasetClient();client.backend=AsyncStratifyX(base_url='https://backend.invalid',token='fixture',httpx_client=http);client.catalogue=CatalogueClient('https://platform.invalid','fixture',http=http)
            with pytest.raises(ValueError):await client.read_dataset_search('old-result',limit=limit)
    asyncio.run(run())

@pytest.mark.parametrize('operation',['catalog','screen'])
@pytest.mark.parametrize('status',[400,401,403,404,409,410,413,422,429,502,503,504])
def test_native_metadata_failures_are_not_retried(operation,status):
    async def run():
        calls=[]
        def fail(request):calls.append(request);return httpx.Response(status,json={'error':'ServiceUnavailable','message':'Explicit failure','timestamp':'2026-11-17T00:00:00Z'})
        async with httpx.AsyncClient(transport=httpx.MockTransport(fail)) as http:
            client=DatasetClient();client.backend=AsyncStratifyX(base_url='https://backend.invalid',token='fixture',httpx_client=http);client.catalogue=CatalogueClient('https://platform.invalid','fixture',http=http)
            with pytest.raises((ApiError,CatalogueHTTPError)):
                if operation=='catalog':await client.dataset_catalog()
                else:await client.screen_assets({'kind':'saved','universe_ref':'owned-cohort'})
        assert len(calls)==1
    asyncio.run(run())

def test_screen_keeps_the_complete_native_membership_definition():
    async def run():
        native={'format':'epoch-universe-v1','universe_ref':'universe:'+'a'*64,'generation':'v1','created_at':'2026-11-17T00:00:00Z','status':'ready','asset_count':2,'matched':2,'definition':{'screen':{'ids':['AAPL-Stocks','MSFT-Stocks']}},'selection':{'selection_semantics':'StaticCatalog','requires_point_in_time_gate':False,'point_in_time_indexes':[]},'sample':[],'facets':{},'excluded_count':0,'exclusions':[]};calls=[]
        def handle(request):calls.append(request);assert request.url.host=='platform.invalid';assert request.url.path.endswith('/assets/screen');return httpx.Response(200,json=native)
        async with httpx.AsyncClient(transport=httpx.MockTransport(handle)) as http:
            client=DatasetClient();client.backend=AsyncStratifyX(base_url='https://backend.invalid',token='fixture',httpx_client=http);client.catalogue=CatalogueClient('https://platform.invalid','fixture',http=http)
            result=await client.screen_assets({'kind':'saved','universe_ref':'owned-cohort'})
            assert result.model_dump(mode='json',by_alias=True,exclude_unset=True)==native
        assert len(calls)==1
    asyncio.run(run())

def test_application_convenience_client_dispatches_search_to_platform_only():
    async def run():
        response={'format':'epoch-search-v4','session_id':'search:test','needs':[],'candidates':[],'saved':[],'omitted':0};calls=[]
        def handle(request):calls.append(request);assert request.url.host=='platform.invalid';return httpx.Response(200,json=response)
        async with httpx.AsyncClient(transport=httpx.MockTransport(handle)) as http:
            client=DatasetClient();client.catalogue=CatalogueClient('https://platform.invalid','fixture',http=http)
            result=await client.search_dataset([DiscoveryQuery.model_validate(QUERY)])
            assert result.format=='epoch-search-v4'
        assert len(calls)==1
    asyncio.run(run())

@pytest.mark.parametrize('limit',[False,True,0,26,1.0,'2'])
def test_search_does_not_coerce_an_invalid_limit(limit):
    async def run():
        async with httpx.AsyncClient(transport=httpx.MockTransport(lambda _:pytest.fail('Invalid limit reached Platform'))) as http:
            client=DatasetClient();client.catalogue=CatalogueClient('https://platform.invalid','fixture',http=http)
            with pytest.raises(ValueError):await client.search_dataset([DiscoveryQuery.model_validate(QUERY)],candidate_limit=limit)
    asyncio.run(run())

@pytest.mark.parametrize('value',['false',0,1,None])
def test_query_semantic_mode_is_a_real_boolean(value):
    with pytest.raises(ValidationError):DiscoveryQuery.model_validate({**QUERY,'semantic':value}) if value is not None else DiscoveryQuery.model_validate({**QUERY,'invented':value})
