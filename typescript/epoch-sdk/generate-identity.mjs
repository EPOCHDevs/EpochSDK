import { readFile, writeFile } from 'node:fs/promises'
import { compile } from 'json-schema-to-typescript'
const source = new URL('../../contracts/asset-identity-v1.schema.json', import.meta.url)
const bytes = await readFile(source, 'utf8')
const schema = JSON.parse(bytes)
const target = new URL('./identity-wire.d.ts', import.meta.url)
const snapshot = new URL('./asset-identity.schema.json', import.meta.url)
const output = await compile({ ...schema.definitions.AssetIdentityProtocol, definitions: schema.definitions }, 'AssetIdentityProtocol', {
  bannerComment: '/* Generated from contracts/asset-identity-v1.schema.json. Do not edit. */', additionalProperties: false,
})
if (process.argv.includes('--check')) {
  if (await readFile(snapshot, 'utf8') !== bytes || await readFile(target, 'utf8') !== output) throw new Error('Regenerate identity types')
} else {
  await writeFile(snapshot, bytes)
  await writeFile(target, output)
}
