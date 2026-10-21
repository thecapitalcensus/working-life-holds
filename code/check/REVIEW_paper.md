# Referee and copy-edit review: household.pdf (draft v1.0, 21 October 2026)

Reviewed: output/paper/household.pdf (21 pages). I read it in full with pdftotext -layout and looked at rendered pages 4–20.
Numbers were checked against output/paper/numbers_in_text.json and the CSVs in output/housing, output/balance and output/life.
Note 3's wording was checked against the predecessor text (income.txt).

Spot-check result: 30 numbers were traced to CSVs. All the generated text values match their source files
(Table 2 in full; Table 4 vs table_hour_return_by_claim.csv; Table 6/A2 vs table_composition_latest_2023.csv;
Table 8/A3 medians recomputed by hand; Table 9 vs A1 and Table 11; Table 10 vs table_payg_return_by_decade_world.csv;
Table 12 vs summary_baseline.csv; Table 14 vs decade_O_vs_R_baseline_variable_bills.csv; Table 16 vs robustness_one_at_a_time.csv;
Z.1 peaks of 24% in 2013 and 19% in 2008 and private business at 23%→8%; the US 1970 cohort at 9.60/4.75/14.0%/2.34/−0.52; extras.json at 3.9/0.25/36.1/45.3).
The problems found are mostly about what the numbers are said to mean, not the numbers themselves.

---

## MUST-FIX

**1. Summary item 1 and §4.4 last paragraph (p.1, p.7): the after-tax comparison says the opposite of what the numbers show.**
Current (Summary): "A property tax of one point a year takes the 1976–2020 net from 40.0 to 30.0; adding the costs of buying and selling every ten years takes it to 22.0. That is about the same as the GMP, not more."
Current (§4.4): "On a like-for-like basis, then, the home earned about as much as the world's investable capital, not more."
Problem: the GMP's 1976–2020 net is 38.0 (Table 2), and 24.7 excluding valuation. Housing after tax and costs is 22.0, or 17.9 excluding valuation (Table A5). That is well below the GMP. It is not "about the same". The GMP's withholding and fund costs are a few hours at most, and the note itself says "those are much smaller".
Proposed (Summary): "A property tax of one point a year takes the 1976–2020 net from 40.0 to 30.0; adding the costs of buying and selling every ten years takes it to 22.0, against 38.0 for the GMP before its (much smaller) fees and withholding taxes. Before taxes and costs the home earned about as much as the world's capital; after them, less."
Proposed (§4.4): "After a property tax and transaction costs, then, the home earned less than the world's investable capital: 22.0 hours against 38.0."
Change the item 1 headline to match: "1. Before taxes and costs, the home earned about as much as the world's capital, by another route."

**2. §4.4 correction box (p.7) and Summary item 2: note 3 is misquoted and its claim is misstated.**
(a) Current: "Note 3 … reported the net rental yield … as 5.52% in 1976, 4.28% in 2000 and 2.73% in 2020." Note 3 printed **5.5%, 4.3% and 2.7%** (income.txt, §7). The two-decimal values are this note's reproduction of note 3's calculation, not what was printed.
Proposed: "Note 3 … reported the net rental yield … as 5.5% in 1976, 4.3% in 2000 and 2.7% in 2020 (5.52, 4.28 and 2.73 unrounded)." Make the same change in Summary item 2 and in the Table 5 row "Note 3 as printed (wrong weights)". Either print 5.5/4.3/2.7 there, or relabel the row "Note 3's calculation (wrong weights)".
(b) Current: "Note 3's statement that housing's yield fell from above the GMP's cash yield to below it reverses at the end: in 2020 the corrected rent yield (3.72%) was above the GMP's cash yield (1.94%)." Note 3 made no such statement. With its own figures, housing was *below* the GMP in 1976 (5.5 vs 7.2) and *above* it in 2020 (2.7 vs 1.9). Note 3 said only that "the direction is comparable".
Proposed: delete the sentence and replace it with: "The substantive change is in the trend. Note 3's figures had the rent yield halving between 1976 and 2020, nearly in step with the GMP's cash yield. Corrected, it fell by a fifth (4.61% to 3.72%) while the GMP's cash yield fell by almost three-quarters (7.15% to 1.94%). Note 3's statement that housing was above the GMP's cash yield in 2020 still holds, by a wider margin."
(c) Optional: issue a v1.5 erratum line on note 3 itself that points here.

