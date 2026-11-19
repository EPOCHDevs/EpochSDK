"""Source-contract and mock HTTP checks; these do not claim live service acceptance."""

from __future__ import annotations

import asyncio
import copy
import hashlib
import json
from pathlib import Path

import httpx
import pytest

from epoch_sdk._storage import StorageTransferError
from epoch_sdk.platform_file_models import FileEditRequest
from epoch_sdk.platform_files import PlatformFileError, PlatformFilesClient
from epoch_sdk.research import EpochClient
from epoch_sdk.supervisor import SupervisorClient

FIXTURES = Path(__file__).resolve().parents[3] / "contracts/fixtures/platform-files"
VERSION = json.loads((FIXTURES / "version.json").read_text())
SAVE = json.loads((FIXTURES / "save.json").read_text())
GRID = json.loads((FIXTURES / "grid.json").read_text())
ORIGINAL, PIN = VERSION["original_file_ref"], VERSION["file"]["file_ref"]


def inline(transport):
    """A Platform without signed storage links: the edit stays in the save request."""

    def handler(request):
        if request.url.path.endswith("/edit-uploads"):
            return httpx.Response(
                409, json={"error": "FILE_DIRECT_TRANSFER_UNAVAILABLE", "message": "Inline here"}
            )
        return transport(request)

    return handler


def test_save_uses_exact_numeric_text_and_retry_body_with_refreshed_auth():
    async def scenario():
        calls = []
        tokens = iter(["first", "first", "second", "second"])  # Link request, then save.

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

        async with httpx.AsyncClient(transport=httpx.MockTransport(inline(transport))) as http:
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
            transport=httpx.MockTransport(inline(lambda _: httpx.Response(200, json=body)))
        ) as http:
            client = PlatformFilesClient("https://api.test", token="fixture", http=http)
            with pytest.raises(ValueError):
                await client.save(ORIGINAL, SAVE)

    asyncio.run(scenario())


class StagingPlatform:
    """Platform with signed storage links, and the storage they point to."""

    def __init__(self, refusals: int = 0):
        self.calls: list[httpx.Request] = []
        self.puts: list[httpx.Request] = []
        self.links = 0
        self.refusals = refusals

    def api(self, request):
        self.calls.append(request)
        body = json.loads(request.content)
        if request.url.path == f"/api/v1/files/{ORIGINAL}/edit-uploads":
            self.links += 1
            self.request = body
            return httpx.Response(200, json={
                "url": f"https://storage.test/staged?X-Amz-Signature=secret{self.links}", "method": "PUT",
                "headers": {"content-type": "application/json", "x-amz-checksum-sha256": "checksum"},
                "size_bytes": body["size_bytes"], "expires_at": "2026-11-19T12:15:00.000Z",
            })
        assert request.url.path == f"/api/v1/files/{ORIGINAL}/versions"
        self.saved = body
        return httpx.Response(200, json=VERSION)

    def storage(self, request):
        self.puts.append(request)
        assert "authorization" not in request.headers  # API credentials never reach storage.
        assert request.headers["content-type"] == "application/json"
        assert request.headers["x-amz-checksum-sha256"] == "checksum"
        if len(self.puts) <= self.refusals:
            return httpx.Response(403, text="<Error><Code>AccessDenied</Code></Error>")
        return httpx.Response(200)


def staged_client(monkeypatch, platform: StagingPlatform):
    monkeypatch.setattr(
        "epoch_sdk.platform_files.storage_client",
        lambda: httpx.AsyncClient(transport=httpx.MockTransport(platform.storage)),
    )
    return httpx.AsyncClient(transport=httpx.MockTransport(platform.api))


def test_save_puts_the_edit_through_a_signed_link_and_names_it(monkeypatch):
    async def scenario():
        platform = StagingPlatform()
        async with staged_client(monkeypatch, platform) as http:
            client = PlatformFilesClient("https://api.test", token="fixture", http=http)
            result = await client.save(ORIGINAL, SAVE)
        assert result.file.file_ref == PIN
        staged = platform.puts[0].content
        assert json.loads(staged) == SAVE["edit"]
        upload = {"size_bytes": len(staged), "content_sha256": hashlib.sha256(staged).hexdigest()}
        assert platform.request == {"request_id": SAVE["request_id"], **upload}
        # The save carries only metadata: no file text passes through the API.
        assert platform.saved == {**{k: v for k, v in SAVE.items() if k != "edit"}, "edit_upload": upload}
        assert [r.headers["Authorization"] for r in platform.calls] == ["Bearer fixture"] * 2

    asyncio.run(scenario())


