-- 2.1: Top 5 best performing stocks (year-to-date return)
WITH yearly_prices AS (
    SELECT ticker,
           MIN(date) AS first_date,
           MAX(date) AS last_date
    FROM daily_prices
    GROUP BY ticker
),
first_last AS (
    SELECT p.ticker,
           MAX(CASE WHEN p.date = y.first_date THEN p.close END) AS first_close,
           MAX(CASE WHEN p.date = y.last_date THEN p.close END) AS last_close
    FROM daily_prices p
    JOIN yearly_prices y ON p.ticker = y.ticker
    GROUP BY p.ticker
)
SELECT ticker,
       ROUND(first_close, 2) AS opening_price,
       ROUND(last_close, 2) AS closing_price,
       ROUND(((last_close - first_close) / first_close) * 100, 2) AS return_pct
FROM first_last
ORDER BY return_pct DESC
LIMIT 5;

-- 2.2: Stocks with highest average daily volume
SELECT s.ticker, s.company_name,
       ROUND(AVG(p.volume)) AS avg_volume,
       ROUND(AVG(p.close), 2) AS avg_price
FROM stocks s
JOIN daily_prices p ON s.ticker = p.ticker
GROUP BY s.ticker
ORDER BY avg_volume DESC;

-- 2.3: Most volatile stocks (standard deviation of daily returns)
WITH daily_returns AS (
    SELECT ticker,
           (close - LAG(close) OVER (PARTITION BY ticker ORDER BY date))
           / LAG(close) OVER (PARTITION BY ticker ORDER BY date) * 100 AS daily_return_pct
    FROM daily_prices
),
stats AS (
    SELECT ticker,
           AVG(daily_return_pct) AS avg_daily_return_pct,
           (SUM(daily_return_pct * daily_return_pct)
            - SUM(daily_return_pct) * SUM(daily_return_pct) / COUNT(*))
           / (COUNT(*) - 1) AS return_variance
    FROM daily_returns
    WHERE daily_return_pct IS NOT NULL
    GROUP BY ticker
)
SELECT ticker,
       ROUND(avg_daily_return_pct, 4) AS avg_daily_return_pct,
       ROUND(SQRT(return_variance), 4) AS stddev_daily_return_pct
FROM stats
ORDER BY stddev_daily_return_pct DESC;
