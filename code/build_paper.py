# -*- coding: utf-8 -*-
"""Note 4: fill paper_template.html from output/housing, output/balance, output/life (tables and every number quoted
in the text) and write output/paper/household.html (+ img/, style.css) and output/paper/numbers_in_text.json.
Re-run after any builder (build_housing*.py, build_balance.py, build_life.py) is re-run: every number re-fills.
Every number comes from output/ (including output/housing/extras.json from build_extras.py). Nothing here writes to the
site or to any repository."""
import os, re, json, shutil, numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

from paths import B, JSTF, CN, GMPC, GMPR, DC, PWTX, SITE_CSS, cnd, label   # release: input locations (env-var overrides) and log labels, see paths.py
O = os.path.join(B, "output"); P = os.path.join(O, "paper")
os.makedirs(os.path.join(P, "img"), exist_ok=True)
LH = json.load(open(os.path.join(O, "housing", "build_log.json"))); LB = json.load(open(os.path.join(O, "balance", "build_log.json")))
LL = json.load(open(os.path.join(O, "life", "build_log.json"))); EXT = LH["extension_2021_2025"]
def rd(sub, f, **k): return pd.read_csv(os.path.join(O, sub, f), **k)

def table(caption, head, rows, numcols=None, bold=(), small=False):
    numcols = set(range(1, len(head))) if numcols is None else numcols
    cls = ' class="small"' if small else ""
    h = [f"<div class=\"scroll\"><table{cls}>", f"<caption style=\"text-align:left;caption-side:top;font-size:.93rem;color:var(--muted);padding:.3rem 0\">{caption}</caption>",
         "<thead><tr>" + "".join(f"<th{' style=\"text-align:right\"' if i in numcols else ''}>{c}</th>" for i, c in enumerate(head)) + "</tr></thead><tbody>"]
    for j, r in enumerate(rows):
        h.append(f"<tr{' class=\"bold\"' if j in bold else ''}>" + "".join(f"<td class=\"num\">{c}</td>" if i in numcols else f"<td>{c}</td>" for i, c in enumerate(r)) + "</tr>")
    h.append("</tbody></table></div>"); return "\n".join(h)

def fmt(d):
    def f(x):
        if x is None or (isinstance(x, float) and np.isnan(x)): return "&ndash;"
        s = f"{x:,.{d}f}"
        if s.startswith("-") and float(s.replace(",", "")) == 0: s = s[1:]
        if s.startswith("-"): s = "&minus;" + s[1:]
        return s
    return f
f0, f1, f2 = fmt(0), fmt(1), fmt(2)
def pct(x, d=0): return fmt(d)(x * 100)
def sg1(x): return ("+" if x >= 0 else "") + f1(x)
N = {}; T = {}

# =========================================================== Section 4: housing
HG = rd("housing", "table_housing_vs_gmp_world_hours_to2025.csv", header=[0, 1], index_col=0)
def hv(asset, per, item): return float(HG[(asset, per)].loc[item])
for a, k in [("housing", "h"), ("gmp", "g")]:
    for per, pk in [("1976-1981", "7681"), ("1982-2000", "8200"), ("2001-2020", "0120"), ("2021-2025", "2125"), ("1976-2020", "7620"), ("1976-2025", "7625")]:
        for item, ik in [("total", "tot"), ("cash", "cash"), ("price", "price"), ("valuation", "val"), ("price_ex_valuation", "pxv"), ("needed", "need"), ("net", "net"), ("net_ex_valuation", "netex")]:
            v = hv(a, per, item); N[f"{k}_{ik}_{pk}"] = f1(v); N[f"{k}_{ik}_{pk}_r"] = f0(v)
N["h_net_7625_pct"] = f1(hv("housing", "1976-2025", "net") / 10); N["g_net_7625_pct"] = f1(hv("gmp", "1976-2025", "net") / 10)
N["h_val_share_2125"] = pct(hv("housing", "2021-2025", "valuation") / hv("housing", "2021-2025", "net"))
N["h_sd"] = f1(LH["vol_annual_net_pct"]["housing"]); N["g_sd"] = f1(LH["vol_annual_net_pct"]["gmp"]); N["hg_corr"] = f2(LH["corr_annual_net_housing_gmp_1976_2020"])
N["h_usa_w"] = pct(LH["housing_usa_weight_1976_2020_mean"])
nat = LH["national_1976_2020"]; nat50 = LH["national_1951_2020"]
N.update(nat_net=f1(nat["net"]), nat_netex=f1(nat["net_ex_valuation"]), nat_pxv=f1(nat["price_ex_valuation"]), nat_need=f1(nat["needed"]), nat_med=f1(nat["net_country_median"]),
         nat_min=f1(nat["net_country_min"]), nat_max=f1(nat["net_country_max"]), nat50_net=f1(nat50["net"]), nat50_med=f1(nat50["net_country_median"]))
NX = EXT["national_per_1000h"]["1976-2025"]; N.update(nat25_net=f1(NX["net"]), nat25_med=f1(NX["net_country_median"]))
HC = rd("housing", "table_housing_by_country_national_hours.csv", header=[0, 1], index_col=0); H25 = rd("housing", "table_housing_by_country_national_hours_2021_2025.csv", index_col=0)
netc = HC[("1976-2020", "net")]; N["nat_min_c"] = {"JPN": "Japan", "NOR": "Norway"}.get(netc.idxmin(), netc.idxmin()); N["nat_max_c"] = {"JPN": "Japan", "NOR": "Norway"}.get(netc.idxmax(), netc.idxmax())
N["nat_all_pos"] = "Every country is positive" if (netc > 0).all() else "Not every country is positive"
N["h25_neg_n"] = f0((H25["net"] < 10).sum())
rh = LH["rent_yield"]; gc = LH["gmp_cash_yield"]
N.update(rent_1950=f2(rh["1950"]), rent_1976=f2(rh["1976"]), rent_2000=f2(rh["2000"]), rent_2020=f2(rh["2020"]), gcash_1976=f2(gc["1976"]), gcash_2000=f2(gc["2000"]), gcash_2020=f2(gc["2020"]),
         rent_2025=f2(EXT["rent_yield_2025_gdpw_pct"]), gcash_2025=f2(EXT["gmp_cash_yield_2025_pct"]))
old = LH["note3_rent_weight_bug"]; N.update(old_1976=f2(old["rent_yield_unscaled_pct"]["1976"]), old_2000=f2(old["rent_yield_unscaled_pct"]["2000"]), old_2020=f2(old["rent_yield_unscaled_pct"]["2020"]))
uw = old["unscaled_weights_mean_1976_2020"]; N["old_w_esp"] = pct(uw["ESP"]); N["old_w_big6"] = pct(sum(uw[c] for c in ["JPN", "USA", "DEU", "FRA", "GBR", "ITA"]), 1)
N["unit_resid"] = f2(LH["jst_gdp_unit_residual_sd_log10_max"])
RY = rd("housing", "rent_vs_gmp_cash_yield.csv", index_col=0); x = RY.loc[2010:2020]
N.update(rent_1020_lo=f1(x.rent_yield_pct_same_year_w.min()), rent_1020_hi=f1(x.rent_yield_pct_same_year_w.max()), gc_1020_lo=f1(x.gmp_cash_yield_pct.min()), gc_1020_hi=f1(x.gmp_cash_yield_pct.max()))
N["gc_above_rent_7699"] = pct((RY.loc[1976:1999].gmp_cash_yield_pct > RY.loc[1976:1999].rent_yield_pct_same_year_w).mean())
RB = rd("housing", "table_housing_robustness.csv", index_col=0)["net_per_1000h"]; RBX = rd("housing", "table_housing_robustness.csv", index_col=0)["net_ex_valuation_per_1000h"]
RE = rd("housing", "table_housing_robustness_ext.csv", index_col=0)
N.update(rb_tax=f1(RB["Property tax 1 pt a year"]), rb_tax_x=f1(RBX["Property tax 1 pt a year"]), rb_taxcost=f1(RB["Property tax 1 pt + costs over 10 years"]), rb_taxcost_x=f1(RBX["Property tax 1 pt + costs over 10 years"]),
         rb_eq=f1(RB["Equal weights"]), rb_exus=f1(RB["Ex-USA (GDP weights)"]), rb_avg=f1(RB["World hour on annual-average timing"]), rb_percap=f1(RB["National hours from GDP per head (JST), median"]),
         rb_taxcost25=f1(RE.loc["Property tax 1 pt + 7.7% costs over 10 years, 1976-2025", "net_per_1000h"]), rb_oecd=f1(RE.loc["OECD rent growth for JST implied rent growth, world, 1976-2020", "net_per_1000h"]),
         rb_oecd_x=f1(RE.loc["OECD rent growth for JST implied rent growth, world, 1976-2020", "net_ex_valuation_per_1000h"]), rb_oecd_med=f1(RE.loc["OECD rent growth, national-hour country median, 1976-2020", "net_per_1000h"]))
tc = LH["transaction_cost_hours_per_year"]; N.update(tc10=f1(tc["10y"]), tc20=f1(tc["20y"]))
R20 = rd("housing", "table_rolling20_housing_vs_gmp.csv"); N.update(r20_n=f0(len(R20)), r20_win=f0((R20.housing_minus_gmp > 0).sum()), r20_h_lo=f0(R20.housing_net.min()), r20_h_hi=f0(R20.housing_net.max()),
                                                                   r20_g_lo=f0(R20.gmp_net.min()), r20_g_hi=f0(R20.gmp_net.max()))
