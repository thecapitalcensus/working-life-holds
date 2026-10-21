# -*- coding: utf-8 -*-
"""Note 4, sections 5 and 6: the household balance sheet in hours, and the pension in hours.
5a composition (OECD T720 financial + Table 9B non-financial, S1M = households + NPISH), 5b net worth per person employed in
national hours / years of work / world hours, 5c US 1952-2026 from Fed Z.1 B.101, 5d PAYG (social-security) entitlements from
Eurostat Table 29, 5e synthesis (shares x section-4 claim hour returns), 6f implicit PAYG return = growth of total hours worked
(PWT 11) and UN WPP 20-64 population (history and projection).  Exploratory, not pre-registered.  Outputs to output/balance/.
No network: all inputs are cached files.  Conventions follow build_housing.py (log returns, x1000 = hours per 1,000 hours)."""
import os, json, hashlib, numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

from paths import B, JSTF, CN, GMPC, GMPR, DC, PWTX, SITE_CSS, cnd, label   # release: input locations (env-var overrides) and log labels, see paths.py
OUT = os.path.join(B, "output", "balance"); os.makedirs(OUT, exist_ok=True)
HOUS = os.path.join(B, "output", "housing")
F = {k: os.path.join(DC, v) for k, v in {"fin": "oecd_hh_financial_bs.csv", "nonfin": "oecd_hh_nonfinancial_bs.csv", "z1": "us_z1_b101_households.csv", "pens": "eurostat_pension_entitlements_F63.csv",
     "egdp": "eurostat_gdp_current_meur.csv", "pwt": "pwt110_hours.csv", "wb": "worldbank_gdp.csv", "wpp": "unwpp2024_population_workingage.csv"}.items()}
F.update({"claims_country": os.path.join(HOUS, "table_claims_by_country_national_hours.csv"), "claims": os.path.join(HOUS, "table_hour_return_by_claim.csv"),
          "housing_decades": os.path.join(HOUS, "table_decades_housing_vs_gmp.csv"), "wh": os.path.join(CN, "world_yardsticks_usd.csv"), "wh_lvl": os.path.join(CN, "world_q_gdp_per_hour_level_usd.csv"),
          "bis_fx": cnd("bis_xru.csv"), "us_gdp": cnd("GDP.csv"), "us_hours_bls": cnd("HOANBS.csv")})
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
LOG = {"inputs_sha256": {label(p): sha(p) for p in F.values()}}
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False})
PAL = ["#1f4e79", "#6b8e6b", "#c98a2b", "#7f9fbf", "#8c4a3c", "#3b3b8f"]
def save(df, name, **kw): df.to_csv(os.path.join(OUT, name), **kw)

# ------------------------------------------------------------------ 0. common inputs
pwt = pd.read_csv(F["pwt"]); PW = {v: pwt[pwt.variable == v].pivot(index="year", columns="iso3", values="value").sort_index() for v in ["emp", "avh", "hours_total_m"]}
EMP, AVH, HRS = PW["emp"], PW["avh"], PW["hours_total_m"]                                            # millions of persons, hours/yr, millions of hours
LOG["pwt_hours_identity_maxrel"] = float(((EMP * AVH - HRS) / HRS).abs().max().max())
wb = pd.read_csv(F["wb"]); NGDP = wb[wb.variable == "NY.GDP.MKTP.CN"].pivot(index="year", columns="iso3", values="value").sort_index()   # LCU, units
UGDP = wb[wb.variable == "NY.GDP.MKTP.CD"].pivot(index="year", columns="iso3", values="value").sort_index()                             # USD, units
wpp = pd.read_csv(F["wpp"]); P2064 = wpp[wpp.variable == "pop_20_64"].pivot(index="year", columns="iso3", values="value").sort_index()
# world hour (note 3 build_v2.py:112-119, as build_housing.py): USD of world GDP per hour worked
wh_idx = pd.read_csv(F["wh"], index_col=0, parse_dates=True)["gdph"]; lvl_q = pd.read_csv(F["wh_lvl"], index_col=0, parse_dates=True).iloc[:, 0]
H = wh_idx / float(wh_idx.loc["2014-01-31":"2014-03-31"].mean()) * float(lvl_q.loc["2014-03-31"])
H_DEC = H[H.index.month == 12]; H_DEC.index = H_DEC.index.year; H_LAST = (H.index[-1].strftime("%Y-%m"), float(H.iloc[-1]))
NEED_W = np.log(H_DEC).diff()
# exchange rates: BIS monthly average, December = year-end proxy (legacy euro-area rates are expressed in EUR by BIS)
I2 = {"AUS": "AU", "AUT": "AT", "BEL": "BE", "BGR": "BG", "BRA": "BR", "CAN": "CA", "CHE": "CH", "CHL": "CL", "COL": "CO", "CZE": "CZ", "DEU": "DE", "DNK": "DK", "ESP": "ES", "EST": "EE",
      "FIN": "FI", "FRA": "FR", "GBR": "GB", "GRC": "GR", "HRV": "HR", "HUN": "HU", "IND": "IN", "IRL": "IE", "ISL": "IS", "ISR": "IL", "ITA": "IT", "JPN": "JP", "KOR": "KR", "LTU": "LT",
      "LUX": "LU", "LVA": "LV", "MEX": "MX", "NLD": "NL", "NOR": "NO", "NZL": "NZ", "POL": "PL", "PRT": "PT", "ROU": "RO", "RUS": "RU", "SVK": "SK", "SVN": "SI", "SWE": "SE", "TUR": "TR", "USA": "US"}
bis = pd.read_csv(F["bis_fx"], usecols=["REF_AREA", "TIME_PERIOD", "OBS_VALUE"]); bis = bis[bis.TIME_PERIOD.str.endswith("-12")]
bis["year"] = bis.TIME_PERIOD.str[:4].astype(int); FXD = bis.pivot_table(index="year", columns="REF_AREA", values="OBS_VALUE", aggfunc="first")
FXD = pd.DataFrame({c3: FXD[c2] for c3, c2 in I2.items() if c2 in FXD.columns})                      # LCU per USD, December average
FXA = NGDP / UGDP                                                                                      # LCU per USD, annual average (World Bank)
_r = np.log(FXD / FXA.reindex(columns=FXD.columns)).loc[1995:2024]; LOG["fx_dec_vs_wb_annual_log_ratio"] = {"median_abs_1995_2024": round(float(_r.abs().stack().median()), 3), "max_abs_1995_2024": round(float(_r.abs().max().max()), 3),
    "max_abs_2015_2024": round(float(_r.loc[2015:].abs().max().max()), 3), "largest_1995_2024": {f"{c} {int(_r[c].abs().idxmax())}": round(float(_r[c].abs().max()), 3) for c in _r.abs().max().sort_values().index[-4:]}}

