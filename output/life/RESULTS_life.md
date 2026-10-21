# Section 7: a life. Results (build_life.py, revision 2, 2026-10-21; exploratory)

**This run corrects the design after the first results were seen.** It is not part of the fixed SPEC_life.md design. The first run followed the spec: the home was priced at 4× pay in 2000. That home cost 5–16 years of pay in the 1950s, so 303 of 476 renters could not pay the rent from their first working year.

The coordinator then changed two things:
- **(a) Home price.** The baseline home now costs **M = 4× pay in the cohort's first working year**, and its price then follows JST hpnom. The 2000 anchor is kept as a robustness row.
- **(b) No flooring.** The account may go negative. A negative balance is charged the national bill rate + 1 pt, under both R and O.

Everything else is as specified:
- 16 countries; 476 of 496 lives (DEU 1950–60 and JPN 1950–58 have no housing data).
- Age 25 at the end of year s, flows in s+1…s+40, wealth in the retirement year.
- Pay is national LCU GDP per hour. Before 1960 it is chained back with JST GDP per head.
- The vehicle is a domestic 60/40 portfolio.
- Gaps filled: ESP, ITA and PRT prices chained back with capgain; BEL 1965–75 rent yield and NLD 1969 hours interpolated.

**Headline.** Units are years of own final pay. Medians are across country×cohort. Columns show all 476 lives, then the 300 lives whose account never went negative.

| | all: median | IQR | GDP-wtd | never-negative: median |
|---|---|---|---|---|
| R: rent and invest | 12.06 | 8.0–18.1 | 12.64 | 14.05 |
| O: buy at 35 (net of sale: 12.64) | 12.79 | 7.9–17.7 | 12.84 | 15.59 |
| O / R | **1.00** | 0.78–1.29 | 1.02 | 1.10 |
| O beats R | 236 of 476 (50%) | | | 59% |
| PAYG claim, 10% of pay | 4.28 | 4.0–4.7 | 4.61 | 4.35 |
| Funded claim, 10% in the 60/40 | 11.09 | 7.9–14.2 | 10.67 | 10.73 |
| **Funded / PAYG** | **2.44** | 1.9–3.2 (funded wins in 95%) | 2.31 | 2.41 |
| **Share of O's wealth from valuation** (rent–price ratio frozen at purchase) | **2.1%** | −1.5%–8.3% | 1.4% | 1.7% |

- **By decade of cohort start (O/R median):** 1950s 1.27, 1960s 1.02, 1970s 0.87, 1980 0.76. Owning won for early cohorts and lost for later ones.
- **Buying age:** median 35; 17 lives never buy.
- **In world hours:** one hour of own final pay buys a median 4.6 world hours. R and O medians are 57.1 and 57.2 years of world-hour pay.
- **USA, 1970 cohort:** R 9.60 vs O 4.75. O buys at 37 and overdraws to −0.52 years of pay.

**Cohort pattern by decade** (decade_O_vs_R_baseline_variable_bills.csv; O/R median and O − R median in years of final pay; decades 1950s, 1960s, 1970s, 1980):

| run | O/R by decade | O − R by decade |
|---|---|---|
| Baseline (fixed rate) | 1.27 / 1.02 / 0.87 / 0.76 | +2.67 / +0.28 / −1.47 / −3.32 |
| Variable-rate mortgage | 1.17 / 1.04 / 0.98 / 0.95 | +2.03 / +0.41 / −0.26 / −0.91 |
| Bills vehicle | 1.43 / 1.50 / 1.49 / 1.46 | +2.56 / +3.08 / +2.41 / +1.58 |

- **Variable rates.** The slope shrinks to about a third. Fixed-rate debt taken out before the 1970s inflation was eroded. Fixed rates locked in around 1980 were not refinanced as rates fell. For example, the USA 1970 cohort bought in 1982 at 14.0%.
- **Bills.** The slope almost disappears. Most of the cohort pattern comes from the 60/40 vehicle's strong 1980–2020 returns, which raise the cost of the forgone return for later cohorts.

**PAYG variants (added after referee review; summary_payg_variants.csv).** Two ways of revaluing the PAYG claim:
- **Wage bill (the main claim):** grows with national GDP per hour × total hours. This is the sustainable Samuelson–Aaron (NDC-like) return.
- **P-payg-avg:** grows with GDP per hour × PWT average hours per worker, i.e. average pay per worker, as in points or earnings-indexed systems. Before 1960, average-hours growth is held at 0.

Medians across 476 lives:

| | PAYG claim (years of final pay) | 60/40: funded/PAYG (funded wins) | GMP | Bills |
|---|---|---|---|---|
| Wage bill | 4.28 | 2.44 (95%) | 1.88 (98%) | 0.92 (27%) |
| Average pay per worker | 3.76 | 2.95 (97%) | 2.20 (99%) | 1.05 (58%) |

The average-pay claim is smaller because hours per worker fell while employment rose.

World GDP-weighted growth of average hours per worker (method as build_balance.py §6f), per 1,000 hours a year:

