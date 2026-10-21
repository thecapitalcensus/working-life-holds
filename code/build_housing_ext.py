# -*- coding: utf-8 -*-
"""Note 4 sec. 4, extension: (1) housing decomposition chained to 2021-2025 with OECD analytical house price indicators
(nominal HPI, rent index = CPI actual rents); (2) cross-check of JST against OECD 1976-2020; (3) robustness with OECD rent
growth in place of JST implied rent growth.  Runs build_housing.py first (exec into this namespace) and extends it.
Extension rules: price growth = OECD annual HPI growth (annual average of quarters); rent yield_t = JST 2020 rent yield x
(RPI_t/RPI_2020)/(HPI_t/HPI_2020); net rent cash return = yield_t x (1 + price growth_t), the JST convention (rent of year t
over price at end t-1); FX = BIS December monthly average (JST xrusd is end-year); weights = World Bank USD GDP of t-1;
national hour = World Bank LCU GDP / PWT hours, hours after 2023 extended with World Bank labour force."""
import os, sys, io, json, contextlib, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); NS = {"__file__": os.path.join(HERE, "build_housing.py"), "__name__": "build_housing"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(open(NS["__file__"]).read(), NS["__file__"], "exec"), NS)
G = NS; OUT, cnd, B, HC, LOG, DC, label = G["OUT"], G["cnd"], G["B"], G["HC"], G["LOG"], G["DC"], G["label"]; sha = G["sha"]; plt = G["plt"]; PAL = G["PAL"]
OECDF = os.path.join(DC, "oecd_house_prices.csv"); WBF = os.path.join(DC, "worldbank_gdp.csv"); RENTUS = os.path.join(OUT, "ext_inputs", "CUUR0000SEHA.csv")
BISF = cnd("bis_xru.csv"); LFF = cnd("wb_lf.json")
EXT = {"inputs_sha256": {label(p): sha(p) for p in [OECDF, WBF, RENTUS, BISF, LFF]}}
YE = list(range(2021, 2026))

# ------------------------------------------------------------------ OECD annual series (fill a missing year from the quarters available)
o = pd.read_csv(OECDF)
def oecd(var):
    a = o[(o.freq == "A") & (o.variable == var) & o.iso3.isin(HC)].assign(y=lambda x: x.period.astype(int)).pivot(index="y", columns="iso3", values="value")
    q = o[(o.freq == "Q") & (o.variable == var) & o.iso3.isin(HC)].assign(y=lambda x: x.period.str[:4].astype(int), qq=lambda x: x.period.str[-1].astype(int))
    fills = {}
    for c in HC:
        if c not in a or 2025 in a[c].dropna().index: continue
        qc = q[q.iso3 == c].set_index(["y", "qq"]).value; have = [k for (yy, k) in qc.index if yy == 2025]
        if have and all((2024, k) in qc.index for k in have) and 2024 in a[c].dropna().index:
            a.loc[2025, c] = a.loc[2024, c] * np.mean([qc[(2025, k)] for k in have]) / np.mean([qc[(2024, k)] for k in have]); fills[c] = f"2025 from Q{min(have)}-Q{max(have)} vs same quarters of 2024"
    return a.sort_index(), fills
HPI, f1 = oecd("HPI"); RPI, f2 = oecd("RPI"); PR, f3 = oecd("HPI_RPI")
us = pd.read_csv(RENTUS); us.columns = ["d", "v"]; us["y"] = pd.to_datetime(us.d).dt.year; usy = pd.to_numeric(us.v, errors="coerce").groupby(us.y).mean()
if pd.isna(RPI.loc[2025, "USA"]):
    RPI.loc[2025, "USA"] = RPI.loc[2024, "USA"] * usy.loc[2025] / usy.loc[2024]; f2["USA"] = "2025 from BLS CPI rent of primary residence (FRED CUUR0000SEHA, annual mean) growth"
EXT["oecd_2025_fills"] = {"HPI": f1, "RPI": f2, "HPI_RPI": f3}

# ------------------------------------------------------------------ (1) chain JST to 2021-2025
TR, RR, YD, CG = [G[k].copy() for k in ["TR", "RR", "YD", "CG"]]
for y in YE:
    for c in HC:
        cg = HPI.loc[y, c] / HPI.loc[y - 1, c] - 1; yd = YD.loc[2020, c] * (RPI.loc[y, c] / RPI.loc[2020, c]) / (HPI.loc[y, c] / HPI.loc[2020, c])
        CG.loc[y, c] = cg; YD.loc[y, c] = yd; RR.loc[y, c] = yd * (1 + cg); TR.loc[y, c] = cg + yd * (1 + cg)
