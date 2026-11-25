# Epoch SDK

The [current SDK/MCP interface](docs/public-client-interface.md) distinguishes
interactive SDK research from the default composable MCP. The latter lets the
calling agent use native catalog/search/screening, then explicitly build and
execute studies. The separate `epoch_sdk.workflow_mcp` compatibility module
provides the saved-answer research workflow.

The [native discovery acceptance examples](examples/notebooks/native-discovery/README.md)
cover the shared catalog, a named asset, an S&P 500 financial universe and GDP
vintages. Their cells are prepared for live service/trace acceptance; no market
results are committed.

Start with the runnable [research/execute](examples/notebooks/01_research_and_execute.ipynb)
and [clarification/reconnect](examples/notebooks/02_clarification_and_reconnect.ipynb)
notebooks. The [US equities desk cases](examples/notebooks/cases/README.md) cover
company analysis, risk, a strategy, screening and macro analysis, with a separate
[saved-output variants](examples/notebooks/03_saved_output_variants.ipynb) notebook.
Their [setup notes](examples/notebooks/README.md) explain the local kernel and Epoch
authentication. These market cases are prepared for live review, not claimed as
completed research results.

Readable operation IDs reconnect notebooks and workflow-MCP callers to the same research
or prepared execution. See [reconnect usage and API semantics](docs/reconnect-operations.md).

Research with an explicit output contract through `EpochClient.research`,
`resume_research` and `research_status`. The result includes a saved response with
the requested named table, JSON and text parts. These advanced SDK methods remain
available alongside interactive `EpochClient.run`. The default composable MCP
uses caller-selected native data and specialist operations; `execute_saved`
remains a separate direct Backend action.

See [the research flow](docs/research-flow.md) for the current API, ownership and
validation limits. The older communication adapter remains available.

The local notebook/MCP cases and their scope are recorded in
[the October 18 verification](docs/verification-2026-10-18.md).

Public, multi-language clients for Epoch analysis workflows. Epoch SDK wraps
LangGraph SDK and the generated StratifyX SDK. Native data methods are shared
with the default MCP; the explicit workflow MCP shares the research session core.

## Repository layout

| Location | Ownership |
| --- | --- |
| `contracts/` | Shared language-neutral API, native parameter snapshot and validation fixtures |
| `python/epoch-sdk/` | Python client package, distributed as `epoch-sdk`, imported as `epoch_sdk` |
| `typescript/epoch-sdk/` | Preview typed workflow client for research, saved study execution and saved responses |
| `tools/` | Shared contract checks and native parameter synchronization |
| `docs/architecture.md` | Client/service boundaries and ordinary workflow |

Backend REST controllers, business persistence and native StratifyX generation
remain in EpochBackend. Graph server implementations live with their services.
This repository does not turn one language implementation into the API authority.

The Python package supplies strict request/error contracts, actual-value output
validation, a native-client access checker, interactive research sessions and a
saved-output reader. The research client returns native clarification questions and supports resuming
the same thread, executing a saved study directly through Backend, or reading
validated values from an explicit saved output mapping. See the
[SDK workflow example](docs/supervisor-workflow.md) and its current limits. The supplied-data research flow passed through actual SDK and workflow-MCP services,
including saved-answer reads and readable-ID reconnect.
`epoch-sdk` is released to PyPI by pushing a tag `epoch-sdk-v<version>` on a `dev` commit whose
package version is `<version>`. The [publish workflow](.github/workflows/publish-pypi.yml) then
builds it and waits for the maintainer's approval before uploading.

Computed research answers use native report outputs. Run the original study
first when needed, then build a saved-input report over its exact completed
execution. Native SQL/transforms compute tables and JSON; an optional bounded
cached `llm_call` produces text for declared response or dashboard sinks. Backend
saves the report's outputs, and the confirmed receipt ends the turn without a
second publication or assistant answer. Response-only work needs no dashboard.
An accepted single-text SDK request that needs no computation can complete from
the ordinary final reply automatically; ordinary platform discussion persists
in its conversation.

`SavedStudy.report_template` retains prepared original-plus-report replay.
Executing it runs a new original and its frozen report without a supervisor;
source and report jobs remain separate. Refining a completed result instead uses
explicit `input_tables` and never reruns that source. Response-plan APIs,
attachments and replay are retired (ENG-3105). Existing saved answers remain
readable directly without replay.

