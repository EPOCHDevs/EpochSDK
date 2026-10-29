import { ExecutionOptions } from "@epoch/stratifyx/serialization/types/ExecutionOptions.js"
import { canonical, EpochError, invariant, operationId, parseParameters, statusCode, throwNativeError } from "./contract.js"

const opts = signal => ({ maxRetries: 0, abortSignal: signal })

export async function ordinarySource(client, reference, signal, inferStudy = false) {
  invariant(reference.sourceExecutionId, "A saved study needs its exact source execution.", "NOT_REUSABLE")
  const job = await client.backend.studiesExecutions.getExecutionById(reference.sourceExecutionId, {}, opts(signal))
  const snapshot = await client.backend.studiesExecutions.getThePerExecutionStudySnapshotAsRunSourceAssetsScreen(reference.sourceExecutionId, {}, opts(signal))
  invariant(job.id === reference.sourceExecutionId && (inferStudy || job.definitionId === reference.studyId) &&
    snapshot.executionId === job.id && snapshot.definitionId === job.definitionId &&
    ["research", "backtest"].includes(job.executionType) && !job.parentExecutionId &&
    (!job.visibility || job.visibility === "primary") && !snapshot.executionInput && snapshot.study.authoringOrigin === "agent",
  "The saved reference is not an owned ordinary study execution.", "NOT_REUSABLE")
  let execution
  if (job.trading) {
    const serialized = ExecutionOptions.json(job.trading)
    invariant(serialized.ok, "The retained trading settings cannot be replayed.", "NOT_REUSABLE")
    execution = parseParameters({ execution: serialized.value }).execution
  }
  return { job, snapshot, execution, bindings: snapshot.executionParameterBindings }
}

export async function startExecution(client, reference, options) {
  const op = operationId(options.operationId)
  if (typeof reference === "string") {
    const research = await client.status(reference, { signal: options.signal })
    invariant(research.status === "succeeded" && research.reusableStudy,
      "This research operation has no reusable saved study.", "NOT_REUSABLE")
    reference = research.reusableStudy
  }
  invariant(reference && typeof reference.studyId === "string" && reference.studyId && reference.sourceExecutionId,
    "Provide the reusable study reference from a completed research operation.", "VALIDATION_ERROR")
  invariant(!(reference.reportTemplate && reference.responsePlan), "Choose one saved report or response plan.", "VALIDATION_ERROR")
  const parameters = parseParameters({ period: options.period, ...(options.execution ? { execution: options.execution } : {}) })
  let bindings
  if (!reference.reportTemplate && !reference.responsePlan) {
    let accepted
    try { accepted = await client.backend.sdkRequests.getSdkExecutionRequestByHandle(op, {}, opts(options.signal)) }
    catch (error) { if (statusCode(error) !== 404) throw error }
    if (accepted) {
      invariant(accepted.request.operationId === op, "The execution handle differs from the requested operation.")
      parameters.execution ??= accepted.request.parameters.execution
      bindings = accepted.request.executionParameterBindings
    } else {
      const source = await ordinarySource(client, reference, options.signal)
      parameters.execution ??= source.execution
      bindings = source.bindings
    }
  }
  options.signal?.throwIfAborted()
  try {
    const record = await client.backend.sdkRequests.createSdkExecutionRequest({
      operationId: op, studyId: reference.studyId, sourceExecutionId: reference.sourceExecutionId,
      parameters,
      ...(reference.threadId ? { threadId: reference.threadId } : {}),
      ...(reference.reportTemplate ? { reportTemplate: reference.reportTemplate } : {}),
      ...(reference.responsePlan ? { responsePlan: reference.responsePlan } : {}),
      ...(bindings ? { executionParameterBindings: bindings } : {}),
    }, opts(options.signal))
    invariant(record.request.operationId === op, "Backend returned another execution operation.")
  } catch (error) {
    if (statusCode(error) !== 409) throw error
    try { await client.backend.sdkRequests.getSdkExecutionRequestByHandle(op, {}, opts(options.signal)) }
    catch (readError) {
      if (statusCode(readError) !== 404) throw readError
      throw new EpochError("INVALID_STATE", error.body?.message ?? "The saved study rejected this execution before admission.")
    }
    throw new EpochError("IDEMPOTENCY_CONFLICT", "This operation ID has different accepted inputs. Use a new ID for a changed execution.")
  }
  return executionStatus(client, op, options)
}