**3. Summary item 5, Table 12 and §7.2 (pp.1, 13–14): the headline median O÷R = 1.00 and O−R = 0.00 is a tie created by the 17 lives that never buy.**
By construction, O = R exactly for non-buyers. In O−R, the 223 negative lives, 17 zeros and 236 positive lives put the 238th and 239th values (the median of 476) inside the block of zeros. That is why the result is exactly 0.00 and 1.00. The same thing happens in Table 16 for the "Home 6×", "Budget 25%" and "original design" rows (239, 182 and 158 never-buyers; each shows O÷R = 1.00). A hostile reader will spot an exact 0.00 at once.
Proposed (Summary item 5): "Across the 459 lives that buy, the owner's median lead at 65 is 0.08 years of final pay (interquartile range −3.10 to 3.48; mean −0.08), and the owner comes out ahead in 236 (51%)."
Proposed (§7.2): add after the first sentence: "The median ratio of exactly 1.00 and difference of exactly 0.00 arise because the 17 lives that never buy have O = R and sit at the middle of the distribution; among the 459 buyers the median difference is 0.08 (Table 13)." In Table 16, add a footnote to the O÷R column: "Lives that never buy have O÷R = 1."

**4. §6.1, §1 bullets, Summary item 4, §7.1 "The pension" (pp.2, 10, 12): "wage-indexed" is used for what is in fact a claim indexed to the wage bill (≈ nominal GDP).**
An individual claim indexed to *average* wages grows with pay per worker. In national hours it would earn the growth of hours per worker (negative: −3.4 to −3.6 per 1,000 in Table 10), not the growth of total hours. Samuelson–Aaron give the sustainable internal return of a balanced pay-as-you-go *system*, not the indexation of an individual's accrued claim. In the model, the claim grows with "the national wage bill", meaning national hour × total hours, i.e. GDP. This is the first thing a pensions economist will attack.
Proposed (§1 bullet): "A pay-as-you-go pension whose claims grow with the wage bill — the return a balanced system can pay (Samuelson 1958; Aaron 1966) — earns the growth of the wage bill."
Proposed (add to §6.1): "This is the return the system can sustain, not the indexation rule of any one country. Individual entitlements are usually indexed to average wages or to prices. A claim indexed to average pay per worker would earn, in national hours, the growth of hours per worker, which was negative (Table 10)."
Proposed (§7.1): "whose value grows with nominal GDP (the wage bill at a constant labour share)". Replace "wage-indexed" with "wage-bill-indexed" in the Summary, §1, §6.1 heading, §7.3, Figure 7 caption and §8, or define the term once in §2.

**5. Summary item 4 and §6.2 (pp.1, 11): "Shorter working years took 4.0 hours per 1,000 a year off" does not match Table 10, which shows −3.4.**
4.0 is employment minus total hours (12.2 − 8.2) over different country sets. The table's hours-per-worker row says −3.4.
Proposed: "Hours per worker fell by 3.4 per 1,000 a year in the countries with that series; employment grew 12.2 and total hours 8.2." Do this in both places. If 4.0 is kept, say "the gap between employment and total-hours growth was 4.0".

**6. §5.1, "In hours of work" paragraph (p.8): the balanced-panel path is GDP-weighted, but the sentence reads as a continuation of the median.**
Current: "The median household net worth per worker was 3.6 years … In a balanced panel of 26 countries it rose from 3.49 years in 1995 to 6.00 in 2021 and fell back to 5.32 in 2023."
The values come from nw_to_gdp (GDP-weighted). The median in that panel went 3.08 → 3.82 → 3.62.
Proposed: "In a balanced panel of 26 countries, the GDP-weighted figure rose from 3.49 years in 1995 to 6.00 in 2021 and fell back to 5.32 in 2023 (median 3.08, 3.82 and 3.62)."

