-- Report queries. Run with:  python3 build.py   (or any SQLite client)

-- 1. Invoice Summary report (with Status between Payment Day and Invoice Total)
SELECT invoice_number, invoice_date, company_name, payment_day, status, invoice_total
FROM invoice_summary;

-- 2. Grand total of all invoices
SELECT COUNT(*) AS invoices, ROUND(SUM(invoice_total), 2) AS grand_total
FROM invoice_summary;

-- 3. Totals per status
SELECT status, COUNT(*) AS invoices, ROUND(SUM(invoice_total), 2) AS total
FROM invoice_summary
GROUP BY status
ORDER BY CASE status WHEN 'Paid' THEN 1 WHEN 'Sent' THEN 2 ELSE 3 END;

-- 4. Invoice Form: header + rows for one invoice (here invoice 20, the student's own)
SELECT v.invoice_number, v.invoice_date, v.days_to_payment, s.payment_day,
       c.customer_id, c.company_name, c.street_address, c.postal_code, c.city, c.country
FROM invoices v
JOIN customers c USING (customer_id)
JOIN invoice_summary s USING (invoice_number)
WHERE v.invoice_number = 20;

SELECT item_id, item_name, price, amount, row_total
FROM invoice_row_lines
WHERE invoice_number = 20
ORDER BY row_id;

-- 5. Best-selling items
SELECT item_name, SUM(amount) AS units_sold, ROUND(SUM(row_total), 2) AS revenue
FROM invoice_row_lines
GROUP BY item_id
ORDER BY revenue DESC;

-- 6. Overdue check: unpaid invoices whose payment day is before a given date
SELECT invoice_number, company_name, payment_day, status, invoice_total
FROM invoice_summary
WHERE status <> 'Paid' AND payment_day < '2026-11-20';
