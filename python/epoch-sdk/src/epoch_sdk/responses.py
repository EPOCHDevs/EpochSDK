"""A saved research answer, shared by notebook code, MCP and the agent."""

from __future__ import annotations

import json
from typing import Annotated, Self

from pydantic import Field, model_validator
from stratifyx import AsyncStratifyX
from stratifyx.core.api_error import ApiError

from .contracts import Contract, DomainError, ErrorCode, NonBlank, OutputRequest
from .errors import EpochError
from .output_validation import OutputValue, TableValue, validate_outputs


class ResearchResponseContent(Contract):
    """Complete bounded selected values; never a preview presented as complete."""

    declarations: Annotated[list[OutputRequest], Field(min_length=1)]
    outputs: Annotated[list[OutputValue], Field(min_length=1)]

    @model_validator(mode="after")
    def actual_values(self) -> Self:
        validate_outputs(self.declarations, self.outputs)
        return self


class SavedResearchResponse(Contract):
    """The SDK's validated view of one native Backend response revision."""

    execution_id: NonBlank
    study_id: NonBlank
    version: Annotated[int, Field(ge=1)]
    published_at_ms: Annotated[int, Field(ge=0)]
    content: ResearchResponseContent


def _native_error(error: ApiError, execution_id: str) -> EpochError:
    code: ErrorCode = "TEMPORARILY_UNAVAILABLE"
    if error.status_code == 401:
        code = "UNAUTHENTICATED"
    elif error.status_code == 403:
        code = "FORBIDDEN"
    elif error.status_code == 404:
        code = "NOT_FOUND"
    elif error.status_code == 409:
        code = "INVALID_STATE"
    elif error.status_code == 413:
        code = "FETCH_LIMIT_EXCEEDED"
    elif error.status_code in (400, 422):
        code = "OUTPUT_VALIDATION_FAILED"
    return EpochError(
        DomainError(
            code=code,
            message=f"Saved response API returned HTTP {error.status_code}.",
            retryable=error.status_code is None or error.status_code >= 500,
        ),
        execution_id=execution_id,
    )


async def publish_response(
    backend: AsyncStratifyX,
    execution_id: str,
    content: ResearchResponseContent,
    *,
    expected_version: int = 0,
) -> SavedResearchResponse:
    """Publish the same complete answer from a notebook or an agent.

    Zero expects no previous response. An edit supplies the version read by
    the caller. This method never starts discovery, an agent or an engine job.
    """
    from stratifyx import SdkContractResearchResponseContent

    if not execution_id.strip() or type(expected_version) is not int or expected_version < 0:
        raise ValueError("Provide an execution identity and a nonnegative expected version")
    checked = ResearchResponseContent.model_validate(content.to_wire())
    if any(isinstance(item, TableValue) and len(item.rows) > 10000 for item in checked.outputs):
        raise EpochError(
            DomainError(
                code="FETCH_LIMIT_EXCEEDED",
                message="A response table exceeds 10000 rows.",
                retryable=False,
            ),
            execution_id=execution_id,
        )
    if len(json.dumps(checked.to_wire(), ensure_ascii=False).encode()) > 4 * 1024 * 1024:
        raise EpochError(
            DomainError(
                code="FETCH_LIMIT_EXCEEDED",
                message="The saved response exceeds 4 MiB.",
                retryable=False,
            ),
            execution_id=execution_id,
        )
    try:
        native = await backend.research_responses.save_research_response(
            execution_id,
            expected_version=expected_version,
            content=SdkContractResearchResponseContent.model_validate(checked.to_wire()),
            request_options={"max_retries": 0},
        )
    except ApiError as error:
        raise _native_error(error, execution_id) from error
    result = SavedResearchResponse.model_validate(
        native.model_dump(mode="json", by_alias=True, exclude_unset=True)
    )
    if (
        result.execution_id != execution_id
        or result.version != expected_version + 1
        or result.content != checked
    ):
        raise EpochError(
            DomainError(
                code="INVALID_STATE",
                message="The published response differs from its accepted values or identity.",
                retryable=False,
            ),
            execution_id=execution_id,
        )
    return result


async def read_response(
    backend: AsyncStratifyX,
    execution_id: str,
    *,
    version: int | None = None,
) -> SavedResearchResponse:
    """Read an owner-scoped saved response; optionally pin an earlier revision."""
    if not execution_id.strip() or (
        version is not None and (type(version) is not int or version < 1)
    ):
        raise ValueError("Provide an execution identity and a positive response version")
    try:
        if version is None:
            native = await backend.research_responses.get_research_response(
                execution_id,
                request_options={"max_retries": 0},
            )
        else:
            native = await backend.research_responses.get_research_response(
                execution_id,
                version=version,
                request_options={"max_retries": 0},
            )
    except ApiError as error:
        raise _native_error(error, execution_id) from error
    result = SavedResearchResponse.model_validate(
        native.model_dump(mode="json", by_alias=True, exclude_unset=True)
    )
    if result.execution_id != execution_id or (version is not None and result.version != version):
        raise EpochError(
            DomainError(
                code="INVALID_STATE",
                message="The response API returned another execution or revision.",
                retryable=False,
            ),
            execution_id=execution_id,
        )
    return result
