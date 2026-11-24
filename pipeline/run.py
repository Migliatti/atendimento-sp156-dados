"""Run the whole pipeline: download -> clean -> load -> SQL -> charts -> report.

    python -m pipeline.run            full data (downloads about 105 MB once)
    python -m pipeline.run --sample   the 20,000-row sample in the repository
"""
import argparse
import json


from . import charts, report
from .clean import clean, read_raw
from .config import RAW_FILE, ROOT, SAMPLE_FILE
from .download import download
from .load import load
from .queries import run_queries


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", action="store_true",
                    help="use data/sample instead of downloading; writes to outputs_sample/")
    args = ap.parse_args()

    if args.sample:
        source, db, out = SAMPLE_FILE, ROOT / "data" / "sample.sqlite", ROOT / "outputs_sample"
    else:
        source, db, out = download(), ROOT / "data" / "sp156.sqlite", ROOT / "reports"

    raw = read_raw(source)
    df, stats = clean(raw)
    print("[clean]", json.dumps(stats))

    con = load(df, db)
    print(f"[load] {db.name}: {len(df)} rows")

    results = run_queries(con, out / "tables")
    con.close()
    charts.make_charts(results, out)
    report.write_report(results, stats, out / "relatorio.md", sample=args.sample)
    print(f"[done] outputs in {out}")


if __name__ == "__main__":
    main()
