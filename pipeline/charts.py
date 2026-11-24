"""Step 5: one PNG per question, drawn from the query results."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # draw to files, no window
import matplotlib.pyplot as plt

COLOR = "#2b6cb0"


def _save(fig, path: Path):
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)
    print(f"[chart] {path.name}")


def _short(text, n=42):
    text = str(text)
    return text if len(text) <= n else text[: n - 1] + "…"


def _hbar(df, label, value, title, xlabel, path, top=10):
    d = df.head(top).iloc[::-1]
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh([_short(x) for x in d[label]], d[value], color=COLOR)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    _save(fig, path)


def make_charts(results: dict, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)

    d = results["02_volume_by_day"].copy()
    d["day"] = d["day"].astype("datetime64[ns]")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(d["day"], d["requests"], color=COLOR, linewidth=1.2)
    ax.set_title("Requests opened per day (SP156, Jul-Sep 2026)")
    ax.set_ylabel("requests")
    ax.set_ylim(bottom=0)
    fig.autofmt_xdate()
    _save(fig, out_dir / "01_requests_per_day.png")

    _hbar(results["03_volume_by_theme"], "theme", "requests",
          "Top 10 themes by number of requests", "requests", out_dir / "02_top_themes.png")

    d = results["04_top_subjects"]
    _hbar(d, "subject", "requests", "Top 10 subjects by number of requests",
          "requests", out_dir / "03_top_subjects.png")

    d = results["05_time_to_close_by_theme"].head(10)
    _hbar(d, "theme", "median_days", "Slowest themes: median days to close",
          "median days (closed requests only)", out_dir / "04_time_to_close.png")

    d = results["06_backlog_by_theme"].sort_values("backlog", ascending=False)
    _hbar(d, "theme", "backlog", "Requests still open or in progress, by theme",
          "requests", out_dir / "05_backlog.png")

    d = results["07_weekday_pattern"]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(d["weekday"], d["avg_requests_per_day"], color=COLOR)
    ax.set_title("Average requests opened per day of the week")
    ax.set_ylabel("requests per day")
    _save(fig, out_dir / "06_weekday.png")
