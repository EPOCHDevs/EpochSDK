# Saved response plans

Research establishes a study and a verified response plan. Deployment executes
that saved sequence without a supervisor. The AAPL case exposed the missing
boundary: account returns, fills and costs exist after execution, so their
performance table cannot be required as a pre-run study relation.

This design is approved in [ENG-2086](https://linear.app/epoch-inc/issue/ENG-2086).
The wire models and structural fixtures are drafted. Native successful-query
recording and the internal complete-result materializer are implemented as
components; query capture has passed a real generated-SDK wire check. Complete
query results now also persist as immutable bounded Arrow parts and page through
the existing owned native response reader. Native v1 plan admission/read APIs,
mapped output assembly and answer-backed verification are now implemented, with
publication over another completed execution tested at the service boundary.
The bounded text endpoint is implemented in EpochAI's candidate. Generated-client
integration, prepared-execution scheduling, live text calls and full replay
acceptance remain incomplete. Existing `execute_saved` currently
returns native execution status and does not regenerate an answer.

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
