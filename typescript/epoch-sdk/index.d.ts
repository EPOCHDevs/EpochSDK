import type { StratifyXClient } from "@epoch/stratifyx"
import type { Client as LangGraphClient } from "@langchain/langgraph-sdk"
import type { ResearchResponseRecord, JobListItem, SdkExecutionRecord, ExecutionReportReference, SdkContractResponsePlanReference } from "@epoch/stratifyx/api/types/index.js"
import type { SdkContractRunRequest as RunSchema } from "@epoch/stratifyx/serialization/types/SdkContractRunRequest.js"
import type { SdkContractRunParameters as ParametersSchema } from "@epoch/stratifyx/serialization/types/SdkContractRunParameters.js"
import type { ResearchResponseRecord as ResponseSchema } from "@epoch/stratifyx/serialization/types/ResearchResponseRecord.js"
import type { SdkContractRunRequest as NativeRunRequest } from "@epoch/stratifyx/api/types/index.js"
import type { DatasetBuild as BuildSchema } from "@epoch/stratifyx/serialization/types/DatasetBuild.js"
import type { DatasetBuildRequest as BuildRequestSchema } from "@epoch/stratifyx/serialization/types/DatasetBuildRequest.js"
import type { DatasetPreviewPage as PreviewSchema } from "@epoch/stratifyx/serialization/types/DatasetPreviewPage.js"

export type RunRequest = Pick<RunSchema.Raw, "task" | "outputs" | "parameters"> & { context?: string[] }
export type OutputDefinition = RunRequest["outputs"][number]
export type RunParameters = ParametersSchema.Raw
export interface ExecutionRequest { reference: SavedStudy; parameters: RunParameters }
export type SavedResponse = ResearchResponseRecord
export interface SavedStudy {
  studyId: string
  sourceExecutionId: string
  threadId?: string
  reportTemplate?: ExecutionReportReference
  responsePlan?: SdkContractResponsePlanReference
}
export interface WorkflowHandle { requestId: string; operationId: string; threadId: string; assistantId: string; runId: string }
export interface Question {
  question: string
  description: string
  options: { label: string; recommended: boolean }[]
  multi_select: boolean
}
export interface QuestionInterrupt {
  id: string
  value: { type: "ask_user"; tool_call_id: string; questions: Question[] }
}
export interface Answer { question_index: number; selected_indices?: number[]; free_form_input?: string }
export type Answers = Record<string, { answers: Answer[] }>
export type DatasetReviewInterrupt = { id: string; value:
  | { type: "dataset_review"; stage: "configure"; tool_call_id: string; proposal_ref: string; preparation_ref: string; request: BuildRequestSchema.Raw }
  | { type: "dataset_review"; stage: "review"; tool_call_id: string; operation: BuildSchema.Raw; preview?: PreviewSchema.Raw; can_edit?: boolean }
}
export type DatasetReviewResponse =
  | { type: "dataset_review"; stage: "configure"; proposal_ref: string; action: "build_preview"; request: BuildRequestSchema.Raw }
  | { type: "dataset_review"; stage: "configure"; proposal_ref: string; action: "cancel" }
  | { type: "dataset_review"; stage: "review"; preparation_ref: string; attempt: number; review_ref: string; result_sha256: string; schema_sha256: string; action: "save" | "save_available" | "decline" | "continue" }
  | { type: "dataset_review"; stage: "review"; preparation_ref: string; attempt: number; review_ref: string; result_sha256: string; schema_sha256: string; action: "edit"; request: BuildRequestSchema.Raw }
export type WorkflowResponses = Record<string, { answers: Answer[] } | DatasetReviewResponse>
interface Operation { operationId: string; requestId: string; kind: "run" | "execute" }
export interface Pending extends Operation { status: "accepted" | "in_progress"; handle?: WorkflowHandle; executionId?: string; execution?: JobListItem }
export interface NeedsInput extends Operation { status: "needs_input"; kind: "run"; handle: WorkflowHandle; interrupts: (QuestionInterrupt | DatasetReviewInterrupt)[] }
export interface ResearchCompleted extends Operation { status: "succeeded"; kind: "run"; response: SavedResponse; reusableStudy?: SavedStudy }
export interface ExecutionCompleted extends Operation { status: "execution_selected"; kind: "execute"; execution: JobListItem; response?: SavedResponse; report?: SdkExecutionRecord; reusableStudy: SavedStudy }
export type OperationState = Pending | NeedsInput | ResearchCompleted | ExecutionCompleted
export interface ObserveOptions { wait?: boolean; signal?: AbortSignal; onStatus?: (state: OperationState) => void }
export class EpochError extends Error { code: string; details: Record<string, unknown>; constructor(code: string, message: string, details?: Record<string, unknown>) }
export class EpochClient {
  constructor(options: { backend: StratifyXClient; graph: LangGraphClient; assistantId?: string; pollIntervalMs?: number })
  run(request: RunRequest, options: ObserveOptions & { operationId: string; threadId?: string }): Promise<OperationState>
  resume(waiting: NeedsInput, responses: WorkflowResponses, options?: ObserveOptions): Promise<OperationState>
  status(operationId: string, options?: { kind?: "run" | "execute"; signal?: AbortSignal }): Promise<OperationState>
  execute(reference: SavedStudy | string, options: ObserveOptions & { operationId: string; period: NonNullable<RunParameters["period"]>; execution?: NonNullable<RunParameters["execution"]> }): Promise<OperationState>
  read(responseId: string, options?: { version?: number; signal?: AbortSignal }): Promise<SavedResponse>
  readRequest(operationId: string, options?: { signal?: AbortSignal }): Promise<RunRequest>
  readExecutionRequest(operationId: string, options?: { signal?: AbortSignal }): Promise<ExecutionRequest>
  observe(state: OperationState, options?: ObserveOptions): Promise<OperationState>
}
export function validateRequest(value: unknown): RunRequest
export function parseRequest(value: unknown): NativeRunRequest
export function requestToWire(value: NativeRunRequest): RunRequest
export function responseToWire(value: SavedResponse): ResponseSchema.Raw
export function validateResponse(value: SavedResponse): SavedResponse
