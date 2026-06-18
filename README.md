# B3 Financial Analysis with SQL

---

![SQL](https://img.shields.io/badge/SQL-SQLite-blue)
![Status](https://img.shields.io/badge/Status-Learning-brightgreen)
![Data](https://img.shields.io/badge/Data-B3%20Stocks-orange)

SQL project analyzing Brazilian stock market data (B3). This is my first public data project — built while learning SQL for a career in financial data analysis.

## Dataset

| Table | Description |
|---|---|
| `stocks` | 10 companies from different sectors |
| `daily_prices` | ~1 year of daily OHLCV data (via Yahoo Finance) |
| `financial_indicators` | Revenue, net income, EBITDA, debt (2022-2023) |

### Stocks covered

| Ticker | Company | Sector |
|---|---|---|
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

## Queries

| File | Topic | Skills practiced |
|---|---|---|
| `01_exploring_data.sql` | Basic exploration | SELECT, WHERE, GROUP BY, subqueries |
| `02_top_performers.sql` | Performance & volatility | CTEs, window functions, joins |
| `03_financial_health.sql` | Financial indicators | JOINs, self-joins, ratio analysis |
| `04_window_functions.sql` | Advanced analytics | LAG, AVG over, RANK, FIRST_VALUE |
| `05_challenge_queries.sql` | Challenge queries | ROW_NUMBER, complex CTEs, self-joins |

## How to run

**Prerequisites:** Python 3, SQLite (or DB Browser for SQLite)

```bash
# 1. Create the database
python create_database.py

# 2. Open with DB Browser or sqlite3
sqlite3 database/b3_stocks.db
```

Then open any `.sql` file and run the queries.

## Sample query

```sql
-- Best performing stocks
WITH first_last AS (
    SELECT p.ticker,
           MAX(CASE WHEN p.date = y.first_date THEN p.close END) AS first_close,
           MAX(CASE WHEN p.date = y.last_date THEN p.close END) AS last_close
    FROM daily_prices p
    JOIN (SELECT ticker, MIN(date) AS first_date, MAX(date) AS last_date
          FROM daily_prices GROUP BY ticker) y
    ON p.ticker = y.ticker
    GROUP BY p.ticker
)
SELECT ticker,
       ROUND(((last_close - first_close) / first_close) * 100, 2) AS return_pct
FROM first_last
ORDER BY return_pct DESC;
```

## Why this project

Applying SQL to real financial data to build the skills needed for a data analyst role in finance. Each query solves a business question an analyst would actually answer.

## Tools used

- **SQLite** — database
- **Python** (pandas, yfinance) — data collection
- **DB Browser for SQLite** — to run and explore queries

---

**Connect with me:** [LinkedIn](https://linkedin.com/in/dennermartins) | denner.rmartins@gmail.com
