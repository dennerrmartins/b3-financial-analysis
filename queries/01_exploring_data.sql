-- 1.1: View all stocks in the database
SELECT * FROM stocks;

-- 1.2: Group stocks by sector
SELECT sector, COUNT(*) AS total_stocks
FROM stocks
GROUP BY sector
ORDER BY total_stocks DESC;

-- 1.3: Latest price for each stock
SELECT ticker, date, close
FROM daily_prices
WHERE date = (SELECT MAX(date) FROM daily_prices);

-- 1.4: Average closing price per stock (last 30 days)
SELECT ticker, ROUND(AVG(close), 2) AS avg_price_30d
FROM daily_prices
WHERE date >= DATE('now', '-30 days')
GROUP BY ticker
ORDER BY avg_price_30d DESC;

-- 1.5: Highest volume day per stock
SELECT ticker, date, volume
FROM daily_prices
WHERE (ticker, volume) IN (
    SELECT ticker, MAX(volume)
    FROM daily_prices
    GROUP BY ticker
)
ORDER BY volume DESC;
