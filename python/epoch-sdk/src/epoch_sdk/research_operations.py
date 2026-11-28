"""Platform-owned research admission, status and terminal guidance.

Native execution admission and response artifacts remain in StratifyX. This
client never retries a write or starts a graph/engine run.
"""

from __future__ import annotations

import json
from enum import StrEnum
from typing import Annotated, Literal, TypedDict
from urllib.parse import quote, urlsplit

import httpx
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator
from stratifyx.core.api_error import ApiError

from .contracts import Contract, ErrorResponse, NonBlank, RunRequest
from .credentials import BearerAuth, Token
from .saved_outputs import SavedOutputManifest


class ResearchPhase(StrEnum):
    ACCEPTED = "accepted"
    ACTIVE = "active"
    NEEDS_INPUT = "needs_input"
    OUTPUTS_RECORDED = "outputs_recorded"
    FAILED = "failed"


type Interaction = Literal["interactive", "one_shot"]


class ResearchRuntime(Contract):
    thread_id: NonBlank
    assistant_id: NonBlank
    execution_ids_before: list[NonBlank]
    outcome_ids_before: list[NonBlank]


class ResearchLaunch(Contract):
    assistant_id: NonBlank
    thread_id: NonBlank | None = None


class ResearchRecord(Contract):
    request_id: Annotated[str, Field(pattern=r"^req_[0-9a-f]{32}$")]
    version: Annotated[int, Field(ge=0)]
    created_at_ms: int
    updated_at_ms: int
    phase: ResearchPhase
    interaction: Interaction
    request: RunRequest
    operation_id: str | None = None
    launch: ResearchLaunch | None = None
    runtime: ResearchRuntime | None = None
    graph_run_id: str | None = None
    current_execution_id: str | None = None
    native_execution_request_id: str | None = None
    source_execution_id: str | None = None
    response_id: str | None = None
    response_version: int | None = None
    output_manifest: SavedOutputManifest | None = None
    error: ErrorResponse | None = None

    @field_validator("phase", mode="before")
    @classmethod
    def parse_phase(cls, value: object) -> ResearchPhase:
        if isinstance(value, ResearchPhase):
            return value
        if isinstance(value, str):
            return ResearchPhase(value)
        raise ValueError("Invalid research phase")


class CreateResearch(Contract):
    request: RunRequest
    operation_id: str | None = None
    launch: ResearchLaunch | None = None


class UpdateResearch(Contract):
    expected_version: Annotated[int, Field(ge=0)]
    runtime: ResearchRuntime | None = None
    phase: Literal["active", "needs_input"] | None = None
    graph_run_id: str | None = None
    prior_graph_run_id: str | None = None
    current_execution_id: str | None = None
    native_execution_request_id: str | None = None
    response_id: str | None = None
    response_version: int | None = None
    output_manifest: SavedOutputManifest | None = None
    error: ErrorResponse | None = None


class OperationRequestOptions(TypedDict, total=False):
    max_retries: Literal[0]
    timeout_in_seconds: int


class PlatformErrorBody(BaseModel):
    model_config = ConfigDict(extra="ignore", strict=True)
    error: str
    message: str
    timestamp: str


class ResearchOperationsHTTPError(ApiError):
    body: PlatformErrorBody | None


