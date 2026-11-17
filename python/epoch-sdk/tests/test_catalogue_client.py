import asyncio
import httpx
import pytest
from epoch_sdk.catalogue import CatalogueClient
from epoch_sdk.discovery_types import DiscoveryQuery
from epoch_sdk.discovery_types import UniverseBinding
from epoch_sdk.catalogue import native_universe_screen


def test_universe_binding_preserves_native_integer_and_recursive_boolean_wire():
    binding=UniverseBinding.model_validate({
        "format":"epoch-universe-binding-v1","universe_ref":"universe:"+"a"*64,"generation":"v1",
        "ids":["AAPL-Stocks"],
        "screen":{"all_of":[{"ids":["AAPL-Stocks"]},{"asset_class":["Stocks"],"ipo_shares_min":"9007199254740993"}],"max_assets":20000},
        "definition":{"screen":{"ids":["AAPL-Stocks"]}},
        "selection":{"selection_semantics":"StaticCatalog","requires_point_in_time_gate":False,"point_in_time_indexes":[]},
    })
    source=native_universe_screen(binding)
    wire=source.model_dump(mode="json",by_alias=True,exclude_none=True)
    assert type(wire["max_assets"]) is int and wire["max_assets"]==20000
    assert wire["any_of"]==[]
    assert wire["all_of"][0]["all_of"]==wire["all_of"][0]["any_of"]==[]
    assert wire["all_of"][1]["ipo_shares_min"]==9007199254740993


def test_platform_request_and_closed_response():
    async def run():
        seen = []
        def handler(request):
            seen.append(request)
            return httpx.Response(200, json={"format":"epoch-search-v4","session_id":"search:test","needs":[],"candidates":[],"saved":[],"omitted":0})
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
            client = CatalogueClient("https://api.example.test", "token", http=http)
            result = await client.search_dataset([DiscoveryQuery(id="one", query="electricity", mode="discover")])
            assert result.format == "epoch-search-v4"
            assert seen[0].url.path == "/api/v1/discovery/datasets/search"
            assert seen[0].headers["authorization"] == "Bearer token"
            assert b'"budget":40000' in seen[0].content
    asyncio.run(run())


def test_response_bound_and_origin():
    with pytest.raises(ValueError):
        CatalogueClient("http://external.example", "token")
    async def run():
        async with httpx.AsyncClient(transport=httpx.MockTransport(lambda _: httpx.Response(200, content=b"x"*40001))) as http:
            client = CatalogueClient("https://api.example.test", "token", http=http)
            with pytest.raises(ValueError, match="exceeds"):
                await client.search_dataset([DiscoveryQuery(id="one", query="x", mode="exact")])
    asyncio.run(run())
