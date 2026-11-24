"""Build the Part E presentation (presentation/presentation.pptx).

7 slides: question/method, dataset, own price charts, Finnish research evidence,
European context + McKinsey model, R-kioski finding, conclusions/limitations.
Every image carries a small source caption. No decorative screenshots.
"""
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt

BASE = Path(__file__).resolve().parent.parent
EV = BASE / "evidence" / "screenshots"
CH = BASE / "outputs" / "charts"
OUT = BASE / "presentation" / "presentation.pptx"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]


def add_text(slide, text, left, top, width, height, size=18, bold=False):
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = box.text_frame
    tf.word_wrap = True
    for i, line in enumerate(text.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.font.size = Pt(size)
        p.font.bold = bold and i == 0
    return box


def add_image(slide, path, left, top, width=None, height=None, caption=None):
    kw = {}
    if width:
        kw["width"] = Inches(width)
    if height:
        kw["height"] = Inches(height)
    pic = slide.shapes.add_picture(str(path), Inches(left), Inches(top), **kw)
    if caption:
        add_text(slide, caption, left, top + (height or width * 0.62) + 0.05, width or 6, 0.6, size=10)
    return pic


def slide_title(slide, title, subtitle=None):
    add_text(slide, title, 0.5, 0.25, 12.3, 0.9, size=28, bold=True)
    if subtitle:
        add_text(slide, subtitle, 0.5, 1.05, 12.3, 0.6, size=14)


# 1 — Title / question / method
s = prs.slides.add_slide(BLANK)
slide_title(s, "Private labels in Finnish grocery retail", 
            "Introduction to Marketing 2026 — individual digital research — Smyrna V.")
add_text(s,
         "Research question: how do Kesko, S Group and Lidl position their private labels "
         "against national brands on price, assortment and differentiation?\n"
         "Method: digital shelf audit — online catalogues, product pages and Wolt menus "
         "(Helsinki, 24 Nov 2026). No physical store visits; that limitation is stated openly.\n"
         "Framework: Begley & McOuat (2020), McKinsey — Turning private labels into powerhouse brands.",
         0.5, 1.9, 12.3, 3.5, size=18)

# 2. Dataset
s = prs.slides.add_slide(BLANK)
slide_title(s, "The dataset", "11 grocery products · 3 matched price pairs · 12 R-kioski menu records")
add_text(s,
         "• Snacks/crisps sampled at K-Ruoka, S-kaupat and Lidl (24 Nov 2026)\n"
         "• Private labels matched against a Taffel benchmark where available\n"
         "• R-kioski filled breads: central (Rautatieasema) vs suburban (Vuosaari) Wolt menus\n"
         "• Every record carries source URL, date and a data-quality flag\n"
         "• Lidl rows are low confidence (older page captures; product URLs now dead)",
         0.5, 1.9, 12.3, 4.5, size=18)

# 3 — Own price charts
s = prs.slides.add_slide(BLANK)
slide_title(s, "Private labels are 23–33% cheaper per kg than the Taffel benchmark")
add_image(s, CH / "01_price_pairs.png", 0.5, 1.4, width=6.4,
          caption="Own analysis of catalogue data (data/processed/price_pairs.csv), 24 Nov 2026.")
add_image(s, CH / "04_price_gap_pct.png", 7.1, 1.4, width=5.8,
          caption="Price gap = (PL unit price − Taffel unit price) / Taffel unit price.")

# 4 — Finnish research evidence
s = prs.slides.add_slide(BLANK)
slide_title(s, "Finnish consumers in 2025: cheaper, yes — equal quality, maybe")
add_image(s, EV / "finnish_research/ptt/ptt_2025_private_label_perceptions-18.png", 0.5, 1.3, height=5.6,
          caption="Figure: PTT consumer survey 2025 (N=1,197), Kuva 6. Source: PTT (2025).")
add_image(s, EV / "finnish_research/kkv/kkv_2025_private_label_sales_share-19.png", 7.0, 1.3, height=5.6,
          caption="Figure: KKV Kuvio 1 — PL share of Finnish grocery sales, 2016–2023. Source: KKV (2025).")

# 5 — European context + McKinsey model
s = prs.slides.add_slide(BLANK)
slide_title(s, "Europe moved on — the framework explains how")
add_image(s, EV / "international_research/plma/plma_2026_european_market_share.png", 0.5, 1.3, height=5.6,
          caption="PLMA 2026 (NielsenIQ data): private label 38.8% of 17 European grocery markets in 2025. Finland not separately reported.")
add_image(s, EV / "mckinsey/mckinsey_2020_maturity_model-5.png", 7.0, 1.3, height=5.6,
          caption="McKinsey's three-stage private-label maturity model. Source: Begley & McOuat (2020, p. 5).")

# 6 — R-kioski finding
s = prs.slides.add_slide(BLANK)
slide_title(s, "R-kioski: identical menus, identical prices, central vs suburban")
add_image(s, CH / "03_rkioski_central_vs_suburban.png", 0.5, 1.4, width=7.2,
          caption="Own analysis of Wolt menu data (data/processed/rkioski_menu.csv).")
add_image(s, EV / "retailers/r_kioski/r_kioski_rautatieasema_wolt_menu.png", 8.0, 1.4, height=5.2,
          caption="Wolt venue page, R-kioski Rautatieasema. Source: Wolt (2026).")

# 7 — Conclusions and limitations
s = prs.slides.add_slide(BLANK)
slide_title(s, "What I take from this")
add_text(s,
         "• Three genuinely different strategies: Kesko's tiered Pirkka family, S Group's three-brand\n"
         "  portfolio in one category, Lidl's own-label-dominated assortment (150+ PL brands, KKV 2025)\n"
         "• A price gap gets a product tried; it does not create loyalty (McKinsey 2020)\n"
         "• R-kioski standardises its delivered convenience range across locations\n\n"
         "Limitations: no physical shelf or customer observation; Helsinki store prices not verified;\n"
         "Lidl sample weak; small exploratory sample — no market-wide claims.",
         0.5, 1.6, 12.3, 5.2, size=18)

prs.save(OUT)
print("saved", OUT)
