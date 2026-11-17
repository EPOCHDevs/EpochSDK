/** DTOs follow contracts/platform-files.openapi.json, owned by EpochPlatform. */
export type CellValue = { type: 'string'; value: string } | { type: 'number'; value: string } | { type: 'boolean'; value: boolean } | { type: 'null' }
export type FileFormat = 'csv' | 'tsv' | 'jsonl' | 'parquet' | 'xlsx'
export interface FileDescriptor {
  file_ref: string; name: string; media_type: string; detected_media_type?: string
  category?: 'dataset' | 'document' | 'other'; size_bytes: number
  status: 'uploading' | 'uploaded' | 'failed'; created_at: string; content_sha256?: string; error?: string
}
export interface FileVersion { original_file_ref: string; version: number; file: FileDescriptor; saved_at: string; limitations: string[] }
export interface FileVersionPage { items: FileVersion[]; next_before?: number }
export interface FileEditLimits { max_file_bytes: number; max_request_bytes: number; max_rows: number; max_columns: number; max_cells: number; max_changes: number; max_expanded_bytes: number }
export type FileEditOptions = { schema_version: 1; latest: FileVersion; limits: FileEditLimits } & (
  { kind: 'text' } | { kind: 'cells'; format: FileFormat; formula_cells_editable: false; formula_recalculation: false } | { kind: null; reason: string }
)
export interface GridOptions { format: FileFormat; sheet?: string; header?: boolean; delimiter?: string; null_values?: string[] }
export interface CellChange { row: number; column: string; value: CellValue; sheet?: string }
export type FileEdit = { kind: 'text'; content: string } | (GridOptions & { kind: 'cells'; changes: CellChange[] })
export interface FileEditRequest { schema_version: 1; request_id: string; base_version: number; base_content_sha256: string; edit: FileEdit }
export interface CellGridRequest extends GridOptions { schema_version: 1; offset?: number; limit?: number }
export interface GridColumn { name: string; native_type: string; nullable: boolean; edit_type: 'string' | 'number' | 'boolean' }
export interface GridCell { value: CellValue; read_only: boolean }
export interface FileEditGrid { schema_version: 1; file_ref: string; source_sha256: string; offset: number; total_rows: number; sheets: string[]; sheet?: string; limitations: string[]; columns: GridColumn[]; rows: GridCell[][] }
export type FilePreview = { state: 'none' | 'pending' } | { state: 'failed'; reason: string } | { state: 'ready'; media_type: 'application/pdf'; size_bytes: number; converter_version: string }
export interface RequestOptions { signal?: AbortSignal }
export interface HistoryOptions extends RequestOptions { before?: number; limit?: number }
export interface ContentOptions extends RequestOptions { preview?: boolean; imagePage?: number; byteRange?: string; ifRange?: string }
export interface PlatformFilesOptions { apiUrl: string; token?: string | (() => string | Promise<string>); fetch?: typeof globalThis.fetch }
export class PlatformFileError extends Error { status: number; code: string; retryAfter?: string; constructor(status: number, code: string, message: string, retryAfter?: string) }
/** No implicit mutation retries. Retain the exact save body/request_id after an uncertain result. */
export class PlatformFilesClient {
  constructor(options: PlatformFilesOptions)
  beginDocumentRead(ref: string, options?: RequestOptions): Promise<PlatformDocumentRead>
  documentRead(ref: string, options?: RequestOptions): Promise<PlatformDocumentRead>
  documentContent(ref: string, options?: DocumentContentOptions): Promise<PlatformDocumentContentPage>
  documentPassage(ref: string, blockRef: string, options?: RequestOptions): Promise<PlatformDocumentSourcePassage>
  preview(ref: string, options?: RequestOptions): Promise<FilePreview>
  imagePreview(ref: string, options?: RequestOptions): Promise<FileImagePreview>
  editOptions(original: string, options?: RequestOptions): Promise<FileEditOptions>
  latest(original: string, options?: RequestOptions): Promise<FileVersion>
  history(original: string, options?: HistoryOptions): Promise<FileVersionPage>
  grid(pin: string, request: CellGridRequest, options?: RequestOptions): Promise<FileEditGrid>
  save(original: string, request: FileEditRequest, options?: RequestOptions): Promise<FileVersion>
  /** The caller streams response.body; this method does not buffer a complete file. */
  content(pin: string, options?: ContentOptions): Promise<Response>
}

export interface ImagePreviewPage { page: number; width: number; height: number; size_bytes: number; content_sha256: string }
export type FileImagePreview = { state: 'none' | 'pending' } | { state: 'failed'; reason: string } | { state: 'ready'; media_type: 'image/png'; converter_version: string; size_bytes: number; pages: ImagePreviewPage[] }

export interface DocumentCoverage { processed_pages: number[]; unread_pages: number[]; total_pages?: number }
export interface PlatformDocumentBlock { block_ref: string; page?: number; kind: 'text' | 'table'; text: string; bounding_box?: number[]; layer: 'primary' | 'element'; start_byte?: number; length?: number }
export interface DocumentOutline { level: number; text: string; block_ref: string }
export interface DocumentAttachment { name: string | null; media_type: string; size_bytes: number }
export interface PlatformDocumentRead { read_ref: string; source: FileDescriptor; state: 'queued' | 'preparing' | 'checking' | 'ready' | 'failed' | 'stopped' | 'deleted'; attempt: number; message: string; created_at: string; updated_at: string; document_version_ref?: string; coverage: DocumentCoverage; limitations: string[]; outline?: DocumentOutline[]; attachments?: DocumentAttachment[] }
export interface PlatformDocumentContentPage { document_version_ref: string; source: FileDescriptor; content_sha256: string; provider_version: string; coverage: DocumentCoverage; limitations: string[]; blocks: PlatformDocumentBlock[]; offset: number; total_blocks: number; has_more: boolean; layer: 'primary' | 'element' | 'all' }
export interface PlatformDocumentSourcePassage { document_version_ref: string; source: FileDescriptor; content_sha256: string; block: PlatformDocumentBlock }
export interface DocumentContentOptions extends RequestOptions { offset?: number; limit?: number; maxBytes?: number; layer?: 'primary' | 'element' | 'all' }
