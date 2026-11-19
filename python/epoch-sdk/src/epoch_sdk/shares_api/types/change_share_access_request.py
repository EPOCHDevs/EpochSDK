# Source-owned Discovery component restored from canonical OpenAPI.
from __future__ import annotations

import typing
import pydantic
from ..core.pydantic_utilities import UniversalBaseModel


class ChangeShareAccessRequest(UniversalBaseModel):
    audience: typing.Optional[typing.Annotated[typing.Literal['anyone_with_link', 'named_subjects'], pydantic.Field(description='Who may open the link. Left out: unchanged')]] = pydantic.Field(description='Who may open the link. Left out: unchanged', default=None)
    subjects: typing.Optional[typing.Annotated[typing.List[str], pydantic.Field(description='The full list of invited email addresses, at most 50; replaces the stored list and is stored lower-cased. Left out: unchanged')]] = pydantic.Field(description='The full list of invited email addresses, at most 50; replaces the stored list and is stored lower-cased. Left out: unchanged', default=None)
    expires_in_seconds: typing.Optional[typing.Annotated[int, pydantic.Field(ge=-9007199254740991, le=9007199254740991, description='From now: 1..31536000, or 0 to clear the expiry. Left out: unchanged')]] = pydantic.Field(strict=True, ge=-9007199254740991, le=9007199254740991, description='From now: 1..31536000, or 0 to clear the expiry. Left out: unchanged', default=None)
    expected_access_version: typing.Annotated[int, pydantic.Field(ge=0, le=9007199254740991, description='The access_version the owner last saw; refused with 409 if access changed since')] = pydantic.Field(strict=True, ge=0, le=9007199254740991, description='The access_version the owner last saw; refused with 409 if access changed since')

    model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="forbid", frozen=True)
