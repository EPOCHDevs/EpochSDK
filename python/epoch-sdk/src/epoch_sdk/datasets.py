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
            request_options={"max_retries": 0, "additional_headers": {"X-Epoch-Dataset-Selection": "v1"}},
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
