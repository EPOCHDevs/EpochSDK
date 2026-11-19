"""Signed storage transfers: Platform's direct file transfer (ENG-2960).

Platform signs a link for one upload part or one staged edit, covering its length and SHA-256.
The bytes go straight to storage and never through the API, whose firewall reads request bodies
(EpochPlatform docs/design/direct-file-transfer.md).
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable, Mapping
from typing import Any

import httpx

SignedLink = tuple[str, Mapping[str, str]]


class StorageTransferError(RuntimeError):
    """Storage refused a signed transfer. The message never includes the link."""

    def __init__(self, status: int):
        super().__init__(f"Storage refused the signed file transfer ({status})")
        self.status = status


class StorageClient:
    """Puts bytes to signed storage links.

    It sends through a transport of its own: no API credentials or cookies, no redirects, and no
    request logging (httpx's client logs every URL at INFO, and a signed URL carries its signature).
    """

    def __init__(self, transport: httpx.AsyncBaseTransport | None = None):
        self._transport = transport or httpx.AsyncHTTPTransport(retries=0)

    async def __aenter__(self) -> StorageClient:
        return self

    async def __aexit__(self, *_: object) -> None:
        await self._transport.aclose()

    async def put(self, url: str, headers: Mapping[str, str], body: bytes) -> int:
        request = httpx.Request(
            "PUT", url, headers=dict(headers), content=body,
            extensions={"timeout": {"connect": 30.0, "read": 300.0, "write": 300.0, "pool": 30.0}},
        )
        response = await self._transport.handle_async_request(request)
        try:
            await response.aread()
        finally:
            await response.aclose()
        return response.status_code


def storage_client() -> StorageClient:
    return StorageClient()


def signed_link(link: Any, size: int) -> SignedLink:
    """The URL and headers of a link Platform signed for exactly `size` bytes."""
    value = link if isinstance(link, Mapping) else link.model_dump(mode="json")
    if value.get("method") != "PUT" or value.get("size_bytes") != size:
        raise ValueError("Platform signed a different file transfer")
    return value["url"], value["headers"]


async def put_signed(
    storage: StorageClient, link: Callable[[], Awaitable[SignedLink]], body: bytes
) -> None:
    """PUT exact bytes with exactly the signed headers.

    A link can lapse before its expiry when Platform's credentials rotate, so a refused PUT
    asks for one new link. Signing records nothing, so asking again is safe.
    """
    for attempt in range(2):
        url, headers = await link()
        status = await storage.put(url, headers, body)
        if 200 <= status < 300:
            return
        if attempt or status not in (400, 403):
            raise StorageTransferError(status)
