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

`saved-output-manifest.schema.json` is the explicit per-execution read receipt
for named values, reusing declarations from `openapi.json`. It identifies exact
native artifact/field bindings; its example uses placeholders. Publishing the
receipt from the accepted workflow remains separate Backend/tool work. Check it
with `tools/validate_saved_output_contract.py`; all references resolve to local,
checked-in resources.

`research-session.schema.json` defines the five client session event variants
used by Python renderers and structured MCP progress. It references the existing
workflow/response schemas instead of copying native result or parameter models.
`tools/validate_session_contract.py` checks reusable fixtures without private
client dependencies; `tools/sync_session_contract.py --check` verifies the Python
binding deliberately. Service-defined UI component names/properties stay open
extension points inside a closed source UI envelope. This adds no REST server.

The `response-plan*.schema.json` files define the proposed versioned replay
contract in [ENG-2086](https://linear.app/epoch-inc/issue/ENG-2086). Query inputs
are Backend-issued successful-query references or exact native relation
projections. Table and JSON mappings are deterministic; text steps explicitly
select computed inputs and a server-owned interpretation policy. A published
plan retains its original answer/source pin and effective non-secret model
settings. `response-plan.cases.json` contains structural fixtures, not market
results. `tools/validate_response_plan_contract.py` uses only local schemas;
`tools/sync_response_plan_contract.py --check` verifies Python/schema parity.
Cross-reference, source ownership and actual replay semantics require the
owning native service as well as schema checks. This is currently a contract
draft; it does not claim that the native save/replay endpoints exist yet.
See [response-plan execution design](../docs/response-plans.md).

The native operation projection also includes saved-execution extension input
catalogue/definition admission, output records, exact presentation reads and
saved-answer/table reads. Regenerate it with `tools/sync_operation_contract.py
--backend-openapi PATH`; native models and discriminator targets retain their
`Native_` namespace. It is a projection of existing Backend endpoints, not a new
gateway. `execution-extension.examples.json` holds documented transport examples:
saved output examples come from native C++ captures, while the catalogue and
definition-save request are explicit synthetic schema/authoring examples. None
establishes a live HTTP, model, notebook or Portal acceptance result.

The saved-answer schema references the projected native
`ExecutionExtensionProvenance` directly. Keep that attribution when reading or
pinning answers. The source execution, derived output execution, publication,
catalogue revision and presentation edit version are distinct identities.
Presentation edit zero is valid. Existing answers without extension attribution
retain their legacy read contract.
# Source connections

source-connections.openapi.json is the generated contract from Backend's
services/source-connections/openapi.json. Backend owns the typed
epoch-source-connections package and its FastAPI service. The Python SDK and MCP
consume those closed request/response models instead of mirroring provider
configuration or native dataset types. Regenerate the contract at its Backend
owner, then copy its exact output here.

These endpoints are served by the Python gateway at /api/v1/sources. Native
Files, dataset review, immutable data and study execution keep their existing
Backend ownership and authentication.
