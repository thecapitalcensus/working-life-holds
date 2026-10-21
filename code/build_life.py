# -*- coding: utf-8 -*-
"""Note 4, section 7: a life.  Stylised cohorts (work 25 -> 65) in the 16 JST housing countries, cohorts 1950..1980,
following the fixed design in SPEC_life.md (set before results).  Exploratory, not pre-registered.  Outputs: output/life/.

Timing convention (annual, end-of-year flows): age 25 at end of year s (account = 0); working years t = s+1 .. s+40;
end of year s+40 = age 65 = the retirement year 1990..2020 named in the spec.  Buy decision at end of year s+10 (age 35).
Units: pay_t = national nominal GDP per hour (LCU) / its 2000 value, so a 2000 pay = 1; wealth / pay_{s+40} = years of
own final pay (= national hours up to the constant hours-per-year).  World hours: q = own hour in USD / world hour H.
Loaders follow code/build_housing.py (JST R6, world hour H as note 3 build_v2.py, GMP monthly TR).  No network."""
import os, json, hashlib, itertools, numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

from paths import B, JSTF, CN, GMPC, GMPR, DC, PWTX, SITE_CSS, cnd, label   # release: input locations (env-var overrides) and log labels, see paths.py
OUT = os.path.join(B, "output", "life"); os.makedirs(OUT, exist_ok=True)
PWTF = os.path.join(DC, "pwt110_hours.csv"); WBF = os.path.join(DC, "worldbank_gdp.csv")
WHF, WLF = os.path.join(CN, "world_yardsticks_usd.csv"), os.path.join(CN, "world_q_gdp_per_hour_level_usd.csv")
INPUTS = [JSTF, GMPR, PWTF, WBF, WHF, WLF]
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
LOG = {"inputs_sha256": {label(p): sha(p) for p in INPUTS}, "notes": []}
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False})
PAL = ["#1f4e79", "#6b8e6b", "#c98a2b", "#7f9fbf", "#8c4a3c", "#3b3b8f"]
HC = ['AUS', 'BEL', 'CHE', 'DEU', 'DNK', 'ESP', 'FIN', 'FRA', 'GBR', 'ITA', 'JPN', 'NLD', 'NOR', 'PRT', 'SWE', 'USA']
Y = np.arange(1945, 2021)
COHORTS = list(range(1950, 1981))

# ------------------------------------------------------------------ 1. JST
d = pd.read_excel(JSTF)
def pv(v): return d.pivot(index="year", columns="iso", values=v).sort_index().reindex(Y)[HC]
HP, CG, YD, LT = pv("hpnom"), pv("housing_capgain"), pv("housing_rent_yd"), pv("ltrate")
EQ, BOND, BILL, FX, GDP, POP = pv("eq_tr"), pv("bond_tr"), pv("bill_rate"), pv("xrusd"), pv("gdp"), pv("pop")
# price index: hpnom; where hpnom is missing in early years, chain it backwards with housing_capgain (ESP<1971, ITA<1970, PRT<1988)
lhp = np.log(HP); lcg = np.log1p(CG); filled = {}
for c in HC:
    s = lhp[c].copy(); f0 = s.first_valid_index(); n = 0
    for y in range(f0 - 1, Y[0] - 1, -1):
        if pd.notna(lcg.loc[y + 1, c]): s.loc[y] = s.loc[y + 1] - lcg.loc[y + 1, c]; n += 1
        else: break
    lhp[c] = s; filled[c] = n
LOG["price_backfilled_years_with_capgain"] = {c: n for c, n in filled.items() if n}
PRICE_IDX = np.exp(lhp)
# rent yield: interpolate internal gaps in log (BEL 1965-75); leading gaps (DEU <1962, JPN <1960) are not filled -> those cohorts drop
YDi = np.exp(np.log(YD).interpolate(limit_area="inside"))
LOG["rent_yield_interpolated"] = {c: [int(y) for y in YD.index[YD[c].isna() & YDi[c].notna()]] for c in HC if (YD[c].isna() & YDi[c].notna()).any()}
BILLi = BILL.interpolate(limit_area="inside"); LOG["bill_rate_interpolated"] = {c: [int(y) for y in BILL.index[BILL[c].isna() & BILLi[c].notna()]] for c in HC if (BILL[c].isna() & BILLi[c].notna()).any()}

# ------------------------------------------------------------------ 2. national hour (pay), total hours
p = pd.read_csv(PWTF); p = p[p.iso3.isin(HC)]
NH = p[p.variable == "hours_total_m"].pivot(index="year", columns="iso3", values="value").reindex(Y)[HC] * 1e6     # hours a year
LOG["pwt_hours_interpolated"] = {c: [int(y) for y in NH.index[NH[c].isna()] if 1950 < y < 2023] for c in HC if NH[c].loc[1951:2022].isna().any()}   # NLD 1969 missing in PWT 11.0
NH = np.exp(np.log(NH).interpolate(limit_area="inside"))
w = pd.read_csv(WBF); w = w[w.iso3.isin(HC)]
WCN = w[w.variable == "NY.GDP.MKTP.CN"].pivot(index="year", columns="iso3", values="value").reindex(Y)[HC]
WCD = w[w.variable == "NY.GDP.MKTP.CD"].pivot(index="year", columns="iso3", values="value").reindex(Y)[HC]
GDPH = WCN / NH                                                                   # LCU per hour, 1960-2020 (WB/PWT 11.0)
# before 1960: chain back with JST nominal GDP per capita growth (spec)
lg = np.log(GDPH); gpc = np.log(GDP / POP).diff()
for c in HC:
    for y in range(1959, Y[0] - 1, -1): lg.loc[y, c] = lg.loc[y + 1, c] - gpc.loc[y + 1, c]
