"""Clean Eurostat nasa_10_pens1 (+pens2) and GDP; Eurostat geo codes -> ISO3."""
import pandas as pd
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__))); from paths import RAW, DC, PWTX   # release: repository-relative paths (paths.py)
B=_os.path.join(RAW,'eurostat','')
C=_os.path.join(DC,'')
iso={'AT':'AUT','BE':'BEL','BG':'BGR','CH':'CHE','CY':'CYP','CZ':'CZE','DE':'DEU','DK':'DNK','EE':'EST','EL':'GRC','ES':'ESP','FI':'FIN','FR':'FRA','HR':'HRV','HU':'HUN','IE':'IRL','IS':'ISL','IT':'ITA','LT':'LTU','LU':'LUX','LV':'LVA','MT':'MLT','NL':'NLD','NO':'NOR','PL':'POL','PT':'PRT','RO':'ROU','SE':'SWE','SI':'SVN','SK':'SVK','UK':'GBR'}
lab={'S1P':'All pension schemes (core and non-core)','S12P':'Private pension schemes','S12PC':'Private DC schemes','S12PB':'Private DB schemes','S12PBI':'DB schemes for gov employees run by financial corporations','S13PC':'General government DC (core)','S13PBI':'Gov-employee DB schemes in general government (core accounts)','S13PBX':'Gov-employee DB schemes in general government (not in core accounts)','S13PS':'Social security pension schemes (PAYG, not in core accounts)','S14R':'Counterpart: resident households','S14NR':'Counterpart: non-resident households','S1PF':'Funded entitlements','S13PU':'Unfunded entitlements'}
out=[]
for n in ['nasa_10_pens1','nasa_10_pens2']:
    d=pd.read_csv(B+n+'.csv',low_memory=False)
    d['dataset']=n
    if 'sector' not in d: d['sector']=''
    out.append(d)
d=pd.concat(out)
d['iso3']=d.geo.map(iso)
d['scheme_label']=d.penscheme.map(lab)
t=d[['iso3','geo','TIME_PERIOD','dataset','penscheme','scheme_label','sector','na_item','unit','OBS_VALUE','OBS_FLAG']]
t.columns=['iso3','eurostat_geo','year','dataset','scheme','scheme_label','sector','variable','unit','value','flag']
t.to_csv(C+'eurostat_pension_entitlements_all.csv',index=False)
e=t[(t.variable.isin(['F63_LE','F63_LS']))&(t.dataset=='nasa_10_pens1')&(t.unit.isin(['MIO_EUR','MIO_NAC','PC_GDP']))]
e.to_csv(C+'eurostat_pension_entitlements_F63.csv',index=False)
g=pd.read_csv(B+'nama_10_gdp.csv')
g=g[['geo','TIME_PERIOD','OBS_VALUE']]; g['iso3']=g.geo.map(iso); g=g.dropna(subset=['iso3'])
g.assign(variable='B1GQ',unit='MIO_EUR')[['iso3','TIME_PERIOD','variable','unit','OBS_VALUE']].rename(columns={'TIME_PERIOD':'year','OBS_VALUE':'value'}).to_csv(C+'eurostat_gdp_current_meur.csv',index=False)
x=e[(e.variable=='F63_LE')&(e.unit=='MIO_EUR')]
print(x.groupby('scheme').agg(c=('iso3','nunique'),yrs=('year',lambda s:sorted(set(s)))))
print(x.iso3.isna().sum())
