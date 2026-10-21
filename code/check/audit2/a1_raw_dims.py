"""Audit 2: dimension values in raw OECD files (filters, unit multipliers)."""
import pandas as pd, sys
import os as _os, sys as _sys; _C = _os.path.dirname(_os.path.abspath(__file__)); _sys.path.insert(0, _os.path.abspath(_os.path.join(_C, '..', '..')))
from paths import R as _R, RAW as _RAW, DC as _DC, CN as _CN, JSTF as _JSTF, GMPR as _GMPR, cnd as _cnd, PWTX   # release: repository-relative paths (code/paths.py)
R=_os.path.join(_RAW,'')
f=pd.read_csv(R+'oecd_bs/t720r_a_hh_xdc.csv',low_memory=False)
for c in ['CONSOLIDATION','TRANSACTION','UNIT_MEASURE','UNIT_MULT','VALUATION','PRICE_BASE','COUNTERPART_AREA','COUNTERPART_SECTOR','CURRENCY_DENOM','MATURITY','ACCOUNTING_ENTRY','SECTOR']:
    print('T720',c,f[c].value_counts(dropna=False).to_dict())
print('T720 UNIT_MULT by country', f.groupby('REF_AREA').UNIT_MULT.unique().apply(list).to_dict())
print('T720 CURRENCY by country (sample)', f.groupby('REF_AREA').CURRENCY.unique().apply(list).to_dict())
n=pd.read_csv(R+'oecd_bs/table9b_s14_s1m.csv',low_memory=False)
for c in ['ACCOUNTING_ENTRY','TRANSACTION','UNIT_MEASURE','UNIT_MULT','VALUATION','PRICE_BASE','TRANSFORMATION','COUNTERPART_AREA','CONSOLIDATION','EXPENDITURE','REF_YEAR_PRICE','SECTOR']:
    print('9B',c,n[c].value_counts(dropna=False).to_dict())
print('9B UNIT_MULT by country', n.groupby('REF_AREA').UNIT_MULT.unique().apply(list).to_dict())
print('9B CURRENCY by country', n.groupby('REF_AREA').CURRENCY.unique().apply(list).to_dict())
h=pd.read_csv(R+'oecd_hpi/an_house_prices.csv',low_memory=False)
for c in ['UNIT_MEASURE','BASE_PER','ADJUSTMENT','UNIT_MULT','FREQ']:
    print('HPI',c,h[c].value_counts(dropna=False).to_dict())
d=h.duplicated(['REF_AREA','FREQ','MEASURE','TIME_PERIOD']).sum(); print('HPI dup keys',d)
