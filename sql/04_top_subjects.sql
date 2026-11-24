-- The 15 most frequent subjects (more specific than the theme).
SELECT subject,
       theme,
       COUNT(*) AS requests,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM requests), 1) AS share_pct
FROM requests
GROUP BY subject, theme
ORDER BY requests DESC
LIMIT 15;
