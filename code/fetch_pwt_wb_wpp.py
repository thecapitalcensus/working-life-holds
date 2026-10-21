"""Clean PWT 11.0 hours, World Bank GDP, UN WPP 2024 population by age (working-age)."""
import pandas as pd, json, gzip
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__))); from paths import RAW, DC, PWTX   # release: repository-relative paths (paths.py)
R=_os.path.join(RAW,'')
C=_os.path.join(DC,'')
# --- PWT 11.0
d=pd.read_excel(PWTX,sheet_name='Data')
d['hours_total_m']=d.emp*d.avh
rows=[]
units={'emp':'millions of persons engaged','avh':'average annual hours worked per person engaged','hours_total_m':'millions of hours (emp*avh)','pop':'millions of persons','hc':'index','cgdpo':'mil. 2021 US$ current PPPs (output-side)','xr':'national currency per USD (market)'}
for v,u in units.items():
    t=d[['countrycode','year',v]].dropna(); t.columns=['iso3','year','value']; t['variable']=v; t['unit']=u; rows.append(t)
p=pd.concat(rows)[['iso3','year','variable','value','unit']]
p.to_csv(C+'pwt110_hours.csv',index=False)
h=p[p.variable=='hours_total_m']; print('PWT hours',h.iso3.nunique(),'countries',h.year.min(),h.year.max())
print(d.groupby('countrycode').apply(lambda g:g.hours_total_m.notna().sum()).gt(0).sum())
# --- World Bank
w=[]
for ind,u in [('NY.GDP.MKTP.CN','current LCU'),('NY.GDP.MKTP.CD','current USD')]:
    j=json.load(open(R+f'wb/{ind}.json'))[1]
    t=pd.DataFrame([{'iso3':r['countryiso3code'],'year':int(r['date']),'variable':ind,'value':r['value'],'unit':u,'wb_name':r['country']['value']} for r in j if r['value'] is not None])
    w.append(t)
w=pd.concat(w)
cs=json.load(open(R+'wb/countries.json'))[1]
agg={c['id'] for c in cs if c['region']['value']=='Aggregates'}
w=w[~w.iso3.isin(agg)&(w.iso3!='')]
w.to_csv(C+'worldbank_gdp.csv',index=False)
print('WB',w.groupby('variable').agg(c=('iso3','nunique'),y0=('year','min'),y1=('year','max')))
# --- UN WPP
u=pd.read_csv(R+'unwpp/WPP2024_PopulationByAge5GroupSex_Medium.csv.gz',compression='gzip',low_memory=False,encoding='utf-8-sig')
u=u[u.ISO3_code.notna()&(u.LocTypeName=='Country/Area')]
u['a0']=u.AgeGrpStart
def agg_(lo,hi,name):
    s=u[(u.AgeGrpStart>=lo)&(u.AgeGrpStart<hi)].groupby(['ISO3_code','Time']).PopTotal.sum().reset_index()
    s['variable']=name; return s
tot=u.groupby(['ISO3_code','Time']).PopTotal.sum().reset_index(); tot['variable']='pop_total'
out=pd.concat([agg_(20,65,'pop_20_64'),agg_(15,65,'pop_15_64'),agg_(65,201,'pop_65plus'),tot])
out.columns=['iso3','year','value','variable']; out['value']=out.value; out['unit']='thousands of persons (medium variant, mid-year; years>=2024 are projections)'
out[['iso3','year','variable','value','unit']].to_csv(C+'unwpp2024_population_workingage.csv',index=False)
print('WPP',out.iso3.nunique(),out.year.min(),out.year.max())
