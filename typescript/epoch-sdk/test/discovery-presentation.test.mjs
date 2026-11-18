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

test('retained metadata preserves optional provider coverage without changing availability', () => {
  for (const coverage of [undefined, { status: 'unknown', discontinued: false }, { status: 'unavailable', discontinued: true }]) {
    const wire = {
      record_ref: `discovery-record:v1:${'a'.repeat(64)}`, request_id: 'saved', request_item_id: 'item',
      status: 'resolved', availability: 'unknown', coverage_basis: 'unknown', qualifications: [],
      identity: { kind: 'te_indicator', country: 'United States', indicator: 'GDP' },
      metadata: {
        data_source_id: 'TradingEconomics:United States:GDP', vendor: 'trading_economics',
        queried_at: '2026-11-17T00:00:00Z', provider_endpoint: 'historical', feedable: false,
        ...(coverage === undefined ? {} : { provider_coverage: coverage }),
      },
    }
    const decoded = parse('DiscoveryMetadataRecord', wire)
    assert.equal(decoded.availability, 'unknown')
    assert.equal(decoded.metadata.feedable, false)
    assert.deepEqual(decoded.metadata.providerCoverage, coverage)
    assert.deepEqual(serialize('DiscoveryMetadataRecord', decoded), wire)
    assert.throws(() => parse('DiscoveryMetadataRecord', {
      ...wire, metadata: { ...wire.metadata, provider_coverage: { status: 'unknown', invented: true } },
    }))
  }
})
