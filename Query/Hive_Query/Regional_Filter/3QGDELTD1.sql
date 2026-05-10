SELECT 
    Actor1Code,
    SQLDATE,
    COUNT(*) as daily_event_count,
    ROUND(MAX(GoldsteinScale) - MIN(GoldsteinScale), 2) as impact_range,
    ROUND(STDDEV_POP(GoldsteinScale), 2) as daily_volatility,
    ROUND(AVG(GoldsteinScale), 2) as avg_daily_impact

FROM <Table_Name>
WHERE pmod(hash(Actor1Code), 128) < 64
AND Actor1Code IS NOT NULL 
AND SQLDATE IS NOT NULL
AND GoldsteinScale IS NOT NULL

GROUP BY Actor1Code, SQLDATE
HAVING daily_event_count > 50

ORDER BY daily_volatility DESC
LIMIT 10; 