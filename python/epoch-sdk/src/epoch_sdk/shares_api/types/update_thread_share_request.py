# Source-owned Discovery component restored from canonical OpenAPI.
from __future__ import annotations

import typing
import pydantic
from ..core.pydantic_utilities import UniversalBaseModel


class UpdateThreadShareRequest(UniversalBaseModel):
    projection: typing.Optional[typing.Any] = pydantic.Field(default=None)
    execution_ids: typing.Optional[typing.Annotated[typing.List[str], pydantic.Field(description='Completed runs of this conversation to include; their files are read from the job index, never from the caller')]] = pydantic.Field(description='Completed runs of this conversation to include; their files are read from the job index, never from the caller', default=None)
    branch_checkpoint_id: typing.Optional[str] = pydantic.Field(default=None)
    expected_snapshot_version: typing.Optional[typing.Annotated[int, pydantic.Field(ge=-9007199254740991, le=9007199254740991, description='The version the owner last saw; the update is refused with 409 if the link has moved on')]] = pydantic.Field(strict=True, ge=-9007199254740991, le=9007199254740991, description='The version the owner last saw; the update is refused with 409 if the link has moved on', default=None)

    model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="forbid", frozen=True)
