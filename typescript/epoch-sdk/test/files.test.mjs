import assert from 'node:assert/strict'
import test from 'node:test'
import { readFile } from 'node:fs/promises'
import { PlatformFilesClient, PlatformFileError } from '../files.js'
const fixture = async name => JSON.parse(await readFile(new URL(`../../../contracts/fixtures/platform-files/${name}.json`, import.meta.url)))
const saved = await fixture('version'), request = await fixture('save'), grid = await fixture('grid')
const original = saved.original_file_ref, pin = saved.file.file_ref
const json = (body, status = 200, headers = {}) => new Response(JSON.stringify(body), { status, headers })
const client = handler => new PlatformFilesClient({ apiUrl: 'https://api.test', token: 'fixture', fetch: handler })

test('exact numeric tokens and a stable body survive an explicit retry; no automatic mutation retry', async () => {
  const calls = []
  let tokens = 0
  const files = new PlatformFilesClient({ apiUrl: 'https://api.test', token: async () => `fresh${++tokens}`, fetch: async (url, init) => {
    calls.push({url, ...init})
    assert.equal(init.redirect, 'error')
    return calls.length === 1 ? json({error: 'FILE_EDIT_BUSY', message: 'Busy'}, 503, {'Retry-After':'2'}) : json(saved)
  } })
  await assert.rejects(files.save(original, request), e => e instanceof PlatformFileError && e.code === 'FILE_EDIT_BUSY' && e.retryAfter === '2')
  assert.equal(calls.length, 1)
  assert.equal((await files.save(original, request)).file.file_ref, pin)
  assert.equal(calls[0].body, calls[1].body)
  assert.equal(JSON.parse(calls[1].body).edit.changes[0].value.value, '9007199254740993')
  assert.deepEqual(calls.map(c=>c.headers.Authorization), ['Bearer fresh1', 'Bearer fresh2'])
})
test('invalid saves fail before token/HTTP; newline reference is not exact', async () => {
  const files = new PlatformFilesClient({apiUrl:'https://api.test', token:()=>assert.fail('auth called'), fetch:()=>assert.fail('HTTP called')})
  const changes = [b=>{b.base_version=true}, b=>{b.request_id='é'.repeat(65)}, b=>{b.edit.changes[0].value.value=9007199254740993}, b=>{b.edit.changes[0].value.value='NaN'}, b=>{b.edit.unexpected=true}]
  for (const change of changes) {
    const body=structuredClone(request); change(body)
    await assert.rejects(files.save(original,body), TypeError)
  }
  await assert.rejects(files.latest(`${original}\n`),TypeError)
})
test('wrong family, hash, generation or unknown response field is rejected', async () => {
  const bodies = [{...saved,original_file_ref:`file:${'c'.repeat(64)}`},{...saved,version:2},{...saved,unexpected:'private'}, {...saved,file:{...saved.file,content_sha256:'c'.repeat(64)}}]
  for (const body of bodies) await assert.rejects(client(async()=>json(body)).save(original,request),TypeError)
})
test('grid keeps typed precision and content is a streamed ranged response', async () => {
  const files=client(async(url,init)=> {
    if(url.endsWith('/content')) {
      assert.equal(init.headers.Range,'bytes=2-5');assert.equal(init.headers['If-Range'],'"hash"')
      return new Response('2345',{status:206,headers:{'Content-Range':'bytes 2-5/10'}})
    }
    return json(grid)
  })
  assert.equal((await files.grid(pin,{schema_version:1,format:'parquet',offset:201,limit:1})).rows[0][0].value.value,'9007199254740993')
  const response=await files.content(pin,{byteRange:'bytes=2-5',ifRange:'"hash"'})
  assert.equal(response.status,206);assert.equal(response.headers.get('content-range'),'bytes 2-5/10');assert.equal(await response.text(),'2345')
})
test('history ordering and cursor cannot silently change version identity', async () => {
  await assert.rejects(client(async()=>json({items:[saved,saved]})).history(original),/unordered/)
  await assert.rejects(client(async()=>json({items:[saved],next_before:2})).history(original),/cursor/)
  assert.equal((await client(async()=>json({items:[saved],next_before:1})).history(original)).items.length,1)
})
test('credentials stay out of redirects and invalid ranges fail before auth', async () => {
  let calls=0
  await assert.rejects(client(async()=>{calls++;return new Response(null,{status:307,headers:{Location:'https://other.test'}})}).latest(original),e=>e instanceof PlatformFileError && e.status===307)
  assert.equal(calls,1)
  const files=new PlatformFilesClient({apiUrl:'https://api.test',token:()=>assert.fail('auth called'),fetch:()=>assert.fail('HTTP called')})
  await assert.rejects(files.content(pin,{byteRange:'bytes=0-1,4-5'}),TypeError)
})

test('PNG image pages stay separate from the existing PDF preview contract', async () => {
  const ready={state:'ready',media_type:'image/png',converter_version:'raster-png-v1',size_bytes:8,pages:[{page:1,width:2,height:2,size_bytes:4,content_sha256:'b'.repeat(64)},{page:2,width:2,height:2,size_bytes:4,content_sha256:'c'.repeat(64)}]}
  const files=client(async(url)=>url.endsWith('/content')?new Response('page',{status:200}):json(url.endsWith('/image-preview')?ready:{state:'none'}))
  assert.equal((await files.imagePreview(original)).pages.length,2)
  assert.equal((await files.preview(original)).state,'none')
  assert.equal(await(await files.content(original,{imagePage:2})).text(),'page')
  await assert.rejects(files.content(original,{imagePage:0}),TypeError)
  await assert.rejects(files.content(original,{imagePage:1,preview:true}),TypeError)
  await assert.rejects(client(async()=>json({...ready,size_bytes:9})).imagePreview(original),/inconsistent/)
})
