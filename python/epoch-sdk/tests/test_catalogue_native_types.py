"""Platform envelopes retain actual compiler leaves after native search retirement."""
import asyncio
import json
from pathlib import Path

import httpx
import pytest
from pydantic import ValidationError

from epoch_sdk.catalogue import CatalogueClient
from epoch_sdk.catalogue_types import CatalogueRequest, CatalogueResult
from epoch_sdk.legacy_discovery_types import DiscoveryStoredQueryResponse
from epoch_sdk.discovery_types import DiscoveryQuery, DiscoveryResult


def test_actual_native_directory_entry_roundtrips_in_its_platform_envelope():
    body=json.loads((Path(__file__).parent/'fixtures/catalogue_native_source.json').read_text())
    parsed=CatalogueResult.model_validate(body)
    assert parsed.sources[0].source.source_id==body['sources'][0]['source']['source_id']
    assert parsed.model_dump(mode='json',by_alias=True,exclude_unset=True)==body
    with pytest.raises(ValidationError):
        CatalogueResult.model_validate({**body,'invented':True})


def test_catalogue_and_private_inventory_use_platform_only():
    async def run():
        calls=[]
        def transport(request):
            calls.append(request)
            assert request.url.host=='platform.invalid'
            if request.method=='GET':
                assert request.url.path=='/api/v1/files/datasets'
                assert request.url.params['query']=='earnings & notes'
                assert request.url.params['cursor']=='next/token'
                assert request.url.params['limit']=='7'
                return httpx.Response(200,json={'items':[],'next_cursor':'later'})
            return httpx.Response(200,json={'registry_version':'v1','loader_registry_version':'r1','overview':'Sources','sources':[]})
        async with httpx.AsyncClient(transport=httpx.MockTransport(transport)) as http:
            client=CatalogueClient('https://platform.invalid','owner-token',http=http)
            result=await client.dataset_catalog(CatalogueRequest(include_saved=False))
            assert result.registry_version=='v1'
            saved=await client.list_saved_datasets(query='earnings & notes',cursor='next/token',limit=7)
            assert saved.next_cursor=='later'
        assert len(calls)==2
        assert all(request.headers['Authorization']=='Bearer owner-token' for request in calls)
    asyncio.run(run())


def test_frozen_platform_legacy_reader_keeps_exact_scalar_values_and_closed_shape():
    body={'records':[],'columns':[],'rows':[['9007199254740993',None,False]],
          'result_refs':[],'receipts':[],'original_receipts':[],
          'total_stored':1,'total_matching':1,'returned':1,'has_more':False}
    value=DiscoveryStoredQueryResponse.model_validate(body)
    assert value.model_dump(mode='json',by_alias=True,exclude_unset=True)==body
    with pytest.raises(ValidationError):
        DiscoveryStoredQueryResponse.model_validate({**body,'invented':True})


@pytest.mark.parametrize('population', [{'kind':'assets','asset_ids':['asset-a','asset-b']},
    {'kind':'universe','universe_ref':'universe:'+'a'*64}])
def test_requested_population_roundtrips_exactly_through_client_and_need(population):
    async def run():
        request=DiscoveryQuery.model_validate({'id':'prices','query':'Daily prices','mode':'exact','population':population})
        body={'format':'epoch-search-v4','session_id':'search:one','needs':[{'id':'prices','population':population,
            'status':'no_match','candidates':[],'next_cursor':None,'completeness':'complete'}],
            'candidates':[],'saved':[],'omitted':0}
        def transport(message):
            assert json.loads(message.content)['requests'][0]['population']==population
            return httpx.Response(200,json=body)
        async with httpx.AsyncClient(transport=httpx.MockTransport(transport)) as http:
            result=await CatalogueClient('https://platform.invalid','owner-token',http=http).search_dataset([request])
        assert result.model_dump(mode='json',exclude_unset=True)==body
        assert DiscoveryResult.model_validate(body).needs[0].population is not None
    asyncio.run(run())


@pytest.mark.parametrize('population', [{'kind':'assets','asset_ids':[]}, {'kind':'assets','asset_ids':['asset-a'],'invented':True},
    {'kind':'assets','asset_ids':['asset-a','asset-a']},
    {'asset_ids':['asset-a']}, {'kind':'universe','universe_ref':'not-a-reference'}])
