"""EGX symbol metadata and provider ticker format helpers."""

from __future__ import annotations

# Active EGX equities from StockAnalysis' Egyptian Stock Exchange list, fetched
# on 2026-05-24. The page currently reports 223 stocks.
_EGX_STOCKS: tuple[tuple[str, str], ...] = (
    ("COMI", "Commercial International Bank Egypt (CIB) S.A.E."),
    ("TMGH", "Talaat Moustafa Group Holding"),
    ("SWDY", "El Sewedy Electric Company"),
    ("ETEL", "Telecom Egypt Company"),
    ("EGAL", "Egypt Aluminum"),
    ("MFPC", "Misr Fertilizer Production Company"),
    ("QNBE", "Qatar National Bank"),
    ("EAST", "Eastern Company S.A.E"),
    ("ABUK", "Abu Qir Fertilizers & Chemical Industries Company (S.A.E)"),
    ("ALCN", "Alexandria Container&Cargo Handling Company"),
    ("ORAS", "Orascom Construction PLC"),
    ("EFIH", "e-finance for Digital and Financial Investments S.A.E."),
    ("HDBK", "Housing and Development Bank- Egypt (S.A.E)"),
    ("FWRY", "Fawry for Banking Technology and Electronic Payments S.A.E."),
    ("SCTS", "Suez Canal Company for Technology Settling (S.A.E)"),
    ("ADIB", "Abu Dhabi Islamic Bank - Egypt - S.A.E"),
    ("EMFD", "Emaar Misr for Development Company (S.A.E.)"),
    ("GPPL", "Golden Pyramids Plaza S.A.E."),
    ("VLMR", "Valmore Holding S.A.E."),
    ("VLMRA", "Valmore Holding S.A.E."),
    ("ORHD", "Orascom Development Egypt S.A.E."),
    ("PHDC", "Palm Hills Developments S.A.E."),
    ("EFID", "Edita Food Industries Company (S.A.E)"),
    ("HRHO", "EFG Holding Company S.A.E"),
    ("CANA", "Suez Canal Bank (S.A.E)"),
    ("JUFO", "Juhayna Food Industries S.A.E."),
    ("BTFH", "Beltone Holding S.A.E"),
    ("IRON", "Egyptian Iron and Steel Company"),
    ("FERC", "Ferchem Misr for fertilizers and chemicals S.A.E"),
    ("RAYA", "Raya Holding Company for Financial Investments (S.A.E)"),
    ("FAIT", "Faisal Islamic Bank of Egypt"),
    ("FAITA", "Faisal Islamic Bank of Egypt"),
    ("CIEB", "Credit Agricole - Egypt Bank (S.A.E.)"),
    ("GBCO", "GB Corp"),
    ("EGCH", "Egyptian Chemical Industries"),
    ("OCDI", 'Sixth of October for Development and Investment Company "SODIC" (S.A.E.)'),
    ("HELI", "Heliopolis Co. for Housing & Development"),
    ("EXPA", "Export Development Bank of Egypt (S.A.E.)"),
    ("VALU", "U Consumer Finance S.A.E."),
    ("CLHO", "Cleopatra Hospitals Group S.A.E."),
    ("CCAP", "QALA For Financial Investments"),
    ("EFIC", "Egyptian Financial and Industrial SAE"),
    ("ARCC", "Arabian Cement Company S.A.E."),
    ("EGTS", "Egyptian Resorts Company (S.A.E)"),
    ("SKPC", "Sidi Kerir Petrochemicals Co."),
    ("MCQE", "Misr Cement (Qena) Company (S.A.E)"),
    ("EGSA", "The Egyptian Satellite Company Nilesat"),
    ("TAQA", "TAQA Arabia S.A.E."),
    ("POUL", "Cairo Poultry Company S.A.E."),
    ("SCEM", "Sinai Cement Co. (S.A.E)"),
    ("MTIE", "MM Group for Industry and International Trade S.A.E."),
    ("SAUD", "alBaraka Bank Egypt S.A.E."),
    ("CIRA", "Cairo For Investment And Real Estate Developments-CIRA Education"),
    ("UBEE", "The United Bank"),
    ("MBSC", "Misr Beni Suef Cement Co. S.A.E"),
    ("ORWE", "Oriental Weavers Carpets Company (S.A.E)"),
    ("MASR", "Madinet Masr For Housing and Development"),
    ("PHAR", "Egyptian International Pharmaceutical Industries Company"),
    ("CICH", "CI Capital Holding For Financial Investments (S.A.E)"),
    ("EGBE", "Egyptian Gulf Bank (S.A.E)"),
    ("MHOT", "Misr Hotels Company"),
    ("ATQA", "Misr National Steel - Ataqa"),
    ("ISPH", "Ibnsina Pharma"),
    ("MOIL", "Maridive and Oil Services S.A.E."),
    ("TALM", "Taaleem Management Services Company S.A.E."),
    ("AMOC", "Alexandria Mineral Oils Company"),
    (
        "RMDA",
        "Tenth of Ramadan for Pharmaceutical Industries and Diagnostic Reagents (Rameda) (S.A.E)",
    ),
    ("IFAP", "International Company for Agricultural Crops"),
    ("CSAG", "Canal Shipping Agencies Company"),
    ("BINV", "B Investments Holding S.A.E."),
    ("SPHT", "El Shams Pyramids Co. For Hotels & Touristic Projects S.A.E"),
    ("OLFI", "Obour Land for Food Industries S.A.E."),
    ("BONY", "Bonyan for Development and Trade"),
    ("NIPH", "EI- Nile Co. for Pharmaceuticals and Chemical Industries"),
    ("OIH", "Orascom Investment Holding S.A.E."),
    ("MIPH", "MINAPHARM Pharmaceuticals"),
    ("DOMT", "Arabian Food Industries Company (DOMTY) - S.A.E"),
    ("ISMQ", "Iron & Steel for Mines & Quarries"),
    ("EGAS", "Egypt Gas Company SAE"),
    ("SUGR", "Delta Sugar Company"),
    ("ELEC", "Electro Cable Egypt"),
    ("AMES", "Alexandria New Medical Center"),
    ("MOIN", "Mohandes Insurance Company"),
    ("ACAP", "A Capital Holding"),
    ("BIOC", "GlaxoSmithKline S.A.E"),
    ("MPRC", "Egyptian Media Production City"),
    ("ZMID", "Zahraa El Maadi Investment and Development Company SAE"),
    ("AXPH", "Alexandria Co. For Pharmaceuticals & Chemical Industries"),
    ("PRDC", "Pioneers Properties For Urban Development - PRE Group"),
    ("CNFN", "Contact Financial Holding S.A.E."),
    ("NINH", "Nozha International Hospital"),
    ("NAPR", "National Printing Company S.A.E."),
    ("CPCI", "Kahira Pharmaceuticals & Chemical Industries Company"),
    ("SPIN", "Alexandria Spinning & Weaving Co."),
    ("GOUR", "Gourmet Egypt.Com Foods"),
    ("PHTV", "Pyramisa Hotels & Resorts"),
    ("ENGC", "Industrial Engineering Company for Construction and Development (ICON) (S.A.E)"),
    ("MFSC", "Egypt Free Shops Co."),
    ("DSCW", "Dice For Ready-Made Garments (SAE)"),
    ("MPCI", "Memphis Pharmaceuticals & Chemical Industries"),
    ("GSSC", "General Co. For Silos & Storage"),
    ("AMIA", "Arab Moltaqa Investments Company"),
    ("SVCE", "South Valley Cement Company"),
    ("OCPH", "October Pharma S.A.E"),
    ("GDWA", "Gadwa for Industrial Development"),
    ("WCDF", "Middle & West Delta Flour Mills"),
    ("MICH", "Misr Chemical Industries Co."),
    ("SAIB", "Societe Arabe Internationale de Banque S.A.E"),
    ("KABO", "El-Nasr Clothing & Textiles Co. (KABO)"),
    ("UEFM", "Upper Egypt Mills Company J.S.C"),
    ("ACTF.CA", "Act Financial"),
    ("UNIT", "United Co. for Housing & Development - S.A.E."),
    ("ACAMD", "Arab Co.,for asset management and development"),
    ("OFH", "O B Financial Holding S.A.E"),
    ("ARAB", "Arab Developers Holding"),
    ("AJWA", "AJWA For Food Industries Co. Egypt"),
    ("CFGH", "Concrete Fashion Group For Commercial and Industrial investments S.A.E"),
    ("ACGC", "Arabia Cotton Ginning Company"),
    ("KZPC", "Kafr El Zayat For Pesticides & Chemicals Co.(S.A.E)"),
    ("ADCI", "The Arab Drug Company"),
    ("AMER", "Amer Group Holding Company S.A.E."),
    ("SDTI", "SHARM DREAMS Co. for Touristic Investment S.A.E"),
    ("GGRN", "Go Green For Agricultural Investment And Development"),
    ("AFMC", "Alexandria Flour Mills"),
    ("ASCM", "ASEC Company for Mining ASCOM, S.A.E"),
    ("ISMA", "Ismailia / Misr Poultry Company S.A.E"),
    ("LCSW", "Lecico Egypt (S.A.E.)"),
    ("PHGC", "Premium Healthcare Group"),
    ("ELKA", "Cairo for Housing and Development Company (S.A.E)"),
    ("INFI", "Ismailia National Co. for Food Industries"),
    ("SNFC", "Sharkia National Company for Food Security"),
    ("NAHO", "Naeem Holding Company For Investments (S.A.E - Free Zone)"),
    ("EDFM", "East Delta Flour Mills"),
    ("SMFR", "Samad Misr EGYFERT.S.A.E"),
    ("ADPC", "The Arab Dairy Products Co."),
    ("DAPH", "Development & Engineering Consultants"),
    ("ATLC", "Al Tawfeek Leasing Company"),
    ("ELSH", "Al Shams Housing and Urbanization SAE"),
    ("EALR", "Arab Company For Land Reclamation"),
    ("RACC", "Raya Customer Experience"),
    ("ETRS", "Egyptian Transport and Commercial Services Company S.A.E."),
    ("ZEOT", "Extracted Oil & Derivatives Co."),
    ("MOSC", "Misr Oils & Soap"),
    ("WKOL", "Wadi Kom Ombo For Land Reclamation Co."),
    ("IDRE", "Ismailia Development and Real Estate Co"),
    ("SCFM", "South Cairo and Giza Flour Mills and Bakeries Company"),
    ("CEFM", "Middle Egypt Flour Mills"),
    ("MPCO", "Mansoura Poultry co.S.A.E"),
    ("ECAP", "Al Ezz Ceramics & Porcelain Co."),
    ("EHDR", "Egyptians for Housing & Development Co."),
    ("MENA", "Mena for Touristic & Real Estate Investment"),
    ("MILS", "North Cairo Flour Mills"),
    ("OBRI", "El-Ebour Co. for Real Estate Investment S.A.E."),
    ("DEIN", "Delta Insurance Company"),
    ("GPIM", "GPI for Urban Growth"),
    ("AALR", "General Company For Land Reclamation, Development & Reconstruction"),
    ("CRST", "Creast Mark For Contracting And Real Estate Development"),
    ("NDRL", "National Drilling Company"),
    ("NARE", "Naeem Real Estate Holding Group"),
    ("CERA", "The Arab Ceramic Co."),
    ("ALRA", "Atlas for Investment & Food Industries"),
    ("ODIN", "ODIN Investments (S.A.E)"),
    ("PRCL", "The General Company for Ceramic and Porcelain Products"),
    ("NHPS", "National Company for Housing Professional Syndicates SAE"),
    ("NCCW", "Nasr Company for Civil Works"),
    ("MEPA", "Medical Packaging Company"),
    ("ALUM", "Arab Aluminum Company (S.A.E)"),
    ("POCO", "Port Said Containers And Cargo Handling Co."),
    ("AIDC", "Arabia for Investment and Development S.A.E."),
    ("UEGC", 'El-Saeed Company for Contracting and Real Estate Investment "SCCD" (S.A.E.)'),
    ("MAAL", "Marseille Almasreia Alkhalegeya For Holding Investment SAE"),
    ("COSG", "Cairo Oil & Soap Company"),
    ("RTVC", "Remco Tourism Villages Construction"),
    ("CAED", "Cairo Educational Services SAE"),
    ("SEIG", "Saudi Egyptian Investment & Finance Co. S.A.E"),
    ("SEIGA", "Saudi Egyptian Investment & Finance Co. S.A.E"),
    ("SIPC", "Sabaa International Company for Pharmaceutical and Chemical Industry"),
    ("EBSC", "Osool ESB Securities Brokerage"),
    ("GTEX", "GTEX for Commercial and Industrial Investments S.A.E"),
    ("GGCC", "Giza General - Contracting and Real Estate Investment S.A.E"),
    ("RREI", "Arab Real Estate Investment Co."),
    ("APSW", "Unirab Polvara Spinning & Weaving Co."),
    ("MEGM", "Middle East Glass Manufacturing Company S.A.E."),
    ("PRMH", "Prime Holding S.A.E"),
    ("ICLE", "International Company for Leasing S.A.E."),
    ("AFDI", "Al Ahly for Development & Investment"),
    ("GTWL", "Golden Textiles & Clothes Wool"),
    ("ANFI", "Tycoon Holding Company For Financial Investments"),
    ("DTPP", "Delta Co. For Printing & Packaging S.A.E"),
    ("RAKT", "Rakta Paper Manufacturing Company"),
    ("MOED", "The Egyptian Modern Education Systems, S.A.E."),
    ("MCRO", "Macro Group Pharmaceuticals (Macro Capital) S.A.E"),
    ("TANM", "Tanmiya For Real Estate Investment (S.A.E)"),
    ("KRDI", "AlKhair River for Development Agricultural Investment and Environmental Services"),
    ("UNIP", "Universal For Paper and Packaging Materials"),
    ("SPMD", "Speed Medical Co"),
    ("RUBX", "Rubex International for Plastic and Acrylic Manufacturing"),
    ("ARVA", "Arab Valves Company"),
    ("ASPI", "Aspire Capital Holding for Financial Investments"),
    ("ROTO", "Rowad Tourism Company"),
    ("KWIN", "El Kahera El Watania Investment"),
    ("AIHC", "Arabia Investments Holding"),
    ("AREH", "Real Estate Egyptian Consortium S.A.E"),
    ("EEII", "Arab Engineering Industries"),
    ("CCRS", "Gulf Canadian Company for Arab Real Estate Investment"),
    ("EASB", "Egyptian Arabian Company (Themar) for securities Brokerage EAC"),
    ("ICID", "International Co. For Investment & Development"),
    ("GRCA", "Grand Capital for Financial Investments"),
    ("EPCO", "Egypt for Poultry"),
    ("ELWA", "El Wadi for International and Investment Development SAE"),
    ("ELNA", "El Nasr Manufacturing Agricultural Crops S.A.E"),
    ("LUTS", "Lotus Agri Capital"),
    ("DGTZ", "I Wave Beyond Your Expectations"),
    ("GIHD", "Gharbia Islamic Housing Development Company"),
    ("DCCC", "Damietta Container & Cargo Handling Co."),
    ("TRTO", "Trans Oceans Tours"),
    ("NEDA", "Northern Upper Egypt For Development & Agricultural Production Co."),
    ("MMAT", "Marsa Marsa Alam For Tourism Development SAE"),
    ("EPPK", "El Ahram Co. For Printing And Packaging SAE"),
    ("GMCI", "GMC Group For Industrial Commercial & Financial Investments"),
    ("EOSB", "El Orouba Securities Brokerage"),
    ("CPME", "Catalyst Partners"),
    ("COPR", "Copper for Commercial Investment & Real Estate Development"),
)

