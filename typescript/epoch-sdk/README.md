# Epoch workflow client for TypeScript

This preview package supports the API Playground's three workflows: research,
prepared study execution, and saved response reads. It wraps the current generated
StratifyX client and LangGraph SDK; it does not add service endpoints or duplicate
Backend persistence. It is not a full port of the Python data/MCP interfaces.
The package has not been published to a registry.

## Use

Supply authenticated native clients. The application remains responsible for
fresh identity tokens, service URLs, and clearing account-scoped state.
Configure the graph client's `callerOptions.maxRetries` as `0`, so a transport
failure cannot implicitly resubmit a launch or clarification command. The
wrapper disables native Backend retries per request; it cannot change an
already constructed graph client's retry configuration.

```ts
import { EpochClient, type RunRequest } from "@epochdevs/epoch-sdk"

const epoch = new EpochClient({ backend, graph })
const request: RunRequest = {
  task: "Explain the supplied evidence",
  context: ["Use only the facts provided in this request."],
  outputs: [{ name: "summary", type: "text", instructions: "Be concise." }],
}
const result = await epoch.run(request, { operationId: "research-example" })
```

`task` is a string, `context` a list of strings, and `outputs` a nonempty list
of uniquely named text, JSON, or table definitions. Wire request keys use the
shared contract's snake_case. Returned native models retain the generated
client's camelCase; `responseToWire` exposes the saved response's wire JSON.

The main methods are:

- `run(request, { operationId })`: create or attach to accepted research, then
  observe it until a saved answer or explicit clarification is available.
- `resume(waiting, answers)`: validate and submit the current interrupt replies.
  Each reply identifies the interrupt, question index and option indices.
- `execute(savedStudy, { operationId, period })`: run a retained study reference
  or a completed research operation's reference. Source settings, report
  templates and historical response plans retain their native semantics.
- `status(operationId, { kind })`: read research or execution state. A published
  graph checkpoint may be attached to the same accepted request receipt; this
  never starts, resumes or reruns graph/engine work.
- `read(responseId, { version })`: validate one saved answer revision. Omit the
  version for the first read, then retain its returned ID/version.
- `readRequest` / `readExecutionRequest`: read accepted inputs to restore a
  playground session without launching work.

`wait: false` returns after admission/observation. `onStatus` reports progress.
An `AbortSignal` stops local observation; it does not cancel server work. Keep
the same operation ID when reconnecting; changed inputs require a new ID.
Mutation calls are not automatically retried. Starting or resuming work always
requires an explicit call. An `accepted` state without a graph run requires an
explicit `run` with the original inputs to continue an interrupted launch.

Saved table sources are references, not complete row arrays. This preview reads
and validates the response envelope and inline values. Consumers must use native
response-table pagination for source-backed rows; the Portal reuses its existing
validated `ResponseTableServices` and `SavedAnswer` renderer. No synthetic values
are substituted for missing or invalid outputs.

## Development

Node.js 24+, the versioned native StratifyX client (3.3.0-rc.44 or later), and
LangGraph SDK 1.12.1+ are required. Install native packages through the Backend's
normal package workflow; do not regenerate or edit them in this repository.

```sh
python tools/sync_typescript_workflow_schemas.py --check
pnpm --dir typescript/epoch-sdk test
pnpm --dir typescript/epoch-sdk pack --pack-destination /path/to/artifacts
```

The schema projection is generated only from the shared `contracts/` sources;
its source hashes are checked in CI. Tests exercise real generated StratifyX
serialization against an in-memory transport, with simulated graph lifecycle
states. For a packed package installed in a consumer, set `EPOCH_SDK_TEST_ENTRY`
and `EPOCH_NATIVE_TEST_ENTRY` to that consumer's installed entry points before
running `node --test typescript/epoch-sdk/test/workflow.test.mjs`.

These tests do not establish live authentication, graph deployment, engine job,
or publication compatibility. Those require service acceptance against the
target environment before release.
