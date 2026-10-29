import { EpochError, canonical, invariant, normalizedDeclarations, operationId, parseRequest,
  requestToWire, responseToWire, statusCode, throwNativeError } from "./contract.js"

const opts = signal => ({ maxRetries: 0, abortSignal: signal })
const object = value => value !== null && typeof value === "object" && !Array.isArray(value)

// Same UUIDv5 identity as Python's uuid5(NAMESPACE_URL, "epoch:research:" + request_id).
export async function researchThreadId(requestId) {
  const ns = "6ba7b8119dad11d180b400c04fd430c8".match(/../g).map(x => parseInt(x, 16))
  const bytes = new Uint8Array([...ns, ...new TextEncoder().encode(`epoch:research:${requestId}`)])
  const hash = new Uint8Array(await crypto.subtle.digest("SHA-1", bytes)).slice(0, 16)
  hash[6] = (hash[6] & 15) | 80
  hash[8] = (hash[8] & 63) | 128
  const hex = [...hash].map(b => b.toString(16).padStart(2, "0")).join("")
  return `${hex.slice(0, 8)}-${hex.slice(8, 12)}-${hex.slice(12, 16)}-${hex.slice(16, 20)}-${hex.slice(20)}`
}

function handle(record) {
  invariant(record.runtime, "The research operation has no accepted runtime.")
  return {
    requestId: record.requestId, operationId: record.operationId, threadId: record.runtime.threadId,
    assistantId: record.runtime.assistantId, runId: record.graphRunId,
  }
}
const active = record => ({ status: "in_progress", kind: "run", requestId: record.requestId,
  operationId: record.operationId, handle: record.runtime ? handle(record) : undefined })

export function parseInterrupts(value) {
  invariant(Array.isArray(value), "The server returned an invalid interrupt list.")
  return value.map(item => {
    invariant(object(item) && typeof item.id === "string" && item.id && object(item.value), "Invalid interrupt identity.")
    const ask = item.value
    invariant(ask.type === "ask_user" && Array.isArray(ask.questions) && typeof ask.tool_call_id === "string",
      "This interrupt must be answered in the existing Epoch conversation.", "UNSUPPORTED_INTERRUPT")
    for (const q of ask.questions) {
      invariant(object(q) && typeof q.question === "string" && typeof q.description === "string" &&
        typeof q.multi_select === "boolean" && Array.isArray(q.options) &&
        q.options.every(o => object(o) && typeof o.label === "string" && typeof o.recommended === "boolean"),
      "Invalid clarification question.")
    }
    return { id: item.id, value: ask }
  })
}

export function resumeCommand(waiting, responses) {
  const ids = waiting.interrupts.map(x => x.id)
  invariant(object(responses) && canonical(Object.keys(responses).sort()) === canonical(ids.sort()),
    "Answer exactly the current interrupt IDs.", "VALIDATION_ERROR")
  for (const item of waiting.interrupts) {
    invariant(object(responses[item.id]) && Object.keys(responses[item.id]).length === 1 && "answers" in responses[item.id],
      "Unknown clarification response field.", "VALIDATION_ERROR")
    const answers = responses[item.id]?.answers
    const questions = item.value.questions
    invariant(Array.isArray(answers) && answers.length === questions.length,
      "Provide an answer row for every question.", "VALIDATION_ERROR")
    const seen = new Set()
    for (const answer of answers) {
      const index = answer.question_index
      invariant(Number.isInteger(index) && index >= 0 && index < questions.length && !seen.has(index),
        "Question index is duplicated or out of range.", "VALIDATION_ERROR")
      seen.add(index)
      const selected = answer.selected_indices ?? []
      const free = answer.free_form_input
      invariant(Array.isArray(selected) && new Set(selected).size === selected.length &&
        selected.every(i => Number.isInteger(i) && i >= 0 && i < questions[index].options.length),
      "An answer contains an invalid option index.", "VALIDATION_ERROR")
      invariant(free === undefined || (typeof free === "string" && free.trim() && free === free.trim()),
        "Free-form answers must be nonblank and trimmed.", "VALIDATION_ERROR")
      invariant(questions[index].multi_select || (selected.length <= 1 && !(selected.length && free)),
        "Choose one option or a free-form answer for this question.", "VALIDATION_ERROR")
      invariant(Object.keys(answer).every(key => ["question_index", "selected_indices", "free_form_input"].includes(key)),
        "Unknown answer field.", "VALIDATION_ERROR")
    }
  }
  return { resume: responses }
}

function runPayload(record) {
  return { metadata: { epoch_sdk_request_id: record.requestId, epoch_sdk_ui_stream: "v1" },
    durability: "sync", multitaskStrategy: "reject", onCompletion: "keep",
    streamMode: ["values", "custom"], streamSubgraphs: true, streamResumable: true }
}

async function current(client, id, signal) {
  const r = await client.backend.sdkRequests.getSdkRequest(id, {}, opts(signal))
  invariant(r.requestId === id, "Backend returned another research request.")
  return r
}

