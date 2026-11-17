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
