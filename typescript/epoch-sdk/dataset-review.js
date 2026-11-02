import Ajv from "ajv/dist/2020.js"
import addFormats from "ajv-formats"
import { serialization } from "@epoch/stratifyx"
import bundle from "./dataset-review.schema.json" with { type: "json" }
import { canonical, EpochError, invariant } from "./contract.js"

const ajv = new Ajv({ strict: false, strictNumbers: true, allErrors: true })
addFormats(ajv)
const interruptSchema = ajv.compile(bundle.interrupt)
const responseSchema = ajv.compile(bundle.response)
const opts = signal => ({ maxRetries: 0, abortSignal: signal })
const terminal = value => ["saved", "discarded", "expired", "stopped"].includes(value)

export function datasetInterrupt(value) {
  invariant(interruptSchema(value), "The dataset review does not match its source-owned contract.", "INVALID_STATE")
  return value
}

export function interruptionIdentity(item) {
  const value = item.value
  if (value.type !== "dataset_review") return canonical(item)
  if (value.stage === "configure") return canonical([item.id, value.type, value.stage, value.tool_call_id, value.proposal_ref, value.preparation_ref])
  const op = value.operation
  return canonical([item.id, value.type, value.stage, value.tool_call_id, op.preparation_ref, op.attempt,
    op.result_sha256, op.review?.review_ref, op.review?.schema_sha256])
}

export function validateDatasetResponse(payload, response) {
  invariant(responseSchema(response), "Provide an explicit closed dataset workflow response.", "VALIDATION_ERROR")
  invariant(payload.stage === response.stage, "The dataset workflow stage changed.", "STALE_REVIEW")
  if (payload.stage === "configure") {
    invariant(response.proposal_ref === payload.proposal_ref, "The dataset proposal changed.", "STALE_REVIEW")
    invariant((response.action === "build_preview") === Boolean(response.request), "Build preview requires the reviewed request; Cancel carries none.", "VALIDATION_ERROR")
    return
  }
  const op = payload.operation
  invariant(op.review && response.preparation_ref === op.preparation_ref && response.attempt === op.attempt &&
    response.review_ref === op.review.review_ref && response.result_sha256 === op.result_sha256 &&
    response.schema_sha256 === op.review.schema_sha256, "The exact dataset review changed.", "STALE_REVIEW")
  invariant((response.action === "edit") === Boolean(response.request), "Only Build preview after Edit carries a request.", "VALIDATION_ERROR")
  if (response.action === "continue") invariant(terminal(op.state), "The dataset outcome is not confirmed.", "INVALID_STATE")
  else if (response.action === "edit") invariant(payload.can_edit === true, "This result cannot be edited.", "INVALID_STATE")
  else invariant(op.review.allowed_actions.includes(response.action === "decline" ? "discard" : response.action) ||
    op.state === "save_failed" && op.review.allowed_actions.includes("retry_save") && ["save", "save_available"].includes(response.action) ||
    op.state === "saved" && ["save", "save_available"].includes(response.action) || op.state === "discarded" && response.action === "decline",
  "This review action is unavailable.", "INVALID_STATE")
}

export async function refreshDatasetInterrupts(client, items, signal) {
  const result = []
  for (const item of items) {
    if (item.value.type !== "dataset_review" || item.value.stage !== "review") { result.push(item); continue }
    let op = await client.backend.userFiles.getDatasetPreparation(item.value.operation.preparation_ref, {}, opts(signal))
    const seen = new Set()
    while (op.replacedBy) {
      invariant(!seen.has(op.preparationRef) && seen.size < 32, "Invalid review replacement chain.")
      seen.add(op.preparationRef)
      const child = await client.backend.userFiles.getDatasetPreparation(op.replacedBy, {}, opts(signal))
      invariant(child.request.replaces?.preparationRef === op.preparationRef, "The replacement belongs to another workflow.")
      op = child
    }
    const preview = op.draftRef && ["pending_review", "incomplete", "save_failed", "saved"].includes(op.state)
      ? await client.backend.userFiles.previewSavedDataset(op.draftRef, { offset: 0, limit: 5 }, opts(signal)) : undefined
    const value = { type: "dataset_review", stage: "review", tool_call_id: item.value.tool_call_id,
      operation: serialization.DatasetBuild.jsonOrThrow(op), can_edit: ["pending_review", "incomplete"].includes(op.state),
      ...(preview ? { preview: serialization.DatasetPreviewPage.jsonOrThrow(preview) } : {}) }
    result.push({ id: item.id, value: datasetInterrupt(value) })
  }
  return result
}

export async function confirmDatasetDecisions(client, waiting, responses, signal) {
  for (const item of waiting.interrupts) {
    if (item.value.type !== "dataset_review" || item.value.stage !== "review") continue
    const answer = responses[item.id]
    if (answer.action === "edit") continue
    let op = await client.backend.userFiles.getDatasetPreparation(answer.preparation_ref, {}, opts(signal))
    invariant(op.review && op.preparationRef === answer.preparation_ref && op.attempt === answer.attempt &&
      op.review.reviewRef === answer.review_ref && op.resultSha256 === answer.result_sha256 && op.review.schemaSha256 === answer.schema_sha256,
    "The native dataset review changed.", "STALE_REVIEW")
    if (answer.action === "continue") { invariant(terminal(op.state), "The native outcome is not confirmed."); continue }
    invariant(op.state !== "saving", "Save is not confirmed. Reconcile the same operation before deciding.", "TEMPORARILY_UNAVAILABLE")
    const expected = answer.action === "decline" ? "discarded" : "saved"
    if (op.state !== expected) {
      const action = answer.action === "decline" ? "discard" : op.state === "save_failed" ? "retry_save" : answer.action
      try {
        op = await client.backend.userFiles.actOnDatasetPreparation(answer.preparation_ref, { body: {
          action, attempt: answer.attempt, resultSha256: answer.result_sha256,
          reviewRef: answer.review_ref, schemaSha256: answer.schema_sha256,
        } }, opts(signal))
      } catch {
        // Only an authoritative read can reconcile a lost write acknowledgement.
        try { op = await client.backend.userFiles.getDatasetPreparation(answer.preparation_ref, {}, opts(signal)) }
        catch { throw new EpochError("TEMPORARILY_UNAVAILABLE", "The dataset decision is unconfirmed; the agent remains paused.") }
      }
    }
    invariant(op.state === expected, "The native dataset decision is not confirmed; the agent remains paused.", "TEMPORARILY_UNAVAILABLE")
  }
}
