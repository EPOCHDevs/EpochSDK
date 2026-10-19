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
let notebooks and MCP clients attach after disconnecting.

## One research session

Install the `notebook` or `terminal` presentation extra and use:

```python
result = await epoch.run(request, operation_id="msft-quality-2025")
```

The SDK renders live Epoch activity, collects explicit replies, resumes the same
native checkpoint and displays the saved answer once. The returned result stays
ordinary Python data. `await epoch.run(operation_id="msft-quality-2025")`
reconnects after a kernel/process restart. MCP consumes the same headless session
core with structured progress and questions. See [interactive sessions](../../docs/interactive-sessions.md).

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
