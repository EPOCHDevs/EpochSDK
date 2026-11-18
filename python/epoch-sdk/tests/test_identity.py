import asyncio
import json
from pathlib import Path

import httpx
import pytest
from pydantic import ValidationError

from epoch_sdk.identity import IdentityClient, IdentityHTTPError
from epoch_sdk.identity_types import AssetSpecification

FIXTURES = Path(__file__).resolve().parents[3] / "contracts" / "fixtures" / "native-identity"


def test_native_metadata_fixtures_and_exact_integers():
    for name, expected in [
        ("adr-false.json", False),
        ("adr-true.json", True),
        ("adr-absent.json", None),
    ]:
        data = json.loads((FIXTURES / name).read_text())
        asset = AssetSpecification.model_validate(data)
        assert asset.stock_profile.is_adr is expected
        assert asset.min_tick == 0.01
        assert asset.name_aliases == []
        with pytest.raises(ValidationError):
            AssetSpecification.model_validate({**data, "unexpected": True})
    asset = AssetSpecification.model_validate_json(
        '{"id":"BIG-Stocks","name_aliases":[],"symbol_changes":[],"ipo_shares":9007199254740993}'
    )
    assert asset.ipo_shares == 9007199254740993


def test_pinned_listing_and_anonymous_access():
    async def run():
        calls = []

        def send(request):
            calls.append(request)
            return httpx.Response(
                200,
                json={
                    "kind": "single",
                    "asset_id": "OLD-Stocks",
                    "image": {
                        "identity": "asset:OLD-Stocks",
                        "state": "unverified",
                        "url": "/api/v1/images/test",
                    },
                },
            )

        client = IdentityClient("https://api.example", transport=httpx.MockTransport(send))
        try:
            result = await client.get_asset_logos(
                "OLD-Stocks", listing_catalogue="a" * 64, listing_selected_at="2026-11-17T00:00:00Z"
            )
            assert result.asset_id == "OLD-Stocks"
            assert calls[0].url.params["listing_catalogue"] == "a" * 64
            assert "authorization" not in calls[0].headers
            with pytest.raises(ValueError, match="another asset"):
                await client.get_asset_logos("OTHER-Stocks")
        finally:
            await client.aclose()

    asyncio.run(run())


def test_identity_failure_has_no_native_fallback_or_retry():
    async def run():
        calls = []

        def send(request):
            calls.append(request)
            return httpx.Response(503, json={"error": "unavailable"})

        client = IdentityClient(
            "https://api.example", "caller-token", transport=httpx.MockTransport(send)
        )
        try:
            with pytest.raises(IdentityHTTPError) as raised:
                await client.get_country_catalog()
            assert raised.value.response.status_code == 503
            assert len(calls) == 1
            assert calls[0].headers["authorization"] == "Bearer caller-token"
        finally:
            await client.aclose()

    asyncio.run(run())


def test_wire_validation_rejects_null_for_a_nonnullable_enum():
    async def run():
        def send(request):
            return httpx.Response(
                200,
                json={
                    "id": "AAPL-Stocks",
                    "name_aliases": [],
                    "symbol_changes": [],
                    "asset_class": None,
                },
            )

        client = IdentityClient("https://api.example", transport=httpx.MockTransport(send))
        try:
            with pytest.raises(ValueError, match="Invalid Platform identity response"):
                await client.get_asset_information("AAPL-Stocks")
        finally:
            await client.aclose()

    asyncio.run(run())


def test_exact_metadata_cannot_be_replaced_by_another_asset():
    async def run():
        def send(request):
            return httpx.Response(
                200, json={"id": "OTHER-Stocks", "name_aliases": [], "symbol_changes": []}
            )

        client = IdentityClient("https://api.example", transport=httpx.MockTransport(send))
        try:
            with pytest.raises(ValueError, match="another asset"):
                await client.get_asset_information("AAPL-Stocks")
            assert (await client.get_asset_information("OTHER-Stocks")).id == "OTHER-Stocks"
        finally:
            await client.aclose()

    asyncio.run(run())
