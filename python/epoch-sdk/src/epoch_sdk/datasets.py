"""Data methods shared by notebook and application clients.

Platform/GDS own current discovery, retained evidence and complete cohorts.
The native client remains the transport for ordinary execution.
"""

from __future__ import annotations

from collections.abc import Sequence

from .catalogue import CatalogueClient
from .discovery_types import DiscoveryQuery, DiscoveryResult, SelectedInputs, AssetUniverseResult, ScreenInput1, ScreenInput2
from .catalogue_types import CatalogueRequest, CatalogueResult
from .legacy_discovery_types import DiscoveryStoredQueryResponse

from pydantic import TypeAdapter
from stratifyx import AsyncStratifyX

_SCREEN_REQUEST = TypeAdapter(ScreenInput1 | ScreenInput2)


class DatasetClient:
    """Data methods shared by application and notebook clients."""

    backend: AsyncStratifyX
    catalogue: CatalogueClient | None = None

    async def dataset_catalog(
        self,
        *,
        source_ids: Sequence[str] = (),
        include_details: bool = False,
        include_saved: bool = True,
        saved_cursor: str | None = None,
        saved_limit: int = 100,
    ) -> CatalogueResult:
        """Read Platform's published constructor directory and private inventory.

        Select source_ids and include_details for constructor schemas, vintage
        and revision options. Saved entries remain scoped to the caller.
        """
        request = CatalogueRequest.model_validate({
            "source_ids": source_ids, "include_details": include_details,
            "include_saved": include_saved, "saved_cursor": saved_cursor, "saved_limit": saved_limit,
        })
        if self.catalogue is None:
            raise RuntimeError("Connect a Platform catalogue client before reading the directory")
        return await self.catalogue.dataset_catalog(request)

    async def search_dataset(self, requests: Sequence[DiscoveryQuery], *,
                             candidate_limit: int | None = None,
                             saved_query: str | None = None) -> DiscoveryResult:
        """Discover through Platform/GDS using the same contract as the agent."""
        if self.catalogue is None:
            raise RuntimeError("Connect a Platform catalogue client before searching")
        return await self.catalogue.search_dataset(requests, limit=5 if candidate_limit is None else candidate_limit,
                                                   saved_query=saved_query)

    async def select_sources(self, session_id: str, candidate_ids: Sequence[str]) -> SelectedInputs:
        if self.catalogue is None:
            raise RuntimeError("Connect a Platform catalogue client before selecting sources")
        return await self.catalogue.select(session_id, candidate_ids)

    async def read_dataset_search(
        self, result_ref: str, *, cursor: str | None = None, limit: int = 10
    ) -> DiscoveryStoredQueryResponse:
        """Read 1..10 saved metadata records; no SQL or vendor search is rerun."""
        if type(limit) is not int or not 1 <= limit <= 10:
            raise ValueError("Saved metadata page limit must be an integer in 1..10.")
        if self.catalogue is None:
            raise RuntimeError("Connect a Platform catalogue client before reopening discovery evidence")
        return await self.catalogue.read_retained(result_ref, cursor=cursor, limit=limit)

    async def screen_assets(self, request: ScreenInput1 | ScreenInput2) -> AssetUniverseResult:
        """Create/reuse a complete cohort, preserving its membership time basis.

        Carry the selected membership definition and qualifications into the
        build_study briefing; keep universe_ref to reread the saved selection.
        Acquisition/integrity gaps remain visible and cannot form a usable
        universe. Screening never applies relevance top-k.
        """
        value = _SCREEN_REQUEST.validate_python(request)
        if self.catalogue is None:
            raise RuntimeError("Connect a Platform catalogue client before screening assets")
        payload = value.model_dump(mode="json", by_alias=True, exclude_unset=True, exclude_none=True)
        def exact_integers(node):
            if not isinstance(node, dict):
                return
            for key in ("ipo_shares_min", "ipo_shares_max"):
                if key in node:
                    node[key] = str(node[key])
            for key in ("any_of", "all_of"):
                for child in node.get(key, []):
                    exact_integers(child)
            if "not" in node:
                exact_integers(node["not"])
        exact_integers(payload.get("screen"))
        return await self.catalogue.screen_assets(payload)
