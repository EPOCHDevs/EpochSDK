"""Real Cognito, live EpochAI catalogue and persistent native Space acceptance.

Use an isolated, disposable Backend storage namespace. This runner creates real
files, datasets, studies, executions and a fitted model. Its receipt records each
created reference before subsequent work; cleanup removes API resources, and the
operator must then destroy the disposable storage namespace (immutable models
have no public deletion endpoint). Tokens are read from private login files and
never written to the evidence. Run create, restart the candidate with fresh local
scratch storage, then verify, optionally foreign, and cleanup.
"""

from __future__ import annotations

import argparse
import asyncio
import base64
import hashlib
import importlib.metadata
import json
import os
import sys
from collections.abc import Awaitable, Mapping
from contextlib import aclosing
from datetime import date, timedelta
from importlib import import_module
from io import BytesIO
from pathlib import Path
from typing import Protocol, cast
from uuid import uuid4

import httpx
from mcp import Client
from mcp.client.stdio import StdioServerParameters
from mcp.types import CallToolResult
from pydantic import BaseModel, ConfigDict, Field
from space_core_acceptance import (
    chart_values,
    completed,
    native_options,
    read_content,
    resource,
    saved,
)
from stratifyx import DataOption, DatePeriodConfig
from stratifyx.core.api_error import ApiError
from stratifyx.core.request_options import RequestOptions
from stratifyx.types import (
    DatasetPurpose,
    DatasetReviewRequest,
    DatasetReviewResponse,
    DatasetTableSchema,
    DataSourceColumn,
    JobListItem,
    SavedDataset,
    SpaceFolder,
    SpacePage,
    SpaceResourceRef,
    StructuredImportRequest,
    StructuredImportResult,
    UserFileDescriptor,
)

from epoch_sdk.agent_tools import AgentToolsClient
from epoch_sdk.agent_tools_contract import AgentToolsCatalog
from epoch_sdk.research import EpochClient

NO_RETRY: RequestOptions = {"max_retries": 0}


class _Scalar(Protocol):
    def as_py(self) -> object: ...


class _Column(Protocol):
    null_count: int
    type: object

    def to_pylist(self) -> list[object]: ...
    def __getitem__(self, index: int) -> _Scalar: ...


class _Table(Protocol):
    def column(self, name: str) -> _Column: ...


class _Reader(Protocol):
    def read_all(self) -> _Table: ...


class _IPC(Protocol):
    def open_file(self, source: BytesIO) -> _Reader: ...


def arrow_file(content: bytes) -> _Table:
    # PyArrow 26 has no bundled stubs. Keep the native table open to arbitrary
    # user columns/cells while typing only the reader methods this check uses.
    return cast(_IPC, import_module("pyarrow.ipc")).open_file(BytesIO(content)).read_all()


async def call(client: Client, name: str, arguments: Mapping[str, object]) -> CallToolResult:
    # MCP owns this open JSON-RPC argument envelope; each native tool validates
    # its own generated request type at the server boundary.
    result = await client.call_tool(name, dict(arguments))
    assert not result.is_error, result
    return result


class State(BaseModel):
    model_config = ConfigDict(extra="forbid")
    run_id: str
    backend_url: str
    graph_url: str
    backend_git_sha: str | None = None
    agent_git_sha: str | None = None
    agent_revision_id: str | None = None
    agent_catalogue_sha256: str | None = None
    native_sdk_version: str = Field(default_factory=lambda: importlib.metadata.version("stratifyx"))
    epoch_sdk_version: str = Field(default_factory=lambda: importlib.metadata.version("epoch-sdk"))
    runner_sha256: str = Field(
        default_factory=lambda: hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    )
    files: list[str] = Field(default_factory=list)
    drafts: list[str] = Field(default_factory=list)
    datasets: list[str] = Field(default_factory=list)
    studies: list[str] = Field(default_factory=list)
    executions: list[str] = Field(default_factory=list)
    placements: list[SpaceResourceRef] = Field(default_factory=lambda: list[SpaceResourceRef]())
    folders: list[str] = Field(default_factory=list)
    dataset_ref: str | None = None
    knowledge_ref: str | None = None
    source_ref: str | None = None
    study_id: str | None = None
    model_ref: str | None = None
    model_sha256: str | None = None
    prepared_sha256: str | None = None
    root_folder: str | None = None
    passed_checks: list[str] = Field(default_factory=list)
    foreign_owner_verified: bool = False
    api_cleanup_complete: bool = False
    cleanup_errors: list[str] = Field(default_factory=list)

    def persist(self, path: Path) -> None:
        path.write_text(self.model_dump_json(indent=2) + "\n")
        path.chmod(0o600)


