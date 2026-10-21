"""Audit 2: housing-section checks needing the builder namespace. RUN WITH HOME pointing at a scratch copy
(build_housing.py writes its outputs under $HOME/gmp_household/output on exec)."""
import os, io, json, contextlib, numpy as np, pandas as pd
import os as _os, sys as _sys; _C = _os.path.dirname(_os.path.abspath(__file__)); _sys.path.insert(0, _os.path.abspath(_os.path.join(_C, '..', '..')))
from paths import R as _R, RAW as _RAW, DC as _DC, CN as _CN, JSTF as _JSTF, GMPR as _GMPR, cnd as _cnd, PWTX   # release: repository-relative paths (code/paths.py)
HOME=_R  # release: the repository itself; run on a scratch copy (exec rewrites output/housing/)
F=_os.path.join(_R,'code','build_housing_ext.py'); NS={'__file__':F,'__name__':'x'}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(open(F).read(),F,'exec'),NS)
G=NS['G']; R={}
national=G['national']; tot_l=G['tot_l']; val=G['val']; NEED_N=G['NEED_N']; NEED_N_DEC=G['NEED_N_DEC']; HC=G['HC']
# (1) Dec-to-Dec robustness row uses 1976-2019; baseline median over the same window
R['dec_row_median_1976_2019']=float(national(tot_l,NEED_N_DEC,1976,2019)[0].median())
R['baseline_median_1976_2019']=float(national(tot_l,NEED_N,1976,2019)[0].median())
R['baseline_median_1976_2020']=float(national(tot_l,NEED_N,1976,2020)[0].median())
R['NEED_N_DEC_2020_available']=int(NEED_N_DEC.loc[2020,HC].notna().sum())
# (2) '1951-2020' label: code averages 1950-2020; is 1950 in the sample, and with which hour?
SRC=G['SRC']; R['national_hour_source_1950']=SRC.loc[1950].value_counts().to_dict(); R['national_hour_source_1951_1960']=SRC.loc[1951:1960].stack().value_counts().to_dict()
R['housing_1950_return_countries']=int((tot_l.loc[1950].notna()&NEED_N.loc[1950,HC].notna()).sum())
CL={'housing':tot_l,'equities':np.log1p(G['EQ'][HC]),'gov_bonds':np.log1p(G['BOND'][HC]),'deposits_bills':np.log1p(G['BILL'][HC])}
for k,x in CL.items():
    xx=x.where(tot_l.notna())
    p50,a50,_=national(xx,NEED_N,1950,2020); p51,a51,_=national(xx,NEED_N,1951,2020)
    R[f'{k}_gdpw_1950_2020']=round(a50,2); R[f'{k}_gdpw_1951_2020']=round(a51,2); R[f'{k}_median_1950_2020']=round(float(p50.median()),2); R[f'{k}_median_1951_2020']=round(float(p51.median()),2)
# Table 3 component method for 1951-2020
W=G['weights']; w=W(tot_l.notna()&val.notna()&NEED_N.notna()&G['W_USD'][HC].notna())
for a in (1950,1951):
    ww=w.loc[a:2020]; R[f'T3_net_{a}_2020']=round(float(((ww*tot_l.loc[a:2020]).sum(axis=1)-(ww*NEED_N[HC].loc[a:2020]).sum(axis=1)).mean()*1000),2)
# per-country 1950 vs 1951 start (Table A1 col 'Net 1951-2020')
pc50=((tot_l-NEED_N[HC]).loc[1950:2020].mean()*1000); pc51=((tot_l-NEED_N[HC]).loc[1951:2020].mean()*1000)
R['A1_net_1951col_maxabs_change_if_1951']=round(float((pc50-pc51).abs().max()),2); R['A1_net_1951col_median_1950_vs_1951']=[round(float(pc50.median()),2),round(float(pc51.median()),2)]
R['A1_first_year_used']=tot_l.loc[1950:2020].apply(lambda s:s.first_valid_index()).to_dict()
# (3) 2021-2025 chain: check identities for one country and the fills
TRx=NS['TR']; YDx=NS['YD']; HPI=NS['HPI']; RPI=NS['RPI']
c='USA'; R['USA_2021_capgain_vs_OECD']=[float(NS['CG'].loc[2021,c]),float(HPI.loc[2021,c]/HPI.loc[2020,c]-1)]
R['yd_2020_continuity_JST_vs_chain']=float((YDx.loc[2020,HC]-G['YD'].loc[2020,HC]).abs().max())
R['oecd_fills']=NS['EXT']['oecd_2025_fills']
# JST hpnom 2020 growth vs OECD 2020 annual growth (does JST look like annual-average or end-year?)
hp=G['pv']('hpnom')[HC]; j=np.log(hp).diff(); o=np.log(HPI).diff()
for lag in (0,1):
    z=pd.concat([j.loc[1990:2020].stack(),o.shift(-lag).loc[1990:2020].stack()],axis=1).dropna(); R[f'corr_JST_hp_growth_vs_OECD_annual_avg_lead{lag}']=round(float(z.corr().iloc[0,1]),3)
# (4) weights and timing of the world hour: Dec-to-Dec vs JST annual (calendar) returns -> how much does a half-year shift matter
NW=G['NEED_W']; HW=NS['HW']
R['world_net_7620_dec']=round(float((HW.total-NW).loc[1976:2020].mean()*1000),2)
R['world_net_7620_need_shift_half']=round(float((HW.total-0.5*(NW+NW.shift(1))).loc[1976:2020].mean()*1000),2)
print(json.dumps(R,indent=1,default=str))
json.dump(R,open(_os.path.join(_C,'a5_housing_timing.json'),'w'),indent=1,default=str)
# per-country A1 change
dd=(pc50-pc51).round(2).sort_values(); print('A1 per-country net (1950-2020 minus 1951-2020):',dd.to_dict())
print('NEED_N 1950 (per-capita proxy) x1000:',(NEED_N.loc[1950,HC]*1000).round(1).to_dict())
print('housing net 1950 x1000:',((tot_l-NEED_N[HC]).loc[1950]*1000).round(1).to_dict())
