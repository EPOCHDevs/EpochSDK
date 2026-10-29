// Schema-bearing keywords from JSON Schema 2020-12, matching json_schema.py.
// Annotation data (including examples and properties named "$ref") is not a schema resource.
const singles = ["additionalProperties", "contains", "contentSchema", "else", "if", "items", "not", "propertyNames", "then", "unevaluatedItems", "unevaluatedProperties"]
const arrays = ["allOf", "anyOf", "oneOf", "prefixItems"]
const maps = ["$defs", "definitions", "dependentSchemas", "patternProperties", "properties"]
const rootId = "https://schemas.epoch.invalid/output-schema"
const dialect = "https://json-schema.org/draft/2020-12/schema"

/** Validate every local reference, including unused branches, without retrieving anything. */
export function compileJsonSchema(schema, validator) {
  JSON.stringify(schema, (_key, value) => {
    if (typeof value === "number" && !Number.isFinite(value)) throw new Error("JSON Schema numbers must be finite")
    return value
  })
  if (!validator.validateSchema(schema)) throw new Error(validator.errorsText())
  const resources = new Map([[rootId, schema]])
  const anchors = new Map()
  const nodes = []
  const own = (value, key) => value !== null && typeof value === "object" && Object.hasOwn(value, key)
  function walk(value, base) {
    if (typeof value === "boolean") return
    if (value === null || typeof value !== "object" || Array.isArray(value)) throw new Error("JSON Schema must be an object or boolean")
    if (value.$schema !== undefined && value.$schema !== dialect) throw new Error("Use the JSON Schema 2020-12 dialect")
    if (value.$id !== undefined) {
      base = validator.opts.uriResolver.resolve(base, value.$id).replace(/#$/, "")
      resources.set(base, value)
    }
    for (const keyword of ["$anchor", "$dynamicAnchor"]) {
      if (value[keyword] !== undefined) anchors.set(`${base}#${value[keyword]}`, value)
    }
    nodes.push({ value, base })
    for (const key of singles) if (own(value, key)) walk(value[key], base)
    for (const key of arrays) if (own(value, key)) for (const child of value[key]) walk(child, base)
    for (const key of maps) if (own(value, key)) for (const child of Object.values(value[key])) walk(child, base)
  }
  walk(schema, rootId)
  for (const { value, base } of nodes) {
    for (const keyword of ["$ref", "$dynamicRef"]) {
      if (!own(value, keyword)) continue
      const ref = value[keyword]
      if (typeof ref !== "string" || (ref !== "" && !ref.startsWith("#"))) throw new Error("JSON Schema references must stay within the supplied schema")
      const fragment = decodeURIComponent(ref.slice(1))
      let target = resources.get(base)
      if (fragment.startsWith("/")) {
        for (const token of fragment.slice(1).split("/")) {
          const key = token.replaceAll("~1", "/").replaceAll("~0", "~")
          if (!own(target, key)) throw new Error(`Unresolved JSON Schema reference: ${ref}`)
          target = target[key]
        }
      } else if (fragment) target = anchors.get(`${base}#${fragment}`)
      if (typeof target !== "boolean" && (target === null || typeof target !== "object" || Array.isArray(target))) throw new Error(`JSON Schema reference must identify a schema: ${ref}`)
    }
  }
  return validator.compile(schema)
}
