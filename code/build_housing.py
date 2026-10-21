# -*- coding: utf-8 -*-
"""Note 4, section 4: the home in hours.  JST R6 housing (16 countries) split into net rent, valuation (change in the
rent-price ratio) and rent growth; expressed per 1,000 hours of housing capital in world hours (USD, GDP-weighted) and in
national hours (LCU nominal GDP per hour worked); set beside the GMP (note 3) and beside the household's other JST claims
(bills, long government bonds, equities).  Exploratory, not pre-registered.  Outputs to output/housing/.
Loaders copied from ~/gmp_income/build_v2.py and ~/composite_numeraire/world.py (no imports: those scripts run on import).
No network: all inputs are cached files."""
import os, json, hashlib, numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

from paths import B, JSTF, CN, GMPC, GMPR, DC, PWTX, SITE_CSS, cnd, label   # release: input locations (env-var overrides) and log labels, see paths.py
OUT = os.path.join(B, "output", "housing"); os.makedirs(OUT, exist_ok=True)
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
LOG = {"inputs_sha256": {}}; INPUTS = [JSTF, GMPC, GMPR] + [os.path.join(CN, f) for f in ["world_yardsticks_usd.csv", "world_q_gdp_per_hour_level_usd.csv"]] + [cnd("wb_ngdp_lcu.json")]
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False})
PAL = ["#1f4e79", "#6b8e6b", "#c98a2b", "#7f9fbf", "#8c4a3c", "#3b3b8f"]
PER = [(1976, 1981), (1982, 2000), (2001, 2020), (1976, 2020)]
def lab(a, b): return f"{a}-{b}"

# ------------------------------------------------------------------ 1. JST
d = pd.read_excel(JSTF)
def pv(v): return d.pivot(index="year", columns="iso", values=v).sort_index()
TR, RR, YD, CG = pv("housing_tr"), pv("housing_rent_rtn"), pv("housing_rent_yd"), pv("housing_capgain")
HC = [c for c in TR.columns if TR[c].notna().any()]; assert len(HC) == 16, HC                     # CAN and IRL have no housing returns
FX = pv("xrusd"); GDP = pv("gdp"); POP = pv("pop"); BILL, BOND, EQ = pv("bill_rate"), pv("bond_tr"), pv("eq_tr")
TR, RR, YD, CG = TR[HC], RR[HC], YD[HC], CG[HC]
# identity checks in the source
disc_tr = (TR - (CG + RR)).abs().max().max(); disc_rr = (RR - YD * (1 + CG)).abs().max().max()
_e = (RR - YD * (1 + CG)).abs().stack(); LOG["rent_rtn_identity_outliers"] = {f"{i[1]} {i[0]}": round(float(v), 4) for i, v in _e[_e > 1e-4].items()}
LOG["identity_source"] = {"max_abs_housing_tr_minus_capgain_plus_rent_rtn": float(disc_tr), "max_abs_rent_rtn_minus_rent_yd_t_x_1plus_capgain": float(disc_rr),
                          "reading": "housing_tr = capgain + rent_rtn; rent_rtn = rent_t / price_{t-1} (rent_yd is rent_t / price_t, net of maintenance, depreciation and other costs per Jorda et al. 2019)"}
# xrusd timing: end-year or average?  Japan: end-1985 200.5 / avg 238.5; end-1986 159.1 / avg 168.5 (known values)
LOG["xrusd_timing"] = {"JPN_1985": float(FX.loc[1985, "JPN"]), "JPN_1986": float(FX.loc[1986, "JPN"]), "conclusion": "end-of-year (matches year-end yen 200.5 and 159.1; annual averages were 238.5 and 168.5)"}

# components, local currency, log
tot_l = np.log1p(TR); cash = np.log1p(RR); price_l = tot_l - cash; val = -np.log(YD).diff(); pxv_l = price_l - val
lrent = np.log(YD) + np.log1p(CG).cumsum(); drent = lrent.diff()                                      # implied log rent growth
gap = (pxv_l - drent).where(val.notna())
LOG["identity_components"] = {"total_minus_(cash+val+pxv)_max": float((tot_l - cash - val - pxv_l).abs().max().max()),
                              "pxv_minus_dlog_rent_mean_pct_1976_2020": float(gap.loc[1976:2020].stack().mean() * 100), "pxv_minus_dlog_rent_maxabs_pct_1976_2020": float(gap.loc[1976:2020].abs().max().max() * 100),
                              "note": "price = log(1+tr) - log(1+rent_rtn) differs from log(1+capgain) by a cross term; so price ex valuation = rent growth only approximately"}