CR = LH["extension_2021_2025"]["crosscheck_median"]; N.update(cc_p=f2(CR["price_corr"]), cc_pg=f"{CR['price_gap_jst_minus_oecd_pt']:+.2f}",
                                                               cc_pr=f2(CR["price_rent_corr"]), cc_r=f2(CR["rent_corr"]), cc_n=f0(EXT["oecd_rent_country_years_used_1976_2020"]))
idc = LH["identity_components"]; N.update(pxv_gap_mean=f2(abs(idc["pxv_minus_dlog_rent_mean_pct_1976_2020"])), pxv_gap_max=f1(idc["pxv_minus_dlog_rent_maxabs_pct_1976_2020"]))
xr = LH["xrusd_timing"]; N.update(jpy85=f1(xr["JPN_1985"]), jpy86=f1(xr["JPN_1986"]))
gp = LH["gdph_vs_proxies"]["WB_PWT_vs_JST_per_capita_1961_2020"]; N.update(gdph_corr=f2(gp["corr"]), gdph_diff=f2(gp["mean_diff_pct"]))
N["fx_ext_gap"] = f1(EXT["fx_check_2020_JST_vs_BIS_dec_logdiff_maxabs"] * 100)
CL = rd("housing", "table_hour_return_by_claim.csv", index_col=0)
for c, k in [("deposits_bills", "bills"), ("gov_bonds", "bonds"), ("equities", "eq"), ("housing", "home"), ("gmp", "gmp")]:
    N[f"cl_{k}"] = f1(CL.loc["world_net_1976-2020", c])
# measurement variants computed by build_extras.py (first found by the independent check)
EX = json.load(open(os.path.join(O, "housing", "extras.json"))); ex0 = EX["world_1976_2020_start_of_year_weights"]; ex1 = EX["world_1976_2020_same_year_weights"]
N.update(ex_val_port=f1(ex0["valuation_portfolio_yield"]), ex_val_mean=f1(ex0["valuation_country_mean"]), ex_val_gap=f2(EX["valuation_gap_country_mean_minus_portfolio"]),
         ex_netex_port=f1(ex0["net_ex_valuation_portfolio_yield"]), ex_sameyear=f1(ex1["net"]), ex_sameyear_x=f1(ex1["net_ex_valuation_country_mean"]))
N["g_net_7681_abs"] = f1(-hv("gmp", "1976-1981", "net"))
# =========================================================== Section 5: balance sheet
LG = LB["latest_shares_gdp_weighted"]; LM = LB["latest_shares_median"]
N.update(bs_year=str(LB["latest_common_year"]), bs_dw=f1(LG["dwellings_land"]), bs_f6=f1(LG["F6_pension_insurance"]), bs_f5=f1(LG["F5_equity_funds"]), bs_f23=f1(LG["F2F3_deposits_debt_sec"]),
         bs_oth=f1(LG["other"]), bs_liab=f1(LG["liab_total_pct_gross"]), bs_dw_med=f1(LM["dwellings_land"]), bs_f6_med=f1(LM["F6_pension_insurance"]), bs_f5_med=f1(LM["F5_equity_funds"]),
         bs_f23_med=f1(LM["F2F3_deposits_debt_sec"]), bs_liab_med=f1(LM["liab_total_pct_gross"]), bs_f5l=f1(LG["F5_listed"]), bs_f5u=f1(LG["F5_unlisted"]), bs_f5o=f1(LG["F5_other_equity"]), bs_f5f=f1(LG["F5_fund_shares"]),
         bs_yrs_med=f1(LM["nw_to_gdp"]), bs_hrs_med=f0(LM["nw_per_worker_national_hours"]), bs_wh_med=f0(LM["nw_per_worker_world_hours"]))
CP = rd("balance", "table_composition_latest_2023.csv", index_col=0); N["bs_n"] = f0(len(CP))
N.update(bs_esp=f0(CP.loc["ESP", "dwellings_land"]), bs_dnk=f0(CP.loc["DNK", "dwellings_land"]), bs_rou=f0(CP.loc["ROU", "dwellings_land"]), bs_jpn_dep=f0(CP.loc["JPN", "F2F3_deposits_debt_sec"]),
         bs_usa_f5=f0(CP.loc["USA", "F5_equity_funds"]), bs_swe_f5=f0(CP.loc["SWE", "F5_equity_funds"]), bs_dnk_f5=f0(CP.loc["DNK", "F5_equity_funds"]))
for c in ["USA", "FRA", "JPN", "DEU", "GBR"]: N[f"yrs_{c}"] = f1(CP.loc[c, "nw_to_gdp"])
N["wh_usa"] = f0(CP.loc["USA", "nw_per_worker_world_hours"]); N["wh_jpn"] = f0(CP.loc["JPN", "nw_per_worker_world_hours"])
WHC = rd("balance", "timepath_nw_world_hours_by_country.csv", index_col=0); N["wh_jpn_2007"] = f0(WHC.loc[2007, "JPN"])
BP = rd("balance", "timepath_balanced_panel_gdp_weighted.csv", index_col=0); N.update(bp_n=f0(BP.n.iloc[-1]), bp_1995=f2(BP.loc[1995, "nw_to_gdp"]), bp_2021=f2(BP.loc[2021, "nw_to_gdp"]), bp_2023=f2(BP.loc[2023, "nw_to_gdp"]),
                                                                                                   bp_dw_1995=f0(BP.loc[1995, "dwellings_land"]), bp_dw_2008=f0(BP.loc[2008, "dwellings_land"]))
N["bs_chk"] = f"{LB['check_years_of_avh_equals_nw_to_gdp_maxabs']:.0e}"
UH = LB["us_headline"]; Z = rd("balance", "us_z1_balance_sheet_1952_2026.csv", index_col=0)
N.update(us_re_52=f0(UH["1952"]["real_estate_pct"]), us_re_26=f0(UH["2026"]["real_estate_pct"]), us_pen_52=f0(UH["1952"]["pension_pct"]), us_pen_26=f0(UH["2026"]["pension_pct"]),
         us_eq_52=f0(UH["1952"]["equities_mf_pct"]), us_eq_26=f0(UH["2026"]["equities_mf_pct"]), us_oth_52=f0(UH["1952"]["other_pct"]), us_oth_26=f0(UH["2026"]["other_pct"]),
         us_liab_52=f0(UH["1952"]["liab_pct"]), us_liab_26=f0(UH["2026"]["liab_pct"]), us_liab_max=f0(Z.liabilities_pct.max()), us_liab_max_y=str(int(Z.liabilities_pct.idxmax())),
         us_pen_max=f0(Z.pension_entitlements_pct.max()), us_pen_max_y=str(int(Z.pension_entitlements_pct.idxmax())),
         us_pb_52=f0(Z.loc[1952, "private_business_IMA_pct"]), us_pb_26=f0(Z.private_business_IMA_pct.iloc[-1]),
         us_yrs_52=f2(UH["1952"]["nw_years_of_work"]), us_yrs_26=f2(UH["2026"]["nw_years_of_work"]), us_yrs_g=f2(LB["us_nw_years_growth_1952_last_pct_per_yr"]),
         us_hrs_52=f0(UH["1952"]["nw_per_worker_us_hours"]), us_hrs_26=f0(UH["2026"]["nw_per_worker_us_hours"]), us_hrs_g=f2(LB["us_nw_hours_growth_1952_2023_pct_per_yr"]),
         us_avh_52=f0(Z.loc[1952, "avh"]), us_avh_23=f0(Z.loc[2023, "avh"]), us_wh_70=f0(UH["1970"]["nw_per_worker_world_hours"]), us_wh_26=f0(UH["2026"]["nw_per_worker_world_hours"]),
         z1_last=LB["z1_last_period"].replace(":", "&nbsp;"), oecd_z1=f2(LB["oecd_vs_z1_usa_2023_nw_ratio"]))
PG = LB["payg_2021"]; N.update(pg_n=f0(PG["countries_with_pct_gdp"]), pg_med=f0(PG["S13PS_pct_gdp_median"]), pg_lo=f0(PG["S13PS_pct_gdp_range"][0]), pg_hi=f0(PG["S13PS_pct_gdp_range"][1]),
                               pg_nw_n=f0(PG["countries_with_pct_nw"]), pg_nw=f0(PG["S13PS_pct_nw_median"]), pg_fund=f0(PG["funded_S1PF_pct_gdp_median"]), pg_nwgdp=f2(PG["nw_to_gdp_median"]), pg_nwgdp2=f2(PG["nw_incl_payg_to_gdp_median"]))
PE = rd("balance", "table_payg_entitlements_2021.csv", index_col=0)
for c in ["BEL", "DEU", "FRA", "ITA", "ESP", "FIN", "POL", "ROU"]: N[f"pg_{c}"] = f0(PE.loc[c, "S13PS_pct_household_nw"])
SY = LB["synthesis"]; N.update(sy_n=f0(len(SY["countries"])), sy_med=f1(SY["return_nw_median"]), sy_gdpw=f1(SY["return_nw_gdpw"]), sy_lo=f1(SY["return_nw_range"][0]), sy_hi=f1(SY["return_nw_range"][1]),
                               sy_home=f1(SY["home_alone_median"]), sy_avg=f1(SY["return_nw_avg_shares_median"]), sy_oz=f1(SY["return_nw_other_zero_median"]), sy_lb=f1(SY["return_nw_liab_at_bills_median"]),
                               sy_gross=f1(SY["return_gross_median"]))
