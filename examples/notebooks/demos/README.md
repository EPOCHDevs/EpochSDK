# US equities desk demos

Each notebook has one desk question and a short, readable sequence:

```python
epoch = connect()
review = task("msft_fundamentals", attempt="desk-v2-01")
display_request(review)
result = await run(epoch, review)
answer = await read(epoch, review, result)
```

Share this whole folder, including `demo_helpers.py`, `case_support.py`,
`notebook_identity.py` and `cases/`. It works without the rest of this checkout.
The recipient needs `epoch-sdk[notebook]` 0.1.0a6 or later, their Epoch login and
the two service URLs. No vendor/model credentials are used by these helpers.

| Notebook | Demo | Answer |
| --- | --- | --- |
| [01_msft_financial_quality.ipynb](01_msft_financial_quality.ipynb) | Growth, margins and cash conversion | Table + Markdown |
| [02_msft_risk_vs_spy.ipynb](02_msft_risk_vs_spy.ipynb) | Single-stock risk against the market | JSON |
| [03_aapl_trend_strategy.ipynb](03_aapl_trend_strategy.ipynb) | Fixed 200-day trend rule versus buy-and-hold | Table + JSON + text |
| [04_sp500_momentum_screen.ipynb](04_sp500_momentum_screen.ipynb) | Current-universe momentum watchlist | Shortlist + coverage tables |
| [05_qqq_treasury_regimes.ipynb](05_qqq_treasury_regimes.ipynb) | Equity performance across yield-change regimes | Table + Markdown |
| [06_msft_plain_text_followup.ipynb](06_msft_plain_text_followup.ipynb) | Another answer format from notebook 01's saved results | Plain text |
| [07_sp500_json_followup.ipynb](07_sp500_json_followup.ipynb) | Notebook 04's same shortlist and snapshot | JSON |
| [08_clarification_and_reconnect.ipynb](08_clarification_and_reconnect.ipynb) | Answer a question, leave it waiting and reconnect | Table + Markdown |

Start with notebook 01. Each research notebook has a short task, data context and
separate output declarations. `display_request` shows parameters first and an
expandable full request. Run the cells in order; the single SDK session owns progress,
questions and the published answer. Optional saved-study execution is clearly
separated from research. Follow-ups read their prerequisite from the services,
not from another notebook's Python variables or local files.

`answer.tables`, `answer.json` and `answer.text` contain the complete saved values.
Reading checks declared output shape and internal arithmetic, not vendor-source
accuracy. It does not display the answer twice. `review.request` remains the
ordinary typed `RunRequest`; the helpers are an example layer, not a new SDK or
workflow server. MCP continues to use the normal structured SDK interfaces.

## Saved study, later period

```python
later = date_range("year to date", as_of="2026-10-16")
display_request(review, period=later)
execution = await execute(epoch, review, result, period=later)
```

`execute` uses the original costs. A changed period gets a readable date suffix
on its native execution ID; the same dates reconnect to that execution. A timeout
or cancelled notebook wait does not cancel server work or submit a replacement.
No-period calls retain the original IDs. Execution currently returns engine
status; replaying saved answers is ENG-2086 work. Fixed fiscal labels, embedded
date filters and a saved roster are not rewritten by an engine-period override.

The public SDK's `date_range` returns the existing native `DatePeriodConfig`.
`"last year"` and `"last month"` mean the previous complete calendar period.
`years=1`, `months=3` and `days=30` are rolling calendar lookbacks, matching
EpochAI's LastN semantics. Month/year subtraction clamps to a real date.
Pin `as_of` in a demo; otherwise the caller's local calendar date is used. Resolved
inclusive dates are sent to Backend, never an unresolved moving expression.

## Dashboard

`await dashboard(epoch, result)` checks the saved study owner, exact execution
binding and native dashboard schema. It shows an **Open dashboard** link when
content exists and `EPOCH_PORTAL_URL` is set to the intended Portal origin. An
empty response-only study gets no dashboard link. This reads existing content;
it does not create presentation or imply that output tables require dashboard
tables. The optional presentation-request contract is described in
[the interface follow-up](../../../docs/notebook-demo-interface.md).

The `desk-v2-01` attempt values match the shorter request revision. Keep IDs to
reconnect; use another attempt for changed inputs or a deliberate data refresh.
Sharing a notebook does not grant access to someone else's saved work. A
recipient needs their own authorized service identity and operations.

The short MSFT fundamentals request has passed a real notebook run, complete
paged reads and reconciliation against independently checked statement values.
The other shorter requests still need their own live acceptance. The AAPL case
needs post-execution response-plan work; the screener and macro cases have
remaining service/data checks. These notebooks contain requests, not pre-filled
successful findings.

The generic chooser and low-level transport walkthroughs remain one folder up
for development. Notebook files here are generated from the canonical requests
with `python3 tools/generate_demo_notebooks.py`; `--check` detects drift in the
notebooks, copied case files and support modules. Generation
and validation call no vendor, model or service.