function checkPublication(record, response) {
  const output = record.extensionOutputs
  const provenance = output?.provenance
  invariant(!record.error && record.executionStatus === "Completed" && record.responsePhase === "outputs_recorded" && provenance,
    "The execution has no confirmed required-output publication.", "OUTPUT_VALIDATION_FAILED")
  invariant(provenance.executionId === record.executionId && provenance.studyId === record.request.studyId &&
    provenance.sourceExecutionId === (record.request.sourceExecutionId ?? "") &&
    canonical(provenance.additionalSources ?? []) === canonical(record.request.additionalSources ?? []) &&
    Object.entries(record.request.executionParameterBindings ?? {}).every(([key, value]) =>
      canonical(provenance.executionParameterBindings?.[key]) === canonical(value)) &&
    output.responseId === record.responseId && output.responseVersion === record.responseVersion,
  "The publication differs from the accepted execution.", "OUTPUT_VALIDATION_FAILED")
  if (response) invariant(response.requestId === record.requestId && response.primaryExecutionId === record.executionId &&
    response.studyId === record.request.studyId && response.threadId === (record.request.threadId ?? record.executionId) &&
    response.responseId === record.responseId && response.version === record.responseVersion &&
    canonical(response.extension) === canonical(provenance) && !response.responsePlan,
  "The saved answer differs from the native publication.", "OUTPUT_VALIDATION_FAILED")
}

export async function executionStatus(client, op, { signal } = {}) {
  operationId(op)
  const record = await client.backend.sdkRequests.getSdkExecutionRequestByHandle(op, {}, opts(signal))
  invariant(record.request.operationId === op, "The execution handle returned another operation.")
  throwNativeError(record)
  invariant(!["Failed", "Cancelled"].includes(record.executionStatus), "The prepared execution failed or was cancelled.", "EXECUTION_FAILED")
  invariant(record.responsePhase !== "failed", "The required outputs failed.", "OUTPUT_VALIDATION_FAILED")
  const pending = { status: "in_progress", kind: "execute", requestId: record.requestId,
    operationId: op, executionId: record.executionId }
  let job
  try { job = await client.backend.studiesExecutions.getExecutionById(record.executionId, {}, opts(signal)) }
  catch (error) { if (statusCode(error) === 404 && record.phase === "accepted") return pending; throw error }
  invariant(job.id === record.executionId && job.definitionId === record.request.studyId,
    "The execution differs from its accepted saved study.")
  invariant(!["failed", "cancelled"].includes(job.status), job.errorReason || "The prepared execution failed.", "EXECUTION_FAILED")
  if (job.status !== "completed" || ((record.request.responsePlan || record.request.reportTemplate || record.responsePhase) &&
    record.responsePhase !== "outputs_recorded")) return { ...pending, execution: job }
  let response
  let report
  if (record.responseId !== undefined) {
    invariant(record.responseVersion !== undefined, "The execution answer has no pinned revision.")
    response = await client.read(record.responseId, { version: record.responseVersion, signal })
  }
  if (record.request.reportTemplate) {
    invariant(record.reportRequestId && record.reportRequest, "The replay has no admitted report.")
    report = await client.backend.sdkRequests.getSdkExecutionRequest(record.reportRequestId, {}, opts(signal))
    invariant(report.requestId === record.reportRequestId && canonical(report.request) === canonical(record.reportRequest) &&
      report.request.sourceExecutionId === record.executionId && report.requestId !== record.requestId &&
      report.responseId === record.responseId && report.responseVersion === record.responseVersion,
    "The replay report differs from its captured source.", "OUTPUT_VALIDATION_FAILED")
    checkPublication(report, response)
  } else if (record.request.responsePlan) {
    invariant(response && response.requestId === record.requestId && response.primaryExecutionId === record.executionId &&
      response.studyId === record.request.studyId && canonical(response.responsePlan) === canonical(record.request.responsePlan) &&
      (!record.request.threadId || response.threadId === record.request.threadId),
    "The saved response differs from the accepted plan.", "OUTPUT_VALIDATION_FAILED")
  } else if (record.responsePhase) checkPublication(record, response)
  return { status: "execution_selected", kind: "execute", operationId: op, requestId: record.requestId,
    execution: job, response, ...(report ? { report } : {}), reusableStudy: {
      studyId: record.request.studyId, sourceExecutionId: record.executionId,
      ...(record.request.threadId ? { threadId: record.request.threadId } : {}),
      ...(record.request.reportTemplate ? { reportTemplate: record.request.reportTemplate } : {}),
      ...(record.request.responsePlan ? { responsePlan: record.request.responsePlan } : {}),
    } }
}
