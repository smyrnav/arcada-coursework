"""Analysis for the private-label retail analytics project.

Reads the three processed CSVs collected during the digital shelf audit
(24 Nov 2026) and produces summary statistics plus charts in outputs/charts/.

All data is preliminary catalogue/aggregator data; Helsinki store-level
validation is pending (see docs/limitations.md).
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data" / "processed"
OUT = BASE / "outputs" / "charts"
OUT.mkdir(parents=True, exist_ok=True)

PL_COLOR = "#2e7d32"   # private label
NB_COLOR = "#c62828"   # national brand


def load():
    products = pd.read_csv(DATA / "grocery_products.csv")
    pairs = pd.read_csv(DATA / "price_pairs.csv")
    kiosk = pd.read_csv(DATA / "rkioski_menu.csv")
    return products, pairs, kiosk


def chart_price_pairs(pairs: pd.DataFrame):
    """Chart 1: matched private-label vs national-brand unit prices."""
    labels = [f"{r.retailer.split(' /')[0]}\n{r.private_label_product.split(' ')[0]} vs Taffel"
              for r in pairs.itertuples()]
    x = range(len(pairs))
    fig, ax = plt.subplots(figsize=(8, 5))
    w = 0.38
    ax.bar([i - w / 2 for i in x], pairs["private_label_unit_price_eur_per_kg"],
           width=w, color=PL_COLOR, label="Private label")
    ax.bar([i + w / 2 for i in x], pairs["national_brand_unit_price_eur_per_kg"],
           width=w, color=NB_COLOR, label="National brand (Taffel)")
    for i, gap in zip(x, pairs["price_gap_pct"]):
        ax.annotate(f"{gap:.0f}%", (i, max(
            pairs["private_label_unit_price_eur_per_kg"][i],
            pairs["national_brand_unit_price_eur_per_kg"][i]) + 0.3),
            ha="center", fontsize=10, fontweight="bold")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel("Unit price (EUR/kg)")
    ax.set_ylim(0, pairs["national_brand_unit_price_eur_per_kg"].max() + 2.5)
    ax.set_title("Private-label vs national-brand unit prices, salted potato chips\n"
                 "(online catalogue listings, 24 Nov 2026; Helsinki store not confirmed)")
    ax.legend(loc="center left", bbox_to_anchor=(1.01, 0.5))
    fig.tight_layout()
    fig.savefig(OUT / "01_price_pairs.png", dpi=150)
    plt.close(fig)


def chart_unit_prices(products: pd.DataFrame):
    """Chart 2: unit price of sampled products — regular listed prices only."""
    df = products[products["price_type"] == "listed_regular_price"].copy()
    df = df.sort_values("unit_price_eur_per_kg")
    colors = [PL_COLOR if t == "private_label" else NB_COLOR for t in df["brand_type"]]
    labels = [f"{r.brand} — {r.product_name[:38]}" for r in df.itertuples()]
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.barh(labels, df["unit_price_eur_per_kg"], color=colors)
    ax.set_xlabel("Unit price (EUR/kg; milk products EUR/l)")
    ax.set_title("Sampled products by unit price — regular listed prices\n"
                 "Green = private label, red = national brand (24 Nov 2026)")
    for i, v in enumerate(df["unit_price_eur_per_kg"]):
        ax.text(v + 0.15, i, f"{v:.2f}", va="center", fontsize=8)
    ax.set_xlim(0, df["unit_price_eur_per_kg"].max() + 4)
    fig.tight_layout()
    fig.savefig(OUT / "02_unit_prices_by_product.png", dpi=150)
    plt.close(fig)


def chart_rkioski(kiosk: pd.DataFrame):
    """Chart 3: R-kioski central vs suburban Wolt menu prices (identical items)."""
    central = kiosk[kiosk["location_type"] == "central"].set_index("product_name")
    suburb = kiosk[kiosk["location_type"] != "central"].set_index("product_name")
    joined = central.join(suburb, suffixes=("_central", "_suburb"))
    labels = [n[:34] for n in joined.index]
    x = range(len(joined))
    w = 0.38
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar([i - w / 2 for i in x], joined["listed_price_eur_central"], width=w,
           label="Central (Rautatieasema)")
    ax.bar([i + w / 2 for i in x], joined["listed_price_eur_suburb"], width=w,
           label="Suburban proxy (Vuosaari)")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, rotation=20, ha="right", fontsize=8)
    ax.set_ylabel("Listed price (EUR/item)")
    ax.set_title("R-kioski filled-bread menu: central vs suburban Wolt listings\n"
                 "(delivery-platform prices, not in-store shelf prices)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "03_rkioski_central_vs_suburban.png", dpi=150)
    plt.close(fig)


def chart_price_gap(pairs: pd.DataFrame):
    """Chart 4: private-label price gap (%) vs the Taffel benchmark."""
    labels = [f"{r.retailer.split(' /')[0]}\n{r.private_label_product.split(' ')[0]}"
              for r in pairs.itertuples()]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    bars = ax.bar(labels, pairs["price_gap_pct"], color=PL_COLOR)
    ax.axhline(0, color="black", linewidth=0.8)
    for b, v in zip(bars, pairs["price_gap_pct"]):
        ax.text(b.get_x() + b.get_width() / 2, v - 1.5, f"{v:.1f}%",
                ha="center", va="top", fontsize=10, fontweight="bold")
    ax.set_ylabel("Price gap vs Taffel benchmark (%)")
    ax.set_title("Private-label unit-price gap vs national brand\n(negative = private label cheaper per kg)")
    fig.tight_layout()
    fig.savefig(OUT / "04_price_gap_pct.png", dpi=150)
    plt.close(fig)


def summarise(products: pd.DataFrame, pairs: pd.DataFrame, kiosk: pd.DataFrame):
    print("== Sample ==")
    print(f"grocery product records: {len(products)}")
    print(products.groupby(["retailer", "brand_type"]).size().to_string())
    print(f"\nmatched price pairs: {len(pairs)}")
    print(f"R-kioski menu records: {len(kiosk)} "
          f"({kiosk['location_name'].nunique()} locations, "
          f"{kiosk['product_name'].nunique()} distinct products)")
    print("\n== Price gaps vs Taffel benchmark ==")
    print(pairs[["retailer", "private_label_product", "price_gap_pct"]].to_string(index=False))
    pl = products[products["brand_type"] == "private_label"]["unit_price_eur_per_kg"]
    print(f"\nprivate-label unit price: median {pl.median():.2f} EUR/kg "
          f"(range {pl.min():.2f}–{pl.max():.2f})")
    c = kiosk[kiosk["location_type"] == "central"]["listed_price_eur"]
    print(f"R-kioski filled breads: {c.min():.2f}–{c.max():.2f} EUR/item, "
          f"identical at both sampled locations")


def main():
    products, pairs, kiosk = load()
    summarise(products, pairs, kiosk)
    chart_price_pairs(pairs)
    chart_unit_prices(products)
    chart_rkioski(kiosk)
    chart_price_gap(pairs)
    print(f"\ncharts written to {OUT}")


if __name__ == "__main__":
    main()
