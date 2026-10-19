# Core research and saved-answer merge verification

This record covers the core research → execution → published-answer flow reconciled with `main`. Research and direct prepared-study execution remain separate. One query publishes one versioned answer with named table, JSON and text parts; tables reference retained native data and are read in bounded pages.

The owning changes are [EpochBackend #480](https://github.com/EPOCHDevs/EpochBackend/pull/480), EpochSDK #1–#7 and [EpochAI #752](https://github.com/EPOCHDevs/EpochAI/pull/752). The merge order is Backend, SDK #1 through #7, then AI. Exact merge results are recorded in those PRs.

## Native and package verification

- The reconciled Backend builds the server, native fixture, exporter and all three required check executables with eight build jobs.
- Request records: **71 assertions / 10 cases**. Saved responses: **77 / 9**. Broader nonhidden Arrow-query regression: **56,293 / 117**, including the 25,003-row response tests.
- The native exporter matches the committed OpenAPI byte-for-byte: `3c582030e4cae3b41c81bcceb22f48c1bb7d73495702d96011e757bbcba3494b`.
- Normal Python `3.3.0rc3` and TypeScript `3.3.0-rc.3` generation passes staged and installed public-client codec checks. Flat table bodies, exact int64 strings, JSON nulls and main's own-record-key serializer fix are verified together. Generated SDK files were not hand-edited.
- Generated-client native HTTP checks: **24 passed**. Installed SDK/MCP native response checks: **14 passed**, including complete traversal of all 25,003 ranked rows, repeated labels, empty/end pages, revisions and owner isolation. These synthetic component checks do not claim real-model research proof.
- Native fixture cold startup exceeded the old 10-second readiness window. The verification helpers now allow 60 seconds, preserving early-exit detection, assertions and cleanup. No product retry or recovery behavior was added.

## SDK and AI checks

- Shared Python SDK: **163 tests passed** with the regenerated native wheel.
- Workflow SDK: **201 tests passed** with the regenerated native wheel.
- AI package/publication/policy checks: **43 passed**.
- Full hosted AI offline gate at `4f74bb9886509bce019b92766e54b7a8d397ff7c`: **5,764 passed, 137 skipped, 42 deselected; 84.83% branch coverage**. Integration/backend-marked tests are outside this offline gate.
- Independent automated review covered Backend and the complete SDK/AI stack. It found one stale prompt instruction requiring post-tool chat text; that instruction now agrees with publication ending the turn. The final bundle hashes, Docker pins, manifests and shared package source bytes were independently verified.

## Actual service proof

The fresh MCP supplied-data run **passed** against actual Backend and model/graph services with normal Cognito authentication. It built a new study, executed it and published one answer containing a source-backed table, JSON and text. The complete values were `2024 → 10`, `2025 → 15`, with row count 2 and total sales 25. The receipt records source-owned model identities and actual token usage, followed by the native build → selected execution → publish sequence.

The test then read the saved answer with the graph unavailable, published an explanation revision without the graph, verified the original request still pinned its original answer version, and directly executed the prepared study again without agent calls. The primary answer execution remained explicit rather than following the newest run.

The actual service pair was Backend `87b7dbeabe4f46ac535343f281cf1bf7fee1ac69` and AI `4f74bb9886509bce019b92766e54b7a8d397ff7c`; the later Backend helper-only commit does not change native code. The local receipt is `evidence-merge-20261018/live-mcp-01.json`, with `real_analysis_proven: true`. Its selected native execution is `f6acf131-9d49-5687-afa0-850955debc82`.

The earlier full supplied-data SDK research and MCP publication from prepared work remain historical v0.13 evidence. Earlier fresh-MCP attempts failed at the configured model provider and were retained; the new successful actual-service rerun closes that specific gap. Component test success was never substituted for successful authoring.

## Archive provenance and limits

The exact local native review wheel is generated from clean Backend `87b7dbeabe4f46ac535343f281cf1bf7fee1ac69`, SHA-256 `85c349103af01158ea01e22f1bbdd8dc19ded16d42ad7122f6eadf514469a53e`. The later Backend helper correction affects only verification startup timing. The shared Epoch SDK wheel is built normally from `27f69a90b0f8c7b489750dd2e5c1e45b7be9e28c`; its package source files match the archive byte-for-byte. The workflow wheel matches package sources at `b21647ba879fb61edc938a4b2f362fa14351a9a6`; the later helper correction does not change that package.

The first native build was interrupted by a machine restart. The resumed controller later stopped near completion; existing compiler children were allowed to finish and the remaining build completed successfully. Failed readiness attempts and final successful checks are retained separately in the local merge evidence. Neither interruption is presented as a successful build.

Offset pages may scan/sort immutable retained sources. Streaming exports, custom response cards and the Portal renderer are separate work. Full native MI-parser/presentation package gates and hidden live-S3 tests are not claimed. Registry SDK publication and environment deployment are separate from these source merges.

[ENG-2067](https://linear.app/epoch-inc/issue/ENG-2067/sdkmcp-reconnect-to-research-and-execution-with-idempotent-readable) readable idempotent reconnect handles remain planned and are not implemented by this merge. [ENG-2065](https://linear.app/epoch-inc/issue/ENG-2065/epochportal-render-published-query-answers-in-the-new-conversation) owns Portal integration against the saved-answer contract.
