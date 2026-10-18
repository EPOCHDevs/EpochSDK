"""A saved research answer, shared by notebook code, MCP and the agent."""

from __future__ import annotations

import json
from typing import Annotated, Self

from pydantic import Field, model_validator
from stratifyx import AsyncStratifyX
from stratifyx.core.api_error import ApiError

from .contracts import (
    Contract,
    DomainError,
    ErrorCode,
    NonBlank,
    OutputRequest,
    TableOutputRequest,
)
from .errors import EpochError
from .output_validation import (
    JsonValueOutput,
    OutputValue,
    TableValue,
    TextValue,
    validate_outputs,
)

type InterpretedOutput = Annotated[JsonValueOutput | TextValue, Field(discriminator="type")]


class ResearchResponseContent(Contract):
    """Complete bounded selected values; never a preview presented as complete."""

    declarations: Annotated[list[OutputRequest], Field(min_length=1)]
    outputs: Annotated[list[OutputValue], Field(min_length=1)]

    @model_validator(mode="after")
    def actual_values(self) -> Self:
        validate_outputs(self.declarations, self.outputs)
        return self


class ResponseReference(Contract):
    """One published answer for a query, independent of its source execution."""

    response_id: NonBlank
    request_id: NonBlank
    thread_id: NonBlank
    version: Annotated[int, Field(ge=1)]
    primary_execution_id: NonBlank | None = None
    study_id: NonBlank | None = None

    @model_validator(mode="after")
    def paired_source(self) -> Self:
        if (self.primary_execution_id is None) != (self.study_id is None):
            raise ValueError("An execution-backed answer requires both execution and study")
        return self


class SavedResearchResponse(ResponseReference):
    """A Backend-owned answer revision. One query can have many named parts."""

    published_at_ms: Annotated[int, Field(ge=0)]
    content: ResearchResponseContent

    def reference(self) -> ResponseReference:
        return ResponseReference.model_validate(
            {
                key: value
                for key, value in self.to_wire().items()
                if key not in {"published_at_ms", "content"}
            }
        )


class ResponseTableSource(Contract):
    """Exact persisted relation/fields from native DESCRIBE; never SQL or rows."""

    name: NonBlank
    table: NonBlank
    field_ids: Annotated[list[NonBlank], Field(min_length=1)]


async def assemble_response(
    backend: AsyncStratifyX,
    execution_id: str | None,
    study_id: str | None,
    declarations: list[OutputRequest],
    interpreted: list[InterpretedOutput],
    *,
    table_sources: list[ResponseTableSource] | None = None,
) -> ResearchResponseContent:
    """Read complete native relations without requiring dashboard exhibits.

    A caller identifies exact DESCRIBE relations and fields. Backend reads the
    complete bounded projection, independently of dashboard layout. JSON/text
    interpretations use evidence read by the caller. No engine work is started.
    """
    from .saved_outputs import TableBinding, decode_saved_table

    non_tables: list[OutputRequest] = [
        item for item in declarations if not isinstance(item, TableOutputRequest)
    ]
    values: list[OutputValue] = validate_outputs(non_tables, list(interpreted))
    tables = [item for item in declarations if isinstance(item, TableOutputRequest)]
    sources = table_sources or []
    if len({item.name for item in sources}) != len(sources) or {item.name for item in sources} != {
        item.name for item in tables
    }:
        raise ValueError("Provide exactly one native table source per requested table")
    if tables and (not execution_id or not study_id):
        raise ValueError("Native response tables require a selected execution and study")
    expanded_bytes = 0
    transferred_bytes = 0
    for declaration in tables:
        assert execution_id is not None
        source = next(item for item in sources if item.name == declaration.name)
        data = bytearray()
        async with backend.research_responses.with_raw_response.read_research_response_table(
            execution_id,
            table=source.table,
            field_ids=source.field_ids,
            request_options={"max_retries": 0},
        ) as response:
            async for chunk in response.data:
                transferred_bytes += len(chunk)
                if transferred_bytes > 4 * 1024 * 1024:
                    raise EpochError(
                        DomainError(
                            code="FETCH_LIMIT_EXCEEDED",
                            message="Complete response tables exceed 4 MiB.",
                            retryable=False,
                        ),
                        execution_id=execution_id,
                    )
                data.extend(chunk)
        binding = TableBinding(
            name=declaration.name,
            type="table",
            category="response",
            table_index=0,
            field_ids=source.field_ids,
        )
        value, expanded = decode_saved_table(
            bytes(data),
            declaration,
            binding,
            execution_id,
            max_rows=10000,
            max_bytes=4 * 1024 * 1024 - expanded_bytes,
        )
        expanded_bytes += expanded
        values.append(value)
    by_name = {value.name: value for value in values}
    return ResearchResponseContent(
        declarations=declarations,
        outputs=[by_name[item.name] for item in declarations],
    )


