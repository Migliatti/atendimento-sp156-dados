-- Requests opened per calendar day (used for the daily line chart).
SELECT opened_date AS day,
       strftime('%w', opened_date) AS weekday_num,   -- 0 = Sunday ... 6 = Saturday
       COUNT(*) AS requests
FROM requests
GROUP BY opened_date
ORDER BY opened_date;
