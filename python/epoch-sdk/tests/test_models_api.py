"""Platform model client wire checks; these do not claim live lifecycle acceptance."""

import asyncio
import json
from pathlib import Path

import httpx
import pytest
from pydantic import ValidationError

from epoch_sdk.models_api import AsyncEpochModels, EpochModels
from epoch_sdk.models_api.errors import ServiceUnavailableError
from epoch_sdk.models_api.types import SaveModelRequest

FIXTURES = Path(__file__).resolve().parents[3] / "contracts/fixtures/platform-models"
SAVE = json.loads((FIXTURES / "save.json").read_text())
SUMMARY = json.loads((FIXTURES / "summary.json").read_text())
FACTS = json.loads((FIXTURES / "facts.json").read_text())


def test_model_save_list_and_read_route_to_platform_without_native_execution_calls():
    seen = []

    def handler(request):
        seen.append(request)
        assert request.headers["authorization"] == "Bearer fixture-token"
        if request.method == "POST":
            assert request.url.path == "/api/v1/models"
            assert json.loads(request.content) == SAVE
            return httpx.Response(200, json=SUMMARY)
        if request.url.path == "/api/v1/models":
            assert request.url.params["limit"] == "1"
            assert request.url.params["cursor"] == "owner-bound-cursor"
            return httpx.Response(200, json={"items": [SUMMARY], "next_cursor": "next"})
        assert request.url.path == "/api/v1/models/" + SUMMARY["model_ref"]
        return httpx.Response(200, json=FACTS)

    async def scenario():
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
            client = AsyncEpochModels(base_url="https://platform.test", token="fixture-token", httpx_client=http)
            saved = await client.save_model(**SAVE)
            page = await client.list_models(limit=1, cursor="owner-bound-cursor")
            facts = await client.read_model(saved.model_ref)
            assert page.items[0].digest == saved.digest
            assert page.next_cursor == "next"
            assert facts.model.manifest_sha256 == saved.manifest_sha256
            assert facts.binding == FACTS["binding"]
            assert facts.producer == FACTS["producer"]

    asyncio.run(scenario())
    assert len(seen) == 3


@pytest.mark.parametrize("change", [
    {"expected_digest": "latest"}, {"name": None}, {"unexpected": True},
])
def test_source_owned_model_save_requests_reject_invalid_or_extra_inputs(change):
    with pytest.raises(ValidationError):
        SaveModelRequest.model_validate({**SAVE, **change})


@pytest.mark.parametrize("change", [{"expected_digest": "latest"}, {"name": ""}, {"name": None}])
@pytest.mark.parametrize("asynchronous", [False, True])
def test_actual_model_client_rejects_invalid_requests_before_http(change, asynchronous):
    def forbidden(request):
        pytest.fail("An invalid Save must not reach HTTP")
    async def scenario():
        async with httpx.AsyncClient(transport=httpx.MockTransport(forbidden)) as http:
            client = AsyncEpochModels(base_url="https://platform.test", token="fixture-token", httpx_client=http)
            with pytest.raises(ValidationError):
                await client.save_model(**{**SAVE, **change})
    if asynchronous:
        asyncio.run(scenario())
    else:
        with httpx.Client(transport=httpx.MockTransport(forbidden)) as http:
            client = EpochModels(base_url="https://platform.test", token="fixture-token", httpx_client=http)
            with pytest.raises(ValidationError):
                client.save_model(**{**SAVE, **change})


def test_model_storage_unavailability_preserves_the_typed_error():
    async def scenario():
        transport = httpx.MockTransport(lambda request: httpx.Response(503, json={
            "error": "ServiceUnavailable", "message": "Pinned model object is unavailable",
            "timestamp": "2026-11-25T00:00:00Z",
        }))
        async with httpx.AsyncClient(transport=transport) as http:
            client = AsyncEpochModels(base_url="https://platform.test", token="fixture-token", httpx_client=http)
            with pytest.raises(ServiceUnavailableError) as failure:
                await client.read_model(SUMMARY["model_ref"], request_options={"max_retries": 0})
            assert failure.value.body.message == "Pinned model object is unavailable"
    asyncio.run(scenario())


def test_explicit_server_save_keeps_source_selection_closed_and_completion_is_retired():
    seen = []
    def handler(request):
        seen.append(request)
        body = json.loads(request.content)
        assert body['source_location'] == 'server'
        assert request.url.path == '/api/v1/models'
        assert body == {**SAVE, 'source_location': 'server'}
        return httpx.Response(200, json=SUMMARY)
    with httpx.Client(transport=httpx.MockTransport(handler)) as http:
        client = EpochModels(base_url='https://platform.test', token='fixture-token', httpx_client=http)
        assert client.save_model(**{**SAVE, 'source_location': 'server'}).digest == SUMMARY['digest']
        assert not hasattr(client, 'complete_model_saves')
        assert not hasattr(AsyncEpochModels, 'complete_model_saves')
        for kind in ('latest', 'fallback'):
            with pytest.raises(ValidationError):
                client.save_model(**{**SAVE, 'source_location': kind})
            with pytest.raises(ValidationError):
                SaveModelRequest.model_validate({**SAVE, 'source_location': kind})
    assert len(seen) == 1
