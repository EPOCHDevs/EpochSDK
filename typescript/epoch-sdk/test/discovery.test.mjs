import test from 'node:test'
import assert from 'node:assert/strict'
import { CatalogueClient, CatalogueHTTPError } from '../discovery.js'
const empty = { format: 'epoch-search-v4', session_id: 'search:test', needs: [], candidates: [], saved: [], omitted: 0 }
test('caller-scoped discovery uses Platform and refreshes credentials for each request', async () => {
  let tokens = 0; const sent = []
  const client = new CatalogueClient({ baseUrl: 'https://platform.invalid', token: async () => 'token' + ++tokens, fetch: async (url, options) => { sent.push({ url, options }); return Response.json(empty) } })
  const input = { requests: [{ id: 'one', query: 'France electricity', mode: 'discover' }] }
  assert.deepEqual(await client.search(input), empty); await client.search(input)
  assert.equal(sent[0].url.pathname, '/api/v1/discovery/datasets/search')
  assert.equal(sent[0].options.headers.Authorization, 'Bearer token1'); assert.equal(sent[1].options.headers.Authorization, 'Bearer token2')
  assert.equal(sent[0].options.redirect, 'error')
  assert.throws(() => client.search({ ...input, invented: true }), /Invalid/)
})
test('bounds and errors remain explicit without a second request', async () => {
  assert.throws(() => new CatalogueClient({ baseUrl: 'http://outside.invalid', token: 'x' }), /HTTPS/)
  let sent = 0
  const client = new CatalogueClient({ baseUrl: 'https://platform.invalid', token: 'x', fetch: async () => { sent++; return new Response('x'.repeat(40001)) } })
  await assert.rejects(client.search({ requests: [], saved_query: 'owned' }), /exceeds/); assert.equal(sent, 1)
  const failed = new CatalogueClient({ baseUrl: 'https://platform.invalid', token: 'x', fetch: async () => Response.json({ message: 'Unavailable' }, { status: 503 }) })
  await assert.rejects(failed.search({ requests: [], saved_query: 'owned' }), CatalogueHTTPError)
})
test('scope conflicts remain incomplete with exact catalogue facts and no candidates', async () => {
  const issue = { code: 'filter_conflict', field: 'exchanges', requested: ['CME'], available: ['GBLX'], source_ids: ['ES-Futures'] }
  const body = { ...empty, needs: [{ id: 'es', status: 'incomplete', candidates: [], next_cursor: null, completeness: 'complete', scope_issues: [issue] }] }
  const client = new CatalogueClient({ baseUrl: 'https://platform.invalid', token: 'x', fetch: async () => Response.json(body) })
  assert.deepEqual((await client.search({ requests: [{ id: 'es', query: 'ES', mode: 'exact' }] })).needs[0].scope_issues, [issue])
})
test('requested populations preserve exact per-need links without new GDS filters or coverage claims', async () => {
  for (const population of [{ kind: 'assets', asset_ids: ['asset-a', 'asset-b'] }, { kind: 'universe', universe_ref: 'universe:' + 'a'.repeat(64) }]) {
    const body = { ...empty, needs: [{ id: 'prices', population, status: 'no_match', candidates: [], next_cursor: null, completeness: 'complete' }] }
    const client = new CatalogueClient({ baseUrl: 'https://platform.invalid', token: 'owner', fetch: async (_url, options) => {
      assert.deepEqual(JSON.parse(options.body).requests[0].population, population)
      return Response.json(body)
    } })
    assert.deepEqual(await client.search({ requests: [{ id: 'prices', query: 'Prices', mode: 'exact', population }] }), body)
  }
})
test('malformed requested populations fail before transport', () => {
  let sent = 0
  const client = new CatalogueClient({ baseUrl: 'https://platform.invalid', token: 'owner', fetch: async () => { sent++; return Response.json(empty) } })
  for (const population of [{ kind: 'assets', asset_ids: [] }, { kind: 'assets', asset_ids: ['a', 'a'] },
    { kind: 'assets', asset_ids: ['a'], invented: true }, { asset_ids: ['a'] }, { kind: 'universe', universe_ref: 'invalid' }])
    assert.throws(() => client.search({ requests: [{ id: 'one', query: 'Prices', mode: 'exact', population }] }), /Invalid/)
  assert.equal(sent, 0)
})
