/** Platform-owned file previews, immutable history and explicit saves. */
import Ajv from 'ajv/dist/2020.js'
import document from './platform-files.openapi.json' with { type: 'json' }

const ajv = new Ajv({ strict: true })
const validators = Object.fromEntries(Object.entries(document.components.schemas).map(([name, schema]) => [name, ajv.compile(schema)]))
const originalPattern = new RegExp(document.components.schemas.FileVersion.properties.original_file_ref.pattern)
const referencePattern = new RegExp(document.components.schemas.FileDescriptor.properties.file_ref.pattern)
const encoder = new TextEncoder()

function validate(name, value) {
  if (!validators[name](value)) throw new TypeError(`Invalid Platform ${name}`)
}
function version(value, original) {
  const hash = value.file.content_sha256
  const ref = value.version === 0 ? original : `file-version:${original.slice(5)}:${value.version}:${hash}`
  if (value.original_file_ref !== original || value.file.file_ref !== ref || !hash || (value.version === 0 && hash !== original.slice(5))) {
    throw new TypeError('Platform returned an inconsistent file version')
  }
  return value
}
function documentPosition(block, source) {
  if ((block.start_byte === undefined) !== (block.length === undefined) || (block.start_byte !== undefined && (block.length !== encoder.encode(block.text).byteLength || block.start_byte + block.length > source.size_bytes))) throw new TypeError('Platform returned an inconsistent document position')
}
export class PlatformFileError extends Error {
  constructor(status, code, message, retryAfter) {
    super(message)
    this.name = 'PlatformFileError'
    this.status = status
    this.code = code
    this.retryAfter = retryAfter
  }
}

