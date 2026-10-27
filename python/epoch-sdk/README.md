# Epoch SDK core contracts

This Python implementation lives in the public, multi-language EpochSDK
repository. `contracts/openapi.json` at the repository root is the shared API
contract for every language client and MCP. Backend owns native REST APIs,
controllers, persistence and StratifyX generation; service repositories own
server graphs. The stateful adapter calls the existing EpochAI supervisor through
LangGraph SDK; it does not import the conversation application's Python code.

Python 3.12 is the first client implementation. The package name is `epoch-sdk`
and its import is `epoch_sdk`. It supplies executable contracts, an access
checker, output-value validation and the [supervisor/MCP adapter](../../docs/supervisor-workflow.md).
The adapter handles native communication, execution selection and explicit
[saved-output reads](../../docs/saved-output-reader.md). Research publishes a saved
answer with named table, JSON and text parts. Prepared-study execution remains
a separate direct Backend operation. [Readable operation IDs](../../docs/reconnect-operations.md)
let notebook and explicit workflow-MCP clients attach after disconnecting.

## One research session

Install the `notebook` or `terminal` presentation extra and use:

```python
result = await epoch.run(request, operation_id="msft-quality-2025")
```

The SDK renders live Epoch activity, collects explicit replies, resumes the same
native checkpoint and displays the saved answer once. The returned result stays
ordinary Python data. `await epoch.run(operation_id="msft-quality-2025")`
reconnects after a kernel/process restart. The explicit workflow MCP consumes that same headless session core; the default composable MCP uses the separate specialist interface. See [interactive sessions](../../docs/interactive-sessions.md).

## SDK workflows and composable MCP

Notebook and terminal callers keep `EpochClient.run`, `execute`, `resume`, `status` and `read` for the research/published-answer workflow.

The default MCP exposes 12 composable tools, including two specialist interfaces:
`epoch_inspect_source` and `epoch_build_study`. Codex or Claude chooses the
sequence and answers directly. Native data lookup and source inspection make no
generative model call; exact retained source references can be reused across
studies. Only explicitly selected study authoring or a program's declared
`llm_call` invokes a model. The retired audit specialist and model-facing
response-inspection/publication/dashboard-editor chain are not available.
No Epoch supervisor or publication is required by the default MCP.

For supported completed results, application/notebook and MCP clients share the
same native extension methods:

- `extension_inputs(execution_id, tables=[...])` reads exact types, flat enum
  references and the frozen executed source. It returns metadata, not sample rows.
- `save_extension(thread_id, source_execution_id=..., tables=[...], source=...,
  name=..., description=...)` compiles and saves supplied EpochScript as an
  immutable definition. This call uses no authoring model and runs no study.
- `execute_extension(CreateSdkExecutionRequest(...))` starts or attaches one
  operation. Supply the saved extension's `study_id`, the original
  `source_execution_id`, explicit `input_tables`, `parameters={}` when no engine
  period is needed, and a readable `operation_id` for reconnecting.
- `extension_status(operation_id)` only reads that operation. The original and
  derived execution IDs remain separate. Numerical status is distinct from
  `response_phase`; confirmed declared destinations appear in `extension_outputs`.
- `response(response_id, version=...)`, `response_table(...)` and
  `extension_presentation(pin)` read exact saved outputs. Presentation edit zero
  is a real pin; it is never replaced by a latest-version lookup.

MCP exposes `epoch_extension_inputs`, `epoch_save_extension` and
`epoch_execute_extension` over these same methods. Use `epoch_status` with
`kind="extension"` and `operation_id`. Use `epoch_read` with `kind="response"`
and its answer revision (optionally `table`, `offset`, `page_size`), or
`kind="presentation"` with the returned publication/catalog/edit pin.

The calling coding agent can author the program itself. Tables, JSON and native
reporters calculate directly in Backend. An explicit `llm_call` returns text
that `response_text`, Markdown or `executive_summary` can consume independently
or together, sharing one bounded cached generation. There is no supervisor, vendor query
or original-study rerun when using explicit `input_tables`. A response table does
not force a matching dashboard table, and dashboard-only work creates no
artificial answer. An unsupported source/type remains an explicit capability
error.

New SDK research can author its calculations, requested text and native output
sinks in one ordinary study. Backend completes those outputs after calculation;
the supervisor does not publish again. An explicit saved-input report is used
for later work over an earlier completed execution, including numerical analysis
of finalized trading results. An accepted
single-text SDK request with no computation can instead complete from its
ordinary final reply automatically. This does not replace missing computed
outputs or a failed native publication.

An ordinary `ResearchCompleted.reusable_study` retains its actual completed
source identity. `execute`/`execute_saved` reuse the saved definition with the
requested period, captured actual simulation settings and declared parameter
bindings. An explicit execution override retains ordinary override semantics.
Required output completion and answer pins are observed through the same native
operation. No report template or extra permission flag is invented.