def _native_error(error: ApiError, execution_id: str | None) -> EpochError:
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
    request_id: str,
    content: ResearchResponseContent,
    *,
    thread_id: str,
    primary_execution_id: str | None = None,
    expected_version: int = 0,
) -> SavedResearchResponse:
    """Publish one query's answer; different queries may reuse one execution.

    Zero creates this query's answer. An edit names its original query/thread
    and expected revision. Existing completed requests retain their pinned read.
    """
    from stratifyx import SdkContractResearchResponseContent

    if (
        not request_id.strip()
        or not thread_id.strip()
        or type(expected_version) is not int
        or expected_version < 0
    ):
        raise ValueError("Provide query/thread identities and a nonnegative response version")
    checked = ResearchResponseContent.model_validate(content.to_wire())
    if any(isinstance(item, TableValue) and len(item.rows) > 10000 for item in checked.outputs):
        raise EpochError(
            DomainError(
                code="FETCH_LIMIT_EXCEEDED",
                message="A response table exceeds 10000 rows.",
                retryable=False,
            ),
            execution_id=primary_execution_id,
        )
    if len(json.dumps(checked.to_wire(), ensure_ascii=False).encode()) > 4 * 1024 * 1024:
        raise EpochError(
            DomainError(
                code="FETCH_LIMIT_EXCEEDED",
                message="The saved response exceeds 4 MiB.",
                retryable=False,
            ),
            execution_id=primary_execution_id,
        )
    try:
        native_content = SdkContractResearchResponseContent.model_validate(checked.to_wire())
        if primary_execution_id is None:
            native = await backend.research_responses.save_research_response(
                request_id,
                thread_id=thread_id,
                expected_version=expected_version,
                content=native_content,
                request_options={"max_retries": 0},
            )
        else:
            native = await backend.research_responses.save_research_response(
                request_id,
                thread_id=thread_id,
                primary_execution_id=primary_execution_id,
                expected_version=expected_version,
                content=native_content,
                request_options={"max_retries": 0},
            )
    except ApiError as error:
        raise _native_error(error, primary_execution_id) from error
    result = SavedResearchResponse.model_validate(
        native.model_dump(mode="json", by_alias=True, exclude_unset=True)
    )
    if (
        result.request_id != request_id
        or result.thread_id != thread_id
        or result.primary_execution_id != primary_execution_id
        or result.version != expected_version + 1
        or result.content != checked
    ):
        raise EpochError(
            DomainError(
                code="INVALID_STATE",
                message="The published answer differs from its query, source or accepted values.",
                retryable=False,
            ),
            execution_id=primary_execution_id,
        )
    return result


async def read_response(
    backend: AsyncStratifyX,
    response_id: str,
    *,
    version: int | None = None,
) -> SavedResearchResponse:
    """Read a saved answer by answer identity, optionally pinning its revision."""
    if not response_id.strip() or (
        version is not None and (type(version) is not int or version < 1)
    ):
        raise ValueError("Provide an answer identity and a positive response version")
    try:
        if version is None:
            native = await backend.research_responses.get_research_response(
                response_id,
                request_options={"max_retries": 0},
            )
        else:
            native = await backend.research_responses.get_research_response(
                response_id,
                version=version,
                request_options={"max_retries": 0},
            )
    except ApiError as error:
        raise _native_error(error, None) from error
    result = SavedResearchResponse.model_validate(
        native.model_dump(mode="json", by_alias=True, exclude_unset=True)
    )
    if result.response_id != response_id or (version is not None and result.version != version):
        raise EpochError(
            DomainError(
                code="INVALID_STATE",
                message="The response API returned another answer or revision.",
                retryable=False,
            )
        )
    return result