dfx = np.log(FX).diff()                                                                               # + = local currency weaker vs USD

# ------------------------------------------------------------------ 2. world hour (note 3 build_v2.py:112-119) and GMP
wh_idx = pd.read_csv(os.path.join(CN, "world_yardsticks_usd.csv"), index_col=0, parse_dates=True)["gdph"]
lvl_q = pd.read_csv(os.path.join(CN, "world_q_gdp_per_hour_level_usd.csv"), index_col=0, parse_dates=True).iloc[:, 0]
H = wh_idx / float(wh_idx.loc["2014-01-31":"2014-03-31"].mean()) * float(lvl_q.loc["2014-03-31"])
Hdec = H[H.index.month == 12]; Hdec.index = Hdec.index.year; NEED_W = np.log(Hdec).diff()           # Dec t-1 -> Dec t
Havg = H.groupby(H.index.year).mean(); NEED_W_AVG = np.log(Havg).diff().where(H.groupby(H.index.year).size() == 12)
GC = pd.read_csv(GMPC, index_col=0, parse_dates=True)
gr = pd.read_csv(GMPR, index_col=0, parse_dates=True).iloc[:, 0]; gr.index = gr.index + pd.offsets.MonthEnd(0)
LOG["gmp_components_check_max_abs_ltr_vs_log1p_TR"] = float((GC["ltr"] - np.log1p(gr.reindex(GC.index))).abs().max())
GA = GC[["ltr", "cash", "val"]].groupby(GC.index.year).sum(); GA = GA[GC.groupby(GC.index.year).size() == 12]
GMP = pd.DataFrame({"total": GA["ltr"], "cash": GA["cash"], "val": GA["val"]}); GMP["price"] = GMP.total - GMP.cash; GMP["pxv"] = GMP.price - GMP.val
gyield = GC["yield_pct"].groupby(GC.index.year).mean()

# ------------------------------------------------------------------ 3. aggregation
# JST 'gdp' is in mixed units (millions, billions or trillions of LCU by country): GDP/xrusd is NOT comparable across countries.
# Unit factor per country = power of ten matching World Bank NY.GDP.MKTP.CD over 1991-2020 (residual spread ~0.03 in log10).
jw = json.load(open(cnd("wb_gdp.json")))[1]
WBG = pd.DataFrame([(r["countryiso3code"], int(r["date"]), r["value"]) for r in jw if r["value"] is not None and r["countryiso3code"]], columns=["c", "y", "v"]).pivot_table(index="y", columns="c", values="v", aggfunc="first")
ratio = np.log10(WBG[GDP.columns] / (GDP / FX)).loc[1991:2020]; UNIT = (10.0 ** ratio.median().round()); LOG["jst_gdp_unit_log10"] = ratio.median().round(3).to_dict(); LOG["jst_gdp_unit_residual_sd_log10_max"] = float(ratio.std().max())
GUSD = GDP / FX * UNIT                                                                                 # USD GDP, same year
W_USD = GUSD.shift(1)                                                                                  # start-of-year USD GDP weights
_bug = (GDP / FX)[HC].where(YD.notna()); _bug = _bug.div(_bug.sum(axis=1), axis=0)                    # note 3 sec. 7 convention (unscaled units)
LOG["note3_rent_weight_bug"] = {"unscaled_weights_mean_1976_2020": _bug.loc[1976:2020].mean().round(3).to_dict(),
                                "rent_yield_unscaled_pct": {str(y): round(float((YD * 100 * _bug).sum(axis=1).loc[y]), 2) for y in [1976, 2000, 2020]}}
def weights(avail, kind="gdp", excl=()):
    w = W_USD[avail.columns].where(avail) if kind == "gdp" else avail.astype(float).where(avail)
    for c in excl: w[c] = np.nan
    return w.div(w.sum(axis=1), axis=0)
