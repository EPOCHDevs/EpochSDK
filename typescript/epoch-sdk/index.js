import { invariant, validateResponse, requestToWire, parametersToWire, operationId } from "./contract.js"
import { researchStatus, resumeResearch, startResearch } from "./research.js"
import { executionStatus, ordinarySource, startExecution } from "./execution.js"
export { EpochError, parseRequest, requestToWire, responseToWire, validateRequest, validateResponse } from "./contract.js"

function pause(ms, signal) {
  signal?.throwIfAborted()
  return new Promise((resolve, reject) => {
    const abort = () => { clearTimeout(timer); reject(signal.reason ?? new DOMException("Observation stopped", "AbortError")) }
    const timer = setTimeout(() => { signal?.removeEventListener("abort", abort); resolve() }, ms)
    signal?.addEventListener("abort", abort, { once: true })
  })
}

/** Uses the caller's authenticated native clients. Credentials never enter workflow arguments. */
export class EpochClient {
  constructor({ backend, graph, assistantId = "epoch-ai", pollIntervalMs = 1000 }) {
    invariant(backend && graph, "Provide authenticated StratifyX and LangGraph clients.")
    this.backend = backend
    this.graph = graph
    this.assistantId = assistantId
    this.pollIntervalMs = Math.max(250, pollIntervalMs)
  }

  async observe(state, options = {}) {
    options.onStatus?.(state)
    while (options.wait !== false && ["accepted", "in_progress"].includes(state.status)) {
      await pause(this.pollIntervalMs, options.signal)
      state = await this.status(state.operationId, { kind: state.kind, signal: options.signal })
      options.onStatus?.(state)
    }
    return state
  }

  async run(request, options) {
    options?.signal?.throwIfAborted()
    return this.observe(await startResearch(this, request, options), options)
  }

  async resume(waiting, responses, options = {}) {
    options.signal?.throwIfAborted()
    return this.observe(await resumeResearch(this, waiting, responses, options), options)
  }

  async status(operationId, { kind = "run", ...options } = {}) {
    options.signal?.throwIfAborted()
    invariant(kind === "run" || kind === "execute", "Choose run or execute for the operation kind.")
    return kind === "run" ? researchStatus(this, operationId, options) : executionStatus(this, operationId, options)
  }

  async execute(reference, options) {
    options?.signal?.throwIfAborted()
    return this.observe(await startExecution(this, reference, options), options)
  }

  async read(responseId, { version, signal } = {}) {
    invariant(typeof responseId === "string" && responseId.trim() === responseId && responseId.length,
      "Provide an exact nonblank response ID.", "VALIDATION_ERROR")
    invariant(version === undefined || (Number.isSafeInteger(version) && version >= 1), "Version must be a positive safe integer.", "VALIDATION_ERROR")
    const response = await this.backend.researchResponses.getResearchResponse(responseId,
      version === undefined ? {} : { version }, { maxRetries: 0, abortSignal: signal })
    invariant(response.responseId === responseId && (version === undefined || response.version === version),
      "Backend returned another saved answer or revision.", "OUTPUT_VALIDATION_FAILED")
    return validateResponse(response)
  }

  async readRequest(id, { signal } = {}) {
    operationId(id)
    const record = await this.backend.sdkRequests.getSdkRequestByHandle(id, {}, { maxRetries: 0, abortSignal: signal })
    invariant(record.operationId === id, "The handle returned another research operation.")
    return requestToWire(record.request)
  }

  async readExecutionRequest(id, { signal } = {}) {
    operationId(id)
    const record = await this.backend.sdkRequests.getSdkExecutionRequestByHandle(id, {}, { maxRetries: 0, abortSignal: signal })
    const request = record.request
    invariant(request.operationId === id && request.sourceExecutionId, "The handle returned another saved study execution.")
    return { reference: {
      studyId: request.studyId, sourceExecutionId: request.sourceExecutionId,
      ...(request.threadId ? { threadId: request.threadId } : {}),
      ...(request.reportTemplate ? { reportTemplate: request.reportTemplate } : {}),
      ...(request.responsePlan ? { responsePlan: request.responsePlan } : {}),
    }, parameters: parametersToWire(request.parameters) }
  }

  ordinarySource(reference, signal, inferStudy = false) { return ordinarySource(this, reference, signal, inferStudy) }
}
