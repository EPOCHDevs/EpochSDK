/* Generated from contracts/discovery-presentation-v1.schema.json. Do not edit. */

export type AssetClass = "Stocks" | "FX" | "Crypto" | "Futures";
export type AssetCategory =
  | "Aggressive_Allocation"
  | "Bank_Loan"
  | "China_Region"
  | "Commodities_Broad_Basket"
  | "Commodities_Focused"
  | "Communications"
  | "Conservative_Allocation"
  | "Consumer_Cyclical"
  | "Consumer_Defensive"
  | "Convertibles"
  | "Corporate_Bond"
  | "Currencies"
  | "Defined_Outcome"
  | "Derivative_Income"
  | "Digital_Assets"
  | "Diversified_Emerging_Mkts"
  | "Diversified_Pacific_Asia"
  | "Emerging_Markets_Bond"
  | "Emerging_Markets_Local_Currency_Bond"
  | "Energies"
  | "Energy_Limited_Partnership"
  | "Equity_Energy"
  | "Equity_Hedged"
  | "Equity_Market_Neutral"
  | "Equity_Precious_Metals"
  | "Europe_Stock"
  | "Event_Driven"
  | "Financial"
  | "Financials"
  | "Foreign_Large_Blend"
  | "Foreign_Large_Growth"
  | "Foreign_Large_Value"
  | "Foreign_Small_Mid_Blend"
  | "Foreign_Small_Mid_Value"
  | "Global_Allocation"
  | "Global_Bond"
  | "Global_Bond_USD_Hedged"
  | "Global_Large_Stock_Blend"
  | "Global_Large_Stock_Growth"
  | "Global_Large_Stock_Value"
  | "Global_Real_Estate"
  | "Global_Small_Mid_Stock"
  | "Grains"
  | "Health"
  | "High_Yield_Bond"
  | "High_Yield_Muni"
  | "India_Equity"
  | "Indices"
  | "Industrials"
  | "Inflation_Protected_Bond"
  | "Infrastructure"
  | "Intermediate_Core_Bond"
  | "Intermediate_Core_Plus_Bond"
  | "Intermediate_Government"
  | "Japan_Stock"
  | "Large_Blend"
  | "Large_Growth"
  | "Large_Value"
  | "Latin_America_Stock"
  | "Long_Government"
  | "Long_Short_Equity"
  | "Long_Term_Bond"
  | "Meats"
  | "Metals"
  | "Mid_Cap_Blend"
  | "Mid_Cap_Growth"
  | "Mid_Cap_Value"
  | "Miscellaneous_Fixed_Income"
  | "Miscellaneous_Region"
  | "Miscellaneous_Sector"
  | "Moderate_Allocation"
  | "Moderately_Aggressive_Allocation"
  | "Moderately_Conservative_Allocation"
  | "Money_Market_Taxable"
  | "Multialternative"
  | "Multisector_Bond"
  | "Multistrategy"
  | "Muni_California_Intermediate"
  | "Muni_California_Long"
  | "Muni_Minnesota"
  | "Muni_National_Interm"
  | "Muni_National_Long"
  | "Muni_National_Short"
  | "Muni_New_York_Intermediate"
  | "Muni_New_York_Long"
  | "Muni_Target_Maturity"
  | "Natural_Resources"
  | "Nontraditional_Bond"
  | "Others"
  | "Pacific_Asia_ex_Japan_Stk"
  | "Preferred_Stock"
  | "Real_Estate"
  | "Relative_Value_Arbitrage"
  | "Short_Government"
  | "Short_Term_Bond"
  | "Short_Term_Inflation_Protected_Bond"
  | "Single_Currency"
  | "Small_Blend"
  | "Small_Growth"
  | "Small_Value"
  | "Softs"
  | "Systematic_Trend"
  | "Tactical_Allocation"
  | "Target_Date_2030"
  | "Target_Date_2035"
  | "Target_Date_2040"
  | "Target_Date_2045"
  | "Target_Date_2050"
  | "Target_Date_2055"
  | "Target_Date_2060"
  | "Target_Date_2065"
  | "Target_Date_Retirement"
  | "Target_Maturity"
  | "Technology"
  | "Trading_Inverse_Commodities"
  | "Trading_Inverse_Debt"
  | "Trading_Inverse_Equity"
  | "Trading_Leveraged_Commodities"
  | "Trading_Leveraged_Debt"
  | "Trading_Leveraged_Equity"
  | "Trading_Miscellaneous"
  | "Ultrashort_Bond"
  | "Utilities";
export type Country =
  | "AD"
  | "AE"
  | "AF"
  | "AG"
  | "AI"
  | "AL"
  | "AM"
  | "AO"
  | "AQ"
  | "AR"
  | "AS"
  | "AT"
  | "AU"
  | "AW"
  | "AX"
  | "AZ"
  | "BA"
  | "BB"
  | "BD"
  | "BE"
  | "BF"
  | "BG"
  | "BH"
  | "BI"
  | "BJ"
  | "BL"
  | "BM"
  | "BN"
  | "BO"
  | "BQ"
  | "BR"
  | "BS"
  | "BT"
  | "BV"
  | "BW"
  | "BY"
  | "BZ"
  | "CA"
  | "CC"
  | "CD"
  | "CF"
  | "CG"
  | "CH"
  | "CI"
  | "CK"
  | "CL"
  | "CM"
  | "CN"
  | "CO"
  | "CR"
  | "CU"
  | "CV"
  | "CW"
  | "CX"
  | "CY"
  | "CZ"
  | "DE"
  | "DJ"
  | "DK"
  | "DM"
  | "DO"
  | "DZ"
  | "EC"
  | "EE"
  | "EG"
  | "EH"
  | "ER"
  | "ES"
  | "ET"
  | "FI"
  | "FJ"
  | "FK"
  | "FM"
  | "FO"
  | "FR"
  | "GA"
  | "GB"
  | "GD"
  | "GE"
  | "GF"
  | "GG"
  | "GH"
  | "GI"
  | "GL"
  | "GM"
  | "GN"
  | "GP"
  | "GQ"
  | "GR"
  | "GS"
  | "GT"
  | "GU"
  | "GW"
  | "GY"
  | "HK"
  | "HM"
  | "HN"
  | "HR"
  | "HT"
  | "HU"
  | "ID"
  | "IE"
  | "IL"
  | "IM"
  | "IN"
  | "IO"
  | "IQ"
  | "IR"
  | "IS"
  | "IT"
  | "JE"
  | "JM"
  | "JO"
  | "JP"
  | "KE"
  | "KG"
  | "KH"
  | "KI"
  | "KM"
  | "KN"
  | "KP"
  | "KR"
  | "KW"
  | "KY"
  | "KZ"
  | "LA"
  | "LB"
  | "LC"
  | "LI"
  | "LK"
  | "LR"
  | "LS"
  | "LT"
  | "LU"
  | "LV"
  | "LY"
  | "MA"
  | "MC"
  | "MD"
  | "ME"
  | "MF"
  | "MG"
  | "MH"
  | "MK"
  | "ML"
  | "MM"
  | "MN"
  | "MO"
  | "MP"
  | "MQ"
  | "MR"
  | "MS"
  | "MT"
  | "MU"
  | "MV"
  | "MW"
  | "MX"
  | "MY"
  | "MZ"
  | "NA"
  | "NC"
  | "NE"
  | "NF"
  | "NG"
  | "NI"
  | "NL"
  | "NO"
  | "NP"
  | "NR"
  | "NU"
  | "NZ"
  | "OM"
  | "PA"
  | "PE"
  | "PF"
  | "PG"
  | "PH"
  | "PK"
  | "PL"
  | "PM"
  | "PN"
  | "PR"
  | "PS"
  | "PT"
  | "PW"
  | "PY"
  | "QA"
  | "RE"
  | "RO"
  | "RS"
  | "RU"
  | "RW"
  | "SA"
  | "SB"
  | "SC"
  | "SD"
  | "SE"
  | "SG"
  | "SH"
  | "SI"
  | "SJ"
  | "SK"
  | "SL"
  | "SM"
  | "SN"
  | "SO"
  | "SR"
  | "SS"
  | "ST"
  | "SV"
  | "SX"
  | "SY"
  | "SZ"
  | "TC"
  | "TD"
  | "TF"
  | "TG"
  | "TH"
  | "TJ"
  | "TK"
  | "TL"
  | "TM"
  | "TN"
  | "TO"
  | "TR"
  | "TT"
  | "TV"
  | "TW"
  | "TZ"
  | "UA"
  | "UG"
  | "UM"
  | "US"
  | "UY"
  | "UZ"
  | "VA"
  | "VC"
  | "VE"
  | "VG"
  | "VI"
  | "VN"
  | "VU"
  | "WF"
  | "WS"
  | "YE"
  | "YT"
  | "ZA"
  | "ZM"
  | "ZW";
