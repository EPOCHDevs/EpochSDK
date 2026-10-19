"""A saved research answer, shared by SDK callers, MCP and the agent."""

from __future__ import annotations

import json
from typing import Annotated, Literal, Self

from pydantic import Field, model_validator
from stratifyx import AsyncStratifyX
from stratifyx.core.api_error import ApiError

from .contracts import (
    Column,
    Contract,
    DomainError,
    ErrorCode,
    NonBlank,
    OutputName,
    OutputRequest,
    TableOutputRequest,
)
from .errors import EpochError
from .output_validation import (
    Cell,
    JsonValueOutput,
    OutputValue,
    TableOrder,
    TableReference,
    TableValue,
    TextValue,
    validate_outputs,
)

type InterpretedOutput = Annotated[JsonValueOutput | TextValue, Field(discriminator="type")]


class ResponsePlanReference(Contract):
    plan_id: Annotated[str, Field(pattern=r"^rpl_[0-9a-f]{64}$")]
    version: Annotated[int, Field(ge=1)]


class ResearchResponseContent(Contract):
    """Answer values or native table references; a preview is never a full table."""

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

    @model_validator(mode="after")
    def table_sources(self) -> Self:
        for value in self.content.outputs:
            if (
                isinstance(value, TableValue)
                and value.source is not None
                and (
                    value.source.execution_id != self.primary_execution_id or self.study_id is None
                )
            ):
                raise ValueError("Referenced tables must use the answer's primary execution")
        return self

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
    order_by: list[TableOrder] = Field(
        default_factory=lambda: list[TableOrder](),
        description="Native field IDs and directions that honor requested ranking or chronology.",
    )


class ResponseTablePage(Contract):
    """One bounded page of a saved answer's table, never an implicit full result."""

    response_id: NonBlank
    version: Annotated[int, Field(ge=1)]
    name: OutputName
    type: Literal["table"]
    columns: list[Column] = Field(alias="schema")
    rows: list[list[Cell]]
    offset: Annotated[int, Field(ge=0)]
    total_rows: Annotated[int, Field(ge=0, le=9007199254740991)]
    next_offset: Annotated[int, Field(ge=0)] | None

    @model_validator(mode="after")
    def actual_page(self) -> Self:
        if len(self.rows) > max(0, self.total_rows - self.offset):
            raise ValueError("Table page exceeds the declared remaining row count")
        end = self.offset + len(self.rows)
        if not self.rows and self.offset < self.total_rows:
            raise ValueError("A nonfinal table page must make progress")
        if self.next_offset != (end if end < self.total_rows else None):
            raise ValueError("Table continuation differs from its returned rows")
        validate_outputs(
            [TableOutputRequest(name=self.name, type="table", schema=self.columns)],
            [TableValue(name=self.name, type="table", schema=self.columns, rows=self.rows)],
        )
        return self


async def _native_page(
    backend: AsyncStratifyX,
    execution_id: str,
    declaration: TableOutputRequest,
    source: ResponseTableSource,
    offset: int,
    page_size: int,
) -> tuple[TableValue, int]:
    from stratifyx import ResearchResponseTableOrder

    from .saved_outputs import decode_saved_table

    if type(offset) is not int or not 0 <= offset <= 9007199254740991:
        raise ValueError("Provide a nonnegative safe row offset")
    if type(page_size) is not int or not 1 <= page_size <= 10000:
        raise ValueError("A transfer page contains between 1 and 10000 rows")
    data = bytearray()
    try:
        async with backend.research_responses.with_raw_response.read_research_response_table(
            execution_id,
            table=source.table,
            field_ids=source.field_ids,
            offset=offset,
            page_size=page_size,
            order_by=[
                ResearchResponseTableOrder(field_id=item.field_id, descending=item.descending)
                for item in source.order_by
            ],
            request_options={"max_retries": 0},
        ) as response:
            headers = {name.lower(): value for name, value in response.headers.items()}
            try:
                total = int(headers["x-arrow-total-rows"])
                returned = int(headers["x-arrow-returned-rows"])
                start = int(headers["x-arrow-row-offset"])
            except (KeyError, ValueError) as error:
                raise EpochError(
                    DomainError(
                        code="OUTPUT_VALIDATION_FAILED",
                        message="Backend did not supply valid table-page metadata.",
                        retryable=False,
                    ),
                    execution_id=execution_id,
                ) from error
            if (
                not 0 <= total <= 9007199254740991
                or start != offset
                or returned < 0
                or returned > min(page_size, max(0, total - offset))
                or (returned == 0 and offset < total)
            ):
                raise EpochError(
                    DomainError(
                        code="OUTPUT_VALIDATION_FAILED",
                        message="Backend table-page metadata is inconsistent.",
                        retryable=False,
                    ),
                    execution_id=execution_id,
                )
            async for chunk in response.data:
                if len(data) + len(chunk) > 4 * 1024 * 1024:
                    raise EpochError(
                        DomainError(
                            code="FETCH_LIMIT_EXCEEDED",
                            message="Request a smaller table page.",
                            retryable=False,
                        ),
                        execution_id=execution_id,
                    )
                data.extend(chunk)
    except ApiError as error:
        raise _native_error(error, execution_id) from error
    try:
        value, _ = decode_saved_table(
            bytes(data),
            declaration,
            source.field_ids,
            execution_id,
            max_rows=page_size,
            max_bytes=4 * 1024 * 1024,
        )
    except (ValueError, TypeError, OSError) as error:
        raise EpochError(
            DomainError(
                code="OUTPUT_VALIDATION_FAILED",
                message="Backend returned an invalid Arrow table page.",
                retryable=False,
            ),
            execution_id=execution_id,
        ) from error
    if value.rows is None or len(value.rows) != returned:
        raise EpochError(
            DomainError(
                code="OUTPUT_VALIDATION_FAILED",
                message="Table-page row count differs from its Arrow data.",
                retryable=False,
            ),
            execution_id=execution_id,
        )
    validate_outputs([declaration], [value], execution_id=execution_id)
    return value, total


