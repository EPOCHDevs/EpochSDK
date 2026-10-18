# Stateful supervisor adapter

This adapter reuses the registered supervisor and native checkpoints. It handles
communication, clarification and execution selection. It does **not** yet wire
the declared named-output API to saved results or certify analytical correctness.
No real service run is claimed by the component tests. Review the agent shape
and handoffs before exercising a real analysis or ingestion run.

Install a reviewed StratifyX 3.2.0rc1 or later wheel through its normal distribution
workflow, then install this source in an isolated Python 3.12 environment:

```bash
python -m pip install 'python/epoch-sdk[mcp,test]'
```

Configure `EPOCH_GRAPH_URL`, `EPOCH_BACKEND_URL` and `EPOCH_TOKEN` using the intended
development services and caller identity. `EPOCH_ASSISTANT_ID` defaults to
`epoch-ai`. Optional `EPOCH_UI_URL` is the existing Epoch UI base URL; no host is
assumed and no credentials are embedded in a URL.

## Build or continue a task

```python
import asyncio
import os

from epoch_sdk.supervisor import NeedsInput, SupervisorClient


async def main():
    client = SupervisorClient.connect(
        graph_url=os.environ["EPOCH_GRAPH_URL"],
        backend_url=os.environ["EPOCH_BACKEND_URL"],
        token=os.environ["EPOCH_TOKEN"],
        assistant_id=os.environ.get("EPOCH_ASSISTANT_ID", "epoch-ai"),
        ui_url=os.environ.get("EPOCH_UI_URL"),
    )
    try:
        result = await client.run("Compare annual sales using my approved company dataset")
        if isinstance(result, NeedsInput):
            print(result.feedback())
        print(result.model_dump_json(indent=2))
    finally:
        await client.aclose()


asyncio.run(main())
```

Pass `thread_id` to continue an existing, idle thread. A new task is rejected
while that thread is waiting on clarification: answer the pending interrupt
instead. The returned handle distinguishes the build thread, native graph run
and this request. Keep the returned `NeedsInput` JSON if a later process will
answer it; it is a resumable reference, not another conversation database.

## Answer a clarification

Open `conversation_url` for the human route, or pass answers to the SDK. Use the
returned interrupt IDs and **zero-based** question/option indices. Answer every
question; an empty answer row explicitly skips that question. Recommended
options are never selected automatically.

```python
from epoch_sdk.supervisor import Answer, Answers, NeedsInput

waiting = NeedsInput.model_validate_json(saved_needs_input_json)
interrupt = waiting.interrupts[0]
questions = interrupt.ask_user().questions
# Inspect questions and supply answers chosen by the caller.
result = await client.resume(
    waiting,
    {interrupt.id: Answers(answers=[Answer(question_index=0, free_form_input="Use 2025")])},
)
```

This snippet illustrates a round with one interrupt and one question. For
multiple interrupts/questions, provide every returned ID and question index.
Resume sends only the native answer command on the same thread; it does not
resubmit the task or clear discovery. Another clarification returns another
`NeedsInput` value. Unsupported custom interrupt payloads remain visible in the
result; this helper decodes only Epoch's native `ask_user` shape.

The UI link uses EpochPortal's existing `threadId` query parameter. The route
has been inspected; opening the thread and preserving it across a sign-in
redirect still need live UI verification. An answer submitted in the UI resumes
that conversation there. Read its state using the saved handle:

```python
result = await client.status(waiting.handle)
```

This starts no graph run. It returns `in_progress` while the graph is busy,
`needs_input` for another clarification, or the request's execution selection.
A fresh client can use the serialized handle. If the UI starts an unrelated
task, a handle whose request identity no longer matches is rejected. The live
UI-to-SDK handoff remains unverified; component tests simulate that transition.

## Execute a saved study without rediscovery

When a result has `status == "execution_selected"`, retain `reusable_study`.
Execute that immutable agent-authored study directly through Backend:

```python
from datetime import date
from stratifyx import DatePeriodConfig
from epoch_sdk.supervisor import SavedStudy

reference = SavedStudy.model_validate_json(saved_study_reference_json)
result = await client.execute_saved(
    reference,
    period=DatePeriodConfig(start=date(2025, 1, 1), end=date(2025, 12, 31)),
)
print(result.execution.id, result.execution.status.value)
```

This uses Backend's existing study read and execution submission APIs. The
returned job may be queued, running, completed or failed. It makes no supervisor
or discovery call. Provide native `ExecutionOptions` explicitly when overrides
are required. Source-run override preservation and the native refresh route are
not implemented by this method; it must not be described as a lossless replay.

## MCP

`epoch-mcp` serves the same adapter over stdio using the environment above.
Configure an MCP host to launch that command in the installed environment.
An MCP host may call:

| Tool | Input | Behavior |
| --- | --- | --- |
| `epoch_run` | `task`, optional `thread_id` | Send a task to the existing supervisor |
| `epoch_resume` | Entire `waiting` result, answers keyed by interrupt ID | Resume the same checkpoint |
| `epoch_execute_saved` | `reference`, `parameters.period`, optional `parameters.execution` | Submit directly to Backend |
| `epoch_status` | `handle` | Read progress or the result after a UI resume; starts no run |

Questions appear as readable text and structured data. Invalid tool arguments
are tool errors. `needs_input`, `no_execution` and `execution_selected` are
structured SDK outcomes, alongside `in_progress`. MCP owns no additional
workflow registry or agent.

## Verification and remaining work

Component tests use actual LangGraph SDK, StratifyX and an in-memory MCP client
with simulated upstream HTTP responses. They cover retained interruption,
answer validation, same-thread resume, current-request execution selection,
Backend failure status, owner rejection, a fresh-client read after a simulated
UI resume, and direct saved-study submission.
The supervisor interrupt/answer schema snapshot records its reviewed owner
source; tests compare the SDK's wire shapes to that snapshot.

The full milestone still needs declared output propagation, saved-result readers
and validation, authenticated live SDK/MCP examples
and the human UI handoff. Separate-attempt controllers and a new analysis graph
are not assumed prerequisites; existing records and supervisor behavior must be
checked for specific missing capabilities first. No retry/recovery subsystem,
new chat UI or interactive CLI is added here.
