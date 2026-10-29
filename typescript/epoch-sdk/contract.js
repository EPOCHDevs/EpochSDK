import Ajv from "ajv/dist/2020.js"
import addFormats from "ajv-formats"
import bundle from "./schemas.generated.json" with { type: "json" }
import { SdkContractRunRequest } from "@epoch/stratifyx/serialization/types/SdkContractRunRequest.js"
import { ResearchResponseRecord } from "@epoch/stratifyx/serialization/types/ResearchResponseRecord.js"
import { SdkContractRunParameters } from "@epoch/stratifyx/serialization/types/SdkContractRunParameters.js"

export class EpochError extends Error {
  constructor(code, message, details = {}) {
    super(message)
    this.name = "EpochError"
    this.code = code
    this.details = details
  }
}

export function invariant(condition, message, code = "INVALID_STATE") {
  if (!condition) throw new EpochError(code, message)
}

const validator = () => {
  const ajv = new Ajv({ strict: false, strictNumbers: true, allErrors: true })
  addFormats(ajv)
  return ajv
}
const ajv = validator()
ajv.addSchema(bundle.request)
ajv.addSchema(bundle.response)
const requestValidator = ajv.compile({ $ref: `${bundle.request.$id}#/components/schemas/RunRequest` })
const parametersValidator = ajv.compile({ $ref: `${bundle.request.$id}#/components/schemas/RunParameters` })
const responseValidator = ajv.getSchema(bundle.response.$id)

function validate(check, value) {
  if (check(value)) return
  const issues = check.errors.map((error) => ({
    path: error.instancePath || "/",
    message: error.message || "Invalid value",
  }))
  throw new EpochError("VALIDATION_ERROR", issues.map(e => `${e.path}: ${e.message}`).join("; "), { issues })
}

function unwrap(result) {
  invariant(result.ok, result.errors?.map(e => `${e.path.join(".")}: ${e.message}`).join("; ") || "Invalid native value", "VALIDATION_ERROR")
  return result.value
}

export function canonical(value) {
  if (Array.isArray(value)) return JSON.stringify(value.map(item => JSON.parse(canonical(item))))
  if (value !== null && typeof value === "object") {
    return JSON.stringify(Object.fromEntries(Object.keys(value).sort().filter(key => value[key] !== undefined)
      .map(key => [key, JSON.parse(canonical(value[key]))])))
  }
  return JSON.stringify(value)
}

export function normalizedDeclarations(outputs) {
  return outputs.map(output => output.type === "table"
    ? { ...output, schema: output.schema.map(column => ({ ...column, nullable: column.nullable ?? false })) }
    : output.type === "text" ? { ...output, format: output.format ?? "plain" } : output)
}

export function validateRequest(request) {
  validate(requestValidator, request)
  if (request.parameters) parseParameters(request.parameters)
  invariant(!request.auto_ingest, "Automatic ingestion is outside the research workflow.", "VALIDATION_ERROR")
  invariant(request.study_id === undefined && request.source_execution_id === undefined,
    "Use execute() with a saved study reference for prepared work.", "VALIDATION_ERROR")
  invariant(new Set(request.outputs.map(o => o.name)).size === request.outputs.length,
    "Output names must be unique.", "VALIDATION_ERROR")
  for (const output of request.outputs) {
    if (output.type === "table") invariant(new Set(output.schema.map(c => c.name)).size === output.schema.length,
      `Table ${output.name}: column names must be unique.`, "VALIDATION_ERROR")
    if (output.type === "json") {
      try { validator().compile(output.schema) }
      catch (error) { throw new EpochError("VALIDATION_ERROR", `JSON output ${output.name}: ${error.message}`) }
    }
  }
  return request
}

export const parseRequest = request => unwrap(SdkContractRunRequest.parse(validateRequest(request)))
export const requestToWire = request => unwrap(SdkContractRunRequest.json(request))
export const responseToWire = response => unwrap(ResearchResponseRecord.json(response))
export const parametersToWire = parameters => unwrap(SdkContractRunParameters.json(parameters))
export function parseParameters(parameters) {
  validate(parametersValidator, parameters)
  const period = parameters.period
  invariant(!period?.start || !period.end || period.start <= period.end,
    "The start date must not follow the end date.", "VALIDATION_ERROR")
  return unwrap(SdkContractRunParameters.parse(parameters))
}

