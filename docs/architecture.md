# SDK and service boundaries

Epoch SDK is a client library over LangGraph SDK and generated StratifyX SDK.
Each language has its own client implementation and the same shared API contract.
MCP exposes the same client capabilities rather than recreating orchestration.

The first flow reuses EpochAI's existing supervisor through LangGraph SDK. Its
checkpointed thread retains discovery findings, study-building progress and
native clarification interrupts. The SDK imports native clients, not EpochAI
application code. Backend owns saved studies, executions, results, REST
controllers and native StratifyX generation.

A build starts or continues a thread. An interrupt returns questions, options,
a resumable handle and an optional link to the existing Epoch UI. A human or
MCP agent supplies answers and resumes that same checkpoint. Recommendations
are displayed as advice; the wrapper does not choose them automatically. No
separate conversation store, new graph or chat UI is required for this adapter.

Keep the identities explicit: `thread_id` identifies the conversation/build;
`study_id` identifies the saved definition; `execution_id` identifies a Backend
job. A workflow saves the chosen study reference and executes it directly through
Backend for a new period, without discovery or a supervisor call. The current
adapter supports immutable agent-authored definitions and explicit native period
and execution parameters. It does not implement source-execution refresh or
promise to preserve every source-run override when those are omitted.

`SupervisorClient` and the MCP tools implement communication and execution
selection. `execution_selected` carries Backend's real status, including queued
or failed; it does not claim that requested output names, values or schemas have
been validated. Selection is limited to the current request's new executions or
new tool outcomes. A failed/unclear request must not return an older success.
The SDK preserves native errors rather than inventing a completed result.

The shared request/output models and actual-value validator remain necessary for
the full analysis API. `contracts/openapi.json` is the earlier v0.9 design draft;
its attempt/admission and terminal-clarification bindings are being reconciled
with this stateful direction. They are not deployed routes or prerequisites for
trying the native communication adapter. Additional Backend tracking must address
a demonstrated gap in existing records. Do not treat this adapter as completion
of the named-output API, saved-output adapters or real-service integration proof.

Real analysis/ingestion runs remain gated on the user's review of the agent shape
and handoffs. Component checks use real client libraries with simulated HTTP;
they start no agent, model, engine or service. Recovery/retry orchestration,
retention, a new graph and an interactive CLI are deferred.

See [the SDK and MCP example](supervisor-workflow.md) for the implemented surface.
