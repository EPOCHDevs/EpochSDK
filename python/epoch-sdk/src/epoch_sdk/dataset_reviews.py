"""Closed SDK projection of EpochAI presentation/dataset_reviews.py.

The projection is checked against the source-owned exported schema. Backend
models and exact draft identities are imported from the versioned native SDK.
"""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, model_validator
from stratifyx.types import DatasetBuild, DatasetBuildRequest, DatasetPreviewPage


class Closed(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)


class DatasetConfigureInterrupt(Closed):
    type: Literal["dataset_review"] = "dataset_review"
    stage: Literal["configure"] = "configure"
    tool_call_id: str = Field(min_length=1)
    proposal_ref: str = Field(pattern=r"^proposal:[a-f0-9]{64}$")
    preparation_ref: str = Field(pattern=r"^preparation:[a-f0-9]{64}$")
    request: DatasetBuildRequest


class DatasetResultInterrupt(Closed):
    type: Literal["dataset_review"] = "dataset_review"
    stage: Literal["review"] = "review"
    tool_call_id: str = Field(min_length=1)
    operation: DatasetBuild
    preview: DatasetPreviewPage | None = None
    can_edit: bool = False


class DatasetConfigureResponse(Closed):
    type: Literal["dataset_review"] = "dataset_review"
    stage: Literal["configure"] = "configure"
    proposal_ref: str = Field(pattern=r"^proposal:[a-f0-9]{64}$")
    action: Literal["build_preview", "cancel"]
    request: DatasetBuildRequest | None = None

    @model_validator(mode="after")
    def exact_action(self) -> DatasetConfigureResponse:
        if (self.action == "build_preview") != (self.request is not None):
            raise ValueError(
                "Build preview requires the reviewed request; Cancel carries no request"
            )
        return self


class DatasetResultResponse(Closed):
    type: Literal["dataset_review"] = "dataset_review"
    stage: Literal["review"] = "review"
    preparation_ref: str = Field(pattern=r"^preparation:[a-f0-9]{64}$")
    attempt: int = Field(ge=1)
    review_ref: str = Field(pattern=r"^review:[a-f0-9]{64}$")
    result_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    schema_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    action: Literal["save", "save_available", "decline", "edit", "continue"]
    request: DatasetBuildRequest | None = None

    @model_validator(mode="after")
    def exact_action(self) -> DatasetResultResponse:
        if (self.action == "edit") != (self.request is not None):
            raise ValueError("Only Build preview after Edit carries a replacement request")
        return self


type DatasetWorkflowInterrupt = Annotated[
    DatasetConfigureInterrupt | DatasetResultInterrupt, Field(discriminator="stage")
]
type DatasetWorkflowResponse = Annotated[
    DatasetConfigureResponse | DatasetResultResponse, Field(discriminator="stage")
]
# Pydantic accepts these aliases at runtime; Pyright 1.1.408 does not yet
# recognize the Annotated discriminator as a TypeForm. Preserve exact results.
interrupt_adapter: TypeAdapter[DatasetWorkflowInterrupt] = TypeAdapter(DatasetWorkflowInterrupt)  # pyright: ignore[reportArgumentType]
response_adapter: TypeAdapter[DatasetWorkflowResponse] = TypeAdapter(DatasetWorkflowResponse)  # pyright: ignore[reportArgumentType]


class DatasetWorkflowProgress(Closed):
    tool_call_id: str
    stage: Literal["preparing", "saved", "not_saved", "not_started"]
    operation: DatasetBuild | None = None
    message: str


class DatasetWorkflowOutcome(Closed):
    status: Literal["saved", "not_saved", "not_started"]
    operation: DatasetBuild | None = None
    message: str


def dataset_response(
    payload: DatasetWorkflowInterrupt,
    action: Literal[
        "build_preview", "cancel", "save", "save_available", "decline", "edit", "continue"
    ],
    request: DatasetBuildRequest | None = None,
) -> DatasetConfigureResponse | DatasetResultResponse:
    """Join an explicit human choice to the displayed source-owned identity."""
    if isinstance(payload, DatasetConfigureInterrupt):
        if action not in ("build_preview", "cancel"):
            raise ValueError("Choose Build preview or Cancel for this configuration")
        return DatasetConfigureResponse(
            proposal_ref=payload.proposal_ref, action=action, request=request
        )
    if action in ("build_preview", "cancel"):
        raise ValueError("Choose a result-review action")
    operation = payload.operation
    if operation.review is None or operation.result_sha256 is None:
        raise ValueError("This operation has no confirmed result review identity")
    return DatasetResultResponse(
        preparation_ref=operation.preparation_ref,
        attempt=operation.attempt,
        review_ref=operation.review.review_ref,
        result_sha256=operation.result_sha256,
        schema_sha256=operation.review.schema_sha256,
        action=action,
        request=request,
    )
