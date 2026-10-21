"""Clean Fed Z.1 B.101 (S1M.b csv from Fed z1_csv_files.zip; ids = FRED BOGZ1<code>), cross-check against FRED keyless CSV where FRED serves the id."""
import pandas as pd, urllib.request, io
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__))); from paths import RAW, DC, PWTX   # release: repository-relative paths (paths.py)
R=_os.path.join(RAW,'fred_z1','')
C=_os.path.join(DC,'')
d=pd.read_csv(R+'fed_zip/csv/S1M_b.csv')
names={}
for line in open(R+'fed_zip/data_dictionary/S1M_b.txt',encoding='utf-8-sig'):
    p=line.rstrip('\n').split('\t')
    if len(p)>=5 and p[0].endswith('.Q'): names[p[0]]=(p[1].strip(),p[4].strip())
keep=['FL152000005','LM152010005','LM155035005','LM155035015','LM155111005','LM155012605','FL154090005','FL153020005','FL153030005','LM153030505','LM154022005','LM153061105','LM153064105','LM153081115','FL153034005','LM153064205','LM153064705','LM153064505','FL153040005','FL153050005','FL153090005','FL154190005','FL154135005','FL153165105','FL153166000','FL152090005','FL155035065','FL155035066']
rows=[]
for k in keep:
    c=k+'.Q'
    if c not in d: print('missing',c); continue
    s=d[['date',c]].dropna(); s.columns=['period','value']
    s['series_id']=c; s['fred_id']='BOGZ1'+k+'Q'; s['label']=names[c][0]; s['unit']=names[c][1][:60]
    rows.append(s)
o=pd.concat(rows); o['iso3']='USA'
o['year']=o.period.str[:4].astype(int); o['freq']=o.period.apply(lambda x:'Q' if 'Q' in x and x[-2:]!='Q4' or True else 'A')
o[['iso3','period','year','series_id','fred_id','label','value','unit']].to_csv(C+'us_z1_b101_households.csv',index=False)
print(o.groupby('series_id').agg(p0=('period','min'),p1=('period','max'),n=('value','size')).to_string())
# cross-check vs FRED (HTTP) for ids that FRED serves
chk={'TNWBSHNO':'FL152090005.Q','TABSHNO':'FL152000005.Q','TFAABSHNO':'FL154090005.Q','TLBSHNO':'FL154190005.Q','HMLBSHNO':'FL153165105.Q','HNOMFSA':'LM153064205.Q','BOGZ1LM152010005Q':'LM152010005.Q','BOGZ1LM153064705Q':'LM153064705.Q'}
for fid,c in chk.items():
    f=pd.read_csv(R+fid+'.csv'); f.columns=['date','v']; f['period']=pd.PeriodIndex(f.date,freq='Q').strftime('%Y:Q%q')
    m=f.merge(d[['date',c]].rename(columns={'date':'period'}),on='period').dropna()
    print(fid,c,len(m),'maxabsdiff',(m.v-m[c]).abs().max())
