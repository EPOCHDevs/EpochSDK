"""A token string or a renewing token provider for the native clients (ENG-2511)."""

from __future__ import annotations

import asyncio

import httpx
import pytest
from epoch_sdk.credentials import BearerAuth
from epoch_sdk.supervisor import SupervisorClient
from stratifyx.core.api_error import ApiError

GRAPH = "https://graph.test"
BACKEND = "https://backend.test"


class Recorder:
    """Records each request's path and Authorization header; serves a short event stream."""

    def __init__(self, stream_chunks: list[bytes] | None = None) -> None:
        self.seen: list[tuple[str, str | None]] = []
        self.stream_chunks = stream_chunks or []
        self.between_chunks: asyncio.Event | None = None

    async def __call__(self, request: httpx.Request) -> httpx.Response:
        self.seen.append((request.url.path, request.headers.get("Authorization")))
        if request.url.path.endswith("/stream"):
            return httpx.Response(200, headers={"content-type": "text/event-stream"}, content=self._events())
        return httpx.Response(
            404, json={"error": "not found", "message": "not found", "timestamp": "2026-11-10T00:00:00Z"}
        )

    async def _events(self):
        for chunk in self.stream_chunks:
            yield chunk
            await asyncio.sleep(0)

    def header(self, path: str) -> str | None:
        return next(value for seen, value in reversed(self.seen) if seen == path)


class Rotating:
    """A provider whose token the test can change."""

    def __init__(self, token: str) -> None:
        self.token = token
        self.calls = 0

    async def __call__(self) -> str:
        self.calls += 1
        return self.token


def connect(token, recorder: Recorder) -> SupervisorClient:
    return SupervisorClient._connect(
        graph_url=GRAPH, backend_url=BACKEND, token=token, transport=httpx.MockTransport(recorder)
    )


async def backend_get(client: SupervisorClient, request_id: str) -> None:
    with pytest.raises(ApiError):
        await client.backend.sdk_requests.get_sdk_request(request_id)


async def sources_list(client: SupervisorClient) -> None:
    assert client.source_connections is not None
    with pytest.raises(Exception):
        await client.source_connections.list()


async def graph_get(client: SupervisorClient, thread_id: str) -> None:
    with pytest.raises(httpx.HTTPStatusError):
        await client.graph.threads.get(thread_id)


def test_a_string_token_is_sent_as_before() -> None:
    async def run() -> None:
        recorder = Recorder()
        client = connect("fixed-token", recorder)
        assert all(http.auth is None or not isinstance(http.auth, BearerAuth) for http in client._owned_http)
        await backend_get(client, "req-1")
        await sources_list(client)
        await graph_get(client, "thread-1")
        await client.aclose()
        assert {value for _, value in recorder.seen} == {"Bearer fixed-token"}
        assert len(recorder.seen) == 3

    asyncio.run(run())


def test_a_provider_is_read_for_every_request() -> None:
    async def run() -> None:
        recorder = Recorder()
        token = Rotating("first")
        client = connect(token, recorder)
        await backend_get(client, "req-1")
        await sources_list(client)
        await graph_get(client, "thread-1")
        assert {value for _, value in recorder.seen} == {"Bearer first"}

        token.token = "second"
        await backend_get(client, "req-2")
        await sources_list(client)
        await graph_get(client, "thread-2")
        await client.aclose()
        assert [value for _, value in recorder.seen[3:]] == ["Bearer second"] * 3
        assert token.calls == 6

    asyncio.run(run())


def test_a_stream_keeps_running_when_the_token_rotates() -> None:
    async def run() -> None:
        events = [f'event: values\ndata: {{"step": {n}}}\n\n'.encode() for n in range(3)]
        recorder = Recorder(stream_chunks=events)
        token = Rotating("first")
        client = connect(token, recorder)

        received = []
        async for part in client.graph.runs.join_stream("thread-1", "run-1"):
            received.append(part.data)
            # Renewal while the stream is open: the stream carries on, later requests renew.
            token.token = "second"
            await graph_get(client, "thread-1")
        await backend_get(client, "req-1")
        await client.aclose()

        assert [data["step"] for data in received if isinstance(data, dict)] == [0, 1, 2]
        assert recorder.header("/threads/thread-1/runs/run-1/stream") == "Bearer first"
        assert recorder.header("/threads/thread-1") == "Bearer second"
        assert recorder.header("/api/v1/integration/requests/req-1") == "Bearer second"

    asyncio.run(run())


def test_two_users_clients_stay_isolated() -> None:
    async def run() -> None:
        recorder = Recorder()
        alice = connect(Rotating("alice-token"), recorder)
        bob = connect(Rotating("bob-token"), recorder)
        await asyncio.gather(
            *(backend_get(alice, f"alice-{n}") for n in range(20)),
            *(backend_get(bob, f"bob-{n}") for n in range(20)),
            *(graph_get(alice, f"alice-t{n}") for n in range(5)),
            *(graph_get(bob, f"bob-t{n}") for n in range(5)),
        )
        await alice.aclose()
        await bob.aclose()
        assert len(recorder.seen) == 50
        for path, value in recorder.seen:
            owner = "alice" if "alice" in path else "bob"
            assert value == f"Bearer {owner}-token", path

    asyncio.run(run())


def test_a_provider_never_sends_its_token_to_another_origin() -> None:
    async def run() -> None:
        recorder = Recorder()
        client = connect(Rotating("secret"), recorder)
        backend_http = client._owned_http[1]
        await backend_http.get("https://uploads.example/presigned")
        await backend_http.get("http://backend.test/insecure")
        await backend_http.get("https://backend.test:8443/other-port")
        await client.aclose()
        assert [value for _, value in recorder.seen] == [None, None, None]

    asyncio.run(run())


def test_a_provider_may_be_a_plain_function_and_must_return_a_token() -> None:
    async def run() -> None:
        recorder = Recorder()
        client = connect(lambda: "plain", recorder)
        await backend_get(client, "req-1")
        await client.aclose()
        assert recorder.seen == [("/api/v1/integration/requests/req-1", "Bearer plain")]

        for bad in ("", "two words", "line\nbreak"):
            broken = connect(Rotating(bad), Recorder())
            with pytest.raises(ValueError, match="non-empty token"):
                await broken.backend.sdk_requests.get_sdk_request("req-1")
            await broken.aclose()

    asyncio.run(run())


def test_a_provider_needs_an_async_client_and_a_callable() -> None:
    with pytest.raises(TypeError):
        BearerAuth("not callable", BACKEND)  # type: ignore[arg-type]
    with httpx.Client(auth=BearerAuth(Rotating("x"), BACKEND), transport=httpx.MockTransport(lambda _: httpx.Response(200))) as http:
        with pytest.raises(RuntimeError, match="asynchronous"):
            http.get(f"{BACKEND}/anything")
