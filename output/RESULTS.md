# B3 Financial Analysis — Resultados
> Gerado em **19/06/2026 16:05** · 10 ações · SQLite · dados via Yahoo Finance
---
## Sumário executivo
**Top 3 retorno no período:**
- **VALE3** → 74.43%
- **PETR4** → 28.77%
- **ABEV3** → 25.39%

---
## 01 — Exploração de Dados
### 1.1: View all stocks in the database
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

### 1.2: Group stocks by sector
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

### 1.3: Latest price for each stock
```sql
SELECT ticker, date, close
FROM daily_prices
WHERE date = (SELECT MAX(date) FROM daily_prices);
```

| ticker | date | close |
| --- | --- | --- |
| PETR4 | 2026-06-18 00:00:00 | 38.849998474121094 |
| VALE3 | 2026-06-18 00:00:00 | 79.94000244140625 |
| ITUB4 | 2026-06-18 00:00:00 | 40.12812042236328 |
| BBDC4 | 2026-06-18 00:00:00 | 17.469999313354492 |
| ABEV3 | 2026-06-18 00:00:00 | 16.219999313354492 |
| WEGE3 | 2026-06-18 00:00:00 | 45.810001373291016 |
| BBAS3 | 2026-06-18 00:00:00 | 19.530000686645508 |
| ENGI3 | 2026-06-18 00:00:00 | 11.699999809265137 |
| KLBN4 | 2026-06-18 00:00:00 | 3.440000057220459 |
| RENT3 | 2026-06-18 00:00:00 | 40.09000015258789 |

### 1.4: Average closing price per stock (last 30 days)
```sql
SELECT ticker, ROUND(AVG(close), 2) AS avg_price_30d
FROM daily_prices
WHERE date >= DATE('now', '-30 days')
GROUP BY ticker
ORDER BY avg_price_30d DESC;
```

| ticker | avg_price_30d |
| --- | --- |
| VALE3 | 81.26 |
| WEGE3 | 43.09 |
| RENT3 | 41.72 |
| PETR4 | 41.42 |
| ITUB4 | 39.48 |
| BBAS3 | 19.92 |
| BBDC4 | 17.64 |
| ABEV3 | 16.35 |
| ENGI3 | 11.82 |
| KLBN4 | 3.37 |

### 1.5: Highest volume day per stock
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
| BBAS3 | 2025-08-15 00:00:00 | 131820200 |
| ABEV3 | 2025-07-31 00:00:00 | 116074600 |
| PETR4 | 2025-08-08 00:00:00 | 107235300 |
| BBDC4 | 2026-02-06 00:00:00 | 94063600 |
| VALE3 | 2026-01-21 00:00:00 | 83134600 |
| ITUB4 | 2026-05-29 00:00:00 | 80334400 |
| RENT3 | 2025-06-26 00:00:00 | 33754000 |
| WEGE3 | 2025-07-23 00:00:00 | 31116000 |
| KLBN4 | 2026-05-06 00:00:00 | 16076300 |
| ENGI3 | 2025-12-19 00:00:00 | 41400 |

