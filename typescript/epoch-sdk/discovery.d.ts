import type { DiscoveryInput, DiscoveryResult, SelectedInputs, DiscoveryDetails, ScreenInput, AssetUniverseResult, UniversePageRequest, UniversePage, AssetLookupResult, UniverseBinding } from './discovery-types.js'
export type * from './discovery-types.js'
export declare class CatalogueHTTPError extends Error { readonly status: number; readonly body: string }
export interface DiscoveryOptions { signal?: AbortSignal }
export declare class CatalogueClient {
  constructor(options: { baseUrl: string; token: string | (() => string | Promise<string>); fetch?: typeof fetch })
  search(input: DiscoveryInput, options?: DiscoveryOptions): Promise<DiscoveryResult>
  select(sessionId: string, ids: string[], options?: DiscoveryOptions): Promise<SelectedInputs>
  details(sessionId: string, ids: string[], options?: DiscoveryOptions): Promise<DiscoveryDetails>
  selection(id: string, options?: DiscoveryOptions): Promise<SelectedInputs>
  screen(input: ScreenInput, options?: DiscoveryOptions): Promise<AssetUniverseResult>
  universePage(input: UniversePageRequest, options?: DiscoveryOptions): Promise<UniversePage>
  resolveAssets(assetIds: string[], options?: DiscoveryOptions): Promise<AssetLookupResult>
  bindUniverse(universeRef: string, options?: DiscoveryOptions): Promise<UniverseBinding>
}
