# Source-owned Discovery component restored from canonical OpenAPI.
from __future__ import annotations

import typing
import pydantic
from ..core.pydantic_utilities import UniversalBaseModel


class CreateThreadShareRequest(UniversalBaseModel):
    projection: typing.Optional[typing.Any] = pydantic.Field(description='The conversation copy, already redacted by EpochAI. Must be a JSON object; stored as received', default=None)
    execution_ids: typing.Optional[typing.Annotated[typing.List[str], pydantic.Field(description='Completed runs of this conversation to include; their files are read from the job index, never from the caller')]] = pydantic.Field(description='Completed runs of this conversation to include; their files are read from the job index, never from the caller', default=None)
    branch_checkpoint_id: typing.Optional[str] = pydantic.Field(default=None)
    audience: typing.Optional[typing.Annotated[str, pydantic.Field(description="Exactly 'anyone_with_link' opens without sign-in; any other value means named_subjects")]] = pydantic.Field(description="Exactly 'anyone_with_link' opens without sign-in; any other value means named_subjects", default=None)
    subjects: typing.Optional[typing.Annotated[typing.List[str], pydantic.Field(description='Invited email addresses for named_subjects, at most 50; stored lower-cased')]] = pydantic.Field(description='Invited email addresses for named_subjects, at most 50; stored lower-cased', default=None)
    expires_in_seconds: typing.Optional[typing.Annotated[int, pydantic.Field(ge=-9007199254740991, le=9007199254740991, description='0 (never) or 1..31536000')]] = pydantic.Field(strict=True, ge=-9007199254740991, le=9007199254740991, description='0 (never) or 1..31536000', default=None)

    model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="forbid", frozen=True)
