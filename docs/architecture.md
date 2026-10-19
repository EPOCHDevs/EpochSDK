# SDK and service boundaries

Epoch SDK is a client library over LangGraph SDK and generated StratifyX SDK.
Each language has its own client implementation and the same shared API contract.
MCP exposes the same client capabilities rather than recreating orchestration.

The service repositories own graph implementations and Backend REST controllers,
persistence, study/execution records and native SDK generation. Ordinary Backend
admission, status, results and refresh use the owning native API directly.
Building or revising a study uses a dedicated integration graph with retained
technical checkpoints; the SDK does not import a conversation application.

The normal flow validates the request, records Backend acceptance, builds or
resolves one authorized study, freezes its binding/parameters, executes through
Backend and returns validated named results. A public attempt handle and a
native engine execution id are distinct; resolve the public handle through its
Backend record before using the mapped native execution for data/control calls.

Clarification is terminal and carries gaps, questions/options and recommended
adjusted task wording. There is no interactive answer/resume operation. The core
API, validation and real Backend records/controllers remain required before an
SDK/MCP prototype can be declared complete. Additional recovery/retry and
retention engineering follows the usable core feature.

The first Python package supplies executable contracts and an access checker.
The complete graph/SDK/MCP flow and saved-output adapters are still being built;
schema/unit checks do not claim real service integration has passed.
