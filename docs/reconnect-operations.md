# Reconnect using readable operation IDs

ENG-2067 adds caller-chosen operation IDs to research and prepared-study execution. A notebook uses this same Python SDK. The operation ID is known before waiting, so closing the notebook does not lose the operation's identity.

## Research

```python
from epoch_sdk import RunRequest, TextOutputRequest

request = RunRequest(
    task="Explain the supplied sales data",
    outputs=[TextOutputRequest(
        name="answer", type="text", format="markdown", instructions="Explain the findings concisely"
    )],
)
result = await epoch.research(request, operation_id="screen-sp500")
```

Run the same cell with the same ID and inputs to attach to the accepted research operation. A fresh client can also call:

```python
result = await epoch.research_status(operation_id="screen-sp500")
```

The result contains progress, pending questions, a recorded failure or the original saved answer. Questions retain their native LangGraph interrupt IDs and can be answered through `resume_research` or the conversation UI. A local cancellation stops observation; explicit native server cancellation is separate.

The first answer revision remains pinned after later answer edits or new conversation queries. The Backend publisher and request service save/reconcile that pin. The original client does not need to reach its completion callback.

## Prepared execution

```python
from stratifyx import DatePeriodConfig

run = await epoch.execute_saved(
    "screen-sp500",  # completed research handle, or a SavedStudy reference
    period=DatePeriodConfig(start="2025-01-01", end="2025-12-31"),
    operation_id="refresh-sp500-2025",
)
run = await epoch.execution_operation("refresh-sp500-2025")
```

Backend admits one native execution and retains its execution ID before starting it. Repeating this call attaches to that job. Each intended new execution uses a new operation ID. An admission still compiling can return `ExecutionAccepted`; read the same operation again for its native job status. This path calls Backend directly.

## IDs and accepted inputs

IDs contain 1–128 ASCII letters, digits, hyphens or underscores and start with a letter or digit. They are case-sensitive and scoped to the authenticated Backend owner. Research and execution use their respective API namespaces.

Matching normalized inputs attach. Changing the task, requested outputs, context, parameters or launch settings returns `IDEMPOTENCY_CONFLICT` (native HTTP 409). Use a new ID for that new operation. Accepted inputs remain readable in the native operation record. Omitting an operation ID preserves the existing unkeyed behavior.

The native LangGraph admission hook atomically records one graph run in Backend. Concurrent SDK submissions attach to that recorded run. Clarification resumes record their new native run ID without creating a new research operation. Reads select checkpoints belonging to that operation/run, rather than the newest conversation query.

## MCP

`epoch_research` accepts `operation_id` with the same `RunRequest`. `epoch_research_status` accepts either `request_id` or `operation_id`. `epoch_execute_saved` accepts the prepared study reference or a completed research handle, execution parameters and a separate operation ID. `epoch_execution_operation` reconnects by that execution handle.

`epoch_run` can opt into readable-ID research with a concise Markdown answer. Use `epoch_research` to declare named table, JSON or text parts. Existing unkeyed conversation tools retain their behavior.

Use the matching Backend, EpochAI admission hook and normally generated StratifyX SDK from this feature's linked PRs. This is healthy-service reconnect; automatic failed-run recovery, retry scheduling and retention remain ENG-2037 work.
