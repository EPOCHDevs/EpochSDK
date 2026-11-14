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
  /** Seconds the server asked you to wait, when it said. */
  readonly retryAfter: number | null
  constructor(problem: Problem, options?: { retryAfter?: number | null })
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
  | {
      /**
       * A stable step: step_started and step_completed (each with a label) around the build and run
       * steps, study_saved, execution_started and answer_saved. Ignore kinds you don't know.
       */
      event: "progress"
      research_id: string
      progress: { kind: string; label?: string | null; study_id?: string | null; execution_id?: string | null; response?: ResponseRef | null }
    }
  | { event: "questions" | "completed" | "failed"; research: Research }

export interface Execution {
  id: string
  object: "execution"
  status: Status
  operation_id?: string | null
  study_id: string
  parent_execution_id?: string | null
  created_at: string
  progress?: { phase?: string | null; percent?: number | null; current?: number | null; total?: number | null; unit?: string | null } | null
  /** The declared answer; the run is running until it settles, so completed means delivered. */
  answer?: { status: Status; response?: ResponseRef | null; report_execution_id?: string | null } | null
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

export interface UserFile {
  file_ref: string
  name: string
  media_type: string
  size_bytes: number
  status: string
  created_at: string
  content_sha256?: string | null
  error?: string | null
  [field: string]: unknown
}

export interface EventsOptions {
  /** Resume after this event id, from an earlier stream. */
  lastEventId?: string
  /** Stops the stream; the research continues. */
  signal?: AbortSignal
  /** Milliseconds without bytes before reconnecting (60 s by default). */
  idleTimeout?: number
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

/** A dataset column's native import type. Answer tables use their own column kinds. */
export type DatasetColumnType = "utf8" | "int64" | "float64" | "bool" | "date32" | "timestamp[ns,UTC]"

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
    events(researchId: string, options?: EventsOptions): AsyncGenerator<ResearchEvent>
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
    upload(content: Uint8Array | Blob | ArrayBuffer, options: { name: string; mediaType?: string }): Promise<UserFile>
  }
  readonly datasets: {
    prepare(request: {
      fileRef: string
      name: string
      /**
       * Leave out to keep the file's own columns. Otherwise every column, in order, with its exact
       * name and one of Backend's native import types.
       */
      columns?: { name: string; dtype: DatasetColumnType; nullable: boolean }[]
      delimiter?: string
      header?: boolean
      nullValues?: string[]
      requestId?: string
    }): Promise<Record<string, unknown>>
    save(draftRef: string, options: { name: string }): Promise<Record<string, unknown>>
  }
  request(
    method: string,
    route: string,
    options?: { json?: unknown; body?: BodyInit; headers?: Record<string, string>; idempotencyKey?: string; deduplicated?: boolean },
  ): Promise<unknown>
}
