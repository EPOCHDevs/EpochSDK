# Saved response plans

Plans can include `qualifications` independently of their accepted answer parts.
Each qualification has a unique name, a short description of its basis, and a
`value` built with the existing query/parameter bindings. Counts, missing
identities and other changing facts belong in that binding, not static prose.
Qualifications have no output JSON Schema from which to read a `schema_constant`.

Backend recomputes every declared qualification against the chosen execution
before publication and before optional text generation. Missing fields, ambiguous
scalar reads, invalid encodings or oversized metadata fail output validation;
they do not silently remove a qualification or fail the completed engine run.
There are at most 16 qualifications, with descriptions up to 1024 characters and
at most 64 KiB of computed qualification metadata in total.

Saved `content.qualifications` is visible in notebook/terminal views and retained
by SDK/MCP reads alongside the table, JSON or text outputs. It does not add an
answer part or change a frozen table schema/description. Computed qualifications
require a source-backed response plan; direct publication cannot claim that
certification. Historical plans and answers that omit the field remain unchanged.

Research establishes a study and a verified response plan. Deployment executes
that saved sequence without a supervisor. Account returns, fills and costs exist
after execution, so a requested performance table can come from post-run queries;
it does not have to be a pre-run study relation or a dashboard exhibit.

This design is approved in [ENG-2086](https://linear.app/epoch-inc/issue/ENG-2086).
Backend owns successful-query receipts, immutable complete result storage,
versioned plan admission/verification, deterministic output mapping and prepared
execution. EpochAI owns research reasoning and the bounded interpretation call
for declared text. SDK/MCP wrap the native APIs and retain the original answer
pin while a new execution publishes its own answer.

The normal generated-client workflow and real authenticated service checks have
proved computed-only and bounded-text plan replay, complete SDK/MCP paging,
same-handle reattachment and exact source/plan/answer identities. Computed-only
replay invokes no model or graph; text replay invokes only its declared bounded
model step. The AAPL strategy's actual notebook research and original-period
replay also passed independent source, account, next-open fill, dividend and cost
review. These checks do not establish every case or a later-period deployment.

The [current acceptance ledger](interactive-acceptance-2026-10-19.md) records
all eight live case flows, exact candidates, independent calculations and trace
coverage. Fresh named-notebook MSFT research and its separate deployment passed,
as did the corrected screener and its exact saved-evidence JSON follow-up.
The screen's full roster is 503, including two unsupported names; two missing
source sectors and four missing-history/cutoff cases bring exclusions to eight.
Original failed answers and as-run sources remain preserved. Explicit live
terminal and MCP replies also completed on their original threads with independently
checked answers. The ledger records exact transport and delivery evidence rather
than inferring correctness from a published answer alone.

A later execution period requires the saved plan's explicit
`allow_period_override` capability. The default is false. During research the
publisher enables it only when the user requests reuse and the executed study,
every recorded query, output schema and text inputs are correct under changed
dates. Engine dates do not rewrite fixed fiscal labels, embedded SQL filters or
a captured roster. A fixed plan rejects an unsupported period before admission.
Alpha10/11 distinguish that Native rejection from a real accepted-input conflict;
they do not resubmit, change the operation ID or relax the frozen plan.

## Establish and publish during research

1. The existing supervisor discovers inputs, builds the saved study, handles
   explicit clarification and executes it. Keep the existing stateful thread.
2. `audit_run` asks focused natural-language questions about the actual saved
   execution. Its analyst may author SQL during research. Capture complete
   successful SQL, source execution, schema and query receipt at the native
   execution boundary. The current 600-character `sql_used` excerpt is an audit
   preview and cannot define replay.
3. The supervisor selects opaque recorded-query references and exact native
   relations. It supplies mappings, output schemas and text instructions. It
   does not transcribe table cells or insert literal financial answers.
4. Backend verifies the selected owned immutable study/execution, resolves full
   recorded queries and evaluates the complete projections. Replay on that
   original execution must reproduce the verified tables and JSON. Check text
   grounding and formatting; new LLM wording need not be identical.
5. Publish the versioned plan and the original saved answer. Retain exploratory
   and failed attempts separately as research history. A follow-up can create a
   different response plan over the same immutable study.

## Contract

`response_plans.py` defines closed wire shapes. Object/row mapping keys are the
user's requested JSON properties; they are intentional extension points inside
closed mapping variants.

- A query is a native successful-query receipt (`recorded_sql`) or an exact
  relation/field/order projection (`relation`). The model-facing draft accepts
  neither arbitrary SQL nor row arrays.
- A table concatenates complete query projections in explicit order. Columns
  retain accepted order, descriptions, units, nullability and types. No join or
  alignment is inferred from equal field names across sealed grids.
- JSON binds cells, one row, all rows, a column array or recursively named
  objects. A single-row binding requires exactly one row. Empty or incomplete
  results do not invent defaults. Parameters bind to the new execution's native
  parameters. Fixed values come from `const` assertions in the accepted JSON
  schema, not a free-form literal-value field.
- Date/datetime/decimal-string conversions are explicit. Date conversion must
  preserve the existing exact UTC-midnight rule; it cannot round away a time.
- A text step names its computed inputs and versioned server-owned model
  policy. Save its effective non-secret model/settings and prompt version.
  Credentials and arbitrary remote endpoints are not plan fields. The AI
  service performs a bounded generation call without tools or a supervisor.
- The definition retains accepted output declarations and captured native
  execution parameters. Execution settings stay frozen. Period variation is
  opt-in only when the study and computations support it; replay does not make
  a fixed historical study into a generic parameterized workflow.

## Execute the deployed plan

The existing prepared-execution admission owns the readable operation ID and
new execution ID. A plan reference accompanies the saved-study reference.

1. Start the ordinary native Backend execution directly.
2. A server-owned runner observes that job to completion. Use existing
   coroutine/offload lanes so status waits and query work do not block IO loops.
3. Run the stored queries in the new execution's data context. Keep the original
   research execution ID as verification provenance, never as the deployed
   query's source context.
4. Construct tables and JSON from actual results. Query-backed table references
   should retain full type validation, immutable source identity and native
   paging; a bounded `audit_run` preview is never a full table. Reuse the existing
   Arrow query engine and private Backend storage rather than introducing a
   second graph, proxy or database.
5. Invoke EpochAI only for declared text interpretation. A computed-only plan
   has no model call, supervisor, discovery, study building or SQL authoring.
6. Publish one answer tied to the new execution and plan revision. The original
   research operation keeps its original answer pin. A response is a sink;
   neither a duplicate dashboard table nor another assistant narrative is
   required.

Client disconnection closes observation while the admitted server work remains
owned. Reusing the same readable operation ID attaches to that same work and
accepted inputs. Keep engine status separate from response-generation status;
if a later response step fails, already-executed source data stays available.
This feature does not add worker recovery, automatic retries or retention rules.

## Ownership and acceptance

Backend owns query receipts, plan persistence, execution admission, post-run
query/mapping evaluation and saved answers. EpochAI owns research reasoning and
the explicit text-generation boundary. SDK/MCP wrap native APIs; client processes
receive Epoch identity and service URLs, never vendor or model credentials.
Generate changed native SDKs through the maintained Backend packaging workflow;
do not edit generated StratifyX models or revive discarded protos.

Acceptance requires the five real US equity cases and two output-only variants,
the actual notebook research cell, complete paged reads, independent source and
financial reconciliation, fill timing/cost inspection and trace/checkpoint
review. For deployment additionally replay the original verified plan, execute
it against a new native job, and prove from traces that only declared
interpretation invokes a model. Model/schema checks alone do not prove this.
