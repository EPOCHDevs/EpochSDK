// Epoch's public v1 API with one URL and one API key (ENG-2520). Each method is one v1 operation
// (contracts/public-v1.openapi.json), plus wait and rows, which repeat reads for you. Calls that
// start work send an Idempotency-Key, so a retried call attaches to the work it already started.
// It needs only fetch: no StratifyX or LangGraph client.

export const DEFAULT_API_URL = "https://api.epoch.trade"
const RETRYABLE = new Set([429, 502, 503, 504])
const FINISHED = new Set(["completed", "failed", "cancelled", "needs_input"])
const FINAL_EVENTS = new Set(["questions", "completed", "failed"])
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms))
const backoff = attempt => Math.min(8000, 500 * 2 ** attempt)
const path = value => encodeURIComponent(value)
const env = name => globalThis.process?.env?.[name]

/** A v1 problem response, with the API's own words and stable code. */
export class EpochApiError extends Error {
  constructor(problem) {
    super(problem.detail || problem.title)
    this.name = "EpochApiError"
    this.problem = problem
    this.status = problem.status
    this.code = problem.code
    this.retryable = problem.retryable
    this.requestId = problem.request_id ?? null
  }
}

const problemOf = async response => {
  try {
    const body = await response.json()
    if (body && typeof body.title === "string") return body
  } catch {
    // Not problem+json: describe it from the status.
  }
  return {
    title: response.statusText || "Request failed",
    status: response.status,
    code: response.status >= 500 ? "TEMPORARILY_UNAVAILABLE" : "INVALID_REQUEST",
    retryable: RETRYABLE.has(response.status),
  }
}

const query = values => {
  const params = new URLSearchParams()
  for (const [key, value] of Object.entries(values)) if (value !== undefined && value !== null) params.set(key, String(value))
  const text = params.toString()
  return text ? `?${text}` : ""
}

async function* sseFrames(body) {
  const reader = body.getReader()
  const decoder = new TextDecoder()
  let buffer = ""
  let id
  let data = []
  try {
    for (;;) {
      const { value, done } = await reader.read()
      if (done) return
      buffer += decoder.decode(value, { stream: true })
      for (let end = buffer.search(/\r?\n/); end >= 0; end = buffer.search(/\r?\n/)) {
        const line = buffer.slice(0, end)
        buffer = buffer.slice(end + (buffer[end] === "\r" ? 2 : 1))
        if (line === "") {
          if (data.length) yield { id, data: JSON.parse(data.join("\n")) }
          id = undefined
          data = []
        } else if (!line.startsWith(":")) {
          const colon = line.indexOf(":")
          const field = colon < 0 ? line : line.slice(0, colon)
          let value = colon < 0 ? "" : line.slice(colon + 1)
          if (value.startsWith(" ")) value = value.slice(1)
          if (field === "data") data.push(value)
          else if (field === "id") id = value
        }
      }
    }
  } finally {
    reader.releaseLock()
  }
}

/** A v1 API client. Reads EPOCH_API_KEY, and EPOCH_API_URL when set. */
export class Epoch {
  #key
  #fetch

