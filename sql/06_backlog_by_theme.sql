-- Backlog: requests still "open" or "in_progress" in the file, by theme.
-- Age is counted from the opening date to the end of the quarter (2026-09-30).
SELECT theme,
       COUNT(*)                                                         AS requests,
       SUM(status IN ('open', 'in_progress'))                           AS backlog,
       ROUND(100.0 * SUM(status IN ('open', 'in_progress')) / COUNT(*), 1) AS backlog_pct,
       ROUND(AVG(CASE WHEN status IN ('open', 'in_progress')
                      THEN julianday('2026-09-30') - julianday(opened_date) END), 1) AS avg_backlog_age_days
FROM requests
GROUP BY theme
HAVING COUNT(*) >= 1000
ORDER BY backlog DESC
LIMIT 12;