def agg_housing(tot, cash_, val_, kind="gdp", excl=()):
    """portfolio of national housing indices: total and cash aggregated as simple returns, valuation as weighted log"""
    w = weights(tot.notna() & val_.notna() & W_USD[tot.columns].notna(), kind, excl)
    T = np.log((w * np.expm1(tot)).sum(axis=1, min_count=1) + 1); C = np.log((w * np.expm1(cash_)).sum(axis=1, min_count=1) + 1); V = (w * val_).sum(axis=1, min_count=1)
    o = pd.DataFrame({"total": T, "cash": C, "val": V}); o["price"] = o.total - o.cash; o["pxv"] = o.price - o.val; o["n"] = w.notna().sum(axis=1); return o
def agg_simple(tot, kind="gdp", excl=()):
    w = weights(tot.notna() & W_USD[tot.columns].notna(), kind, excl); return np.log((w * np.expm1(tot)).sum(axis=1, min_count=1) + 1)
tot_u = tot_l - dfx[HC]; price_u = tot_u - cash; pxv_u = price_u - val
HW = agg_housing(tot_u, cash, val); HW_EQ = agg_housing(tot_u, cash, val, "eq"); HW_XUS = agg_housing(tot_u, cash, val, excl=("USA",))
# check: weighted average of logs instead of log of weighted simple returns
w0 = weights(tot_u.notna() & val.notna() & W_USD[HC].notna()); LOG["housing_logavg_minus_portfolio_total_pct_1976_2020"] = float(((w0 * tot_u).sum(axis=1).loc[1976:2020] - HW.total.loc[1976:2020]).mean() * 100)
LOG["housing_countries_1976_2020"] = {"min": int(HW.n.loc[1976:2020].min()), "max": int(HW.n.loc[1976:2020].max())}
LOG["housing_usa_weight_1976_2020_mean"] = float(w0["USA"].loc[1976:2020].mean())

# ------------------------------------------------------------------ 4. hours tables
def hours_table(X, need, periods=PER, extra=None):
    rows = []
    for a, b in periods:
        x = X.loc[a:b]; n = need.loc[a:b]; assert x.total.notna().all() and n.notna().all() and len(x) == b - a + 1, (a, b)
        r = {"period": lab(a, b), "total": x.total.mean(), "cash": x.cash.mean(), "price": x.price.mean(), "valuation": x.val.mean(), "price_ex_valuation": x.pxv.mean(), "needed": n.mean()}
        r["net"] = r["total"] - r["needed"]; r["net_ex_valuation"] = r["total"] - r["valuation"] - r["needed"]; rows.append(r)
    return (pd.DataFrame(rows).set_index("period") * 1000).round(1)                                   # log per year x 1000 = hours per 1,000 hours
T_H = hours_table(HW, NEED_W); T_G = hours_table(GMP, NEED_W)
side = pd.concat({"housing": T_H.T, "gmp": T_G.T}, axis=1); side.to_csv(os.path.join(OUT, "table_housing_vs_gmp_world_hours.csv"))
T_H.to_csv(os.path.join(OUT, "table_housing_world_hours.csv")); T_G.to_csv(os.path.join(OUT, "table_gmp_world_hours.csv"))
hours_table(HW_EQ, NEED_W).to_csv(os.path.join(OUT, "table_housing_world_hours_equal_weight.csv")); hours_table(HW_XUS, NEED_W).to_csv(os.path.join(OUT, "table_housing_world_hours_ex_usa.csv"))
HW.round(6).to_csv(os.path.join(OUT, "housing_world_annual.csv")); GMP.round(6).to_csv(os.path.join(OUT, "gmp_annual.csv"))
pd.DataFrame({"dec_to_dec": NEED_W, "annual_average": NEED_W_AVG}).loc[1969:2025].round(6).to_csv(os.path.join(OUT, "world_hour_growth_annual.csv"))

# ------------------------------------------------------------------ 5. national hours (LCU GDP per hour worked)
def pwt_cache(sid):
    s = pd.read_csv(cnd(f"{sid}.csv"), index_col=0, parse_dates=True).iloc[:, 0]; s.index = s.index.year; return pd.to_numeric(s, errors="coerce")
