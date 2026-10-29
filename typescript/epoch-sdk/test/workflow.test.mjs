import assert from "node:assert/strict"
import test from "node:test"
import { pathToFileURL } from "node:url"
import { readFile } from "node:fs/promises"
import { createRequire } from "node:module"

const entry = process.env.EPOCH_SDK_TEST_ENTRY ? pathToFileURL(process.env.EPOCH_SDK_TEST_ENTRY) : new URL("../index.js", import.meta.url)
const sdk = await import(entry.href)
const native = await import(process.env.EPOCH_NATIVE_TEST_ENTRY ? pathToFileURL(process.env.EPOCH_NATIVE_TEST_ENTRY).href : "@epoch/stratifyx")
const { researchThreadId } = await import(new URL("./research.js", entry).href)
const { EpochClient, validateRequest, parseRequest, requestToWire, responseToWire, validateResponse } = sdk
const copy = value => JSON.parse(JSON.stringify(value))
const request = () => ({ task: "Explain a concept", context: ["Use supplied facts."], outputs: [
  { name: "answer", type: "text", format: "markdown", instructions: "Be concise." },
] })
const answer = (req, threadId) => ({ response_id: "example_response", request_id: "req_11111111111111111111111111111111",
  thread_id: threadId, version: 1, published_at_ms: 0,
  content: { declarations: copy(req.outputs), outputs: [{ name: "answer", type: "text", format: "markdown", value: "Example answer." }] } })
const question = () => ({ id: "interrupt_1", value: { type: "ask_user", tool_call_id: "tool_1", questions: [
  { question: "Which interval?", description: "Choose one.", multi_select: false,
    options: [{ label: "Daily", recommended: true }, { label: "Weekly", recommended: false }] },
] } })

function harness() {
  const calls = []
  const graphCalls = []
  const state = { record: null, response: null, runStatus: "running", interrupts: [], published: null, execution: null, job: null }
  const response = (body, args) => ({ ok: true, body: copy(body), rawResponse: new Response(JSON.stringify(body), { status: 200 }) })
  const backend = new native.StratifyXClient({ baseUrl: "https://backend.invalid", fetcher: async args => {
    assert.equal(args.maxRetries, 0, "No implicit retries, including reads")
    const path = new URL(args.url).pathname
    const body = typeof args.body === "string" ? JSON.parse(args.body) : args.body
    calls.push({ path, method: args.method, body: body && copy(body), query: args.queryParameters })
    if (path === "/api/v1/integration/requests" && args.method === "POST") {
      if (state.record) {
        if (JSON.stringify(state.record.request) !== JSON.stringify(body.request)) return { ok: false,
          error: { reason: "status-code", statusCode: 409, body: { message: "Changed inputs" } }, rawResponse: new Response(null, { status: 409 }) }
      } else state.record = { request_id: "req_11111111111111111111111111111111", version: 1,
        created_at_ms: 0, updated_at_ms: 0, phase: "accepted", request: body.request,
        operation_id: body.operation_id, launch: body.launch }
      return response(state.record, args)
    }
    if (path.startsWith("/api/v1/integration/requests/")) {
      assert.ok(state.record)
      if (args.method === "PATCH") {
        assert.equal(body.expected_version, state.record.version)
        const { expected_version, ...patch } = body
        Object.assign(state.record, patch, { version: state.record.version + 1 })
      }
      return response(state.record, args)
    }
    if (path.startsWith("/api/v1/research/responses/")) return response(state.response, args)
    if (path.startsWith("/api/v1/integration/execution-requests")) {
      assert.ok(state.execution)
      if (args.method === "POST") {
        assert.equal(body.operation_id, state.execution.request.operation_id)
        state.execution.request = copy(body)
      }
      return response(state.execution, args)
    }
    if (path.startsWith("/api/v1/studies/executions/")) return response(state.job, args)
    throw new Error(`Unexpected request ${args.method} ${path}`)
  } })
  const graph = {
    threads: {
      create: async payload => { graphCalls.push(["threads.create", payload]); return { thread_id: payload.threadId } },
      getState: async () => ({ values: {}, interrupts: [] }),
      getHistory: async (id, options) => {
        graphCalls.push(["history", id, options])
        return [{ values: { authority_turn_id: `user-turn:${state.record.request_id}`,
          ...(state.published ? { published_response: state.published } : {}) }, interrupts: copy(state.interrupts) }]
      },
    },
    runs: {
      create: async (threadId, assistantId, payload) => {
        graphCalls.push(["runs.create", threadId, assistantId, payload])
        state.record.graph_run_id = `run_${graphCalls.filter(c => c[0] === "runs.create").length}`
        state.record.phase = "active"
        if (payload.command) { state.interrupts = []; state.runStatus = "running" }
        return { run_id: state.record.graph_run_id }
      },
      get: async (threadId, runId) => ({ thread_id: threadId, run_id: runId, status: state.runStatus,
        metadata: { epoch_sdk_request_id: state.wrongRequest ?? state.record.request_id } }),
    },
  }
  const client = new EpochClient({ backend, graph, pollIntervalMs: 250 })
  return { client, backend, graph, calls, graphCalls, state, finish() {
    state.response = answer(state.record.request, state.record.runtime.thread_id)
    state.record.response_id = state.response.response_id
    state.record.response_version = state.response.version
    state.runStatus = "success"
  } }
}