_KNOWN_SECTORS = {
    "COMI": "Financials",
    "TMGH": "Real Estate",
    "SWDY": "Industrials",
    "ETEL": "Communication Services",
    "ORAS": "Industrials",
    "HRHO": "Financials",
    "BTFH": "Financials",
    "PHDC": "Real Estate",
    "ORWE": "Consumer Discretionary",
    "ISPH": "Healthcare",
    "EAST": "Consumer Staples",
    "MFPC": "Materials",
    "EMFD": "Real Estate",
    "FWRY": "Information Technology",
    "JUFO": "Consumer Staples",
    "IRON": "Materials",
    "AMOC": "Energy",
    "SKPC": "Materials",
    "PHAR": "Healthcare",
    "CLHO": "Healthcare",
    "RAYA": "Information Technology",
    "DOMT": "Consumer Staples",
    "MASR": "Real Estate",
    "QNBE": "Financials",
    "HDBK": "Financials",
    "SCEM": "Materials",
}

_ALIASES = {
    "CIBEA": "COMI",
    "DOMTY": "DOMT",
    "EIPICO": "PHAR",
    "MNHD": "MASR",
    "QNBA": "QNBE",
    "SINAI": "SCEM",
}


def _yahoo_ticker(symbol: str) -> str:
    return symbol if "." in symbol else f"{symbol}.CA"


