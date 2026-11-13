#!/usr/bin/env python3
"""Convert a folder of Excel submissions (itslearning bulk download) into
submissions/*.json for update.py.

Usage:
    python3 ingest.py /path/to/downloaded/excels [--grp SV|INT] [--dry-run]

Username is taken from the file name (itslearning names downloads by student
username, e.g. "totterad_portfolio.xlsx") or from a user/username cell inside
the file. Group comes from a grupp/group cell in the file, else from --grp
(default SV). Position columns are matched by header names; without headers,
rows containing a ticker-looking string, a date and a number are picked up.
Both "amount in EUR" and "number of shares" styles are accepted.
"""
import argparse
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

from openpyxl import load_workbook

TICKER_KEYS = {"ticker", "symbol", "aktie", "stock", "bolag", "company",
               "värdepapper", "vardepapper", "instrument", "namn", "name"}
DATE_KEYS = {"date", "datum", "köpdatum", "kopdatum", "buy date", "buy",
             "inköpsdatum", "inkopsdatum", "purchase date", "purchase"}
AMOUNT_KEYS = {"amount", "belopp", "summa", "investerat", "invested", "eur",
               "€", "euro", "euros", "kapital", "amount (€)", "belopp (€)"}
SHARES_KEYS = {"shares", "antal", "st", "qty", "quantity", "antal aktier"}
GROUP_KEYS = {"grupp", "group", "grp"}
USER_KEYS = {"user", "username", "användarnamn", "anvandarnamn", "användare"}

USERNAME_RE = re.compile(r"^[a-z]{6,10}$")
TICKER_RE = re.compile(r"^[A-Za-z]{1,6}([.-][A-Za-z0-9]{1,5}){0,2}$")
DATE_RE = re.compile(r"^(\d{4})-(\d{1,2})-(\d{1,2})$|^(\d{1,2})[./](\d{1,2})[./](\d{4})$")


def norm(v):
    return str(v).strip().lower() if v is not None else ""


def parse_date(v):
    if isinstance(v, datetime):
        return str(v.date())
    if isinstance(v, date):
        return str(v)
    s = str(v).strip()
    m = DATE_RE.match(s)
    if not m:
        return None
    if m.group(1):
        y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
    else:
        d, mo, y = int(m.group(4)), int(m.group(5)), int(m.group(6))
    try:
        return str(date(y, mo, d))
    except ValueError:
        return None


def looks_like_ticker(v):
    if not isinstance(v, str):
        return False
    s = v.strip()
    return 1 < len(s) <= 12 and " " not in s and bool(TICKER_RE.match(s)) \
        and any(c.isalpha() for c in s)


def username_from_filename(stem):
    tokens = re.split(r"[_\-\s.()]+", stem.lower())
    hits = [t for t in tokens if USERNAME_RE.match(t)]
    return hits[0] if hits else None


def read_cells(ws):
    for row in ws.iter_rows(values_only=True):
        yield [c for c in row]


def extract_positions(rows):
    """Return (positions, info) from raw rows of cell values."""
    # Pass 1: header-driven.
    for i, row in enumerate(rows):
        keys = {j: norm(c) for j, c in enumerate(row)}
        col = {}
        for j, k in keys.items():
            if k in TICKER_KEYS:
                col.setdefault("ticker", j)
            elif k in DATE_KEYS:
                col.setdefault("date", j)
            elif k in AMOUNT_KEYS:
                col.setdefault("amount", j)
            elif k in SHARES_KEYS:
                col.setdefault("shares", j)
        if "ticker" in col and "date" in col and ("amount" in col or "shares" in col):
            positions = []
            for r in rows[i + 1:]:
                ticker = r[col["ticker"]] if col["ticker"] < len(r) else None
                if not looks_like_ticker(ticker):
                    if positions:
                        break
                    continue
                d = parse_date(r[col["date"]]) if col["date"] < len(r) else None
                pos = {"ticker": ticker.strip().upper() if "." not in ticker else ticker.strip(), "date": d}
                ok = False
                if "amount" in col and col["amount"] < len(r) and isinstance(r[col["amount"]], (int, float)):
                    pos["amount"] = float(r[col["amount"]])
                    ok = True
                if "shares" in col and col["shares"] < len(r) and isinstance(r[col["shares"]], (int, float)):
                    pos["shares"] = float(r[col["shares"]])
                    ok = True
                if d and ok:
                    positions.append(pos)
            if positions:
                return positions[:5], "header"
    # Pass 2: heuristic row scan.
    positions = []
    for row in rows:
        ticker = next((c for c in row if looks_like_ticker(c)), None)
        d = next((parse_date(c) for c in row if parse_date(c)), None)
        num = next((float(c) for c in row if isinstance(c, (int, float)) and c > 0), None)
        if ticker and d and num:
            positions.append({"ticker": ticker.strip(), "date": d, "amount": num})
    return positions[:5], "heuristic" if positions else "none"


def find_meta(rows, keys):
    for row in rows:
        for j, c in enumerate(row):
            if norm(c) in keys and j + 1 < len(row) and row[j + 1] is not None:
                return str(row[j + 1]).strip()
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder", type=Path, help="folder with .xlsx submissions")
    ap.add_argument("--grp", default="SV", choices=["SV", "INT"],
                    help="default group if the file does not say (default: SV)")
    ap.add_argument("--out", type=Path, default=Path(__file__).resolve().parent / "submissions")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    files = sorted(p for p in args.folder.iterdir()
                   if p.suffix.lower() in (".xlsx", ".xlsm") and not p.name.startswith("~$"))
    if not files:
        sys.exit(f"no .xlsx files in {args.folder}")
    args.out.mkdir(parents=True, exist_ok=True)

    problems = 0
    for f in files:
        try:
            wb = load_workbook(f, read_only=True, data_only=True)
            rows = [r for ws in wb.worksheets for r in read_cells(ws)]
        except Exception as e:
            print(f"!! {f.name}: unreadable ({e})")
            problems += 1
            continue
        user = username_from_filename(f.stem) or find_meta(rows, USER_KEYS)
        if not user:
            print(f"!! {f.name}: could not determine username, skipped")
            problems += 1
            continue
        grp = (find_meta(rows, GROUP_KEYS) or args.grp).upper()
        grp = grp if grp in ("SV", "INT") else args.grp
        positions, how = extract_positions(rows)
        sub = {"user": user, "grp": grp, "positions": positions}
        total = sum(p.get("amount", 0) for p in positions)
        flag = ""
        if not positions:
            flag = "  <- no positions found"
        elif total > 10000:
            flag = f"  <- WARNING: total {total:.0f} € exceeds 10000 €"
            problems += 1
        print(f"{f.name} -> {user} ({grp}), {len(positions)} positions [{how}]{flag}")
        if not args.dry_run:
            (args.out / f"{user}.json").write_text(
                json.dumps(sub, ensure_ascii=False, indent=1) + "\n")
    if problems:
        print(f"\n{problems} file(s) need a manual look")
    print("dry run, nothing written" if args.dry_run else f"written to {args.out}")


if __name__ == "__main__":
    main()
