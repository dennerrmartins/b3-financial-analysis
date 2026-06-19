"""Executa todas as queries SQL e gera output/RESULTS.md com os resultados."""

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
    "03_financial_health.sql": "03 — Saúde Financeira",
    "04_window_functions.sql": "04 — Window Functions",
    "05_challenge_queries.sql": "05 — Queries Desafio",
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


def rows_to_markdown(headers: list[str], rows: list[tuple]) -> str:
    if not rows:
        return "_Sem resultados._\n"

    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        cells = [str(v) if v is not None else "" for v in row]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def run_query(conn: sqlite3.Connection, sql: str) -> tuple[list[str], list[tuple]] | None:
    try:
        cur = conn.execute(sql)
        rows = cur.fetchall()
        headers = [desc[0] for desc in cur.description] if cur.description else []
        return headers, rows
    except sqlite3.Error as exc:
        return None, [(str(exc),)]


def build_report() -> str:
    conn = sqlite3.connect(DB_PATH)
    parts = [
        "# B3 Financial Analysis — Resultados\n",
        f"> Gerado em **{datetime.now().strftime('%d/%m/%Y %H:%M')}** · "
        f"10 ações · SQLite · dados via Yahoo Finance\n",
        "---\n",
        "## Sumário executivo\n",
    ]

    summary_sql = """
    SELECT ticker,
           ROUND(((last_close - first_close) / first_close) * 100, 2) AS return_pct
    FROM (
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
    ORDER BY return_pct DESC
    LIMIT 3
    """
    headers, rows = run_query(conn, summary_sql)
    parts.append("**Top 3 retorno no período:**\n")
    for row in rows:
        parts.append(f"- **{row[0]}** → {row[1]}%\n")
    parts.append("\n---\n")

    for filename in sorted(QUERIES_DIR.glob("*.sql")):
        label = FILE_LABELS.get(filename.name, filename.stem)
        parts.append(f"## {label}\n")
        content = filename.read_text(encoding="utf-8")

        for title, sql in parse_queries(content):
            parts.append(f"### {title}\n")
            parts.append("```sql\n")
            parts.append(sql.strip() + "\n")
            parts.append("```\n\n")

            result = run_query(conn, sql)
            if result[0] is None:
                parts.append(f"**Erro:** {result[1][0][0]}\n\n")
                continue

            headers, rows = result
            if len(rows) > 25:
                parts.append(f"_{len(rows)} linhas — exibindo top 25_\n\n")
                rows = rows[:25]
            parts.append(rows_to_markdown(headers, rows))
            parts.append("\n")

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
