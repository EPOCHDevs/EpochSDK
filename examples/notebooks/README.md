# Try the SDK with a US equities desk case

For sharing and demos, use the [individual case notebooks](demos/README.md).
There is one standalone notebook for each of the five desk cases, two separate
format follow-ups and a clarification/reconnect example. Each includes its own
request and setup; it does not import the local notebook helpers or case files.

The generic **01_research_and_execute.ipynb** below is retained as a development
walkthrough. Select the **Epoch SDK (local prototype)** kernel. Its case files
live in the **cases** subfolder beside the notebooks;
[the case list](cases/README.md) explains the desk questions, output
formats and data assumptions. Each task is one or two short sentences; context
describes the data and business assumptions, while `outputs` declares the answer.

The five scenarios use real vendor data: MSFT financial quality, MSFT risk versus
SPY, an AAPL trend filter, an S&P 500 momentum shortlist, and QQQ/SPY sensitivity
to US Treasury yield changes. Two further requests change the format of existing
MSFT/screener evidence. No market result or winning backtest has been pre-filled.

**Request revision:** `desk-v2` uses shorter, natural desk requests. Earlier live
acceptance covered MSFT fundamentals, risk JSON and the saved plain-text variant
with more explicit requests. This revision needs its own live acceptance; those
earlier runs do not prove that the shorter requests work.

## Notebook order

1. **01_research_and_execute.ipynb**: choose a base `CASE_FILE`, inspect the
   request, research, display/check the answer, and optionally continue through
   the separate saved-study execution steps. It defaults to MSFT fundamentals.
   Run it again with another base case to try another desk task.
2. **02_clarification_and_reconnect.ipynb**: an optional advanced transport test.
   The low-level calls are exposed deliberately to test observer disconnects;
   normal notebook sessions use the single call in notebook 01. An MSFT fiscal-year
   confirmation demonstrates a natural-language answer, a disconnected local
   wait and reconnecting to the same operation. The extra question is deliberate;
   normal base cases do not force it. Disconnecting does not cancel the server.
3. **03_saved_output_variants.ipynb**: after completing the matching base case in
   notebook 01, request MSFT plain text or the same screener as JSON. It reads the
   original operation, supplies its exact saved identities, attaches to its
   thread, and checks that the answer uses the same execution. It does not start
   the prerequisite case automatically.

Each cell explains what it does. `epoch = connect()` prepares the normal SDK
client from the environment; `await check_services()` prints package versions
and checks the service health endpoints. Neither starts research. The later
`epoch.run(...)` cell starts actual model/vendor/engine work. That one call renders
live activity, collects explicit replies in notebook widgets, resumes the same
checkpoint and displays the saved answer. No manual polling or reply code is
needed for normal research. Output variants
start a model turn over retained evidence; their instructions prohibit new
discovery and execution, and live tool traces still need review.

## Choosing cases and IDs

Change `CASE_FILE` in notebook 01 to another base request in `cases/` and rerun
from the beginning. Each file contains ordinary SDK `task`, `context`,
`parameters` and `outputs` fields (output variants omit new-execution parameters).
`cases/index.json` is a local catalogue, not an API request; it is not sent to Epoch.

IDs include the case name and `ATTEMPT`, for example
`notebook-demo-msft_fundamentals-desk-v2-01-research` and
`notebook-demo-msft_fundamentals-desk-v2-01-execute`. The default
`ATTEMPT = "desk-v2-01"` keeps these changed requests separate from earlier runs.
Keep the same attempt to reconnect
after a kernel restart. Identical accepted inputs attach; changed accepted inputs
require a new attempt. `EPOCH_NOTEBOOK_PREFIX` can provide a separate namespace.

The output-variant notebook has `BASE_ATTEMPT` and `VARIANT_ATTEMPT`. Keep the base
attempt equal to the one used in notebook 01. Exact source identities are loaded
from that completed answer, not guessed from a name or a last execution.

The screener fixes its price cutoff at **2026-10-16** and records its actual
current-membership snapshot time. Reusing its research ID reads that saved
snapshot. An intentional new membership snapshot needs a new research ID; a
prepared execution is not an automatic membership refresh.

## What is checked

Every case validates against the shared request contract and installed native SDK
models. Every output field has a description, with units for numerical measures.
Answer checks cover complete pagination, requested output names/types, fiscal-year
ordering, FCF/margin/conversion arithmetic, risk return differences, strategy
table/JSON agreement, screener ranks/coverage, and macro regime counts. The JSON
screener variant compares every cell and the original ordering.

These are internal consistency checks, not an independent source audit. Live
review must still reconcile source observations, inspect actual strategy
signals/fills/costs, check macro timing and read the conclusions. Schema-valid
JSON does not establish factual accuracy. From the repository root:

```bash
python tools/validate_notebook_cases.py
```

This offline validator needs no service, native build or market run. Notebooks
are committed with empty outputs. The old deterministic supplied-data fixture
remains at `examples/research-service-proof.case.json` for its automated proof
runner; it is not a desk case or a notebook default.

## MCP uses the same requests

Pass the selected base file's object to `epoch_research`, with its own readable
operation ID. No notebook-specific SDK or server is involved. The notebook's
helpers only load local files, format displays and check results.

For an output variant, notebook 03 displays the fully resolved request with the
source study/execution identities. Supply that request and original thread ID to
MCP's `epoch_research`, using a distinct operation ID. Do not submit an unresolved
variant alone, select another execution or refresh market data.

## Another environment

Use Python 3.12 or later and the matching native StratifyX package from its normal
distribution workflow. These notebooks were prepared with StratifyX 3.3.0rc4 and
Epoch SDK 0.1.0a4. Install this checkout's `python/epoch-sdk[notebook]`, plus
`ipykernel` and `jupyterlab`, in the selected environment.

Supply only these client settings to the notebook process:

- `EPOCH_BACKEND_URL`: the intended Backend origin.
- `EPOCH_GRAPH_URL`: the intended EpochAI/LangGraph origin.
- `EPOCH_TOKEN`: your Epoch identity token.

Backend retains vendor configuration and EpochAI retains model configuration.
Do not put credentials in cells or commit credential-bearing outputs. The prepared
server supplies client settings to its kernels; another notebook environment
needs its own client settings.

Epoch identity tokens expire. On 401, refresh through the normal login flow and
create a fresh client; keep the same operation ID. Restarting the local notebook
launcher refreshes the prepared environment's identity token.

The prepared server also configures `EPOCH_NOTEBOOK_TOKEN_COMMAND`, a trusted
local login-helper argv list. `connect()` and `check_services()` obtain a current
Epoch token from that helper when you rerun setup, rather than keeping the
server's expired startup token. The helper uses the existing Epoch login cache;
it returns only the current identity token. No vendor or model credentials are
returned to the notebook. Independently configured notebooks can still use a
static `EPOCH_TOKEN` and their own normal identity-refresh flow.

See [interactive sessions](../../docs/interactive-sessions.md) for the same
terminal experience, structured MCP progress and headless event API.
