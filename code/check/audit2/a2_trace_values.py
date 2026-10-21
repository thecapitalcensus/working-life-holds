"""Audit 2: trace individual values raw -> clean (-> output) across all sources."""
import pandas as pd, numpy as np, json, gzip
import os as _os, sys as _sys; _C = _os.path.dirname(_os.path.abspath(__file__)); _sys.path.insert(0, _os.path.abspath(_os.path.join(_C, '..', '..')))
from paths import R as _R, RAW as _RAW, DC as _DC, CN as _CN, JSTF as _JSTF, GMPR as _GMPR, cnd as _cnd, PWTX   # release: repository-relative paths (code/paths.py)
B=_os.path.join(_R,''); R=_os.path.join(_RAW,''); C=_os.path.join(_DC,''); O=B+'output/'
rows=[]
def rec(src,item,raw,clean,note=''):
    rel=np.nan if (raw is None or clean is None or raw==0) else clean/raw-1
    rows.append(dict(source=src,item=item,raw=raw,clean=clean,rel_diff=rel,note=note))
# --- OECD HPI
h=pd.read_csv(R+'oecd_hpi/an_house_prices.csv',low_memory=False); hc=pd.read_csv(C+'oecd_house_prices.csv',low_memory=False)
for c,m,f,p in [('USA','HPI','A','2020'),('JPN','RPI','A','2010'),('DEU','HPI_RPI','A','2020'),('GBR','HPI','Q','2025-Q2')]:
    r=h[(h.REF_AREA==c)&(h.MEASURE==m)&(h.FREQ==f)&(h.TIME_PERIOD.astype(str)==p)].OBS_VALUE.iloc[0]
    k=hc[(hc.iso3==c)&(hc.variable==m)&(hc.freq==f)&(hc.period.astype(str)==p)].value.iloc[0]; rec('OECD HPI',f'{c} {m} {f} {p}',r,k)
# 2015=100 check: annual mean of 2015 = 100?
a=hc[(hc.freq=='A')&(hc.variable.isin(['HPI','RPI','HPI_RPI']))&(hc.period.astype(str)=='2015')]
rows.append(dict(source='OECD HPI',item='2015 annual value, all areas: min/max',raw=a.value.min(),clean=a.value.max(),note='should be 100'))
q=hc[(hc.freq=='Q')&(hc.variable=='HPI')&(hc.iso3=='USA')&hc.period.str.startswith('2020')].value.mean()
rec('OECD HPI','USA HPI 2020 annual vs mean of quarters',q,hc[(hc.freq=='A')&(hc.variable=='HPI')&(hc.iso3=='USA')&(hc.period.astype(str)=='2020')].value.iloc[0])
# --- T720
f=pd.read_csv(R+'oecd_bs/t720r_a_hh_xdc.csv',low_memory=False); fc=pd.read_csv(C+'oecd_hh_financial_bs.csv',low_memory=False)
def fr(c,s,e,i,y,mat=('_Z','T')):
    x=f[(f.REF_AREA==c)&(f.SECTOR==s)&(f.ACCOUNTING_ENTRY==e)&(f.INSTR_ASSET==i)&(f.TIME_PERIOD==y)&f.MATURITY.isin(mat)&(f.CURRENCY_DENOM=='_T')]; assert len(x)==1,(c,i,len(x)); return float(x.OBS_VALUE.iloc[0])
def fcl(c,s,e,i,y):
    x=fc[(fc.iso3==c)&(fc.sector==s)&(fc.entry==e)&(fc.instrument==i)&(fc.year==y)&fc.maturity.isin(['_Z','T'])&(fc.currency_denom=='_T')]; assert len(x)==1; return float(x.value.iloc[0])
for c,s,e,i,y in [('USA','S1M','A','F',2023),('JPN','S1M','A','F2',2023),('DEU','S1M','L','F',2023),('FRA','S1M','N','BF90',2023),('SWE','S1M','A','F5',2023)]:
    rec('OECD T720',f'{c} {s} {e} {i} {y}',fr(c,s,e,i,y),fcl(c,s,e,i,y))
