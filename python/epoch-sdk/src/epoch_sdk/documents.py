"""Shared document/public-web adapters; retained reads stay native and owner scoped.

Explicit start/prepare methods initiate provider work. Retained document search,
content, status and preview never start a model or another web fetch.
"""
from __future__ import annotations

import hashlib
from typing import Literal, cast

import httpx
from pydantic import BaseModel, ConfigDict, Field, field_validator
from stratifyx import AsyncStratifyX
from stratifyx.types import (
    DatasetBuild,
    DatasetBuildActionRequest,
    DatasetBuildAttentionList,
    DatasetBuildList,
    DatasetBuildRequest,
    DocumentCapture,
    DocumentContentPage,
    DocumentRead,
    DocumentReadList,
    DocumentSearchResponse,
    DocumentSourcePassage,
    WebResearch,
    WebResearchRequest,
    WebSourceContent,
)


class CaptureDocumentRequest(BaseModel):
    """EpochAI's explicit URL capture request; no worker/owner/storage authority."""
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)
    request_id: str = Field(min_length=1, max_length=128, description="At most 128 UTF-8 bytes.")
    url: str = Field(min_length=1, max_length=8192)

    @field_validator("request_id")
    @classmethod
    def bounded_identity(cls, value: str) -> str:
        if len(value.encode("utf-8")) > 128:
            raise ValueError("Capture request_id must fit 128 UTF-8 bytes")
        return value


def _closed(value: object) -> None:
    if isinstance(value, BaseModel):
        if value.model_extra:
            raise ValueError("The document request contains unknown contract fields")
        for field in type(value).model_fields:
            _closed(getattr(value, field))
    elif isinstance(value, (list, tuple)):
        for member in cast(list[object] | tuple[object, ...], value):
            _closed(member)
    # json_schema_text is exact authored text; do not project or reinterpret it.


