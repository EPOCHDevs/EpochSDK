"""Installed native models and MCP dispatch over captured HTTP, never a provider call."""
from __future__ import annotations

import asyncio
import hashlib
import json
from pathlib import Path

import httpx
import pytest
from jsonschema import Draft202012Validator, FormatChecker
from mcp import Client
from mcp.types import ResourceLink, TextResourceContents
from stratifyx.types import DatasetBuildRequest
from test_agent_tools import Service

from epoch_sdk.documents import CaptureDocumentRequest
from epoch_sdk.mcp import create_server

FILE = "file:" + "a" * 64
READ = "document-read:" + "b" * 64
VERSION = "document:" + "c" * 64
BLOCK = "block:" + "d" * 64
BUILD = "preparation:" + "e" * 64
DATASET = "dataset:" + "f" * 64
NOW = "2026-11-01T00:00:00Z"
ORIGINAL = b"Revenue: 9007199254740993; approved: false"
SOURCE = {"file_ref": FILE, "name": "Revenue.txt", "media_type": "text/plain",
    "size_bytes": len(ORIGINAL), "status": "uploaded", "created_at": NOW,
    "content_sha256": hashlib.sha256(ORIGINAL).hexdigest()}
PDF_ORIGINAL = b"%PDF-1.7\nRevenue: 9007199254740993; approved: false"
PDF_SHA256 = hashlib.sha256(PDF_ORIGINAL).hexdigest()
PDF_FILE = "file:" + PDF_SHA256
PDF_SOURCE = {**SOURCE, "file_ref": PDF_FILE, "name": "Revenue.pdf",
    "media_type": "application/pdf", "size_bytes": len(PDF_ORIGINAL),
    "content_sha256": PDF_SHA256}
OPERATION = {"read_ref": READ, "source": SOURCE, "state": "ready", "attempt": 1,
    "message": "Source text is ready", "created_at": NOW, "updated_at": NOW,
    "document_version_ref": VERSION, "coverage": {"processed_pages": [], "unread_pages": []},
    "limitations": ["Native text has no physical page locations."]}
PASSAGE = {"document_version_ref": VERSION, "source": SOURCE,
    "content_sha256": "1" * 64, "block": {"block_ref": BLOCK, "kind": "text",
        "text": ORIGINAL.decode(), "layer": "primary"}}
CONTENT = {"document_version_ref": VERSION, "source": SOURCE, "content_sha256": "1" * 64,
    "provider_version": "utf8-v1", "coverage": OPERATION["coverage"],
    "limitations": OPERATION["limitations"], "blocks": [PASSAGE["block"]],
    "offset": 0, "total_blocks": 1, "has_more": False, "layer": "primary"}
REQUEST = {"request_id": "document-sdk-request", "name": "Reported revenue",
    "preparation": {"inputs": [{"kind": "file", "file_ref": PDF_FILE}], "instruction": "Reported revenue",
        "output_format": "json", "schema_choice": {"mode": "provided",
            "json_schema_text": '{"type":"integer"}'},
        "purpose": "knowledge", "enrichment": {"mode": "automatic"}}}
PREPARATION = {"preparation_ref": BUILD, "request": REQUEST, "source": PDF_SOURCE,
    "state": "queued", "attempt": 1, "message": "Queued", "created_at": NOW,
    "updated_at": NOW, "limitations": [], "coverage": OPERATION["coverage"], "acknowledged": False}


def test_captured_document_wire_fixtures_agree_with_projected_service_contracts():
    contract = json.loads((Path(__file__).resolve().parents[3] / "contracts/openapi.json").read_text())
    projected_paths = set(contract["x-epoch-document-operations"]["paths"])
    cases = [
        ("/api/v1/files/documents/reads/{readRef}", "get", "200", OPERATION),
        ("/api/v1/files/documents/{documentVersionRef}/blocks", "get", "200", CONTENT),
        ("/api/v1/files/documents/{documentVersionRef}/blocks/{blockRef}", "get", "200", PASSAGE),
        ("/api/v1/files/documents/search", "post", "request", {"query": "Revenue", "file_refs": [FILE], "limit": 20}),
        ("/api/v1/files/documents/search", "post", "200", {"matches": [PASSAGE], "filename_matches": [],
            "filename_match_count": 0, "unprepared_files": [], "unprepared_count": 0,
            "prepared_count": 1, "incomplete_count": 0, "limitations": []}),
        ("/api/v1/files/preparations/{preparationRef}", "get", "200", PREPARATION),
        ("/api/v1/document-reads", "post", "request", {"file_ref": FILE}),
        ("/api/v1/document-reads", "post", "200", OPERATION),
        ("/api/v1/document-preparations", "post", "request", REQUEST),
        ("/api/v1/document-preparations", "post", "200", PREPARATION),
    ]
    for path, method, role, value in cases:
        assert path in projected_paths
        operation = contract["paths"][path][method]
        container = operation["requestBody"] if role == "request" else operation["responses"][role]
        schema = container["content"]["application/json"]["schema"]
        Draft202012Validator({"allOf": [schema], "components": contract["components"]},
            format_checker=FormatChecker()).validate(value)


