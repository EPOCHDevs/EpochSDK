"""Shared controlled native transport; no composable MCP or tools-graph server."""
from contextlib import asynccontextmanager
import json
import httpx
from langgraph_sdk.client import LangGraphClient
from stratifyx import AsyncStratifyX
from epoch_sdk.research import EpochClient
from epoch_sdk.supervisor import SupervisorClient
STUDY = {"name":"Saved fixture","description":"Explicit test data","source":"fixture source","data":{"assets":[]},"authoring_origin":"agent"}

class Service:
    def __init__(self):
        self.graph_calls = []
        self.backend_calls = []
        self.native_status = "running"
        self.messages = []
        self.metadata = {}
        self.study_registry = {}
        self.owner_denied = False

    def graph(self, request):
        self.graph_calls.append(request)
        raise AssertionError("An ordinary native client must not call a tools graph")

    def backend(self, request):
        self.backend_calls.append(request)
        path = request.url.path
        assert request.headers["Authorization"] == "Bearer fixture"
        if path == "/api/v1/studies/definitions/study-one":
            return httpx.Response(200, json=STUDY)
        if path == "/api/v1/studies/definitions":
            return httpx.Response(200, json=["study-one", "study-two"])
        if path == "/api/v1/studies/executions" and request.method == "GET":
            return httpx.Response(200, json=["execution-one"])
        if path == "/api/v1/studies/executions" and request.method == "POST":
            body = json.loads(request.content)
            assert body["id"] == "study-one" and body["period"]["start"] == "2024-01-01"
            assert "response_plan" not in body
            return httpx.Response(
                200, json={"id": "execution-one", "message": "Execution accepted"}
            )
        if path == "/api/v1/studies/executions/execution-one/study":
            if self.owner_denied:
                return httpx.Response(
                    404,
                    json={
                        "error": "DataNotFound",
                        "message": "Unavailable",
                        "timestamp": "2026-10-20T00:00:00Z",
                    },
                )
            return httpx.Response(
                200,
                json={
                    "execution_id": "execution-one",
                    "definition_id": "study-one",
                    "captured_at": 1,
                    "study": STUDY,
                },
            )
        if path == "/api/v1/studies/executions/execution-one":
            return httpx.Response(
                200,
                json={
                    "id": "execution-one",
                    "definition_id": "study-one",
                    "created_at": 1,
                    "execution_type": "research",
                    "status": "completed",
                },
            )
        raise AssertionError(f"Unexpected Backend request: {request.method} {path}")

    @asynccontextmanager
    async def client(self):
        async with (
            httpx.AsyncClient(
                base_url="https://graph.invalid", transport=httpx.MockTransport(self.graph)
            ) as graph_http,
            httpx.AsyncClient(transport=httpx.MockTransport(self.backend)) as backend_http,
        ):
            yield EpochClient(SupervisorClient(
                LangGraphClient(graph_http),
                AsyncStratifyX(base_url="https://backend.invalid", token="fixture", httpx_client=backend_http),
                document_http=graph_http,
            ))

