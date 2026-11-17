"""Platform-owned discovery transport. It never calls native Backend search."""
from __future__ import annotations

from collections.abc import Sequence
from urllib.parse import quote, urlencode, urlsplit

import httpx
from pydantic import TypeAdapter
from stratifyx.types import AssetScreen as NativeAssetScreen
from .catalogue_types import CatalogueRequest, CatalogueResult, SavedInventory
from .legacy_discovery_types import DiscoveryStoredQueryResponse

from .credentials import BearerAuth, Token
from .discovery_types import (DiscoveryInput, DiscoveryQuery, DiscoveryResult, SelectedInputs, DiscoveryDetails,
                              ScreenInput1, ScreenInput2, AssetUniverseResult, UniversePageRequest, UniversePage, AssetLookupResult, UniverseBinding, AssetPredicate)
_SCREEN = TypeAdapter(ScreenInput1 | ScreenInput2)


def native_universe_screen(binding: UniverseBinding) -> NativeAssetScreen:
    """Convert the catalogue selector through the source-owned native model.

    The native wire requires both Boolean arrays and integer numeric tokens;
    catalogue int64 range bounds travel as decimal text until this boundary.
    """
    def convert(node: AssetPredicate) -> NativeAssetScreen:
        payload = node.model_dump(mode="json", by_alias=True, exclude_none=True,
                                  exclude={"all_of", "any_of", "not_"})
        for key in ("ipo_shares_min", "ipo_shares_max"):
            if key in payload:
                payload[key] = int(payload[key])
        payload["all_of"] = [convert(child) for child in node.all_of or []]
        payload["any_of"] = [convert(child) for child in node.any_of or []]
        if node.not_ is not None:
            payload["not"] = convert(node.not_)
        return NativeAssetScreen.model_validate(payload)

    return convert(binding.screen)


class CatalogueHTTPError(httpx.HTTPStatusError):
    """An HTTP failure retaining the bounded Platform error envelope."""


