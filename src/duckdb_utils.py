import duckdb
from . import config

def connect_duckdb(threads: int = config.DUCKDB_THREADS, memory_limit: str = config.DUCKDB_MEMORY) -> duckdb.DuckDBPyConnection:
    con = duckdb.connect()
    con.execute(f"SET threads = {threads}")
    con.execute(f"SET memory_limit = '{memory_limit}'")
    con.execute("SET preserve_insertion_order = false")
    return con