I2 = {"AUS": "AU", "BEL": "BE", "CHE": "CH", "DEU": "DE", "DNK": "DK", "ESP": "ES", "FIN": "FI", "FRA": "FR", "GBR": "GB", "ITA": "IT", "JPN": "JP", "NLD": "NL", "NOR": "NO", "PRT": "PT", "SWE": "SE", "USA": "US"}
j = json.load(open(cnd("wb_ngdp_lcu.json")))[1]
NG = pd.DataFrame([(r["countryiso3code"], int(r["date"]), r["value"]) for r in j if r["value"] is not None and r["countryiso3code"]], columns=["c", "y", "v"]).pivot_table(index="y", columns="c", values="v", aggfunc="first").sort_index()
HRS = {}
for c3, c2 in I2.items():
    for f in [f"EMPENG{c2}A148NRUG", f"AVHWPE{c2}A065NRUG"]: LOG["inputs_sha256"][f + ".csv"] = sha(cnd(f + ".csv"))
    HRS[c3] = (pwt_cache(f"EMPENG{c2}A148NRUG") * pwt_cache(f"AVHWPE{c2}A065NRUG")).dropna()
HRS = pd.DataFrame(HRS)
g_wb = np.log(NG[HC] / HRS[HC].reindex(NG.index)).diff()                                              # World Bank LCU GDP / PWT hours (as world.py gdph_panel)
g_jh = np.log(GDP[HC] / HRS[HC].reindex(GDP.index)).diff()                                            # JST LCU GDP / PWT hours (reaches 1951)
g_pc = np.log(GDP[HC] / POP[HC]).diff()                                                               # JST GDP per capita (fallback proxy)
NEED_N = g_wb.reindex(g_pc.index).combine_first(g_jh).combine_first(g_pc)
SRC = pd.DataFrame(np.where(g_wb.reindex(g_pc.index).notna(), "WB/PWT", np.where(g_jh.notna(), "JST/PWT", np.where(g_pc.notna(), "JST per capita", ""))), index=g_pc.index, columns=HC)
cov = {c: {"WB_PWT_from": int(g_wb[c].first_valid_index()), "JST_PWT_from": int(g_jh[c].first_valid_index()), "WB_PWT_to": int(g_wb[c].last_valid_index())} for c in HC}
LOG["national_hour_coverage"] = cov
def cmp(a, b_, y0, y1):
    x = pd.concat([a.loc[y0:y1].stack(), b_.loc[y0:y1].stack()], axis=1).dropna(); return {"n": len(x), "corr": round(float(x.corr().iloc[0, 1]), 3), "mean_diff_pct": round(float((x[0] - x[1]).mean() * 100), 3)}
LOG["gdph_vs_proxies"] = {"WB_PWT_vs_JST_per_capita_1961_2020": cmp(g_wb.reindex(g_pc.index), g_pc, 1961, 2020), "WB_PWT_vs_JST_PWT_1961_2020": cmp(g_wb.reindex(g_pc.index), g_jh, 1961, 2020),
                          "JST_PWT_vs_JST_per_capita_1951_2020": cmp(g_jh, g_pc, 1951, 2020),
                          "country_mean_diff_WB_PWT_minus_per_capita_1976_2020_pct": {c: round(float((g_wb[c].reindex(g_pc.index) - g_pc[c]).loc[1976:2020].mean() * 100), 2) for c in HC}}
NEED_N_DEC = 0.5 * (NEED_N + NEED_N.shift(-1))                                                        # Dec-to-Dec from mid-year points (log-interpolated), robustness
NEED_N_PC = g_pc

def national(tot, need, y0, y1, extra_cash=None):
    """per-country means of tot - need, plus GDP-weighted aggregate (weighted average of country nets each year)"""
    net = (tot - need[tot.columns]).loc[y0:y1]
    per = (net.mean() * 1000).where(net.notna().sum() >= 0.8 * (y1 - y0 + 1))
    w = weights(net.notna() & W_USD.loc[y0:y1, tot.columns].notna()).loc[y0:y1]
    agg = float((w * net).sum(axis=1).mean() * 1000); return per, agg, net