export type Exchange =
  | "HKFE"
  | "EUREX"
  | "NYSE"
  | "NASDAQ"
  | "XNAS"
  | "XNYS"
  | "AMEX"
  | "ARCX"
  | "BATS"
  | "XASE"
  | "CBOT"
  | "CBOTM"
  | "KCBT"
  | "CME"
  | "NYMEX"
  | "CBOE"
  | "COMEX"
  | "NYMI"
  | "ICEUS"
  | "ICESI"
  | "GBLX"
  | "CXMI"
  | "FX"
  | "INDEX"
  | "CRYPTO"
  | "APEX"
  | "BMF"
  | "BSE"
  | "CFE"
  | "CFFEX"
  | "CZCE"
  | "DCE"
  | "DGCX"
  | "EEX"
  | "ENDEX"
  | "EUIDX"
  | "FAIRX"
  | "GME"
  | "GPW"
  | "ICE"
  | "ICEAD"
  | "ISE"
  | "JPX"
  | "KFE"
  | "LIFFE"
  | "LME"
  | "MATBA"
  | "MATIF"
  | "MDEX"
  | "MEFF"
  | "MIAX"
  | "MIAXF"
  | "MNTRL"
  | "NCDEX"
  | "NSE"
  | "NZD"
  | "NZX"
  | "OMX"
  | "ROFEX"
  | "SAFEX"
  | "SFE"
  | "SGCOM"
  | "SGIDX"
  | "SGXFX"
  | "SGXNZ"
  | "SHFE"
  | "SIEE"
  | "SIMEX"
  | "SMALL"
  | "TAIWA"
  | "TFEX"
  | "TIFFE"
  | "TURK"
  | "WCE"
  | "COINBASE"
  | "LSE"
  | "TSX"
  | "TSXV"
  | "CNQ"
  | "NEO"
  | "AMS"
  | "ASX"
  | "ATH"
  | "BER"
  | "BME"
  | "BRU"
  | "BUE"
  | "CPH"
  | "DFM"
  | "DOH"
  | "DUB"
  | "DUS"
  | "DXE"
  | "FSX"
  | "HAM"
  | "HEL"
  | "HKSE"
  | "IOB"
  | "IST"
  | "JKT"
  | "JNB"
  | "KLS"
  | "KOE"
  | "KSC"
  | "LIS"
  | "MCX"
  | "MEX"
  | "MIL"
  | "MUN"
  | "NZE"
  | "OSL"
  | "PAR"
  | "PRA"
  | "SAO"
  | "SAU"
  | "SES"
  | "SET"
  | "SGO"
  | "SHH"
  | "SHZ"
  | "SIX"
  | "STO"
  | "STU"
  | "TAI"
  | "TLV"
  | "TWO"
  | "VIE"
  | "WSE"
  | "XETRA"
  | "OTC";
export type IndexMembershipMode = "CurrentSnapshot" | "PointInTime";
export type StockIndustry =
  | "Others"
  | "Advertising_Agencies"
  | "Aerospace_And_Defense"
  | "Agricultural_Commodities_Milling"
  | "Agricultural_Machinery"
  | "Agricultural_Farm_Products"
  | "Agricultural_Inputs"
  | "Airlines_Airports_And_Air_Services"
  | "Aluminum"
  | "Apparel_Footwear_And_Accessories"
  | "Apparel_Manufacturers"
  | "Apparel_Retail"
  | "Asset_Management"
  | "Asset_Management_Bonds"
  | "Asset_Management_Cryptocurrency"
  | "Asset_Management_Global"
  | "Asset_Management_Income"
  | "Asset_Management_Leveraged"
  | "Auto_Dealerships"
  | "Auto_Manufacturers"
  | "Auto_Parts"
  | "Auto_Recreational_Vehicles"
  | "Banking_Services"
  | "Banks"
  | "Banks_Diversified"
  | "Banks_Regional"
  | "Beverages_Alcoholic"
  | "Beverages_Non_Alcoholic"
  | "Beverages_Wineries_And_Distilleries"
  | "Biotechnology"
  | "Broadcasting"
  | "Business_Equipment_And_Supplies"
  | "Chemicals"
  | "Chemicals_Specialty"
  | "Coal"
  | "Communication_Equipment"
  | "Computer_Hardware"
  | "Computers_Phones_And_Household_Electronics"
  | "Conglomerates"
  | "Construction"
  | "Construction_Materials"
  | "Consulting_Services"
  | "Consumer_Electronics"
  | "Copper"
  | "Department_Stores"
  | "Discount_Stores"
  | "Diversified_Utilities"
  | "Drug_Manufacturers_General"
  | "Drug_Manufacturers_Specialty_And_Generic"
  | "Drug_Manufacturers_Specialty_Generic"
  | "Education_And_Training_Services"
  | "Electrical_Equipment_And_Parts"
  | "Electronic_Gaming_And_Multimedia"
  | "Engineering_And_Construction"
  | "Entertainment"
  | "Environmental_Services"
  | "Financial_Capital_Markets"
  | "Financial_Conglomerates"
  | "Financial_Credit_Services"
  | "Financial_Data_And_Stock_Exchanges"
  | "Financial_Diversified"
  | "Financial_Mortgages"
  | "Food_And_Drug_Retailing"
  | "Food_Confectioners"
  | "Food_Distribution"
  | "Furnishings_Fixtures_And_Appliances"
  | "Gambling_Resorts_And_Casinos"
  | "General_Transportation"
  | "General_Utilities"
  | "Gold"
  | "Grocery_Stores"
  | "Hardware_Equipment_And_Parts"
  | "Home_Improvement"
  | "Household_And_Personal_Products"
  | "Independent_Power_Producers"
  | "Industrial_Capital_Goods"
  | "Industrial_Distribution"
  | "Industrial_Infrastructure_Operations"
  | "Industrial_Machinery"
  | "Industrial_Pollution_And_Treatment_Controls"
  | "Industrial_Specialties"
  | "Industrial_Materials"
  | "Information_Technology_Services"
  | "Insurance_Brokers"
  | "Insurance_Diversified"
  | "Insurance_Life"
  | "Insurance_Property_And_Casualty"
  | "Insurance_Reinsurance"
  | "Insurance_Specialty"
  | "Integrated_Freight_And_Logistics"
  | "Internet_Content_And_Information"
  | "Investment_Banking_And_Investment_Services"
  | "Leisure"
  | "Luxury_Goods"
  | "Manufacturing_Metal_Fabrication"
  | "Manufacturing_Miscellaneous"
  | "Manufacturing_Textiles"
  | "Manufacturing_Tools_And_Accessories"
  | "Marine_Shipping"
  | "Media_And_Entertainment"
  | "Medical_Care_Facilities"
  | "Medical_Devices"
  | "Medical_Diagnostics_And_Research"
  | "Medical_Distribution"
  | "Medical_Equipment_And_Services"
  | "Medical_Healthcare_Information_Services"
  | "Medical_Healthcare_Plans"
  | "Medical_Instruments_And_Supplies"
  | "Medical_Pharmaceuticals"
  | "Medical_Specialties"
  | "Oil_And_Gas_Drilling"
  | "Oil_And_Gas_Energy"
  | "Oil_And_Gas_Equipment_And_Services"
  | "Oil_And_Gas_Exploration_And_Production"
  | "Oil_And_Gas_Integrated"
  | "Oil_And_Gas_Midstream"
  | "Oil_And_Gas_Refining_And_Marketing"
  | "Other_Precious_Metals"
  | "Packaged_Foods"
  | "Packaging_And_Containers"
  | "Paper_Lumber_And_Forest_Products"
  | "Personal_Products_And_Services"
  | "Professional_And_Commercial_Services"
  | "Publishing"
  | "REIT_Diversified"
  | "REIT_Healthcare_Facilities"
  | "REIT_Hotel_And_Motel"
  | "REIT_Industrial"
  | "REIT_Mortgage"
  | "REIT_Office"
  | "REIT_Residential"
  | "REIT_Retail"
  | "REIT_Specialty"
  | "Railroads"
  | "Real_Estate_Development"
  | "Real_Estate_Diversified"
  | "Real_Estate_General"
  | "Real_Estate_Services"
  | "Regulated_Electric"
  | "Regulated_Gas"
  | "Regulated_Water"
  | "Renewable_Utilities"
  | "Rental_And_Leasing_Services"
  | "Residential_And_Commercial_REITs"
  | "Residential_Construction"
  | "Restaurants"
  | "Security_And_Protection_Services"
  | "Semiconductors"
  | "Semiconductors_And_Semiconductor_Equipment"
  | "Shell_Companies"
  | "Silver"
  | "Software_Application"
  | "Software_Infrastructure"
  | "Software_Services"
  | "Solar"
  | "Specialty_Business_Services"
  | "Specialty_Retail"
  | "Staffing_And_Employment_Services"
  | "Steel"
  | "Technology_Distributors"
  | "Telecommunications_Services"
  | "Tobacco"
  | "Travel_Lodging"
  | "Travel_Services"
  | "Trucking"
  | "Uranium"
  | "Waste_Management";
