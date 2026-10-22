# Historical composable MCP acceptance — 20 October 2026

This records the earlier alpha14 interface with its Discovery specialist. The current native lookup interface is described in [the public interface](public-client-interface.md); its live acceptance is tracked separately in ENG-2162.

The calling coding agent directs the work. The default MCP dispatches explicit
specialists and deterministic Backend operations; it does not run Epoch's
supervisor or require a published answer. See the [interface](public-client-interface.md).

## Live service flow

One owned tools workspace retained discovery references across two saved studies.
The test used configured FMP Microsoft annual statements with latest-restated
semantics, not an as-published historical-data claim.

| Stage | Observed result | Epoch model calls in trace |
| --- | --- | --- |
| Discover | Resolved two exact income/cash-flow references; kept unknown metadata visible. | 2 |
| Inspect | Read those references; confirmed USD observations. | 0 |
| Build | Authored two study variants using those same references. No new discovery or execution. | 4 |
| Execute | Both saved studies completed through the generated Backend client. No response plan required. | None requested |
| Read | Read the saved dashboard directly. | None requested |
| Audit | Compared both completed executions; common FY2025 amounts matched. | 1 |

Reviewed the discovery, inspection, authoring and audit trace trees: all roots
were `epoch-tools`, with zero Epoch supervisor or response-publication calls.
The existing discovery, authoring and audit specialists still use models.

Trace links: [discovery](https://smith.langchain.com/o/9d9fa1e9-9c9e-4552-9295-990ed2a189a0/projects/p/46001c43-a7ba-471f-9eb4-e698ab8c1768/r/01a158bc-6739-75e2-8123-7bfa145dafab),
[inspection](https://smith.langchain.com/o/9d9fa1e9-9c9e-4552-9295-990ed2a189a0/projects/p/46001c43-a7ba-471f-9eb4-e698ab8c1768/r/01a158be-217e-7071-a1c4-cf4c3667e830),
[authoring](https://smith.langchain.com/o/9d9fa1e9-9c9e-4552-9295-990ed2a189a0/projects/p/46001c43-a7ba-471f-9eb4-e698ab8c1768/r/01a158c0-3bb0-705b-9771-738c1a82ef45),
[audit](https://smith.langchain.com/o/9d9fa1e9-9c9e-4552-9295-990ed2a189a0/projects/p/46001c43-a7ba-471f-9eb4-e698ab8c1768/r/01a158c3-b6d8-74a8-820d-8f3e47cfed16).

These checks prove service integration and reference reuse. They do not replace
an independent financial-data audit or demonstrate every possible specialist interrupt.

## Installed transport and validation

- SDK: 374 tests passed; full package type checking passed.
- EpochAI: 69 focused graph, ownership, architecture and packaging tests passed.
- Standalone installed SDK: six transport tests passed.
- Both standalone and registered stdio commands exposed exactly nine tools.
  Guide reads, saved tool reconnection and owned execution reads passed without
  submitting new work. The saved workspace survived a Python-preview restart.
- Shared contract validators and changed-file lint checks passed.

Installed SDK artifact: `epoch_sdk-0.1.0a14-py3-none-any.whl`, built from
`84d342b436f660c1f0a11d0a7529ce35a08682d5`, SHA-256
`923af237c2cf6c449f9acc5256b6871a11501e0838742a0d30dd451b854b1f58`.
EpochAI source: `68e9645517ced6f5f3ee9f1b90ac78b6b989a0be`.
Generated native SDK: `3.3.0rc8`. Python graph runtime: LangGraph API `0.15.1`,
LangGraph `1.2.5`.

Local installation uses the tools-only Python preview on port 12059 and the
already running Backend on port 19305. No Backend/native build was started;
the other agent's Backend process and build allocation were left alone.
Codex and Claude Code retain their existing `epoch-research-mcp` registration.
Reconnect the host to refresh its tools. These changes are installed locally
for testing; they have not been pushed, merged or deployed.
