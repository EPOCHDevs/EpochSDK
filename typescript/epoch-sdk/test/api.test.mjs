import assert from "node:assert/strict"
import test from "node:test"
import { createHash } from "node:crypto"
import { Epoch, EpochApiError } from "../api.js"

const KEY = "epk_test_0123456789abcdef_" + "a".repeat(64)
const RESEARCH = {
  id: "req_1", object: "research", status: "queued", operation_id: "op-1", created_at: "2026-11-11T10:00:00Z",
  updated_at: "2026-11-11T10:00:00Z", questions: [], result: null, error: null,
  links: { self: "/v1/research/req_1", events: "/v1/research/req_1/events" },
}
const json = (status, body, headers = {}) => new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json", ...headers } })
const client = (handler) => {
  const calls = []
  const epoch = new Epoch({ apiKey: KEY, apiUrl: "https://api.test.epoch.trade/", fetch: async (url, init = {}) => {
    calls.push({ url, ...init })
    return handler(url, init, calls.length)
  } })
  return { epoch, calls }
}

test("starting research sends the request with the key and an idempotency key", async () => {
  const { epoch, calls } = client(() => json(202, RESEARCH))
  const research = await epoch.research.create({ task: "Compare MSFT and SPY volatility in 2025.", context: ["Use daily returns."],
    outputs: [{ name: "summary", type: "text", instructions: "Explain it." }] })
  assert.equal(research.id, "req_1")
  const [call] = calls
  assert.equal(call.url, "https://api.test.epoch.trade/v1/research")
  assert.equal(call.headers.Authorization, `Bearer ${KEY}`)
  assert.ok(call.headers["Idempotency-Key"])
  assert.deepEqual(JSON.parse(call.body), { request: { task: "Compare MSFT and SPY volatility in 2025.", context: ["Use daily returns."],
    outputs: [{ name: "summary", type: "text", instructions: "Explain it." }] } })
  assert.ok(!String(epoch).includes(KEY))
})

test("a key is required", () => {
  const saved = process.env.EPOCH_API_KEY
  delete process.env.EPOCH_API_KEY
  try {
    assert.throws(() => new Epoch(), /EPOCH_API_KEY/)
  } finally {
    if (saved !== undefined) process.env.EPOCH_API_KEY = saved
  }
})

test("an outage is retried with the same idempotency key", async () => {
  const { epoch, calls } = client((url, init, n) => n === 1
    ? json(503, { title: "Service unavailable", status: 503, code: "TEMPORARILY_UNAVAILABLE", retryable: true }, { "Retry-After": "0" })
    : json(202, RESEARCH))
  await epoch.research.create({ task: "Task", outputs: [], idempotencyKey: "mine" })
  assert.deepEqual(calls.map(c => c.headers["Idempotency-Key"]), ["mine", "mine"])
})

test("a problem raises EpochApiError with its details", async () => {
  const { epoch } = client(() => json(409, { title: "Conflict", status: 409, code: "IDEMPOTENCY_CONFLICT", retryable: false,
    detail: "This operation ID already has different accepted inputs.", request_id: "r-9" }))
  await assert.rejects(epoch.research.create({ task: "Task", outputs: [] }), (error) =>
    error instanceof EpochApiError && error.status === 409 && error.code === "IDEMPOTENCY_CONFLICT" && error.requestId === "r-9"
    && /different accepted inputs/.test(error.message))
})

test("wait reads until research finishes or asks", async () => {
  const states = ["queued", "running", "needs_input"]
  const { epoch } = client(() => json(200, { ...RESEARCH, status: states.shift() }))
  assert.equal((await epoch.research.wait("req_1", { pollInterval: 1 })).status, "needs_input")
})