# ------------------------------------------------------------------ 5a. composition, OECD S1M
fin = pd.read_csv(F["fin"]); fin = fin[fin.maturity.isin(["_Z", "T"]) & (fin.currency_denom == "_T")]
assert not fin.duplicated(["iso3", "sector", "entry", "instrument", "year"]).any()
LOG["fin_rows_without_year_dropped"] = int(fin.year.isna().sum()); fin = fin[fin.year.notna()].copy(); fin["year"] = fin.year.astype(int)
nf = pd.read_csv(F["nonfin"]); LOG["nonfin_rows_without_year_dropped"] = int(nf.year.isna().sum()); nf = nf[nf.year.notna()].copy(); nf["year"] = nf.year.astype(int)
assert not nf.duplicated(["iso3", "sector", "instrument", "year"]).any()
SECT = "S1M"
FA = fin[(fin.sector == SECT) & (fin.entry == "A")].pivot_table(index=["iso3", "year"], columns="instrument", values="value", aggfunc="first")
FL = fin[(fin.sector == SECT) & (fin.entry == "L")].pivot_table(index=["iso3", "year"], columns="instrument", values="value", aggfunc="first")
FN = fin[(fin.sector == SECT) & (fin.entry == "N") & (fin.instrument == "BF90")].set_index(["iso3", "year"]).value
NF = nf[nf.sector == SECT].pivot_table(index=["iso3", "year"], columns="instrument", values="value", aggfunc="first")
idx = FA.index.intersection(NF.index[NF["N111N"].notna()]); idx = [i for i in idx if pd.notna(FA.loc[i, "F"])]
def g(df, col, i): return df[col].reindex(i) if col in df.columns else pd.Series(np.nan, index=i)
I = pd.MultiIndex.from_tuples(sorted(idx), names=["iso3", "year"])
C = pd.DataFrame(index=I)
C["dwellings"] = g(NF, "N111N", I); C["land"] = g(NF, "N211N", I); C["land_missing"] = C.land.isna(); C["land"] = C.land.fillna(0)
# produced: fixed assets + inventories + valuables (N1N is not used: for NLD it equals N1ON + land, i.e. it already contains land)
prod_tot = g(NF, "N11N", I) + g(NF, "N12N", I).fillna(0) + g(NF, "N13N", I).fillna(0); prod_other = prod_tot - C.dwellings
_n1 = (g(NF, "N1N", I) / prod_tot - 1).abs(); LOG["N1N_vs_N11N+N12N+N13N_relgap_over_1pct"] = {f"{a} {b}": round(float(v), 3) for (a, b), v in _n1[_n1 > 0.01].groupby(level=0).tail(1).items()}
np_other = (g(NF, "N2N", I) - C.land).where(g(NF, "N2N", I).notna() & ~C.land_missing, 0.0)
nn = g(NF, "NN", I); C["nonfin_other"] = (nn - C.dwellings - C.land).where(nn.notna(), prod_other.fillna(0) + np_other.fillna(0))
C["nonfin_other_source"] = np.where(nn.notna(), "NN", np.where(prod_tot.notna(), "N11N+N12N+N13N(+N2N)", "none"))
C["fin_total"] = g(FA, "F", I); C["F2"] = g(FA, "F2", I); C["F3"] = g(FA, "F3", I).fillna(0); C["F5"] = g(FA, "F5", I); C["F6"] = g(FA, "F6", I)
for k in ["F511", "F512", "F519", "F52"]: C[k] = g(FA, k, I)
C["fin_other"] = C.fin_total - C.F2 - C.F3 - C.F5 - C.F6
C["gross_assets"] = C.fin_total + C.dwellings + C.land + C.nonfin_other
C["liab_F4"] = g(FL, "F4", I); C["liab_total"] = g(FL, "F", I); C["net_worth"] = C.gross_assets - C.liab_total
C["net_fin_worth_BF90"] = FN.reindex(I)
LOG["check_BF90_eq_fin_assets_minus_liab_maxrel"] = float(((C.fin_total - C.liab_total - C.net_fin_worth_BF90) / C.fin_total).abs().max())
S = pd.DataFrame(index=I)
S["dwellings_land"] = (C.dwellings + C.land) / C.gross_assets * 100; S["other_nonfin"] = C.nonfin_other / C.gross_assets * 100
S["F6_pension_insurance"] = C.F6 / C.gross_assets * 100; S["F5_equity_funds"] = C.F5 / C.gross_assets * 100
for k, n in [("F511", "F5_listed"), ("F512", "F5_unlisted"), ("F519", "F5_other_equity"), ("F52", "F5_fund_shares")]: S[n] = C[k] / C.gross_assets * 100
S["F2F3_deposits_debt_sec"] = (C.F2 + C.F3) / C.gross_assets * 100; S["other_financial"] = C.fin_other / C.gross_assets * 100
S["other"] = S.other_nonfin + S.other_financial
S["sum_check"] = S[["dwellings_land", "F6_pension_insurance", "F5_equity_funds", "F2F3_deposits_debt_sec", "other"]].sum(axis=1)
S["liab_F4_pct_gross"] = C.liab_F4 / C.gross_assets * 100; S["liab_total_pct_gross"] = C.liab_total / C.gross_assets * 100
S["land_missing"] = C.land_missing; S["nonfin_other_source"] = C.nonfin_other_source
LOG["check_shares_sum_to_100_maxabs"] = float((S.sum_check - 100).abs().max())
# 5b. per worker
yr = I.get_level_values("year"); cc = I.get_level_values("iso3")
def look(df, i): return pd.Series([df.at[y, c] if (y in df.index and c in df.columns) else np.nan for c, y in i], index=i)
avh = look(AVH, I); emp = look(EMP, I); gdp = look(NGDP, I); fxd = look(FXD, I); hdec = pd.Series([H_DEC.get(y, np.nan) for y in yr], index=I)
avh_held = avh.copy(); emp_held = emp.copy()
for c in set(cc):                                                                                     # PWT ends 2023: hold avh and emp at 2023 for 2024-25 (flagged)
    m = (cc == c) & (yr > 2023)
    if m.any() and c in AVH.columns: avh_held[m] = AVH.at[2023, c]; emp_held[m] = EMP.at[2023, c]