SB = rd("balance", "table_balance_sheet_hour_return_by_country.csv", index_col=0); N["sy_usa"] = f1(SB.loc["USA", "return_net_worth"]); N["sy_prt"] = f1(SB.loc["PRT", "return_net_worth"]); N["sy_prt_home"] = f1(SB.loc["PRT", "home_alone"])
N["eq_prt"] = f1(rd("housing", "table_claims_by_country_national_hours.csv", header=[0, 1], index_col=0).loc["PRT", ("equities", "1976-2020")])
ip = pd.DataFrame(SY["incl_payg"]).T; N.update(sy_pn=f0(len(ip)), sy_p0=f1(ip.return_net_worth.median()), sy_p1=f1(ip.return_net_worth_incl_payg.median()),
                                               sy_deu0=f1(ip.loc["DEU", "return_net_worth"]), sy_deu1=f1(ip.loc["DEU", "return_net_worth_incl_payg"]), sy_fin0=f1(ip.loc["FIN", "return_net_worth"]), sy_fin1=f1(ip.loc["FIN", "return_net_worth_incl_payg"]))
lo_c, hi_c = SB.return_net_worth.idxmin(), SB.return_net_worth.idxmax(); N["sy_lo_c"] = lo_c; N["sy_hi_c"] = hi_c

# =========================================================== Section 6: PAYG
PD = rd("balance", "table_payg_return_by_decade_world.csv", index_col=0)
N.update(pd_5123=f1(PD.loc["1951-2023", "hours_all"]), pd_5123_pct=f2(PD.loc["1951-2023", "hours_all"] / 10), pd_emp_5123=f1(PD.loc["1951-2023", "emp_all"]), pd_drag=f1(-PD.loc["1951-2023", "avh_drag"]),
         pd_drag_pct=f1(-PD.loc["1951-2023", "avh_drag"] / 10), pd_7620=f1(PD.loc["1976-2020", "hours_all"]), pd_7620_pct=f2(PD.loc["1976-2020", "hours_all"] / 10), pd_jst=f1(PD.loc["1976-2020", "hours_jst16"]),
         pd_s50=f1(PD.loc["1951-2023", "hours_1950_sample"]), pd_n_7620=f0(PD.loc["1976-2020", "n_countries_mean"]))
for d in ["1951-1960", "1961-1970", "1971-1980", "1981-1990", "1991-2000", "2001-2010", "2011-2020", "2011-2023"]: N["pd_" + d[:4] + d[5:]] = f1(PD.loc[d, "hours_all"])
PC = rd("balance", "table_payg_return_by_country.csv", index_col=0)
for c in ["JPN", "DEU", "FRA", "ITA", "USA"]: N[f"pc_{c}"] = f1(PC.loc[c, "hours_1976_2020"])
N["pc_med13"] = f1(SY["payg_median"])
PJ = rd("balance", "table_pop2064_projection.csv", index_col=0)
N.update(pj_1=f1(PJ.iloc[0, 0]), pj_2=f1(PJ.iloc[1, 0]), pj_3=f1(PJ.iloc[2, 0]), pj_4=f1(PJ.iloc[3, 0]), pj_all=f1(PJ.loc["2024-2060 (projection)", "pop2064_gdp_weighted_2023w"]),
         pj_head=f1(PJ.loc["2024-2060 (projection)", "pop2064_world_headcount"]), pj_jst=f1(PJ.loc["2024-2060 (projection)", "pop2064_jst16_gdpw"]),
         pj_jst_abs=f1(abs(PJ.loc["2024-2060 (projection)", "pop2064_jst16_gdpw"])), pj_hist=f1(PJ.loc["1976-2020 (history, 2023 weights)", "pop2064_gdp_weighted_2023w"]))
CW = rd("balance", "table_claims_hour_return_with_payg.csv", index_col=0)
N.update(cw_payg_w=f1(CW.loc["PAYG (growth of total hours), all PWT countries with hours", "world_1976_2020"]), cw_payg_n=f1(CW.loc["PAYG (growth of total hours), same 16 JST countries", "national_gdpw_1951_2020"]),
         cw_home_n=f1(CW.loc["Home (JST housing)", "national_gdpw_1951_2020"]), cw_eq_n=f1(CW.loc["Equities", "national_gdpw_1951_2020"]), cw_bond_n=f1(CW.loc["Government bonds", "national_gdpw_1951_2020"]),
         cw_bill_n=f1(CW.loc["Deposits / bills", "national_gdpw_1951_2020"]), cw_payg_n76=f1(CW.loc["PAYG (growth of total hours), same 16 JST countries", "national_gdpw_jst16_1976_2020"]),
         cw_home_n76=f1(CW.loc["Home (JST housing)", "national_gdpw_jst16_1976_2020"]))

# =========================================================== Section 7: a life
SL = rd("life", "summary_baseline.csv", index_col=0); SN = rd("life", "summary_baseline_never_negative.csv", index_col=0); SA = rd("life", "summary_anchor2000.csv", index_col=0)
C = LL["counts"]; D = LL["design"]
N.update(lf_n=f0(C["n"]), lf_poss=f0(LL["cohorts"]["possible"]), lf_M=f0(D["base"]["M"]), lf_c=f1(D["base"]["c"] * 100), lf_b=f0(D["base"]["b"] * 100), lf_tau=f0(D["base"]["tau"] * 100),
         lf_dep=f0(D["deposit"] * 100), lf_ltv=f0(D["ltv"] * 100), lf_buyc=f2(D["buy_cost"] * 100), lf_term=f0(D["term"]), lf_spread=f1(D["spread"] * 100), lf_ospread=f1(D["borrow_spread_over_bill"] * 100),
         lf_R=f2(SL.loc["W_R", "median"]), lf_O=f2(SL.loc["W_O", "median"]), lf_Os=f2(SL.loc["W_O_net_sell", "median"]), lf_OR=f2(SL.loc["O_over_R", "median"]), lf_OR25=f2(SL.loc["O_over_R", "p25"]), lf_OR75=f2(SL.loc["O_over_R", "p75"]),
         lf_OmR=f2(SL.loc["O_minus_R", "median"]), lf_OmR25=f2(SL.loc["O_minus_R", "p25"]), lf_OmR75=f2(SL.loc["O_minus_R", "p75"]), lf_OmR_mean=f2(SL.loc["O_minus_R", "mean"]),
         lf_beats=f0(C["O_beats_R"]), lf_beats_pct=pct(C["O_beats_R"] / C["n"]), lf_payg=f2(SL.loc["W_payg", "median"]), lf_fund=f2(SL.loc["W_funded", "median"]),
         lf_fp=f2(SL.loc["funded_over_payg", "median"]), lf_fp25=f2(SL.loc["funded_over_payg", "p25"]), lf_fp75=f2(SL.loc["funded_over_payg", "p75"]), lf_fp_win=pct(C["funded_beats_payg"] / C["n"]),
         lf_val=pct(SL.loc["O_valuation_share", "median"], 1), lf_val25=pct(SL.loc["O_valuation_share", "p25"], 1), lf_val75=pct(SL.loc["O_valuation_share", "p75"], 1), lf_val_n=f0(SL.loc["O_valuation_share", "n"]),
         lf_buyage=f0(SL.loc["buy_age", "median"]), lf_never=f0(C["never_buy"]), lf_q=f1(SL.loc["q_final", "median"]), lf_Rw=f1(SL.loc["W_R_worldhr", "median"]), lf_Ow=f1(SL.loc["W_O_worldhr", "median"]),
         lf_nn=f0(C["never_negative"]), lf_nn_OR=f2(SN.loc["O_over_R", "median"]), lf_nn_OmR=f2(SN.loc["O_minus_R", "median"]), lf_nn_beats=pct(rd("life", "robustness_one_at_a_time.csv").iloc[0]["nn_share_O_beats_R"]),
         lf_negany=f0(C["any_negative"]), lf_negR=f0(C["R_negative"]), lf_negO=f0(C["O_negative"]), lf_negmin=f2(C["median_min_balance_negative_lives_years_of_pay"]), lf_endneg=f0(C["negative_W_R"]),
         lf_Rmin=f1(SL.loc["W_R", "min"]))
DC = rd("life", "summary_by_cohort_decade.csv", index_col=0); N.update(dc_50=f2(DC.loc["1950s", "O_over_R"]), dc_60=f2(DC.loc["1960s", "O_over_R"]), dc_70=f2(DC.loc["1970s", "O_over_R"]), dc_80=f2(DC.loc["1980s", "O_over_R"]),
                                                                      dc_50d=f2(DC.loc["1950s", "O_minus_R"]), dc_80d=f2(DC.loc["1980s", "O_minus_R"]))
DV = rd("life", "decade_O_vs_R_baseline_variable_bills.csv", header=[0, 1], index_col=0)
for v in ["baseline", "variable", "bills"]:
    N[f"dv_{v}_50"] = f2(DV.loc["1950s", ("O_over_R", v)]); N[f"dv_{v}_80"] = f2(DV.loc["1980s", ("O_over_R", v)])
    N[f"dv_{v}_lo"] = f2(DV[("O_over_R", v)].min()); N[f"dv_{v}_hi"] = f2(DV[("O_over_R", v)].max())