def test_a_refused_put_asks_for_one_new_link_then_fails_without_the_link(monkeypatch):
    async def scenario():
        async with staged_client(monkeypatch, platform := StagingPlatform(refusals=1)) as http:
            client = PlatformFilesClient("https://api.test", token="fixture", http=http)
            await client.save(ORIGINAL, SAVE)
        assert platform.links == 2 and len(platform.puts) == 2
        assert platform.puts[1].url.params["X-Amz-Signature"] == "secret2"

        async with staged_client(monkeypatch, platform := StagingPlatform(refusals=2)) as http:
            client = PlatformFilesClient("https://api.test", token="fixture", http=http)
            with pytest.raises(StorageTransferError) as error:
                await client.save(ORIGINAL, SAVE)
        assert error.value.status == 403 and "secret" not in str(error.value)
        assert platform.links == 2 and not hasattr(platform, "saved")

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


def test_native_document_contract_keeps_positions_headings_and_identity():
    read = json.loads((FIXTURES / "document_read.json").read_text())
    page = json.loads((FIXTURES / "document_page.json").read_text())
    passage = json.loads((FIXTURES / "document_passage.json").read_text())
    original = (FIXTURES / "document-original.txt").read_bytes()

    async def scenario():
        calls = []

        def transport(request):
            calls.append(request)
            if request.url.path.endswith("/reads"):
                assert json.loads(request.content) == {"file_ref": read["source"]["file_ref"]}
                body = read
            elif "/reads/" in request.url.path:
                body = read
            elif request.url.path.endswith("/blocks"):
                assert request.url.params["max_bytes"] == "32768"
                body = page
            else:
                body = passage
            return httpx.Response(200, json=body)

        async with httpx.AsyncClient(transport=httpx.MockTransport(transport)) as http:
            client = PlatformFilesClient("https://api.test", token="fixture", http=http)
            result = await client.begin_document_read(read["source"]["file_ref"])
            assert result.outline and result.outline[0].text == "Résumé"
            assert (await client.document_read(read["read_ref"])).read_ref == read["read_ref"]
            content = await client.document_content(page["document_version_ref"])
            block = (
                await client.document_passage(
                    page["document_version_ref"], content.blocks[0].block_ref
                )
            ).block
            assert block.start_byte is not None and block.length is not None
            assert (
                original[block.start_byte : block.start_byte + block.length].decode() == block.text
            )
            assert len(calls) == 4

    asyncio.run(scenario())


def test_document_positions_and_page_identity_cannot_be_fabricated():
    page = json.loads((FIXTURES / "document_page.json").read_text())

    async def scenario():
        for change in [
            lambda p: p.update(offset=1),
            lambda p: p["blocks"][0].update(length=1),
            lambda p: p["blocks"][0].pop("length"),
        ]:
            invalid = copy.deepcopy(page)
            change(invalid)
            async with httpx.AsyncClient(
                transport=httpx.MockTransport(
                    lambda _, value=invalid: httpx.Response(200, json=value)
                )
            ) as http:
                client = PlatformFilesClient("https://api.test", token="fixture", http=http)
                with pytest.raises(ValueError, match="inconsistent"):
                    await client.document_content(page["document_version_ref"])

    asyncio.run(scenario())


def test_invalid_document_references_and_bounds_fail_before_authentication():
    async def scenario():
        def forbidden():
            pytest.fail("Authentication must not run for an invalid request")

        client = PlatformFilesClient("https://api.test", token=forbidden)
        try:
            for ref in ["document:invalid", "document:" + "b" * 64 + "\n"]:
                with pytest.raises(ValueError):
                    await client.document_content(ref)
            with pytest.raises(ValueError):
                await client.document_content("document:" + "b" * 64, offset=True)
            with pytest.raises(ValueError):
                await client.document_passage("document:" + "b" * 64, "block:" + "c" * 64 + "\n")
        finally:
            await client.aclose()

    asyncio.run(scenario())
