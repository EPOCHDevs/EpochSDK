"""Source-contract and mock HTTP checks; these do not claim live service acceptance."""

from __future__ import annotations

import asyncio
import copy
import json
from pathlib import Path

import httpx
import pytest

from epoch_sdk.platform_file_models import FileEditRequest
from epoch_sdk.platform_files import PlatformFileError, PlatformFilesClient
from epoch_sdk.research import EpochClient
from epoch_sdk.supervisor import SupervisorClient

FIXTURES = Path(__file__).resolve().parents[3] / "contracts/fixtures/platform-files"
VERSION = json.loads((FIXTURES / "version.json").read_text())
SAVE = json.loads((FIXTURES / "save.json").read_text())
GRID = json.loads((FIXTURES / "grid.json").read_text())
ORIGINAL, PIN = VERSION["original_file_ref"], VERSION["file"]["file_ref"]


def test_save_uses_exact_numeric_text_and_retry_body_with_refreshed_auth():
    async def scenario():
        calls = []
        tokens = iter(["first", "second"])

        def transport(request):
            calls.append(request)
            assert request.method == "POST"
            assert request.url.path == f"/api/v1/files/{ORIGINAL}/versions"
            if len(calls) == 1:
                return httpx.Response(
                    503,
                    json={"error": "FILE_EDIT_BUSY", "message": "Busy"},
                    headers={"Retry-After": "2"},
                )
            return httpx.Response(200, json=VERSION)

        async with httpx.AsyncClient(transport=httpx.MockTransport(transport)) as http:
            client = PlatformFilesClient("https://api.test", token=lambda: next(tokens), http=http)
            with pytest.raises(PlatformFileError) as error:
                await client.save(ORIGINAL, SAVE)
            assert error.value.code == "FILE_EDIT_BUSY" and error.value.retry_after == "2"
            assert len(calls) == 1  # No mutation retry.
            result = await client.save(ORIGINAL, SAVE)
            assert result.file.file_ref == PIN
            assert calls[0].content == calls[1].content
            assert (
                json.loads(calls[1].content)["edit"]["changes"][0]["value"]["value"]
                == "9007199254740993"
            )
            assert [r.headers["Authorization"] for r in calls] == ["Bearer first", "Bearer second"]

    asyncio.run(scenario())


def test_grid_preserves_tagged_values_and_stream_range_metadata():
    async def scenario():
        def transport(request):
            if request.url.path.endswith("/content"):
                assert request.headers["Range"] == "bytes=2-5"
                assert request.headers["If-Range"] == '"hash"'
                return httpx.Response(
                    206,
                    content=b"2345",
                    headers={"Content-Range": "bytes 2-5/10", "ETag": '"hash"'},
                )
            return httpx.Response(200, json=GRID)

        async with httpx.AsyncClient(transport=httpx.MockTransport(transport)) as http:
            client = PlatformFilesClient("https://api.test", token="fixture", http=http)
            grid = await client.grid(
                PIN, {"schema_version": 1, "format": "parquet", "offset": 201, "limit": 1}
            )
            assert grid.rows[0][0].value.value == "9007199254740993"
            async with client.content(PIN, byte_range="bytes=2-5", if_range='"hash"') as content:
                assert content.status == 206 and content.headers["content-range"] == "bytes 2-5/10"
                assert b"".join([chunk async for chunk in content.body]) == b"2345"

    asyncio.run(scenario())


@pytest.mark.parametrize(
    "change",
    [
        lambda b: b.update(base_version=True),
        lambda b: b.update(request_id="é" * 65),
        lambda b: b["edit"]["changes"][0]["value"].update(value=9007199254740993),
        lambda b: b["edit"]["changes"][0]["value"].update(value="NaN"),
        lambda b: b["edit"].update(unexpected="field"),
    ],
)
def test_invalid_wire_is_rejected_before_auth_or_transport(change):
    async def scenario():
        body = copy.deepcopy(SAVE)
        change(body)

        def forbidden(*args):
            raise AssertionError("Invalid input must not reach token or HTTP")

        async with httpx.AsyncClient(transport=httpx.MockTransport(forbidden)) as http:
            client = PlatformFilesClient("https://api.test", token=forbidden, http=http)
            with pytest.raises(ValueError):
                await client.save(ORIGINAL, body)

    asyncio.run(scenario())