assert TR.loc[YE].notna().all().all()
# FX: JST end-year to 2020, then BIS December average growth
x = pd.read_csv(BISF, low_memory=False); x = x[x.TIME_PERIOD.str.endswith("-12")]; x["y"] = x.TIME_PERIOD.str[:4].astype(int)
bis = x.pivot_table(index="y", columns="REF_AREA", values="OBS_VALUE"); bis["US"] = 1.0
I2 = G["I2"]; dfx_b = np.log(pd.DataFrame({c3: bis[c2] for c3, c2 in I2.items()})).diff()
FX = G["FX"].copy(); dfx = np.log(FX).diff()
for y in YE: dfx.loc[y, HC] = dfx_b.loc[y, HC]
EXT["fx_check_2020_JST_vs_BIS_dec_logdiff_maxabs"] = float((np.log(G["FX"].loc[2020, ["JPN", "GBR", "CHE", "SWE", "NOR", "DNK", "AUS"]]) - np.log(pd.Series({c3: bis.loc[2020, I2[c3]] for c3 in ["JPN", "GBR", "CHE", "SWE", "NOR", "DNK", "AUS"]}))).abs().max())
# weights: JST USD GDP (unit-fixed) to 2020, World Bank USD GDP after
wb = pd.read_csv(WBF); wbu = wb[wb.variable == "NY.GDP.MKTP.CD"].pivot_table(index="year", columns="iso3", values="value"); wbl = wb[wb.variable == "NY.GDP.MKTP.CN"].pivot_table(index="year", columns="iso3", values="value")
GUSD = G["GUSD"].copy()
for y in range(2021, 2026): GUSD.loc[y, HC] = wbu.loc[y, HC]
W_USD = GUSD.shift(1); EXT["weights_2020_jst_vs_wb_usd_ratio_range"] = [float((G["GUSD"].loc[2020, HC] / wbu.loc[2020, HC]).min()), float((G["GUSD"].loc[2020, HC] / wbu.loc[2020, HC]).max())]
# national hour 2021-2025
j = json.load(open(LFF))[1]; lf = pd.DataFrame([(r["countryiso3code"], int(r["date"]), r["value"]) for r in j if r["value"] is not None and r["countryiso3code"]], columns=["c", "y", "v"]).pivot_table(index="y", columns="c", values="v")
HRS = G["HRS"].copy()
for y in range(int(HRS.index.max()) + 1, 2026):
    for c in HC: HRS.loc[y, c] = HRS.loc[y - 1, c] * lf.loc[y, c] / lf.loc[y - 1, c]
NEED_N = G["NEED_N"].copy(); gx = np.log(wbl[HC] / HRS[HC].reindex(wbl.index)).diff()
for y in YE: NEED_N.loc[y, HC] = gx.loc[y, HC]
EXT["national_hour_2021_2025"] = "World Bank NY.GDP.MKTP.CN (clean file) / PWT hours (FRED vintage to 2023; 2024-25 by WB labour-force growth)"
# put everything back into the base namespace and recompute components
tot_l = np.log1p(TR); cash = np.log1p(RR); val = -np.log(YD).diff(); pxv_l = tot_l - cash - val; tot_u = tot_l - dfx[HC]
G.update(W_USD=W_USD, NEED_N=NEED_N)
HW = G["agg_housing"](tot_u, cash, val); HW_EQ = G["agg_housing"](tot_u, cash, val, "eq"); HW_XUS = G["agg_housing"](tot_u, cash, val, excl=("USA",))
GMP, NEED_W = G["GMP"], G["NEED_W"]; assert GMP.total.loc[2021:2025].notna().all() and NEED_W.loc[2021:2025].notna().all()
PERX = [(1976, 1981), (1982, 2000), (2001, 2020), (2021, 2025), (1976, 2020), (1976, 2025)]
T_H = G["hours_table"](HW, NEED_W, PERX); T_G = G["hours_table"](GMP, NEED_W, PERX)
side = pd.concat({"housing": T_H.T, "gmp": T_G.T}, axis=1); side.to_csv(os.path.join(OUT, "table_housing_vs_gmp_world_hours_to2025.csv"))
HW.round(6).to_csv(os.path.join(OUT, "housing_world_annual_to2025.csv"))
EXT["world_hour_provisional_note"] = "world hour hard data to 2025-06 (note 3); Dec-2025 value uses provisional months"
# national hours table to 2025
rows = []
for a, b in PERX:
    w = G["weights"](tot_l.notna() & val.notna() & NEED_N.notna() & W_USD[HC].notna()).loc[a:b]; r = {"period": f"{a}-{b}"}
    for k, xx in [("total", tot_l), ("cash", cash), ("valuation", val), ("price_ex_valuation", pxv_l), ("needed", NEED_N[HC])]: r[k] = float((w * xx.loc[a:b]).sum(axis=1).mean() * 1000)
    r["net"] = r["total"] - r["needed"]; r["net_ex_valuation"] = r["net"] - r["valuation"]
    per = ((tot_l - NEED_N[HC]).loc[a:b].mean() * 1000); perx = ((tot_l - val - NEED_N[HC]).loc[a:b].mean() * 1000)
    r.update(net_country_min=per.min(), net_country_median=per.median(), net_country_max=per.max(), net_ex_val_country_median=perx.median()); rows.append(r)
