"""Tests for the cleaning step, with tiny hand-made tables (no download needed)."""
import pandas as pd
import pytest

from pipeline.clean import clean

COLS = ["Data de Abertura", "Data de Finalização", "Meio de Comunicação", "Tema",
        "Assunto", "Serviço", "Status", "Órgão", "Prefeitura Operacional", "Distrito"]


def make(*rows):
    """Each row: (opened, closed, status, theme). The other columns get fixed values."""
    return pd.DataFrame(
        [[o, c, "portal", t, "Assunto  X ", "Servico", s, "ORG", "", ""] for o, c, s, t in rows],
        columns=COLS,
    )


def test_dates_are_month_first_and_days_to_close_is_computed():
    df, _ = clean(make(("07/01/2026", "07/25/2026", "Finalizada", "Animais")))
    assert df.loc[0, "opened_date"] == pd.Timestamp("2026-07-01")
    assert df.loc[0, "days_to_close"] == 24


def test_status_is_normalised_and_unknown_becomes_other():
    df, _ = clean(make(
        ("07/01/2026", "07/02/2026", "Finalizada", "A"),
        ("07/01/2026", "", "Aberto", "A"),
        ("07/01/2026", "", "Em Andamento", "A"),
        ("07/01/2026", "07/03/2026", "Cancelada", "A"),
        ("07/01/2026", "", "Em Aprovação", "A"),
    ))
    assert list(df["status"]) == ["closed", "open", "in_progress", "cancelled", "other"]


def test_test_records_are_removed_and_counted():
    df, stats = clean(make(
        ("07/01/2026", "", "Aberto", "tema001 - teste"),
        ("07/01/2026", "", "Aberto", "Animais"),
    ))
    assert len(df) == 1 and stats["dropped_test_records"] == 1


def test_closing_before_opening_is_discarded():
    df, stats = clean(make(("07/10/2026", "07/01/2026", "Finalizada", "A")))
    assert stats["closing_before_opening"] == 1
    assert pd.isna(df.loc[0, "closed_date"]) and pd.isna(df.loc[0, "days_to_close"])


def test_open_request_has_no_days_to_close_and_empty_text_becomes_missing():
    df, _ = clean(make(("07/01/2026", "", "Aberto", "A")))
    assert pd.isna(df.loc[0, "days_to_close"])
    assert pd.isna(df.loc[0, "district"])          # was an empty string
    assert df.loc[0, "subject"] == "Assunto X"     # extra spaces collapsed


def test_row_without_valid_opening_date_is_dropped():
    df, stats = clean(make(("not a date", "", "Aberto", "A"), ("07/02/2026", "", "Aberto", "A")))
    assert len(df) == 1 and stats["dropped_no_opened_date"] == 1
