# Case Study — B3 Financial Analysis

**Autor:** Denner Martins  
**Área:** Dados · BI · Mercado Financeiro  
**Stack:** SQL · Python · SQLite · pandas · matplotlib

> **Aviso:** este case é **educacional** e faz parte de um portfólio profissional. **Não constitui recomendação de investimento.**

---

## 1. Contexto

Profissionais de dados na área financeira precisam ir além de planilhas manuais: estruturar dados, escrever queries reprodutíveis e comunicar achados com clareza — para gestores, áreas de risco ou clientes internos.

Este projeto nasce desse contexto: uma análise SQL sobre **uma amostra de 10 tickers da B3**, usando preços reais baixados via Yahoo Finance, com documentação completa do fluxo analítico.

Conecta minha experiência em **controle de pagamentos, orçamento x realizado (DRE) e BI** com prática quantitativa em ativos listados.

---

## 2. Problema de negócio

> *"Como identificar, de forma reprodutível, quais tickers da amostra tiveram melhor retorno, maior volatilidade e maior liquidez em um período — e documentar isso para revisão técnica ou apresentação?"*

Sem um pipeline estruturado, a análise ficaria em planilhas descartáveis, difíceis de auditar e impossíveis de versionar. O objetivo foi criar um **mini pipeline analítico** versionado no GitHub.

---

## 3. Metodologia

| Etapa | Ferramenta | Entrega |
|-------|------------|---------|
| 1. Coleta | Python + yfinance | Dados OHLCV no SQLite |
| 2. Modelagem | SQLite | 3 tabelas relacionadas |
| 3. Análise | SQL (20+ queries) | Respostas por pergunta de negócio |
| 4. Relatório | `run_queries.py` | `output/RESULTS.md` |
| 5. Visualização | `generate_charts.py` | `assets/charts/*.png` |

**Princípios adotados:**
- Separar dados **reais** (preços) de dados **ilustrativos** (indicadores contábeis do módulo 03)
- Nomear métricas com precisão (`stddev_daily_return_pct`, não "volatilidade genérica")
- Documentar limitações da amostra explicitamente

---

## 4. Dados utilizados

### Dados reais (Yahoo Finance)
- Tabela `daily_prices`: preços diários de abertura, máxima, mínima, fechamento e volume
- ~249 pregões por ticker · 10 tickers · período definido na coleta

### Dados ilustrativos (módulo 03)
- Tabela `financial_indicators`: receita, lucro, EBITDA e dívida (2022–2023)
- Inseridos manualmente em `create_database.py` **apenas para prática de JOINs e ratios**
- **Não substituem** demonstrações financeiras oficiais

### Amostra
10 tickers de setores distintos (PETR4, VALE3, ITUB4, BBDC4, ABEV3, WEGE3, BBAS3, ENGI3, KLBN4, RENT3). **Não representa o mercado B3 como um todo.**

---

## 5. Consultas SQL aplicadas

| Módulo | Pergunta respondida |
|--------|---------------------|
| 01 — Exploração | Qual a composição da base? Quais os preços e volumes recentes? |
| 02 — Performance | Quem liderou em retorno? Quem teve maior volatilidade e volume? |
| 03 — Saúde financeira | Como comparar margem, dívida/EBITDA e crescimento? *(ilustrativo)* |
| 04 — Window functions | Como calcular média móvel, retorno diário e retorno acumulado? |
| 05 — Desafio | Qual o melhor/pior dia? Quem subiu na semana? Há correlação simplificada? |

**Exemplo técnico — retorno no período (query 2.1):**
```sql
WITH yearly_prices AS (
    SELECT ticker, MIN(date) AS first_date, MAX(date) AS last_date
    FROM daily_prices GROUP BY ticker
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
       ROUND(((last_close - first_close) / first_close) * 100, 2) AS return_pct
FROM first_last
ORDER BY return_pct DESC;
```

---

## 6. Principais descobertas

*(Valores dependem da data de execução — consulte [RESULTS.md](../output/RESULTS.md) para números atualizados.)*

1. **Retorno:** na última execução, VALE3 liderou o ranking de retorno na amostra, seguido por PETR4 e ABEV3.
2. **Volatilidade:** tickers com maior `stddev_daily_return_pct` concentram maior oscilação diária — métrica útil para leitura de risco relativo *dentro da amostra*.
3. **Liquidez:** volume médio (query 2.2) ajuda a distinguir ativos com maior interesse de negociação no período.
4. **Setores:** a amostra tem peso em Banking (3 tickers), mas o gráfico de setores mostra apenas a **composição da amostra**, não o mercado inteiro.
5. **Indicadores contábeis (módulo 03):** exercício válido de SQL, mas com dados ilustrativos — não devem ser citados como fatos de mercado.

---

## 7. Limitações da análise

| Limitação | Impacto |
|-----------|---------|
| Amostra de apenas 10 tickers | Não generalizável para a B3 |
| Período ~12 meses | Retornos sensíveis à janela temporal |
| Indicadores do módulo 03 ilustrativos | Não usar para decisão de investimento |
| Correlação simplificada (query 5.3) | Proxy estatístico, não correlação de Pearson |
| Dados Yahoo Finance | Podem diferir de fontes oficiais da B3 |

---

## 8. Aplicações práticas

As habilidades demonstradas neste case transferem-se para:

- **Dashboards financeiros** — KPIs de retorno, volatilidade e volume
- **Relatórios automatizados** — SQL + Python + exportação periódica
- **BI para pequenos negócios** — organização de dados e indicadores
- **Controle de carteira** — acompanhamento de performance *(com dados reais e governança adequada)*
- **Áreas de risco e crédito** — análises reprodutíveis e auditáveis

---

## 9. Próximos passos

- [ ] Conectar pipeline a PostgreSQL (ambiente mais próximo de produção)
- [ ] Adicionar testes automatizados para queries críticas
- [ ] Integrar camada Power BI sobre o SQLite exportado
- [ ] Expandir amostra ou parametrizar tickers via CLI
- [ ] Substituir indicadores ilustrativos por API de fundamentos *(se disponível e licenciada)*

---

## 10. Como reproduzir

```bash
pip install -r requirements.txt
python create_database.py
python run_queries.py
python generate_charts.py
```

---

**Denner Martins**  
[LinkedIn](https://linkedin.com/in/dennermartins) · [GitHub](https://github.com/dennerrmartins) · denner.rmartins@gmail.com

*Case de portfólio — conteúdo educacional, sem recomendação de investimento.*