T_N = pd.DataFrame(rows).set_index("period").round(1); T_N.to_csv(os.path.join(OUT, "table_housing_national_hours_to2025.csv"))
pc25 = pd.DataFrame({k: xx.loc[2021:2025].mean() * 1000 for k, xx in [("total", tot_l), ("cash", cash), ("valuation", val), ("price_ex_valuation", pxv_l), ("needed", NEED_N[HC])]})
pc25["net"] = pc25.total - pc25.needed; pc25.round(1).to_csv(os.path.join(OUT, "table_housing_by_country_national_hours_2021_2025.csv"))

# ------------------------------------------------------------------ (2) cross-check JST vs OECD, 1976-2020
hp = G["pv"]("hpnom")[HC]; jst_p = np.log(hp).diff(); jst_p2 = np.log1p(G["CG"]); jst_pr = G["val"]; jst_r = G["drent"]
oe_p = np.log(HPI).diff(); oe_pr = np.log(PR).diff(); oe_r = np.log(RPI).diff()
EXT["jst_hpnom_vs_capgain_maxabs"] = float((jst_p - jst_p2).loc[1976:2020].abs().max().max())
rows = []
for c in HC:
    r = {"country": c}
    for nm, a_, b_ in [("price", jst_p, oe_p), ("price_rent", jst_pr, oe_pr), ("rent", jst_r, oe_r)]:
        z = pd.concat([a_[c], b_[c]], axis=1).loc[1976:2020].dropna()
        r[f"{nm}_n"] = len(z); r[f"{nm}_corr"] = z.corr().iloc[0, 1] if len(z) > 2 else np.nan; r[f"{nm}_gap_jst_minus_oecd_pt"] = (z.iloc[:, 0] - z.iloc[:, 1]).mean() * 100 if len(z) else np.nan
    rows.append(r)
XC = pd.DataFrame(rows).set_index("country"); XC.loc["median"] = XC.median(); XC.round(3).to_csv(os.path.join(OUT, "table_crosscheck_jst_vs_oecd.csv"))

# ------------------------------------------------------------------ (3) OECD rent growth in place of JST implied rent growth
pxv_alt = oe_r.reindex(pxv_l.index)[HC].where(lambda s: s.notna(), pxv_l); used = int((oe_r.reindex(pxv_l.index)[HC].loc[1976:2020].notna()).sum().sum())
tot_alt_l = cash + val + pxv_alt; tot_alt_u = tot_alt_l - dfx[HC]; HWA = G["agg_housing"](tot_alt_u, cash, val)
def nw(X, a, b): return float((X.total - NEED_W).loc[a:b].mean() * 1000)
def nwx(X, a, b): return float((X.total - X.val - NEED_W).loc[a:b].mean() * 1000)
def natmed(t, a, b): return float(((t - NEED_N[HC]).loc[a:b].mean() * 1000).median())
tc10 = LOG["transaction_cost_hours_per_year"]["10y"]
ROBX = [("Baseline, world hours, 1976-2020", nw(HW, 1976, 2020), nwx(HW, 1976, 2020)), ("Baseline, world hours, 1976-2025", nw(HW, 1976, 2025), nwx(HW, 1976, 2025)),
        ("OECD rent growth for JST implied rent growth, world, 1976-2020", nw(HWA, 1976, 2020), nwx(HWA, 1976, 2020)),
        ("OECD rent growth for JST implied rent growth, world, 1976-2025", nw(HWA, 1976, 2025), nwx(HWA, 1976, 2025)),
        ("OECD rent growth, national-hour country median, 1976-2020", natmed(tot_alt_l, 1976, 2020), natmed(tot_alt_l - val, 1976, 2020)),
        ("JST baseline, national-hour country median, 1976-2020", natmed(tot_l, 1976, 2020), natmed(tot_l - val, 1976, 2020)),
        ("Equal weights, 1976-2025", nw(HW_EQ, 1976, 2025), nwx(HW_EQ, 1976, 2025)), ("Ex-USA, 1976-2025", nw(HW_XUS, 1976, 2025), nwx(HW_XUS, 1976, 2025)),
        ("Property tax 1 pt + 7.7% costs over 10 years, 1976-2025", nw(HW, 1976, 2025) - 10 - tc10, nwx(HW, 1976, 2025) - 10 - tc10),
        ("GMP, world hours, 1976-2025", nw(GMP, 1976, 2025), nwx(GMP, 1976, 2025))]
