# Epoch SDK

Readable operation IDs reconnect notebooks and MCP callers to the same research
or prepared execution. See [reconnect usage and API semantics](docs/reconnect-operations.md).

Research with an explicit output contract through `EpochClient.research`,
`resume_research` and `research_status`. The result includes a saved response with
the requested named table, JSON and text parts. Both notebooks and MCP use this
flow; `execute_saved` remains a separate direct Backend action.

See [the research flow](docs/research-flow.md) for the current API, ownership and
validation limits. The older communication adapter remains available.

The local notebook/MCP cases and their scope are recorded in
[the October 18 verification](docs/verification-2026-10-18.md).

Public, multi-language clients for Epoch analysis workflows. Epoch SDK wraps
LangGraph SDK and the generated StratifyX SDK; MCP uses the same client behavior.

## Repository layout

| Location | Ownership |
| --- | --- |
| `contracts/` | Shared language-neutral API, native parameter snapshot and validation fixtures |
| `python/epoch-sdk/` | Python client package, distributed as `epoch-sdk`, imported as `epoch_sdk` |
| `typescript/` | TypeScript packages; the new integration wrapper will use the same shared contract |
| `tools/` | Shared contract checks and native parameter synchronization |
| `docs/architecture.md` | Client/service boundaries and ordinary workflow |

Backend REST controllers, business persistence and native StratifyX generation
remain in EpochBackend. Graph server implementations live with their services.
This repository does not turn one language implementation into the API authority.

The Python package supplies strict request/error contracts, actual-value output
validation, a native-client access checker and a thin stateful supervisor/MCP
adapter and a saved-output reader. The adapter returns native clarification questions and supports resuming
the same thread, executing a saved study directly through Backend, or reading
validated values from an explicit saved output mapping. See the
[SDK/MCP example](docs/supervisor-workflow.md) and its current limits. The complete
named-output analysis flow is implemented and component-tested; real-service
research proof remains pending.
Package registry publication is separate; this is public source, not a released
PyPI package.

The saved research response API serves both notebook users and MCP agents. Use
`SupervisorClient.publish_response(request_id, content, thread_id=thread_id, primary_execution_id=execution_id, expected_version=0)`
after analysis, then `response(response_id, version=...)` to read the same
Backend-owned answer. A response contains named table, JSON and text parts and
their declarations; updates create another revision of that answer. Another query may reuse the
same execution while retaining a different answer.
MCP exposes `epoch_publish_response` and `epoch_response` over the same methods.
Newly assembled tables reference native saved data. Use `response_table` or
`iter_response_table` to read all rows in bounded pages; MCP uses
`epoch_response_table`. See [table access](docs/response-tables.md) for the wire
contract, retrieval ordering and compatibility with older inline answers.
This publication path starts no agent or engine job. It requires the generated
StratifyX 3.3.0rc3 response API. The existing supervisor publication tool is integrated in EpochAI #752. Complete
real research integration proof remains pending.

## Development checks

Shared checks need no native SDK or Backend checkout:

```bash
python -m pip install 'jsonschema[format]>=4.23,<5' 'openapi-spec-validator>=0.7,<0.9'
python tools/validate_contract.py
python tools/sync_native_parameters.py --check
python tools/validate_saved_output_contract.py
python tools/validate_research_response_contract.py
```

For Python runtime tests, install a reviewed versioned StratifyX wheel from its
normal package workflow, then:

```bash
python -m pip install 'python/epoch-sdk[mcp,test]'
python tools/check_python_contracts.py
python -m pytest python/epoch-sdk/tests
```

The public workflow validates the shared contract and fixtures. The Backend
producer's SDK compatibility job supplies its newly generated native wheel for
Python runtime/conformance checks. Local tests can use that same versioned wheel.
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
