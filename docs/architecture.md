# SDK and service boundaries

Epoch SDK is a client library over LangGraph SDK and generated StratifyX SDK.
Each language has its own client implementation and the same shared API contract.
MCP exposes the same client capabilities rather than recreating orchestration.

Research serves notebook users as well as MCP agents and the existing platform.
Building/research and application execution against prepared work are separate
actions. A single run does not implicitly combine training, dataset publication
and serving. Existing direct native execution remains a distinct SDK/MCP action.

The response API is a shared Backend-owned answer document for an exact query,
containing named table, JSON and text parts. Notebook code and the
existing supervisor can publish after analysis through the same API. Each edit
creates a new response revision; different queries may reuse one execution. Tables
keep exact columns/types and annotations, JSON uses standard JSON Schema, and
text keeps its requested format. New table answers reference saved relations;
Backend validates the complete projection before publication. Clients page rows
directly from Backend. The 10,000-row/4-MiB bounds apply to a transfer page, with
no fixed total-table row ceiling. Saved answer JSON remains bounded to 4 MiB.
Older inline-row answers remain readable. See [table access](response-tables.md).

Response production is: compute, read actual results, assemble the requested
parts, validate, publish, then return the saved response. JSON/text response
values do not need to live in dashboard Markdown. Existing reporters continue
to supply computed artifacts; new EpochScript response transforms are deferred
until the common API demonstrates a concrete authoring need. Backend reuses its
private blob storage and atomic revision primitives, with no extra database or
background coordinator. Current component evidence does not establish real
agent response production or the full live-service notebook/MCP flow yet.

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

`EpochClient.research` and the three research MCP tools connect accepted
Backend requests, native supervisor clarification and pinned saved responses.
A fresh client reads a completed request through Backend alone.

`SupervisorClient` and the older conversation MCP tools implement communication
and execution selection. `execution_selected` carries Backend's real status, including queued
or failed; it does not claim that requested output names, values or schemas have
been validated. Selection is limited to the current request's new executions or
new tool outcomes. A failed/unclear request must not return an older success.
The SDK preserves native errors rather than inventing a completed result.

The shared request/output models and actual-value validator are used by the
research client and supervisor publication tool. `contracts/openapi.json` keeps
the shared data models and earlier illustrative REST proposals; its combined
`/v1/run` operation is deprecated and is not a deployed gateway. The current
SDK/MCP methods and actual native routes are documented in
[the research flow](research-flow.md). Backend #480 owns the additional accepted
request and response controllers. Component evidence is not full real-service
research proof.

Real analysis/ingestion runs remain gated on the user's review of the agent shape
and handoffs. Component checks include actual generated clients over compiled native
HTTP/storage fixtures and the supervisor publication helper. Synthetic execution
references do not establish a model/engine research run. Recovery/retry orchestration,
retention, a new graph and an interactive CLI are deferred.

See [the SDK and MCP example](supervisor-workflow.md) for the implemented surface.