export async function startResearch(client, request, options) {
  const op = operationId(options.operationId)
  const native = parseRequest(request)
  let record
  try {
    record = await client.backend.sdkRequests.createSdkRequest({ request: native, operationId: op,
      launch: { assistantId: client.assistantId, ...(options.threadId ? { threadId: options.threadId } : {}) } }, opts(options.signal))
  } catch (error) {
    if (statusCode(error) === 409) throw new EpochError("IDEMPOTENCY_CONFLICT",
      "This operation ID has different accepted inputs. Use a new ID for a changed request.")
    throw error
  }
  invariant(record.operationId === op, "Backend returned another operation.")
  record = await current(client, record.requestId, options.signal)
  if (record.error || record.responseVersion !== undefined || record.nativeExecutionRequestId)
    return researchStatus(client, op, options)
  if (!record.runtime) {
    const threadId = options.threadId ?? await researchThreadId(record.requestId)
    if (!options.threadId) await client.graph.threads.create({ threadId, ifExists: "do_nothing", signal: options.signal })
    const snapshot = options.threadId ? await client.graph.threads.getState(threadId, undefined, { signal: options.signal }) : { values: {}, interrupts: [] }
    invariant(!snapshot.interrupts?.length && !snapshot.values?.__interrupt__?.length,
      "This conversation is waiting for input. Continue its existing operation.")
    const values = snapshot.values ?? {}
    try {
      record = await client.backend.sdkRequests.updateSdkRequest(record.requestId, {
        expectedVersion: record.version,
        runtime: { threadId, assistantId: client.assistantId, executionIdsBefore: values.execution_ids ?? [],
          outcomeIdsBefore: Object.keys(values.next_action_outcomes ?? {}) },
      }, opts(options.signal))
    } catch (error) {
      if (statusCode(error) !== 409) throw error
      record = await current(client, record.requestId, options.signal)
    }
  }
  throwNativeError(record)
  if (record.responseVersion !== undefined || record.nativeExecutionRequestId)
    return researchStatus(client, op, options)
  invariant(record.runtime, "The research runtime could not be attached.")
  if (!record.graphRunId) {
    try {
      await client.graph.runs.create(record.runtime.threadId, record.runtime.assistantId, {
        ...runPayload(record), signal: options.signal, input: {
          messages: [{ role: "user", id: record.requestId, content: request.task }], sdk_request_id: record.requestId,
        },
      })
    } catch (error) {
      if (statusCode(error) !== 409) throw error
    }
    record = await current(client, record.requestId, options.signal)
    invariant(record.graphRunId || record.error || record.responseVersion !== undefined || record.nativeExecutionRequestId,
      "The conversation is busy and this operation has not started. Reconnect using the same operation ID.")
  }
  return researchStatus(client, op, options)
}

async function completed(client, record, signal) {
  invariant(record.responseId && record.responseVersion !== undefined && record.runtime,
    "The research request has no pinned saved answer.")
  const response = await client.read(record.responseId, { version: record.responseVersion, signal })
  invariant(response.requestId === (record.nativeExecutionRequestId ?? record.requestId) &&
    response.threadId === record.runtime.threadId && response.primaryExecutionId === record.currentExecutionId &&
    canonical(normalizedDeclarations(responseToWire(response).content.declarations)) ===
      canonical(normalizedDeclarations(requestToWire(record.request).outputs)),
  "Saved answer identity, source or declarations differ from this research request.", "OUTPUT_VALIDATION_FAILED")
  let reusableStudy
  if (record.nativeExecutionRequestId) {
    const native = await client.backend.sdkRequests.getSdkExecutionRequest(record.nativeExecutionRequestId, {}, opts(signal))
    invariant(native.requestId === record.nativeExecutionRequestId && !native.error &&
      (!native.request.researchRequestId || native.request.researchRequestId === record.requestId) &&
      native.request.threadId === record.runtime.threadId && native.executionId === record.currentExecutionId &&
      native.responsePhase === "outputs_recorded" && native.responseId === response.responseId &&
      native.responseVersion === response.version && native.extensionOutputs?.responseId === response.responseId &&
      native.extensionOutputs?.responseVersion === response.version &&
      canonical(native.extensionOutputs?.provenance) === canonical(response.extension),
    "The answer differs from the linked native publication.", "OUTPUT_VALIDATION_FAILED")
    if (!native.request.inputTables && !record.sourceExecutionId && !native.request.sourceExecutionId) {
      reusableStudy = { studyId: native.request.studyId, sourceExecutionId: native.executionId, threadId: record.runtime.threadId }
    } else if (record.sourceExecutionId) {
      invariant(native.request.sourceExecutionId === record.sourceExecutionId, "Saved report source differs from the research source.")
      try {
        const source = await client.ordinarySource({ sourceExecutionId: record.sourceExecutionId }, signal, true)
        reusableStudy = { studyId: source.job.definitionId, sourceExecutionId: source.job.id,
          threadId: record.runtime.threadId, reportTemplate: { requestId: native.requestId } }
      } catch (error) {
        // The answer remains readable if its older original no longer offers prepared replay.
        if (statusCode(error) !== 404 && error.code !== "NOT_REUSABLE") throw error
      }
    }
  } else if (response.studyId && response.primaryExecutionId) {
    reusableStudy = { studyId: response.studyId, sourceExecutionId: response.primaryExecutionId,
      threadId: record.runtime.threadId, ...(response.responsePlan ? { responsePlan: response.responsePlan } : {}) }
  }
  return { status: "succeeded", kind: "run", requestId: record.requestId, operationId: record.operationId,
    response, ...(reusableStudy ? { reusableStudy } : {}) }
}