**7. Summary item 3 (p.1): "across 31 OECD countries".** Table A2 includes Bulgaria, Romania and Croatia, which are not OECD members.
Proposed: "across 31 countries in the OECD household accounts".
In the same item: "Across 30 European countries in 2021 that claim was a median 272% of GDP, or 78% of household net worth". The 78% is over 24 countries.
Proposed: "… a median 272% of GDP across 30 European countries, and a median 78% of household net worth in the 24 where net worth is known."

**8. Section 8, first paragraph (p.16): "the home through rent, the portfolio mostly through price" is wrong.**
Table 2: in 1976–2025 the GMP's cash was 50.4 and its price 32.5. In 1976–2020 the figures were 52.8 and 34.8. The GMP paid *more* cash than housing paid rent.
Proposed: "They earned it differently: the home through rents that kept rising after valuation is set aside (price excluding valuation 39.6 hours a year against the GMP's 21.5), the portfolio with more help from falling yields (valuation 11.0 against 6.2)."
In the same paragraph, current: "fell to around zero in Germany, Japan, France and Italy". Germany is −2.9 and Japan −2.2.
Proposed: "was negative in Germany and Japan and about zero in France and Italy over 1976–2020".
Current: "on the UN projections turns negative across the rich countries after 2030". This is a population projection, GDP-weighted, and the US, UK and Sweden stay positive (Table 11).
Proposed: "and the UN projection of the population aged 20–64 turns negative on GDP-weighted average after 2030".

**9. Summary closing paragraph (p.2): it mixes units and contradicts itself.**
Current: "Capital — the home and the portfolio — earned about 3.5 to 4.1% a year more than the growth of the hour. The claim indexed to work itself earned the growth of hours worked, 0.66% a year in 1976–2020 … A wage-indexed pension is built to stand still in hours, and it earns nothing more."
(a) 3.5–4.1% is in world hours over 1976–2025. 0.66% is national-hours growth across all countries over 1976–2020. §6.3 itself says these can be set side by side "only in aggregate". (b) The figures are before taxes and costs (see item 1). (c) "earns nothing more" contradicts the sentence before it.
Proposed: "Before taxes and costs, capital — the home and the portfolio — earned about 4% a year more than the growth of the hour (1976–2025, world hours). A claim on the wage bill earns only the growth of hours worked: across the 16 Macrohistory countries, 0.44% a year in national hours in 1976–2020, against 3.97% for housing on the same basis. That growth is falling."

**10. Inconsistent values for the same quantity, §4.2/Table 3/Table A1 vs Table 4/§6.3 (pp.6, 12).**
Housing net in national hours, GDP-weighted, is 39.6 for 1976–2020 and 35.4 for 1950–2020 in Table 3, Table A1, §4.2 and table_housing_robustness.csv. Table 4 and §6.3 give 39.7 and 35.5 (from table_hour_return_by_claim.csv). The two builders use different paths.
Fix: use one computation. If they genuinely differ (for example in sample start for Germany or Japan, or in the hour series), say why in the Table 4 note.

**11. §7.2 "By cohort" and Summary item 5: the cause of the cohort decline is overstated, and stated differently in four places.**
Current (§7.2): "With variable-rate mortgages, the ratio falls only from 1.17 to 0.95, about 44% of the baseline decline … The decline is therefore mostly the 60/40's strong returns over 1980–2020 … fixed-rate debt adds to it."
On these numbers, switching to variable rates removes 56% of the decline, and switching to bills removes all of it. The two effects overlap, so neither "mostly" claim follows. The note also says: Summary, "mostly because the 60/40 … did well after 1980"; §7.2, "leverage and the timing of purchase decide the sign"; §8, "depended mostly on when it bought and on the cost of its mortgage"; §9, "The vehicle matters more".
Proposed (§7.2): "Two changes each remove most of the decline: variable-rate mortgages remove 56% of it, and bills as the saving vehicle remove all of it. The decline is therefore the combination of strong 60/40 returns after 1980, which later renters held for most of their working lives, and fixed-rate debt, which inflation eroded for early buyers and which locked later buyers into high rates. The two overlap and cannot be added."
Summary: "… later ones lost (0.76 for the 1980 cohort), because renters' 60/40 did well after 1980 and later buyers locked in high fixed rates." Make §8 and §9 consistent with this.

