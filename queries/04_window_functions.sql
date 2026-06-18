-- 4.1: 20-day moving average for Petrobras
SELECT date, close,
       ROUND(AVG(close) OVER (ORDER BY date ROWS BETWEEN 19 PRECEDING AND CURRENT ROW), 2) AS ma_20
FROM daily_prices
WHERE ticker = 'PETR4'
ORDER BY date;

-- 4.2: Daily return with LAG
SELECT ticker, date, close,
       LAG(close) OVER (PARTITION BY ticker ORDER BY date) AS prev_close,
       ROUND((close - LAG(close) OVER (PARTITION BY ticker ORDER BY date)) / LAG(close) OVER (PARTITION BY ticker ORDER BY date) * 100, 2) AS daily_return_pct
FROM daily_prices
WHERE ticker IN ('PETR4', 'VALE3', 'ITUB4')
ORDER BY ticker, date;

-- 4.3: Rank stocks by average price per sector
SELECT s.sector, s.ticker,
       ROUND(AVG(p.close), 2) AS avg_price,
       RANK() OVER (PARTITION BY s.sector ORDER BY AVG(p.close) DESC) AS rank_in_sector
FROM stocks s
JOIN daily_prices p ON s.ticker = p.ticker
GROUP BY s.sector, s.ticker
ORDER BY s.sector, rank_in_sector;

-- 4.4: Cumulative return since first date
WITH base_prices AS (
    SELECT ticker, date, close,
           FIRST_VALUE(close) OVER (PARTITION BY ticker ORDER BY date) AS base_price
    FROM daily_prices
)
SELECT ticker, date,
       ROUND((close - base_price) / base_price * 100, 2) AS cumulative_return_pct
FROM base_prices
WHERE ticker = 'PETR4'
ORDER BY date;
