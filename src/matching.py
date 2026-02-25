import re
import unicodedata
import pandas as pd
from rapidfuzz import fuzz

# Regular expression to match common legal entity words in names
LEGAL_WORDS = r"\b(inc|llc|l\.l\.c|corp|corporation|co|company|ltd|limited|pllc)\b"
# Regular expression to match unit/apartment identifiers in addresses
UNIT_WORDS  = r"\b(apt|apartment|unit|ste|suite|#)\b"

def norm_basic(s):
    s = "" if s is None else str(s)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = s.lower().strip()
    s = re.sub(r"[^\w\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def norm_name(s):
    s = norm_basic(s)
    s = re.sub(LEGAL_WORDS, " ", s)
    s = s.replace("&", " and ")
    s = re.sub(r"\s+", " ", s).strip()
    return s

def norm_address(s):
    s = norm_basic(s)
    s = re.sub(UNIT_WORDS + r".*$", " ", s)   
    s = re.sub(r"\bstreet\b", "st", s)
    s = re.sub(r"\broad\b", "rd", s)
    s = re.sub(r"\bavenue\b", "ave", s)
    s = re.sub(r"\bboulevard\b", "blvd", s)
    s = re.sub(r"\bdrive\b", "dr", s)
    s = re.sub(r"\blane\b", "ln", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def zip5(z):
    z = "" if z is None else str(z).strip()
    m = re.search(r"\d{5}", z)
    return m.group(0) if m else ""

def add_standard_cols_raw(raw_df: pd.DataFrame) -> pd.DataFrame:
    raw_df = raw_df.copy()
    raw_df["name_norm"]  = raw_df["name"].map(norm_name)
    raw_df["addr_norm"]  = raw_df["address"].map(norm_address)
    raw_df["city_norm"]  = raw_df["city"].map(norm_basic)
    raw_df["state_norm"] = raw_df["state"].map(norm_basic)
    raw_df["zip5"]       = raw_df["postal_code"].map(zip5)
    raw_df["block_zip"]  = raw_df["state_norm"] + "|" + raw_df["zip5"]
    raw_df["zip3"]       = raw_df["zip5"].str[:3]
    raw_df["block_fallback"] = raw_df["state_norm"] + "|" + raw_df["city_norm"] + "|" + raw_df["zip3"]
    return raw_df

def add_standard_cols_loc(loc_df: pd.DataFrame) -> pd.DataFrame:
    loc_df = loc_df.copy()
    loc_df["name_norm"]  = loc_df["name"].map(norm_name)
    loc_df["addr_norm"]  = loc_df["street_address"].map(norm_address)
    loc_df["city_norm"]  = loc_df["city"].map(norm_basic)
    loc_df["state_norm"] = loc_df["state"].map(norm_basic)
    loc_df["zip5"]       = loc_df["postal_code"].map(zip5)
    loc_df["block_zip"]  = loc_df["state_norm"] + "|" + loc_df["zip5"]
    loc_df["zip3"]       = loc_df["zip5"].str[:3]
    loc_df["block_fallback"] = loc_df["state_norm"] + "|" + loc_df["city_norm"] + "|" + loc_df["zip3"]
    return loc_df

def score_candidates(df: pd.DataFrame, w_name=0.35, w_addr=0.65) -> pd.DataFrame:
    df = df.copy()
    df["name_score"] = [fuzz.token_set_ratio(a,b) for a,b in zip(df["raw_name_norm"], df["loc_name_norm"])]
    df["addr_score"] = [fuzz.token_set_ratio(a,b) for a,b in zip(df["raw_addr_norm"], df["loc_addr_norm"])]
    df["final_score"] = w_name*df["name_score"] + w_addr*df["addr_score"]
    return df