S["pwt_held_at_2023"] = (yr > 2023)
nw = C.net_worth * 1e6
S["nw_to_gdp"] = nw / gdp                                                                              # = years of own average annual hours per person employed
S["nw_per_worker_national_hours"] = nw / (gdp / (emp_held * avh_held * 1e6)) / (emp_held * 1e6)       # = nw_to_gdp x avh
S["nw_per_worker_years_of_avh"] = S.nw_per_worker_national_hours / avh_held
S["nw_per_worker_world_hours"] = nw / fxd / hdec / (emp_held * 1e6)
S["nw_per_worker_world_hours_years_of_own_avh"] = S.nw_per_worker_world_hours / avh_held
LOG["check_years_of_avh_equals_nw_to_gdp_maxabs"] = float((S.nw_per_worker_years_of_avh - S.nw_to_gdp).abs().max())
COMP = pd.concat([C, S.drop(columns=["land_missing", "nonfin_other_source"])], axis=1).round(4); save(COMP, "balance_sheet_oecd_s1m_country_year.csv")
cnt = S.groupby(level="year").size(); LOG["oecd_countries_per_year"] = {int(k): int(v) for k, v in cnt.loc[2015:].items()}
# latest common year: the latest year with at least 90% of the maximum count of countries
LY = int(cnt[cnt >= 0.9 * cnt.max()].index.max()); LOG["latest_common_year"] = LY
cols = ["dwellings_land", "F6_pension_insurance", "F5_equity_funds", "F5_listed", "F5_unlisted", "F5_other_equity", "F5_fund_shares", "F2F3_deposits_debt_sec", "other", "sum_check",
        "liab_F4_pct_gross", "liab_total_pct_gross", "nw_to_gdp", "nw_per_worker_national_hours", "nw_per_worker_years_of_avh", "nw_per_worker_world_hours", "land_missing"]
LAT = S.xs(LY, level="year")[cols].sort_values("dwellings_land", ascending=False)
LAT["net_worth_bn_lcu"] = (C.xs(LY, level="year").net_worth / 1e3).reindex(LAT.index)
save(LAT.round(2), f"table_composition_latest_{LY}.csv")
# countries with financial accounts but no dwellings (excluded)
LOG["financial_but_no_dwellings"] = sorted(set(FA.index.get_level_values(0)) - set(I.get_level_values(0)))
LOG["dwellings_but_no_financial"] = sorted(set(NF.index[NF["N111N"].notna()].get_level_values(0)) - set(I.get_level_values(0)))
# GDP-weighted (USD) and median shares in LY
wl = look(UGDP, LAT.index.map(lambda c: (c, LY))).values; wl = wl / np.nansum(wl)
LOG["latest_shares_gdp_weighted"] = {k: round(float(np.nansum(LAT[k].values * wl)), 1) for k in cols[:12]}
LOG["latest_shares_median"] = LAT[cols[:16]].median().round(2).to_dict()
# time paths: GDP-weighted shares and nw/gdp for a balanced panel from 1995
pan = S.reset_index(); pan = pan[pan.year >= 1995]; bal = pan.groupby("iso3").year.agg(["min", "max", "count"]); bal_c = bal[(bal["min"] <= 1995) & (bal["max"] >= LY)].index.tolist()
P = pan[pan.iso3.isin(bal_c) & (pan.year <= LY)].copy(); P["w"] = [UGDP.at[y, c] if y in UGDP.index else np.nan for c, y in zip(P.iso3, P.year)]
TP = P.groupby("year").apply(lambda d: pd.Series({k: np.average(d[k], weights=d.w) for k in ["dwellings_land", "F6_pension_insurance", "F5_equity_funds", "F2F3_deposits_debt_sec", "other", "liab_total_pct_gross", "nw_to_gdp"]} | {"n": len(d)}))
TP["nw_to_gdp_median"] = P.groupby("year").nw_to_gdp.median(); save(TP.round(3), "timepath_balanced_panel_gdp_weighted.csv"); LOG["balanced_panel_countries"] = bal_c
save(S.reset_index().pivot(index="year", columns="iso3", values="nw_to_gdp").round(3), "timepath_nw_years_of_work_by_country.csv")
save(S.reset_index().pivot(index="year", columns="iso3", values="nw_per_worker_world_hours").round(0), "timepath_nw_world_hours_by_country.csv")

