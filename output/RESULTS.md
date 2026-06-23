# B3 Financial Analysis — Relatório de Resultados

> Gerado em **23/06/2026 12:05** · amostra de 10 tickers · SQLite · preços via Yahoo Finance

> **Avisos legais e técnicos**
> - Conteúdo **educacional**. Não é recomendação de investimento.
> - A amostra **não representa** a B3 como um todo.
> - Indicadores do módulo 03 são **dados ilustrativos** para prática de SQL.

---

## Sumário executivo

- **Período analisado:** 2025-06-20 a 2026-06-18
- **Registros de preço:** 2,490 linhas · 10 tickers na amostra

**Maior retorno no período (tickers):**
- **VALE3** → 74.43%
- **PETR4** → 28.77%
- **ABEV3** → 25.39%

**Maior volatilidade (stddev retorno diário):**
- **RENT3** → 2.42%
- **ENGI3** → 2.31%
- **WEGE3** → 1.86%

> Gráficos disponíveis em [`assets/charts/`](../assets/charts/) (gerados por `generate_charts.py`).

---

## 01 — Exploração de Dados

Validação da base, distribuição da amostra e leitura inicial de preços e volume.

### Query

```sql
-- MÓDULO 01 — Exploração de Dados
-- Objetivo: validar a base, entender a amostra e obter leituras iniciais
-- Fonte: daily_prices (Yahoo Finance) + stocks
```

_Sem resultados._
### 1.1: Quais tickers compõem a amostra?

```sql
SELECT * FROM stocks;
```

| ticker | company_name | sector |
| --- | --- | --- |
| PETR4 | Petrobras | Oil & Gas |
| VALE3 | Vale | Mining |
| ITUB4 | Itaú Unibanco | Banking |
| BBDC4 | Bradesco | Banking |
| ABEV3 | Ambev | Beverages |
| WEGE3 | WEG | Industrial |
| BBAS3 | Banco do Brasil | Banking |
| ENGI3 | Energisa | Energy |
| KLBN4 | Klabin | Paper & Packaging |
| RENT3 | Localiza | Car Rental |
### 1.2: Como os tickers se distribuem por setor na amostra?

```sql
SELECT sector, COUNT(*) AS total_stocks
FROM stocks
GROUP BY sector
ORDER BY total_stocks DESC;
```

| sector | total_stocks |
| --- | --- |
| Banking | 3 |
| Paper & Packaging | 1 |
| Oil & Gas | 1 |
| Mining | 1 |
| Industrial | 1 |
| Energy | 1 |
| Car Rental | 1 |
| Beverages | 1 |
### 1.3: Qual o último preço de fechamento de cada ticker?

```sql
SELECT ticker, date, close
FROM daily_prices
WHERE date = (SELECT MAX(date) FROM daily_prices);
```

| ticker | date | close |
| --- | --- | --- |
| PETR4 | 2026-06-18 | 38.85 |
| VALE3 | 2026-06-18 | 79.94 |
| ITUB4 | 2026-06-18 | 40.13 |
| BBDC4 | 2026-06-18 | 17.47 |
| ABEV3 | 2026-06-18 | 16.22 |
| WEGE3 | 2026-06-18 | 45.81 |
| BBAS3 | 2026-06-18 | 19.53 |
| ENGI3 | 2026-06-18 | 11.70 |
| KLBN4 | 2026-06-18 | 3.44 |
| RENT3 | 2026-06-18 | 40.09 |
### 1.4: Qual o preço médio de fechamento nos últimos 30 dias?

```sql
SELECT ticker, ROUND(AVG(close), 2) AS avg_price_30d
FROM daily_prices
WHERE date >= DATE('now', '-30 days')
GROUP BY ticker
ORDER BY avg_price_30d DESC;
```

