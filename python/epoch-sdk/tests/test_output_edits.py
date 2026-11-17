"""Generated-client routing controls; native service acceptance is recorded separately."""
import asyncio
import copy
import json
from pathlib import Path

import httpx
import pytest
from stratifyx import AsyncStratifyX
from stratifyx.types import CreateExecutionOutputEdit, ExecutionOutputEditKind, ExecutionResponseTextEdit

from epoch_sdk.extensions import ExecutionExtensionClient

FIXTURES = Path(__file__).parent / "fixtures/execution_extensions"
RECORD = json.loads((FIXTURES / "execution-record.json").read_text())


def test_output_edit_reads_reconnect_and_history_preserve_execution_identity():
    async def scenario():
        execution = RECORD["execution_id"]
        first = {"execution_id": execution, "version": 1, "sha256": "a" * 64}
        second = {"execution_id": execution, "version": 2, "sha256": "b" * 64}
        body = CreateExecutionOutputEdit(operation_id="edit-words", expected_revision=1,
            kind=ExecutionOutputEditKind.RESPONSE_TEXT,
            response_text=[ExecutionResponseTextEdit(name="answer", value="Updated wording.")])
        edit = {"execution_id": execution, "request_id": "req_" + "c" * 32,
                "request": body.model_dump(mode="json", exclude_none=True), "phase": "completed",
                "accepted_revision": second}
        calls = []

        def handle(request):
            calls.append((request.method, request.url.path))
            assert request.headers["Authorization"] == "Bearer fixture"
            base = f"/api/v1/studies/executions/{execution}"
            if request.url.path == base + "/outputs":
                result = copy.deepcopy(RECORD)
                result["output_revision"] = first if request.url.params.get("revision") == "1" else second
                return httpx.Response(200, json=result)
            if request.method == "POST" and request.url.path == base + "/output-edits":
                assert json.loads(request.content) == edit["request"]
                return httpx.Response(200, json=edit)
            if request.url.path == base + "/output-revisions":
                return httpx.Response(200, json={"execution_id": execution, "offset": 0,
                                                "total": 2, "revisions": [first, second]})
            if request.url.path.startswith(base + "/output-edits/"):
                return httpx.Response(200, json=edit)
            raise AssertionError("An output edit cannot launch computation or an AI graph")

        async with httpx.AsyncClient(transport=httpx.MockTransport(handle)) as http:
            client = ExecutionExtensionClient()
            client.backend = AsyncStratifyX(base_url="https://native.invalid", token="fixture", httpx_client=http)
            current = await client.execution_outputs(execution)
            historical = await client.execution_outputs(execution, revision=1)
            assert current.output_revision.version == 2 and historical.output_revision.version == 1
            accepted = await client.edit_outputs(execution, body)
            assert accepted.execution_id == execution and accepted.accepted_revision.version == 2
            assert await client.output_edit_status(execution, accepted.request_id) == accepted
            assert await client.output_edit_by_handle(execution, body.operation_id) == accepted
            # Cancel after acceptance returns the original completed receipt.
            assert await client.cancel_output_edit(execution, accepted.request_id) == accepted
            page = await client.output_revisions(execution)
            assert page.total == 2 and [item.version for item in page.revisions] == [1, 2]
            assert sum(method == "POST" and path.endswith("/output-edits") for method, path in calls) == 1
            assert all("/integration/execution-requests" not in path for _, path in calls)
    asyncio.run(scenario())


def test_output_edit_rejects_unknown_numerical_fields_before_transport():
    async def scenario():
        def unused(_):
            raise AssertionError("Invalid edit arguments must never reach transport")
        async with httpx.AsyncClient(transport=httpx.MockTransport(unused)) as http:
            client = ExecutionExtensionClient()
            client.backend = AsyncStratifyX(base_url="https://native.invalid", token="fixture", httpx_client=http)
            request = CreateExecutionOutputEdit.model_validate({"operation_id": "edit-words", "expected_revision": 1,
                "kind": "response_text", "response_text": [{"name": "answer", "value": "Updated."}],
                "period": {"start": "2020-01-01"}})
            with pytest.raises(ValueError, match="Unknown"):
                await client.edit_outputs(RECORD["execution_id"], request)
            with pytest.raises(ValueError):
                await client.execution_outputs(RECORD["execution_id"], revision=0)
            with pytest.raises(ValueError):
                await client.output_revisions(RECORD["execution_id"], page_size=201)
    asyncio.run(scenario())
