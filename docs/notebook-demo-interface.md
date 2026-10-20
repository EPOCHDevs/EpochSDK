# Notebook demo interface

Use one client-facing notebook per case. The question, data assumptions and
requested formats stay visible. The cells expose `connect`, `task`,
`display_request`, `run`, `read`, `execute` and `dashboard`. Shared local helpers
call the existing SDK; they introduce no graph, persistent store or retry system.

`display_request` shows native parameters and resolved dates before a submission,
plus expandable task/context/output declarations. `run` uses the existing shared
interactive session. `read` retrieves complete paged values and preserves answer
identity without printing a second narrative. Follow-ups resolve their exact
completed source on the service, attach to its thread and check the original pin.

`date_range` is a public SDK convenience that resolves explicit ranges, complete
calendar presets and rolling lookbacks to native `DatePeriodConfig`. LastN year
and month shifts match EpochAI's calendar subtraction, including month-end/leap
clamping. A pinned `as_of` makes demos reproducible. The resolved request, not a
moving phrase, is the input to native idempotence. Changing execution dates gets
a new readable execution handle and retains the original costs. It does not
change research inputs or claim that a fixed-date study becomes a rolling study.

## Optional dashboard request — next contract change

The current accepted `RunRequest` has no `presentation` field. Do not put a new
field into its closed wire shape or silently pass it as if Backend supports it.
Add this coherently to the native request contract, generated clients, Epoch SDK,
MCP schemas and active-request supervisor/authoring context before using it in
live notebooks.

The intended optional field should separate three choices: allow the agent's
normal dashboard judgment, request no dashboard, or describe a requested
dashboard. A compact candidate shape is:

```json
{
  "presentation": {
    "dashboard": "requested",
    "instructions": "Show a revenue and free-cash-flow trend chart and operating-margin card."
  }
}
```

This is a design example, not an implemented request. Proposed dashboard modes:
`auto`, `none`, `requested`; omitted means `auto`, which permits response-only
work. `none` forbids presentation sinks while keeping response sinks valid;
`requested` supplies a short natural-language dashboard brief. These instructions
are frozen with the accepted request and must reach both supervisor and study
author. Output declarations continue to specify the published answer. A table
answer does not imply a dashboard table; a dashboard brief does not replace the
published response. One source execution can back both, without duplicating text.

Acceptance must include response-only, explicitly no-dashboard, and explicitly
requested dashboard cases. Only real populated artifacts produce a dashboard
link tied to the exact execution; no existence claim is inferred from a URL.
The requested-dashboard example should ask for a wealth/drawdown chart for the
AAPL strategy and benchmark while keeping the performance table and short
conclusion in the published answer. Its acceptance needs both the saved answer
and an actually populated dashboard; a mocked link is not sufficient. A table
in the answer need not be copied into that dashboard.
The current demo `dashboard` helper already reads the native schema and uses
Portal's existing `/dashboard/{execution_id}` route, with a configured origin.
It first discovers categories from native performance metadata, including
event-marker-only output. No-category response-only studies stop there. It never
guesses a category or translates an arbitrary 404/authentication failure into an
empty dashboard.

## Stage presentation — deferred

The current source of activity is EpochAI's existing UI stream; SDK terminal and
notebook adapters project those events. Improve this shared presentation layer
with Discovery → Build study → Execute → Publish stages rather than adding
another workflow controller. Show the current stage and retained activity if the
agent returns to discovery/build. Publication is complete only when a saved
answer exists. Fixed 25/50/75/100 percentages are proposed milestone weights,
not elapsed-work estimates; do not display them as measured progress. This is
separate from completing the core prototype and response-plan replay.

## Verified on 19 October 2026

The [acceptance ledger](interactive-acceptance-2026-10-19.md) records current
packages, actual notebook/CLI/MCP evidence and remaining cases. It distinguishes
fresh research from reattaching to an older saved answer and from deployed replay.

The named `01_research_and_execute.ipynb` has now completed a fresh short MSFT
request under alpha11/Native rc8: real research cell, complete paged table reads,
all 36 fiscal fields compared to independent source calculations, and a new
verified response plan. Its 173-word Markdown memo and 22 numerical claims
passed review. The original answer and idle thread checkpoint remain pinned.

AAPL, MSFT-risk, macro, plain-text and explicit clarification have separate real
service, notebook and financial/source evidence. Clarification resumes the same
thread after terminal leave and MCP reconnect; recommendations remain unselected.
Alpha11's validation-label cleanup also passed a separate actual widget check.

AAPL has populated Native dashboard content and a verified exact-execution link.
Authenticated Portal rendering after sign-in is still frontend acceptance. An
optional presentation-request field and weighted stage display remain proposals,
not fields silently added to the closed request contract.

The screener's first published result passed full saved-price calculations but
failed roster coverage counts. Its next attempt built the correct count, then
stopped because the supervisor lacked the Native aggregate provenance in its
normal message. That handoff is now fixed and tested; a fresh screener and its
saved-evidence JSON follow-up remain required. Existing failed answers and owner
notebook outputs remain intact.

Original-period computed-only and bounded-text saved-plan execution passed real
SDK/MCP and source/trace checks. Fixed fiscal labels, SQL date filters and
populations stay frozen. Their later-period rejection is not evidence of a
rolling-period financial result. Automatic recovery, retries and retention
systems remain outside this prototype.