test("validates the actual task/context/output contract and rejects invalid output definitions", () => {
  assert.deepEqual(requestToWire(parseRequest(request())), request())
  for (const bad of [ { ...request(), task: ["x"] }, { ...request(), context: "x" },
    { ...request(), context: [""] }, { ...request(), outputs: [] },
    { ...request(), outputs: [request().outputs[0], request().outputs[0]] },
    { ...request(), context: null }, { ...request(), auto_ingest: true },
    { ...request(), parameters: { period: { start: "2025-12-31", end: "2024-01-01" } } },
    { ...request(), source_execution_id: "old" },
    { ...request(), outputs: [{ name: "table", type: "table", schema: [{ name: "x", type: "string" }, { name: "x", type: "string" }] }] },
    { ...request(), outputs: [{ name: "data", type: "json", schema: { type: "unknown-type" } }] },
  ]) assert.throws(() => validateRequest(bad))
})

test("does not lose special JSON property keys during native serialization", () => {
  const schema = JSON.parse('{"type":"object","properties":{"__proto__":{"type":"string"},"constructor":{"type":"string"}},"required":["__proto__"],"additionalProperties":false}')
  const value = { ...request(), outputs: [{ name: "data", type: "json", schema }] }
  assert.deepEqual(requestToWire(parseRequest(value)), value)
  assert.equal({}.polluted, undefined)
})

test("validates saved output names, types, schemas, JSON values and response pins", async () => {
  const wire = JSON.parse(await readFile(new URL("../../../contracts/research-response.example.json", import.meta.url), "utf8"))
  const parsed = native.serialization.ResearchResponseRecord.parseOrThrow(wire)
  assert.deepEqual(responseToWire(validateResponse(parsed)), wire)
  const missing = copy(wire); missing.content.outputs.pop()
  assert.throws(() => validateResponse(native.serialization.ResearchResponseRecord.parseOrThrow(missing)))
  const wrongJson = copy(wire); wrongJson.content.outputs.find(x => x.type === "json").value.matches = "one"
  assert.throws(() => validateResponse(native.serialization.ResearchResponseRecord.parseOrThrow(wrongJson)))
  const wrongTable = copy(wire); wrongTable.content.outputs.find(x => x.type === "table").schema[0].name = "different"
  assert.throws(() => validateResponse(native.serialization.ResearchResponseRecord.parseOrThrow(wrongTable)))
})

test("research admission uses native models, durable run options, and one graph run on reattach", async () => {
  const h = harness()
  const first = await h.client.run(request(), { operationId: "run-example", wait: false })
  assert.equal(first.status, "in_progress")
  const created = h.calls.find(c => c.method === "POST").body
  assert.deepEqual(created.request, request())
  assert.equal(created.operation_id, "run-example")
  const run = h.graphCalls.find(c => c[0] === "runs.create")[3]
  assert.equal(run.durability, "sync")
  assert.equal(run.multitaskStrategy, "reject")
  assert.equal(run.onCompletion, "keep")
  assert.equal(run.input.sdk_request_id, h.state.record.request_id)
  await h.client.run(request(), { operationId: "run-example", wait: false })
  assert.equal(h.graphCalls.filter(c => c[0] === "runs.create").length, 1)
  await assert.rejects(h.client.run({ ...request(), task: "Changed" }, { operationId: "run-example", wait: false }), e => e.code === "IDEMPOTENCY_CONFLICT")
  assert.equal(h.graphCalls.filter(c => c[0] === "runs.create").length, 1)
})

