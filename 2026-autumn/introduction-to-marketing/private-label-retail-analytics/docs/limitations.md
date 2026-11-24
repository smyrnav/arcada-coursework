# Limitations

Listed explicitly so that nothing in the report overstates the evidence.

## Method substitution

- **No physical store visits.** Shelf placement, in-store merchandising, product
  photographs and customer observation — all required by the original group template —
  were **not assessed**. Sections 2.5 and 3.3 of the report state this openly instead of
  substituting invented observations.
- The teacher approved individual completion, the article reflection as a Part C
  substitute, and a recorded presentation. She has **not explicitly confirmed** that
  digital research may replace the physical observations; the report discloses the
  substitution rather than assuming approval.

## Data limitations

- **Helsinki store confirmation pending.** K-Ruoka and S-kaupat catalogue prices were
  captured without a verified selected Helsinki store; Finnish grocery prices can vary
  by store. Records carry `location_confidence` flags. One intermediate search result
  pointed to a store in Espoo; affected rows were excluded or flagged.
- **Lidl data is the weakest.** Two of three Lidl rows come from page captures several
  weeks old, and one is a *promotional* aggregator price (FeedMyCart, valid to 25 Nov
  2026) — it is excluded from regular-price comparisons and kept only as a flagged row.
  Lidl therefore has **no matched price pair**; claims about Lidl rest on assortment and
  brand-architecture evidence (including KKV 3/2025), not on our price data.
- **Promotional vs regular prices** are never mixed: every record has a `price_type`
  field and only `listed_regular_price` rows enter the price-pair analysis.
- **Small, unbalanced sample.** 11 grocery records, 3 matched pairs, 1 snack category
  (plus R-kioski filled breads). This supports illustration of positioning differences,
  **not** statistical generalisation about the Finnish grocery market, market shares,
  sales volumes or consumer preferences.
- **Wolt menu prices are delivery-platform prices**, which can differ from in-store
  shelf prices at R-kioski. The Vuosaari location is a neighbourhood proxy; a standalone
  ground-floor suburban format (as the template specifies) was not verified.
- **Package sizes differ** within matched pairs (e.g. 275 g Pirkka vs 250 g Taffel);
  comparisons are made on unit price (€/kg) to compensate, but products are "reasonable
  category matches", not identical SKUs.

## Interpretation limits

- A lower private-label price does **not** imply customers prefer it; no consumer
  behaviour was measured anywhere in this project.
- Product counts and catalogue presence do not indicate sales, demand or loyalty.
- The McKinsey article's 2020 US survey figures are used as framework, not as evidence
  about Finnish consumers in 2026.

## What would strengthen the study

1. Completing Kesko Developer API registration for authoritative, store-specific prices.
2. Verifying one Helsinki store per chain and re-pulling all prices against it.
3. Extending Open Prices / Open Food Facts lookups for dated, barcode-matched prices.
4. A short real shelf visit to validate (or falsify) the digital-merchandising findings.