## 02 — Performance e Volatilidade
### 2.1: Top 5 best performing stocks (year-to-date return)
```sql
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

### 2.2: Stocks with highest average daily volume
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
| PETR4 | Petrobras | 40602575.0 | 34.52 |
| BBDC4 | Bradesco | 31294019.0 | 17.66 |
| BBAS3 | Banco do Brasil | 29898929.0 | 21.68 |
| ABEV3 | Ambev | 29158410.0 | 13.76 |
| ITUB4 | Itaú Unibanco | 25487895.0 | 38.03 |
| VALE3 | Vale | 23010805.0 | 68.43 |
| RENT3 | Localiza | 8787068.0 | 41.7 |
| WEGE3 | WEG | 8725155.0 | 42.97 |
| KLBN4 | Klabin | 3710491.0 | 3.54 |
| ENGI3 | Energisa | 6765.0 | 12.17 |

### 2.3: Most volatile stocks (standard deviation of daily returns)
```sql
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
```

| ticker | avg_daily_return_pct | variance |
| --- | --- | --- |
| RENT3 | 0.0184 | 5.8773 |
| ENGI3 | 0.06 | 5.3241 |
| WEGE3 | 0.075 | 3.4612 |
| BBAS3 | -0.0101 | 3.2848 |
| ABEV3 | 0.1043 | 2.6936 |
| BBDC4 | 0.0664 | 2.5054 |
| VALE3 | 0.237 | 2.4886 |
| PETR4 | 0.1144 | 2.4747 |
| ITUB4 | 0.0947 | 2.1502 |
| KLBN4 | 0.0367 | 1.788 |

## 03 — Saúde Financeira
### 3.1: Revenue vs Net Income comparison (2023)
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
| PETR4 | Petrobras | Oil & Gas | 511.7 | 124.6 | 24.35 |
| VALE3 | Vale | Mining | 169.5 | 38.2 | 22.54 |
| BBAS3 | Banco do Brasil | Banking | 142.8 | 30.5 | 21.36 |
| ITUB4 | Itaú Unibanco | Banking | 189.7 | 34.2 | 18.03 |
| ABEV3 | Ambev | Beverages | 78.4 | 14.1 | 17.98 |
| BBDC4 | Bradesco | Banking | 157.2 | 24.5 | 15.59 |
| RENT3 | Localiza | Car Rental | 38.4 | 4.9 | 12.76 |
| KLBN4 | Klabin | Paper & Packaging | 24.8 | 3.1 | 12.5 |
| WEGE3 | WEG | Industrial | 48.5 | 5.8 | 11.96 |
| ENGI3 | Energisa | Energy | 28.4 | 3.2 | 11.27 |

### 3.2: Debt ratio analysis
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
| VALE3 | Vale | 34.7 | 62.1 | 0.56 |
| WEGE3 | WEG | 6.4 | 8.2 | 0.78 |
| PETR4 | Petrobras | 187.3 | 184.2 | 1.02 |
| ABEV3 | Ambev | 19.2 | 18.5 | 1.04 |
| RENT3 | Localiza | 14.8 | 7.2 | 2.06 |
| BBAS3 | Banco do Brasil | 98.4 | 45.2 | 2.18 |
| KLBN4 | Klabin | 12.7 | 5.4 | 2.35 |
| ENGI3 | Energisa | 18.5 | 7.1 | 2.61 |
| ITUB4 | Itaú Unibanco | 145.3 | 52.1 | 2.79 |
| BBDC4 | Bradesco | 178.2 | 38.4 | 4.64 |

### 3.3: Year-over-year revenue growth
```sql
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
| KLBN4 | 22.5 | 24.8 | 10.22 |
| WEGE3 | 44.2 | 48.5 | 9.73 |
| RENT3 | 35.1 | 38.4 | 9.4 |
| ENGI3 | 26.1 | 28.4 | 8.81 |
| BBDC4 | 149.8 | 157.2 | 4.94 |
| PETR4 | 488.2 | 511.7 | 4.81 |
| ITUB4 | 182.4 | 189.7 | 4.0 |
| ABEV3 | 75.6 | 78.4 | 3.7 |
| BBAS3 | 138.1 | 142.8 | 3.4 |
| VALE3 | 175.4 | 169.5 | -3.36 |

### 3.4: Banking sector overview
```sql
SELECT s.ticker, s.company_name,
       f.revenue, f.net_income, f.total_debt
FROM stocks s
JOIN financial_indicators f ON s.ticker = f.ticker
WHERE s.sector = 'Banking' AND f.year = 2023;
```

| ticker | company_name | revenue | net_income | total_debt |
| --- | --- | --- | --- | --- |
| ITUB4 | Itaú Unibanco | 189.7 | 34.2 | 145.3 |
| BBDC4 | Bradesco | 157.2 | 24.5 | 178.2 |
| BBAS3 | Banco do Brasil | 142.8 | 30.5 | 98.4 |

## 04 — Window Functions
### 4.1: 20-day moving average for Petrobras
```sql
SELECT date, close,
       ROUND(AVG(close) OVER (ORDER BY date ROWS BETWEEN 19 PRECEDING AND CURRENT ROW), 2) AS ma_20
FROM daily_prices
WHERE ticker = 'PETR4'
ORDER BY date;
```

_249 linhas — exibindo top 25_

