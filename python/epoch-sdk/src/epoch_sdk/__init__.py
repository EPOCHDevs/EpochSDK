"""Shared Epoch contracts. SDK/MCP flow adapters are added in their owning issues."""

from .api import Epoch, EpochApiError, UsageLimitReached
from .catalogue import CatalogueClient
from .contracts import (
    Acknowledgement,
    AiTextSkipped,
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
from .identity import IdentityClient, IdentityHTTPError
from .platform_files import PlatformFileError, PlatformFilesClient

__all__ = [
    "Acknowledgement",
    "CatalogueClient",
    "AiTextSkipped",
    "DomainError",
    "Epoch",
    "EpochApiError",
    "EpochError",
    "ErrorResponse",
    "FetchPageRequest",
    "FetchRequest",
    "FreshFetchRequest",
    "IngestRequest",
    "IdentityClient",
    "IdentityHTTPError",
    "JsonOutputRequest",
    "PlatformFileError",
    "PlatformFilesClient",
    "RefreshRequest",
    "RunParameters",
    "RunRequest",
    "TableOutputRequest",
    "TextOutputRequest",
    "UsageLimitReached",
    "date_range",
    "parse_fetch",
]
