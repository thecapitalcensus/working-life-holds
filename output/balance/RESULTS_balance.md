# Sections 5–6: the household balance sheet and the pension in hours. Results (build_balance.py, 2026-10-21; exploratory, not pre-registered)

**5a Composition, 2023** (latest year with ≥90% of the maximum country count; 31 countries; OECD T720 + Table 9B, S1M = households + NPISH for both, so the two sides match; net worth = gross assets − total liabilities).
Shares of gross assets, USD-GDP-weighted (median): dwellings + land 41.6 (48.3), F6 pension & insurance 16.0 (8.1), F5 equity & fund shares 23.3 (15.6), F2+F3 deposits & debt securities 14.2 (15.5), other 4.9 (5.5). Liabilities 11.7 (13.0)% of gross assets.
F5 split (GDP-w.): listed 8.7, unlisted 1.8, other equity 5.6, funds 6.3. The range is wide: dwellings + land run from 66 (ESP) to 24–28 (ROU, DNK); Japan holds 34% in deposits; US, Sweden and Denmark hold about 30% in F5.
Land is not reported for GRC, CHL, ISR and ROU (marked *); their housing share is understated. CHE, NOR, IRL, NZL, TUR, BRA, COL, IND and ISL have financial accounts but no dwellings, and Australia has the reverse. All are excluded.

**5b Net worth per person employed.** Measured in national hours, the net worth per worker ÷ average annual hours is exactly net worth / GDP (check: 2e-15). So "years of own work" is the wealth-to-GDP ratio.
2023 median: 3.6 years, or 5,850 hours. US 6.0, FRA 5.4, JPN 5.1, DEU 4.6, GBR 4.0. Balanced 26-country panel (GDP-w.): 3.5 years (1995) → 6.0 (2021) → 5.35 (2023).
In world hours (USD at the December BIS rate ÷ world hour H): median 17,100 hours per worker. US 52,400; JPN 17,000, down from 28,000 in 2007 because of the yen, while its national-hour measure rose.

**5c US 1952–2026Q2 (Z.1 B.101).** Real estate 23→25%, pension entitlements 9→16% (peak 24% in 2013), equities + mutual funds 13→31%, deposits + MMF + debt securities 13→12%, other 42→16%. Most of "other" is private business, which falls from 23% to 8%.
Liabilities rise from 7% to 10% of assets (19% in 2008). Net worth per worker goes from 3.6 to 6.1 years of US work (+0.69%/yr). In US hours it goes from 7,500 to 10,900 hours: annual hours per worker fell from 2,060 to 1,789, so growth to 2023 is only +0.41%/yr. In world hours: 45,000 (1970) → 54,500.
PWT ends in 2023. For 2024–26, total hours are extended with BLS nonfarm-business hours (on disk) and annual hours per worker are held at 2023. The years measure needs only GDP (FRED quarterly; 2026 uses H1).

**5d PAYG (Eurostat Table 29, S13PS, 2021).** The median across 30 countries is 270% of GDP (Eurostat's own GDP; 272 with World Bank GDP) (range DNK 2% to ESP 452%). Funded entitlements (S1PF) have a median of 11% of GDP.
Where household net worth exists (24 countries), PAYG entitlements are a median 78% of net worth (BEL 44, DEU 59, FRA 58, ITA 73, ESP 73, FIN 106, POL 161, ROU 300). Adding them lifts the median from 3.5 to 6.5 years of GDP, so the standard balance sheet leaves out nearly half of the household's claims in most of Europe.

**6f Implicit PAYG return = growth of total hours worked** (PWT 11, emp × avh). GDP-weighted, per 1,000 hours a year: 1951–2023 8.2 (employment 12.2; hours per worker −3.4 — employment minus total hours is 4.0 because the country samples differ by year). By decade: 10.0, 9.3, 9.2, 11.2, 5.6, 3.8, then 2.2 for 2011–20 and 28.8 for 2021–23 (2020 fall and rebound); 8.4 over 2011–23.
1976–2020: all countries 6.6, the 16 JST countries 4.4, median of the 13 synthesis countries 1.1. JPN −2.2, DEU −2.9 and FRA −0.4, against USA 11.1.
Population 20–64 (UN WPP, **projection**, 2023 GDP weights): +1.2 (2024–30), −0.6, −4.0, −5.6 (2051–60). The world headcount is still +5.0 over 2024–60.
Side by side, 1976–2020: PAYG 6.6 against housing 40.0, GMP 38.0, government bonds 27.9 and bills −1.6 (world hours, section 4). Over 1951–2020 in national hours (JST 16, GDP-w.): PAYG 5.1, housing 36.0, bonds +0.8, bills −12.1 (revised after audit 2: window now 1951–2020).

**5e Synthesis (a weighted average of index returns, not a measured household return).** 2023 shares × section-4 country hour returns for 1976–2020 (national hours). Mapping:
- dwellings + land → JST housing
- F5 → equities
- F2 → bills
- F3 → government bonds
- F6 → 0.6 equities + 0.4 bonds
- other → bills
- liabilities → bills + 10

Results over 13 countries, per 1,000 hours of net worth: median 35.5, GDP-weighted 41.3 (US 50.8), range JPN 13.8 to SWE 68.9. Housing alone: median 39.9.
This sits at the GMP's 3.5%/yr in world hours (35; 38.0 over 1976–2020), but the units differ (national hours here, world hours there). Robustness medians: average shares 36.4, other at zero 35.6, liabilities at bills 36.9.
Adding PAYG at hours growth (10 European countries) lowers the median from 42.2 to 23.8 (DEU 25.9→15.2, FIN 53.2→25.2).

**Checks.** Shares sum to 100 (max error 3e-14). Z.1 net worth = assets − liabilities to $0.001bn, and assets = non-financial + financial exactly. BF90 = financial assets − liabilities to 1e-4. PWT emp × avh = hours. FRED vs World Bank US GDP agree to 0.07%. OECD US net worth is 1.072 × Z.1 (2023). Eurostat S1P % of GDP recomputed with World Bank GDP: median gap 0.3 pt.

**Weakens the story / caveats.**
1. PAYG is the weakest claim in hours and is turning negative. In Germany, Japan and Italy hours already fell over 1976–2020; the dependency projection is a projection, not data.
2. The synthesis is index arithmetic. It has no tax, costs, selection or leverage spread beyond 1 pt. Equity returns differ by country, e.g. PRT −38, which drags Portugal to 16.6 despite housing at 53.
3. PAYG present values depend on country discount rates (France 2021 is below 2018). UK is only to 2018.
4. The 1995 balanced panel lacks land for DEU before 1999 and for some others. Many dwellings series end in 2023. PWT ends in 2023.
5. World-hour net worth swings with exchange rates. The BIS December rate is used, against the World Bank annual average: median gap 4%; larger gaps in BGR 1996, RUS 1998, KOR 1997 and TUR 2021.
6. Before 1961, world weights are fixed at 1960 USD GDP. The country set grows from 28 to 129 (constant 1950 sample: 7.2 vs 8.2).
7. OECD "N1N" for NLD contains land, so produced assets are taken as N11N + N12N + N13N.
