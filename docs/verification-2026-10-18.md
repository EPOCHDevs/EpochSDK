# Local prototype verification, October 18

Notebook SDK and the separately started MCP process have been exercised against
the compiled Backend and the existing EpochAI supervisor, with normal Cognito
authentication, configured models and actual study execution. These are local
service checks; they do not claim a deployment or a package-registry release.

The recorded cases cover:

- Supplied annual sales: two rows, a computed total of 25, and a published answer
  containing the requested table, JSON and explanation.
- FMP annual statements: native discovery, a comparison question, explicit
  answer and resume on the same checkpoint without repeating discovery. Actual
  results match a separately recorded vendor baseline; latest statements are
  identified as snapshots rather than point-in-time vintages.
- Fresh Backend reads with graph access disabled, immutable answer revisions
  and completed requests retaining their original answer/version pins.
- Saved-study execution with a different period, checked against the period in
  the native execution record, without a graph or discovery call.
- Independent queries sharing an explicitly selected earlier execution. A new
  clarification clears the previous selected answer; resume retains the new
  query identity. Earlier request pins remain unchanged.
- Response tables independent of detailed dashboard tables. The vendor cases
  use metric cards; their published explanations are not copied to the dashboard.
  The last graph message is the publication receipt, with no second final answer.
- Ordinary, unmarked conversations publishing a brief answer without an engine
  execution, through both SDK and MCP.
- A controlled publication outage after an earlier success. Both clients return
  the specific unconfirmed-publication error and preserve it on fresh status
  reads, rather than returning the older answer or retrying automatically.
- Invalid authentication, missing answers, invalid table selectors and stale
  answer edits, including unchanged saved answers after those rejected calls.

The vendor author initially produced a computation-only candidate, which the
compiler rejected under its existing sink requirement. That infeasible candidate
remains in history; the existing supervisor corrected the handoff and completed
the study using a useful metric card. No new graph, output transform or compiler
exception was added to make the test pass.

Vendor credentials remain in Backend's normal `.env.local` locally and SSM in
deployed environments. EpochAI owns model configuration. SDK/MCP processes use
Epoch authentication and service URLs; they do not load either service's private
environment file. The independent vendor connector was an operator's baseline
instrument, not an SDK/MCP dependency.

Private receipts retain case and artifact hashes, exact service revisions,
selected executions, model/tool evidence and failed attempts. The reusable runner
and commands are described in [integration-proof.md](integration-proof.md).
Runtime regression checks distinguish mocked protocol tests from these real
service cases. Current Python SDK tests and strict typing also cover nullable
checkpoint metadata, ordinary plain/Markdown answers and specific publication
transport failures.

The platform renderer still needs the documented saved-answer consumer before a
global rollout. Review/merge, deployment, registry publication, richer prepared
work, new data preparation, recovery workers and retention remain separate work.
