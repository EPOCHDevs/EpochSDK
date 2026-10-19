"""Shared Epoch contracts. SDK/MCP flow adapters are added in their owning issues."""

from .contracts import (
    Acknowledgement,
    DomainError,
    ErrorResponse,
    FetchPageRequest,
    FetchRequest,
    FreshFetchRequest,
    IngestRequest,
    JsonOutputRequest,
    RefreshRequest,
    RunParameters,
    RunRequest,
    TableOutputRequest,
    TextOutputRequest,
    parse_fetch,
)
from .errors import EpochError

__all__ = [
    "Acknowledgement",
    "DomainError",
    "EpochError",
    "ErrorResponse",
    "FetchPageRequest",
    "FetchRequest",
    "FreshFetchRequest",
    "IngestRequest",
    "JsonOutputRequest",
    "RefreshRequest",
    "RunParameters",
    "RunRequest",
    "TableOutputRequest",
    "TextOutputRequest",
    "parse_fetch",
]
