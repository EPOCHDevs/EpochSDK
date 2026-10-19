"""Versioned response recipes; research establishes them, Backend replays them.

These are language-neutral wire definitions. Native APIs own saved query
receipts, plans and executions. A deployment selects recorded computations;
it never asks a supervisor to author SQL or transcribe a table.
"""
from __future__ import annotations

from typing import Annotated, Literal, Self

from pydantic import Field, model_validator

from .contracts import Contract, DomainError, NonBlank, OutputName, OutputRequest, RunParameters
from .responses import ResponsePlanReference, ResponseReference, ResponseTableSource


class RecordedSqlPlanQuery(Contract):
    kind: Literal["recorded_sql"]
    name: OutputName
    # Minted by Backend only after the exact SQL successfully executes.
    query_ref: Annotated[str, Field(pattern=r"^rqr_[0-9a-f]{64}$")]


class NativeRelationPlanQuery(ResponseTableSource):
    kind: Literal["relation"]
    name: OutputName


type ResponsePlanQuery = Annotated[
    RecordedSqlPlanQuery | NativeRelationPlanQuery, Field(discriminator="kind")
]


class PlanQueryField(Contract):
    field_id: NonBlank
    encoding: Literal["native", "date", "datetime", "decimal_string"] = "native"


class PlanCellBinding(Contract):
    kind: Literal["cell"]
    query: OutputName
    field: PlanQueryField
    # Omission requires exactly one row; zero rows never invent a default value.
    row_index: Annotated[int, Field(ge=0)] | None = None


class PlanRowBinding(Contract):
    kind: Literal["row"]
    query: OutputName
    # Names are requested JSON properties; columns are Backend query identities.
    fields: Annotated[dict[str, PlanQueryField], Field(min_length=1)]


class PlanRowsBinding(Contract):
    kind: Literal["rows"]
    query: OutputName
    fields: Annotated[dict[str, PlanQueryField], Field(min_length=1)]


class PlanColumnBinding(Contract):
    kind: Literal["column_array"]
    query: OutputName
    field: PlanQueryField


class PlanParameterBinding(Contract):
    kind: Literal["parameter"]
    # JSON Pointer into this execution's native period/execution parameters.
    pointer: Annotated[str, Field(pattern=r"^(/([^~/]|~[01])*)+$")]


class PlanSchemaConstantBinding(Contract):
    kind: Literal["schema_constant"]
    # Read this property's const from the accepted output JSON Schema. The
    # model cannot insert an arbitrary literal financial value into a recipe.


class PlanObjectBinding(Contract):
    kind: Literal["object"]
    # Keys belong to the user's JSON schema, not a fixed SDK business model.
    fields: Annotated[dict[str, PlanJsonBinding], Field(min_length=1)]


type PlanJsonBinding = Annotated[
    PlanCellBinding | PlanRowBinding | PlanRowsBinding | PlanColumnBinding
    | PlanParameterBinding | PlanSchemaConstantBinding | PlanObjectBinding,
    Field(discriminator="kind"),
]


class PlanTableProjection(Contract):
    query: OutputName
    field_ids: Annotated[list[NonBlank], Field(min_length=1)]


class PlanTableOutput(Contract):
    name: OutputName
    type: Literal["table"]
    # Concatenate complete projections in this explicit order. No implicit joins.
    projections: Annotated[list[PlanTableProjection], Field(min_length=1)]


class PlanJsonOutput(Contract):
    name: OutputName
    type: Literal["json"]
    value: PlanJsonBinding


class PlanTextOutput(Contract):
    name: OutputName
    type: Literal["text"]
    # Versioned server-owned model/settings policy; never a caller endpoint/key.
    model_policy: NonBlank
    instructions: NonBlank
    # Named facts deliberately selected from the newly computed query results.
    inputs: Annotated[dict[str, PlanJsonBinding], Field(min_length=1)]


type ResponsePlanOutput = Annotated[
    PlanTableOutput | PlanJsonOutput | PlanTextOutput, Field(discriminator="type")
]


def _query_references(binding: PlanJsonBinding) -> list[str]:
    if isinstance(binding, PlanObjectBinding):
        return [query for child in binding.fields.values() for query in _query_references(child)]
    if isinstance(binding, (PlanCellBinding, PlanRowBinding, PlanRowsBinding, PlanColumnBinding)):
        return [binding.query]
    return []


