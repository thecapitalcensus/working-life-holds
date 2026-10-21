# Verification of the audit-2 fixes (2026-10-21)

The coordinator's fixes check out. Two small loose ends remain; see the bottom of this file.

## 1. E1: the long window is now 1951–2020 — confirmed

**In the code.** `build_housing.py` now uses (1951, 2020) and (1951, 1975) for the long windows. No other 1950–2020 window remains in the code. The only remaining 1950 references are in `build_life.py`, for the price/pay figure (Table 15, 1950–2020), which is a legitimate use.

**In the outputs and text.** The printed values match my table:

| Item | Value |
|---|---|
| Table 3, GDP-weighted | 35.9 |
| Median | 40.1 |
| Table 4 / §6.3: housing | 36.0 |
| Equities | 36.1 |
| Government bonds | +0.8 |
| Bills | −12.1 (I gave −12.15; this is a rounding difference) |
| Medians: equities | 34.2 |
| Medians: bonds | −1.9 |
| Medians: bills | −19.9 |
| PAYG (`build_balance` reads the 1951 keys) | 5.1 |

**Cleanup.** The keys `nat50_net`, `nat50_med` and `cw_*` changed as expected, and the "first return needs a 1950 level" rationale is gone.

## 2. Belgium fix: Table A1 now adds up

**Table A1.** Belgium's components now add up: 52.2 + 17.1 + 28.8 = 98.1, against a total of 98.0, which is within rounding. Across all countries the largest gap between the components and the total is 0.1.

**Nothing else moved.** Per-country 1976–2020 values for the other 15 countries are unchanged. Tables `table_housing_national_hours*.csv` and `table_hour_return_by_claim.csv` are unchanged on every row they shared with the old version; the only differences are the new 1951 rows.

**Minor new inconsistency.** Table 9 "Housing alone" for Belgium still shows 57.6, because `table_claims_by_country_national_hours.csv` keeps the 1976 return. Table A1 now gives 55.6. This is the only per-country difference between the two files (+2.0 for BEL). Medians are unaffected. Either align the two files or note it in the Table 9 caption.

## 3. New numbers are computed, not typed

Each of the following comes from code:

| Number | Where it is computed |
|---|---|
| `ex_sameyear_wb` 42.6 | `extras.json` `same_year_weights_wb_avg_fx` |
| `ex_sameyear` 45.3 | `extras.json` |
| `rb_dec_base` 47.5 and `rb_dec` 48.2 | robustness CSV rows |
| `ls_eff` 1.7 and `ls_eff_usd` 1.8 | `extras.json` |
| `ls_mean` 62, `earn_home` 6.5, `earn_budget` 57 | `extras.json`: 4 / L and 35 / L, where L is the mean labour share 1951–2019 |
| `us_yrs_g23` 0.60 and `us_avh_g` 0.20 | `build_paper` lines 220–221, from the Z.1 output |
| `us_hrs_g` 0.41 | unchanged |
| `pg_med` 270 | `build_balance`, Eurostat GDP |

## 4. Fresh rerun: byte-identical

I copied the project to a new scratch folder, `audit_copy2`, and ran the whole pipeline from `fetch_*` to `build_paper`. All 95 regenerated files are byte-identical to the current outputs, including the HTML, the PNGs and `numbers_in_text.json`. Four files are not regenerated: the hand-written `RESULTS_*.md` files and `household.pdf`.

## 5. PDF scan: nothing broken

**Old numbers.** None of 272, 0.69, 37.3 or "1950-2020" remains as a value for the old quantities. Where 35.4, 39.9, −0.4, 57.6 or 10,890 still appear, they are other quantities:
- 35.4: the 2001–20 net, and a Portugal cell.
- 39.9: France.
- −0.4: France's hours.
- 57.6: Belgium in Table 9 (see section 2 above), and a world-hours median in Table 12.
- 10,890: the 2026 US hours in Table 7.

**Cross-references and layout.** Every Table and Figure reference has a matching caption. The only "Table" references without one are Table 29 and Table 720, which are the names of the Eurostat and OECD source tables. The PDF has 22 pages and no unfilled {{…}} placeholders.

## Remaining loose ends

1. Belgium shows 57.6 in Table 9 against 55.6 in Table A1.
2. Optional: §7.2 still says "Over 1950–2020 their returns were close" (home vs 60/40, the life section). This is a loose qualitative statement, not a computed number.
