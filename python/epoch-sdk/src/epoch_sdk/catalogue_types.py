"""Closed Platform directory envelopes around native compiler-owned definitions.

The directory and private inventory are served by Platform/GDS. Native schema
leaves describe executable source capabilities; no native search API is needed.
"""
from __future__ import annotations

from typing import Literal

from pydantic import Field, StrictBool, StrictInt, StrictStr
from stratifyx.types import (
    DataSourceRegistryBacking,
    DataSourceRegistryEndpoint,
    DataSourceRegistryFamily,
    DataSourceRegistryKey,
    DataSourceRegistryOption,
    DataSourceRegistryOutput,
    DataSourceRegistryScope,
    DataSourceRegistrySource,
    DataSourceRegistryWindow,
)

from .discovery_model import DiscoveryModel
from .files_api.types import SavedDataset


class CatalogueRequest(DiscoveryModel):
    source_ids: list[StrictStr] = Field(default_factory=list, max_length=1000)
    include_details: StrictBool = False
    include_summaries: StrictBool = False
    include_overview: StrictBool = True
    include_saved: StrictBool = True
    saved_cursor: StrictStr | None = None
    saved_limit: StrictInt = Field(default=100, ge=1, le=100)


class SourceImplementation(DiscoveryModel):
    id: StrictStr
    description: StrictStr
    signature: StrictStr
    options: list[DataSourceRegistryOption]
    outputs: list[DataSourceRegistryOutput]


class SourceEntry(DiscoveryModel):
    source: DataSourceRegistrySource
    implementations: list[SourceImplementation]
    endpoints: dict[str, DataSourceRegistryEndpoint]
    documentation: StrictStr


class SourceSummary(DiscoveryModel):
    source_id: StrictStr
    name: StrictStr
    description: StrictStr
    family: DataSourceRegistryFamily
    data_categories: list[StrictStr]
    scope: DataSourceRegistryScope
    keys: list[DataSourceRegistryKey]
    requires_futures_root: StrictBool
    window: DataSourceRegistryWindow
    browse_groups: list[Literal['market_data','fundamentals','macro','saved_data','events']]
    vendor: StrictStr | None = None
    backing: DataSourceRegistryBacking | None = None


class SavedInventory(DiscoveryModel):
    items: list[SavedDataset]
    next_cursor: StrictStr | None = None


class CatalogueResult(DiscoveryModel):
    registry_version: StrictStr
    loader_registry_version: StrictStr
    overview: StrictStr
    sources: list[SourceEntry]
    summaries: list[SourceSummary] | None = None
    saved: SavedInventory | None = None
