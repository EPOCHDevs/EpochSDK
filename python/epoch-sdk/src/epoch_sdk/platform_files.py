"""Platform-owned file previews and version saves, without AI or automatic retries."""

from __future__ import annotations

import inspect
import json
import re
from collections.abc import AsyncIterator, Mapping
from contextlib import asynccontextmanager
from copy import deepcopy
from dataclasses import dataclass
from importlib.resources import files
from typing import Any, cast
from urllib.parse import quote, urlsplit

import httpx
from jsonschema import Draft202012Validator
from pydantic import BaseModel, JsonValue, TypeAdapter
from referencing import Registry, Resource

from .credentials import Token
from .platform_file_models import (
    CellGridRequest,
    FileEditGrid,
    FileEditOptions,
    FileEditRequest,
    FileImagePreview,
    FilePreview,
    FileVersion,
    FileVersionPage,
)

_URI = "https://epoch.trade/contracts/platform-files-v1"
_document = json.loads(files("epoch_sdk").joinpath("data/platform-files.openapi.json").read_text())
_registry = Registry().with_resource(
    _URI,
    Resource.from_contents(
        {"$schema": "https://json-schema.org/draft/2020-12/schema", **_document}
    ),
)
_validators = {
    name: Draft202012Validator({"$ref": f"{_URI}#/components/schemas/{name}"}, registry=_registry)
    for name in _document["components"]["schemas"]
}
_adapters = {
    "FilePreview": TypeAdapter(FilePreview),
    "FileImagePreview": TypeAdapter(FileImagePreview),
    "FileEditOptions": TypeAdapter(FileEditOptions),
    "FileVersion": TypeAdapter(FileVersion),
    "FileVersionPage": TypeAdapter(FileVersionPage),
    "FileEditGrid": TypeAdapter(FileEditGrid),
}
_original = re.compile(
    _document["components"]["schemas"]["FileVersion"]["properties"]["original_file_ref"]["pattern"]
)
_reference = re.compile(
    _document["components"]["schemas"]["FileDescriptor"]["properties"]["file_ref"]["pattern"]
)


def _validate(name: str, value: object) -> None:
    problem = next(_validators[name].iter_errors(cast(JsonValue, value)), None)
    if problem is not None:
        raise ValueError(
            f"Invalid Platform {name} at {'.'.join(map(str, problem.absolute_path)) or 'body'}"
        )


def _request(name: str, value: BaseModel | Mapping[str, object]) -> dict[str, object]:
    wire = (
        value.model_dump(mode="json", exclude_none=True)
        if isinstance(value, BaseModel)
        else deepcopy(dict(value))
    )
    _validate(name, wire)
    if name == "FileEditRequest" and len(str(wire["request_id"]).encode("utf-8")) > 128:
        raise ValueError("request_id must fit 128 UTF-8 bytes")
    return wire


class PlatformFileError(RuntimeError):
    def __init__(self, status: int, code: str, message: str, retry_after: str | None = None):
        super().__init__(message)
        self.status, self.code, self.retry_after = status, code, retry_after


@dataclass(frozen=True)
class FileContent:
    status: int
    headers: Mapping[str, str]
    body: AsyncIterator[bytes]


