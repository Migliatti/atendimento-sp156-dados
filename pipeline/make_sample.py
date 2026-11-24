"""Build the small sample kept in the repository (run only by the author).

Takes a fixed random 20,000 rows of the raw file, keeps only the allowed
columns (no street, number, ZIP code or coordinates) and writes a CSV in the
original format, so the same cleaning code reads it.
"""
import pandas as pd

from .clean import read_raw
from .config import RAW_FILE, SAMPLE_FILE

SAMPLE_SIZE = 20000


def main():
    raw = read_raw(RAW_FILE)
    sample = raw.sample(n=SAMPLE_SIZE, random_state=42).sort_values("Data de Abertura")
    SAMPLE_FILE.parent.mkdir(parents=True, exist_ok=True)
    sample.to_csv(SAMPLE_FILE, index=False)
    print(f"{SAMPLE_FILE}: {SAMPLE_FILE.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