# ------------------------------------------------------------------ 5c. US, Fed Z.1 B.101, 1952-2026
z = pd.read_csv(F["z1"]); z = z[z.period.str.endswith("Q4") | (z.period == z.period.max())]
Z = z.pivot(index="year", columns="series_id", values="value").loc[1952:] / 1e6                     # trillions USD
LZ = z.period.max(); LOG["z1_last_period"] = LZ
s = lambda k: Z[k + ".Q"]
U = pd.DataFrame(index=Z.index)
U["real_estate"] = s("LM155035005"); U["pension_entitlements"] = s("FL153050005"); U["equities_mutual_funds"] = s("LM153064105") + s("LM153064205")
U["deposits_debt_securities"] = s("FL153020005") + s("FL153030005") + s("FL153034005") + s("LM154022005")       # MMF shares counted as deposits
U["private_business_IMA"] = s("LM153081115"); U["life_insurance"] = s("FL153040005"); U["durables"] = s("LM155111005")
U["total_assets"] = s("FL152000005")
U["other"] = U.total_assets - U[["real_estate", "pension_entitlements", "equities_mutual_funds", "deposits_debt_securities"]].sum(axis=1)
U["liabilities"] = s("FL154190005"); U["net_worth"] = s("FL152090005")
LOG["z1_check_nw_eq_assets_minus_liab_maxabs_bn"] = float((U.total_assets - U.liabilities - U.net_worth).abs().max() * 1e3)
LOG["z1_check_assets_eq_nonfin_plus_fin_maxabs_bn"] = float((s("LM152010005") + s("FL154090005") - U.total_assets).abs().max() * 1e3)
for k in ["real_estate", "pension_entitlements", "equities_mutual_funds", "deposits_debt_securities", "other", "private_business_IMA", "life_insurance", "durables", "liabilities"]: U[k + "_pct"] = U[k] / U.total_assets * 100
LOG["z1_check_shares_sum_maxabs"] = float((U[[k + "_pct" for k in ["real_estate", "pension_entitlements", "equities_mutual_funds", "deposits_debt_securities", "other"]]].sum(axis=1) - 100).abs().max())
gq = pd.read_csv(F["us_gdp"], parse_dates=["date"]); gq["year"] = gq.date.dt.year
gy = gq.groupby("year").v.mean() / 1e3                                                               # trillions, calendar-year GDP (mean of SAAR quarters; 2026 = H1 SAAR)
LOG["us_gdp_quarters_in_last_year"] = int((gq.year == gq.year.max()).sum())
LOG["us_gdp_fred_vs_wb_maxrel_1960_2025"] = float((gy.loc[1960:2025] * 1e12 / NGDP["USA"].loc[1960:2025] - 1).abs().max())
U["gdp_tn"] = gy.reindex(U.index); U["nw_years_of_us_work_per_worker"] = U.net_worth / U.gdp_tn
# hours: PWT to 2023; 2024-26 total hours extended with BLS nonfarm-business hours (HOANBS, on disk) and avh held at 2023 -> employment implied
hb = pd.read_csv(F["us_hours_bls"], parse_dates=["date"]); hb = hb.groupby(hb.date.dt.year).v.mean()
th = HRS["USA"].copy(); av = AVH["USA"].copy()
for y in range(2024, int(U.index.max()) + 1): th.loc[y] = th.loc[2023] * hb.loc[y] / hb.loc[2023]; av.loc[y] = av.loc[2023]
em = th / av; U["avh"] = av.reindex(U.index); U["emp_m"] = em.reindex(U.index); U["hours_extended_bls"] = U.index > 2023
U["nw_per_worker_us_hours"] = U.nw_years_of_us_work_per_worker * U.avh
U["H_world_usd"] = [H_DEC.get(y, H_LAST[1] if y == int(LZ[:4]) else np.nan) for y in U.index]
U["nw_per_worker_world_hours"] = U.net_worth * 1e12 / U.H_world_usd / (U.emp_m * 1e6)
save(U.round(4), "us_z1_balance_sheet_1952_2026.csv")
LOG["us_headline"] = {str(y): {"real_estate_pct": round(float(U.at[y, "real_estate_pct"]), 1), "pension_pct": round(float(U.at[y, "pension_entitlements_pct"]), 1), "equities_mf_pct": round(float(U.at[y, "equities_mutual_funds_pct"]), 1),
                      "deposits_debt_pct": round(float(U.at[y, "deposits_debt_securities_pct"]), 1), "other_pct": round(float(U.at[y, "other_pct"]), 1), "liab_pct": round(float(U.at[y, "liabilities_pct"]), 1),
                      "nw_years_of_work": round(float(U.at[y, "nw_years_of_us_work_per_worker"]), 2), "nw_per_worker_us_hours": round(float(U.at[y, "nw_per_worker_us_hours"]), 0),
                      "nw_per_worker_world_hours": None if pd.isna(U.at[y, "nw_per_worker_world_hours"]) else round(float(U.at[y, "nw_per_worker_world_hours"]), 0)} for y in [1952, 1970, 1990, 2000, 2007, 2019, 2023, int(U.index.max())]}
LOG["us_nw_years_growth_1952_last_pct_per_yr"] = round(float(np.log(U.nw_years_of_us_work_per_worker.iloc[-1] / U.nw_years_of_us_work_per_worker.loc[1952]) / (U.index[-1] - 1952 + 0.5) * 100), 2)
LOG["us_nw_hours_growth_1952_2023_pct_per_yr"] = round(float(np.log(U.nw_per_worker_us_hours.loc[2023] / U.nw_per_worker_us_hours.loc[1952]) / 71 * 100), 2)
# OECD USA (Table 9B + T720) vs Z.1 in the overlap
if ("USA", 2023) in C.index: LOG["oecd_vs_z1_usa_2023_nw_ratio"] = round(float(C.at[("USA", 2023), "net_worth"] / 1e6 / U.at[2023, "net_worth"]), 3)

# ------------------------------------------------------------------ 5d. PAYG entitlements (Eurostat Table 29)
pe = pd.read_csv(F["pens"]); pe = pe[(pe.variable == "F63_LE") & pe.value.notna()]
PN = pe[pe.unit == "MIO_NAC"].pivot_table(index=["iso3", "year"], columns="scheme", values="value", aggfunc="first")
PG = pe[pe.unit == "PC_GDP"].pivot_table(index=["iso3", "year"], columns="scheme", values="value", aggfunc="first")
D = pd.DataFrame(index=PN.index)
D["S13PS_bn_nac"] = PN["S13PS"] / 1e3; D["S1P_bn_nac"] = PN["S1P"] / 1e3
gd = look(NGDP, D.index)
# PAYG % of GDP on Eurostat's own GDP (nama_10_gdp, current MEUR) and Eurostat's MIO_EUR entitlements; World Bank LCU GDP only where Eurostat GDP is missing
PE_EUR = pe[pe.unit == "MIO_EUR"].pivot_table(index=["iso3", "year"], columns="scheme", values="value", aggfunc="first")
EG = pd.read_csv(F["egdp"]); EG = EG[EG.unit == "MIO_EUR"].set_index(["iso3", "year"])["value"]
D["S13PS_pct_gdp_wb"] = PN["S13PS"] * 1e6 / gd * 100
D["S13PS_pct_gdp"] = (PE_EUR["S13PS"].reindex(D.index) / EG.reindex(D.index) * 100).fillna(D["S13PS_pct_gdp_wb"])
LOG["payg_pct_gdp_basis"] = "Eurostat F63_LE (MIO_EUR) / Eurostat nama_10_gdp B1GQ (MIO_EUR); World Bank LCU GDP where Eurostat GDP is missing"
D["S1P_pct_gdp_eurostat"] = PG["S1P"].reindex(D.index); D["S1P_pct_gdp_calc"] = PN["S1P"] * 1e6 / gd * 100
D["S1PF_funded_pct_gdp"] = PG["S1PF"].reindex(D.index); D["S13PU_unfunded_pct_gdp"] = PG["S13PU"].reindex(D.index)
D["S13PS_share_of_S1P_pct"] = PN["S13PS"] / PN["S1P"] * 100
LOG["check_S1P_pct_gdp_calc_vs_eurostat_median_abs_pt"] = float((D.S1P_pct_gdp_calc - D.S1P_pct_gdp_eurostat).abs().median())
nwc = C.net_worth.reindex(D.index); D["household_nw_bn_nac"] = nwc / 1e3; D["oecd_F6_pct_gdp"] = (C.F6.reindex(D.index) * 1e6 / gd * 100)
D["oecd_F63_pension_pct_gdp"] = (g(FA, "F63", D.index) * 1e6 / gd * 100)
D["S13PS_pct_household_nw"] = PN["S13PS"] / nwc * 100; D["nw_incl_payg_over_nw"] = (nwc + PN["S13PS"]) / nwc
D["nw_to_gdp"] = nwc * 1e6 / gd; D["nw_incl_payg_to_gdp"] = (nwc + PN["S13PS"]) * 1e6 / gd
for c in ["CHE", "NOR"]:                                                                              # no dwellings in OECD: NW not available (financial only)
    pass
