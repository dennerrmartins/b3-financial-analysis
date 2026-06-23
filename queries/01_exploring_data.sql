-- =============================================================================
-- MÓDULO 01 — Exploração de Dados
-- Objetivo: validar a base, entender a amostra e obter leituras iniciais
-- Fonte: daily_prices (Yahoo Finance) + stocks
-- =============================================================================

-- 1.1: Quais tickers compõem a amostra?
SELECT * FROM stocks;

-- 1.2: Como os tickers se distribuem por setor na amostra?
SELECT sector, COUNT(*) AS total_stocks
FROM stocks
GROUP BY sector
ORDER BY total_stocks DESC;

-- 1.3: Qual o último preço de fechamento de cada ticker?
SELECT ticker, date, close
FROM daily_prices
WHERE date = (SELECT MAX(date) FROM daily_prices);

-- 1.4: Qual o preço médio de fechamento nos últimos 30 dias?
SELECT ticker, ROUND(AVG(close), 2) AS avg_price_30d
FROM daily_prices
WHERE date >= DATE('now', '-30 days')
GROUP BY ticker
ORDER BY avg_price_30d DESC;

-- 1.5: Qual foi o dia de maior volume negociado por ticker?
SELECT ticker, date, volume
FROM daily_prices
WHERE (ticker, volume) IN (
    SELECT ticker, MAX(volume)
    FROM daily_prices
    GROUP BY ticker
)
ORDER BY volume DESC;
