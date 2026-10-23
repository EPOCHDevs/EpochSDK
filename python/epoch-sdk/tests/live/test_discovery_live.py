"""Opt-in Discovery acceptance over real SDK and registered stdio MCP paths.

Run with EPOCH_LIVE_DISCOVERY=1 and ordinary client URLs/token. Provider secrets
remain in Backend. Each test makes one public search. Explicit SDK pool reads are independent
test diagnostics and never rescue a missing first-response match; no agent
paging tool is invoked and a failed first attempt is never retried. Fixtures distinguish binding semantics
from the separate natural-language caller acceptance scenarios.
"""

import asyncio
from datetime import datetime, timezone
import importlib.metadata
import hashlib
import inspect
import json
import os
import sys
from pathlib import Path
import time
from typing import Annotated, Literal

from mcp import Client, StdioServerParameters
import pytest
from pydantic import BaseModel, ConfigDict, Field, TypeAdapter
from stratifyx.types import (
    DatasetCatalogRequest,
    DatasetCatalogResponse,
    DatasetSearchRequest,
    DiscoveryDatasetRequest,
    DiscoveryMetadataRecord,
    DiscoverySearchResponse,
    DiscoverySelectors,
    DiscoverySourceAddress,
    DiscoveryStoredQueryResponse,
    AssetUniverseResponse,
    ScreenAssetsRequest,
)
from stratifyx.core.api_error import ApiError

from epoch_sdk.research import EpochClient

FIXTURES = Path(__file__).parent / "fixtures"
pytestmark = [
    pytest.mark.live_discovery,
    pytest.mark.skipif(
        os.environ.get("EPOCH_LIVE_DISCOVERY") != "1",
        reason="Explicitly opt in with EPOCH_LIVE_DISCOVERY=1",
    ),
]


