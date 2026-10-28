"""Exercise installed SDK and fresh stdio MCP against the native Files HTTP gate.

Run the Backend epoch_personal_files_http_test with EPOCH_SPACE_FULL_HTTP=1 and
EPOCH_FILES_SDK_TEST_RECEIPT pointing to a private temporary file. This driver
reads that receipt and signals .done in finally. All resource/study operations
use the real native service. A controlled HTTP service supplies only the frozen,
source-owned specialist catalogue needed by the existing MCP tools/list path;
it cannot implement resource, execution or specialist operations.
"""
from __future__ import annotations

import argparse
import asyncio
import base64
import hashlib
import importlib.metadata
import json
import os
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from uuid import uuid4

import pyarrow as pa
from mcp import Client
from mcp.client.stdio import StdioServerParameters
from mcp.types import BlobResourceContents, CallToolResult, ResourceLink
from pydantic import BaseModel, ConfigDict
from stratifyx import DataOption, DatePeriodConfig
from stratifyx.core.api_error import ApiError
from stratifyx.types import (
    DatasetReviewRequest,
    DatasetReviewResponse,
    DatasetTableSchema,
    DataSourceColumn,
    JobListItem,
    SavedDataset,
    SpaceFolder,
    SpacePage,
    SpaceResourceRef,
    StructuredImportOptions,
    StructuredImportRequest,
    StructuredImportResult,
    UserFileDescriptor,
)

from epoch_sdk.agent_tools import AgentToolsClient
from epoch_sdk.research import EpochClient

SDK_ROOT = Path(__file__).resolve().parents[4]


class Receipt(BaseModel):
    model_config = ConfigDict(extra="forbid")
    base_url: str
    alice: str
    bob: str
    study_metadata: DatasetTableSchema
    model_ref: str | None


class Evidence(BaseModel):
    model_config = ConfigDict(extra="forbid")
    scope: str = "isolated native HTTP, installed SDK, fresh stdio MCP"
    specialist_catalogue_is_a_fixture: bool = True
    native_sdk_version: str
    epoch_sdk_version: str
    backend_git_sha: str
    sdk_git_sha: str
    study_dataset_ref: str
    knowledge_dataset_ref: str
    source_ref: str
    study_id: str
    model_ref: str
    sdk_execution_id: str
    mcp_execution_id: str
    prepared_sha256: str
    oversized_text_bytes: int
    passed_checks: list[str]


class CatalogueServer:
    def __init__(self, receipt: Receipt):
        content = json.dumps(json.loads((SDK_ROOT / "contracts/agent-tools-native.json").read_text())["catalog"]).encode()
        tokens = {"Bearer " + receipt.alice, "Bearer " + receipt.bob}
        self.requests = 0
        owner = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                assert self.path == "/api/v1/agent-tools", "A graph operation was unexpectedly invoked"
                assert self.headers.get("Authorization") in tokens
                owner.requests += 1
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)

            def log_message(self, *args):
                pass

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)

    def __enter__(self):
        self.thread.start()
        return "http://127.0.0.1:" + str(self.server.server_port)

    def __exit__(self, *args):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()


def native_options(columns: list[DataSourceColumn] | None = None) -> StructuredImportOptions:
    return StructuredImportOptions(
        format="csv", sheet=None, json_pointer=None, delimiter=",", header=True,
        null_values=[""], columns=columns or [],
    )


def resource(kind: str, ref: str) -> SpaceResourceRef:
    return SpaceResourceRef.model_validate({"kind": kind, "ref": ref})


def arrow_file(content: bytes) -> pa.Table:
    return pa.ipc.open_file(pa.BufferReader(content)).read_all()


def saved(review: DatasetReviewResponse) -> SavedDataset:
    item = review.results[0]
    assert item.status == "saved", "Review did not publish a dataset"
    return item.dataset


async def completed(client: AgentToolsClient, identifier: str) -> JobListItem:
    deadline = time.monotonic() + 90
    while time.monotonic() < deadline:
        result = await client.execution(identifier)
        if result.status == "completed":
            return result
        assert result.status not in {"failed", "cancelled"}, result.model_dump_json()
        await asyncio.sleep(0.1)
    raise AssertionError("Native study execution did not complete")


