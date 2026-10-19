from __future__ import annotations

import asyncio
import json

import httpx
import pytest

from epoch_sdk import capabilities


def transport(
    monkeypatch: pytest.MonkeyPatch,
    *,
    study_status: int = 200,
    graph_present: bool = True,
    expect_token: bool = True,
) -> list[httpx.Request]:
    calls: list[httpx.Request] = []
    original = httpx.AsyncClient
    monkeypatch.delenv("LANGGRAPH_API_KEY", raising=False)

    def respond(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        if request.method == "GET" and request.url.path == "/health":
            return httpx.Response(200, json={"status": "ok", "git_sha": "fixture"})
        if request.method == "GET" and request.url.path == "/api/v1/studies/definitions/owned":
            if expect_token:
                assert request.headers["Authorization"] == "Bearer fixture-only"
            else:
                assert "Authorization" not in request.headers
            if study_status != 200:
                return httpx.Response(
                    study_status,
                    json={
                        "error": "Unauthorized",
                        "message": "Rejected",
                        "timestamp": "2026-10-18T00:00:00Z",
                    },
                )
            return httpx.Response(
                200,
                json={
                    "name": "Owned saved study",
                    "description": "Fixture",
                    "source": "Saved source",
                    "data": {"assets": []},
                    "authoring_origin": "agent",
                },
            )
        if request.method == "POST" and request.url.path == "/assistants/search":
            assert json.loads(request.content)["graph_id"] == "epoch-ai"
            return httpx.Response(
                200, json=[{"assistant_id": "graph-fixture"}] if graph_present else []
            )
        if request.method == "GET" and request.url.path == "/assistants/graph-fixture/schemas":
            return httpx.Response(200, json={"graph_id": "epoch-ai", "input_schema": {}})
        raise AssertionError(f"Unexpected check: {request.method} {request.url.path}")

    def factory(*args, **kwargs):
        kwargs["transport"] = httpx.MockTransport(respond)
        return original(*args, **kwargs)

    monkeypatch.setattr(httpx, "AsyncClient", factory)
    return calls


def test_owned_study_and_existing_supervisor_pass_without_an_attempt_controller(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = transport(monkeypatch)
    report = asyncio.run(
        capabilities.check_access(
            "https://backend.invalid",
            "https://graph.invalid",
            "epoch-ai",
            "fixture-only",
            study_id="owned",
        )
    )
    assert report.ready()
    assert not report.backend_attempt_sdk_available
    assert all(call.method == "GET" or call.url.path == "/assistants/search" for call in calls)
    assert not any("/runs" in call.url.path or call.url.path == "/threads" for call in calls)


def test_public_health_does_not_claim_protected_backend_access(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    transport(monkeypatch)
    report = asyncio.run(
        capabilities.check_access(
            "https://backend.invalid", "https://graph.invalid", "epoch-ai", None
        )
    )
    assert not report.ready()
    backend = next(item for item in report.services if item.service == "Backend")
    assert backend.status == "reachable" and backend.authenticated is None


def test_an_open_development_read_without_a_bearer_does_not_claim_authenticated_access(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    transport(monkeypatch, expect_token=False)
    report = asyncio.run(
        capabilities.check_access(
            "https://backend.invalid",
            "https://graph.invalid",
            "epoch-ai",
            None,
            study_id="owned",
        )
    )
    assert not report.ready()
    backend = next(item for item in report.services if item.service == "Backend")
    assert backend.status == "reachable" and backend.authenticated is False


def test_rejected_owned_read_is_not_hidden_by_successful_health(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    transport(monkeypatch, study_status=401)
    report = asyncio.run(
        capabilities.check_access(
            "https://backend.invalid",
            "https://graph.invalid",
            "epoch-ai",
            "fixture-only",
            study_id="owned",
        )
    )
    assert not report.ready()
    backend = next(item for item in report.services if item.service == "Backend")
    assert backend.status == "auth_required" and backend.authenticated is False


def test_missing_requested_graph_is_not_reported_as_available(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    transport(monkeypatch, graph_present=False)
    report = asyncio.run(
        capabilities.check_access(
            "https://backend.invalid",
            "https://graph.invalid",
            "epoch-ai",
            "fixture-only",
            study_id="owned",
        )
    )
    assert not report.ready()
    assert any(item.status == "missing_graph" for item in report.services)


def test_legacy_attempt_probe_is_optional_but_explicit_missing_probe_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    transport(monkeypatch)
    report = asyncio.run(
        capabilities.check_access(
            "https://backend.invalid",
            "https://graph.invalid",
            "epoch-ai",
            "fixture-only",
            attempt_id="legacy",
        )
    )
    assert not report.ready()
    assert any(item.status == "missing_capability" for item in report.services)