| period | all countries | JST 16 | balance table `avh_all` | balance table `avh_drag` (hours − employment) |
|---|---|---|---|---|
| 1951–2023 | −3.36 | −3.6 | −3.4 | −4.0 |
| 1976–2020 | −3.57 | −3.5 | −3.6 | −4.4 |

`avh_drag` differs from `avh_all` because the yearly country sample with total hours is not the same as the sample with average hours. Check: the P-payg-avg claim equals τ·Σ(avh₆₅/avh_t) to 4e-15.

**Negative balances.** 176 lives go negative at some point: 128 under R, 176 under O, and every R case is also an O case. The median minimum is −0.26 years of pay (R −0.20, O −0.26).
- **By country:** FIN 31, NOR 29, SWE 24, NLD 16, FRA 14, AUS 13, others ≤11.
- **Twelve lives end below zero.**
  - **France, 1950–57 cohorts:** as low as −12.9. JST's French price/pay goes from 4 to 15 between 1951 and 1965 with a 5.5% net rent yield, so rent exceeds a full year's pay.
  - **Others:** FIN 1950 and 1978, NOR 1975 and 1979.

**Why O/R ≈ 1.** Medians across the 459 buyers, in years of final pay:

| item | median | mean |
|---|---|---|
| Home price gain | +2.20 | +2.50 |
| Imputed rent saved (gross) | +3.16 | +3.23 |
| Running costs | −0.94 | −1.05 |
| *Net rent saved (gross rent − running costs)* | *+2.14* | |
| Mortgage interest | −1.10 | −1.20 |
| Buying cost | −0.03 | −0.03 |
| Forgone 60/40 return on the deposit and extra outlays | −2.76 | −3.52 |
| **O − R** | **+0.08** | **−0.08** |

The means add up exactly. In words: the home's price gain plus rent saved, net of running costs, is about 4.3 years of pay. Interest plus the forgone 60/40 return take almost all of it back.

**The 2000-anchored home: price in years of pay** (price_to_pay_standard_2000_home.csv, fig_4). Medians across countries:

| year | 1950 | 1960 | 1970 | 1980 | 1990 | 2000 | 2010 | 2020 |
|---|---|---|---|---|---|---|---|---|
| price / pay | 6.5 | 6.0 | 5.3 | 4.8 | 4.5 | 4.0 | 5.0 | 5.1 |

- Price/pay fell by half from 1950 to 2000, about −0.36% a year in the median from 1950 to 2020. House prices (an index, roughly constant quality) grew slower than pay, consistent with §4's finding that rent grew slower than the national hour.
- **The drift is not monotone.** Price/pay rose by about a quarter after 2000.

**Robustness on the new baseline** (median O/R · O beats R · valuation share · lives going negative):

| change | median O/R | O beats R | valuation share | lives negative |
|---|---|---|---|---|
| M 3 | 1.04 | 58% | 1% | 37 |
| M 6 | 1.00 | 21% | 5% | 415 (239 never buy) |
| c 1.5% | 1.03 | 53% | 2% | 141 |
| c 3% | 0.96 | 39% | 2% | 258 |
| b 25% | 1.00 | 29% | 8% | 391 |
| b 45% | 1.05 | 57% | 1% | 40 |
| GMP vehicle (from 1976) | 1.16 | 63% | 3% | 176 |
| Bills | 1.48 | 80% | 5% | 200 |
| Variable-rate mortgage | 1.02 | 53% | 2% | 182 |
| **Spec's 2000 anchor** | 1.00 | 30% | 12% | 346 (158 never buy; median R 3.8 vs O 4.2) |

- **Funded/PAYG** is 2.44 in every housing variant. It is 1.88 with the GMP and **0.92 with bills**, where funded wins in only 27% of lives.
- **Full grid** (324 runs; 162 per anchor):
  - Entry anchor: O beats R in 2–95% of lives (median 58%), and the median valuation share ranges from −15% to 12%.
  - 2000 anchor: O beats R in a median 30% of lives, with a valuation share of 11%.

**Checks (build_log.json).** All within 1e-14:
- With all rates set to zero, R wealth equals Σ(b·pay − rent) exactly for all 476 lives.
- With zero returns, funded wealth equals τ·Σpay.
- The PAYG claim in years of final pay equals τ·Σ(N₆₅/N_t).
- The O, R and O−R decompositions add up.
- Price/pay at entry equals 4.
- A 25-year annuity leaves no balance.

**What weakens the story**
1. Owning versus renting is a coin toss on the baseline. The answer depends on the vehicle (bills or GMP favour O) and on cohort (O won for the 1950s and lost for the 1970s). The valuation share is small (2%). The 2000-anchor run gives a larger valuation share (12%) only because buyers there are later and more leveraged on the post-2000 rise.
2. The baseline was chosen after the results were seen. The spec's design gives much lower wealth (median about 4 years of pay) because the fixed home was unaffordable before about 1980.
3. FIN, NOR and SWE rent yields (gross 8–9% of price) make most lives overdraw. French post-war price/pay (×4 by 1965) produces large debts. These come from JST levels and may reflect rent-control-era data.
4. Funded beats PAYG only through the domestic 60/40 return. PAYG is valued at its indexation return, not at real benefit rules. There are no taxes, tax relief or survival risk, and an index is not a house.
