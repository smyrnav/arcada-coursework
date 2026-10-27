#!/usr/bin/env python3
"""Build blueberry.db from sql/, export CSVs for FileMaker and write the reports.

Usage:  python3 build.py
Needs only the Python standard library.
"""
import csv
import sqlite3
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DB = ROOT / "blueberry.db"
EXPORTS = ROOT / "exports"
REPORTS = ROOT / "reports"

# Invoices 1–3 already exist in the FileMaker file; only these get exported for import.
FIRST_NEW_INVOICE = 4
FORM_INVOICE = 20


def fi_date(iso):
    """2026-10-02 -> 2.10.2026 (the date format FileMaker uses on Finnish/Swedish Windows)."""
    d = date.fromisoformat(iso)
    return f"{d.day}.{d.month}.{d.year}"


def eur(x):
    return f"{x:,.2f} €".replace(",", " ")


def build_db():
    DB.unlink(missing_ok=True)
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    for name in ("01_schema.sql", "02_seed.sql"):
        con.executescript((ROOT / "sql" / name).read_text(encoding="utf-8"))
    con.commit()
    return con


def export_csv(con, filename, query, params=(), date_cols=()):
    rows = con.execute(query, params).fetchall()
    with open(EXPORTS / filename, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(rows[0].keys())
        for r in rows:
            w.writerow([fi_date(r[k]) if k in date_cols else r[k] for k in r.keys()])
    return len(rows)


def export_for_filemaker(con):
    EXPORTS.mkdir(exist_ok=True)
    counts = {
        "customers.csv": export_csv(con, "customers.csv", "SELECT * FROM customers ORDER BY customer_id"),
        "items.csv": export_csv(con, "items.csv", "SELECT * FROM items ORDER BY item_id"),
        "invoices.csv": export_csv(
            con, "invoices.csv",
            "SELECT * FROM invoices WHERE invoice_number >= ? ORDER BY invoice_date, invoice_number",
            (FIRST_NEW_INVOICE,), date_cols=("invoice_date",)),
        "invoice_rows.csv": export_csv(
            con, "invoice_rows.csv",
            "SELECT * FROM invoice_rows WHERE invoice_number >= ? ORDER BY invoice_number, row_id",
            (FIRST_NEW_INVOICE,)),
    }
    return counts


def write_summary_report(con):
    rows = con.execute("SELECT * FROM invoice_summary").fetchall()
    grand = sum(r["invoice_total"] for r in rows)
    lines = [
        "# Invoice Summary — Blueberry Electronics Ltd",
        "",
        f"All {len(rows)} invoices, October–November 2026. Generated from `invoice_summary` view.",
        "",
        "| Invoice | Date | Customer | Payment day | Status | Invoice total |",
        "|---:|---|---|---|---|---:|",
    ]
    for r in rows:
        lines.append(
            f"| {r['invoice_number']} | {fi_date(r['invoice_date'])} | {r['company_name']} "
            f"| {fi_date(r['payment_day'])} | {r['status']} | {eur(r['invoice_total'])} |")
    lines += ["", f"**Grand total: {eur(grand)}**", "", "## Totals per status", "",
              "| Status | Invoices | Total |", "|---|---:|---:|"]
    for r in con.execute(
            "SELECT status, COUNT(*) n, SUM(invoice_total) t FROM invoice_summary GROUP BY status "
            "ORDER BY CASE status WHEN 'Paid' THEN 1 WHEN 'Sent' THEN 2 ELSE 3 END"):
        lines.append(f"| {r['status']} | {r['n']} | {eur(r['t'])} |")
    (REPORTS / "invoice_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(rows), grand


def write_all_invoices(con):
    lines = ["# All invoices with rows", "",
             "Every invoice with its item rows, in date order.", ""]
    for h in con.execute(
            "SELECT s.*, v.customer_id FROM invoice_summary s JOIN invoices v USING (invoice_number)"):
        lines += [
            f"## Invoice {h['invoice_number']} — {fi_date(h['invoice_date'])} — {h['status']}",
            "",
            f"Customer: **{h['company_name']}** (id {h['customer_id']}) · "
            f"days to payment {h['days_to_payment']} · payment day {fi_date(h['payment_day'])}",
            "",
            "| Item ID | Item name | Amount | Row total |",
            "|---:|---|---:|---:|",
        ]
        for r in con.execute(
                "SELECT * FROM invoice_row_lines WHERE invoice_number = ? ORDER BY row_id",
                (h["invoice_number"],)):
            lines.append(f"| {r['item_id']} | {r['item_name']} | {r['amount']} | {eur(r['row_total'])} |")
        lines += ["", f"Invoice total: **{eur(h['invoice_total'])}**", ""]
    (REPORTS / "all_invoices.md").write_text("\n".join(lines), encoding="utf-8")


def write_invoice_form(con, number):
    h = con.execute(
        "SELECT v.*, s.payment_day, s.invoice_total, c.* FROM invoices v "
        "JOIN customers c USING (customer_id) JOIN invoice_summary s USING (invoice_number) "
        "WHERE v.invoice_number = ?", (number,)).fetchone()
    lines = [
        f"# INVOICE {h['invoice_number']}",
        "",
        "**Blueberry Electronics Ltd**",
        "",
        "| | |", "|---|---|",
        f"| Invoice number | {h['invoice_number']} |",
        f"| Invoice date | {fi_date(h['invoice_date'])} |",
        f"| Days to payment | {h['days_to_payment']} |",
        f"| Payment day | {fi_date(h['payment_day'])} |",
        "",
        f"**Bill to** (customer {h['customer_id']})  ",
        f"{h['company_name']}  ",
        f"{h['street_address']}  ",
        f"{h['postal_code']} {h['city']}  ",
        f"{h['country']}",
        "",
        "| Item ID | Item name | Price | Amount | Total |",
        "|---:|---|---:|---:|---:|",
    ]
    for r in con.execute(
            "SELECT * FROM invoice_row_lines WHERE invoice_number = ? ORDER BY row_id", (number,)):
        lines.append(f"| {r['item_id']} | {r['item_name']} | {eur(r['price'])} "
                     f"| {r['amount']} | {eur(r['row_total'])} |")
    lines += ["", f"**TOTAL: {eur(h['invoice_total'])}**", "", "---", "",
              "Arcada Accessories, Hameentie 3, 00500 HELSINKI · Bank account 123456-7890  ",
              f"Due date: {fi_date(h['payment_day'])}"]
    (REPORTS / f"invoice_{number}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    REPORTS.mkdir(exist_ok=True)
    con = build_db()
    counts = export_for_filemaker(con)
    n, grand = write_summary_report(con)
    write_all_invoices(con)
    write_invoice_form(con, FORM_INVOICE)
    con.close()
    print(f"Built {DB.name}: {n} invoices, grand total {eur(grand)}")
    for name, c in counts.items():
        print(f"  exports/{name}: {c} rows")
    print(f"  reports/invoice_summary.md, reports/all_invoices.md, reports/invoice_{FORM_INVOICE}.md")


if __name__ == "__main__":
    main()
