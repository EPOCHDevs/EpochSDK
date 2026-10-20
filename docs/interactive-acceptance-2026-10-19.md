# Interactive-session acceptance — 19 October 2026

The acceptance goal is open. Source, component checks and actual service results
are recorded separately. An answer can publish successfully and still fail its
financial/source review; the screener below demonstrated that distinction.

## Candidate and boundaries

- Epoch SDK `0.1.0a11`, built from `163393b9cbc4f0f8502f203a63a39b4fed8f98f5`.
  Its installed suite passed 341 tests with Native Python `3.3.0rc8`.
  Alpha12 adds concise human activity errors while retaining exact source events;
  its installed-package check is pending.
- Native built source `63939005a2906e30ca9157eb74ad63a7e9dc50ac`, server SHA-256
  `4f280f480b68183db5dcefabb87b1f0b395b53e1daaea01053ede8e5393d2d6c`.
  The normal packaging workflow generated Python `3.3.0rc8` and TypeScript
  `3.3.0-rc.8`; generated models were not patched.
- EpochAI `1597b4cc10274e4712c19c7bd71c7c64cd7dd32a` retains the existing
  supervisor and kept runtime, plus the explicit bounded interpretation call.
  Native registry/reference version remains `aff8345a0813f681`.
- Real service checks use ordinary Epoch authentication and loopback URLs.
  Vendor credentials stay in Backend configuration; model credentials stay in
  EpochAI. Client environments contain neither.
- Existing owner notebook outputs, kernels and unanswered operations are
  preserved. Acceptance uses separate folders/kernels. Draft review branches
  have not been merged, released or deployed to production.

## Case evidence

| Case | Direct evidence | Current acceptance |
| --- | --- | --- |
| MSFT financial quality | Actual notebook research, all three fiscal rows and independent statement arithmetic passed on `desk-v2-01`. An alpha11 named-notebook reattachment preserved its exact original answer. | Fresh `plan-a11-01` passed the actual research/read cells in `01_research_and_execute.ipynb`, all 36 fiscal fields, 22 quantitative memo checks and three complete successful-query receipts under one verified plan. Its 173-word Markdown memo meets the 180-word limit. The original-period deployment check remains pending. |
| MSFT risk versus SPY | Real MCP research; five real notebook cells; independent prices/dividends, 1,256 common observations, 1,255 returns, annual returns, volatility and drawdown/recovery review. | Passed for the short `plan-a9-01` request. |
| AAPL fixed trend strategy | Fresh actual notebook research; complete SDK/MCP table reads; all 2,514 evaluation dates, 51 next-open fills, cash/equity, dividends, commission and published metrics independently reconciled. Original-period saved-plan execution and its new answer also passed. | Passed at the original period. Vendor session/auction basis remains disclosed. The fixed plan correctly rejects later-period execution; this is not rolling-period acceptance. |
| S&P 500 momentum screen | Fresh notebook and real MCP shared one operation; all 223,990 persisted price rows read over 28 pages, every shortlisted row and its arithmetic reconciled. | `provenance-a11-01` failed coverage review: reported universe/exclusions 501/4 instead of 503/6. `provenance-a11-02` built with the correct 503 count, then stopped before execution after the supervisor demanded unsupported identities for aggregate counts. The missing Native facts in its normal/bounded message are now fixed and tested; another fresh check remains required. |
| QQQ/SPY Treasury regimes | Actual MCP research and five notebook cells; 120 months, every regime statistic, prices/dividends and month-end clocks independently reconciled. All 2,521 yield observations also match Federal Reserve DGS10 history. | Passed for `plan-a9-02`. Uses latest history, not a point-in-time vintage guarantee. |
| MSFT plain-text follow-up | Actual notebook cells; same saved study/execution/thread, new answer ID, original revision unchanged. All 19 numerical claims in the 132-word brief checked against independent fiscal calculations. | Passed. Complete trace contains only saved-result audit and publication. |
| Screener JSON follow-up | Must use the accepted notebook 04 source, preserve every ordered row and coverage field, produce a new deterministic JSON answer and retain the original pin. | Pending accepted screener source; not substituted with a smaller synthetic table. |
| Clarification/reconnect | Real MCP admission, terminal `/leave`, fresh MCP reconnect, unselected notebook choices, empty-reply rejection, explicit fiscal reply in the same cell, and complete final reads. Same thread/checkpoint retained; one study execution. | Passed. Alpha11's stale validation-message cleanup also passed an isolated actual widget check without submitting a real answer. |

## Behavioral evidence

Public response SQL terminals qualify as study sinks; no dashboard exhibit is
required. Response-only MSFT/risk/macro cases returned their requested answer
without fabricating a dashboard link. AAPL has populated Native dashboard
content and an exact-execution Portal link; authenticated Portal rendering after
sign-in remains frontend acceptance, not a claim made by that link check.

The terminal, asynchronous notebook view and MCP share the same SDK session.
MCP uses structured progress and questions with no human renderer. Actual CLI
and subprocess-MCP observers left/rejoined the same native operation without
creating another graph run or engine job. Blank/recommended choices do not
silently answer questions. Publication ends research without a second assistant
narrative. Completed risk, macro, plain and clarification traces were checked
for tool/model errors and model calls after publication.

Saved-plan deployment reads complete computed data from the new native
execution, maps table/JSON deterministically and uses one bounded model call
only for declared text. Real computed-only replay made no graph/model call;
text replay made no supervisor/tool call. Same-handle reattachment retains the
new answer revision while the original research answer remains pinned.

The alpha9 later-period error was a client classification defect, not permission
to change a frozen plan. Alpha10/11 preserve the Native pre-admission rejection
reason instead of calling every HTTP 409 an accepted-input conflict. No new job
is created by the rejected request.

## Evidence ownership and remaining work

Private local evidence is retained under the task's
`output/interactive-sessions-2026-10-19` directory: versioned launch records,
redacted acceptance receipts, actual notebook outputs/screenshots, complete
Arrow page digests, immutable as-run snapshots, vendor captures and trace
exports. Raw licensed data and authentication material are not committed into
this public SDK repository.

Before closing ENG-2083: verify fresh named-notebook plan deployment and traces, independently
accept the corrected full screener, run/compare its JSON follow-up, inspect their
complete traces and native records, and update this ledger with the outcomes.
Keep all failed and abandoned attempts. Broader recovery/retry/retention systems
remain outside the goal.