N["dv_share"] = pct((DV.loc["1950s", ("O_over_R", "variable")] - DV.loc["1980s", ("O_over_R", "variable")]) / (DV.loc["1950s", ("O_over_R", "baseline")] - DV.loc["1980s", ("O_over_R", "baseline")]))
N["us70_buy_year"] = str(1970 + int(LL["usa_1970"]["buy_age"]) - 25)
SC = rd("life", "summary_by_country.csv", index_col=0); neg = SC.O_negative.sort_values(ascending=False)
NM = {"AUS": "Australia", "BEL": "Belgium", "CHE": "Switzerland", "DEU": "Germany", "DNK": "Denmark", "ESP": "Spain", "FIN": "Finland", "FRA": "France", "GBR": "the UK", "ITA": "Italy", "JPN": "Japan", "NLD": "the Netherlands", "NOR": "Norway", "PRT": "Portugal", "SWE": "Sweden", "USA": "the US"}
N["neg_top"] = ", ".join(f"{NM[c]} {int(v)}" for c, v in neg.iloc[:6].items()); N["neg_rest"] = f0(neg.iloc[6])
LC = rd("life", "life_cohorts_baseline.csv"); en = LC[LC.W_O < 0]; fr = en[en.country == "FRA"]
N.update(fr_first=str(int(fr.cohort.min())), fr_last=str(int(fr.cohort.max())), fr_min=f1(fr.W_O.min()))
N["neg_others"] = " and ".join(f"{NM[c]} ({', '.join(str(int(y)) for y in g.cohort)})" for c, g in en[en.country != "FRA"].groupby("country"))
PPC = rd("life", "price_to_pay_standard_2000_home_by_country.csv", index_col=0); N["fr_pp_65"] = f0(4 * PPC.loc[1965, "FRA"] / PPC.loc[1951, "FRA"])
DEC = rd("life", "decomposition_own_minus_rent.csv", header=[0, 1], index_col=0)
def dm(k, s="median", grp="all_buyers"): return float(DEC.loc[k, (grp, s)])
N.update(d_n=f0(dm("OR_price_gain", "n")), d_pg=f2(dm("OR_price_gain")), d_gr=f2(dm("OR_gross_rent_saved")), d_rc=f2(dm("OR_running_costs")), d_nr=f2(dm("OR_net_rent_saved")), d_int=f2(dm("OR_interest")),
         d_bc=f2(dm("OR_buycost")), d_fr=f2(dm("OR_forgone_return")), d_omr=f2(dm("O_minus_R")), d_pg_m=f2(dm("OR_price_gain", "mean")), d_nr_m=f2(dm("OR_net_rent_saved", "mean")),
         d_int_m=f2(dm("OR_interest", "mean")), d_fr_m=f2(dm("OR_forgone_return", "mean")), d_bc_m=f2(dm("OR_buycost", "mean")), d_omr_m=f2(dm("O_minus_R", "mean")),
         d_gain=f1(dm("OR_price_gain") + dm("OR_net_rent_saved")), d_cost=f1(dm("OR_interest") + dm("OR_forgone_return")))
PP = rd("life", "price_to_pay_standard_2000_home.csv", index_col=0)
for y in [1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020]: N[f"pp_{y}"] = f1(PP.loc[y, "median"])
N["pp_drift"] = f2(LL["price_to_pay_drift"]["median_log_change_per_year_1950_2020_pct_balanced"]); N["pp_rise"] = pct(PP.loc[2020, "median"] / PP.loc[2000, "median"] - 1)
U = LL["usa_1970"]; N.update(us70_R=f2(U["W_R"]), us70_O=f2(U["W_O"]), us70_age=f0(U["buy_age"]), us70_min=f2(U["O_min_balance"]), us70_mort=f1(U["mort_rate_at_buy"] * 100),
                             us70_int=f2(U["O_interest"]), us70_fr=f2(U["OR_forgone_return"]), us70_pg=f2(U["OR_price_gain"]))
A2 = LL["anchor2000_robustness"]; N.update(a2_R=f1(A2["medians"]["W_R"]), a2_O=f1(A2["medians"]["W_O"]), a2_negR=f0(A2["R_negative"]), a2_never=f0(A2["never_buy"]), a2_val=pct(A2["medians"]["O_valuation_share"]),
                                          a2_beats=pct(A2["O_beats_R"] / C["n"]), a2_age=f0(A2["medians"]["buy_age"]))
RO = rd("life", "robustness_one_at_a_time.csv", index_col=0)
N.update(ro_gmp_fp=f2(RO.loc["veh=gmp", "median_funded_over_payg"]), ro_bill_fp=f2(RO.loc["veh=bills", "median_funded_over_payg"]), ro_bill_fpwin=pct(RO.loc["veh=bills", "share_funded_beats_payg"]),
         ro_gmp_OR=f2(RO.loc["veh=gmp", "median_O_over_R"]), ro_bill_OR=f2(RO.loc["veh=bills", "median_O_over_R"]), ro_gmp_beats=pct(RO.loc["veh=gmp", "share_O_beats_R"]), ro_bill_beats=pct(RO.loc["veh=bills", "share_O_beats_R"]),
         ro_m6_never=f0(RO.loc["M=6.0", "n_never_buy"]), ro_m6_beats=pct(RO.loc["M=6.0", "share_O_beats_R"]))
FG = rd("life", "robustness_full_grid.csv"); ge, g2 = FG[FG.anchor == "entry"], FG[FG.anchor == "2000"]
N.update(fg_n=f0(len(ge)), fg_tot=f0(len(FG)), fg_lo=pct(ge.share_O_beats_R.min()), fg_hi=pct(ge.share_O_beats_R.max()), fg_med=pct(ge.share_O_beats_R.median()),
         fg_vlo=pct(ge.median_valuation_share.min()), fg_vhi=pct(ge.median_valuation_share.max()), fg2_med=pct(g2.share_O_beats_R.median()), fg2_v=pct(g2.median_valuation_share.median()),
         fg_or_lo=f2(ge.median_O_over_R.min()), fg_or_hi=f2(ge.median_O_over_R.max()))
ck = LL["checks"]; N["lf_chk"] = f"{max(v for k, v in ck.items() if isinstance(v, float)):.0e}"
N["pre1960"] = f2(abs(LL["pre1960_pay_growth_percap_minus_JST_GDP_per_PWT_hour_pct_mean"]))

dr = LL["cohorts"]["dropped"]; N["deu_from"] = str(max(dr["DEU"]) + 1); N["jpn_from"] = str(max(dr["JPN"]) + 1)
nm = {"AUS": "Australia", "BEL": "Belgium", "CHE": "Switzerland", "DEU": "Germany", "DNK": "Denmark", "ESP": "Spain", "FIN": "Finland", "FRA": "France", "GBR": "United Kingdom", "ITA": "Italy", "JPN": "Japan", "NLD": "Netherlands", "NOR": "Norway", "PRT": "Portugal", "SWE": "Sweden", "USA": "United States"}
# ---- review round: added keys
N.update(old_1976_p=f1(old["rent_yield_unscaled_pct"]["1976"]), old_2000_p=f1(old["rent_yield_unscaled_pct"]["2000"]), old_2020_p=f1(old["rent_yield_unscaled_pct"]["2020"]),
         rent_1976_p=f1(rh["1976"]), rent_2000_p=f1(rh["2000"]), rent_2020_p=f1(rh["2020"]), rent_gap_2020=f2(rh["2020"] - gc["2020"]), old_gap_2020=f2(old["rent_yield_unscaled_pct"]["2020"] - gc["2020"]),
         rent_fall_pct=f0((rh["2020"] / rh["1976"] - 1) * 100), gc_fall_pct=f0((gc["2020"] / gc["1976"] - 1) * 100))
N.update(pd_avh_7620=f1(PD.loc["1976-2020", "avh_all"]), pd_avh_5123=f1(-PD.loc["1951-2023", "avh_all"]), pd_20212023=f1(PD.loc["2021-2023", "hours_all"]), pd_pop_7620=f1(PD.loc["1976-2020", "pop2064_same_countries"]))
PV = rd("life", "summary_payg_variants.csv").set_index(["vehicle", "payg_claim"])
N.update(pv_avg=f2(PV.loc[("6040", "payg_avg_pay_per_worker"), "median_payg_claim_years_final_pay"]), pv_fp_avg=f2(PV.loc[("6040", "payg_avg_pay_per_worker"), "median_funded_over_payg"]),
         pv_fp_avg_win=pct(PV.loc[("6040", "payg_avg_pay_per_worker"), "share_funded_beats_payg"]), pv_bill_fp_avg=f2(PV.loc[("bills", "payg_avg_pay_per_worker"), "median_funded_over_payg"]),
         pv_gmp_fp_avg=f2(PV.loc[("gmp", "payg_avg_pay_per_worker"), "median_funded_over_payg"]))
N.update(d_omr25=f2(dm("O_minus_R", "p25")), d_omr75=f2(dm("O_minus_R", "p75")), lf_beats_pct_b=pct(C["O_beats_R"] / dm("OR_price_gain", "n")))
N.update(cl_home_pct=f2(CW.loc["Home (JST housing)", "national_gdpw_jst16_1976_2020"] / 10), cl_payg_pct=f2(CW.loc["PAYG (growth of total hours), same 16 JST countries", "national_gdpw_jst16_1976_2020"] / 10))
N["bs_f5sum"] = f1(LG["F5_listed"] + LG["F5_unlisted"] + LG["F5_other_equity"] + LG["F5_fund_shares"])
N.update(bpm_1995=f2(BP.loc[1995, "nw_to_gdp_median"]), bpm_2021=f2(BP.loc[2021, "nw_to_gdp_median"]), bpm_2023=f2(BP.loc[2023, "nw_to_gdp_median"]))
N.update(sy_lo_name=nm[lo_c], sy_hi_name=nm[hi_c])
LS = EX["labour_share_jst16"]; N.update(ls_a=f1(LS["level_start"] * 100), ls_b=f1(LS["level_end"] * 100), ls_eff=f1(abs(LS["effect_per_1000h_per_year"])), ls_eff_abs=f1(abs(LS["effect_per_1000h_per_year"])))
N["dv_removed"] = f0(100 - float(N["dv_share"])); N["pp_drift_abs"] = f2(abs(LL["price_to_pay_drift"]["median_log_change_per_year_1950_2020_pct_balanced"]))
N["rb_dec"] = f1(RB["National hours, Dec-to-Dec interpolated hour, median, 1976-2019"])
Zu = Z.loc[[1952, 2023]]
N.update(us_yrs_g23=f2(np.log(Zu.loc[2023, "nw_years_of_us_work_per_worker"] / Zu.loc[1952, "nw_years_of_us_work_per_worker"]) / 71 * 100),
         us_avh_g=f2(abs(np.log(Zu.loc[2023, "avh"] / Zu.loc[1952, "avh"]) / 71 * 100)), us_yrs_23=f2(Zu.loc[2023, "nw_years_of_us_work_per_worker"]), us_hrs_23=f0(Zu.loc[2023, "nw_per_worker_us_hours"]))
