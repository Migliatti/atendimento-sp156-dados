"""Paths and the source of the data, in one place."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Official page of the dataset (license: Creative Commons CCZero / CC0).
DATASET_PAGE = "https://dados.prefeitura.sp.gov.br/dataset/dados-do-sp156"
# SP156 requests opened in the 3rd quarter of 2026 (July to September), about 105 MB.
DOWNLOAD_URL = (
    "https://dados.prefeitura.sp.gov.br/dataset/0aecfa2b-aa3a-40d4-8183-0d4351b7fd0a/"
    "resource/f67fcc12-8da4-485f-92a3-d2af40cc771e/download/arquivo-final-3-trim-26.csv"
)

RAW_FILE = ROOT / "data" / "raw" / "sp156_2026_q3.csv"
SAMPLE_FILE = ROOT / "data" / "sample" / "sp156_sample.csv"
SQL_DIR = ROOT / "sql"

# Columns of the original file that are kept. Street, number, ZIP code and
# coordinates are never read: they point to where a citizen lives.
KEEP_COLUMNS = [
    "Data de Abertura", "Data de Finalização", "Meio de Comunicação", "Tema",
    "Assunto", "Serviço", "Status", "Órgão", "Prefeitura Operacional", "Distrito",
]

# The status is a snapshot taken when the file was generated, not on the last
# day of the quarter. Ages of open requests are measured up to this date.
REFERENCE_DATE = "2026-09-30"
