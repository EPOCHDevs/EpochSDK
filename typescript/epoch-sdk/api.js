// Epoch's public v1 API with one URL and one API key (ENG-2520). Each method is one v1 operation
// (contracts/public-v1.openapi.json), plus wait and rows, which repeat reads for you. Calls that
// start work send an Idempotency-Key, so a retried call attaches to the work it already started.
// Calls the server does not deduplicate (answering, saving a dataset) are never sent twice.
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
  constructor(problem, { retryAfter = null } = {}) {
    super(problem.detail || problem.title || `HTTP ${problem.status}`)
    this.name = "EpochApiError"
    this.problem = problem
    this.status = problem.status
    this.code = problem.code
    this.retryable = problem.retryable
    this.requestId = problem.request_id ?? null
    /** Seconds the server asked you to wait, when it said. */
    this.retryAfter = retryAfter
  }
}

const retryAfterOf = response => {
  const header = response.headers.get("Retry-After")
  const seconds = header === null ? NaN : Number(header)
  return Number.isFinite(seconds) ? Math.min(30, Math.max(0, seconds)) : null
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

async function* sseFrames(body, idleTimeout) {
  const reader = body.getReader()
  const decoder = new TextDecoder()
  let buffer = ""
  let id
  let data = []
  // The server sends a comment every 15 seconds, so a quiet connection is a dead one.
  const read = () => {
    let timer
    const quiet = new Promise((_, reject) => {
      timer = setTimeout(() => reject(new TypeError("The event stream went quiet")), idleTimeout)
    })
    return Promise.race([reader.read(), quiet]).finally(() => clearTimeout(timer))
  }
  try {
    for (;;) {
      const { value, done } = await read()
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
    // Stopping early closes the connection rather than leaving it to the server's keep-alives.
    await reader.cancel().catch(() => {})
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
    // Browsers and Workers refuse a fetch called without its global as `this`.
    this.#fetch = fetch === globalThis.fetch ? fetch.bind(globalThis) : fetch
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
      /**
       * Answers every pending question by its id; the research continues from the same point.
       * Sent once: if the reply is lost, read the research to see whether it continued.
       */
      answer: (researchId, answers) =>
        this.request("POST", `/v1/research/${path(researchId)}/answers`, { json: { answers }, deduplicated: false }),
      /** Reads the research until it finishes, stops, or asks a question. */
      wait: async (researchId, { pollInterval = 10_000, timeout } = {}) => {
        const deadline = timeout === undefined ? Infinity : Date.now() + timeout
        for (;;) {
          const research = await this.#retrying(() => this.research.get(researchId))
          if (research && FINISHED.has(research.status)) return research
          const remaining = deadline - Date.now()
          if (remaining <= 0) throw new Error(`Research ${researchId} is still ${research?.status ?? "unread"}`)
          await sleep(Math.min(pollInterval, remaining))
        }
      },
      /**
       * Each event as it happens, until a question, the answer or a failure. A dropped, quiet or
       * briefly unavailable stream reconnects after the last event. Stopping never cancels it.
       */
      events: (researchId, options) => this.#events(researchId, options),
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
          const remaining = deadline - Date.now()
          if (remaining <= 0) throw new Error(`Run ${executionId} is still ${run?.status ?? "unread"}`)
          await sleep(Math.min(pollInterval, remaining))
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
        for (let offset = 0; offset != null; ) {
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
      /**
       * Prepares a dataset from an uploaded CSV file and returns a preview. Nothing is saved yet.
       * Leave out columns to keep the file's own; columns must otherwise name every column, in order.
       */
      prepare: ({ fileRef, name, columns = [], delimiter = ",", header = true, nullValues = [""], requestId = crypto.randomUUID() }) =>
        this.request("POST", "/v1/datasets", {
          json: { file_ref: fileRef, request_id: requestId, name, options: { format: "csv", delimiter, header, null_values: nullValues, columns } },
        }),
      /** Saves a prepared dataset; research can then find and use it. Sent once, like answer. */
      save: (draftRef, { name }) =>
        this.request("POST", "/v1/datasets/reviews", {
          json: { decisions: [{ action: "save", draft_ref: draftRef, name }] },
          deduplicated: false,
        }),
    }
  }

  /**
   * One call, retried when the server marks its problem retryable. Starting work reuses one
   * Idempotency-Key, so a retry attaches to the same work. A call the server does not deduplicate
   * is retried only after a rate limit, which refuses it before any work.
   */
  async request(method, route, { json, body, headers = {}, idempotencyKey, deduplicated = true } = {}) {
    const sent = { Authorization: `Bearer ${this.#key}`, ...headers }
    if (json !== undefined) {
      sent["Content-Type"] = "application/json"
      body = JSON.stringify(json)
    }
    if (method === "POST" && deduplicated) sent["Idempotency-Key"] = idempotencyKey ?? crypto.randomUUID()
    for (let attempt = 0; ; attempt++) {
      const last = attempt >= this.maxRetries
      let response
      try {
        response = await this.#fetch(this.apiUrl + route, { method, headers: sent, body })
      } catch (error) {
        // A lost reply may follow work that was done: only a deduplicated call is sent again.
        if (last || !deduplicated) throw error
        await sleep(backoff(attempt))
        continue
      }
      if (response.ok) return response.json()
      const problem = await problemOf(response)
      const after = retryAfterOf(response)
      if (!last && problem.retryable && (deduplicated || response.status === 429)) {
        await sleep(after !== null ? after * 1000 : backoff(attempt))
        continue
      }
      throw new EpochApiError(problem, { retryAfter: after })
    }
  }

  /** A read inside a wait loop: a retryable problem or a lost connection means "not yet". */
  async #retrying(read) {
    try {
      return await read()
    } catch (error) {
      // fetch reports a lost connection as a TypeError; anything else (a bad reply, say) is real.
      if (error instanceof EpochApiError ? error.retryable : error instanceof TypeError) return null
      throw error
    }
  }

  async *#events(researchId, { lastEventId, signal, idleTimeout = 60_000 } = {}) {
    let last = lastEventId
    for (let attempt = 0; ; attempt++) {
      const headers = { Authorization: `Bearer ${this.#key}`, Accept: "text/event-stream", ...(last ? { "Last-Event-ID": last } : {}) }
      let wait = null
      try {
        const response = await this.#fetch(`${this.apiUrl}/v1/research/${path(researchId)}/events`, { headers, signal })
        if (!response.ok) {
          const error = new EpochApiError(await problemOf(response), { retryAfter: retryAfterOf(response) })
          if (!error.retryable) throw error
          wait = error.retryAfter
        } else {
          for await (const frame of sseFrames(response.body, idleTimeout)) {
            attempt = 0
            if (frame.id) last = frame.id
            yield frame.data
            if (FINAL_EVENTS.has(frame.data.event)) return
          }
        }
      } catch (error) {
        // Stopping and refusals end the stream; a dropped or quiet connection reconnects.
        if (signal?.aborted || error instanceof EpochApiError) throw error
      }
      if (attempt >= this.maxRetries) throw new EpochApiError({ title: "The event stream kept dropping", status: 503, code: "TEMPORARILY_UNAVAILABLE", retryable: true })
      await sleep(wait !== null ? wait * 1000 : backoff(attempt))
    }
  }

  toString() {
    return `Epoch(${this.apiUrl})`
  }
}
