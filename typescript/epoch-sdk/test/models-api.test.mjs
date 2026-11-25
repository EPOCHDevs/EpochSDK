// Platform saved-model mock HTTP checks; not live lifecycle acceptance.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import { EpochModelsClient } from '@epochdevs/epoch-sdk/models-api';

const fixture = name => JSON.parse(readFileSync(new URL(`../../../contracts/fixtures/platform-models/${name}.json`, import.meta.url), 'utf8'));
const summary = fixture('summary');
const facts = fixture('facts');
const wire = fixture('save');
const request = { requestId: wire.request_id, name: wire.name, executionId: wire.execution_id,
  fitName: wire.fit_name, expectedDigest: wire.expected_digest };

async function withFetch(reply, scenario) {
  const previous = globalThis.fetch;
  const seen = [];
  globalThis.fetch = async (url, init) => {
    seen.push({ url: String(url), init });
    const [status, body] = reply(String(url), init);
    return new Response(JSON.stringify(body), { status, headers: { 'content-type': 'application/json' } });
  };
  try { await scenario(seen); } finally { globalThis.fetch = previous; }
}
const client = () => new EpochModelsClient({ environment: 'https://platform.test', token: 'fixture-token' });

test('model Save/list/read carry exact pins through Platform routes', () => withFetch((url, init) => {
  const parsed = new URL(url);
  assert.equal(init.headers.Authorization, 'Bearer fixture-token');
  if (init.method === 'POST') {
    assert.equal(parsed.pathname, '/api/v1/models');
    assert.deepEqual(JSON.parse(init.body), wire);
    return [200, summary];
  }
  if (parsed.pathname === '/api/v1/models') {
    assert.equal(parsed.searchParams.get('limit'), '1');
    assert.equal(parsed.searchParams.get('cursor'), 'owner-bound-cursor');
    return [200, { items: [summary], next_cursor: 'next' }];
  }
  assert.equal(parsed.pathname, `/api/v1/models/${summary.model_ref}`);
  return [200, facts];
}, async seen => {
  const models = client();
  const saved = await models.saveModel(request, { maxRetries: 0 });
  const page = await models.listModels({ limit: 1, cursor: 'owner-bound-cursor' }, { maxRetries: 0 });
  const detail = await models.readModel(saved.modelRef, {}, { maxRetries: 0 });
  assert.equal(page.items[0].digest, saved.digest);
  assert.equal(page.nextCursor, 'next');
  assert.equal(detail.model.manifestSha256, saved.manifestSha256);
  assert.deepEqual(detail.binding, facts.binding);
  assert.deepEqual(detail.producer, facts.producer);
  assert.equal(seen.length, 3);
}));

test('outbound Save rejects unexpected fields before HTTP', () => withFetch(() => {
  assert.fail('Invalid request must not reach HTTP');
}, async () => {
  await assert.rejects(client().saveModel({ ...request, unexpected: true }, { maxRetries: 0 }));
  await assert.rejects(client().saveModel({ ...request, expectedDigest: 'latest' }, { maxRetries: 0 }));
  await assert.rejects(client().saveModel({ ...request, name: '' }, { maxRetries: 0 }));
}));

test('unavailable model storage retains its typed error', () => withFetch(() => [503, {
  error: 'ServiceUnavailable', message: 'Pinned model object is unavailable', timestamp: '2026-11-25T00:00:00Z',
}], async () => {
  await assert.rejects(client().readModel(summary.model_ref, {}, { maxRetries: 0 }), error => {
    assert.equal(error.statusCode, 503);
    assert.equal(error.body.message, 'Pinned model object is unavailable');
    return true;
  });
}));
