# Methodology

## Design

Small exploratory **digital shelf audit**, replacing the assignment's physical mystery
shopping. The comparison location is Helsinki; the product focus is snacks and
convenience foods, because those categories appear in both Part A (grocery private
labels) and Part B (R-kioski ready-to-eat range).

## Data collection (24 Nov 2026)

1. **Grocery products (n = 11):** salted potato chips and adjacent snack products from
   K-Ruoka (Kesko), S-kaupat (S Group) and Lidl Finland online catalogues. For each
   record: retailer, product, brand, brand type (private label / national brand),
   package size, listed price, unit price (€/kg), price type (regular vs promotional),
   source URL and a data-quality flag.
2. **Matched price pairs (n = 3):** private-label plain salted crisps matched within
   retailer against a Taffel plain salted benchmark. Taffel is available at both K-Ruoka
   and S-kaupat, making it a usable cross-retailer reference product. Lidl has no Taffel
   listing in the sample, so no Lidl pair was constructed.
3. **R-kioski menus (n = 12 records):** the filled-bread/sandwich section of the Wolt
   menus for one central location (Helsinki Rautatieasema, Scandic Grand Central) and
   one suburban-proxy location (Vuosaari, Kaivonkatsojantie 13): 6 products × 2
   locations, with item price and weight.

## Analysis

All calculations are in `src/analyze.py` and reproducible from the CSVs.

- Unit prices normalised to €/kg (weight-based products only).
- Price gap per pair: `(private_label_unit_price − national_brand_unit_price) / national_brand_unit_price × 100`. Negative = private label cheaper.
- Descriptive statistics only (counts, medians, ranges, matched-pair gaps). The sample
  is far too small for significance testing, and none is attempted.
- R-kioski analysis compares identical menu items across the two locations.

## Brand classification

A product is classed as a private label only when the brand is retailer-owned or
retailer-controlled (Pirkka, K-Menu → Kesko; Coop, Kotimaista, Xtra → S Group;
Snack Day, Deluxe → Lidl), consistent with the Finnish regulatory definition based on
trademark ownership/control — not merely because the retailer stocks it.

## Analytical framework

Findings are interpreted against Begley & McOuat (2020): the five strategic areas
(brand strategy; assortment and pricing; communication, marketing and packaging;
product design and sourcing; organisation and operating model) and the three-stage
private-label maturity model (optimisation of core assortment → portfolio management →
sophisticated private-label ownership). See `docs/article_analysis.md`.

## Methodological substitution 

| Original task (group version) | What was done instead |
|---|---|
| Visit stores, photograph 6 products | Online catalogue records with source URLs; no product photographs |
| Observe physical shelf placement (2.5) | Digital-merchandising observations only (catalogue ordering, listing visibility); physical placement not assessed |
| Visit 2 R-kiosks, observe customers | Wolt menu comparison of 2 locations; customer segments developed as labelled hypotheses |
| Web survey in lecture 25.11 (Part C) | Individual reflection on the McKinsey article, as agreed with the teacher |
| In-class presentation 2.12 (Part E) | Narrated/recorded presentation, as agreed with the teacher |