**12. §7.1 / Table 16 / §7.3 / Summary item 4: the "GMP vehicle (from 1976)" is not defined.**
Cohorts start from 1950, so the reader cannot tell what the vehicle is before 1976, or how the dollar GMP is converted into local currency.
Proposed (add to §7.1): "In the GMP variant the account holds the domestic 60/40 until 1975 and the GMP, converted to local currency at the database's year-end rate, from 1976." Use whatever is actually the case.

---

## SHOULD-FIX

**13. Summary item 1 (p.1): "Housing's surplus is its net rent yield: rents grew more slowly than the hour."** Placed straight after the comparison with the GMP, it reads as housing's lead *over the GMP*. Yet the GMP paid more cash (52.8 vs 44.0). Housing's lead excluding valuation comes from price excluding valuation (41.4 vs 21.4).
Proposed: "Housing's gain over the hour comes from its net rent; rents themselves grew more slowly than the hour."

**14. §7.2 "Valuation is a small part" (p.15):** "The owner's gain over a life came from net rent and from rents that grew with nominal incomes". §4.2 and §7.4 say rents grew *more slowly* than the national hour (pay).
Proposed: "… came from net rent and from rent growth, not from a rising price per unit of rent."

**15. §7.2 "Lives that overdraw" (p.15):** "These levels may reflect rent-controlled post-war markets." Rent control lowers rents and so lowers yields. It cannot explain yields that are *high* relative to prices.
Proposed: "The database's post-war rent levels in these countries may be imperfectly measured." Or delete the sentence.
Also add: "All 12 lives that end below zero never buy, so O and R are identical for them." (CHECK_life.md item 1 confirms this.) Otherwise readers will assume owners went bankrupt.

**16. §7.1 (p.12), "Pay":** pay is GDP per worker (national hour × fixed hours), not wages. With a labour share of about 0.6, "4 times pay" is roughly 6–7 years of actual earnings, and a "35% budget" is about 55–60% of earnings.
Proposed (add): "Because pay here is output per worker, levels such as a home at 4 times pay or a 35% budget are lower, as multiples of actual earnings, than they look."

**17. §7.1 "Budget" (p.12):** "The home costs 4 times pay in the cohort's first working year (year s+1, age 26)". "Starts work at 25" and "first working year … age 26" conflict for readers (CHECK_life.md also asked for this).
Proposed: "… in the cohort's first full year of pay (the year after it starts work at 25, age 26)".

**18. §7.2 and Table 12 (pp.13–14): the world-hour wealth rows are ambiguous.**
The table label is "R in world hours per hour of own final pay"; the text says "57.1 … years of world-hour pay". 57.1 ≈ 12.06 years × 4.6 world hours per own hour.
Proposed label: "R, years of final pay × world hours per own hour (= wealth in world hours ÷ annual hours)". Use the same wording in the text.

**19. §7 generally:** the 476 lives are heavily overlapping (31 cohorts per country sharing 39 of 40 years). They are not 476 independent observations, so "50% of lives" and "95% of lives" overstate precision.
Proposed (add to §7.1): "Neighbouring cohorts share 39 of their 40 years, so the 476 lives contain far fewer independent histories than their number suggests: in effect 16 countries and a few distinct periods."

**20. Summary item 5 omits the most important robustness fact.** Across the 162-variant grid, the share of lives in which O beats R runs from 2% to 95% (§9).
Proposed (add): "Across 162 variants of the assumptions, the owner's win rate ranges from 2% to 95%; the answer is the assumptions'."

