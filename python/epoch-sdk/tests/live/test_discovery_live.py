"""Opt-in Platform/GDS acceptance over the retained discovery intent corpus.

Constructor selectors/windows remain authoring contracts. This runner checks
identities, product bindings, complete universes, and owned replay through the
current SDK. It never launches the retired composable MCP or calls Backend search.
"""
from __future__ import annotations

import asyncio
import importlib.metadata
import json
import os
from pathlib import Path

import pytest
from pydantic import TypeAdapter
from stratifyx.types import DatasetCatalogRequest, ScreenAssetsRequest

from epoch_sdk.catalogue import CatalogueClient
from epoch_sdk.datasets import DatasetClient
from epoch_sdk.discovery_types import DiscoveryQuery, UniversePageRequest

FIXTURES = Path(__file__).parent / "fixtures"
GROUPS = ["catalog", "fundamentals", "corporate_actions", "macro", "instruments", "market", "screens", "boundaries", "queries"]
CASES = [case for group in GROUPS for case in json.loads((FIXTURES / (group + ".json")).read_text())["cases"]]
pytestmark = [pytest.mark.live_discovery, pytest.mark.skipif(os.environ.get("EPOCH_LIVE_DISCOVERY") != "1", reason="Explicitly opt in with EPOCH_LIVE_DISCOVERY=1")]
PROVIDERS = {"macrobond": "Macrobond", "trading_economics": "TradingEconomics", "Macrobond": "Macrobond", "TradingEconomics": "TradingEconomics"}


def queries(case: dict) -> list[DiscoveryQuery]:
    result = []
    for index, request in enumerate(case["request"]["requests"]):
        products = request.get("datasets") or [None]
        for number, subject in enumerate(request["subjects"]):
            for product_number, product in enumerate(products):
                filters = {}
                if product:
                    filters["categories"] = [product["category"]]
                kind = subject["kind"]
                mode = "exact"
                if kind in {"asset", "symbol", "asset_name"}:
                    query = subject.get("asset_id") or subject.get("ticker") or subject.get("symbol") or subject.get("name")
                    if subject.get("asset_type"):
                        filters["asset_classes"] = [subject["asset_type"]]
                    if subject.get("exchange"):
                        filters["exchanges"] = [subject["exchange"]]
                    mode = "discover" if kind == "asset_name" else "exact"
                elif kind == "macro_concept":
                    query, mode = subject["concept"], "discover"
                    if subject.get("geographies"):
                        filters["countries"] = subject["geographies"]
                    if subject.get("providers"):
                        filters["providers"] = [PROVIDERS[p] for p in subject["providers"]]
                    if subject.get("macrobond"):
                        filters["macrobond"] = subject["macrobond"]
                elif kind == "source":
                    address = subject["address"]
                    family = address["kind"]
                    if family == "asset":
                        query = address.get("asset_id") or address["ticker"]
                        filters["asset_classes"] = [address["asset_type"]]
                    elif family == "series":
                        query = address["series_id"]
                        filters["providers"] = [PROVIDERS[address["vendor"]]]
                    elif family == "te_market":
                        query = address["symbol"]
                        filters["providers"] = ["TradingEconomics"]
                    elif family == "te_indicator":
                        query, mode = address["indicator"], "discover"
                        filters.update(countries=[address["country"]], providers=["TradingEconomics"])
                    elif family == "te_ratings":
                        query, mode = address["country"], "discover"
                        filters.update(countries=[address["country"]], providers=["TradingEconomics"])
                    elif family == "mb_release":
                        query = address["release_id"]
                        filters.update(providers=["Macrobond"], kinds=["release"])
                    elif family == "global_source":
                        # Shared constructors belong to the directory, not an invented data identity.
                        continue
                    else:
                        raise AssertionError(f"Unmapped retained source kind: {family}")
                else:
                    raise AssertionError(f"Unmapped retained subject kind: {kind}")
                result.append(DiscoveryQuery(id=f"{index}:{number}:{product_number}", query=query, mode=mode, filters=filters or None))
    return result


def identifier_matches(candidate, expected: str) -> bool:
    values = {candidate.source_id, *(item.value for item in candidate.identifiers)}
    if expected in values:
        return True
    ticker, _, asset_class = expected.rpartition("-")
    return asset_class in {"Stocks", "FX", "Crypto", "Futures"} and ticker in values


def expected_identifier(identity: dict) -> str | None:
    return next((identity[key] for key in ("asset_id", "series_id", "symbol", "release_id", "ticker") if identity.get(key)), None)


