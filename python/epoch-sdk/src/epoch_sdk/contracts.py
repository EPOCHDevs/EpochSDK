"""The core wire contract shared by the SDK, dedicated graphs and MCP adapters."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Annotated, Literal, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    GetJsonSchemaHandler,
    JsonValue,
    RootModel,
    StringConstraints,
    field_validator,
    model_validator,
)
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema

from .json_schema import JsonSchemaDocument, validate_schema
from .native_parameters import NativeExecutionOptions, NativePeriod

NonBlank = Annotated[str, StringConstraints(min_length=1, pattern=r"\S")]
OutputName = Annotated[str, StringConstraints(pattern=r"^[A-Za-z][A-Za-z0-9_]*$", max_length=100)]
ExecutionId = Annotated[str, StringConstraints(min_length=1, pattern=r"\S")]


class Contract(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, allow_inf_nan=False)

    @model_validator(mode="before")
    @classmethod
    def omit_optional_fields_instead_of_null(cls, value: object) -> object:
        original = value
        if isinstance(value, Mapping):
            for name, field in cls.model_fields.items():
                key = field.alias or name
                if not field.is_required() and key in value and value[key] is None:
                    raise ValueError(f"Omit '{key}' instead of supplying null")
        return original

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        result = handler(schema)
        # Optional metadata is omitted rather than null. Required nullable
        # values, such as a page's terminal continuation, keep their null type.
        required = set(result.get("required", []))
        for name, value in result.get("properties", {}).items():
            if name in required:
                continue
            alternatives = value.get("anyOf", [])
            non_null = [item for item in alternatives if item != {"type": "null"}]
            if alternatives and len(non_null) != len(alternatives):
                value.pop("anyOf")
                value.pop("default", None)
                if len(non_null) == 1:
                    value.update(non_null[0])
                else:
                    value["anyOf"] = non_null
        return result

    def to_wire(self) -> dict[str, JsonValue]:
        # A serialization boundary only. Shapes stay closed in all model fields.
        return self.model_dump(mode="json", by_alias=True, exclude_unset=True)


class Column(Contract):
    name: NonBlank
    type: Literal["string", "int64", "float64", "boolean", "date", "datetime"]
    description: str | None = Field(
        default=None, description="Field meaning and calculation/time basis."
    )
    unit: str | None = None
    nullable: bool = False


class NamedOutput(Contract):
    name: OutputName
    description: str | None = None


class TableOutputRequest(NamedOutput):
    type: Literal["table"]
    columns: Annotated[list[Column], Field(min_length=1)] = Field(alias="schema")

    @field_validator("columns")
    @classmethod
    def unique_columns(cls, columns: list[Column]) -> list[Column]:
        names = [column.name for column in columns]
        if len(names) != len(set(names)):
            raise ValueError("Table column names must be unique")
        return columns


class JsonOutputRequest(NamedOutput):
    type: Literal["json"]
    json_schema: JsonSchemaDocument = Field(alias="schema")

    @field_validator("json_schema")
    @classmethod
    def valid_json_schema(cls, value: JsonSchemaDocument) -> JsonSchemaDocument:
        return validate_schema(value)


class TextOutputRequest(NamedOutput):
    type: Literal["text"]
    instructions: NonBlank
    format: Literal["plain", "markdown"] = "plain"


OutputRequest = Annotated[
    TableOutputRequest | JsonOutputRequest | TextOutputRequest, Field(discriminator="type")
]


def _unique_outputs(outputs: list[OutputRequest]) -> list[OutputRequest]:
    names = [output.name for output in outputs]
    if len(names) != len(set(names)):
        raise ValueError("Output names must be unique")
    return outputs


class RunParameters(Contract):
    """Only the closed parameter types supported by native Backend execution."""

    period: NativePeriod | None = None
    execution: NativeExecutionOptions | None = None

    @model_validator(mode="after")
    def period_order(self) -> Self:
        if (
            self.period
            and self.period.start
            and self.period.end
            and self.period.start > self.period.end
        ):
            raise ValueError("period.start must not follow period.end")
        return self


class RunRequest(Contract):
    model_config = ConfigDict(
        json_schema_extra={"not": {"required": ["study_id", "source_execution_id"]}}
    )
    task: NonBlank
    context: list[NonBlank] = Field(default_factory=list)
    outputs: Annotated[list[OutputRequest], Field(min_length=1)]
    auto_ingest: bool = False
    study_id: NonBlank | None = Field(
        default=None, description="Execute this exact authorized study."
    )
    source_execution_id: ExecutionId | None = Field(
        default=None, description="Resolve the exact study from this authorized Backend execution."
    )
    parameters: RunParameters | None = Field(
        default=None,
        description="Supported native overrides; resolve defaults before freezing the binding.",
    )

    _outputs_unique = field_validator("outputs")(_unique_outputs)

    @model_validator(mode="after")
    def one_reference(self) -> Self:
        if self.study_id is not None and self.source_execution_id is not None:
            raise ValueError("Choose study_id or source_execution_id, not both")
        return self


def _ingest_schema(schema: JsonSchemaValue) -> None:
    outputs = schema["properties"]["outputs"]
    table_ref = outputs["items"]["discriminator"]["mapping"]["table"]
    outputs.update(contains={"$ref": table_ref}, minContains=1)


class IngestRequest(Contract):
    model_config = ConfigDict(json_schema_extra=_ingest_schema)
    task: NonBlank
    context: list[NonBlank] = Field(default_factory=list)
    outputs: Annotated[list[OutputRequest], Field(min_length=1)]

    _outputs_unique = field_validator("outputs")(_unique_outputs)

    @model_validator(mode="after")
    def reusable_table(self) -> Self:
        if not any(isinstance(output, TableOutputRequest) for output in self.outputs):
            raise ValueError("Ingestion requires at least one reusable table output")
        return self


class FreshFetchRequest(Contract):
    task: NonBlank
    context: list[NonBlank] = Field(default_factory=list)
    outputs: Annotated[list[OutputRequest], Field(min_length=1)] | None = None
    page_size: Annotated[int, Field(ge=1, le=1000)] = 100

    @field_validator("outputs")
    @classmethod
    def unique_requested_outputs(
        cls, value: list[OutputRequest] | None
    ) -> list[OutputRequest] | None:
        return _unique_outputs(value) if value is not None else None


class FetchPageRequest(Contract):
    cursor: NonBlank


type FetchRequest = FreshFetchRequest | FetchPageRequest


class _FetchEnvelope(RootModel[FetchRequest]):
    pass


def parse_fetch(value: object) -> FetchRequest:
    return _FetchEnvelope.model_validate(value).root


class RefreshRequest(Contract):
    context: list[NonBlank] = Field(default_factory=list)
    auto_ingest: bool = False
    parameters: RunParameters | None = None


class Gap(Contract):
    description: NonBlank
    field: str | None = None


class Question(Contract):
    model_config = ConfigDict(
        json_schema_extra={"dependentRequired": {"recommended_option": ["options"]}}
    )
    question: NonBlank
    options: Annotated[list[NonBlank], Field(min_length=1)] | None = None
    recommended_option: NonBlank | None = None

    @model_validator(mode="after")
    def suggestion_is_an_option(self) -> Self:
        if self.recommended_option is not None and (
            self.options is None or self.recommended_option not in self.options
        ):
            raise ValueError("recommended_option must be one of options")
        return self


class DataRequirement(Contract):
    description: NonBlank
    required_coverage: str | None = None
    suggested_resolution: str | None = None


class AccessRequirement(Contract):
    source: NonBlank
    permission: NonBlank
    suggested_resolution: str | None = None


type ErrorCode = Literal[
    "INVALID_REQUEST",
    "UNAUTHENTICATED",
    "FORBIDDEN",
    "NOT_FOUND",
    "CLARIFICATION_REQUIRED",
    "DATA_REQUIRED",
    "ACCESS_REQUIRED",
    "OUTPUT_VALIDATION_FAILED",
    "EXECUTION_FAILED",
    "EXECUTION_NOT_READY",
    "INVALID_STATE",
    "IDEMPOTENCY_CONFLICT",
    "EVENT_CURSOR_EXPIRED",
    "FETCH_CURSOR_EXPIRED",
    "FETCH_LIMIT_EXCEEDED",
    "RATE_LIMITED",
    "TEMPORARILY_UNAVAILABLE",
    "UPSTREAM_TIMEOUT",
]


class DomainError(Contract):
    model_config = ConfigDict(
        json_schema_extra={
            "allOf": [
                {
                    "if": {
                        "properties": {"code": {"const": "CLARIFICATION_REQUIRED"}},
                        "required": ["code"],
                    },
                    "then": {
                        "required": ["gaps", "questions", "recommended_task"],
                        "properties": {"retryable": {"const": False}},
                    },
                },
                {
                    "if": {
                        "properties": {"code": {"const": "DATA_REQUIRED"}},
                        "required": ["code"],
                    },
                    "then": {"required": ["data_requirements"]},
                },
                {
                    "if": {
                        "properties": {"code": {"const": "ACCESS_REQUIRED"}},
                        "required": ["code"],
                    },
                    "then": {"required": ["access_requirements"]},
                },
            ]
        }
    )
    code: ErrorCode
    message: NonBlank
    retryable: bool
    gaps: Annotated[list[Gap], Field(min_length=1)] | None = None
    questions: Annotated[list[Question], Field(min_length=1)] | None = None
    recommended_task: NonBlank | None = None
    data_requirements: Annotated[list[DataRequirement], Field(min_length=1)] | None = None
    access_requirements: Annotated[list[AccessRequirement], Field(min_length=1)] | None = None

    @model_validator(mode="after")
    def required_guidance(self) -> Self:
        if self.code == "CLARIFICATION_REQUIRED" and (
            self.retryable or not (self.gaps and self.questions and self.recommended_task)
        ):
            raise ValueError(
                "Clarification must be terminal with gaps, questions and recommended_task"
            )
        if self.code == "DATA_REQUIRED" and not self.data_requirements:
            raise ValueError("DATA_REQUIRED needs data_requirements")
        if self.code == "ACCESS_REQUIRED" and not self.access_requirements:
            raise ValueError("ACCESS_REQUIRED needs access_requirements")
        return self


class ErrorResponse(Contract):
    error: DomainError
    execution_id: ExecutionId | None = Field(
        default=None,
        description="Existing/accepted execution this failure refers to; a failed fetch does not change its source status.",
    )


class Acknowledgement(Contract):
    execution_id: ExecutionId
    status: Literal["queued"]
