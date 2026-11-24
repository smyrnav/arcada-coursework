# Private-Label Positioning in Finnish Grocery Retail

**Course:** Introduction to Marketing, Arcada UAS — group work 2026, completed individually (Smyrna V.)
**Research question:** How do Finnish grocery retailers (Kesko, S Group, Lidl) position their private-label products against established consumer brands in terms of price, assortment and product differentiation?
**Scope:** Helsinki, Finland — snacks and convenience foods. Digital research only.

## What this is

An individual, digital substitute for the group "mystery shopping" assignment. Instead of
physical store visits, shelf photographs and customer observation, this project uses a
**digital shelf audit**: retailer online catalogues, product listings and delivery-platform
menus, analysed with Python. Physical shelf placement and in-person customer behaviour
were **not** assessed — see `docs/limitations.md`.

The analytical framework is Begley & McOuat (2020), *Turning Private Labels into
Powerhouse Brands*, McKinsey & Company — the article that replaces the Part C
classroom survey for individual completion.

## Structure

```
data/processed/          CSV datasets (grocery products, R-kioski menu, price pairs)
docs/                    source audit, methodology, article analysis, limitations,
                         research source notes
evidence/                screenshot library + evidence_register.csv
                         (real page captures via headless Firefox, 24 Nov 2026)
src/                     analyze.py (stats + charts), build_report.py,
                         build_presentation.py
outputs/charts/          generated figures
report/                  filled assignment report (markdown source + docx build script)
presentation/            presentation.pptx + narration_script.md (Part E)
```

## Reproduce

```bash
python3 -m venv .venv && .venv/bin/pip install pandas matplotlib python-docx
.venv/bin/python src/analyze.py            # summary stats + charts
.venv/bin/python src/build_report.py       # builds report docx
```

## Key preliminary findings

- Private-label salted crisps are 23–33% cheaper per kg than the Taffel benchmark in
  both K-Ruoka and S-kaupat catalogue listings.
- The three retailers use clearly different brand architectures: Kesko's tiered
  Pirkka family, S Group's multi-brand portfolio (Coop / Kotimaista / Xtra), and Lidl's
  broad catalogue of 150+ private labels.
- R-kioski central (Rautatieasema) and suburban-proxy (Vuosaari) Wolt menus list the
  same six filled-bread products at identical prices — no location-based differentiation
  visible in the digital assortment.
