"""Research admission and completion over the existing two native clients."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator, AsyncIterator
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Literal, TypedDict
from uuid import uuid4

import httpx
from stratifyx import (
    DatePeriodConfig,
    ExecutionOptions,
    SdkContractErrorResponse,
    SdkContractResponsePlanReference,
    SdkContractRunParameters,
    SdkContractRunRequest,
    SdkExecutionRecord,
    SdkRequestPhase,
    SdkRequestRecord,
    SdkRequestRuntime,
    SdkResearchLaunch,
)
from stratifyx.core.api_error import ApiError
from stratifyx.types.error_response import ErrorResponse as NativeErrorResponse
from stratifyx.types.job_list_item import JobListItem

from .contracts import (
    Contract,
    DomainError,
    ErrorResponse,
    OutputRequest,
    RunParameters,
    RunRequest,
    TextOutputRequest,
)
from .datasets import DatasetClient
from .errors import EpochError
from .extensions import ExecutionExtensionClient
from .responses import ResponseTablePage, SavedResearchResponse
from .supervisor import (
    Answers,
    ChosenExecution,
    InProgress,
    NeedsInput,
    NoExecution,
    PublishedAnswer,
    SavedStudy,
    SupervisorClient,
    SupervisorResult,
    WorkflowHandle,
)

if TYPE_CHECKING:
    from .session import EventHandler, ResearchSession


class _TaskOverrides(TypedDict, total=False):
    parameters: RunParameters
    auto_ingest: bool


class ResearchAccepted(Contract):
    status: Literal["accepted"] = "accepted"
    request_id: str
    operation_id: str | None = None


class ResearchCompleted(Contract):
    status: Literal["succeeded"] = "succeeded"
    request_id: str
    reusable_study: SavedStudy | None = None
    response: SavedResearchResponse
    operation_id: str | None = None


class ExecutionAccepted(Contract):
    status: Literal["accepted"] = "accepted"
    request_id: str
    operation_id: str
    execution_id: str


class ResearchFailure(ErrorResponse):
    request_id: str


class ResearchError(EpochError):
    def __init__(self, response: ResearchFailure):
        super().__init__(response.error, execution_id=response.execution_id)
        self.request_id = response.request_id
        self.response = response


type ResearchResult = ResearchAccepted | ResearchCompleted | NeedsInput | InProgress


@asynccontextmanager
async def _boundary(request_id: str | None) -> AsyncGenerator[None, None]:
    """Preserve request identity on failure; never retry or resubmit unknown work."""
    try:
        yield
    except ResearchError:
        raise
    except (EpochError, ApiError, httpx.HTTPError, ValueError) as error:
        execution_id: str | None = None
        if isinstance(error, EpochError):
            detail = error.error
            execution_id = error.execution_id
        elif isinstance(error, ValueError):
            detail = DomainError(code="INVALID_STATE", message=str(error), retryable=False)
        else:
            status = (
                error.status_code
                if isinstance(error, ApiError)
                else (
                    error.response.status_code if isinstance(error, httpx.HTTPStatusError) else None
                )
            )
            code = {
                400: "INVALID_REQUEST",
                401: "UNAUTHENTICATED",
                403: "FORBIDDEN",
                404: "NOT_FOUND",
                409: "INVALID_STATE",
                422: "INVALID_REQUEST",
                429: "RATE_LIMITED",
            }.get(status or 0, "TEMPORARILY_UNAVAILABLE")
            detail = DomainError.model_validate(
                {
                    "code": code,
                    "message": (
                        f"Research service returned HTTP {status}."
                        if status
                        else "The service connection failed. Read the same request status; do not resubmit."
                    ),
                    "retryable": status is None or status == 429 or status >= 500,
                }
            )
        if request_id is None:
            raise EpochError(detail, execution_id=execution_id) from error
        failure = ResearchFailure.model_validate(
            {
                "request_id": request_id,
                "error": detail.to_wire(),
                **({"execution_id": execution_id} if execution_id is not None else {}),
            }
        )
        raise ResearchError(failure) from error


class EpochClient(DatasetClient, ExecutionExtensionClient):
    """Research explicitly; prepared study execution remains a separate action.

    Backend owns accepted requests and response revisions. LangGraph owns the
    checkpointed conversation. A client instance owns neither an outcome cache
    nor a second thread store.
    """

    def __init__(self, supervisor: SupervisorClient):
        self.supervisor = supervisor
        self.backend = supervisor.backend

    @classmethod
    def connect(
        cls,
        *,
        graph_url: str,
        backend_url: str,
        token: str,
        assistant_id: str = "epoch-ai",
        ui_url: str | None = None,
    ) -> EpochClient:
        return cls(
            SupervisorClient.connect(
                graph_url=graph_url,
                backend_url=backend_url,
                token=token,
                assistant_id=assistant_id,
                ui_url=ui_url,
            )
        )

    async def aclose(self) -> None:
        await self.supervisor.aclose()

    def session(
        self,
        request: RunRequest | None = None,
        *,
        operation_id: str,
        thread_id: str | None = None,
    ) -> ResearchSession:
        """Observe/continue one server-owned research operation without a renderer.

        Supply a request to create-or-attach. Omit it to reconnect read-only to
        an existing operation. No local session file or second graph is created.
        """
        from .session import ResearchSession

        return ResearchSession(self, request, operation_id=operation_id, thread_id=thread_id)

    async def run(
        self,
        task: RunRequest | str | None = None,
        *,
        operation_id: str | None = None,
        thread_id: str | None = None,
        context: list[str] | None = None,
        outputs: list[OutputRequest] | None = None,
        parameters: RunParameters | None = None,
        auto_ingest: bool = False,
        interface: Literal["auto", "terminal", "notebook", "headless"] = "auto",
        on_event: EventHandler | None = None,
        request: RunRequest | None = None,
    ) -> ResearchCompleted | NeedsInput:
        """Stream research, collect explicit replies, and display its saved answer.

        Notebook and terminal adapters are optional presentation extras. In a
        noninteractive process this returns structured questions without waiting
        for keyboard input. A plain task defaults to a concise Markdown answer.
        Supply operation_id to reconnect; omit the task to observe saved work.
        Use execute for prepared work. Typed RunRequest callers remain supported.
        """
        from .interactive import run_interactive

        if request is not None:
            if task is not None:
                raise ValueError("Supply task or the legacy request keyword, not both.")
            task = request
        parsed = task
        additions = (context, outputs, parameters)
        if isinstance(parsed, str):
            overrides: _TaskOverrides = {}
            if parameters is not None:
                overrides["parameters"] = parameters
            if auto_ingest:
                overrides["auto_ingest"] = True
            parsed = RunRequest(
                task=parsed,
                context=[] if context is None else context,
                outputs=outputs
                if outputs is not None
                else [
                    TextOutputRequest(
                        name="answer",
                        type="text",
                        format="markdown",
                        instructions="Answer the task concisely using the research evidence.",
                    )
                ],
                **overrides,
            )
        elif any(value is not None for value in additions) or auto_ingest:
            raise ValueError("Supply task fields with a plain task, or put them in RunRequest.")
        if parsed is None and operation_id is None:
            raise ValueError("Supply a task to start work or operation_id to reconnect.")
        return await run_interactive(
            self.session(
                parsed,
                operation_id=operation_id if operation_id is not None else "run-" + uuid4().hex,
                thread_id=thread_id,
            ),
            interface,
            on_event=on_event,
        )

    async def resume(
        self,
        operation_id: str,
        responses: dict[str, Answers],
        *,
        interface: Literal["auto", "terminal", "notebook", "headless"] = "auto",
        on_event: EventHandler | None = None,
    ) -> ResearchCompleted | NeedsInput:
        """Answer this operation's current questions, then continue the same session."""
        from .interactive import run_interactive

        waiting = await self.research_status(operation_id=operation_id)
        if waiting.status != "needs_input":
            raise ValueError("This operation is not waiting for an answer.")
        session = self.session(operation_id=operation_id)
        await session.resume(waiting, responses)
        return await run_interactive(session, interface, on_event=on_event)

    async def status(
        self,
        operation_id: str,
        *,
        kind: Literal["run", "execute"] = "run",
    ) -> ResearchResult | ChosenExecution | ExecutionAccepted:
        """Read one operation; never submit, resume or execute work."""
        if kind == "run":
            return await self.research_status(operation_id=operation_id)
        if kind == "execute":
            return await self.execution_operation(operation_id)
        raise ValueError("Operation kind must be run or execute.")

    async def execute(
        self,
        reference: SavedStudy | str,
        *,
        period: DatePeriodConfig,
        execution: ExecutionOptions | None = None,
        operation_id: str | None = None,
    ) -> ChosenExecution:
        """Run prepared work and wait for completion and any saved response plan.

        Waiting only reads the accepted operation. Cancelling this local observer
        does not cancel Backend work. execute_saved remains the admission-only API.
        """
        operation_id = operation_id if operation_id is not None else "execute-" + uuid4().hex
        if not operation_id.strip() or operation_id != operation_id.strip():
            raise ValueError("Provide an exact nonblank operation_id")
        current = await self.execute_saved(
            reference, period=period, execution=execution, operation_id=operation_id
        )
        while True:
            if isinstance(current, ChosenExecution):
                state = current.execution.status.value
                if state == "completed":
                    return current
                if state in {"failed", "cancelled"}:
                    raise EpochError(
                        DomainError(
                            code="EXECUTION_FAILED",
                            message=f"Prepared execution {state}.",
                            retryable=False,
                        ),
                        execution_id=current.execution.id,
                    )
            await asyncio.sleep(1)
            current = await self.execution_operation(operation_id)

    async def read(
        self,
        response_id: str,
        *,
        table: str | None = None,
        version: int | None = None,
        offset: int = 0,
        page_size: int = 1000,
    ) -> SavedResearchResponse | ResponseTablePage:
        """Read an answer or one table page from Backend, without starting work."""
        if table is None:
            if offset != 0 or page_size != 1000:
                raise ValueError("Table paging options require a table name.")
            return await self.response(response_id, version=version)
        return await self.response_table(
            response_id, table, version=version, offset=offset, page_size=page_size
        )

    async def response(
        self, response_id: str, *, version: int | None = None
    ) -> SavedResearchResponse:
        """Read a saved answer directly from Backend."""
        return await self.supervisor.response(response_id, version=version)

    async def response_table(
        self,
        response_id: str,
        name: str,
        *,
        version: int | None = None,
        offset: int = 0,
        page_size: int = 1000,
    ) -> ResponseTablePage:
        return await self.supervisor.response_table(
            response_id, name, version=version, offset=offset, page_size=page_size
        )

    async def iter_response_table(
        self,
        response_id: str,
        name: str,
        *,
        version: int | None = None,
        page_size: int = 1000,
    ) -> AsyncIterator[ResponseTablePage]:
        async for page in self.supervisor.iter_response_table(
            response_id, name, version=version, page_size=page_size
        ):
            yield page

    async def execute_saved(
        self,
        reference: SavedStudy | str,
        *,
        period: DatePeriodConfig,
        execution: ExecutionOptions | None = None,
        operation_id: str | None = None,
    ) -> ChosenExecution | ExecutionAccepted:
        """Start/attach prepared work; a string reference is a completed research handle."""
        if isinstance(reference, str):
            research = await self.research_status(operation_id=reference)
            if not isinstance(research, ResearchCompleted) or research.reusable_study is None:
                raise ValueError("The research operation has no completed prepared study")
            reference = research.reusable_study
        if operation_id is None and reference.response_plan is None:
            return await self.supervisor.execute_saved(
                reference, period=period, execution=execution
            )
        if operation_id is None:
            operation_id = "execute-" + uuid4().hex
        async with _boundary(None):
            parameters = (
                RunParameters(period=period)
                if execution is None
                else RunParameters(period=period, execution=execution)
            )
            try:
                native_parameters = SdkContractRunParameters.model_validate(parameters.to_wire())
                if reference.response_plan is not None:
                    plan = SdkContractResponsePlanReference.model_validate(
                        reference.response_plan.to_wire()
                    )
                    if reference.thread_id is None:
                        record = await self.backend.sdk_requests.create_sdk_execution_request(
                            operation_id=operation_id,
                            study_id=reference.study_id,
                            source_execution_id=reference.source_execution_id,
                            parameters=native_parameters,
                            response_plan=plan,
                            request_options={"max_retries": 0},
                        )
                    else:
                        record = await self.backend.sdk_requests.create_sdk_execution_request(
                            operation_id=operation_id,
                            study_id=reference.study_id,
                            source_execution_id=reference.source_execution_id,
                            parameters=native_parameters,
                            response_plan=plan,
                            thread_id=reference.thread_id,
                            request_options={"max_retries": 0},
                        )
                elif reference.thread_id is None:
                    record = await self.backend.sdk_requests.create_sdk_execution_request(
                        operation_id=operation_id,
                        study_id=reference.study_id,
                        source_execution_id=reference.source_execution_id,
                        parameters=native_parameters,
                        request_options={"max_retries": 0},
                    )
                else:
                    record = await self.backend.sdk_requests.create_sdk_execution_request(
                        operation_id=operation_id,
                        study_id=reference.study_id,
                        source_execution_id=reference.source_execution_id,
                        parameters=native_parameters,
                        thread_id=reference.thread_id,
                        request_options={"max_retries": 0},
                    )
            except ApiError as error:
                if error.status_code == 409:
                    raise await self._execution_admission_conflict(operation_id, error) from error
                raise
            return await self._execution_operation(record)

    async def _execution_admission_conflict(self, operation_id: str, error: ApiError) -> EpochError:
        # Native checks an existing operation before evaluating a new plan.
        # Other 409s (for example a frozen period) reject before admission;
        # changing the ID cannot repair those and may duplicate accepted work.
        try:
            await self.backend.sdk_requests.get_sdk_execution_request_by_handle(
                operation_id, request_options={"max_retries": 0}
            )
        except ApiError as observation:
            if observation.status_code != 404:
                raise
            try:
                message = NativeErrorResponse.model_validate(error.body).message
            except ValueError:
                message = "The saved execution was rejected before admission."
            return EpochError(DomainError(code="INVALID_STATE", message=message, retryable=False))
        return EpochError(
            DomainError(
                code="IDEMPOTENCY_CONFLICT",
                message="This operation ID already has different accepted inputs. Use a new operation ID.",
                retryable=False,
            )
        )

    async def execution_operation(self, operation_id: str) -> ChosenExecution | ExecutionAccepted:
        """Read this prepared execution operation; start no job or agent."""
        async with _boundary(None):
            record = await self.backend.sdk_requests.get_sdk_execution_request_by_handle(
                operation_id,
                request_options={"max_retries": 0},
            )
            return await self._execution_operation(record)

    async def _execution_operation(
        self, record: SdkExecutionRecord
    ) -> ChosenExecution | ExecutionAccepted:
        if record.error is not None:
            failure = ErrorResponse.model_validate_json(
                record.error.model_dump_json(by_alias=True, exclude_unset=True)
            )
            raise EpochError(failure.error, execution_id=record.execution_id)
        accepted = ExecutionAccepted(
            request_id=record.request_id,
            operation_id=record.request.operation_id,
            execution_id=record.execution_id,
        )
        try:
            job = await self.supervisor.execution(record.execution_id)
        except ApiError as error:
            if error.status_code == 404 and record.phase.value == "accepted":
                return accepted
            raise
        if job.id != record.execution_id or job.definition_id != record.request.study_id:
            raise ValueError("The native execution differs from its accepted operation")
        if record.request.response_plan is not None and (
            record.response_phase is None or record.response_phase.value != "outputs_recorded"
        ):
            return accepted
        result = ChosenExecution(
            execution=job,
            request_id=record.request_id,
            operation_id=record.request.operation_id,
            reusable_study=SavedStudy(
                study_id=record.request.study_id,
                source_execution_id=record.execution_id,
                thread_id=record.request.thread_id,
            ),
        )
        if record.request.response_plan is not None:
            if record.response_id is None or record.response_version is None:
                raise ValueError("The completed execution plan has no pinned answer revision")
            response = await self.response(record.response_id, version=record.response_version)
            plan = record.request.response_plan
            if (
                response.request_id != record.request_id
                or response.primary_execution_id != record.execution_id
                or response.study_id != record.request.study_id
                or response.response_plan is None
                or response.response_plan.plan_id != plan.plan_id
                or response.response_plan.version != plan.version
                or (
                    record.request.thread_id is not None
                    and response.thread_id != record.request.thread_id
                )
            ):
                raise ValueError(
                    "The published execution answer differs from its exact admitted plan/source"
                )
            study = result.reusable_study.model_copy(
                update={"response_plan": response.response_plan}
            )
            result = result.model_copy(update={"response": response, "reusable_study": study})
        return result

    async def execution(self, execution_id: str) -> JobListItem:
        """Read queued/running/completed native status without a supervisor call."""
        try:
            async with _boundary(None):
                return await self.supervisor.execution(execution_id)
        except EpochError as error:
            raise EpochError(error.error, execution_id=execution_id) from error

    @staticmethod
    def _handle(record: SdkRequestRecord) -> WorkflowHandle:
        if record.runtime is None:
            raise ValueError("This research request has no supervisor runtime")
        return WorkflowHandle(
            request_id=record.request_id,
            thread_id=record.runtime.thread_id,
            assistant_id=record.runtime.assistant_id,
            execution_ids_before=record.runtime.execution_ids_before,
            outcome_ids_before=record.runtime.outcome_ids_before,
            run_id=record.graph_run_id,
            operation_id=record.operation_id,
        )

    async def research(
        self,
        request: RunRequest,
        *,
        thread_id: str | None = None,
        operation_id: str | None = None,
        wait: bool = True,
    ) -> ResearchResult:
        request = RunRequest.model_validate(request.to_wire())
        if request.study_id is not None or request.source_execution_id is not None:
            raise ValueError("Use the separate saved-study execution action for prepared work")
        if request.auto_ingest:
            raise ValueError("Automatic ingestion is outside the core research capability")
        if not wait and operation_id is None:
            raise ValueError("Nonblocking research requires a readable operation_id")
        if operation_id is not None:
            return await self._research_operation(request, operation_id, thread_id, wait=wait)
        async with _boundary(None):
            record = await self.backend.sdk_requests.create_sdk_request(
                request=SdkContractRunRequest.model_validate(request.to_wire()),
                request_options={"max_retries": 0},
            )
        async with _boundary(record.request_id):
            handle = await self.supervisor.prepare(thread_id, request_id=record.request_id)
            await self.backend.sdk_requests.update_sdk_request(
                record.request_id,
                expected_version=record.version,
                runtime=SdkRequestRuntime(
                    thread_id=handle.thread_id,
                    assistant_id=handle.assistant_id,
                    execution_ids_before=handle.execution_ids_before,
                    outcome_ids_before=handle.outcome_ids_before,
                ),
                request_options={"max_retries": 0},
            )
            outcome = await self.supervisor.submit(
                handle,
                sdk_request_id=record.request_id,
                task=request.task
                + "\n\nAccepted SDK research contract:\n"
                + request.model_dump_json(by_alias=True, exclude_unset=True),
            )
            return await self._finish(record.request_id, outcome)

    async def _research_operation(
        self, request: RunRequest, operation_id: str, thread_id: str | None, *, wait: bool = True
    ) -> ResearchResult:
        request = RunRequest.model_validate(request)
        if request.study_id is not None or request.source_execution_id is not None:
            raise ValueError("Research builds a study; use execute_saved for prepared work")
        async with _boundary(None):
            launch = (
                SdkResearchLaunch(assistant_id=self.supervisor.assistant_id)
                if thread_id is None
                else SdkResearchLaunch(
                    assistant_id=self.supervisor.assistant_id, thread_id=thread_id
                )
            )
            try:
                record = await self.backend.sdk_requests.create_sdk_request(
                    request=SdkContractRunRequest.model_validate(
                        request.model_dump(mode="json", by_alias=True, exclude_none=True)
                    ),
                    operation_id=operation_id,
                    launch=launch,
                    request_options={"max_retries": 0},
                )
            except ApiError as error:
                if error.status_code == 409:
                    raise EpochError(
                        DomainError(
                            code="IDEMPOTENCY_CONFLICT",
                            message="This operation ID already has different accepted inputs. Use a new operation ID.",
                            retryable=False,
                        )
                    ) from error
                raise
        async with _boundary(record.request_id):
            record = await self.backend.sdk_requests.get_sdk_request(
                record.request_id, request_options={"max_retries": 0}
            )
            if record.response_version is not None or record.error is not None:
                return await self.research_status(record.request_id)
            if record.runtime is None:
                try:
                    handle = await self.supervisor.prepare_operation(record.request_id, thread_id)
                except ValueError:
                    # Another same-ID caller may already have reached a question
                    # after this caller read its admission response.
                    record = await self.backend.sdk_requests.get_sdk_request(
                        record.request_id, request_options={"max_retries": 0}
                    )
                    if record.runtime is None:
                        raise
                else:
                    try:
                        record = await self.backend.sdk_requests.update_sdk_request(
                            record.request_id,
                            expected_version=record.version,
                            runtime=SdkRequestRuntime(
                                thread_id=handle.thread_id,
                                assistant_id=handle.assistant_id,
                                execution_ids_before=handle.execution_ids_before,
                                outcome_ids_before=handle.outcome_ids_before,
                            ),
                            request_options={"max_retries": 0},
                        )
                    except ApiError as error:
                        if error.status_code != 409:
                            raise
                        record = await self.backend.sdk_requests.get_sdk_request(
                            record.request_id, request_options={"max_retries": 0}
                        )
            if record.graph_run_id is None and record.response_version is None:
                try:
                    await self.supervisor.start_operation(self._handle(record), request.task)
                except httpx.HTTPStatusError as error:
                    if error.response.status_code != 409:
                        raise
                record = await self.backend.sdk_requests.get_sdk_request(
                    record.request_id, request_options={"max_retries": 0}
                )
                if record.graph_run_id is None:
                    raise ValueError(
                        "The conversation is busy; this operation has not started a native run. Reattach when it is available."
                    )
            if record.response_version is not None or record.error is not None:
                return await self.research_status(record.request_id)
            if not wait:
                return await self.research_status(record.request_id)
            return await self._finish(
                record.request_id, await self.supervisor.join_operation(self._handle(record))
            )

    async def resume_research(
        self,
        waiting: NeedsInput,
        responses: dict[str, Answers],
        *,
        wait: bool = True,
    ) -> ResearchResult:
        async with _boundary(waiting.handle.request_id):
            record = await self.backend.sdk_requests.get_sdk_request(
                waiting.handle.request_id,
                request_options={"max_retries": 0},
            )
            handle = self._handle(record)
            if waiting.handle.model_copy(update={"run_id": None}) != handle.model_copy(
                update={"run_id": None}
            ):
                raise ValueError("The pending handle differs from the accepted research runtime")
            if record.operation_id is not None and (
                record.response_version is not None
                or record.error is not None
                or record.graph_run_id != waiting.handle.run_id
            ):
                return await self.research_status(record.request_id)
            if record.phase.value not in {"active", "needs_input"}:
                raise ValueError("The research request is already closed")
            try:
                if wait:
                    outcome = await self.supervisor.resume(waiting, responses)
                else:
                    if record.operation_id is None:
                        raise ValueError("Nonblocking resume requires a readable operation_id")
                    await self.supervisor.start_resume(waiting, responses)
                    return await self.research_status(record.request_id)
            except httpx.HTTPStatusError as error:
                if record.operation_id is None or error.response.status_code != 409:
                    raise
                return await self.research_status(record.request_id)
            return await self._finish(record.request_id, outcome)

    async def research_status(
        self, request_id: str | None = None, *, operation_id: str | None = None
    ) -> ResearchResult:
        if (request_id is None) == (operation_id is None):
            raise ValueError("Provide either request_id or operation_id")
        async with _boundary(request_id):
            if operation_id is not None:
                record = await self.backend.sdk_requests.get_sdk_request_by_handle(
                    operation_id, request_options={"max_retries": 0}
                )
                request_id = record.request_id
            else:
                assert request_id is not None
                record = await self.backend.sdk_requests.get_sdk_request(
                    request_id, request_options={"max_retries": 0}
                )
            if record.request_id != request_id:
                raise ValueError("Backend returned another request identity")
            if record.error is not None:
                raise ResearchError(
                    ResearchFailure.model_validate(
                        {
                            **record.error.model_dump(
                                mode="json", by_alias=True, exclude_unset=True
                            ),
                            "request_id": request_id,
                        }
                    )
                )
            if record.response_version is not None:
                return await self._completed(record)
            if record.runtime is None or (
                record.operation_id is not None and record.graph_run_id is None
            ):
                accepted = ResearchAccepted(status="accepted", request_id=request_id)
                if record.operation_id is not None:
                    accepted.operation_id = record.operation_id
                return accepted
            return await self._finish(
                request_id,
                await self.supervisor.status(self._handle(record)),
            )

    async def _completed(self, record: SdkRequestRecord) -> ResearchCompleted:
        if record.response_id is None or record.response_version is None:
            raise ValueError("The research request has no pinned answer")
        response = await self.supervisor.response(
            record.response_id, version=record.response_version
        )
        request = RunRequest.model_validate_json(
            record.request.model_dump_json(by_alias=True, exclude_unset=True)
        )
        if (
            response.request_id != record.request_id
            or record.runtime is None
            or response.thread_id != record.runtime.thread_id
            or response.primary_execution_id != record.current_execution_id
            or response.content.declarations != request.outputs
        ):
            raise EpochError(
                DomainError(
                    code="OUTPUT_VALIDATION_FAILED",
                    message="Saved answer identity, source or declarations differ from this query.",
                    retryable=False,
                ),
                execution_id=record.current_execution_id,
            )
        reusable = None
        if response.primary_execution_id is not None and response.study_id is not None:
            reusable = SavedStudy(
                study_id=response.study_id,
                source_execution_id=response.primary_execution_id,
                thread_id=record.runtime.thread_id,
            )
            if response.response_plan is not None:
                reusable = reusable.model_copy(update={"response_plan": response.response_plan})
        completed = ResearchCompleted(
            status="succeeded", request_id=record.request_id, response=response
        )
        if reusable is not None:
            completed.reusable_study = reusable
        if record.operation_id is not None:
            completed.operation_id = record.operation_id
        return completed

    async def _fail(
        self,
        record: SdkRequestRecord,
        error: DomainError,
        execution_id: str | None = None,
    ) -> ResearchError:
        failure = ResearchFailure.model_validate(
            {
                "request_id": record.request_id,
                "error": error.to_wire(),
                **({"execution_id": execution_id} if execution_id is not None else {}),
            }
        )
        wire = ErrorResponse.model_validate(
            {key: value for key, value in failure.to_wire().items() if key != "request_id"}
        )
        await self.backend.sdk_requests.update_sdk_request(
            record.request_id,
            expected_version=record.version,
            error=SdkContractErrorResponse.model_validate(wire.to_wire()),
            request_options={"max_retries": 0},
        )
        return ResearchError(failure)

    async def _finish(self, request_id: str, outcome: SupervisorResult) -> ResearchResult:
        try:
            return await self._finish_once(request_id, outcome)
        except ApiError as error:
            if error.status_code != 409:
                raise
            current = await self.backend.sdk_requests.get_sdk_request(
                request_id, request_options={"max_retries": 0}
            )
            if current.operation_id is None:
                raise
            if (
                isinstance(outcome, NeedsInput)
                and current.error is None
                and current.response_version is None
                and current.graph_run_id == outcome.handle.run_id
            ):
                # A phase hint is advisory. A duplicate observer must receive the
                # same questions even when its write lost the metadata CAS.
                return outcome
            return await self.research_status(request_id)

    async def _finish_once(self, request_id: str, outcome: SupervisorResult) -> ResearchResult:
        record = await self.backend.sdk_requests.get_sdk_request(
            request_id,
            request_options={"max_retries": 0},
        )
        if record.response_version is not None:
            return await self._completed(record)
        if record.error is not None:
            return await self.research_status(request_id)
        if (
            record.operation_id is not None
            and outcome.handle is not None
            and record.graph_run_id != outcome.handle.run_id
        ):
            return await self.research_status(request_id)
        if isinstance(outcome, NeedsInput):
            if record.phase.value != "needs_input":
                await self.backend.sdk_requests.update_sdk_request(
                    request_id,
                    expected_version=record.version,
                    phase=SdkRequestPhase.NEEDS_INPUT,
                    request_options={"max_retries": 0},
                )
            return outcome
        if isinstance(outcome, InProgress):
            return outcome
        if isinstance(outcome, NoExecution):
            raise await self._fail(
                record,
                outcome.publication_error
                or DomainError(
                    code="OUTPUT_VALIDATION_FAILED"
                    if outcome.publication_failed
                    else "EXECUTION_FAILED",
                    message=outcome.reason,
                    retryable=False,
                ),
                outcome.execution_id,
            )
        if not isinstance(outcome, PublishedAnswer):
            raise await self._fail(
                record,
                DomainError(
                    code="OUTPUT_VALIDATION_FAILED",
                    message="Research completion requires an explicit published answer.",
                    retryable=False,
                ),
            )
        reference = outcome.response
        try:
            response = await self.supervisor.response(
                reference.response_id, version=reference.version
            )
        except EpochError as error:
            if error.error.code == "NOT_FOUND":
                raise await self._fail(
                    record,
                    DomainError(
                        code="OUTPUT_VALIDATION_FAILED",
                        message="The published answer reference is not saved.",
                        retryable=False,
                    ),
                    reference.primary_execution_id,
                ) from error
            raise
        if response.reference() != reference:
            raise await self._fail(
                record,
                DomainError(
                    code="OUTPUT_VALIDATION_FAILED",
                    message="Published answer reference differs from storage.",
                    retryable=False,
                ),
            )
        if response.primary_execution_id is None:
            record = await self.backend.sdk_requests.update_sdk_request(
                request_id,
                expected_version=record.version,
                response_id=response.response_id,
                response_version=response.version,
                request_options={"max_retries": 0},
            )
        else:
            record = await self.backend.sdk_requests.update_sdk_request(
                request_id,
                expected_version=record.version,
                current_execution_id=response.primary_execution_id,
                response_id=response.response_id,
                response_version=response.version,
                request_options={"max_retries": 0},
            )
        return await self._completed(record)