N.update(ls_eff_usd=f1(abs(LS["usd_weights_effect_per_1000h_per_year"])), earn_home=f1(LS["home_4x_pay_in_years_of_earnings"]), earn_budget=f0(LS["budget_35pct_of_pay_in_pct_of_earnings"]),
         ls_mean=f0(LS["mean_level_1951_2019_ppp_weights"] * 100))
EXW = EX["world_1976_2020_same_year_weights_wb_avg_fx"]; N["ex_sameyear_wb"] = f1(EXW["net"])
N["rb_dec_base"] = f1(RB["Baseline national hour, median, same window 1976-2019"])
N["pc_FIN"] = f1(PC.loc["FIN", "hours_1976_2020"])
N["nat50_bond_med"] = f1(CL.loc["national_net_median_1951-2020", "gov_bonds"])
N["pg_med_wb"] = f0(PE.S13PS_pct_gdp_wb.median()) if "S13PS_pct_gdp_wb" in PE else ""
TPN = rd("balance", "timepath_nw_years_of_work_by_country.csv", index_col=0)[LB["balanced_panel_countries"]]
N.update(bpm_1995=f2(TPN.loc[1995].median()), bpm_2021=f2(TPN.loc[2021].median()), bpm_2023=f2(TPN.loc[2023].median()))
N["rb_eq_gap"] = f1(RB["Equal weights"] - hv("gmp", "1976-2020", "net"))
# closing paragraph
N["cl_cap_lo"] = f1(hv("gmp", "1976-2025", "net") / 10); N["cl_cap_hi"] = f1(hv("housing", "1976-2025", "net") / 10); N["cl_payg"] = f2(PD.loc["1976-2020", "hours_all"] / 10)

# =========================================================== tables
pers = ["1976-1981", "1982-2000", "2001-2020", "2021-2025", "1976-2020", "1976-2025"]
labs = [("total", "Total return (a)"), ("cash", "&mdash; net rent / cash"), ("price", "&mdash; price"), ("valuation", "&mdash;&mdash; valuation change"), ("price_ex_valuation", "&mdash;&mdash; price excluding valuation"),
        ("needed", "Needed to keep pace with the hour (c)"), ("net", "Net gain: (a) &minus; (c)"), ("net_ex_valuation", "Net gain excluding valuation")]
rows = [["<strong>Housing, 16 countries</strong>"] + [""] * 6] + [[l] + [f1(hv("housing", p, k)) for p in pers] for k, l in labs]
rows += [["<strong>GMP (note 3)</strong>"] + [""] * 6] + [[l.replace("net rent / cash", "cash")] + [f1(hv("gmp", p, k)) for p in pers] for k, l in labs]
T["T2"] = table("Table 2. Hours a year generated by housing and by the GMP, per 1,000 world hours of capital (author&rsquo;s calculations). Annual log returns, % a year &times; 10. Housing: Macrohistory Database to 2020, OECD-chained 2021&ndash;2025, GDP-weighted at start-of-year US-dollar GDP. Components may not add exactly because of rounding",
                [""] + [p.replace("-", "&ndash;") for p in pers], rows, bold=(7, 16))
nm = {"AUS": "Australia", "BEL": "Belgium", "CHE": "Switzerland", "DEU": "Germany", "DNK": "Denmark", "ESP": "Spain", "FIN": "Finland", "FRA": "France", "GBR": "United Kingdom", "ITA": "Italy", "JPN": "Japan", "NLD": "Netherlands", "NOR": "Norway", "PRT": "Portugal", "SWE": "Sweden", "USA": "United States"}
rows = [[nm[c]] + [f1(HC.loc[c, ("1976-2020", k)]) for k in ["total", "cash", "valuation", "price_ex_valuation", "needed", "net", "net_ex_valuation"]] + [f1(HC.loc[c, ("1951-2020", "net")]), f1(H25.loc[c, "net"])] for c in HC.index]
HN = rd("housing", "table_housing_national_hours_to2025.csv", index_col=0)
rows.append(["<strong>GDP-weighted</strong>"] + [f1(nat[k]) for k in ["total", "cash", "valuation", "price_ex_valuation", "needed", "net", "net_ex_valuation"]] + [f1(nat50["net"]), f1(HN.loc["2021-2025", "net"])])
rows.append(["<strong>Median</strong>"] + [f1(HC[("1976-2020", k)].median()) for k in ["total", "cash", "valuation", "price_ex_valuation", "needed"]] + [f1(nat["net_country_median"]), f1(nat["net_ex_val_country_median"])] + [f1(HC[("1951-2020", "net")].median()), f1(H25.net.median())])
def summ(df, cols, f=f1):
    return [["<strong>" + l + "</strong>"] + [f(getattr(df[c], m)()) for c in cols] for l, m in [("Median", "median"), ("Minimum", "min"), ("Maximum", "max")]]
c3 = [("1976-2020", k) for k in ["total", "cash", "valuation", "price_ex_valuation", "needed", "net", "net_ex_valuation"]] + [("1951-2020", "net")]
r3 = [["<strong>GDP-weighted</strong>"] + [f1(nat[k]) for k in ["total", "cash", "valuation", "price_ex_valuation", "needed", "net", "net_ex_valuation"]] + [f1(nat50["net"]), f1(HN.loc["2021-2025", "net"])]]
for l, m in [("Median", "median"), ("Minimum", "min"), ("Maximum", "max")]:
    r3.append([l] + [f1(getattr(HC[c], m)()) for c in c3] + [f1(getattr(H25["net"], m)())])
r3[1][6] = f1(nat["net_country_median"]); r3[1][7] = f1(nat["net_ex_val_country_median"]); r3[1][8] = f1(nat50["net_country_median"])   # medians as computed from unrounded data
T["T3s"] = table("Table 3. Housing in each country&rsquo;s own hours (local nominal GDP per hour worked), hours a year per 1,000 hours of housing capital, 16 countries (author&rsquo;s calculations). Columns 1&ndash;7: 1976&ndash;2020. Country rows: Table A1",
                ["", "Total", "Net rent", "Valuation", "Price ex val.", "Needed", "Net", "Net ex val.", "Net 1951&ndash;2020", "Net 2021&ndash;2025"], r3, bold=(0,), small=True)
T["T3"] = table("Table A1. Housing in each country&rsquo;s own hours (local nominal GDP per hour worked), hours a year per 1,000 hours of housing capital (author&rsquo;s calculations). Columns 1&ndash;7: 1976&ndash;2020. Germany&rsquo;s 1951&ndash;2020 column starts in 1963 and Japan&rsquo;s in 1960",
                ["", "Total", "Net rent", "Valuation", "Price ex val.", "Needed", "Net", "Net ex val.", "Net 1951&ndash;2020", "Net 2021&ndash;2025"], rows, bold=(16, 17), small=True)
yrs = [1950, 1976, 1981, 1990, 2000, 2010, 2020]
rows = [["Net rent yield, corrected weights"] + [f2(RY.loc[y, "rent_yield_pct_same_year_w"]) for y in yrs] + [f2(EXT["rent_yield_2025_gdpw_pct"])],
        ["GMP cash distribution yield (note 3)"] + [("&ndash;" if pd.isna(RY.loc[y, "gmp_cash_yield_pct"]) else f2(RY.loc[y, "gmp_cash_yield_pct"])) for y in yrs] + [f2(EXT["gmp_cash_yield_2025_pct"])],
        ["<em>Note 3&rsquo;s calculation as reproduced here (wrong weights; printed as " + f1(old["rent_yield_unscaled_pct"]["1976"]) + ", " + f1(old["rent_yield_unscaled_pct"]["2000"]) + ", " + f1(old["rent_yield_unscaled_pct"]["2020"]) + ")</em>"] + [(f"<em>{f2(old['rent_yield_unscaled_pct'][str(y)])}</em>" if str(y) in old["rent_yield_unscaled_pct"] else "&ndash;") for y in yrs] + ["&ndash;"]]
T["T4"] = table("Table 5. Housing net rent yield and the GMP&rsquo;s cash distribution yield, % (author&rsquo;s calculations). Rent yield: 16 countries, weighted by same-year US-dollar GDP; 2025 chained with OECD price and rent indices",
                [""] + [str(y) for y in yrs] + ["2025"], rows)
rows = [[a, f1(CL.loc["world_net_1976-2020", k]), f1(CL.loc["national_net_gdpw_1976-2020", k]) if k != "gmp" else "&ndash;", f1(CL.loc["national_net_median_1976-2020", k]) if k != "gmp" else "&ndash;",
         f1(CL.loc["national_net_gdpw_1951-2020", k]) if k != "gmp" else "&ndash;", f1(CL.loc["national_net_median_1951-2020", k]) if k != "gmp" else "&ndash;"]
        for a, k in [("Housing", "housing"), ("Equities", "equities"), ("GMP (note 3)", "gmp"), ("Government bonds", "gov_bonds"), ("Bills", "deposits_bills")]]