TRX = pd.DataFrame(ROBX, columns=["case", "net_per_1000h", "net_ex_valuation_per_1000h"]).round(1); TRX.to_csv(os.path.join(OUT, "table_housing_robustness_ext.csv"), index=False)
EXT["oecd_rent_country_years_used_1976_2020"] = used; EXT["mean_pxv_jst_minus_oecd_rent_world_wtd_pt_1976_2020"] = round(float((HW.pxv - HWA.pxv).loc[1976:2020].mean() * 100), 3)

# ------------------------------------------------------------------ figure (a) to 2025
cumH = 1000 * np.exp((HW.total - NEED_W).loc[1976:2025].cumsum()); cumG = 1000 * np.exp((GMP.total - NEED_W).loc[1976:2025].cumsum())
cumHx = 1000 * np.exp((HW.total - HW.val - NEED_W).loc[1976:2025].cumsum()); cumGx = 1000 * np.exp((GMP.total - GMP.val - NEED_W).loc[1976:2025].cumsum())
F = pd.DataFrame({"housing": cumH, "gmp": cumG, "housing_ex_val": cumHx, "gmp_ex_val": cumGx}); F.loc[1975] = 1000.0; F = F.sort_index(); F.round(1).to_csv(os.path.join(OUT, "fig_a_cumulative_to2025.csv"))
from matplotlib.ticker import FixedLocator, FuncFormatter, NullLocator
fig, ax = plt.subplots(figsize=(8.4, 4.2))
ax.plot(F.housing, color=PAL[2], lw=1.8, label="Housing, 16 countries, GDP-weighted (Macrohistory Database to 2020, OECD-chained 2021\u201325)"); ax.plot(F.gmp, color=PAL[0], lw=1.8, label="Global market portfolio (note 3)")
ax.plot(F.housing_ex_val, color=PAL[2], lw=1.0, ls="--", label="Housing, ex valuation change"); ax.plot(F.gmp_ex_val, color=PAL[0], lw=1.0, ls="--", label="GMP, ex valuation change")
ax.axvspan(2020.5, 2025.5, color="grey", alpha=0.08, lw=0); ax.axhline(1000, color="grey", lw=0.6); ax.set_yscale("log"); ax.set_ylabel("world hours (log scale)")
ax.yaxis.set_major_locator(FixedLocator([1000, 1500, 2000, 3000, 4000, 6000])); ax.yaxis.set_minor_locator(NullLocator()); ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}"))
ax.set_title("1,000 hours of world work placed in housing or in the GMP at end-1975, in world hours", loc="left", fontsize=9.5); ax.legend(fontsize=7.5, frameon=False); fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig_a_cumulative_hours_to2025.png"), dpi=160); plt.close(fig)

# ------------------------------------------------------------------ log
EXT["headline_world_per_1000h"] = {"housing": T_H.to_dict(orient="index"), "gmp": T_G.to_dict(orient="index")}
EXT["national_per_1000h"] = T_N.to_dict(orient="index"); EXT["robustness_ext"] = TRX.set_index("case").to_dict(orient="index")
EXT["crosscheck_median"] = XC.loc["median"].round(3).to_dict(); EXT["rent_yield_2025_gdpw_pct"] = round(float((YD.loc[2025, HC] * 100 * GUSD.loc[2025, HC] / GUSD.loc[2025, HC].sum()).sum()), 2)
EXT["gmp_cash_yield_2025_pct"] = round(float(G["gyield"].loc[2025]), 2)
L = json.load(open(os.path.join(OUT, "build_log.json"))); L["extension_2021_2025"] = EXT
json.dump(L, open(os.path.join(OUT, "build_log.json"), "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
pd.set_option("display.width", 250)
print(side.to_string()); print(T_N.to_string()); print(XC.round(2).to_string()); print(TRX.to_string()); print(pc25.round(1).to_string())
print(json.dumps({k: EXT[k] for k in ["oecd_2025_fills", "fx_check_2020_JST_vs_BIS_dec_logdiff_maxabs", "weights_2020_jst_vs_wb_usd_ratio_range", "jst_hpnom_vs_capgain_maxabs", "oecd_rent_country_years_used_1976_2020", "mean_pxv_jst_minus_oecd_rent_world_wtd_pt_1976_2020", "rent_yield_2025_gdpw_pct", "gmp_cash_yield_2025_pct"]}, indent=0, default=str))