| date | close | ma_20 |
| --- | --- | --- |
| 2025-06-20 00:00:00 | 30.16919708251953 | 30.17 |
| 2025-06-23 00:00:00 | 29.415428161621094 | 29.79 |
| 2025-06-24 00:00:00 | 28.836313247680664 | 29.47 |
| 2025-06-25 00:00:00 | 28.689231872558594 | 29.28 |
| 2025-06-26 00:00:00 | 28.91904067993164 | 29.21 |
| 2025-06-27 00:00:00 | 28.689231872558594 | 29.12 |
| 2025-06-30 00:00:00 | 28.845502853393555 | 29.08 |
| 2025-07-01 00:00:00 | 28.946617126464844 | 29.06 |
| 2025-07-02 00:00:00 | 29.461387634277344 | 29.11 |
| 2025-07-03 00:00:00 | 29.562503814697266 | 29.15 |
| 2025-07-04 00:00:00 | 29.525733947753906 | 29.19 |
| 2025-07-07 00:00:00 | 29.470582962036133 | 29.21 |
| 2025-07-08 00:00:00 | 29.893428802490234 | 29.26 |
| 2025-07-09 00:00:00 | 29.709579467773438 | 29.3 |
| 2025-07-10 00:00:00 | 29.636045455932617 | 29.32 |
| 2025-07-11 00:00:00 | 29.99454689025879 | 29.36 |
| 2025-07-14 00:00:00 | 29.599273681640625 | 29.37 |
| 2025-07-15 00:00:00 | 29.36946678161621 | 29.37 |
| 2025-07-16 00:00:00 | 29.222389221191406 | 29.37 |
| 2025-07-17 00:00:00 | 28.928232192993164 | 29.34 |
| 2025-07-18 00:00:00 | 28.487003326416016 | 29.26 |
| 2025-07-21 00:00:00 | 28.54215431213379 | 29.22 |
| 2025-07-22 00:00:00 | 28.81792640686035 | 29.22 |
| 2025-07-23 00:00:00 | 29.406234741210938 | 29.25 |
| 2025-07-24 00:00:00 | 29.360273361206055 | 29.27 |

### 4.2: Daily return with LAG
```sql
SELECT ticker, date, close,
       LAG(close) OVER (PARTITION BY ticker ORDER BY date) AS prev_close,
       ROUND((close - LAG(close) OVER (PARTITION BY ticker ORDER BY date)) / LAG(close) OVER (PARTITION BY ticker ORDER BY date) * 100, 2) AS daily_return_pct
FROM daily_prices
WHERE ticker IN ('PETR4', 'VALE3', 'ITUB4')
ORDER BY ticker, date;
```

_747 linhas — exibindo top 25_

| ticker | date | close | prev_close | daily_return_pct |
| --- | --- | --- | --- | --- |
| ITUB4 | 2025-06-20 00:00:00 | 32.5827751159668 |  |  |
| ITUB4 | 2025-06-23 00:00:00 | 32.51164245605469 | 32.5827751159668 | -0.22 |
| ITUB4 | 2025-06-24 00:00:00 | 33.12522888183594 | 32.51164245605469 | 1.89 |
| ITUB4 | 2025-06-25 00:00:00 | 32.5294303894043 | 33.12522888183594 | -1.8 |
| ITUB4 | 2025-06-26 00:00:00 | 32.2893180847168 | 32.5294303894043 | -0.74 |
| ITUB4 | 2025-06-27 00:00:00 | 32.25375747680664 | 32.2893180847168 | -0.11 |
| ITUB4 | 2025-06-30 00:00:00 | 32.85845184326172 | 32.25375747680664 | 1.87 |
| ITUB4 | 2025-07-01 00:00:00 | 33.00761413574219 | 32.85845184326172 | 0.45 |
| ITUB4 | 2025-07-02 00:00:00 | 32.7407112121582 | 33.00761413574219 | -0.81 |
| ITUB4 | 2025-07-03 00:00:00 | 33.550323486328125 | 32.7407112121582 | 2.47 |
| ITUB4 | 2025-07-04 00:00:00 | 33.568115234375 | 33.550323486328125 | 0.05 |
| ITUB4 | 2025-07-07 00:00:00 | 33.12327575683594 | 33.568115234375 | -1.33 |
| ITUB4 | 2025-07-08 00:00:00 | 33.043190002441406 | 33.12327575683594 | -0.24 |
| ITUB4 | 2025-07-09 00:00:00 | 32.35813522338867 | 33.043190002441406 | -2.07 |
| ITUB4 | 2025-07-10 00:00:00 | 31.361677169799805 | 32.35813522338867 | -3.08 |
| ITUB4 | 2025-07-11 00:00:00 | 31.10366439819336 | 31.361677169799805 | -0.82 |
| ITUB4 | 2025-07-14 00:00:00 | 31.05028533935547 | 31.10366439819336 | -0.17 |
| ITUB4 | 2025-07-15 00:00:00 | 31.157052993774414 | 31.05028533935547 | 0.34 |
| ITUB4 | 2025-07-16 00:00:00 | 31.308292388916016 | 31.157052993774414 | 0.49 |
| ITUB4 | 2025-07-17 00:00:00 | 31.77983283996582 | 31.308292388916016 | 1.51 |
| ITUB4 | 2025-07-18 00:00:00 | 31.201539993286133 | 31.77983283996582 | -1.82 |
| ITUB4 | 2025-07-21 00:00:00 | 31.566307067871094 | 31.201539993286133 | 1.17 |
| ITUB4 | 2025-07-22 00:00:00 | 31.13925552368164 | 31.566307067871094 | -1.35 |
| ITUB4 | 2025-07-23 00:00:00 | 31.486236572265625 | 31.13925552368164 | 1.11 |
| ITUB4 | 2025-07-24 00:00:00 | 31.192642211914062 | 31.486236572265625 | -0.93 |

