# Exact native parameter bounds

Backend `cbef46bfbb` preserves numeric lexemes through OpenAPI transformations.
The prior double-only intermediate representation rounded int64 endpoints beyond
native range; direct OpenAI rejected the study tool before model generation.

The shared snapshot is regenerated from that native export. The SDK's existing
non-null parameter owner contract is retained: unset optional owners are omitted,
not supplied as null. Source optional-use component aliases are normalized only
at the two selected owner roots; nested schema constraints remain unchanged.

Validation:

- Native OpenAPI: 175 cases / 17,926 assertions passed, no failures or skips.
- Export diff: 465 numeric minimum/maximum corrections; no other semantic changes.
- SDK full offline tests: 814 passed, two explicit native-service opt-ins skipped.
- SDK request/error schemas, shared contract (68 paths, 99 examples, 28 fixtures),
  packaged snapshot agreement and changed-file lint passed.
- New SDK endpoint tests fail against the prior snapshot (four failures), then
  pass after regeneration. They cover exact published bounds, max-int64 wire
  preservation, rejection beyond int64 and omission versus explicit null.
- Projection tests retain nested nullability and exact bounds and reject an
  unknown owner shape.

This is a source and offline qualification receipt, not proof of a completed
live CPI study or a package publication. Consumer/API evidence is recorded
separately by the AgentTesting attempt.
