-- =============================================================================
-- MÓDULO 04 — Window Functions
-- Objetivo: análises temporais — médias móveis, retorno diário, ranking e acumulado
-- Fonte: daily_prices (dados reais)
-- =============================================================================

-- 4.1: Qual a média móvel de 20 dias para PETR4?
-- AVG() OVER com frame ROWS: janela deslizante de 20 pregões
SELECT date, close,
       ROUND(AVG(close) OVER (ORDER BY date ROWS BETWEEN 19 PRECEDING AND CURRENT ROW), 2) AS ma_20
FROM daily_prices
WHERE ticker = 'PETR4'
ORDER BY date;

-- 4.2: Qual o retorno diário usando LAG (preço anterior)?
-- LAG() OVER PARTITION BY ticker: compara cada dia com o pregão anterior
SELECT ticker, date, close,
       LAG(close) OVER (PARTITION BY ticker ORDER BY date) AS prev_close,
       ROUND((close - LAG(close) OVER (PARTITION BY ticker ORDER BY date))
             / LAG(close) OVER (PARTITION BY ticker ORDER BY date) * 100, 2) AS daily_return_pct
FROM daily_prices
WHERE ticker IN ('PETR4', 'VALE3', 'ITUB4')
ORDER BY ticker, date;

-- 4.3: Como ranquear tickers por preço médio dentro de cada setor?
-- RANK() OVER PARTITION BY sector: ranking relativo por setor na amostra
SELECT s.sector, s.ticker,
       ROUND(AVG(p.close), 2) AS avg_price,
       RANK() OVER (PARTITION BY s.sector ORDER BY AVG(p.close) DESC) AS rank_in_sector
FROM stocks s
JOIN daily_prices p ON s.ticker = p.ticker
GROUP BY s.sector, s.ticker
ORDER BY s.sector, rank_in_sector;

-- 4.4: Qual o retorno acumulado de PETR4 desde o primeiro pregão?
-- FIRST_VALUE() OVER: define preço base para cálculo de retorno acumulado
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