# housing national table
rows = []; PERN = PER + [(1951, 2020), (1951, 1975)]
for a, b in PERN:
    r = {"period": lab(a, b)}
    for k, x in [("total", tot_l), ("cash", cash), ("valuation", val), ("price_ex_valuation", pxv_l)]:
        w = weights(tot_l.notna() & val.notna() & NEED_N.notna() & W_USD[HC].notna()).loc[a:b]; r[k] = float((w * x.loc[a:b]).sum(axis=1).mean() * 1000)
    r["needed"] = float((w * NEED_N.loc[a:b]).sum(axis=1).mean() * 1000); r["net"] = r["total"] - r["needed"]; r["net_ex_valuation"] = r["net"] - r["valuation"]
    per, _, _ = national(tot_l, NEED_N, a, b); per_x, _, _ = national(tot_l - val, NEED_N, a, b)
    r.update({"net_country_min": per.min(), "net_country_median": per.median(), "net_country_max": per.max(), "net_ex_val_country_median": per_x.median(), "countries": int(per.notna().sum())}); rows.append(r)
T_N = pd.DataFrame(rows).set_index("period").round(1); T_N.to_csv(os.path.join(OUT, "table_housing_national_hours.csv"))
# per country 1976-2020 and 1951-2020
PC = {}
for a, b in [(1976, 2020), (1951, 2020)]:
    ok = tot_l.notna() & val.notna() & NEED_N[HC].notna()                                              # same years for every component (BEL 1976: no rent-yield change)
    for k, x in [("total", tot_l), ("cash", cash), ("valuation", val), ("price_ex_valuation", pxv_l), ("needed", NEED_N[HC])]:
        PC[(lab(a, b), k)] = x.where(ok).loc[a:b].mean() * 1000
    PC[(lab(a, b), "net")] = PC[(lab(a, b), "total")] - PC[(lab(a, b), "needed")]; PC[(lab(a, b), "net_ex_valuation")] = PC[(lab(a, b), "net")] - PC[(lab(a, b), "valuation")]
    PC[(lab(a, b), "years")] = ok.loc[a:b].sum()
    PC[(lab(a, b), "first_year")] = tot_l.where(ok).loc[a:b].apply(lambda s: s.first_valid_index())
PCT = pd.DataFrame(PC).round(1); PCT.to_csv(os.path.join(OUT, "table_housing_by_country_national_hours.csv"))
# world hours by country (USD)
PCW = pd.DataFrame({"total_usd": tot_u.loc[1976:2020].mean() * 1000, "cash": cash.loc[1976:2020].mean() * 1000, "valuation": val.loc[1976:2020].mean() * 1000,
                    "price_ex_valuation_usd": pxv_u.loc[1976:2020].mean() * 1000, "needed_world": NEED_W.loc[1976:2020].mean() * 1000}); PCW["net"] = PCW.total_usd - PCW.needed_world
PCW["net_ex_valuation"] = PCW.net - PCW.valuation; PCW.round(1).to_csv(os.path.join(OUT, "table_housing_by_country_world_hours.csv"))

# ------------------------------------------------------------------ 6. the household's other claims (bills, bonds, equities): hour return of each claim
CL = {"housing": tot_l, "deposits_bills": np.log1p(BILL[HC]), "gov_bonds": np.log1p(BOND[HC]), "equities": np.log1p(EQ[HC])}
rows = []
for k, x in CL.items():
    xu = x - dfx[HC]; r = {"claim": k}
    wu = agg_housing(xu, cash, val).total if k == "housing" else agg_simple(xu.where(tot_l.notna()))   # same 16 countries, same years as housing
    for a, b in [(1976, 2020), (1976, 1981), (1982, 2000), (2001, 2020)]:
        r[f"world_total_{lab(a, b)}"] = wu.loc[a:b].mean() * 1000; r[f"world_net_{lab(a, b)}"] = (wu - NEED_W).loc[a:b].mean() * 1000
    for a, b in [(1976, 2020), (1951, 2020)]:
        per, aggn, _ = national(x.where(tot_l.notna() & val.notna()), NEED_N, a, b)                    # same years as Table A1 (rent-yield change available)
        r[f"national_net_gdpw_{lab(a, b)}"] = aggn; r[f"national_net_median_{lab(a, b)}"] = per.median(); r[f"national_net_min_{lab(a, b)}"] = per.min(); r[f"national_net_max_{lab(a, b)}"] = per.max()
    rows.append(r)
