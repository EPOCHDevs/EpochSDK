"""The Files and Space client a connected Epoch client carries (ENG-2819).

Platform owns Files and Space. Its client is generated from Platform's contract
(`epoch_sdk.files_api`), never from Backend's.
"""
from __future__ import annotations

from .files_api import AsyncEpochFiles


def files_client(owner: object) -> AsyncEpochFiles:
    client = getattr(owner, "files_api", None)
    if client is None:
        raise ValueError(
            "Pass files_api (epoch_sdk.files_api.AsyncEpochFiles), or use a connected Epoch client"
        )
    return client
