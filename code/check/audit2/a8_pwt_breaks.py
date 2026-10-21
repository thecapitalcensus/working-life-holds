"""Audit 2: breaks in PWT 11 total hours (unification, territorial changes) that enter GDP-weighted hours growth and national hours."""
import numpy as np, pandas as pd, json
import os as _os, sys as _sys; _C = _os.path.dirname(_os.path.abspath(__file__)); _sys.path.insert(0, _os.path.abspath(_os.path.join(_C, '..', '..')))
from paths import R as _R, RAW as _RAW, DC as _DC, CN as _CN, JSTF as _JSTF, GMPR as _GMPR, cnd as _cnd, PWTX   # release: repository-relative paths (code/paths.py)
C=_os.path.join(_DC,'')
p=pd.read_csv(C+'pwt110_hours.csv'); H=p[p.variable=='hours_total_m'].pivot(index='year',columns='iso3',values='value')
wb=pd.read_csv(C+'worldbank_gdp.csv'); U=wb[wb.variable=='NY.GDP.MKTP.CD'].pivot_table(index='year',columns='iso3',values='value'); L=wb[wb.variable=='NY.GDP.MKTP.CN'].pivot_table(index='year',columns='iso3',values='value')
dH=np.log(H).diff(); W=U.shift(1).reindex(dH.index)
for y in range(1951,1961): W.loc[y]=U.loc[1960]
big=dH.stack(); big=big[big.abs()>0.10]
rows=[]
for (y,c),v in big.items():
    w=W.loc[y].reindex(dH.columns); m=dH.loc[y].notna()&w.notna(); share=float(w.get(c,np.nan)/w[m].sum()) if c in w and pd.notna(w.get(c)) and m.get(c,False) else np.nan
    gl=float(np.log(L[c]).diff().get(y,np.nan)) if c in L else np.nan
    rows.append(dict(year=int(y),iso3=c,dlog_hours=round(float(v),3),weight=round(share,4) if share==share else None,contrib_per1000=round(float(v*share*1000),2) if share==share else None,dlog_LCU_GDP=round(gl,3) if gl==gl else None))
T=pd.DataFrame(rows).sort_values('contrib_per1000',key=lambda s:s.abs(),ascending=False); print(T.head(20).to_string())
print('DEU dlog hours 1989-1992:',dH.loc[1989:1992,'DEU'].round(3).to_dict())
print('DEU LCU GDP dlog 1989-1992:',np.log(L['DEU']).diff().loc[1989:1992].round(3).to_dict())
T.to_csv(_os.path.join(_C,'a8_pwt_breaks.csv'),index=False)
