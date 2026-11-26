"""Actual generated Platform clients over mock HTTP; no live acceptance claim."""

import asyncio
import hashlib
import json
from copy import deepcopy
from pathlib import Path

import httpx
import pytest
from pydantic import ValidationError

from epoch_sdk.presentation_api import AsyncEpochPresentations, EpochPresentations
from epoch_sdk.presentation_api import errors as presentation_errors
from epoch_sdk.presentation_api.core.api_error import ApiError
from epoch_sdk.presentation_api.types import (
    FinalPresentationDelivery,
    FinalPresentationDeliveryRequest,
)

FIXTURES = Path(__file__).resolve().parents[3] / "contracts/fixtures/platform-presentations"


def fixture(name):
    return json.loads((FIXTURES / (name + ".json")).read_text())


@pytest.mark.parametrize("asynchronous", [False, True])
@pytest.mark.parametrize(
    "name",
    ["pending-delivery", "retained-delivery", "absent-response-delivery", "literal-null-delivery"],
)
def test_actual_clients_keep_source_identity_raw_documents_and_nulls(name, asynchronous):
    wire, seen = fixture(name), []

    def handler(request):
        seen.append(request)
        assert request.method == "POST"
        assert request.url.path == "/api/v1/contexts/executions/fixture-run/presentation/delivery"
        assert request.headers["authorization"] == "Bearer fixture-token"
        assert json.loads(request.content) == fixture("initial-request")
        return httpx.Response(200, json={**wire, "future_server_field": {"keep": True}})

    async def scenario():
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
            client = AsyncEpochPresentations(
                base_url="https://platform.test", token="fixture-token", httpx_client=http
            )
            return await client.read_final_presentation_delivery(
                "fixture-run", **fixture("initial-request"), request_options={"max_retries": 0}
            )

    if asynchronous:
        result = asyncio.run(scenario())
    else:
        with httpx.Client(transport=httpx.MockTransport(handler)) as http:
            client = EpochPresentations(
                base_url="https://platform.test", token="fixture-token", httpx_client=http
            )
            result = client.read_final_presentation_delivery(
                "fixture-run", **fixture("initial-request"), request_options={"max_retries": 0}
            )
    assert len(seen) == 1
    assert result.schema_version == 2
    assert result.retention.state == wire["retention"]["state"]
    assert result.content.model_dump() == wire["content"]
    for field, pin in [
        ("dashboard_json", "schema_sha256"),
        ("canonical_prose_json", "prose_sha256"),
        ("response_json", "response_sha256"),
    ]:
        raw = getattr(result.content, field)
        assert (hashlib.sha256(raw.encode()).hexdigest() if raw is not None else None) == getattr(
            result.source, pin
        )
    assert result.artifacts[0].url == wire["artifacts"][0]["url"]
    assert result.response_tables[0].parts[0].url == wire["response_tables"][0]["parts"][0]["url"]
    assert result.model_extra["future_server_field"] == {"keep": True}


@pytest.mark.parametrize("asynchronous", [False, True])
def test_renewal_uses_exact_source_and_retained_reference_without_rewriting(asynchronous):
    request = fixture("renewal-request")

    def handler(wire):
        assert json.loads(wire.content) == request
        return httpx.Response(200, json=fixture("retained-delivery"))

    async def scenario():
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
            client = AsyncEpochPresentations(
                base_url="https://platform.test", token="fixture-token", httpx_client=http
            )
            await client.read_final_presentation_delivery("fixture-run", **request)

    if asynchronous:
        asyncio.run(scenario())
    else:
        with httpx.Client(transport=httpx.MockTransport(handler)) as http:
            EpochPresentations(
                base_url="https://platform.test", token="fixture-token", httpx_client=http
            ).read_final_presentation_delivery("fixture-run", **request)