GDPH = np.exp(lg); assert GDPH.loc[1950:2020].notna().all().all()
PAY = GDPH / GDPH.loc[2000]                                                       # pay_2000 = 1
assert NH.loc[1950:2020].notna().all().all()
WAGEBILL = PAY * NH                                                               # national GDP per hour x total hours (index)
AVH = p[p.variable == "avh"].pivot(index="year", columns="iso3", values="value").reindex(Y)[HC]
LOG["pwt_avh_interpolated"] = {c: [int(y) for y in AVH.index[AVH[c].isna()] if 1960 < y < 2023] for c in HC if AVH[c].loc[1961:2022].isna().any()}
AVH = np.exp(np.log(AVH).interpolate(limit_area="inside"))
for c in HC: AVH.loc[:1959, c] = AVH.loc[1960, c]                                   # pre-1960: avh growth held at 0 (P-payg-avg variant)
assert AVH.loc[1950:2020].notna().all().all()
AVGPAY = PAY * AVH                                                                  # pay per worker = national GDP per hour x average hours per worker
# robustness note: JST GDP / PWT hours 1951-59 vs JST per capita
_alt = np.log(GDP / NH).diff().loc[1951:1959]; LOG["pre1960_pay_growth_percap_minus_JST_GDP_per_PWT_hour_pct_mean"] = round(float((gpc.loc[1951:1959] - _alt).stack().mean() * 100), 3)

# euro legacy units: JST xrusd is in legacy currency per USD throughout; World Bank LCU is euro -> convert
EURO = {"BEL": 40.3399, "DEU": 1.95583, "ESP": 166.386, "FIN": 5.94573, "FRA": 6.55957, "ITA": 1936.27, "NLD": 2.20371, "PRT": 200.482}
FXL = FX.copy()
for c, k in EURO.items(): FXL[c] = FX[c] / k
_chk = (FXL / (WCN / WCD)).loc[1990:2020]; LOG["xrusd_end_year_over_WB_implied_avg_fx_1990_2020"] = {"median": round(float(_chk.stack().median()), 3), "min": round(float(_chk.stack().min()), 3), "max": round(float(_chk.stack().max()), 3)}

# world hour H (note 3 build_v2.py:112-119), December values
wh = pd.read_csv(WHF, index_col=0, parse_dates=True)["gdph"]; lvl = pd.read_csv(WLF, index_col=0, parse_dates=True).iloc[:, 0]
H = wh / float(wh.loc["2014-01-31":"2014-03-31"].mean()) * float(lvl.loc["2014-03-31"])
Hdec = H[H.index.month == 12]; Hdec.index = Hdec.index.year; Havg = H.groupby(H.index.year).mean()
Q = (GDPH / FXL).div(Hdec.reindex(Y), axis=0)                                     # own hour in world hours (end-year FX, Dec H)
Q_avg = (WCD / NH).div(Havg.reindex(Y), axis=0)                                   # check: WB annual-average USD, annual mean H
LOG["q_endyear_over_q_avg_1990_2020_median"] = round(float((Q / Q_avg).loc[1990:2020].stack().median()), 3)

# ------------------------------------------------------------------ 3. vehicles (annual simple returns, LCU)
gr = pd.read_csv(GMPR, index_col=0, parse_dates=True).iloc[:, 0]
GMPU = np.log1p(gr).groupby(gr.index.year).sum(); GMPU = GMPU[gr.groupby(gr.index.year).size() == 12]   # Dec-Dec log, USD
_ga = pd.read_csv(os.path.join(B, "output", "housing", "gmp_annual.csv"), index_col=0)["total"]; LOG["gmp_annual_vs_section4_maxabs"] = float((GMPU.reindex(_ga.index) - _ga).abs().max())
R6040 = 0.6 * EQ + 0.4 * BOND
dfx = np.log(FX).diff()
RGMP = R6040.copy()
for c in HC:
    yy = [y for y in GMPU.index if 1976 <= y <= 2020]; RGMP.loc[yy, c] = np.expm1(GMPU.loc[yy].values + dfx.loc[yy, c].values)
VEH = {"6040": R6040, "gmp": RGMP, "bills": BILLi}
LOG["notes"].append("Vehicle default: domestic 60/40 of JST eq_tr and bond_tr (LCU, rebalanced yearly). GMP variant: note-3 GMP TR in USD, unhedged, converted with JST end-year xrusd, from 1976; domestic 60/40 for 1951-75 (no GMP before 1976).")

# ------------------------------------------------------------------ 4. the life
# REVISION 2 (2026-10-21, after seeing the spec's 2000-anchor results; design correction by the coordinator, not pre-set):
#  (a) baseline home = M x pay in the cohort's first working year (anchor "entry"); price then follows JST hpnom.
#      The spec's 2000 anchor is kept as a robustness row.
#  (b) no flooring: the account may go negative; a negative balance accrues the national bill rate + 1 pt (R and O alike).
BUYC, SELLC, LTV, TERM, SPREAD, DEP, BORROW_SPREAD = 0.0385, 0.0385, 0.80, 25, 0.01, 0.20, 0.01
BASE = dict(M=4.0, c=0.02, b=0.35, veh="6040", mort="fixed", tau=0.10, anchor="entry")
LOG["notes"].append("Revision 2 (design correction after seeing the 2000-anchor results): baseline home priced at M x pay in the first working year; negative account balances allowed, charged bill rate + 1 pt.")

