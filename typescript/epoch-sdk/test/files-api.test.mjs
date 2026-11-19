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

test('a download that fails keeps its typed JSON error body', () =>
  withFetch(() => [404, { error: 'NotFound', message: 'No such dataset', timestamp: '2026-11-19T00:00:00Z' }], async () => {
    await assert.rejects(client().userFiles.downloadPreparedDataset(ref('dataset'), {}, { maxRetries: 0 }), (error) => {
      assert.equal(error.statusCode, 404);
      assert.equal(error.body.error, 'NotFound');
      return true;
    });
  }));

test('an app can wrap the generated fetcher, as it does for its other API clients', async () => {
  const { fetcher } = await import('@epochdevs/epoch-sdk/files-api/core/fetcher');
  const seen = [];
  const files = new EpochFilesClient({
    environment: 'https://platform.test', token: 'unused',
    // The app sets its own bearer and turns retries off, as the Portal does for StratifyX.
    fetcher: (args) => { seen.push(args); return fetcher({ ...args, headers: { ...args.headers, Authorization: 'Bearer app' }, maxRetries: 0 }); },
  });
  await withFetch(() => [200, { items: [], next_cursor: null }], async (requests) => {
    await files.userFiles.listSavedDatasets({ limit: 1 });
    assert.equal(seen.length, 1);
    assert.equal(requests[0].init.headers.Authorization, 'Bearer app');
  });
});
