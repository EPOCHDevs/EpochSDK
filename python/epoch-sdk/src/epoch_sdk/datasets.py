"""Shared native data discovery for notebook, application and MCP clients.

Backend owns the catalog, source options, search facts and saved universes.
These methods make no EpochAI or generative model call. Search may use the
Backend's non-generative relevance ranker; it never fetches observations.
"""

from __future__ import annotations

from collections.abc import Sequence

from pydantic import BaseModel, ConfigDict, TypeAdapter
from stratifyx import AsyncStratifyX
from stratifyx.types import (
    AssetUniverseResponse,
    DatasetCatalogRequest,
    DatasetCatalogResponse,
    DatasetSearchQuery,
    DatasetSearchRequest,
    DatasetSearchSelection,
    DiscoveryMetadataRecord,
    DiscoverySearchResponse,
    DiscoveryStoredQueryResponse,
    ScreenAssetsRequest,
)
from stratifyx.types.discovery_stored_operation import DiscoveryStoredOperation_Read

_SCREEN_REQUEST = TypeAdapter(ScreenAssetsRequest)


class DatasetSearchResult(BaseModel):
    """Backend-ranked selections for every requested subject/product.

    The original completeness/receipt still describes the full captured pool.
    page is retained only to decode historical client/checkpoint deliveries;
    ordinary search returns its complete selection without a metadata read.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)
    result: DiscoverySearchResponse
    page: DiscoveryStoredQueryResponse | None = None


def _selection_of(result: DiscoverySearchResponse, record: DiscoveryMetadataRecord) -> DatasetSearchSelection | None:
    """The selection a record belongs to under selection protocol v3.

    A record names its requested_dataset only when its request item has several
    selections; otherwise the item's single selection is the record's.
    """
    matches = [
        selection for selection in result.selections or []
        if selection.request_id == record.request_id and selection.request_item_id == record.request_item_id
        and (record.requested_dataset is None or selection.requested_dataset == record.requested_dataset)
    ]
    return matches[0] if len(matches) == 1 else None


def complete_records(result: DiscoverySearchResponse) -> DiscoverySearchResponse:
    """The same result with every record carrying all of its facts.

    Selection protocol v3 states a fact every delivered record shares once: on the
    response, or on the record's selection (qualifications, loader, vendor and
    provider-search completeness). A record's facts are its own, its selection's
    and the response's. Use this for displays that show one record at a time; a
    model or an API caller should read the compact result as delivered.
    """
    shared = list(result.qualifications or [])
    records = []
    for record in result.records:
        selection = _selection_of(result, record)
        update: dict[str, object] = {"qualifications": list(dict.fromkeys(
            [*record.qualifications, *((selection.qualifications or []) if selection else []), *shared]))}
        if selection is not None:
            for name in ("loader", "vendor", "source_search_completeness", "requested_dataset"):
                if getattr(record, name) is None and getattr(selection, name) is not None:
                    update[name] = getattr(selection, name)
        records.append(record.model_copy(update=update))
    selections = [
        selection.model_copy(update={"qualifications": None, "loader": None, "vendor": None,
                                     "source_search_completeness": None})
        for selection in result.selections
    ] if result.selections is not None else None
    return result.model_copy(update={"records": records, "qualifications": None, "selections": selections})


class DatasetClient:
    """Native data methods shared by EpochClient and AgentToolsClient."""

    backend: AsyncStratifyX

    async def dataset_catalog(
        self,
        *,
        source_ids: Sequence[str] = (),
        include_details: bool = False,
        include_saved: bool = True,
        saved_cursor: str | None = None,
        saved_limit: int = 100,
    ) -> DatasetCatalogResponse:
        """Read Backend's dataset directory, options and exact shared prose.

        Select source_ids and include_details for constructor schemas, vintage
        and revision options. Saved entries remain scoped to the caller.
        """
        request = DatasetCatalogRequest.model_validate({
            "source_ids": source_ids, "include_details": include_details,
            "include_saved": include_saved, "saved_cursor": saved_cursor, "saved_limit": saved_limit,
        })
        return await self.backend.discovery.read_dataset_catalog(
            source_ids=request.source_ids,
            include_details=request.include_details,
            include_saved=request.include_saved,
            saved_cursor=request.saved_cursor,
            saved_limit=request.saved_limit,
            request_options={"max_retries": 0},
        )

    async def search_dataset(
        self,
        requests: Sequence[DatasetSearchQuery],
        *,
        candidate_limit: int | None = None,
        saved_query: str | None = None,
    ) -> DatasetSearchResult:
        """Find native asset/series identities, optionally with a constructor.

        Carry selected native identities, loader options and material source
        qualifications into the build_study briefing. References identify saved
        metadata; they are not native loader inputs.
        Backend delivers relevant candidates per requested subject and product.
        A fact every delivered record shares is stated once, on the result or on
        the record's selection (selection protocol v3); complete_records restores
        it to each record for display.
        saved_query finds caller-owned datasets by descriptive metadata or exact
        returned references. Search does not create an asset cohort; use
        screen_assets for a complete universe.
        """
        request = DatasetSearchRequest.model_validate({
            "requests": requests, "candidate_limit": candidate_limit, "saved_query": saved_query,
        })
        result = await self.backend.discovery.search_dataset(
            requests=request.requests,
            candidate_limit=request.candidate_limit,
            saved_query=request.saved_query,
            request_options={"max_retries": 0, "additional_headers": {"X-Epoch-Dataset-Selection": "v3"}},
        )
        if not result.records_complete and not result.records:
            raise RuntimeError("Backend returned an incomplete search without ranked candidates; update the Backend dataset-search service. No candidate paging was started.")
        return DatasetSearchResult(result=result)

    async def read_dataset_search(
        self, result_ref: str, *, cursor: str | None = None, limit: int = 10
    ) -> DiscoveryStoredQueryResponse:
        """Read 1..10 saved metadata records; no SQL or vendor search is rerun."""
        if type(limit) is not int or not 1 <= limit <= 10:
            raise ValueError("Saved metadata page limit must be an integer in 1..10.")
        return await self.backend.discovery.query_stored_discovery(
            result_refs=[result_ref],
            operation=DiscoveryStoredOperation_Read(kind="read"),
            cursor=cursor,
            limit=limit,
            request_options={"max_retries": 0},
        )

    async def screen_assets(self, request: ScreenAssetsRequest) -> AssetUniverseResponse:
        """Create/reuse a complete cohort, preserving its membership time basis.

        Carry the selected membership definition and qualifications into the
        build_study briefing; keep universe_ref to reread the saved selection.
        Acquisition/integrity gaps remain visible and cannot form a usable
        universe. Screening never applies relevance top-k.
        """
        return await self.backend.discovery.screen_asset_universe(
            request=_SCREEN_REQUEST.validate_python(request), request_options={"max_retries": 0}
        )