class DocumentsService(Service):
    def __init__(self):
        super().__init__()
        self.json_bytes = b'{"value":9007199254740993,"decimal":0.12345678901234567890123456789,"approved":false}'
        self.content_type = "application/json"
        self.content_length: str | None = None
        self.capture_mismatch = False

    def backend(self, request):
        self.backend_calls.append(request)
        assert request.headers["Authorization"] == "Bearer fixture"
        if self.owner_denied:
            return httpx.Response(404, json={"error": "DataNotFound", "message": "Unavailable", "timestamp": NOW})
        path = request.url.path
        if path == f"/api/v1/files/documents/reads/{READ}":
            return httpx.Response(200, json=OPERATION)
        if path == f"/api/v1/files/documents/{VERSION}/blocks":
            assert request.url.params["layer"] == "primary"
            assert int(request.url.params["max_bytes"]) <= 65536
            return httpx.Response(200, json=CONTENT)
        if path == f"/api/v1/files/documents/{VERSION}/blocks/{BLOCK}":
            return httpx.Response(200, json=PASSAGE)
        if path == "/api/v1/files/documents/search":
            body = json.loads(request.content)
            assert body["query"] == "Revenue" and body["file_refs"] == [FILE]
            return httpx.Response(200, json={"matches": [PASSAGE], "filename_matches": [],
                "filename_match_count": 0, "unprepared_files": [], "unprepared_count": 0,
                "prepared_count": 1, "incomplete_count": 0, "limitations": []})
        if path == f"/api/v1/files/preparations/{BUILD}":
            return httpx.Response(200, json=PREPARATION)
        if path == f"/api/v1/files/datasets/{DATASET}/preview":
            return httpx.Response(200, json={"target": {"kind": "saved", "dataset_ref": DATASET},
                "content": {"format": "json", "json_pointer": "", "json_text": self.json_bytes.decode()}})
        if path == f"/api/v1/files/datasets/{DATASET}/content":
            headers = {"Content-Type": self.content_type}
            if self.content_length is not None:
                headers["Content-Length"] = self.content_length
            return httpx.Response(200, content=self.json_bytes, headers=headers)
        raise AssertionError(f"Unexpected native request: {request.method} {path}")

    def graph(self, request):
        path = request.url.path
        if path.startswith("/api/v1/document-"):
            self.graph_calls.append(request)
            body = json.loads(request.content)
            if path == "/api/v1/document-reads":
                assert body == {"file_ref": FILE}
                return httpx.Response(200, json=OPERATION)
            if path == "/api/v1/document-preparations":
                assert body == REQUEST
                return httpx.Response(200, json=PREPARATION)
            if path == "/api/v1/document-captures":
                ref = "capture:" + hashlib.sha256(body["request_id"].encode()).hexdigest()
                return httpx.Response(200, json={"capture_ref": ref,
                    "request_url_sha256": "0" * 64 if self.capture_mismatch else hashlib.sha256(body["url"].encode()).hexdigest(),
                    "source_url": "https://example.org/report.txt", "final_url": "https://example.org/report.txt",
                    "captured_at": NOW, "file": SOURCE})
            raise AssertionError(path)
        return super().graph(request)


@pytest.mark.parametrize("identity", ["é" * 64, "😀" * 32])
def test_capture_identity_accepts_exact_utf8_boundary(identity):
    request = CaptureDocumentRequest(request_id=identity, url="https://example.org/report.pdf")
    assert request.request_id == identity


