# Epoch SDK

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

The initial Python package implements strict request/error contracts and a
native-client access checker. The complete analysis/SDK/MCP flow is still being
implemented. Package registry publication is separate; this change publishes
source, not a completed service or a released PyPI package.

## Development checks

Shared checks need no native SDK or Backend checkout:

```bash
python -m pip install 'jsonschema[format]>=4.23,<5' 'openapi-spec-validator>=0.7,<0.9'
python tools/validate_contract.py
python tools/sync_native_parameters.py --check
```

For Python runtime tests, install a reviewed versioned StratifyX wheel from its
normal package workflow, then:

```bash
python -m pip install 'python/epoch-sdk[clients,test]'
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