export type OptionalBool = boolean;
export type SharedPtr_AssetScreen = {
  all_of: AssetScreen[];
  any_of: AssetScreen[];
  asset_class?: AssetClass[] | null;
  base_currency?: string[] | null;
  category?: AssetCategory[] | null;
  country?: Country[] | null;
  delisted_after?: string;
  delisted_before?: string;
  exchange?: Exchange[] | null;
  ids?: string[] | null;
  index?: string[] | null;
  index_membership_mode?: IndexMembershipMode;
  industry?: StockIndustry[] | null;
  ipo_after?: string;
  ipo_before?: string;
  ipo_market_cap_max?: number;
  ipo_market_cap_min?: number;
  ipo_price_max?: number;
  ipo_price_min?: number;
  ipo_shares_max?: number;
  ipo_shares_min?: number;
  is_actively_trading?: OptionalBool | null;
  max_assets?: number;
  not?: SharedPtr_AssetScreen;
  order_by?: AssetScreenOrder;
  quote_currency?: string[] | null;
  sector?: StockSector[] | null;
  security_type?: SecurityType[] | null;
} | null;
export type AssetScreenOrder = "IdAsc";
export type StockSector =
  | "Others"
  | "Basic_Materials"
  | "Communication_Services"
  | "Consumer_Cyclical"
  | "Consumer_Defensive"
  | "Energy"
  | "Financial_Services"
  | "Healthcare"
  | "Industrials"
  | "Real_Estate"
  | "Technology"
  | "Utilities";
export type SecurityType = "CommonStock" | "Etf" | "Fund" | "TestSecurity";
export type CatalogFreshness = {
  classification_checked_at?: string;
  classification_source: string;
  generation?: string;
  unverified_current_rosters: string[];
} | null;
export type DiscoveryRequestedWindow = {
  from: string;
  to: string;
} | null;
export type UniversePopulation = {
  excluded: UniverseExclusion[];
  matched: number;
  policy: string;
  returned: number;
  verified: number;
} | null;
export type ScreenAssetsRequest = ScreenAssetsRequestScreen | ScreenAssetsRequestSaved;
export type AssetScreenSelectionSemantics = "StaticCatalog" | "HistoricalUnion";
export type DataCategory =
  | "DailyBars"
  | "MinuteBars"
  | "OpenInterest"
  | "Dividends"
  | "Splits"
  | "Earnings"
  | "Events"
  | "BalanceSheets"
  | "CashFlowStatements"
  | "IncomeStatements"
  | "Ratios"
  | "KeyMetrics"
  | "EnterpriseValues"
  | "OwnerEarnings"
  | "BalanceSheetGrowth"
  | "IncomeStatementGrowth"
  | "CashFlowGrowth"
  | "FinancialGrowth"
  | "RevenueProductSegmentation"
  | "RevenueGeographicSegmentation"
  | "Ipos"
  | "MacrobondData"
  | "MacrobondVintageData"
  | "MacrobondRevisionInfo"
  | "MacrobondReleaseSchedule"
  | "TradingEconomicsHistorical"
  | "TradingEconomicsCalendar"
  | "TradingEconomicsMarkets"
  | "TradingEconomicsRatings"
  | "TradingEconomicsForecast"
  | "TradingEconomicsMarketForecast"
  | "ReferenceAgg"
  | "HistoricalMarketCap"
  | "IpoProspectus"
  | "EarningsCalendar"
  | "DividendsCalendar"
  | "SplitsCalendar"
  | "HistoricalEmployeeCount"
  | "EtfInformation"
  | "EtfHoldings"
  | "AssetCatalog";
export type DiscoverySelectors = DiscoverySelectors1 & DiscoverySelectors2;
export type DiscoverySelectors1 = DiscoverySelectorsFinancial | DiscoverySelectorsVintage;
export type FundamentalsIndexBy = "FilingDate" | "AcceptanceDate" | "ObservationDate";
export type FinancialsTimeframe = "quarterly" | "annual" | "trailing_twelve_months";
export type VintageRevision = "Last" | "First" | "NthFromLast";
export type DiscoverySelectors2 =
  | (DiscoverySelectorsFinancial | DiscoverySelectorsVintage)
  | (null & (DiscoverySelectorsFinancial | DiscoverySelectorsVintage));
export type ExtentCompleteness = "Unknown" | "ObservedRequest" | "AuthoritativeComplete";
export type DiscoveryAvailability = "available" | "unavailable" | "unknown";
export type DiscoveryCoverageBasis = "observation" | "publication" | "forecast_horizon" | "snapshot" | "unknown";
export type DiscoveryMetadataError = {
  error_class: FetchErrorClass;
  error_kind?: FetchErrorKind;
  message: string;
} | null;
export type FetchErrorClass = "Transient" | "RequestShape" | "EntityTerminal" | "AccessDenied";
export type FetchErrorKind =
  | "Transient"
  | "NotFound"
  | "Gone"
  | "NotEntitled"
  | "RateLimited"
  | "BadRequest"
  | "Cancelled"
  | "Unknown"
  | "Unusable";
export type DiscoverySourceAddress = DiscoverySourceAddress1 & DiscoverySourceAddress2;
export type DiscoverySourceAddress1 =
  | DiscoverySourceAddressAsset
  | DiscoverySourceAddressSeries
  | DiscoverySourceAddressTeIndicator
  | DiscoverySourceAddressTeMarket
  | DiscoverySourceAddressTeRatings
  | DiscoverySourceAddressMbRelease
  | DiscoverySourceAddressGlobalSource;
export type AssetType = "Stocks" | "Futures" | "FX" | "Crypto";
export type ResolvableVendor = "macrobond" | "trading_economics";
export type DiscoverySourceAddress2 =
  | (
      | DiscoverySourceAddressAsset
      | DiscoverySourceAddressSeries
      | DiscoverySourceAddressTeIndicator
      | DiscoverySourceAddressTeMarket
      | DiscoverySourceAddressTeRatings
      | DiscoverySourceAddressMbRelease
      | DiscoverySourceAddressGlobalSource
    )
  | (null &
      (
        | DiscoverySourceAddressAsset
        | DiscoverySourceAddressSeries
        | DiscoverySourceAddressTeIndicator
        | DiscoverySourceAddressTeMarket
        | DiscoverySourceAddressTeRatings
        | DiscoverySourceAddressMbRelease
        | DiscoverySourceAddressGlobalSource
      ));
