import assert from 'node:assert/strict'
import test from 'node:test'
import { readFile } from 'node:fs/promises'
import { IdentityClient, IdentityHTTPError, parseAssetInformation, parseAssetLogos } from '../identity.js'

const fixtures = new URL('../../../contracts/fixtures/native-identity/', import.meta.url)
test('Platform-owned models preserve native metadata states without a native SDK import', async () => {
  for (const [name, value] of [['adr-false.json', false], ['adr-true.json', true], ['adr-absent.json', undefined]]) {
    const wire = JSON.parse(await readFile(new URL(name, fixtures), 'utf8'))
    const asset = parseAssetInformation(wire)
    assert.equal(asset.stockProfile.isAdr, value)
    assert.equal(asset.minTick, 0.01)
    assert.deepEqual(asset.nameAliases, [])
    assert.equal(asset.assetClass, 'Stocks')
    assert.throws(() => parseAssetInformation({ ...wire, unexpected: true }))
  }
})

test('identity requests preserve anonymous access and validate pinned listing responses', async () => {
  const calls = []
  const client = new IdentityClient({ baseUrl: 'https://api.example', fetch: async (url, options) => {
    calls.push({ url: String(url), options })
    return Response.json({ kind: 'single', asset_id: 'OLD-Stocks', image: { identity: 'asset:OLD-Stocks', state: 'unverified', image_id: 'a'.repeat(64), url: '/api/v1/images/' + 'a'.repeat(64) } })
  } })
  const result = await client.getAssetLogos('OLD-Stocks', { listingCatalogue: 'b'.repeat(64), listingSelectedAt: '2026-11-17T00:00:00Z' })
  assert.equal(result.assetId, 'OLD-Stocks'); assert.equal(result.image.imageId, 'a'.repeat(64))
  assert(calls[0].url.includes('listing_catalogue=' + 'b'.repeat(64)))
  assert(calls[0].url.includes('listing_selected_at=2026-11-17T00%3A00%3A00Z'))
  assert.equal(calls[0].options.headers.Authorization, undefined)
  assert.equal(calls[0].options.redirect, 'error')
  await assert.rejects(client.getAssetLogos('OTHER-Stocks'))
  assert.throws(() => parseAssetLogos({ kind: 'single', asset_id: 'OLD-Stocks', image: { state: 'available' } }))
})

test('caller tokens are resolved per request and batch identities cannot change', async () => {
  let token = 'one'; const sent = []
  const client = new IdentityClient({ baseUrl: 'https://api.example', token: () => token, fetch: async (_url, options) => {
    sent.push(options.headers.Authorization)
    const { asset_ids } = JSON.parse(options.body)
    return Response.json({ items: [...new Set(asset_ids)].map(asset_id => ({ asset_id, reason: 'unknown_asset' })) })
  } })
  assert.equal((await client.resolveAssetInformation(['MISSING-Stocks', 'MISSING-Stocks'])).items.length, 1)
  token = 'two'; await client.resolveAssetInformation(['MISSING-Stocks'])
  assert.deepEqual(sent, ['Bearer one', 'Bearer two'])
  const bad = new IdentityClient({ baseUrl: 'https://api.example', fetch: async () => Response.json({ items: [{ asset_id: 'OTHER-Stocks' }] }) })
  await assert.rejects(bad.resolveAssetInformation(['MISSING-Stocks']), /different asset/)
})

test('exact metadata cannot be replaced by a different asset', async () => {
  const client = new IdentityClient({ baseUrl: 'https://api.example', fetch: async () => Response.json({ id: 'OTHER-Stocks', name_aliases: [], symbol_changes: [] }) })
  await assert.rejects(client.getAssetInformation('AAPL-Stocks'), /another asset/)
  assert.equal((await client.getAssetInformation('OTHER-Stocks')).id, 'OTHER-Stocks')
})

test('errors, oversized content and cancellation do not trigger retry or fallback', async () => {
  let calls = 0
  const client = new IdentityClient({ baseUrl: 'https://api.example', fetch: async () => { calls++; return new Response('{}', { status: 503 }) } })
  await assert.rejects(client.getCountryCatalog(), error => error instanceof IdentityHTTPError && error.status === 503)
  assert.equal(calls, 1)
  const signal = AbortSignal.abort()
  await assert.rejects(client.getCountryCatalog({ signal })); assert.equal(calls, 1)
  const large = new IdentityClient({ baseUrl: 'https://api.example', fetch: async () => new Response('{}', { headers: { 'Content-Length': String(9 * 1024 * 1024) } }) })
  await assert.rejects(large.getCountryCatalog(), /exceeds bound/)
})
