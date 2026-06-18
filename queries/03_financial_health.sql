-- 3.1: Revenue vs Net Income comparison (2023)
SELECT s.ticker, s.company_name, s.sector,
       f.revenue, f.net_income,
       ROUND(f.net_income / f.revenue * 100, 2) AS profit_margin_pct
FROM stocks s
JOIN financial_indicators f ON s.ticker = f.ticker
WHERE f.year = 2023
ORDER BY profit_margin_pct DESC;

-- 3.2: Debt ratio analysis
SELECT s.ticker, s.company_name,
       f.total_debt,
       f.ebitda,
       ROUND(f.total_debt / NULLIF(f.ebitda, 0), 2) AS debt_to_ebitda
FROM stocks s
JOIN financial_indicators f ON s.ticker = f.ticker
WHERE f.year = 2023
ORDER BY debt_to_ebitda;

-- 3.3: Year-over-year revenue growth
SELECT a.ticker,
       a.revenue AS revenue_2022,
       b.revenue AS revenue_2023,
       ROUND((b.revenue - a.revenue) / a.revenue * 100, 2) AS revenue_growth_pct
FROM financial_indicators a
JOIN financial_indicators b ON a.ticker = b.ticker
WHERE a.year = 2022 AND b.year = 2023
ORDER BY revenue_growth_pct DESC;

-- 3.4: Banking sector overview
SELECT s.ticker, s.company_name,
       f.revenue, f.net_income, f.total_debt
FROM stocks s
JOIN financial_indicators f ON s.ticker = f.ticker
WHERE s.sector = 'Banking' AND f.year = 2023;
