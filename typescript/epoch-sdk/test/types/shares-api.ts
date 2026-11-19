import { EpochSharesClient, type EpochShares } from '@epochdevs/epoch-sdk/shares-api';
const client = new EpochSharesClient({ environment: 'https://platform.test', token: 'fixture' });
void client.studiesShares.changeWhoCanOpenAShareLink('share-1', { expectedAccessVersion: 0 });
void client.studiesShares.selectPublishedShareVersion('share-1', { snapshotVersion: 1, expectedCurrentVersion: 3 });
// @ts-expect-error Access compare-and-set is required.
void client.studiesShares.changeWhoCanOpenAShareLink('share-1', {});
// @ts-expect-error Current-version compare-and-set is required.
void client.studiesShares.selectPublishedShareVersion('share-1', { snapshotVersion: 1 });
function counts(version: EpochShares.ShareVersionsResponseVersionsItem): number | string {
  if (version.available) return version.messageCount + version.runCount;
  return version.reason;
}
void counts;
