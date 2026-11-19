"""Platform sharing transport/model checks; these do not exercise native computation."""

from __future__ import annotations

import asyncio
import json
from pathlib import Path

import httpx
import pytest

from epoch_sdk.shares_api import AsyncEpochShares
from epoch_sdk.shares_api.errors import ConflictError
from epoch_sdk.shares_api.types import (
    ChangeShareAccessRequest,
    SelectShareVersionRequest,
    ShareVersionsResponse,
)


def fixture(name):
    return json.loads(
        (
            Path(__file__).resolve().parents[3] / f"contracts/fixtures/platform-shares/{name}.json"
        ).read_text()
    )


def client(handler):
    return AsyncEpochShares(
        base_url="https://platform.test",
        token="fixture-token",
        httpx_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
    )


def test_changes_access_without_replacing_the_url_and_keeps_access_zero():
    seen = []

    def handler(request):
        seen.append(request)
        return httpx.Response(
            200, json={**fixture("summary"), "access_version": 1, "added_later": True}
        )

    async def scenario():
        share = await client(handler).studies_shares.change_who_can_open_a_share_link(
            "share 1",
            expected_access_version=0,
            audience="named_subjects",
            subjects=["reader@example.test"],
        )
        assert share.access_version == 1 and share.model_extra == {"added_later": True}

    asyncio.run(scenario())
    assert seen[0].url.raw_path == b"/api/v1/studies/shares/share%201"
    assert seen[0].method == "PATCH" and json.loads(seen[0].content) == fixture("access")
    assert seen[0].headers["authorization"] == "Bearer fixture-token"


def test_lists_published_versions_including_an_unavailable_legacy_version():
    seen = []

    def handler(request):
        seen.append(request)
        return httpx.Response(200, json=fixture("versions"))

    async def scenario():
        page = await client(handler).studies_shares.list_published_share_versions("share 1")
        assert isinstance(page, ShareVersionsResponse)
        available, unavailable = page.versions
        assert (
            available.available is True
            and available.message_count == 9
            and available.run_count == 2
        )
        assert unavailable.available is False and unavailable.reason == "legacy_missing"

    asyncio.run(scenario())
    assert seen[0].url.raw_path == b"/api/v1/studies/shares/share%201/versions"
    malformed = fixture("versions")
    malformed["versions"][0]["available"] = False
    with pytest.raises(ValueError):
        ShareVersionsResponse.model_validate(malformed)


def test_selects_an_older_version_with_compare_and_set():
    seen = []

    def handler(request):
        seen.append(request)
        return httpx.Response(200, json={**fixture("summary"), "snapshot_version": 1})

    async def scenario():
        share = await client(handler).studies_shares.select_published_share_version(
            "share 1", snapshot_version=1, expected_current_version=3
        )
        assert share.snapshot_version == 1

    asyncio.run(scenario())
    assert seen[0].url.raw_path == b"/api/v1/studies/shares/share%201/current-version"
    assert seen[0].method == "PUT" and json.loads(seen[0].content) == fixture("selection")


def test_received_shares_use_the_static_endpoint_and_only_the_five_metadata_fields():
    seen = []

    def handler(request):
        seen.append(request)
        return httpx.Response(200, json=fixture("received"))

    async def scenario():
        page = await client(handler).studies_shares.list_received_thread_shares()
        item = page.shares[0].model_dump()
        assert set(item) == {
            "share_id",
            "thread_title",
            "owner_display_name",
            "snapshot_version",
            "frozen_at_ms",
        }
        assert item["thread_title"] == "Synthetic conversation"

    asyncio.run(scenario())
    assert seen[0].url.path == "/api/v1/studies/shares/received"


@pytest.mark.parametrize("operation", ["access", "selection"])
def test_conflicts_keep_the_typed_409_body_without_repeating_the_mutation(operation):
    seen = []

    def handler(request):
        seen.append(request)
        return httpx.Response(
            409,
            json={
                "error": "Conflict",
                "message": "Changed in another window.",
                "timestamp": "2026-11-19T00:00:00Z",
            },
        )

    async def scenario():
        shares = client(handler).studies_shares
        with pytest.raises(ConflictError) as problem:
            if operation == "access":
                await shares.change_who_can_open_a_share_link(
                    "share-1",
                    expected_access_version=0,
                    audience="named_subjects",
                    subjects=["reader@example.test"],
                    request_options={"max_retries": 0},
                )
            else:
                await shares.select_published_share_version(
                    "share-1",
                    snapshot_version=1,
                    expected_current_version=3,
                    request_options={"max_retries": 0},
                )
        assert (
            problem.value.status_code == 409
            and problem.value.body.message == "Changed in another window."
        )

    asyncio.run(scenario())
    assert len(seen) == 1


def test_restored_request_models_keep_requiredness_closure_and_strict_integers():
    for model in (ChangeShareAccessRequest, SelectShareVersionRequest):
        assert model.model_config["extra"] == "forbid"
    assert ChangeShareAccessRequest(expected_access_version=0).expected_access_version == 0
    for value in [
        {},
        {"expected_access_version": -1},
        {"expected_access_version": True},
        {"expected_access_version": 0, "audience": "other"},
        {"expected_access_version": 0, "surprise": True},
    ]:
        with pytest.raises(ValueError):
            ChangeShareAccessRequest.model_validate(value)
    for value in [
        {"snapshot_version": 1},
        {"snapshot_version": 0, "expected_current_version": 2},
        {"snapshot_version": 1.5, "expected_current_version": 2},
    ]:
        with pytest.raises(ValueError):
            SelectShareVersionRequest.model_validate(value)