class DocumentClient:
    backend: AsyncStratifyX
    document_http: httpx.AsyncClient | None = None

    def _document_http(self) -> httpx.AsyncClient:
        if self.document_http is None:
            raise ValueError("Configure an EpochAI endpoint to initiate document processing")
        return self.document_http

    async def start_web_research(self, request: WebResearchRequest) -> WebResearch:
        """Discover/read from a public question, or read explicitly supplied URLs.
        Preserve request_id for reconciliation after an uncertain acknowledgement.
        """
        _closed(request)
        response = await self._document_http().post("/api/v1/web-research",
            content=request.model_dump_json(by_alias=True, exclude_unset=True),
            headers={"Content-Type": "application/json"}, timeout=30)
        response.raise_for_status()
        result = WebResearch.model_validate_json(response.content)
        expected = "web-read:" + hashlib.sha256(request.request_id.encode()).hexdigest()
        if result.read_ref != expected:
            raise ValueError("Web research returned a different immutable identity")
        return result

    async def web_research(self, read_ref: str) -> WebResearch:
        return await self.backend.user_files.get_web_research(read_ref, request_options={"max_retries": 0})

    async def read_web_source(self, source_ref: str, *, offset: int = 0, max_bytes: int = 65536) -> WebSourceContent:
        if type(offset) is not int or offset < 0 or type(max_bytes) is not int or not 1 <= max_bytes <= 8 * 1024 * 1024:
            raise ValueError("Use a nonnegative byte offset and a budget up to 8 MiB")
        return await self.backend.user_files.read_web_source(source_ref, offset=offset, max_bytes=max_bytes, request_options={"max_retries": 0})

    async def act_web_research(self, read_ref: str, request: DatasetBuildActionRequest) -> WebResearch:
        _closed(request)
        return await self.backend.user_files.act_on_web_research(read_ref, action=request.action, attempt=request.attempt,
            result_sha256=request.result_sha256, request_options={"max_retries": 0})

    async def delete_web_research(self, read_ref: str) -> None:
        await self.backend.user_files.delete_web_research(read_ref, request_options={"max_retries": 0})

    async def prepare_web_dataset(self, request: DatasetBuildRequest) -> DatasetBuild:
        _closed(request)
        if len(request.preparation.inputs) != 1 or request.preparation.inputs[0].kind != "web_read":
            raise ValueError("Select one retained web research result")
        response = await self._document_http().post("/api/v1/web-preparations",
            content=request.model_dump_json(by_alias=True, exclude_unset=True),
            headers={"Content-Type": "application/json"}, timeout=30)
        response.raise_for_status()
        return DatasetBuild.model_validate_json(response.content)

    async def capture_document_url(self, request: CaptureDocumentRequest) -> DocumentCapture:
        """Capture exact URL bytes into Uploads. Reuse request_id after an unknown
        response; changed URLs require a new identity. No parsing/model starts.
        """
        _closed(request)
        response = await self._document_http().post("/api/v1/document-captures",
            content=request.model_dump_json(), headers={"Content-Type": "application/json"}, timeout=120)
        response.raise_for_status()
        capture = DocumentCapture.model_validate_json(response.content)
        if (capture.capture_ref != "capture:" + hashlib.sha256(request.request_id.encode()).hexdigest()
                or capture.request_url_sha256 != hashlib.sha256(request.url.encode()).hexdigest()):
            raise ValueError("Document capture returned a different immutable request identity")
        return capture

    async def document_capture(self, capture_ref: str) -> DocumentCapture:
        return await self.backend.user_files.get_document_capture(capture_ref, request_options={"max_retries": 0})

    async def delete_document_capture(self, capture_ref: str) -> None:
        await self.backend.user_files.delete_document_capture(capture_ref, request_options={"max_retries": 0})

    async def start_document_read(self, file_ref: str) -> DocumentRead:
        response = await self._document_http().post("/api/v1/document-reads", json={"file_ref": file_ref}, timeout=30)
        response.raise_for_status()
        return DocumentRead.model_validate_json(response.content)

    async def document_read(self, read_ref: str) -> DocumentRead:
        return await self.backend.user_files.get_document_read(read_ref, request_options={"max_retries": 0})

    async def current_document_reads(self, file_ref: str) -> DocumentReadList:
        return await self.backend.user_files.current_document_read(file_ref=file_ref, request_options={"max_retries": 0})

    async def delete_document_read(self, read_ref: str) -> None:
        """Explicitly retire parsed read artifacts. The original upload remains."""
        await self.backend.user_files.delete_document_read(read_ref, request_options={"max_retries": 0})

    async def document_build_attention(self) -> DatasetBuildAttentionList:
        """Lightweight unread/active build references; does not acknowledge work."""
        return await self.backend.user_files.list_dataset_preparation_attention(request_options={"max_retries": 0})

    async def document_content(self, document_version_ref: str, *, offset: int = 0, limit: int = 4, layer: Literal["primary", "element", "all"] = "primary") -> DocumentContentPage:
        if type(offset) is not int or offset < 0 or type(limit) is not int or not 1 <= limit <= 100:
            raise ValueError("Use a nonnegative offset and a block limit in 1..100")
        if layer not in {"primary", "element", "all"}:
            raise ValueError("Unknown document source layer")
        return await self.backend.user_files.read_document_content(document_version_ref, offset=offset, limit=limit, layer=layer, max_bytes=65536, request_options={"max_retries": 0})

    async def document_passage(self, document_version_ref: str, block_ref: str) -> DocumentSourcePassage:
        return await self.backend.user_files.read_document_passage(document_version_ref, block_ref, request_options={"max_retries": 0})

    async def search_documents(self, query: str, *, file_refs: list[str] | None = None, cursor: str | None = None, limit: int = 10) -> DocumentSearchResponse:
        if type(limit) is not int or not 1 <= limit <= 20:
            raise ValueError("Document search limit must be in 1..20")
        return await self.backend.user_files.search_documents(query=query, file_refs=file_refs or [], cursor=cursor, limit=limit, request_options={"max_retries": 0})

    async def prepare_document_dataset(self, request: DatasetBuildRequest) -> DatasetBuild:
        _closed(request)
        response = await self._document_http().post("/api/v1/document-preparations", content=request.model_dump_json(by_alias=True, exclude_unset=True), headers={"Content-Type": "application/json"}, timeout=30)
        response.raise_for_status()
        return DatasetBuild.model_validate_json(response.content)

    async def document_preparation(self, preparation_ref: str) -> DatasetBuild:
        return await self.backend.user_files.get_dataset_preparation(preparation_ref, request_options={"max_retries": 0})

    async def current_document_preparations(self, file_ref: str) -> DatasetBuildList:
        return await self.backend.user_files.current_dataset_preparation(file_ref=file_ref, request_options={"max_retries": 0})

    async def act_document_preparation(self, preparation_ref: str, request: DatasetBuildActionRequest) -> DatasetBuild:
        _closed(request)
        return await self.backend.user_files.act_on_dataset_preparation(preparation_ref, action=request.action, attempt=request.attempt, result_sha256=request.result_sha256,
            review_ref=request.review_ref, schema_sha256=request.schema_sha256, request_options={"max_retries": 0})

    async def act_document_read(self, read_ref: str, request: DatasetBuildActionRequest) -> DocumentRead:
        _closed(request)
        return await self.backend.user_files.act_on_document_read(read_ref, action=request.action, attempt=request.attempt, result_sha256=request.result_sha256, request_options={"max_retries": 0})
