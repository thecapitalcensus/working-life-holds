"""Audit 2: portfolio-yield valuation and same-year weights under the two weight sources (JST GDP/xrusd x unit vs WB USD GDP)."""
import json, numpy as np, pandas as pd
import os as _os, sys as _sys; _C = _os.path.dirname(_os.path.abspath(__file__)); _sys.path.insert(0, _os.path.abspath(_os.path.join(_C, '..', '..')))
from paths import R as _R, RAW as _RAW, DC as _DC, CN as _CN, JSTF as _JSTF, GMPR as _GMPR, cnd as _cnd, PWTX   # release: repository-relative paths (code/paths.py)
H=_R
d=pd.read_excel(_JSTF); pv=lambda v:d.pivot(index='year',columns='iso',values=v).sort_index()
TR,RR,YD=pv('housing_tr'),pv('housing_rent_rtn'),pv('housing_rent_yd'); HC=[c for c in TR.columns if TR[c].notna().any()]
TR,RR,YD=TR[HC],RR[HC],YD[HC]; FX=pv('xrusd'); GDP=pv('gdp')
tot_u=np.log1p(TR)-np.log(FX).diff()[HC]; val=-np.log(YD).diff()
g=pd.read_csv(f'{_CN}/world_yardsticks_usd.csv',index_col=0,parse_dates=True)['gdph']; dec=g[g.index.month==12]; dec.index=dec.index.year; need=np.log(dec).diff()
wb=pd.read_csv(f'{_DC}/worldbank_gdp.csv'); usd=wb[wb.variable=='NY.GDP.MKTP.CD'].pivot_table(index='year',columns='iso3',values='value')[HC]
jw=json.load(open(_cnd('wb_gdp.json')))[1]
WBG=pd.DataFrame([(r['countryiso3code'],int(r['date']),r['value']) for r in jw if r['value'] is not None and r['countryiso3code']],columns=['c','y','v']).pivot_table(index='y',columns='c',values='v',aggfunc='first')
UNIT=10.0**np.log10(WBG[GDP.columns]/(GDP/FX)).loc[1991:2020].median().round(); JU=(GDP/FX*UNIT)[HC]
def run(Wt):
    avail=tot_u.notna()&val.notna()&Wt.notna(); w=Wt.where(avail); w=w.div(w.sum(axis=1),axis=0)
    T=np.log((w*np.expm1(tot_u)).sum(axis=1,min_count=1)+1); Vm=(w*val).sum(axis=1,min_count=1)
    Vp=-(np.log((w*YD).sum(axis=1,min_count=1))-np.log((w*YD.shift(1)).sum(axis=1,min_count=1)))
    s=slice(1976,2020); return dict(net=round(float((T-need).loc[s].mean()*1000),2),val_mean=round(float(Vm.loc[s].mean()*1000),2),val_port=round(float(Vp.loc[s].mean()*1000),2))
R={'JST_start_of_year':run(JU.shift(1)),'JST_same_year':run(JU),'WB_start_of_year':run(usd.shift(1).reindex(JU.index)),'WB_same_year':run(usd.reindex(JU.index))}
print(json.dumps(R,indent=1)); json.dump(R,open(_os.path.join(_C,'a7_valuation_variants.json'),'w'),indent=1)
