"""Exercise installed SDK and fresh SDK client against the native Files HTTP gate.

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
from pydantic import BaseModel, ConfigDict
from stratifyx import DataOption, DatePeriodConfig
from stratifyx.core.api_error import ApiError
from stratifyx.types import DatasetReviewRequest, DatasetReviewResponse, DatasetTableSchema, DataSourceColumn, JobListItem, SavedDataset, SpaceFolder, SpacePage, SpaceResourceRef, StructuredImportOptions, StructuredImportRequest, StructuredImportResult, UserFileDescriptor
from epoch_sdk.research import EpochClient
SDK_ROOT = Path(__file__).resolve().parents[4]

class Receipt(BaseModel):
    model_config = ConfigDict(extra='forbid')
    base_url: str
    alice: str
    bob: str
    study_metadata: DatasetTableSchema
    model_ref: str | None

class Evidence(BaseModel):
    model_config = ConfigDict(extra='forbid')
    scope: str = 'isolated native HTTP, installed SDK, fresh SDK client'
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
    reopened_execution_id: str
    prepared_sha256: str
    oversized_text_bytes: int
    passed_checks: list[str]

def native_options(columns: list[DataSourceColumn] | None=None) -> StructuredImportOptions:
    return StructuredImportOptions(format='csv', sheet=None, json_pointer=None, delimiter=',', header=True, null_values=[''], columns=columns or [])

def resource(kind: str, ref: str) -> SpaceResourceRef:
    return SpaceResourceRef.model_validate({'kind': kind, 'ref': ref})

def arrow_file(content: bytes) -> pa.Table:
    return pa.ipc.open_file(pa.BufferReader(content)).read_all()

def saved(review: DatasetReviewResponse) -> SavedDataset:
    item = review.results[0]
    assert item.status == 'saved', 'Review did not publish a dataset'
    return item.dataset

async def completed(client: EpochClient, identifier: str) -> JobListItem:
    deadline = time.monotonic() + 90
    while time.monotonic() < deadline:
        result = await client.execution(identifier)
        if result.status == 'completed':
            return result
        assert result.status not in {'failed', 'cancelled'}, result.model_dump_json()
        await asyncio.sleep(0.1)
    raise AssertionError('Native study execution did not complete')

async def chart_values(client: EpochClient, execution_id: str) -> None:
    dashboard = await client.dashboard(execution_id, category='ALL')
    assert dashboard.charts
    chart = dashboard.charts[0]
    data = bytearray()
    async with client.backend.studies_dashboard.with_raw_response.get_chart_table_data_as_arrow_ipc(execution_id, chart.data_id, category='ALL', request_options={'max_retries': 0}) as response:
        async for chunk in response.data:
            data.extend(chunk)
    raw = bytes(data)
    reader = pa.ipc.open_file(pa.BufferReader(raw)) if raw.startswith(b'ARROW1') else pa.ipc.open_stream(pa.BufferReader(raw))
    table = reader.read_all()
    assert any(([value for value in column.to_pylist() if value is not None] == [1.25, 2.5] and column.null_count == 1 for column in table.columns if pa.types.is_floating(column.type))), 'Delivered chart values/nulls differ from the accepted dataset'

async def native_execute(client, study_id, *, period, execution_id=None):
    arguments = {"id": study_id, "period": period, "request_options": {"max_retries": 0}}
    if execution_id is not None:
        arguments["execution_id"] = execution_id
    accepted = await client.backend.studies_executions.start_execute_a_study(**arguments)
    return await client.execution(accepted.id)


async def scenario(receipt: Receipt, graph_url: str, backend: Path) -> Evidence:
    assert receipt.model_ref, 'Enable EPOCH_SPACE_FULL_HTTP for model/study acceptance'
    notebook = EpochClient.connect(graph_url=graph_url, backend_url=receipt.base_url, token=receipt.alice)
    native = EpochClient.connect(graph_url=graph_url, backend_url=receipt.base_url, token=receipt.alice)
    bob = EpochClient.connect(graph_url=graph_url, backend_url=receipt.base_url, token=receipt.bob)
    checks: list[str] = []
    try:
        csv = b'date,value\n2020-01-02,1.25\n2020-01-03,\n2020-01-06,2.5\n'
        pending = await notebook.backend.user_files.init_file_upload(name='observations.csv', media_type='text/csv', size_bytes=len(csv), content_sha256=hashlib.sha256(csv).hexdigest(), request_options={'max_retries': 0})
        try:
            await notebook.backend.user_files.complete_file_upload(pending.file_ref, upload_id=pending.upload_id, request_options={'max_retries': 0})
            raise AssertionError('An incomplete upload was published')
        except ApiError as error:
            assert error.status_code in {400, 409}
        uploaded = await notebook.upload_file(csv, name='observations.csv', media_type='text/csv')
        assert uploaded.file_ref == pending.file_ref
        assert (await notebook.upload_file(csv, name='observations.csv', media_type='text/csv')).file_ref == uploaded.file_ref
        checks.append('incomplete upload fails; retry and completion preserve one file identity')
        await notebook.inspect_file(uploaded.file_ref, format='csv')
        request = StructuredImportRequest(file_ref=uploaded.file_ref, request_id=str(uuid4()), name='Observed values', options=native_options(), metadata=receipt.study_metadata, purpose='study_source')
        draft = await notebook.prepare_dataset(request)
        assert (await notebook.prepare_dataset(request)).draft.draft_ref == draft.draft.draft_ref
        raw = await notebook.download_dataset(draft.draft.draft_ref)
        table = arrow_file(raw)
        assert table.num_rows == 3 and table.column('value').to_pylist() == [1.25, None, 2.5]
        assert table.column('date').type == pa.timestamp('ns', 'UTC')
        review = DatasetReviewRequest.model_validate({'decisions': [{'action': 'save', 'draft_ref': draft.draft.draft_ref, 'name': 'Observed values'}]})
        accepted = saved(await notebook.review_datasets(review))
        assert accepted.source_ref
        assert saved(await notebook.review_datasets(review)).dataset_ref == accepted.dataset_ref
        assert await notebook.download_dataset(accepted.dataset_ref) == raw
        assert hashlib.sha256(raw).hexdigest() == accepted.descriptor.content_sha256
        checks.append('SDK upload/import/preview/review/full retrieval preserves dates, values, nulls and identity')
        root = await notebook.create_folder('Phase 1')
        child = await notebook.create_folder('Inputs', parent_folder_ref=root.folder_ref)
        await notebook.place_resource(resource('file', uploaded.file_ref), folder_ref=child.folder_ref)
        await notebook.place_resource(resource('dataset', accepted.dataset_ref), folder_ref=child.folder_ref)
        await notebook.place_resource(resource('model', receipt.model_ref), folder_ref=child.folder_ref)
        code = 'data = custom_data(source_ref=' + json.dumps(accepted.source_ref) + ', window=SourceWindow(start=EarliestAvailable, end=LatestAvailable))()\nline(category="Space", title="Saved values")(key=index_of(data.value), values=data.value)\n'
        study = await notebook.backend.studies_definitions.create_manual_study_definition(name='Saved data study', description='Deterministic Phase 1 fixture', data=DataOption.model_validate({'assets': []}), source=code, request_options={'max_retries': 0})
        await notebook.place_resource(resource('study', study.id), folder_ref=child.folder_ref)
        first = await native_execute(native, study.id, period=DatePeriodConfig(start='2020-01-02', end='2020-01-06'))
        await completed(native, first.id)
        await chart_values(native, first.id)
        checks.append('accepted source executes through the real native study API and returns matching chart values')
        try:
            await notebook.delete_dataset(accepted.dataset_ref)
            raise AssertionError("An execution's retained input was deleted")
        except ApiError as error:
            assert error.status_code == 409
        checks.append('completed execution retains its exact input dataset')
        async with EpochClient.connect(backend_url=receipt.base_url, graph_url=graph_url, token=receipt.alice) as reader:
            page = await reader.browse_space(folder_ref=root.folder_ref, recursive=True)
            assert len(SpacePage.model_validate(page).items) == 5
            assert await reader.download_dataset(accepted.dataset_ref) == raw
            changed = await reader.update_folder(folder_ref=root.folder_ref, name='Renamed phase 1')
            assert SpaceFolder.model_validate(changed).folder_ref == root.folder_ref
            await reader.place_resource(resource=SpaceResourceRef.model_validate({'kind': 'dataset', 'ref': accepted.dataset_ref}), folder_ref=root.folder_ref, name='Selected observations')
            try:
                await reader.delete_folder(folder_ref=root.folder_ref)
                raise AssertionError('Expected a conflict')
            except ApiError as error:
                assert error.status_code == 409
            large = 'id,text\n9007199254740993,' + 'x' * (1024 * 1024 + 128) + '\n'
            file_call = await reader.upload_file(content=large.encode(), name='large.csv', media_type='text/csv')
            large_file = UserFileDescriptor.model_validate(file_call)
            knowledge_request = StructuredImportRequest(file_ref=large_file.file_ref, request_id=str(uuid4()), name='Complete knowledge data', options=native_options([DataSourceColumn(name='id', dtype='uint64', nullable=False, is_index=False, transforms=[]), DataSourceColumn(name='text', dtype='utf8', nullable=False, is_index=False, transforms=[])]), metadata=None, purpose='knowledge')
            prepared_call = await reader.prepare_dataset(request=StructuredImportRequest.model_validate(knowledge_request.model_dump(mode='json', by_alias=True, exclude_unset=True)))
            knowledge_draft = StructuredImportResult.model_validate(prepared_call)
            assert knowledge_draft.preview.content.requires_download
            decisions = {'decisions': [{'action': 'save', 'draft_ref': knowledge_draft.draft.draft_ref, 'name': 'Complete knowledge data'}]}
            accepted_call = await reader.review_datasets(request=DatasetReviewRequest.model_validate(decisions))
            knowledge = saved(DatasetReviewResponse.model_validate(accepted_call))
            assert knowledge.source_ref is None
            repeated = await reader.review_datasets(request=DatasetReviewRequest.model_validate(decisions))
            assert saved(DatasetReviewResponse.model_validate(repeated)).dataset_ref == knowledge.dataset_ref
            complete = arrow_file(await reader.download_dataset(knowledge.dataset_ref))
            assert complete.column('id')[0].as_py() == 9007199254740993
            assert len(complete.column('text')[0].as_py()) == 1024 * 1024 + 128
            checks.append('SDK imports, reviews and fully reads a row beyond preview limits without integer/text loss')
            checks.append('knowledge data receives no study source; repeated acceptance creates no duplicate dataset')
            rejected_request = knowledge_request.model_copy(update={'request_id': str(uuid4())})
            reject_call = await reader.prepare_dataset(request=StructuredImportRequest.model_validate(rejected_request.model_dump(mode='json', by_alias=True, exclude_unset=True)))
            rejected = StructuredImportResult.model_validate(reject_call)
            await reader.review_datasets(request=DatasetReviewRequest.model_validate({'decisions': [{'action': 'reject', 'draft_ref': rejected.draft.draft_ref}]}))
            try:
                await notebook.download_dataset(rejected.draft.draft_ref)
                raise AssertionError('A rejected draft remained readable')
            except ApiError as error:
                assert error.status_code == 409
        async with EpochClient.connect(backend_url=receipt.base_url, graph_url=graph_url, token=receipt.alice) as fresh:
            listing = await fresh.list_datasets()
            assert any((item['dataset_ref'] == accepted.dataset_ref for item in listing.items))
            assert await fresh.download_dataset(accepted.dataset_ref) == raw
            execution_id = str(uuid4())
            args = {'study_id': study.id, 'period': {'start': '2020-01-02', 'end': '2020-01-06'}, 'execution_id': execution_id}
            executed = await native_execute(fresh, **native_execution_args(args))
            reopened_job = JobListItem.model_validate(executed)
            assert reopened_job.id == execution_id
            await completed(native, execution_id)
            await chart_values(native, execution_id)
            try:
                await native_execute(fresh, **native_execution_args(args))
                raise AssertionError('Expected a conflict')
            except ApiError as error:
                assert error.status_code == 409
            observed = await fresh.execution(execution_id=execution_id)
            assert JobListItem.model_validate(observed).id == execution_id
            checks.append('fresh SDK client rediscovers exact saved refs, reads full data and executes the saved study after folder moves')
        for kind, ref in [('file', uploaded.file_ref), ('dataset', accepted.dataset_ref), ('model', receipt.model_ref), ('study', study.id)]:
            try:
                await bob.place_resource(resource(kind, ref))
                raise AssertionError('A foreign resource was placed')
            except ApiError as error:
                assert error.status_code == 404
        try:
            await bob.browse_space(folder_ref=root.folder_ref)
            raise AssertionError('A foreign folder was read')
        except ApiError as error:
            assert error.status_code == 404
        checks.append('real owner checks reject foreign files, datasets, models, studies and folders')
        return Evidence(native_sdk_version=importlib.metadata.version('stratifyx'), epoch_sdk_version=importlib.metadata.version('epoch-sdk'), backend_git_sha=(await asyncio.to_thread(subprocess.check_output, ['git', 'rev-parse', 'HEAD'], cwd=backend, text=True)).strip(), sdk_git_sha=(await asyncio.to_thread(subprocess.check_output, ['git', 'rev-parse', 'HEAD'], cwd=SDK_ROOT, text=True)).strip(), study_dataset_ref=accepted.dataset_ref, knowledge_dataset_ref=knowledge.dataset_ref, source_ref=accepted.source_ref, study_id=study.id, model_ref=receipt.model_ref, sdk_execution_id=first.id, reopened_execution_id=execution_id, prepared_sha256=hashlib.sha256(raw).hexdigest(), oversized_text_bytes=1024 * 1024 + 128, passed_checks=checks)
    finally:
        await notebook.aclose()
        await native.aclose()
        await bob.aclose()

async def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receipt', type=Path, required=True)
    parser.add_argument('--backend', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        deadline = time.monotonic() + 40
        while not args.receipt.exists() and time.monotonic() < deadline:
            await asyncio.sleep(0.1)
        receipt = Receipt.model_validate_json(args.receipt.read_text())
        graph_url = 'http://127.0.0.1:2024'
        evidence = await scenario(receipt, graph_url, args.backend)
        args.output.write_text(evidence.model_dump_json(indent=2) + '\n')
        print(evidence.model_dump_json(indent=2))
    finally:
        Path(str(args.receipt) + '.done').touch()

def native_execution_args(arguments):
    return {**arguments, "period": DatePeriodConfig.model_validate(arguments["period"])}

if __name__ == '__main__':
    asyncio.run(main())
