"""Audit 2: FRED PWT cache (used by build_housing national hour) vs PWT 11.0 file (used by build_balance/build_life)."""
import pandas as pd, numpy as np
import os as _os, sys as _sys; _C = _os.path.dirname(_os.path.abspath(__file__)); _sys.path.insert(0, _os.path.abspath(_os.path.join(_C, '..', '..')))
from paths import R as _R, RAW as _RAW, DC as _DC, CN as _CN, JSTF as _JSTF, GMPR as _GMPR, cnd as _cnd, PWTX   # release: repository-relative paths (code/paths.py)
CND=_os.path.join(_os.path.dirname(_cnd('wb_gdp.json')),'')
p=pd.read_csv(_os.path.join(_DC,'pwt110_hours.csv'))
I2={"AUS":"AU","BEL":"BE","CHE":"CH","DEU":"DE","DNK":"DK","ESP":"ES","FIN":"FI","FRA":"FR","GBR":"GB","ITA":"IT","JPN":"JP","NLD":"NL","NOR":"NO","PRT":"PT","SWE":"SE","USA":"US"}
out=[]
for c3,c2 in I2.items():
    def fr(s):
        x=pd.read_csv(CND+s+'.csv',index_col=0,parse_dates=True).iloc[:,0]; x.index=x.index.year; return pd.to_numeric(x,errors='coerce')
    h_f=(fr(f'EMPENG{c2}A148NRUG')*fr(f'AVHWPE{c2}A065NRUG')).dropna()
    h_p=p[(p.iso3==c3)&(p.variable=='hours_total_m')].set_index('year').value
    z=pd.concat([h_f,h_p],axis=1,keys=['fred','pwt11']).dropna()
    g=np.log(z).diff().loc[1976:2020]
    out.append(dict(c=c3,years=f'{z.index.min()}-{z.index.max()}',maxrel_level=float((z.fred/z.pwt11-1).abs().max()),mean_growth_diff_per1000_7620=float((g.fred-g.pwt11).mean()*1000)))
o=pd.DataFrame(out); print(o.to_string()); print('max abs level rel diff', o.maxrel_level.max())
