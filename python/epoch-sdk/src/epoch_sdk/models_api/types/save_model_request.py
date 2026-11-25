# Source-owned Discovery component restored from canonical OpenAPI.
from __future__ import annotations

import typing
import pydantic
from ..core.pydantic_utilities import UniversalBaseModel


class SaveModelRequest(UniversalBaseModel):
    request_id: typing.Annotated[str, pydantic.Field(min_length=1, max_length=128)]
    name: typing.Annotated[str, pydantic.Field(min_length=1, max_length=255)]
    execution_id: typing.Annotated[str, pydantic.Field(min_length=1, max_length=256)]
    fit_name: typing.Annotated[str, pydantic.Field(min_length=1, max_length=128)]
    expected_digest: typing.Annotated[str, pydantic.Field(pattern='^sha256:[0-9a-f]{64}$')]
    source_location: typing.Optional[typing.Literal['shared_personal_v1', 'server']] = pydantic.Field(default=None)

    model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="forbid", frozen=True)
