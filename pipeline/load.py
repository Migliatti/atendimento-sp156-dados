"""Step 3: load the clean table into SQLite (standard library `sqlite3`)."""
import sqlite3
from pathlib import Path

from .config import SQL_DIR

COLUMNS = ["opened_date", "closed_date", "channel", "theme", "subject", "service",
           "status", "organ", "subprefecture", "district", "days_to_close"]


def load(df, db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()
    out = df[COLUMNS].copy()
    for col in ("opened_date", "closed_date"):
        out[col] = out[col].dt.strftime("%Y-%m-%d")
    out["days_to_close"] = out["days_to_close"].astype(object)
    out = out.astype(object).where(out.notna(), None)  # missing values become NULL

    con = sqlite3.connect(db_path)
    con.executescript((SQL_DIR / "schema.sql").read_text(encoding="utf-8"))
    marks = ",".join("?" * len(COLUMNS))
    con.executemany(
        f"INSERT INTO requests ({','.join(COLUMNS)}) VALUES ({marks})",
        out.itertuples(index=False, name=None),
    )
    con.commit()
    return con