**21. Table 10 vs §6.2 text and Figure 5 (p.11):** the text and Figure 5 use "8.4 in 2011–2023", but Table 10 has columns for 2011–2020 (2.2) and 2021–2023 (28.8) only.
Fix: add a 2011–2023 column to Table 10, or change the text to "2.2 in 2011–2020, then 28.8 in 2021–2023 as hours recovered from 2020".

**22. §6.4 (p.12):** "Over 1976–2020 the same population grew 13.9 at the same weights." It is unclear whether "the same population" means all countries or the 16, and Table 10's memo row gives 10.0 for 1976–2020 (time-varying weights).
Proposed: "Over 1976–2020 the population aged 20–64 across all countries grew 13.9 per 1,000 a year at 2023 GDP weights (10.0 at each year's weights, Table 10)." Adjust if it is the 16.

**23. §5.1 (p.8):** "Equity and fund shares were 23.3% …: listed shares 8.7, unlisted 1.8, other equity 5.6 and investment-fund shares 6.3." These sum to 22.4, because Japan, Korea, Chile and Canada lack some sub-items.
Proposed: add "(sub-items sum to 22.4 because four countries do not report all of them)".
Also: "Dwellings and land run from 66% in Spain to 28% in Denmark and 24% in Romania." Romania reports no land.
Proposed: "… from 66% in Spain to 28% in Denmark (24% in Romania, which reports no land)."

**24. §5.4 (p.10):**
(a) "The range runs from 13.8 in JPN to 68.9 in SWE" → "in Japan … in Sweden" (no ISO codes in prose).
(b) "The GMP's net over 1976–2026 was 35 in world hours (note 3)" → "34.8 over 1976–2025 (Table 2)", to keep one period throughout.
(c) Table 9's Median row mixes a 13-country median (35.5) and a 10-country median (23.8) in one row. Add a note: "Last column: median of the 10 countries with Eurostat data; the same 10 have a median of 42.1 without PAYG."

**25. Section 7.1 vs Table A1 (pp.12, 18):** lives lack data for "Germany before 1961 and Japan before 1959", but Table A1 says Germany's housing series starts in 1963 and Japan's in 1960. Explain the difference (for example, which series binds), or harmonise.

**26. Period labels 1950–2020 vs 1951–2020.** Tables 3, 4 and A1 say "1950–2020"; §6.3 and Figure 5 say "1951–2020" for the same 35.5/37.3/−0.4/−12.9. Use one label, presumably 1951–2020 for annual returns.

**27. §4.1 (p.5):** "The annual net of housing had a standard deviation of 3.3%" has no period, and "In the 26 twenty-year windows" does not say which span.
Proposed: "Over 1976–2020, the annual net …"; "In the 26 twenty-year windows within 1976–2020 …".

**28. Causal and over-general language to soften:**
- §4.3: "post-war inflation and repressed rates made a deposit a claim that shrank in hours" → "consistent with post-war inflation and repressed rates, a deposit shrank in hours".
- §4.4: "The rent yield moved much less than the GMP's yield because rents are not reset by interest rates in the way bond coupons are." → "… moved much less than the GMP's yield, which is dominated by bond coupons that reset with interest rates."
- §4.2: "sits below the median because the large economies with low housing returns, Japan and Germany, carry much of the weight" → "partly because Japan and Germany, with low housing returns, carry large weights" (the US, at 41%, is above the median).
- §5.3: "France's 2021 value is below its 2018 value mainly because of the discount rate" needs a number or source. Otherwise: "partly because of a change in discount rate".
- §9: "larger only because buyers there buy later" → "larger mainly because …".
- Summary item 4 headline: "The pension earns demography" → "The pension earns the growth of hours worked". Working time (−3.4) and participation are as large as demography.

