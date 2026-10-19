"""Research admission and completion over the existing two native clients."""

from __future__ import annotations

from collections.abc import AsyncGenerator, AsyncIterator
from contextlib import asynccontextmanager
from typing import Literal

import httpx
from stratifyx import (
    DatePeriodConfig,
    ExecutionOptions,
    SdkContractErrorResponse,
    SdkContractRunRequest,
    SdkRequestPhase,
    SdkRequestRecord,
    SdkRequestRuntime,
)
from stratifyx.core.api_error import ApiError
from stratifyx.types.job_list_item import JobListItem

from .contracts import Contract, DomainError, ErrorResponse, RunRequest
from .errors import EpochError
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


class ResearchAccepted(Contract):
    status: Literal["accepted"] = "accepted"
    request_id: str


class ResearchCompleted(Contract):
    status: Literal["succeeded"] = "succeeded"
    request_id: str
    reusable_study: SavedStudy | None = None
    response: SavedResearchResponse


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


class EpochClient:
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
        reference: SavedStudy,
        *,
        period: DatePeriodConfig,
        execution: ExecutionOptions | None = None,
    ) -> ChosenExecution:
        """Execute prepared work directly; never start research or discovery."""
        return await self.supervisor.execute_saved(reference, period=period, execution=execution)

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
        )

    async def research(
        self, request: RunRequest, *, thread_id: str | None = None
    ) -> ResearchResult:
        request = RunRequest.model_validate(request.to_wire())
        if request.study_id is not None or request.source_execution_id is not None:
            raise ValueError("Use the separate saved-study execution action for prepared work")
        if request.auto_ingest:
            raise ValueError("Automatic ingestion is outside the core research capability")
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

    async def resume_research(
        self,
        waiting: NeedsInput,
        responses: dict[str, Answers],
    ) -> ResearchResult:
        async with _boundary(waiting.handle.request_id):
            record = await self.backend.sdk_requests.get_sdk_request(
                waiting.handle.request_id,
                request_options={"max_retries": 0},
            )
            handle = self._handle(record)
            if waiting.handle.model_copy(update={"run_id": None}) != handle:
                raise ValueError("The pending handle differs from the accepted research runtime")
            if record.phase.value not in {"active", "needs_input"}:
                raise ValueError("The research request is already closed")
            return await self._finish(
                record.request_id,
                await self.supervisor.resume(waiting, responses),
            )

    async def research_status(self, request_id: str) -> ResearchResult:
        async with _boundary(request_id):
            record = await self.backend.sdk_requests.get_sdk_request(
                request_id,
                request_options={"max_retries": 0},
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
            if record.runtime is None:
                return ResearchAccepted(status="accepted", request_id=request_id)
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
        if reusable is None:
            return ResearchCompleted(
                status="succeeded", request_id=record.request_id, response=response
            )
        return ResearchCompleted(
            status="succeeded",
            request_id=record.request_id,
            response=response,
            reusable_study=reusable,
        )

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
        record = await self.backend.sdk_requests.get_sdk_request(
            request_id,
            request_options={"max_retries": 0},
        )
        if record.response_version is not None:
            return await self._completed(record)
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
