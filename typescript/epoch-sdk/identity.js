import Ajv from 'ajv'
import schema from './asset-identity.schema.json' with { type: 'json' }

const ajv = new Ajv({ strict: true, allowUnionTypes: true })
const validators = new Map()
const camel = key => key.replace(/_([a-z])/g, (_match, letter) => letter.toUpperCase())
const decoded = value => Array.isArray(value) ? value.map(decoded)
  : value && typeof value === 'object' ? Object.fromEntries(Object.entries(value).map(([key, field]) => [camel(key), decoded(field)])) : value

function parse(name, value) {
  let validate = validators.get(name)
  if (!validate) {
    validate = ajv.compile({ $ref: '#/definitions/' + name, definitions: schema.definitions })
    validators.set(name, validate)
  }
  if (!validate(value)) throw new TypeError('Invalid Platform identity response: ' + name)
  return decoded(value)
}
export const parseAssetInformation = value => parse('AssetSpecification', value)
export const parseAssetLogos = value => parse('AssetLogoResponse', value)
export const parseCountryCatalog = value => parse('CountryCatalogResponse', value)

export class IdentityHTTPError extends Error {
  constructor(status, body) { super('Identity HTTP ' + status + ': ' + body); this.name = 'IdentityHTTPError'; this.status = status; this.body = body }
}
const id = value => {
  if (typeof value !== 'string' || !value || value.length > 256 || /[\x00-\x20\x7f/\\%?#]/.test(value)) throw new TypeError('Invalid identity ID')
  return encodeURIComponent(value)
}

/** Platform-owned presentation metadata; no dependency on a native API client. */
export class IdentityClient {
  #origin
  #token
  #fetch
  constructor({ baseUrl, token, fetch: transport = globalThis.fetch }) {
    const origin = new URL(baseUrl)
    if (origin.protocol !== 'https:' && !(origin.protocol === 'http:' && ['localhost', '127.0.0.1', '[::1]'].includes(origin.hostname))) throw new TypeError('Identity origin must use HTTPS or loopback')
    if (origin.pathname !== '/' || origin.search || origin.hash || origin.username || origin.password) throw new TypeError('Invalid identity origin')
    if (token !== undefined && typeof token !== 'string' && typeof token !== 'function') throw new TypeError('Invalid identity token provider')
    this.#origin = origin; this.#token = token
    this.#fetch = transport === globalThis.fetch ? transport.bind(globalThis) : transport
  }
  async #request(path, name, options = {}, body) {
    options.signal?.throwIfAborted()
    const token = typeof this.#token === 'function' ? await this.#token() : this.#token
    options.signal?.throwIfAborted()
    if (token !== undefined && token !== null && token !== '' && (typeof token !== 'string' || /\s/.test(token))) throw new TypeError('Invalid identity token')
    const timeout = AbortSignal.timeout(12000)
    const response = await this.#fetch(new URL(path, this.#origin), {
      method: body === undefined ? 'GET' : 'POST', redirect: 'error',
      headers: { ...(token ? { Authorization: 'Bearer ' + token } : {}), ...(body === undefined ? {} : { 'Content-Type': 'application/json' }) },
      ...(body === undefined ? {} : { body: JSON.stringify(body) }),
      signal: options.signal ? AbortSignal.any([options.signal, timeout]) : timeout,
    })
    const reader = response.body?.getReader(), parts = []; let size = 0
    try {
      if (Number(response.headers.get('content-length')) > 8 * 1024 * 1024) throw new RangeError('Identity response exceeds bound')
      if (reader) for (;;) {
        const part = await reader.read(); if (part.done) break
        size += part.value.byteLength
        if (size > 8 * 1024 * 1024) throw new RangeError('Identity response exceeds bound')
        parts.push(part.value)
      }
    } finally { await reader?.cancel() }
    const bytes = new Uint8Array(size); let offset = 0
    for (const part of parts) { bytes.set(part, offset); offset += part.byteLength }
    const text = new TextDecoder('utf-8', { fatal: true }).decode(bytes)
    if (!response.ok) throw new IdentityHTTPError(response.status, text)
    return parse(name, JSON.parse(text))
  }
  async getAssetInformation(assetId, options) {
    const result = await this.#request('/api/v1/metadata/assets/' + id(assetId), 'AssetSpecification', options)
    if (result.id !== assetId) throw new TypeError('Metadata belongs to another asset')
    return result
  }
  async getAssetLogos(assetId, scope = {}, options) {
    const path = '/api/v1/assets/' + id(assetId) + '/logos'
    if (!!scope.listingCatalogue !== !!scope.listingSelectedAt) throw new TypeError('Both listing catalogue and clock are required')
    const query = scope.listingCatalogue ? '?' + new URLSearchParams({ listing_catalogue: scope.listingCatalogue, listing_selected_at: scope.listingSelectedAt }) : ''
    const result = await this.#request(path + query, 'AssetLogoResponse', options)
    if (result.assetId !== assetId) throw new TypeError('Artwork belongs to another asset')
    return result
  }
  getCountryCatalog(options) { return this.#request('/api/v1/metadata/countries', 'CountryCatalogResponse', options) }
  getCountry(code, options) { return this.#request('/api/v1/metadata/countries/' + id(code), 'CountryIdentity', options) }
  getRegion(code, options) { return this.#request('/api/v1/metadata/regions/' + id(code), 'CountryIdentity', options) }
  listAssets(query = {}, options) {
    const values = new URLSearchParams()
    for (const [key, value] of Object.entries({ query: query.query, page: query.page, page_size: query.pageSize })) if (value !== undefined) values.set(key, String(value))
    return this.#request('/api/v1/metadata/assets' + (values.size ? '?' + values : ''), 'AssetInformationPage', options)
  }
  async resolveAssetInformation(assetIds, options) {
    if (!Array.isArray(assetIds) || !assetIds.length || assetIds.length > 200) throw new TypeError('Resolve 1..200 asset IDs')
    assetIds.forEach(id)
    const result = await this.#request('/api/v1/metadata/assets/resolve', 'AssetLookupResponse', options, { asset_ids: assetIds })
    if (JSON.stringify(result.items.map(item => item.assetId)) !== JSON.stringify([...new Set(assetIds)])) throw new TypeError('Lookup returned different asset IDs')
    return result
  }
}
