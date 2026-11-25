import { EpochModelsClient } from '@epochdevs/epoch-sdk/models-api';

const models = new EpochModelsClient({ environment: 'https://platform.test', token: 'token' });
async function examples() {
  const saved = await models.saveModel({ requestId: 'explicit-save', name: 'OLS', executionId: 'run',
    fitName: 'fit', expectedDigest: `sha256:${'a'.repeat(64)}` });
  const page = await models.listModels({ limit: 1 });
  const detail = await models.readModel(saved.modelRef);
  const pins: string[] = [saved.digest, saved.manifestSha256, detail.model.manifestSha256];
  return { page, detail, pins };
}
void examples;
