# Source-owned Discovery component restored from canonical OpenAPI.
from __future__ import annotations

import typing
import pydantic
from ..core.pydantic_utilities import UniversalBaseModel


class SelectShareVersionRequest(UniversalBaseModel):
    snapshot_version: typing.Annotated[int, pydantic.Field(le=9007199254740991)] = pydantic.Field(strict=True, le=9007199254740991, gt=0)
    expected_current_version: typing.Annotated[int, pydantic.Field(le=9007199254740991)] = pydantic.Field(strict=True, le=9007199254740991, gt=0)

    model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="forbid", frozen=True)
