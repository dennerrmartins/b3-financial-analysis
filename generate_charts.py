"""Gera gráficos PNG para README e portfólio a partir do banco SQLite."""

import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

ROOT = Path(__file__).parent
DB_PATH = ROOT / "database" / "b3_stocks.db"
OUT_DIR = ROOT / "assets" / "charts"

COLORS = {
    "bg": "#0f1419",
    "card": "#1a2332",
    "accent": "#3b82f6",
    "green": "#22c55e",
    "text": "#e2e8f0",
    "muted": "#94a3b8",
    "lines": ["#3b82f6", "#22c55e", "#f59e0b", "#a78bfa", "#ef4444"],
}

plt.rcParams.update({
    "figure.facecolor": COLORS["bg"],
    "axes.facecolor": COLORS["card"],
    "axes.edgecolor": COLORS["muted"],
    "axes.labelcolor": COLORS["text"],
    "text.color": COLORS["text"],
    "xtick.color": COLORS["muted"],
    "ytick.color": COLORS["muted"],
    "font.family": "Segoe UI",
    "font.size": 10,
})


def query(sql: str) -> list[tuple]:
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(sql).fetchall()
    conn.close()
    return rows


def save(fig: plt.Figure, name: str) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / name
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=COLORS["bg"])
    plt.close(fig)
    print(f"  {path.name}")
    return path


def footer(fig: plt.Figure, text: str, y: float = 0.02) -> None:
    fig.text(0.5, y, text, ha="center", fontsize=8, color=COLORS["muted"])


def chart_top_returns() -> None:
    rows = query("""
        WITH bounds AS (
            SELECT ticker, MIN(date) AS d1, MAX(date) AS d2
            FROM daily_prices GROUP BY ticker
        ),
        fl AS (
            SELECT p.ticker,
                   MAX(CASE WHEN p.date = b.d1 THEN p.close END) AS c1,
                   MAX(CASE WHEN p.date = b.d2 THEN p.close END) AS c2
            FROM daily_prices p JOIN bounds b ON p.ticker = b.ticker
            GROUP BY p.ticker
        )
        SELECT ticker, ROUND((c2 - c1) / c1 * 100, 2) FROM fl
        ORDER BY 2 DESC LIMIT 5
    """)
    tickers = [r[0] for r in rows][::-1]
    values = [r[1] for r in rows][::-1]

    fig, ax = plt.subplots(figsize=(10, 5.5))
    bars = ax.barh(tickers, values, color=COLORS["green"], height=0.55)
    for bar, val in zip(bars, values):
        ax.text(bar.get_width() + 0.8, bar.get_y() + bar.get_height() / 2,
                f"+{val}%", va="center", color=COLORS["green"], fontweight="bold", fontsize=9)
    ax.set_xlabel("Retorno no período (%)")
    ax.set_title("Top 5 tickers da amostra — maior retorno", fontsize=14, fontweight="bold", pad=12)
    ax.spines[["top", "right"]].set_visible(False)
    footer(fig, "Amostra de 10 tickers · preços via Yahoo Finance · conteúdo educacional")
    save(fig, "01_top_returns.png")


def chart_volatility() -> None:
    rows = query("""
        WITH daily_returns AS (
            SELECT ticker,
                   (close - LAG(close) OVER (PARTITION BY ticker ORDER BY date))
                   / LAG(close) OVER (PARTITION BY ticker ORDER BY date) * 100 AS ret
            FROM daily_prices
        ),
        stats AS (
            SELECT ticker,
                   (SUM(ret * ret) - SUM(ret) * SUM(ret) / COUNT(*)) / (COUNT(*) - 1) AS var
            FROM daily_returns WHERE ret IS NOT NULL GROUP BY ticker
        )
        SELECT ticker, ROUND(SQRT(var), 2) FROM stats ORDER BY 2 DESC
    """)
    tickers = [r[0] for r in rows]
    values = [r[1] for r in rows]

    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.bar(tickers, values, color=COLORS["accent"], width=0.62)
    ax.set_ylabel("Desvio padrão do retorno diário (%)")
    ax.set_title("Volatilidade por ticker (stddev_daily_return_pct)", fontsize=14, fontweight="bold", pad=12)
    plt.xticks(rotation=40, ha="right")
    ax.spines[["top", "right"]].set_visible(False)
    footer(fig, "Métrica alinhada à query 2.3 · não representa a B3 inteira")
    save(fig, "02_volatility.png")