save(D.round(2), "table_payg_entitlements_all_years.csv")
RY = 2021; DR = D.xs(RY, level="year").dropna(subset=["S13PS_pct_gdp"]).sort_values("S13PS_pct_gdp", ascending=False); save(DR.round(1), f"table_payg_entitlements_{RY}.csv")
dd = DR.dropna(subset=["S13PS_pct_household_nw"])
LOG["payg_2021"] = {"countries_with_pct_gdp": len(DR), "countries_with_pct_nw": len(dd), "S13PS_pct_gdp_median": round(float(DR.S13PS_pct_gdp.median()), 0), "S13PS_pct_gdp_range": [round(float(DR.S13PS_pct_gdp.min()), 0), round(float(DR.S13PS_pct_gdp.max()), 0)],
                    "S13PS_pct_nw_median": round(float(dd.S13PS_pct_household_nw.median()), 0), "S13PS_pct_nw_range": [round(float(dd.S13PS_pct_household_nw.min()), 0), round(float(dd.S13PS_pct_household_nw.max()), 0)],
                    "funded_S1PF_pct_gdp_median": round(float(DR.S1PF_funded_pct_gdp.median()), 0), "nw_to_gdp_median": round(float(dd.nw_to_gdp.median()), 2), "nw_incl_payg_to_gdp_median": round(float(dd.nw_incl_payg_to_gdp.median()), 2),
                    "missing_nw": sorted(set(DR.index) - set(dd.index))}

# ------------------------------------------------------------------ 6f. implicit PAYG return = growth of total hours worked (PWT 11)
dH = np.log(HRS).diff(); dE = np.log(EMP).diff(); dA = np.log(AVH).diff(); dP = np.log(P2064).diff()
W = UGDP.shift(1).reindex(index=dH.index)                                                              # start-of-year USD GDP weights
for y in range(1951, 1961): W.loc[y] = UGDP.loc[1960]                                                  # before 1961: 1960 weights (World Bank starts 1960)
def wavg(x, sample=None, years=range(1951, 2024)):
    o = {}
    for y in years:
        v = x.loc[y] if y in x.index else pd.Series(dtype=float)
        if sample is not None: v = v.reindex(sample)
        w = W.loc[y].reindex(v.index) if y in W.index else pd.Series(np.nan, index=v.index); m = v.notna() & w.notna()
        o[y] = np.average(v[m], weights=w[m]) if m.sum() else np.nan
    return pd.Series(o)
cov = lambda x: pd.Series({y: int((x.loc[y].notna() & W.loc[y].reindex(x.columns).notna()).sum()) for y in range(1951, 2024)})
S50 = [c for c in HRS.columns if HRS[c].loc[1950:2023].notna().all()]
JST16 = ["AUS", "BEL", "CHE", "DEU", "DNK", "ESP", "FIN", "FRA", "GBR", "ITA", "JPN", "NLD", "NOR", "PRT", "SWE", "USA"]
WG = pd.DataFrame({"hours_all": wavg(dH), "emp_all": wavg(dE), "avh_all": wavg(dA), "n_all": cov(dH),
                   "hours_1950_sample": wavg(dH, S50), "emp_1950_sample": wavg(dE, S50), "hours_jst16": wavg(dH, JST16), "emp_jst16": wavg(dE, JST16),
                   "pop2064_same_countries": wavg(dP.where(dH.reindex(columns=dP.columns).notna())), "pop2064_world_headcount": np.log(P2064.sum(axis=1)).diff().reindex(range(1951, 2024))})
save((WG * 1000).round(2).assign(n_all=WG.n_all), "payg_world_annual_per_1000h.csv"); LOG["sample_1950_countries"] = S50
DECS = [(1951, 1960), (1961, 1970), (1971, 1980), (1981, 1990), (1991, 2000), (2001, 2010), (2011, 2020), (2021, 2023), (2011, 2023), (1951, 2023), (1976, 2020), (1951, 2020), (1976, 2023)]
DT = pd.DataFrame({f"{a}-{b}": (WG.drop(columns="n_all").loc[a:b].mean() * 1000) for a, b in DECS}).T.round(1); DT["n_countries_mean"] = [round(WG.n_all.loc[a:b].mean(), 0) for a, b in DECS]
DT["avh_drag"] = (DT.hours_all - DT.emp_all).round(1); save(DT, "table_payg_return_by_decade_world.csv")
# per country
PCN = pd.DataFrame({"hours_1951_2023": dH.loc[1951:2023].mean() * 1000, "emp_1951_2023": dE.loc[1951:2023].mean() * 1000, "hours_1976_2020": dH.loc[1976:2020].mean() * 1000,
                    "emp_1976_2020": dE.loc[1976:2020].mean() * 1000, "hours_2001_2023": dH.loc[2001:2023].mean() * 1000, "pop2064_1976_2020": dP.loc[1976:2020].mean() * 1000,
                    "pop2064_proj_2024_2060": dP.loc[2024:2060].mean() * 1000, "first_year": HRS.apply(lambda s_: s_.first_valid_index())})
