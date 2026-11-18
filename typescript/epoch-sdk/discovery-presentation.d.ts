/* Generated from contracts/discovery-presentation-v1.schema.json. Do not edit. */
import type { DiscoveryPresentationProtocol as Wire } from './discovery-presentation-wire.js'
type Camel<S extends string> = S extends `${infer First}_${infer Rest}` ? `${First}${Capitalize<Camel<Rest>>}` : S
type Decoded<T> = T extends readonly (infer V)[] ? Decoded<V>[] : T extends object ? { [K in keyof T as K extends string ? Camel<K> : K]: Decoded<T[K]> } : T
export type DiscoveryPresentationModels = { [K in keyof Wire]: Decoded<Wire[K]> }
export type AssetScreen = DiscoveryPresentationModels['AssetScreen']
export type AssetUniverseResponse = DiscoveryPresentationModels['AssetUniverseResponse']
export type DatasetBrowseGroup = DiscoveryPresentationModels['DatasetBrowseGroup']
export type DatasetCatalogEntry = DiscoveryPresentationModels['DatasetCatalogEntry']
export type DatasetCatalogResponse = DiscoveryPresentationModels['DatasetCatalogResponse']
export type DatasetCatalogRequest = DiscoveryPresentationModels['DatasetCatalogRequest']
export type DatasetCatalogSummary = DiscoveryPresentationModels['DatasetCatalogSummary']
export type DatasetSearchDataset = DiscoveryPresentationModels['DatasetSearchDataset']
export type DatasetSearchQuery = DiscoveryPresentationModels['DatasetSearchQuery']
export type DatasetSearchSubject = DiscoveryPresentationModels['DatasetSearchSubject']
export type DatasetSearchRequest = DiscoveryPresentationModels['DatasetSearchRequest']
export type DatasetSourceMetadataResponse = DiscoveryPresentationModels['DatasetSourceMetadataResponse']
export type DiscoveryDatasetRequest = DiscoveryPresentationModels['DiscoveryDatasetRequest']
export type DiscoveryLoaderBinding = DiscoveryPresentationModels['DiscoveryLoaderBinding']
export type DiscoveryMetadataRecord = DiscoveryPresentationModels['DiscoveryMetadataRecord']
export type DiscoveryResultReceipt = DiscoveryPresentationModels['DiscoveryResultReceipt']
export type DiscoverySearchResponse = DiscoveryPresentationModels['DiscoverySearchResponse']
export type DiscoverySelectors = DiscoveryPresentationModels['DiscoverySelectors']
export type DiscoverySourceAddress = DiscoveryPresentationModels['DiscoverySourceAddress']
export type DiscoveryStoredQueryResponse = DiscoveryPresentationModels['DiscoveryStoredQueryResponse']
export type ScreenAssetsRequest = DiscoveryPresentationModels['ScreenAssetsRequest']
export type DatasetSourceMetadataResponseConstructor = DiscoveryPresentationModels['DatasetSourceMetadataResponseConstructor']
export function parseDiscoveryPresentation<K extends keyof DiscoveryPresentationModels>(name: K, value: unknown): DiscoveryPresentationModels[K]
export function serializeDiscoveryPresentation<K extends keyof DiscoveryPresentationModels>(name: K, value: DiscoveryPresentationModels[K]): Wire[K]