T["T5"] = table("Table 4. Net hour return of each claim, hours a year per 1,000 hours (author&rsquo;s calculations; same 16 countries and years; Macrohistory Database total returns). National-hour columns average each country&rsquo;s net at each year&rsquo;s GDP weights, over the same country-years as Table 3." + ("" if (f1(nat["net"]), f1(nat50["net"])) == (f1(CL.loc["national_net_gdpw_1976-2020", "housing"]), f1(CL.loc["national_net_gdpw_1951-2020", "housing"])) else " Table 3 weights the components instead, which gives " + f1(nat["net"]) + " and " + f1(nat50["net"]) + " for housing.") + " Bills stand in for deposits, which typically earn less",
                ["Claim", "World, 1976&ndash;2020", "National, GDP-w., 1976&ndash;2020", "National, median, 1976&ndash;2020", "National, GDP-w., 1951&ndash;2020", "National, median, 1951&ndash;2020"], rows)
star = lambda c, r: c + ("*" if r["land_missing"] else "")
rows = [[star(c, r), f1(r.dwellings_land), f1(r.F5_equity_funds), f1(r.F6_pension_insurance), f1(r.F2F3_deposits_debt_sec), f1(r.other), f1(r.liab_total_pct_gross), f1(r.nw_to_gdp), f0(r.nw_per_worker_world_hours)] for c, r in CP.iterrows()]
rows.append(["<strong>GDP-weighted</strong>", f1(LG["dwellings_land"]), f1(LG["F5_equity_funds"]), f1(LG["F6_pension_insurance"]), f1(LG["F2F3_deposits_debt_sec"]), f1(LG["other"]), f1(LG["liab_total_pct_gross"]), "&ndash;", "&ndash;"])
rows.append(["<strong>Median</strong>", f1(LM["dwellings_land"]), f1(LM["F5_equity_funds"]), f1(LM["F6_pension_insurance"]), f1(LM["F2F3_deposits_debt_sec"]), f1(LM["other"]), f1(LM["liab_total_pct_gross"]), f1(LM["nw_to_gdp"]), f0(LM["nw_per_worker_world_hours"])])
c6 = ["dwellings_land", "F5_equity_funds", "F6_pension_insurance", "F2F3_deposits_debt_sec", "other", "liab_total_pct_gross", "nw_to_gdp", "nw_per_worker_world_hours"]
r6 = [["<strong>GDP-weighted</strong>"] + [f1(LG[k]) for k in c6[:6]] + ["&ndash;", "&ndash;"]]
for l, m in [("Median", "median"), ("Minimum", "min"), ("Maximum", "max")]:
    r6.append([l] + [f1(getattr(CP[k], m)()) for k in c6[:7]] + [f0(getattr(CP[c6[7]], m)())])
r6.append(["United States"] + [f1(CP.loc["USA", k]) for k in c6[:7]] + [f0(CP.loc["USA", c6[7]])]); r6.append(["Japan"] + [f1(CP.loc["JPN", k]) for k in c6[:7]] + [f0(CP.loc["JPN", c6[7]])])
T["T6s"] = table(f"Table 6. Household balance sheets (households and non-profit institutions serving them), {LB['latest_common_year']}, {len(CP)} countries: shares of gross assets, % (author&rsquo;s calculations from OECD Tables 720 and 9B). Years of work = net worth &divide; GDP. Country rows: Table A2",
                ["", "Dwellings + land", "Equity &amp; fund shares (F5)", "Pension &amp; insurance (F6)", "Deposits &amp; debt sec. (F2+F3)", "Other", "Liabilities", "Net worth, years of work", "Net worth per worker, world hours"], r6, bold=(0,), small=True)
T["T6"] = table(f"Table A2. Household balance sheets (households and non-profit institutions serving them), {LB['latest_common_year']}: shares of gross assets, % (author&rsquo;s calculations from OECD Tables 720 and 9B). Years of work = net worth &divide; GDP = net worth per worker in hours of national work &divide; annual hours per worker. * land not reported, so the housing share is understated",
                ["Country", "Dwellings + land", "Equity &amp; fund shares (F5)", "Pension &amp; insurance (F6)", "Deposits &amp; debt sec. (F2+F3)", "Other", "Liabilities", "Net worth, years of work", "Net worth per worker, world hours"],
                rows, bold=(len(rows) - 2, len(rows) - 1), small=True)
uy = ["1952", "1970", "1990", "2000", "2007", "2019", "2026"]
rows = [[l] + [f(UH[y][k]) if UH[y][k] is not None else "&ndash;" for y in uy] for l, k, f in [("Real estate", "real_estate_pct", f1), ("Pension entitlements", "pension_pct", f1), ("Corporate equities + mutual funds", "equities_mf_pct", f1),
        ("Deposits, money-market funds, debt securities", "deposits_debt_pct", f1), ("Other (private business, durables, life insurance)", "other_pct", f1), ("Liabilities, % of assets", "liab_pct", f1),
        ("Net worth per worker, years of US work", "nw_years_of_work", f2), ("&hellip; in US hours", "nw_per_worker_us_hours", f0), ("&hellip; in world hours", "nw_per_worker_world_hours", f0)]]
T["T7"] = table(f"Table 7. US households and non-profits, Federal Reserve Z.1 table B.101, % of total assets at year-end (2026: {LB['z1_last_period'].replace(':', ' ')}; its world-hour value uses the world hour of March 2026, the last available) (author&rsquo;s calculations). On the OECD basis of Table 6, US net worth per worker is " + f1(CP.loc["USA", "nw_to_gdp"]) + " years in 2023, against " + f2(UH["2023"]["nw_years_of_work"]) + " here", [""] + uy, rows, bold=(6,))
rows = [[c, f0(r.S13PS_pct_gdp), f0(r.S1PF_funded_pct_gdp), f0(r.S13PS_pct_household_nw) if pd.notna(r.S13PS_pct_household_nw) else "&ndash;", f1(r.nw_to_gdp) if pd.notna(r.nw_to_gdp) else "&ndash;",
         f1(r.nw_incl_payg_to_gdp) if pd.notna(r.nw_incl_payg_to_gdp) else "&ndash;"] for c, r in PE.iterrows()]
c8 = ["S13PS_pct_gdp", "S1PF_funded_pct_gdp", "S13PS_pct_household_nw", "nw_to_gdp", "nw_incl_payg_to_gdp"]
r8 = []
for l, m in [("Median", "median"), ("Minimum", "min"), ("Maximum", "max")]:
    r8.append([l] + [f0(getattr(PE[k], m)()) for k in c8[:3]] + [f1(getattr(PE[k], m)()) for k in c8[3:]])
for c, l in [("DEU", "Germany"), ("FRA", "France"), ("ITA", "Italy"), ("NLD", "Netherlands")]:
    r8.append([l] + [f0(PE.loc[c, k]) for k in c8[:3]] + [f1(PE.loc[c, k]) for k in c8[3:]])
T["T8s"] = table("Table 8. Accrued-to-date pension entitlements, 2021 (Eurostat national accounts Table 29; author&rsquo;s calculations). Social-security (pay-as-you-go) schemes S13PS and funded schemes S1PF; PAYG % of GDP on Eurostat&rsquo;s own GDP. Net worth is households and non-profits (S1M). Country rows: Table A3",
                ["", "PAYG, % of GDP", "Funded, % of GDP", "PAYG, % of household net worth", "Net worth, years of work (= years of GDP)", "&hellip; including PAYG"], r8, bold=(0,))
T["T8"] = table("Table A3. Accrued-to-date pension entitlements, 2021 (Eurostat national accounts Table 29; author&rsquo;s calculations). Social-security (pay-as-you-go) schemes S13PS and funded schemes S1PF",
                ["Country", "PAYG, % of GDP", "Funded, % of GDP", "PAYG, % of household net worth", "Net worth, years of work (= years of GDP)", "&hellip; including PAYG"], rows, small=True)
rows = [[c, f0(r.share_home), f0(r.share_F5), f0(r.share_F6), f0(r.share_F2F3), f0(r.share_other), f0(r.liab_pct_gross), f1(r.home_alone), f1(r.return_gross_assets), f1(r.return_net_worth), f1(r.payg_hours_growth),
         f1(r.return_net_worth_incl_payg) if pd.notna(r.return_net_worth_incl_payg) else "&ndash;"] for c, r in SB.iterrows()]
rows.append(["<strong>Median</strong>", "", "", "", "", "", "", f1(SB.home_alone.median()), f1(SB.return_gross_assets.median()), f1(SB.return_net_worth.median()), f1(SB.payg_hours_growth.median()), f1(SB.return_net_worth_incl_payg.median())])
T["T9"] = table("Table 9. A weighted average of index returns, not a measured household return: 2023 balance-sheet shares (%) times each claim&rsquo;s net return in national hours, 1976&ndash;2020, hours a year per 1,000 (author&rsquo;s calculations). Last column: median of the " + f0(len(ip)) + " countries with Eurostat data; the same countries have a median of " + f1(ip.return_net_worth.median()) + " without PAYG",
                ["Country", "Dwellings + land", "F5", "F6", "F2+F3", "Other", "Liab.", "Housing alone", "Gross assets", "Net worth", "PAYG (hours growth)", "Net worth incl. PAYG"], rows, bold=(len(rows) - 1,), small=True)
dd = ["1951-1960", "1961-1970", "1971-1980", "1981-1990", "1991-2000", "2001-2010", "2011-2020", "2021-2023", "2011-2023", "1951-2023", "1976-2020"]
rows = [[l] + [f1(PD.loc[d, k]) for d in dd] for l, k in [("Total hours worked: the PAYG return", "hours_all"), ("&mdash; employment", "emp_all"), ("&mdash; annual hours per worker (return of a claim on average pay)", "avh_all"),
                                                        ("Total hours, constant 1950 sample", "hours_1950_sample"), ("Total hours, 16 Macrohistory countries", "hours_jst16"), ("<em>Memo: population 20&ndash;64, same countries</em>", "pop2064_same_countries")]]
