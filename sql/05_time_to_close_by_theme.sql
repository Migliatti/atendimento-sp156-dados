-- Days from opening to closing, by theme: average, median and 90th percentile.
-- Only closed requests with a closing date. SQLite has no MEDIAN, so each
-- request gets its position (rn) inside its theme and we pick the middle one.
-- Themes with fewer than 500 such requests are left out (too few to compare).
WITH closed AS (
    SELECT theme, days_to_close
    FROM requests
    WHERE status = 'closed' AND days_to_close IS NOT NULL
),
ranked AS (
    SELECT theme, days_to_close,
           ROW_NUMBER() OVER (PARTITION BY theme ORDER BY days_to_close) AS rn,
           COUNT(*)     OVER (PARTITION BY theme)                        AS n
    FROM closed
)
SELECT theme,
       MAX(n)                                                                  AS closed_requests,
       ROUND(AVG(days_to_close), 1)                                            AS avg_days,
       AVG(CASE WHEN rn IN ((n + 1) / 2, (n + 2) / 2) THEN days_to_close END)  AS median_days,
       MIN(CASE WHEN rn >= 0.9 * n THEN days_to_close END)                     AS p90_days
FROM ranked
GROUP BY theme
HAVING MAX(n) >= 500
ORDER BY median_days DESC, avg_days DESC;
