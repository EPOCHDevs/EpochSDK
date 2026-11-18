import type * as Wire from './identity-wire.js'
type Camel<S extends string> = S extends `${infer First}_${infer Rest}` ? `${First}${Capitalize<Camel<Rest>>}` : S
type Decoded<T> = T extends readonly (infer V)[] ? Decoded<V>[] : T extends object ? { [K in keyof T as K extends string ? Camel<K> : K]: Decoded<T[K]> } : T
export type AssetInformation = Decoded<Wire.AssetSpecification>
export type AssetLogoResponse = Decoded<Wire.AssetLogoResponse>
export type IdentityImage = Decoded<Wire.IdentityImage>
export type CountryIdentity = Decoded<Wire.CountryIdentity>
export type CountryCatalogResponse = Decoded<Wire.CountryCatalogResponse>
export type AssetInformationPage = Decoded<Wire.AssetInformationPage>
export type AssetLookupResponse = Decoded<Wire.AssetLookupResponse>
export interface IdentityOptions { signal?: AbortSignal }
export interface ListingScope { listingCatalogue?: string; listingSelectedAt?: string }
export class IdentityHTTPError extends Error { status: number; body: string }
export function parseAssetInformation(value: unknown): AssetInformation
export function parseAssetLogos(value: unknown): AssetLogoResponse
export function parseCountryCatalog(value: unknown): CountryCatalogResponse
export class IdentityClient {
  constructor(options: { baseUrl: string; token?: string | (() => string | null | undefined | Promise<string | null | undefined>); fetch?: typeof fetch })
  getAssetInformation(assetId: string, options?: IdentityOptions): Promise<AssetInformation>
  getAssetLogos(assetId: string, scope?: ListingScope, options?: IdentityOptions): Promise<AssetLogoResponse>
  getCountryCatalog(options?: IdentityOptions): Promise<CountryCatalogResponse>
  getCountry(code: string, options?: IdentityOptions): Promise<CountryIdentity>
  getRegion(code: string, options?: IdentityOptions): Promise<CountryIdentity>
  listAssets(query?: { query?: string; page?: number; pageSize?: number }, options?: IdentityOptions): Promise<AssetInformationPage>
  resolveAssetInformation(assetIds: readonly string[], options?: IdentityOptions): Promise<AssetLookupResponse>
}