test("events resume after the last event and stop at the answer", async () => {
  const completed = { event: "completed", research: { ...RESEARCH, status: "completed" } }
  const { epoch, calls } = client((url, init, n) => new Response(n === 1
    ? 'data: {"event":"status","research_id":"req_1","status":"running"}\n\n: keep-alive\n\nid: 1-0\ndata: {"event":"ui","research_id":"req_1","message":{}}\n\n'
    : `id: 2-0\ndata: ${JSON.stringify(completed)}\n\n`, { headers: { "Content-Type": "text/event-stream" } }))
  epoch.maxRetries = 2
  const events = []
  for await (const event of epoch.research.events("req_1")) events.push(event.event)
  assert.deepEqual(events, ["status", "ui", "completed"])
  assert.deepEqual(calls.map(c => c.headers["Last-Event-ID"]), [undefined, "1-0"])
})

test("rows reads every page of the same version", async () => {
  const { epoch, calls } = client((url) => {
    const offset = Number(new URL(url).searchParams.get("offset"))
    return json(200, { response_id: "rsp_1", version: 3, name: "t", type: "table", schema: [], rows: [[`S${offset}`]],
      offset, total_rows: 2, next_offset: offset === 0 ? 1 : null })
  })
  assert.deepEqual(await epoch.responses.rows("rsp_1", "t"), [["S0"], ["S1"]])
  assert.deepEqual(calls.map(c => new URL(c.url).search), ["?offset=0&page_size=1000", "?version=3&offset=1&page_size=1000"])
})

test("a run needs exactly one source and sends its dates", async () => {
  const { epoch, calls } = client(() => json(202, { id: "job_1", status: "running" }))
  await epoch.executions.create({ researchId: "req_1", start: "2026-01-01", end: "2026-10-31" })
  assert.deepEqual(JSON.parse(calls[0].body), { research_id: "req_1", parameters: { period: { start: "2026-01-01", end: "2026-10-31" } } })
  assert.throws(() => epoch.executions.create({}), /exactly one/)
})

test("upload sends the exact bytes and their digest", async () => {
  const bytes = new TextEncoder().encode("date,revenue\n2026-07-01,1\n")
  const { epoch, calls } = client(() => json(200, { file_ref: "file_1" }))
  await epoch.files.upload(bytes, { name: "q3-sales.csv", mediaType: "text/csv" })
  const url = new URL(calls[0].url)
  assert.equal(url.searchParams.get("content_sha256"), createHash("sha256").update(bytes).digest("hex"))
  assert.equal(url.searchParams.get("name"), "q3-sales.csv")
  assert.equal(calls[0].headers["Content-Type"], "application/octet-stream")
  assert.deepEqual(calls[0].body, bytes)
})

test("wait keeps reading through a passing outage", async () => {
  const replies = [
    json(503, { title: "Busy", status: 503, code: "TEMPORARILY_UNAVAILABLE", retryable: true }),
    json(200, { ...RESEARCH, status: "completed" }),
  ]
  const { epoch } = client(() => replies.shift())
  epoch.maxRetries = 0
  assert.equal((await epoch.research.wait("req_1", { pollInterval: 1 })).status, "completed")
})

const problem = (status, code, retryable) => ({ title: "Problem", status, code, retryable })

test("the default fetch is called with its global, as browsers require", async () => {
  const saved = globalThis.fetch
  globalThis.fetch = function (url) {
    if (this !== globalThis) throw new TypeError("Illegal invocation")
    return Promise.resolve(json(200, RESEARCH))
  }
  try {
    const epoch = new Epoch({ apiKey: KEY, apiUrl: "https://api.test.epoch.trade" })
    assert.equal((await epoch.research.get("req_1")).id, "req_1")
  } finally {
    globalThis.fetch = saved
  }
})

test("wait does not mistake a bad reply for an outage", async () => {
  const { epoch } = client(() => new Response("<html>", { status: 200 }))
  await assert.rejects(epoch.research.wait("req_1", { pollInterval: 1, timeout: 1000 }), SyntaxError)
})