@pytest.mark.parametrize(
    "body",
    [
        {**VERSION, "original_file_ref": "file:" + "c" * 64},
        {**VERSION, "version": 2},
        {**VERSION, "unexpected": "private-field"},
        {**VERSION, "file": {**VERSION["file"], "content_sha256": "c" * 64}},
    ],
)
def test_response_identity_and_closed_schema_are_checked(body):
    async def scenario():
        async with httpx.AsyncClient(
            transport=httpx.MockTransport(lambda _: httpx.Response(200, json=body))
        ) as http:
            client = PlatformFilesClient("https://api.test", token="fixture", http=http)
            with pytest.raises(ValueError):
                await client.save(ORIGINAL, SAVE)

    asyncio.run(scenario())


def test_connected_client_exposes_platform_operations_with_origin_scoped_auth():
    async def scenario():
        calls = []

        async def token():
            return "fresh"

        def transport(request):
            calls.append(request)
            assert request.headers["Authorization"] == "Bearer fresh"
            return httpx.Response(200, json=VERSION)

        supervisor = SupervisorClient._connect(
            graph_url="https://graph.test",
            backend_url="https://api.test",
            token=token,
            transport=httpx.MockTransport(transport),
        )
        try:
            sdk = EpochClient(supervisor)
            assert (await sdk.file_edits.latest(ORIGINAL)).file.file_ref == PIN
            assert len(calls) == 1
        finally:
            await supervisor.aclose()

    asyncio.run(scenario())


def test_redirects_are_not_followed_and_model_requests_are_validated():
    async def scenario():
        model = FileEditRequest.model_validate(SAVE)
        calls = []

        def transport(request):
            calls.append(request)
            return httpx.Response(307, headers={"Location": "https://other.test/steal"})

        async with httpx.AsyncClient(transport=httpx.MockTransport(transport)) as http:
            client = PlatformFilesClient("https://api.test", token="fixture", http=http)
            with pytest.raises(PlatformFileError) as error:
                await client.save(ORIGINAL, model)
            assert error.value.status == 307 and len(calls) == 1

    asyncio.run(scenario())


def test_image_pages_are_validated_and_do_not_change_the_pdf_preview_contract():
    async def scenario():
        ready = {
            "state": "ready",
            "media_type": "image/png",
            "converter_version": "raster-png-v1",
            "size_bytes": 8,
            "pages": [
                {"page": n, "width": 2, "height": 2, "size_bytes": 4, "content_sha256": "b" * 64}
                for n in (1, 2)
            ],
        }

        def transport(request):
            if request.url.path.endswith("/content"):
                assert request.url.path.endswith("/image-preview/2/content")
                return httpx.Response(200, content=b"page")
            return httpx.Response(
                200,
                json=ready if request.url.path.endswith("/image-preview") else {"state": "none"},
            )

        async with httpx.AsyncClient(transport=httpx.MockTransport(transport)) as http:
            client = PlatformFilesClient("https://api.test", token="fixture", http=http)
            assert len((await client.image_preview(ORIGINAL)).pages) == 2
            assert (await client.preview(ORIGINAL)).state == "none"
            async with client.content(ORIGINAL, image_page=2) as result:
                assert b"".join([chunk async for chunk in result.body]) == b"page"
            with pytest.raises(ValueError):
                async with client.content(ORIGINAL, image_page=0):
                    pass
            with pytest.raises(ValueError):
                async with client.content(ORIGINAL, image_page=1, preview=True):
                    pass

    asyncio.run(scenario())