def annuity(L, i, n): return L / n if abs(i) < 1e-10 else L * i / (1 - (1 + i) ** -n)
def cohort_ok(c, s): return all(pd.notna(PRICE_IDX.loc[y, c]) and pd.notna(YDi.loc[y, c]) for y in range(s + 1, s + 41))
A_ = lambda df: {c: df[c].to_numpy(dtype=float) for c in HC}
NP = {"PI": A_(PRICE_IDX), "YD": A_(YDi), "LT": A_(LT), "PAY": A_(PAY), "WB": A_(WAGEBILL), "AP": A_(AVGPAY), "BILL": A_(BILLi), **{"V_" + k: A_(v) for k, v in VEH.items()}}
I0 = int(Y[0]); i2000 = 2000 - I0

def life(c, s, M=4.0, c_run=0.02, b=0.35, veh="6040", mort="fixed", tau=0.10, anchor="entry", rzero=False, valcf=False, path=False):
    yrs = list(range(s + 1, s + 41)); r = NP["V_" + veh][c]; PAYc = NP["PAY"][c]; YDc = NP["YD"][c]; LTc = NP["LT"][c]; WBc = NP["WB"][c]; APc = NP["AP"][c]; BLc = NP["BILL"][c]
    ia = i2000 if anchor == "2000" else s + 1 - I0
    P = M * PAYc[ia] * NP["PI"][c] / NP["PI"][c][ia]                     # standard home: price / pay = M in the anchor year
    o = {"country": c, "cohort": s, "retire_year": s + 40}
    A_R = 0.0; fl_R = 0.0; min_R = 0.0
    A = 0.0; fl = 0.0; min_O = 0.0; owner = False; buy_y = None; L = 0.0; i_fix = None; P_buy = None; YD_buy = None
    interest = 0.0; principal = 0.0; n_paid = 0; buycost = 0.0; down = 0.0; gross_saved = 0.0; running = 0.0
    payg = 0.0; payg_avg = 0.0; fund = 0.0; contrib_payg = 0.0; rows = []
    for k, y in enumerate(yrs):
        j = y - I0; pay = PAYc[j]; Py = P[j]; yd = YDc[j]
        ret = 0.0 if rzero else r[j]; brw = 0.0 if rzero else BLc[j] + BORROW_SPREAD
        rent = (yd + c_run) * Py
        f = b * pay - rent; A_R = A_R * (1 + (ret if A_R >= 0 else brw)) + f; fl_R += f; min_R = min(min_R, A_R / pay)
        if owner:
            Pv = (Py * yd / YD_buy) if valcf else Py                         # valuation counterfactual: rent-price ratio held at purchase level
            if L > 1e-12 and n_paid < TERM:
                i = i_fix if mort == "fixed" else LTc[j] / 100 + SPREAD
                pmt = annuity(L, i, TERM - n_paid); it = L * i; L = L + it - pmt; n_paid += 1; interest += it; principal += pmt - it
            else: pmt = 0.0
            f = b * pay - pmt - c_run * Pv; gross_saved += rent; running += c_run * Pv
        else:
            Pv = Py; f = b * pay - rent
        A = A * (1 + (ret if A >= 0 else brw)) + f; fl += f
        age = 25 + k + 1
        if (not owner) and age >= 35 and age < 65 and A >= (DEP + BUYC) * Py:
            owner = True; buy_y = y; P_buy = Py; YD_buy = yd; down = DEP * Py; buycost = BUYC * Py; A -= down + buycost; L = LTV * Py
            i_fix = LTc[j] / 100 + SPREAD
        min_O = min(min_O, A / pay)
        if k > 0: payg *= WBc[j] / WBc[j - 1]; payg_avg *= APc[j] / APc[j - 1]
        payg += tau * pay; payg_avg += tau * pay; fund = fund * (1 + ret) + tau * pay; contrib_payg += tau * pay
        if path: rows.append({"year": y, "age": age, "pay": pay, "home": Pv if owner else 0.0, "loan": L if owner else 0.0, "account_O": A, "account_R": A_R, "payg": payg, "funded": fund})
    yT = yrs[-1]; jT = yT - I0; payT = PAYc[jT]; PT = (P[jT] * YDc[jT] / YD_buy if valcf else P[jT]) if owner else 0.0
    W_R = A_R; W_O = A + (PT - L if owner else 0.0)
    R_ret = W_R - fl_R; O_ret = A - (fl - down - buycost) if owner else A - fl
    o.update({"W_R": W_R / payT, "W_O": W_O / payT, "W_O_net_sell": (W_O - SELLC * PT) / payT, "W_payg": payg / payT, "W_funded": fund / payT,
              "funded_over_payg": fund / payg, "W_payg_avg": payg_avg / payT, "funded_over_payg_avg": fund / payg_avg, "buy_age": (25 + buy_y - s) if owner else np.nan, "bought": owner,
              "R_negative": min_R < 0, "R_min_balance": min_R, "O_negative": min_O < 0, "O_min_balance": min_O,
              "R_contrib": fl_R / payT, "R_return": R_ret / payT,
              "O_contrib": (fl + principal - buycost) / payT, "O_acct_return": O_ret / payT,
              "O_price_gain": (PT - P_buy) / payT if owner else 0.0, "O_interest": interest / payT, "O_buycost": buycost / payT,
              "O_loan_left": (L if owner else 0.0) / payT, "O_home": PT / payT, "O_account": A / payT,
              "price_to_pay_at_entry": P[s + 1 - I0] / PAYc[s + 1 - I0], "price_to_pay_at_65": P[jT] / payT,
              "mort_rate_at_buy": i_fix if owner else np.nan,
              "payg_contrib": contrib_payg / payT, "q_final": float(Q.loc[yT, c]), "gdp_usd_retire": float(WCD.loc[yT, c]),
              # O minus R: (price gain + imputed rent saved) - (interest + running costs + buying cost) - forgone vehicle return
              "OR_price_gain": (PT - P_buy) / payT if owner else 0.0, "OR_gross_rent_saved": gross_saved / payT, "OR_net_rent_saved": (gross_saved - running) / payT,
              "OR_running_costs": running / payT, "OR_interest": interest / payT, "OR_buycost": buycost / payT, "OR_forgone_return": (R_ret - O_ret) / payT})
    o["O_identity_gap"] = o["W_O"] - (o["O_contrib"] + o["O_acct_return"] + o["O_price_gain"])
    o["OR_identity_gap"] = (o["W_O"] - o["W_R"]) - (o["OR_price_gain"] + o["OR_gross_rent_saved"] - o["OR_running_costs"] - o["OR_interest"] - o["OR_buycost"] - o["OR_forgone_return"])
    if owner and not valcf: o["O_valuation_part_of_price"] = (P[jT] - P[jT] * YDc[jT] / YD_buy) / payT
    return (o, pd.DataFrame(rows)) if path else o

