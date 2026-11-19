// Generated Platform sharing client. HTTP stand-ins; live acceptance is separate.
import assert from 'node:assert/strict';
import test from 'node:test';
import { readFileSync } from 'node:fs';
import { EpochSharesClient, serialization } from '@epochdevs/epoch-sdk/shares-api';

const fixture = name => JSON.parse(readFileSync(new URL(`../../../contracts/fixtures/platform-shares/${name}.json`, import.meta.url), 'utf8'));
const options = { maxRetries: 0 };
function withFetch(reply, scenario) {
  const original = globalThis.fetch, seen = [];
  globalThis.fetch = async (url, init) => {
    seen.push({ url: String(url), init });
    const [status, body] = reply(String(url), init);
    return new Response(JSON.stringify(body), { status, headers: { 'content-type': 'application/json' } });
  };
  return scenario(seen).finally(() => { globalThis.fetch = original; });
}
const client = () => new EpochSharesClient({ environment: 'https://platform.test', token: 'fixture-token' });

test('changes access on the same encoded link and preserves version zero', () =>
  withFetch(() => [200, { ...fixture('summary'), access_version: 1, added_later: true }], async seen => {
    const share = await client().studiesShares.changeWhoCanOpenAShareLink('share 1', {
      audience: 'named_subjects', subjects: ['reader@example.test'], expectedAccessVersion: 0,
    }, options);
    assert.equal(share.accessVersion, 1);
    assert.equal(share.added_later, true);
    assert.equal(seen[0].url, 'https://platform.test/api/v1/studies/shares/share%201');
    assert.equal(seen[0].init.method, 'PATCH');
    assert.deepEqual(JSON.parse(seen[0].init.body), fixture('access'));
    assert.equal(seen[0].init.headers.Authorization, 'Bearer fixture-token');
  }));

test('lists available and explicitly unavailable versions, with usable boolean tags', () =>
  withFetch(() => [200, fixture('versions')], async seen => {
    const page = await client().studiesShares.listPublishedShareVersions('share 1', {}, options);
    assert.equal(seen[0].url, 'https://platform.test/api/v1/studies/shares/share%201/versions');
    assert.deepEqual(page.versions.map(v => [v.available, v.snapshotVersion, v.isCurrent]), [[true, 2, true], [false, 1, false]]);
    assert.equal(page.versions[0].messageCount, 9);
    assert.equal(page.versions[0].runCount, 2);
    assert.equal(page.versions[1].reason, 'legacy_missing');
    assert.throws(() => serialization.ShareVersionsResponse.parseOrThrow({ versions: [{ ...fixture('versions').versions[0], available: false }] }));
  }));

test('selects an older version with the explicit current-version compare-and-set', () =>
  withFetch(() => [200, { ...fixture('summary'), snapshot_version: 1 }], async seen => {
    const share = await client().studiesShares.selectPublishedShareVersion('share 1', {
      snapshotVersion: 1, expectedCurrentVersion: 3,
    }, options);
    assert.equal(share.snapshotVersion, 1);
    assert.equal(seen[0].url, 'https://platform.test/api/v1/studies/shares/share%201/current-version');
    assert.equal(seen[0].init.method, 'PUT');
    assert.deepEqual(JSON.parse(seen[0].init.body), fixture('selection'));
  }));

test('received shares use the static endpoint and return the five approved metadata fields', () =>
  withFetch(() => [200, fixture('received')], async seen => {
    const page = await client().studiesShares.listReceivedThreadShares(options);
    assert.equal(seen[0].url, 'https://platform.test/api/v1/studies/shares/received');
    assert.deepEqual(Object.keys(page.shares[0]).sort(), ['shareId', 'threadTitle', 'ownerDisplayName', 'snapshotVersion', 'frozenAtMs'].sort());
    assert.equal(page.shares[0].threadTitle, 'Synthetic conversation');
  }));

for (const operation of ['access', 'selection']) {
  test(`${operation} conflicts retain the typed 409 body without automatic mutation retries`, () =>
    withFetch(() => [409, { error: 'Conflict', message: 'Changed in another window.', timestamp: '2026-11-19T00:00:00Z' }], async seen => {
      const shares = client().studiesShares;
      await assert.rejects(operation === 'access'
        ? shares.changeWhoCanOpenAShareLink('share-1', { expectedAccessVersion: 0, audience: 'named_subjects', subjects: ['reader@example.test'] }, options)
        : shares.selectPublishedShareVersion('share-1', { snapshotVersion: 1, expectedCurrentVersion: 3 }, options), error => {
        assert.equal(error.statusCode, 409);
        assert.equal(error.body.message, 'Changed in another window.');
        return true;
      });
      assert.equal(seen.length, 1);
    }));
}

test('invalid or incomplete compare-and-set requests fail before HTTP', () =>
  withFetch(() => [400, {}], async seen => {
    const shares = client().studiesShares;
    for (const request of [{}, { expectedAccessVersion: -1 }, { expectedAccessVersion: true }, { expectedAccessVersion: 0, audience: 'other' }, { expectedAccessVersion: 0, surprise: true }])
      await assert.rejects(shares.changeWhoCanOpenAShareLink('share-1', request, options));
    for (const request of [{ snapshotVersion: 1 }, { snapshotVersion: 0, expectedCurrentVersion: 2 }, { snapshotVersion: 1.5, expectedCurrentVersion: 2 }])
      await assert.rejects(shares.selectPublishedShareVersion('share-1', request, options));
    assert.equal(seen.length, 0, 'Invalid input must be refused before HTTP');
  }));

test('an application can reuse the generated fetcher with its existing authentication handling', async () => {
  const { fetcher } = await import('@epochdevs/epoch-sdk/shares-api/core/fetcher');
  assert.equal(typeof fetcher, 'function');
});
