# Audit 2: code and data (2026-10-21)

Scope: what CHECK_4_6.md, CHECK_life.md and REVIEW_paper.md did not cover — the fetch/clean step, build_housing_ext.py, build_extras.py, the PAYG average-pay variant, the robustness grids, the build_paper.py key mapping, timing, and a full rerun.
Scripts in this folder: a1_raw_dims.py, a2_trace_values.py (+ .csv), a3_pwt_vintage.py, a4_wb_vintage.py, a5_housing_timing.py (+ .json; run it with HOME set to a scratch copy, because it execs the builder), a6_balance_checks.py (+ .json), a7_valuation_variants.py (+ .json), a8_pwt_breaks.py (+ .csv), and key_contexts.txt (every {{n:key}} with its sentence).
No existing file was modified.

## ERROR

**E1. "1951–2020" national-hour figures actually average 1950–2020, and 1950 uses a proxy hour.**
- *Where:* build_housing.py lines 135–176 (`PERN` (1950, 2020); `national(..., 1950, 2020)`; `PC[("1950-2020", ...)]`). These feed build_paper.py lines 49–51 (`nat50_*`), 141–144 (`cw_*_n`), Table 3 and Table A1 (column "Net 1951–2020"), Table 4 (both "1951–2020" columns), Figure 5 (left panel), and the §4.2, §4.3 and §6.3 text.
- *What happens:* the code includes the 1950 return (1949→1950). For 1950 the national hour falls back, for all 16 countries, to JST GDP per head (`SRC` in 1950 = "JST per capita"). The methods text says that the national hour before 1961 is JST GDP over PWT hours for 1951–1960, and REVIEW item 26 relabelled these columns 1951–2020 on the grounds that "the first annual return needs a 1950 level". That premise is wrong: 1950 is in the sample.
- *Side effect:* the window also includes Australia's anomalous 1950 return (+737 per 1,000 net), the one identity outlier the text names.
- *Mismatch with PAYG:* the PAYG figure set beside these values in §6.3 and Figure 5 (5.1) is a genuine 1951–2020 average, so the side-by-side comparison mixes two windows.
- *Old → new values with a true 1951–2020 window (a5_housing_timing.json):*

| quantity | old | new |
|---|---|---|
| Table 3 / §4.2 GDP-weighted net (`nat50_net`) | 35.4 | 35.9 |
| Median net (`nat50_med`, Table 3 median row) | 39.9 | 40.1 |
| Table 4 / §6.3 / Fig. 5: housing | 35.5 | 36.0 |
| equities | 37.3 | 36.1 |
| government bonds | −0.4 | **+0.8** (sign changes) |
| bills | −12.9 | −12.2 |
| Table 4 medians: housing | 39.9 | 40.1 |
| equities | 35.2 | 34.2 |
| bonds | −2.5 | −1.85 |
| bills | −19.9 | −19.9 |
| Table A1 per country: Australia | — | −9.8 |
| Table A1 per country: Spain | — | +3.6 |
| Table A1: other countries | — | under 2 each |

- *Fix:* either loop over (1951, 2020), or label the columns "1950–2020" and say that 1950 uses GDP per head.
- *Wording:* with the fix, "bonds … lost ground to the hour" no longer holds for the GDP-weighted bond figure (+0.8). The median is still negative, so "in most countries" survives.

No other number in the paper was found to be wrong.

## WEAKNESS (defensible; should be stated)
1. **Dec-to-Dec robustness row** (Table A5; `rb_dec` = 48.2) runs over 1976–2019, because the interpolation needs year t+1. The row label gives no window. The baseline median over the same window is 47.5, so the comparison holds.
2. **Same-year weights** (`ex_sameyear` = 45.3) combine same-year GDP with the same year's end-of-year xrusd. With World Bank annual-average US-dollar GDP, the figure is 42.6. That explains CHECK_4_6's 42.7. The look-ahead from end-year FX is part of the 45.3.
3. **Portfolio-yield valuation of 3.9 is correct.** It is 3.8 with World Bank weights. CHECK_4_6's 3.3 came from that check's own code: the two yield sums used different country sets in years when a country entered.
4. **PAYG average-pay variant** (`pv_avg` = 3.75, `pv_fp_avg` = 2.95):
   - Contributions are 10% of GDP per hour at fixed hours, but the claim is revalued with GDP per hour × actual avh. So the claim earns avh growth relative to the worker's own pay.
   - In a consistent per-worker framing, where pay and contributions both scale with avh, the claim is exactly τ × 40 = 4.00 years of final pay.
   - The 3.75 depends on the framing, and the text should say so.
5. **PAYG as % of GDP** divides by World Bank LCU GDP. Eurostat's own GDP is downloaded (`nama_10_gdp`) but not used. With it, the median is 270 instead of 272; per country the differences are within 1%.
6. **PAYG as % of household net worth** uses S1M net worth (it includes NPISH). The households-only (S14) share would be slightly higher: the median S14/S1M ratio of net financial worth is 0.98.
7. **US 2026 in world hours** (54,541) divides 2026 Q2 net worth by the world hour of 2026-03, the last month available.
8. **Labour share** (1.7 per 1,000) is weighted by PWT cgdpo (PPP). Elsewhere "GDP-weighted" means US dollars, and with US-dollar weights the figure is 1.8 (64.5% → 59.8%). It is also not the PAYG window: 1976–2019 against 1976–2020.
9. **2021–25 extension:** rents come from the CPI actual-rent index, which lags market rents. Part of the 24.4 "valuation" in 2021–25 may be that lag.
10. **Timing of JST house-price growth:** it tracks OECD annual-average growth (correlation 0.97 at lag 0, 0.70 at lead 1), so it is probably mid-year to mid-year, against a Dec-to-Dec hour. Shifting the hour half a year changes the 1976–2020 net from 40.0 to 40.15, which is negligible.
11. **Silent fallbacks:** NLD 1969–70 uses GDP per head, because PWT 11 has no NLD 1969 figure. See also E1.
12. **Stale text (no numbers affected):**
   - SOURCES.md calls the FRED PWT cache "apparently PWT 10.x". It is identical to PWT 11.0 (a3), so national hours and PAYG use the same hours.
   - The build_paper.py docstring says three numbers are parsed from CHECK_4_6.md. None are any more.
   - RESULTS_balance.md still says "falling annual hours cost 4.0" and "8.4 for 2011–23".
   - build_balance.py hard-codes `gmp_world_hours_note3_1976_2026` = 35.0. It is unused in the text.

