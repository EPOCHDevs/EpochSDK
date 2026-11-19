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


def storage_client() -> httpx.AsyncClient:
    """A client of its own: the API client's credentials must never reach storage."""
    return httpx.AsyncClient(timeout=httpx.Timeout(300, connect=30), follow_redirects=False)


def signed_link(link: Any, size: int) -> SignedLink:
    """The URL and headers of a link Platform signed for exactly `size` bytes."""
    value = link if isinstance(link, Mapping) else link.model_dump(mode="json")
    if value.get("method") != "PUT" or value.get("size_bytes") != size:
        raise ValueError("Platform signed a different file transfer")
    return value["url"], value["headers"]


async def put_signed(
    storage: httpx.AsyncClient, link: Callable[[], Awaitable[SignedLink]], body: bytes
) -> None:
    """PUT exact bytes with exactly the signed headers.

    A link can lapse before its expiry when Platform's credentials rotate, so a refused PUT
    asks for one new link. Signing records nothing, so asking again is safe.
    """
    for attempt in range(2):
        url, headers = await link()
        response = await storage.put(url, content=body, headers=dict(headers))
        if response.is_success:
            return
        if attempt or response.status_code not in (400, 403):
            raise StorageTransferError(response.status_code)
