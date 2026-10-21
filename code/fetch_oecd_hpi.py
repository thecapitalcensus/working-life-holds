"""Clean OECD analytical house price indicators (raw csv fetched by curl; see SOURCES.md)."""
import pandas as pd
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__))); from paths import RAW, DC, PWTX   # release: repository-relative paths (paths.py)
R=_os.path.join(RAW,'oecd_hpi','an_house_prices.csv')
O=_os.path.join(DC,'oecd_house_prices.csv')
d=pd.read_csv(R,low_memory=False)
o=d[['REF_AREA','FREQ','TIME_PERIOD','MEASURE','Measure','UNIT_MEASURE','BASE_PER','ADJUSTMENT','OBS_VALUE']].copy()
o.columns=['iso3','freq','period','variable','variable_label','unit','base_period','adjustment','value']
o.to_csv(O,index=False)
print(o.groupby(['variable','freq']).agg(n=('value','size'),ctry=('iso3','nunique')))
for v in ['HPI','RPI','HPI_RPI']:
    for f in 'QA':
        s=o[(o.variable==v)&(o.freq==f)]
        print(v,f,s.period.min(),s.period.max(), s.iso3.nunique())
pri='AUS BEL CAN CHE DEU DNK ESP FIN FRA GBR IRL ITA JPN NLD NOR PRT SWE USA'.split()
s=o[(o.variable=='HPI')&(o.freq=='A')]
print(s.groupby('iso3').period.agg(['min','max']).loc[[c for c in pri if c in set(s.iso3)]])
print(set(pri)-set(s.iso3))
