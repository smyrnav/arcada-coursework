# Getting the data into FileMaker

Step by step, for the school computer (Windows, FileMaker Pro).

**Plan A** imports the invoices from the CSV files. **Plan B** is typing them in by hand from
[all_invoices.md](reports/all_invoices.md) — slower but can't go wrong. Try A; if it gets messy, delete what
was imported (see step 5) and do B.

## 1. Download the files

1. Get `invoicing_final_assignment_2026.fmp12` from itslearning → Databases. Save it to **Documents**
   (not straight from the browser's download bar — FileMaker needs a normal folder).
2. Open the repo page <https://github.com/smyrnav/arcada-coursework>, click the green **Code** button →
   **Download ZIP**.
3. In the Downloads folder, right-click the ZIP → **Extract All…** → Extract.
4. The CSVs are now in
   `arcada-coursework-main\2026-autumn\databases\blueberry-invoicing\exports\`.
   You only need **invoices.csv** and **invoice_rows.csv**.

## 2. Do the hand-made parts first (the assignment wants these anyway)

Double-click the `.fmp12` file to open it in FileMaker.

1. Go to the **Customers** layout (layout menu at the top left) → **Records → New Record**.
   Company name: **your full name** (the FileMaker file is only sent to the teacher, so the full name is fine there), fill in the address.
   **Write down the Customer ID** that appears.
2. Go to the **Items** layout. Add the 3 items from [items.csv](exports/items.csv), one **New Record** each,
   filling every field. **Write down the 3 Item IDs** FileMaker gives them.
3. Pick **4 existing customers** (browse with the arrows) and write down their Customer IDs.
4. Go to the **Invoices** layout and look at the 3 existing invoices: write down their **invoice numbers**
   and change their **dates** to 2.10.2026, 5.10.2026 and 7.10.2026, status **Paid**.

⚠️ If the IDs are long codes like `8F3A1C2E-…` instead of plain numbers, skip Plan A and use Plan B.

## 3. Fix the IDs in the CSVs

The CSVs use these IDs. Replace them with the ones you wrote down:

| In the CSV | Means | Replace with |
|---|---|---|
| customer_id **1** | you | your new Customer ID |
| customer_id **2, 3, 4, 5** | the made-up companies | the 4 existing Customer IDs |
| item_id **1, 2, 3** | the 3 new items | the 3 new Item IDs |
| invoice_number **4–20** | the new invoices | only change if the existing invoices are not numbered 1, 2, 3 (e.g. 1001–1003 → use 1004–1020) |

Right-click the CSV → **Open with → Notepad**. Each line is one record:

- `invoices.csv`: `invoice_number, customer_id, invoice_date, days_to_payment, status` → fix the **2nd** number.
- `invoice_rows.csv`: `row_id, invoice_number, item_id, amount` → fix the **3rd** number
  (and the 2nd if invoice numbers changed).

**File → Save** (keep the name and `.csv`). If the IDs already match, skip this step.

## 4. Import

Import **invoices.csv first**, then **invoice_rows.csv**.

1. **File → Import Records → File…** → choose the CSV → Open.
2. The **Import Field Mapping** window opens:
   - **Target** (top right): pick the table — **Invoices** for invoices.csv, **Invoice rows** for invoice_rows.csv.
   - Tick **"Don't import first record (contains field names)"** — the first line is just column headings.
   - Import action: **Add**.
   - Left = columns from the CSV, right = FileMaker fields. Line them up by dragging the fields on the right
     up/down (the ↕ handle). The arrow in the middle must be **→** for columns you import;
     click it to change it to **–** for the ones you skip.

   | invoices.csv | → FileMaker field |
   |---|---|
   | invoice_number | Invoice Number |
   | customer_id | Customer ID |
   | invoice_date | Invoice Date |
   | days_to_payment | Days to payment |
   | status | Status |

   | invoice_rows.csv | → FileMaker field |
   |---|---|
   | row_id | – skip |
   | invoice_number | the invoice number / invoice ID field |
   | item_id | Item ID |
   | amount | Amount |

   Never import into Payment Day, totals or other calculated fields — FileMaker can't, and computes them itself.
3. Click **Import**. In the next box **untick "Perform auto-enter options while importing"** → Import.
4. FileMaker says how many records it added (17 invoices, 29 rows).

## 5. Check it

- Invoices layout, invoice 4: date **9 October 2026**, customer is the right one, item rows visible,
  total **1 997.50 €**. Compare a few more with [all_invoices.md](reports/all_invoices.md).
- Invoice Summary layout → **Show All** → 20 invoices, grand total **15 745.30 €**
  (if your 3 ready-made invoices have other rows, the total will differ — that's fine).

**If something went wrong:** right after an import FileMaker shows only the imported records.
Use **Records → Delete All Records** (it deletes only the records being shown — check the counter says 17 or 29,
not all of them!) and try again.

Common problems:
- *Dates wrong or empty* → the computer uses US date format. Open invoices.csv in Notepad and rewrite dates
  as `10/9/2026` (month/day/year), or type the dates by hand.
- *Invoice rows show no item name or price* → the item_id doesn't match a real Item ID (step 3).
  Or try **Records → Relookup Field Contents** on the Item ID field.
- *Invoices show no customer* → the customer_id doesn't match (step 3).

## 6. Statuses

The CSV already has them: invoices 4–10 **Paid**, 11–15 **Sent**, 16–20 **Open**.
Then continue with the assignment from part 2 (Invoice Summary) onwards.
