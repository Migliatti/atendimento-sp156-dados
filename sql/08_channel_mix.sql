-- Channels: volume, share, how many are closed and median days to close.
WITH closed AS (
    SELECT channel, days_to_close,
           ROW_NUMBER() OVER (PARTITION BY channel ORDER BY days_to_close) AS rn,
           COUNT(*)     OVER (PARTITION BY channel)                        AS n
    FROM requests
    WHERE status = 'closed' AND days_to_close IS NOT NULL
),
medians AS (
    SELECT channel,
           AVG(CASE WHEN rn IN ((n + 1) / 2, (n + 2) / 2) THEN days_to_close END) AS median_days
    FROM closed
    GROUP BY channel
)
SELECT r.channel,
       COUNT(*)                                                  AS requests,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM requests), 1) AS share_pct,
       ROUND(100.0 * SUM(r.status = 'closed') / COUNT(*), 1)    AS closed_pct,
       m.median_days
FROM requests r
LEFT JOIN medians m ON m.channel = r.channel
GROUP BY r.channel
ORDER BY requests DESC;
