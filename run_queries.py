"""Executa todas as queries SQL e gera output/RESULTS.md com resultados e interpretações."""

import sqlite3
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent
DB_PATH = ROOT / "database" / "b3_stocks.db"
QUERIES_DIR = ROOT / "queries"
OUTPUT_DIR = ROOT / "output"
OUTPUT_FILE = OUTPUT_DIR / "RESULTS.md"

FILE_LABELS = {
    "01_exploring_data.sql": "01 — Exploração de Dados",
    "02_top_performers.sql": "02 — Performance e Volatilidade",
    "03_financial_health.sql": "03 — Saúde Financeira (dados ilustrativos)",
    "04_window_functions.sql": "04 — Window Functions",
    "05_challenge_queries.sql": "05 — Queries Desafio",
}

FILE_INTROS = {
    "01_exploring_data.sql": (
        "Validação da base, distribuição da amostra e leitura inicial de preços e volume."
    ),
    "02_top_performers.sql": (
        "Análise de retorno, liquidez e volatilidade com dados reais de preço (Yahoo Finance)."
    ),
    "03_financial_health.sql": (
        "**Atenção:** indicadores desta seção vêm de `financial_indicators`, "
        "dados **ilustrativos** inseridos manualmente para prática de JOINs e ratios — "
        "não substituem balanços auditados."
    ),
    "04_window_functions.sql": (
        "Séries temporais com médias móveis, retorno diário, ranking por setor e retorno acumulado."
    ),
    "05_challenge_queries.sql": (
        "Queries avançadas: melhor/pior dia, performance semanal, correlação simplificada e consistência mensal."
    ),
}

INTERPRETATIONS = {
    "2.1: Top 5 best performing stocks (year-to-date return)": (
        "Ranking de retorno na amostra. Útil para comparar desempenho relativo entre tickers no período analisado."
    ),
    "2.3: Most volatile stocks (standard deviation of daily returns)": (
        "Maior `stddev_daily_return_pct` indica maior oscilação diária. "
        "Métrica alinhada ao cálculo estatístico de desvio padrão amostral."
    ),
    "3.1: Revenue vs Net Income comparison (2023)": (
        "_Dados ilustrativos._ Exercício de margem líquida via SQL — não usar para decisão de investimento."
    ),
    "5.2: Stocks that gained the most in the last week": (
        "Leitura de curto prazo. Sensível à data de geração do banco local."
    ),
}


def parse_queries(content: str) -> list[tuple[str, str]]:
    blocks: list[tuple[str, str]] = []
    current_title = "Query"
    current_lines: list[str] = []

    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("--") and ":" in stripped[2:]:
            if current_lines:
                blocks.append((current_title, "\n".join(current_lines).strip()))
                current_lines = []
            current_title = stripped.lstrip("- ").strip()
        elif stripped:
            current_lines.append(line)

    if current_lines:
        blocks.append((current_title, "\n".join(current_lines).strip()))

    return blocks


def format_cell(value) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.2f}" if abs(value) >= 0.01 else f"{value:.4f}"
    text = str(value)
    if " 00:00:00" in text:
        return text.split(" ")[0]
    return text


def rows_to_markdown(headers: list[str], rows: list[tuple]) -> str:
    if not rows:
        return "_Sem resultados._\n"

    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        cells = [format_cell(v) for v in row]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def run_query(conn: sqlite3.Connection, sql: str):
    try:
        cur = conn.execute(sql)
        rows = cur.fetchall()
        headers = [desc[0] for desc in cur.description] if cur.description else []
        return headers, rows
    except sqlite3.Error as exc:
        return None, [(str(exc),)]


