import sqlite3
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os

os.makedirs("database", exist_ok=True)
conn = sqlite3.connect("database/b3_stocks.db")
cursor = conn.cursor()

cursor.executescript("""
CREATE TABLE IF NOT EXISTS stocks (
    ticker TEXT PRIMARY KEY,
    company_name TEXT NOT NULL,
    sector TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS daily_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL,
    date TEXT NOT NULL,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume INTEGER,
    FOREIGN KEY (ticker) REFERENCES stocks(ticker)
);

CREATE TABLE IF NOT EXISTS financial_indicators (
    ticker TEXT NOT NULL,
    year INTEGER NOT NULL,
    revenue REAL,
    net_income REAL,
    ebitda REAL,
    total_debt REAL,
    PRIMARY KEY (ticker, year),
    FOREIGN KEY (ticker) REFERENCES stocks(ticker)
);
""")

stocks_data = [
    ("PETR4", "Petrobras", "Oil & Gas"),
    ("VALE3", "Vale", "Mining"),
    ("ITUB4", "Itaú Unibanco", "Banking"),
    ("BBDC4", "Bradesco", "Banking"),
    ("ABEV3", "Ambev", "Beverages"),
    ("WEGE3", "WEG", "Industrial"),
    ("BBAS3", "Banco do Brasil", "Banking"),
    ("ENGI3", "Energisa", "Energy"),
    ("KLBN4", "Klabin", "Paper & Packaging"),
    ("RENT3", "Localiza", "Car Rental"),
]

cursor.executemany(
    "INSERT OR IGNORE INTO stocks VALUES (?, ?, ?)", stocks_data
)

end = datetime.now()
start = end - timedelta(days=365)

for ticker, name, sector in stocks_data:
    try:
        df = yf.download(f"{ticker}.SA", start=start.strftime('%Y-%m-%d'), end=end.strftime('%Y-%m-%d'), progress=False, auto_adjust=True)
        if df.empty:
            print(f"  {ticker}: no data")
            continue

        df = df.reset_index()

        flat_cols = []
        for c in df.columns:
            if isinstance(c, tuple):
                flat_cols.append(c[0].lower())
            else:
                flat_cols.append(str(c).lower())
        df.columns = flat_cols

        df["ticker"] = ticker
        df = df.rename(columns={"adj close": "close"})

        df[["ticker", "date", "open", "high", "low", "close", "volume"]].to_sql(
            "daily_prices", conn, if_exists="append", index=False
        )
        print(f"  {ticker}: {len(df)} days loaded")
    except Exception as e:
        print(f"  {ticker}: {e}")

fin_data = [
    ("PETR4", 2023, 511.7, 124.6, 184.2, 187.3),
    ("PETR4", 2022, 488.2, 116.3, 175.1, 192.5),
    ("VALE3", 2023, 169.5, 38.2, 62.1, 34.7),
    ("VALE3", 2022, 175.4, 44.8, 70.2, 36.1),
    ("ITUB4", 2023, 189.7, 34.2, 52.1, 145.3),
    ("ITUB4", 2022, 182.4, 30.8, 48.7, 152.1),
    ("BBDC4", 2023, 157.2, 24.5, 38.4, 178.2),
    ("BBDC4", 2022, 149.8, 22.1, 35.2, 185.4),
    ("ABEV3", 2023, 78.4, 14.1, 18.5, 19.2),
    ("ABEV3", 2022, 75.6, 13.2, 17.8, 20.1),
    ("WEGE3", 2023, 48.5, 5.8, 8.2, 6.4),
    ("WEGE3", 2022, 44.2, 5.1, 7.4, 5.8),
    ("BBAS3", 2023, 142.8, 30.5, 45.2, 98.4),
    ("BBAS3", 2022, 138.1, 27.8, 42.6, 102.3),
    ("ENGI3", 2023, 28.4, 3.2, 7.1, 18.5),
    ("ENGI3", 2022, 26.1, 2.8, 6.4, 19.2),
    ("KLBN4", 2023, 24.8, 3.1, 5.4, 12.7),
    ("KLBN4", 2022, 22.5, 2.7, 4.9, 13.1),
    ("RENT3", 2023, 38.4, 4.9, 7.2, 14.8),
    ("RENT3", 2022, 35.1, 4.2, 6.5, 15.3),
]

cursor.executemany(
    "INSERT OR IGNORE INTO financial_indicators VALUES (?, ?, ?, ?, ?, ?)",
    fin_data
)

conn.commit()
conn.close()
print("\nDatabase created: database/b3_stocks.db")
