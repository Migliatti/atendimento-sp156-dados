"""Step 4: run every file in sql/ and save each result as a CSV table."""
import sqlite3
from pathlib import Path

import pandas as pd

from .config import SQL_DIR


def run_queries(con: sqlite3.Connection, tables_dir: Path) -> dict:
    """Return {query_name: DataFrame}. Names come from the file names."""
    tables_dir.mkdir(parents=True, exist_ok=True)
    results = {}
    for path in sorted(SQL_DIR.glob("[0-9][0-9]_*.sql")):
        df = pd.read_sql_query(path.read_text(encoding="utf-8"), con)
        df.to_csv(tables_dir / f"{path.stem}.csv", index=False)
        results[path.stem] = df
        print(f"[sql] {path.name}: {len(df)} rows")
    return results
