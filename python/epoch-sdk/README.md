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
The adapter handles native communication and execution selection; connecting it
to the full named-output analysis API remains work in progress.

## Use the actual core contract

`RunRequest`, `IngestRequest`, fresh/cursor fetch, refresh, acceptance and errors
are executable Pydantic models. They reject unknown fields and type coercion,
validate exact output/column names, and preserve descriptions and standard JSON
Schema. These models preserve the earlier draft API's domain-error envelope.
The current supervisor adapter exposes native clarification as `NeedsInput` and
supports answering/resuming the same thread. The earlier terminal-only design
is superseded; the draft contract is being reconciled with this direction.

`../../contracts/openapi.json` is the public draft, now v0.9. It preserves the eight logical
operations from the v0.8 design; the illustrative REST paths do not assert that
another gateway is deployed. Request/error models must conform to that shared contract. Response/result schemas are still draft contracts; implementing their
Backend adapters and actual output validation remains ENG-2038.

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

This example parses a declaration only; it does not execute a study or validate
saved results. The native supervisor adapter accepts a task string today.
Connecting these declarations to the supervisor and saved-output reader remains
explicit work. Malformed declarations fail before any service call.

## Verify locally

Install the reviewed native StratifyX wheel through its existing package
workflow, then install `python/epoch-sdk[mcp,test]` in your isolated Python environment.
Never edit or vendor the generated StratifyX models. From the repository root:

```bash
python3 tools/sync_native_parameters.py --check
python3 tools/check_python_contracts.py
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
prints no credentials, and returns nonzero for missing capabilities. A public
health response proves connectivity only, **not** authenticated attempt access.
Once the matching native SDK is available, pass `--attempt-id` for an existing
caller-owned record to check that read as well; connectivity alone never passes
the complete check.
Use `EPOCH_ACCESS_TOKEN`/`LANGGRAPH_API_KEY` in the process environment when needed;
credentials must not be put in URLs. This package does not load another
application's `.env` or mutate its installed SDK.

See [the architecture notes](../../docs/architecture.md) for client/service
ownership. The native adapter uses existing supervisor and Backend study/execution
APIs. The older attempt-route check is relevant only to that draft API and is
not a prerequisite for the native communication adapter. The checker reports
availability; it does not start missing services. Additional recovery and
retention work is separate.
