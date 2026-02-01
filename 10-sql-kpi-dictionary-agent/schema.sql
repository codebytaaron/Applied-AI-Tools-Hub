-- KPI Dictionary Schema (portable SQL)
CREATE TABLE IF NOT EXISTS kpi_dictionary (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  definition TEXT NOT NULL,
  formula TEXT NOT NULL,
  source_system TEXT,
  refresh_cadence TEXT,
  owner TEXT
);

-- Example inserts
INSERT INTO kpi_dictionary (name, definition, formula, source_system, refresh_cadence, owner)
VALUES
('Revenue', 'Total recognized revenue', 'SUM(invoice_amount)', 'Accounting', 'daily', 'Finance'),
('Gross Margin', 'Revenue minus COGS', '(Revenue - COGS) / Revenue', 'Accounting', 'weekly', 'Finance');

SELECT * FROM kpi_dictionary;
