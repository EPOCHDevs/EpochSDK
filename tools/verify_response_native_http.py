"""Prove SDK/MCP response transport against the native loopback fixture.

The fixture uses synthetic execution references. This is not real study or
model integration evidence; it proves the response API boundary and storage.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import socket
import subprocess
import tempfile
import time
from pathlib import Path

import httpx
from epoch_sdk.contracts import TableOutputRequest
from epoch_sdk.mcp import create_server
from epoch_sdk.responses import (
    ResearchResponseContent,
    ResponseTableSource,
    assemble_response,
)
from epoch_sdk.supervisor import SupervisorClient
from langgraph_sdk.client import LangGraphClient
from mcp import Client
from stratifyx import AsyncStratifyX
from stratifyx._release import SDK_RELEASE

ROOT = Path(__file__).resolve().parents[1]


async def verify(url: str) -> None:
    def no_graph(request: httpx.Request) -> httpx.Response:
        raise AssertionError("Reading/publishing a response must not invoke an agent")

    async with (
        httpx.AsyncClient(timeout=10) as backend_http,
        httpx.AsyncClient(transport=httpx.MockTransport(no_graph)) as graph_http,
    ):
        backend = AsyncStratifyX(
            base_url=url, token="sdk-fixture-owner", httpx_client=backend_http
        )
        sdk = SupervisorClient(LangGraphClient(graph_http), backend)
        content = ResearchResponseContent.model_validate(
            json.loads((ROOT / "contracts/research-response.example.json").read_text())[
                "content"
            ]
        )
        # The native fixture supplies a computed relation without dashboard exhibits.
        # Binding and reading the source succeed independently of presentation.
        selected = await assemble_response(
            backend,
            "native-one",
            "study-one",
            [
                TableOutputRequest(
                    name="sales",
                    type="table",
                    schema=[
                        {
                            "name": "year",
                            "type": "int64",
                            "description": "Calendar year",
                        },
                        {
                            "name": "sales",
                            "type": "float64",
                            "nullable": True,
                            "unit": "USD",
                        },
                    ],
                )
            ],
            [],
            table_sources=[
                ResponseTableSource(
                    name="sales", table="computed_sales", field_ids=["year", "sales"]
                )
            ],
        )
        assert selected.to_wire()["outputs"][0]["source"] == {
            "execution_id": "native-one",
            "table": "computed_sales",
            "field_ids": ["year", "sales"],
            "row_count": 2,
        }
        selected_answer = await sdk.publish_response(
            "selected-table",
            selected,
            thread_id="thread-one",
            primary_execution_id="native-one",
        )
        page = await sdk.response_table(
            selected_answer.response_id, "sales", page_size=1
        )
        assert page.rows == [["2025", None]] and page.next_offset == 1
        page = await sdk.response_table(
            selected_answer.response_id, "sales", offset=1, page_size=1
        )
        assert page.rows == [["9007199254740993", 12.5]] and page.next_offset is None

        # Large, non-temporal tables retain repeated labels and requested ranking.
        large = json.loads(
            (ROOT / "contracts/research-response-reference.example.json").read_text()
        )["content"]
        large["outputs"][0]["source"]["execution_id"] = "native-one"
        large["outputs"][0]["source"]["order_by"] = [
            {"field_id": "value", "descending": True}
        ]
        large_answer = await sdk.publish_response(
            "large-table",
            ResearchResponseContent.model_validate(large),
            thread_id="thread-one",
            primary_execution_id="native-one",
        )
        all_rows = []
        async for page in sdk.iter_response_table(
            large_answer.response_id, "results", page_size=5000
        ):
            assert page.total_rows == 25003 and len(page.rows) <= 5000
            all_rows.extend(page.rows)
        assert [int(row[1]) for row in all_rows] == list(range(25002, -1, -1))
        assert all(row[0] == ("B" if int(row[1]) % 2 else "A") for row in all_rows)
        assert len(json.dumps(large_answer.to_wire())) < 4096
        execution_free = ResearchResponseContent.model_validate(
            {
                "declarations": [
                    {"name": "answer", "type": "json", "schema": {"type": "null"}}
                ],
                "outputs": [{"name": "answer", "type": "json", "value": None}],
            }
        )
        ordinary = await sdk.publish_response(
            "ordinary-query", execution_free, thread_id="thread-one"
        )
        assert ordinary.primary_execution_id is None and ordinary.study_id is None
        assert (await sdk.response(ordinary.response_id)).content == execution_free
        first = await sdk.publish_response(
            "query-one",
            content,
            thread_id="thread-one",
            primary_execution_id="native-one",
        )
        assert first.version == 1 and first.content == content
        # A fresh SDK object reads the native record; it owns no response cache.
        fresh = SupervisorClient(
            LangGraphClient(graph_http),
            AsyncStratifyX(
                base_url=url,
                token="sdk-fixture-owner",
                httpx_client=backend_http,
            ),
        )
        assert await fresh.response(first.response_id) == first
        async with Client(create_server(fresh)) as mcp:
            gathered = []
            offset = 0
            while True:
                native_page = await mcp.call_tool(
                    "epoch_response_table",
                    {
                        "response_id": large_answer.response_id,
                        "name": "results",
                        "version": 1,
                        "offset": offset,
                        "page_size": 5000,
                    },
                )
                assert not native_page.is_error
                data = native_page.structured_content
                assert data["version"] == 1 and data["total_rows"] == 25003
                gathered.extend(data["rows"])
                if data["next_offset"] is None:
                    break
                offset = data["next_offset"]
            assert gathered == all_rows
            read = await mcp.call_tool(
                "epoch_response", {"response_id": first.response_id}
            )
            assert not read.is_error and read.structured_content == first.to_wire()
            changed = content.to_wire()
            changed["outputs"][2]["value"] = (
                "Updated interpretation from the MCP client."
            )
            updated = await mcp.call_tool(
                "epoch_publish_response",
                {
                    "request_id": "query-one",
                    "thread_id": "thread-one",
                    "primary_execution_id": "native-one",
                    "expected_version": 1,
                    "content": changed,
                },
            )
            assert not updated.is_error and updated.structured_content["version"] == 2
            old = await mcp.call_tool(
                "epoch_response", {"response_id": first.response_id, "version": 1}
            )
            assert not old.is_error and old.structured_content == first.to_wire()
            stale = await mcp.call_tool(
                "epoch_publish_response",
                {
                    "request_id": "query-one",
                    "thread_id": "thread-one",
                    "primary_execution_id": "native-one",
                    "expected_version": 1,
                    "content": changed,
                },
            )
            assert (
                not stale.is_error
                and stale.structured_content["error"]["code"] == "INVALID_STATE"
            )
        other = SupervisorClient(
            LangGraphClient(graph_http),
            AsyncStratifyX(
                base_url=url,
                token="sdk-fixture-other",
                httpx_client=backend_http,
            ),
        )
        async with Client(create_server(other)) as mcp:
            denied = await mcp.call_tool(
                "epoch_response", {"response_id": first.response_id}
            )
            assert (
                not denied.is_error
                and denied.structured_content["error"]["code"] == "NOT_FOUND"
            )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    binary = args.binary.resolve(strict=True)
    with tempfile.TemporaryDirectory(prefix="epoch-response-sdk-mcp-") as temporary:
        root = Path(temporary)
        storage = root / "storage"
        storage.mkdir()
        with socket.socket() as reserved:
            reserved.bind(("127.0.0.1", 0))
            port = reserved.getsockname()[1]
        with (root / "server.log").open("w") as log:
            server = subprocess.Popen(
                [str(binary), str(port), str(storage)],
                cwd=binary.parent,
                stdout=log,
                stderr=subprocess.STDOUT,
            )
            try:
                for _ in range(100):
                    if server.poll() is not None:
                        raise RuntimeError((root / "server.log").read_text()[-3000:])
                    try:
                        with socket.create_connection(("127.0.0.1", port), timeout=0.1):
                            break
                    except OSError:
                        time.sleep(0.1)
                else:
                    raise RuntimeError("Native response fixture did not listen")
                asyncio.run(verify(f"http://127.0.0.1:{port}"))
            finally:
                server.terminate()
                try:
                    server.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    server.kill()
                    server.wait(timeout=10)
    proof = {
        "scope": "sdk-and-mcp-native-response-component",
        "native_binary_sha256": hashlib.sha256(binary.read_bytes()).hexdigest(),
        "native_sdk_release": SDK_RELEASE,
        "checks": [
            "native-table-reference-without-dashboard",
            "int64-null-pages",
            "sdk-complete-25003-row-ranked-traversal",
            "mcp-complete-25003-row-ranked-traversal",
            "bounded-answer-metadata",
            "execution-free-json-null-answer",
            "sdk-publication",
            "fresh-sdk-read",
            "mcp-read",
            "mcp-post-analysis-update",
            "earlier-revision",
            "stale-edit-domain-error",
            "owner-isolation",
            "no-agent-call",
        ],
        "real_analysis_proven": False,
    }
    args.output.write_text(json.dumps(proof, indent=2) + "\n")
    print(json.dumps(proof, indent=2))


if __name__ == "__main__":
    main()
