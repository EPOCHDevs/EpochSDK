"""Installed native clients, captured HTTP, explicit decisions and graph delivery.

The fixtures are exported by the Backend's native storage tests. These checks do
not invoke an extraction provider or claim to reproduce its output.
"""

from __future__ import annotations

import asyncio
import json
from contextlib import asynccontextmanager
from copy import deepcopy
from pathlib import Path

import httpx
import pytest
from langgraph_sdk.client import LangGraphClient
from pydantic import ValidationError
from stratifyx import AsyncStratifyX
from stratifyx.types import DatasetBuild

from epoch_sdk.dataset_reviews import (
    DatasetConfigureInterrupt,
    DatasetConfigureResponse,
    DatasetResultInterrupt,
    DatasetResultResponse,
    dataset_response,
)
from epoch_sdk.supervisor import GraphInterrupt, NeedsInput, SupervisorClient, WorkflowHandle

ROOT = Path(__file__).parent / "fixtures/document-review"
BUILD = json.loads((ROOT / "build-review.json").read_text())
PREVIEW = json.loads((ROOT / "preview.json").read_text())
HANDLE = WorkflowHandle(thread_id="thread-one", request_id="request-one", assistant_id="epoch-ai")


def waiting(build=None):
    payload = DatasetResultInterrupt(
        tool_call_id="prepare-one",
        operation=DatasetBuild.model_validate(build or BUILD),
        can_edit=True,
    )
    return NeedsInput(
        handle=HANDLE,
        interrupts=[
            GraphInterrupt(
                id="review-one",
                value=payload.model_dump(mode="json", by_alias=True, exclude_none=True),
            )
        ],
    )


@asynccontextmanager
async def harness(build=None):
    state = {
        "build": deepcopy(build or BUILD),
        "interrupts": [item.model_dump(mode="json") for item in waiting(build).interrupts],
        "save_status": "saved",
        "lost": False,
    }
    calls = []

    def native(request):
        calls.append(
            (
                "native",
                request.method,
                request.url.path,
                json.loads(request.content) if request.content else None,
            )
        )
        if state.get("deny_reads"):
            return httpx.Response(
                404,
                json={
                    "error": "DataNotFound",
                    "message": "Unavailable",
                    "timestamp": "2026-11-02T00:00:00Z",
                },
            )
        if request.url.path.endswith("/preview"):
            return httpx.Response(200, json=state.get("preview", PREVIEW))
        if request.url.path.endswith("/content"):
            return httpx.Response(
                200, content=state["content"], headers={"content-type": "application/json"}
            )
        if request.method == "POST":
            decision = json.loads(request.content)
            expected = {
                "attempt": state["build"]["attempt"],
                "review_ref": state["build"]["review"]["review_ref"],
                "schema_sha256": state["build"]["review"]["schema_sha256"],
                "result_sha256": state["build"]["result_sha256"],
            }
            assert {key: decision[key] for key in expected} == expected
            state["build"]["state"] = (
                "discarded" if decision["action"] == "discard" else state["save_status"]
            )
            if state["build"]["state"] == "saved":
                draft = state["build"]["review"]["draft"]
                state["build"]["dataset"] = {
                    "dataset_ref": "dataset:" + "e" * 64,
                    "name": draft["name"],
                    "descriptor": draft["descriptor"],
                    "saved_at": "2026-11-02T00:00:00Z",
                    "archived": False,
                }
            if state["lost"]:
                raise httpx.ReadError("Lost native acknowledgement")
        return httpx.Response(200, json=state["build"])

    def graph(request):
        calls.append(
            (
                "graph",
                request.method,
                request.url.path,
                json.loads(request.content) if request.content else None,
            )
        )
        if request.method == "POST":
            body = json.loads(request.content)
            assert body["command"]["resume"]["review-one"]["type"] == "dataset_review"
            state["interrupts"] = []
            return httpx.Response(
                200, json={"messages": [{"type": "ai", "content": "Outcome received"}]}
            )
        if request.url.path.endswith("/state"):
            return httpx.Response(
                200, json={"values": {}, "next": [], "interrupts": state["interrupts"]}
            )
        return httpx.Response(200, json={"thread_id": "thread-one", "status": "idle"})

    async with (
        httpx.AsyncClient(transport=httpx.MockTransport(native)) as native_http,
        httpx.AsyncClient(
            base_url="https://graph.test", transport=httpx.MockTransport(graph)
        ) as graph_http,
    ):
        client = SupervisorClient(
            LangGraphClient(graph_http),
            AsyncStratifyX(
                base_url="https://native.test", token="fixture", httpx_client=native_http
            ),
        )
        yield client, state, calls


