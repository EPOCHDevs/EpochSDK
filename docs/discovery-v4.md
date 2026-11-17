# Discovery v4 migration

`CatalogueClient` talks to Platform. Native StratifyX remains the execution client. Configure the two origins independently for local testing; production uses the coordinated public routing release.

The Python preview is `0.1.0a44`; the TypeScript preview is `0.1.0-alpha.9`. A local preview is not a published package. Consumers must use the exact coordinated package artifacts when the service release is approved.

## Search, inspect, select

```python
from epoch_sdk.catalogue import CatalogueClient
from epoch_sdk.discovery_types import DiscoveryQuery

catalogue = CatalogueClient(platform_origin, bearer_token)
try:
    result = await catalogue.search_dataset([
        DiscoveryQuery(
            id="electricity",
            query="France electricity prices",
            mode="discover",
            filters={"providers": ["TradingEconomics"]},
        )
    ])
    # Review result.needs and result.candidates. A compact candidate may
    # require details; an unavailable or held source cannot be selected.
    detail = await catalogue.details(result.session_id, [reviewed_candidate_id])
    selected = await catalogue.select(result.session_id, [reviewed_candidate_id])
finally:
    await catalogue.aclose()
```

Selection returns the exact native constructor, arguments, registry version and available metadata. Preserve that binding; do not reconstruct it from a display name. TE economic IDs and colon-delimited market symbols are different inputs. An approved proxy has an explicit qualification. Vendor-advertised coverage and accepted cached coverage are separate fields; neither proves every requested observation is present.

Search is a bounded candidate operation. `needs_detail`, `incomplete`, `no_match`, provider failures and continuation cursors are meaningful states. Long company descriptions in search are original-text excerpts of at most 480 characters plus an ellipsis; `details` returns the full original text. Semantic scores remain internal. Exact lookup and ordinary browse do not invoke the embedding model or reranker.

## Complete asset universes

Use screening for a complete cohort, not semantic search or its sample rows:

```python
universe = await catalogue.screen_assets({
    "kind": "screen",
    "screen": {
        "index": ["SP500"],
        "index_membership_mode": "CurrentSnapshot",
    },
})
if universe.status == "ready":
    binding = await catalogue.bind_universe(universe.universe_ref)
    # binding.ids contains the full roster. Convert the wire through
    # epoch_sdk.catalogue.native_universe_screen(binding) before passing it
    # to native execution; this preserves integer bounds and required arrays.
```

The sample is a preview, not a substitute for the roster. `incomplete` and `over_limit` cannot issue a usable universe. A historical request requires `PointInTime` and an explicit membership window; execution must retain its per-date membership gate. Current-cap lookups remain observational and must not silently become historical capitalization rules.

## Retained evidence and clients

`read_retained` reopens original owner-scoped `discovery-handoff:v1` evidence and unexpired `discovery-result:v1` records. It does not rerun a vendor query or accept arbitrary SQL. Expired working references do not become fresh searches. The old one-hour `metadata-snapshot:v1` SQL surface and separate query-proof addressing are not part of the new public search contract; retain their original artifacts during Backend cleanup.

The old dataset-discovery MCP server is removed. The separate workflow MCP tools remain. Direct application clients, notebooks and the AI use the same Platform discovery contract.

The AI keeps full transport evidence for the UI/checkpoint and projects a smaller model view. After a successful selection it removes resolved alternatives while preserving unanswered needs and unselected private inputs. This projection never edits the original retained records.