def test_closed_requested_population_rejects_invalid_client_shapes(population):
    with pytest.raises(ValidationError):
        DiscoveryQuery.model_validate({'id':'one','query':'Prices','mode':'exact','population':population})


def test_duplicate_population_echo_is_rejected_in_native_result_model():
    with pytest.raises(ValidationError):
        DiscoveryResult.model_validate({'format':'epoch-search-v4','session_id':'search:one',
            'needs':[{'id':'one','population':{'kind':'assets','asset_ids':['asset-a','asset-a']},
                      'status':'no_match','candidates':[],'next_cursor':None,'completeness':'complete'}],
            'candidates':[],'saved':[],'omitted':0})


def test_client_revalidates_mutated_nested_population_before_any_http():
    async def run():
        query=DiscoveryQuery.model_validate({'id':'one','query':'Prices','mode':'exact',
            'population':{'kind':'assets','asset_ids':['asset-b','asset-a']}})
        # Frozen model attributes do not freeze the contents of a list.
        query.population.asset_ids.append('asset-a')
        calls=[]
        def transport(request):
            calls.append(request)
            raise AssertionError('Invalid population must not reach HTTP')
        async with httpx.AsyncClient(transport=httpx.MockTransport(transport)) as http:
            with pytest.raises(ValidationError):
                await CatalogueClient('https://platform.invalid','owner-token',http=http).search_dataset([query])
        assert calls==[]
    asyncio.run(run())


def test_client_rejects_duplicate_echo_without_coercing_result_order():
    async def run():
        query=DiscoveryQuery.model_validate({'id':'one','query':'Prices','mode':'exact',
            'population':{'kind':'assets','asset_ids':['asset-b','asset-a']}})
        calls=[]
        def transport(request):
            calls.append(request)
            assert json.loads(request.content)['requests'][0]['population']['asset_ids']==['asset-b','asset-a']
            return httpx.Response(200,json={'format':'epoch-search-v4','session_id':'search:one',
                'needs':[{'id':'one','population':{'kind':'assets','asset_ids':['asset-a','asset-a']},
                          'status':'no_match','candidates':[],'next_cursor':None,'completeness':'complete'}],
                'candidates':[],'saved':[],'omitted':0})
        async with httpx.AsyncClient(transport=httpx.MockTransport(transport)) as http:
            with pytest.raises(ValidationError):
                await CatalogueClient('https://platform.invalid','owner-token',http=http).search_dataset([query])
        assert len(calls)==1
    asyncio.run(run())


@pytest.mark.parametrize('coverage', [None, {'status': 'unknown', 'discontinued': False},
                                      {'status': 'unavailable', 'discontinued': True}])
def test_retained_provider_coverage_does_not_infer_availability_or_feedability(coverage):
    metadata = {'data_source_id': 'TradingEconomics:United States:GDP',
                'vendor': 'trading_economics', 'queried_at': '2026-11-17T00:00:00Z',
                'provider_endpoint': 'historical', 'feedable': False}
    if coverage is not None:
        metadata['provider_coverage'] = coverage
    record = {'record_ref': 'discovery-record:v1:'+'a'*64, 'request_id': 'saved',
              'request_item_id': 'item', 'status': 'resolved', 'availability': 'unknown',
              'coverage_basis': 'unknown', 'qualifications': [],
              'identity': {'kind': 'te_indicator', 'country': 'United States', 'indicator': 'GDP'},
              'metadata': metadata}
    body = {'records': [record], 'columns': [], 'rows': [], 'result_refs': [], 'receipts': [],
            'original_receipts': [], 'total_stored': 1, 'total_matching': 1,
            'returned': 1, 'has_more': False}
    parsed = DiscoveryStoredQueryResponse.model_validate(body)
    assert parsed.model_dump(mode='json', by_alias=True, exclude_unset=True) == body
    with pytest.raises(ValidationError):
        DiscoveryStoredQueryResponse.model_validate({**body, 'records': [{**record,
            'metadata': {**metadata, 'provider_coverage': {'status': 'unknown', 'invented': True}}}]})