test("deterministic thread identities match Python UUIDv5", async () => {
  assert.equal(await researchThreadId("req_11111111111111111111111111111111"), 'e5007dd1-72eb-5070-b662-9a4f50e9d3ee')
})

test("the real LangGraph client sends the accepted launch contract and does not retry failed mutations", async () => {
  const { Client } = await import(pathToFileURL(createRequire(entry).resolve("@langchain/langgraph-sdk")).href)
  const h = harness()
  const sent = []
  let failLaunch = false
  const graph = new Client({ apiUrl: "https://graph.invalid", apiKey: null, callerOptions: { maxRetries: 0,
    fetch: async (input, init) => {
      const path = new URL(input).pathname
      const body = init?.body ? JSON.parse(init.body) : undefined
      sent.push({ path, method: init?.method ?? "GET", body })
      if (path === "/threads") return Response.json({ thread_id: body.thread_id })
      if (path.endsWith("/runs")) {
        if (failLaunch) return Response.json({ message: "Temporarily unavailable" }, { status: 503 })
        h.state.record.graph_run_id = "native-run"
        return Response.json({ run_id: "native-run", thread_id: h.state.record.runtime.thread_id, status: "running" })
      }
      if (path.endsWith("/runs/native-run")) return Response.json({ status: "interrupted", metadata: { epoch_sdk_request_id: h.state.record.request_id } })
      if (path.endsWith("/history")) return Response.json([{ values: { authority_turn_id: `user-turn:${h.state.record.request_id}` }, interrupts: [question()] }])
      throw new Error(`Unexpected graph path ${path}`)
    },
  } })
  h.client.graph = graph
  const waiting = await h.client.run(request(), { operationId: "run-example", wait: false })
  assert.equal(waiting.status, "needs_input")
  const body = sent.find(c => c.path.endsWith("/runs")).body
  assert.equal(body.assistant_id, "epoch-ai")
  assert.equal(body.multitask_strategy, "reject")
  assert.equal(body.on_completion, "keep")
  assert.equal(body.durability, "sync")
  assert.equal(body.stream_resumable, true)
  assert.deepEqual(sent.find(c => c.path.endsWith("/history")).body.metadata,
    { epoch_sdk_request_id: h.state.record.request_id, epoch_sdk_run_id: "native-run" })
  failLaunch = true
  const before = sent.filter(c => c.path.endsWith("/runs")).length
  await assert.rejects(h.client.resume(waiting, { interrupt_1: { answers: [{ question_index: 0, selected_indices: [0] }] } }, { wait: false }))
  assert.equal(sent.filter(c => c.path.endsWith("/runs")).length, before + 1)
})

test("status observes the exact operation checkpoint and rejects another run's metadata", async () => {
  const h = harness(); await h.client.run(request(), { operationId: "run-example", wait: false })
  h.state.runStatus = "interrupted"; h.state.interrupts = [question()]
  const result = await h.client.status("run-example")
  assert.equal(result.status, "needs_input")
  const history = h.graphCalls.find(c => c[0] === "history")
  assert.deepEqual(history[2].metadata, { epoch_sdk_request_id: h.state.record.request_id, epoch_sdk_run_id: "run_1" })
  assert.equal(h.graphCalls.filter(c => c[0] === "runs.create").length, 1)
  h.state.wrongRequest = "another"
  await assert.rejects(h.client.status("run-example"), /another request/)
})

test("resume validates every current question and sends only the native reply command", async () => {
  const h = harness(); await h.client.run(request(), { operationId: "run-example", wait: false })
  h.state.runStatus = "interrupted"; h.state.interrupts = [question()]
  const waiting = await h.client.status("run-example")
  await assert.rejects(h.client.resume(waiting, {}, { wait: false }), /current interrupt/)
  await assert.rejects(h.client.resume(waiting, { interrupt_1: { answers: [{ question_index: 0, selected_indices: [9] }] } }, { wait: false }), /invalid option/)
  const responses = { interrupt_1: { answers: [{ question_index: 0, selected_indices: [0] }] } }
  await h.client.resume(waiting, responses, { wait: false })
  const run = h.graphCalls.filter(c => c[0] === "runs.create").at(-1)[3]
  assert.equal(run.input, undefined)
  assert.deepEqual(run.command, { resume: responses })
  assert.equal(run.metadata.epoch_sdk_request_id, h.state.record.request_id)
})

