# Native discovery acceptance

Four separate notebooks exercise ENG-2152 without changing the earlier demos.
They use ordinary SDK helpers, local request files and the prepared Epoch login.
Vendor/model credentials stay on the services.

1. `00_catalog_search_and_mcp.ipynb`: shared Backend prose/options, name lookup,
   a complete current cohort, then the same owned saved search read through MCP.
   This notebook starts no research agent or execution.
2. `01_aapl_volatility.ipynb`: a short single-asset question, response-only table
   and summary, saved-value arithmetic, then the same saved study/plan executed
   again for its original period.
3. `02_sp500_cash_flow.ipynb`: one current S&P 500 universe with a known generic
   financial loader, a ranked saved table and cash-flow arithmetic.
4. `03_gdp_vintages.ipynb`: source-defined first/latest vintages, matched growth
   definitions, saved revision table and explicit native clock qualifications.

Choose the **Epoch Native Discovery (local)** kernel. The local acceptance setup
points it to Backend `127.0.0.1:19052` and EpochAI `127.0.0.1:12052`. Other users
supply their usual `EPOCH_BACKEND_URL`, `EPOCH_GRAPH_URL` and Epoch login/token.
`connect()` prepares access; `check_services()` only reads health. `task()` reads
its JSON beside the notebook; `display_request()` shows it before submission.
`run()` starts/reconnects the standard SDK session. `read()` pages the saved
answer, and `execute()` reuses prepared work without a supervisor.

Keep the attempt label to reconnect. Change it for an intentional fresh request.
A genuine unresolved question remains in the running SDK session; do not silently
choose a recommendation or change the required source. Source/data limitations
must remain visible. No market values or winning results are pre-filled.

These files are prepared acceptance examples, not evidence of live success by
themselves. ENG-2162 requires executing the actual cells, checking source choices,
values and saved-reference reuse, and reviewing the matching traces for absence
of a dedicated Discovery agent or hidden observation probe. Arithmetic and
schema checks do not establish vendor-source or vintage correctness.


## Acceptance record (22 October 2026, local services)

The first full cell runs used published StratifyX 3.3.0rc11, EpochSDK 0.1.0a15,
Native source efa98205b and the reviewed EpochAI PR #769 preview. The actual
executed notebooks and full traces remain in the operator's private acceptance
folder; these public examples intentionally contain no saved market values.

- All four notebooks completed. The Apple answer had 21 daily return rows and a
  103-word summary; its saved study/response plan executed again successfully.
  Re-running the original research ID reattached in 2.17 seconds without a new
  research submission.
- The current S&P 500 screen retained 503 security members. Its cash-flow study
  returned 10 issuer-deduplicated companies; saved rows passed date, ordering,
  uniqueness and cash-flow arithmetic checks.
- The GDP answer had eight quarterly First/Last comparisons and an 87-word
  limitation note. The selected native growth-series identity appeared in a
  returned ranked page before selection. Bedrock supplied relevance scores over
  500 collected identities; full provider completeness remained unknown.
- A separately installed MCP process listed 11 composable tools, matched the
  SDK's catalog prose/options, built two studies using retained source evidence,
  executed a study and read its dashboard. A direct native Arrow read checked
  its 21 computed daily-return rows. This is MCP protocol evidence, not a claim
  that an already-open Codex or Claude session refreshed its cached tools.
- Full traces showed no dedicated Discovery agent. Metadata calls fetched no
  observations. Requested study authoring and response text still use their
  explicit model paths; this is not a zero-model research claim.

Trace review found two fixed transport defects (integer fact coercion and
`from_` versus `from` in returned source windows), plus a metadata page-bound
mismatch and stale macro-source instructions. ENG-2166 through ENG-2170 track
those corrections, including the ownership metadata needed to list existing MCP
workspaces. The initial GDP run recovered from a schema tag error and
paging error; it is not evidence that every discovery call was clean. A fresh
run on the final guidance, final installation and compatibility inventory were
required before ENG-2162/ENG-2163 could close. The 464 archived cases
are hash-checked and classified; they have not all been replayed live. There is
no paid before/after model-cost or source-recall benchmark claim.

The final local pass used Native `0b998e82`, EpochAI `4d9f1d96`, frozen
EpochSDK `0.1.0a17` and StratifyX `3.3.0rc11`. All four fresh notebooks completed
with the same row counts, including Apple saved-plan replay and all eight GDP
quarters. The final installed stdio MCP also matched shared source prose/options,
read 1- and 10-record pages, continued a native cursor, rejected invalid bounds,
listed an owned workspace and read pre-upgrade studies without model submissions.
Native validation passed 99 cases / 19,928 assertions. Actual executed copies and
full traces remain private; these committed notebooks stay unexecuted.

The cash-flow run recovered from a selector-tag error and an authoring requirement
added by the supervisor. Its audit repaired indented source excerpts rejected by
a prompt/validation mismatch (ENG-2172). Calculation/plan replay can make an
explicit bounded text-model call; it does not promise identical prose. None of
these checks independently certifies vendor values or complete statement history.

Broad instrument relevance is still open in ENG-2171: real API searches reproduced
missing Google/Facebook issuer candidates, a micro-futures name miss, opposite FX
pair queries with identical ordering and a typo candidate lost behind prefixes.
Maintain the separate accuracy/library evaluation gate; successful examples do
not establish general search quality. Final installation, host reconnection and
compatibility retirement must be reported separately.
