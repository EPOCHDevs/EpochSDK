"""Platform-owned file previews and version saves, without AI or automatic retries."""

from __future__ import annotations

import hashlib
import inspect
import json
import re
from collections.abc import AsyncIterator, Mapping
from contextlib import asynccontextmanager
from copy import deepcopy
from dataclasses import dataclass
from importlib.resources import files
from typing import Any, Literal, cast
from urllib.parse import quote, urlsplit

import httpx
from jsonschema import Draft202012Validator
from pydantic import BaseModel, JsonValue, TypeAdapter
from referencing import Registry, Resource

from ._storage import SignedLink, put_signed, signed_link, storage_client
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
    PlatformDocumentBlock,
    PlatformDocumentContentPage,
    PlatformDocumentRead,
    PlatformDocumentSourcePassage,
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
    "DocumentRead": TypeAdapter(PlatformDocumentRead),
    "DocumentContentPage": TypeAdapter(PlatformDocumentContentPage),
    "DocumentSourcePassage": TypeAdapter(PlatformDocumentSourcePassage),
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

    def _document_url(self, ref: str, kind: str, suffix: str = "") -> str:
        if not isinstance(ref, str) or not re.fullmatch(rf"{kind}:[0-9a-f]{{64}}", ref):
            raise ValueError(f"Provide an exact {kind} reference")
        prefix = "reads/" if kind == "document-read" else ""
        return f"{self.base_url}/api/v1/files/documents/{prefix}{quote(ref, safe='')}{suffix}"

    @staticmethod
    def _positions(block: PlatformDocumentBlock, source_bytes: int) -> None:
        if (block.start_byte is None) != (block.length is None) or (
            block.start_byte is not None
            and (
                block.length != len(block.text.encode("utf-8"))
                or block.start_byte + (block.length or 0) > source_bytes
            )
        ):
            raise ValueError("Platform returned an inconsistent document position")

    async def begin_document_read(self, ref: str) -> PlatformDocumentRead:
        self._url(ref, "")
        result = cast(
            PlatformDocumentRead,
            await self._json(
                f"{self.base_url}/api/v1/files/documents/reads",
                "DocumentRead",
                body={"file_ref": ref},
            ),
        )
        if result.source.file_ref != ref:
            raise ValueError("Platform returned a different document source")
        return result

    async def document_read(self, ref: str) -> PlatformDocumentRead:
        result = cast(
            PlatformDocumentRead,
            await self._json(self._document_url(ref, "document-read"), "DocumentRead"),
        )
        if result.read_ref != ref:
            raise ValueError("Platform returned a different document read")
        return result

    async def document_content(
        self,
        ref: str,
        *,
        offset: int = 0,
        limit: int = 4,
        max_bytes: int = 32768,
        layer: Literal["primary", "element", "all"] = "primary",
    ) -> PlatformDocumentContentPage:
        url = self._document_url(ref, "document", "/blocks")
        if (
            type(offset) is not int
            or not 0 <= offset <= 2**53 - 1
            or type(limit) is not int
            or not 1 <= limit <= 100
            or type(max_bytes) is not int
            or not 16384 <= max_bytes <= 131072
            or layer not in {"primary", "element", "all"}
        ):
            raise ValueError("Invalid document content page")
        query = str(
            httpx.QueryParams(
                {"offset": offset, "limit": limit, "max_bytes": max_bytes, "layer": layer}
            )
        )
        result = cast(
            PlatformDocumentContentPage, await self._json(f"{url}?{query}", "DocumentContentPage")
        )
        if (
            result.document_version_ref != ref
            or result.offset != offset
            or result.layer != layer
            or len(result.blocks) > limit
            or result.offset + len(result.blocks) > result.total_blocks
        ):
            raise ValueError("Platform returned an inconsistent document page")
        for block in result.blocks:
            self._positions(block, result.source.size_bytes)
        return result

    async def document_passage(self, ref: str, block_ref: str) -> PlatformDocumentSourcePassage:
        if not isinstance(block_ref, str) or not re.fullmatch(r"block:[0-9a-f]{64}", block_ref):
            raise ValueError("Provide an exact block reference")
        result = cast(
            PlatformDocumentSourcePassage,
            await self._json(
                self._document_url(ref, "document", f"/blocks/{quote(block_ref, safe='')}"),
                "DocumentSourcePassage",
            ),
        )
        if result.document_version_ref != ref or result.block.block_ref != block_ref:
            raise ValueError("Platform returned a different document passage")
        self._positions(result.block, result.source.size_bytes)
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

    async def _staged(self, ref: str, wire: dict[str, object]) -> dict[str, object]:
        """Put the edit through a signed link, so the save names it and carries no file text.

        Where Platform has no signed links, the edit stays inline. Platform keys the staged
        edit by request_id and its SHA-256, so a retry puts the same bytes to the same place.
        """
        edit = json.dumps(wire["edit"], ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        upload = {"size_bytes": len(edit), "content_sha256": hashlib.sha256(edit).hexdigest()}
        url = self._url(ref, "/edit-uploads", original=True)

        async def link() -> SignedLink:
            response = await self._http.post(
                url, json={"request_id": wire["request_id"], **upload},
                headers=await self._headers(), timeout=130, follow_redirects=False,
            )
            self._error(response)
            try:
                value = response.json()
                _validate("FileTransferLink", value)
            except ValueError:
                raise ValueError("Platform returned an invalid FileTransferLink") from None
            return signed_link(value, len(edit))

        try:
            first = await link()
        except PlatformFileError as error:
            # No links here, or a Platform from before direct transfer (no such route).
            if error.code == "FILE_DIRECT_TRANSFER_UNAVAILABLE" or error.status == 404:
                return wire
            raise
        links = iter([first])

        async def next_link() -> SignedLink:
            return next(links, None) or await link()

        async with storage_client() as storage:
            await put_signed(storage, next_link, edit)
        staged = {key: value for key, value in wire.items() if key != "edit"}
        staged["edit_upload"] = upload
        _validate("FileEditRequest", staged)
        return staged

    async def save(self, ref: str, request: FileEditRequest | Mapping[str, object]) -> FileVersion:
        """Save an edit against its exact base version; Platform never retries it.

        The edit is put through a signed storage link where Platform offers one, so its text
        never passes through the API's firewall (Platform docs/design/direct-file-transfer.md).
        """
        wire = _request("FileEditRequest", request)
        if "edit" not in wire or "edit_upload" in wire:
            raise ValueError("Pass the edit itself; the client stages it")
        body = await self._staged(ref, wire)
        result = cast(
            FileVersion,
            await self._json(self._url(ref, "/versions", original=True), "FileVersion", body=body),
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