def chart_price_evolution() -> None:
    tickers = [r[0] for r in query("""
        WITH bounds AS (
            SELECT ticker, MIN(date) AS d1, MAX(date) AS d2 FROM daily_prices GROUP BY ticker
        ),
        fl AS (
            SELECT p.ticker,
                   MAX(CASE WHEN p.date = b.d1 THEN p.close END) AS c1,
                   MAX(CASE WHEN p.date = b.d2 THEN p.close END) AS c2
            FROM daily_prices p JOIN bounds b ON p.ticker = b.ticker GROUP BY p.ticker
        )
        SELECT ticker FROM fl ORDER BY (c2 - c1) / c1 DESC LIMIT 3
    """)]

    fig, ax = plt.subplots(figsize=(10, 5.5))
    for i, ticker in enumerate(tickers):
        rows = query(f"""
            SELECT date, close FROM daily_prices
            WHERE ticker = '{ticker}' ORDER BY date
        """)
        if not rows:
            continue
        base = rows[0][1]
        dates = range(len(rows))
        normalized = [(r[1] / base - 1) * 100 for r in rows]
        ax.plot(dates, normalized, label=ticker, color=COLORS["lines"][i], linewidth=2)

    ax.set_title("Evolução do retorno acumulado — top 3 tickers", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Dias no período")
    ax.set_ylabel("Retorno acumulado (%)")
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f%%"))
    ax.legend(loc="upper left", framealpha=0.2)
    ax.spines[["top", "right"]].set_visible(False)
    ax.axhline(0, color=COLORS["muted"], linewidth=0.5, alpha=0.5)
    footer(fig, "Base 100 = primeiro pregão do período · dados reais de preço")
    save(fig, "03_price_evolution.png")


def chart_sector_sample() -> None:
    rows = query("SELECT sector, COUNT(*) FROM stocks GROUP BY sector ORDER BY 2 DESC")
    labels = [r[0] for r in rows]
    sizes = [r[1] for r in rows]

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(
        sizes, labels=labels, autopct="%1.0f%%",
        colors=COLORS["lines"][: len(labels)],
        startangle=140,
        textprops={"color": COLORS["text"], "fontsize": 9},
        wedgeprops={"edgecolor": COLORS["bg"], "linewidth": 2},
    )
    ax.set_title("Composição da amostra por setor\n(10 tickers, 8 setores)",
                 fontsize=13, fontweight="bold", pad=14)
    footer(fig, "Distribuição da amostra do projeto — não é o mercado B3 como um todo", y=0.01)
    save(fig, "04_sector_sample.png")


def chart_volume_leaders() -> None:
    rows = query("""
        SELECT s.ticker, ROUND(AVG(p.volume))
        FROM stocks s JOIN daily_prices p ON s.ticker = p.ticker
        GROUP BY s.ticker ORDER BY 2 DESC LIMIT 5
    """)
    tickers = [r[0] for r in rows][::-1]
    volumes = [r[1] for r in rows][::-1]

    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.barh(tickers, volumes, color=COLORS["accent"], height=0.55)
    ax.set_xlabel("Volume médio diário")
    ax.set_title("Top 5 tickers — maior volume médio negociado", fontsize=14, fontweight="bold", pad=12)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x/1e6:.1f}M"))
    ax.spines[["top", "right"]].set_visible(False)
    footer(fig, "Query 2.2 · liquidez como proxy de interesse do mercado na amostra")
    save(fig, "05_volume_leaders.png")


def main() -> None:
    if not DB_PATH.exists():
        raise SystemExit("Banco não encontrado. Execute: python create_database.py")

    print("Gerando gráficos em assets/charts/ ...")
    chart_top_returns()
    chart_volatility()
    chart_price_evolution()
    chart_sector_sample()
    chart_volume_leaders()
    print(f"Concluído: {OUT_DIR}")


if __name__ == "__main__":
    main()
