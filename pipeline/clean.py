"""Step 2: clean the raw table.

`clean(df)` takes the raw columns (Portuguese names, all text) and returns a
tidy table plus a small dict that counts what was changed or dropped.
"""
import pandas as pd

from .config import KEEP_COLUMNS

RENAME = {
    "Data de Abertura": "opened_date",
    "Data de Finalização": "closed_date",
    "Meio de Comunicação": "channel",
    "Tema": "theme",
    "Assunto": "subject",
    "Serviço": "service",
    "Status": "status",
    "Órgão": "organ",
    "Prefeitura Operacional": "subprefecture",
    "Distrito": "district",
}

STATUS_MAP = {
    "finalizada": "closed",
    "finalizado": "closed",
    "aberto": "open",
    "aberta": "open",
    "em andamento": "in_progress",
    "cancelada": "cancelled",
    "indeferido": "rejected",
}


def read_raw(path) -> pd.DataFrame:
    """Read only the allowed columns, as text (no guessing of types)."""
    return pd.read_csv(path, dtype=str, keep_default_na=False,
                       usecols=lambda c: c in KEEP_COLUMNS, encoding="utf-8-sig")


def clean(raw: pd.DataFrame):
    stats = {"rows_in": len(raw)}
    df = raw.rename(columns=RENAME).copy()

    # Extra spaces and empty strings become missing values.
    for col in df.columns:
        df[col] = df[col].astype(str).str.strip().str.replace(r"\s+", " ", regex=True)
        df[col] = df[col].replace("", pd.NA)

    # Dates come as MM/DD/YYYY (for example 07/25/2026). Wrong values become NaT.
    for col in ("opened_date", "closed_date"):
        df[col] = pd.to_datetime(df[col], format="%m/%d/%Y", errors="coerce")

    # Rows without an opening date cannot be placed in time.
    before = len(df)
    df = df[df["opened_date"].notna()]
    stats["dropped_no_opened_date"] = before - len(df)

    # Test records created by the city's own teams (theme or subject says "teste").
    is_test = (df["theme"].fillna("").str.contains("teste", case=False)
               | df["subject"].fillna("").str.contains("teste", case=False))
    stats["dropped_test_records"] = int(is_test.sum())
    df = df[~is_test]

    # Same status with one spelling, lower case.
    status_key = df["status"].fillna("").str.lower()
    df["status"] = status_key.map(STATUS_MAP).fillna("other")
    df["channel"] = df["channel"].str.upper()

    # A closing date only makes sense for closed requests, and not before the opening.
    no_close_date = (df["status"] == "closed") & df["closed_date"].isna()
    stats["closed_without_date"] = int(no_close_date.sum())
    bad_order = df["closed_date"].notna() & (df["closed_date"] < df["opened_date"])
    stats["closing_before_opening"] = int(bad_order.sum())
    df.loc[bad_order, "closed_date"] = pd.NaT

    days = (df["closed_date"] - df["opened_date"]).dt.days
    df["days_to_close"] = days.where(df["status"] == "closed").astype("Int64")

    df = df.reset_index(drop=True)
    stats["rows_out"] = len(df)
    return df, stats
