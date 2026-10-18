# Materialized output validation

The graph and SDK use `epoch_sdk.output_validation.validate_outputs` to check
the actual named results against the accepted output declarations. It rejects
missing, duplicate or extra outputs; changed ordered columns or annotations;
wrong row widths; incompatible cell values/nulls; invalid JSON Schema values;
and a different requested text format. Failures retain the accepted execution
reference and use `OUTPUT_VALIDATION_FAILED`.

`int64` cells use base-10 JSON strings so every supported language preserves
their value. Numeric observations must be finite, booleans are distinct from
numbers, dates are ISO calendar dates, and timestamps include a timezone.
Column and JSON Schema property descriptions remain part of the declaration.

Materialized values have a closed tagged shape. Arbitrary keys are confined to
the caller-owned JSON value. Readers must supply the complete bounded result
or report a limit/error; validating five preview rows does not certify the rest
of a table. This function validates types and structure, not analytical truth.

New table answers may instead contain a typed native source reference. The
Python validator checks that reference and its declared column mapping; Backend
validates types/nullability across the complete native projection before saving
it. Each later page is also checked as it is decoded. See
[table access](response-tables.md). A schema probe or UI preview alone is never
the whole-table validation gate.

`saved_outputs.read_saved_outputs` connects the validator to explicit native
saved-artifact bindings. It reads through StratifyX and exposes the same behavior
through `SupervisorClient.outputs` and MCP `epoch_outputs`. See
[the saved-output reader](saved-output-reader.md) for supported representations,
limits and the remaining accepted-request/publication integration.

Backend publication/persistence of the accepted declarations and artifact
bindings, automatic handoff from the supervisor, and real SDK/MCP checks are
still required by ENG-2033/2035/2038 and the first milestone. Component tests do
not establish a live service or completed natural-language workflow.
