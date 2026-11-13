# Investment Challenge — the leaderboard that updates itself

*For the portfolio competition in **Introduction to Accounting** (2026–2027).*

**Demo version — all students and portfolios here are made up.**

## What is this?

A replacement for the weekly routine of collecting the students' Excel files,
looking up stock prices by hand, calculating everyone's returns, and editing
the standings page.

You keep doing exactly one thing you already do: downloading the submissions
from itslearning. Everything after that — prices, exchange rates, rankings,
the web page — happens by itself.

## What you do each week (about 2 minutes)

1. Download the assignment submissions from itslearning (as usual).
2. Open this repo in your browser → click the **`submissions-xlsx`** folder →
   **Add file → Upload files** → drag the Excel files in → **Commit changes**.
3. Done. Within a minute or two the standings page is updated with current
   prices. No software to install, nothing to run, no computer that needs to
   stay on.

It also runs by itself every Friday evening, so if nobody submits anything
new, the page still refreshes with the week's closing prices.

## What students see

The same standings page as before — same design, same Swedish/English text:
**https://smyrnav.github.io/portfolio-challenge-demo/dashboard.html**

They open the link and type their username to see their rank, return and
portfolio value. (In this demo the link shows made-up students.)

## Questions you might have

**Do I need to know programming or git?**
No. Uploading files through the GitHub website is the only thing you'll ever
do.

**What does it cost?**
Nothing. It runs on GitHub's free tier.

**Where do the prices come from?**
Yahoo Finance's daily closing prices — the same numbers you'd look up
manually, just fetched automatically.

**A student is missing from the list!**
Open the **Actions** tab → the latest run → the log lists every file and
flags ones that couldn't be read (e.g. an empty submission or a broken
file). Fix the file with the student, upload it again, the page updates.

**A student submitted late / changed their picks.**
Just upload the new file the same way. The page updates.

**Are the competition rules the same?**
Yes — €10,000 start, max 5 positions, buy at the closing price on the buy
date, foreign stocks converted at that day's exchange rate, unspent money
stays as cash, ranking within each group, dividends not included.

**Can students see each other's real names?**
The page shows usernames only (like `totterad`), no real names — same as the
current page.

**What if it breaks?**
Nothing is lost — the Excel files and every previous version of the page are
stored in the repo's history. The worst case is you update the page by hand
one week, exactly like today.

## På svenska (kortversion)

Det här ersätter det manuella arbetet med portföljtävlingen. Du laddar ner
inlämningarna från itslearning som vanligt och lägger upp dem i mappen
`submissions-xlsx` här på GitHub (dra och släpp i webbläsaren). Resten —
kurser, valutor, ranking, webbsidan — sköts automatiskt, även varje fredag
utan att någon gör något. Eleverna ser samma sida som tidigare och slår upp
sin placering med sitt användarnamn. Kostar ingenting, kräver ingen
programmering.

---

## How it works (technical — not required reading)

| Step | Who | What happens | Tool | Output |
|---|---|---|---|---|
| 1 | Students | Submit one Excel file with up to 5 picks (ticker, buy date, amount € or shares) | itslearning assignment | `.xlsx` files named by username |
| 2 | Teacher | Upload the files to `submissions-xlsx/` | GitHub web UI | Raw submissions in repo |
| 3 | Automation | Parse Excel files, extract username, group, positions | `ingest.py` | `submissions/<user>.json` |
| 4 | Automation | Fetch closing prices + FX rates | Yahoo Finance via `update.py` | Portfolio values in EUR |
| 5 | Automation | Rank within SV / INT groups, render page | `update.py` + `template.html` | `dashboard.html` |
| 6 | Automation | Publish weekly, on upload, or on demand | GitHub Actions → Pages | Always-current URL |
| 7 | Students | Open link, type username | Browser | Their standing |

Runs weekly (`.github/workflows/update.yml`) plus on every upload and via a
manual "Run workflow" button in the Actions tab.

### Repo layout

```
submissions-xlsx/   student Excel files (what the teacher uploads)
submissions/        generated per-student JSON
ingest.py           Excel -> JSON converter
update.py           price fetching, valuation, ranking, page generation
template.html       page design; data block and date are regenerated
dashboard.html      the published page (output)
```

### Run locally (optional)

```bash
pip install openpyxl
python3 ingest.py submissions-xlsx --dry-run   # preview, writes nothing
python3 ingest.py submissions-xlsx
python3 update.py                              # -> dashboard.html
```

### Notes for whoever adopts this

- Ticker symbols follow Yahoo Finance conventions: `NOKIA.HE` (Helsinki),
  `VOLV-B.ST` (Stockholm), `MC.PA` (Paris), `SAP.DE` (Frankfurt), plain
  symbols for US stocks.
- For the real course, keep submissions in a **private** repo and have the
  Action publish only `dashboard.html` to a separate public repo — the page
  contains usernames only.
- A zero-code alternative exists (Google Sheets with `GOOGLEFINANCE()`), but
  this repo implements the exact competition rules above.