export class PlatformFilesClient {
  #token
  #fetch
  constructor({ apiUrl, token, fetch: authenticatedFetch }) {
    const url = new URL(apiUrl)
    if (apiUrl !== apiUrl.trim() || /[\u0000-\u001f]/u.test(apiUrl) || !['https:', 'http:'].includes(url.protocol) || url.username || url.password || url.search || url.hash) {
      throw new TypeError('Provide an HTTP(S) Platform API endpoint without credentials')
    }
    if (token == null && typeof authenticatedFetch !== 'function') throw new TypeError('Provide a bearer token/provider or an authenticated fetch')
    this.apiUrl = url.href.replace(/\/$/u, '')
    this.#token = token
    this.#fetch = authenticatedFetch ?? globalThis.fetch
  }
  _url(ref, suffix, original = false) {
    if (typeof ref !== 'string' || (original ? originalPattern : referencePattern).exec(ref)?.[0] !== ref) throw new TypeError('Provide an exact file reference')
    if (ref.startsWith('file-version:') && !Number.isSafeInteger(Number(ref.split(':')[2]))) throw new TypeError('Provide an exact file reference')
    return `${this.apiUrl}/api/v1/files/${encodeURIComponent(ref)}${suffix}`
  }
  async _headers() {
    if (this.#token == null) return {}
    const token = typeof this.#token === 'function' ? await this.#token() : this.#token
    if (typeof token !== 'string' || !/^[!-~]+$/u.test(token)) throw new TypeError('The token provider must return a nonempty printable bearer token')
    return { Authorization: `Bearer ${token}` }
  }
  async _error(response) {
    if (response.ok) return
    let code = 'INVALID_PLATFORM_RESPONSE'
    let message = `Platform file request failed (${response.status})`
    try {
      const body = await response.json()
      if (typeof body?.error === 'string' && typeof body.message === 'string') {
        code = body.error
        message = body.message
      }
    } catch { /* An untrusted error body is never included in diagnostics. */ }
    throw new PlatformFileError(response.status, code, message, response.headers.get('retry-after') ?? undefined)
  }
  async _json(url, model, body, { signal } = {}) {
    const serialized = body === undefined ? undefined : JSON.stringify(body)
    const headers = await this._headers()
    if (body !== undefined) headers['Content-Type'] = 'application/json'
    const response = await this.#fetch(url, { method: body === undefined ? 'GET' : 'POST', headers, body: serialized, signal, redirect: 'error' })
    await this._error(response)
    let result
    try {
      if (response.status !== 200) throw new Error()
      result = await response.json()
      validate(model, result)
    } catch { throw new TypeError(`Platform returned an invalid ${model}`) }
    return result
  }
  _documentUrl(ref, kind, suffix = '') {
    if (typeof ref !== 'string' || new RegExp(`^${kind}:[0-9a-f]{64}$`, 'u').exec(ref)?.[0] !== ref) throw new TypeError(`Provide an exact ${kind} reference`)
    return `${this.apiUrl}/api/v1/files/documents/${kind === 'document-read' ? 'reads/' : ''}${encodeURIComponent(ref)}${suffix}`
  }
  async beginDocumentRead(ref, options) {
    this._url(ref, '')
    const result = await this._json(`${this.apiUrl}/api/v1/files/documents/reads`, 'DocumentRead', {file_ref: ref}, options)
    if (result.source.file_ref !== ref) throw new TypeError('Platform returned a different document source')
    return result
  }
  async documentRead(ref, options) {
    const result = await this._json(this._documentUrl(ref, 'document-read'), 'DocumentRead', undefined, options)
    if (result.read_ref !== ref) throw new TypeError('Platform returned a different document read')
    return result
  }
  async documentContent(ref, {offset = 0, limit = 4, maxBytes = 32768, layer = 'primary', signal} = {}) {
    const url = new URL(this._documentUrl(ref, 'document', '/blocks'))
    if (!Number.isSafeInteger(offset) || offset < 0 || !Number.isSafeInteger(limit) || limit < 1 || limit > 100 || !Number.isSafeInteger(maxBytes) || maxBytes < 16384 || maxBytes > 131072 || !['primary','element','all'].includes(layer)) throw new TypeError('Invalid document content page')
    for (const [key,value] of Object.entries({offset,limit,max_bytes:maxBytes,layer})) url.searchParams.set(key, String(value))
    const result = await this._json(url.href, 'DocumentContentPage', undefined, {signal})
    if (result.document_version_ref !== ref || result.offset !== offset || result.layer !== layer || result.blocks.length > limit || result.offset + result.blocks.length > result.total_blocks) throw new TypeError('Platform returned an inconsistent document page')
    for (const block of result.blocks) documentPosition(block, result.source)
    return result
  }
  async documentPassage(ref, blockRef, options) {
    if (typeof blockRef !== 'string' || /^block:[0-9a-f]{64}$/u.exec(blockRef)?.[0] !== blockRef) throw new TypeError('Provide an exact block reference')
    const result = await this._json(this._documentUrl(ref, 'document', `/blocks/${encodeURIComponent(blockRef)}`), 'DocumentSourcePassage', undefined, options)
    if (result.document_version_ref !== ref || result.block.block_ref !== blockRef) throw new TypeError('Platform returned a different document passage')
    documentPosition(result.block, result.source)
    return result
  }
  preview(ref, options) { return this._json(this._url(ref, '/preview'), 'FilePreview', undefined, options) }
  async imagePreview(ref, options) {
    const result = await this._json(this._url(ref, '/image-preview'), 'FileImagePreview', undefined, options)
    if (result.state === 'ready' && (result.pages.reduce((sum, page) => sum + page.size_bytes, 0) !== result.size_bytes || result.pages.some((page, index) => page.page !== index + 1))) throw new TypeError('Platform returned an inconsistent image preview')
    return result
  }
  async editOptions(ref, options) {
    const result = await this._json(this._url(ref, '/edit-options', true), 'FileEditOptions', undefined, options)
    version(result.latest, ref)
    return result
  }
  async latest(ref, options) {
    return version(await this._json(this._url(ref, '/versions/latest', true), 'FileVersion', undefined, options), ref)
  }
  async history(ref, { before, limit = 50, signal } = {}) {
    if (!Number.isSafeInteger(limit) || limit < 1 || limit > 100 || (before !== undefined && (!Number.isSafeInteger(before) || before < 1))) throw new TypeError('Invalid version history page')
    const url = new URL(this._url(ref, '/versions', true))
    url.searchParams.set('limit', String(limit))
    if (before !== undefined) url.searchParams.set('before', String(before))
    const result = await this._json(url.href, 'FileVersionPage', undefined, { signal })
    let previous = before ?? Number.MAX_SAFE_INTEGER + 1
    for (const item of result.items) {
      version(item, ref)
      if (item.version >= previous) throw new TypeError('Platform returned unordered file history')
      previous = item.version
    }
    if (result.items.length > limit || (result.next_before !== undefined && result.next_before !== result.items.at(-1)?.version)) throw new TypeError('Platform returned an invalid history cursor')
    return result
  }
  async grid(ref, request, options) {
    request = structuredClone(request)
    const url = this._url(ref, '/edit-grid')
    validate('CellGridRequest', request)
    const result = await this._json(url, 'FileEditGrid', request, options)
    const hash = ref.startsWith('file:') ? ref.slice(5) : ref.split(':').at(-1)
    if (result.file_ref !== ref || result.source_sha256 !== hash || result.offset !== (request.offset ?? 0) || result.rows.length > (request.limit ?? 100) || result.rows.some(row => row.length !== result.columns.length)) throw new TypeError('Platform returned an inconsistent file grid')
    return result
  }
  async save(ref, request, options) {
    request = structuredClone(request)
    const url = this._url(ref, '/versions', true)
    validate('FileEditRequest', request)
    if (encoder.encode(request.request_id).byteLength > 128) throw new TypeError('request_id must fit 128 UTF-8 bytes')
    const result = version(await this._json(url, 'FileVersion', request, options), ref)
    if (result.version !== request.base_version + 1) throw new TypeError('Platform returned another save generation')
    return result
  }
  async content(ref, { preview = false, imagePage, byteRange, ifRange, signal } = {}) {
    if (imagePage !== undefined && (preview || !Number.isInteger(imagePage) || imagePage < 1 || imagePage > 1000)) throw new TypeError('Provide one image page in 1..1000, separately from PDF preview')
    const url = this._url(ref, imagePage === undefined ? preview ? '/preview/content' : '/content' : `/image-preview/${imagePage}/content`)
    const headers = {}
    if (byteRange !== undefined) {
      if (typeof byteRange !== 'string' || byteRange.length > 256 || !/^bytes=(?:\d+-\d*|-\d+)$/u.test(byteRange)) throw new TypeError('Provide one byte range')
      headers.Range = byteRange
    }
    if (ifRange !== undefined) {
      if (typeof ifRange !== 'string' || ifRange.length > 256 || /[^\u0020-\u007e]/u.test(ifRange)) throw new TypeError('Invalid If-Range validator')
      headers['If-Range'] = ifRange
    }
    Object.assign(headers, await this._headers())
    const response = await this.#fetch(url, { method: 'GET', headers, signal, redirect: 'error' })
    await this._error(response)
    if (![200, 206].includes(response.status)) throw new TypeError('Platform returned an invalid content response')
    return response
  }
}
