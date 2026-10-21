# Note 4 — outline and story (orchestrator, 2026-10-21; numbers provisional until checks finish)

Title: "What a Working Life Holds: The Home, the Pension and the Portfolio in Hours of the World's Work"
Lede: Research note, draft v1.0, 21 October 2026. Keisuke Nakanishi. SSRN id: [TBD on submission].

Summary: five numbered results, then one closing paragraph (style of note 3).
1. The home earned about as much as the world's capital, by another route. Per 1,000 world hours of housing
   capital, 1976–2025: net ≈ 41 h/yr vs GMP 35; excluding valuation 34 vs 24. Housing's surplus is its net rent
   yield; rents grew slower than the hour. Smooth index (sd 3.3 vs 8.2). After property tax (1 pt) and transaction
   costs it falls to ~22–30 — "about the same as the GMP", not more. 2021–25 housing gains were mostly valuation.
2. Correction to note 3 §7 (state plainly, with old and new numbers, and why: JST gdp units).
3. The household balance sheet: dwellings+land 42% of gross assets (2023, 31 OECD, GDP-weighted), F5 23, F6 16,
   deposits+bonds 14; liabilities 12%. Wealth per worker in years of national work = wealth/GDP (identity) —
   median 3.6, US 3.6 (1952) → 6.1 (2026). Omitted PAYG claim: median 272% of GDP, 78% of net worth (Eurostat 2021).
4. The pension earns demography. Wage-indexed PAYG claim's hour return = growth of total hours worked:
   ~0.8%/yr world 1951–2023 (0.66 in 1976–2020), already negative in Germany and Japan; falling annual hours
   cost 0.4 pt; UN projection of 20–64 population turns negative after 2030 (projection, not data).
   At retirement, a funded claim of the same contributions is a median 2.4× the PAYG claim (domestic 60/40),
   1.9× in GMP, 0.9× in bills.
5. A life: buying vs renting-and-investing roughly ties (median O/R 1.00, IQR 0.78–1.29). Price gain + net rent
   saved ≈ mortgage interest + forgone return on the deposit. Early cohorts gained by buying (1950s 1.27), later
   ones lost (1980 0.76). Valuation ≈ 2% of owners' wealth. The standard 2000 home cost 6.5 years of pay in 1950,
   4.0 in 2000, 5.1 in 2020.
Closing paragraph: what a life holds is less about which asset than about what each claim is indexed to — capital
(home, portfolio) earned ~3–4% a year above the hour; the claim indexed to work itself earned the growth of
hours worked, under 1% and falling. Standing still in hours is what a wage-indexed pension does by design; it
earns nothing more.

Sections: 1 The question; 2 Definitions (world hour, national hour, years of own pay; identity NW/GDP);
3 Data and construction (incl. JST units fix, OECD extension, chaining, Eurostat T29, PWT 11, UN WPP);
4 The home in hours (Tables: housing vs GMP per 1,000 h by period; national hours by country; rent yield vs GMP cash
yield; correction box to note 3); 5 The household balance sheet in hours (composition table; US Z.1 figure; PAYG
entitlements table; balance-sheet hour return synthesis — clearly a weighted average of index returns);
6 The pension in hours (Aaron; table by decade; countries; projection); 7 A life (design summary, the design
correction stated openly, results, O−R decomposition, by cohort, never-negative lives, 2000-anchor row);
8 What it means and what it does not; 9 Robustness (housing grid, life grid summary); Disclaimer; Revision history
(v1.0 only); References (JST 2017/2019; Knoll–Schularick–Steger 2017 "No Price Like Home"; Samuelson 1958; Aaron
1966; Eurostat T29 methodology; Feenstra–Inklaar–Timmer 2015 PWT; UN WPP 2024; OECD sources; Fed Z.1; Nakanishi
2026a–d); Appendix (input hashes, data sources).

Style: plain English, short sentences, numbers in text pulled from outputs via {{n:key}}, no jargon. Exploratory,
not pre-registered, run with results visible (say so, as note 3 did). AI disclosure as note 3.
Licence: text CC BY-NC-ND 4.0; JST-derived series CC BY-NC-SA 4.0; PWT CC BY 4.0; OECD/Eurostat/Fed/UN terms
(check SOURCES.md); CC-GMP/CC-WH CC BY-NC 4.0.

## Wording rules from the independent check (check/CHECK_4_6.md) — apply
- Say how housing valuation is measured: GDP-weighted mean of each country's −Δlog rent yield (not the yield of the whole portfolio); state the 0.8 h residual in price ex valuation.
- "Dwellings + land" includes all household land; don't call it "the home". Gross assets include other non-financial assets.
- PAYG vs other claims: compare in national hours on the same country set (≈5.1 vs housing 35.5 per 1,000), not world-hour housing vs national-hour PAYG; world comparison only with the country-set caveat.
- Hours fell in Germany and Japan, flat in Italy and France.
- PAYG return = hours growth holds only if pay per hour keeps pace with GDP per hour (labour share constant); say so.
- Weights are start-of-year; same-year weights would give 42.7 (robustness row).
