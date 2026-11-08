# Public v1 API (draft for review)

Status: accepted for implementation on 8 November 2026 ([ENG-2504](https://linear.app/epoch-inc/issue/ENG-2504)).
Nothing is served yet: ENG-2512 mounts the routes, and each operation names the issue that
implements it. Change the contract by changing EpochAI's routes and models.

The v1 API is one public surface per environment for curl, any language, CI jobs and other
agents. It runs the Epoch SDK core on the server, so callers get the SDK's research flow,
reconnect rules, validation and paging without the LangGraph protocol, two service URLs or a
Cognito token.

## Where the contract comes from

The contract is generated from code, in the server's language, as Backend's is from its C++
routes and Glaze types:

1. EpochAI's `agent_src/public_api` declares the v1 routes with FastAPI and their models with
   Pydantic. Payloads reuse the SDK's models (`RunRequest`, `RunParameters`, `SavedStudy`,
   `SavedResearchResponse`, `ResponseTablePage`, question and dataset-review models) and the
   generated native `stratifyx` models for files, datasets and Space.
2. `python tools/export_public_api.py` in EpochAI writes `docs/public-api/openapi.json`.
   EpochAI's tests fail when that file is stale or an example is not a valid model value.
3. `python tools/sync_public_contract.py --epochai-openapi PATH` copies it here as
   [`contracts/public-v1.openapi.json`](../contracts/public-v1.openapi.json). Do not edit the copy.
4. `python tools/validate_public_contract.py` checks the copy independently of Python: OpenAPI
   validity, every example against the JSON Schemas, no internal routes, scopes and reuse records,
   and the endpoint map below.

Each operation's `x-epoch-scopes` lists the scopes it needs, and `x-epoch-reuses` names the SDK
method and native routes it reuses, or the work it still needs.

## Scope: start small

21 operations. 15 are what a caller does; 6 are credentials and health.

- Research: start, read, stream, answer.
- Saved studies: run, read.
- Answers: read, read table pages.
- Your data: upload a file, prepare a dataset draft, save or reject it, place it in Space.
- Webhooks: create, list, delete.
- Credentials: create, list and revoke API keys; exchange a sign-in for a token; signing keys;
  health.

Everything else waits until a caller needs it, and is added within `/v1` because changes there are
additive. That includes cancel, execution events, whole-table and provenance downloads, study lists,
file and dataset management, document reads and search, Space folders, and webhook tests and
delivery logs.

## A first call

```bash
curl -X POST "$EPOCH_API_URL/v1/research" \
  -H "Authorization: Bearer $EPOCH_API_KEY" \
  -H "Idempotency-Key: msft-gross-margin-2026-11" \
  -H "Content-Type: application/json" \
  -d '{"request": {"task": "Compare Microsoft and Apple quarterly gross margin over two years.",
       "outputs": [{"name": "summary", "type": "text", "instructions": "Three sentences."}]}}'

curl -N "$EPOCH_API_URL/v1/research/$RESEARCH_ID/events" -H "Authorization: Bearer $EPOCH_API_KEY"
```

The stream ends with `questions` (answer with `POST /v1/research/{id}/answers`, then reconnect),
`completed` (read `result.response` with `GET /v1/responses/{id}?version=`) or `failed`.

## Decisions

| # | Decision | Proposal |
| -- | -- | -- |
| D1 | Host | `/v1` runs as custom routes in the existing EpochAI server. `agent_src/webapp.py` already serves `/api/v1/document-*` and `/api/v1/agent-tools` with custom-route auth, and ENG-2353 records the direction not to deploy another Python server. One host per environment forwards only `/v1/*` and `/.well-known/*` (ENG-2521). The routes are not mounted until ENG-2512. |
| D2 | Identities | Research is addressed by Backend's request id. `Idempotency-Key` is the SDK `operation_id` (same pattern, at most 128 characters): the same input attaches, different input returns 409. Without a key the server generates one. Other ids are the native ones. |
| D3 | Research events | The SDK's five session events (`status`, `ui`, `ui_removed`, `questions`, `completed`) plus `progress` (ENG-2513) and `failed`. Public events carry `research_id` instead of the SDK's internal `WorkflowHandle`; `questions`, `completed` and `failed` carry the whole research object. Event ids are LangGraph's, so `Last-Event-ID` resumes; disconnecting never cancels; a comment every 15 seconds keeps connections open. `ui` events are display hints that may change. ENG-2520's SDK reader maps these back to `SessionEvent`. |
| D4 | Questions and answers | Questions reuse the SDK's AskUser `Question` model without the internal `tool_call_id`, and the SDK's dataset-review interrupts unchanged. Answers are the SDK's `InterruptResponse` values, keyed by question id. |
| D5 | Running saved studies | `POST /v1/executions` takes the completed research's id or the exact `reusable_study` (`SavedStudy`), as `execute_saved` does. A bare study id does not identify the source execution or report template, so v1 refuses it. |
| D6 | Executions | Addressed by execution id. A prepared report's saved answer appears under `answer`, separate from the run's own `status`; Backend's `/outputs` read is folded into the execution object. |
| D7 | Status values | `queued`, `running`, `needs_input` (research only), `completed`, `failed`, `cancelled`. Research maps Backend's request phase (accepted → queued, active → running, needs_input, outputs_recorded → completed, failed). Executions map Backend's job status (pending or queued → queued, running, completed, failed, cancelled). |
| D8 | Paging | Lists use `cursor`, `limit` and `next_cursor`. Answer tables keep the SDK's `offset`, `page_size` (at most 10,000 rows and 4 MiB) and `next_offset`. |
| D9 | Errors | RFC 9457 problem+json with the SDK's `ErrorCode` and `retryable`. Request-validation failures are 400, not FastAPI's 422 (ENG-2512 installs the handler). A missing scope is 403. |
| D10 | Authentication | `Authorization: Bearer` with an API key or an Epoch access token; raw Cognito tokens are refused. Scopes: `read`, `research`, `execute`, `files:write`, `space:write`, `webhooks:write`. API keys are managed only with a browser sign-in. `POST /v1/auth/token` exchanges an unexpired Cognito ID token (RFC 8693). There are no Epoch refresh tokens: a signed-in SDK refreshes its Cognito session and exchanges again, and signing out revokes that session. Signing keys are at `/.well-known/jwks.json`. |
| D11 | Webhooks | Events: `research.needs_input`, `research.completed`, `research.failed`, `execution.completed`, `execution.failed`, `execution.cancelled`, `dataset.ready`, `dataset.needs_review`. `Epoch-Signature: t=<unix>,v1=<hex>` is HMAC-SHA256 over `<t>.<raw body>`; reject timestamps older than 5 minutes. Delivery is at least once with a stable event id; endpoints answer 2xx within 10 seconds; repeated failures disable the endpoint. HTTPS only. |
| D12 | Uploads | One request with the file's bytes, name, media type and SHA-256. The server splits it into Backend's upload parts; the same content returns the same file. |
| D13 | Nulls | FastAPI drops nulls from the generated document, so nullable fields are optional rather than required. Responses still send `null`. |
| D14 | Versioning | Changes within `/v1` are additive. A removal is announced with `Deprecation` and `Sunset` headers at least 90 days ahead. |

## Gaps needing new work

| Operations | Gap | Owner |
| -- | -- | -- |
| Webhooks | New storage, durable event outbox and delivery. | ENG-2519 |
| API keys | New key store. | ENG-2508 |
| Token exchange and JWKS | Backend's token issuer (`docs/contracts/epoch-tokens.md`). | ENG-2505 |
| Health | Served by the v1 host. | ENG-2512 |

## Endpoint map

Generated from each operation's `x-epoch-reuses` with
`python tools/validate_public_contract.py --map`; the validator fails when this table is stale.

<!-- endpoint-map:start -->
| Operation | SDK method reused | Native routes | Gaps |
| -- | -- | -- | -- |
| `POST /v1/research`<br>Start research | `EpochClient.research(request, operation_id=..., thread_id=..., wait=False)` | Backend POST /api/v1/integration/requests (createSdkRequest)<br>Backend PATCH /api/v1/integration/requests/{requestId} (updateSdkRequest)<br>EpochAI LangGraph threads.create and runs.create on assistant epoch-ai with stream_resumable=True | – |
| `GET /v1/research/{research_id}`<br>Read research | `EpochClient.research_status(request_id)` | Backend GET /api/v1/integration/requests/{requestId} (getSdkRequest)<br>EpochAI LangGraph threads.get_state for pending interrupts | – |
| `GET /v1/research/{research_id}/events`<br>Stream research events | `ResearchSession.events()` | EpochAI LangGraph runs.join_stream(thread_id, run_id, stream_mode=['values', 'custom'], last_event_id=..., cancel_on_disconnect=False) | – |
| `POST /v1/research/{research_id}/answers`<br>Answer research questions | `EpochClient.resume_research(waiting, responses, wait=False)` | Backend GET /api/v1/integration/requests/{requestId} (getSdkRequest)<br>EpochAI LangGraph runs.create with Command(resume=...) on the same thread | – |
| `POST /v1/executions`<br>Run a saved study | `EpochClient.execute_saved(SavedStudy from the research or the reference, period=..., execution=..., operation_id=...)` | Backend POST /api/v1/integration/execution-requests (createSdkExecutionRequest) | – |
| `GET /v1/executions/{execution_id}`<br>Read an execution | `EpochClient.execution(execution_id)` | Backend GET /api/v1/studies/executions/{executionId}<br>Backend GET /api/v1/studies/executions/{executionId}/outputs (getExecutionOutputs) | – |
| `GET /v1/responses/{response_id}`<br>Read a saved answer | `EpochClient.response(response_id, version=...)` | Backend GET /api/v1/research/responses/{responseId} (getResearchResponse) | – |
| `GET /v1/responses/{response_id}/tables/{table_name}`<br>Read a page of an answer table | `EpochClient.response_table(response_id, name, version=..., offset=..., page_size=...)` | Backend GET /api/v1/research/responses/{responseId}<br>Backend POST /api/v1/studies/executions/{executionId}/response-tables (readResearchResponseTable) | – |
| `POST /v1/files`<br>Upload a file | `EpochClient.upload_file(content, name=..., media_type=...)` | Backend POST /api/v1/files/uploads (init_file_upload)<br>Backend PUT /api/v1/files/{fileRef}/content (upload_file_part)<br>Backend POST /api/v1/files/{fileRef}/complete (complete_file_upload) | – |
| `POST /v1/datasets`<br>Prepare a dataset draft from a file | `EpochClient.prepare_dataset(request)` | Backend POST /api/v1/files/imports (prepare_structured_import) | – |
| `POST /v1/datasets/reviews`<br>Save or reject dataset drafts | `EpochClient.review_datasets(request)` | Backend POST /api/v1/files/imports/review (review_structured_import) | – |
| `PUT /v1/space/items`<br>Place or move an item in Space | `EpochClient.place_resource(...)` | Backend PUT /api/v1/space/resources (place_space_resource) | – |
| `POST /v1/webhooks`<br>Create a webhook endpoint | – | – | New Backend storage, outbox and delivery (ENG-2519). |
| `GET /v1/webhooks`<br>List webhook endpoints | – | – | New Backend storage, outbox and delivery (ENG-2519). |
| `DELETE /v1/webhooks/{webhook_id}`<br>Delete a webhook endpoint | – | – | New Backend storage, outbox and delivery (ENG-2519). |
| `POST /v1/api-keys`<br>Create an API key | – | – | New Backend key store (ENG-2508). |
| `GET /v1/api-keys`<br>List API keys | – | – | New Backend key store (ENG-2508). |
| `POST /v1/api-keys/{key_id}/revoke`<br>Revoke an API key | – | – | New Backend key store (ENG-2508). |
| `POST /v1/auth/token`<br>Exchange a sign-in for Epoch tokens | – | Backend POST /api/v1/auth/token (exchange_epoch_token) | – |
| `GET /.well-known/jwks.json`<br>Read token signing keys | – | Backend GET /api/v1/auth/jwks (get_epoch_jwks) | – |
| `GET /v1/health`<br>Check the API | – | – | Served by the v1 host (ENG-2512). |
<!-- endpoint-map:end -->
