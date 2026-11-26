// Generated Platform presentation client HTTP checks, not live acceptance.
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {readFileSync} from 'node:fs';
import test from 'node:test';
import {EpochPresentationsClient,EpochPresentations} from '@epochdevs/epoch-sdk/presentation-api';

const fixture=name=>JSON.parse(readFileSync(new URL(`../../../contracts/fixtures/platform-presentations/${name}.json`,import.meta.url),'utf8'));
const request=()=>({executionCategory:'ALL'});
const client=()=>new EpochPresentationsClient({environment:'https://platform.test',token:'fixture-token'});
async function withFetch(reply,scenario){
 const previous=globalThis.fetch,seen=[];
 globalThis.fetch=async(url,init)=>{seen.push({url:String(url),init});const [status,body,headers]=await reply(String(url),init);return new Response(JSON.stringify(body),{status,headers:{'content-type':'application/json',...headers}});};
 try{await scenario(seen);}finally{globalThis.fetch=previous;}
}
const sha=text=>createHash('sha256').update(text).digest('hex');

test('pending/retained/null raw documents cross actual SDK aliases with exact UTF8 hashes',async()=>{
 for(const name of ['pending-delivery','retained-delivery','absent-response-delivery','literal-null-delivery']){
  const wire=fixture(name);
  await withFetch((url,init)=>{
   assert.equal(new URL(url).pathname,'/api/v1/contexts/executions/fixture-run/presentation/delivery');
   assert.equal(init.method,'POST');assert.equal(init.headers.Authorization,'Bearer fixture-token');
   assert.deepEqual(JSON.parse(init.body),fixture('initial-request'));
   return[200,{...wire,future_server_field:{keep:true}}];
  },async seen=>{
   const value=await client().readFinalPresentationDelivery('fixture-run',request(),{maxRetries:0});
   assert.equal(seen.length,1);assert.equal(value.schemaVersion,2);assert.equal(value.retention.state,wire.retention.state);
   assert.equal(value.content.dashboardJson,wire.content.dashboard_json);
   assert.equal(value.content.canonicalProseJson,wire.content.canonical_prose_json);
   assert.equal(value.content.responseJson,wire.content.response_json);
   assert.equal(sha(value.content.dashboardJson),value.source.schemaSha256);
   assert.equal(sha(value.content.canonicalProseJson),value.source.proseSha256);
   assert.equal(value.content.responseJson===null?null:sha(value.content.responseJson),value.source.responseSha256);
   assert.equal(value.artifacts[0].url,wire.artifacts[0].url);
   assert.equal(value.responseTables[0].parts[0].url,wire.response_tables[0].parts[0].url);
   assert.deepEqual(value.future_server_field,{keep:true});
  });
 }
});

test('renewal carries exact selected source/reference through source-generated serialization',()=>withFetch((_url,init)=>{
 assert.deepEqual(JSON.parse(init.body),fixture('renewal-request'));return[200,fixture('retained-delivery')];
},async()=>{
 const wire=fixture('renewal-request'),s=wire.expected_source,p=wire.retained_reference;
 const expectedSource={executionId:s.execution_id,definitionId:s.definition_id,executionCategory:s.execution_category,
  configSha256:s.config_sha256,generationSha256:s.generation_sha256,schemaSha256:s.schema_sha256,
  proseSha256:s.prose_sha256,runOutputManifestSha256:s.run_output_manifest_sha256,responseSha256:s.response_sha256};
 await client().readFinalPresentationDelivery('fixture-run',{executionCategory:'ALL',expectedSource,
  retainedReference:{executionId:p.execution_id,publicationId:p.publication_id,catalogRevision:p.catalog_revision,editVersion:p.edit_version},
  maxExpiresEpoch:wire.max_expires_epoch},{maxRetries:0});
}));

test('invalid or extra source-owned request data cannot reach HTTP',()=>withFetch(()=>assert.fail('Invalid request reached HTTP'),async()=>{
 const source=Object.fromEntries(Object.entries(fixture('renewal-request').expected_source).map(([key,value])=>[key.replace(/_([a-z])/g,(_match,letter)=>letter.toUpperCase()),value]));
 const bad=[{executionCategory:''},{executionCategory:'ALL',unexpected:true},{executionCategory:'ALL',expectedSource:null},
  {executionCategory:'ALL',maxExpiresEpoch:true},{executionCategory:'ALL',maxExpiresEpoch:-1},{executionCategory:'ALL',maxExpiresEpoch:9007199254740992},
  {executionCategory:'ALL',expectedSource:{...source,configSha256:'latest'}},{executionCategory:'ALL',expectedSource:{...source,unexpected:'not owned'}}];
 for(const value of bad)await assert.rejects(client().readFinalPresentationDelivery('fixture-run',value,{maxRetries:0}));
}));

test('all declared errors preserve body/status/Retry-After without retries or replacement reads',async()=>{
 const errors={400:'BadRequestError',401:'UnauthorizedError',403:'ForbiddenError',404:'NotFoundError',409:'ConflictError',410:'GoneError',413:'ContentTooLargeError',425:'TooEarlyError',503:'ServiceUnavailableError',504:'GatewayTimeoutError'};
 for(const status of [400,401,403,404,409,410,413,425,503,504])await withFetch(()=>[status,fixture('error'),{'Retry-After':'1'}],async seen=>{
  await assert.rejects(client().readFinalPresentationDelivery('fixture-run',request(),{maxRetries:0}),error=>{
   assert.equal(error.statusCode,status);assert.equal(error.body.message,fixture('error').message);
   assert.ok(error instanceof EpochPresentations[errors[status]]);
   assert.equal(error.rawResponse.headers.get('retry-after'),'1');return true;
  });assert.equal(seen.length,1);
 });
});

test('source version, retention discriminator and required-null fields stay exact',async()=>{
 for(const change of ['version','retention','missing-null']){
  const value=fixture('absent-response-delivery');
  if(change==='version')value.schema_version=3;
  else if(change==='retention')value.retention={state:'invented'};
  else delete value.content.response_json;
  await withFetch(()=>[200,value],async()=>{await assert.rejects(client().readFinalPresentationDelivery('fixture-run',request(),{maxRetries:0}));});
 }
});

test('abort stops the generated read without a second operation',async()=>{
 const previous=globalThis.fetch,controller=new AbortController();let started,count=0;
 const seen=new Promise(resolve=>{started=resolve;});
 globalThis.fetch=(_url,init)=>{count++;started();return new Promise((_resolve,reject)=>{init.signal.addEventListener('abort',()=>reject(init.signal.reason),{once:true});});};
 try{
  const pending=client().readFinalPresentationDelivery('fixture-run',request(),{maxRetries:0,timeoutInSeconds:0.1,abortSignal:controller.signal});
  await seen;controller.abort(new Error('owner changed'));await assert.rejects(pending);assert.equal(count,1);
 }finally{globalThis.fetch=previous;}
});