PCN = PCN[PCN.hours_2001_2023.notna()]; PCN["avh_drag_1976_2020"] = PCN.hours_1976_2020 - PCN.emp_1976_2020
save(PCN.round(1), "table_payg_return_by_country.csv")
PCD = pd.DataFrame({f"{a}-{b}": dH.loc[a:b].mean() * 1000 for a, b in DECS[:8]}).where(lambda d_: d_.notna()); PCD = PCD[PCD.notna().any(axis=1)]
PCD["years_1951_2023"] = dH.loc[1951:2023].notna().sum(); save(PCD.round(1), "table_payg_return_by_country_decade.csv")
# 20-64 population projection, GDP weights frozen at 2023 USD GDP, same countries; and world headcount
wf = UGDP.loc[2023]; PR = {}
for a, b in [(2024, 2030), (2031, 2040), (2041, 2050), (2051, 2060), (2024, 2060)]:
    v = dP.loc[a:b].mean(); m = v.notna() & wf.reindex(v.index).notna() & v.index.isin(PCN.index)
    PR[f"{a}-{b} (projection)"] = {"pop2064_gdp_weighted_2023w": np.average(v[m], weights=wf.reindex(v.index)[m]) * 1000, "pop2064_world_headcount": np.log(P2064.sum(axis=1)).diff().loc[a:b].mean() * 1000,
                                   "pop2064_jst16_gdpw": np.average(v.reindex(JST16), weights=wf.reindex(JST16)) * 1000}
for a, b in [(1951, 2023), (1976, 2020), (2001, 2023)]:
    v = dP.loc[a:b].mean(); m = v.notna() & wf.reindex(v.index).notna() & v.index.isin(PCN.index)
    PR[f"{a}-{b} (history, 2023 weights)"] = {"pop2064_gdp_weighted_2023w": np.average(v[m], weights=wf.reindex(v.index)[m]) * 1000, "pop2064_world_headcount": np.log(P2064.sum(axis=1)).diff().loc[a:b].mean() * 1000,
                                             "pop2064_jst16_gdpw": np.average(v.reindex(JST16), weights=wf.reindex(JST16)) * 1000}
TPR = pd.DataFrame(PR).T.round(1); save(TPR, "table_pop2064_projection.csv")
# comparison with section 4 claim returns
CLM = pd.read_csv(F["claims"], index_col=0)
CMPT = pd.DataFrame({
    "PAYG (growth of total hours), all PWT countries with hours": {"world_1976_2020": DT.loc["1976-2020", "hours_all"], "national_gdpw_1951_2020": DT.loc["1951-2020", "hours_all"]},
    "PAYG (growth of total hours), same 16 JST countries": {"national_gdpw_jst16_1976_2020": DT.loc["1976-2020", "hours_jst16"], "national_gdpw_1951_2020": DT.loc["1951-2020", "hours_jst16"], "national_median_jst16_1951_2020": dH[JST16].loc[1951:2020].mean().median() * 1000},
    "Home (JST housing)": {"world_1976_2020": CLM.at["world_net_1976-2020", "housing"], "national_gdpw_jst16_1976_2020": CLM.at["national_net_gdpw_1976-2020", "housing"], "national_gdpw_1951_2020": CLM.at["national_net_gdpw_1951-2020", "housing"], "national_median_jst16_1951_2020": CLM.at["national_net_median_1951-2020", "housing"]},
    "GMP (note 3)": {"world_1976_2020": CLM.at["world_net_1976-2020", "gmp"]},
    "Government bonds": {"world_1976_2020": CLM.at["world_net_1976-2020", "gov_bonds"], "national_gdpw_jst16_1976_2020": CLM.at["national_net_gdpw_1976-2020", "gov_bonds"], "national_gdpw_1951_2020": CLM.at["national_net_gdpw_1951-2020", "gov_bonds"], "national_median_jst16_1951_2020": CLM.at["national_net_median_1951-2020", "gov_bonds"]},
    "Deposits / bills": {"world_1976_2020": CLM.at["world_net_1976-2020", "deposits_bills"], "national_gdpw_jst16_1976_2020": CLM.at["national_net_gdpw_1976-2020", "deposits_bills"], "national_gdpw_1951_2020": CLM.at["national_net_gdpw_1951-2020", "deposits_bills"], "national_median_jst16_1951_2020": CLM.at["national_net_median_1951-2020", "deposits_bills"]},
    "Equities": {"world_1976_2020": CLM.at["world_net_1976-2020", "equities"], "national_gdpw_jst16_1976_2020": CLM.at["national_net_gdpw_1976-2020", "equities"], "national_gdpw_1951_2020": CLM.at["national_net_gdpw_1951-2020", "equities"], "national_median_jst16_1951_2020": CLM.at["national_net_median_1951-2020", "equities"]}}).T.round(1)
save(CMPT, "table_claims_hour_return_with_payg.csv")
LOG["payg_note"] = "PAYG world_1976_2020 is the GDP-weighted average of national total-hours growth (all PWT countries with hours), i.e. the PAYG return in national hours of a GDP-weighted set of countries; it equals a world-hour return only if wage shares and the mix of national hours are stable."

