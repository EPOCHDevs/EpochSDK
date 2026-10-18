# Epoch SDK ownership

- `contracts/openapi.json` is the language-neutral integration contract. Keep
  language bindings and SDK/MCP behavior consistent with it and its fixtures.
- Implement clients under their language directories. Python lives at
  `python/epoch-sdk`; future language clients use the same contracts.
- Epoch SDK wraps LangGraph SDK and generated StratifyX SDK. Backend owns its
  native REST APIs, controllers, persistence and native SDK generation. Graph
  server implementations belong to their service repository, not a client SDK.
- Do not hand-edit or restore historical generated packages as new client
  dependencies. Existing generated SDK snapshots are retained for history.
- `python/epoch-protos/` and `typescript/epoch-protos/` are discarded legacy
  artifacts. Do not use, sync, publish or revive them for the SDK/MCP work.
- Use the installed, versioned native SDK and keep its closed model types through
  request handling. Validate untrusted wire inputs before invoking services.
- Run shared contract checks and the affected language tests. Distinguish schema
  checks, native-client tests and real service integration evidence.