export async function researchStatus(client, op, { signal } = {}) {
  operationId(op)
  let record = await client.backend.sdkRequests.getSdkRequestByHandle(op, {}, opts(signal))
  invariant(record.operationId === op, "The handle returned another operation.")
  throwNativeError(record)
  if (record.responseVersion !== undefined) return completed(client, record, signal)
  if (record.nativeExecutionRequestId) return active(record)
  if (!record.runtime || !record.graphRunId)
    return { status: "accepted", kind: "run", operationId: op, requestId: record.requestId }
  const h = handle(record)
  let run
  try { run = await client.graph.runs.get(h.threadId, h.runId, { signal }) }
  catch (error) { if (statusCode(error) === 404) return active(record); throw error }
  invariant(run.metadata?.epoch_sdk_request_id === record.requestId, "The recorded run belongs to another request.")
  if (["pending", "running"].includes(run.status)) return active(record)
  if (["error", "timeout"].includes(run.status)) throw new EpochError("EXECUTION_FAILED", "The research run failed.")
  const history = await client.graph.threads.getHistory(h.threadId, { limit: 1,
    metadata: { epoch_sdk_request_id: record.requestId, epoch_sdk_run_id: record.graphRunId }, signal })
  invariant(history.length, "The run ended without a saved result checkpoint.")
  const snapshot = history[0]
  const state = snapshot.values ?? {}
  invariant(!state.authority_turn_id || state.authority_turn_id === `user-turn:${record.requestId}`,
    "The checkpoint belongs to another research request.")
  const interrupts = snapshot.interrupts?.length ? snapshot.interrupts : state.__interrupt__ ?? []
  if (interrupts.length) return { status: "needs_input", kind: "run", operationId: op,
    requestId: record.requestId, handle: h, interrupts: parseInterrupts(interrupts) }
  // Completion may have been recorded while the graph was being observed.
  record = await current(client, record.requestId, signal)
  throwNativeError(record)
  if (record.responseVersion !== undefined) return completed(client, record, signal)
  if (record.nativeExecutionRequestId || record.graphRunId !== h.runId) return active(record)
  if (state.publication_error) throw new EpochError(state.publication_error.code ?? "OUTPUT_VALIDATION_FAILED",
    state.publication_error.message ?? "The required outputs could not be saved.")
  const reference = state.published_response
  invariant(object(reference) && reference.request_id === record.requestId && reference.thread_id === h.threadId,
    "The run ended without a saved answer for this request.", "OUTPUT_VALIDATION_FAILED")
  const response = await client.read(reference.response_id, { version: reference.version, signal })
  const wire = responseToWire(response)
  for (const key of ["response_id", "request_id", "thread_id", "version", "primary_execution_id", "study_id", "response_plan", "extension"])
    invariant(canonical(reference[key] ?? undefined) === canonical(wire[key] ?? undefined),
      "Published answer reference differs from storage.", "OUTPUT_VALIDATION_FAILED")
  try {
    record = await client.backend.sdkRequests.updateSdkRequest(record.requestId, { expectedVersion: record.version,
      responseId: response.responseId, responseVersion: response.version,
      ...(response.primaryExecutionId ? { currentExecutionId: response.primaryExecutionId } : {}) }, opts(signal))
  } catch (error) { if (statusCode(error) !== 409) throw error; record = await current(client, record.requestId, signal) }
  if (record.responseVersion !== undefined) return completed(client, record, signal)
  return active(record)
}

export async function resumeResearch(client, waiting, responses, options = {}) {
  invariant(waiting.status === "needs_input", "This operation is not waiting for an answer.")
  const latest = await researchStatus(client, waiting.operationId, options)
  if (latest.status !== "needs_input") return latest
  invariant(canonical(latest.handle) === canonical(waiting.handle) && canonical(latest.interrupts) === canonical(waiting.interrupts),
    "The pending question changed. Review the current questions before replying.", "STALE_QUESTION")
  const command = resumeCommand(latest, responses)
  const record = await current(client, latest.requestId, options.signal)
  try { await client.graph.runs.create(latest.handle.threadId, latest.handle.assistantId, { ...runPayload(record), signal: options.signal, command }) }
  catch (error) { if (statusCode(error) !== 409) throw error }
  return researchStatus(client, latest.operationId, options)
}
