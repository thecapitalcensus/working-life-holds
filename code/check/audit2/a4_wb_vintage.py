"""Audit 2: World Bank vintages - composite_numeraire cache (build_housing, build_extras) vs data/clean (ext, balance, life)."""
import pandas as pd, numpy as np, json
import os as _os, sys as _sys; _C = _os.path.dirname(_os.path.abspath(__file__)); _sys.path.insert(0, _os.path.abspath(_os.path.join(_C, '..', '..')))
from paths import R as _R, RAW as _RAW, DC as _DC, CN as _CN, JSTF as _JSTF, GMPR as _GMPR, cnd as _cnd, PWTX   # release: repository-relative paths (code/paths.py)
CND=None
HC=['AUS','BEL','CHE','DEU','DNK','ESP','FIN','FRA','GBR','ITA','JPN','NLD','NOR','PRT','SWE','USA']
w=pd.read_csv(_os.path.join(_DC,'worldbank_gdp.csv'))
for f,ind in [('wb_ngdp_lcu.json','NY.GDP.MKTP.CN'),('wb_gdp.json','NY.GDP.MKTP.CD')]:
    j=json.load(open(_cnd(f)))[1]
    old=pd.DataFrame([(r['countryiso3code'],int(r['date']),r['value']) for r in j if r['value'] is not None and r['countryiso3code']],columns=['c','y','v']).pivot_table(index='y',columns='c',values='v',aggfunc='first')
    new=w[w.variable==ind].pivot_table(index='year',columns='iso3',values='value')
    r=(old[HC]/new[HC]-1).loc[1960:2025]
    print(f,ind,'years old',old.index.min(),old.index.max(),'| max abs rel diff 16 ctry',float(r.abs().max().max()))
    print(r.abs().max().sort_values().tail(5).round(4).to_dict())
    gr=(np.log(old[HC]).diff()-np.log(new[HC]).diff()).loc[1976:2020]
    print(' mean growth diff 1976-2020 per 1000 by country:', (gr.mean()*1000).round(3).to_dict())