g = {"claim": "gmp"}
for a, b in [(1976, 2020), (1976, 1981), (1982, 2000), (2001, 2020)]: g[f"world_total_{lab(a, b)}"] = GMP.total.loc[a:b].mean() * 1000; g[f"world_net_{lab(a, b)}"] = (GMP.total - NEED_W).loc[a:b].mean() * 1000
rows.append(g); T_C = pd.DataFrame(rows).set_index("claim").round(1); T_C.T.to_csv(os.path.join(OUT, "table_hour_return_by_claim.csv"))
# per country, each claim, national hours 1976-2020 and 1951-2020
pcc = {}
for k, x in CL.items():
    for a, b in [(1976, 2020), (1951, 2020)]: pcc[(k, lab(a, b))] = national(x.where(tot_l.notna() & val.notna()), NEED_N, a, b)[0]
pd.DataFrame(pcc).round(1).to_csv(os.path.join(OUT, "table_claims_by_country_national_hours.csv"))

# ------------------------------------------------------------------ 7. robustness (housing, 1976-2020 unless stated)
def net_w(X, need=NEED_W, a=1976, b=2020): return float((X.total - need).loc[a:b].mean() * 1000)
def netx_w(X, need=NEED_W, a=1976, b=2020): return float((X.total - X.val - need).loc[a:b].mean() * 1000)
base = net_w(HW); tc10 = -np.log(1 - 0.077) / 10 * 1000; tc20 = -np.log(1 - 0.077) / 20 * 1000
nat = T_N.loc["1976-2020"]
ROB = [("Baseline: world hours, GDP weights", base, netx_w(HW)),
       ("Property tax 1 pt a year", base - 10, netx_w(HW) - 10),
       ("Transaction costs 7.7% round trip, 10-year hold", base - tc10, netx_w(HW) - tc10),
       ("Transaction costs 7.7% round trip, 20-year hold", base - tc20, netx_w(HW) - tc20),
       ("Property tax 1 pt + costs over 10 years", base - 10 - tc10, netx_w(HW) - 10 - tc10),
       ("Equal weights", net_w(HW_EQ), netx_w(HW_EQ)), ("Ex-USA (GDP weights)", net_w(HW_XUS), netx_w(HW_XUS)),
       ("World hour on annual-average timing", net_w(HW, NEED_W_AVG), netx_w(HW, NEED_W_AVG)),
       ("National hours, GDP weights, 1976-2020", nat["net"], nat["net_ex_valuation"]),
       ("National hours, country median, 1976-2020", nat["net_country_median"], nat["net_ex_val_country_median"]),
       ("National hours, Dec-to-Dec interpolated hour, median, 1976-2019", national(tot_l, NEED_N_DEC, 1976, 2019)[0].median(), national(tot_l - val, NEED_N_DEC, 1976, 2019)[0].median()),
       ("Baseline national hour, median, same window 1976-2019", national(tot_l, NEED_N, 1976, 2019)[0].median(), national(tot_l - val, NEED_N, 1976, 2019)[0].median()),
       ("National hours from GDP per head (JST), median", national(tot_l, NEED_N_PC, 1976, 2020)[0].median(), national(tot_l - val, NEED_N_PC, 1976, 2020)[0].median()),
       ("National hours, GDP weights, 1951-2020", T_N.loc["1951-2020", "net"], T_N.loc["1951-2020", "net_ex_valuation"]),
       ("National hours, country median, 1951-2020", T_N.loc["1951-2020", "net_country_median"], T_N.loc["1951-2020", "net_ex_val_country_median"]),
       ("GMP, world hours (for comparison)", net_w(GMP), netx_w(GMP))]