| ticker | avg_price_30d |
| --- | --- |
| VALE3 | 81.04 |
| WEGE3 | 43.18 |
| RENT3 | 41.35 |
| PETR4 | 41.00 |
| ITUB4 | 39.50 |
| BBAS3 | 19.80 |
| BBDC4 | 17.62 |
| ABEV3 | 16.37 |
| ENGI3 | 11.78 |
| KLBN4 | 3.38 |
### 1.5: Qual foi o dia de maior volume negociado por ticker?

```sql
SELECT ticker, date, volume
FROM daily_prices
WHERE (ticker, volume) IN (
    SELECT ticker, MAX(volume)
    FROM daily_prices
    GROUP BY ticker
)
ORDER BY volume DESC;
```

| ticker | date | volume |
| --- | --- | --- |
| BBAS3 | 2025-08-15 | 131820200 |
| ABEV3 | 2025-07-31 | 116074600 |
| PETR4 | 2025-08-08 | 107235300 |
| BBDC4 | 2026-02-06 | 94063600 |
| VALE3 | 2026-01-21 | 83134600 |
| ITUB4 | 2026-05-29 | 80334400 |
| RENT3 | 2025-06-26 | 33754000 |
| WEGE3 | 2025-07-23 | 31116000 |
| KLBN4 | 2026-05-06 | 16076300 |
| ENGI3 | 2025-12-19 | 41400 |
## 02 — Performance e Volatilidade

Análise de retorno, liquidez e volatilidade com dados reais de preço (Yahoo Finance).

### Query

```sql
-- MÓDULO 02 — Performance e Volatilidade
-- Objetivo: retorno, liquidez e risco relativo na amostra
-- Fonte: daily_prices (dados reais de preço via Yahoo Finance)
```

_Sem resultados._
### 2.1: Quais tickers tiveram maior retorno no período analisado?

```sql
-- CTE yearly_prices: identifica primeira e última data por ticker
-- CTE first_last: extrai preços de abertura e fechamento do período
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
```

| ticker | opening_price | closing_price | return_pct |
| --- | --- | --- | --- |
| VALE3 | 45.83 | 79.94 | 74.43 |
| PETR4 | 30.17 | 38.85 | 28.77 |
| ABEV3 | 12.94 | 16.22 | 25.39 |
| ITUB4 | 32.58 | 40.13 | 23.16 |
| WEGE3 | 39.71 | 45.81 | 15.37 |
### 2.2: Quais tickers têm maior volume médio (proxy de liquidez)?

```sql
SELECT s.ticker, s.company_name,
       ROUND(AVG(p.volume)) AS avg_volume,
       ROUND(AVG(p.close), 2) AS avg_price
FROM stocks s
JOIN daily_prices p ON s.ticker = p.ticker
GROUP BY s.ticker
ORDER BY avg_volume DESC;
```

| ticker | company_name | avg_volume | avg_price |
| --- | --- | --- | --- |
| PETR4 | Petrobras | 40602575.00 | 34.52 |
| BBDC4 | Bradesco | 31294019.00 | 17.66 |
| BBAS3 | Banco do Brasil | 29898929.00 | 21.68 |
| ABEV3 | Ambev | 29158410.00 | 13.76 |
| ITUB4 | Itaú Unibanco | 25487895.00 | 38.03 |
| VALE3 | Vale | 23010805.00 | 68.43 |
| RENT3 | Localiza | 8787068.00 | 41.70 |
| WEGE3 | WEG | 8725155.00 | 42.97 |
| KLBN4 | Klabin | 3710491.00 | 3.54 |
| ENGI3 | Energisa | 6765.00 | 12.17 |
### 2.3: Quais tickers apresentam maior volatilidade (desvio padrão do retorno diário)?

```sql
-- Window function LAG: obtém o preço do dia anterior para calcular retorno %
-- CTE stats: calcula variância amostral e extrai stddev via SQRT
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
```

