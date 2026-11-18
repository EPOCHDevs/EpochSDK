import Ajv from 'ajv'
import schema from './discovery.schema.json' with { type: 'json' }
const ajv = new Ajv({ strict: true })
const validate = name => ajv.compile({ $ref: '#/definitions/' + name, definitions: schema.definitions })
const requestSchema = validate('DiscoveryInput')
const responseSchema = validate('DiscoveryResult')
const selectedSchema = validate('SelectedInputs')
const detailsSchema = validate('DiscoveryDetails')
const screenRequestSchema = validate('ScreenInput')
const screenResponseSchema = validate('AssetUniverseResult')
const universeRequestSchema = validate('UniversePageRequest')
const universeResponseSchema = validate('UniversePage')
const assetLookupSchema = validate('AssetLookupResult')
const universeBindingSchema = validate('UniverseBinding')

export class CatalogueHTTPError extends Error {
  constructor(status, body) { super(`Catalogue HTTP ${status}: ${body}`); this.name = 'CatalogueHTTPError'; this.status = status; this.body = body }
}

/** Caller-scoped Platform discovery. It never sends a query to native Backend. */
export class CatalogueClient {
  #origin
  #token
  #fetch
  constructor({ baseUrl, token, fetch: transport = globalThis.fetch }) {
    const origin = new URL(baseUrl)
    if (origin.protocol !== 'https:' && !(origin.protocol === 'http:' && ['127.0.0.1', 'localhost', '[::1]'].includes(origin.hostname))) throw new TypeError('Catalogue origin must use HTTPS or loopback')
    if (origin.pathname !== '/' || origin.search || origin.hash || origin.username || origin.password) throw new TypeError('Invalid catalogue origin')
    if (typeof token !== 'string' && typeof token !== 'function') throw new TypeError('A caller token or token provider is required')
    this.#origin = origin; this.#token = token
    this.#fetch = transport === globalThis.fetch ? transport.bind(globalThis) : transport
  }
  async #request(path, body, bound, check, signal, method = 'POST') {
    const token = typeof this.#token === 'function' ? await this.#token() : this.#token
    if (typeof token !== 'string' || !token || /\s/.test(token)) throw new TypeError('Invalid caller token')
    const deadline = AbortSignal.timeout(35000)
    const response = await this.#fetch(new URL(path, this.#origin), { method, redirect: 'error', headers: { Authorization: 'Bearer ' + token, 'Content-Type': 'application/json' }, ...(body === undefined ? {} : { body: JSON.stringify(body) }), signal: signal ? AbortSignal.any([signal, deadline]) : deadline })
    const chunks = []; let bytes = 0
    const reader = response.body?.getReader()
    if (reader) try { for (;;) { const part = await reader.read(); if (part.done) break; bytes += part.value.byteLength; if (bytes > bound) throw new RangeError('Catalogue response exceeds bound'); chunks.push(part.value) } } finally { await reader.cancel() }
    const content = new Uint8Array(bytes); let offset = 0
    for (const chunk of chunks) { content.set(chunk, offset); offset += chunk.byteLength }
    const text = new TextDecoder().decode(content)
    if (!response.ok) throw new CatalogueHTTPError(response.status, text)
    const value = JSON.parse(text)
    if (!check(value)) throw new TypeError('Invalid Platform discovery response')
    return value
  }
  search(input, { signal } = {}) {
    if (!requestSchema(input) || input.requests.length > 32 || !input.requests.length && !input.saved_query || !Number.isInteger(input.limit ?? 5) || (input.limit ?? 5) < 1 || (input.limit ?? 5) > 25 || !Number.isInteger(input.budget ?? 40000) || (input.budget ?? 40000) < 1024 || (input.budget ?? 40000) > 40000) throw new TypeError('Invalid Platform discovery request')
    return this.#request('/api/v1/discovery/datasets/search', input, input.budget ?? 40000, responseSchema, signal)
  }
  select(sessionId, ids, { signal } = {}) {
    if (!ids.length || ids.length > 32 || new Set(ids).size !== ids.length) throw new TypeError('Select 1..32 distinct candidates')
    return this.#request('/api/v1/discovery/selections', { session_id: sessionId, ids }, 16 * 1024 * 1024, selectedSchema, signal)
  }
  details(sessionId, ids, { signal } = {}) {
    if (!ids.length || ids.length > 10 || new Set(ids).size !== ids.length) throw new TypeError('Read 1..10 distinct source details')
    return this.#request('/api/v1/discovery/datasets/details', { session_id: sessionId, ids }, 1024 * 1024, detailsSchema, signal)
  }
  selection(id, { signal } = {}) { return this.#request('/api/v1/discovery/selections/' + encodeURIComponent(id), undefined, 16 * 1024 * 1024, selectedSchema, signal, 'GET') }
  screen(input, { signal } = {}) {
    if (!screenRequestSchema(input)) throw new TypeError('Invalid asset screen')
    return this.#request('/api/v1/discovery/assets/screen', input, 40000, screenResponseSchema, signal)
  }
  universePage(input, { signal } = {}) {
    if (!universeRequestSchema(input)) throw new TypeError('Invalid universe page request')
    return this.#request('/api/v1/discovery/assets/universes/query', input, 1024 * 1024, universeResponseSchema, signal)
  }
  resolveAssets(assetIds, { signal } = {}) {
    if (!Array.isArray(assetIds) || !assetIds.length || assetIds.length > 200 || new Set(assetIds).size !== assetIds.length || assetIds.some(id => typeof id !== 'string' || !id || id.length > 256)) throw new TypeError('Resolve 1..200 distinct asset IDs')
    return this.#request('/api/v1/discovery/assets/resolve', {asset_ids: assetIds}, 8 * 1024 * 1024, assetLookupSchema, signal)
  }
  bindUniverse(universeRef, {signal} = {}) {
    return this.#request('/api/v1/discovery/assets/universes/binding', {universe_ref:universeRef}, 8 * 1024 * 1024, universeBindingSchema, signal)
  }
}
