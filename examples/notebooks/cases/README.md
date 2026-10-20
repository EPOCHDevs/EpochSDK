# US equities desk case list

These are runnable requests, not completed findings. Open the JSON beside this
file to see the full natural-language question, assumptions and output contracts.
Use notebook 01 for the five base scenarios, then notebook 03 for output variants.

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

## Fixed meanings

- **MSFT statements:** annual fiscal periods, with FY2022 revenue as the growth
  baseline. FCF is operating cash flow minus positive capex; cash conversion is
  operating cash flow / net income. Statements available at retrieval are latest
  snapshots and must not be presented as historical vintages.
- **Risk:** daily dividend-inclusive MSFT/SPY returns; sample volatility scaled
  by sqrt(252); drawdown is wealth / peak - 1, zero or negative. Both assets use
  the same dates for the worst-drawdown comparison. Returns are fractions.
- **Strategy:** AAPL, 2016–2025, one long position or cash, 200-session SMA,
  completed-close decisions and next daily regular-session open execution.
  USD 1 million initial cash, 10 bps one-way native commission as the simplified
  all-in transaction cost, no additional slippage, zero cash interest and no
  leverage. The comparator is gross analytical buy-and-hold total return. The
  rule is fixed, with no search for a winning parameter.
- **Screen:** price cutoff **2026-10-16**, current roster captured at discovery.
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

## Review status

Requests, schemas, notebook syntax and local checking helpers are validated
offline. No real vendor/model case has been executed as part of preparing these
files. Financial values must be independently reconciled during live review;
do not treat generated JSON, prose or a successful engine status as that proof.
Unavailable data or modeling capability must stay an explicit gap.