def token(path: Path) -> str:
    value = json.loads(path.read_text())["id_token"]
    assert isinstance(value, str) and value, "A private Cognito ID-token session is required"
    return value


def subject(value: str) -> str:
    # Used only to reject accidentally reusing the same test identity. Actual
    # authorization is performed by both services' normal Cognito validators.
    encoded = value.split(".")[1]
    return json.loads(base64.urlsafe_b64decode(encoded + "=" * (-len(encoded) % 4)))["sub"]


def metadata() -> DatasetTableSchema:
    # Explicit caller-reviewed mapping for the synthetic input: descriptive
    # daily observations, not fabricated publication timestamps.
    return DatasetTableSchema.model_validate(
        {
            "frame_schema": {
                "columns": [
                    {
                        "name": "date",
                        "dtype": "timestamp[ns,UTC]",
                        "nullable": False,
                        "is_index": True,
                        "semantic": "Timestamp",
                        "transforms": [
                            {"kind": "ParseDateTime", "format": "%Y-%m-%d"},
                            {"kind": "AssumeTimezone", "tz": "UTC"},
                        ],
                    },
                    {
                        "name": "value",
                        "dtype": "float64",
                        "nullable": True,
                        "is_index": False,
                        "semantic": "Percent",
                        "unit": "percent per annum",
                    },
                ],
                "transforms": [{"kind": "PromoteIndex"}],
            },
            "key_fields": [],
            "dataframe_metadata": {
                "data_type": "user_dataset",
                "description": "Synthetic integration observations",
                "foundation": "Daily",
                "entity_columns": [],
                "source_capabilities": {
                    "range": "FullPayloadLocalSlice",
                    "future_rows": "PastOrPresentOnly",
                    "predecessor": "FullPayloadLocalSlice",
                    "availability_axis": "KnownAtIndex",
                },
            },
            "time_axis": {
                "meaning": "observation",
                "source_precision": "date",
                "source_timezone": "UTC",
                "assumed": True,
                "date_only_convention": "Descriptive calendar-date labels at midnight UTC",
            },
        }
    )


