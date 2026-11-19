import assert from 'node:assert/strict'
import test from 'node:test'
import { readFile } from 'node:fs/promises'
import { createHash } from 'node:crypto'
import { PlatformFilesClient, PlatformFileError, StorageTransferError, putSigned } from '../files.js'
const fixture = async name => JSON.parse(await readFile(new URL(`../../../contracts/fixtures/platform-files/${name}.json`, import.meta.url)))
const saved = await fixture('version'), request = await fixture('save'), grid = await fixture('grid')
const original = saved.original_file_ref, pin = saved.file.file_ref
const json = (body, status = 200, headers = {}) => new Response(JSON.stringify(body), { status, headers })
const client = handler => new PlatformFilesClient({ apiUrl: 'https://api.test', token: 'fixture', fetch: handler })
// A Platform without signed storage links: the edit stays in the save request.
const inline = handler => async (url, init) => String(url).endsWith('/edit-uploads')
  ? json({ error: 'FILE_DIRECT_TRANSFER_UNAVAILABLE', message: 'Inline here' }, 409) : handler(url, init)

test('exact numeric tokens and a stable body survive an explicit retry; no automatic mutation retry', async () => {
  const calls = []
  let tokens = 0
  const files = new PlatformFilesClient({ apiUrl: 'https://api.test', token: async () => `fresh${++tokens}`, fetch: inline(async (url, init) => {
    calls.push({url, ...init})
    assert.equal(init.redirect, 'error')
    return calls.length === 1 ? json({error: 'FILE_EDIT_BUSY', message: 'Busy'}, 503, {'Retry-After':'2'}) : json(saved)
  }) })
  await assert.rejects(files.save(original, request), e => e instanceof PlatformFileError && e.code === 'FILE_EDIT_BUSY' && e.retryAfter === '2')
  assert.equal(calls.length, 1)
  assert.equal((await files.save(original, request)).file.file_ref, pin)
  assert.equal(calls[0].body, calls[1].body)
  assert.equal(JSON.parse(calls[1].body).edit.changes[0].value.value, '9007199254740993')
  assert.deepEqual(calls.map(c=>c.headers.Authorization), ['Bearer fresh2', 'Bearer fresh4']) // Each after its link request.
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
  for (const body of bodies) await assert.rejects(client(inline(async()=>json(body))).save(original,request),/inconsistent file version|another save generation|invalid FileVersion/)
})
// Platform with signed storage links, and the storage they point to.
function staging({ refusals = 0 } = {}) {
  const state = { api: [], puts: [], links: 0 }
  state.files = new PlatformFilesClient({ apiUrl: 'https://api.test', token: 'fixture',
    fetch: async (url, init) => {
      state.api.push({ url: String(url), ...init })
      const body = JSON.parse(init.body)
      if (String(url).endsWith('/edit-uploads')) {
        state.links++
        state.linkRequest = body
        return json({ url: `https://storage.test/staged?X-Amz-Signature=secret${state.links}`, method: 'PUT',
          headers: { 'content-type': 'application/json', 'x-amz-checksum-sha256': 'checksum' }, size_bytes: body.size_bytes, expires_at: '2026-11-19T12:15:00.000Z' })
      }
      state.saved = body
      return json(saved)
    },
    storageFetch: async (url, init) => {
      state.puts.push({ url, ...init })
      assert.equal(init.headers.Authorization, undefined) // API credentials never reach storage.
      assert.equal(init.credentials, 'omit')
      assert.deepEqual(init.headers, { 'content-type': 'application/json', 'x-amz-checksum-sha256': 'checksum' })
      return state.puts.length <= refusals ? new Response('<Error><Code>AccessDenied</Code></Error>', { status: 403 }) : new Response(null, { status: 200 })
    } })
  return state
}
test('a save puts its edit through a signed link and names it, so no file text crosses the API', async () => {
  const state = staging()
  assert.equal((await state.files.save(original, request)).file.file_ref, pin)
  const staged = state.puts[0].body
  assert.deepEqual(JSON.parse(new TextDecoder().decode(staged)), request.edit)
  const upload = { size_bytes: staged.byteLength, content_sha256: createHash('sha256').update(staged).digest('hex') }
  assert.deepEqual(state.linkRequest, { request_id: request.request_id, ...upload })
  const { edit: _edit, ...metadata } = request
  assert.deepEqual(state.saved, { ...metadata, edit_upload: upload })
})
test('putSigned takes a generated client link and refuses one signed for other bytes', async () => {
  const puts = []
  const body = new Blob(['part'])
  const link = { url: 'https://storage.test/p?X-Amz-Signature=s', method: 'PUT', headers: { 'x-amz-checksum-sha256': 'c' }, sizeBytes: 4, expiresAt: '2026-11-19T12:15:00.000Z' }
  await putSigned(async (url, init) => { puts.push({ url, ...init }); return new Response(null, { status: 200 }) }, async () => link, body)
  assert.equal(puts.length, 1)
  assert.equal(puts[0].body, body)
  await assert.rejects(putSigned(async () => assert.fail('PUT'), async () => ({ ...link, sizeBytes: 5 }), body), /different file transfer/)
})
test('a refused put asks for one new link, then fails without exposing it', async () => {
  const once = staging({ refusals: 1 })
  await once.files.save(original, request)
  assert.equal(once.links, 2)
  assert.match(once.puts[1].url, /secret2$/)
  const twice = staging({ refusals: 2 })
  await assert.rejects(twice.files.save(original, request), e => e instanceof StorageTransferError && e.status === 403 && !e.message.includes('secret'))
  assert.equal(twice.saved, undefined)
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

test('native document DTOs preserve exact positions, outlines and passage identity', async () => {
  const read=await fixture('document_read'),page=await fixture('document_page'),passage=await fixture('document_passage')
  const originalBytes=await readFile(new URL('../../../contracts/fixtures/platform-files/document-original.txt',import.meta.url))
  const files=client(async(url,init)=> {
    if(url.endsWith('/reads')) { assert.deepEqual(JSON.parse(init.body),{file_ref:read.source.file_ref});return json(read) }
    if(url.includes('/reads/')) return json(read)
    return json(new URL(url).pathname.endsWith('/blocks')?page:passage)
  })
  assert.equal((await files.beginDocumentRead(read.source.file_ref)).outline[0].text,'Résumé')
  assert.equal((await files.documentRead(read.read_ref)).read_ref,read.read_ref)
  const content=await files.documentContent(page.document_version_ref)
  const {block}=await files.documentPassage(page.document_version_ref,content.blocks[0].block_ref)
  assert.equal(originalBytes.subarray(block.start_byte,block.start_byte+block.length).toString(),block.text)
  for(const mutate of [value=>value.offset++,value=>value.blocks[0].length=1,value=>delete value.blocks[0].length]) {
    const invalid=structuredClone(page);mutate(invalid)
    await assert.rejects(client(async()=>json(invalid)).documentContent(page.document_version_ref),/inconsistent/)
  }
  const forbidden=new PlatformFilesClient({apiUrl:'https://api.test',token:()=>assert.fail('auth called'),fetch:()=>assert.fail('HTTP called')})
  await assert.rejects(forbidden.documentContent(page.document_version_ref+'\n'),TypeError)
  await assert.rejects(forbidden.documentContent(page.document_version_ref,{offset:-1}),TypeError)
  await assert.rejects(forbidden.documentPassage(page.document_version_ref,block.block_ref+'\n'),TypeError)
})