async def chart_values(client: AgentToolsClient, execution_id: str) -> None:
    # "ALL" is the native assetless report scope. Chart.category is a display
    # section label and must not replace that physical data scope.
    dashboard = await client.dashboard(execution_id, category="ALL")
    assert dashboard.charts
    chart = dashboard.charts[0]
    data = bytearray()
    async with client.backend.studies_dashboard.with_raw_response.get_chart_table_data_as_arrow_ipc(
        execution_id, chart.data_id, category="ALL", request_options={"max_retries": 0},
    ) as response:
        async for chunk in response.data:
            data.extend(chunk)
    raw = bytes(data)
    reader = pa.ipc.open_file(pa.BufferReader(raw)) if raw.startswith(b"ARROW1") else pa.ipc.open_stream(pa.BufferReader(raw))
    table = reader.read_all()
    assert any(
        [value for value in column.to_pylist() if value is not None] == [1.25, 2.5]
        and column.null_count == 1
        for column in table.columns if pa.types.is_floating(column.type)
    ), "Delivered chart values/nulls differ from the accepted dataset"


async def call(mcp: Client, name: str, arguments: dict) -> CallToolResult:
    result = await mcp.call_tool(name, arguments)
    assert not result.is_error, result
    return result


async def read_content(mcp: Client, dataset_ref: str) -> bytes:
    link = await call(mcp, "epoch_dataset_content", {"dataset_ref": dataset_ref})
    assert isinstance(link.content[0], ResourceLink)
    result = await mcp.read_resource(link.content[0].uri)
    assert isinstance(result.contents[0], BlobResourceContents)
    return base64.b64decode(result.contents[0].blob, validate=True)


def mcp_process(receipt: Receipt, graph_url: str, *, token: str | None = None) -> Client:
    environment = os.environ.copy()
    environment.update(EPOCH_BACKEND_URL=receipt.base_url, EPOCH_GRAPH_URL=graph_url,
                       EPOCH_TOKEN=token or receipt.alice)
    return Client(StdioServerParameters(
        command=sys.executable, args=["-m", "epoch_sdk.mcp"], env=environment,
    ), read_timeout_seconds=90)


