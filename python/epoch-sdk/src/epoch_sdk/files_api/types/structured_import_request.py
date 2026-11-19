# Source-owned Discovery component restored from canonical OpenAPI.
from __future__ import annotations

import typing
import pydantic
from ..core.pydantic_utilities import UniversalBaseModel
from .dataset_purpose import DatasetPurpose
from .dataset_table_schema import DatasetTableSchema
from .structured_import_options import StructuredImportOptions


class StructuredImportRequest(UniversalBaseModel):
    file_ref: str
    metadata: typing.Optional[DatasetTableSchema] = pydantic.Field(default=None)
    name: str
    options: StructuredImportOptions
    purpose: typing.Optional[DatasetPurpose] = pydantic.Field(default=None)
    request_id: str

    model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="forbid", frozen=True)
