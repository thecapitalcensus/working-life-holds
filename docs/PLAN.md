# Note 4 — plan (exploratory, not pre-registered; written 2026-10-21 before any result was computed)

Working title: **"What a Working Life Holds: The Home, the Pension and the Portfolio in Hours of the World's Work"**
Promised in note 3 §7: take the world hour to the household balance sheet — home, pension claims and the
investable portfolio together, over a working life — and ask of a life what note 3 asked of a market:
what is generated, what is paid, what is needed to stand still.

## Core idea
A household holds four kinds of claim, and each has its own return *in hours of work*:

| claim | return in hours (identity) | note-3 analogue |
|---|---|---|
| Investable portfolio (GMP) | GMP TR − growth of the hour | note 3: 3.5%/yr 1976–2026 |
| Home | net rent yield + rent growth + Δ(price/rent) − hour growth | §7 left open |
| Pay-as-you-go pension (wage-indexed) | ≈ growth of total hours worked (Samuelson–Aaron: return = growth of the wage bill; in hours the wage-per-hour part cancels) | new |
| Deposits / nominal bonds | interest − hour growth | note 3 bond rows |

The PAYG point is the conceptual contribution: a wage-indexed pension claim is the one asset that is denominated
in hours by construction; its hour return is the growth of the number of hours worked, i.e. demography.

## Sections
1. The question (life vs market; the four claims).
2. Definitions: world hour (note 2), national hour (that country's nominal GDP per hour worked, LCU), years of
   own pay; generated / paid / needed to stand still, as in note 3.
3. Data.
4. **The home in hours** (Table 3 analogue). JST R6, 16 countries with housing returns, GDP(USD)-weighted;
   1976–2020 main window to match note 3 (also 1950–2020 in national hours where the world hour is absent).
   Per 1,000 hours of housing capital: generated = net rent + price; price = rent growth (price ex valuation)
   + change in rent–price ratio (valuation); needed = hour growth; net. Both world hours (USD) and national
   hours (LCU). Extend 2021–2025 with OECD analytical house price indicators (HPI and rent index) if feasible.
   Housing vs GMP side by side; by decade; by country (dispersion).
5. **The aggregate household balance sheet in hours.** Composition (dwellings+land, pension & insurance
   entitlements, equity & fund shares, deposits & debt securities, liabilities) for OECD countries with
   financial + non-financial balance sheets; US back to the 1950s from Fed Z.1. Net worth per worker in
   national hours (hours of the country's own work) and its growth; share of each claim. Where available,
   PAYG (social-security) entitlements from the Eurostat/national-accounts supplementary pension table, to
   show the size of the claim the standard balance sheet omits.
6. **The pension in hours.** Implicit PAYG return = growth of total hours worked (PWT employment × average hours)
   per country and world (GDP-weighted), 1950–2023; compare with the hour returns of the home and the GMP;
   note dependency-ratio projection (UN WPP working-age population) as the forward-looking part, labelled as
   projection, not data.
7. **A life.** Stylised cohorts: enter work at 25, retire at 65, in each JST country, cohorts starting 1950…1980
   (retire 1990…2020). Pay = national hour × hours (pay grows with the national hour). Fixed budget share of pay
   for housing + saving. Rules: (R) rent and invest the rest in the GMP (USD, unhedged; national bills before 1976
   unless GMP proxy available — decide in build, state it); (O) buy at 35 with 80% LTV, mortgage at JST
   long rate + spread, maintenance inside net rent, transaction cost 7.7% round trip; (P) part of saving into a
   PAYG claim earning hours growth. Outcome: wealth at 65 in years of own final pay and in world hours; what share
   came from contributions vs returns vs valuation. Distribution across countries and cohorts, not a single number.
8. What it means / what it does not (no tax, no leverage costs beyond mortgage rate, index ≠ a house, survivorship).
9. Robustness: transaction costs, property tax 1pt, LTV, start/end ages, world vs national hour, OECD vs JST HPI,
   GDP vs equal weights.

## Rules for the work
- Free public data only; record URL, retrieval date, licence (JST = CC BY-NC-SA → derived series share-alike).
- Reuse note-3 inputs unchanged (frozen engine ~/gmp_bt_b61, world hour ~/composite_numeraire/output); record hashes.
- Same style and pipeline as note 3 (HTML template → PDF via headless Chrome), plain English, no jargon.
- Report everything computed, including results that weaken the story.
