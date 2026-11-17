"""Shared Epoch contracts. SDK/MCP flow adapters are added in their owning issues."""

from .api import Epoch, EpochApiError
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
from .dates import date_range
from .errors import EpochError
from .platform_files import PlatformFileError, PlatformFilesClient

__all__ = [
    "Acknowledgement",
    "DomainError",
    "Epoch",
    "EpochApiError",
    "EpochError",
    "ErrorResponse",
    "FetchPageRequest",
    "FetchRequest",
    "FreshFetchRequest",
    "IngestRequest",
    "JsonOutputRequest",
    "PlatformFileError",
    "PlatformFilesClient",
    "RefreshRequest",
    "RunParameters",
    "RunRequest",
    "TableOutputRequest",
    "TextOutputRequest",
    "date_range",
    "parse_fetch",
]