liab=f[(f.ACCOUNTING_ENTRY=='L')&(f.INSTR_ASSET=='F')]; rows.append(dict(source='OECD T720',item='liabilities F: share of negative values',raw=float((liab.OBS_VALUE<0).mean()),clean=None,note='sign convention: liabilities positive'))
rec('OECD T720','FRA BF90 vs F(A)-F(L) 2023',fr('FRA','S1M','A','F',2023)-fr('FRA','S1M','L','F',2023),fr('FRA','S1M','N','BF90',2023))
# S1M vs S14 gap (NPISH share)
rec('OECD T720','DEU F assets S14 vs S1M 2023',fr('DEU','S1M','A','F',2023),fr('DEU','S14','A','F',2023),'S14/S1M-1 = NPISH share')
# --- 9B
n=pd.read_csv(R+'oecd_bs/table9b_s14_s1m.csv',low_memory=False); nc=pd.read_csv(C+'oecd_hh_nonfinancial_bs.csv',low_memory=False)
for c,i,y in [('USA','N111N',2023),('ESP','N211N',2023),('JPN','N111N',2023)]:
    r=float(n[(n.REF_AREA==c)&(n.SECTOR=='S1M')&(n.INSTR_ASSET==i)&(n.TIME_PERIOD==y)].OBS_VALUE.iloc[0]); k=float(nc[(nc.iso3==c)&(nc.sector=='S1M')&(nc.instrument==i)&(nc.year==y)].value.iloc[0]); rec('OECD 9B',f'{c} S1M {i} {y}',r,k)
# --- Z.1
z=pd.read_csv(C+'us_z1_b101_households.csv')
def zc(s,p): return float(z[(z.series_id==s)&(z.period==p)].value.iloc[0])
for fid,s in [('TNWBSHNO','FL152090005.Q'),('HNOREMV','LM155035005.Q'),('TLBSHNO','FL154190005.Q')]:
    ff=pd.read_csv(R+f'fred_z1/{fid}.csv'); ff.columns=['d','v']; ff['p']=pd.PeriodIndex(ff.d,freq='Q').strftime('%Y:Q%q')
    for p in ['2023:Q4',ff.p.iloc[-1]]:
        rec('Fed Z.1',f'{fid}={s} {p}',float(ff[ff.p==p].v.iloc[0]),zc(s,p))
# OECD USA vs Z.1, financial assets 2023 (both millions USD)
rec('OECD vs Z.1','USA financial assets 2023: OECD T720 S1M vs Z.1 FL154090005 Q4',fr('USA','S1M','A','F',2023),zc('FL154090005.Q','2023:Q4'))
rec('OECD vs Z.1','USA liabilities 2023: OECD vs Z.1 FL154190005',fr('USA','S1M','L','F',2023),zc('FL154190005.Q','2023:Q4'))
# --- Eurostat
e=pd.read_csv(R+'eurostat/nasa_10_pens1.csv'); ec=pd.read_csv(C+'eurostat_pension_entitlements_F63.csv')
dup=ec.duplicated(['iso3','year','scheme','variable','unit']).sum(); rows.append(dict(source='Eurostat',item='duplicate keys in F63 clean',raw=float(dup),clean=None))
for g,iso,sch,u in [('DE','DEU','S13PS','MIO_EUR'),('DE','DEU','S1P','MIO_EUR'),('FR','FRA','S1P','PC_GDP'),('SE','SWE','S13PS','MIO_NAC'),('PL','POL','S13PS','MIO_NAC')]:
    r=float(e[(e.geo==g)&(e.penscheme==sch)&(e.na_item=='F63_LE')&(e.unit==u)&(e.TIME_PERIOD==2021)].OBS_VALUE.iloc[0]); k=float(ec[(ec.iso3==iso)&(ec.scheme==sch)&(ec.variable=='F63_LE')&(ec.unit==u)&(ec.year==2021)].value.iloc[0]); rec('Eurostat T29',f'{g} {sch} F63_LE {u} 2021',r,k)
