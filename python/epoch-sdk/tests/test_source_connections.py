"""Source SDK/MCP transport and shared-contract checks; live Airbyte is separate."""
import asyncio
import json
from pathlib import Path

import httpx
import pytest
from epoch_sources.client import AsyncSourcesClient
from epoch_sources.models import CreateConnection, SourceAPIError, StartSync
from jsonschema import Draft202012Validator
from mcp import Client
from native_service_fixture import Service


REF = "connection:" + "a" * 64
CONNECTION = {
    "connection_ref": REF, "source_type": "postgres", "name": "Saved database",
    "state": "ready", "postgres": {"host": "database.internal", "port": 5432,
        "database": "research", "username": "reader", "schemas": ["public"], "ssl_mode": "require"},
    "selected_streams": [{"namespace": "public", "name": "prices"}],
    "created_at": "2026-10-28T00:00:00Z", "error": None, "latest_sync": None,
}


def test_sdk_transmits_write_only_credentials_once_and_validates_shared_contract():
    async def scenario():
        calls = []
        def backend(request):
            calls.append(request)
            assert request.headers["Authorization"] == "Bearer fixture"
            assert request.url.path == "/api/v1/sources/connections/postgres"
            assert json.loads(request.content)["postgres"]["password"] == "fixture-password"
            return httpx.Response(200, json=CONNECTION)
        async with httpx.AsyncClient(transport=httpx.MockTransport(backend)) as http:
            client = AsyncSourcesClient(base_url="https://epoch.invalid/", token="fixture", http=http)
            request = CreateConnection.model_validate({
                "request_id": "once", "name": CONNECTION["name"],
                "postgres": {**CONNECTION["postgres"], "password": "fixture-password"},
            })
            result = await client.create(request)
            assert "password" not in result.model_dump_json()
            assert result.connection_ref == REF and len(calls) == 1
            contract = json.loads((Path(__file__).resolve().parents[3] / "contracts/source-connections.openapi.json").read_text())
            schemas = contract["components"]["schemas"]
            Draft202012Validator({"$ref": "#/components/schemas/CreateConnection",
                                  "components": {"schemas": schemas}}).validate(json.loads(request.model_dump_json(by_alias=True)))
            Draft202012Validator({"$ref": "#/components/schemas/SourceConnection",
                                  "components": {"schemas": schemas}}).validate(json.loads(result.model_dump_json(by_alias=True)))
    asyncio.run(scenario())


def test_unknown_submission_is_not_retried_or_inferred_successful():
    async def scenario():
        calls = []
        def backend(request):
            calls.append(request)
            return httpx.Response(503, json={"code": "unavailable", "message": "Job submission was not confirmed"})
        async with httpx.AsyncClient(transport=httpx.MockTransport(backend)) as http:
            client = AsyncSourcesClient(base_url="https://epoch.invalid", token="fixture", http=http)
            with pytest.raises(SourceAPIError, match="not confirmed"):
                await client.start(REF, StartSync(request_id="one-attempt"))
            assert len(calls) == 1 and calls[0].method == "POST"
    asyncio.run(scenario())