  constructor({ apiKey = env("EPOCH_API_KEY"), apiUrl = env("EPOCH_API_URL"), maxRetries = 2, fetch = globalThis.fetch } = {}) {
    if (!apiKey) throw new Error("Pass apiKey or set EPOCH_API_KEY")
    this.#key = apiKey
    this.#fetch = fetch
    this.apiUrl = (apiUrl || DEFAULT_API_URL).replace(/\/+$/, "")
    this.maxRetries = maxRetries

    this.research = {
      /** Starts research and returns at once. Follow it with wait, events or get. */
      create: ({ task, context = [], outputs, threadId, idempotencyKey }) =>
        this.request("POST", "/v1/research", {
          json: { request: { task, ...(context.length ? { context } : {}), outputs }, ...(threadId ? { thread_id: threadId } : {}) },
          idempotencyKey,
        }),
      /** The research now. Reading never starts or resumes work. */
      get: researchId => this.request("GET", `/v1/research/${path(researchId)}`),
      /** Answers every pending question by its id; the research continues from the same point. */
      answer: (researchId, answers) => this.request("POST", `/v1/research/${path(researchId)}/answers`, { json: { answers } }),
      /** Reads the research until it finishes, stops, or asks a question. */
      wait: async (researchId, { pollInterval = 10_000, timeout } = {}) => {
        const deadline = timeout === undefined ? Infinity : Date.now() + timeout
        for (;;) {
          const research = await this.#retrying(() => this.research.get(researchId))
          if (research && FINISHED.has(research.status)) return research
          if (Date.now() + pollInterval > deadline) throw new Error(`Research ${researchId} is still ${research?.status ?? "unread"}`)
          await sleep(pollInterval)
        }
      },
      /** Each event as it happens, until a question, the answer or a failure. Stopping never cancels it. */
      events: researchId => this.#events(researchId),
    }
    this.executions = {
      /** Runs a finished research's study again, for new dates. Pass researchId or study. */
      create: ({ researchId, study, start, end, idempotencyKey }) => {
        if (!researchId === !study) throw new Error("Pass exactly one of researchId or study")
        const period = { ...(start ? { start } : {}), ...(end ? { end } : {}) }
        return this.request("POST", "/v1/executions", {
          json: { ...(researchId ? { research_id: researchId } : { study }), parameters: Object.keys(period).length ? { period } : {} },
          idempotencyKey,
        })
      },
      get: executionId => this.request("GET", `/v1/executions/${path(executionId)}`),
      /** Reads the run until it finishes and its answer is saved, or it stops. */
      wait: async (executionId, { pollInterval = 10_000, timeout } = {}) => {
        const deadline = timeout === undefined ? Infinity : Date.now() + timeout
        for (;;) {
          const run = await this.#retrying(() => this.executions.get(executionId))
          const writing = run?.status === "completed" && ["queued", "running"].includes(run.answer?.status)
          if (run && FINISHED.has(run.status) && !writing) return run
          if (Date.now() + pollInterval > deadline) throw new Error(`Run ${executionId} is still ${run?.status ?? "unread"}`)
          await sleep(pollInterval)
        }
      },
    }
    this.responses = {
      /** A saved answer; the latest version unless you pin one. */
      get: (responseId, { version } = {}) => this.request("GET", `/v1/responses/${path(responseId)}${query({ version })}`),
      /** One page of an answer's table. Follow next_offset, with the page's version. */
      table: (responseId, name, { version, offset = 0, pageSize = 1000 } = {}) =>
        this.request("GET", `/v1/responses/${path(responseId)}/tables/${path(name)}${query({ version, offset, page_size: pageSize })}`),
      /** Every row of an answer's table, reading page after page of the same version. */
      rows: async (responseId, name, { version } = {}) => {
        const rows = []
        for (let offset = 0; offset !== null; ) {
          const page = await this.responses.table(responseId, name, { version, offset })
          version = page.version
          rows.push(...page.rows)
          offset = page.next_offset
        }
        return rows
      },
    }
    this.files = {
      /** Uploads one file's bytes. The same content uploaded again returns the same file. */
      upload: async (content, { name, mediaType = "application/octet-stream" }) => {
        const bytes = content instanceof Uint8Array ? content : new Uint8Array(await new Response(content).arrayBuffer())
        const digest = new Uint8Array(await crypto.subtle.digest("SHA-256", bytes))
        const contentSha256 = [...digest].map(byte => byte.toString(16).padStart(2, "0")).join("")
        return this.request("POST", `/v1/files${query({ name, media_type: mediaType, content_sha256: contentSha256 })}`, {
          body: bytes,
          headers: { "Content-Type": "application/octet-stream" },
        })
      },
    }
    this.datasets = {
      /** Prepares a dataset from an uploaded CSV file and returns a preview. Nothing is saved yet. */
      prepare: ({ fileRef, name, columns, delimiter = ",", header = true, nullValues = [""], requestId = crypto.randomUUID() }) =>
        this.request("POST", "/v1/datasets", {
          json: { file_ref: fileRef, request_id: requestId, name, options: { format: "csv", delimiter, header, null_values: nullValues, columns } },
        }),
      /** Saves a prepared dataset; research can then find and use it. */
      save: (draftRef, { name }) =>
        this.request("POST", "/v1/datasets/reviews", { json: { decisions: [{ action: "save", draft_ref: draftRef, name }] } }),
    }
  }

  /** One call, retried on rate limits and outages. Starting work reuses one Idempotency-Key. */
  async request(method, route, { json, body, headers = {}, idempotencyKey } = {}) {
    const sent = { Authorization: `Bearer ${this.#key}`, ...headers }
    if (json !== undefined) {
      sent["Content-Type"] = "application/json"
      body = JSON.stringify(json)
    }
    if (method === "POST") sent["Idempotency-Key"] = idempotencyKey ?? crypto.randomUUID()
    for (let attempt = 0; ; attempt++) {
      const last = attempt >= this.maxRetries
      let response
      try {
        response = await this.#fetch(this.apiUrl + route, { method, headers: sent, body })
      } catch (error) {
        if (last) throw error
        await sleep(backoff(attempt))
        continue
      }
      if (RETRYABLE.has(response.status) && !last) {
        const after = Number(response.headers.get("Retry-After"))
        await sleep(Number.isFinite(after) && after > 0 ? Math.min(30, after) * 1000 : backoff(attempt))
        continue
      }
      if (response.ok) return response.json()
      throw new EpochApiError(await problemOf(response))
    }
  }

  /** A read inside a wait loop: a passing outage means "not yet", not a failure. */
  async #retrying(read) {
    try {
      return await read()
    } catch (error) {
      if (error instanceof EpochApiError && !error.retryable) throw error
      return null
    }
  }

  async *#events(researchId) {
    let last
    for (let attempt = 0; ; attempt++) {
      const headers = { Authorization: `Bearer ${this.#key}`, Accept: "text/event-stream", ...(last ? { "Last-Event-ID": last } : {}) }
      let response
      try {
        response = await this.#fetch(`${this.apiUrl}/v1/research/${path(researchId)}/events`, { headers })
        if (!response.ok) throw new EpochApiError(await problemOf(response))
        for await (const frame of sseFrames(response.body)) {
          attempt = 0
          if (frame.id) last = frame.id
          yield frame.data
          if (FINAL_EVENTS.has(frame.data.event)) return
        }
      } catch (error) {
        if (error instanceof EpochApiError) throw error
      }
      if (attempt >= this.maxRetries) throw new EpochApiError({ title: "The event stream kept dropping", status: 503, code: "TEMPORARILY_UNAVAILABLE", retryable: true })
      await sleep(backoff(attempt))
    }
  }

  toString() {
    return `Epoch(${this.apiUrl})`
  }
}
