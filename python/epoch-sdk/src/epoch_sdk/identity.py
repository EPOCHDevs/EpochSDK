"""Platform-owned exact asset metadata and artwork descriptors."""

from __future__ import annotations

import json
from collections.abc import Sequence
from functools import lru_cache
from pathlib import Path
from typing import Protocol, cast
from urllib.parse import quote, urlencode, urlsplit

import httpx
from jsonschema import Draft7Validator
from jsonschema.exceptions import ValidationError

from .credentials import BearerAuth, Token
from .identity_types import (
    AssetInformationPage,
    AssetLogoResponse1,
    AssetLogoResponse2,
    AssetLookupResponse,
    AssetSpecification,
    CountryCatalogResponse,
    CountryIdentity,
)

type AssetLogoResponse = AssetLogoResponse1 | AssetLogoResponse2


class _Validator(Protocol):
    def validate(self, instance: object) -> None: ...


@lru_cache(maxsize=8)
def _validator(name: str) -> _Validator:
    schema = json.loads(
        (Path(__file__).with_name("data") / "asset-identity.schema.json").read_text()
    )
    return cast(
        _Validator,
        Draft7Validator({"$ref": "#/definitions/" + name, "definitions": schema["definitions"]}),
    )


class IdentityHTTPError(httpx.HTTPStatusError):
    """A bounded error response from the public identity API."""


def _id(value: object) -> str:
    if (
        not isinstance(value, str)
        or not value
        or len(value) > 256
        or any(ord(char) <= 32 or ord(char) == 127 or char in "/\\%?#" for char in value)
    ):
        raise ValueError("Invalid identity ID")
    return quote(value, safe="")


class IdentityClient:
    def __init__(
        self,
        base_url: str,
        token: Token | None = None,
        *,
        http: httpx.AsyncClient | None = None,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        parsed = urlsplit(base_url)
        if parsed.scheme != "https" and not (
            parsed.scheme == "http" and parsed.hostname in {"127.0.0.1", "localhost", "::1"}
        ):
            raise ValueError("Identity origin must use HTTPS or loopback")
        if (
            parsed.username
            or parsed.password
            or parsed.query
            or parsed.fragment
            or parsed.path not in {"", "/"}
        ):
            raise ValueError("Invalid identity origin")
        if http is not None and transport is not None:
            raise ValueError("Pass an HTTP client or a transport, not both")
        self._base_url = base_url.rstrip("/")
        self._owned = http is None
        self._http = http or httpx.AsyncClient(
            timeout=12.0, follow_redirects=False, transport=transport
        )
        self._auth = (
            None
            if token is None
            else BearerAuth((lambda: token) if isinstance(token, str) else token, base_url)
        )

    async def aclose(self) -> None:
        if self._owned:
            await self._http.aclose()

    async def _request(self, path: str, schema_name: str, body: object = None) -> bytes:
        async with self._http.stream(
            "GET" if body is None else "POST",
            self._base_url + path,
            json=body,
            auth=self._auth,
            follow_redirects=False,
        ) as response:
            if int(response.headers.get("content-length", "0")) > 8 * 1024 * 1024:
                raise ValueError("Identity response exceeds bound")
            result = bytearray()
            async for chunk in response.aiter_bytes():
                if len(result) + len(chunk) > 8 * 1024 * 1024:
                    raise ValueError("Identity response exceeds bound")
                result.extend(chunk)
            content = bytes(result)
            if not response.is_success:
                failed = httpx.Response(
                    response.status_code,
                    headers=response.headers,
                    content=content,
                    request=response.request,
                )
                raise IdentityHTTPError(
                    f"Identity HTTP {response.status_code}: {failed.text}",
                    request=response.request,
                    response=failed,
                )
            try:
                _validator(schema_name).validate(json.loads(content))
            except ValidationError as error:
                raise ValueError("Invalid Platform identity response") from error
            return content

    async def get_asset_information(self, asset_id: str) -> AssetSpecification:
        result = AssetSpecification.model_validate_json(
            await self._request("/api/v1/metadata/assets/" + _id(asset_id), "AssetSpecification")
        )
        if result.id != asset_id:
            raise ValueError("Metadata belongs to another asset")
        return result

    async def get_asset_logos(
        self,
        asset_id: str,
        *,
        listing_catalogue: str | None = None,
        listing_selected_at: str | None = None,
    ) -> AssetLogoResponse:
        if bool(listing_catalogue) != bool(listing_selected_at):
            raise ValueError("Both listing catalogue and clock are required")
        query = (
            "?"
            + urlencode(
                {"listing_catalogue": listing_catalogue, "listing_selected_at": listing_selected_at}
            )
            if listing_catalogue
            else ""
        )
        content = await self._request(
            "/api/v1/assets/" + _id(asset_id) + "/logos" + query, "AssetLogoResponse"
        )
        result = (
            AssetLogoResponse1 if json.loads(content)["kind"] == "single" else AssetLogoResponse2
        ).model_validate_json(content)
        if result.asset_id != asset_id:
            raise ValueError("Artwork belongs to another asset")
        return result

    async def get_country_catalog(self) -> CountryCatalogResponse:
        return CountryCatalogResponse.model_validate_json(
            await self._request("/api/v1/metadata/countries", "CountryCatalogResponse")
        )

    async def get_country(self, code: str) -> CountryIdentity:
        return CountryIdentity.model_validate_json(
            await self._request("/api/v1/metadata/countries/" + _id(code), "CountryIdentity")
        )

    async def get_region(self, code: str) -> CountryIdentity:
        return CountryIdentity.model_validate_json(
            await self._request("/api/v1/metadata/regions/" + _id(code), "CountryIdentity")
        )

    async def list_assets(
        self, *, query: str | None = None, page: int | None = None, page_size: int | None = None
    ) -> AssetInformationPage:
        values = {
            key: value
            for key, value in {"query": query, "page": page, "page_size": page_size}.items()
            if value is not None
        }
        suffix = "?" + urlencode(values) if values else ""
        return AssetInformationPage.model_validate_json(
            await self._request("/api/v1/metadata/assets" + suffix, "AssetInformationPage")
        )

    async def resolve_asset_information(self, asset_ids: Sequence[str]) -> AssetLookupResponse:
        if isinstance(asset_ids, (str, bytes)) or not asset_ids or len(asset_ids) > 200:
            raise ValueError("Resolve 1..200 asset IDs")
        for asset_id in asset_ids:
            _id(asset_id)
        result = AssetLookupResponse.model_validate_json(
            await self._request(
                "/api/v1/metadata/assets/resolve",
                "AssetLookupResponse",
                {"asset_ids": list(asset_ids)},
            )
        )
        if [item.asset_id for item in result.items] != list(dict.fromkeys(asset_ids)):
            raise ValueError("Lookup returned different asset IDs")
        return result