@pytest.mark.parametrize(
    "change",
    [
        {"execution_category": ""},
        {"expected_source": None},
        {"max_expires_epoch": True},
        {"max_expires_epoch": -1},
        {"max_expires_epoch": 9007199254740992},
        {
            "expected_source": {
                **fixture("renewal-request")["expected_source"],
                "config_sha256": "latest",
            }
        },
        {
            "expected_source": {
                **fixture("renewal-request")["expected_source"],
                "unexpected": "not owned",
            }
        },
    ],
)
@pytest.mark.parametrize("asynchronous", [False, True])
def test_source_owned_invalid_requests_do_not_reach_http(change, asynchronous):
    value = {**fixture("initial-request"), **change}
    with pytest.raises(ValidationError):
        FinalPresentationDeliveryRequest.model_validate(value)

    def forbidden(request):
        pytest.fail("Source-invalid request reached HTTP")

    async def scenario():
        async with httpx.AsyncClient(transport=httpx.MockTransport(forbidden)) as http:
            client = AsyncEpochPresentations(
                base_url="https://platform.test", token="fixture-token", httpx_client=http
            )
            with pytest.raises(ValidationError):
                await client.read_final_presentation_delivery("fixture-run", **value)

    if asynchronous:
        asyncio.run(scenario())
    else:
        with (
            httpx.Client(transport=httpx.MockTransport(forbidden)) as http,
            pytest.raises(ValidationError),
        ):
            EpochPresentations(
                base_url="https://platform.test", token="fixture-token", httpx_client=http
            ).read_final_presentation_delivery("fixture-run", **value)


@pytest.mark.parametrize(
    "status,error_name",
    [
        (400, "BadRequestError"),
        (401, "UnauthorizedError"),
        (403, "ForbiddenError"),
        (404, "NotFoundError"),
        (409, "ConflictError"),
        (410, "GoneError"),
        (413, "ContentTooLargeError"),
        (425, "TooEarlyError"),
        (503, "ServiceUnavailableError"),
        (504, "GatewayTimeoutError"),
    ],
)
def test_typed_errors_preserve_body_status_and_retry_header_without_retries(status, error_name):
    calls = []

    def handler(request):
        calls.append(request)
        assert request.extensions["timeout"]["read"] == 0.125
        return httpx.Response(status, json=fixture("error"), headers={"Retry-After": "1"})

    with httpx.Client(transport=httpx.MockTransport(handler)) as http:
        client = EpochPresentations(
            base_url="https://platform.test", token="fixture-token", httpx_client=http
        )
        with pytest.raises(ApiError) as caught:
            client.read_final_presentation_delivery(
                "fixture-run",
                execution_category="ALL",
                request_options={"max_retries": 0, "timeout_in_seconds": 0.125},
            )
    assert len(calls) == 1
    assert type(caught.value) is getattr(presentation_errors, error_name)
    assert caught.value.status_code == status
    assert caught.value.body.model_dump() == fixture("error")
    assert caught.value.headers["retry-after"] == "1"


def test_required_nullable_and_control_discriminators_are_not_widened():
    for change in ["missing-null", "version", "retention"]:
        value = deepcopy(fixture("absent-response-delivery"))
        if change == "missing-null":
            value["content"].pop("response_json")
        elif change == "version":
            value["schema_version"] = 3
        else:
            value["retention"] = {"state": "invented"}
        with pytest.raises(ValidationError):
            FinalPresentationDelivery.model_validate(value)


def test_async_cancellation_stops_the_read_without_another_operation():
    async def scenario():
        started, count = asyncio.Event(), []

        async def handler(request):
            count.append(request)
            started.set()
            await asyncio.Event().wait()

        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
            client = AsyncEpochPresentations(
                base_url="https://platform.test", token="fixture-token", httpx_client=http
            )
            task = asyncio.create_task(
                client.read_final_presentation_delivery(
                    "fixture-run", execution_category="ALL", request_options={"max_retries": 0}
                )
            )
            await started.wait()
            task.cancel()
            with pytest.raises(asyncio.CancelledError):
                await task
        assert len(count) == 1

    asyncio.run(scenario())
