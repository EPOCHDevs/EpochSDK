from __future__ import annotations

import asyncio
import json
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import httpx
import pytest
from langgraph_sdk.client import LangGraphClient
from mcp import Client, StdioServerParameters
from stratifyx import AsyncStratifyX
from test_supervisor import job

from epoch_sdk import EpochError
from epoch_sdk.research import EpochClient
from epoch_sdk.supervisor import SupervisorClient


@pytest.mark.parametrize("status,returned_id,expected", [
    (404, "execution-one", "NOT_FOUND"), (200, "another-execution", "INVALID_STATE"),
])
def test_native_execution_reads_keep_domain_failure_and_identity(status, returned_id, expected):
    async def scenario():
        calls = []

        def respond(request):
            calls.append(request)
            assert request.method == "GET"
            assert request.url.path == "/api/v1/studies/executions/execution-one"
            return httpx.Response(status, json=job(returned_id) if status == 200 else {
                "error": "DataNotFound", "message": "Not found", "timestamp": "2026-10-18T00:00:00Z",
            })

        async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as http:
            sdk = EpochClient(SupervisorClient(
                LangGraphClient(http),
                AsyncStratifyX(base_url="https://backend.invalid", token="fixture", httpx_client=http),
            ))
            with pytest.raises(EpochError) as error:
                await sdk.execution("execution-one")
            assert error.value.error.code == expected
            assert error.value.execution_id == "execution-one"
            assert len(calls) == 1

    asyncio.run(scenario())


def test_installed_mcp_process_reads_native_status_without_a_graph():
    """Actual stdio entrypoint and HTTP transport; synthetic native job only."""
    observed = []

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            observed.append((self.command, self.path, self.headers.get("Authorization")))
            body = json.dumps(job("execution-one", status="queued")).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *_args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    async def scenario():
        params = StdioServerParameters(command=sys.executable, args=["-m", "epoch_sdk.mcp"], env={
            "EPOCH_BACKEND_URL": f"http://127.0.0.1:{server.server_port}",
            "EPOCH_GRAPH_URL": "http://127.0.0.1:1",
            "EPOCH_TOKEN": "fixture-only",
        })
        async with Client(params) as client:
            result = await client.call_tool("epoch_execution", {"execution_id": "execution-one"})
            assert not result.is_error
            assert result.structured_content["id"] == "execution-one"
            assert result.structured_content["status"] == "queued"

    try:
        asyncio.run(scenario())
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
    assert observed == [("GET", "/api/v1/studies/executions/execution-one", "Bearer fixture-only")]