rows.append(["Countries (average)"] + [f0(PD.loc[d, "n_countries_mean"]) for d in dd])
T["T10"] = table("Table 10. Growth of total hours worked, GDP-weighted across countries, per 1,000 a year (log growth in % &times; 10) (author&rsquo;s calculations from Penn World Table 11.0). Employment and hours per worker do not add exactly to total hours because the country sets with each series differ slightly",
                 [""] + [d.replace("-", "&ndash;") for d in dd], rows, bold=(0,), small=True)
jst = list(nm.keys())
rows = [[nm[c], f1(PC.loc[c, "hours_1951_2023"]), f1(PC.loc[c, "hours_1976_2020"]), f1(PC.loc[c, "emp_1976_2020"]), f1(PC.loc[c, "avh_drag_1976_2020"]), f1(PC.loc[c, "hours_2001_2023"]), f1(PC.loc[c, "pop2064_proj_2024_2060"])] for c in jst]
T["T11"] = table("Table 11. The PAYG return by country: growth of total hours worked, per 1,000 a year (author&rsquo;s calculations; Penn World Table 11.0; UN World Population Prospects 2024, medium variant, for the projection)",
                 ["Country", "Hours, 1951&ndash;2023", "Hours, 1976&ndash;2020", "Employment, 1976&ndash;2020", "Hours per worker, 1976&ndash;2020", "Hours, 2001&ndash;2023", "Population 20&ndash;64, 2024&ndash;2060 (projection)"], rows)
rows = [[l] + [f1(PJ.loc[i, k]) for k in ["pop2064_gdp_weighted_2023w", "pop2064_world_headcount", "pop2064_jst16_gdpw"]] for i, l in
        [(i, i.replace("-", "&ndash;")) for i in PJ.index]]
T["T12x"] = table("Table 12. Growth of the population aged 20&ndash;64, per 1,000 a year (UN World Population Prospects 2024, medium variant; author&rsquo;s calculations). Rows marked projection are projections, not data",
                 ["Period", "GDP-weighted (2023 weights)", "World headcount", "16 Macrohistory countries, GDP-weighted"], rows)
def srow(lab, k, f=f2, src=SL, extra=None):
    r = src.loc[k]; return [lab, f(r["median"]), f"{f(r['p25'])}&ndash;{f(r['p75'])}", f"{f(r['min'])} to {f(r['max'])}", f(r["gdp_weighted_mean"]), f(SN.loc[k, "median"])]
pf = lambda x: pct(x, 1)
rows = [srow("R: rent and invest", "W_R"), srow("O: buy at 35", "W_O"), srow("O, net of selling cost", "W_O_net_sell"), srow("<strong>O &minus; R</strong>", "O_minus_R"), srow("<strong>O &divide; R</strong>", "O_over_R"),
        srow("PAYG claim indexed to the wage bill, 10% of pay", "W_payg"), srow("Funded claim, 10% of pay in the 60/40", "W_funded"), srow("<strong>Funded &divide; PAYG</strong>", "funded_over_payg"),
        srow("Share of O&rsquo;s wealth from valuation, %", "O_valuation_share", f=pf), srow("Buying age", "buy_age", f=f0),
        srow("R in world hours &divide; fixed annual hours per worker", "W_R_worldhr", f=f1), srow("O in world hours &divide; fixed annual hours per worker", "W_O_worldhr", f=f1)]
T["T13"] = table(f"Table 12. Wealth at 65 in years of own final pay, {C['n']} lives (16 countries &times; cohorts starting work 1950&ndash;1980) (author&rsquo;s calculations). Last column: the {C['never_negative']} lives whose account never went below zero",
                 ["", "Median", "Interquartile range", "Min to max", "GDP-weighted mean", "Median, never negative"], rows, bold=(3, 4, 7))
rows = [[l, f2(dm(k)), f2(dm(k, "p25")), f2(dm(k, "p75")), f2(dm(k, "mean")), f2(dm(k, "median", "never_negative_buyers"))] for l, k in
        [("Home price gain", "OR_price_gain"), ("Imputed rent saved (gross)", "OR_gross_rent_saved"), ("Running costs paid by the owner (&minus;)", "OR_running_costs"), ("<em>Net rent saved</em>", "OR_net_rent_saved"),
         ("Mortgage interest (&minus;)", "OR_interest"), ("Buying cost (&minus;)", "OR_buycost"), ("Forgone 60/40 return on the deposit and extra outlays, and the difference in overdraft interest (&minus;)", "OR_forgone_return"), ("<strong>O &minus; R</strong>", "O_minus_R")]]
T["T14"] = table(f"Table 13. Why owning and renting come out close: O &minus; R for the {f0(dm('OR_price_gain', 'n'))} lives that buy, years of own final pay (author&rsquo;s calculations). Costs are shown as positive numbers to be subtracted. Means add up exactly; medians do not",
                 ["Item", "Median", "25th pct.", "75th pct.", "Mean", "Median, never negative"], rows, bold=(7,))
rows = [[d, f0(DC.loc[d, "n"]), f2(DC.loc[d, "W_R"]), f2(DC.loc[d, "W_O"]), f2(DC.loc[d, "O_minus_R"]), f2(DC.loc[d, "O_over_R"]), pct(DC.loc[d, "O_beats_R_share"]), pct(DC.loc[d, "O_valuation_share"], 1), f2(DC.loc[d, "funded_over_payg"]), f0(DC.loc[d, "R_negative"]), f0(DC.loc[d, "O_negative"])] for d in DC.index]
T["T15x"] = table("Table 15. A life by decade of the cohort&rsquo;s start, medians (author&rsquo;s calculations). &ldquo;1980s&rdquo; is the 1980 cohort only",
                 ["Cohort", "Lives", "R", "O", "O &minus; R", "O &divide; R", "O beats R, %", "Valuation share, %", "Funded &divide; PAYG", "R ever negative", "O ever negative"], rows, small=True)
rows = [[nm[c], f0(r.n), f2(r.W_R), f2(r.W_O), f2(r.O_over_R), pct(r.O_beats_R_share), f2(r.W_payg), f2(r.W_funded), f2(r.funded_over_payg), f0(r.buy_age), f0(r.O_negative)] for c, r in SC.iterrows()]
T["T16"] = table("Table A4. A life by country, medians across cohorts, years of own final pay (author&rsquo;s calculations)",
                 ["Country", "Lives", "R", "O", "O &divide; R", "O beats R, %", "PAYG", "Funded", "Funded &divide; PAYG", "Buying age", "O ever negative"], rows, small=True)
rows = [[l] + sum([[f2(DV.loc[d, ("O_over_R", v)]), f2(DV.loc[d, ("O_minus_R", v)])] for v in ["baseline", "variable", "bills"]], []) for d, l in [(d, d) for d in DV.index]]
T["T16v"] = table("Table 14. Owning against renting by decade of the cohort&rsquo;s start, under three variants: medians of O &divide; R and O &minus; R in years of own final pay (author&rsquo;s calculations). &ldquo;1980s&rdquo; is the 1980 cohort only",
                  ["Cohort", "Baseline: O &divide; R", "O &minus; R", "Variable-rate mortgage: O &divide; R", "O &minus; R", "Bills vehicle: O &divide; R", "O &minus; R"], rows)
py = [1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020]
rows = [["Median"] + [f1(PP.loc[y, "median"]) for y in py], ["25th percentile"] + [f1(PP.loc[y, "p25"]) for y in py], ["75th percentile"] + [f1(PP.loc[y, "p75"]) for y in py], ["Countries"] + [f0(PP.loc[y, "n"]) for y in py]]
T["T17"] = table("Table 15. Price of a home that cost 4 years of pay in 2000, in years of pay (Macrohistory Database nominal house prices &divide; national GDP per hour; author&rsquo;s calculations)", [""] + [str(y) for y in py], rows, bold=(0,))
lab = {"baseline (M4 at entry, c2.0, b35, 60/40, fixed)": "Baseline", "M=3.0": "Home 3&times; pay", "M=6.0": "Home 6&times; pay", "c=0.015": "Running costs 1.5%", "c=0.03": "Running costs 3%", "b=0.25": "Budget 25% of pay",
       "b=0.45": "Budget 45% of pay", "veh=gmp": "GMP vehicle (from 1976)", "veh=bills": "Bills vehicle", "mort=variable": "Variable-rate mortgage", "anchor=2000": "Home 4&times; pay in 2000 (original design)"}
rows = [[lab[i], f2(r.median_W_R), f2(r.median_W_O), f2(r.median_O_over_R), pct(r.share_O_beats_R), pct(r.median_valuation_share, 1), f2(r.median_funded_over_payg), pct(r.share_funded_beats_payg), f0(r.n_any_negative), f0(r.n_never_buy)] for i, r in RO.iterrows()]
T["T18"] = table("Table 16. A life: one change at a time from the baseline, medians across lives (author&rsquo;s calculations). * Lives that never buy have O &divide; R = 1, so rows with many non-buyers show 1.00. PAYG: indexed to the wage bill",
                 ["Variant", "R", "O", "O&#8239;&divide;&#8239;R*", "O wins, %", "Val. share, %", "Funded &divide; PAYG", "Funded wins, %", "O ever negative", "Never buy"], rows, bold=(0,), small=True)