def test_exact_response_union_rejects_missing_fields_extra_authority_and_implicit_actions():
    payload = waiting().interrupts[0].dataset_review()
    response = dataset_response(payload, "save")
    wire = response.model_dump(mode="json", exclude_none=True)
    for key in ("review_ref", "schema_sha256", "result_sha256", "attempt"):
        with pytest.raises(ValidationError):
            DatasetResultResponse.model_validate(
                {name: value for name, value in wire.items() if name != key}
            )
    for change in (
        {"action": "auto"},
        {"owner": "bob"},
        {"action": "edit"},
        {"request": BUILD["request"]},
    ):
        with pytest.raises(ValidationError):
            DatasetResultResponse.model_validate(wire | change)
    with pytest.raises(ValueError, match="exact displayed"):
        SupervisorClient.resume_command(
            waiting(), {"review-one": response.model_copy(update={"schema_sha256": "f" * 64})}
        )


def test_configuration_is_a_closed_explicit_choice_not_an_automatic_build():
    payload = DatasetConfigureInterrupt(
        tool_call_id="prepare-one",
        proposal_ref="proposal:" + "a" * 64,
        preparation_ref=BUILD["preparation_ref"],
        request=DatasetBuild.model_validate(BUILD).request,
    )
    with pytest.raises(ValidationError):
        DatasetConfigureResponse(proposal_ref=payload.proposal_ref, action="build_preview")
    with pytest.raises(ValidationError):
        DatasetConfigureResponse(
            proposal_ref=payload.proposal_ref, action="cancel", request=payload.request
        )
    assert dataset_response(payload, "cancel").request is None


@pytest.mark.parametrize("action,terminal", [("save", "saved"), ("decline", "discarded")])
def test_native_decision_is_confirmed_before_same_graph_resume(action, terminal):
    async def scenario():
        async with harness() as (client, state, calls):
            pending = waiting()
            result = await client.resume(
                pending,
                {"review-one": dataset_response(pending.interrupts[0].dataset_review(), action)},
            )
            assert result.reply == "Outcome received" and state["build"]["state"] == terminal
            writes = [call for call in calls if call[1] == "POST"]
            assert [call[0] for call in writes] == ["native", "graph"]
            assert all(
                "preparations" not in call[2] or call[1] == "GET" or call[2].endswith("/actions")
                for call in calls
            )

    asyncio.run(scenario())


def test_unknown_save_never_resumes_the_agent_or_allows_decline():
    async def scenario():
        async with harness() as (client, state, calls):
            state["save_status"] = "saving"
            pending = waiting()
            response = dataset_response(pending.interrupts[0].dataset_review(), "save")
            with pytest.raises(ValueError, match="not confirmed"):
                await client.resume(pending, {"review-one": response})
            assert not any(call[0] == "graph" and call[1] == "POST" for call in calls)
            with pytest.raises(ValueError, match="not yet confirmed"):
                await client.resume(pending, {"review-one": response})
            assert len([call for call in calls if call[0] == "native" and call[1] == "POST"]) == 1

    asyncio.run(scenario())


def test_saved_native_outcome_can_deliver_after_a_lost_ack_without_repeating_save():
    async def scenario():
        async with harness() as (client, state, calls):
            state["lost"] = True
            pending = waiting()
            response = dataset_response(pending.interrupts[0].dataset_review(), "save")
            with pytest.raises(httpx.ReadError):
                await client.resume(pending, {"review-one": response})
            assert state["build"]["state"] == "saved"
            assert not any(call[0] == "graph" and call[1] == "POST" for call in calls)
            state["lost"] = False
            await client.resume(pending, {"review-one": response})
            assert len([call for call in calls if call[0] == "native" and call[1] == "POST"]) == 1
            assert len([call for call in calls if call[0] == "graph" and call[1] == "POST"]) == 1

    asyncio.run(scenario())


