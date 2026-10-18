# Tables without a total row ceiling

A newly assembled table answer stores its ordered column schema and a `source`
reference to the selected execution's native relation. The reference carries
`execution_id`, `table`, `field_ids` and the complete `row_count`. It does not
embed the table's rows or require a visible dashboard table. Columns may identify
dates, labels or multiple dimensions; no timestamp or unique row label is assumed.

The publisher probes the native Arrow schema. Before committing the answer,
Backend validates the complete selected projection in one aggregate query:
physical types, nullability and supported value representations. A valid first
page alone does not certify a table. The saved answer stays small while its
source may contain more than 10,000 rows. JSON and text parts remain inline.

## Read pages

`SupervisorClient.response_table(response_id, name, version=..., offset=0,
page_size=1000)` returns a typed page containing its answer ID/version, `schema`/`rows`,
`offset`, `total_rows` and `next_offset` (null at the end). Each page contains
actual typed `rows`; it is explicitly a page, not the entire answer table.
MCP exposes the same action as `epoch_response_table`.

Notebook code can traverse every page without collecting the whole table in RAM:

```python
async for page in client.iter_response_table(answer.response_id, "results",
                                             version=answer.version,
                                             page_size=5000):
    consume(page.rows)
```

The iterator reads the answer once, pins that revision and follows `next_offset`.
Pages read Backend directly without invoking a graph, model, discovery or study
execution. Display clients can request a smaller first page and clearly show its
total row count. Never present that page as all rows when continuation remains.

The native REST surface is still
`POST /api/v1/studies/executions/{executionId}/response-tables`. Its body contains
the exact saved `table` and `field_ids`, plus `offset` and `page_size`. The response
is binary Arrow IPC with `X-Arrow-Total-Rows`, `X-Arrow-Returned-Rows` and
`X-Arrow-Row-Offset` headers, exposed to browser clients through CORS. Callers
supply identifiers, not SQL. Backend quotes identifiers and owns the query.

The source can bind `order_by` keys, each containing a native `field_id` and
`descending` boolean. Bind the requested ranking or chronology explicitly; a
sort key may be an index column that is not projected into the answer. Backend
validates those field bindings before publication. Selected column values then
provide deterministic tie-breaking, ascending with nulls last. With no explicit
keys this becomes the default retrieval order. Duplicate labels and duplicate
rows remain valid; no primary-key semantics are inferred.

## Limits and compatibility

A transfer page allows 1–10,000 rows and at most 4 MiB. The complete table has no
fixed row ceiling. Reduce page size for wide rows. The saved answer JSON envelope
still has a 4 MiB limit. Readers validate every returned Arrow page against its
declared column types and preserve int64 strings, dates, units and nulls.

Older answers with complete inline `rows` remain readable and can be paged
locally through the same client method. A table uses either `rows` or `source`,
never both. Inline answers retain their saved row order. Existing completed
requests keep their original pinned revisions.

Pages re-query immutable source relations and may scan/sort the selected data;
this implementation does not promise constant-time offset seeks or provide a
streaming file export. Normal query deadlines and resource limits still apply.
References require the execution's stored data to remain available. Missing or
changed sources fail explicitly rather than returning another run or a preview.

The shared schemas are `contracts/research-response.schema.json` and
`contracts/research-response-table-page.schema.json`. The reference example is
`contracts/research-response-reference.example.json`; the original example is
retained to verify legacy inline-answer compatibility.