Saved answers contain named table, JSON and text parts with exact declarations
and immutable revisions. Another query may reuse the same execution while
retaining a different answer. Use `response_table` or `iter_response_table` to
read every row in bounded pages; [table access](docs/response-tables.md) describes
ordering, limits and older inline answers. The default composable MCP advertises
12 tools, including the two specialist interfaces `epoch_inspect_source` and
`epoch_build_study`; the caller can answer directly without publication. Source
inspection is a native read; only explicitly selected authoring or a declared
`llm_call` invokes a model. The former model-facing `audit_run`, `inspect_response_sources`,
`publish_response` and `edit_dashboard` tools are retired.

The low-level native publication API remains available for direct integrations:
`SupervisorClient.publish_response(request_id, content, thread_id=thread_id,
primary_execution_id=execution_id, expected_version=0)` followed by
`response(response_id, version=...)`. It starts no agent or engine job, but is not
a model-facing publication tool or the normal research finalization path. The
current package requires generated StratifyX `>=3.3.0rc24,<4`; generated-client
production and distribution remain with Backend.

## Saved model API

Saved models use Platform's source-owned contract, mirrored in
`contracts/platform-models.openapi.json`. Native fitting leaves a temporary,
execution-owned fit. An explicit Save copies that exact fit and its provenance;
it does not execute the study again.

```python
from epoch_sdk.models_api import AsyncEpochModels

models = AsyncEpochModels(base_url=api_url, token=bearer_token)
saved = await models.save_model(
    request_id="one-stable-save-intent", name="Demand forecast",
    execution_id=producer_execution_id, fit_name=fit_name,
    expected_digest=selected_digest,
)
facts = await models.read_model(saved.model_ref)
# Carry both saved.model_ref and saved.manifest_sha256 into a native consumer.
```

TypeScript exports `EpochModelsClient` from `@epochdevs/epoch-sdk/models-api`,
with `saveModel`, `listModels` and `readModel`. Use the API front door or the
Platform endpoint. The saved identity, artifact digest and manifest hash are
explicit pins; a missing object cannot select another fit. Native-owned detail
objects remain opaque JSON, while the Platform summary and Save request are
typed. Browsing and reading have no AI or numerical execution effects.

The generated clients are built by `tools/generate_models_api.py` from the
mirrored Platform contract using pinned Fern versions and source-derived
normalization. The saved-model fixtures and mocked HTTP tests verify the wire
contract; they do not establish live lifecycle acceptance.

## Development checks

Shared checks need no native SDK or Backend checkout:

```bash
python -m pip install 'jsonschema[format]>=4.23,<5' 'openapi-spec-validator>=0.7,<0.9'
python tools/validate_contract.py
python tools/sync_native_parameters.py --check
python tools/sync_platform_models_contract.py --check
python tools/generate_models_api.py --check
python tools/validate_saved_output_contract.py
python tools/validate_research_response_contract.py
python tools/validate_notebook_cases.py
```

For Python runtime tests, install a reviewed versioned StratifyX wheel from its
normal package workflow, then:

```bash
python -m pip install 'python/epoch-sdk[mcp,test]'
python tools/check_python_contracts.py
python -m pytest python/epoch-sdk/tests
```

The public workflow validates the shared contract, fixtures and standalone
TypeScript clients. The Backend release's SDK conformance step installs its exact
newly generated native Python and TypeScript packages and source-connections,
then runs all Python and TypeScript runtime tests against a pinned shared SDK
source commit. These include the Platform Files HTTP and native workflow checks.
Local tests use those same normal versioned packages.
Native SDK distribution/authentication remains owned by its package workflow;
no private wheel or registry credentials are copied into this public repository.

## Historical packages

Existing generated packages and the old sync script are retained. They are
historical snapshots, not the dependency source for the new wrapper. Current
native SDK generation and publication remain with EpochBackend.
The `python/epoch-protos/` and `typescript/epoch-protos/` folders are discarded
legacy artifacts; the current contracts, SDK and MCP do not use them, and the
old sync script no longer updates them.
See [the historical package notes](docs/legacy-packages.md).

One query publishes one answer with its own identity and revisions. Different queries
can reuse the same execution. Native response tables use exact relation
and field sources, independently of dashboard exhibits.
