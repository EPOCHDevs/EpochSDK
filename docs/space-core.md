# Persistent Files and Space

`EpochClient` provides native file, prepared-dataset and
folder operations. They use the installed generated StratifyX SDK and make no
graph/model call for these operations. Backend owns resource identity, review,
authorization and persistence across conversations.

The Space capability requires the native SDK version declared in
`python/epoch-sdk/pyproject.toml`. Use a matching published package or the
verified package generated from the supporting Backend change. Generated native
models are not copied into EpochSDK.

## Notebook/API flow

The following prepares a knowledge table. Supply an explicit reviewed time
mapping and `purpose="study_source"` when the input is intended for a study.
Knowledge data receives a dataset reference without an implicit source reference.

```python
import pyarrow as pa
from stratifyx.types import (
    DatasetReviewRequest, SpaceResourceRef,
    StructuredImportOptions, StructuredImportRequest,
)

# client is an authenticated EpochClient.
uploaded = await client.upload_file(
    b"label,value\nfirst,1.25\nsecond,2.5\n",
    name="observations.csv", media_type="text/csv",
)
await client.inspect_file(uploaded.file_ref, format="csv")
request = StructuredImportRequest(
    file_ref=uploaded.file_ref, request_id="retain-this-id-for-retries",
    name="Observed values",
    options=StructuredImportOptions(
        format="csv", delimiter=",", header=True, null_values=[], columns=[],
    ),
    metadata=None, purpose="knowledge",
)
draft = await client.prepare_dataset(request)
preview = draft.preview
complete = await client.download_dataset(draft.draft.draft_ref)
table = pa.ipc.open_file(pa.BufferReader(complete)).read_all()

# Review the exact draft and its complete data before deciding to save/reject.
review = await client.review_datasets(DatasetReviewRequest.model_validate({
    "decisions": [{"action": "save", "draft_ref": draft.draft.draft_ref,
                   "name": "Observed values"}],
}))
result = review.results[0]
assert result.status == "saved"
dataset = result.dataset
folder = await client.create_folder("Research")
child = await client.create_folder("Inputs", parent_folder_ref=folder.folder_ref)
await client.place_resource(
    SpaceResourceRef.model_validate({"kind": "dataset", "ref": dataset.dataset_ref}),
    folder_ref=child.folder_ref,
)
page = await client.browse_space(folder_ref=folder.folder_ref, recursive=True)
```

Retain the exact upload/import/draft/resource references and the original import
request ID when retrying. Backend verifies chunks and content digests, rejects
incomplete publication, and owns repeated review decisions. An uncertain study
submission still follows the existing explicit execution-ID rules.

`download_dataset` returns complete verified Arrow IPC file bytes for pending
drafts and accepted datasets. Previews remain bounded. A preview with
`requires_download=true` cannot show its next complete row within the preview
budget; retrieve the complete content instead of reconstructing a dataset from
preview text or following a non-advancing cursor.

## Organization behavior

Kinds are `file`, `dataset`, `model` and `study`; their references come from the
existing owning services. Space browses folders and explicitly placed resources.
Original library/catalogue methods still discover unplaced resources.

`update_folder` replaces the name and parent while retaining `folder_ref`.
Supply the existing parent to rename in place; a null parent moves to root.
`place_resource` moves a reference and may set its Space display name. Omitting
the name preserves an existing display name. Canonical content, metadata and
source identity stay with the owning service.

`delete_folder` accepts empty folders only. `unplace_resource` removes
organization metadata, including an obsolete reference, without deleting the
underlying asset. Normal native deletion dependency checks still apply.
Restart pagination after a 409 caused by changed contents or selections.

## Direct SDK access

Use `EpochClient` file, dataset and Space methods. The composable `epoch-mcp` file/Space facade is retired. Complete dataset content remains an owner-authorized binary download; saved studies keep their native execution and input-retention semantics after folder moves.

Controlled transport coverage lives in the direct SDK tests. Live drivers retain their explicit disposable-storage and caller-authentication requirements; they must not be pointed at production storage.
