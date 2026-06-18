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
    SELECT ticker, date, close,
           LAG(close) OVER (PARTITION BY ticker ORDER BY date) AS prev_close
    FROM daily_prices
)
SELECT ticker,
       ROUND(AVG((close - prev_close) / prev_close * 100), 4) AS avg_daily_return_pct,
       ROUND((SUM((close - prev_close) / prev_close * 100 * (close - prev_close) / prev_close * 100) -
              SUM((close - prev_close) / prev_close * 100) * SUM((close - prev_close) / prev_close * 100) / COUNT(*)) / (COUNT(*) - 1), 4) AS variance
FROM daily_returns
WHERE prev_close IS NOT NULL
GROUP BY ticker
ORDER BY variance DESC;