pe=pd.read_csv(O+'balance/table_payg_entitlements_2021.csv',index_col=0)
# MIO_NAC/GDP(WB LCU) vs Eurostat PC_GDP for S13PS (code computes its own %GDP)
for g,iso in [('DE','DEU'),('SE','SWE'),('PL','POL'),('FR','FRA'),('DK','DNK')]:
    x=e[(e.geo==g)&(e.penscheme=='S13PS')&(e.na_item=='F63_LE')&(e.unit=='MIO_EUR')&(e.TIME_PERIOD==2021)]
    gg=pd.read_csv(R+'eurostat/nama_10_gdp.csv'); gg=float(gg[(gg.geo==g)&(gg.TIME_PERIOD==2021)].OBS_VALUE.iloc[0])
    rec('Eurostat vs output',f'{iso} S13PS %GDP 2021: Eurostat MIO_EUR / Eurostat GDP vs output (MIO_NAC / WB LCU GDP)',float(x.OBS_VALUE.iloc[0])/gg*100,float(pe.loc[iso,'S13PS_pct_gdp']))
eg=pd.read_csv(R+'eurostat/nama_10_gdp.csv'); egc=pd.read_csv(C+'eurostat_gdp_current_meur.csv')
rec('Eurostat GDP','DE B1GQ CP_MEUR 2021',float(eg[(eg.geo=='DE')&(eg.TIME_PERIOD==2021)].OBS_VALUE.iloc[0]),float(egc[(egc.iso3=='DEU')&(egc.year==2021)].value.iloc[0]))
# --- PWT
pw=pd.read_excel(PWTX,sheet_name='Data'); pc=pd.read_csv(C+'pwt110_hours.csv')
for c,y,v in [('JPN',2019,'emp'),('JPN',2019,'avh'),('USA',2023,'hours_total_m'),('DEU',1976,'avh')]:
    r=float((pw.emp*pw.avh if v=='hours_total_m' else pw[v])[(pw.countrycode==c)&(pw.year==y)].iloc[0]); k=float(pc[(pc.iso3==c)&(pc.year==y)&(pc.variable==v)].value.iloc[0]); rec('PWT 11.0',f'{c} {v} {y}',r,k)
# --- World Bank
for ind,c,y in [('NY.GDP.MKTP.CD','USA',2023),('NY.GDP.MKTP.CN','JPN',2023),('NY.GDP.MKTP.CN','DEU',1995)]:
    j=json.load(open(R+f'wb/{ind}.json'))[1]; r=[x['value'] for x in j if x['countryiso3code']==c and x['date']==str(y)][0]
    wc=pd.read_csv(C+'worldbank_gdp.csv'); k=float(wc[(wc.iso3==c)&(wc.year==y)&(wc.variable==ind)].value.iloc[0]); rec('World Bank',f'{c} {ind} {y}',r,k)
wc=pd.read_csv(C+'worldbank_gdp.csv'); rows.append(dict(source='World Bank',item='duplicate (iso3,year,variable)',raw=float(wc.duplicated(['iso3','year','variable']).sum()),clean=None))
# --- UN WPP
u=pd.read_csv(R+'unwpp/WPP2024_PopulationByAge5GroupSex_Medium.csv.gz',compression='gzip',low_memory=False,encoding='utf-8-sig')
uc=pd.read_csv(C+'unwpp2024_population_workingage.csv')
for c,y in [('JPN',2023),('USA',2050)]:
    x=u[(u.ISO3_code==c)&(u.Time==y)&(u.LocTypeName=='Country/Area')]; r=float(x[(x.AgeGrpStart>=20)&(x.AgeGrpStart<65)].PopTotal.sum())
    k=float(uc[(uc.iso3==c)&(uc.year==y)&(uc.variable=='pop_20_64')].value.iloc[0]); rec('UN WPP',f'{c} pop 20-64 {y} (thousands)',r,k)
    rows.append(dict(source='UN WPP',item=f'{c} {y} rows per age group (dup check)',raw=float(x.groupby('AgeGrpStart').size().max()),clean=None,note='should be 1'))
T=pd.DataFrame(rows); pd.set_option('display.width',250); pd.set_option('display.max_colwidth',90)
print(T.to_string()); T.to_csv(_os.path.join(_C,'a2_trace_values.csv'),index=False)