### 4.3: Rank stocks by average price per sector
```sql
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
| Car Rental | RENT3 | 41.7 | 1 |
| Energy | ENGI3 | 12.17 | 1 |
| Industrial | WEGE3 | 42.97 | 1 |
| Mining | VALE3 | 68.43 | 1 |
| Oil & Gas | PETR4 | 34.52 | 1 |
| Paper & Packaging | KLBN4 | 3.54 | 1 |

### 4.4: Cumulative return since first date
```sql
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

_249 linhas — exibindo top 25_

| ticker | date | cumulative_return_pct |
| --- | --- | --- |
| PETR4 | 2025-06-20 00:00:00 | 0.0 |
| PETR4 | 2025-06-23 00:00:00 | -2.5 |
| PETR4 | 2025-06-24 00:00:00 | -4.42 |
| PETR4 | 2025-06-25 00:00:00 | -4.91 |
| PETR4 | 2025-06-26 00:00:00 | -4.14 |
| PETR4 | 2025-06-27 00:00:00 | -4.91 |
| PETR4 | 2025-06-30 00:00:00 | -4.39 |
| PETR4 | 2025-07-01 00:00:00 | -4.05 |
| PETR4 | 2025-07-02 00:00:00 | -2.35 |
| PETR4 | 2025-07-03 00:00:00 | -2.01 |
| PETR4 | 2025-07-04 00:00:00 | -2.13 |
| PETR4 | 2025-07-07 00:00:00 | -2.32 |
| PETR4 | 2025-07-08 00:00:00 | -0.91 |
| PETR4 | 2025-07-09 00:00:00 | -1.52 |
| PETR4 | 2025-07-10 00:00:00 | -1.77 |
| PETR4 | 2025-07-11 00:00:00 | -0.58 |
| PETR4 | 2025-07-14 00:00:00 | -1.89 |
| PETR4 | 2025-07-15 00:00:00 | -2.65 |
| PETR4 | 2025-07-16 00:00:00 | -3.14 |
| PETR4 | 2025-07-17 00:00:00 | -4.11 |
| PETR4 | 2025-07-18 00:00:00 | -5.58 |
| PETR4 | 2025-07-21 00:00:00 | -5.39 |
| PETR4 | 2025-07-22 00:00:00 | -4.48 |
| PETR4 | 2025-07-23 00:00:00 | -2.53 |
| PETR4 | 2025-07-24 00:00:00 | -2.68 |

