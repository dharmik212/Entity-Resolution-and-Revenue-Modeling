from pathlib import Path
from .duckdb_utils import connect_duckdb

def run_part_a_checks(financial_table_path: Path, final_matches_path: Path):
    con = connect_duckdb(threads=2, memory_limit="2GB")

    coverage = con.execute(f"""
    SELECT
      COUNT(*) AS total_raw_rows,
      SUM(matched_location_id IS NOT NULL) AS matched_rows,
      SUM(matched_location_id IS NULL) AS unmatched_rows,
      ROUND(100.0 * SUM(matched_location_id IS NOT NULL) / COUNT(*), 2) AS matched_pct
    FROM read_parquet('{financial_table_path.as_posix()}')
    """).df()

    status = con.execute(f"""
    SELECT
      COALESCE(match_status, 'unmatched') AS match_status,
      COUNT(*) AS n,
      ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM read_parquet('{financial_table_path.as_posix()}')), 2) AS pct
    FROM read_parquet('{financial_table_path.as_posix()}')
    GROUP BY 1
    ORDER BY n DESC
    """).df()

    uniq = con.execute(f"""
    SELECT
      COUNT(*) AS match_rows,
      COUNT(DISTINCT raw_id) AS distinct_raw_id,
      (COUNT(*) - COUNT(DISTINCT raw_id)) AS duplicate_raw_id_rows
    FROM read_parquet('{final_matches_path.as_posix()}')
    """).df()

    return coverage, status, uniq