def _has_schema_constant(binding: PlanJsonBinding) -> bool:
    if isinstance(binding, PlanObjectBinding):
        return any(_has_schema_constant(child) for child in binding.fields.values())
    return isinstance(binding, PlanSchemaConstantBinding)


class ResponsePlanDraft(Contract):
    format_version: Literal[1]
    queries: Annotated[list[ResponsePlanQuery], Field(min_length=1)]
    outputs: Annotated[list[ResponsePlanOutput], Field(min_length=1)]

    @model_validator(mode="after")
    def exact_references(self) -> Self:
        names = [query.name for query in self.queries]
        if len(set(names)) != len(names):
            raise ValueError("Plan query names must be unique")
        if len({output.name for output in self.outputs}) != len(self.outputs):
            raise ValueError("Plan output names must be unique")
        used: list[str] = []
        for output in self.outputs:
            if isinstance(output, PlanTableOutput):
                used.extend(projection.query for projection in output.projections)
            elif isinstance(output, PlanJsonOutput):
                used.extend(_query_references(output.value))
            else:
                for binding in output.inputs.values():
                    if _has_schema_constant(binding):
                        raise ValueError("Text inputs have no output JSON Schema constant to read")
                    used.extend(_query_references(binding))
        if not set(used) <= set(names):
            raise ValueError("Every mapping must reference an exact named plan query")
        return self


class ResponsePlanDefinition(ResponsePlanDraft):
    study_id: NonBlank
    declarations: Annotated[list[OutputRequest], Field(min_length=1)]
    captured_parameters: RunParameters
    # Execution options remain frozen. A period override is explicit opt-in;
    # the author must establish that its study/queries support that variation.
    allow_period_override: bool = False

    @model_validator(mode="after")
    def declared_outputs(self) -> Self:
        expected = [(item.name, item.type) for item in self.declarations]
        actual = [(item.name, item.type) for item in self.outputs]
        if expected != actual:
            raise ValueError("The plan must preserve every accepted named output in order")
        for declaration, output in zip(self.declarations, self.outputs, strict=True):
            if (declaration.type == "table" and isinstance(output, PlanTableOutput)
                    and any(len(part.field_ids) != len(declaration.columns)
                            for part in output.projections)):
                raise ValueError("Every table projection must map each declared column")
        return self


class ResolvedTextSettings(Contract):
    """Effective non-secret model settings captured by the owning AI service."""
    model_policy: NonBlank
    model_id: NonBlank
    prompt_version: NonBlank
    max_output_tokens: Annotated[int, Field(ge=1)]
    temperature: Annotated[float, Field(ge=0, le=2)] | None = None
    reasoning_effort: Literal["none", "low", "medium", "high", "xhigh", "max"] | None = None


class SavedResponsePlan(ResponsePlanReference):
    request_id: NonBlank
    thread_id: NonBlank
    source_execution_id: NonBlank
    created_at_ms: Annotated[int, Field(ge=0)]
    phase: Literal["accepted", "active", "outputs_recorded", "failed"]
    definition: ResponsePlanDefinition
    # Keys are declared text-output names. Provider credentials are never saved.
    text_settings: dict[str, ResolvedTextSettings] = Field(default_factory=dict)
    verified_response: ResponseReference | None = None
    error: DomainError | None = None

    @model_validator(mode="after")
    def verified_source(self) -> Self:
        if self.phase == "outputs_recorded":
            expected = {output.name for output in self.definition.outputs
                        if isinstance(output, PlanTextOutput)}
            if set(self.text_settings) != expected:
                raise ValueError("A published plan must retain each declared text step's settings")
            for output in self.definition.outputs:
                if (isinstance(output, PlanTextOutput)
                        and self.text_settings[output.name].model_policy != output.model_policy):
                    raise ValueError("Text settings must belong to the declared model policy")
            response = self.verified_response
            if (response is None or response.request_id != self.request_id
                    or response.thread_id != self.thread_id
                    or response.primary_execution_id != self.source_execution_id
                    or response.study_id != self.definition.study_id):
                raise ValueError("A verified plan must retain its exact original answer/source")
        elif self.verified_response is not None:
            raise ValueError("Only a fully published plan has a verified answer")
        if (self.phase == "failed") != (self.error is not None):
            raise ValueError("Only a failed plan retains a terminal error")
        return self
