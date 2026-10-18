# Shared contract

`openapi.json` is the language-neutral API contract for Epoch SDK clients and MCP.
It defines the eight logical operations, requests, named outputs, acceptance and
domain errors. Its REST paths are illustrative bindings, not another deployed
gateway. It is the earlier v0.9 draft: its separate-attempt and terminal-only
clarification bindings need reconciliation with the current stateful supervisor
direction before they can define the full analysis adapter.

`supervisor-native.schema.json` snapshots the current supervisor's owned
interrupt/answer wire without importing or running its application. It is an
interoperability input for language wrappers, not a second agent protocol.
Regenerate/check it with `tools/snapshot_supervisor_wire.py --epoch-ai PATH
[--check]` against a reviewed EpochAI checkout. The source commit and file hash
are recorded; ordinary component tests require only the checked-in snapshot.

`native-parameters.json` is the projection of the native Backend parameter
schemas used by the integration contract. Native API schema generation remains
owned by EpochBackend. The Python package carries a generated copy so installed
clients do not need a Backend checkout.

`validation-cases.json` is reusable by every language client. `schema_valid`
records what standard JSON Schema can establish; `valid` also includes semantic
rules such as unique output/column names, permitted schema references and option
membership. Language runtimes must enforce both parts.

Change the shared contract deliberately, update each affected binding, and run
the conformance checks. One language's implementation does not define the API for
the others.