async def exercise(case: dict, receipt: dict):
    origin = os.environ["EPOCH_PLATFORM_URL"]
    client = CatalogueClient(origin, os.environ["EPOCH_TOKEN"])
    data = DatasetClient()
    data.catalogue = client
    try:
        if case["operation"] == "catalog":
            response = await client.dataset_catalog(DatasetCatalogRequest.model_validate(case["request"]))
            receipt["response"] = response.model_dump(mode="json", by_alias=True, exclude_unset=True)
            assert {source.source.source_id for source in response.sources} == set(case["expected_source_ids"])
            assert response.loader_registry_version and response.registry_version
            return
        if case["operation"] == "screen":
            request = TypeAdapter(ScreenAssetsRequest).validate_python(case["request"])
            response = await data.screen_assets(request)
            receipt["response"] = response.model_dump(mode="json", by_alias=True, exclude_unset=True)
            assert response.status == "ready", receipt["response"]
            assert response.asset_count >= case.get("minimum_members", 1)
            assert response.selection.requires_point_in_time_gate == case.get("point_in_time", False)
            assert response.universe_ref
            records, cursor = [], None
            while True:
                page = await client.universe_page(UniversePageRequest(universe_ref=response.universe_ref, limit=100, cursor=cursor))
                records.extend(page.records)
                if not page.next_cursor:
                    break
                assert page.next_cursor != cursor
                cursor = page.next_cursor
            assert len(records) == response.asset_count and len({row.id for row in records}) == len(records)
            wanted = case.get("expected_asset_ids")
            if wanted is not None:
                actual = {row.id for row in records} | {row.ticker + "-" + row.asset_class for row in records}
                assert set(wanted) <= actual and len(wanted) == len(records)
            assert set(case.get("required_asset_ids", [])) <= ({row.id for row in records} | {row.ticker + "-" + row.asset_class for row in records})
            if case.get("check_saved_reuse"):
                assert await client.screen_assets({"kind":"saved", "universe_ref":response.universe_ref}) == response
            return
        expected = case["expected"]
        if expected["kind"] == "http_error":
            pytest.skip("Retained constructor-selector error belongs to native authoring validation; not a v4 search parameter")
        requests = queries(case)
        if not requests:
            pytest.skip("Constructor-only intent is covered by the published directory cases")
        candidates = []
        receipt["responses"] = []
        for offset in range(0, len(requests), 32):
            response = await client.search_dataset(requests[offset:offset+32], limit=case["request"].get("candidate_limit") or 10)
            receipt["responses"].append(response.model_dump(mode="json", by_alias=True, exclude_unset=True))
            assert not any(need.status in {"error", "incomplete"} for need in response.needs), receipt["responses"]
            candidates.extend(response.candidates)
        if expected["kind"] in {"unknown", "unavailable"}:
            assert not candidates or all(getattr(row, "support", None) is not None and row.support.state != "qualified" for row in candidates)
            return
        if expected["kind"] == "identities":
            assert any(identifier_matches(row, wanted) for wanted in expected["relevant_ids"] for row in candidates[:expected["top_k"]])
        elif expected["kind"] == "series":
            for identity in expected["relevant_identities"]:
                wanted = identity.get("series_id") or identity.get("symbol")
                if wanted:
                    assert any(identifier_matches(row, wanted) for row in candidates[:expected["top_k"]])
        elif expected["kind"] == "bindings":
            wanted = expected_identifier(expected["identity"])
            if wanted:
                assert any(identifier_matches(row, wanted) for row in candidates)
            # Selection verifies the actual registered constructor, not a copied display name.
            selected_sources = []
            for response_value in receipt["responses"]:
                chosen = [candidate.id for candidate in candidates if getattr(candidate, "support", None) is not None and candidate.support.state == "qualified" and (not wanted or identifier_matches(candidate, wanted)) and candidate.id in {row["id"] for row in response_value["candidates"]}]
                if chosen:
                    selection = await client.select(response_value["session_id"], chosen)
                    selected_sources.extend(selection.sources)
            assert set(expected["source_ids"]) <= {source.binding.source_id for source in selected_sources if source.binding}
        elif expected["kind"] == "batch":
            for row in expected["rows"]:
                wanted = expected_identifier(row["identity"]) if row.get("identity") else None
                if wanted and row["status"] != "unknown":
                    matches = [candidate for candidate in candidates if identifier_matches(candidate, wanted)]
                    assert matches, row
                    if row.get("requested_dataset"):
                        assert any(candidate.product == row["requested_dataset"]["category"] for candidate in matches), row
                elif row["status"] == "unknown":
                    assert any(need["status"] == "no_match" for response in receipt["responses"] for need in response["needs"]), row
        else:
            raise AssertionError("Unmapped retained expectation: " + expected["kind"])
    finally:
        await client.aclose()


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["id"])
def test_discovery_live(case):
    folder = Path(os.environ["EPOCH_LIVE_DISCOVERY_ARTIFACT_DIR"])
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / (case["id"] + ".json")
    assert not path.exists(), "Use a fresh evidence directory; never overwrite the first outcome"
    receipt = {"case":case,"client":"Platform CatalogueClient","epoch_sdk_version":importlib.metadata.version("epoch-sdk")}
    try:
        asyncio.run(exercise(case, receipt))
    finally:
        path.write_text(json.dumps(receipt, indent=2) + "\n")
