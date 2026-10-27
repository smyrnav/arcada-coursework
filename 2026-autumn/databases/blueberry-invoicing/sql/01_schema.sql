-- Blueberry Electronics Ltd — invoicing database
-- Mirrors the FileMaker file invoicing_final_assignment_2026.fmp12:
-- Customers 1—n Invoices 1—n Invoice rows n—1 Items

PRAGMA foreign_keys = ON;

DROP VIEW  IF EXISTS invoice_summary;
DROP VIEW  IF EXISTS invoice_row_lines;
DROP TABLE IF EXISTS invoice_rows;
DROP TABLE IF EXISTS invoices;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id     INTEGER PRIMARY KEY,
    company_name    TEXT    NOT NULL,
    street_address  TEXT    NOT NULL,
    postal_code     TEXT    NOT NULL,
    city            TEXT    NOT NULL,
    country         TEXT    NOT NULL DEFAULT 'Finland',
    email           TEXT,
    phone           TEXT
);

CREATE TABLE items (
    item_id         INTEGER PRIMARY KEY,
    item_name       TEXT    NOT NULL,
    category        TEXT    NOT NULL,
    description     TEXT    NOT NULL,
    price           NUMERIC NOT NULL CHECK (price > 0),   -- EUR, VAT 0 % for the exercise
    stock           INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0)
);

CREATE TABLE invoices (
    invoice_number  INTEGER PRIMARY KEY,
    customer_id     INTEGER NOT NULL REFERENCES customers (customer_id),
    invoice_date    TEXT    NOT NULL,                      -- ISO date YYYY-MM-DD
    days_to_payment INTEGER NOT NULL DEFAULT 14 CHECK (days_to_payment > 0),
    status          TEXT    NOT NULL DEFAULT 'Open'
                    CHECK (status IN ('Open', 'Sent', 'Paid'))
);

CREATE TABLE invoice_rows (
    row_id          INTEGER PRIMARY KEY,
    invoice_number  INTEGER NOT NULL REFERENCES invoices (invoice_number) ON DELETE CASCADE,
    item_id         INTEGER NOT NULL REFERENCES items (item_id),
    amount          INTEGER NOT NULL CHECK (amount > 0)    -- quantity
);

-- One line per invoice row, with the calculated row total
CREATE VIEW invoice_row_lines AS
SELECT r.row_id,
       r.invoice_number,
       r.item_id,
       i.item_name,
       i.price,
       r.amount,
       ROUND(i.price * r.amount, 2) AS row_total
FROM invoice_rows r
JOIN items i USING (item_id);

-- The "Invoice Summary" report: one line per invoice, incl. status
-- (FileMaker: Payment Day = Invoice Date + Days to payment, Invoice Total = Sum(row totals))
CREATE VIEW invoice_summary AS
SELECT v.invoice_number,
       v.invoice_date,
       c.company_name,
       v.days_to_payment,
       DATE(v.invoice_date, '+' || v.days_to_payment || ' days') AS payment_day,
       v.status,
       ROUND(COALESCE(SUM(l.row_total), 0), 2)                  AS invoice_total
FROM invoices v
JOIN customers c USING (customer_id)
LEFT JOIN invoice_row_lines l USING (invoice_number)
GROUP BY v.invoice_number
ORDER BY v.invoice_date, v.invoice_number;