| ticker | avg_daily_return_pct | stddev_daily_return_pct |
| --- | --- | --- |
| RENT3 | 0.02 | 2.42 |
| ENGI3 | 0.06 | 2.31 |
| WEGE3 | 0.07 | 1.86 |
| BBAS3 | -0.01 | 1.81 |
| ABEV3 | 0.10 | 1.64 |
| BBDC4 | 0.07 | 1.58 |
| VALE3 | 0.24 | 1.58 |
| PETR4 | 0.11 | 1.57 |
| ITUB4 | 0.09 | 1.47 |
| KLBN4 | 0.04 | 1.34 |
## 03 — Saúde Financeira (dados ilustrativos)

**Atenção:** indicadores desta seção vêm de `financial_indicators`, dados **ilustrativos** inseridos manualmente para prática de JOINs e ratios — não substituem balanços auditados.

### Query

```sql
-- MÓDULO 03 — Saúde Financeira
-- ATENÇÃO: financial_indicators contém DADOS ILUSTRATIVOS inseridos manualmente
-- Objetivo: praticar JOINs, self-joins e ratios financeiros em SQL
-- NÃO usar para decisão de investimento
```

_Sem resultados._
### 3.1: Qual a margem líquida por ticker em 2023? (dados ilustrativos)

```sql
SELECT s.ticker, s.company_name, s.sector,
       f.revenue, f.net_income,
       ROUND(f.net_income / f.revenue * 100, 2) AS profit_margin_pct
FROM stocks s
JOIN financial_indicators f ON s.ticker = f.ticker
WHERE f.year = 2023
ORDER BY profit_margin_pct DESC;
```

| ticker | company_name | sector | revenue | net_income | profit_margin_pct |
| --- | --- | --- | --- | --- | --- |
| PETR4 | Petrobras | Oil & Gas | 511.70 | 124.60 | 24.35 |
| VALE3 | Vale | Mining | 169.50 | 38.20 | 22.54 |
| BBAS3 | Banco do Brasil | Banking | 142.80 | 30.50 | 21.36 |
| ITUB4 | Itaú Unibanco | Banking | 189.70 | 34.20 | 18.03 |
| ABEV3 | Ambev | Beverages | 78.40 | 14.10 | 17.98 |
| BBDC4 | Bradesco | Banking | 157.20 | 24.50 | 15.59 |
| RENT3 | Localiza | Car Rental | 38.40 | 4.90 | 12.76 |
| KLBN4 | Klabin | Paper & Packaging | 24.80 | 3.10 | 12.50 |
| WEGE3 | WEG | Industrial | 48.50 | 5.80 | 11.96 |
| ENGI3 | Energisa | Energy | 28.40 | 3.20 | 11.27 |
### 3.2: Qual o índice dívida/EBITDA por ticker? (dados ilustrativos)

```sql
SELECT s.ticker, s.company_name,
       f.total_debt,
       f.ebitda,
       ROUND(f.total_debt / NULLIF(f.ebitda, 0), 2) AS debt_to_ebitda
FROM stocks s
JOIN financial_indicators f ON s.ticker = f.ticker
WHERE f.year = 2023
ORDER BY debt_to_ebitda;
```

| ticker | company_name | total_debt | ebitda | debt_to_ebitda |
| --- | --- | --- | --- | --- |
| VALE3 | Vale | 34.70 | 62.10 | 0.56 |
| WEGE3 | WEG | 6.40 | 8.20 | 0.78 |
| PETR4 | Petrobras | 187.30 | 184.20 | 1.02 |
| ABEV3 | Ambev | 19.20 | 18.50 | 1.04 |
| RENT3 | Localiza | 14.80 | 7.20 | 2.06 |
| BBAS3 | Banco do Brasil | 98.40 | 45.20 | 2.18 |
| KLBN4 | Klabin | 12.70 | 5.40 | 2.35 |
| ENGI3 | Energisa | 18.50 | 7.10 | 2.61 |
| ITUB4 | Itaú Unibanco | 145.30 | 52.10 | 2.79 |
| BBDC4 | Bradesco | 178.20 | 38.40 | 4.64 |
### 3.3: Qual o crescimento de receita YoY (2022 → 2023)? (dados ilustrativos)

