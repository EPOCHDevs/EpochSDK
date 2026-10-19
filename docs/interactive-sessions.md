# Interactive research sessions

The ordinary SDK can run a whole research conversation in one call:

```python
result = await epoch.run(request, operation_id="msft-quality-2025")
```

`epoch` is an `EpochClient` connected with an Epoch identity and the Backend and
LangGraph service URLs. Install `epoch-sdk[notebook]` in Jupyter or
`epoch-sdk[terminal]` for a terminal. Auto mode selects the current notebook or
an interactive terminal. A noninteractive process receives a typed result or
structured `NeedsInput`; it never waits for keyboard input.

The session displays the existing Epoch UI stream, asks for explicit replies,
resumes the native checkpoint, and displays the saved answer once. The returned
`ResearchCompleted` is still ordinary Python data. It contains the pinned answer
revision, requested named parts, source execution and reusable study reference.
Prepared study execution remains the separate `execute_saved` action.

Notebook Markdown uses CommonMark formatting in a normal HTML widget. Currency
such as `$87 billion to $136 billion` stays literal instead of becoming an
inline math expression. Code, emphasis, links and Markdown tables retain their
formatting; raw HTML is escaped. This changes presentation only, not the saved
answer or its values.

## Questions and reconnect

Notebook replies use asynchronous widgets in the running cell. Select an option
or write a natural-language reply and click **Send reply**. A recommended option
is advice; it is never preselected. Multi-select questions support several
choices. **Leave waiting** returns the pending question without changing the
server. Stopping the cell also leaves the server operation available.

Terminal replies accept displayed option numbers or plain language; commas select
multiple options where allowed. `/leave` returns the pending question and `/skip`
explicitly skips a question. Blank input never selects a recommendation.

To reconnect after stopping Python or restarting a kernel:

```python
result = await epoch.run(operation_id="msft-quality-2025")
```

Omitting the request reads the existing operation. Resubmitting the same request
and ID uses native idempotent admission. Different accepted inputs require a new
ID. The operation record owns its request, thread and run identities; the client
creates no second state store, graph or workflow. The session does not implement
worker recovery, automatic retry, retention or implicit cancellation.

## Terminal command

With the ordinary Epoch identity and service URLs supplied in the environment:

```bash
epoch research cases/msft_fundamentals.json --operation-id msft-quality-2025
epoch research --operation-id msft-quality-2025
```

`EPOCH_TOKEN` (or `EPOCH_ACCESS_TOKEN`), `EPOCH_BACKEND_URL` and `EPOCH_GRAPH_URL`
supply access. The CLI does not read service `.env` files or vendor/model keys.
`--json`, or piping the command, returns structured JSON without a human prompt.
Exit status 0 means an answer, 2 means pending input, 1 means failure, and 130
means the local observer was interrupted. The server may still be running after
an observer exits; reuse its operation ID.

## Headless session core and MCP

Applications can consume the same typed events without either renderer:

```python
session = epoch.session(request, operation_id="msft-quality-2025")
async for event in session.events():
    await my_event_handler(event)
```

The event variants are `status`, `ui`, `ui_removed`, `questions`, and `completed`.
UI events preserve LangGraph's source ID, component name, properties and
metadata. Service-owned component extensions remain JSON; the session event
shapes and result/question contracts are closed models. Repeated UI IDs replace
or merge according to the native UI contract, and removals retain their meaning.
Raw draft model tokens are not rendered as another final answer.

`session.run(on_event=..., on_question=...)` encapsulates observation and resume.
The optional question callback receives `NeedsInput` and returns native
`dict[str, Answers]` keyed by interrupt ID, or `None` to leave the question
pending. Without a question callback, a pending question returns immediately.

MCP's `epoch_research` with a readable `operation_id` uses this headless core.
MCP progress messages contain the closed session event as JSON using the standard
progress notification. Questions and the saved answer are returned as structured
tool results. The calling agent uses context to answer an authorized question or
asks its user, then calls `epoch_resume_research`. The MCP server never imports a
terminal/notebook renderer or opens keyboard/widget input. Legacy calls without
an operation ID retain the older native research path; supply an ID for streamed,
reconnectable sessions.

## Results and dashboard independence

A published response is the final answer. A table part references complete typed
native data; it does not require a matching dashboard table. Public
`sql_program` terminals qualify as study outputs under Backend's output contract.
Private SQL relations and ordinary named intermediates are not independent output
sinks. The author retains requested evidence; the supervisor inspects it and
publishes table, JSON, plain text or Markdown parts after execution.

Human views show a bounded table preview, labeled when additional rows exist.
The result and native table APIs retain every row and the exact answer revision:

```python
async for page in epoch.iter_response_table(
    result.response.response_id,
    "fundamentals",
    version=result.response.version,
):
    consume(page.rows)
```

JSON values retain their native types; text is shown according to its declared
plain/Markdown format. No second assistant narrative is printed after the answer.
Source credentials remain on their owning services.

## Presentation libraries

The terminal uses [Rich Live](https://rich.readthedocs.io/en/stable/live.html) and
[prompt_toolkit asynchronous input](https://python-prompt-toolkit.readthedocs.io/en/stable/pages/asking_for_input.html).
The notebook uses [ipywidgets with asynchronous event-loop callbacks](https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20Asynchronous.html).
These are optional presentation dependencies; headless SDK and MCP use the same
native session transport without them.
