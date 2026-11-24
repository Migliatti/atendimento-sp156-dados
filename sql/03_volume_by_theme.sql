-- Which themes receive the most requests, and their share of the total.
SELECT theme,
       COUNT(*) AS requests,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM requests), 1) AS share_pct
FROM requests
GROUP BY theme
ORDER BY requests DESC
LIMIT 15;