```sql
-- Self-join: cruza o mesmo ticker em anos diferentes
SELECT a.ticker,
       a.revenue AS revenue_2022,
       b.revenue AS revenue_2023,
       ROUND((b.revenue - a.revenue) / a.revenue * 100, 2) AS revenue_growth_pct
FROM financial_indicators a
JOIN financial_indicators b ON a.ticker = b.ticker
WHERE a.year = 2022 AND b.year = 2023
ORDER BY revenue_growth_pct DESC;
```

| ticker | revenue_2022 | revenue_2023 | revenue_growth_pct |
| --- | --- | --- | --- |
| KLBN4 | 22.50 | 24.80 | 10.22 |
| WEGE3 | 44.20 | 48.50 | 9.73 |
| RENT3 | 35.10 | 38.40 | 9.40 |
| ENGI3 | 26.10 | 28.40 | 8.81 |
| BBDC4 | 149.80 | 157.20 | 4.94 |
| PETR4 | 488.20 | 511.70 | 4.81 |
| ITUB4 | 182.40 | 189.70 | 4.00 |
| ABEV3 | 75.60 | 78.40 | 3.70 |
| BBAS3 | 138.10 | 142.80 | 3.40 |
| VALE3 | 175.40 | 169.50 | -3.36 |
### 3.4: Como está o setor Banking na amostra? (dados ilustrativos)

```sql
SELECT s.ticker, s.company_name,
       f.revenue, f.net_income, f.total_debt
FROM stocks s
JOIN financial_indicators f ON s.ticker = f.ticker
WHERE s.sector = 'Banking' AND f.year = 2023;
```

| ticker | company_name | revenue | net_income | total_debt |
| --- | --- | --- | --- | --- |
| ITUB4 | Itaú Unibanco | 189.70 | 34.20 | 145.30 |
| BBDC4 | Bradesco | 157.20 | 24.50 | 178.20 |
| BBAS3 | Banco do Brasil | 142.80 | 30.50 | 98.40 |
## 04 — Window Functions

Séries temporais com médias móveis, retorno diário, ranking por setor e retorno acumulado.

### Query

```sql
-- MÓDULO 04 — Window Functions
-- Objetivo: análises temporais — médias móveis, retorno diário, ranking e acumulado
-- Fonte: daily_prices (dados reais)
```

_Sem resultados._
### 4.1: Qual a média móvel de 20 dias para PETR4?

```sql
-- AVG() OVER com frame ROWS: janela deslizante de 20 pregões
SELECT date, close,
       ROUND(AVG(close) OVER (ORDER BY date ROWS BETWEEN 19 PRECEDING AND CURRENT ROW), 2) AS ma_20
FROM daily_prices
WHERE ticker = 'PETR4'
ORDER BY date;
```

_249 linhas — exibindo as primeiras 25_

| date | close | ma_20 |
| --- | --- | --- |
| 2025-06-20 | 30.17 | 30.17 |
| 2025-06-23 | 29.42 | 29.79 |
| 2025-06-24 | 28.84 | 29.47 |
| 2025-06-25 | 28.69 | 29.28 |
| 2025-06-26 | 28.92 | 29.21 |
| 2025-06-27 | 28.69 | 29.12 |
| 2025-06-30 | 28.85 | 29.08 |
| 2025-07-01 | 28.95 | 29.06 |
| 2025-07-02 | 29.46 | 29.11 |
| 2025-07-03 | 29.56 | 29.15 |
| 2025-07-04 | 29.53 | 29.19 |
| 2025-07-07 | 29.47 | 29.21 |
| 2025-07-08 | 29.89 | 29.26 |
| 2025-07-09 | 29.71 | 29.30 |
| 2025-07-10 | 29.64 | 29.32 |
| 2025-07-11 | 29.99 | 29.36 |
| 2025-07-14 | 29.60 | 29.37 |
| 2025-07-15 | 29.37 | 29.37 |
| 2025-07-16 | 29.22 | 29.37 |
| 2025-07-17 | 28.93 | 29.34 |
| 2025-07-18 | 28.49 | 29.26 |
| 2025-07-21 | 28.54 | 29.22 |
| 2025-07-22 | 28.82 | 29.22 |
| 2025-07-23 | 29.41 | 29.25 |
| 2025-07-24 | 29.36 | 29.27 |
### 4.2: Qual o retorno diário usando LAG (preço anterior)?

