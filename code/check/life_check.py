# -*- coding: utf-8 -*-
"""Independent re-implementation of section 7 "A life", baseline only (revision 2), written from SPEC_life.md and
RESULTS_life.md without reading code/build_life.py.  Countries USA JPN GBR FRA SWE, cohorts 1950..1980.

My reading of the design:
  age 25 at end of year s, account 0; working years t = s+1..s+40; wealth at end of s+40.
  pay_t = WB LCU nominal GDP / PWT total hours (from 1960); before 1960 chained back with JST gdp/pop growth.
  home price P_t = 4 * pay_{s+1} * hpnom_t / hpnom_{s+1}  (4x pay in first working year).
  gross rent_t = (housing_rent_yd_t + c) * P_t, c = 2%.
  vehicle return r_t = 0.6 eq_tr_t + 0.4 bond_tr_t; a negative opening balance earns -(bill_rate_t + 1pt).
  A_t = A_{t-1}(1+r_t) + b pay_t - outlay_t   (end-of-year flows, b = 35%).
  O: buy at end of s+10 (age 35) or first later year-end with A >= (0.20+0.0385) P; loan 0.8 P,
     25y annuity at ltrate_buy + 1pt; from next year outlay = annuity + c P_t (annuity stops after 25 payments).
  PAYG claim: C_t = C_{t-1} * Y_t/Y_{t-1} + tau pay_t, Y = pay*hours (national nominal wage bill), tau = 10%.
  Funded: F_t = F_{t-1}(1+r_t) + tau pay_t.  All wealth / pay_{s+40}.
Variant flags let me test alternative timing readings.
"""
import sys
import numpy as np, pandas as pd

import os as _os, sys as _sys; _C = _os.path.dirname(_os.path.abspath(__file__)); _sys.path.insert(0, _os.path.abspath(_os.path.join(_C, '..')))
from paths import R as _R, RAW as _RAW, DC as _DC, CN as _CN, JSTF as _JSTF, GMPR as _GMPR, cnd as _cnd, PWTX   # release: repository-relative paths (code/paths.py)
ROOT = _R
JST = _JSTF
CTRY = ['USA', 'JPN', 'GBR', 'FRA', 'SWE']
B, C, TAU, M, DEP, BUYC, SPREAD, NYR = 0.35, 0.02, 0.10, 4.0, 0.20, 0.0385, 0.01, 25

ENTRY = sys.argv[1] if len(sys.argv) > 1 else 's+1'   # year whose pay sets the price ('s' or 's+1')

jst = pd.read_excel(JST)
pwt = pd.read_csv(f'{_DC}/pwt110_hours.csv')
wb = pd.read_csv(f'{_DC}/worldbank_gdp.csv')


def series(iso):
    d = jst[jst.iso == iso].set_index('year').sort_index()
    h = pwt[(pwt.iso3 == iso) & (pwt.variable == 'hours_total_m')].set_index('year')['value']
    y = wb[(wb.iso3 == iso) & (wb.variable == 'NY.GDP.MKTP.CN')].set_index('year')['value'].sort_index()
    yrs = range(1950, 2021)
    df = pd.DataFrame(index=yrs)
    df['H'] = h.reindex(yrs).interpolate()
    df['Y'] = y.reindex(yrs)
    df['pay'] = df.Y / df.H
    # chain pay before 1960 with JST nominal GDP per head
    gpc = (d.gdp / d['pop']).reindex(yrs)
    for t in range(1959, 1949, -1):
        df.loc[t, 'pay'] = df.loc[t + 1, 'pay'] * gpc[t] / gpc[t + 1]
    df['Wbill'] = df.pay * df.H
    df['hp'] = d.hpnom.reindex(yrs)
    df['yd'] = d.housing_rent_yd.reindex(yrs)
    df['r'] = 0.6 * d.eq_tr.reindex(yrs) + 0.4 * d.bond_tr.reindex(yrs)
    df['bill'] = d.bill_rate.reindex(yrs)
    df['ltr'] = d.ltrate.reindex(yrs) / 100
    return df


def annuity(L, i, n=NYR):
    return L * i / (1 - (1 + i) ** -n)


def life(df, s):
    T = range(s + 1, s + 41)
    e = s + 1 if ENTRY == 's+1' else s
    if df.loc[list(T) + [e], ['hp', 'yd', 'r', 'bill', 'pay']].isna().any().any():
        return None
    P = {t: M * df.pay[e] * df.hp[t] / df.hp[e] for t in range(s, s + 41)}

    def grow(A, t):
        return A * (1 + (df.r[t] if A >= 0 else df.bill[t] + SPREAD))  # debt accrues bill + 1pt
    # R
    A = 0.0; mnR = 0.0
    for t in T:
        A = grow(A, t) + B * df.pay[t] - (df.yd[t] + C) * P[t]
        mnR = min(mnR, A)
    WR = A / df.pay[s + 40]
    # O
    A = 0.0; owned = False; loan = 0.0; pmt = 0.0; npaid = 0; buy_age = np.nan; mnO = 0.0
    for t in T:
        if not owned:
            A = grow(A, t) + B * df.pay[t] - (df.yd[t] + C) * P[t]
        else:
            pay_m = pmt if npaid < NYR else 0.0
            if pay_m:
                loan = loan * (1 + i) - pmt; npaid += 1
            A = grow(A, t) + B * df.pay[t] - pay_m - C * P[t]
        mnO = min(mnO, A)
        age = 25 + (t - s)
        if (not owned) and age >= 35 and t < s + 40 and A >= (DEP + BUYC) * P[t]:
            owned = True; buy_age = age
            i = df.ltr[t] + SPREAD
            loan = (1 - DEP) * P[t]; pmt = annuity(loan, i)
            A -= (DEP + BUYC) * P[t]
    home = P[s + 40] if owned else 0.0
    WO = (home - loan + A) / df.pay[s + 40]
    # pensions
    Cp = 0.0; F = 0.0
    for t in T:
        Cp = Cp * df.Wbill[t] / df.Wbill[t - 1] + TAU * df.pay[t]
        F = F * (1 + df.r[t]) + TAU * df.pay[t]
    return dict(W_R=WR, W_O=WO, W_payg=Cp / df.pay[s + 40], W_funded=F / df.pay[s + 40], buy_age=buy_age,
                R_min=mnR / df.pay[s + 40], O_min=mnO / df.pay[s + 40])


rows = []
for c in CTRY:
    df = series(c)
    for s in range(1950, 1981):
        out = life(df, s)
        if out:
            rows.append(dict(country=c, cohort=s, **out))
mine = pd.DataFrame(rows)
mine.to_csv(f'{_C}/life_check_mine_{ENTRY.replace("+", "p")}.csv', index=False)
ref = pd.read_csv(f'{ROOT}/output/life/life_cohorts_baseline.csv')
m = mine.merge(ref[['country', 'cohort', 'W_R', 'W_O', 'W_payg', 'W_funded', 'buy_age']], on=['country', 'cohort'],
               suffixes=('', '_ref'))
print('lives compared', len(m), 'of mine', len(mine))
for k in ['W_R', 'W_O', 'W_payg', 'W_funded']:
    d = (m[k] / m[k + '_ref'] - 1)
    big = m[(d.abs() > 0.02)]
    print(f'{k}: max |rel diff| {d.abs().max():.2e}, median {d.abs().median():.2e}, >2%: {len(big)}')
    if len(big):
        print(big[['country', 'cohort', k, k + '_ref']].head(12).to_string())
print('buy age mismatches', int(((m.buy_age != m.buy_age_ref) & ~(m.buy_age.isna() & m.buy_age_ref.isna())).sum()))
