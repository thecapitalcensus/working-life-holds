# Independent check of note 4, sections 4–6 (2026-10-21)

Scripts: check_housing.py, check_housing_ext.py, check_national_payg.py, check_balance.py (this folder). Own FX for 2021–25: FRED monthly averages, December (check/fx/). I wrote these before reading build_housing*.py and build_balance.py, then read the builders' code only to explain the gaps.

## Claim vs check

| item | claim | check | verdict |
|---|---|---|---|
| Housing 1976–2020, total / net / net ex val (world hours, per 1,000 h) | 89.5 / 40.0 / 35.9 | 89.2 / 39.7 / 36.3 (start-of-year WB USD GDP weights, portfolio aggregation) | confirmed |
| Housing cash / valuation / needed | 44.0 / 4.1 / 49.5 | 44.0 / 3.3 (portfolio yield) or 4.1 (weighted mean of country logs) / 49.5 | explained (see 1) |
| GMP 1976–2020 total / net | 87.6 / 38.0 | 87.6 / 38.0 | confirmed (cash and valuation not rechecked: sleeve file) |
| Housing 2021–25 net / ex val | 45.8 / 21.5 | 46.3 / 20.8 | confirmed (different FX source) |
| Housing 1976–2025 | 40.6 / 34.4 | 40.3 / 34.8 | confirmed |
| GMP 1976–2025 net; needed | 34.8; 48.2 | 34.8; 48.2 | confirmed |
| Rent yield in 2025 | 3.26% | 3.26% | confirmed |
| Note 3 §7 rent yields as printed (gdp/xrusd weights) | 5.52 / 4.28 / 2.73 | 5.52 / 4.28 / 2.73. JPN weight 0.000, USA 0.003, ESP 0.17–0.23 | error in note 3 confirmed |
| Corrected rent yields | 4.61 / 4.47 / 3.72 | 4.58 / 4.45 / 3.75 (WB USD weights) | confirmed |
| PAYG, all countries 1951–2023 / 1976–2020 | 8.2 / 6.6 | 8.22 / 6.65 (prior-year USD GDP, 1960 weights before 1961) | confirmed |
| PAYG: JST 16; DEU, JPN, FRA, USA | 4.4; −2.9, −2.2, −0.4, 11.1 | 4.44; −2.9, −2.2, −0.4, 11.1 | confirmed |
| OECD 2023 shares (GDP-weighted): dwellings and land, F6, F5, F2 and F3, liabilities | 41.6 / 16.0 / 23.3 / 14.2 / 11.7 | 41.6 / 16.0 / 23.3 / 14.2 / 11.7 (43.2 / 16.6 / 24.3 / 14.7 / 12.2 without other non-financial assets) | explained (see 2) |
| US Z.1 NW/GDP 1952 → 2026 | 3.6 → 6.1 | 3.64 → 6.08 | confirmed |
| Eurostat S13PS 2021: % of GDP median, min, max | 272 (DNK 2, ESP 452) | 271.6 (2.2, 451.8) | confirmed |
| S13PS as % of net worth (median, n=24) | 78 | 78.1 (82.7 with the narrower net worth) | explained (see 2) |
| National-hours net, USA / JPN / DEU | 49.9 / 21.5 / 27.6 | 49.9 / 21.5 / 27.6 (net ex val 45.6 / 28.2 / 26.6 also matches) | confirmed |

## Explanations
1. **Valuation.** The builders aggregate total and cash as portfolio simple returns, but valuation as the GDP-weighted mean of each country's −Δlog yield. Valuation measured as the change in the portfolio's own yield gives 3.3 rather than 4.1. The 0.8 gap sits inside "price ex valuation", and net ex valuation moves only by 0.4. This is a defensible choice, but the text should state the method.
2. **Gross assets.** The builders include other non-financial assets (non-dwelling produced assets and other land) in gross assets. With the same definition, every share matches.

## Conceptual review: no errors found
- No double counting: housing_tr = capgain + rent_rtn, and rent_rtn = yd_t·(1+cg_t), i.e. the rent over the start-of-year price (identity holds to 7e-9).
- Sign of valuation is right: a falling yield gives a positive valuation.
- Timing is consistent: weights are start-of-year (same-year weights would give net 42.7), FX is Dec-to-Dec end-year (xrusd), and the world hour runs Dec-to-Dec. National hours use calendar-year GDP per hour, a half-year offset. That is covered by the robustness rows.

## Caveats to state in the text (not blocking)
- (a) "Dwellings + land" uses all household land (N211N), not only land under dwellings. Do not call it "the home".
- (b) PAYG (hours growth) is a national-hour return. Setting it beside world-hour housing (6.6 vs 40.0) is valid only in aggregate, where world GDP growth minus world-hour growth equals world hours growth. Even there, the country sets differ (79 vs 44 countries). The cleaner comparison is the national-hours one (5.1 vs 35.5).
- (c) "Hours fell in Italy" is wrong: ITA 1976–2020 is −0.01, i.e. flat. Say "fell in Germany and Japan, flat in Italy and France".
- (d) PAYG return = hours growth holds only if wages per hour track GDP per hour (constant labour share).

**Nothing has to be fixed before writing except caveat (c).**
