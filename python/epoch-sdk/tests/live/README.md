# Live discovery acceptance

This opt-in suite calls a real Backend through the installed Python SDK and an
explicitly selected stdio MCP launcher. It makes one primary operation per case,
then reads its saved pages and optionally checks saved-universe reuse. It does not retry a failed lookup, change its query,
fetch observations, author a study, or invoke the supervisor.

The initial corpus has 310 cases, each run through both clients:

| Group | Cases | What is checked |
| --- | ---: | --- |
| Catalog | 43 | Complete directory, details and every source; all 45 implementation option/output contracts and endpoint schemas |
| Fundamentals | 90 | All 13 sources, supported reporting periods and date bases, including omitted `FilingDate` defaults |
| Corporate actions | 24 | All 12 sources, native bindings and selected value fields |
| Instruments | 60 | 48 reviewed name/typo/alias/directed-FX cases and 12 exact identities |
| Macro | 36 | All 11 sources, first/latest/intermediate vintages, tape, calendars, forecasts, market series and ratings |
| Market | 6 | Daily/minute primary/reference bars, FX, crypto and raw futures contracts |
| Screens | 18 | Explicit rosters, boolean membership, listing filters, current/historical index semantics and saved reuse |
| Boundaries | 20 | Inconsistent selectors/windows, unknown identities, quarantine, unsupported products and invalid fields |
| Concept search | 6 | Independent GDP/CPI/yield labels and measurement facts in the first returned page; first-place accuracy recorded separately |
| Batches | 7 | Multiple groups, subjects and products, distinct selectors, mixed unknown/success and atomic request errors |

`asset_catalog` and `custom_data` are constructor-only entries, not external
vendor identity searches. Their options are checked through the catalog.
Window anchors, lookback, roll/session controls, previous-observation behavior
and TE update controls belong to study authoring/execution. The catalog checks
their declarations; these tests do not pretend to execute them as search knobs.

## Run

Install the ordinary SDK test and MCP extras plus the compatible native SDK.
Point the client at the intended local or test services:

```bash
export EPOCH_BACKEND_URL=http://127.0.0.1:19052
export EPOCH_GRAPH_URL=http://127.0.0.1:12052
export EPOCH_LIVE_MCP_COMMAND=/absolute/path/to/the/registered-mcp-launcher
export EPOCH_LIVE_DISCOVERY=1
export EPOCH_LIVE_DISCOVERY_ARTIFACT_DIR=/absolute/path/to/a/new/receipt-directory
# Supply EPOCH_TOKEN using the normal Epoch login environment.
python -m pytest python/epoch-sdk/tests/live/test_discovery_live.py -q
```

Run from the repository root. A focused profile can use `-k`, for example
`-k 'macro-mb-vintage or financial-cash_flow'`. The default test run skips all
live calls. Provider/model credentials stay in Backend; they must not be added
to notebook, SDK or MCP configuration. MCP subprocesses receive only the
allowlisted client environment.

Each receipt preserves the request, expected result, first outcome, complete
saved rows, paging and timings, caller package versions, test-source hash and
MCP launcher path/hash. Counts distinguish the planned primary operation,
returned saved pages and an optional saved-universe read; they do not claim to
measure every HTTP request or provider call. SDK no-retry request options are
covered separately by transport unit tests. Reusing the same artifact directory fails rather than
overwriting an earlier outcome. Keep a failed attempt when correcting an
oracle or a product defect, and use a new directory for the next run.

## What a pass means

Binding tests check exact identities, constructor multiplicity, effective
selectors, schemas, original requests and honest coverage/status qualifiers.
An exact TE historical/rating address can retain `unknown` identity status when
only structural/base metadata is available. Unknown availability is not data
access or numerical validation. A native timestamp index is visible in the
catalog schema but is not a selectable value column.

Name relevance labels are independent fixtures inherited from the reviewed
native corpus. Broad names allow legitimate ambiguity; directed currency pairs
require the intended order. Screening checks complete saved membership rather
than a relevance top-k and preserves historical-integrity qualifications. Its
native bar-serveable venue gate applies even to explicit screen IDs; that
eligible domain is not the same as an unrestricted listing catalog. The current
index case checks an intersection with two explicit IDs, not a full current
roster. The historical index case checks the complete delivered pool and its
saved reuse; it does not certify vendor membership history independently.

The original `Euro Dollar` oracle assumed USD despite omitting its country/code.
The revised case measures broad catalog ambiguity across independently observed
dollar-family names. It also records the original EURUSD/USDEUR top-five recall
as a separate diagnostic, preserving the earlier failures. Passing ambiguity is
not a claim that the former narrower common-name ranking target was restored.

These are live integration tests, not a claim of universal retrieval accuracy
or financial correctness. They do not prove that an agent chooses the right
dataset from a natural-language research task. That separate acceptance lane
must withhold expected identifiers/selectors from the task and review the real
tool trace. Numerical studies, private-connector fixtures, cold-start deadlines,
provider outages and deployment validation also remain distinct evidence.
Native instrument names use lexical matching. Macro and TE-market retrieval
may use Backend's non-generative relevance ranker and vendor metadata APIs, so these tests can incur those costs even
though they make no generative AI calls.

Macro search returns ranked candidates, not a semantically verified source
selection. Its acceptance gate requires the correct source and measurement facts
within the first returned page of ten on one public query; receipts separately
report the correct source's position and first-place accuracy. A top result with
the wrong unit or definition must not be selected by the caller. Initial stricter
first-place failures are retained as ranking-quality evidence, not rewritten as
successful runs. The representative caller lane must prove that it chooses the
correct source before authoring or executing anything.

The frozen catalog inventory intentionally makes new sources/options/schema
changes fail review until the corpus is updated. Do not regenerate labels from
the response being tested merely to make a run green.
