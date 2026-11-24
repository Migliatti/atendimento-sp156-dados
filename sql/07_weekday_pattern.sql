-- Average requests per day of the week. Each day is counted first, then the
-- days are averaged by weekday, so weekdays with more dates in the quarter
-- do not look bigger just because they appear more often.
WITH per_day AS (
    SELECT opened_date, strftime('%w', opened_date) AS weekday_num, COUNT(*) AS requests
    FROM requests
    GROUP BY opened_date
)
SELECT CASE weekday_num WHEN '0' THEN 'Sun' WHEN '1' THEN 'Mon' WHEN '2' THEN 'Tue'
                        WHEN '3' THEN 'Wed' WHEN '4' THEN 'Thu' WHEN '5' THEN 'Fri'
                        ELSE 'Sat' END AS weekday,
       weekday_num,
       COUNT(*)                       AS days_in_period,
       ROUND(AVG(requests))           AS avg_requests_per_day
FROM per_day
GROUP BY weekday_num
ORDER BY (CAST(weekday_num AS INTEGER) + 6) % 7;   -- Monday first
