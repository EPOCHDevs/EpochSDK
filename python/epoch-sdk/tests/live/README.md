# Live discovery acceptance

The opt-in suite calls Platform/GDS through the ordinary Python CatalogueClient. It does not launch the retired composable MCP, invoke a research agent or call Backend search.

The retained corpus has 314 intent cases across constructor capabilities, asset identities, fundamentals, corporate actions, TE/Macrobond series and releases, complete screens, ambiguous names and multi-need queries. Constructor windows, selected vintages, reporting periods and value-field selectors now belong to authoring/execution; their old request-error cases are explicitly marked for that boundary rather than being described as search coverage.

Set EPOCH_PLATFORM_URL, EPOCH_TOKEN and EPOCH_LIVE_DISCOVERY_ARTIFACT_DIR to an isolated test service and a fresh evidence directory. Then run:

```bash
EPOCH_LIVE_DISCOVERY=1 python -m pytest python/epoch-sdk/tests/live/test_discovery_live.py -q
```

Each case retains its original intent and first response. Failures are not retried with a different query. Saved universe pages verify complete membership, ownership and frozen replay; ranked search pages are not expanded to rescue a failed first-page identity match. A schema pass alone does not establish numerical coverage or retrieval quality. Native compilation/execution, provider feedability, field fidelity, context size and labelled retrieval evaluation have separate evidence.

The default offline SDK suite skips live cases. A skipped case is not acceptance evidence. Provider and model credentials remain in GDS; the client receives only the normal caller token.