export type IdentityCurrencyKind = "fiat" | "crypto";
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
export type MarketCoverageDefinitionDTO = {
  earliest_history_verified: boolean;
  observed_start?: string;
  relation: string;
  roll_convention?: string;
  vendor_symbol: string;
} | null;
export type HandleResolution = "Resolved" | "Unknown" | "AccessDenied" | "Transient" | "RequestShape";
export type Extent__MacrobondSourceDefinition = {
  discontinued_reason?: string;
  discontinued_replacements: string[];
  federal_reserve_code?: string;
  release_ids: string[];
  replaces: string[];
  revision_history_source?: string;
  revision_history_source_cutoff?: string;
  source_ids: string[];
} | null;
export type DiscoveryItemStatus = "resolved" | "candidate" | "unavailable" | "unknown" | "error";
export type DataVendor = "Macrobond" | "Barchart" | "FMP" | "TradingEconomics";
export type DatasetSavedSearchResult = {
  items: SavedDataset[];
  query: string;
  total_matches: number;
} | null;
export type DatasetEnrichmentMode = "automatic" | "user_defined";
export type DataSourceValueTransform =
  DataSourceValueTransform_ParseDateTime | DataSourceValueTransform_FloorDay | DataSourceValueTransform_AssumeTimezone;
export type DataSourcePostReadTransform =
  | DataSourcePostReadTransform_PromoteIndex
  | DataSourcePostReadTransform_CombineDateTime
  | DataSourcePostReadTransform_AddContextColumn;
export type DatasetOrigin = "upload" | "document" | "web" | "derived";
export type DatasetPurpose = "knowledge" | "study_source";
export type DatasetSchemaChoice = DatasetSchemaChoiceAgent | DatasetSchemaChoiceProvided | DatasetSchemaChoiceImported;
export type DatasetShape = DatasetShapeTable | DatasetShapeJson;
export type DataFoundation = "Daily" | "Minute" | "Nanosecond" | "Null";
export type SourceAvailabilityAxis = "None" | "ObservationIndex" | "KnownAtIndex" | "CurrentSnapshot";
export type SourceFutureCapability = "PastOrPresentOnly" | "ProviderKnownFutureRows";
export type SourcePredecessorCapability = "Unsupported" | "ExactBounded" | "FullPayloadLocalSlice";
export type SourceRangeCapability = "Unsupported" | "ExactBounded" | "FullPayloadLocalSlice";
export type DatasetTimeMeaning = "observation" | "event" | "publication" | "user_snapshot";
export type DatasetTimePrecision = "date" | "second" | "millisecond" | "microsecond" | "nanosecond";
export type DatasetProvenanceSource =
  | DatasetProvenanceSourceFile
  | DatasetProvenanceSourceWeb
  | DatasetProvenanceSourceDataset
  | DatasetProvenanceSourceStudyResult;
/**
 * Whether later pages of this selection remain in the stored result (selection protocol v2).
 */
export type OptionalBool1 = boolean;
/**
 * The provider-search completeness every delivered record of this selection shares, omitted from those records (selection protocol v3).
 */
export type ExtentCompleteness1 = "Unknown" | "ObservedRequest" | "AuthoritativeComplete";
/**
 * The vendor every delivered record of this selection shares, omitted from those records (selection protocol v3).
 */
export type DataVendor1 = "Macrobond" | "Barchart" | "FMP" | "TradingEconomics";
export type DatasetBrowseGroup = "market_data" | "fundamentals" | "macro" | "events" | "saved_data";
export type RawJson = number | string | boolean | {} | unknown[] | null;
export type DataSourceRegistryBacking = "vendor_endpoint" | "stored_dataset" | "pinned_catalog";
export type DataSourceRegistrySourceConstructor = "transform" | "macro";
export type DataSourceRegistryFamily = "market" | "fundamentals" | "corporate_actions" | "macro" | "dataset";
export type DataSourceRegistryScope = "per_study_asset" | "shared" | "keyed";
export type DataSourceRegistryWindow = "required" | "optional" | "execution_period" | "none";
/**
 * One native category. Supply category or nonempty categories, never both.
 */
export type DataCategory1 =
  | "DailyBars"
  | "MinuteBars"
  | "OpenInterest"
  | "Dividends"
  | "Splits"
  | "Earnings"
  | "Events"
  | "BalanceSheets"
  | "CashFlowStatements"
  | "IncomeStatements"
  | "Ratios"
  | "KeyMetrics"
  | "EnterpriseValues"
  | "OwnerEarnings"
  | "BalanceSheetGrowth"
  | "IncomeStatementGrowth"
  | "CashFlowGrowth"
  | "FinancialGrowth"
  | "RevenueProductSegmentation"
  | "RevenueGeographicSegmentation"
  | "Ipos"
  | "MacrobondData"
  | "MacrobondVintageData"
  | "MacrobondRevisionInfo"
  | "MacrobondReleaseSchedule"
  | "TradingEconomicsHistorical"
  | "TradingEconomicsCalendar"
  | "TradingEconomicsMarkets"
  | "TradingEconomicsRatings"
  | "TradingEconomicsForecast"
  | "TradingEconomicsMarketForecast"
  | "ReferenceAgg"
  | "HistoricalMarketCap"
  | "IpoProspectus"
  | "EarningsCalendar"
  | "DividendsCalendar"
  | "SplitsCalendar"
  | "HistoricalEmployeeCount"
  | "EtfInformation"
  | "EtfHoldings"
  | "AssetCatalog";
export type DatasetSearchSubject =
  | DatasetSearchSubjectAsset
  | DatasetSearchSubjectSymbol
  | DatasetSearchSubjectAssetName
  | DatasetSearchSubjectMacroConcept
  | DatasetSearchSubjectSource;
export type DiscoveryMacrobondFacets = {
  category?: MacrobondCategory[];
  currency?: MacrobondCurrency[];
  data_type?: MacrobondDataType[];
  exchange?: string[];
  frequency?: MacrobondFrequency[];
  include_discontinued?: OptionalBool;
  klass?: MacrobondClass[];
  must_have_revisions?: OptionalBool;
  /**
   * Explicit Macrobond-native Region value or unique declared compact-catalog name. Countries, aggregates, historical and opaque geography-entity values keep their native meaning; eu is Euro Area and wq is World (51 Countries). This axis is not a shared ISO2 country code. When no common country is supplied, omission leaves Macrobond search unrestricted.
   */
  region?: string;
} | null;
export type MacrobondCategory =
  | "rate"
  | "bank"
  | "bopa"
  | "caes"
  | "cons"
  | "demo"
  | "eqma"
  | "flof"
  | "fofi"
  | "lama"
  | "naac"
  | "pric"
  | "prod"
  | "surv"
  | "tour"
  | "trad"
  | "tran"
  | "fund"
  | "gpfi"
  | "fcst"
  | "bust"
  | "esgc";
