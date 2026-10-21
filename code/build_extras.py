# -*- coding: utf-8 -*-
"""Note 4, section 4: two measurement variants of the housing headline that the paper quotes, computed from data
(first found by the independent check, check/check_housing.py; confirmed here with the builder's own loaders).
  (1) valuation measured as the change in the yield of the 16-country portfolio itself (same start-of-year weights in
      both years), instead of the GDP-weighted mean of each country's -dlog rent yield;
  (2) same-year instead of start-of-year GDP weights.
Loaders and aggregation copied from build_housing.py (which writes files on import).  Writes output/housing/extras.json."""
import os, json, hashlib, numpy as np, pandas as pd

from paths import B, JSTF, CN, GMPC, GMPR, DC, PWTX, SITE_CSS, cnd, label   # release: input locations (env-var overrides) and log labels, see paths.py
OUT = os.path.join(B, "output", "housing")
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
INPUTS = [JSTF, os.path.join(CN, "world_yardsticks_usd.csv"), os.path.join(CN, "world_q_gdp_per_hour_level_usd.csv"), cnd("wb_gdp.json")]

d = pd.read_excel(JSTF)
def pv(v): return d.pivot(index="year", columns="iso", values=v).sort_index()
TR, RR, YD = pv("housing_tr"), pv("housing_rent_rtn"), pv("housing_rent_yd")
HC = [c for c in TR.columns if TR[c].notna().any()]; assert len(HC) == 16
TR, RR, YD = TR[HC], RR[HC], YD[HC]; FX = pv("xrusd"); GDP = pv("gdp")
tot_l = np.log1p(TR); cash = np.log1p(RR); val = -np.log(YD).diff(); dfx = np.log(FX).diff(); tot_u = tot_l - dfx[HC]

wh_idx = pd.read_csv(INPUTS[1], index_col=0, parse_dates=True)["gdph"]
lvl_q = pd.read_csv(INPUTS[2], index_col=0, parse_dates=True).iloc[:, 0]
H = wh_idx / float(wh_idx.loc["2014-01-31":"2014-03-31"].mean()) * float(lvl_q.loc["2014-03-31"])
Hdec = H[H.index.month == 12]; Hdec.index = Hdec.index.year; NEED_W = np.log(Hdec).diff()

jw = json.load(open(INPUTS[3]))[1]
WBG = pd.DataFrame([(r["countryiso3code"], int(r["date"]), r["value"]) for r in jw if r["value"] is not None and r["countryiso3code"]], columns=["c", "y", "v"]).pivot_table(index="y", columns="c", values="v", aggfunc="first")
UNIT = 10.0 ** np.log10(WBG[GDP.columns] / (GDP / FX)).loc[1991:2020].median().round()
GUSD = (GDP / FX * UNIT)[HC]

def agg(WB):
    avail = tot_u.notna() & val.notna() & WB.notna()
    w = WB.where(avail); w = w.div(w.sum(axis=1), axis=0)
    T = np.log((w * np.expm1(tot_u)).sum(axis=1, min_count=1) + 1)
    V_mean = (w * val).sum(axis=1, min_count=1)                                                      # baseline: weighted mean of country logs
    V_port = -(np.log((w * YD).sum(axis=1, min_count=1)) - np.log((w * YD.shift(1)).sum(axis=1, min_count=1)))  # portfolio's own yield, same weights
    return pd.DataFrame({"total": T, "val_mean": V_mean, "val_port": V_port})

def stats(X, a=1976, b=2020):
    x = X.loc[a:b]; n = NEED_W.loc[a:b]
    return {"total": float(x.total.mean() * 1000), "valuation_country_mean": float(x.val_mean.mean() * 1000), "valuation_portfolio_yield": float(x.val_port.mean() * 1000),
            "net": float((x.total - n).mean() * 1000), "net_ex_valuation_country_mean": float((x.total - x.val_mean - n).mean() * 1000),
            "net_ex_valuation_portfolio_yield": float((x.total - x.val_port - n).mean() * 1000)}

base = stats(agg(GUSD.shift(1))); same = stats(agg(GUSD))
WBU = WBG.reindex(columns=HC).reindex(GUSD.index)                                                        # World Bank USD GDP (annual-average FX)
same_wb = stats(agg(WBU)); base_wb = stats(agg(WBU.shift(1)))
E = {"inputs_sha256": {label(p): sha(p) for p in INPUTS},
     "world_1976_2020_start_of_year_weights": base, "world_1976_2020_same_year_weights": same, "world_1976_2020_same_year_weights_wb_avg_fx": same_wb,
     "world_1976_2020_start_of_year_weights_wb_avg_fx": base_wb,
     "valuation_gap_country_mean_minus_portfolio": base["valuation_country_mean"] - base["valuation_portfolio_yield"],
     "net_ex_valuation_change_portfolio_vs_baseline": base["net_ex_valuation_portfolio_yield"] - base["net_ex_valuation_country_mean"],
     "note": "per 1,000 world hours a year; baseline weights are start-of-year USD GDP as in build_housing.py; confirmed by check/check_housing.py"}
# (3) labour share, PWT 11.0 labsh, 16 Macrohistory countries weighted by PWT output-side GDP (cgdpo): does pay per hour
#     keep pace with GDP per hour?  A falling share lowers the wage-bill (PAYG) return relative to hours growth.
E["inputs_sha256"][label(PWTX)] = sha(PWTX)
pw = pd.read_excel(PWTX, sheet_name="Data")
pw = pw[pw.countrycode.isin(HC)]
ls = pw.pivot(index="year", columns="countrycode", values="labsh"); wg = pw.pivot(index="year", columns="countrycode", values="cgdpo")
ok = ls.notna() & wg.notna(); w = wg.where(ok); w = w.div(w.sum(axis=1), axis=0); L = (w * ls).sum(axis=1, min_count=1)
wu = WBG.reindex(columns=HC).reindex(ls.index).where(ls.notna()); wu = wu.div(wu.sum(axis=1), axis=0); LU = (wu * ls).sum(axis=1, min_count=1)
a, b = 1976, 2019
E["labour_share_jst16"] = {"years": [a, b], "level_start": float(L.loc[a]), "level_end": float(L.loc[b]), "change_pts": float((L.loc[b] - L.loc[a]) * 100),
                           "effect_per_1000h_per_year": float(np.log(L.loc[b] / L.loc[a]) / (b - a) * 1000), "countries": int(ok.loc[a].sum()),
                           "usd_weights_level_start": float(LU.loc[a]), "usd_weights_level_end": float(LU.loc[b]), "usd_weights_effect_per_1000h_per_year": float(np.log(LU.loc[b] / LU.loc[a]) / (b - a) * 1000),
                           "mean_level_1951_2019_ppp_weights": float(L.loc[1951:2019].mean()),
                           "home_4x_pay_in_years_of_earnings": float(4 / L.loc[1951:2019].mean()), "budget_35pct_of_pay_in_pct_of_earnings": float(35 / L.loc[1951:2019].mean()),
                           "note": "GDP-weighted (PWT cgdpo) mean of PWT labsh; effect = annual log change x 1000, the gap between wage-bill growth and GDP growth"}
json.dump(E, open(os.path.join(OUT, "extras.json"), "w"), indent=1)
print(json.dumps({k: v for k, v in E.items() if k != "inputs_sha256"}, indent=1, default=str))
