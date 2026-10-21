# Check of section 7 "A life" (baseline, revision 2), 2026-10-21

Checker's script: `check/life_check.py`. I wrote it from SPEC_life.md and RESULTS_life.md before reading `code/build_life.py`. Output is in `check/life_check_mine_sp1.csv`.

## 1. Replication

**Scope:** USA, JPN, GBR, FRA and SWE, all cohorts 1950–1980, which gives 146 lives. JPN 1950–58 drop out in both versions because the rent yield is missing. I took these inputs:
- **Pay:** World Bank LCU GDP divided by PWT total hours, chained back before 1960 with JST GDP per head.
- **Home price:** 4 × pay in year s+1, then follows hpnom.
- **Rent:** gross rent = (rent_yd + 2%) × P.
- **Vehicle:** 60/40 of eq_tr and bond_tr. A negative balance accrues the bill rate + 1 pt.
- **Flows:** at the end of each year.
- **Buying:** buy at the end of s+10 if the account holds at least 23.85% of P. The loan is 80% of P, as a 25-year annuity at ltrate + 1 pt.
- **PAYG:** the claim grows with pay × hours.
- **Funded:** the account grows with the 60/40 return.

| quantity | max relative difference | lives > 2% |
|---|---|---|
| W_R | 1.4e-5 | 0 |
| W_O | 1.4e-5 | 0 |
| W_payg | 1.4e-6 | 0 |
| W_funded | 1.1e-6 | 0 |
| buy age | — | 0 mismatches |

The differences are only the 5-decimal rounding of the CSV.

Two points from my first pass:
- **Debt sign.** My first pass found 18 R and 31 O lives off by more than 2%. That came from a sign error in my own code: debt shrank instead of growing. After I fixed it, everything matches.
- **Anchor year.** Anchoring the price to pay in year s instead of s+1 gives differences of 5–10% in 126 lives. So "first working year" means s+1, which is the age-26 year. The text should say this.

I also recomputed the RESULTS headline figures from the full 476-life CSV:
- Medians: R 12.06, O 12.79, O/R 1.00, PAYG 4.28, funded 11.09, funded/PAYG 2.44 (funded wins in 95% of lives), valuation share 2.1%.
- O beats R in 236 of 476 lives.
- Negative balances: 176, 128 and 176. No life goes negative under R only.
- 12 lives end below zero and 17 lives never buy.
- USA 1970: R 9.60, O 4.75, buys at 37, lowest balance −0.52.
- Decade medians: 1.27, 1.02, 0.87, 0.76.
- The mean O−R decomposition adds up exactly.

All of these match RESULTS.

## 2. Design review (after reading build_life.py)

**Timing.** Flows come at the end of each year and the return is earned on the opening balance, for R, O, funded and PAYG alike. Consistent.
- The purchase-year rent is paid as a renter. The deposit and buying cost leave the account at the end of that year, and the first instalment falls a year later.
- Buying at age 35 gives 25 payments, ending at 60. A later buyer carries a loan balance at 65, which is netted off.
- No error.

**Mortgage annuity.** The code re-amortises each year with `annuity(L, i, TERM − n_paid)`. At a fixed rate this equals the original payment, and my constant-payment version matches to 1e-5. The variable-rate variant re-amortises over the remaining term, which is a standard choice. The i = 0 case is guarded. Correct.

**Rent and the owner's implicit rent.**
- The renter pays (yd + c)·P.
- The owner pays c·P plus the mortgage, and gains the capital gain only, from hpnom rather than housing_tr.
- The owner's implicit return is therefore net rent yd·P plus the price gain, with no double count.
- This relies on JST housing_rent_yd being a net yield, as the spec assumes. If it were gross, owners would be undercharged by c and renters overcharged by c.

**Units.**
- pay_t = LCU GDP per hour, normalised to 2000 = 1. Price, budget and contributions all scale with pay_t, so W / pay₆₅ is free of scale. It reads as years of pay, with annual pay proportional to GDP per hour, i.e. hours per worker held fixed.
- It is not years of actual annual earnings: falling hours per worker (FRA, JPN, SWE) are ignored. That is acceptable but should be said once.
- World-hour conversion: W × q₆₅, with q = own LCU hour ÷ end-year xrusd ÷ world hour. Euro legacy units are handled correctly (WB LCU is in euros, JST xrusd in legacy currency, divided by the fixed rates).

**PAYG growth.** The claim grows with PAY × NH, which is national GDP per hour × total hours, as the spec says.
- In years of final pay this reduces to τ·Σ H₆₅/H_t. That is independent of the pay path, so the pre-1960 per-head chaining does not affect PAYG.
- The chaining does affect the funded and R/O figures of the 1950–58 cohorts slightly. Per the log, it runs 0.54 pp a year below JST GDP per PWT hour over 1951–59.

**Decomposition.** I checked it algebraically:
- O − R = (P₆₅ − P_buy) + gross rent saved − running costs − interest − buying cost − (R return − O return).
- Principal repaid cancels against the lower remaining loan.
- The deposit plus the loan equals P_buy.
- The identity gap is exactly 0 in the CSV.
- The label "forgone return on the deposit and extra outlays" is loose: that term also includes the different overdraft interest paid under O and R.

**Points to state, not errors.**
1. **The O/R ratio.** It is safe here because the 12 lives with wealth ≤ 0 all never buy, so O/R = 1. Any variant with a negative W_R and a buyer would make the ratio meaningless. The O−R difference is the safer headline.
2. **Overdraft cost.** The overdraft costs the bill rate + 1 pt, which is usually below the mortgage rate (ltrate + 1). An owner who overdraws therefore borrows more cheaply than the mortgage. The 176 O overdraft lives get cheap unsecured credit, which flatters both O and R in FIN, NOR, SWE and FRA.
3. **Valuation share.** The counterfactual also scales running costs c·P down with the counterfactual price, so the "valuation share" includes a small running-cost effect.
4. **Anchor year.** The price anchor year is s+1 (age 26), not s.

## Verdict

The numbers reproduce exactly (all 146 lives within 1.4e-5). I found no coding or design error that must be fixed. Wording fixes:
- the anchor year (s+1);
- "pay" meaning GDP per hour at constant hours per worker;
- the "forgone return" label;
- the cheap-overdraft caveat.
