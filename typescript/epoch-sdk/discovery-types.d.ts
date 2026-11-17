/* Generated from Platform contracts/discovery-v4.schema.json. Do not edit. */

export type Provider = "TradingEconomics" | "Macrobond" | "FMP" | "Barchart" | "EpochCatalog";
export type SourceKind = "asset" | "series" | "release" | "calendar";
export type SupportState = "qualified" | "held" | "excluded" | "unknown";
export type IntegerCount = number;
export type CompactCandidate = CandidateDetails | CandidateSummary;
export type Json =
  | null
  | boolean
  | number
  | string
  | Json[]
  | {
      [k: string]: Json;
    };
export type Integer = number;
export type ScreenInput =
  | {
      screen: AssetPredicate;
      membership_window?: {
        from: string;
        to: string;
      };
      current_cap_min_exclusive?: number;
      current_cap_max_exclusive?: number;
      kind: "screen";
    }
  | {
      kind: "saved";
      universe_ref: string;
      current_cap_min_exclusive?: number;
      current_cap_max_exclusive?: number;
    };

export interface PublicDiscoveryProtocol {
  request: DiscoveryInput;
  response: DiscoveryResult;
  selection: SelectedInputs;
  details: DiscoveryDetails;
  screen_request: ScreenInput;
  screen_response: AssetUniverseResult;
  universe_page_request: UniversePageRequest;
  universe_page: UniversePage;
  universe_binding: UniverseBinding;
  observation_request: ObservationInput;
  asset_lookup_request: AssetLookupInput;
  asset_lookup_response: AssetLookupResult;
}
export interface DiscoveryInput {
  requests: DiscoveryQuery[];
  saved_query?: string;
  limit?: IntegerCount;
  budget?: IntegerCount;
}
export interface DiscoveryQuery {
  id: string;
  query: string;
  /**
   * Concise lexical/vendor recall terms; query remains the complete relevance intent.
   */
  retrieval_query?: string;
  mode: "discover" | "exact" | "browse";
  filters?: SearchFilters;
  semantic?: boolean;
  cursor?: string;
}
export interface SearchFilters {
  providers?: Provider[];
  kinds?: SourceKind[];
  countries?: string[];
  asset_classes?: string[];
  exchanges?: string[];
  sectors?: string[];
  industries?: string[];
  security_types?: string[];
  active?: boolean;
  support?: SupportState[];
  categories?: string[];
  classifications?: string[];
  unit?: string;
  frequency?: string;
  loaders?: string[];
  macrobond?: {
    category?: string[];
    currency?: string[];
    data_type?: string[];
    region?: string[];
    exchange?: string[];
    frequency?: string[];
    klass?: string[];
    include_discontinued?: boolean;
    must_have_revisions?: boolean;
  };
}
export interface DiscoveryResult {
  format: "epoch-search-v4";
  session_id: string;
  needs: NeedResult[];
  candidates: CompactCandidate[];
  saved: SavedCandidate[];
  omitted: IntegerCount;
}
export interface NeedResult {
  id: string;
  status: "ok" | "no_match" | "incomplete" | "needs_detail" | "error";
  reason?: "low_relevance";
  /**
   * Source facts outside a requested filter; never matching/selectable candidates.
   */
  scope_issues?: ScopeIssue[];
  candidates: string[];
  next_cursor: string | null;
  completeness: "complete" | "candidate_set";
  failures?: SearchRequestFailure[];
  error?: {
    status: IntegerCount;
    message: string;
  };
}
export interface ScopeIssue {
  code: "filter_conflict" | "metadata_unknown";
  field: "countries" | "exchanges" | "kinds";
  requested: string[];
  available: string[];
  source_ids: string[];
}
export interface SearchRequestFailure {
  provider: Provider;
  message: string;
}
export interface CandidateDetails {
  id: string;
  source_id: string;
  identifiers: {
    scheme: string;
    value: string;
  }[];
  name: string;
  provider: Provider;
  kind: SourceKind;
  product: string | null;
  asset_class?: string;
  exchange?: string;
  sector?: string;
  coverage: {
    vendor: {
      start: string | null;
      end: string | null;
    } | null;
    accepted: {
      start: string | null;
      end: string | null;
      missing_years?: IntegerCount[];
    } | null;
  };
  detail: "full";
  definition: string;
  geography: string[];
  asset_attributes?: {
    industry: string | null;
    category?: string | null;
    base_currency?: string;
    quote_currency?: string;
    active: boolean | null;
    ipo_date: string | null;
    delisted_date: string | null;
  };
  history?: {
    high: number | null;
    high_on: string | null;
    low: number | null;
    low_on: string | null;
  };
  measurement?: {
    currency?: string;
    base?: string;
    maturity?: string;
    inflation_adjustment?: string;
  };
  revisions?: {
    available: boolean;
    first?: string;
    last?: string;
    source?: string;
    source_cutoff?: string;
  };
  last_observation?: string;
  publishers?: string[];
  relationships?: {
    release_ids?: string[];
    replaces?: string[];
    replaced_by?: string[];
  };
  lifecycle?: {
    state?: string;
    reason?: string;
  };
  unit: string | null;
  frequency: string | null;
  adjustment: string | null;
  publisher: string | null;
  classification: string | null;
  support: {
    state: SupportState;
    reason: string | null;
  };
  delivery: {
    mode: "native" | "published" | "unavailable" | "unknown";
    environment: string;
  };
  entitlement: "allowed" | "denied" | "unchecked";
  qualifications: {
    code: string;
    text: string;
  }[];
}
export interface CandidateSummary {
  id: string;
  source_id: string;
  identifiers: {
    scheme: string;
    value: string;
  }[];
  name: string;
  provider: Provider;
  kind: SourceKind;
  product: string | null;
  asset_class?: string;
  exchange?: string;
  sector?: string;
  coverage: {
    vendor: {
      start: string | null;
      end: string | null;
    } | null;
    accepted: {
      start: string | null;
      end: string | null;
      missing_years?: IntegerCount[];
    } | null;
  };
  detail: "compact";
}
export interface SavedCandidate {
  id: string;
  name: string;
  format: "table" | "json";
  source_ref: string | null;
  description?: string;
  schema?: Json;
  columns?: string[];
  needs_detail?: true;
}
export interface SelectedInputs {
  format: "epoch-selected-inputs-v1";
  id: string;
  owner: string;
  created_at: string;
  sources: SourceRecord[];
  saved: PrivateSource[];
}
export interface SourceRecord {
  id: string;
  source_id: string;
  revision: string;
  kind: SourceKind;
  provider: Provider;
  title: string;
  definition: string;
  identifiers: {
    scheme: string;
    value: string;
  }[];
  geography: {
    name: string;
    code: string | null;
  }[];
  asset_class: string | null;
  exchange: string | null;
  sector: string | null;
  asset_attributes?: {
    industry: string | null;
    category?: string | null;
    base_currency?: string;
    quote_currency?: string;
    active: boolean | null;
    ipo_date: string | null;
    delisted_date: string | null;
  };
  asset_details?: AssetDetails;
  unit: string | null;
  frequency: string | null;
  adjustment: string | null;
  publisher: string | null;
  publishers?: string[];
  relationships?: {
    release_ids?: string[];
    replaces?: string[];
    replaced_by?: string[];
  };
  lifecycle?: {
    state?: string;
    reason?: string;
  };
  classification: string | null;
  history?: {
    high: number | null;
    high_on: string | null;
    low: number | null;
    low_on: string | null;
  };
  measurement?: {
    currency?: string;
    base?: string;
    maturity?: string;
    inflation_adjustment?: string;
  };
  revisions?: {
    available: boolean;
    first?: string;
    last?: string;
    source?: string;
    source_cutoff?: string;
  };
  last_observation?: string;
  support: {
    state: SupportState;
    reason: string | null;
  };
  delivery: {
    mode: "native" | "published" | "unavailable" | "unknown";
    environment: string;
    revision: string | null;
  };
  entitlement: "allowed" | "denied" | "unchecked";
  coverage: {
    vendor: Extent | null;
    accepted: {
      revision: string;
      missing_years?: Integer[];
      start: string | null;
      end: string | null;
    } | null;
  };
  qualifications: {
    code: string;
    text: string;
  }[];
  binding: LoaderBinding | null;
  evidence: {
    uri: string;
    sha256: string;
  }[];
  /**
   * Original provider-owned JSON, retained for audit and excluded from model projections.
   */
  vendor_metadata?:
    | null
    | boolean
    | number
    | string
    | Json[]
    | {
        [k: string]: Json;
      };
}
export interface AssetDetails {
  min_tick: string;
  multiplier: string;
  expiry_months: string | null;
  logo_url: string | null;
  cik: string | null;
  description_source: string | null;
  eod_history_start: string | null;
  minute_history_start: string | null;
  ipo_shares: string | null;
  ipo_market_cap: string | null;
  ipo_price_range: string | null;
  ipo_price_min: string | null;
  ipo_price_max: string | null;
  ipo_market_cap_usd: string | null;
  ipo_market_cap_at_listing_usd: string | null;
  name_aliases: {
    name: string;
    source: string;
  }[];
  symbol_changes: {
    old_symbol: string;
    new_symbol: string;
    effective_date: string | null;
    company_name: string | null;
    source: string;
  }[];
  currency_pair:
    | {
        code: string;
        kind: "fiat" | "crypto";
      }[]
    | null;
  source_profile?: {
    provider: "FMP";
    symbol: string;
    observed_at: string;
    isin: string | null;
    cusip: string | null;
    cik: string | null;
  };
}
export interface Extent {
  start: string | null;
  end: string | null;
}
/**
 * Native argument keys are owned by the versioned loader contract, not by discovery.
 */
