// Epoch's public v1 API with one URL and one API key. Shapes follow contracts/public-v1.openapi.json.

export declare const DEFAULT_API_URL: "https://api.epoch.trade"

export type Status = "queued" | "running" | "needs_input" | "completed" | "failed" | "cancelled"

export interface Problem {
  type?: string
  title: string
  status: number
  detail?: string | null
  code: string
  retryable: boolean
  request_id?: string | null
}

export declare class EpochApiError extends Error {
  readonly problem: Problem
  readonly status: number
  readonly code: string
  readonly retryable: boolean
  readonly requestId: string | null
  constructor(problem: Problem)
}

export interface Links {
  self: string
  events?: string | null
  /** Opens the same work in the Epoch Terminal. */
  app?: string | null
  response?: string | null
}
export interface ResponseRef {
  id: string
  version: number
}
export interface SavedStudy {
  study_id: string
  source_execution_id: string
  thread_id?: string | null
  [field: string]: unknown
}
export interface Column {
  name: string
  type: "string" | "int64" | "float64" | "boolean" | "date" | "datetime"
  description?: string
  unit?: string
  nullable?: boolean
}
export type Output =
  | { name: string; type: "text"; instructions: string; format?: "plain" | "markdown"; description?: string }
  | { name: string; type: "table"; schema: Column[]; description?: string }
  | { name: string; type: "json"; schema: Record<string, unknown>; description?: string }

export interface PendingQuestion {
  id: string
  kind: "ask_user" | "dataset_review"
  questions?: {
    question: string
    description: string
    options: { label: string; recommended: boolean }[]
    multi_select: boolean
  }[]
  review?: Record<string, unknown>
}
export interface Research {
  id: string
  object: "research"
  status: Status
  operation_id: string
  thread_id?: string | null
  created_at: string
  updated_at: string
  questions: PendingQuestion[]
  result?: { response: ResponseRef; reusable_study?: SavedStudy | null; source_execution_id?: string | null } | null
  error?: Problem | null
  links: Links
}
export type ResearchEvent =
  | { event: "status"; research_id: string; status: Status }
  | { event: "ui"; research_id: string; message: { type: "ui"; id: string; name: string; props: Record<string, unknown>; metadata?: Record<string, unknown> } }
  | { event: "ui_removed"; research_id: string; id: string }
  | { event: "progress"; research_id: string; progress: { kind: string; label?: string | null } }
  | { event: "questions" | "completed" | "failed"; research: Research }

export interface Execution {
  id: string
  object: "execution"
  status: Status
  operation_id?: string | null
  study_id: string
  created_at: string
  progress?: { phase?: string | null; percent?: number | null; current?: number | null; total?: number | null; unit?: string | null } | null
  answer?: { status: Status; response?: ResponseRef | null } | null
  reusable_study?: SavedStudy | null
  error?: Problem | null
  links: Links
}

export interface SavedAnswer {
  response_id: string
  request_id: string
  thread_id: string
  version: number
  study_id?: string | null
  published_at_ms: number
  content: {
    declarations: Output[]
    outputs: (
      | { name: string; type: "text"; format: "plain" | "markdown"; value: string }
      | { name: string; type: "table"; schema: Column[]; rows?: unknown[][] | null; source?: unknown }
      | { name: string; type: "json"; value: unknown }
    )[]
    [field: string]: unknown
  }
  [field: string]: unknown
}
export interface TablePage {
  response_id: string
  version: number
  name: string
  type: "table"
  schema: Column[]
  rows: unknown[][]
  offset: number
  total_rows: number
  next_offset: number | null
}

export interface EpochOptions {
  /** Defaults to EPOCH_API_KEY. */
  apiKey?: string
  /** Defaults to EPOCH_API_URL, then https://api.epoch.trade. */
  apiUrl?: string
  maxRetries?: number
  fetch?: typeof fetch
}
interface Wait {
  /** Milliseconds between reads (10 s by default). */
  pollInterval?: number
  /** Give up after this many milliseconds. */
  timeout?: number
}

export declare class Epoch {
  constructor(options?: EpochOptions)
  readonly apiUrl: string
  readonly maxRetries: number
  readonly research: {
    create(request: {
      task: string
      context?: string[]
      outputs: Output[]
      threadId?: string
      idempotencyKey?: string
    }): Promise<Research>
    get(researchId: string): Promise<Research>
    answer(researchId: string, answers: Record<string, unknown>): Promise<Research>
    wait(researchId: string, options?: Wait): Promise<Research>
    events(researchId: string): AsyncGenerator<ResearchEvent>
  }
  readonly executions: {
    create(request: {
      researchId?: string
      study?: SavedStudy
      start?: string
      end?: string
      idempotencyKey?: string
    }): Promise<Execution>
    get(executionId: string): Promise<Execution>
    wait(executionId: string, options?: Wait): Promise<Execution>
  }
  readonly responses: {
    get(responseId: string, options?: { version?: number }): Promise<SavedAnswer>
    table(responseId: string, name: string, options?: { version?: number; offset?: number; pageSize?: number }): Promise<TablePage>
    rows(responseId: string, name: string, options?: { version?: number }): Promise<unknown[][]>
  }
  readonly files: {
    upload(content: Uint8Array | Blob | ArrayBuffer, options: { name: string; mediaType?: string }): Promise<Record<string, unknown>>
  }
  readonly datasets: {
    prepare(request: {
      fileRef: string
      name: string
      columns: { name: string; dtype: Column["type"]; nullable: boolean }[]
      delimiter?: string
      header?: boolean
      nullValues?: string[]
      requestId?: string
    }): Promise<Record<string, unknown>>
    save(draftRef: string, options: { name: string }): Promise<Record<string, unknown>>
  }
  request(method: string, route: string, options?: Record<string, unknown>): Promise<unknown>
}
