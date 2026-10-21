# Second audit: household.pdf (draft v1.0, 21 Oct 2026, 22 pp), after the first review

Method: pdftotext -layout of the PDF read in full; check/REVIEW_paper.md and its responses read; every number in the
Summary and Sections 1, 8, 9 traced to output/paper/numbers_in_text.json and to the CSV/JSON in output/housing,
output/balance and output/life; table arithmetic recomputed by hand (Table 2 every column and period-weighted
averages, Tables 3/A1 rows, Table 8/A3 medians, Table 9 medians, Table 10 sub-period averages, Table 11 rows,
Table 13 means, Table 14 share removed); all seven figure PNGs (output/paper/img) inspected; note 3's §7 compared
with income.txt. No existing file was modified.

Result in brief: the large majority of numbers trace exactly (Table 2 sums and the 6/19/20-year weighting reproduce
40.0/40.6/38.0; 13 of 26 windows; 56% removed = 1 − 0.2248/0.5059; medians 272/11/78/3.47/6.54; 23.8/42.1; 0.36%
drift = ln(5.048/6.489)/70; labour-share 1.68 per 1,000; 0.6% / 22% weights; 1.78 and 0.79 points). The problems
below are mostly new or left over after the revision.

---

## ERROR

**E1. Karabarbounis and Neiman (2014) is cited but not in the References.**
Location: §6.1 ("Karabarbounis and Neiman 2014 document the fall"); References.
The response to review item 32 says it was added; it is not in the PDF or the HTML reference list.
Fix: add "Karabarbounis, L. and Neiman, B. (2014). 'The Global Decline of the Labor Share.' Quarterly Journal of
Economics, 129(1), 61–103."

**E2. §7.1 "Pay": the direction of the caveat is reversed.**
Current: "Because pay here is output per worker, levels such as a home at 4 times pay or a 35% budget are lower, as
multiples of actual earnings, than they look."
Pay here exceeds earnings (labour share ≈ 0.6), so a home at 4× this pay is ≈ 6–7× actual earnings and a 35% budget
≈ 55–60% of earnings: the multiples are *higher* than they look (this is what review item 16 said).
Also, pay is the national hour × *fixed* hours, i.e. output per hour scaled, not output per worker (the same bullet
says actual pay grew more slowly where hours per worker fell).
Fix: "Because pay here is output per hour at fixed hours, not earnings, a home at 4 times pay or a 35% budget is a
larger multiple of actual earnings (roughly 6–7 years and 55–60%) than it looks."

**E3. §5.2: compares growth over two different periods and so overstates the hours-per-worker effect.**
Current: "Net worth per worker went from 3.64 to 6.09 years of US work, 0.69% a year. … Growth in hours (to 2023) was
only 0.41% a year, because annual hours per worker fell from 2,060 to 1,789."
0.69% is 1952–2026; 0.41% is 1952–2023 (us_z1 CSV: 7,506 → 10,013). Like-for-like, years of work grew
ln(5.5975/3.6433)/71 = 0.60% a year over 1952–2023; hours per worker explain ln(1789/2060)/71 = −0.20 points, not 0.28.
Over 1952–2026 (hours held at 2023), growth in hours is ln(10,890/7,506)/74 = 0.50%.
Fix: "Over 1952–2023 it grew 0.60% a year in years of work but only 0.41% in US hours, because annual hours per worker
fell from 2,060 to 1,789 (−0.20% a year)."

**E4. Figure 7 title still says "wage-indexed PAYG claim".**
Location: img/h_fig7.png title "a domestic 60/40 account over a wage-indexed PAYG claim". Response 4 says the term no
longer appears. Fix: "… over a PAYG claim indexed to the wage bill".

**E5. §2 and §6.1: NDC schemes are said to credit accounts with wage-bill growth as a rule.**
Current (§2): "this is … how notional defined-contribution schemes credit accounts"; (§6.1) "notional
defined-contribution schemes credit accounts with it."
Not general: Sweden's NDC credits the growth of average income per insured person (an average-pay rule, the note's
second indexation); Italy uses GDP growth; Poland and Latvia use wage-bill growth.
Fix: "… as some notional defined-contribution schemes do (Poland and Latvia credit wage-bill growth, Italy GDP growth;
Sweden credits average income)."

**E6. Figure 4 caption mislabels the period.**
Current: "US households and non-profits (Federal Reserve Z.1, B.101), 2026 Q2: shares of total assets (areas) …"
The figure is the full 1952–2026 Q2 time path (its own title says so). Fix: "…, 1952–2026 Q2: …".

---

## INCONSISTENCY

**I1. Finland omitted from the countries where hours fell (Summary item 4, §6.2, §9).**
Table 11 (and table_payg_return_by_country.csv): Finland −1.0 over 1976–2020, below France (−0.4) and Italy (−0.0).
Current: Summary "negative in Germany and Japan"; §6.2 "Hours fell in Germany (−2.9) and Japan (−2.2) and were flat in
France (−0.4) and Italy (−0.0)"; §9 likewise.
Fix: "negative in Germany, Japan and Finland" (§6.2: "… Japan (−2.2) and Finland (−1.0) …"). Print Italy as "0.0" (also
Table 9 ITA).