test("an answer is sent once after an outage, and again after a rate limit", async () => {
  const outage = client(() => json(503, problem(503, "TEMPORARILY_UNAVAILABLE", true), { "Retry-After": "0" }))
  await assert.rejects(outage.epoch.research.answer("req_1", {}), EpochApiError)
  assert.equal(outage.calls.length, 1)
  assert.equal(outage.calls[0].headers["Idempotency-Key"], undefined)
  const limited = client((url, init, n) => n === 1
    ? json(429, problem(429, "RATE_LIMITED", true), { "Retry-After": "-1" })
    : json(202, { ...RESEARCH, status: "running" }))
  assert.equal((await limited.epoch.research.answer("req_1", {})).status, "running")
  assert.equal(limited.calls.length, 2)
})

test("retries follow the server's retryable flag", async () => {
  const { epoch, calls } = client((url, init, n) => n === 1
    ? json(500, problem(500, "INTERNAL_ERROR", true), { "Retry-After": "0" })
    : json(200, RESEARCH))
  assert.equal((await epoch.research.get("req_1")).id, "req_1")
  assert.equal(calls.length, 2)
})

const stream = (text, onCancel) => new ReadableStream({
  start(controller) {
    if (text !== null) controller.enqueue(new TextEncoder().encode(text))
  },
  cancel: onCancel,
})

test("stopping an event stream early closes its connection", async () => {
  let cancelled = false
  const { epoch } = client(() => new Response(stream('data: {"event":"status","research_id":"req_1","status":"running"}\n\n', () => {
    cancelled = true
  }), { headers: { "Content-Type": "text/event-stream" } }))
  for await (const event of epoch.research.events("req_1")) {
    assert.equal(event.event, "status")
    break
  }
  assert.ok(cancelled)
})

test("events reconnect after a quiet connection or a brief outage, from the last event id", async () => {
  const completed = `id: 3-0\ndata: ${JSON.stringify({ event: "completed", research: { ...RESEARCH, status: "completed" } })}\n\n`
  const { epoch, calls } = client((url, init, n) => n === 1
    ? new Response(stream(null), { headers: { "Content-Type": "text/event-stream" } })
    : n === 2
      ? json(503, problem(503, "TEMPORARILY_UNAVAILABLE", true), { "Retry-After": "0" })
      : new Response(completed, { headers: { "Content-Type": "text/event-stream" } }))
  epoch.maxRetries = 3
  const events = []
  for await (const event of epoch.research.events("req_1", { lastEventId: "2-0", idleTimeout: 20 })) events.push(event.event)
  assert.deepEqual(events, ["completed"])
  assert.deepEqual(calls.map(c => c.headers["Last-Event-ID"]), ["2-0", "2-0", "2-0"])
})

test("events stop at a lasting refusal and when the caller aborts", async () => {
  const refused = client(() => json(404, problem(404, "NOT_FOUND", false)))
  await assert.rejects((async () => {
    for await (const event of refused.epoch.research.events("req_other")) void event
  })(), error => error instanceof EpochApiError && error.code === "NOT_FOUND")
  const controller = new AbortController()
  controller.abort()
  const aborted = client((url, init) => {
    init.signal.throwIfAborted()
    return json(200, {})
  })
  await assert.rejects((async () => {
    for await (const event of aborted.epoch.research.events("req_1", { signal: controller.signal })) void event
  })(), error => error.name === "AbortError")
  assert.equal(aborted.calls.length, 1)
})

test("rows stops at the last page even when next_offset is left out", async () => {
  const { epoch, calls } = client(() => json(200, { response_id: "rsp_1", version: 1, name: "t", type: "table", schema: [],
    rows: [["a"]], offset: 0, total_rows: 1 }))
  assert.deepEqual(await epoch.responses.rows("rsp_1", "t"), [["a"]])
  assert.equal(calls.length, 1)
})

test("a dataset keeps the file's own columns unless you name them", async () => {
  const { epoch, calls } = client(() => json(200, {}))
  await epoch.datasets.prepare({ fileRef: "file:abc", name: "Sales" })
  assert.deepEqual(JSON.parse(calls[0].body).options.columns, [])
})
