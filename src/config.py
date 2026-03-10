from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = ROOT / "data"
OUT_DIR = ROOT / "outputs"
FIG_DIR = OUT_DIR / "figures"
INT_DIR = OUT_DIR / "intermediate"

OUT_DIR.mkdir(exist_ok=True)
FIG_DIR.mkdir(exist_ok=True)
INT_DIR.mkdir(exist_ok=True)

RAW_PATH = DATA_DIR / "raw_financials.parquet"
LOC_PATH = DATA_DIR / "business_locations.parquet"

# Part A intermediate files
CAND_ZIP_PATH = INT_DIR / "candidates_zip.parquet"
MATCH_ZIP_PATH = INT_DIR / "matches_zip.parquet"
CAND_FALLBACK_TOPK_PATH = INT_DIR / "cand_fallback_topk.parquet"
MATCH_FALLBACK_PATH = INT_DIR / "matches_fallback.parquet"
FINAL_MATCHES_PATH = INT_DIR / "final_matches.parquet"

# Part A deliverable
FIN_TABLE_PATH = OUT_DIR / "financial_table.parquet"
FIN_TABLE_CSV_PATH = OUT_DIR / "financial_table.csv"

# Part B deliverables
FIN_FINAL_PATH = OUT_DIR / "financial_table_final.parquet"
FIN_FINAL_CSV_PATH = OUT_DIR / "financial_table_final.csv"

# Part B intermediate files
M1_PATH = INT_DIR / "financial_table_m1.parquet"
M2_PATH = INT_DIR / "financial_table_m2.parquet"

# DuckDB resource limits - (Adjust based your available system resources)
DUCKDB_THREADS = 4
DUCKDB_MEMORY = "3GB"

# Matching thresholds
MATCH_HI = 90
MATCH_LO = 85
GAP_MIN = 3

# Fuzzy weights
W_NAME = 0.35
W_ADDR = 0.65

# Fallback settings
TOPK = 10

