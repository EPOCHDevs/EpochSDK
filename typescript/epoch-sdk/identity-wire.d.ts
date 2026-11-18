/* Generated from contracts/asset-identity-v1.schema.json. Do not edit. */

export type AssetClass = "Stocks" | "FX" | "Crypto" | "Futures";
export type IdentityCurrencyKind = "fiat" | "crypto";
export type OptionalBool = boolean;
export type StockProfileIdentity = {
  cik?: string;
  cusip?: string;
  is_adr?: OptionalBool;
  isin?: string;
  observed_at: string;
  source: string;
  symbol: string;
  test_classification?: StockTestClassificationEvidence;
} | null;
export type StockTestClassificationEvidence = {
  description?: string;
  is_etf?: OptionalBool;
  is_fund?: OptionalBool;
  state?: StockTestClassificationState;
} | null;
export type StockTestClassificationState = "DeclaredTest" | "ConflictingRoles" | "Withdrawn";
export type AssetLogoResponse =
  | {
      asset_id: string;
      image: IdentityImage;
      kind: SingleAssetLogoKind;
    }
  | {
      asset_id: string;
      base: IdentityImage;
      counter: IdentityImage;
      kind: PairedAssetLogoKind;
    };
export type IdentityImageState = "available" | "unverified" | "missing" | "unavailable";
export type SingleAssetLogoKind = "single";
export type PairedAssetLogoKind = "pair";

export interface AssetIdentityProtocol {
  asset_information: AssetSpecification;
  asset_lookup_request: AssetLookupRequest;
  asset_lookup_response: AssetLookupResponse;
  asset_logos: AssetLogoResponse;
  country_catalog: CountryCatalogResponse;
  country: CountryIdentity;
  asset_page: AssetInformationPage;
}
export interface AssetSpecification {
  asset_class?: AssetClass;
  base?: CurrencyIdentity;
  category?: string;
  cik?: string;
  counter?: CurrencyIdentity;
  country?: string;
  currency?: string;
  delisted_date?: string;
  description?: string;
  description_source?: string;
  disclosure_filings?: AssetDisclosure[] | null;
  eod_history_start?: string;
  exchange?: string;
  expiry_months?: string;
  id: string;
  industry?: string;
  ipo_date?: string;
  ipo_market_cap?: number;
  ipo_market_cap_at_listing_usd?: number;
  ipo_market_cap_usd?: number;
  ipo_price_max?: number;
  ipo_price_min?: number;
  ipo_price_range?: string;
  ipo_shares?: number;
  is_actively_trading?: OptionalBool;
  logo_url?: string;
  min_tick?: number;
  minute_history_start?: string;
  multiplier?: number;
  name?: string;
  name_aliases: AssetNameAlias[];
  prospectus_filings?: AssetProspectus[] | null;
  root_id?: string;
  sector?: string;
  security_type?: string;
  stock_profile?: StockProfileIdentity;
  symbol_changes: AssetSymbolChange[];
  ticker?: string;
}
export interface CurrencyIdentity {
  code: string;
  kind: IdentityCurrencyKind;
}
export interface AssetDisclosure {
  accepted_date?: string;
  effectiveness_date?: string;
  filing_date?: string;
  form?: string;
  url?: string;
}
export interface AssetNameAlias {
  name: string;
  source: string;
}
export interface AssetProspectus {
  accepted_date?: string;
  discounts_and_commissions_per_share?: number;
  discounts_and_commissions_total?: number;
  filing_date?: string;
  form?: string;
  price_public_per_share?: number;
  price_public_total?: number;
  proceeds_before_expenses_per_share?: number;
  proceeds_before_expenses_total?: number;
  url?: string;
}
export interface AssetSymbolChange {
  company_name?: string;
  effective_date?: string;
  new_symbol: string;
  old_symbol: string;
  source: string;
}
export interface AssetLookupRequest {
  asset_ids: string[];
}
export interface AssetLookupResponse {
  items: AssetLookupResult[];
}
export interface AssetLookupResult {
  asset?: AssetSpecification;
  asset_id: string;
  reason?: string;
}
export interface IdentityImage {
  attribution?: string;
  identity: string;
  image_id?: string;
  provider?: string;
  reason?: string;
  state: IdentityImageState;
  url?: string;
}
export interface CountryCatalogResponse {
  countries: CountryIdentity[];
  globe: IdentityImage;
  regions: CountryIdentity[];
}
export interface CountryIdentity {
  code: string;
  image: IdentityImage;
  name: string;
}
export interface AssetInformationPage {
  items: AssetSpecification[];
  page?: number;
  total_pages?: number;
  total_items: number;
}