class BindingExpectation(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    kind: Literal["bindings"]
    source_ids: list[str]
    identity: DiscoverySourceAddress
    availability: Literal["unknown", "available"] | list[Literal["unknown", "available"]]
    requested_dataset: DiscoveryDatasetRequest
    status: Literal["resolved", "unknown"] = "resolved"
    effective_selectors: DiscoverySelectors | None = None
    schema_ref: str | None = None


class IdentityExpectation(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    kind: Literal["identities"]
    relevant_ids: list[str]
    top_k: int = Field(ge=1, le=5)
    reason: str
    ambiguous: bool = False
    diagnostic_relevant_ids: list[str] = []


class ErrorExpectation(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    kind: Literal["http_error"]
    status: Literal[400, 503]
    message_contains: str


class NoBindingExpectation(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    kind: Literal["unknown", "unavailable"]
    record_count: int = 1


class SeriesExpectation(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    kind: Literal["series"]
    relevant_identities: list[DiscoverySourceAddress]
    top_k: int = Field(ge=1, le=10)
    unit: str | None = None
    frequency: str | None = None
    description_fragments: list[str] = []
    required_vendors: list[Literal["macrobond", "trading_economics"]] = []
    products: list[BindingExpectation] = Field(min_length=1)


class BatchRow(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    request_item_id: str
    identity: DiscoverySourceAddress | None
    source_id: str | None = None
    requested_dataset: DiscoveryDatasetRequest | None = None
    status: Literal["resolved", "candidate", "unknown"] = "resolved"


class BatchExpectation(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    kind: Literal["batch"]
    rows: list[BatchRow]


class SearchCase(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    id: str
    group: Literal["fundamentals", "corporate_actions", "macro", "market", "instruments",
                   "boundaries", "macro_search", "batch"]
    operation: Literal["search"]
    request: DatasetSearchRequest
    expected: Annotated[BindingExpectation | IdentityExpectation | ErrorExpectation |
                        NoBindingExpectation | SeriesExpectation | BatchExpectation,
                        Field(discriminator="kind")]


class CatalogCase(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    id: str
    group: Literal["catalog"]
    operation: Literal["catalog"]
    request: DatasetCatalogRequest
    expected_source_ids: list[str]


class ScreenCase(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    id: str
    group: Literal["screens"]
    operation: Literal["screen"]
    request: ScreenAssetsRequest
    expected_asset_ids: list[str] | None = None
    required_asset_ids: list[str] = []
    minimum_members: int = 1
    point_in_time: bool = False
    check_saved_reuse: bool = False


Case = Annotated[SearchCase | CatalogCase | ScreenCase, Field(discriminator="operation")]
CASE_ADAPTER = TypeAdapter(Case)


def load_cases() -> list[SearchCase | CatalogCase | ScreenCase]:
    result = []
    for name in ("catalog.json", "fundamentals.json", "corporate_actions.json", "macro.json",
                 "instruments.json", "market.json", "screens.json", "boundaries.json",
                 "queries.json"):
        path = FIXTURES / name
        assert path.is_file(), f"Required live corpus group is missing: {name}"
        result.extend(CASE_ADAPTER.validate_python(row) for row in json.loads(path.read_text())["cases"])
    assert result, "Live acceptance corpus must not be empty"
    assert len({case.id for case in result}) == len(result), "Duplicate live case ID"
    return result


CASES = load_cases()
INVENTORY = json.loads((FIXTURES / "catalog_inventory.json").read_text())


def wire(model: BaseModel) -> dict:
    """Serialize a closed native model at the captured JSON boundary."""
    return model.model_dump(mode="json", by_alias=True, exclude_unset=True)


def contract_shape(value):
    """Freeze source-owned structure while allowing prose corrections.

    This projection is only used at the fixture JSON boundary. Column/output
    names, option defaults/ranges, routing and endpoint capabilities remain.
    """
    if isinstance(value, dict):
        return {key: contract_shape(item) for key, item in value.items()
                if key not in {"description", "display_name", "signature", "documentation"}}
    if isinstance(value, list):
        return [contract_shape(item) for item in value]
    return value


def assert_bindings(expected: BindingExpectation, records: list[DiscoveryMetadataRecord]) -> None:
    assert all(str(row.status) == expected.status for row in records), [wire(row) for row in records]
    assert len(records) == len(expected.source_ids), "Unexpected binding multiplicity"
    assert len({row.binding_ref for row in records}) == len(records), "Duplicate binding"
    assert {row.loader.source_id for row in records if row.loader} == set(expected.source_ids)
    for row in records:
        assert row.identity and wire(row.identity) == wire(expected.identity)
        assert row.loader and row.loader.schema_ref and row.loader.registry_version
        assert row.binding_ref
        allowed = (expected.availability if isinstance(expected.availability, list)
                   else [expected.availability])
        assert str(row.availability) in allowed
        if str(row.availability) == "unknown":
            assert row.qualifications, "Unknown coverage needs an explicit qualification"
        assert row.requested_dataset
        requested = row.requested_dataset
        original = expected.requested_dataset
        assert requested.category == original.category
        # Native canonicalization emits an empty field vector for an
        # omitted selection. Both mean no column narrowing; extra fields
        # must still fail the comparison.
        assert (requested.fields or []) == (original.fields or [])
        assert requested.selectors == original.selectors
        assert requested.requested_window == original.requested_window
        assert row.loader.category == expected.requested_dataset.category
        if expected.requested_dataset.selectors:
            assert row.loader.selectors
            provided = wire(expected.requested_dataset.selectors)
            actual = wire(row.loader.selectors)
            assert all(actual.get(key) == value for key, value in provided.items())
        if expected.effective_selectors is not None:
            assert row.loader.selectors
            effective = wire(row.loader.selectors)
            assert all(effective.get(key) == value
                       for key, value in wire(expected.effective_selectors).items())
        if expected.schema_ref is not None:
            assert row.loader.schema_ref == expected.schema_ref


def client_environment() -> dict[str, str]:
    required = ("EPOCH_BACKEND_URL", "EPOCH_GRAPH_URL", "EPOCH_TOKEN")
    missing = [name for name in required if not os.environ.get(name)]
    assert not missing, "Live client configuration missing: " + ", ".join(missing)
    # Only client configuration enters MCP; no vendor or model credentials.
    names = {"PATH", "HOME", "USER", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR"}
    names.update(required)
    names.add("EPOCH_MCP_GRAPH_URL")
    return {name: os.environ[name] for name in names if name in os.environ}


async def drain_records(result, page, route: str, epoch: EpochClient, mcp):
    cursors = set()

    def check_page(value):
        assert value.result_refs == [result.receipt.result_ref], "Foreign saved result page"
        assert value.total_stored == result.counts.stored_records
        assert value.total_matching == result.counts.stored_records
        assert value.returned == len(value.records)
        assert value.receipts == [result.receipt]
        assert not value.original_receipts, "Fresh search unexpectedly became an archival handoff"

    if not result.records_complete and page is None:
        page = await epoch.read_dataset_search(result.receipt.result_ref)
    records = list(page.records if page is not None else result.records)
    pages = 1 if page is not None else 0
    if page is not None:
        check_page(page)
    while page is not None and page.has_more:
        assert page.next_cursor
        assert page.next_cursor not in cursors, "Repeated saved-page cursor"
        cursors.add(page.next_cursor)
        assert len(records) < result.counts.stored_records, "More pages after declared row count"
        page = await epoch.read_dataset_search(result.receipt.result_ref, cursor=page.next_cursor)
        records.extend(page.records)
        check_page(page)
        pages += 1
    assert len(records) == result.counts.stored_records
    assert len({row.record_ref for row in records}) == len(records), "Duplicate saved records"
    return records, pages


async def search_once(case: SearchCase, route: str, epoch: EpochClient, mcp):
    began = time.monotonic()
    if route == "sdk":
        value = await epoch.search_dataset(
            case.request.requests, candidate_limit=case.request.candidate_limit
        )
        result, page = value.result, value.page
    else:
        value = await mcp.call_tool("epoch_search_dataset", wire(case.request))
        assert not value.is_error, value.model_dump(mode="json", by_alias=True)
        result = DiscoverySearchResponse.model_validate(value.structured_content["result"])
        page = (
            DiscoveryStoredQueryResponse.model_validate(value.structured_content["page"])
            if value.structured_content.get("page") else None
        )
    lookup_seconds = time.monotonic() - began
    initial_records = list(page.records if page is not None else result.records)
    records, pages = await drain_records(result, page, route, epoch, mcp)
    return result, records, pages, lookup_seconds, initial_records


async def exercise(case, route, env, receipt):
    epoch = EpochClient.connect(
        graph_url=env["EPOCH_GRAPH_URL"], backend_url=env["EPOCH_BACKEND_URL"],
        token=env["EPOCH_TOKEN"],
    )

    async def run(mcp=None):
        if isinstance(case, SearchCase) and isinstance(case.expected, ErrorExpectation):
            expected = case.expected
            if route == "sdk":
                with pytest.raises(ApiError) as failure:
                    await epoch.search_dataset(case.request.requests,
                                               candidate_limit=case.request.candidate_limit)
                receipt["http_error"] = {"status": failure.value.status_code,
                                         "message": str(failure.value.body)}
            else:
                response = await mcp.call_tool("epoch_search_dataset", wire(case.request))
                assert response.is_error, response.model_dump(mode="json", by_alias=True)
                receipt["http_error"] = {
                    "status": response.structured_content.get("http_status"),
                    "message": json.dumps(response.structured_content),
                }
            assert receipt["http_error"]["status"] == expected.status
            assert expected.message_contains.lower() in receipt["http_error"]["message"].lower()
            return
        if isinstance(case, ScreenCase):
            async def screen(request):
                if route == "sdk":
                    return await epoch.screen_assets(request)
                response = await mcp.call_tool("epoch_screen_assets", {"request": wire(request)})
                assert not response.is_error, response.model_dump(mode="json", by_alias=True)
                return AssetUniverseResponse.model_validate(response.structured_content)

            response = await screen(case.request)
            receipt["response"] = wire(response)
            assert response.universe_ref and response.definition
            records, pages = await drain_records(response.result, None, route, epoch, mcp)
            receipt.update(records=[wire(row) for row in records], saved_pages=pages)
            assert all(row.error is None and row.identity and row.identity.kind == "asset"
                       for row in records), receipt["records"]
            identities = [row.identity.ticker + "-" + str(row.identity.asset_type)
                          for row in records]
            assert len(identities) == len(set(identities)), "A screen duplicated a member"
            assert response.asset_count == len(identities), "Screen count and saved pool differ"
            assert response.result.receipt.stored_complete
            assert str(response.result.source_completeness) == "AuthoritativeComplete"
            assert len(identities) >= case.minimum_members
            if case.expected_asset_ids is not None:
                assert set(identities) == set(case.expected_asset_ids), identities
            assert set(case.required_asset_ids) <= set(identities)
            definition = response.definition
            assert definition.membership_screen == case.request.screen
            assert definition.selection.requires_point_in_time_gate == case.point_in_time
            if case.point_in_time:
                assert definition.selection.selection_semantics == "HistoricalUnion"
                assert definition.membership_window == case.request.membership_window
                assert definition.historical_integrity
            if case.check_saved_reuse:
                request = TypeAdapter(ScreenAssetsRequest).validate_python({
                    "kind": "saved", "universe_ref": response.universe_ref,
                })
                reused = await screen(request)
                receipt["saved_universe_read_calls"] = 1
                receipt["saved_reuse"] = wire(reused)
                kept, _ = await drain_records(reused.result, None, route, epoch, mcp)
                assert [wire(row.identity) for row in kept] == [wire(row.identity) for row in records]
                assert reused.asset_count == len(kept)
                assert reused.universe_ref == response.universe_ref
                assert reused.result == response.result
                assert reused.qualifications == response.qualifications
                assert reused.definition == definition, "Saved membership qualifiers changed"
            return
        if isinstance(case, CatalogCase):
            if route == "sdk":
                request = case.request
                response = await epoch.dataset_catalog(
                    source_ids=request.source_ids, include_details=request.include_details,
                    include_saved=request.include_saved, saved_limit=request.saved_limit,
                    saved_cursor=request.saved_cursor,
                )
            else:
                value = await mcp.call_tool("epoch_read", {"kind": "guide"})
                assert not value.is_error, value.model_dump(mode="json", by_alias=True)
                guide = "\n".join(part.text for part in value.content if part.type == "text")
                # Independent SDK reference proves the live MCP briefing is the
                # exact Backend prose. Detailed field schemas are an SDK/author
                # contract, not a second default supervisor catalog tool.
                response = await epoch.dataset_catalog(
                    source_ids=case.request.source_ids,
                    include_details=case.request.include_details,
                    include_saved=case.request.include_saved,
                    saved_limit=case.request.saved_limit,
                    saved_cursor=case.request.saved_cursor,
                )
                assert response.overview in guide
                receipt["catalog_reference_calls"] = 1
                receipt["mcp_briefing_sha256"] = hashlib.sha256(response.overview.encode()).hexdigest()
            receipt["response"] = wire(response)
            assert sorted(entry.source.source_id for entry in response.sources) == sorted(
                case.expected_source_ids
            )
            assert response.overview
            inventory = {entry["source_id"]: entry for entry in INVENTORY["sources"]}
            for entry in response.sources:
                assert entry.documentation
                actual = wire(entry.source)
                expected = inventory[entry.source.source_id]
                for key in ("family", "scope", "backing", "vendor", "data_categories"):
                    assert actual.get(key) == expected.get(key), (entry.source.source_id, key)
                options = {option["id"]: option for option in actual["options"]}
                assert set(options) == {option["id"] for option in expected["options"]}
                for option in expected["options"]:
                    assert all(options[option["id"]].get(key) == value
                               for key, value in option.items()), (entry.source.source_id, option)
                # Source summaries alone miss options belonging to individual
                # implementations, including futures roll/session controls.
                assert contract_shape(wire(entry)) == expected["contract"], entry.source.source_id
            return
        result, records, pages, lookup_seconds, initial_records = await search_once(case, route, epoch, mcp)
        receipt.update(result=wire(result), records=[wire(row) for row in records],
                       initial_page_records=[wire(row) for row in initial_records],
                       diagnostic_pool_pages=pages, lookup_seconds=lookup_seconds)
        expected = case.expected
        assert records, "Supported binding returned no saved records"
        if isinstance(expected, NoBindingExpectation):
            assert len(records) == expected.record_count
            assert all(str(row.status) == expected.kind and str(row.availability) == expected.kind
                       and row.loader is None for row in records), receipt["records"]
            if expected.kind == "unknown":
                assert all(row.identity is None for row in records), "Unknown identity was echoed"
                assert all(row.error and str(row.error.error_class) == "RequestShape"
                           for row in records), receipt["records"]
            else:
                assert all(row.error is None for row in records), receipt["records"]
            return
        if isinstance(expected, BatchExpectation):
            assert len(records) == len(expected.rows)
            matched = set()
            for item in expected.rows:
                selected = [row for row in records if row.request_item_id == item.request_item_id
                            and (row.loader.source_id if row.loader else None) == item.source_id
                            and (row.requested_dataset.category if row.requested_dataset else None)
                            == (item.requested_dataset.category if item.requested_dataset else None)]
                assert len(selected) == 1, (item, receipt["records"])
                row = selected[0]
                assert row.record_ref not in matched
                matched.add(row.record_ref)
                assert row.identity == item.identity and str(row.status) == item.status
                assert row.request_id + "/subject/" in row.request_item_id
                if item.requested_dataset:
                    assert row.requested_dataset
                    actual, wanted = row.requested_dataset, item.requested_dataset
                    assert actual.category == wanted.category
                    assert actual.selectors == wanted.selectors
                    assert actual.requested_window == wanted.requested_window
                    assert (actual.fields or []) == (wanted.fields or [])
                    if row.loader:
                        assert row.loader.category == wanted.category
                        assert row.loader.selectors == wanted.selectors
                        assert row.loader.schema_ref and row.loader.registry_version
                if item.status == "unknown":
                    assert row.error and str(row.error.error_class) == "RequestShape"
                    assert row.loader is None and row.identity is None
                else:
                    assert row.error is None and row.binding_ref
            assert len(matched) == len(records)
            return
        assert all(row.error is None for row in records), receipt["records"]
        revision_filtered_requests = {
            query.request_id for query in case.request.requests
            if query.subjects and all(
                subject.kind == "macro_concept" and subject.macrobond is not None
                and subject.macrobond.must_have_revisions is True
                for subject in query.subjects
            )
        }
        if revision_filtered_requests:
            macro_rows = [row for row in records
                          if row.request_id in revision_filtered_requests and row.identity is not None
                          and row.identity.kind == "series"
                          and row.identity.vendor == "macrobond"]
            assert macro_rows, "Revision filter returned no Macrobond series"
            assert all(row.metadata is not None and row.metadata.has_revision_history is True
                       for row in macro_rows), "Revision filter disagrees with returned source facts"
            receipt["revision_filtered_macrobond_rows"] = len(macro_rows)
        if isinstance(expected, SeriesExpectation):
            candidates = []
            identities = []
            for row in records:
                if not row.identity or row.availability == "unavailable":
                    continue
                identity = wire(row.identity)
                if identity not in identities:
                    identities.append(identity)
                    candidates.append(row)
            wanted = [wire(identity) for identity in expected.relevant_identities]
            receipt["ranking_quality"] = {
                "first_rank_matches": bool(initial_records and initial_records[0].identity
                                           and wire(initial_records[0].identity) in wanted),
                "relevant_record_positions": [index + 1 for index, row in enumerate(records)
                                              if row.identity and wire(row.identity) in wanted],
                "relevant_identity_positions": [index + 1 for index, identity in enumerate(identities)
                                                if identity in wanted],
                "acceptance_page_limit": expected.top_k,
            }
            delivered_by_need = {}
            for row in initial_records:
                if row.identity:
                    key = (row.request_item_id, json.dumps(wire(row.requested_dataset), sort_keys=True))
                    delivered_by_need.setdefault(key, set()).add(json.dumps(wire(row.identity), sort_keys=True))
            assert all(len(identities) <= expected.top_k for identities in delivered_by_need.values())
            receipt["acceptance_scope"] = "First response, independently bounded per subject/product; archived-pool reads are diagnostics only"
            matching = [row for row in initial_records if row.identity
                        and wire(row.identity) in wanted and row.availability != "unavailable"]
            assert matching, [wire(row.identity) if row.identity else None for row in initial_records]
            for product in expected.products:
                product_rows = [row for row in matching if row.identity == product.identity
                                and row.loader and row.loader.source_id in product.source_ids]
                assert_bindings(product, product_rows)
            for row in matching:
                assert row.metadata
                if expected.unit:
                    assert row.metadata.unit and row.metadata.unit.lower() == expected.unit.lower()
                if expected.frequency:
                    assert row.metadata.frequency and row.metadata.frequency.lower() == expected.frequency.lower()
                for fragment in expected.description_fragments:
                    assert fragment.lower() in (row.metadata.description or "").lower()
            vendors = {str(row.identity.vendor) for row in candidates
                       if row.identity.kind == "series"}
            assert set(expected.required_vendors) <= vendors
            return
        if isinstance(expected, IdentityExpectation):
            identities = []
            for row in records:
                assert row.identity and row.identity.kind == "asset"
                assert row.availability != "unavailable"
                identity = row.identity.ticker + "-" + str(row.identity.asset_type)
                if identity not in identities:
                    identities.append(identity)
            assert set(identities[:expected.top_k]) & set(expected.relevant_ids), identities
            if expected.diagnostic_relevant_ids:
                receipt["original_oracle_quality"] = {
                    "top_k_hit": bool(set(identities[:expected.top_k])
                                      & set(expected.diagnostic_relevant_ids)),
                    "positions": {identity: identities.index(identity) + 1
                                  for identity in expected.diagnostic_relevant_ids
                                  if identity in identities},
                    "scope": "Preserved narrower quality target; not broad-ambiguity authority",
                }
            if expected.ambiguous:
                assert len(identities) > 1, "An ambiguous name became an unjustified unique answer"
                assert all(str(row.status) == "candidate" for row in records)
            return
        assert_bindings(expected, records)

    try:
        if route == "sdk":
            await run()
        else:
            command = os.environ.get("EPOCH_LIVE_MCP_COMMAND")
            assert command, "Explicitly set the registered launcher in EPOCH_LIVE_MCP_COMMAND"
            launcher = Path(command).resolve(strict=True)
            receipt["mcp_launcher"] = {
                "command": command, "resolved_path": str(launcher),
                "sha256": hashlib.sha256(launcher.read_bytes()).hexdigest(),
            }
            async with Client(StdioServerParameters(command=command, args=[], env=env)) as mcp:
                await run(mcp)
    finally:
        await epoch.aclose()


@pytest.mark.parametrize("route", ["sdk", "mcp"])
@pytest.mark.parametrize("case", CASES, ids=lambda case: case.id)
def test_discovery_live(case: SearchCase | CatalogCase | ScreenCase, route: str):
    env = client_environment()
    output = os.environ.get("EPOCH_LIVE_DISCOVERY_ARTIFACT_DIR")
    assert output, "Set a fresh EPOCH_LIVE_DISCOVERY_ARTIFACT_DIR to preserve every first attempt"
    folder = Path(output)
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{case.id}-{route}.json"
    assert not path.exists(), "Do not overwrite or silently retry a captured live attempt"
    receipt = {
        "case": wire(case), "route": route, "planned_primary_operation_calls": 1,
        "saved_universe_read_calls": 0,
        "passed": False, "started_at": datetime.now(timezone.utc).isoformat(),
        "versions": {name: importlib.metadata.version(name)
                     for name in ("stratifyx", "epoch-sdk")},
        "runtime": {"interpreter": sys.executable, "prefix": sys.prefix,
                    "epoch_client_module": inspect.getfile(EpochClient),
                    "native_request_module": inspect.getfile(DatasetSearchRequest)},
        "test_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    start = time.monotonic()
    try:
        asyncio.run(exercise(case, route, env, receipt))
        receipt["passed"] = True
    except BaseException as error:
        receipt["error_type"] = type(error).__name__
        receipt["error"] = str(error)
        pending = [error]
        leaves = []
        while pending:
            current = pending.pop()
            if isinstance(current, BaseExceptionGroup):
                pending.extend(current.exceptions)
            else:
                leaves.append({"type": type(current).__name__, "message": str(current)})
        receipt["error_details"] = leaves
        raise
    finally:
        receipt["seconds_with_pages"] = time.monotonic() - start
        receipt["completed_at"] = datetime.now(timezone.utc).isoformat()
        with path.open("x") as stream:
            path.chmod(0o600)
            json.dump(receipt, stream, indent=2)
            stream.write("\n")