## 05 — Queries Desafio
### 5.1: Best and worst day for each stock
```sql
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
| ABEV3 | 2026-05-05 00:00:00 | 7.01 | 2025-07-28 00:00:00 | -3.04 |
| BBAS3 | 2025-08-15 00:00:00 | 8.51 | 2025-08-01 00:00:00 | -7.79 |
| BBDC4 | 2026-01-05 00:00:00 | 4.23 | 2025-12-05 00:00:00 | -6.11 |
| ENGI3 | 2025-08-15 00:00:00 | 7.97 | 2025-10-28 00:00:00 | -5.85 |
| ITUB4 | 2026-01-21 00:00:00 | 3.48 | 2025-12-05 00:00:00 | -4.73 |
| KLBN4 | 2026-02-11 00:00:00 | 5.56 | 2026-04-07 00:00:00 | -3.66 |
| PETR4 | 2026-04-08 00:00:00 | 4.27 | 2025-06-23 00:00:00 | -3.88 |
| RENT3 | 2026-05-20 00:00:00 | 5.11 | 2025-12-05 00:00:00 | -7.38 |
| VALE3 | 2026-01-14 00:00:00 | 4.06 | 2026-04-29 00:00:00 | -4.06 |
| WEGE3 | 2025-10-17 00:00:00 | 4.8 | 2025-07-24 00:00:00 | -5.16 |

### 5.2: Stocks that gained the most in the last week
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
| WEGE3 | 42.61 | 45.81 | 7.51 |
| ENGI3 | 11.52 | 11.7 | 1.56 |
| KLBN4 | 3.4 | 3.44 | 1.18 |
| VALE3 | 79.17 | 79.94 | 0.97 |
| BBAS3 | 19.46 | 19.53 | 0.36 |
| ITUB4 | 40.24 | 40.13 | -0.27 |
| RENT3 | 40.7 | 40.09 | -1.5 |
| BBDC4 | 17.8 | 17.47 | -1.85 |
| ABEV3 | 16.61 | 16.22 | -2.35 |
| PETR4 | 41.18 | 38.85 | -5.66 |

### 5.3: Correlation between stocks (simplified — same direction days)
```sql
SELECT a.ticker AS stock_a,
       b.ticker AS stock_b,
       ROUND(SUM(CASE WHEN (a.close - a.open) * (b.close - b.open) > 0 THEN 1 ELSE 0 END) * 1.0 / COUNT(*), 4) AS same_direction_pct
FROM daily_prices a
JOIN daily_prices b ON a.date = b.date AND a.ticker < b.ticker
GROUP BY stock_a, stock_b
HAVING COUNT(*) > 100
ORDER BY same_direction_pct DESC;
```

_45 linhas — exibindo top 25_

| stock_a | stock_b | same_direction_pct |
| --- | --- | --- |
| BBDC4 | ITUB4 | 0.759 |
| BBDC4 | RENT3 | 0.751 |
| BBAS3 | ITUB4 | 0.7149 |
| BBAS3 | BBDC4 | 0.6988 |
| ITUB4 | RENT3 | 0.6948 |
| BBAS3 | RENT3 | 0.6225 |
| BBDC4 | VALE3 | 0.6064 |
| ABEV3 | BBAS3 | 0.6024 |
| ABEV3 | BBDC4 | 0.6024 |
| BBAS3 | VALE3 | 0.5944 |
| BBAS3 | WEGE3 | 0.5904 |
| BBDC4 | ENGI3 | 0.5904 |
| BBAS3 | PETR4 | 0.5863 |
| ITUB4 | VALE3 | 0.5863 |
| ABEV3 | ITUB4 | 0.5823 |
| ENGI3 | ITUB4 | 0.5823 |
| ABEV3 | VALE3 | 0.5783 |
| BBAS3 | KLBN4 | 0.5783 |
| ITUB4 | WEGE3 | 0.5743 |
| RENT3 | VALE3 | 0.5743 |
| BBAS3 | ENGI3 | 0.5703 |
| ENGI3 | RENT3 | 0.5703 |
| ABEV3 | PETR4 | 0.5622 |
| BBDC4 | WEGE3 | 0.5582 |
| ITUB4 | PETR4 | 0.5582 |

### 5.4: Stocks with consistent growth (higher close each month)
```sql
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
| VALE3 | 12 | 9 | 75.0 |
| ABEV3 | 12 | 8 | 66.7 |
| PETR4 | 12 | 7 | 58.3 |
| KLBN4 | 12 | 7 | 58.3 |
| ITUB4 | 12 | 7 | 58.3 |
| BBDC4 | 12 | 7 | 58.3 |
| WEGE3 | 12 | 6 | 50.0 |
| RENT3 | 12 | 5 | 41.7 |
| ENGI3 | 12 | 4 | 33.3 |
| BBAS3 | 12 | 4 | 33.3 |

