// The Files and Space client generated from Platform's contract (ENG-2819).
// Mock HTTP checks; they do not claim live service acceptance.
import assert from 'node:assert/strict';
import test from 'node:test';
import { EpochFilesClient } from '@epochdevs/epoch-sdk/files-api';

import { readFileSync } from 'node:fs';

const ref = (prefix) => `${prefix}:${'a'.repeat(64)}`;
const saved = JSON.parse(readFileSync(new URL('../../../contracts/fixtures/platform-files/saved_dataset.json', import.meta.url), 'utf8'));

function withFetch(reply, scenario) {
  const original = globalThis.fetch;
  const seen = [];
  globalThis.fetch = async (url, init) => {
    seen.push({ url: String(url), init });
    const [status, body] = reply(String(url), init);
    return new Response(JSON.stringify(body), { status, headers: { 'content-type': 'application/json' } });
  };
  return scenario(seen).finally(() => { globalThis.fetch = original; });
}

const client = () => new EpochFilesClient({ environment: 'https://platform.test', token: 'token' });

test('the saved-dataset list keeps its StratifyX method name and keeps fields Platform adds later', () =>
  withFetch(() => [200, { items: [saved], next_cursor: 'next', added_later: true }], async (seen) => {
    const page = await client().userFiles.listSavedDatasets({ limit: 1 }, { maxRetries: 0 });
    assert.equal(page.items[0].datasetRef, saved.dataset_ref);
    assert.equal(page.nextCursor, 'next');
    // A field this client doesn't know yet passes through instead of failing the read.
    assert.equal(page.added_later, true);
    assert.equal(new URL(seen[0].url).pathname, '/api/v1/files/datasets');
    assert.equal(new URL(seen[0].url).searchParams.get('limit'), '1');
  }));

test('an import carries the person\'s sort choice as sort_by', () =>
  withFetch(() => [400, { error: 'BadRequest', message: 'stop', timestamp: '2026-11-19T00:00:00Z' }], async (seen) => {
    await assert.rejects(client().userFiles.prepareStructuredImport({
      fileRef: ref('file'), requestId: 'r', name: 'Prices',
      options: { format: 'csv', delimiter: ',', header: true, nullValues: [''], columns: [], sortBy: ['date'] },
    }, { maxRetries: 0 }));
    assert.deepEqual(JSON.parse(seen[0].init.body).options.sort_by, ['date']);
  }));