class PlatformFilesClient:
    def __init__(
        self, base_url: str, *, token: Token | None = None, http: httpx.AsyncClient | None = None
    ):
        parsed = urlsplit(base_url)
        if (
            base_url != base_url.strip()
            or any(ord(c) < 32 for c in base_url)
            or parsed.scheme not in {"http", "https"}
            or not parsed.hostname
            or parsed.username
            or parsed.password
            or parsed.query
            or parsed.fragment
        ):
            raise ValueError("Provide an HTTP(S) Platform API endpoint without credentials")
        if token is None and http is None:
            raise ValueError("Provide a bearer token/provider or an authenticated HTTP client")
        self.base_url = base_url.rstrip("/")
        self._token, self._owned = token, http is None
        self._http = http or httpx.AsyncClient(timeout=130)

    async def aclose(self) -> None:
        if self._owned:
            await self._http.aclose()

    async def _headers(self) -> dict[str, str]:
        if self._token is None:
            return {}
        value = self._token() if callable(self._token) else self._token
        if inspect.isawaitable(value):
            value = await value
        if not isinstance(value, str) or not re.fullmatch(r"[!-~]+", value):
            raise ValueError("The token provider must return a nonempty printable bearer token")
        return {"Authorization": f"Bearer {value}"}

    def _url(self, ref: str, suffix: str, *, original: bool = False) -> str:
        if not isinstance(ref, str) or not (_original if original else _reference).fullmatch(ref):
            raise ValueError(
                "Provide an exact original file reference"
                if original
                else "Provide an exact file reference"
            )
        if ref.startswith("file-version:") and int(ref.split(":")[2]) > 2**53 - 1:
            raise ValueError("Provide an exact file reference")
        return f"{self.base_url}/api/v1/files/{quote(ref, safe='')}{suffix}"

    @staticmethod
    def _error(response: httpx.Response) -> None:
        if response.is_success:
            return
        try:
            body = response.json()
            code, message = body["error"], body["message"]
            if not isinstance(code, str) or not isinstance(message, str):
                raise TypeError()
        except (ValueError, TypeError, KeyError):
            code, message = (
                "INVALID_PLATFORM_RESPONSE",
                f"Platform file request failed ({response.status_code})",
            )
        raise PlatformFileError(
            response.status_code, code, message, response.headers.get("retry-after")
        )

    async def _json(self, url: str, model: str, *, body: dict[str, object] | None = None) -> Any:
        response = await self._http.request(
            "GET" if body is None else "POST",
            url,
            json=body,
            headers=await self._headers(),
            timeout=130,
            follow_redirects=False,
        )
        self._error(response)
        try:
            if response.status_code != 200:
                raise ValueError()
            wire = response.json()
            _validate(model, wire)
            return _adapters[model].validate_json(response.content)
        except ValueError:
            raise ValueError(f"Platform returned an invalid {model}") from None

    @staticmethod
    def _version(result: FileVersion, original: str) -> FileVersion:
        digest = result.file.content_sha256
        expected = (
            original
            if result.version == 0
            else f"file-version:{original[5:]}:{result.version}:{digest}"
        )
        if (
            result.original_file_ref != original
            or result.file.file_ref != expected
            or not digest
            or (result.version == 0 and digest != original[5:])
        ):
            raise ValueError("Platform returned an inconsistent file version")
        return result

    async def preview(self, ref: str) -> FilePreview:
        return cast(FilePreview, await self._json(self._url(ref, "/preview"), "FilePreview"))

    async def image_preview(self, ref: str) -> FileImagePreview:
        result = cast(
            FileImagePreview, await self._json(self._url(ref, "/image-preview"), "FileImagePreview")
        )
        if result.state == "ready" and (
            sum(page.size_bytes for page in result.pages) != result.size_bytes
            or any(page.page != index + 1 for index, page in enumerate(result.pages))
        ):
            raise ValueError("Platform returned an inconsistent image preview")
        return result

    async def edit_options(self, ref: str) -> FileEditOptions:
        result = cast(
            FileEditOptions,
            await self._json(self._url(ref, "/edit-options", original=True), "FileEditOptions"),
        )
        self._version(result.latest, ref)
        return result

    async def latest(self, ref: str) -> FileVersion:
        result = cast(
            FileVersion,
            await self._json(self._url(ref, "/versions/latest", original=True), "FileVersion"),
        )
        return self._version(result, ref)

    async def history(
        self, ref: str, *, before: int | None = None, limit: int = 50
    ) -> FileVersionPage:
        if (
            type(limit) is not int
            or not 1 <= limit <= 100
            or (before is not None and (type(before) is not int or not 1 <= before <= 2**53 - 1))
        ):
            raise ValueError("Invalid version history page")
        url = httpx.URL(self._url(ref, "/versions", original=True)).copy_merge_params(
            {"limit": limit, **({"before": before} if before is not None else {})}
        )
        result = cast(FileVersionPage, await self._json(str(url), "FileVersionPage"))
        previous = before if before is not None else 2**53
        for item in result.items:
            self._version(item, ref)
            if item.version >= previous:
                raise ValueError("Platform returned unordered file history")
            previous = item.version
        if len(result.items) > limit or (
            result.next_before is not None
            and (not result.items or result.next_before != result.items[-1].version)
        ):
            raise ValueError("Platform returned an invalid history cursor")
        return result

    async def grid(self, ref: str, request: CellGridRequest | Mapping[str, object]) -> FileEditGrid:
        wire = _request("CellGridRequest", request)
        result = cast(
            FileEditGrid, await self._json(self._url(ref, "/edit-grid"), "FileEditGrid", body=wire)
        )
        expected_hash = ref[5:] if ref.startswith("file:") else ref.rsplit(":", 1)[1]
        if (
            result.file_ref != ref
            or result.source_sha256 != expected_hash
            or result.offset != wire.get("offset", 0)
            or len(result.rows) > cast(int, wire.get("limit", 100))
            or any(len(row) != len(result.columns) for row in result.rows)
        ):
            raise ValueError("Platform returned an inconsistent file grid")
        return result

    async def save(self, ref: str, request: FileEditRequest | Mapping[str, object]) -> FileVersion:
        wire = _request("FileEditRequest", request)
        result = cast(
            FileVersion,
            await self._json(self._url(ref, "/versions", original=True), "FileVersion", body=wire),
        )
        self._version(result, ref)
        if result.version != cast(int, wire["base_version"]) + 1:
            raise ValueError("Platform returned another file or save generation")
        return result

    @asynccontextmanager
    async def content(
        self,
        ref: str,
        *,
        preview: bool = False,
        image_page: int | None = None,
        byte_range: str | None = None,
        if_range: str | None = None,
    ) -> AsyncIterator[FileContent]:
        if image_page is not None and (
            preview or type(image_page) is not int or not 1 <= image_page <= 1000
        ):
            raise ValueError("Provide one image page in 1..1000, separately from PDF preview")
        suffix = (
            f"/image-preview/{image_page}/content"
            if image_page is not None
            else "/preview/content"
            if preview
            else "/content"
        )
        url = self._url(ref, suffix)
        headers: dict[str, str] = {}
        if byte_range is not None:
            if len(byte_range) > 256 or not re.fullmatch(r"bytes=(?:\d+-\d*|-\d+)", byte_range):
                raise ValueError("Provide one byte range")
            headers["Range"] = byte_range
        if if_range is not None:
            if len(if_range) > 256 or any(ord(c) < 32 or ord(c) > 126 for c in if_range):
                raise ValueError("Invalid If-Range validator")
            headers["If-Range"] = if_range
        headers.update(await self._headers())
        async with self._http.stream(
            "GET", url, headers=headers, timeout=130, follow_redirects=False
        ) as response:
            if response.status_code not in {200, 206}:
                await response.aread()
                self._error(response)
                raise ValueError("Platform returned an invalid content response")
            yield FileContent(response.status_code, dict(response.headers), response.aiter_bytes())