## OK
- **Raw → clean trace:** 49 traced values are identical across OECD HPI, T720, 9B, Z.1, Eurostat, PWT, WB and WPP (a2_trace_values.csv).
- **Units and filters:** UNIT_MULT = 6 everywhere; XDC; non-consolidated (N); LE stocks; counterpart S1/W; liabilities are positive; T720 BF90 = assets − liabilities. There are no duplicate keys, and maturity/currency filters are correct.
- **Index base:** every 2015 annual value is 100, and only ratios of the index are used.
- **Currency mapping:** EUR is consistent for BGR and HRV in OECD, WB, BIS and Eurostat.
- **Cross-source:** OECD US figures equal Z.1. The WB caches and the clean WB file are identical, and the PWT cache equals PWT 11. There is no German unification break.
- **2021–25 chain:** the 2020 rent yield is continuous (gap 0), the 2021 capital gain equals OECD's, and the fills are listed (Australia's 2025 RPI from quarters; US 2025 RPI from the BLS rent index).
- **Life robustness:** each variant changes only its parameter. The vehicle variant also changes the funded pension, as the text says. 16 anchor-2000 variants have no buyers; the summary statistics handle them.
- **Rerun:** the full pipeline was rerun into a clean scratch copy. The 95 regenerated files are byte-identical to the originals, including household.html and the PNGs, so there is no nondeterminism and no stale CSV.
- **Hand-made files:** the RESULTS_*.md notes and household.pdf are not regenerated. All 385 text numbers appear in the PDF.
- **Sentence check:** every sentence in key_contexts.txt was checked against the source key's period, country set and median-or-mean status. Apart from E1, all match.

---

## Response to audit 2 (2026-10-21; pipeline rerun build_housing → build_housing_ext → build_balance → build_extras → build_life → build_paper; PDF 22 pp)

| item | response |
|---|---|
| E1 | Fixed. build_housing.py long windows are now (1951, 2020) and (1951, 1975). The 1950 GDP-per-head hour and the Australia 1950 return have dropped out. New: GDP-weighted housing 35.9 (Table 3) / 36.0 (Table 4); median 40.1; equities 36.1; bonds +0.8 (sign change); bills −12.1; medians: bonds −1.9, equities 34.2. Text in §4.3 and §6.3 is rewritten (bonds roughly kept pace on GDP-weighted average and lost in the median country). The wrong "first return needs a 1950 level" rationale is gone. build_balance.py now reads the 1951 keys. build_life.py does not use these outputs: it was rerun only for the Figure 7 title, and every life CSV is byte-identical. |
| W1 | Fixed. The row is labelled 1976–2019, and a same-window baseline row was added (47.5; §8 states both). |
| W2 | Fixed. extras.json also reports same-year weights on World Bank average-FX GDP (42.6). §8 gives 42.6 first and 45.3 second, with the end-year-FX look-ahead explained. |
| W3 | No change needed. The 3.9 is kept; World Bank weights give 3.8 (extras.json). |
| W4 | Fixed. §7.3 explains the framing: contributions scale with fixed-hours pay while the claim is revalued with actual hours per worker. If contributions also scaled with hours per worker, the claim would be exactly 4.00. |
| W5 | Fixed. PAYG % of GDP = Eurostat MIO_EUR entitlements / Eurostat nama_10_gdp, falling back to World Bank LCU GDP. The median is now 270 (Summary, §5.3, Table 8 caption). The World Bank version is kept as column S13PS_pct_gdp_wb. |
| W6 | Noted. The Table 8 caption says net worth is S1M (households and non-profits). Not switched to S14 (ratio 0.98). |
| W7 | Fixed. The Table 7 caption says the 2026 world-hour value uses the March 2026 world hour. |
| W8 | Fixed. §6.1 says PPP weights (1.7) and gives the US-dollar-weight figure (1.8), computed in build_extras.py. The 1976–2019 window is stated. |
| W9 | Fixed. §3 now says the CPI rent index lags market rents, so part of the 2021–25 valuation may be that lag. |
| W10 | Not added. The effect is negligible (40.0 → 40.15). |
| W11 | Declined. The NLD 1969–70 fallback affects two country-years and is recorded in build_life's log. |
| W12 | Fixed: SOURCES.md (PWT cache = PWT 11.0; the 2024–25 labour-force extension; the PAYG GDP basis), the build_paper.py docstring, and RESULTS_balance.md (hours per worker −3.4; 2011–20 / 2021–23). The unused hard-coded 35.0 was removed from build_balance.py. |
| Also | Fixed Belgium's components in Table A1 (paper audit I2). Per-country components now use the same years: Belgium 1976 had no rent-yield change. Belgium's 1976–2020 national net is now 55.6 (was 57.6); the components add. |
