# Native response tables and bounded pages

New table answers store an annotated schema and native source reference instead
of embedding the whole dataset. The 10,000-row ceiling applies to each transfer,
with 4 MiB byte limits; it is not a total-table ceiling. JSON/text remain inline.
The same Python SDK works in notebooks, scripts and applications. MCP wraps it.

The source binds the primary execution, relation, physical fields, row count and
optional native ordering. Backend validates the complete projection before
publication. A schema probe or first page cannot certify later rows. Readers
pin an answer revision and retrieve typed pages with explicit continuation;
`next_offset: null` marks the end. Historical inline-row answers remain readable.

## Verified scopes

| Scope | Result |
| --- | --- |
| Full native server/exporter/fixture/check build | Passed with eight jobs |
| Native request/response records | 71 assertions/10 cases and 77/9 passed |
| Native response paging and complete-column validation | 50,294 assertions/3 cases passed |
| Broader nonhidden native query regression | 56,293 assertions/117 cases passed |
| Shared/workflow Python SDK source suites | 163 and 201 tests passed |
| SDK strict typing | Both zero errors; Ruff clean |
| Compiled-controller/generated-client HTTP checks | 24 checks passed |
| Installed SDK/MCP native response component | 14 checks passed, including complete 25,003-row traversal |
| Agent focused/package/identity tests and publication policy | 17 + 2 tests passed; typing, Ruff and commit hooks passed |

The 25,003-row cases use repeated labels and deliberately reversed physical
input. They check deterministic boundaries, descending order, hidden sort keys,
empty end pages and invalid values beyond any preview. No time index or unique
row-label assumption is made. Component fixtures use synthetic execution
references; they do not establish a real model-built study by themselves.

## Actual local services

The supplied-data SDK research case passed with normal Cognito authentication,
configured models and the native engine: 2024 sales 10 USD, 2025 sales 15 USD,
two rows and total 25. The answer contains a table reference plus the requested
JSON and explanation. Full page values, explicit execution linkage, fresh reads,
answer revisions, the original request's pin and direct saved-study execution
all passed.

An actual MCP query reused that retained study/execution, reviewed its evidence
with the model, published a distinct answer and read all table values. Both its
new answer pin and the original SDK answer pin were preserved. This proves
MCP post-analysis publication from prepared work, rather than a new MCP build.

Production Backend checks through SDK and MCP passed for one-row pages, empty
end pages, explicit descending order and original-version reads. A direct
publication with a physically incompatible column type was rejected before
storage, even without the SDK schema probe. No answer was left by that rejected
publication. These read/publication checks used an unreachable graph URL.

Three fresh MCP authoring attempts encountered a model-provider response saying
the service was temporarily unavailable. Their incomplete publications were
rejected; those failures are retained in the private receipts. The earlier
[core verification](verification-2026-10-18.md) remains historical evidence for
the previous transport. Do not infer a successful fresh MCP build from the
post-analysis or component checks above.

## Packages and limits

Native Python `3.3.0rc3` and TypeScript `3.3.0-rc.3` were generated and tested
through the normal Backend workflow from clean source
`5dff9af4aa71f7fb7c055dfe618e0e37a62a12b3`. The served OpenAPI SHA-256 is
`3c582030e4cae3b41c81bcceb22f48c1bb7d73495702d96011e757bbcba3494b`.
The native wheel SHA-256 is
`20c0e3a1e29659a258aac49d273ca1eea3d535b9d6460b34c74aeedd506f8aa3`.

Fern initially interpreted the validation-only table `oneOf` as a boxed `value`
field. The supported generation workflow now projects those constraints out of
the generator's type-shape input while preserving the canonical served schema
and Backend validator. Staged and installed Python/TypeScript codec checks now
exercise flat inline/reference table bodies, int64 strings and JSON nulls.
No generated SDK file was hand-edited. The failed first archive and compile
corrections are retained in local evidence.

The normal wheel's global MI-parser/presentation flags remain unverified; the
feature checks above do not certify those separate gates. No registry release,
merge, deployment or new Portal renderer is claimed.

Source references require retained immutable execution data. Missing sources,
row-count changes and invalid page values fail explicitly. There is no content
hash check on every read. Offset pages may scan/sort their source; streaming
file export is not implemented.

[ENG-2065](https://linear.app/epoch-inc/issue/ENG-2065) is the separate Portal
consumer handoff. [ENG-2067](https://linear.app/epoch-inc/issue/ENG-2067) records
the next core usability step: readable, idempotent operation handles that let a
fresh SDK/MCP client reattach after disconnect. Those handles are planned and
are not implemented by this table-access change.