def test_reopening_always_observes_native_expiry_and_can_continue_without_save():
    async def scenario():
        async with harness() as (client, state, calls):
            state["build"]["state"] = "expired"
            state["build"]["review"]["allowed_actions"] = []
            fresh = await client.status(HANDLE)
            assert isinstance(fresh, NeedsInput)
            payload = fresh.interrupts[0].dataset_review()
            assert payload.operation.state.value == "expired" and payload.can_edit is False
            await client.resume(fresh, {"review-one": dataset_response(payload, "continue")})
            assert not any(call[0] == "native" and call[1] == "POST" for call in calls)

    asyncio.run(scenario())


def test_default_same_agent_mcp_reads_full_unsaved_draft_without_adding_a_tool():
    from hashlib import sha256

    from mcp import Client

    from epoch_sdk.workflow_mcp import create_server

    async def scenario():
        async with harness() as (client, state, calls), Client(create_server(client)) as caller:
            tools = {tool.name for tool in (await caller.list_tools()).tools}
            assert tools == {
                "epoch_run",
                "epoch_execute",
                "epoch_resume",
                "epoch_status",
                "epoch_read",
            }
            raw = b'{ "revenue": 9007199254740993.1200 }'
            state["content"] = raw
            state["preview"] = deepcopy(PREVIEW)
            state["preview"]["content"].update(json_text="", requires_download=True)
            first = await caller.call_tool("epoch_read", {"draft_ref": BUILD["draft_ref"]})
            assert (
                not first.is_error
                and first.structured_content["content"]["requires_download"] is True
            )
            linked = await caller.call_tool(
                "epoch_read",
                {
                    "draft_ref": BUILD["draft_ref"],
                    "full_content": True,
                    "expected_sha256": sha256(raw).hexdigest(),
                },
            )
            assert not linked.is_error
            resource = linked.content[0]
            content = await caller.read_resource(str(resource.uri))
            assert content.contents[0].text.encode() == raw
            assert state["build"]["state"] == "pending_review"
            assert all(call[0] == "native" and call[1] == "GET" for call in calls)

    asyncio.run(scenario())


def test_default_mcp_draft_resource_rechecks_content_digest_on_every_read():
    from hashlib import sha256

    from mcp import Client

    from epoch_sdk.workflow_mcp import create_server

    async def scenario():
        async with harness() as (client, state, calls), Client(create_server(client)) as caller:
            state["content"] = b"false"
            digest = sha256(b"true").hexdigest()
            linked = await caller.call_tool(
                "epoch_read",
                {"draft_ref": BUILD["draft_ref"], "full_content": True, "expected_sha256": digest},
            )
            assert not linked.is_error
            with pytest.raises(Exception, match="authorized or verified"):
                await caller.read_resource(str(linked.content[0].uri))
            assert all(call[1] == "GET" for call in calls)

    asyncio.run(scenario())


def test_default_mcp_resource_link_never_grants_access_after_native_owner_denial():
    from hashlib import sha256

    from mcp import Client

    from epoch_sdk.workflow_mcp import create_server

    async def scenario():
        async with harness() as (client, state, calls), Client(create_server(client)) as caller:
            state["content"] = b"false"
            linked = await caller.call_tool(
                "epoch_read",
                {
                    "draft_ref": BUILD["draft_ref"],
                    "full_content": True,
                    "expected_sha256": sha256(b"false").hexdigest(),
                },
            )
            state["deny_reads"] = True
            before = len(calls)
            with pytest.raises(Exception, match="authorized or verified"):
                await caller.read_resource(str(linked.content[0].uri))
            assert len(calls) == before + 1
            assert calls[-1][1] == "GET" and calls[-1][2].endswith("/preview")

    asyncio.run(scenario())