```sql
-- LAG() OVER PARTITION BY ticker: compara cada dia com o pregão anterior
SELECT ticker, date, close,
       LAG(close) OVER (PARTITION BY ticker ORDER BY date) AS prev_close,
       ROUND((close - LAG(close) OVER (PARTITION BY ticker ORDER BY date))
             / LAG(close) OVER (PARTITION BY ticker ORDER BY date) * 100, 2) AS daily_return_pct
FROM daily_prices
WHERE ticker IN ('PETR4', 'VALE3', 'ITUB4')
ORDER BY ticker, date;
```

_747 linhas — exibindo as primeiras 25_

| ticker | date | close | prev_close | daily_return_pct |
| --- | --- | --- | --- | --- |
| ITUB4 | 2025-06-20 | 32.58 |  |  |
| ITUB4 | 2025-06-23 | 32.51 | 32.58 | -0.22 |
| ITUB4 | 2025-06-24 | 33.13 | 32.51 | 1.89 |
| ITUB4 | 2025-06-25 | 32.53 | 33.13 | -1.80 |
| ITUB4 | 2025-06-26 | 32.29 | 32.53 | -0.74 |
| ITUB4 | 2025-06-27 | 32.25 | 32.29 | -0.11 |
| ITUB4 | 2025-06-30 | 32.86 | 32.25 | 1.87 |
| ITUB4 | 2025-07-01 | 33.01 | 32.86 | 0.45 |
| ITUB4 | 2025-07-02 | 32.74 | 33.01 | -0.81 |
| ITUB4 | 2025-07-03 | 33.55 | 32.74 | 2.47 |
| ITUB4 | 2025-07-04 | 33.57 | 33.55 | 0.05 |
| ITUB4 | 2025-07-07 | 33.12 | 33.57 | -1.33 |
| ITUB4 | 2025-07-08 | 33.04 | 33.12 | -0.24 |
| ITUB4 | 2025-07-09 | 32.36 | 33.04 | -2.07 |
| ITUB4 | 2025-07-10 | 31.36 | 32.36 | -3.08 |
| ITUB4 | 2025-07-11 | 31.10 | 31.36 | -0.82 |
| ITUB4 | 2025-07-14 | 31.05 | 31.10 | -0.17 |
| ITUB4 | 2025-07-15 | 31.16 | 31.05 | 0.34 |
| ITUB4 | 2025-07-16 | 31.31 | 31.16 | 0.49 |
| ITUB4 | 2025-07-17 | 31.78 | 31.31 | 1.51 |
| ITUB4 | 2025-07-18 | 31.20 | 31.78 | -1.82 |
| ITUB4 | 2025-07-21 | 31.57 | 31.20 | 1.17 |
| ITUB4 | 2025-07-22 | 31.14 | 31.57 | -1.35 |
| ITUB4 | 2025-07-23 | 31.49 | 31.14 | 1.11 |
| ITUB4 | 2025-07-24 | 31.19 | 31.49 | -0.93 |
### 4.3: Como ranquear tickers por preço médio dentro de cada setor?

```sql
-- RANK() OVER PARTITION BY sector: ranking relativo por setor na amostra
SELECT s.sector, s.ticker,
       ROUND(AVG(p.close), 2) AS avg_price,
       RANK() OVER (PARTITION BY s.sector ORDER BY AVG(p.close) DESC) AS rank_in_sector
FROM stocks s
JOIN daily_prices p ON s.ticker = p.ticker
GROUP BY s.sector, s.ticker
ORDER BY s.sector, rank_in_sector;
```