**I2. Table A1, Belgium: components do not add to the total.**
Rent 52.7 + valuation 17.1 + price ex val. 28.8 = 98.6, against Total 102.0 (gap 3.4; same in
table_housing_by_country_national_hours.csv). All other 15 rows add within 0.1. Net (57.6) and Net ex val. (40.5) are
consistent with the Total and the valuation, so the price-ex-valuation (or rent) entry is computed over a different
year set. Fix in build_housing.py, or footnote the cause.

**I3. Median "Net ex val." national hours 1976–2020: 29.1 in Tables 3 and A1, 29.2 in the source.**
table_housing_national_hours.csv and table_housing_robustness.csv give 29.2; the paper's 29.1 is the median of the
rounded country values (28.2, 30.1 → 29.15). Use the CSV value.

**I4. Housing, national, GDP-weighted 1951–2020: 35.4 (Table 3, A1, §4.2) vs 35.5 (Table 4, §6.3, Figure 5 left).**
The Table 4 caption explains 39.6 vs 39.7 only. Extend it: "… gives 39.6 rather than 39.7 (1976–2020) and 35.4 rather
than 35.5 (1951–2020)."

**I5. §5.4 compares Table 9 (1976–2020 returns) with the GMP over 1976–2025.**
Current: "The GMP's net over 1976–2025 was 34.8 in world hours (Table 2)". Same period would be 38.0 (1976–2020). Fix:
"The GMP's net over 1976–2020 was 38.0 in world hours (Table 2), but the units differ …".

**I6. §8: "None of these changes the finding that … housing earned about as much as the GMP."**
Equal weights give 48.2 against the GMP's 38.0 (+27%); same-year weights 45.3. Fix: "None of these reverses the
finding … ; equal country weights (48.2) put housing clearly ahead."

**I7. National hour 2024–2025 is not documented.**
build_housing_ext.py extends PWT hours to 2024–25 with World Bank labour-force growth (wb_lf.json is in the input
hashes), which feeds Table 3/A1 "Net 2021–2025". Table 1 and §2–3 mention only "US hours after 2023". Add a line to §3
"Housing, 2021–2025" and to Table 1 (World Bank row: "labour force, 2024–2025").
Related: §4/§7 hours come from the FRED copies of PWT (EMPENG…/AVHWPE…), §6 from pwt110.xlsx; data/SOURCES.md
records them as "not reconciled". Reconcile, or say both are PWT 11.0.

**I8. US net worth per worker: OECD (Table 6, §5.1: 6.0 years, 52,361 world hours in 2023) vs Z.1 (Table 7: 5.60,
48,847 in 2023; 6.09, 54,541 in 2026).**
Side by side, "6.0 in 2023 … 6.09 in 2026" suggests little change; on one basis, Z.1 rose 5.60 → 6.09. Add "(OECD basis;
Z.1 gives 5.6)" in §5.1, or a note to Table 7.

**I9. Correction box: note 3's trend is overstated.**
Current: "Note 3's figures had the rent yield halving between 1976 and 2020, nearly in step with the GMP's cash yield."
Note 3 printed 5.5 → 2.7 (−51%) against 7.2 → 1.9 (−74%), and said only that "the direction is comparable". Fix:
"Note 3's figures had the rent yield halving between 1976 and 2020, in the same direction as the GMP's cash yield."
Also "(5.52, 4.28 and 2.73 unrounded)" → "(5.52, 4.28 and 2.73 as reproduced here)": note 3 did not print them.
The rest of the box is quoted accurately: 5.5/4.3/2.7, 16 countries, GDP in US dollars, §7; the 2020 margin
(0.79 vs 1.78) and the 0.6%/22% weights trace to build_log.json.

**I10. Balanced-panel median 2021: 3.81 in text, 3.82 in the review response.** The CSV holds 3.815 (3 dp), so the
two-decimal value is rounded twice. Compute from unrounded data.

---

## WORDING

- W1. Summary item 4: "4.4 across 16 rich ones" → "4.4 across the 16 Macrohistory countries" (the term used elsewhere).
- W2. §6.4: "Across the 16 Macrohistory countries it shrinks by 1.4 per 1,000 a year": add "over 2024–2060".
- W3. §7.3: "11.09 (2.95 times the average-pay claim)": 11.09/3.75 = 2.96. Say "a median 2.95 times".
- W4. §1: "a pension that grows with wages" is the one remaining ambiguous phrase → "that grows with the wage bill or
  with average pay".
- W5. Term drift: "Macrohistory Database" in text but "JST" in Figure 1 legend and Table A5 rows; "non-profits" (Table 7,
  Figure 4 caption) vs "nonprofits" (Figure 4 title, alt text); "NPISH" still unexpanded in Figure 3 title; Table 6
  "years of work" vs Table 8 "years of GDP" (same quantity); Table 9 "Home" vs "Dwellings + land".
- W6. Hyphens for en dashes: Figure 2 title "1976-2020", Figure 4 "1952-2026Q2", Table A5 rows "1976-2020/1976-2025";
  minus signs printed as hyphens in Figure 5 labels ("-0.4", "-12.9").
