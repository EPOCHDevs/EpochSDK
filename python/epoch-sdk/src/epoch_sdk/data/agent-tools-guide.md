# Epoch tools: the calling agent is the supervisor

Use the user's task and approved context to choose steps. There is no required
pipeline, Epoch supervisor call or response-publication step. Answer the user
directly from the evidence you read.

1. Use `epoch_find` and `epoch_read` to inspect existing studies, executions or
   tools workspaces before doing work again.
2. Read `epoch_dataset_catalog` for the Backend-owned dataset directory and source options. Select source_ids with include_details for full schemas, vintage/revision selectors and qualifications. This is metadata, not an entitlement or populated-data certificate.
3. Use `epoch_search_dataset` for native instruments/series, or `epoch_screen_assets` for a complete cohort. These call Backend without a Discovery agent or generative LLM. Keep exact result_ref/record_ref or universe_ref, and choose dataset/options in build_study source_refs. Large searches include one stored page; continue with epoch_read(kind="dataset_search") and its cursor. Do not rerun a provider search to page metadata. A saved build returns retained source_refs for later studies; preserve their time basis and registry compatibility.
4. Use `epoch_inspect_source` only when actual observations are needed. Supply
   the exact returned inspection addresses/handles and an explicit window.
5. `epoch_build_study` uses the existing study author. Fill its source-owned
   command schema, cite selected refs and choose distinct slots for distinct
   studies. Specialists do not see the calling agent's whole conversation:
   include the relevant task, approved definitions and parameters. Never invent
   internal decision receipts; convey external user choices in the current task.
6. `epoch_execute` calls Backend directly using a saved study ID and period.
   This is native execution, not saved-answer-plan replay. A changed period does
   not rewrite fixed dates or fiscal labels in a script; inspect the saved
   study before using another window.
7. Read dashboard metadata/values directly with `epoch_read` when they answer
   the question. For necessary non-inline analysis, call `epoch_audit_run` with
   exact completed `execution_ids` and targeted natural-language questions.
   Multiple IDs allow an explicit comparison; never silently join unrelated grids.

For a new report over a completed execution, `epoch_extension_inputs` reads the
selected native table/field catalogue. Write the EpochScript yourself and use
`epoch_save_extension`, then `epoch_execute_extension` with the returned study
ID, original source execution ID, selected input tables and a reusable operation
ID. This path uses no supervisor or authoring model and never reruns the source
study. Tables/JSON and native dashboard reporters are independent destinations.
An optional `llm_call` generates bounded cached text that explicit
`response_text`, Markdown or `executive_summary` consumers can share.
Read `epoch_status(kind="extension", operation_id=...)` until declared outputs
are confirmed, then use `epoch_read` for exact answer revisions or presentation
pins. Numerical completion alone does not establish text/publication completion.

Specialist calls return a background-operation handle. Poll `epoch_status`
with `kind="tool"` and that handle. Engine jobs use `kind="execution"` and the
native execution ID. Reconnecting and status reads do not resubmit work. Keep
accepted handles/IDs and inspect saved work after an uncertain submission.

Completion of a tool is not certification of its analysis. Preserve partial,
unknown, infeasible and failed outcomes. Ask the human through your host's
normal conversation when requirements must change. Use `epoch_resume` only
when an actual pending native interrupt was returned; never choose a
recommendation automatically.

Explicit authoring and auditing use their specialist LLMs; only a declared
`llm_call` invokes the extension's bounded text model. A deterministic extension
without that declaration uses no model. Native search may use Backend’s
non-generative relevance ranker. Source inspection, ordinary `epoch_execute`,
catalogue/status/find/read operations make no LLM call. Model/vendor credentials
remain on their services.
