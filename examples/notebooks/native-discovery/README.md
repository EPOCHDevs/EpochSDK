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