| sector | ticker | avg_price | rank_in_sector |
| --- | --- | --- | --- |
| Banking | ITUB4 | 38.03 | 1 |
| Banking | BBAS3 | 21.68 | 2 |
| Banking | BBDC4 | 17.66 | 3 |
| Beverages | ABEV3 | 13.76 | 1 |
| Car Rental | RENT3 | 41.70 | 1 |
| Energy | ENGI3 | 12.17 | 1 |
| Industrial | WEGE3 | 42.97 | 1 |
| Mining | VALE3 | 68.43 | 1 |
| Oil & Gas | PETR4 | 34.52 | 1 |
| Paper & Packaging | KLBN4 | 3.54 | 1 |
### 4.4: Qual o retorno acumulado de PETR4 desde o primeiro pregão?

```sql
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
```

_249 linhas — exibindo as primeiras 25_

| ticker | date | cumulative_return_pct |
| --- | --- | --- |
| PETR4 | 2025-06-20 | 0.0000 |
| PETR4 | 2025-06-23 | -2.50 |
| PETR4 | 2025-06-24 | -4.42 |
| PETR4 | 2025-06-25 | -4.91 |
| PETR4 | 2025-06-26 | -4.14 |
| PETR4 | 2025-06-27 | -4.91 |
| PETR4 | 2025-06-30 | -4.39 |
| PETR4 | 2025-07-01 | -4.05 |
| PETR4 | 2025-07-02 | -2.35 |
| PETR4 | 2025-07-03 | -2.01 |
| PETR4 | 2025-07-04 | -2.13 |
| PETR4 | 2025-07-07 | -2.32 |
| PETR4 | 2025-07-08 | -0.91 |
| PETR4 | 2025-07-09 | -1.52 |
| PETR4 | 2025-07-10 | -1.77 |
| PETR4 | 2025-07-11 | -0.58 |
| PETR4 | 2025-07-14 | -1.89 |
| PETR4 | 2025-07-15 | -2.65 |
| PETR4 | 2025-07-16 | -3.14 |
| PETR4 | 2025-07-17 | -4.11 |
| PETR4 | 2025-07-18 | -5.58 |
| PETR4 | 2025-07-21 | -5.39 |
| PETR4 | 2025-07-22 | -4.48 |
| PETR4 | 2025-07-23 | -2.53 |
| PETR4 | 2025-07-24 | -2.68 |
## 05 — Queries Desafio

Queries avançadas: melhor/pior dia, performance semanal, correlação simplificada e consistência mensal.

### Query

```sql
-- MÓDULO 05 — Queries Desafio
-- Objetivo: combinar CTEs, window functions e lógica condicional avançada
-- Fonte: daily_prices (dados reais)
```

_Sem resultados._
### 5.1: Qual foi o melhor e o pior dia de cada ticker?

```sql
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
```

| ticker | best_day | best_change_pct | worst_day | worst_change_pct |
| --- | --- | --- | --- | --- |
| ABEV3 | 2026-05-05 | 7.01 | 2025-07-28 | -3.04 |
| BBAS3 | 2025-08-15 | 8.51 | 2025-08-01 | -7.79 |
| BBDC4 | 2026-01-05 | 4.23 | 2025-12-05 | -6.11 |
| ENGI3 | 2025-08-15 | 7.97 | 2025-10-28 | -5.85 |
| ITUB4 | 2026-01-21 | 3.48 | 2025-12-05 | -4.73 |
| KLBN4 | 2026-02-11 | 5.56 | 2026-04-07 | -3.66 |
| PETR4 | 2026-04-08 | 4.27 | 2025-06-23 | -3.88 |
| RENT3 | 2026-05-20 | 5.11 | 2025-12-05 | -7.38 |
| VALE3 | 2026-01-14 | 4.06 | 2026-04-29 | -4.06 |
| WEGE3 | 2025-10-17 | 4.80 | 2025-07-24 | -5.16 |
### 5.2: Quais tickers mais valorizaram na última semana disponível na base?