- W7. Sentences starting with numerals (§7.2: "176 lives go below zero", "12 lives end below zero") → "In all, 176 …".
- W8. Table 16 "Ever negative": say "O ever negative" (R is 128 at baseline).
- W9. Table 12 / §7.2 "in world hours ÷ annual hours": say which annual hours (the fixed hours per worker).
- W10. Licence paragraph: "every series derived from it here — housing returns …" omits the JST equity, bond and bill
  returns (Table 4, Table 9, Figure 5). Write "including".
- W11. Nakanishi (2026c) is still cited only through the range "2026a–d" in Table 1. Cite it in §3 "From note 3" where
  the GMP weights are used.
- W12. §2: "Every figure in Sections 4–6 is in these units": Section 5 is mostly shares and years → "Every return in …".
- W13. Front matter: "draft v1.0" vs Revision history "v1.0 … First version". Drop "draft" for the release.
- W14. Table 2 caption: "in percent × 10" vs "%" elsewhere (and §2 "1% a year (log)").

Checked and sound: the DOIs (2026a 10.2139/ssrn.7394599, 2026b 10.2139/ssrn.7445203, 2026c 10.5281/zenodo.22151403 with
concept .22151402, 2026d 10.2139/ssrn.7515699); the other references, all cited; the table and figure numbering and
every Table/Section cross-reference; the Appendix B count of 58 hashes; British spelling throughout (no -ize, "labour",
"favour"); the identity NW per worker in years of work = NW/GDP; the §6.1 lives identity (claim/final pay = Σ H_T/H_t);
the wage-bill vs average-pay logic and the 1.7 labour-share drag; figure contents against the tables (Figure 1 end values
≈ e^(50×net); Figure 2 median line 47.5; Figure 5 values 5.1/35.5/37.3/−0.4/−12.9 and the decade bars).

---

## Response to audit 2 (2026-10-21; rebuilt, 22 pp)

| item | response |
|---|---|
| E1 | Fixed: Karabarbounis and Neiman (2014) added to the References. |
| E2 | Fixed. The direction is corrected: pay is output per hour at fixed hours. The earnings multiples are computed in build_extras.py from the PWT labour share (mean 62%, 1951–2019): a home at 4× pay ≈ 6.5 years of earnings; a 35% budget ≈ 57% of earnings. |
| E3 | Fixed. §5.2 now uses 1952–2023 for both measures: 0.60% a year in years of work, 0.41% in US hours, hours per worker −0.20% a year. 2026 is stated separately. |
| E4 | Fixed in build_life.py ("… over a PAYG claim indexed to the wage bill"). The life CSVs are unchanged. |
| E5 | Fixed in §2 and §6.1: "NDC schemes credit accounts with wage-bill, average-income or GDP growth, depending on the country." |
| E6 | Fixed: the caption reads "1952–2026 Q2". |
| I1 | Fixed: Finland (−1.0) added in the Summary, §6.2 and §9. Italy now prints as 0.0 (negative-zero formatting fixed throughout). |
| I2 | Fixed in build_housing.py: every component uses the same years (Belgium 1976 had no rent-yield change). Belgium is now 98.0 = 52.2 + 17.1 + 28.8, net 55.6. |
| I3 | Fixed: medians of net and net excluding valuation are taken from the unrounded computation (29.2). |
| I4 | Fixed: the Table 4 caption explains both pairs (39.6/39.7 for 1976–2020; 35.9/36.0 for 1951–2020, after code-audit E1). |
| I5 | Fixed: 38.0 (1976–2020). |
| I6 | Fixed: "None of these reverses …; equal country weights (48.2 against 38.0) put housing clearly ahead." |
| I7 | Fixed: §3, Table 1 and SOURCES.md now cover the 2024–25 labour-force extension and the fact that the FRED PWT copies are identical to PWT 11.0. |
| I8 | Fixed. The text uses Z.1 for the US path (5.60 in 2023, 6.09 in 2026). The OECD basis (6.0) is labelled where it appears, and the Table 7 note shows both. |
| I9 | Fixed. "Nearly in step" is replaced by "in the same direction", quoting note 3's own "the direction is comparable". The two-decimal values are called "this note's reproduction of note 3's calculation", and the Table 5 row label matches. |
| I10 | Fixed: the balanced-panel medians are computed from the unrounded country series (3.81 for 2021). |
| W1–W4 | Done. |
| W5 | Done: Figure 1 legend and Table A5 say "Macrohistory Database"; Figure 3 title spells out the sector; "non-profits" used throughout; Table 8 says "years of work (= years of GDP)"; Table 9 header says "Dwellings + land". |
| W6 | Done: en dashes in Figures 2 and 4 and Table A5; true minus signs in Figure 5. |
| W7–W14 | Done (W13: "draft" dropped from the lede; W14: Table 2 caption uses "% a year × 10"). |
| Code audit E1 | Applied: the long window is now 1951–2020. The text is rewritten for the bond sign change (+0.8 GDP-weighted, −1.9 median). |
