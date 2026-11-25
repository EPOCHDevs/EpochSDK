# Source-owned Discovery component restored from canonical OpenAPI.
from __future__ import annotations

import typing
import pydantic
from ..core.pydantic_utilities import UniversalBaseModel


class CompleteModelSavesRequest(UniversalBaseModel):
    execution_id: typing.Annotated[str, pydantic.Field(min_length=1, max_length=256)]
    source_location: typing.Optional[typing.Literal['shared_personal_v1', 'server']] = pydantic.Field(default=None)

    model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="forbid", frozen=True)
