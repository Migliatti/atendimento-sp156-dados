-- Requests opened per month, and how many of them are already closed.
SELECT strftime('%Y-%m', opened_date)                         AS month,
       COUNT(*)                                               AS requests,
       SUM(status = 'closed')                                 AS closed,
       ROUND(100.0 * SUM(status = 'closed') / COUNT(*), 1)    AS closed_pct
FROM requests
GROUP BY month
ORDER BY month;
