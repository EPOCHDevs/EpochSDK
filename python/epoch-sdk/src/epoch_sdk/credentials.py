"""Bearer credentials for the native clients: a fixed token, or one read for every request.

A server that runs the SDK on a caller's behalf (the v1 API) holds short-lived delegated tokens
that renew. It passes a token provider instead of a string, and every graph, Backend and document
request awaits the provider for its token. A stream already open keeps the token it started with,
so renewal never interrupts it. Use one client per user and request; never share a provider
across users.
"""

from __future__ import annotations

import inspect
from collections.abc import AsyncGenerator, Awaitable, Callable, Generator
from urllib.parse import urlsplit

import httpx

TokenProvider = Callable[[], Awaitable[str] | str]
Token = str | TokenProvider

_DEFAULT_PORTS = {"http": 80, "https": 443}


def _origin(scheme: str, host: str | None, port: int | None) -> tuple[str, str, int | None]:
    return scheme, (host or "").lower(), port or _DEFAULT_PORTS.get(scheme)


def _url_origin(url: str) -> tuple[str, str, int | None]:
    parts = urlsplit(url)
    return _origin(parts.scheme, parts.hostname, parts.port)


def _valid(token: object) -> str:
    if not isinstance(token, str) or not token or any(c.isspace() or not c.isprintable() for c in token):
        raise ValueError("The token provider must return a non-empty token without spaces")
    return token


class BearerAuth(httpx.Auth):
    """Sets ``Authorization: Bearer <token>`` from a provider on requests to one origin.

    The provider is awaited for each request; it may also be a plain function. Requests to any
    other origin get no credential, so a token never reaches a third-party URL.
    """

    def __init__(self, token: TokenProvider, origin: str) -> None:
        if not callable(token):
            raise TypeError("token must be a string or a callable that returns one")
        self._token = token
        self._origin = _url_origin(origin)

    async def async_auth_flow(self, request: httpx.Request) -> AsyncGenerator[httpx.Request, httpx.Response]:
        if _origin(request.url.scheme, request.url.host, request.url.port) == self._origin:
            value = self._token()
            if inspect.isawaitable(value):
                value = await value
            request.headers["Authorization"] = f"Bearer {_valid(value)}"
        yield request

    def sync_auth_flow(self, request: httpx.Request) -> Generator[httpx.Request, httpx.Response, None]:
        raise RuntimeError("A token provider needs an asynchronous HTTP client")
        yield request  # pragma: no cover - makes this a generator


def http_clients(
    *,
    graph_url: str,
    backend_url: str,
    token: Token,
    transport: httpx.AsyncBaseTransport | None = None,
) -> tuple[httpx.AsyncClient, httpx.AsyncClient]:
    """The graph and Backend HTTP clients for one credential.

    A string becomes a fixed header on the graph client; the Backend clients send it themselves.
    A provider becomes an auth flow on both, scoped to each client's origin.
    """
    extra: dict[str, httpx.AsyncBaseTransport] = {"transport": transport} if transport else {}
    if isinstance(token, str):
        graph = httpx.AsyncClient(
            base_url=graph_url, headers={"Authorization": f"Bearer {token}"}, timeout=None, **extra
        )
        return graph, httpx.AsyncClient(timeout=30.0, **extra)
    graph = httpx.AsyncClient(base_url=graph_url, auth=BearerAuth(token, graph_url), timeout=None, **extra)
    return graph, httpx.AsyncClient(auth=BearerAuth(token, backend_url), timeout=30.0, **extra)
