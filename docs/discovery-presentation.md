# Saved discovery activity and constructor directories

The TypeScript `@epochdevs/epoch-sdk/discovery-presentation` module owns the
closed presentation models needed after Backend's discovery API is removed.
It decodes historical search/screen activity and Platform/GDS's preserved
constructor-directory response. It has no network client or model-visible tool.
New searches continue to use the Platform discovery-v4 client.

`contracts/discovery-presentation-v1.schema.json` contains the reachable wire
definitions for these reads. Its provenance records the canonical native API
commit and digest from which the preserved contract was extracted. The
constructor alias refers to the original `StudyDataConstructor` definition.
Generated bindings come from this contract, independently of the retired
native SDK operations; no historical generated client is restored.

`parseDiscoveryPresentation(name, wire)` validates before converting declared
field names to camelCase. `serializeDiscoveryPresentation(name, model)` performs
the reverse conversion and validates the resulting wire object. Dictionary
keys, arbitrary provider JSON, discriminant values and nulls remain literal.
Unknown members and malformed retained references fail validation.

Regenerate with `node typescript/epoch-sdk/generate-discovery-presentation.mjs`.
Use its `--check` option to verify the packaged schema and both declarations.
Portal sends current catalogue reads to Platform and owner-checked retained
reads to Platform/GDS. A legacy snapshot that those readers cannot verify stays
explicitly unavailable; this module does not manufacture a replacement binding.