async def read_response_table_page(
    backend: AsyncStratifyX,
    response: SavedResearchResponse,
    name: str,
    *,
    offset: int = 0,
    page_size: int = 1000,
) -> ResponseTablePage:
    """Read a pinned table without graph/model work or a whole-table JSON copy."""
    if type(offset) is not int or not 0 <= offset <= 9007199254740991:
        raise ValueError("Provide a nonnegative safe row offset")
    if type(page_size) is not int or not 1 <= page_size <= 10000:
        raise ValueError("A transfer page contains between 1 and 10000 rows")
    value = next((part for part in response.content.outputs if part.name == name), None)
    declaration = next((part for part in response.content.declarations if part.name == name), None)
    if not isinstance(value, TableValue) or not isinstance(declaration, TableOutputRequest):
        raise EpochError(
            DomainError(
                code="INVALID_REQUEST",
                message="Choose a declared table in this saved answer.",
                retryable=False,
            )
        )
    if value.source is None:
        assert value.rows is not None
        total = len(value.rows)
        table = TableValue(
            name=name,
            type="table",
            schema=value.columns,
            rows=value.rows[offset : offset + page_size],
        )
    else:
        source = value.source
        table, total = await _native_page(
            backend,
            source.execution_id,
            declaration,
            ResponseTableSource(
                name=name, table=source.table, field_ids=source.field_ids, order_by=source.order_by
            ),
            offset,
            page_size,
        )
        if total != source.row_count:
            raise EpochError(
                DomainError(
                    code="INVALID_STATE",
                    message="The saved table's row count changed.",
                    retryable=False,
                ),
                execution_id=source.execution_id,
            )
    assert table.rows is not None
    end = offset + len(table.rows)
    result = ResponseTablePage(
        response_id=response.response_id,
        version=response.version,
        name=table.name,
        type="table",
        schema=table.columns,
        rows=table.rows,
        offset=offset,
        total_rows=total,
        next_offset=end if end < total else None,
    )
    if len(result.model_dump_json(by_alias=True, exclude_unset=True).encode()) > 4 * 1024 * 1024:
        raise EpochError(
            DomainError(
                code="FETCH_LIMIT_EXCEEDED",
                message="Request a smaller table page.",
                retryable=False,
            ),
            execution_id=response.primary_execution_id,
        )
    return result


async def assemble_response(
    backend: AsyncStratifyX,
    execution_id: str | None,
    study_id: str | None,
    declarations: list[OutputRequest],
    interpreted: list[InterpretedOutput],
    *,
    table_sources: list[ResponseTableSource] | None = None,
) -> ResearchResponseContent:
    """Bind native relations without requiring dashboard exhibits or copying all rows.

    A caller identifies exact DESCRIBE relations and fields. A one-row native
    probe checks the schema and returns the total row count. Backend validates
    the complete projection when it saves the answer; clients then page through
    the referenced table. JSON/text interpretations use evidence read by the
    caller. No study execution is started.
    """
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
    for declaration in tables:
        assert execution_id is not None
        source = next(item for item in sources if item.name == declaration.name)
        _, total = await _native_page(backend, execution_id, declaration, source, 0, 1)
        reference = TableReference(
            execution_id=execution_id,
            table=source.table,
            field_ids=source.field_ids,
            row_count=total,
        )
        if source.order_by:
            reference.order_by = source.order_by
        values.append(
            TableValue(
                name=declaration.name, type="table", schema=declaration.columns, source=reference
            )
        )
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
