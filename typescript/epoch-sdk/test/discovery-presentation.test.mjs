import assert from 'node:assert/strict'
import test from 'node:test'
import { parseDiscoveryPresentation as parse, serializeDiscoveryPresentation as serialize } from '../discovery-presentation.js'

test('historical requests round-trip without exposing a search operation', () => {
  const wire = { requests: [{ request_id: 'saved-request', subjects: [{ kind: 'symbol', symbol: 'AAPL', asset_type: 'Stocks' }], datasets: [] }] }
  const parsed = parse('DatasetSearchRequest', wire)
  assert.equal(parsed.requests[0].requestId, 'saved-request')
  assert.equal(parsed.requests[0].subjects[0].assetType, 'Stocks')
  assert.deepEqual(serialize('DatasetSearchRequest', parsed), wire)
  assert.throws(() => parse('DatasetSearchRequest', { ...wire, extra: true }))
  assert.throws(() => parse('search', wire))
})

test('published directories keep map keys literal and ignore inherited constructor members', () => {
  const wire = { registry_version: 'registry:sha', loader_registry_version: 'loader:sha', overview: '', sources: [], summaries: null }
  const decoded = parse('DatasetCatalogResponse', wire)
  assert.equal(decoded.registryVersion, 'registry:sha')
  assert.equal(decoded.summaries, null)
  assert.deepEqual(serialize('DatasetCatalogResponse', decoded), wire)
  assert.equal(Object.hasOwn(decoded, 'constructor'), false)
})
