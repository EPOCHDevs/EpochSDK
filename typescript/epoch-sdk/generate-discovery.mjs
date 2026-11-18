import {readFile,writeFile} from 'node:fs/promises'
import {compile} from 'json-schema-to-typescript'
const schema=JSON.parse(await readFile(new URL('./discovery.schema.json',import.meta.url),'utf8'))
const value=await compile({...schema.definitions.PublicDiscoveryProtocol,definitions:schema.definitions},'PublicDiscoveryProtocol',{bannerComment:'/* Generated from Platform contracts/discovery-v4.schema.json. Do not edit. */',additionalProperties:false})
const target=new URL('./discovery-types.d.ts',import.meta.url)
if(process.argv.includes('--check')){if(await readFile(target,'utf8')!==value)throw new Error('Regenerate discovery types')}else await writeFile(target,value)