# ------------------------------------------------------------------ 5e. synthesis: hour return of the balance sheet (national hours, 1976-2020)
cr = pd.read_csv(F["claims_country"], header=[0, 1], index_col=0); cr = cr.xs("1976-2020", axis=1, level=1)
cr.index.name = "iso3"; cr = cr.loc[[i for i in cr.index if isinstance(i, str) and len(i) == 3]].astype(float)
R = pd.DataFrame(index=cr.index)
R["r_home"] = cr.housing; R["r_equity_F5"] = cr.equities; R["r_bills_F2"] = cr.deposits_bills; R["r_bonds_F3"] = cr.gov_bonds
R["r_pension_F6"] = 0.6 * cr.equities + 0.4 * cr.gov_bonds; R["r_other"] = cr.deposits_bills; R["r_liab"] = cr.deposits_bills + 10.0
R["r_payg"] = PCN.hours_1976_2020.reindex(R.index)
SY = []
for c in R.index:
    if (c, LY) not in C.index: continue
    x = C.loc[(c, LY)]; ga = x.gross_assets; r = R.loc[c]
    sh = {"home": (x.dwellings + x.land) / ga, "F5": x.F5 / ga, "F2": x.F2 / ga, "F3": x.F3 / ga, "F6": x.F6 / ga, "other": (x.nonfin_other + x.fin_other) / ga}; l = x.liab_total / ga
    ra = sh["home"] * r.r_home + sh["F5"] * r.r_equity_F5 + sh["F2"] * r.r_bills_F2 + sh["F3"] * r.r_bonds_F3 + sh["F6"] * r.r_pension_F6 + sh["other"] * r.r_other
    rnw = (ra - l * r.r_liab) / (1 - l)
    o = {"iso3": c, "year_shares": LY, "share_home": sh["home"] * 100, "share_F5": sh["F5"] * 100, "share_F2F3": (sh["F2"] + sh["F3"]) * 100, "share_F6": sh["F6"] * 100, "share_other": sh["other"] * 100,
         "liab_pct_gross": l * 100, "return_gross_assets": ra, "return_net_worth": rnw, "home_alone": r.r_home, "payg_hours_growth": r.r_payg, "land_missing": bool(x.land_missing)}
    # with PAYG (S13PS 2021, scaled to the household net worth of 2021) added as an asset earning hours growth
    if (c, RY) in D.index and pd.notna(D.at[(c, RY), "S13PS_pct_household_nw"]):
        p = D.at[(c, RY), "S13PS_pct_household_nw"] / 100; o["payg_pct_nw_2021"] = p * 100
        o["return_net_worth_incl_payg"] = (rnw + p * r.r_payg) / (1 + p)
    SY.append(o)
SYN = pd.DataFrame(SY).set_index("iso3")
# robustness: shares averaged over all available years for the country; other assets at zero hour return
for c in SYN.index:
    xs = C.loc[c]; ga = xs.gross_assets; r = R.loc[c]; l = (xs.liab_total / ga).mean()
    shm = {"home": ((xs.dwellings + xs.land) / ga).mean(), "F5": (xs.F5 / ga).mean(), "F2": (xs.F2 / ga).mean(), "F3": (xs.F3 / ga).mean(), "F6": (xs.F6 / ga).mean(), "other": ((xs.nonfin_other + xs.fin_other) / ga).mean()}
    ra = shm["home"] * r.r_home + shm["F5"] * r.r_equity_F5 + shm["F2"] * r.r_bills_F2 + shm["F3"] * r.r_bonds_F3 + shm["F6"] * r.r_pension_F6 + shm["other"] * r.r_other
    SYN.at[c, "return_net_worth_avg_shares"] = (ra - l * r.r_liab) / (1 - l); SYN.at[c, "years_avg_shares"] = f"{int(xs.index.min())}-{int(xs.index.max())}"
    x = C.loc[(c, LY)]; sh_o = (x.nonfin_other + x.fin_other) / x.gross_assets; l0 = x.liab_total / x.gross_assets
    SYN.at[c, "return_net_worth_other_at_zero"] = SYN.at[c, "return_net_worth"] - sh_o * r.r_other / (1 - l0)
    SYN.at[c, "return_net_worth_liab_at_bills"] = SYN.at[c, "return_net_worth"] + l0 * 10 / (1 - l0)
save(SYN.round(1), "table_balance_sheet_hour_return_by_country.csv")
wsy = np.array([UGDP.at[LY, c] for c in SYN.index]); wsy = wsy / wsy.sum()
LOG["synthesis"] = {"countries": SYN.index.tolist(), "year_shares": LY, "return_nw_gdpw": round(float((SYN.return_net_worth * wsy).sum()), 1), "return_nw_median": round(float(SYN.return_net_worth.median()), 1),
                    "return_nw_range": [round(float(SYN.return_net_worth.min()), 1), round(float(SYN.return_net_worth.max()), 1)], "return_gross_median": round(float(SYN.return_gross_assets.median()), 1),
                    "home_alone_median": round(float(SYN.home_alone.median()), 1), "home_alone_gdpw": round(float((SYN.home_alone * wsy).sum()), 1),
                    "payg_median": round(float(SYN.payg_hours_growth.median()), 1), "return_nw_avg_shares_median": round(float(SYN.return_net_worth_avg_shares.median()), 1),
                    "return_nw_other_zero_median": round(float(SYN.return_net_worth_other_at_zero.median()), 1), "return_nw_liab_at_bills_median": round(float(SYN.return_net_worth_liab_at_bills.median()), 1),
                    "incl_payg": SYN.dropna(subset=["return_net_worth_incl_payg"])[["return_net_worth", "payg_pct_nw_2021", "return_net_worth_incl_payg"]].round(1).to_dict("index"),
                    "gmp_world_hours_sec4_1976_2020": float(CLM.at["world_net_1976-2020", "gmp"]),
                    "mapping": "dwellings+land -> JST housing; F5 -> JST equities; F2 deposits -> JST bills; F3 debt securities -> JST long gov bonds; F6 -> 0.6 equities + 0.4 gov bonds; other assets -> bills; liabilities -> bills + 10 per 1,000 h; PAYG (S13PS) -> growth of total hours (PWT 11); all per-country national-hour means 1976-2020 (section 4)"}

# ------------------------------------------------------------------ figures
# (1) composition, latest common year
fig, ax = plt.subplots(figsize=(8.4, 4.2)); L = LAT.sort_values("dwellings_land", ascending=False); x = np.arange(len(L)); bot = np.zeros(len(L))
for k, lb, col in [("dwellings_land", "Dwellings + land", PAL[2]), ("F6_pension_insurance", "Pension & insurance (F6)", PAL[1]), ("F5_equity_funds", "Equity & fund shares (F5)", PAL[0]),
                   ("F2F3_deposits_debt_sec", "Deposits & debt securities (F2+F3)", PAL[3]), ("other", "Other", "#bbbbbb")]:
    ax.bar(x, L[k].values, 0.75, bottom=bot, color=col, label=lb); bot += L[k].values