export interface LoaderBinding {
  source_id: string;
  category: string;
  registry_version: string;
  arguments: {
    [k: string]: Json;
  };
  /**
   * Native per-study sources take their assets from the study input, never an invented constructor argument.
   */
  asset_ids?: string[];
}
export interface PrivateSource {
  id: string;
  name: string;
  description: string;
  format: "table" | "json";
  revision: string;
  source_ref: string | null;
  schema: Json;
  columns: string[];
  updated_at: string;
}
export interface DiscoveryDetails {
  format: "epoch-search-details-v1";
  session_id: string;
  sources: SourceRecord[];
  saved: PrivateSource[];
}
export interface AssetPredicate {
  ids?: string[];
  index?: string[];
  asset_class?: string[];
  exchange?: string[];
  country?: string[];
  sector?: string[];
  industry?: string[];
  category?: string[];
  security_type?: string[];
  is_actively_trading?: boolean;
  base_currency?: string[];
  quote_currency?: string[];
  ipo_after?: string;
  ipo_before?: string;
  delisted_after?: string;
  delisted_before?: string;
  /**
   * Decimal integer text preserves the complete int64 domain over JSON.
   */
  ipo_shares_min?: string;
  ipo_shares_max?: string;
  ipo_market_cap_min?: number;
  ipo_market_cap_max?: number;
  ipo_price_min?: number;
  ipo_price_max?: number;
  all_of?: AssetPredicate[];
  any_of?: AssetPredicate[];
  not?: AssetPredicate;
  max_assets?: Integer;
  order_by?: "IdAsc";
  index_membership_mode?: "CurrentSnapshot" | "PointInTime";
}
export interface AssetUniverseResult {
  format: "epoch-universe-v1";
  universe_ref: string | null;
  generation: string;
  created_at: string;
  status: "ready" | "no_match" | "incomplete" | "over_limit";
  asset_count: IntegerCount;
  matched: IntegerCount;
  definition: UniverseRequest;
  selection: {
    selection_semantics: "StaticCatalog" | "HistoricalUnion";
    requires_point_in_time_gate: boolean;
    point_in_time_indexes: string[];
  };
  sample: UniverseMember[];
  facets: {
    [k: string]: {
      value: string;
      count: Integer;
    }[];
  };
  excluded_count: IntegerCount;
  exclusions: {
    id: string;
    reason: string;
  }[];
  current_cap?: {
    provider: "FMP";
    queried_at: string;
    source_as_of: null;
    min_exclusive: number | null;
    max_exclusive: number | null;
  };
  membership?: {
    index: string;
    source_kind: string;
    source_symbol: string | null;
    is_proxy: boolean;
    source_as_of: string | null;
    checked_at: string;
  }[];
  historical_integrity?: {
    index: string;
    unresolved: Integer;
    unmatched_removals: Integer;
    address_conflicts: Integer;
    identity_reviews: Integer;
    completeness_verified: false;
  }[];
}
export interface UniverseRequest {
  screen: AssetPredicate;
  membership_window?: {
    from: string;
    to: string;
  };
  current_cap_min_exclusive?: number;
  current_cap_max_exclusive?: number;
}
export interface UniverseMember {
  id: string;
  ticker: string;
  name: string;
  asset_class: string;
  exchange: string;
  country: string | null;
  sector: string | null;
  industry: string | null;
  fmp_symbol?: string;
  current_market_cap?: string;
}
export interface UniversePageRequest {
  universe_ref: string;
  query?: string;
  exchange?: string;
  country?: string;
  limit?: IntegerCount;
  cursor?: string;
}
export interface UniversePage {
  format: "epoch-universe-page-v1";
  universe_ref: string;
  generation: string;
  records: UniverseMember[];
  total: IntegerCount;
  next_cursor: string | null;
  facets: {
    [k: string]: {
      value: string;
      count: Integer;
    }[];
  };
}
export interface UniverseBinding {
  format: "epoch-universe-binding-v1";
  universe_ref: string;
  generation: string;
  ids: string[];
  screen: AssetPredicate;
  definition: UniverseRequest;
  selection: {
    selection_semantics: "StaticCatalog" | "HistoricalUnion";
    requires_point_in_time_gate: boolean;
    point_in_time_indexes: string[];
  };
}
export interface ObservationInput {
  session_id: string;
  id: string;
  window?: {
    from: string;
    to: string;
  };
  options?: {
    [k: string]: Json;
  };
  market?: {
    [k: string]: Json;
  };
  limit?: IntegerCount;
}
export interface AssetLookupInput {
  asset_ids: string[];
}
export interface AssetLookupResult {
  items: {
    asset_id: string;
    source?: SourceRecord;
    reason?: string;
  }[];
}