test("stale replies cannot resume a different question and completed work cannot be resumed twice", async () => {
  const h = harness(); await h.client.run(request(), { operationId: "run-example", wait: false })
  h.state.runStatus = "interrupted"; h.state.interrupts = [question()]
  const waiting = await h.client.status("run-example")
  h.state.interrupts[0].value.questions[0].question = "A changed question"
  await assert.rejects(h.client.resume(waiting, {}, { wait: false }), e => e.code === "STALE_QUESTION")
  h.finish()
  const result = await h.client.resume(waiting, {}, { wait: false })
  assert.equal(result.status, "succeeded")
  assert.equal(h.graphCalls.filter(c => c[0] === "runs.create").length, 1)
})

test("completion reads the pinned response and rejects mismatched output declarations", async () => {
  const h = harness(); await h.client.run(request(), { operationId: "run-example", wait: false }); h.finish()
  const result = await h.client.status("run-example")
  assert.equal(result.response.version, 1)
  assert.equal(h.calls.at(-1).query.version, "1")
  h.state.response.content.declarations[0].instructions = "Different instructions"
  await assert.rejects(h.client.status("run-example"), /declarations differ/)
})

test("a published checkpoint is adopted once without another graph run", async () => {
  const h = harness(); await h.client.run(request(), { operationId: "run-example", wait: false })
  h.state.response = answer(h.state.record.request, h.state.record.runtime.thread_id)
  h.state.published = { response_id: h.state.response.response_id, request_id: h.state.response.request_id,
    thread_id: h.state.response.thread_id, version: 1 }
  h.state.runStatus = "success"
  const result = await h.client.status("run-example")
  assert.equal(result.status, "succeeded")
  assert.equal(h.state.record.response_version, 1)
  assert.equal(h.graphCalls.filter(c => c[0] === "runs.create").length, 1)
})

test("read rejects a different response identity or revision without mutation", async () => {
  const h = harness(); h.state.response = answer(request(), "thread")
  await assert.rejects(h.client.read("another", { version: 1 }), /another saved answer/)
  await assert.rejects(h.client.read("example_response", { version: 2 }), /another saved answer/)
  assert.ok(h.calls.every(c => c.method === "GET"))
})

test("aborting observation never cancels or resubmits admitted work", async () => {
  const h = harness(); const controller = new AbortController()
  await assert.rejects(h.client.run(request(), { operationId: "run-example", signal: controller.signal,
    onStatus: () => controller.abort() }), e => e.name === "AbortError")
  assert.equal(h.graphCalls.filter(c => c[0] === "runs.create").length, 1)
  assert.equal(h.state.runStatus, "running")
})

test("prepared execution keeps captured options and waits for required output publication", async () => {
  const h = harness()
  h.state.execution = { request_id: "execute-request", created_at_ms: 0, phase: "accepted", execution_id: "execution-1",
    request: { operation_id: "execute-example", study_id: "study-1", source_execution_id: "source-1",
      parameters: { period: { start: "2025-01-01", end: "2025-12-31" }, execution: { cash: 50000, currency: "USD" } } } }
  h.state.job = { id: "execution-1", definition_id: "study-1", created_at: 0, execution_type: "research", status: "running" }
  await h.client.execute({ studyId: "study-1", sourceExecutionId: "source-1" }, { operationId: "execute-example", period: { start: "2025-01-01", end: "2025-12-31" }, wait: false })
  const created = h.calls.find(c => c.path === "/api/v1/integration/execution-requests" && c.method === "POST")
  assert.equal(created.body.parameters.execution.cash, 50000)
  const beforeRead = h.calls.length
  const accepted = await h.client.readExecutionRequest("execute-example")
  assert.equal(accepted.reference.sourceExecutionId, "source-1")
  assert.equal(accepted.parameters.execution.cash, 50000)
  assert.ok(h.calls.slice(beforeRead).every(c => c.method === "GET"))
  h.state.job.status = "completed"; h.state.execution.execution_status = "Completed"; h.state.execution.response_phase = "active"
  assert.equal((await h.client.status("execute-example", { kind: "execute" })).status, "in_progress")
  h.state.execution.response_phase = "failed"
  await assert.rejects(h.client.status("execute-example", { kind: "execute" }), e => e.code === "OUTPUT_VALIDATION_FAILED")
})
