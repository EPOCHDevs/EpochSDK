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

The normally built alpha6 wheel with native SDK 3.3.0rc5 passed all 332 Python
tests, strict source Pyright, Ruff and shared contract checks. Eight actual cells
in the new MSFT helper notebook passed against the authenticated local services.
Existing user notebooks and kernels were preserved in a separate folder/kernel.

The research call reconnected to
`notebook-demo-msft_fundamentals-desk-v2-01-research`, retained the original
revision-1 answer and read all three fiscal rows. The source trace remains
`01a155b8-2f76-7420-ab70-f76ebd975635`: fourteen tools, no tool error, and publication
last; reconnect created no new graph run. Its native checkpoint remains idle
without pending steps or interrupts.

The optional original-period execution produced
`adf46b03-be0b-4d76-ade0-1c86766f3902`, completed, and reattached to that same job
on the second call. Native projection reads matched all original rows. The
study/thread/source execution binding and the original answer pin were retained.
Native metadata confirmed no dashboard; no dashboard link was fabricated.

The later-period preview resolved to 1 January–16 October 2026 with a distinct
readable ID. Its job was not submitted in this check. Changed-period/cost/ID
forwarding, cancellation, follow-up source preservation and populated-dashboard
links have component coverage. Rolling-period financial results, a populated
dashboard through Portal, the other shorter desk cases, and complete stored
response-plan replay still require their own live acceptance.

Subsequent alpha9/Native rc7 checks passed both computed-only and bounded-text
prepared-plan replay, including actual MCP reads and independent fiscal audits.
The AAPL helper notebook also completed a fresh research cell with its three
requested formats. Its complete SDK/MCP reads and independent source, fill,
cost and account audit passed. The other desk cases and a real populated
dashboard still need their own acceptance. The screener exposed a missing
roster-provenance field on the active native Discovery handoff; its failed
attempt has been preserved, and no Backend build will run without permission.
