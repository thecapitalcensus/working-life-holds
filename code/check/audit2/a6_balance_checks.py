"""Audit 2: balance-sheet / PAYG / extras checks from output files and clean data (read only)."""
import json, numpy as np, pandas as pd
import os as _os, sys as _sys; _C = _os.path.dirname(_os.path.abspath(__file__)); _sys.path.insert(0, _os.path.abspath(_os.path.join(_C, '..', '..')))
from paths import R as _R, RAW as _RAW, DC as _DC, CN as _CN, JSTF as _JSTF, GMPR as _GMPR, cnd as _cnd, PWTX   # release: repository-relative paths (code/paths.py)
B=_os.path.join(_R,''); O=B+'output/'; C=_os.path.join(_DC,''); R={}
LB=json.load(open(O+'balance/build_log.json')); R['world_hour_last_month']=LB['world_hour_last_month']; R['z1_last']=LB['z1_last_period']
BP=pd.read_csv(O+'balance/timepath_balanced_panel_gdp_weighted.csv',index_col=0); R['balanced_panel_n_by_year_min_max']=[int(BP.n.min()),int(BP.n.max())]
R['balanced_panel_years_with_n_lt_max']=[int(y) for y in BP.index[BP.n<BP.n.max()]]
# PAYG %GDP with Eurostat's own GDP (MIO_EUR / nama_10_gdp) instead of WB LCU GDP
e=pd.read_csv(C+'eurostat_pension_entitlements_F63.csv'); g=pd.read_csv(C+'eurostat_gdp_current_meur.csv')
x=e[(e.variable=='F63_LE')&(e.unit=='MIO_EUR')&(e.scheme=='S13PS')&(e.year==2021)].set_index('iso3').value
gg=g[g.year==2021].set_index('iso3').value; s=(x/gg*100).dropna()
PE=pd.read_csv(O+'balance/table_payg_entitlements_2021.csv',index_col=0)
R['S13PS_pct_gdp_2021_median_eurostat_gdp']=round(float(s.reindex(PE.index).median()),1); R['S13PS_pct_gdp_2021_median_output']=round(float(PE.S13PS_pct_gdp.median()),1)
R['S13PS_pct_gdp_countries_eurostat_gdp']=int(s.reindex(PE.index).notna().sum())
# S14 vs S1M: PAYG as % of households-only net worth would be larger; size of NPISH in net financial worth
f=pd.read_csv(C+'oecd_hh_financial_bs.csv',low_memory=False); f=f[f.maturity.isin(['_Z','T'])&(f.currency_denom=='_T')&(f.entry=='N')&(f.instrument=='BF90')&(f.year==2021)]
pv=f.pivot_table(index='iso3',columns='sector',values='value'); r=(pv.S14/pv.S1M).dropna(); R['BF90_S14_over_S1M_2021_median_range']=[round(float(r.median()),3),round(float(r.min()),3),round(float(r.max()),3),int(len(r))]
# extras: labour share sample
EX=json.load(open(O+'housing/extras.json')); R['labour_share']=EX['labour_share_jst16']
pw=pd.read_excel(PWTX,sheet_name='Data')
HC=['AUS','BEL','CHE','DEU','DNK','ESP','FIN','FRA','GBR','ITA','JPN','NLD','NOR','PRT','SWE','USA']; pw=pw[pw.countrycode.isin(HC)]
ls=pw.pivot(index='year',columns='countrycode',values='labsh'); cg=pw.pivot(index='year',columns='countrycode',values='cgdpo'); cu=None
wb=pd.read_csv(C+'worldbank_gdp.csv'); usd=wb[wb.variable=='NY.GDP.MKTP.CD'].pivot_table(index='year',columns='iso3',values='value')[HC]
def L(wt,fixed=None):
    w=(wt if fixed is None else pd.DataFrame([wt.loc[fixed]]*len(wt),index=wt.index)).where(ls.notna()); w=w.div(w.sum(axis=1),axis=0); return (w*ls).sum(axis=1,min_count=1)
for nm,l in [('cgdpo_weights',L(cg)),('usd_weights',L(usd.reindex(ls.index))),('cgdpo_fixed_1976',L(cg,1976)),('equal',ls.mean(axis=1))]:
    R[f'labsh_{nm}_1976_2019']=[round(float(l.loc[1976]*100),1),round(float(l.loc[2019]*100),1),round(float(np.log(l.loc[2019]/l.loc[1976])/43*1000),2)]
R['labsh_countries_1976']=int(ls.loc[1976].notna().sum())
# life: PAYG average-pay variant framing
LC=pd.read_csv(O+'life/life_cohorts_baseline.csv'); R['W_payg_avg_median']=round(float(LC.W_payg_avg.median()),3)
R['note_consistent_framing']='if own pay per worker = GDP/hour x avh (contributions scale with avh too), an average-pay-indexed claim is exactly tau x 40 = 4.00 years of final pay per worker'
print(json.dumps(R,indent=1,default=str)); json.dump(R,open(_os.path.join(_C,'a6_balance_checks.json'),'w'),indent=1,default=str)