T_R = pd.DataFrame(ROB, columns=["case", "net_per_1000h", "net_ex_valuation_per_1000h"]).round(1); T_R.to_csv(os.path.join(OUT, "table_housing_robustness.csv"), index=False)
LOG["transaction_cost_hours_per_year"] = {"10y": round(tc10, 1), "20y": round(tc20, 1)}
# rolling 20-year windows, world hours
RL = []
for e in range(1995, 2021):
    a = e - 19; RL.append({"window": lab(a, e), "housing_net": net_w(HW, a=a, b=e), "gmp_net": net_w(GMP, a=a, b=e), "housing_net_ex_val": netx_w(HW, a=a, b=e), "gmp_net_ex_val": netx_w(GMP, a=a, b=e)})
T_RL = pd.DataFrame(RL).set_index("window").round(1); T_RL["housing_minus_gmp"] = T_RL.housing_net - T_RL.gmp_net; T_RL.to_csv(os.path.join(OUT, "table_rolling20_housing_vs_gmp.csv"))
# by decade
DEC = [(1976, 1980), (1981, 1990), (1991, 2000), (2001, 2010), (2011, 2020)]
T_D = pd.concat({"housing": hours_table(HW, NEED_W, DEC)[["total", "cash", "valuation", "needed", "net", "net_ex_valuation"]], "gmp": hours_table(GMP, NEED_W, DEC)[["total", "cash", "valuation", "needed", "net", "net_ex_valuation"]]}, axis=1)
T_D.to_csv(os.path.join(OUT, "table_decades_housing_vs_gmp.csv"))
corr = float(pd.concat([HW.total - NEED_W, GMP.total - NEED_W], axis=1).loc[1976:2020].corr().iloc[0, 1])
LOG["corr_annual_net_housing_gmp_1976_2020"] = round(corr, 3)
LOG["vol_annual_net_pct"] = {"housing": round(float((HW.total - NEED_W).loc[1976:2020].std() * 100), 2), "gmp": round(float((GMP.total - NEED_W).loc[1976:2020].std() * 100), 2)}

# rent yield (note 3 §7 convention: same-year weights) vs GMP cash yield
ryw = GUSD[HC].where(YD.notna()); ryw = ryw.div(ryw.sum(axis=1), axis=0); RENTY = (YD * 100 * ryw).sum(axis=1, min_count=1)
rnet = (RR * 100 * weights(RR.notna() & W_USD[HC].notna())).sum(axis=1, min_count=1)
YT = pd.DataFrame({"rent_yield_pct_same_year_w": RENTY, "rent_return_pct_lagged_w": rnet, "gmp_cash_yield_pct": gyield}).loc[1950:2020].round(3); YT.to_csv(os.path.join(OUT, "rent_vs_gmp_cash_yield.csv"))

