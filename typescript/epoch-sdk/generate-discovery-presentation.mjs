import { readFile, writeFile } from 'node:fs/promises'
import { compile } from 'json-schema-to-typescript'
const source = new URL('../../contracts/discovery-presentation-v1.schema.json', import.meta.url)
const bytes = await readFile(source, 'utf8'), schema = JSON.parse(bytes)
const output = await compile({ ...schema.definitions.DiscoveryPresentationProtocol, definitions: schema.definitions }, 'DiscoveryPresentationProtocol', {
  bannerComment: '/* Generated from contracts/discovery-presentation-v1.schema.json. Do not edit. */', additionalProperties: false,
})
const declaration = new URL('./discovery-presentation-wire.d.ts', import.meta.url)
const snapshot = new URL('./discovery-presentation.schema.json', import.meta.url)
const types = new URL('./discovery-presentation.d.ts', import.meta.url)
const names = Object.keys(schema.definitions.DiscoveryPresentationProtocol.properties)
const aliases = `/* Generated from contracts/discovery-presentation-v1.schema.json. Do not edit. */
import type { DiscoveryPresentationProtocol as Wire } from './discovery-presentation-wire.js'
type Camel<S extends string> = S extends \`\${infer First}_\${infer Rest}\` ? \`\${First}\${Capitalize<Camel<Rest>>}\` : S
type Decoded<T> = T extends readonly (infer V)[] ? Decoded<V>[] : T extends object ? { [K in keyof T as K extends string ? Camel<K> : K]: Decoded<T[K]> } : T
export type DiscoveryPresentationModels = { [K in keyof Wire]: Decoded<Wire[K]> }
${names.map(name => `export type ${name} = DiscoveryPresentationModels['${name}']`).join('\n')}
export function parseDiscoveryPresentation<K extends keyof DiscoveryPresentationModels>(name: K, value: unknown): DiscoveryPresentationModels[K]
export function serializeDiscoveryPresentation<K extends keyof DiscoveryPresentationModels>(name: K, value: DiscoveryPresentationModels[K]): Wire[K]
`
if (process.argv.includes('--check')) {
  if (await readFile(snapshot, 'utf8') !== bytes || await readFile(declaration, 'utf8') !== output || await readFile(types, 'utf8') !== aliases) throw new Error('Regenerate discovery presentation types')
} else {
  await writeFile(snapshot, bytes)
  await writeFile(declaration, output)
  await writeFile(types, aliases)
}
