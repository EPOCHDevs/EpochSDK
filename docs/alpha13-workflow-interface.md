# Alpha13 workflow interface (historical)

This describes the previous default MCP. Alpha14 uses the composable tools in
[the current interface](public-client-interface.md). The workflow SDK remains supported.

The default MCP server exposes five operations over `EpochClient`. It has no
separate agent, controller or workflow implementation. Notebook, terminal and
MCP callers share the same research session; only rendering and input differ.

| SDK | MCP | Behavior |
| --- | --- | --- |
| `run` | `epoch_run` | Submit a task, handle the research flow and return its published answer. |
| `execute` | `epoch_execute` | Execute prepared work and wait for completion/publication, without a supervisor. |
| `resume` | `epoch_resume` | Answer current questions by operation ID and continue the same session. |
| `status` | `epoch_status` | Read progress, pending questions or the pinned result. |
| `read` | `epoch_read` | Read an answer or one page of a named table. |

A plain task is enough to start. Optional context, output declarations and native
parameters make the request more precise. If outputs are omitted, `run` uses a
concise Markdown answer. Explicit table/JSON schemas retain the same validation
as a typed `RunRequest`. Unknown tool arguments fail before service work begins.
Output preparation, validation and publication belong
to Epoch; the calling agent never constructs internal manifests or publishes
copied table values.

```python
result = await epoch.run(
    "Has Microsoft's growth become more cash-generative?",
    context=["Use annual income and cash-flow statements."],
    operation_id="msft-quality",
)
```

The matching MCP call is `epoch_run` with those same task fields. The SDK also
continues to accept an existing typed `RunRequest` as its first argument. Do not
combine a typed request with overrides for its task fields.

`run` always uses the shared session, including when the caller omits an
operation ID. An omitted ID is generated and returned; provide a readable ID
before a long call so it is available for reconnecting after a disconnect.
Matching inputs attach; changed inputs conflict. An explicitly blank ID is an
error, not a request to generate a replacement.

MCP consumes structured progress notifications and returns `needs_input` without
selecting recommendations or blocking on notebook/terminal input. Call
`epoch_resume` with `operation_id` and explicit `responses` keyed by the returned
interrupt IDs. The SDK retrieves and validates the current waiting state; the
caller does not copy an entire checkpoint into the tool arguments.

`execute` accepts a completed research operation ID or its `reusable_study`, a
native `period`, optional native `execution` options and a separate operation ID.
It waits by reading that same Backend operation. It never restarts discovery,
rebuilds the study, retries a failed job or invokes the supervisor. A saved plan
can include a bounded text interpretation step owned by EpochAI. Cancelling the
local wait does not cancel server work.

Use `status(operation_id, kind="run")` for research and `kind="execute"` for a
prepared execution. Status never submits work. `read(response_id)` returns the
saved answer; add `table`, `version`, `offset` and `page_size` to read table pages.
Pin the returned version and follow `next_offset` until null. A page size limits
one transfer, not the complete table.

## Alpha 13 migration

The previous 13-tool MCP catalogue is replaced by these five tools. Reconnect
the MCP host to refresh its tool list. There is no legacy default MCP profile:
`epoch_research` becomes `epoch_run`; `epoch_execute_saved` becomes
`epoch_execute`; separate research/execution status calls become `epoch_status`;
answer/table reads become `epoch_read`. Resume now takes an operation ID rather
than a full `waiting` object.

Advanced SDK methods (`research`, `research_status`, `resume_research`,
`execute_saved`, `execution`, `response`, `response_table` and owner publication)
remain available for existing typed callers and service tooling. They are not
additional default MCP tools. Older unkeyed request records remain readable
through those SDK methods and their saved answer IDs.

Changing EpochAI's supervisor, introducing a graph or fine-tuning its model
belongs behind this contract. It does not require another client tool surface.
