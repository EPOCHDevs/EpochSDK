import assert from 'node:assert/strict'
import test from 'node:test'
import { ResearchOperationsClient } from '../research-operations.js'
import { parseRequest } from '../contract.js'
const request = { task: 'Explain', outputs: [{ name: 'answer', type: 'text', instructions: 'Explain' }] }
const record = { request_id: 'req_' + 'a'.repeat(32), version: 0, created_at_ms: 1, updated_at_ms: 1,
  phase: 'accepted', interaction: 'one_shot', request }

test('research lifecycle targets Platform and renews one owner credential per request', async () => {
  let calls = 0, tokens = 0
  const client = new ResearchOperationsClient({ baseUrl: 'https://platform.invalid', token: async () => 'token-' + ++tokens,
    fetch: async (url, options) => {
      assert.equal(new URL(url).origin, 'https://platform.invalid'); assert.equal(options.redirect, 'error')
      assert.equal(options.headers.Authorization, 'Bearer token-' + ++calls)
      return new Response(JSON.stringify(record), { status: 200 })
    } })
  const admitted = await client.createSdkRequest({ request: parseRequest(request) })
  assert.equal(admitted.interaction, 'one_shot')
  await client.getSdkRequest(admitted.requestId)
  assert.equal(calls, 2); assert.equal(tokens, 2)
})

test('unrepresentable accepted integers are refused rather than rounded', async () => {
  const raw = JSON.stringify(record).replace('"task":"Explain"', '"parameters":{"execution":{"cash":9007199254740993}},"task":"Explain"')
  const client = new ResearchOperationsClient({ baseUrl: 'https://platform.invalid', fetch: async () => new Response(raw, { status: 200 }) })
  await assert.rejects(client.getSdkRequest(record.request_id), /cannot represent this exact research integer/)
})

test('failed lifecycle writes are sent once', async () => {
  let calls = 0
  const client = new ResearchOperationsClient({ baseUrl: 'https://platform.invalid', fetch: async () => { calls++; return new Response('{}', { status: 503 }) } })
  await assert.rejects(client.createSdkRequest({ request: parseRequest(request) }), error => error.statusCode === 503)
  assert.equal(calls, 1)
})
