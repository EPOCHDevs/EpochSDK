# Asset identity clients

Asset metadata and artwork are served by Platform/GDS at the existing public
API URLs. They are independent of the native computation client. The shared
contract is `contracts/asset-identity-v1.schema.json`; Python and TypeScript
bindings are generated from it. Its provenance records the original native
wire contract, and its page items follow the enriched runtime asset response.

Python uses `epoch_sdk.identity.IdentityClient` and snake_case fields. TypeScript
uses `@epochdevs/epoch-sdk/identity` and camelCase fields, matching the previous
generated client conventions. Both clients accept one API origin and an optional
token/provider. Leaving the token absent supports public shared-report reads.
A supplied token is sent to that origin only.

The clients provide exact asset lookup, bounded batch lookup, asset browsing,
country/region metadata and logo descriptors. A saved listing descriptor accepts
both the original catalogue and selection clock. Neither is substituted with
the current catalogue. Errors and ambiguous/missing records remain explicit;
the client does not retry or fall back to a native search operation.

Python validates the original JSON before constructing closed models and keeps
int64 values exact. TypeScript validates the wire shape and preserves the
existing JavaScript numeric convention. Callers needing exact large numeric
table values should retain their Arrow or raw JSON representation.

Regenerate the bindings with `scripts/generate_identity_types.sh` and
`node typescript/epoch-sdk/generate-identity.mjs`. The latter supports `--check`.
The schema, packaged schema copies and generated bindings must move together.

Validation includes original native response fixtures, absent/false/true ADR
states, exact Python integer values, changed/foreign response IDs, optional
authentication, capture parameters, cancellation and bounded failure behavior.
These tests do not establish deployment or public traffic cutover.