class ResearchOperationsClient:
    def __init__(
        self,
        base_url: str,
        token: Token | None = None,
        *,
        http: httpx.AsyncClient | None = None,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        parsed = urlsplit(base_url)
        if (
            (
                parsed.scheme != "https"
                and not (
                    parsed.scheme == "http" and parsed.hostname in {"localhost", "127.0.0.1", "::1"}
                )
            )
            or parsed.username
            or parsed.password
            or parsed.query
            or parsed.fragment
            or parsed.path not in {"", "/"}
        ):
            raise ValueError("Research operation origin must be HTTPS or loopback without a path")
        if http is not None and transport is not None:
            raise ValueError("Pass an HTTP client or a transport, not both")
        self._origin = base_url.rstrip("/")
        self._owned = http is None
        self._http = http or httpx.AsyncClient(
            transport=transport, timeout=30.0, follow_redirects=False
        )
        self._auth = (
            None
            if token is None
            else BearerAuth((lambda: token) if isinstance(token, str) else token, base_url)
        )

    async def aclose(self) -> None:
        if self._owned:
            await self._http.aclose()

    async def _request(
        self,
        method: str,
        path: str,
        body: CreateResearch | UpdateResearch | None,
        options: OperationRequestOptions | None,
    ) -> ResearchRecord:
        if options and options.get("max_retries", 0) != 0:
            raise ValueError("Research operation writes are never automatically retried")
        async with self._http.stream(
            method,
            self._origin + "/api/v1/integration/requests" + path,
            content=json.dumps(body.to_wire(), allow_nan=False) if body else None,
            headers={"Content-Type": "application/json"},
            auth=self._auth,
            timeout=(options or {}).get("timeout_in_seconds", 30),
            follow_redirects=False,
        ) as response:
            data = bytearray()
            async for part in response.aiter_bytes():
                if len(data) + len(part) > 512 * 1024:
                    raise ValueError("Research operation response exceeds 512 KiB")
                data.extend(part)
            if response.status_code != 200:
                try:
                    problem = PlatformErrorBody.model_validate_json(data)
                except ValidationError:
                    problem = None
                raise ResearchOperationsHTTPError(
                    status_code=response.status_code, headers=dict(response.headers), body=problem
                )
            return ResearchRecord.model_validate_json(data)

    @staticmethod
    def _segment(value: str) -> str:
        if not value or len(value) > 128 or any(c.isspace() or c in "/\\%?#" for c in value):
            raise ValueError("Invalid research identity")
        return quote(value, safe="")

    async def create_sdk_request(
        self,
        *,
        request: RunRequest,
        operation_id: str | None = None,
        launch: ResearchLaunch | None = None,
        request_options: OperationRequestOptions | None = None,
    ) -> ResearchRecord:
        body = CreateResearch.model_validate(
            {
                "request": request.to_wire(),
                **({"operation_id": operation_id} if operation_id is not None else {}),
                **({"launch": launch.to_wire()} if launch is not None else {}),
            }
        )
        return await self._request("POST", "", body, request_options)

    async def get_sdk_request(
        self, request_id: str, *, request_options: OperationRequestOptions | None = None
    ) -> ResearchRecord:
        return await self._request("GET", "/" + self._segment(request_id), None, request_options)

    async def get_sdk_request_by_handle(
        self, operation_id: str, *, request_options: OperationRequestOptions | None = None
    ) -> ResearchRecord:
        return await self._request(
            "GET", "/by-handle/" + self._segment(operation_id), None, request_options
        )

    async def update_sdk_request(
        self,
        request_id: str,
        *,
        expected_version: int,
        runtime: ResearchRuntime | None = None,
        phase: Literal["active", "needs_input"] | ResearchPhase | None = None,
        graph_run_id: str | None = None,
        prior_graph_run_id: str | None = None,
        current_execution_id: str | None = None,
        native_execution_request_id: str | None = None,
        response_id: str | None = None,
        response_version: int | None = None,
        output_manifest: SavedOutputManifest | None = None,
        error: ErrorResponse | None = None,
        request_options: OperationRequestOptions | None = None,
    ) -> ResearchRecord:
        body = UpdateResearch.model_validate(
            {
                key: value
                for key, value in {
                    "expected_version": expected_version,
                    "runtime": runtime.to_wire() if runtime else None,
                    "phase": str(phase) if phase is not None else None,
                    "graph_run_id": graph_run_id,
                    "prior_graph_run_id": prior_graph_run_id,
                    "current_execution_id": current_execution_id,
                    "native_execution_request_id": native_execution_request_id,
                    "response_id": response_id,
                    "response_version": response_version,
                    "output_manifest": output_manifest.to_wire() if output_manifest else None,
                    "error": error.to_wire() if error else None,
                }.items()
                if value is not None
            }
        )
        return await self._request("PATCH", "/" + self._segment(request_id), body, request_options)
