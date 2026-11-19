# Source-owned Discovery component restored from canonical OpenAPI.
from __future__ import annotations

import typing
import pydantic
from ..core.pydantic_utilities import UniversalBaseModel
from .space_resource_ref import SpaceResourceRef


class SpacePlacementRequest(UniversalBaseModel):
    folder_ref: typing.Optional[str] = pydantic.Field(default=None)
    name: typing.Optional[str] = pydantic.Field(default=None)
    resource: SpaceResourceRef

    model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="forbid", frozen=True)
