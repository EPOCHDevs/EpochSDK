# Reading saved outputs

The SDK can read complete bounded table, JSON and text values from an existing
Backend execution, then apply the actual-value validator. It uses native
StratifyX APIs. Reading saved results starts no supervisor, model or engine job.

The workflow/Backend owner must supply a saved mapping between the accepted
output declarations and exact native artifacts. The current reader accepts that
mapping explicitly as `SavedOutputManifest`. Publishing/persisting it during the
real workflow is still unfinished. This helper is not a replacement for that
work and does not prove that a natural-language task produced the right analysis.

## Existing APIs and representations

| Requested value | Exact saved source | Read behavior |
| --- | --- | --- |
| Table | Native category, table index and Arrow field IDs | Read the saved Arrow file/stream and bind fields in declared column order |
| JSON | Stable producer Markdown block ID containing raw JSON | Parse the complete JSON, rejecting duplicate keys/non-finite numbers, then validate its JSON Schema |
| Text | Stable producer Markdown block ID and declared format | Read the complete stored text and validate the saved format against the request |

Display titles and Backend SQL table names are not output identities. The reader
uses the explicit mapping and never constructs SQL. It does not extract JSON
from assistant prose, strip code fences, fill missing values or choose another
artifact when a binding is missing. JSON-in-Markdown is a supported existing
storage representation; producing/publishing those blocks for arbitrary tasks
is not implemented by this reader.

The native execution must match the mapping's exact study/version, its
owner-scoped definition read must succeed, and the job must be completed before
artifacts are read. Failed/cancelled jobs produce `EXECUTION_FAILED`;
queued/running jobs produce `EXECUTION_NOT_READY`. Native REST authorization and
transport exceptions currently retain their generated SDK behavior; complete
public error mapping remains part of core API alignment.

The reader selects only original producer `content.markdown`, rather than
inferring factual results from a selected presentation context or generated
summary. It also checks native categories to reject a server category fallback
that would select another saved source.

## SDK and MCP

Install a reviewed StratifyX wheel, then `python/epoch-sdk[clients,results]` for
the Python client or `python/epoch-sdk[mcp]` for the stdio server. The result
reader uses PyArrow 26; the SDK's declared optional dependency supplies it.

```python
from pathlib import Path
from epoch_sdk.saved_outputs import SavedOutputManifest

mapping = SavedOutputManifest.model_validate_json(Path("saved-output-mapping.json").read_text())
result = await client.outputs(mapping)
print(result.to_wire())
```

`client` is the configured `SupervisorClient` from the existing SDK example.
The same mapping is the `manifest` argument to MCP `epoch_outputs`. Values and
declarations are returned as structured content; the accepted column and JSON
Schema descriptions are preserved. Output-validation/read-limit domain failures
return the existing structured error envelope with execution identity. Malformed
tool arguments remain MCP tool errors.

Use `to_wire()` or `model_dump_json(by_alias=True, exclude_unset=True)` to save a
mapping. Omitted declaration fields must stay omitted; the core contract rejects
explicit nulls for optional metadata. Null values inside tables/JSON remain data
and are retained.

The language-neutral read receipt is
`contracts/saved-output-manifest.schema.json`; it references the existing shared
output declarations. `saved-output-manifest.example.json` illustrates its shape
with placeholder identities, not a live run. A schema check alone cannot prove
the source belongs to the accepted request. Backend publication and the
supervisor handoff must establish that association.

## Deterministic output handoff

`epoch_sdk.output_handoff.output_manifest` creates that mapping from a native
`DashboardSchema` and the accepted declarations. For tables, the study author
must emit `exhibit_id` equal to the declared output name and preserve the declared
column labels in order. The helper binds the resulting physical field IDs. For
JSON/text it requires the exact producer Markdown block ID equal to the output
name. Output descriptions and column/field annotations remain in the accepted
declarations.

The helper rejects missing IDs, duplicate IDs, changed column labels and a wrong
category with `OUTPUT_VALIDATION_FAILED`. Display titles never fill a missing
identity. Pass the resulting manifest to `client.outputs` for actual-value
validation; creating a mapping alone does not validate stored values.

This is the deterministic handoff component, not a new resolver agent. Automatic
request propagation to the existing supervisor, producing the declared artifacts
and saving the mapping in Backend still need to be connected and verified.

## Value preservation and limits

Integer outputs use decimal strings, preserving int64 values beyond JavaScript's
safe integer range. Native timestamp-to-string conversion preserves nanoseconds
and an existing timezone. A naive timestamp is rejected rather than assigned a
timezone. Nullability, finite numeric values, actual column types and JSON Schema
are validated even when a table is empty. Semantic descriptions/units come from
the accepted declarations, independently of presentation labels.

Default read limits are 8 MiB of source/decoded value bytes across the read and
10,000 rows per table. The Python helper accepts explicit limits. It reads all
batches or reports `FETCH_LIMIT_EXCEEDED`; it never labels a preview as a complete
validated output. These are client read limits, not engine admission limits or
a hard memory sandbox for the native IPC decoder. Rich paging/large-result
handling remains separately scheduled.

## Evidence and remaining integration

Component checks use the actual native StratifyX client over simulated HTTP,
real Arrow file/stream bytes and an in-memory native MCP client. They cover all
three output types, exact bindings, annotations, integer/nanosecond precision,
multiple batches, empty tables, limits, ownership rejection and defined failures.
All upstream calls in these checks are reads; no graph is called.

Still required: save accepted declarations and exact bindings in the owning
records, have the existing supervisor hand them to the SDK automatically, align
the full shared request/result API and run authenticated SDK/MCP examples. The
user's supervisor-structure review remains required before real analysis or
ingestion runs. No issue is completed by the reader component alone.
