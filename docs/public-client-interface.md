# SDK workflows and composable MCP tools

The default MCP lets Codex or Claude replace Epoch’s supervisor. The caller chooses when to discover data, reuse it across studies, build, execute, compare and answer. The MCP does not call `epoch-ai`, require publication or create a final answer on the caller’s behalf.

| Tool | Purpose | Epoch model call |
| --- | --- | --- |
| `epoch_dataset_catalog` | Read the Backend dataset directory, complete loader options and saved-dataset metadata. | None |
| `epoch_search_dataset` | Resolve native instruments/series and rank metadata alternatives. | No generative model |
| `epoch_screen_assets` | Resolve or reuse a complete asset universe with explicit membership semantics. | None |
| `epoch_inspect_source` | Read selected source observations and optional read-only queries. | None |
| `epoch_build_study` | Author, validate and save studies from the selected references. | Existing study author |
| `epoch_execute` | Execute a saved study for an explicit period. | None |
| `epoch_extension_inputs` | Read exact selected retained tables, types and frozen source. | None |
| `epoch_save_extension` | Compile/save caller-authored EpochScript over one saved execution. | None |
| `epoch_execute_extension` | Execute or reconnect to that saved program by operation ID. | Only explicitly declared cached commentary |
| `epoch_audit_run` | Ask targeted questions of completed execution IDs, including comparisons. | Existing audit specialist |
| `epoch_find` | List owned tools workspaces or saved study IDs. | None |
| `epoch_read` | Read owned work, exact saved answer/table pages or pinned presentations. | None |
| `epoch_status` | Observe a tool handle, native execution ID or extension operation ID. | None |
| `epoch_resume` | Explicitly answer a specialist interrupt, when one exists. | Only the selected specialist continues |

## Reuse saved results

Both `AgentToolsClient` and `EpochClient` expose `extension_inputs`,
`save_extension`, `execute_extension`, `extension_status`, `response`,
`response_table` and `extension_presentation`. The three extension MCP tools
call these same methods; they do not invoke a supervisor or study author.

Read the source's selected input catalog, supply an EpochScript program using
its flat enum references, save the returned definition, then execute it with
the original `source_execution_id` and a reusable `operation_id`. Tables, JSON
and native dashboard reporters are independent destinations. Text commentary
is optional and explicitly model-backed. Read the confirmed output references:
the derived `execution_id` differs from the source, and presentation edit zero
is an exact saved version. Keep earlier answer/view pins when choosing a newer
report. A page size bounds one read, never the complete table.

The default MCP advertises 14 tools. Diagnostic and comparison tools remain
available until the separately tracked parity/retirement gate; this addition
does not claim that they have been replaced in every result family.

## Reuse discovery

1. Read `epoch_dataset_catalog` for supported datasets and their options. Ask for details of selected source IDs to see vintage/revision, fields and clock choices. The prose and schemas come from Backend.
2. Use `epoch_search_dataset` for asset/series identities, or `epoch_screen_assets` for a whole cohort. Search returns its unchanged receipt and, when inline rows are omitted, one bounded stored page. Continue with `epoch_read(kind="dataset_search", identifier=result_ref, cursor=next_cursor)`; no provider search is repeated. Metadata page limits are 1..10, matching Backend.
3. Pass exact record/result references or the `universe_ref`, plus the selected dataset/options, as `source_refs` to `epoch_build_study`. It retains and validates them internally. A historical universe needs the requested study period inside its captured membership window. Metadata does not certify populated observations or account access.
4. Keep the build handle and poll `epoch_status`. Its saved outcome returns retained `source_refs` for later builds, including after the original working search expires. Reuse the workspace and select a new study slot for a different study. Registry compatibility still applies.
5. Execute a saved study ID with `epoch_execute`, then observe its native execution ID with `epoch_status(kind="execution")`.
6. Read dashboard values directly, or use `epoch_audit_run` for targeted analysis of exact completed execution IDs. The caller answers the user; publication is not a completion requirement.

A workspace is an ordinary owner-scoped LangGraph thread using the `epoch-tools` graph. That graph has only admission and tool-execution nodes: no supervisor model, planner, next-action model or publication loop. Original typed specialist state and native checkpoints stay in EpochAI. Do not submit internal state, bearer tokens, approval receipts or `ToolRuntime` as tool arguments.

Specialist operations return a native background run handle. Reading status, reconnecting or closing an MCP client does not submit the tool again. Never blindly repeat an uncertain mutation; retain the accepted handle or execution ID. This initial surface adds no recovery worker, retry policy or separate operation database.

## Native ownership

Dataset catalog/search/screening, metadata paging, execution, study reads and dashboard reads use the generated StratifyX client directly. They do not route through EpochAI. Execution reads and audit bindings verify the owned per-execution snapshot before trusting an execution ID. A response plan is neither required nor replayed by this MCP’s `epoch_execute`.

Specialist tool schemas come from authenticated `GET /api/v1/agent-tools` on EpochAI. Parameter schemas are generated from the actual tool owners, retaining their recursive definitions, constraints and tags. MCP adds `task` and optional `workspace_id` to those specialist calls. Native data methods share `DatasetClient` with the workflow SDK; they do not invoke the tools graph or a Discovery agent. Schema loading is a read-only service request, not a model call.

The SDK exposes this same transport as `epoch_sdk.agent_tools.AgentToolsClient`. For example:

```python
from stratifyx.types import DatasetSearchQuery

catalog = await tools.dataset_catalog(source_ids=["cash_flow"], include_details=True)
found = await tools.search_dataset([DatasetSearchQuery.model_validate({
    "request_id": "issuer",
    "subjects": [{"kind": "asset_name", "name": "Microsoft", "asset_type": "Stocks"}],
})])
```

`EpochClient` exposes those same `dataset_catalog`, `search_dataset`,
`screen_assets` and `read_dataset_search` methods. Only user authentication and
service URLs belong in the client; vendor/model credentials stay on the services.
Native search can use Backend's non-generative reranker. The retired
`epoch_discover` LLM tool is not advertised by the default MCP; old operation
handles remain readable through the compatibility client.

## Notebook and workflow SDK

`EpochClient.run`, `execute`, `resume`, `status` and `read` keep their existing research/published-answer workflow. Notebook and terminal rendering are unchanged. Saved response plans still replay through that explicit workflow interface.

The old five-tool MCP remains an explicit compatibility module, `python -m epoch_sdk.workflow_mcp`. It is not the default MCP installation. See the [historical alpha13 contract](alpha13-workflow-interface.md) for those operation IDs and pinned-response semantics. The default `epoch-mcp` command uses the composable tools above; reconnect the MCP host after upgrading.

## Local services

The composable graph must be deployed before switching clients. `EPOCH_MCP_GRAPH_URL` can select a separate Python preview service while notebooks continue using their existing graph URL. Clients receive only the Epoch identity and service addresses; vendor/model credentials remain server-side.
