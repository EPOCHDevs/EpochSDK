# Shared contract

`openapi.json` is the language-neutral API contract for Epoch SDK clients and MCP.
It defines the eight logical operations, requests, named outputs, acceptance and
domain errors. Its REST paths are illustrative bindings, not another deployed
gateway. All language implementations conform to this contract.

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
