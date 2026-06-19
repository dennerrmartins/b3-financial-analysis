# B3 Financial Analysis with SQL

[![SQL](https://img.shields.io/badge/SQL-SQLite-003B57?style=flat&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat)](https://github.com/dennerrmartins/b3-financial-analysis)
[![Data](https://img.shields.io/badge/Data-B3%20Stocks-orange?style=flat)](#dataset)

SQL project analyzing **real Brazilian stock market data (B3)**. Built while transitioning from BI/Automation into **Financial Data Analysis**.

> 10 stocks · 2,490+ price records · 20+ SQL queries · JOINs, CTEs & Window Functions

---

## Why this project

Applying SQL to real financial data to build the skills needed for a **Data Analyst role in Finance**. Each query answers a business question an analyst would actually face — returns, volatility, sector comparison, financial health ratios.

---

## Dataset

| Table | Description |
|-------|-------------|
| `stocks` | 10 companies from different sectors |
| `daily_prices` | ~1 year of daily OHLCV data (via Yahoo Finance) |
| `financial_indicators` | Revenue, net income, EBITDA, debt (2022–2023) |

### Stocks covered

| Ticker | Company | Sector |
|--------|---------|--------|
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

---

## Queries

| File | Topic | Skills practiced |
|------|-------|------------------|
| [`01_exploring_data.sql`](queries/01_exploring_data.sql) | Basic exploration | SELECT, WHERE, GROUP BY, subqueries |
| [`02_top_performers.sql`](queries/02_top_performers.sql) | Performance & volatility | CTEs, window functions, JOINs |
| [`03_financial_health.sql`](queries/03_financial_health.sql) | Financial indicators | JOINs, self-joins, ratio analysis |
| [`04_window_functions.sql`](queries/04_window_functions.sql) | Advanced analytics | LAG, AVG OVER, RANK, FIRST_VALUE |
| [`05_challenge_queries.sql`](queries/05_challenge_queries.sql) | Challenge queries | ROW_NUMBER, complex CTEs, self-joins |

---

## Quick start

**Prerequisites:** Python 3.10+, pip

```bash
# 1. Clone the repo
git clone https://github.com/dennerrmartins/b3-financial-analysis.git
cd b3-financial-analysis

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create the database (downloads data from Yahoo Finance)
python create_database.py

# 4. Run queries with sqlite3 or DB Browser for SQLite
sqlite3 database/b3_stocks.db
```

> The `.db` file is gitignored — run `create_database.py` to generate it locally.

---

## Sample query

```sql
-- Best performing stocks (year-to-date return)
WITH first_last AS (
    SELECT p.ticker,
           MAX(CASE WHEN p.date = y.first_date THEN p.close END) AS first_close,
           MAX(CASE WHEN p.date = y.last_date THEN p.close END) AS last_close
    FROM daily_prices p
    JOIN (
        SELECT ticker, MIN(date) AS first_date, MAX(date) AS last_date
        FROM daily_prices GROUP BY ticker
    ) y ON p.ticker = y.ticker
    GROUP BY p.ticker
)
SELECT ticker,
       ROUND(((last_close - first_close) / first_close) * 100, 2) AS return_pct
FROM first_last
ORDER BY return_pct DESC;
```

---

## Project structure

```
b3-financial-analysis/
├── create_database.py      # Downloads data & builds SQLite DB
├── requirements.txt        # Python dependencies
├── database/               # Generated locally (gitignored)
│   └── b3_stocks.db
└── queries/
    ├── 01_exploring_data.sql
    ├── 02_top_performers.sql
    ├── 03_financial_health.sql
    ├── 04_window_functions.sql
    └── 05_challenge_queries.sql
```

---

## Tools used

- **SQLite** — relational database
- **Python** (pandas, yfinance) — data collection & ETL
- **DB Browser for SQLite** — query exploration (optional)

---

## Author

**Denner Martins** — Data Analyst | BI & SQL | Economics @ UERJ

[![LinkedIn](https://img.shields.io/badge/LinkedIn-dennermartins-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/dennermartins)
[![GitHub](https://img.shields.io/badge/GitHub-dennerrmartins-181717?style=flat&logo=github&logoColor=white)](https://github.com/dennerrmartins)

---

*Part of my portfolio for a career in Financial Data Analysis — targeting international opportunities.*
