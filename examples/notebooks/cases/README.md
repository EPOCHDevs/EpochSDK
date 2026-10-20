# US equities desk case list

Each case is an ordinary desk request: a short `task`, a few `context` items
describing the data and business assumptions, and separate `outputs` for the
answer formats and fields. Users do not need to describe Epoch's internal tools,
SQL, publishing process or dashboard behavior.

For example, the MSFT task is: “Has Microsoft's growth become more cash-generative
over FY2023–FY2025? Highlight what changed in margins, capex and cash conversion.”
Its context identifies annual statements, USD and the cash-flow definitions; its
outputs request a fiscal-year table and a short Markdown memo.

Use notebook 01 for the five base scenarios, then notebook 03 for output variants.
Open the JSON beside this file to inspect each complete request.

| Order | Request file | Desk question | Published answer |
| --- | --- | --- | --- |
| 1 | [msft_fundamentals.json](msft_fundamentals.json) | How did MSFT growth, margins and cash conversion evolve in FY2023–FY2025? | Fiscal-year table + short Markdown memo |
| 2 | [msft_risk_json.json](msft_risk_json.json) | What were MSFT's returns and risk versus SPY in 2021–2025? | JSON only |
| 3 | [aapl_trend_strategy.json](aapl_trend_strategy.json) | Did a fixed 200-session AAPL trend filter reduce drawdown, and at what return cost? | Performance table + JSON + plain text |
| 4 | [sp500_momentum_screener.json](sp500_momentum_screener.json) | Which current S&P 500 names pass a trend/momentum screen at the price cutoff? | Ranked ticker table + one coverage table |
| 5 | [qqq_treasury_regimes.json](qqq_treasury_regimes.json) | How did QQQ versus SPY behave in months with large Treasury yield moves? | Three labelled regime rows + Markdown |
| 6 | [msft_fundamentals_plain.json](msft_fundamentals_plain.json) | Explain the same saved MSFT findings in plain text. | Plain text only; reuses case 1 |
| 7 | [sp500_momentum_json.json](sp500_momentum_json.json) | Give the identical saved shortlist and coverage to an application. | JSON only; reuses case 4 |

[msft_fundamentals_confirmation.json](msft_fundamentals_confirmation.json) is an
optional extra variant for notebook 02. It intentionally asks one fiscal-year
confirmation, then continues the same real-company review. It is not a sixth
research scenario or a requirement that complete requests ask extra questions.

## Data and interpretation

The notes below explain the financial definitions used by the output schemas and
the checks. They are not an additional prompt sent to the agent.

- **MSFT statements:** annual fiscal periods, with FY2022 revenue as the growth
  baseline. FCF is operating cash flow minus positive capex; cash conversion is
  operating cash flow / net income. Statements available at retrieval are latest
  snapshots and must not be presented as historical vintages.
- **Risk:** daily dividend-inclusive MSFT/SPY returns; sample volatility scaled
  by sqrt(252); drawdown is wealth / peak - 1, zero or negative. Both assets use
  the same dates for the worst-drawdown comparison. Returns are fractions.
- **Strategy:** AAPL, 2016–2025, one long position or cash, 200-session SMA,
  completed-close decisions and next vendor daily-open execution. The vendor's
  daily metadata does not establish exact session/auction prints; disclose that
  limitation. This prototype data basis was approved on 2026-10-19 after
  the first strict-session attempt stopped without executing.
  USD 1 million initial cash, 10 bps one-way native commission as the simplified
  all-in transaction cost, no additional slippage, zero cash interest and no
  leverage. The comparator is gross analytical buy-and-hold total return. The
  rule is fixed, with no search for a winning parameter.
- **Screen:** price cutoff **2026-10-16**, current roster captured at discovery.
  Use the same disclosed vendor-native daily basis without asserting verified
  regular-session/auction prices.
  This is not historical membership. Momentum is C(t-21)/C(t-252)-1; three-month
  return is C(t)/C(t-63)-1. Rank descending momentum, ticker ascending on ties;
  retain only prices above the 200-session SMA. Show up to 20 names without
  silently truncating the input universe or padding the output. Ticker rows do
  not require a time-series index.
- **Macro:** January 2016–December 2025, nominal US 10-year Treasury yield changes
  of at least +25 bp, at most -25 bp, or between those thresholds. December 2015
  supplies the first baseline. Compare contemporaneous monthly total returns;
  this is descriptive association, not a causal result or a predictive strategy.

## Saved-evidence variants

Cases 6 and 7 require the exact completed base answer. `load_case(..., source=...)`
adds its authorized study/execution IDs and answer revision to the ordinary
request context. Notebook 03 attaches to its thread and checks that the new
answer references the same execution while the original answer remains pinned.
No prepared-execution selector or new API is invented for this step.

The screener JSON must preserve every original row, rank and coverage value.
Native table int64 cells are decimal strings; their JSON counterparts are
integers. Large result sets belong in paged native tables; this small, at-most-20
shortlist is deliberately suitable for inline JSON.

## Request revision and acceptance

`desk-v2` replaces the long test-style tasks and contexts with short desk requests.
The parameters and output declarations are unchanged. The notebooks default to
`ATTEMPT = "desk-v2-01"`, with the same value for `BASE_ATTEMPT` in notebook 03,
so changed requests do not collide with accepted earlier operations. Keep that
ID to reconnect; choose another attempt when intentionally changing the request.

Earlier live acceptance covered MSFT fundamentals, MSFT risk JSON and the MSFT
plain-text variant using the earlier, more explicit requests. Those results do
not establish acceptance of this shorter revision. Its actual cells and traces
must be reviewed separately. Shape checks and a successful engine status do not
replace an independent financial/source audit.
