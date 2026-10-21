# Section 4: the home in hours. Results (build_housing.py, 2026-10-21; exploratory, not pre-registered)

**Headline, 1976–2020, world hours, hours a year per 1,000 hours of capital (GDP-weighted, 16 JST countries)**

| | total | cash | price | valuation | price ex val. | needed | **net** | **net ex val.** |
|---|---|---|---|---|---|---|---|---|
| Housing | 89.5 | 44.0 | 45.5 | 4.1 | 41.4 | 49.5 | **40.0** | **35.9** |
| GMP (note 3) | 87.6 | 52.8 | 34.8 | 13.4 | 21.4 | 49.5 | **38.0** | **24.7** |

Housing net by period: 45.6 (1976–81), 43.1 (1982–2000), 35.4 (2001–20). GMP: −6.4, 73.3, 17.9.
National hours (each country's nominal GDP per hour worked, LCU), 1976–2020: GDP-weighted net 39.6 (ex valuation 35.5).
Country median 47.5, range 21.5 (Japan) to 63.9 (Norway). Every country is positive. 1951–2020 (revised 2026-10-21 after audit 2; previously 1950–2020 incl. a GDP-per-head hour for 1950): GDP-weighted 35.9, median 40.1.

**Hour return of each claim (net, per 1,000 hours, same 16 countries and years)**: world hours 1976–2020: bills −1.6, government bonds 27.9,
equities 50.4, housing 40.0, GMP 38.0. National-hour median 1951–2020: bills −19.9, bonds −1.9, equities 34.2, housing 40.1 (GDP-weighted: bills −12.1, bonds +0.8, equities 36.1, housing 36.0). Per-country components in table_housing_by_country_national_hours.csv now use the same years for every component (Belgium 1976 had no rent-yield change; its 1976–2020 net is 55.6).

**Robustness (world hours, net / net ex valuation)**: property tax 1 pt: 30.0 / 25.9. Transaction costs of 7.7% round trip cost 8.0 hours a year over a 10-year hold and 4.0 over a 20-year hold. Tax plus 10-year costs: 22.0 / 17.9.
Equal weights: 48.2 / 37.3. Ex-USA: 35.3 / 31.2. World hour on annual-average timing: 41.1.
National hour from JST GDP per head instead of GDP per hour: median 46.8.
Rolling 20-year windows: housing beats the GMP in 13 of 26. Housing net ranges from 26 to 48; GMP net ranges from 14 to 70.

**Identity checks.** housing_tr = capgain + rent_rtn to 3e-8 in every observation. rent_rtn = rent_yd_t × (1+capgain_t), i.e. the rent of year t over the price at the end of t−1, to 1e-9; the one exception is Australia 1950 (0.05).
Total = cash + valuation + price ex valuation exactly, by construction. Price ex valuation differs from implied log rent growth because log(1+cg+rr) − log(1+rr) ≠ log(1+cg): the mean gap is −0.24 pt and the largest is 1.8 pt.
JST `xrusd` is end-of-year: Japan reads 200.5 for 1985 and 159.1 for 1986, which are the year-end rates; the annual averages were about 238 and 168. Dec-to-Dec FX is therefore used.
GDP per hour (World Bank LCU GDP over PWT hours, from 1961; JST GDP over PWT hours for 1951–60) and JST GDP per head: annual growth correlation 0.90, with GDP per hour growing 0.24 pt a year faster on average.

**Surprising or weakening**
1. **Error found in note 3 §7.** JST `gdp` comes in mixed units: millions, billions or trillions of local currency depending on the country. So gdp/xrusd is not a USD weight. Note 3's rent-yield weights put about 0 on Japan, the US, Germany, France, the UK and Italy, and 22% on Spain.
   Note 3 printed rent yields of 5.52 / 4.28 / 2.73% for 1976 / 2000 / 2020. With corrected weights they are 4.61 / 4.47 / 3.72%. Here the weights are fixed with power-of-ten unit factors fitted to World Bank USD GDP; the log10 residual s.d. is ≤0.051.
2. Housing matches the GMP on net, and beats it ex valuation, with far lower measured volatility: annual net s.d. 3.3% against 8.2%, correlation −0.05. Much of that smoothness is in the index (annual-average and appraisal-style prices), not in a house.
3. Rents grew slower than the hour: in national hours, price ex valuation was 37.8 against 46.3 needed. Housing's surplus is the net rent yield, not rising prices. Since 2010 the net rent yield (3.7–4.5%) has been above the GMP cash yield (1.9–3.6%); before 2000 it was well below.
4. GDP weights are dominated by low-return Japan and Germany, so the GDP-weighted net (40) sits below the country median (47.5).

**Extension to 2025 (build_housing_ext.py; OECD analytical house prices chained onto JST 2020).**
How the chaining works: the price is the OECD nominal HPI (annual average). The rent yield is JST's 2020 yield × (rent index ÷ HPI) growth since 2020.
Two gaps were filled: Australia's 2025 rent comes from Q1–Q3, and the US 2025 rent comes from BLS CPI rent (FRED CUUR0000SEHA). After 2020, FX is the BIS December average, which sits within 2.3% of JST's 2020 end-year rate. Weights after 2020 use World Bank USD GDP.
World hours (net / net ex valuation), housing vs GMP: 2021–25: 45.8 / 21.5 vs 5.3 / 15.7. 1976–2025: 40.6 / 34.4 vs 34.8 / 23.8.
Of housing's 2021–25 net, 24 hours a year is valuation, because prices outran CPI rents. National hours 1976–2025: GDP-weighted 40.3, median 47.5.
The rent yield in 2025 is 3.26%, against a GMP cash yield of 3.23%.
Cross-check against OECD, 1976–2020, country medians (`table_crosscheck_jst_vs_oecd.csv`):

| | correlation | gap, JST − OECD (pt/yr) |
|---|---|---|
| Price growth | 0.98 | +0.09 |
| Price–rent change | 0.92 | −0.12 |
| Rent growth | 0.93 | +0.06 |

The outliers are Norway (price corr 0.80, rent gap +1.3), Portugal (price–rent gap +1.8, rent gap +1.1) and Sweden (rent gap −0.75).
OECD rent growth substituted for JST implied rent growth (714 country-years): world net 41.7 / 37.5 for 1976–2020, against 40.0 / 35.9 in the baseline. The national median is 45.8, against 47.5.

**Caveats.** An index is not a house: no selection, depreciation beyond JST's cost deduction, or idiosyncratic risk. Net rent follows JST's definition (after maintenance, depreciation and other costs) and is imputed for owners.
No income, property or transfer taxes in the baseline. The 16 rich countries are survivors. Housing is annual, so years are compared as a whole, while the GMP and world hour are monthly aggregated to calendar years; many national house-price indices are annual averages, so timing is blurred.
No leverage or mortgage cost. For 2021–25, the rent figures are CPI rents on sitting tenants, not new-lease rents, and the world hour after mid-2025 is provisional. JST `capgain` differs from `hpnom` growth in some years (max 0.17), presumably break adjustments.
