# Standalone US equities desk notebooks

Each notebook has one fixed case, its complete request and its own setup. Share
an individual `.ipynb`; no case JSON, helper module or access to this checkout is
needed. The recipient needs an installed Epoch SDK notebook environment, an
Epoch login and access to the two services. Credentials are not stored in these
files.

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
separate output declarations. Long schemas and the login helper are collapsed
by default. Run the cells in order; the single session cell owns progress,
questions and the published answer. Optional saved-study execution is clearly
separated from research. Follow-ups read their prerequisite from the services,
not from another notebook's Python variables or local files.

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
with `python tools/generate_demo_notebooks.py`; `--check` detects drift. Generation
and validation call no vendor, model or service.
