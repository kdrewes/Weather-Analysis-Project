
-- Query 1: Find the highest temperature per city
SELECT DISTINCT ON (c.city_id)
    c.name AS city,
    w.record_date,
    w.temp_max_c AS hottest_max_temp_c
FROM weather w
JOIN cities c ON c.city_id = w.city_id
ORDER BY c.city_id, w.temp_max_c DESC, w.record_date;


-- Determine average rainfall per city each day using order by 
SELECT
    c.name AS city,
    ROUND(AVG(w.rain_mm), 2) AS average_rain,
    ROUND(SUM(w.rain_mm), 2) AS total_rain
FROM weather w
JOIN cities c ON c.city_id = w.city_id
GROUP BY c.name
ORDER BY average_rain DESC;


-- Query 3: Total monthly precipitation by city
SELECT
    c.name AS city,
    DATE_TRUNC('month', w.record_date)::DATE AS month,
    ROUND(SUM(w.rain_mm), 2) AS total_rain,
    COUNT(*) AS days_in_month
FROM weather w
JOIN cities c ON c.city_id = w.city_id
GROUP BY c.name, DATE_TRUNC('month', w.record_date)
ORDER BY c.name, month;


-- Query 4: Windiest week of the year per city
SELECT
    c.name AS city,
    DATE_TRUNC('week', w.record_date)::DATE AS week_start,
    ROUND(MAX(w.wind_speed_max_kmh), 2) AS peak_wind_kmh
FROM weather w
JOIN cities c ON c.city_id = w.city_id
GROUP BY c.name, DATE_TRUNC('week', w.record_date)
ORDER BY peak_wind_kmh DESC
LIMIT 5;

-- Query 5: Determine frequency of extreme heat days (max temp >= 86°C)
SELECT
    c.name AS city,
    COUNT(*) FILTER (WHERE w.temp_max_c >= 40) AS hot_days,
    COUNT(*) AS total_days,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE w.temp_max_c >= 40) / COUNT(*),
        1
    ) AS pct_hot_days
FROM weather w
JOIN cities c ON c.city_id = w.city_id
GROUP BY c.name
ORDER BY hot_days DESC;
