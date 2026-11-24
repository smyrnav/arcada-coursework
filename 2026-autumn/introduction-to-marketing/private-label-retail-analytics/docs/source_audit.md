# Source audit

Data collected 24 November 2026. Every record in `data/processed/` carries its source URL
and a data-quality flag.

| Source | URL | API? | What it gave us | Limitations |
|---|---|---|---|---|
| K-Ruoka (Kesko) online catalogue | https://www.k-ruoka.fi/kauppa/tuotehaku/... | Official developer portal exists (k-developer.kesko.fi) but registration/API subscription not completed; data collected from public catalogue listings | Product names, package sizes, listed regular prices, unit prices (€/kg) for Pirkka private-label and Taffel national-brand snacks | Selected Helsinki store not established; prices may be a generic/default store view. Medium data quality. |
| S-kaupat (S Group) online catalogue | https://www.s-kaupat.fi/tuotteet/snacksit/... | No documented public API used; undocumented GraphQL endpoint exists but was deliberately not reverse-engineered | Product names, sizes, listed regular prices and unit prices for Xtra, Coop, Kotimaista private labels and Taffel | Store context not confirmed as Helsinki. Medium data quality. |
| Lidl Finland product pages | https://www.lidl.fi/p/... | No public product-price API identified | Snack Day and Deluxe private-label product listings with package sizes and listed prices | Page captures several weeks old; one price is a promotional aggregator price (FeedMyCart, valid to 25 Nov 2026), not a regular price. Low data quality — flagged accordingly. |
| Wolt (delivery platform) | wolt.com venue menus | No API used; public menu pages | R-kioski filled-bread/sandwich menus for Helsinki Rautatieasema (central) and Vuosaari Kaivonkatsojantie 13 (suburban proxy), with item prices and weights | Delivery-platform menu prices, **not** verified in-store shelf prices; the Vuosaari venue is a neighbourhood proxy, not a verified standalone ground-floor format. |
| FeedMyCart (offer aggregator) | https://feedmycart.nl/fi/countries/finland/lidl/ | No | One Lidl promotional price observation (dated 23 Nov 2026) | Third-party aggregator; promotional, not regular pricing. Used only as a flagged supplementary row. |
| Kesko corporate pages | kesko.fi / Pirkka and K-Menu brand pages | No | Brand architecture evidence: Pirkka family >2,800 products; K-Menu as price-conscious tier; Pirkka Parhaat as premium tier | Marketing material from the retailer itself. |
| S Group brand pages | s-kaupat.fi/tuotemerkit | No | Brand architecture evidence: Coop, Kotimaista, Xtra own-brand portfolio | Retailer's own marketing material. |
| Finnish Competition and Consumer Authority (KKV), research report 3/2025 | kkv.fi | No | Independent confirmation that Lidl Finland's assortment contains 150+ private-label brands; Finnish market context for private labels | Dataset is from 2025, not 2026. |
| Finnish grocery trade regulation (4 c §, own-brand favouring prohibition) | finlex / KKV guidance | No | Legal definition basis: a private label is determined by trademark ownership/control, not merely by shelf presence | Legal text, not market data. |
| McKinsey & Company article | Begley & McOuat (2020), *Turning Private Labels into Powerhouse Brands* | — | Analytical framework (five strategic areas, three-stage maturity model) | Published October 2020; relies on US COVID-era consumer surveys — see `article_analysis.md` for the critical assessment. |

## Sources investigated but not used

- **Kesko Developer API** — official but requires registration and an API subscription; not completed within the assignment timeframe. Documented as a future improvement, not a blocker.
- **Open Food Facts / Open Prices** — available open APIs for product attributes and community price observations; not needed for the current sample size but suitable for extending the dataset.
- **Similarweb / market-research plugin** — suggested during planning, then dropped: website-traffic estimates cannot evidence product-level private-label positioning, and the plugin was unavailable.
- **S-kaupat undocumented GraphQL endpoint** — deliberately not used; no confirmed permission.
