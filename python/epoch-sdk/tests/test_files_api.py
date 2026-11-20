"""The Files and Space client generated from Platform's contract (ENG-2819).

Mock HTTP checks; they do not claim live service acceptance.
"""

from __future__ import annotations

import asyncio
import copy
import json
from pathlib import Path
import re

import httpx
import pytest

from epoch_sdk.files_api import AsyncEpochFiles
from epoch_sdk.files_api.errors import BadRequestError
from epoch_sdk.files_api.types import (
    DatasetReviewRequest,
    SavedDatasetListPage,
    SpacePlacementRequest,
    StructuredImportOptions,
    StructuredImportRequest,
    UserFileListPage,
    UserFileStatus,
)

SAVED = json.loads(
    (Path(__file__).resolve().parents[3] / "contracts/fixtures/platform-files/saved_dataset.json").read_text()
)


def client(handler) -> AsyncEpochFiles:
    return AsyncEpochFiles(
        base_url="https://platform.test",
        token="token",
        httpx_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
    )


def test_method_names_match_the_platform_files_contract():
    import epoch_sdk.files_api.user_files.client as generated

    contract = json.loads(
        (Path(__file__).resolve().parents[3] / "contracts/platform-files.openapi.json").read_text()
    )
    expected = {
        re.sub(r"(?<!^)(?=[A-Z])", "_", operation["operationId"]).lower()
        for path in contract["paths"].values()
        for verb, operation in path.items()
        if verb in {"get", "put", "post", "patch", "delete", "options", "head", "trace"}
        and "UserFiles" in operation.get("tags", [])
    }

    def methods(client_type) -> set[str]:
        return {
            name
            for name in dir(client_type)
            if not name.startswith("_") and name != "with_raw_response"
        }

    # Files belongs to Platform; the retired native client is no longer a dependency.
    assert expected and "archive_user_file" not in expected
    assert methods(generated.UserFilesClient) == expected
    assert methods(generated.AsyncUserFilesClient) == expected


def test_saved_datasets_list_and_keeps_fields_platform_adds_later():
    saved = copy.deepcopy(SAVED)
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={"items": [saved], "next_cursor": "next", "added_later": True})

    async def scenario():
        files_client = client(handler)
        page = await files_client.user_files.list_saved_datasets(limit=1)
        assert isinstance(page, SavedDatasetListPage)
        assert page.items[0].dataset_ref == saved["dataset_ref"]
        assert page.next_cursor == "next"
        # A field this client doesn't know yet is kept, not refused.
        assert page.model_extra == {"added_later": True}

    asyncio.run(scenario())
    assert seen[0].url.path == "/api/v1/files/datasets" and seen[0].url.params["limit"] == "1"
    assert seen[0].headers["authorization"] == "Bearer token"


def test_an_import_carries_the_persons_sort_choice():
    sent = []

    def handler(request: httpx.Request) -> httpx.Response:
        sent.append(json.loads(request.content))
        return httpx.Response(400, json={"error": "BadRequest", "message": "stop", "timestamp": "2026-11-19T00:00:00Z"})

    async def scenario():
        options = StructuredImportOptions(
            format="csv", delimiter=",", header=True, null_values=[""], columns=[], sort_by=["date"]
        )
        with pytest.raises(BadRequestError):
            await client(handler).user_files.prepare_structured_import(
                file_ref="file:" + "a" * 64, request_id="r", name="Prices", options=options,
                request_options={"max_retries": 0},
            )

    asyncio.run(scenario())
    assert sent[0]["options"]["sort_by"] == ["date"]


def test_a_status_platform_adds_later_parses_instead_of_failing_the_page():
    file = {
        "file_ref": "file:" + "a" * 64, "name": "prices.csv", "media_type": "text/csv", "size_bytes": 3,
        "created_at": "2026-11-19T00:00:00Z", "status": "quarantined",
    }

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"items": [file], "total_count": 1})

    async def scenario():
        page = await client(handler).user_files.list_user_files(request_options={"max_retries": 0})
        assert isinstance(page, UserFileListPage)
        status = page.items[0].status
        # Its own member: equal to the raw value and never a known one.
        assert status == "quarantined" and status not in list(UserFileStatus)

    asyncio.run(scenario())


def test_request_bodies_are_closed_models_with_their_source_requiredness():
    # Fern flattens these bodies into method arguments; they are restored as types, as in StratifyX.
    for model in (StructuredImportRequest, DatasetReviewRequest, SpacePlacementRequest):
        assert model.model_config["extra"] == "forbid"
    options = StructuredImportOptions(format="csv", delimiter=",", header=True, null_values=[""], columns=[])
    request = StructuredImportRequest(file_ref="file:" + "a" * 64, request_id="r", name="Prices", options=options)
    assert request.purpose is None
    with pytest.raises(ValueError):
        StructuredImportRequest(file_ref="f", request_id="r", name="n", options=options, sorted=True)
    with pytest.raises(ValueError):
        StructuredImportRequest(file_ref="f", name="n", options=options)