**29. Caveats (§8, p.16).** These are adequate in coverage but thin in three places:
- No taxes: add "Imputed rent on an owner's home is untaxed in most countries, which favours owning."
- Survivorship: add the direction. "Their housing and equity returns are likely higher than those of a random sample of countries over the same years."
- Labour share: give the magnitude or cite it. PWT 11.0 has labsh, so the wage bill can be computed directly as a check (note 3 cites Karabarbounis and Neiman 2014 for the fall). Proposed: "Over 1976–2020 the GDP-weighted labour share changed by X points (PWT labsh), which would change the PAYG return by about Y per 1,000 a year."
- Eurostat: state the discount rates (or range) behind Table 29, or a ±1 point sensitivity if available.

**30. Missing citations for parameters.** The 7.7% round-trip transaction cost and the one-point property tax come from Jordà et al. (2019); note 3 cites them for this. Add "(Jordà et al. 2019)" in §4.4 and Table A5.

**31. Layout (pp.4–20):**
- Table 2's caption sits alone at the foot of p.4 with the body on p.5. Keep them together.
- Table 8 is split after Germany (p.9/p.10), with the header repeated.
- Table 11 is split after its first row (Australia alone on p.11).
- Table 12 is split after two rows (p.13/p.14).
- Table 15's caption is at the foot of p.15, with the body on p.16.
- Table 16 is split after four rows (p.16/p.17).
- Table A3 is split, leaving Denmark alone on p.20.
- Use page-break-inside: avoid on tables (and keep captions with tables).
- Table 4 and Table 16 headers wrap badly ("O ÷ O beats R, R %"); shorten the column heads.

**32. References.**
- Nakanishi (2026c) is not cited anywhere except as part of "Nakanishi 2026a–d" in Table 1, which is labelled "Notes 1–3" but spans four works. Either cite 2026c where the GMP weights are used, or relabel: "Notes 1–3 and the weight history (Nakanishi 2026a–d)".
- Jordà, Schularick and Taylor (2017) is listed but never cited in the text. The database's terms ask for it. Add it at first mention in §3: "The Macrohistory Database, release 6 (Jordà, Schularick and Taylor 2017; Jordà et al. 2019), …".
- Verify the PWT 11.0 DOI (10.34894/FABVLR). Each PWT release has its own DOI.
- If item 29 adds labour-share text, add Karabarbounis and Neiman (2014).

---

## OPTIONAL

**33. Front matter, header nav:** "Monthly Index Methodology Verification Ledger Data …". The site nav bar is printed in the PDF. Consider dropping it from the print version.

**34. §4.1:** "The effect was first found, and its sign confirmed, by an independent check." This is process detail. Delete it, or move it to Appendix B.

**35. §4.1:** "the log of one plus the capital gain plus the rent return, less the log of one plus the rent return, is not the log of one plus the capital gain." Hard to parse. Use a formula: "ln(1+g+y) − ln(1+y) ≠ ln(1+g)".

**36. Notation:** "3e-15", "7e-15" (§2, §7.1) vs "3×10−8" (§3). Use one style. Better, drop the tolerances from the main text ("checked to machine precision").

**37. §2:** "Ten hours per 1,000 is one percent a year." Note 3 uses "%"; "1% a year (log)" is consistent.

**38. §7.4:** "fell by −0.36% a year" is a double negative → "fell by 0.36% a year". "Rose by about 26%" while the medians go 4.0 → 5.0 (25%). Say "about a quarter".

**39. Section order:** Robustness (§9) comes after "What it means" (§8). Consider swapping them, so the conclusions follow the checks.

**40. Table 4 row "Bills (deposits)":** bank deposits usually pay less than bills. Add "(deposits typically earn less)" in the note.

**41. Table A5:** add the "OECD rent growth, national median 45.8" row cited in §9. Explain "Dec-to-Dec interpolated hour" (48.2) vs the baseline national median (47.5).

**42. Figures:**
- Figure 3: the country-code tick labels and the liability marks are very small at print size. Spell out "NPISH" in the panel title.
- Figure 5: the "−12.9" label overlaps the Bills bar.
- Figure 1: the legend text is tiny.
- Raise the font size to at least 8 pt in Figures 1, 3, 6 and 7.