ax.plot(x, L.liab_total_pct_gross.values, "_", color=PAL[4], ms=9, mew=2, label="Liabilities, % of gross assets")
ax.set_xticks(x); ax.set_xticklabels([c + ("*" if L.at[c, "land_missing"] else "") for c in L.index], fontsize=6.5, rotation=90); ax.set_ylim(0, 100); ax.set_ylabel("% of gross assets")
ax.set_title(f"Household balance sheets (households + non-profit institutions serving households), {LY}: share of gross assets", loc="left", fontsize=9.5)
ax.text(1.0, 1.01, "* land not reported", transform=ax.transAxes, ha="right", fontsize=7, color="#555555")
ax.legend(fontsize=7.5, frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.17)); fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig1_composition_latest.png"), dpi=160); plt.close(fig)
# (2) US composition and net worth in years of work
fig, ax = plt.subplots(figsize=(8.4, 4.2)); ks = [("real_estate_pct", "Real estate", PAL[2]), ("pension_entitlements_pct", "Pension entitlements", PAL[1]), ("equities_mutual_funds_pct", "Corporate equities + mutual funds", PAL[0]),
                                                  ("deposits_debt_securities_pct", "Deposits + MMF + debt securities", PAL[3]), ("other_pct", "Other (private business, durables, life ins., misc.)", "#bbbbbb")]
ax.stackplot(U.index, *[U[k].values for k, _, _ in ks], labels=[l_ for _, l_, _ in ks], colors=[c_ for _, _, c_ in ks], alpha=0.9)
ax.plot(U.index, U.liabilities_pct, color=PAL[4], lw=1.4, label="Liabilities, % of assets"); ax.set_ylim(0, 100); ax.set_xlim(1952, U.index.max()); ax.set_ylabel("% of total assets")
a2 = ax.twinx(); a2.plot(U.index, U.nw_years_of_us_work_per_worker, color="k", lw=1.8, label="Net worth per worker, years of US work (right)"); a2.set_ylabel("years of work"); a2.spines["top"].set_visible(False); a2.set_ylim(0, None)
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = a2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, fontsize=7, frameon=False, ncol=2, loc="upper center", bbox_to_anchor=(0.5, -0.1))
ax.set_title(f"US households and non-profits (Fed Z.1 B.101), 1952\u2013{LZ.replace(':', ' ')}", loc="left", fontsize=9.5); fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig2_us_composition_years.png"), dpi=160); plt.close(fig)
# (3) four claims side by side + decade bars for PAYG
fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.4, 4.2), gridspec_kw={"width_ratios": [1, 1.6]})
four = [("PAYG\n(hours growth)", DT.loc["1976-2020", "hours_all"], PAL[5]), ("Home", CLM.at["world_net_1976-2020", "housing"], PAL[2]), ("GMP", CLM.at["world_net_1976-2020", "gmp"], PAL[0]), ("Deposits\n(bills)", CLM.at["world_net_1976-2020", "deposits_bills"], PAL[3])]
a1.bar(range(4), [v for _, v, _ in four], color=[c_ for _, _, c_ in four], width=0.65)
for i, (_, v, _) in enumerate(four): a1.text(i, v + (0.8 if v >= 0 else -0.8), f"{v:.1f}", ha="center", va="bottom" if v >= 0 else "top", fontsize=7.5)
a1.set_ylim(-7, None); a1.text(0, -6.8, "PAYG: GDP-weighted national hours growth;\nothers: world hours (section 4)", fontsize=6.5, color="#555555")
a1.axhline(0, color="k", lw=0.6); a1.set_xticks(range(4)); a1.set_xticklabels([n for n, _, _ in four], fontsize=7.5); a1.set_ylabel("hours a year per 1,000 hours")
a1.set_title("Hour return of four claims, 1976-2020", loc="left", fontsize=9.5)
dec = [r for r in DT.index if r in ["1951-1960", "1961-1970", "1971-1980", "1981-1990", "1991-2000", "2001-2010", "2011-2023"]]   # 2011-2023 as one bar: 2020 COVID fall and 2021-23 rebound offset
xx = np.arange(len(dec)); a2.bar(xx - 0.2, DT.loc[dec, "hours_all"], 0.4, color=PAL[5], label="Total hours (PAYG return)"); a2.bar(xx + 0.2, DT.loc[dec, "emp_all"], 0.4, color=PAL[3], label="Employment")
pj = [r for r in TPR.index if "projection" in r and not r.startswith("2024-2060")]; xp = np.arange(len(dec), len(dec) + len(pj))
a2.bar(xp, TPR.loc[pj, "pop2064_gdp_weighted_2023w"], 0.4, color="white", edgecolor=PAL[5], hatch="///", label="Population 20-64, projection (UN WPP)")
a2.axhline(0, color="k", lw=0.6); a2.set_xticks(list(xx) + list(xp)); a2.set_xticklabels([d_.replace("-", "-\n") for d_ in dec] + [p_.split(" ")[0].replace("-", "-\n") for p_ in pj], fontsize=6.5)
a2.set_title("PAYG return by decade, GDP-weighted (hours per 1,000)", loc="left", fontsize=9.5); a2.legend(fontsize=7, frameon=False)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig3_four_claims_payg_decades.png"), dpi=160); plt.close(fig)

# ------------------------------------------------------------------ log
LOG["payg_decades_world"] = DT.to_dict("index"); LOG["pop2064_projection"] = TPR.to_dict("index"); LOG["claims_with_payg"] = CMPT.to_dict("index")
LOG["latest_cross_section"] = LAT[["dwellings_land", "F6_pension_insurance", "F5_equity_funds", "F2F3_deposits_debt_sec", "other", "liab_total_pct_gross", "nw_to_gdp", "nw_per_worker_national_hours", "nw_per_worker_world_hours"]].round(1).to_dict("index")
LOG["world_hour_last_month"] = H_LAST
json.dump(LOG, open(os.path.join(OUT, "build_log.json"), "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
print(LAT.round(1).to_string()); print(TP.round(2).to_string()); print(DR.round(0).to_string()); print(DT.to_string()); print(PCN.round(1).to_string()); print(TPR.to_string()); print(CMPT.to_string()); print(SYN.round(1).to_string())
print(json.dumps({k: v for k, v in LOG.items() if k not in ["inputs_sha256", "latest_cross_section", "payg_decades_world", "claims_with_payg", "pop2064_projection"]}, indent=0, default=str))