# ------------------------------------------------------------------ 8. figures
cumH = 1000 * np.exp((HW.total - NEED_W).loc[1976:2020].cumsum()); cumG = 1000 * np.exp((GMP.total - NEED_W).loc[1976:2020].cumsum())
cumHx = 1000 * np.exp((HW.total - HW.val - NEED_W).loc[1976:2020].cumsum()); cumGx = 1000 * np.exp((GMP.total - GMP.val - NEED_W).loc[1976:2020].cumsum())
for s in (cumH, cumG, cumHx, cumGx): s.loc[1975] = 1000.0; s.sort_index(inplace=True)
pd.DataFrame({"housing": cumH, "gmp": cumG, "housing_ex_val": cumHx, "gmp_ex_val": cumGx}).sort_index().round(1).to_csv(os.path.join(OUT, "fig_a_cumulative.csv"))
fig, ax = plt.subplots(figsize=(8.4, 4.2))
ax.plot(cumH.sort_index(), color=PAL[2], lw=1.8, label="Housing, 16 countries, GDP-weighted (Macrohistory Database, net rent reinvested)")
ax.plot(cumG.sort_index(), color=PAL[0], lw=1.8, label="Global market portfolio (note 3)")
ax.plot(cumHx.sort_index(), color=PAL[2], lw=1.0, ls="--", label="Housing, ex valuation change"); ax.plot(cumGx.sort_index(), color=PAL[0], lw=1.0, ls="--", label="GMP, ex valuation change")
ax.axhline(1000, color="grey", lw=0.6); ax.set_yscale("log"); ax.set_ylabel("world hours (log scale)")
from matplotlib.ticker import FixedLocator, FuncFormatter, NullLocator; ax.yaxis.set_major_locator(FixedLocator([1000, 1500, 2000, 3000, 4000, 6000])); ax.yaxis.set_minor_locator(NullLocator()); ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}"))
ax.set_title("1,000 hours of world work placed in housing or in the GMP at end-1975, in world hours", loc="left", fontsize=9.5); ax.legend(fontsize=7.5, frameon=False); fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig_a_cumulative_hours.png"), dpi=160); plt.close(fig)
pc = PCT[("1976-2020", "net")].sort_values(); pcx = PCT[("1976-2020", "net_ex_valuation")].reindex(pc.index)
fig, ax = plt.subplots(figsize=(8.4, 4.2)); x = np.arange(len(pc))
ax.bar(x - 0.2, pc.values, 0.4, color=PAL[2], label="Net"); ax.bar(x + 0.2, pcx.values, 0.4, color=PAL[3], label="Net ex valuation change")
ax.axhline(0, color="k", lw=0.6); ax.axhline(pc.median(), color=PAL[2], lw=0.8, ls=":"); ax.set_xticks(x); ax.set_xticklabels(pc.index, fontsize=7.5); ax.set_ylabel("hours a year per 1,000 hours")
ax.set_title("Housing in each country's own hours (local nominal GDP per hour worked), 1976\u20132020", loc="left", fontsize=9.5); ax.legend(fontsize=7.5, frameon=False); fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig_b_country_net_national_hours.png"), dpi=160); plt.close(fig)
fig, ax = plt.subplots(figsize=(8.4, 4.2)); y = YT.loc[1950:2020]
ax.plot(y.index, y.rent_yield_pct_same_year_w, color=PAL[2], lw=1.6, label="Net rent yield, 16 countries, GDP-weighted (JST)")
ax.plot(y.index, y.gmp_cash_yield_pct, color=PAL[0], lw=1.6, label="GMP cash distribution yield (note 3, annual mean)")
ax.set_ylabel("% a year"); ax.set_ylim(bottom=0); ax.set_title("Rent yield on housing vs the cash yield of the GMP", loc="left", fontsize=9.5); ax.legend(fontsize=7.5, frameon=False); fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig_c_rent_vs_gmp_yield.png"), dpi=160); plt.close(fig)

# ------------------------------------------------------------------ 9. log
for p in INPUTS: LOG["inputs_sha256"][label(p)] = sha(p)
LOG["headline_1976_2020_per_1000h"] = {"housing": T_H.loc["1976-2020"].to_dict(), "gmp": T_G.loc["1976-2020"].to_dict()}
LOG["national_1976_2020"] = T_N.loc["1976-2020"].to_dict(); LOG["national_1951_2020"] = T_N.loc["1951-2020"].to_dict()
LOG["rent_yield"] = {str(yy): round(float(RENTY.loc[yy]), 2) for yy in [1950, 1976, 2000, 2020]}; LOG["gmp_cash_yield"] = {str(yy): round(float(gyield.loc[yy]), 2) for yy in [1976, 2000, 2020]}
LOG["rolling20_housing_beats_gmp"] = f"{int((T_RL.housing_minus_gmp > 0).sum())} of {len(T_RL)}"
json.dump(LOG, open(os.path.join(OUT, "build_log.json"), "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
pd.set_option("display.width", 250)
print(side.to_string()); print(T_N.to_string()); print(T_C.T.to_string()); print(T_R.to_string()); print(T_RL.to_string()); print(T_D.to_string()); print(PCT.to_string())
print(json.dumps({k: LOG[k] for k in ["identity_source", "identity_components", "xrusd_timing", "gdph_vs_proxies", "national_hour_coverage", "corr_annual_net_housing_gmp_1976_2020", "vol_annual_net_pct", "rent_yield", "gmp_cash_yield", "note3_rent_weight_bug", "jst_gdp_unit_log10", "housing_logavg_minus_portfolio_total_pct_1976_2020", "housing_usa_weight_1976_2020_mean", "gmp_components_check_max_abs_ltr_vs_log1p_TR"]}, indent=0, default=str))
