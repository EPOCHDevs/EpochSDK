/** Platform-owned research lifecycle. Native execution remains on StratifyX. */
import Ajv from 'ajv/dist/2020.js'
import addFormats from 'ajv-formats'
import * as core from '@epoch/stratifyx/core/index.js'
import { SdkContractRunRequest } from '@epoch/stratifyx/serialization/types/SdkContractRunRequest.js'
import { SdkContractErrorResponse } from '@epoch/stratifyx/serialization/types/SdkContractErrorResponse.js'
import { SdkContractSavedOutputManifest } from '@epoch/stratifyx/serialization/types/SdkContractSavedOutputManifest.js'
import contract from './platform-research.openapi.json' with { type: 'json' }

const s = core.serialization
const runtime = s.object({ threadId: s.property('thread_id', s.string()), assistantId: s.property('assistant_id', s.string()),
  executionIdsBefore: s.property('execution_ids_before', s.list(s.string())), outcomeIdsBefore: s.property('outcome_ids_before', s.list(s.string())) })
const launch = s.object({ assistantId: s.property('assistant_id', s.string()), threadId: s.property('thread_id', s.string().optional()) })
const record = s.object({ requestId: s.property('request_id', s.string()), version: s.number(),
  createdAtMs: s.property('created_at_ms', s.number()), updatedAtMs: s.property('updated_at_ms', s.number()),
  phase: s.enum_(['accepted', 'active', 'needs_input', 'outputs_recorded', 'failed']), interaction: s.enum_(['interactive', 'one_shot']),
  request: SdkContractRunRequest, operationId: s.property('operation_id', s.string().optional()), launch: launch.optional(), runtime: runtime.optional(),
  graphRunId: s.property('graph_run_id', s.string().optional()), currentExecutionId: s.property('current_execution_id', s.string().optional()),
  nativeExecutionRequestId: s.property('native_execution_request_id', s.string().optional()), sourceExecutionId: s.property('source_execution_id', s.string().optional()),
  responseId: s.property('response_id', s.string().optional()), responseVersion: s.property('response_version', s.number().optional()),
  outputManifest: s.property('output_manifest', SdkContractSavedOutputManifest.optional()), error: SdkContractErrorResponse.optional(),
})
const create = s.object({ request: SdkContractRunRequest, operationId: s.property('operation_id', s.string().optional()), launch: launch.optional() })
const update = s.object({ expectedVersion: s.property('expected_version', s.number()), runtime: runtime.optional(),
  phase: s.enum_(['active', 'needs_input']).optional(), graphRunId: s.property('graph_run_id', s.string().optional()),
  priorGraphRunId: s.property('prior_graph_run_id', s.string().optional()), currentExecutionId: s.property('current_execution_id', s.string().optional()),
  nativeExecutionRequestId: s.property('native_execution_request_id', s.string().optional()), responseId: s.property('response_id', s.string().optional()),
  responseVersion: s.property('response_version', s.number().optional()), outputManifest: s.property('output_manifest', SdkContractSavedOutputManifest.optional()),
  error: SdkContractErrorResponse.optional(),
})
const ajv = new Ajv({ strict: false, allErrors: true }); addFormats(ajv)
const check = name => ajv.compile({ ...contract, $ref: '#/components/schemas/' + name })
const checks = { CreateResearch: check('CreateResearch'), UpdateResearch: check('UpdateResearch'), ResearchRecord: check('ResearchRecord') }
const unwrap = result => {
  if (!result.ok) throw new TypeError('Invalid Platform research contract')
  return result.value
}
const strict = { unrecognizedObjectKeys: 'fail', allowUnrecognizedEnumValues: false, allowUnrecognizedUnionMembers: false }
function validate(name, value) {
  if (!checks[name](value)) throw new TypeError('Invalid Platform ' + name)
  return value
}
export function parseResearchFailure(wire) { return unwrap(SdkContractErrorResponse.parse(wire, strict)) }
export class ResearchOperationsHTTPError extends Error {
  constructor(statusCode) { super('Research operation HTTP ' + statusCode); this.statusCode = statusCode }
}
const segment = value => {
  if (typeof value !== 'string' || !/^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$/.test(value)) throw new TypeError('Invalid research identity')
  return encodeURIComponent(value)
}
/** Fixed token or per-request provider, scoped to one Platform origin. No write retries. */
export class ResearchOperationsClient {
  constructor({ baseUrl, token, fetch = globalThis.fetch, fetcher }) {
    const url = new URL(baseUrl)
    if ((url.protocol !== 'https:' && !(url.protocol === 'http:' && ['localhost', '127.0.0.1', '[::1]'].includes(url.hostname))) ||
      url.username || url.password || url.pathname !== '/' || url.search || url.hash) throw new TypeError('Invalid research origin')
    this.origin = url.origin; this.token = token; this.fetcher = fetcher
    this.fetch = fetch === globalThis.fetch ? fetch.bind(globalThis) : fetch
  }
  async request(method, path, body, options = {}) {
    if (options.maxRetries !== undefined && options.maxRetries !== 0) throw new TypeError('Research writes are never automatically retried')
    const token = typeof this.token === 'function' ? await this.token() : this.token
    if (token !== undefined && (typeof token !== 'string' || !/^[!-~]+$/.test(token))) throw new TypeError('Invalid research credential')
    const url = this.origin + '/api/v1/integration/requests' + path
    const headers = { 'Content-Type': 'application/json', ...(token ? { Authorization: 'Bearer ' + token } : {}) }
    let value
    if (this.fetcher) {
      const result = await this.fetcher({ url, method, body, headers, contentType: 'application/json', maxRetries: 0, abortSignal: options.abortSignal })
      if (!result.ok) throw new ResearchOperationsHTTPError(result.error?.statusCode ?? 503)
      value = result.body
    } else {
      const response = await this.fetch(url, { method, headers, body: body === undefined ? undefined : JSON.stringify(body), redirect: 'error', signal: options.abortSignal ?? AbortSignal.timeout(30_000) })
      if (response.status !== 200) { await response.body?.cancel(); throw new ResearchOperationsHTTPError(response.status) }
      const reader = response.body?.getReader(); const parts = []; let size = 0
      if (reader) try {
        while (true) {
          const part = await reader.read(); if (part.done) break
          size += part.value.byteLength
          if (size > 512 * 1024) { await reader.cancel(); throw new TypeError('Research record exceeds 512 KiB') }
          parts.push(part.value)
        }
      } finally { reader.releaseLock() }
      const bytes = new Uint8Array(size); let offset = 0
      for (const part of parts) { bytes.set(part, offset); offset += part.byteLength }
      value = JSON.parse(new TextDecoder('utf-8', { fatal: true }).decode(bytes), (_key, value, context) => {
        // The native TS model uses numbers. Refuse an unrepresentable integer
        // rather than returning a rounded accepted cash value or schema bound.
        if (typeof value === 'number' && /^-?\d+$/.test(context?.source ?? '') && BigInt(context.source) !== BigInt(value))
          throw new TypeError('The native TypeScript number model cannot represent this exact research integer')
        return value
      })
    }
    return unwrap(record.parse(validate('ResearchRecord', value), strict))
  }
  createSdkRequest(body, options) { return this.request('POST', '', validate('CreateResearch', unwrap(create.json(body, strict))), options) }
  getSdkRequest(id, _query = {}, options) { return this.request('GET', '/' + segment(id), undefined, options) }
  getSdkRequestByHandle(id, _query = {}, options) { return this.request('GET', '/by-handle/' + segment(id), undefined, options) }
  updateSdkRequest(id, body, options) { return this.request('PATCH', '/' + segment(id), validate('UpdateResearch', unwrap(update.json(body, strict))), options) }
}
