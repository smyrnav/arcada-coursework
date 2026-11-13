#!/usr/bin/env python3
"""Rebuild dashboard.html from submissions/*.json with live prices.

Each submission file is named <username>.json:
  {"user": "virtanem", "grp": "SV",
   "positions": [{"ticker": "NOKIA.HE", "date": "2026-10-06", "amount": 4000}]}

Rules (same as the course): EUR 10,000 start, up to 5 positions, buy at the
closing price on the buy date (or the next trading day), foreign shares are
converted to EUR at that day's rate, unspent money stays as cash, ranking is
within each group. Price return only, no dividends.

Prices come from Yahoo Finance's public chart API, no key needed.
Run manually or from cron; output is a fully static dashboard.html.
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SUBMISSIONS = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "submissions"
TEMPLATE = ROOT / "template.html"
OUTPUT = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "dashboard.html"
CACHE = ROOT / ".price_cache.json"
START_CAPITAL = 10000.0
SV_MONTHS = ["jan", "feb", "mar", "apr", "maj", "jun",
             "jul", "aug", "sep", "okt", "nov", "dec"]


def fetch_daily(symbol, start):
    """Return (currency, [(date, close), ...]) from Yahoo Finance."""
    p1 = int(datetime.combine(start - timedelta(days=10), datetime.min.time()).timestamp())
    p2 = int(time.time()) + 86400
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/"
           f"{urllib.parse.quote(symbol)}?period1={p1}&period2={p2}&interval=1d")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                payload = json.load(r)
            break
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2)
    result = payload["chart"]["result"][0]
    meta = result["meta"]
    offset = meta.get("gmtoffset", 0)
    closes = result["indicators"]["quote"][0]["close"]
    series = []
    for ts, close in zip(result.get("timestamp", []), closes):
        if close is None:
            continue
        d = datetime.fromtimestamp(ts + offset, timezone.utc).date()
        series.append((str(d), close))
    if not series:
        raise RuntimeError(f"no price data for {symbol}")
    return meta.get("currency", "EUR"), series


def get_series(symbol, start, cache):
    """Fetch with a same-day disk cache so re-runs are instant."""
    today = str(date.today())
    entry = cache.get(symbol)
    if entry and entry["fetched"] == today and entry["start"] <= str(start):
        return entry["currency"], [(d, c) for d, c in entry["series"]]
    currency, series = fetch_daily(symbol, start)
    time.sleep(0.15)
    cache[symbol] = {"fetched": today, "start": str(start),
                     "currency": currency, "series": series}
    return currency, series


def close_on_or_after(series, d):
    for date_str, close in series:
        if date_str >= d:
            return date_str, close
    raise RuntimeError(f"no close on or after {d}")


def main():
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    subs = []
    for f in sorted(SUBMISSIONS.glob("*.json")):
        sub = json.loads(f.read_text())
        sub.setdefault("user", f.stem)
        subs.append(sub)
    if not subs:
        sys.exit("no submissions found")

    students = []
    latest_price_date = ""
    errors = []
    for sub in subs:
        user, grp = sub["user"], sub.get("grp", "SV")
        positions = sub.get("positions", [])
        if not positions:
            students.append({"user": user, "grp": grp, "ret": None, "value": None,
                             "pnl": None, "rank": None,
                             "note": "Inga positioner inlämnade"})
            continue
        try:
            spent = 0.0
            holdings_value = 0.0
            for pos in positions[:5]:
                ticker, buy_date = pos["ticker"], pos["date"]
                currency, series = get_series(ticker, date.fromisoformat(buy_date), cache)
                actual_buy_date, buy_price = close_on_or_after(series, buy_date)
                latest_date, latest_price = series[-1]
                latest_price_date = max(latest_price_date, latest_date)
                if currency == "EUR":
                    fx_buy = fx_now = 1.0
                else:
                    _, fx_series = get_series(f"EUR{currency}=X",
                                              date.fromisoformat(buy_date), cache)
                    _, fx_buy = close_on_or_after(fx_series, actual_buy_date)
                    fx_now = fx_series[-1][1]
                    latest_price_date = max(latest_price_date, fx_series[-1][0])
                if "amount" in pos:
                    amount = float(pos["amount"])
                    shares = amount * fx_buy / buy_price
                else:
                    shares = float(pos["shares"])
                    amount = shares * buy_price / fx_buy
                holdings_value += shares * latest_price / fx_now
                spent += amount
            cash = START_CAPITAL - spent
            value = cash + holdings_value
            students.append({"user": user, "grp": grp, "ret": value / START_CAPITAL - 1,
                             "value": round(value, 2), "pnl": round(value - START_CAPITAL, 2),
                             "rank": None, "note": ""})
        except Exception as e:
            errors.append(f"{user}: {e}")
            students.append({"user": user, "grp": grp, "ret": None, "value": None,
                             "pnl": None, "rank": None,
                             "note": f"Kunde inte värderas: {e}"})

    CACHE.write_text(json.dumps(cache))

    for grp in ("SV", "INT"):
        ranked = sorted((s for s in students if s["grp"] == grp and s["ret"] is not None),
                        key=lambda s: s["ret"], reverse=True)
        for i, s in enumerate(ranked, 1):
            s["rank"] = i

    d = date.fromisoformat(latest_price_date) if latest_price_date else date.today()
    sv_date = f"{d.day} {SV_MONTHS[d.month - 1]} {d.year}"

    html = TEMPLATE.read_text()
    html, n = re.subn(r"const DATA=.*?\};",
                      lambda _: "const DATA=" + json.dumps({"students": students}) + ";",
                      html, count=1, flags=re.S)
    if n != 1:
        sys.exit("could not find DATA block in template.html")
    html = re.sub(r"stängningskurser \d{1,2} \w+ \d{4}", f"stängningskurser {sv_date}", html)
    html = re.sub(r"Closing prices \d{1,2} \w+ \d{4}", f"Closing prices {sv_date}", html)
    OUTPUT.write_text(html)

    for grp in ("SV", "INT"):
        ranked = sorted((s for s in students if s["grp"] == grp and s["rank"]),
                        key=lambda s: s["rank"])
        print(f"\n{grp}: {len(ranked)} ranked")
        for s in ranked:
            print(f"  #{s['rank']:<2} {s['user']:<10} {s['ret']*100:+.2f}%  {s['value']:.2f} €")
    if errors:
        print("\nERRORS:", file=sys.stderr)
        for e in errors:
            print("  " + e, file=sys.stderr)
    print(f"\n-> {OUTPUT} (prices as of {sv_date})")


if __name__ == "__main__":
    main()