export type MacrobondCurrency =
  | "usd"
  | "eur"
  | "cny"
  | "vnd"
  | "php"
  | "sek"
  | "mad"
  | "rsd"
  | "kwd"
  | "mwk"
  | "gel"
  | "dzd"
  | "kgs"
  | "mxn"
  | "czk"
  | "ngn"
  | "jod"
  | "zmw"
  | "kes"
  | "tzs"
  | "uah"
  | "mkd"
  | "bwp"
  | "nok"
  | "_try"
  | "inr"
  | "pln"
  | "idr"
  | "kzt"
  | "bdt"
  | "iqd"
  | "bam"
  | "npr"
  | "sar"
  | "ars"
  | "huf"
  | "clp"
  | "ron"
  | "lkr"
  | "bhd"
  | "mnt"
  | "jmd"
  | "mur"
  | "chf"
  | "krw"
  | "dkk"
  | "ils"
  | "cad"
  | "jpy"
  | "bsd"
  | "xbc"
  | "tjs"
  | "tpe"
  | "cdf"
  | "all"
  | "xaf"
  | "xfo"
  | "clf"
  | "tnd"
  | "xdr"
  | "aud"
  | "amd"
  | "tmm"
  | "aed"
  | "bif"
  | "bob"
  | "fkp"
  | "pgk"
  | "ern"
  | "cup"
  | "myr"
  | "sgd"
  | "bnd"
  | "cve"
  | "eek"
  | "xba"
  | "byr"
  | "zar"
  | "rol"
  | "crc"
  | "xag"
  | "xpd"
  | "zwd"
  | "zmk"
  | "lvl"
  | "pab"
  | "xpt"
  | "mmk"
  | "djf"
  | "wst"
  | "vuv"
  | "qar"
  | "gbp"
  | "top"
  | "gnf"
  | "hnl"
  | "sit"
  | "gwp"
  | "mzm"
  | "bmd"
  | "awg"
  | "szl"
  | "mro"
  | "khr"
  | "uzs"
  | "kyd"
  | "srd"
  | "irr"
  | "scr"
  | "gyd"
  | "ugx"
  | "uyu"
  | "sbd"
  | "kmf"
  | "xau"
  | "cou"
  | "lrd"
  | "lsl"
  | "ghc"
  | "gmd"
  | "mdl"
  | "azm"
  | "thb"
  | "hrk"
  | "kpw"
  | "cop"
  | "dop"
  | "fjd"
  | "sll"
  | "egp"
  | "mop"
  | "xbd"
  | "isk"
  | "yer"
  | "mvr"
  | "nad"
  | "lak"
  | "gip"
  | "cuc"
  | "etb"
  | "gtq"
  | "brl"
  | "veb"
  | "cyp"
  | "nzd"
  | "bbd"
  | "csd"
  | "rwf"
  | "hkd"
  | "xcd"
  | "xof"
  | "pkr"
  | "rub"
  | "pen"
  | "pyg"
  | "ggp"
  | "afa"
  | "shp"
  | "skk"
  | "bov"
  | "ang"
  | "sdd"
  | "ttd"
  | "xbb"
  | "twd"
  | "std"
  | "svc"
  | "sos"
  | "mgf"
  | "btn"
  | "omr"
  | "aoa"
  | "htg"
  | "lyd"
  | "lbp"
  | "bzd"
  | "ltl"
  | "mtl"
  | "mxv"
  | "xpf"
  | "nio"
  | "mga"
  | "syp"
  | "bgn"
  | "zwr"
  | "vef"
  | "ghs"
  | "mzn"
  | "zwl"
  | "sdg"
  | "azn"
  | "tmt"
  | "afn"
  | "bef"
  | "dem"
  | "esp"
  | "frf"
  | "iep"
  | "itl"
  | "luf"
  | "nlg"
  | "ats"
  | "pte"
  | "fim"
  | "grd"
  | "ecs"
  | "uyi"
  | "imp"
  | "cnh"
  | "sml"
  | "ssp"
  | "adf"
  | "xeu"
  | "byn"
  | "csk"
  | "yum"
  | "stn"
  | "mru"
  | "trl"
  | "ves"
  | "mxp"
  | "ved"
  | "sle"
  | "zwg"
  | "xcg";
export type MacrobondDataType =
  | "close"
  | "open"
  | "high"
  | "low"
  | "eop"
  | "average"
  | "mop"
  | "sett"
  | "closexsd"
  | "beginning"
  | "weighted"
  | "start"
  | "vl"
  | "lr";
export type MacrobondFrequency =
  "annual" | "bimonthly" | "daily" | "quadmonthly" | "monthly" | "quarterly" | "semiannual" | "weekly";
export type MacrobondClass = "stock" | "flow" | "step";
export type DiscoveryTradingEconomicsFacets = {
  /**
   * Optional Trading Economics category group narrowing that vendor's search. Markets searches only the markets catalog (indices, FX, commodities, bond yields); another group, such as Prices or Labour, searches only indicators in that group. Omit to search both Trading Economics catalogs.
   */
  category_group?: string;
  /**
   * Optional explicit Trading Economics-native country or aggregate code/name, resolved by its source vocabulary. WL/World, EA/Euro area and EU/European Union remain distinct; no country or proxy is guessed when omitted. A conflicting common country filter is a request-shape error.
   */
  country?: string;
} | null;
export type VariantDoubleStringBoolNullptrT = VariantDoubleStringBoolNullptrT1 & VariantDoubleStringBoolNullptrT2;
export type VariantDoubleStringBoolNullptrT1 = number | string | boolean | null;
export type VariantDoubleStringBoolNullptrT2 =
  | (number & (number | string | boolean | null))
  | ((number | string | boolean | null) & string)
  | (boolean & (number | string | boolean | null))
  | (null & (number | string | boolean | null));

