"""Step 6: write reports/relatorio.md.

The text is fixed, but every number is read from the query results (the CSV
tables in reports/tables), so the report cannot drift from the SQL.
"""
from pathlib import Path


FULL = {"Mon": "Monday", "Tue": "Tuesday", "Wed": "Wednesday", "Thu": "Thursday", "Fri": "Friday"}


def n(x):
    return f"{int(round(x)):,}"


def write_report(results, stats, path: Path, sample=False):
    month = results["01_volume_by_month"]
    day = results["02_volume_by_day"]
    theme = results["03_volume_by_theme"]
    subj = results["04_top_subjects"]
    ttc = results["05_time_to_close_by_theme"]
    backlog = results["06_backlog_by_theme"]
    wk = results["07_weekday_pattern"].set_index("weekday")
    chan = results["08_channel_mix"]

    total = int(month["requests"].sum())
    top4 = theme.head(4)
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    wd_min, wd_max = wk.loc[weekdays, "avg_requests_per_day"].agg(["min", "max"])
    lowest_wd = wk.loc[weekdays, "avg_requests_per_day"].idxmin()
    weekend = wk.loc[["Sat", "Sun"], "avg_requests_per_day"].mean()
    weekday_all = wk.loc[weekdays, "avg_requests_per_day"].mean()
    wd_rows = day[day["weekday_num"].astype(int).between(1, 5)]
    low = wd_rows.loc[wd_rows["requests"].idxmin()]
    holiday = (" (September 7 is Independence Day, a national holiday in Brazil; "
               "that explanation is mine, the data only shows the drop)"
               if low["day"] == "2026-09-07" else "")

    top_subject = subj.iloc[0]
    fast = ttc.sort_values(["median_days", "avg_days"]).iloc[0]
    slow = ttc.iloc[0]
    big_cut = ttc["closed_requests"].median()
    slow_big = ttc[ttc["closed_requests"] >= big_cut].iloc[0]
    big_backlog = backlog.iloc[0]
    worst_pct = backlog.sort_values("backlog_pct", ascending=False).iloc[0]
    first, last = month.iloc[0], month.iloc[-1]

    banner = ""
    if sample:
        banner = ("> **SAMPLE RUN.** These numbers come from the 20,000-row sample in `data/sample/`, "
                  "so counts are about 4% of the real ones. The report committed in `reports/` is "
                  "the one made from the full file.\n\n")

    text = f"""# SP156 requests, July to September 2026: what the data says

{banner}Source: SP156 open data (São Paulo city hall), requests opened in the 3rd quarter of 2026.
After cleaning, {n(stats['rows_out'])} requests ({n(stats['dropped_test_records'])} test records removed).
Every number below comes from a query in `sql/`; the result of each query is saved in `reports/tables/`.
Read the "Limits" section before quoting any of these numbers.

## 1. About {int(round(month['requests'].mean()/1000))} thousand requests arrive every month, and the share closed drops for the newest month

- Total in the quarter: {n(total)}. Per month: {", ".join(f"{r.month} = {n(r.requests)}" for r in month.itertuples())}.
- The closed share goes from {first.closed_pct}% ({first.month}) to {last.closed_pct}% ({last.month}).
  A likely reason is timing: newer requests have had less time to be closed (my reading;
  the data alone cannot prove it). It should not be read as the service getting worse.
- Query: `sql/01_volume_by_month.sql`. Chart: `reports/01_requests_per_day.png`.

![requests per day](01_requests_per_day.png)

## 2. Requests follow the work week

- Monday to Friday average {n(wd_min)} to {n(wd_max)} requests per day; Saturday and Sunday average {n(weekend)}
  (about {weekend / weekday_all * 100:.0f}% of a weekday).
- {FULL[lowest_wd]} is the lowest weekday on average ({n(wk.loc[lowest_wd, 'avg_requests_per_day'])} per day).
- The lowest weekday of the quarter was {low['day']} with {n(low['requests'])} requests{holiday}.
- Queries: `sql/07_weekday_pattern.sql` and `sql/02_volume_by_day.sql`. Charts: `reports/06_weekday.png`, `reports/01_requests_per_day.png`.

![weekday](06_weekday.png)

![requests per day](01_requests_per_day.png)
- The file only has dates, with no time of day, so a pattern by hour cannot be checked.

## 3. A few themes account for most of the volume

- The 4 biggest themes ({", ".join(top4['theme'])}) hold {top4['share_pct'].sum():.1f}% of all requests.
- The single most frequent subject is "{top_subject['subject']}" with {n(top_subject['requests'])} requests
  ({top_subject['share_pct']}% of the total), under the theme "{top_subject['theme']}".
- Queries: `sql/03_volume_by_theme.sql` and `sql/04_top_subjects.sql`. Charts: `reports/02_top_themes.png`, `reports/03_top_subjects.png`.

![top themes](02_top_themes.png)

![top subjects](03_top_subjects.png)

## 4. Time to close varies a lot by theme

- Among closed requests, the median is {fast['median_days']:.0f} day(s) for "{fast['theme']}" and
  {slow['median_days']:.0f} days for "{slow['theme']}" (only {n(slow['closed_requests'])} closed requests, so treat with care).
- Among the larger half of themes (at least {n(big_cut)} closed requests), the slowest median is "{slow_big['theme']}":
  {slow_big['median_days']:.0f} days (90% of them closed within {slow_big['p90_days']:.0f} days).
- Query: `sql/05_time_to_close_by_theme.sql`. Chart: `reports/04_time_to_close.png`.

![time to close](04_time_to_close.png)
- Median is used instead of average because a few very slow requests pull the average up.

## 5. The backlog is concentrated in a few themes

- "{big_backlog['theme']}" has the biggest backlog: {n(big_backlog['backlog'])} requests still open or in progress
  ({big_backlog['backlog_pct']}% of its requests), on average {big_backlog['avg_backlog_age_days']:.0f} days old at the end of the quarter.
- The highest backlog share is "{worst_pct['theme']}": {worst_pct['backlog_pct']}% of its {n(worst_pct['requests'])} requests.
- Query: `sql/06_backlog_by_theme.sql`. Chart: `reports/05_backlog.png`.

![backlog](05_backlog.png)

## Extra: channels

- {chan.iloc[0]['channel']} is the biggest channel ({chan.iloc[0]['share_pct']}% of requests), then
  {chan.iloc[1]['channel']} ({chan.iloc[1]['share_pct']}%) and {chan.iloc[2]['channel']} ({chan.iloc[2]['share_pct']}%).
  Query: `sql/08_channel_mix.sql`. The file does not explain the channel codes `CRM` and `INTEGRACAO`, so they are shown as they are.

## Limits

- Status is a snapshot from when the city published the file, not the state on the last day of the quarter.
  "Backlog" here means "not closed in the snapshot".
- Time to close only counts requests that are closed. Requests still open are left out, so times look shorter
  than reality, mainly for slow themes and for the newest weeks.
- {n(stats['closed_without_date'])} requests are marked closed but have no closing date. They count as closed
  in shares but not in days to close.
- One row is one request, but one citizen can open several requests for the same problem, and one problem can
  be reported by many people. The number of requests is not the number of problems in the city (the dataset glossary says the same).
- The raw file has no request id, so identical rows were kept. They may be real separate requests.
- Street, number, ZIP code and coordinates are not used by this project.
"""
    path.write_text(text, encoding="utf-8")
