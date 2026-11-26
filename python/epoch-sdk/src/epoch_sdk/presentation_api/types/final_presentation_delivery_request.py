# Source-owned Discovery component restored from canonical OpenAPI.
from __future__ import annotations

import typing
import pydantic
from ..core.pydantic_utilities import UniversalBaseModel
from .final_presentation_reference import FinalPresentationReference
from .final_presentation_source import FinalPresentationSource


class FinalPresentationDeliveryRequest(UniversalBaseModel):
    execution_category: typing.Annotated[str, pydantic.Field(min_length=1, max_length=256)]
    expected_source: typing.Optional[FinalPresentationSource] = pydantic.Field(default=None)
    retained_reference: typing.Optional[FinalPresentationReference] = pydantic.Field(default=None)
    max_expires_epoch: typing.Optional[typing.Annotated[int, pydantic.Field(ge=0, le=9007199254740991)]] = pydantic.Field(strict=True, ge=0, le=9007199254740991, default=None)

    model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="forbid", frozen=True)

    @pydantic.model_validator(mode="after")
    def _validate_platform_source_request(self):
        from ..core.platform_request_schema import validate_request
        validate_request('FinalPresentationDeliveryRequest', self.model_dump(mode="json", by_alias=True, exclude_unset=True))
        return self