PAIRS = [(c, s) for c in HC for s in COHORTS]; OKP = [(c, s) for c, s in PAIRS if cohort_ok(c, s)]
LOG["cohorts"] = {"possible": len(PAIRS), "with_data": len(OKP), "dropped": {c: [s for cc, s in PAIRS if cc == c and (cc, s) not in OKP] for c in HC if any(cc == c and (cc, s) not in OKP for cc, s in PAIRS)}}

def run(**kw):
    rows = []
    for c, s in OKP:
        o = life(c, s, **kw); cf = life(c, s, valcf=True, **kw)
        o["W_O_cf_noval"] = cf["W_O"]; o["O_valuation_share"] = (o["W_O"] - cf["W_O"]) / o["W_O"] if o["bought"] else np.nan
        rows.append(o)
    t = pd.DataFrame(rows)
    t["O_over_R"] = t.W_O / t.W_R; t["O_minus_R"] = t.W_O - t.W_R; t["any_negative"] = t.R_negative | t.O_negative
    t["R_plus_payg"] = t.W_R + t.W_payg; t["O_plus_payg"] = t.W_O + t.W_payg; t["R_plus_funded"] = t.W_R + t.W_funded; t["O_plus_funded"] = t.W_O + t.W_funded
    for k in ["W_R", "W_O", "W_payg", "W_funded"]: t[k + "_worldhr"] = t[k] * t.q_final           # years of world-hour pay
    t["decade"] = (t.cohort // 10 * 10).astype(str) + "s"; return t

def kw_of(P_): return dict(M=P_["M"], c_run=P_["c"], b=P_["b"], veh=P_["veh"], mort=P_["mort"], tau=P_["tau"], anchor=P_["anchor"])
T = run(**kw_of(BASE)); T.round(5).to_csv(os.path.join(OUT, "life_cohorts_baseline.csv"), index=False)
T2000 = run(**kw_of(dict(BASE, anchor="2000"))); T2000.round(5).to_csv(os.path.join(OUT, "life_cohorts_anchor2000.csv"), index=False)
for f_ in ["life_cohorts_entry_anchor.csv", "summary_entry_anchor.csv", "summary_baseline_never_flagged.csv"]:     # superseded revision-1 files
    if os.path.exists(os.path.join(OUT, f_)): os.remove(os.path.join(OUT, f_))

KEYS = ["W_R", "W_O", "W_O_net_sell", "O_over_R", "O_minus_R", "W_payg", "W_funded", "funded_over_payg", "O_valuation_share", "buy_age", "W_R_worldhr", "W_O_worldhr", "q_final", "price_to_pay_at_65", "R_min_balance", "O_min_balance"]
def summ(t, keys=KEYS):
    rows = []
    for k in keys:
        x = t[k].dropna(); g = t.loc[x.index]
        wts = g.gdp_usd_retire / g.groupby("cohort").gdp_usd_retire.transform("sum")          # GDP weights within cohort, each cohort equal
        rows.append({"metric": k, "n": len(x), "median": x.median(), "p25": x.quantile(.25), "p75": x.quantile(.75), "min": x.min(), "max": x.max(), "mean": x.mean(),
                     "gdp_weighted_mean": float((x * wts).groupby(g.cohort).sum().div(wts.groupby(g.cohort).sum()).mean())})
    return pd.DataFrame(rows).set_index("metric")
S = summ(T); S.round(4).to_csv(os.path.join(OUT, "summary_baseline.csv"))
CLEAN = T[~T.any_negative]; SN = summ(CLEAN); SN.round(4).to_csv(os.path.join(OUT, "summary_baseline_never_negative.csv"))
S2000 = summ(T2000); S2000.round(4).to_csv(os.path.join(OUT, "summary_anchor2000.csv"))
SD = T.groupby("decade")[KEYS].median(); SD["n"] = T.groupby("decade").size(); SD["R_negative"] = T.groupby("decade").R_negative.sum(); SD["O_negative"] = T.groupby("decade").O_negative.sum()
SD["O_beats_R_share"] = T.groupby("decade").apply(lambda g: (g.W_O > g.W_R).mean()); SD.round(4).to_csv(os.path.join(OUT, "summary_by_cohort_decade.csv"))
def dec_table(t):
    sd = t.groupby("decade")[KEYS].median(); sd["n"] = t.groupby("decade").size(); sd["R_negative"] = t.groupby("decade").R_negative.sum(); sd["O_negative"] = t.groupby("decade").O_negative.sum()
    sd["O_beats_R_share"] = t.groupby("decade").apply(lambda g: (g.W_O > g.W_R).mean()); return sd
TV = run(**kw_of(dict(BASE, mort="variable"))); TBL = run(**kw_of(dict(BASE, veh="bills")))
SDV, SDB = dec_table(TV), dec_table(TBL); SDV.round(4).to_csv(os.path.join(OUT, "summary_by_cohort_decade_variable.csv")); SDB.round(4).to_csv(os.path.join(OUT, "summary_by_cohort_decade_bills.csv"))
DCMP = pd.concat({"O_over_R": pd.DataFrame({"baseline": SD.O_over_R, "variable": SDV.O_over_R, "bills": SDB.O_over_R}),
                  "O_minus_R": pd.DataFrame({"baseline": SD.O_minus_R, "variable": SDV.O_minus_R, "bills": SDB.O_minus_R}),
                  "O_beats_R_share": pd.DataFrame({"baseline": SD.O_beats_R_share, "variable": SDV.O_beats_R_share, "bills": SDB.O_beats_R_share})}, axis=1)
DCMP.round(4).to_csv(os.path.join(OUT, "decade_O_vs_R_baseline_variable_bills.csv")); LOG["decade_O_vs_R"] = {f"{a}|{b}": v for (a, b), v in DCMP.round(3).to_dict().items()}
SC = T.groupby("country")[["W_R", "W_O", "O_over_R", "O_valuation_share", "funded_over_payg", "W_payg", "W_funded", "buy_age", "q_final", "R_min_balance", "O_min_balance"]].median(); SC["n"] = T.groupby("country").size()
SC["O_beats_R_share"] = T.groupby("country").apply(lambda g: (g.W_O > g.W_R).mean()); SC["R_negative"] = T.groupby("country").R_negative.sum(); SC["O_negative"] = T.groupby("country").O_negative.sum(); SC.round(4).to_csv(os.path.join(OUT, "summary_by_country.csv"))
DEC = ["R_contrib", "R_return", "W_R", "O_contrib", "O_acct_return", "O_price_gain", "O_valuation_part_of_price", "O_interest", "O_buycost", "W_O", "payg_contrib", "W_payg", "W_funded"]
summ(T, DEC).round(4).to_csv(os.path.join(OUT, "decomposition_baseline.csv"))
ORK = ["OR_price_gain", "OR_gross_rent_saved", "OR_running_costs", "OR_net_rent_saved", "OR_interest", "OR_buycost", "OR_forgone_return", "O_minus_R"]
TB = T[T.bought]; ORD = pd.concat({"all_buyers": summ(TB, ORK), "never_negative_buyers": summ(TB[~TB.any_negative], ORK)}, axis=1)
ORD.round(4).to_csv(os.path.join(OUT, "decomposition_own_minus_rent.csv"))
NEG = T[T.any_negative | ~T.bought][["country", "cohort", "R_negative", "R_min_balance", "O_negative", "O_min_balance", "bought", "buy_age", "price_to_pay_at_entry"]]
NEG.round(4).to_csv(os.path.join(OUT, "cohorts_flagged.csv"), index=False)
# price / pay of the spec's standard 2000 home (price / pay = 4 in 2000), 1950-2020
PP = (4.0 * PRICE_IDX / PRICE_IDX.loc[2000]).div(PAY).loc[1950:2020]
PPS = pd.DataFrame({"median": PP.median(axis=1), "p25": PP.quantile(.25, axis=1), "p75": PP.quantile(.75, axis=1), "min": PP.min(axis=1), "max": PP.max(axis=1), "n": PP.notna().sum(axis=1)})
PPS.round(4).to_csv(os.path.join(OUT, "price_to_pay_standard_2000_home.csv")); PP.round(4).to_csv(os.path.join(OUT, "price_to_pay_standard_2000_home_by_country.csv"))
_bal = PP.loc[[1950, 2020]].dropna(axis=1); LOG["price_to_pay_drift"] = {"median_1950": round(float(PPS.loc[1950, "median"]), 2), "median_1960": round(float(PPS.loc[1960, "median"]), 2), "median_1980": round(float(PPS.loc[1980, "median"]), 2), "median_2020": round(float(PPS.loc[2020, "median"]), 2),
    "median_log_change_per_year_1950_2020_pct_balanced": round(float((np.log(_bal.loc[2020] / _bal.loc[1950]) / 70).median() * 100), 2), "countries_balanced": list(_bal.columns)}

# PAYG variants (referee): wage-bill indexation (Samuelson-Aaron / NDC-like) vs average pay per worker (points / earnings-indexed)
TG = run(**kw_of(dict(BASE, veh="gmp"))); PV = []
for vname, tt in [("6040", T), ("gmp", TG), ("bills", TBL)]:
    for claim, wc, rc in [("payg_wagebill", "W_payg", "funded_over_payg"), ("payg_avg_pay_per_worker", "W_payg_avg", "funded_over_payg_avg")]:
        PV.append({"vehicle": vname, "payg_claim": claim, "n": len(tt), "median_payg_claim_years_final_pay": tt[wc].median(), "median_funded_years_final_pay": tt.W_funded.median(),
                   "median_funded_over_payg": tt[rc].median(), "p25_funded_over_payg": tt[rc].quantile(.25), "p75_funded_over_payg": tt[rc].quantile(.75), "share_funded_beats_payg": (tt[rc] > 1).mean()})
PV = pd.DataFrame(PV); PV.round(4).to_csv(os.path.join(OUT, "summary_payg_variants.csv"), index=False)
LOG["payg_variants"] = PV.round(4).to_dict(orient="records"); LOG["notes"].append("P-payg-avg: claim revalued with national GDP per hour x PWT avh (average pay per worker); pre-1960 avh growth held at 0.")
# world GDP-weighted avh growth, per 1,000 hours, same method as build_balance.py section 6f (start-of-year WB USD GDP weights; 1960 weights before 1961)
pa = pd.read_csv(PWTF); AVA = pa[pa.variable == "avh"].pivot(index="year", columns="iso3", values="value").sort_index()
wa = pd.read_csv(WBF); UG = wa[wa.variable == "NY.GDP.MKTP.CD"].pivot(index="year", columns="iso3", values="value").sort_index()
dA = np.log(AVA).diff(); WW = UG.shift(1).reindex(index=dA.index)
for y in range(1951, 1961): WW.loc[y] = UG.loc[1960]
def wavg_(x, sample=None):
    o = {}
    for y in range(1951, 2024):
        v = x.loc[y] if sample is None else x.loc[y].reindex(sample); w = WW.loc[y].reindex(v.index); m = v.notna() & w.notna()
        o[y] = np.average(v[m], weights=w[m]) if m.sum() else np.nan
    return pd.Series(o)
AW, AW16 = wavg_(dA), wavg_(dA, HC)
BALT = os.path.join(B, "output", "balance", "table_payg_return_by_decade_world.csv"); bt = pd.read_csv(BALT, index_col=0); LOG["inputs_sha256"][label(BALT)] = sha(BALT)
AVHG = {}
for a, b_ in [(1951, 2023), (1976, 2020)]:
    k = f"{a}-{b_}"; AVHG[k] = {"world_gdp_weighted_avh_per_1000h": round(float(AW.loc[a:b_].mean() * 1000), 2), "jst16_gdp_weighted_avh_per_1000h": round(float(AW16.loc[a:b_].mean() * 1000), 2),
                                "balance_table_avh_all": float(bt.loc[k, "avh_all"]), "balance_table_avh_drag_hours_minus_emp": float(bt.loc[k, "avh_drag"])}
LOG["world_avh_growth"] = AVHG

# ------------------------------------------------------------------ 5. robustness (on the revised baseline)
GRID = {"M": [3.0, 4.0, 6.0], "c": [0.015, 0.02, 0.03], "b": [0.25, 0.35, 0.45], "veh": ["6040", "gmp", "bills"], "mort": ["fixed", "variable"], "anchor": ["entry", "2000"]}
def rsum(t, case):
    tb = t[t.bought]; cl = t[~t.any_negative]
    return {"case": case, "median_W_R": t.W_R.median(), "median_W_O": t.W_O.median(), "median_O_over_R": t.O_over_R.median(), "share_O_beats_R": (t.W_O > t.W_R).mean(),
            "median_valuation_share": tb.O_valuation_share.median(), "median_funded_over_payg": t.funded_over_payg.median(), "share_funded_beats_payg": (t.funded_over_payg > 1).mean(),
            "n_R_negative": int(t.R_negative.sum()), "n_O_negative": int(t.O_negative.sum()), "n_any_negative": int(t.any_negative.sum()),
            "median_min_balance_negative_lives": float(np.minimum(t.R_min_balance, t.O_min_balance)[t.any_negative].median()) if t.any_negative.any() else 0.0,
            "nn_n": len(cl), "nn_median_W_R": cl.W_R.median(), "nn_median_W_O": cl.W_O.median(), "nn_share_O_beats_R": (cl.W_O > cl.W_R).mean(),
            "n_never_buy": int((~t.bought).sum()), "median_buy_age": tb.buy_age.median(), "n": len(t)}
RB = [rsum(T, "baseline (M4 at entry, c2.0, b35, 60/40, fixed)")]
for k, vals in GRID.items():
    for v in vals:
        if v == BASE[k]: continue
        P_ = dict(BASE); P_[k] = v; RB.append(rsum(T2000 if (k == "anchor" and v == "2000") else run(**kw_of(P_)), f"{k}={v}"))
RB = pd.DataFrame(RB).set_index("case"); RB.round(4).to_csv(os.path.join(OUT, "robustness_one_at_a_time.csv"))
FULL = []
for M, c_, b_, v_, m_, a_ in itertools.product(*GRID.values()):
    P_ = dict(BASE, M=M, c=c_, b=b_, veh=v_, mort=m_, anchor=a_); r_ = rsum(run(**kw_of(P_)), ""); r_.pop("case"); FULL.append({"M": M, "c": c_, "b": b_, "veh": v_, "mort": m_, "anchor": a_, **r_})
FULL = pd.DataFrame(FULL); FULL.round(4).to_csv(os.path.join(OUT, "robustness_full_grid.csv"), index=False)

# ------------------------------------------------------------------ 6. checks
CHK = {}
Z = pd.DataFrame([life(c, s, rzero=True, **kw_of(BASE)) for c, s in OKP])
CHK["zero_return_R_wealth_minus_contrib_maxabs_all_lives"] = float((Z.W_R - Z.R_contrib).abs().max())
def _sum_contrib(r_):
    c, s = r_.country, r_.cohort; P = BASE["M"] * PAY.loc[s + 1, c] * PRICE_IDX[c] / PRICE_IDX.loc[s + 1, c]
    return sum(BASE["b"] * PAY.loc[y, c] - (YDi.loc[y, c] + BASE["c"]) * P.loc[y] for y in range(s + 1, s + 41)) / PAY.loc[s + 40, c]
CHK["zero_return_R_equals_sum_b_pay_minus_rent_maxabs"] = float(max(abs(r_.W_R - _sum_contrib(r_)) for r_ in Z.itertuples()))
CHK["zero_return_funded_equals_tau_sum_pay_maxabs"] = float(max(abs(r_.W_funded - BASE["tau"] * PAY.loc[r_.cohort + 1:r_.cohort + 40, r_.country].sum() / PAY.loc[r_.cohort + 40, r_.country]) for r_ in Z.itertuples()))
CHK["payg_equals_tau_sum_hours_growth_factors_maxabs"] = float(max(abs(r_.W_payg - BASE["tau"] * (NH.loc[r_.cohort + 40, r_.country] / NH.loc[r_.cohort + 1:r_.cohort + 40, r_.country]).sum()) for r_ in T.itertuples()))
CHK["payg_avg_equals_tau_sum_avh_growth_factors_maxabs"] = float(max(abs(r_.W_payg_avg - BASE["tau"] * (AVH.loc[r_.cohort + 40, r_.country] / AVH.loc[r_.cohort + 1:r_.cohort + 40, r_.country]).sum()) for r_ in T.itertuples()))
CHK["O_decomposition_identity_maxabs"] = float(T.O_identity_gap.abs().max())
CHK["O_minus_R_decomposition_identity_maxabs"] = float(T.OR_identity_gap.abs().max())
CHK["R_decomposition_identity_maxabs"] = float((T.W_R - T.R_contrib - T.R_return).abs().max())
CHK["entry_price_to_pay_equals_M_maxabs"] = float((T.price_to_pay_at_entry - BASE["M"]).abs().max())
L0 = 1.0; n0 = 0
for _ in range(TERM): pm = annuity(L0, 0.05, TERM - n0); L0 = L0 * 1.05 - pm; n0 += 1
CHK["annuity_25y_5pct_residual"] = float(L0)
CHK["payg_hours_return_note"] = "PAYG claim / final pay = tau x sum_t (N_65 / N_t): its hour return is the growth of total hours worked"
LOG["checks"] = CHK

# ------------------------------------------------------------------ 7. figures
from matplotlib.ticker import FixedLocator, FuncFormatter, NullLocator
co = T.groupby("cohort")
fig, ax = plt.subplots(figsize=(8.4, 4.2))
for k, col, lab_ in [("W_R", PAL[0], "Rent and invest (R)"), ("W_O", PAL[2], "Buy at 35 (O)")]:
    m = co[k].median(); ax.fill_between(m.index, co[k].quantile(.25), co[k].quantile(.75), color=col, alpha=.25, lw=0)
    ax.plot(m.index, co[k].min(), color=col, lw=.6, ls=":"); ax.plot(m.index, co[k].max(), color=col, lw=.6, ls=":"); ax.plot(m.index, m, color=col, lw=1.8, label=f"{lab_}: median, interquartile band, min/max dotted")
ax.axhline(0, color="grey", lw=.6); ax.set_xlabel("year the cohort starts work at 25 (retires 40 years later)"); ax.set_ylabel("wealth at 65, years of own final pay")
ax.set_title("Wealth at 65: 35% of pay to housing and saving, home = 4 years of pay at entry, 16 countries", loc="left", fontsize=9.5); ax.legend(fontsize=7.5, frameon=False, loc="upper left")
fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig_1_own_vs_rent_by_cohort.png"), dpi=160); plt.close(fig)
fig, ax = plt.subplots(figsize=(8.4, 4.2))
pw = T.pivot(index="cohort", columns="country", values="funded_over_payg")
for c in pw.columns: ax.plot(pw.index, pw[c], color=PAL[3], lw=.7, alpha=.8)
for c, col in [("USA", PAL[0]), ("JPN", PAL[4]), ("ITA", PAL[1])]: ax.plot(pw.index, pw[c], color=col, lw=1.3, label=c)
ax.plot(pw.index, pw.median(axis=1), color="k", lw=2, label="median of 16 countries"); ax.axhline(1, color="grey", lw=.6); ax.set_yscale("log")
ax.yaxis.set_major_locator(FixedLocator([0.5, 1, 2, 3, 5])); ax.yaxis.set_minor_locator(NullLocator()); ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
ax.set_xlabel("year the cohort starts work at 25"); ax.set_ylabel("funded / PAYG claim at 65 (log scale)")
ax.set_title("10% of pay for 40 years: a domestic 60/40 account over a PAYG claim indexed to the wage bill", loc="left", fontsize=9.5); ax.legend(fontsize=7.5, frameon=False, loc="upper left")
fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig_2_funded_over_payg.png"), dpi=160); plt.close(fig)
o, pth = life("USA", 1970, path=True, **kw_of(BASE)); pth.round(5).to_csv(os.path.join(OUT, "path_USA_1970.csv"), index=False)
x = pth.set_index("age"); dv = x.div(x.pay, axis=0)
fig, ax = plt.subplots(figsize=(8.4, 4.2))
ax.stackplot(dv.index, dv.account_O.clip(lower=0), dv.home - dv.loan, dv.payg, colors=[PAL[0], PAL[2], PAL[1]], labels=["Account (60/40)", "Home equity (home minus loan)", "PAYG claim (10% of pay)"], alpha=.85)
ax.fill_between(dv.index, dv.account_O.clip(upper=0), 0, color=PAL[5], alpha=.6, lw=0, label="Account overdrawn (bill rate + 1 pt)")
ax.plot(dv.index, -dv.loan, color=PAL[4], lw=1.2, label="Mortgage outstanding (negative)"); ax.plot(dv.index, dv.account_R + dv.payg, color="k", lw=1.2, ls="--", label="Renter: account + PAYG claim")
ax.axhline(0, color="grey", lw=.6); ax.set_xlabel("age (end of year)"); ax.set_ylabel("years of current own pay")
ax.set_title(f"USA, cohort starting work in 1970 (buys at {int(o['buy_age'])}): the owner's balance sheet over a working life", loc="left", fontsize=9.5); ax.legend(fontsize=7.5, frameon=False, loc="upper left")
fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig_3_usa_1970_balance_sheet.png"), dpi=160); plt.close(fig)
fig, ax = plt.subplots(figsize=(8.4, 4.2))
for c in PP.columns: ax.plot(PP.index, PP[c], color=PAL[3], lw=.6, alpha=.7)
ax.fill_between(PPS.index, PPS.p25, PPS.p75, color=PAL[2], alpha=.25, lw=0); ax.plot(PPS.index, PPS["median"], color=PAL[2], lw=2, label="median of 16 countries (band: interquartile range; thin lines: countries)")
ax.axhline(4, color="grey", lw=.6); ax.set_yscale("log"); ax.yaxis.set_major_locator(FixedLocator([1, 2, 3, 4, 6, 8, 12, 16])); ax.yaxis.set_minor_locator(NullLocator()); ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
ax.set_ylabel("price / annual pay (log scale)"); ax.set_title("A home that cost 4 years of pay in 2000: its price in years of pay, 1950-2020 (JST hpnom / GDP per hour)", loc="left", fontsize=9.5)
ax.legend(fontsize=7.5, frameon=False, loc="upper right"); fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig_4_price_to_pay_2000_home.png"), dpi=160); plt.close(fig)

# ------------------------------------------------------------------ 8. log
LOG["design"] = {"base": BASE, "deposit": DEP, "buy_cost": BUYC, "sell_cost": SELLC, "ltv": LTV, "term": TERM, "spread": SPREAD, "borrow_spread_over_bill": BORROW_SPREAD, "timing": "age 25 at end of year s; flows t=s+1..s+40; wealth at end of s+40 (retire year)"}
LOG["headline"] = {k: {kk: round(float(vv), 4) for kk, vv in S.loc[k].items()} for k in S.index}
LOG["headline_never_negative"] = {k: {kk: round(float(vv), 4) for kk, vv in SN.loc[k].items()} for k in SN.index}
_mn = np.minimum(T.R_min_balance, T.O_min_balance)
LOG["counts"] = {"n": len(T), "O_beats_R": int((T.W_O > T.W_R).sum()), "funded_beats_payg": int((T.funded_over_payg > 1).sum()), "R_negative": int(T.R_negative.sum()), "O_negative": int(T.O_negative.sum()),
                 "any_negative": int(T.any_negative.sum()), "never_negative": len(CLEAN), "median_min_balance_negative_lives_years_of_pay": round(float(_mn[T.any_negative].median()), 4),
                 "R_median_min_if_negative": round(float(T.R_min_balance[T.R_negative].median()), 4), "O_median_min_if_negative": round(float(T.O_min_balance[T.O_negative].median()), 4),
                 "never_buy": int((~T.bought).sum()), "negative_W_R": int((T.W_R < 0).sum()), "negative_W_O": int((T.W_O < 0).sum())}
LOG["anchor2000_robustness"] = {"medians": S2000["median"].round(4).to_dict(), "R_negative": int(T2000.R_negative.sum()), "O_negative": int(T2000.O_negative.sum()), "never_buy": int((~T2000.bought).sum()), "O_beats_R": int((T2000.W_O > T2000.W_R).sum())}
LOG["own_minus_rent_decomposition_median_all_buyers"] = ORD["all_buyers"]["median"].round(4).to_dict()
LOG["usa_1970"] = {k: (round(float(v), 4) if isinstance(v, (float, np.floating)) else v) for k, v in o.items() if not isinstance(v, (bool, np.bool_))}
json.dump(LOG, open(os.path.join(OUT, "build_log.json"), "w"), indent=1, default=lambda v: v.item() if hasattr(v, "item") else str(v))
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
print(S.round(3).to_string()); print(SN.round(3).to_string()); print(SD.round(3).to_string()); print(SC.round(3).to_string()); print(summ(T, DEC).round(3).to_string()); print(ORD.round(3).to_string()); print(RB.round(3).T.to_string()); print(PPS.loc[[1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020]].round(2).to_string())
print(DCMP.round(3).to_string()); print(PV.round(3).to_string()); print(json.dumps(AVHG)); print(json.dumps({k: LOG[k] for k in ["counts", "anchor2000_robustness", "checks", "price_to_pay_drift", "cohorts"]}, indent=0, default=str))
