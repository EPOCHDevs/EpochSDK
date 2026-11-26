import {EpochPresentationsClient, EpochPresentations} from '@epochdevs/epoch-sdk/presentation-api';

const client=new EpochPresentationsClient({environment:'https://platform.test',token:'token'});
async function example(){
 const value=await client.readFinalPresentationDelivery('fixture-run',{executionCategory:'ALL'},{maxRetries:0});
 const version:2=value.schemaVersion;
 const raw:string=value.content.dashboardJson;
 const response:string|null=value.content.responseJson;
 if(value.retention.state==='retained'){
  const pin:string=value.retention.reference.catalogRevision;
  return{version,raw,response,pin};
 }
 // @ts-expect-error A pending delivery has no accepted retained reference.
 value.retention.reference;
 const selected:EpochPresentations.FinalPresentationSource=value.source;
 return{version,raw,response,selected};
}
void example;