**43. Repetition:**
- The O−R decomposition is spelled out three times (Summary, Table 13 caption, §7.2 with the full equation). Keep the equation once, in §7.2.
- The Summary's closing paragraph largely repeats §8's first paragraph. Cut one.

**44. Phrases to plainen:**
- "The cleanest comparison" → "The like-for-like comparison".
- "changes the picture in Europe" → "lowers the European figures".
- "the forward part" (§6.4 heading) → "Projection".
- "In most of Europe, then, the standard balance sheet leaves out close to half of what households are owed": net worth is not "what households are owed" → "… leaves out about 45% of household wealth including the pension claim".

---

## Notes on items checked and found sound
- The design correction is disclosed in the front matter, §7.1 (box, with the original results in Table 16) and §8. This is adequate.
- Index vs a house: §4.1 and §8. Adequate.
- Spelling is consistently British (labour, favour, stylised, individualised, Licence), as in note 3.
- Captions are numbered in order (Tables 1–16, A1–A5; Figures 1–7). All "Table n" and "Section n" cross-references resolve correctly.
- Table 2 adds up in every column within rounding. Tables 8/A3 medians (272, 11, 78, 3.47, 6.54) recompute exactly. Table 9's PAYG and housing columns match Tables 11 and A1. Table A4 overdraws sum to 176.

---

## Response to review (2026-10-21, rebuild of household.html/pdf, 22 pages)

All numbers below are filled from outputs by code/build_paper.py; new inputs are output/housing/extras.json (code/build_extras.py) and output/life/summary_payg_variants.csv.