export interface DiscoveryPresentationProtocol {
  AssetScreen: AssetScreen;
  AssetUniverseResponse: AssetUniverseResponse;
  DatasetBrowseGroup: DatasetBrowseGroup;
  DatasetCatalogEntry: DatasetCatalogEntry;
  DatasetCatalogResponse: DatasetCatalogResponse;
  DatasetCatalogRequest: DatasetCatalogRequest;
  DatasetCatalogSummary: DatasetCatalogSummary;
  DatasetSearchDataset: DatasetSearchDataset;
  DatasetSearchQuery: DatasetSearchQuery;
  DatasetSearchSubject: DatasetSearchSubject;
  DatasetSearchRequest: DatasetSearchRequest;
  DatasetSourceMetadataResponse: DatasetSourceMetadataResponse;
  DiscoveryDatasetRequest: DiscoveryDatasetRequest;
  DiscoveryLoaderBinding: DiscoveryLoaderBinding;
  DiscoveryMetadataRecord: DiscoveryMetadataRecord;
  DiscoveryResultReceipt: DiscoveryResultReceipt;
  DiscoverySearchResponse: DiscoverySearchResponse;
  DiscoverySelectors: DiscoverySelectors;
  DiscoverySourceAddress: DiscoverySourceAddress;
  DiscoveryStoredQueryResponse: DiscoveryStoredQueryResponse;
  ScreenAssetsRequest: ScreenAssetsRequest;
  DatasetSourceMetadataResponseConstructor: StudyDataConstructor;
}
export interface AssetScreen {
  all_of: AssetScreen[];
  any_of: AssetScreen[];
  asset_class?: AssetClass[] | null;
  base_currency?: string[] | null;
  category?: AssetCategory[] | null;
  country?: Country[] | null;
  delisted_after?: string;
  delisted_before?: string;
  exchange?: Exchange[] | null;
  ids?: string[] | null;
  index?: string[] | null;
  index_membership_mode?: IndexMembershipMode;
  industry?: StockIndustry[] | null;
  ipo_after?: string;
  ipo_before?: string;
  ipo_market_cap_max?: number;
  ipo_market_cap_min?: number;
  ipo_price_max?: number;
  ipo_price_min?: number;
  ipo_shares_max?: number;
  ipo_shares_min?: number;
  is_actively_trading?: OptionalBool | null;
  max_assets?: number;
  not?: SharedPtr_AssetScreen;
  order_by?: AssetScreenOrder;
  quote_currency?: string[] | null;
  sector?: StockSector[] | null;
  security_type?: SecurityType[] | null;
}
export interface AssetUniverseResponse {
  asset_count: number;
  definition?: AssetUniverseDefinition;
  qualifications: string[];
  result: DiscoverySearchResponse;
  universe_ref?: string;
}
export interface AssetUniverseDefinition {
  catalog_freshness?: CatalogFreshness;
  historical_integrity: HistoricalMembershipIntegrity[];
  index_rosters: IndexRosterProvenance[];
  membership_screen: AssetScreen;
  membership_window?: DiscoveryRequestedWindow;
  population?: UniversePopulation;
  scope: ScreenAssetsRequest;
  selection: AssetScreenSelectionContract;
}
export interface HistoricalMembershipIntegrity {
  address_conflict_count: number;
  completeness_verified: boolean;
  examples_truncated: boolean;
  identity_examples: HistoricalIdentityExample[];
  identity_review_count: number;
  index: string;
  note: string;
  scope: string;
  unmatched_removal_count: number;
  unresolved_count: number;
}
export interface HistoricalIdentityExample {
  event_dates: string[];
  provider_names: string[];
  ticker: string;
}
export interface IndexRosterProvenance {
  cache_disposition: string;
  cache_version?: number;
  catalog_checked_at: string;
  catalog_published_at: string;
  catalog_version: string;
  index: string;
  member_count: number;
  payload_fetched_at?: string;
  roster_hash: string;
  served_stale: boolean;
  source_as_of?: string;
  source_as_of_note?: string;
  source_endpoint: string;
  source_is_proxy: boolean;
  source_kind: string;
  source_provider: string;
  source_symbol?: string;
  unsupported_count: number;
}
export interface UniverseExclusion {
  id: string;
  reason: string;
  ticker: string;
}
export interface ScreenAssetsRequestScreen {
  current_cap_max_exclusive?: number;
  current_cap_min_exclusive?: number;
  kind: "screen";
  membership_window?: DiscoveryRequestedWindow;
  screen: AssetScreen;
}
export interface ScreenAssetsRequestSaved {
  current_cap_max_exclusive?: number;
  current_cap_min_exclusive?: number;
  kind: "saved";
  universe_ref: string;
}
export interface AssetScreenSelectionContract {
  point_in_time_indexes: string[];
  requires_point_in_time_gate: boolean;
  selection_semantics?: AssetScreenSelectionSemantics;
}
export interface DiscoverySearchResponse {
  collections?: DiscoveryCollectionSummary[] | null;
  counts: DiscoveryResultCounts;
  /**
   * Qualifications every delivered record shares, stated once here and omitted from the records (selection protocol v3). Under v3 a record belongs to the selection with its request_id, request_item_id and, when the record states one, requested_dataset.
   */
  qualifications?: string[] | null;
  receipt: DiscoveryResultReceipt;
  records: DiscoveryMetadataRecord[];
  records_complete: boolean;
  saved?: DatasetSavedSearchResult;
  selections?: DatasetSearchSelection[] | null;
  source_completeness: ExtentCompleteness;
}
export interface DiscoveryCollectionSummary {
  asset_count: number;
  availability_unknown: number;
  available: number;
  collection_ref: string;
  counts: DiscoveryResultCounts;
  index_rosters?: IndexRosterProvenance[] | null;
  loader?: DiscoveryLoaderBinding;
  request_id: string;
  requested_dataset?: DiscoveryDatasetRequest;
  screen_ref: string;
  source_completeness: ExtentCompleteness;
  unavailable: number;
}
export interface DiscoveryResultCounts {
  candidates: number;
  errors: number;
  resolved: number;
  stored_records: number;
  unavailable: number;
  unknown: number;
}
export interface DiscoveryLoaderBinding {
  category: DataCategory;
  registry_version: string;
  schema_ref: string;
  selectors?: DiscoverySelectors;
  source_id: string;
}
export interface DiscoverySelectorsFinancial {
  index_by?: FundamentalsIndexBy;
  kind: "financial";
  period?: FinancialsTimeframe;
}
export interface DiscoverySelectorsVintage {
  full_tape?: OptionalBool;
  kind: "vintage";
  nth?: number;
  revision?: VintageRevision;
}
export interface DiscoveryDatasetRequest {
  category: DataCategory;
  fields?: string[];
  requested_window?: DiscoveryRequestedWindow;
  selectors?: DiscoverySelectors;
}
export interface DiscoveryResultReceipt {
  captured_at: string;
  columns: string[];
  expires_at?: string;
  result_ref: string;
  retained: boolean;
  source_completeness: ExtentCompleteness;
  stored_complete: boolean;
  table: string;
}
export interface DiscoveryMetadataRecord {
  availability: DiscoveryAvailability;
  binding_ref?: string;
  coverage_basis: DiscoveryCoverageBasis;
  display_name?: string;
  error?: DiscoveryMetadataError;
  identity?: DiscoverySourceAddress;
  issuer?: CompanySearchCandidate;
  loader?: DiscoveryLoaderBinding;
  metadata?: DataExtentDTO;
  qualifications: string[];
  ranked_from?: number;
  record_ref: string;
  relevance?: number;
  request_id: string;
  request_item_id: string;
  requested_dataset?: DiscoveryDatasetRequest;
  source_search_completeness?: ExtentCompleteness;
  status: DiscoveryItemStatus;
  vendor?: DataVendor;
}
export interface DiscoverySourceAddressAsset {
  asset_id?: string;
  asset_type: AssetType;
  kind: "asset";
  ticker: string;
}
export interface DiscoverySourceAddressSeries {
  kind: "series";
  series_id: string;
  vendor: ResolvableVendor;
}
export interface DiscoverySourceAddressTeIndicator {
  country: string;
  indicator: string;
  kind: "te_indicator";
}
export interface DiscoverySourceAddressTeMarket {
  kind: "te_market";
  symbol: string;
}
export interface DiscoverySourceAddressTeRatings {
  country: string;
  kind: "te_ratings";
}
export interface DiscoverySourceAddressMbRelease {
  kind: "mb_release";
  release_id: string;
}
export interface DiscoverySourceAddressGlobalSource {
  kind: "global_source";
  source_id: string;
}
export interface CompanySearchCandidate {
  cik?: string;
  country?: string;
  currency?: string;
  cusip?: string;
  description?: string;
  exchange?: string;
  exchange_full_name?: string;
  industry?: string;
  ipo_date?: string;
  is_actively_trading?: OptionalBool;
  is_etf?: OptionalBool;
  is_fund?: OptionalBool;
  isin?: string;
  name?: string;
  profile_error?: string;
  profile_error_class?: FetchErrorClass;
  profile_name?: string;
  profile_symbol?: string;
  sector?: string;
  symbol: string;
}
export interface DataExtentDTO {
  ask?: string;
  asset_class?: string;
  catalog_asset?: AssetSpecification;
  catalog_exact_match?: OptionalBool;
  category?: string;
  country?: string;
  coverage_completeness?: ExtentCompleteness;
  currency?: string;
  data_source_id: string;
  delisted_date?: string;
  description?: string;
  display_name?: string;
  end?: string;
  entity_state?: string;
  error?: string;
  error_class?: FetchErrorClass;
  error_kind?: FetchErrorKind;
  exchange?: string;
  feedable?: OptionalBool;
  first_revision_time?: string;
  frequency?: string;
  has_revision_history?: OptionalBool;
  index_by?: FundamentalsIndexBy;
  industry?: string;
  ipo_date?: string;
  last_observation?: string;
  last_published_at?: string;
  market_coverage_definition?: MarketCoverageDefinitionDTO;
  metadata_end?: string;
  metadata_end_exceeded?: OptionalBool;
  metadata_endpoint?: string;
  min_tick?: string;
  multiplier?: string;
  period?: FinancialsTimeframe;
  provider_endpoint: string;
  queried_at: string;
  resolution?: HandleResolution;
  sector?: string;
  source_definition?: Extent__MacrobondSourceDefinition;
  start?: string;
  unit?: string;
  vendor: string;
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
export interface SavedDataset {
  archived: boolean;
  dataset_ref: string;
  descriptor: DatasetDescriptor;
  name: string;
  saved_at: string;
  source_ref?: string;
}
export interface DatasetDescriptor {
  content_sha256: string;
  evidence_ref?: string;
  limitations: string[];
  preparation: DatasetPreparation;
  schema_sha256: string;
  shape: DatasetShape;
  sources: DatasetProvenanceSource[];
}
export interface DatasetPreparation {
  enrichment: DatasetEnrichmentMode;
  implementation_version: string;
  import_options?: StructuredImportOptions;
  input_schema?: DataSourceSchema;
  instruction: string;
  origin: DatasetOrigin;
  provider?: string;
  provider_version?: string;
  purpose: DatasetPurpose;
  schema_choice: DatasetSchemaChoice;
}
export interface StructuredImportOptions {
  columns: DataSourceColumn[];
  delimiter: string;
  format: string;
  header: boolean;
  json_pointer?: string;
  null_values: string[];
  sheet?: string;
}
export interface DataSourceColumn {
  description?: string;
  display_name?: string;
  dtype: string;
  is_index?: boolean;
  is_index_alternative?: boolean;
  name: string;
  nullable: boolean;
  semantic?: string;
  synthetic?: boolean;
  transforms?: DataSourceValueTransform[];
  unit?: string;
}
export interface DataSourceValueTransform_ParseDateTime {
  format?: string;
  kind: "ParseDateTime";
}
export interface DataSourceValueTransform_FloorDay {
  kind: "FloorDay";
}
export interface DataSourceValueTransform_AssumeTimezone {
  kind: "AssumeTimezone";
  tz?: string;
}
export interface DataSourceSchema {
  columns: DataSourceColumn[];
  transforms?: DataSourcePostReadTransform[];
}
export interface DataSourcePostReadTransform_PromoteIndex {
  kind: "PromoteIndex";
}
export interface DataSourcePostReadTransform_CombineDateTime {
  date_col?: string;
  kind: "CombineDateTime";
  output_col?: string;
  time_col?: string;
}
export interface DataSourcePostReadTransform_AddContextColumn {
  col_name?: string;
  kind: "AddContextColumn";
  source_path?: string;
}
export interface DatasetSchemaChoiceAgent {
  mode: "agent";
}
export interface DatasetSchemaChoiceProvided {
  json_schema_text: string;
  mode: "provided";
}
export interface DatasetSchemaChoiceImported {
  mode: "imported";
}
export interface DatasetShapeTable {
  coverage: DatasetCoverage;
  format: "table";
  schema: DatasetTableSchema;
}
export interface DatasetCoverage {
  first_timestamp?: string;
  last_timestamp?: string;
  row_count: number;
}
export interface DatasetTableSchema {
  asset_field?: string;
  dataframe_metadata?: DataSourceFrameMetadata;
  frame_schema: DataSourceSchema;
  key_fields: string[];
  time_axis?: DatasetTimeAxis;
}
export interface DataSourceFrameMetadata {
  asset_class?: AssetClass;
  data_type: string;
  description: string;
  entity_columns: string[];
  foundation: DataFoundation;
  source_capabilities: DataSourceCapabilities;
}
export interface DataSourceCapabilities {
  availability_axis: SourceAvailabilityAxis;
  future_rows: SourceFutureCapability;
  predecessor: SourcePredecessorCapability;
  range: SourceRangeCapability;
}
export interface DatasetTimeAxis {
  assumed: boolean;
  date_only_convention?: string;
  meaning: DatasetTimeMeaning;
  source_precision: DatasetTimePrecision;
  source_timezone: string;
}
export interface DatasetShapeJson {
  format: "json";
  json_schema_text: string;
}
export interface DatasetProvenanceSourceFile {
  file_ref: string;
  kind: "file";
}
export interface DatasetProvenanceSourceWeb {
  content_sha256: string;
  evidence_ref?: string;
  fetched_at: string;
  kind: "web";
  snapshot_as_of?: string;
  url: string;
}
export interface DatasetProvenanceSourceDataset {
  dataset_ref: string;
  kind: "dataset";
}
export interface DatasetProvenanceSourceStudyResult {
  execution_ref: string;
  kind: "study_result";
  query_sha256: string;
  result_ref: string;
}
export interface DatasetSearchSelection {
  counts: DiscoveryResultCounts;
  delivered_records: number;
  has_more?: OptionalBool1;
  loader?: DiscoveryLoaderBinding1;
  /**
   * Delivered page number of this selection (selection protocol v2).
   */
  page?: number;
  /**
   * Qualifications every delivered record of this selection shares, stated once here and omitted from its records (selection protocol v3). A record's qualifications are its own, this selection's and the response's.
   */
  qualifications?: string[] | null;
  request_id: string;
  request_item_id: string;
  requested_dataset?: DiscoveryDatasetRequest;
  source_search_completeness?: ExtentCompleteness1;
  vendor?: DataVendor1;
}
/**
 * The loader every delivered record of this selection shares, omitted from those records (selection protocol v3).
 */
export interface DiscoveryLoaderBinding1 {
  category: DataCategory;
  registry_version: string;
  schema_ref: string;
  selectors?: DiscoverySelectors;
  source_id: string;
}
export interface DatasetCatalogEntry {
  documentation: string;
  endpoints: {
    [k: string]: DataSourceRegistryEndpoint;
  };
  implementations: DatasetCatalogImplementation[];
  source: DataSourceRegistrySource;
}
export interface DataSourceRegistryEndpoint {
  asset_class?: string;
  columns: DataSourceRegistryEndpointColumn[];
  description: string;
  entity_columns: string[];
  foundation?: string;
  id: string;
  index_alternatives: string[];
  index_column?: string;
  path: string;
  provider: string;
  refresh?: DataSourceRegistryRefresh;
  source_capabilities: DataSourceRegistrySourceCapabilities;
}
export interface DataSourceRegistryEndpointColumn {
  description?: string;
  display_name?: string;
  dtype: string;
  is_index: boolean;
  is_index_alternative: boolean;
  name: string;
  nullable: boolean;
  semantic?: string;
  synthetic: boolean;
  unit?: string;
}
export interface DataSourceRegistryRefresh {
  time: string;
  tz: string;
}
export interface DataSourceRegistrySourceCapabilities {
  availability_axis: string;
  future_rows: string;
  predecessor: string;
  range: string;
}
export interface DatasetCatalogImplementation {
  description: string;
  id: string;
  options: DataSourceRegistryOption[];
  outputs: DataSourceRegistryOutput[];
  signature: string;
}
export interface DataSourceRegistryOption {
  default_value?: RawJson;
  description: string;
  element_type: string;
  enum_type?: string;
  id: string;
  maximum?: number;
  minimum?: number;
  name: string;
  required: boolean;
  step: number;
  type: string;
  values: string[];
}
export interface DataSourceRegistryOutput {
  description: string;
  name: string;
  optional: boolean;
  semantic?: string;
  type: string;
}
export interface DataSourceRegistrySource {
  backing?: DataSourceRegistryBacking;
  constructor: DataSourceRegistrySourceConstructor;
  data_categories: string[];
  description: string;
  endpoint?: DataSourceRegistryEndpoint;
  endpoint_ids: string[];
  family: DataSourceRegistryFamily;
  impl_ids: string[];
  index_by?: DataSourceRegistrySelector;
  keys: DataSourceRegistryKey[];
  macro?: DataSourceRegistryMacro;
  name: string;
  options: DataSourceRegistryOption[];
  outputs: DataSourceRegistryOutput[];
  package: string;
  period?: DataSourceRegistrySelector;
  requires_futures_root: boolean;
  scope: DataSourceRegistryScope;
  signature: string;
  source_id: string;
  vendor?: string;
  window: DataSourceRegistryWindow;
}
export interface DataSourceRegistrySelector {
  default_value?: RawJson;
  enum_type: string;
  option: string;
  required: boolean;
  values: string[];
}
export interface DataSourceRegistryKey {
  from: string;
  option: string;
}
export interface DataSourceRegistryMacro {
  impl_selection?: DataSourceRegistryImplSelection;
  kwargs: string[];
  max_positional: number;
  min_positional: number;
  option_routing: DataSourceRegistryOptionRoute[];
  required_kwargs: string[];
  single_output: boolean;
}
export interface DataSourceRegistryImplSelection {
  cases: {
    [k: string]: string;
  };
  computed_helper?: string;
  default_impl?: string;
  dispatch: DataSourceRegistryImplDispatch[];
  enum_type?: string;
  extract_spec_field?: string;
  impl?: string;
  per_arg_spec_field?: string;
  per_output_from_list?: string;
  per_output_lookup: {
    [k: string]: string;
  };
  switch_kwarg?: string;
}
export interface DataSourceRegistryImplDispatch {
  equals_any: string[];
  impl: string;
  when_kwarg: string;
}
export interface DataSourceRegistryOptionRoute {
  default_boolean?: OptionalBool;
  default_number?: number;
  default_number_overrides: {
    [k: string]: number;
  };
  default_string?: string;
  default_strings?: string[] | null;
  distribute: boolean;
  extract_spec_field?: string;
  from?: string;
  mapping: {
    [k: string]: {
      [k: string]: string;
    };
  };
  only_when_impl_is: string[];
  reject_empty: boolean;
  require_literal?: string;
  to?: string;
  when_kwarg?: string;
  wrap_in_list: boolean;
}
export interface DatasetCatalogResponse {
  loader_registry_version: string;
  overview: string;
  registry_version: string;
  saved?: SavedDatasetListPage;
  sources: DatasetCatalogEntry[];
  summaries?: DatasetCatalogSummary[] | null;
}
export interface SavedDatasetListPage {
  items: SavedDataset[];
  next_cursor?: string;
}
export interface DatasetCatalogSummary {
  backing?: DataSourceRegistryBacking;
  browse_groups: DatasetBrowseGroup[];
  data_categories: string[];
  description: string;
  family: DataSourceRegistryFamily;
  keys: DataSourceRegistryKey[];
  name: string;
  requires_futures_root: boolean;
  scope: DataSourceRegistryScope;
  source_id: string;
  vendor?: string;
  window: DataSourceRegistryWindow;
}
export interface DatasetCatalogRequest {
  include_details: boolean;
  /**
   * Include Backend-owned planner guidance. Set false for a compact UI directory; overview is then empty. Detailed source entries and saved metadata retain their separate selection controls.
   */
  include_overview?: boolean;
  include_saved: boolean;
  /**
   * Include compact structured summaries of built-in dataset constructors. Uses source_ids when supplied; otherwise includes the complete directory. Does not load observations or establish account access or coverage.
   */
  include_summaries?: boolean;
  saved_cursor?: string;
  saved_limit?: number;
  source_ids: string[];
}
export interface DatasetSearchDataset {
  /**
   * Native categories sharing fields, selectors and requested_window. Use separate groups when settings differ. Each category retains its compatibility checks and attribution; expanded dataset limit is 64.
   */
  categories?: DataCategory[];
  category?: DataCategory1;
  fields?: string[];
  requested_window?: DiscoveryRequestedWindow;
  selectors?: DiscoverySelectors;
}
export interface DatasetSearchQuery {
  /**
   * Native dataset needs applied to every subject in this request. Choose categories compatible with the subject kind and vendor in the dataset directory. Split independent subject/product needs into separate requests. Omit or pass [] when only resolving identity. A macro_concept with no datasets searches Macrobond series, Trading Economics indicators and the Trading Economics markets catalog (indices, FX, commodities, bond yields).
   */
  datasets?: DatasetSearchDataset[];
  /**
   * Ranked identities delivered per subject and dataset in the first page, 1..25 (default 10). Raise it only when the default page lacks the requested measurement. The complete pool is stored either way; later pages use the request's page field.
   */
  page_size?: number;
  request_id: string;
  subjects: DatasetSearchSubject[];
}
export interface DatasetSearchSubjectAsset {
  /**
   * Native catalogue asset_id copied from a returned asset identity, with its single ticker. A returned FX or crypto ticker such as BTC-USD also resolves without it.
   */
  asset_id?: string;
  asset_type: AssetType;
  kind: "asset";
  /**
   * One asset ticker. Supply ticker or nonempty tickers, never both.
   */
  ticker?: string;
  /**
   * Asset tickers sharing asset_type; supply instead of ticker. Order and per-asset attribution are preserved. Expanded subject limit is 256.
   */
  tickers?: string[];
}
export interface DatasetSearchSubjectSymbol {
  asset_type?: AssetType;
  exchange?: string;
  kind: "symbol";
  symbol: string;
}
export interface DatasetSearchSubjectAssetName {
  asset_type?: AssetType;
  country?: string;
  exchange?: string;
  kind: "asset_name";
  name: string;
}
export interface DatasetSearchSubjectMacroConcept {
  /**
   * Complete economic measurement intent used for relevance ranking, including meaningful level/growth, real/nominal, frequency and unit distinctions. This subject supports Macrobond and Trading Economics categories, not instrument DailyBars/MinuteBars. Use asset/symbol/asset_name for instrument products. This text is also used for provider retrieval when keywords is omitted.
   */
  concept: string;
  /**
   * Common country ISO2 codes or unique exact source-catalog country names, ASCII-case-insensitive with outer ASCII whitespace ignored. Japan and JP select the same country. Ambiguous names or native-only codes require explicit native facets; EU and EA do not have the same meaning across vendors. Omit or pass [] for unscoped search. Source definitions, coverage and access remain independent facts.
   */
  geographies?: string[];
  /**
   * Optional short provider retrieval terms. These replace concept only for literal provider text search; relevance ranking still uses the full concept. Trading Economics catalog discovery retains the candidate catalog for semantic ranking. Keep separate analysis requirements and native facets out of this literal query.
   */
  keywords?: string;
  kind: "macro_concept";
  macrobond?: DiscoveryMacrobondFacets;
  /**
   * Macro providers to search: TradingEconomics and/or Macrobond. Omit or pass [] to search every macro catalog together. Naming Macrobond also excludes series the current subscription cannot load, listed in one explicit row. A dataset category or native facet for an excluded provider is a request-shape error.
   */
  providers?: DataVendor[];
  trading_economics?: DiscoveryTradingEconomicsFacets;
}
export interface DatasetSearchSubjectSource {
  address: DiscoverySourceAddress;
  kind: "source";
}
export interface DatasetSearchRequest {
  /**
   * Optional company identity candidate limit. Vendor limits remain explicit; macro retrieval uses its native source limits independently. This does not limit the saved collected pool or the separate model-facing preview.
   */
  candidate_limit?: number;
  page?: DatasetSearchPage;
  requests: DatasetSearchQuery[];
  saved_query?: string;
}
/**
 * Read a later page of one returned selection instead of searching. Supply requests: [] and no other options. Nothing is refetched or re-ranked.
 */
export interface DatasetSearchPage {
  /**
   * Page number, 2 or later; the search response delivered page 1 with the request's page_size.
   */
  page: number;
  /**
   * selections[].request_item_id of the selection to continue.
   */
  request_item_id: string;
  requested_dataset?: DiscoveryDatasetRequest1;
  /**
   * receipt.result_ref from the search response being continued.
   */
  result_ref: string;
}
/**
 * selections[].requested_dataset of that selection, copied exactly; omit when it has none.
 */
export interface DiscoveryDatasetRequest1 {
  category: DataCategory;
  fields?: string[];
  requested_window?: DiscoveryRequestedWindow;
  selectors?: DiscoverySelectors;
}
export interface DatasetSourceMetadataResponse {
  constructor?: StudyDataConstructor;
  error?: DiscoveryMetadataError;
  record: DiscoveryMetadataRecord;
  result_ref: string;
}
export interface StudyDataConstructor {
  dataset: DiscoveryDatasetRequest;
  endpoint: DataSourceRegistryEndpoint;
  loader: DiscoveryLoaderBinding;
  qualifications: string[];
  source: DataSourceRegistrySource;
}
export interface DiscoveryStoredQueryResponse {
  columns: DescribeColumn[];
  has_more: boolean;
  next_cursor?: string;
  original_receipts: DiscoveryResultReceipt[];
  /**
   * Opaque owner-scoped receipt for the exact delivered request and output page. It is comparison evidence, not a loader binding or retained source pool.
   */
  query_ref?: string;
  receipts: DiscoveryResultReceipt[];
  records: DiscoveryMetadataRecord[];
  result_refs: string[];
  /**
   * Current retained authority for this replayed query proof. Original result refs, receipts, expiry, total_stored, has_more and next_cursor are archival query facts; they are not live paging handles or an active retained source pool.
   */
  retained_in_handoff?: string;
  returned: number;
  rows: VariantDoubleStringBoolNullptrT[][];
  total_matching: number;
  total_stored: number;
}
export interface DescribeColumn {
  approx_unique: number;
  max_value?: string;
  min_value?: string;
  name: string;
  null_percentage: number;
  only_in_tables: string[];
  type: string;
  unique_values: string[];
}
