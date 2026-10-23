# Reports from completed results

Share this whole folder: each notebook has a short question, a local case file and
the same small helpers. No credentials, financial values or private execution IDs
are committed. Use `epoch-sdk[notebook]` **0.1.0a25+** with normal native SDK
**3.3.0rc19+**, a running Backend and EpochAI.

Prepare `EPOCH_TOKEN` (or the existing notebook login helper), `EPOCH_BACKEND_URL`
and `EPOCH_GRAPH_URL`. These are Epoch access settings; vendor/model credentials
belong to the services. Set the following source IDs to your existing completed
results, or pass `source_execution_id=` to `task(...)` explicitly:

- `EPOCH_MSFT_EXECUTION_ID`: Microsoft annual fundamentals with recorded fiscal
  year, revenue and operating cash flow in reported USD units.
- `EPOCH_AAPL_EXECUTION_ID`: an AAPL backtest with recorded orders and side values.

Set `EPOCH_PORTAL_URL` to your Portal address to open the requested dashboard.

| Notebook | What it does |
| --- | --- |
| [01 · Microsoft annual figures](01_msft_annual_figures.ipynb) | A natural question produces matching native JSON/table outputs, then reads every row and reconnects to the same answer. |
| [02 · AAPL order activity](02_aapl_order_activity.ipynb) | Counts recorded orders by side, requests a short data-backed note and explicitly adds a side-mix dashboard chart. The table/note stay in the answer. Order intent is not fill or return evidence. |
| [03 · Rerun and reuse text](03_reexecute_and_reuse_text.ipynb) | Runs the exact definition from 02 under a new operation ID, compares complete values/text/provenance and preserves the original answer pin. No supervisor or source backtest is run. |
| [04 · Unavailable input](04_unavailable_input.ipynb) | Inspects actual table metadata and verifies a deliberate unknown-table refusal, with no replacement source or fabricated output. |

The first two notebooks use `epoch.run(...)`'s normal activity and question
widgets. Native replay displays its saved answer through the same SDK renderer.
`read(...)` returns complete tables for Python use without reprinting the answer;
the rendered preview is not a total-row limit. Keep operation IDs to reconnect;
use a new attempt for intentionally changed inputs.

Notebook 03 compares retained outputs; provider/cache traces are still needed to
prove zero new inference. Successful cells alone do not establish every numerical
claim: compare with independent source data and review root/child traces. No
notebook starts a source study or silently fills a data gap.

Coding agents use the same native lifecycle through MCP:
`epoch_extension_inputs`, `epoch_save_extension`, `epoch_execute_extension`,
`epoch_status(kind="extension")` and `epoch_read`. They supply EpochScript or reuse
an existing definition; the MCP interface does not invoke the notebook renderer
or a hidden supervisor. Authoring helpers use their explicitly advertised models.

Regenerate source notebooks with `python tools/generate_report_notebooks.py` from
the repository root; `--check` checks only local files. Executed acceptance copies
and full trace receipts are separate evidence, not prefilled notebook outputs.
