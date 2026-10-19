"""Read-only checks against the actual native clients; never starts analytical work."""

from __future__ import annotations

import argparse
import asyncio
import importlib.metadata
import json
import os
from typing import Literal, Protocol, cast
from urllib.parse import urlsplit

import httpx
from langgraph_sdk import get_client
from pydantic import BaseModel, ConfigDict
from stratifyx import AsyncStratifyX, StratifyX
from stratifyx.core.api_error import ApiError
from stratifyx.core.request_options import RequestOptions


class ServiceAccess(BaseModel):
    model_config = ConfigDict(extra="forbid")
    service: Literal["Backend", "LangGraph"]
    status: Literal["reachable", "unavailable", "auth_required", "missing_graph", "http_error"]
    authenticated: bool | None = None
    detail: str


class AccessReport(BaseModel):
    model_config = ConfigDict(extra="forbid")
    stratifyx_version: str
    langgraph_sdk_version: str
    backend_attempt_sdk_available: bool
    services: list[ServiceAccess]


class _AttemptReader(Protocol):
    # Source-owned native operation; the installed preview currently lacks it.
    async def get_integration_execution(
        self, execution_id: str, *, request_options: RequestOptions | None = None
    ) -> object: ...


class _IntegrationClient(Protocol):
    @property
    def integration_executions(self) -> _AttemptReader: ...


def _validate_url(url: str) -> str:
    parsed = urlsplit(url)
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise ValueError("Provide an HTTP(S) service URL")
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("Keep credentials out of service URLs; use token environment variables")
    return url


async def check_access(
    backend_url: str,
    graph_url: str,
    graph_id: str,
    token: str | None,
    attempt_id: str | None = None,
) -> AccessReport:
    _validate_url(backend_url)
    _validate_url(graph_url)

    async def backend() -> ServiceAccess:
        try:
            async with httpx.AsyncClient(timeout=3.0) as http:
                client = AsyncStratifyX(base_url=backend_url, token=token, httpx_client=http)
                await client.health.health_check(request_options={"max_retries": 0})
                if attempt_id is not None and hasattr(client, "integration_executions"):
                    reader = cast(_IntegrationClient, client).integration_executions
                    await reader.get_integration_execution(
                        attempt_id, request_options={"max_retries": 0}
                    )
                    return ServiceAccess(
                        service="Backend",
                        status="reachable",
                        authenticated=True,
                        detail="Native owner-scoped attempt read succeeded.",
                    )
            # Public health confirms connectivity only, never owner-scoped authorization.
            return ServiceAccess(
                service="Backend",
                status="reachable",
                detail="Native health API responded; authenticated attempt access still needs verification.",
            )
        except ApiError as exc:
            return ServiceAccess(
                service="Backend",
                status="auth_required" if exc.status_code in (401, 403) else "http_error",
                authenticated=False if exc.status_code in (401, 403) else None,
                detail="Native Backend API rejected the check.",
            )
        except httpx.HTTPError:
            return ServiceAccess(
                service="Backend",
                status="unavailable",
                detail="Configured Backend endpoint is unavailable.",
            )

    async def graph() -> ServiceAccess:
        headers = {"Authorization": f"Bearer {token}"} if token else None
        client = get_client(
            url=graph_url, api_key=os.environ.get("LANGGRAPH_API_KEY"), headers=headers, timeout=3.0
        )
        try:
            assistants = await client.assistants.search(graph_id=graph_id, limit=1)
            if isinstance(assistants, dict):
                return ServiceAccess(
                    service="LangGraph",
                    status="http_error",
                    detail="Unexpected assistant-discovery response shape.",
                )
            if not assistants:
                return ServiceAccess(
                    service="LangGraph",
                    status="missing_graph",
                    detail="Server responded, but the dedicated integration graph is not registered.",
                )
            await client.assistants.get_schemas(assistants[0]["assistant_id"])
            return ServiceAccess(
                service="LangGraph",
                status="reachable",
                detail="Native assistant discovery found the integration graph.",
            )
        except httpx.HTTPStatusError as exc:
            return ServiceAccess(
                service="LangGraph",
                status="auth_required" if exc.response.status_code in (401, 403) else "http_error",
                authenticated=False if exc.response.status_code in (401, 403) else None,
                detail="Native LangGraph API rejected the check.",
            )
        except httpx.HTTPError:
            return ServiceAccess(
                service="LangGraph",
                status="unavailable",
                detail="Configured LangGraph endpoint is unavailable.",
            )
        finally:
            await client.aclose()

    results = await asyncio.gather(backend(), graph())
    return AccessReport(
        stratifyx_version=importlib.metadata.version("stratifyx"),
        langgraph_sdk_version=importlib.metadata.version("langgraph-sdk"),
        backend_attempt_sdk_available=hasattr(StratifyX, "integration_executions"),
        services=list(results),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend-url", default=os.environ.get("EPOCH_CAMPAIGN_SERVER"))
    parser.add_argument("--graph-url", default=os.environ.get("LANGGRAPH_API_URL"))
    parser.add_argument("--graph-id", default="integration_run")
    parser.add_argument(
        "--attempt-id",
        help="Existing attempt owned by the caller; verifies authenticated read access",
    )
    args = parser.parse_args()
    if not args.backend_url or not args.graph_url:
        parser.error("Provide both native service URLs")
    report = asyncio.run(
        check_access(
            args.backend_url,
            args.graph_url,
            args.graph_id,
            os.environ.get("EPOCH_ACCESS_TOKEN"),
            args.attempt_id,
        )
    )
    print(json.dumps(report.model_dump(), indent=2))
    if (
        not report.backend_attempt_sdk_available
        or not any(c.service == "Backend" and c.authenticated is True for c in report.services)
        or any(c.status != "reachable" for c in report.services)
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
