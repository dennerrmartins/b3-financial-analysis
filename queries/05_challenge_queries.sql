-- =============================================================================
-- MÓDULO 05 — Queries Desafio
-- Objetivo: combinar CTEs, window functions e lógica condicional avançada
-- Fonte: daily_prices (dados reais)
-- =============================================================================

-- 5.1: Qual foi o melhor e o pior dia de cada ticker?
-- ROW_NUMBER() OVER: rankeia dias por variação intraday (open → close)
WITH ranked_days AS (
    SELECT ticker, date,
           ROUND((close - open) / open * 100, 2) AS daily_change_pct,
           ROW_NUMBER() OVER (PARTITION BY ticker ORDER BY (close - open) / open DESC) AS best_rank,
           ROW_NUMBER() OVER (PARTITION BY ticker ORDER BY (close - open) / open ASC) AS worst_rank
    FROM daily_prices
)
SELECT ticker,
       MAX(CASE WHEN best_rank = 1 THEN date END) AS best_day,
       MAX(CASE WHEN best_rank = 1 THEN daily_change_pct END) AS best_change_pct,
       MAX(CASE WHEN worst_rank = 1 THEN date END) AS worst_day,
       MAX(CASE WHEN worst_rank = 1 THEN daily_change_pct END) AS worst_change_pct
FROM ranked_days
GROUP BY ticker;

-- 5.2: Quais tickers mais valorizaram na última semana disponível na base?
WITH week_ago AS (
    SELECT ticker, close
    FROM daily_prices
    WHERE date = (SELECT MIN(date) FROM daily_prices WHERE date >= DATE('now', '-7 days'))
),
today AS (
    SELECT ticker, close
    FROM daily_prices
    WHERE date = (SELECT MAX(date) FROM daily_prices)
)
SELECT t.ticker,
       ROUND(w.close, 2) AS price_week_ago,
       ROUND(t.close, 2) AS current_price,
       ROUND((t.close - w.close) / w.close * 100, 2) AS week_change_pct
FROM today t
JOIN week_ago w ON t.ticker = w.ticker
ORDER BY week_change_pct DESC;

-- 5.3: Quais pares de tickers movem-se na mesma direção com mais frequência?
-- Proxy simplificado de correlação (não é Pearson) — mesma direção intraday
SELECT a.ticker AS stock_a,
       b.ticker AS stock_b,
       ROUND(SUM(CASE WHEN (a.close - a.open) * (b.close - b.open) > 0 THEN 1 ELSE 0 END) * 1.0 / COUNT(*), 4) AS same_direction_pct
FROM daily_prices a
JOIN daily_prices b ON a.date = b.date AND a.ticker < b.ticker
GROUP BY stock_a, stock_b
HAVING COUNT(*) > 100
ORDER BY same_direction_pct DESC;

-- 5.4: Quais tickers têm maior consistência de alta mês a mês?
-- CTE growth_check: compara média mensal com o mês anterior via LAG
WITH monthly_avg AS (
    SELECT ticker,
           STRFTIME('%Y-%m', date) AS month,
           AVG(close) AS avg_close
    FROM daily_prices
    GROUP BY ticker, month
),
growth_check AS (
    SELECT ticker, month, avg_close,
           LAG(avg_close) OVER (PARTITION BY ticker ORDER BY month) AS prev_month_close
    FROM monthly_avg
)
SELECT ticker,
       COUNT(*) AS months_analysed,
       SUM(CASE WHEN avg_close > prev_month_close THEN 1 ELSE 0 END) AS months_grew,
       ROUND(SUM(CASE WHEN avg_close > prev_month_close THEN 1 ELSE 0 END) * 1.0 / COUNT(*) * 100, 1) AS growth_consistency_pct
FROM growth_check
WHERE prev_month_close IS NOT NULL
GROUP BY ticker
ORDER BY growth_consistency_pct DESC;
