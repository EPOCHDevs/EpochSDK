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


@pytest.mark.parametrize(
    "status,returned_id,expected",
    [
        (404, "execution-one", "NOT_FOUND"),
        (200, "another-execution", "INVALID_STATE"),
    ],
)
def test_native_execution_reads_keep_domain_failure_and_identity(status, returned_id, expected):
    async def scenario():
        calls = []

        def respond(request):
            calls.append(request)
            assert request.method == "GET"
            assert request.url.path == "/api/v1/studies/executions/execution-one"
            return httpx.Response(
                status,
                json=job(returned_id)
                if status == 200
                else {
                    "error": "DataNotFound",
                    "message": "Not found",
                    "timestamp": "2026-10-18T00:00:00Z",
                },
            )

        async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as http:
            sdk = EpochClient(
                SupervisorClient(
                    LangGraphClient(http),
                    AsyncStratifyX(
                        base_url="https://backend.invalid", token="fixture", httpx_client=http
                    ),
                )
            )
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
            value = (
                {
                    "request_id": "req_" + "1" * 32,
                    "execution_id": "execution-one",
                    "phase": "active",
                    "created_at_ms": 1,
                    "request": {
                        "operation_id": "prepared-one",
                        "study_id": "study-one",
                        "source_execution_id": "old",
                        "parameters": {"period": {"start": "2025-01-01"}},
                    },
                }
                if self.path.startswith("/api/v1/integration/execution-requests/")
                else job("execution-one", status="queued")
            )
            body = json.dumps(value).encode()
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
        params = StdioServerParameters(
            command=sys.executable,
            args=["-m", "epoch_sdk.workflow_mcp"],
            env={
                "EPOCH_BACKEND_URL": f"http://127.0.0.1:{server.server_port}",
                "EPOCH_GRAPH_URL": "http://127.0.0.1:1",
                "EPOCH_TOKEN": "fixture-only",
            },
        )
        async with Client(params) as client:
            assert {tool.name for tool in (await client.list_tools()).tools} == {
                "epoch_run",
                "epoch_execute",
                "epoch_resume",
                "epoch_status",
                "epoch_read",
            }
            result = await client.call_tool(
                "epoch_status", {"operation_id": "prepared-one", "kind": "execute"}
            )
            assert not result.is_error
            assert result.structured_content["execution"]["id"] == "execution-one"
            assert result.structured_content["execution"]["status"] == "queued"

    try:
        asyncio.run(scenario())
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
    assert len(observed) == 2 and all(
        item[0] == "GET" and item[2] == "Bearer fixture-only" for item in observed
    )
    assert observed[0][1].startswith("/api/v1/integration/execution-requests/")
    assert observed[1][1] == "/api/v1/studies/executions/execution-one"
