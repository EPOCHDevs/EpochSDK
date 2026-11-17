# SDK workflows and discovery

Current discovery is owned by Platform and GDS. Compile/run and execution validation remain native engine operations. The composable `epoch-mcp` command, `epoch-tools` graph and `AgentToolsClient` have been retired. The public research MCP is served by EpochAI.

## Search and selection

```python
from epoch_sdk import CatalogueClient
from epoch_sdk.discovery_types import DiscoveryQuery

catalogue = CatalogueClient(platform_url, token)
found = await catalogue.search_dataset([
    DiscoveryQuery(id="power", query="French electricity prices", mode="discover")
])
selected = await catalogue.select(found.session_id, [found.candidates[0].id])
await catalogue.aclose()
```

Check source meaning, product, support and coverage before choosing. Full details use the first 30,000 bytes of the response budget; compact identity rows fill the 40,000-byte ceiling. `details()` resolves a compact candidate within its owned session. Incomplete inventory, no match, provider failure and held sources remain distinct.

`EpochClient.connect` accepts a separate `platform_url`; a shared public gateway can use the same origin as native operations. Caller tokens may be renewable providers. Vendor credentials remain inside GDS.

## Native execution and retained results

`EpochClient` exposes `extension_inputs`, `save_extension`, `execute_extension`, `extension_status`, `response`, `response_table` and `extension_presentation`. Preserve returned source identities and publication pins. A page size bounds a read, never the complete result table.

Read acquisition provenance with `execution_provenance` or `response_provenance`; preserve its original acquisition/cache clocks. Metadata visibility does not establish populated observations or entitlement. A failed lookup never proves zero observations.

The notebook research workflow (`run`, `execute`, `resume`, `status`, `read`) remains available. `python -m epoch_sdk.workflow_mcp` is its independent compatibility adapter; it does not restore the retired composable tool server.