EGX_SYMBOLS: dict[str, dict[str, str]] = {
    symbol: {
        "name": name,
        "sector": _KNOWN_SECTORS.get(symbol, "Unknown"),
        "yahoo_ticker": _yahoo_ticker(symbol),
    }
    for symbol, name in _EGX_STOCKS
}


def _canonical(symbol: str) -> str:
    s = symbol.upper()
    return _ALIASES.get(s, s)


def provider_formats(symbol: str, provider: str) -> list[str]:
    """Return ticker formats to try for a provider."""
    original = symbol.upper()
    s = _canonical(original)
    meta = EGX_SYMBOLS.get(s, {})

    if "." in s:
        return [s]

    stripped = s[:-2] if s.endswith("EA") else s
    yahoo_ticker = meta.get("yahoo_ticker", _yahoo_ticker(s))

    if provider == "alpha_vantage":
        return list(dict.fromkeys([s, f"{s}.EGX", yahoo_ticker, f"{s}.EG", stripped]))
    if provider == "finnhub":
        return list(dict.fromkeys([s, f"{s}.EGX", f"EGX:{s}", yahoo_ticker, stripped]))
    if provider == "yahoo":
        return list(dict.fromkeys([yahoo_ticker, f"{s}.EG", s, f"{s}.EGX", f"{stripped}.CA"]))
    return [s]


def get_yahoo_ticker(symbol: str) -> str | None:
    entry = EGX_SYMBOLS.get(_canonical(symbol))
    return entry["yahoo_ticker"] if entry else None


def get_symbol_name(symbol: str) -> str | None:
    entry = EGX_SYMBOLS.get(_canonical(symbol))
    return entry["name"] if entry else None


def is_valid_symbol(symbol: str) -> bool:
    return _canonical(symbol) in EGX_SYMBOLS


def all_symbols() -> list[dict[str, str]]:
    return [{"symbol": sym, **meta} for sym, meta in EGX_SYMBOLS.items()]