export function validateResponse(response) {
  const wire = responseToWire(response)
  validate(responseValidator, wire)
  const { declarations, outputs } = wire.content
  invariant(new Set(declarations.map(o => o.name)).size === declarations.length &&
    new Set(outputs.map(o => o.name)).size === outputs.length && outputs.length === declarations.length,
  "Saved output names do not match the declarations.", "OUTPUT_VALIDATION_FAILED")
  for (const declaration of declarations) {
    const output = outputs.find(o => o.name === declaration.name)
    invariant(output?.type === declaration.type, `Missing or incompatible output: ${declaration.name}`, "OUTPUT_VALIDATION_FAILED")
    if (output.type === "text") invariant(output.format === (declaration.format ?? "plain"),
      `Text format changed for ${output.name}.`, "OUTPUT_VALIDATION_FAILED")
    if (output.type === "json") {
      const check = validator().compile(declaration.schema)
      invariant(check(output.value), `JSON output ${output.name} does not match its schema.`, "OUTPUT_VALIDATION_FAILED")
    }
    if (output.type === "table") {
      invariant(canonical(normalizedDeclarations([declaration])[0].schema) === canonical(normalizedDeclarations([output])[0].schema),
        `Table ${output.name} has a different column schema.`, "OUTPUT_VALIDATION_FAILED")
      if (output.source) invariant(output.source.execution_id === wire.primary_execution_id && !!wire.study_id &&
        output.source.field_ids.length === output.schema.length &&
        new Set(output.source.field_ids).size === output.source.field_ids.length && output.source.field_ids.every(Boolean),
      `Table ${output.name} belongs to another execution or projection.`, "OUTPUT_VALIDATION_FAILED")
      for (const row of output.rows ?? []) {
        invariant(row.length === declaration.schema.length, `Table ${output.name} has an incomplete row.`, "OUTPUT_VALIDATION_FAILED")
        row.forEach((cell, index) => {
          const col = declaration.schema[index]
          let valid = cell === null ? col.nullable === true : typeof cell === "string"
          if (cell !== null && col.type === "float64") valid = typeof cell === "number" && Number.isFinite(cell)
          if (cell !== null && col.type === "boolean") valid = typeof cell === "boolean"
          if (cell !== null && col.type === "int64") valid = typeof cell === "string" && /^-?(0|[1-9][0-9]*)$/.test(cell) &&
            BigInt(cell) >= -(2n ** 63n) && BigInt(cell) < 2n ** 63n
          if (cell !== null && ["date", "datetime"].includes(col.type)) {
            const dateCheck = validator().compile({ type: "string", format: col.type === "date" ? "date" : "date-time" })
            valid = dateCheck(cell)
          }
          invariant(valid, `Table ${output.name}: invalid value in ${col.name}.`, "OUTPUT_VALIDATION_FAILED")
        })
      }
    }
  }
  invariant((wire.primary_execution_id === undefined) === (wire.study_id === undefined),
    "The answer has incomplete execution identity.", "OUTPUT_VALIDATION_FAILED")
  invariant(!wire.response_plan || wire.primary_execution_id !== undefined,
    "A response plan requires its source execution.", "OUTPUT_VALIDATION_FAILED")
  invariant(!wire.content.qualifications?.length || !!wire.response_plan,
    "Computed qualifications require their saved response plan.", "OUTPUT_VALIDATION_FAILED")
  if (wire.extension) invariant(wire.extension.execution_id === wire.primary_execution_id && wire.extension.study_id === wire.study_id,
    "The answer differs from its native output provenance.", "OUTPUT_VALIDATION_FAILED")
  return response
}

export function operationId(value) {
  invariant(typeof value === "string" && /^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$/.test(value),
    "Use an operation ID of 1–128 letters, numbers, hyphens or underscores, starting with a letter or number.", "VALIDATION_ERROR")
  return value
}

export function statusCode(error) { return error?.statusCode ?? error?.status ?? error?.response?.status }
export function throwNativeError(record) {
  if (record.error) throw new EpochError(record.error.error.code, record.error.error.message, { record })
}
