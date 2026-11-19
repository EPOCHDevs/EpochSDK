# Source-owned Discovery component restored from canonical OpenAPI.
from __future__ import annotations

import typing
import pydantic
from ..core.pydantic_utilities import UniversalBaseModel
from .dataset_review_decision import DatasetReviewDecision


class DatasetReviewRequest(UniversalBaseModel):
    decisions: typing.List[DatasetReviewDecision]

    model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="forbid", frozen=True)