class CatalogueClient:
    def __init__(self, base_url: str, token: Token, *, http: httpx.AsyncClient | None = None,
                 transport: httpx.AsyncBaseTransport | None = None):
        parsed = urlsplit(base_url)
        if parsed.scheme != "https" and not (
            parsed.scheme == "http" and parsed.hostname in {"127.0.0.1", "localhost", "::1"}
        ):
            raise ValueError("Catalogue origin must use HTTPS or loopback")
        if parsed.username or parsed.password or parsed.query or parsed.fragment or parsed.path not in {"", "/"}:
            raise ValueError("Invalid catalogue origin")
        if http is not None and transport is not None:
            raise ValueError("Pass an HTTP client or a transport, not both")
        self._base_url = base_url.rstrip("/")
        self._owned = http is None
        self._http = http or httpx.AsyncClient(timeout=35.0, follow_redirects=False, transport=transport)
        self._auth = BearerAuth((lambda: token) if isinstance(token, str) else token, base_url)

    async def aclose(self) -> None:
        if self._owned:
            await self._http.aclose()

    async def _request(self, method: str, path: str, body: object, bound: int) -> bytes:
        async with self._http.stream(method, self._base_url + path, json=body,
                                     auth=self._auth, follow_redirects=False) as response:
            if int(response.headers.get("content-length", "0")) > bound:
                raise ValueError("Catalogue response exceeds the response bound")
            result = bytearray()
            async for chunk in response.aiter_bytes():
                if len(result) + len(chunk) > bound:
                    raise ValueError("Catalogue response exceeds the response bound")
                result.extend(chunk)
            content = bytes(result)
            if response.is_error:
                failed = httpx.Response(response.status_code, headers=response.headers, content=content, request=response.request)
                raise CatalogueHTTPError(f"Catalogue HTTP {response.status_code}: {failed.text}", request=response.request, response=failed)
            return content

    async def search_dataset(self, requests: Sequence[DiscoveryQuery], *,
                             saved_query: str | None = None, limit: int = 5,
                             budget: int = 40_000) -> DiscoveryResult:
        if type(limit) is not int or type(budget) is not int or not 1 <= limit <= 25 or not 1024 <= budget <= 40_000 or len(requests) > 32:
            raise ValueError("Invalid discovery request budget")
        if not requests and not saved_query:
            raise ValueError("A source need or saved query is required")
        request = DiscoveryInput(requests=list(requests), saved_query=saved_query, limit=limit, budget=budget)
        content = await self._request("POST", "/api/v1/discovery/datasets/search",
                                      request.model_dump(mode="json", exclude_none=True), budget)
        return DiscoveryResult.model_validate_json(content)

    async def select(self, session_id: str, candidate_ids: Sequence[str]) -> SelectedInputs:
        if not candidate_ids or len(candidate_ids) > 32 or len(set(candidate_ids)) != len(candidate_ids):
            raise ValueError("Select 1..32 distinct source candidates")
        content = await self._request("POST", "/api/v1/discovery/selections",
                                      {"session_id": session_id, "ids": list(candidate_ids)}, 16_777_216)
        return SelectedInputs.model_validate_json(content)

    async def selection(self, selection_id: str) -> SelectedInputs:
        content = await self._request("GET", "/api/v1/discovery/selections/" + quote(selection_id, safe=""),
                                      None, 16_777_216)
        return SelectedInputs.model_validate_json(content)

    async def details(self, session_id: str, candidate_ids: Sequence[str]) -> DiscoveryDetails:
        if not candidate_ids or len(candidate_ids) > 10 or len(set(candidate_ids)) != len(candidate_ids):
            raise ValueError("Read 1..10 distinct source details")
        content = await self._request("POST", "/api/v1/discovery/datasets/details",
                                      {"session_id": session_id, "ids": list(candidate_ids)}, 1_048_576)
        return DiscoveryDetails.model_validate_json(content)

    async def dataset_catalog(self, request: CatalogueRequest) -> CatalogueResult:
        """Read the published constructor directory and caller-private inventory."""
        content = await self._request("POST", "/api/v1/discovery/catalog",
                                      request.model_dump(mode="json", by_alias=True, exclude_none=True), 16_777_216)
        return CatalogueResult.model_validate_json(content)

    async def list_saved_datasets(self, *, query: str | None = None, cursor: str | None = None,
                                  limit: int = 100) -> SavedInventory:
        if type(limit) is not int or not 1 <= limit <= 100:
            raise ValueError("Dataset page limit must be an integer in 1..100")
        parameters = {"limit": str(limit)}
        if query is not None: parameters["query"] = query
        if cursor is not None: parameters["cursor"] = cursor
        content = await self._request("GET", "/api/v1/files/datasets?" + urlencode(parameters), None, 16_777_216)
        return SavedInventory.model_validate_json(content)

    async def screen_assets(self, request: ScreenInput1 | ScreenInput2 | dict) -> AssetUniverseResult:
        value = _SCREEN.validate_python(request)
        content = await self._request("POST", "/api/v1/discovery/assets/screen",
                                      _SCREEN.dump_python(value, mode="json", by_alias=True, exclude_none=True), 40_000)
        return AssetUniverseResult.model_validate_json(content)

    async def universe_page(self, request: UniversePageRequest) -> UniversePage:
        content = await self._request("POST", "/api/v1/discovery/assets/universes/query",
                                      request.model_dump(mode="json", by_alias=True, exclude_none=True), 1_048_576)
        return UniversePage.model_validate_json(content)

    async def read_retained(self, reference: str, *, cursor: str | None = None, limit: int = 10) -> DiscoveryStoredQueryResponse:
        """Reopen original owner-scoped evidence without rerunning its search."""
        if type(limit) is not int or not 1 <= limit <= 10:
            raise ValueError("Saved metadata page limit must be an integer in 1..10.")
        content = await self._request("POST", "/api/v1/discovery/retained/read",
                                      {"reference": reference, "limit": limit, **({"cursor": cursor} if cursor else {})}, 1_048_576)
        return DiscoveryStoredQueryResponse.model_validate_json(content)

    async def resolve_assets(self, asset_ids: Sequence[str]) -> AssetLookupResult:
        if not asset_ids or len(asset_ids) > 200 or len(set(asset_ids)) != len(asset_ids) or any(type(value) is not str or not value or len(value) > 256 for value in asset_ids):
            raise ValueError("Resolve 1..200 distinct asset IDs")
        content = await self._request("POST", "/api/v1/discovery/assets/resolve", {"asset_ids": list(asset_ids)}, 8 * 1024 * 1024)
        return AssetLookupResult.model_validate_json(content)

    async def bind_universe(self, universe_ref: str) -> UniverseBinding:
        content = await self._request("POST", "/api/v1/discovery/assets/universes/binding", {"universe_ref": universe_ref}, 8 * 1024 * 1024)
        result = UniverseBinding.model_validate_json(content)
        if result.universe_ref != universe_ref:
            raise ValueError("Universe binding differs from the requested reference")
        return result