rb = rd("housing", "table_housing_robustness.csv"); rbe = rd("housing", "table_housing_robustness_ext.csv")
DUP = ("National hours, GDP weights", "National hours, country median", "GMP", "Baseline, world hours, 1976-2025")
rows = [[r.case, f1(r.net_per_1000h), f1(r.net_ex_valuation_per_1000h)] for _, r in rb.iterrows() if not r.case.startswith(DUP)] + [[r.case, f1(r.net_per_1000h), f1(r.net_ex_valuation_per_1000h)] for _, r in rbe.iterrows() if not r.case.startswith(("Baseline, world hours, 1976-2020", "JST baseline", "GMP") + DUP)]
T["T19"] = table("Table A5. Housing: robustness, net hours a year per 1,000 hours (author&rsquo;s calculations). World hours 1976&ndash;2020 unless stated. National-hour and GMP comparisons are in Tables 2, 3 and A1. &ldquo;Dec-to-Dec interpolated hour&rdquo;: the national hour interpolated to December values instead of calendar-year averages. Tax and cost parameters from Jord&agrave; et al. (2019)", ["Case", "Net", "Net excluding valuation"], [[re.sub(r"(\d{4})-(\d{4})", r"\1&ndash;\2", c).replace("(JST)", "(Macrohistory Database)").replace("JST implied", "the database&rsquo;s implied"), a, b] for c, a, b in rows], bold=(0,))
T["T1"] = table("Table 1. Data (all free and public; retrieved September&ndash;October 2026)", ["Source", "Used for", "Coverage", "Terms"], [
    ["Jord&agrave;&ndash;Schularick&ndash;Taylor Macrohistory Database, release 6", "House prices, housing returns and net rent yields; equity, bond and bill returns; long rates; GDP; exchange rates", "16 countries with housing data, to 2020", "CC BY-NC-SA 4.0"],
    ["OECD analytical house price indicators", "House price and rent indices chained onto 2020; cross-check", "1970s&ndash;2025", "OECD terms (reuse with attribution)"],
    ["OECD household balance sheets: Table 720 (financial) and Table 9B (non-financial)", "Composition of household assets and liabilities", "31 countries with both sides in 2023", "OECD terms"],
    ["Federal Reserve, Financial Accounts of the United States (Z.1), table B.101", "US household balance sheet", "1952&ndash;2026&nbsp;Q2", "Public domain, attribution"],
    ["Eurostat, pension entitlements in national accounts (Table 29: nasa_10_pens1)", "Accrued pay-as-you-go and funded pension entitlements", "30 countries, 2021", "CC BY 4.0"],
    ["Penn World Table 11.0 (also via FRED; the two copies are identical)", "Persons engaged, average annual hours, labour share", "1950&ndash;2023", "CC BY 4.0"],
    ["World Bank, World Development Indicators", "GDP in local currency and US dollars; labour force (to extend hours to 2024&ndash;2025)", "1960&ndash;2025", "CC BY 4.0"],
    ["UN World Population Prospects 2024", "Population aged 20&ndash;64 (estimates and medium-variant projection)", "1950&ndash;2100", "CC BY 3.0 IGO"],
    ["BIS exchange rates; FRED (BLS CPI rent of primary residence; US GDP; nonfarm business hours)", "Exchange rates after 2020; US 2025 rent; US hours after 2023", "to 2026", "Public, attribution"],
    ["Notes 1&ndash;3 and the GMP weight history (Nakanishi 2026a&ndash;d)", "GMP total return and cash yield; the world hour", "1976&ndash;2026", "CC BY-NC 4.0 (CC-GMP TR, CC-WH)"]], numcols=set())
T["T_FILES"] = table("", ["File", "Content"], [["<code>code/fetch_*.py</code>", "Download and clean the public inputs (<code>data/SOURCES.md</code> lists URLs, dates and terms)"],
    ["<code>code/build_housing.py</code>, <code>build_housing_ext.py</code>", "Section 4: housing in world and national hours, 1951&ndash;2020 and the OECD extension to 2025; the note-3 correction; Tables 2&ndash;5, A1, A5; Figures 1&ndash;2"],
    ["<code>code/build_balance.py</code>", "Sections 5&ndash;6: balance sheets, Z.1, Eurostat Table 29, hours growth, projections; Tables 6&ndash;11, A2, A3; Figures 3&ndash;4"],
    ["<code>code/build_life.py</code>", "Section 7: the stylised lives, decompositions and robustness grid; Tables 12&ndash;16, A4; Figures 6&ndash;7"],
    ["<code>code/build_extras.py</code>", "Two measurement variants of the housing headline (portfolio-yield valuation, same-year weights); <code>output/housing/extras.json</code>"],
    ["<code>code/build_paper.py</code>", "All tables and every number in the text, generated from <code>output/</code>; Figure 5"],
    ["<code>output/*/build_log.json</code>", "Input checksums, identity checks, headline values"], ["<code>check/</code>", "Independent checks of Sections 4&ndash;7, written before reading the builders"]], numcols=set())
H = {}
for L in (LH, LB, LL, EX):
    H.update(L["inputs_sha256"])
H.update(EXT["inputs_sha256"])
T["HASHES"] = "\n".join(f"{v}  {k}" for k, v in sorted(H.items(), key=lambda kv: kv[0]))
N["n_hashes"] = f0(len(H))

# =========================================================== Figure 5 (regenerated): PAYG beside the other claims in national hours, and by decade
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False}); PAL = ["#1f4e79", "#6b8e6b", "#c98a2b", "#7f9fbf", "#8c4a3c", "#3b3b8f"]
fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.4, 4.2), gridspec_kw={"width_ratios": [1, 1.5]})
labs5 = ["PAYG\n(hours)", "Home", "Equities", "Gov.\nbonds", "Bills"]
vals = [CW.loc["PAYG (growth of total hours), same 16 JST countries", "national_gdpw_1951_2020"], CW.loc["Home (JST housing)", "national_gdpw_1951_2020"], CW.loc["Equities", "national_gdpw_1951_2020"],
        CW.loc["Government bonds", "national_gdpw_1951_2020"], CW.loc["Deposits / bills", "national_gdpw_1951_2020"]]
b = a1.bar(range(5), vals, 0.65, color=[PAL[5], PAL[2], PAL[0], PAL[3], "#b9b9b9"]); a1.axhline(0, color="black", lw=0.7)
for i, v in enumerate(vals): a1.text(i, v + 1 if v >= 0 else v - 1, f"{v:.1f}".replace("-", "\u2212"), ha="center", va="bottom" if v >= 0 else "top", fontsize=8)
a1.set_ylim(min(vals) - 7, max(vals) + 6)
a1.set_xticks(range(5)); a1.set_xticklabels(labs5, fontsize=8); a1.set_ylabel("hours a year per 1,000 hours")
a1.set_title("Net return in national hours, 16 countries,\nGDP-weighted, 1951–2020", loc="left", fontsize=9.5)
dec = ["1951-1960", "1961-1970", "1971-1980", "1981-1990", "1991-2000", "2001-2010", "2011-2023"]; x = np.arange(len(dec))
a2.bar(x - 0.2, PD.loc[dec, "hours_all"], 0.4, color=PAL[5], label="Total hours worked (the PAYG return)"); a2.bar(x + 0.2, PD.loc[dec, "emp_all"], 0.4, color=PAL[3], label="Employment")
pj = [i for i in PJ.index if "projection" in i and not i.startswith("2024-2060")]; xp = np.arange(len(dec), len(dec) + len(pj))
a2.bar(xp, PJ.loc[pj, "pop2064_gdp_weighted_2023w"], 0.4, color="white", edgecolor=PAL[5], hatch="///", label="Population 20–64, UN projection")
a2.axhline(0, color="black", lw=0.7); a2.set_xticks(list(x) + list(xp)); a2.set_xticklabels([d.replace("-", "–\n") for d in dec] + [p.split(" ")[0].replace("-", "–\n") for p in pj], fontsize=7)
a2.set_title("Growth of hours, all countries with data, GDP-weighted\n(per 1,000 a year)", loc="left", fontsize=9.5); a2.legend(fontsize=7.5, frameon=False)
fig.tight_layout(); fig.savefig(os.path.join(P, "img", "h_fig5.png"), dpi=160); plt.close(fig)

# =========================================================== fill
page = open(os.path.join(B, "paper_template.html"), encoding="utf-8").read()
for k, v in T.items(): page = page.replace("{{" + k + "}}", v)
used = set(re.findall(r"\{\{n:([A-Za-z0-9_]+)\}\}", page)); missing = sorted(used - set(N)); assert not missing, missing
for k in used: page = page.replace("{{n:" + k + "}}", str(N[k]))
left = sorted(set(re.findall(r"\{\{[^}]*\}\}", page))); assert not left, left
assert "{{" not in page
for src, dst in [("housing/fig_a_cumulative_hours_to2025.png", "h_fig1.png"), ("housing/fig_b_country_net_national_hours.png", "h_fig2.png"), ("balance/fig1_composition_latest.png", "h_fig3.png"),
                 ("balance/fig2_us_composition_years.png", "h_fig4.png"), ("life/fig_1_own_vs_rent_by_cohort.png", "h_fig6.png"), ("life/fig_2_funded_over_payg.png", "h_fig7.png"),
                 ]:
    shutil.copy(os.path.join(O, src), os.path.join(P, "img", dst))
if os.path.abspath(SITE_CSS) != os.path.abspath(os.path.join(P, "style.css")): shutil.copy(SITE_CSS, os.path.join(P, "style.css"))   # default: keep the shipped copy
open(os.path.join(P, "household.html"), "w", encoding="utf-8").write(page)
json.dump({k: N[k] for k in sorted(used)}, open(os.path.join(P, "numbers_in_text.json"), "w"), indent=1)
print("written", len(page), "bytes;", len(used), "numbers in text;", len(T), "tables")
