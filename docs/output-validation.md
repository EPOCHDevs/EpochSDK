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

The saved-result adapters, Backend output persistence and SDK/MCP integration
checks are still required by ENG-2038 and the first delivery milestone. The
validator's unit tests do not establish a live service or completed workflow.
