"""Native client/MCP transport checks; live acceptance is a separate real-HTTP gate."""
from __future__ import annotations

import asyncio
import base64
import hashlib
import json
import math

import httpx
import pyarrow as pa
import pytest
from mcp import Client
from mcp.types import BlobResourceContents, ResourceLink
from test_agent_tools import Service

from epoch_sdk.mcp import create_server

FILE = "file:" + "a" * 64
DATASET = "dataset:" + "b" * 64
FOLDER = "folder:" + "c" * 64


class FilesService(Service):
    def __init__(self):
        super().__init__()
        self.uploaded = False
        self.parts: list[bytes] = []
        self.name = "data.bin"
        self.folder_name = "Research"
        self.upload_size = 0
        self.digest = ""
        table = pa.table({"value": pa.array([9007199254740993], type=pa.uint64()),
                          "text": ["x" * (1024 * 1024 + 128)]})
        buffer = pa.BufferOutputStream()
        with pa.ipc.new_file(buffer, table.schema) as writer:
            writer.write_table(table)
        self.arrow = buffer.getvalue().to_pybytes()

    def descriptor(self):
        return {"file_ref": FILE, "name": self.name, "media_type": "application/octet-stream",
                "size_bytes": self.upload_size, "status": "uploaded",
                "created_at": "2026-10-27T00:00:00Z", "content_sha256": self.digest}

    def backend(self, request):
        self.backend_calls.append(request)
        assert request.headers["Authorization"] == "Bearer fixture"
        path = request.url.path
        if path == "/api/v1/files/uploads":
            body = json.loads(request.content)
            self.upload_size = body["size_bytes"]
            self.digest = body["content_sha256"]
            self.name = body["name"]
            return httpx.Response(200, json={
                "file_ref": FILE, "upload_id": "generation",
                "status": "uploaded" if self.uploaded else "uploading",
                "upload_url": f"/api/v1/files/{FILE}/content?upload_id=generation",
                "required_headers": {}, "chunk_size_bytes": 4,
                "part_count": math.ceil(self.upload_size / 4),
            })
        if path == f"/api/v1/files/{FILE}/content" and request.method == "PUT":
            assert request.url.params["upload_id"] == "generation"
            assert int(request.url.params["part_index"]) == len(self.parts)
            self.parts.append(request.content)
            return httpx.Response(204)
        if path == f"/api/v1/files/{FILE}/complete":
            assert hashlib.sha256(b"".join(self.parts)).hexdigest() == self.digest
            self.uploaded = True
            return httpx.Response(200, json=self.descriptor())
        if path == f"/api/v1/files/{FILE}":
            return httpx.Response(200, json={"file": self.descriptor(), "referenced_by": []})
        if path == "/api/v1/space/folders":
            self.folder_name = json.loads(request.content)["name"]
            return httpx.Response(200, json={"folder_ref": FOLDER, "name": self.folder_name,
                                            "parent_folder_ref": None})
        if path == "/api/v1/space/resources":
            body = json.loads(request.content)
            return httpx.Response(200, json={"resource": body["resource"],
                "folder_ref": body.get("folder_ref"), "name": body.get("name") or self.name})
        if path == "/api/v1/space":
            return httpx.Response(200, json={"items": [{"kind": "folder", "folder_ref": FOLDER,
                "name": self.folder_name, "parent_folder_ref": None}], "next_cursor": None})
        if path == f"/api/v1/files/datasets/{DATASET}/preview":
            return httpx.Response(200, json={"target": {"kind": "saved", "dataset_ref": DATASET},
                "content": {"format": "table", "field_ids": ["value", "text"], "rows": [],
                "offset": 0, "total_rows": 1, "next_cursor": None, "requires_download": True}})
        if path == f"/api/v1/files/datasets/{DATASET}/content":
            return httpx.Response(200, content=self.arrow,
                                  headers={"Content-Type": "application/vnd.apache.arrow.file"})
        raise AssertionError(f"Unexpected native call: {request.method} {path}")


def test_upload_chunks_binary_content_and_reuses_completed_native_identity():
    async def scenario():
        service = FilesService()
        content = b"binary\x00\xffdata"
        async with service.client() as sdk:
            first = await sdk.upload_file(content, name="data.bin", media_type="application/octet-stream")
            again = await sdk.upload_file(content, name="data.bin", media_type="application/octet-stream")
            assert first.file_ref == again.file_ref == FILE
            assert b"".join(service.parts) == content
            assert len(service.parts) == 3
            assert service.graph_calls == []
            assert sum(r.url.path.endswith("/complete") for r in service.backend_calls) == 1
    asyncio.run(scenario())


@pytest.mark.parametrize("limit", [0, 101, True, "1", 1.0])
def test_space_page_limits_are_not_coerced_before_transport(limit):
    async def scenario():
        service = FilesService()
        async with service.client() as sdk:
            with pytest.raises(ValueError):
                await sdk.browse_space(limit=limit)
            assert service.backend_calls == service.graph_calls == []
    asyncio.run(scenario())


def test_space_mcp_keeps_refs_and_serves_complete_binary_data_as_a_resource():
    async def scenario():
        service = FilesService()
        async with service.client() as sdk, Client(create_server(sdk)) as mcp:
            tools = {item.name: item for item in (await mcp.list_tools()).tools}
            assert tools["epoch_space_browse"].input_schema["additionalProperties"] is False
            folder = await mcp.call_tool("epoch_space_create_folder", {"name": "Research"})
            assert not folder.is_error and folder.structured_content["folder_ref"] == FOLDER
            placed = await mcp.call_tool("epoch_space_place_resource", {
                "resource": {"kind": "file", "ref": FILE}, "folder_ref": FOLDER, "name": "Saved file",
            })
            assert not placed.is_error
            assert placed.structured_content["resource"]["ref"] == FILE
            assert placed.structured_content["name"] == "Saved file"
            preview = await mcp.call_tool("epoch_preview_dataset", {"dataset_ref": DATASET})
            assert not preview.is_error
            assert preview.structured_content["content"]["requires_download"] is True
            link = await mcp.call_tool("epoch_dataset_content", {"dataset_ref": DATASET})
            assert not link.is_error and isinstance(link.content[0], ResourceLink)
            result = await mcp.read_resource(link.content[0].uri)
            assert isinstance(result.contents[0], BlobResourceContents)
            content = base64.b64decode(result.contents[0].blob, validate=True)
            assert content == service.arrow
            table = pa.ipc.open_file(pa.BufferReader(content)).read_all()
            assert table.column("value")[0].as_py() == 9007199254740993
            assert len(table.column("text")[0].as_py()) == 1024 * 1024 + 128
            assert await sdk.download_dataset(DATASET) == content
            assert all(r.url.path == "/api/v1/agent-tools" for r in service.graph_calls)
    asyncio.run(scenario())


def test_mcp_rejects_unknown_authority_fields_without_native_work():
    async def scenario():
        service = FilesService()
        async with service.client() as sdk, Client(create_server(sdk)) as mcp:
            result = await mcp.call_tool("epoch_space_create_folder", {"name": "Research", "owner_user_id": "bob"})
            assert result.is_error
            assert service.backend_calls == []
            result = await mcp.call_tool("epoch_upload_file", {"name": "data.bin", "media_type": "application/octet-stream", "content_base64": "invalid!"})
            assert result.is_error and service.backend_calls == []
    asyncio.run(scenario())