```sql
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
```

| ticker | price_week_ago | current_price | week_change_pct |
| --- | --- | --- | --- |
| WEGE3 | 42.83 | 45.81 | 6.96 |
| KLBN4 | 3.41 | 3.44 | 0.88 |
| PETR4 | 38.54 | 38.85 | 0.80 |
| BBAS3 | 19.40 | 19.53 | 0.67 |
| ITUB4 | 40.09 | 40.13 | 0.10 |
| ENGI3 | 11.73 | 11.70 | -0.26 |
| BBDC4 | 17.66 | 17.47 | -1.08 |
| ABEV3 | 16.44 | 16.22 | -1.34 |
| VALE3 | 81.44 | 79.94 | -1.84 |
| RENT3 | 40.96 | 40.09 | -2.12 |
### 5.3: Quais pares de tickers movem-se na mesma direção com mais frequência?

```sql
-- Proxy simplificado de correlação (não é Pearson) — mesma direção intraday
SELECT a.ticker AS stock_a,
       b.ticker AS stock_b,
       ROUND(SUM(CASE WHEN (a.close - a.open) * (b.close - b.open) > 0 THEN 1 ELSE 0 END) * 1.0 / COUNT(*), 4) AS same_direction_pct
FROM daily_prices a
JOIN daily_prices b ON a.date = b.date AND a.ticker < b.ticker
GROUP BY stock_a, stock_b
HAVING COUNT(*) > 100
ORDER BY same_direction_pct DESC;
```

_45 linhas — exibindo as primeiras 25_

| stock_a | stock_b | same_direction_pct |
| --- | --- | --- |
| BBDC4 | ITUB4 | 0.76 |
| BBDC4 | RENT3 | 0.75 |
| BBAS3 | ITUB4 | 0.71 |
| BBAS3 | BBDC4 | 0.70 |
| ITUB4 | RENT3 | 0.69 |
| BBAS3 | RENT3 | 0.62 |
| BBDC4 | VALE3 | 0.61 |
| ABEV3 | BBAS3 | 0.60 |
| ABEV3 | BBDC4 | 0.60 |
| BBAS3 | VALE3 | 0.59 |
| BBAS3 | WEGE3 | 0.59 |
| BBDC4 | ENGI3 | 0.59 |
| BBAS3 | PETR4 | 0.59 |
| ITUB4 | VALE3 | 0.59 |
| ABEV3 | ITUB4 | 0.58 |
| ENGI3 | ITUB4 | 0.58 |
| ABEV3 | VALE3 | 0.58 |
| BBAS3 | KLBN4 | 0.58 |
| ITUB4 | WEGE3 | 0.57 |
| RENT3 | VALE3 | 0.57 |
| BBAS3 | ENGI3 | 0.57 |
| ENGI3 | RENT3 | 0.57 |
| ABEV3 | PETR4 | 0.56 |
| BBDC4 | WEGE3 | 0.56 |
| ITUB4 | PETR4 | 0.56 |
### 5.4: Quais tickers têm maior consistência de alta mês a mês?

```sql
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
```

| ticker | months_analysed | months_grew | growth_consistency_pct |
| --- | --- | --- | --- |
| VALE3 | 12 | 9 | 75.00 |
| ABEV3 | 12 | 8 | 66.70 |
| PETR4 | 12 | 7 | 58.30 |
| KLBN4 | 12 | 7 | 58.30 |
| ITUB4 | 12 | 7 | 58.30 |
| BBDC4 | 12 | 7 | 58.30 |
| WEGE3 | 12 | 6 | 50.00 |
| RENT3 | 12 | 5 | 41.70 |
| ENGI3 | 12 | 4 | 33.30 |
| BBAS3 | 12 | 4 | 33.30 |