@pytest.mark.parametrize("identity", ["é" * 65, "😀" * 33, "\ud800"])
def test_capture_identity_rejects_oversized_or_invalid_utf8_before_transport(identity):
    with pytest.raises(ValueError):
        CaptureDocumentRequest(request_id=identity, url="https://example.org/report.pdf")


def test_native_reads_never_start_a_graph_or_processing_request():
    async def scenario():
        service = DocumentsService()
        async with service.client() as sdk:
            assert (await sdk.document_read(READ)).document_version_ref == VERSION
            assert (await sdk.document_content(VERSION)).blocks[0].block_ref == BLOCK
            assert (await sdk.document_passage(VERSION, BLOCK)).source.file_ref == FILE
            assert (await sdk.search_documents("Revenue", file_refs=[FILE])).prepared_count == 1
            assert (await sdk.document_preparation(BUILD)).preparation_ref == BUILD
            assert service.graph_calls == []
    asyncio.run(scenario())


def test_explicit_processing_preserves_exact_identity_and_url_digest():
    async def scenario():
        service = DocumentsService()
        async with service.client() as sdk:
            assert (await sdk.start_document_read(FILE)).read_ref == READ
            assert (await sdk.prepare_document_dataset(DatasetBuildRequest.model_validate(REQUEST))).preparation_ref == BUILD
            capture = CaptureDocumentRequest(request_id="same-url", url="https://example.org/report.txt?signature=private")
            assert (await sdk.capture_document_url(capture)).file.file_ref == FILE
            service.capture_mismatch = True
            with pytest.raises(ValueError, match="immutable request identity"):
                await sdk.capture_document_url(capture)
            assert service.backend_calls == []
            assert all(not request.url.path.startswith("/threads") for request in service.graph_calls)
    asyncio.run(scenario())


@pytest.mark.parametrize("value", [True, -1, "0", 1.5])
def test_document_content_limits_reject_coercion_before_transport(value):
    async def scenario():
        service = DocumentsService()
        async with service.client() as sdk:
            with pytest.raises(ValueError):
                await sdk.document_content(VERSION, offset=value)
            assert service.backend_calls == service.graph_calls == []
    asyncio.run(scenario())


@pytest.mark.parametrize("payload", [b'{"value":9007199254740993,"decimal":0.12345678901234567890123456789,"approved":false}', b"false", b'"Exact text \\n -0"', b"9007199254740993"])
def test_mcp_json_resource_keeps_every_original_numeric_token_and_false(payload):
    async def scenario():
        service = DocumentsService()
        service.json_bytes = payload
        async with service.client() as sdk, Client(create_server(sdk)) as mcp:
            result = await mcp.call_tool("epoch_dataset_content", {"dataset_ref": DATASET})
            assert not result.is_error and isinstance(result.content[0], ResourceLink)
            assert result.content[0].mime_type == "application/json"
            resource = await mcp.read_resource(result.content[0].uri)
            assert isinstance(resource.contents[0], TextResourceContents)
            assert resource.contents[0].text.encode() == service.json_bytes
            assert service.graph_calls and all(r.url.path == "/api/v1/agent-tools" for r in service.graph_calls)
    asyncio.run(scenario())


def test_mcp_owner_denial_and_unknown_authority_are_errors_without_source_disclosure():
    async def scenario():
        service = DocumentsService()
        async with service.client() as sdk, Client(create_server(sdk)) as mcp:
            for tool, args in [("epoch_read_documents", {"document_version_ref": VERSION, "owner": "bob"}),
                ("epoch_prepare_document_dataset", {"request": {**REQUEST, "owner": "bob"}})]:
                result = await mcp.call_tool(tool, args)
                assert result.is_error and service.backend_calls == []
            service.owner_denied = True
            result = await mcp.call_tool("epoch_document_read", {"read_ref": READ})
            assert result.is_error and ORIGINAL.decode() not in str(result)
    asyncio.run(scenario())


@pytest.mark.parametrize("kind", ["mime", "length", "hash", "budget"])
def test_complete_content_download_enforces_transport_and_integrity_bounds(kind):
    async def scenario():
        service = DocumentsService()
        if kind == "mime": service.content_type = "text/html"
        if kind == "length": service.content_length = str(len(service.json_bytes) + 1)
        async with service.client() as sdk:
            with pytest.raises(ValueError):
                await sdk.download_dataset(DATASET, max_bytes=1 if kind == "budget" else 4096,
                    expected_sha256="0" * 64 if kind == "hash" else None)
    asyncio.run(scenario())
