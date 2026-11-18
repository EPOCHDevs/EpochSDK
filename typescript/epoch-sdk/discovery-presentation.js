import Ajv from 'ajv'
import addFormats from 'ajv-formats'
import schema from './discovery-presentation.schema.json' with { type: 'json' }

const ajv = new Ajv({ strict: false, allowUnionTypes: true })
addFormats(ajv)
const checks = new Map()
const camel = key => key.replace(/_([a-z])/g, (_match, char) => char.toUpperCase())
function check(shape, value) {
  let test = checks.get(shape)
  if (!test) { test = ajv.compile({ ...shape, definitions: schema.definitions }); checks.set(shape, test) }
  return test(value)
}
function transform(shape, value, encode) {
  if (shape.$ref) return transform(schema.definitions[shape.$ref.split('/').pop()], value, encode)
  const choices = shape.oneOf ?? shape.anyOf
  if (choices) {
    for (const choice of choices) {
      const candidate = encode ? transform(choice, value, true) : value
      if (check(choice, candidate)) return encode ? candidate : transform(choice, value, false)
    }
    return value
  }
  if (Array.isArray(value)) return value.map(item => transform(shape.items ?? {}, item, encode))
  if (!value || typeof value !== 'object') return value
  const properties = shape.properties ?? {}
  const names = new Map(Object.keys(properties).map(key => [encode ? camel(key) : key, key]))
  return Object.fromEntries(Object.entries(value).filter(([, item]) => item !== undefined).map(([key, item]) => {
    const wire = names.get(key)
    const child = wire === undefined ? shape.additionalProperties : properties[wire]
    return [wire === undefined ? key : encode ? wire : camel(wire), child && typeof child === 'object' ? transform(child, item, encode) : item]
  }))
}
function root(name) {
  const property = schema.definitions.DiscoveryPresentationProtocol.properties
  if (!Object.hasOwn(property, name)) throw new TypeError('Unknown discovery presentation model')
  return property[name]
}
/** Decode saved activity or a Platform/GDS directory. This module has no HTTP/search methods. */
export function parseDiscoveryPresentation(name, value) {
  const shape = root(name)
  if (!check(shape, value)) throw new TypeError('Invalid discovery presentation: ' + name)
  return transform(shape, value, false)
}
/** Serialize only the same closed presentation model, for a preserved request or fixture. */
export function serializeDiscoveryPresentation(name, value) {
  const shape = root(name), wire = transform(shape, value, true)
  if (!check(shape, wire)) throw new TypeError('Invalid discovery presentation: ' + name)
  return wire
}
