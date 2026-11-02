# Document workflows

Python `EpochClient` and `AgentToolsClient` share the same document adapter.
Configure the ordinary Backend and EpochAI origins and current bearer identity.
Native resources remain on Backend; explicit processing and URL capture use the
existing EpochAI server. No graph run is needed for these direct API methods.

```python
read = await client.start_document_read(file_ref)  # explicit request
read = await client.document_read(read.read_ref)  # exact saved status
if read.state == "ready":
    page = await client.document_content(read.document_version_ref)
    for block in page.blocks:
        passage = await client.document_passage(page.document_version_ref, block.block_ref)
```

Read the returned `has_more`, coverage and limitations before claiming the whole
document was read. Advance offset by returned blocks and stop on zero progress.
Primary is one source stream; element/all layers can overlap it. Search matches
filenames and already prepared primary blocks. Unprepared files and unknown
coverage do not establish absence. Status/content/search calls start no AI.

```python
from epoch_sdk.documents import CaptureDocumentRequest
from stratifyx.types import DatasetBuildRequest

captured = await client.capture_document_url(CaptureDocumentRequest(
    request_id="my-stable-capture-id",
    url=direct_document_url,
))
build = await client.prepare_document_dataset(DatasetBuildRequest.model_validate({
    "request_id": "my-stable-extraction-id",
    "name": "Reported revenue",
    "preparation": {
        "inputs": [{"kind": "file", "file_ref": captured.file.file_ref}],
        "capture_ref": captured.capture_ref,
        "instruction": "Extract the reported revenue exactly as written",
        "output_format": "json",
        "schema_choice": {"mode": "provided", "json_schema_text": '{"type":"number"}'},
        "purpose": "knowledge",
        "enrichment": {"mode": "automatic"},
    },
}))
build = await client.document_preparation(build.preparation_ref)
```

URL capture persists the original in Uploads before processing. It accepts public
direct-file and presigned URLs, rejects private networks/general HTML, and retains
query-free URL provenance plus the exact request URL's digest. Reuse the same
capture/extraction request identity after an unknown response. A changed URL or
new intentional extraction needs a new identity; never automatically repeat paid
work to hide an incomplete or unknown result.

Schema is required. Table uses an object containing a `rows` array of flat
objects; JSON supports a flat object or text/number/integer/Boolean primitive.
Complete output remains `pending_review`; only explicit `save` publishes it.
Partial output requires explicit `save_available`. All decisions carry the
displayed attempt, `review_ref`, `schema_sha256` and `result_sha256`. Saving retry performs no extraction. Closing a view acknowledges
nothing. An accepted result exposes its ordinary stable `dataset_ref`.

`download_dataset` returns complete verified native content. JSON is UTF-8 text
with original numeric tokens, including large integers and precise decimals.
For Python decoding, use `json.loads(raw, parse_float=Decimal)` when decimal
precision matters. Table content is Arrow IPC. Inspect preview format first;
do not assume every dataset is a table or decode JSON through floating-point
re-serialization. Scalar study reuse uses native `saved_value`; temporal tables
still require an issued `source_ref`.

The composable MCP exposes `epoch_start_document_read`, `epoch_document_read`,
`epoch_read_documents`, `epoch_document_passage`, `epoch_search_documents`,
`epoch_capture_document_url`, `epoch_prepare_document_dataset` and exact
preparation/action methods. These complement deterministic `epoch_prepare_dataset`
imports. `epoch_dataset_content` selects an exact JSON text or binary Arrow
resource. Reading that resource rechecks ownership and starts no processing.

The first extraction adapter accepts PDF, PNG, JPEG, TIFF and DOCX. UTF-8
plain-text/CSV/TSV/JSON source reading is native; dataset extraction from those
originals is not provided by this AWS adapter. Public web preparation uses the same review lifecycle; see
[shared dataset review](dataset-review.md). Nested extraction schemas and
FMP/Data Explorer document intelligence remain separate scope. DOCX has no invented original page highlights.
