"""Native generated web models and real MCP dispatch over controlled HTTP."""
import asyncio
import hashlib
import json

import httpx
from mcp import Client
from stratifyx.types import DatasetBuildRequest, WebResearchRequest
from test_agent_tools import Service
from test_documents import NOW, PREPARATION, REQUEST

from epoch_sdk.mcp import create_server

READ = "web-read:" + hashlib.sha256(b"web-sdk-request").hexdigest()
SOURCE = "web-source:" + "b" * 64
TEXT = "Revenue is 124."
RESEARCH_REQUEST = {"request_id": "web-sdk-request", "input": {"kind": "url", "url": "https://example.com/results"},
                    "content": {"snapshot_as_of": "2026-10-31T23:59:00Z"}}
RESEARCH = {"read_ref": READ, "request": RESEARCH_REQUEST, "state": "ready", "attempt": 1,
            "created_at": NOW, "updated_at": NOW, "message": "Sources ready", "limitations": [],
            "sources": [{"source_ref": SOURCE, "url": "https://example.com/results", "title": "Results", "state": "read",
                         "content_sha256": hashlib.sha256(TEXT.encode()).hexdigest(), "retrieved_at": NOW,
                         "snapshot_as_of": "2026-10-31T23:59:00Z", "limitations": []}]}
CONTENT = {"read_ref": READ, "source": RESEARCH["sources"][0], "text": TEXT,
           "offset": 0, "total_bytes": len(TEXT), "has_more": False}
WEB_REQUEST = {**REQUEST, "preparation": {**REQUEST["preparation"], "inputs": [{"kind": "web_read", "read_ref": READ}]}}
WEB_BUILD = {key: value for key, value in PREPARATION.items() if key != "source"}
WEB_BUILD.update(request=WEB_REQUEST, web_read_ref=READ)


class WebService(Service):
    def graph(self, request):
        if request.url.path == "/api/v1/web-research":
            self.graph_calls.append(request)
            assert json.loads(request.content) == RESEARCH_REQUEST
            return httpx.Response(200, json=RESEARCH)
        if request.url.path == "/api/v1/web-preparations":
            self.graph_calls.append(request)
            assert json.loads(request.content) == WEB_REQUEST
            return httpx.Response(200, json=WEB_BUILD)
        return super().graph(request)

    def backend(self, request):
        self.backend_calls.append(request)
        assert request.headers["Authorization"] == "Bearer fixture"
        if request.url.path == f"/api/v1/files/web/reads/{READ}":
            return httpx.Response(200, json=RESEARCH)
        if request.url.path == f"/api/v1/files/web/sources/{SOURCE}":
            assert int(request.url.params["max_bytes"]) == 65536
            return httpx.Response(200, json=CONTENT)
        raise AssertionError(request.url.path)


def test_web_sdk_preserves_source_identity_and_asof_policy():
    async def scenario():
        service = WebService()
        async with service.client() as client:
            result = await client.start_web_research(WebResearchRequest.model_validate(RESEARCH_REQUEST))
            assert result.read_ref == READ
            assert (await client.read_web_source(SOURCE)).text == TEXT
            assert (await client.web_research(READ)).sources[0].content_sha256 == CONTENT["source"]["content_sha256"]
            build = await client.prepare_web_dataset(DatasetBuildRequest.model_validate(WEB_REQUEST))
            assert build.web_read_ref == READ and build.source is None
    asyncio.run(scenario())


def test_mcp_uses_retained_web_sources_without_restarting_provider_work():
    async def scenario():
        service = WebService()
        async with service.client() as client:
            server = create_server(client)
            async with Client(server) as mcp:
                result = await mcp.call_tool("epoch_read_web_source", {"source_ref": SOURCE})
                assert not result.is_error
                assert result.structured_content["text"] == TEXT
                assert all(request.url.path == "/api/v1/agent-tools" for request in service.graph_calls)
    asyncio.run(scenario())
