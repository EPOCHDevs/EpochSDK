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
    AcquisitionProvenancePage,
    CreateSdkExecutionRequest,
    CreateExecutionOutputEdit,
    DashboardEditView,
    DataOption,
    ExecutionInputCatalogResponse,
    ExecutionInputSelection,
    ExecutionParameterValue,
    ExecutionPresentationPin,
    ExecutionReportReference,
    ExecutionOutputEditRecord,
    ExecutionOutputRevisionPage,
    ExecutionResponseTextEdit,
    ExecutionPresentationEdit,
    ExecutionReportEdit,
    IdResponse,
    NamedExecutionInputSelection,
    SdkExecutionRecord,
    StudyType,
)

from .responses import (
    ResponseTablePage,
    SavedResearchResponse,
    read_execution_acquisition_provenance,
    read_response,
    read_response_acquisition_provenance,
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


class _OutputEditOptions(TypedDict, total=False):
    response_text: list[ExecutionResponseTextEdit]
    presentation: ExecutionPresentationEdit
    report: ExecutionReportEdit


class ExecutionExtensionClient:
    backend: AsyncStratifyX

    async def execution_outputs(self, execution_id: str, *, revision: int | None = None) -> SdkExecutionRecord:
        """Read current accepted outputs, or pin a historical output revision.

        The numerical execution identity is stable through all output edits.
        Reading this record invokes neither computation nor a model.
        """
        if revision is not None and (isinstance(revision, bool) or revision < 1):
            raise ValueError("Choose a positive accepted output revision.")
        record = await self.backend.sdk_requests.get_execution_outputs(
            execution_id, revision=revision, request_options={"max_retries": 0},
        )
        if record.execution_id != execution_id or (
            revision is not None and (record.output_revision is None or record.output_revision.version != revision)
        ):
            raise ValueError("The output record differs from its selected execution and revision.")
        return record

    async def edit_outputs(self, execution_id: str, request: CreateExecutionOutputEdit) -> ExecutionOutputEditRecord:
        """Submit one explicit direct or EpochScript output edit to this run.

        Keep operation_id and the returned request_id to reconnect. Direct text
        saves invoke no model. Authored reports consume selected saved tables;
        original numerical acquisition and simulation are never rerun.
        """
        if request.model_extra:
            raise ValueError("Unknown execution output-edit fields.")
        options: _OutputEditOptions = {}
        if request.response_text is not None:
            options["response_text"] = request.response_text
        if request.presentation is not None:
            options["presentation"] = request.presentation
        if request.report is not None:
            options["report"] = request.report
        record = await self.backend.execution_output_edits.create_execution_output_edit(
            execution_id, operation_id=request.operation_id, expected_revision=request.expected_revision,
            kind=request.kind, **options, request_options={"max_retries": 0},
        )
        if record.execution_id != execution_id or record.request != request:
            raise ValueError("The output edit receipt differs from its submitted target and request.")
        return record

    async def output_edit_status(self, execution_id: str, request_id: str) -> ExecutionOutputEditRecord:
        """Reconnect the original edit operation without dispatching another attempt."""
        record = await self.backend.execution_output_edits.get_execution_output_edit(
            execution_id, request_id, request_options={"max_retries": 0},
        )
        if record.execution_id != execution_id or record.request_id != request_id:
            raise ValueError("The edit receipt differs from its original operation identity.")
        return record

    async def output_edit_by_handle(self, execution_id: str, operation_id: str) -> ExecutionOutputEditRecord:
        """Read an admitted edit after losing its initial reply; this starts no work."""
        record = await self.backend.execution_output_edits.get_execution_output_edit_by_handle(
            execution_id, operation_id, request_options={"max_retries": 0},
        )
        if record.execution_id != execution_id or record.request.operation_id != operation_id:
            raise ValueError("The edit receipt differs from its original target and handle.")
        return record

    async def cancel_output_edit(self, execution_id: str, request_id: str) -> ExecutionOutputEditRecord:
        """Cancel a candidate edit while preserving the last accepted output."""
        record = await self.backend.execution_output_edits.cancel_execution_output_edit(
            execution_id, request_id, request_options={"max_retries": 0},
        )
        if record.execution_id != execution_id or record.request_id != request_id:
            raise ValueError("The cancellation receipt differs from its original edit operation.")
        return record

    async def output_revisions(self, execution_id: str, *, offset: int = 0, page_size: int = 50) -> ExecutionOutputRevisionPage:
        """Page immutable accepted history. Failed candidates remain edit receipts."""
        if isinstance(offset, bool) or offset < 0 or isinstance(page_size, bool) or not 1 <= page_size <= 200:
            raise ValueError("Choose a nonnegative history offset and page_size from 1 to 200.")
        page = await self.backend.execution_output_edits.list_execution_output_revisions(
            execution_id, offset=offset, page_size=page_size, request_options={"max_retries": 0},
        )
        if page.execution_id != execution_id or page.offset != offset:
            raise ValueError("The output history differs from its selected execution and offset.")
        return page

    async def execution_answer(self, execution_id: str, *, revision: int | None = None) -> SavedResearchResponse | None:
        """Read the answer pinned by the selected output revision; dashboard-only runs return None."""
        record = await self.execution_outputs(execution_id, revision=revision)
        outputs = record.extension_outputs
        if outputs is None or outputs.response_id is None or outputs.response_version is None:
            if record.response_id is not None and record.response_version is not None:
                return await self.response(record.response_id, version=record.response_version)
            return None
        return await self.response(outputs.response_id, version=outputs.response_version)

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

    async def response_provenance(
        self, response_id: str, *, version: int | None = None,
        offset: int = 0, page_size: int = 50,
    ) -> AcquisitionProvenancePage:
        """Page the immutable source receipts retained with an answer."""
        return await read_response_acquisition_provenance(
            self.backend, response_id, version=version, offset=offset, page_size=page_size)

    async def execution_provenance(
        self, execution_id: str, *, expected_sha256: str | None = None,
        offset: int = 0, page_size: int = 50,
    ) -> AcquisitionProvenancePage:
        """Page owned execution receipts; catalogue digests can pin the snapshot."""
        return await read_execution_acquisition_provenance(
            self.backend, execution_id, expected_sha256=expected_sha256,
            offset=offset, page_size=page_size)

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
