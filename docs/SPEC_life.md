# §7 "A life" — fixed design (set 2026-10-21 before results)

Countries: the 16 JST countries with housing data. Cohorts: start work at 25 in each year 1950…1980, retire at 65
(year start+40, so 1990…2020). Annual time step, end-of-year flows.

Units: pay_t ∝ national nominal GDP per hour worked (LCU), so wealth / pay_t is "years of own pay" and equals
wealth in national hours up to a constant. Also report in world hours (convert LCU → USD by JST xrusd, divide by
world hour H, rescale by pay at 65 in world hours) — i.e. "years of final pay" and "world hours per hour of own
final pay". National GDP per hour from PWT 11.0 hours (data/clean/pwt110_hours.csv) and World Bank LCU GDP
(data/clean/worldbank_gdp.csv) from 1960; before 1960 use JST nominal GDP per capita growth (state it).

Home: a fixed "standard home" priced at M × annual pay in 2000 (M = 4 baseline; 3 and 6 robustness), price path from
JST hpnom (so price/pay moves with the data). Gross rent = net rent (JST housing_rent_yd × price) + running costs
c × price, c = 2.0% (1.5, 3.0 robustness). Owner pays c × price; renter pays gross rent.

Budget: each year b = 35% of pay goes to housing + saving (25%, 45% robustness). The remainder is consumed and
is identical across rules.

Saving vehicle (default): domestic 60/40 of JST eq_tr / bond_tr in LCU, all years (identical across countries
and cohorts). Variant: GMP in USD unhedged converted to LCU from 1976 (domestic 60/40 before). Variant: bills.

Rules:
- R (rent): pays gross rent each year; saves b·pay − gross rent into the vehicle (negative = withdraw; record if
  the account would go below zero, and flag that cohort as "unaffordable" rather than borrowing).
- O (own): rents and saves as R until age 35, then buys if account ≥ 20% deposit + 3.85% buying cost (else waits,
  record the age). Mortgage = 80% of price, 25-year annuity at JST ltrate + 1.0 pt (fixed at purchase; variable-rate
  variant: reset each year). Thereafter pays mortgage + c·price; saves b·pay − (mortgage + c·price) into the vehicle
  (same non-negativity flag). Wealth at 65 = home − remaining loan + account; also report net of 3.85% selling cost.
- P (pension): on top of R and O, a contribution of τ = 10% of pay (outside the budget b) goes either to (P-payg) a
  wage-indexed PAYG claim whose value grows with the national wage bill (national GDP per hour × total hours worked),
  or to (P-funded) the saving vehicle. Report the ratio funded/PAYG at 65 per cohort.

Outputs: for each country × cohort: wealth at 65 in years of final pay for R, O, P-payg, P-funded; decomposition
contributions vs investment return; the share of O's wealth from housing valuation (rerun O with the rent–price ratio
held at its purchase-year level, i.e. price grows with rent). Summaries: median, interquartile range, min, max across
country×cohort; by cohort decade; GDP-weighted. Figures: (1) O vs R wealth at 65 by cohort (median and range);
(2) PAYG vs funded ratio by cohort and country; (3) one illustrative country path (e.g. USA 1970 cohort) of balance
sheet composition over the life.
Report results that weaken the story. This is a stylised exercise: no taxes, no tax relief, one home type, index ≠ a house.