def mcp(state: State, bearer: str) -> Client:
    allowed = {"PATH", "HOME", "USER", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR"}
    env = {key: value for key, value in os.environ.items() if key in allowed}
    env.update(
        EPOCH_BACKEND_URL=state.backend_url, EPOCH_GRAPH_URL=state.graph_url, EPOCH_TOKEN=bearer
    )
    return Client(
        StdioServerParameters(command=sys.executable, args=["-m", "epoch_sdk.mcp"], env=env),
        read_timeout_seconds=120,
    )


async def preflight(state: State, bearer: str, path: Path) -> None:
    async with httpx.AsyncClient(timeout=20) as http:
        for headers in ({}, {"Authorization": "Bearer deliberately-invalid"}):
            denied = await http.get(state.backend_url + "/api/v1/files/limits", headers=headers)
            assert denied.status_code == 401
        headers = {"Authorization": "Bearer " + bearer}
        response = await http.get(state.backend_url + "/api/v1/health")
        response.raise_for_status()
        state.backend_git_sha = response.json()["git_sha"]
        response = await http.get(state.backend_url + "/api/v1/space", headers=headers)
        response.raise_for_status()
        assert response.headers["cache-control"] == "private, no-store"
        assert not SpacePage.model_validate(response.json()).items, "Storage namespace is not empty"
        response = await http.get(state.graph_url + "/health/custom", headers=headers)
        response.raise_for_status()
        health = response.json()
        assert health["status"] == "healthy"
        assert health["authentication"]["mode"] == "cognito_id_token_rs256"
        state.agent_git_sha = health["deployment"]["git_sha"]
        state.agent_revision_id = health["deployment"]["revision_id"]
        response = await http.get(state.graph_url + "/api/v1/agent-tools", headers=headers)
        response.raise_for_status()
        catalog = AgentToolsCatalog.model_validate(response.json())
        state.agent_catalogue_sha256 = hashlib.sha256(
            catalog.model_dump_json().encode()
        ).hexdigest()
    async with aclosing(
        AgentToolsClient.connect(
            graph_url=state.graph_url, backend_url=state.backend_url, token=bearer
        )
    ) as client:
        # Fixed synthetic bytes can reuse an existing native content identity.
        # Refuse a populated library before tracking anything as test-created.
        assert not (await client.list_files(limit=1, include_archived=True)).items
        assert not (await client.list_datasets(limit=1)).items
        assert not (await client.import_drafts()).items
        assert not await client.backend.studies_definitions.list_study_definitions(
            request_options=NO_RETRY
        )
        assert not await client.backend.studies_executions.list_executions(request_options=NO_RETRY)
        assert not await client.backend.model_artifacts.list_the_authenticated_users_immutable_model_artifacts(
            request_options=NO_RETRY
        )
    state.passed_checks.append(
        "normal Cognito authentication; missing/invalid tokens rejected; live EpochAI catalogue"
    )
    state.persist(path)


async def import_source(
    client: EpochClient, state: State, path: Path, content: bytes, name: str
) -> tuple[UserFileDescriptor, SavedDataset, bytes]:
    pending = await client.backend.user_files.init_file_upload(
        name=name,
        media_type="text/csv",
        size_bytes=len(content),
        content_sha256=hashlib.sha256(content).hexdigest(),
        request_options=NO_RETRY,
    )
    state.files.append(pending.file_ref)
    state.persist(path)
    try:
        await client.backend.user_files.complete_file_upload(
            pending.file_ref, upload_id=pending.upload_id, request_options=NO_RETRY
        )
        raise AssertionError("Incomplete upload was published")
    except ApiError as error:
        assert error.status_code in {400, 409}
    uploaded = await client.upload_file(content, name=name, media_type="text/csv")
    assert uploaded.file_ref == pending.file_ref
    assert (
        await client.upload_file(content, name=name, media_type="text/csv")
    ).file_ref == uploaded.file_ref
    await client.inspect_file(uploaded.file_ref, format="csv")
    request = StructuredImportRequest(
        file_ref=uploaded.file_ref,
        request_id=str(uuid4()),
        name=name,
        options=native_options(),
        metadata=metadata(),
        purpose=DatasetPurpose.STUDY_SOURCE,
    )
    draft = await client.prepare_dataset(request)
    state.drafts.append(draft.draft.draft_ref)
    state.persist(path)
    assert (await client.prepare_dataset(request)).draft.draft_ref == draft.draft.draft_ref
    raw = await client.download_dataset(draft.draft.draft_ref)
    review = DatasetReviewRequest.model_validate(
        {"decisions": [{"action": "save", "draft_ref": draft.draft.draft_ref, "name": name}]}
    )
    accepted = saved(await client.review_datasets(review))
    state.datasets.append(accepted.dataset_ref)
    state.persist(path)
    assert saved(await client.review_datasets(review)).dataset_ref == accepted.dataset_ref
    assert accepted.source_ref
    assert await client.download_dataset(accepted.dataset_ref) == raw
    assert hashlib.sha256(raw).hexdigest() == accepted.descriptor.content_sha256
    return uploaded, accepted, raw


async def execute(
    native: AgentToolsClient, state: State, path: Path, study_id: str, end: str
) -> str:
    execution_id = str(uuid4())
    state.executions.append(execution_id)
    state.persist(path)
    job = await native.execute(
        study_id,
        period=DatePeriodConfig(start=date(2020, 1, 1), end=date.fromisoformat(end)),
        execution_id=execution_id,
    )
    assert job.id == execution_id
    await completed(native, execution_id)
    return execution_id


async def create(state: State, bearer: str, path: Path) -> None:
    await preflight(state, bearer, path)
    async with (
        aclosing(
            EpochClient.connect(
                graph_url=state.graph_url, backend_url=state.backend_url, token=bearer
            )
        ) as client,
        aclosing(
            AgentToolsClient.connect(
                graph_url=state.graph_url, backend_url=state.backend_url, token=bearer
            )
        ) as native,
    ):
        uploaded, accepted, raw = await import_source(
            client,
            state,
            path,
            b"date,value\n2020-01-02,1.25\n2020-01-03,\n2020-01-06,2.5\n",
            "Space observed values",
        )
        table = arrow_file(raw)
        assert table.column("value").to_pylist() == [1.25, None, 2.5]
        assert (
            table.column("date").null_count == 0
            and str(table.column("date").type) == "timestamp[ns, tz=UTC]"
        )
        state.dataset_ref, state.source_ref = accepted.dataset_ref, accepted.source_ref
        state.prepared_sha256 = hashlib.sha256(raw).hexdigest()
        state.persist(path)
        root = await client.create_folder("Space integration " + state.run_id)
        state.folders.append(root.folder_ref)
        state.root_folder = root.folder_ref
        state.persist(path)
        child = await client.create_folder("Inputs", parent_folder_ref=root.folder_ref)
        state.folders.append(child.folder_ref)
        state.persist(path)
        source = (
            "data = custom_data(source_ref="
            + json.dumps(accepted.source_ref)
            + ", window=SourceWindow(start=EarliestAvailable, end=LatestAvailable))()\n"
        )
        study = await client.backend.studies_definitions.create_manual_study_definition(
            name="Space integration data study",
            description="Temporary integration test",
            data=DataOption.model_validate({"assets": []}),
            source=source
            + 'line(category="Space", title="Observed values")(key=index_of(data.value), values=data.value)\n',
            request_options=NO_RETRY,
        )
        state.studies.append(study.id)
        state.study_id = study.id
        state.persist(path)
        execution_id = await execute(native, state, path, study.id, "2020-01-06")
        await chart_values(native, execution_id)
        try:
            await client.delete_dataset(accepted.dataset_ref)
            raise AssertionError("Completed execution input was deleted")
        except ApiError as error:
            assert error.status_code == 409
        state.passed_checks.append(
            "SDK upload/import/review/full retrieval; exact dates/values/nulls; safe retries; real execution and retained input"
        )

        # Produce an actual small fitted model through the same native API.
        # No synthetic model payload or model-authoring service is used.
        rows = [
            f"{date(2020, 1, 1) + timedelta(days=i)},{(-1 - 0.05 * i) if i < 10 else (1 + 0.05 * i)}"
            for i in range(20)
        ]
        _, training, _ = await import_source(
            client,
            state,
            path,
            ("date,value\n" + "\n".join(rows) + "\n").encode(),
            "Space model training",
        )
        state.model_ref = "space_it_" + state.run_id[:12]
        model_source = (
            "data = custom_data(source_ref="
            + json.dumps(training.source_ref)
            + ", window=SourceWindow(start=EarliestAvailable, end=LatestAvailable))()\n"
        )
        model_source += f'fit = hmm_fit(model_ref="{state.model_ref}", num_states=2, random_state=42)(data.value)\n'
        model_source += (
            f'inference = hmm_infer(model_ref="{state.model_ref}", num_states=2)(data.value)\n'
        )
        model_source += 'p0 = inference.state_probs[0]\nline(category="HMM", title="Integration fitted model")(key=index_of(p0), values=p0)\n'
        model_study = await client.backend.studies_definitions.create_manual_study_definition(
            name="Space integration model fit",
            description="Temporary deterministic small HMM",
            data=DataOption.model_validate({"assets": []}),
            source=model_source,
            request_options=NO_RETRY,
        )
        state.studies.append(model_study.id)
        state.persist(path)
        await execute(native, state, path, model_study.id, "2020-01-20")
        model = await client.backend.model_artifacts.describe_one_authenticated_immutable_model_artifact(
            state.model_ref, request_options=NO_RETRY
        )
        state.model_sha256 = hashlib.sha256(model.model_dump_json().encode()).hexdigest()
        state.passed_checks.append(
            "real native HMM fit publishes an owner-authorized immutable model"
        )
        for item in [
            resource("file", uploaded.file_ref),
            resource("dataset", accepted.dataset_ref),
            resource("model", state.model_ref),
            resource("study", study.id),
        ]:
            await client.place_resource(item, folder_ref=child.folder_ref)
            state.placements.append(item)
            state.persist(path)
        async with mcp(state, bearer) as connection:
            names = {tool.name for tool in (await connection.list_tools()).tools}
            assert {
                "epoch_upload_file",
                "epoch_prepare_dataset",
                "epoch_space_browse",
                "epoch_execute",
            } <= names
            assert await read_content(connection, accepted.dataset_ref) == raw
            renamed = await call(
                connection,
                "epoch_space_update_folder",
                {"folder_ref": root.folder_ref, "name": "Renamed " + state.run_id},
            )
            assert (
                SpaceFolder.model_validate(renamed.structured_content).folder_ref == root.folder_ref
            )
            await call(
                connection,
                "epoch_space_place_resource",
                {
                    "resource": {"kind": "dataset", "ref": accepted.dataset_ref},
                    "folder_ref": root.folder_ref,
                    "name": "Selected observations",
                },
            )
            denied = await connection.call_tool(
                "epoch_space_delete_folder", {"folder_ref": root.folder_ref}
            )
            assert denied.is_error and denied.structured_content["http_status"] == 409
            large = "id,text\n9007199254740993," + "x" * (1024 * 1024 + 128) + "\n"
            response = await call(
                connection,
                "epoch_upload_file",
                {
                    "name": "large.csv",
                    "media_type": "text/csv",
                    "content_base64": base64.b64encode(large.encode()).decode(),
                },
            )
            large_file = UserFileDescriptor.model_validate(response.structured_content)
            state.files.append(large_file.file_ref)
            state.persist(path)
            request = StructuredImportRequest(
                file_ref=large_file.file_ref,
                request_id=str(uuid4()),
                name="Complete knowledge data",
                options=native_options(
                    [
                        DataSourceColumn(
                            name="id", dtype="uint64", nullable=False, is_index=False, transforms=[]
                        ),
                        DataSourceColumn(
                            name="text", dtype="utf8", nullable=False, is_index=False, transforms=[]
                        ),
                    ]
                ),
                metadata=None,
                purpose=DatasetPurpose.KNOWLEDGE,
            )
            prepared = await call(
                connection,
                "epoch_prepare_dataset",
                {"request": request.model_dump(mode="json", by_alias=True, exclude_unset=True)},
            )
            draft = StructuredImportResult.model_validate(prepared.structured_content)
            state.drafts.append(draft.draft.draft_ref)
            state.persist(path)
            preview = draft.preview.content
            assert preview.format == "table"
            assert preview.requires_download and not preview.rows
            decision = {
                "decisions": [
                    {
                        "action": "save",
                        "draft_ref": draft.draft.draft_ref,
                        "name": "Complete knowledge data",
                    }
                ]
            }
            result = await call(connection, "epoch_review_datasets", {"request": decision})
            knowledge = saved(DatasetReviewResponse.model_validate(result.structured_content))
            state.datasets.append(knowledge.dataset_ref)
            state.knowledge_ref = knowledge.dataset_ref
            state.persist(path)
            assert knowledge.source_ref is None
            again = await call(connection, "epoch_review_datasets", {"request": decision})
            assert (
                saved(DatasetReviewResponse.model_validate(again.structured_content)).dataset_ref
                == knowledge.dataset_ref
            )
            full = arrow_file(await read_content(connection, knowledge.dataset_ref))
            assert full.column("id")[0].as_py() == 9007199254740993
            assert full.column("text")[0].as_py() == "x" * (1024 * 1024 + 128)
            rejected = await client.prepare_dataset(
                request.model_copy(update={"request_id": str(uuid4())})
            )
            state.drafts.append(rejected.draft.draft_ref)
            state.persist(path)
            await client.review_datasets(
                DatasetReviewRequest.model_validate(
                    {"decisions": [{"action": "reject", "draft_ref": rejected.draft.draft_ref}]}
                )
            )
            try:
                await client.download_dataset(rejected.draft.draft_ref)
                raise AssertionError("Rejected draft remained readable")
            except ApiError as error:
                assert error.status_code == 409
        state.passed_checks.append(
            "live-catalogue MCP imports/reviews/reads oversized exact data; knowledge has no implicit study source; rejected drafts unavailable; folder moves preserve refs"
        )
        state.persist(path)


async def verify(state: State, bearer: str, path: Path) -> None:
    assert state.dataset_ref and state.knowledge_ref and state.study_id and state.model_ref
    async with aclosing(
        AgentToolsClient.connect(
            graph_url=state.graph_url, backend_url=state.backend_url, token=bearer
        )
    ) as client:
        raw = await client.download_dataset(state.dataset_ref)
        assert hashlib.sha256(raw).hexdigest() == state.prepared_sha256
        assert (await client.dataset(state.dataset_ref)).source_ref == state.source_ref
        model = await client.backend.model_artifacts.describe_one_authenticated_immutable_model_artifact(
            state.model_ref, request_options=NO_RETRY
        )
        assert hashlib.sha256(model.model_dump_json().encode()).hexdigest() == state.model_sha256
        page = await client.browse_space(folder_ref=state.root_folder, recursive=True)
        assert len(page.items) == 5
        async with mcp(state, bearer) as fresh:
            await fresh.list_tools()
            assert await read_content(fresh, state.dataset_ref) == raw
            full = arrow_file(await read_content(fresh, state.knowledge_ref))
            assert full.column("id")[0].as_py() == 9007199254740993
            assert full.column("text")[0].as_py() == "x" * (1024 * 1024 + 128)
            execution_id = str(uuid4())
            state.executions.append(execution_id)
            state.persist(path)
            args = {
                "study_id": state.study_id,
                "period": {"start": "2020-01-02", "end": "2020-01-06"},
                "execution_id": execution_id,
            }
            result = await call(fresh, "epoch_execute", args)
            assert JobListItem.model_validate(result.structured_content).id == execution_id
            await completed(client, execution_id)
            await chart_values(client, execution_id)
            duplicate = await fresh.call_tool("epoch_execute", args)
            assert duplicate.is_error and duplicate.structured_content["http_status"] == 409
            observed = await call(
                fresh, "epoch_status", {"kind": "execution", "execution_id": execution_id}
            )
            assert JobListItem.model_validate(observed.structured_content).status == "completed"
    state.passed_checks.append(
        "cold native restart with fresh local scratch and fresh MCP retains S3 data/model/folders/source refs and executes the saved study"
    )
    state.persist(path)


async def foreign(state: State, bearer: str, other: str, path: Path) -> None:
    assert subject(bearer) != subject(other), (
        "Cross-owner acceptance requires two distinct real Cognito subjects"
    )
    async with aclosing(
        AgentToolsClient.connect(
            graph_url=state.graph_url, backend_url=state.backend_url, token=other
        )
    ) as client:
        for item in state.placements:
            try:
                await client.place_resource(item)
                raise AssertionError("Foreign resource placement succeeded")
            except ApiError as error:
                assert error.status_code == 404
        try:
            await client.browse_space(folder_ref=state.root_folder)
            raise AssertionError("Foreign folder read succeeded")
        except ApiError as error:
            assert error.status_code == 404
    state.foreign_owner_verified = True
    state.passed_checks.append(
        "two real Cognito subjects reject cross-owner file/dataset/model/study placements and folder reads"
    )
    state.persist(path)


async def cleanup(state: State, bearer: str, path: Path) -> None:
    async with aclosing(
        AgentToolsClient.connect(
            graph_url=state.graph_url, backend_url=state.backend_url, token=bearer
        )
    ) as client:

        async def remove(label: str, operation: Awaitable[object]) -> None:
            try:
                await operation
            except ApiError as error:
                if error.status_code != 404:
                    state.cleanup_errors.append(label + ":" + str(error.status_code))
            except Exception as error:  # noqa: BLE001 - Attempt all remaining cleanup after any failure.
                state.cleanup_errors.append(label + ":" + type(error).__name__)
            state.persist(path)

        for item in reversed(state.placements):
            await remove("unplace", client.unplace_resource(item))
        for identifier in reversed(state.executions):
            await remove(
                "execution",
                client.backend.studies_executions.delete_execution_by_id(
                    identifier, request_options=NO_RETRY
                ),
            )
        for identifier in reversed(state.studies):
            await remove(
                "study",
                client.backend.studies_definitions.delete_a_study_definition_and_all_linked_executions(
                    identifier, request_options=NO_RETRY
                ),
            )
        for draft in (await client.import_drafts()).items:
            if draft.draft_ref in state.drafts:
                await remove(
                    "draft",
                    client.review_datasets(
                        DatasetReviewRequest.model_validate(
                            {"decisions": [{"action": "reject", "draft_ref": draft.draft_ref}]}
                        )
                    ),
                )
        for identifier in reversed(state.datasets):
            await remove("dataset", client.delete_dataset(identifier))
        for identifier in reversed(state.files):
            await remove("file", client.delete_file(identifier))
        for identifier in reversed(state.folders):
            await remove("folder", client.delete_folder(identifier))
        assert not (await client.list_files()).items
        assert not (await client.list_datasets()).items
        assert not (await client.browse_space(recursive=True)).items
        assert not await client.backend.studies_definitions.list_study_definitions(
            request_options=NO_RETRY
        )
        assert not await client.backend.studies_executions.list_executions(request_options=NO_RETRY)
        state.api_cleanup_complete = not state.cleanup_errors
        state.persist(path)
    assert state.api_cleanup_complete, (
        "API cleanup errors are recorded; destroy the disposable namespace"
    )


async def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=["create", "verify", "foreign", "cleanup"])
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--backend-url")
    parser.add_argument("--graph-url")
    parser.add_argument("--token-file", type=Path, required=True)
    parser.add_argument("--other-token-file", type=Path)
    args = parser.parse_args()
    if args.phase == "create":
        assert not args.state.exists()
        assert args.backend_url and args.graph_url
        state = State(run_id=uuid4().hex, backend_url=args.backend_url, graph_url=args.graph_url)
        state.persist(args.state)
    else:
        state = State.model_validate_json(args.state.read_text())
    bearer = token(args.token_file)
    if args.phase == "foreign":
        assert args.other_token_file
        await foreign(state, bearer, token(args.other_token_file), args.state)
    else:
        await globals()[args.phase](state, bearer, args.state)
    print(
        json.dumps(
            {
                "phase": args.phase,
                "passed_checks": state.passed_checks,
                "foreign_owner_verified": state.foreign_owner_verified,
                "api_cleanup_complete": state.api_cleanup_complete,
            }
        )
    )


if __name__ == "__main__":
    asyncio.run(main())