`ResearchCompleted.reusable_study` retains a native `report_template` for an
original-plus-report result. `execute`/`execute_saved` with that reference run a
new original and its frozen report once, without a supervisor. The original job
and report child have distinct IDs; response/presentation pins belong to the
report. Native MCP replay uses `epoch_execute_extension` with `report_template`
instead of `input_tables`. Period changes require captured permission; costs
and declared original parameters remain captured. Historical response-plan
read/replay remains an explicit compatibility path, not new authoring policy.

The current package requires the normal generated native `>=3.3.0rc41,<4`
package, including Backend-owned research-to-extension links and report replay.
Controlled transport checks and real service/notebook/MCP/ClientPortal acceptance
are distinct evidence; historical milestone records do not prove a newer build.

See [the public interface](../../docs/public-client-interface.md) for the 12 tools, service boundaries and upgrade instructions. The old workflow MCP is retained only as `python -m epoch_sdk.workflow_mcp`.

## Use the actual core contract

`RunRequest`, `IngestRequest`, fresh/cursor fetch, refresh, acceptance and errors
are executable Pydantic models. They reject unknown fields and type coercion,
validate exact output/column names, and preserve descriptions and standard JSON
Schema. These models preserve the earlier draft API's domain-error envelope.
The current supervisor adapter exposes native clarification as `NeedsInput` and
supports answering/resuming the same thread. The earlier terminal-only design
is superseded; the draft contract is being reconciled with this direction.

`../../contracts/openapi.json` contains the shared request/error models, historical
illustrative `/v1` bindings, and source-owned native `/api/v1/integration` operation
projections. Native schema names have a `Native_` prefix and identify the original
Backend DTO. The wrapper calls the existing Backend and LangGraph origins.

The draft had omitted the agreed saved-study reference and execution parameters.
`RunRequest` now permits **either** `study_id` **or** `source_execution_id`, with
optional `parameters.period` and `parameters.execution`. These use the generated
StratifyX `DatePeriodConfig` and `ExecutionOptions` models and Backend's own wire
schemas; arbitrary named parameters or another study id inside `parameters` are
rejected. Resolve omitted defaults/relative dates before freezing the Backend
binding. Refresh can use those same supported parameter types; changing study
logic is a new definition/revision, not an ordinary refresh.

```python
from epoch_sdk import RunRequest
from epoch_sdk.parsing import parse_request

request = parse_request(RunRequest, '''{
  "task": "Compare annual sales for the approved company dataset in 2024",
  "outputs": [{
    "name": "annual_sales",
    "type": "table",
    "schema": [
      {"name": "year", "type": "int64", "description": "Calendar year"},
      {"name": "sales", "type": "float64", "unit": "USD"}
    ]
  }],
  "parameters": {"period": {"start": "2024-01-01", "end": "2024-12-31"}}
}''')
```

This example parses a declaration. Submit it with `await epoch.research(request,
operation_id="annual-sales")` using an `EpochClient` connected to the two services.
Malformed declarations fail before a service call. Research builds/analyses through
the supervisor and returns a saved answer; `execute_saved` starts or attaches to a
prepared study execution. See the [current flow](../../docs/research-flow.md).

## Verify locally

Install the reviewed native StratifyX wheel through its existing package
workflow, then install `python/epoch-sdk[mcp,terminal,notebook,test]` in your isolated Python environment.
Never edit or vendor the generated StratifyX models. From the repository root:

```bash
python3 tools/sync_native_parameters.py --check
python3 tools/check_python_contracts.py
python3 tools/validate_saved_output_contract.py
python3 -m pytest python/epoch-sdk/tests
```

`tools/sync_native_parameters.py` checks the packaged snapshot against the shared
native parameter contract. Its optional `--backend-openapi` input refreshes from
a reviewed Backend export; no Backend checkout is needed for ordinary client
checks. `tools/check_python_contracts.py` checks Python conformance without
rewriting the shared contract. Standard JSON Schema 2020-12 and local references
are supported; remote schema references are never fetched.

## Check real API availability

Install the `clients` extra and use the existing development origins explicitly:

```bash
epoch-api-check --backend-url "$EPOCH_BACKEND_URL" --graph-url "$EPOCH_GRAPH_URL"
```

The command uses the actual generated StratifyX health client and LangGraph
assistant discovery client. It starts no thread, study, ingestion or engine job,
prints no credentials, and returns nonzero for missing capabilities. It defaults
to the existing `epoch-ai` graph; use `--graph-id` or `EPOCH_GRAPH_ID` for another
registered graph. A public health response proves connectivity only. Pass
`--study-id` for an existing caller-owned definition and configure a bearer token
to check protected Backend access as well; connectivity alone never passes the
complete check. This diagnostic creates no thread or execution. The optional
`--attempt-id` checks the older draft controller only when explicitly requested.
Use `EPOCH_TOKEN` (or `EPOCH_ACCESS_TOKEN`) and `LANGGRAPH_API_KEY` in the environment;
credentials must not be put in URLs. This package does not load another
application's `.env` or mutate its installed SDK.

See [the architecture notes](../../docs/architecture.md) for client/service
ownership. The native adapter uses existing supervisor and Backend study/execution
APIs. The older attempt-route check is relevant only to that draft API and is
not a prerequisite for the native communication adapter. The checker reports
availability; it does not start missing services. Additional recovery and
retention work is separate.