def executive_summary(conn: sqlite3.Connection) -> str:
    period = conn.execute(
        "SELECT MIN(date), MAX(date), COUNT(*) FROM daily_prices"
    ).fetchone()
    d1, d2, total_rows = period[0], period[1], period[2]
    d1 = str(d1).split(" ")[0] if d1 else "—"
    d2 = str(d2).split(" ")[0] if d2 else "—"

    parts = [
        f"- **Período analisado:** {d1} a {d2}\n",
        f"- **Registros de preço:** {total_rows:,} linhas · 10 tickers na amostra\n",
    ]

    returns_sql = """
        SELECT ticker, ROUND(((c2 - c1) / c1) * 100, 2)
        FROM (
            SELECT p.ticker,
                   MAX(CASE WHEN p.date = b.d1 THEN p.close END) AS c1,
                   MAX(CASE WHEN p.date = b.d2 THEN p.close END) AS c2
            FROM daily_prices p
            JOIN (
                SELECT ticker, MIN(date) AS d1, MAX(date) AS d2
                FROM daily_prices GROUP BY ticker
            ) b ON p.ticker = b.ticker
            GROUP BY p.ticker
        ) ORDER BY 2 DESC LIMIT 3
    """
    parts.append("\n**Maior retorno no período (tickers):**\n")
    for row in conn.execute(returns_sql):
        parts.append(f"- **{row[0]}** → {row[1]}%\n")

    vol_sql = """
        WITH daily_returns AS (
            SELECT ticker,
                   (close - LAG(close) OVER (PARTITION BY ticker ORDER BY date))
                   / LAG(close) OVER (PARTITION BY ticker ORDER BY date) * 100 AS ret
            FROM daily_prices
        ),
        stats AS (
            SELECT ticker,
                   (SUM(ret*ret) - SUM(ret)*SUM(ret)/COUNT(*)) / (COUNT(*)-1) AS var
            FROM daily_returns WHERE ret IS NOT NULL GROUP BY ticker
        )
        SELECT ticker, ROUND(SQRT(var), 2) FROM stats ORDER BY 2 DESC LIMIT 3
    """
    parts.append("\n**Maior volatilidade (stddev retorno diário):**\n")
    for row in conn.execute(vol_sql):
        parts.append(f"- **{row[0]}** → {row[1]}%\n")

    parts.append(
        "\n> Gráficos disponíveis em [`assets/charts/`](../assets/charts/) "
        "(gerados por `generate_charts.py`).\n"
    )
    return "".join(parts)


def build_report() -> str:
    conn = sqlite3.connect(DB_PATH)
    parts = [
        "# B3 Financial Analysis — Relatório de Resultados\n\n",
        f"> Gerado em **{datetime.now().strftime('%d/%m/%Y %H:%M')}** · "
        "amostra de 10 tickers · SQLite · preços via Yahoo Finance\n\n",
        "> **Avisos legais e técnicos**\n",
        "> - Conteúdo **educacional**. Não é recomendação de investimento.\n",
        "> - A amostra **não representa** a B3 como um todo.\n",
        "> - Indicadores do módulo 03 são **dados ilustrativos** para prática de SQL.\n\n",
        "---\n\n",
        "## Sumário executivo\n\n",
        executive_summary(conn),
        "\n---\n\n",
    ]

    for filename in sorted(QUERIES_DIR.glob("*.sql")):
        label = FILE_LABELS.get(filename.name, filename.stem)
        intro = FILE_INTROS.get(filename.name, "")
        parts.append(f"## {label}\n\n")
        if intro:
            parts.append(f"{intro}\n\n")

        content = filename.read_text(encoding="utf-8")
        for title, sql in parse_queries(content):
            parts.append(f"### {title}\n\n")
            parts.append("```sql\n")
            parts.append(sql.strip() + "\n")
            parts.append("```\n\n")

            result = run_query(conn, sql)
            if result[0] is None:
                parts.append(f"**Erro:** {result[1][0][0]}\n\n")
                continue

            headers, rows = result
            if len(rows) > 25:
                parts.append(f"_{len(rows)} linhas — exibindo as primeiras 25_\n\n")
                rows = rows[:25]

            parts.append(rows_to_markdown(headers, rows))

            note = INTERPRETATIONS.get(title)
            if note:
                parts.append(f"**Interpretação:** {note}\n\n")

    conn.close()
    return "".join(parts)


def main() -> None:
    if not DB_PATH.exists():
        raise SystemExit("Banco não encontrado. Rode: python create_database.py")

    OUTPUT_DIR.mkdir(exist_ok=True)
    report = build_report()
    OUTPUT_FILE.write_text(report, encoding="utf-8")
    print(f"Relatório gerado: {OUTPUT_FILE}")
    print(f"Tamanho: {OUTPUT_FILE.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
