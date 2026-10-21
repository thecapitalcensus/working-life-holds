"""Clean OECD household balance sheets: Table 720 (non-consolidated financial, S14 & S1M) and Table 9B (non-financial)."""
import pandas as pd
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__))); from paths import RAW, DC, PWTX   # release: repository-relative paths (paths.py)
B=_os.path.join(RAW,'oecd_bs','')
C=_os.path.join(DC,'')
f=pd.read_csv(B+'t720r_a_hh_xdc.csv',low_memory=False)
f=f[(f.UNIT_MEASURE=='XDC')&(f.COUNTERPART_SECTOR=='S1')]
print(f.groupby(['COUNTERPART_AREA']).size().head(10))
f=f[f.COUNTERPART_AREA=='W'] if 'W' in set(f.COUNTERPART_AREA) else f
o=f[['REF_AREA','SECTOR','ACCOUNTING_ENTRY','INSTR_ASSET','Financial instruments and non-financial assets','MATURITY','CURRENCY_DENOM','TIME_PERIOD','OBS_VALUE','UNIT_MULT','CURRENCY','OBS_STATUS']].copy()
o.columns=['iso3','sector','entry','instrument','instrument_label','maturity','currency_denom','year','value','unit_mult_exp','currency','obs_status']
o['unit']='millions of national currency (current prices, end-year stock)'
o['table']='T0720 non-consolidated'
o.to_csv(C+'oecd_hh_financial_bs.csv',index=False)
print(o.groupby('sector').agg(n=('value','size'),ctry=('iso3','nunique'),y0=('year','min'),y1=('year','max')))
n=pd.read_csv(B+'table9b_s14_s1m.csv',low_memory=False)
p=n[['REF_AREA','SECTOR','INSTR_ASSET','Financial instruments and non-financial assets','TIME_PERIOD','OBS_VALUE','OBS_STATUS']].copy()
p.columns=['iso3','sector','instrument','instrument_label','year','value','obs_status']
p['currency']=n['CURRENCY'] if 'CURRENCY' in n else ''
p['unit']='millions of national currency (current prices, end-year stock, net)'
p['table']='T2600 / Table 9B'
p.to_csv(C+'oecd_hh_nonfinancial_bs.csv',index=False)
print(p.groupby('sector').agg(n=('value','size'),ctry=('iso3','nunique'),y0=('year','min'),y1=('year','max')))
# coverage of key items per country for S1M preferred else S14
key={'dwell':'N111N','land_dw':'N21111N','land':'N211N','nonfin_total':'NN'}
for k,v in key.items():
    s=p[p.instrument==v]; print(k, s.groupby('iso3').year.agg(['min','max']).T.to_dict()) if False else print(k, s.iso3.nunique(), 'countries')
fk=['F','F2','F3','F4','F5','F511','F512','F52','F6','F62','F63','BF90']
for k in fk:
    s=f[f.INSTR_ASSET==k]; print(k,s.REF_AREA.nunique(),'ctry', s.TIME_PERIOD.min(), s.TIME_PERIOD.max(), set(s.ACCOUNTING_ENTRY))