| # | Response |
|---|---|
| 1 | Changed. Item 1 headline now "Before taxes and costs … about as much …; after them, less"; Summary and §4.4 state 22.0 vs 38.0, with the GMP's smaller costs noted. §8 robustness sentence and §9 qualified the same way. |
| 2 | Changed. Note 3 is quoted as printed (5.5/4.3/2.7), unrounded values given in brackets; Table 5 row relabelled "Note 3's calculation, unrounded (printed as …)". The false attribution is deleted; the box now describes the trend change (rent yield −19% vs GMP cash −73% over 1976–2020) and the 2020 margin (1.78 points corrected vs 0.79 in note 3's figures). (c) Erratum on note 3: not done here (outside this build); flagged to coordinator. |
| 3 | Changed. Summary item 5 and §7.2 headline the 459 buyers (median O−R 0.08, IQR −3.10 to 3.48, owner wins in 236 = 51%); the 17 never-buyers and the exact 1.00/0.00 are explained; Table 16 footnote added. |
| 4 | Changed. Two indexations defined in §2 (wage bill vs average pay per worker); §1, §6.1 heading and text, §7.1, §7.3, Figure 7 caption, Table 12, §9 use them. Summary item 4 reports both (wage bill 6.6 / 4.4 per 1,000; average pay −3.6) and the life results (4.28 vs 3.75 years; funded 2.44× and 2.95×). "Wage-indexed" no longer appears. |
| 5 | Changed. Uses avh_all (−3.4 in 1951–2023; −3.6 in 1976–2020) as growth of hours per worker; the "took 4.0" wording is removed; text notes country sets differ. |
| 6 | Changed. GDP-weighted labelled; medians 3.08 / 3.82 / 3.62 added. |
| 7 | Changed ("31 countries in the OECD household accounts"; 78% stated over the 24 countries). |
| 8 | Changed as proposed (price ex valuation 39.6 vs 21.5; valuation 11.0 vs 6.2; Germany/Japan negative, France/Italy about zero; GDP-weighted population projection). |
| 9 | Changed. Closing paragraph compares on one basis (national hours, 16 countries, 1976–2020: housing 3.97% vs wage-bill claim 0.44% a year) and drops "earns nothing more". |
| 10 | Explained rather than merged: Table 4 caption states that it averages country nets at each year's weights (39.7) while Table 3 weights the components (39.6). |
| 11 | Changed. §7.2 states it once: variable rates remove 56% of the decline, bills remove all of it; both effects needed, they overlap. Summary, §8 and §9 made consistent. |
| 12 | Changed. GMP vehicle defined in §7.1 (domestic 60/40 to 1975, GMP in USD converted at the database's year-end rate from 1976). |
| 13 | Changed as proposed. |
| 14 | Changed ("from net rent and from rent growth"). |
| 15 | Changed. Rent-control sentence replaced; "all 12 lives that end below zero never buy" added. |
| 16 | Changed (sentence added under "Pay"). |
| 17 | Changed ("first full year of pay (the year after it starts work at 25, age 26)"). |
| 18 | Changed (Table 12 label "in world hours ÷ annual hours"; same wording in text). |
| 19 | Changed (overlap paragraph in §7.1; shares described as history, not probabilities). |
| 20 | Changed (grid range 2–95% in Summary item 5). |
| 21 | Changed (2011–2023 column added to Table 10; text cites 2011–2020 and 2021–2023). |
| 22 | Changed as proposed (13.9 at 2023 weights, 10.0 at each year's weights, all countries). |
| 23 | Changed (sub-item sum 22.4 noted; Romania reports no land). |
| 24 | Changed: (a) names; (b) 34.8 over 1976–2025 (Table 2); (c) Table 9 note with the 10-country median without PAYG. |
| 25 | Changed: §7.1 says Table A1's long-period column also needs national hours and the rent-yield change, so it starts later. |
| 26 | Changed: national-hour long period labelled 1951–2020 throughout (the first annual return needs a 1950 level). |
| 27 | Changed (periods added). |
| 28 | Changed, all six (headline 4 now "earns the growth of hours worked, or less"). |
| 29 | Changed: imputed-rent and survivorship sentences added; labour share computed from PWT 11.0 labsh (16 countries, GDP-weighted, 64.3% in 1976 → 59.8% in 2019, ≈1.7 per 1,000 a year off the wage-bill return), with Karabarbounis and Neiman (2014). Eurostat discount rates: declined — no common-rate version in the data; stated as a limitation. |
| 30 | Changed (Jordà et al. 2019 cited in §4.4, §8 and Table A5). |
| 31 | Changed: body tables kept whole (break-inside: avoid; captions kept with tables); appendix tables may split; Table 16 and Table 4 headers shortened. Rendered pages checked. |
| 32 | Changed: Table 1 row "Notes 1–3 and the GMP weight history (Nakanishi 2026a–d)"; Jordà, Schularick and Taylor (2017) cited in §3; Karabarbounis and Neiman (2014) added. PWT DOI kept as recorded at download (data/SOURCES.md: doi 10.34894/FABVLR for PWT 11.0). |
| 33 | Done (site nav hidden in print). |
| 34 | Done (process sentence removed; Appendix B lists build_extras.py and check/). |
| 35 | Done (formula). |
| 36 | Done ("machine precision" in the text). |
| 37 | Done ("1% a year (log)"). |
| 38 | Done ("fell by 0.36% a year"; "about a quarter"). |
| 39 | Done (Robustness is now §8, "What it means" §9). |
| 40 | Done (Table 4 note; row relabelled "Bills"). |
| 41 | Done (OECD national median row restored in Table A5; Dec-to-Dec explained in caption and §8). |
| 42 | Partly: Figure 5 label overlap fixed (figure made by build_paper.py). Font sizes of Figures 1, 3, 6, 7 not changed: they are produced by the section builders, whose outputs the independent checks refer to; can be done in a later version. |
| 43 | Done: the decomposition equation appears once (§7.2); Summary no longer repeats it; §9's first paragraph no longer repeats the Summary closing. |
| 44 | Done ("like-for-like", "lowers the European figures", "Projection", "close to half of household wealth once the pension claim is counted"). |
| Coord. | Overlapping lives acknowledged (§7.1). |
