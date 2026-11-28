import { ResearchOperationsClient } from '../../research-operations.js'
import { parseRequest } from '../../index.js'
const operations = new ResearchOperationsClient({ baseUrl: 'https://platform.invalid', token: async () => 'token' })
const request = parseRequest({ task: 'Explain', outputs: [{ name: 'answer', type: 'text', instructions: 'Explain' }] })
void operations.createSdkRequest({ request }).then(record => {
  const mode: 'interactive' | 'one_shot' = record.interaction
  void mode
})
// @ts-expect-error Caller cannot write an interaction policy in the lifecycle body.
void operations.updateSdkRequest('req_one', { expectedVersion: 0, interaction: 'one_shot' })
// @ts-expect-error Native execution admission remains on the native SDK.
void operations.getSdkExecutionRequest('req_one')
