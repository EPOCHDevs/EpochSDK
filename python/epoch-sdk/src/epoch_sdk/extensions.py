"""One native saved-execution lifecycle shared by application and MCP clients.

Backend owns compilation, authorization, immutable inputs, idempotent operations
and publication. These methods never launch an EpochAI graph, interpret prose,
choose a model or copy table values. Direct input programs reuse a completed
study; report_template replay runs its original study and saved report natively.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TypedDict

from stratifyx import AsyncStratifyX
from stratifyx.types import (
    CreateSdkExecutionRequest,
    DashboardEditView,
    DataOption,
    ExecutionInputCatalogResponse,
    ExecutionInputSelection,
    ExecutionParameterValue,
    ExecutionPresentationPin,
    ExecutionReportReference,
    IdResponse,
    NamedExecutionInputSelection,
    SdkExecutionRecord,
    StudyType,
)

from .responses import (
    ResponseTablePage,
    SavedResearchResponse,
    read_response,
    read_response_table_page,
)


class _DefinitionOptions(TypedDict, total=False):
    parent_definition_id: str


class _ExecutionOptions(TypedDict, total=False):
    thread_id: str
    execution_parameter_bindings: dict[str, ExecutionParameterValue]
    base_presentation: ExecutionPresentationPin
    research_request_id: str
    allow_period_override: bool
    report_template: ExecutionReportReference
    additional_sources: list[NamedExecutionInputSelection]


class ExecutionExtensionClient:
    backend: AsyncStratifyX

    async def extension_inputs(
        self, execution_id: str, *, tables: Sequence[str],
        additional_sources: Sequence[NamedExecutionInputSelection] | None = None,
    ) -> ExecutionInputCatalogResponse:
        """Read exact owned schemas, flat enum references and frozen source.

        Use tables=[] when the native table names are unknown, then select an
        explicit subset for save/execute. This inspection saves no selection and
        starts no work. Backend rejects unsupported or oversized catalogues.
        """
        if additional_sources is not None:
            return await self.backend.studies_executions.describe_execution_inputs(
                execution_id, tables=tables, additional_sources=list(additional_sources),
                request_options={"max_retries": 0},
            )
        return await self.backend.studies_executions.describe_execution_inputs(
            execution_id, tables=tables, request_options={"max_retries": 0}
        )

    async def save_extension(
        self,
        thread_id: str,
        *,
        source_execution_id: str,
        tables: Sequence[str],
        source: str,
        name: str,
        description: str,
        parent_definition_id: str | None = None,
        additional_sources: Sequence[NamedExecutionInputSelection] | None = None,
    ) -> IdResponse:
        """Compile and save supplied EpochScript as an immutable definition.

        The caller writes the program or explicitly selects an authoring helper.
        This direct native call uses no LLM and starts no numerical execution.
        thread_id supplies native ownership scope; it creates no graph thread.
        """
        options: _DefinitionOptions = {}
        if parent_definition_id is not None:
            options["parent_definition_id"] = parent_definition_id
        selected = ExecutionInputSelection(source_execution_id=source_execution_id, tables=list(tables))
        if additional_sources is not None:
            selected = selected.model_copy(update={"additional_sources": list(additional_sources)})
        return await self.backend.agents.create_agent_study_definition(
            thread_id,
            name=name,
            description=description,
            source=source,
            study_type=StudyType.RESEARCH,
            data=DataOption(assets=[]),
            execution_input=selected,
            **options,
            request_options={"max_retries": 0},
        )

    async def execute_extension(self, request: CreateSdkExecutionRequest) -> SdkExecutionRecord:
        """Start or attach to one native extension operation and return its record.

        Keep operation_id to reconnect. Matching inputs attach; changed inputs
        conflict. Numerical completion and declared output completion are distinct.
        An explicit llm_call may use the bounded cached text step; deterministic
        table/JSON/dashboard programs make no model call. No supervisor is used.
        report_template replays the original study then its verified report;
        direct input_tables mode reuses completed results without a source rerun.
        When research_request_id is supplied, Backend confirms that accepted
        research attempt's link before starting work; standalone callers omit it.
        """
        if (request.input_tables is None) == (request.report_template is None):
            raise ValueError("Choose explicit input_tables or one verified report_template.")
        if request.response_plan is not None:
            raise ValueError("An extension declares outputs in EpochScript, without response_plan.")
        # Fern permits response extensions; the native request's outer shape
        # is closed. Never silently drop a misspelled request field here.
        if request.model_extra:
            raise ValueError("Unknown execution extension request fields.")
        options: _ExecutionOptions = {}
        if request.execution_parameter_bindings is not None:
            options["execution_parameter_bindings"] = request.execution_parameter_bindings
        if request.thread_id is not None:
            options["thread_id"] = request.thread_id
        if request.base_presentation is not None:
            options["base_presentation"] = request.base_presentation
        if request.research_request_id is not None:
            options["research_request_id"] = request.research_request_id
        if request.allow_period_override is not None:
            options["allow_period_override"] = request.allow_period_override
        if request.report_template is not None:
            options["report_template"] = request.report_template
        if request.additional_sources is not None:
            options["additional_sources"] = request.additional_sources
        if request.input_tables is not None:
            return await self.backend.sdk_requests.create_sdk_execution_request(
                operation_id=request.operation_id,
                study_id=request.study_id,
                source_execution_id=request.source_execution_id,
                parameters=request.parameters,
                input_tables=request.input_tables,
                **options,
                request_options={"max_retries": 0},
            )
        return await self.backend.sdk_requests.create_sdk_execution_request(
            operation_id=request.operation_id,
            study_id=request.study_id,
            source_execution_id=request.source_execution_id,
            parameters=request.parameters,
            **options,
            request_options={"max_retries": 0},
        )

    async def extension_status(self, operation_id: str) -> SdkExecutionRecord:
        """Read one accepted extension and its exact output pins; start no work.

        Check error/response_phase first. Confirmed extension_outputs belong to
        outputs_recorded; admission phase may remain active after computation or
        output failure. Read the underlying execution for numerical job status.
        """
        record = await self.backend.sdk_requests.get_sdk_execution_request_by_handle(
            operation_id, request_options={"max_retries": 0}
        )
        if record.request.operation_id != operation_id or (record.request.input_tables is None and record.request.report_template is None):
            raise ValueError("The native operation is not the requested execution extension.")
        return record

    async def response(
        self, response_id: str, *, version: int | None = None
    ) -> SavedResearchResponse:
        """Read a saved answer with its source attribution, without a graph call."""
        return await read_response(self.backend, response_id, version=version)

    async def extension_presentation(
        self,
        pin: ExecutionPresentationPin,
        *,
        category: str | None = None,
    ) -> DashboardEditView:
        """Read an exact published view, including authored Markdown and edit zero.

        The publication is independent of the numerical execution's dashboard.
        This never follows an unpinned latest producer or changes human overlays.
        """
        if pin.model_extra:
            raise ValueError("Unknown presentation pin fields.")
        view = await self.backend.contexts.read_presentation(
            pin.publication_id,
            category=category,
            edit_version=pin.edit_version,
            request_options={"max_retries": 0},
        )
        if (
            view.publication_id != pin.publication_id
            or view.catalog_revision != pin.catalog_revision
            or view.edit_version != pin.edit_version
        ):
            raise ValueError(
                "The presentation differs from its exact publication/catalog/edit pin."
            )
        return view

    async def response_table(
        self,
        response_id: str,
        name: str,
        *,
        version: int | None = None,
        offset: int = 0,
        page_size: int = 1000,
    ) -> ResponseTablePage:
        """Read one page from the selected answer revision, never an implicit preview."""
        saved = await self.response(response_id, version=version)
        return await read_response_table_page(
            self.backend, saved, name, offset=offset, page_size=page_size
        )
