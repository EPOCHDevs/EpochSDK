import type { SdkContractRunRequest, SdkContractErrorResponse, SdkContractSavedOutputManifest } from '@epoch/stratifyx/api/types/index.js'
import type { FetchFunction } from '@epoch/stratifyx/core/fetcher/index.js'
export interface ResearchRuntime { threadId: string; assistantId: string; executionIdsBefore: string[]; outcomeIdsBefore: string[] }
export interface ResearchLaunch { assistantId: string; threadId?: string }
export interface ResearchRecord {
  requestId: string; version: number; createdAtMs: number; updatedAtMs: number
  phase: 'accepted' | 'active' | 'needs_input' | 'outputs_recorded' | 'failed'
  interaction: 'interactive' | 'one_shot'; request: SdkContractRunRequest
  operationId?: string; runtime?: ResearchRuntime; launch?: ResearchLaunch; graphRunId?: string
  currentExecutionId?: string; nativeExecutionRequestId?: string; sourceExecutionId?: string
  responseId?: string; responseVersion?: number; outputManifest?: SdkContractSavedOutputManifest; error?: SdkContractErrorResponse
}
export interface ResearchUpdate {
  expectedVersion: number; runtime?: ResearchRuntime; phase?: 'active' | 'needs_input'; graphRunId?: string; priorGraphRunId?: string
  currentExecutionId?: string; nativeExecutionRequestId?: string; responseId?: string; responseVersion?: number
  outputManifest?: SdkContractSavedOutputManifest; error?: SdkContractErrorResponse
}
export interface ResearchRequestOptions { maxRetries?: 0; abortSignal?: AbortSignal }
export class ResearchOperationsHTTPError extends Error { statusCode: number; constructor(statusCode: number) }
export class ResearchOperationsClient {
  constructor(options: { baseUrl: string; token?: string | (() => string | Promise<string>); fetch?: typeof globalThis.fetch; fetcher?: FetchFunction })
  createSdkRequest(body: { request: SdkContractRunRequest; operationId?: string; launch?: ResearchLaunch }, options?: ResearchRequestOptions): Promise<ResearchRecord>
  getSdkRequest(id: string, query?: Record<string, never>, options?: ResearchRequestOptions): Promise<ResearchRecord>
  getSdkRequestByHandle(id: string, query?: Record<string, never>, options?: ResearchRequestOptions): Promise<ResearchRecord>
  updateSdkRequest(id: string, body: ResearchUpdate, options?: ResearchRequestOptions): Promise<ResearchRecord>
}
