# Research service proof

The runner in `tools/verify_research_services.py` calls the actual EpochClient or
starts the installed MCP entrypoint as a separate process. It does not supply a
replacement graph, model, study implementation or response publisher.

Validate and inspect the supplied-data case without making a service call:

```bash
.venv/bin/python tools/verify_research_services.py \
  --case examples/research-service-proof.case.json --mode sdk \
  --output /tmp/epoch-sdk-proof-plan.json
```

The case asks the supervisor to create and execute a saved study using two
supplied synthetic sales observations. Expected table and JSON values are
registered before execution. This checks the result-producing path without
vendor availability affecting it. It does not prove live provider discovery.
The complete milestone also needs a separate approved data-discovery case and
clarification after discovery, as recorded in ENG-2047.

For those cases, register `requires_discovery`,
`require_discovery_before_clarification` and `no_new_discovery_on_resume` as
appropriate. The verifier then checks the observed native call sequence and
retained prefix across the explicit resume. It does not infer discovery from
the assistant's explanation.

For an authorized real run, configure `EPOCH_GRAPH_URL`, `EPOCH_BACKEND_URL` and
`EPOCH_TOKEN` in the environment. Optional `EPOCH_ASSISTANT_ID` and `EPOCH_UI_URL`
use the same settings as the SDK and MCP. Do not put credentials in a case or
receipt. The services must run the reviewed adapter/Backend revisions; their
health receipts must identify those exact commits and confirm the agent is ready
against the selected Backend.

```bash
.venv/bin/python tools/verify_research_services.py \
  --case examples/research-service-proof.case.json --mode sdk \
  --expected-backend-sha BACKEND_COMMIT --expected-agent-sha AGENT_COMMIT \
  --output /tmp/epoch-sdk-live-proof.json --execute
```

Run the same command with `--mode mcp` and a separate output path to exercise the
installed MCP process. An executed command can invoke the configured model and
create research records, a thread and native study executions. It belongs after
the structure review and any model-spend approval required for that environment.
No real service run was performed merely by preparing this runner.

On success the runner checks:

1. The native thread retains the exact SDK request and user-turn identities.
   Source-owned model receipts/token usage and build -> chosen run -> publish
   tool calls are captured; the completed-run outcome must identify the response's
   actual execution. Conversation content and tool arguments are omitted.
2. Exact table values, JSON values, declarations and execution/study linkage.
3. A fresh client returns the same pinned answer with an unreachable graph URL.
4. Running the saved study creates a different completed native execution of the
   same study while the graph URL remains unreachable.

The separate native execution read is available as `EpochClient.execution` and
MCP `epoch_execution`; it needs an execution ID rather than a graph handle.
Engine completion remains distinct from publishing another structured answer.

If clarification interrupts the task, the runner saves the native questions and
handle. Supply explicit `Answers` keyed by interrupt ID in a JSON file, then
repeat the command with `--resume-from RECEIPT --answers ANSWERS_FILE`. It resumes
the retained thread; it never chooses recommended answers automatically.

Keep receipts outside the public repository. A failed or interrupted attempt is
evidence too. Record service source/binary provenance alongside the runner's
dependency versions and case digest. A completed supplied-data case proves this
case's real service path, not the entire milestone or analytical correctness of
an arbitrary research task.