async def scenario(receipt: Receipt, graph_url: str, backend: Path) -> Evidence:
    assert receipt.model_ref, "Enable EPOCH_SPACE_FULL_HTTP for model/study acceptance"
    notebook = EpochClient.connect(graph_url=graph_url, backend_url=receipt.base_url, token=receipt.alice)
    native = AgentToolsClient.connect(graph_url=graph_url, backend_url=receipt.base_url, token=receipt.alice)
    bob = AgentToolsClient.connect(graph_url=graph_url, backend_url=receipt.base_url, token=receipt.bob)
    checks: list[str] = []
    try:
        csv = b"date,value\n2020-01-02,1.25\n2020-01-03,\n2020-01-06,2.5\n"
        pending = await notebook.backend.user_files.init_file_upload(
            name="observations.csv", media_type="text/csv", size_bytes=len(csv),
            content_sha256=hashlib.sha256(csv).hexdigest(), request_options={"max_retries": 0},
        )
        try:
            await notebook.backend.user_files.complete_file_upload(
                pending.file_ref, upload_id=pending.upload_id, request_options={"max_retries": 0},
            )
            raise AssertionError("An incomplete upload was published")
        except ApiError as error:
            assert error.status_code in {400, 409}
        uploaded = await notebook.upload_file(csv, name="observations.csv", media_type="text/csv")
        assert uploaded.file_ref == pending.file_ref
        assert (await notebook.upload_file(csv, name="observations.csv", media_type="text/csv")).file_ref == uploaded.file_ref
        checks.append("incomplete upload fails; retry and completion preserve one file identity")
        await notebook.inspect_file(uploaded.file_ref, format="csv")
        request = StructuredImportRequest(
            file_ref=uploaded.file_ref, request_id=str(uuid4()), name="Observed values",
            options=native_options(), metadata=receipt.study_metadata, purpose="study_source",
        )
        draft = await notebook.prepare_dataset(request)
        assert (await notebook.prepare_dataset(request)).draft.draft_ref == draft.draft.draft_ref
        raw = await notebook.download_dataset(draft.draft.draft_ref)
        table = arrow_file(raw)
        assert table.num_rows == 3 and table.column("value").to_pylist() == [1.25, None, 2.5]
        assert table.column("date").type == pa.timestamp("ns", "UTC")
        review = DatasetReviewRequest.model_validate({"decisions": [
            {"action": "save", "draft_ref": draft.draft.draft_ref, "name": "Observed values"},
        ]})
        accepted = saved(await notebook.review_datasets(review))
        assert accepted.source_ref
        assert saved(await notebook.review_datasets(review)).dataset_ref == accepted.dataset_ref
        assert await notebook.download_dataset(accepted.dataset_ref) == raw
        assert hashlib.sha256(raw).hexdigest() == accepted.descriptor.content_sha256
        checks.append("SDK upload/import/preview/review/full retrieval preserves dates, values, nulls and identity")
        root = await notebook.create_folder("Phase 1")
        child = await notebook.create_folder("Inputs", parent_folder_ref=root.folder_ref)
        await notebook.place_resource(resource("file", uploaded.file_ref), folder_ref=child.folder_ref)
        await notebook.place_resource(resource("dataset", accepted.dataset_ref), folder_ref=child.folder_ref)
        await notebook.place_resource(resource("model", receipt.model_ref), folder_ref=child.folder_ref)
        code = (
            "data = custom_data(source_ref=" + json.dumps(accepted.source_ref) +
            ", window=SourceWindow(start=EarliestAvailable, end=LatestAvailable))()\n"
            'line(category="Space", title="Saved values")(key=index_of(data.value), values=data.value)\n'
        )
        study = await notebook.backend.studies_definitions.create_manual_study_definition(
            name="Saved data study", description="Deterministic Phase 1 fixture",
            data=DataOption.model_validate({"assets": []}), source=code, request_options={"max_retries": 0},
        )
        await notebook.place_resource(resource("study", study.id), folder_ref=child.folder_ref)
        first = await native.execute(study.id, period=DatePeriodConfig(start="2020-01-02", end="2020-01-06"))
        await completed(native, first.id)
        await chart_values(native, first.id)
        checks.append("accepted source executes through the real native study API and returns matching chart values")
        try:
            await notebook.delete_dataset(accepted.dataset_ref)
            raise AssertionError("An execution's retained input was deleted")
        except ApiError as error:
            assert error.status_code == 409
        checks.append("completed execution retains its exact input dataset")
        async with mcp_process(receipt, graph_url) as mcp:
            names = {tool.name for tool in (await mcp.list_tools()).tools}
            assert {"epoch_upload_file", "epoch_prepare_dataset", "epoch_space_browse", "epoch_execute"} <= names
            page = await call(mcp, "epoch_space_browse", {"folder_ref": root.folder_ref, "recursive": True})
            assert len(SpacePage.model_validate(page.structured_content).items) == 5
            assert await read_content(mcp, accepted.dataset_ref) == raw
            changed = await call(mcp, "epoch_space_update_folder", {"folder_ref": root.folder_ref, "name": "Renamed phase 1"})
            assert SpaceFolder.model_validate(changed.structured_content).folder_ref == root.folder_ref
            await call(mcp, "epoch_space_place_resource", {
                "resource": {"kind": "dataset", "ref": accepted.dataset_ref},
                "folder_ref": root.folder_ref, "name": "Selected observations",
            })
            nonempty = await mcp.call_tool("epoch_space_delete_folder", {"folder_ref": root.folder_ref})
            assert nonempty.is_error
            large = "id,text\n9007199254740993," + "x" * (1024 * 1024 + 128) + "\n"
            file_call = await call(mcp, "epoch_upload_file", {"name": "large.csv", "media_type": "text/csv",
                "content_base64": base64.b64encode(large.encode()).decode()})
            large_file = UserFileDescriptor.model_validate(file_call.structured_content)
            knowledge_request = StructuredImportRequest(
                file_ref=large_file.file_ref, request_id=str(uuid4()), name="Complete knowledge data",
                options=native_options([
                    DataSourceColumn(name="id", dtype="uint64", nullable=False, is_index=False, transforms=[]),
                    DataSourceColumn(name="text", dtype="utf8", nullable=False, is_index=False, transforms=[]),
                ]), metadata=None, purpose="knowledge",
            )
            prepared_call = await call(mcp, "epoch_prepare_dataset", {"request": knowledge_request.model_dump(mode="json", by_alias=True, exclude_unset=True)})
            knowledge_draft = StructuredImportResult.model_validate(prepared_call.structured_content)
            assert knowledge_draft.preview.content.requires_download
            decisions = {"decisions": [{"action": "save", "draft_ref": knowledge_draft.draft.draft_ref, "name": "Complete knowledge data"}]}
            accepted_call = await call(mcp, "epoch_review_datasets", {"request": decisions})
            knowledge = saved(DatasetReviewResponse.model_validate(accepted_call.structured_content))
            assert knowledge.source_ref is None
            repeated = await call(mcp, "epoch_review_datasets", {"request": decisions})
            assert saved(DatasetReviewResponse.model_validate(repeated.structured_content)).dataset_ref == knowledge.dataset_ref
            complete = arrow_file(await read_content(mcp, knowledge.dataset_ref))
            assert complete.column("id")[0].as_py() == 9007199254740993
            assert len(complete.column("text")[0].as_py()) == 1024 * 1024 + 128
            checks.append("MCP imports, reviews and fully reads a row beyond preview limits without integer/text loss")
            checks.append("knowledge data receives no study source; repeated acceptance creates no duplicate dataset")
            rejected_request = knowledge_request.model_copy(update={"request_id": str(uuid4())})
            reject_call = await call(mcp, "epoch_prepare_dataset", {"request": rejected_request.model_dump(mode="json", by_alias=True, exclude_unset=True)})
            rejected = StructuredImportResult.model_validate(reject_call.structured_content)
            await call(mcp, "epoch_review_datasets", {"request": {"decisions": [{"action": "reject", "draft_ref": rejected.draft.draft_ref}]}})
            try:
                await notebook.download_dataset(rejected.draft.draft_ref)
                raise AssertionError("A rejected draft remained readable")
            except ApiError as error:
                assert error.status_code == 409
        async with mcp_process(receipt, graph_url) as fresh:
            listing = await call(fresh, "epoch_list_datasets", {})
            assert any(item["dataset_ref"] == accepted.dataset_ref for item in listing.structured_content["items"])
            assert await read_content(fresh, accepted.dataset_ref) == raw
            execution_id = str(uuid4())
            args = {"study_id": study.id, "period": {"start": "2020-01-02", "end": "2020-01-06"}, "execution_id": execution_id}
            executed = await call(fresh, "epoch_execute", args)
            mcp_job = JobListItem.model_validate(executed.structured_content)
            assert mcp_job.id == execution_id
            await completed(native, execution_id)
            await chart_values(native, execution_id)
            again = await fresh.call_tool("epoch_execute", args)
            assert again.is_error and again.structured_content["http_status"] == 409
            observed = await call(fresh, "epoch_status", {"kind": "execution", "execution_id": execution_id})
            assert JobListItem.model_validate(observed.structured_content).id == execution_id
            checks.append("fresh stdio MCP rediscovers exact saved refs, reads full data and executes the saved study after folder moves")
        for kind, ref in [("file", uploaded.file_ref), ("dataset", accepted.dataset_ref), ("model", receipt.model_ref), ("study", study.id)]:
            try:
                await bob.place_resource(resource(kind, ref))
                raise AssertionError("A foreign resource was placed")
            except ApiError as error:
                assert error.status_code == 404
        try:
            await bob.browse_space(folder_ref=root.folder_ref)
            raise AssertionError("A foreign folder was read")
        except ApiError as error:
            assert error.status_code == 404
        checks.append("real owner checks reject foreign files, datasets, models, studies and folders")
        return Evidence(
            native_sdk_version=importlib.metadata.version("stratifyx"),
            epoch_sdk_version=importlib.metadata.version("epoch-sdk"),
            backend_git_sha=(await asyncio.to_thread(subprocess.check_output, ["git", "rev-parse", "HEAD"], cwd=backend, text=True)).strip(),
            sdk_git_sha=(await asyncio.to_thread(subprocess.check_output, ["git", "rev-parse", "HEAD"], cwd=SDK_ROOT, text=True)).strip(),
            study_dataset_ref=accepted.dataset_ref, knowledge_dataset_ref=knowledge.dataset_ref,
            source_ref=accepted.source_ref, study_id=study.id, model_ref=receipt.model_ref,
            sdk_execution_id=first.id, mcp_execution_id=execution_id,
            prepared_sha256=hashlib.sha256(raw).hexdigest(), oversized_text_bytes=1024 * 1024 + 128,
            passed_checks=checks,
        )
    finally:
        await notebook.aclose()
        await native.aclose()
        await bob.aclose()


async def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--backend", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        deadline = time.monotonic() + 40
        while not args.receipt.exists() and time.monotonic() < deadline:
            await asyncio.sleep(0.1)
        receipt = Receipt.model_validate_json(args.receipt.read_text())
        with CatalogueServer(receipt) as graph_url:
            evidence = await scenario(receipt, graph_url, args.backend)
        args.output.write_text(evidence.model_dump_json(indent=2) + "\n")
        print(evidence.model_dump_json(indent=2))
    finally:
        Path(str(args.receipt) + ".done").touch()


if __name__ == "__main__":
    asyncio.run(main())
