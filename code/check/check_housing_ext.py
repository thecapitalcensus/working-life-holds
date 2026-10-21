"""Independent check of the 2021-25 extension (OECD HPI/RPI chained on JST 2020). FX: FRED monthly averages, December."""
import numpy as np, pandas as pd
import check_housing as ch
import os as _os, sys as _sys; _C = _os.path.dirname(_os.path.abspath(__file__)); _sys.path.insert(0, _os.path.abspath(_os.path.join(_C, '..')))
from paths import R as _R, RAW as _RAW, DC as _DC, CN as _CN, JSTF as _JSTF, GMPR as _GMPR, cnd as _cnd, PWTX   # release: repository-relative paths (code/paths.py)
H = _R
o = pd.read_csv(f'{_DC}/oecd_house_prices.csv')
EUR = ['BEL','DEU','ESP','FIN','FRA','ITA','NLD','PRT']
fxs = {'JPN': ('EXJPUS', -1), 'GBR': ('EXUSUK', 1), 'CHE': ('EXSZUS', -1), 'DNK': ('EXDNUS', -1),
       'NOR': ('EXNOUS', -1), 'SWE': ('EXSDUS', -1), 'AUS': ('EXUSAL', 1), **{c: ('EXUSEU', 1) for c in EUR}}
def usd_per_lcu_dec(c):
    if c == 'USA': return pd.Series(1.0, index=range(2020, 2026))
    s, p = fxs[c]; f = pd.read_csv(f'{_C}/fx/{s}.csv', parse_dates=[0], index_col=0).iloc[:, 0]
    f = f[f.index.month == 12]; f.index = f.index.year
    return f ** p
def ann(c, v):
    a = o[(o.iso3 == c) & (o.variable == v) & (o.freq == 'A')].set_index('period').value
    a.index = a.index.astype(int)
    q = o[(o.iso3 == c) & (o.variable == v) & (o.freq == 'Q')]
    if 2025 not in a.index or pd.isna(a.get(2025)):
        q25 = q[q.period.str.startswith('2025')].value
        if len(q25): a.loc[2025] = q25.mean()   # partial-year average (AUS)
    return a
cpirent = pd.read_csv(f'{H}/output/housing/ext_inputs/CUUR0000SEHA.csv', parse_dates=[0], index_col=0).iloc[:, 0]
cpirent = cpirent.groupby(cpirent.index.year).mean()
j = ch.j; rows = []
for c in ch.C16:
    hp = ann(c, 'HPI'); rp = ann(c, 'RPI')
    if c == 'USA' and pd.isna(rp.get(2025)):
        rp.loc[2025] = rp.loc[2024] * cpirent.loc[2025] / cpirent.loc[2024]
    fx = usd_per_lcu_dec(c)
    y20 = j[(j.iso == c) & (j.year == 2020)].housing_rent_yd.iloc[0]
    yd_prev = y20
    for y in range(2021, 2026):
        cg = hp[y] / hp[y - 1] - 1
        yd = y20 * (rp[y] / rp[2020]) / (hp[y] / hp[2020])
        rr = yd * (1 + cg)
        tr = cg + rr
        tr_usd = (1 + tr) * fx[y] / fx[y - 1] - 1
        rows.append(dict(iso=c, year=y, housing_capgain=cg, housing_rent_yd=yd, housing_rent_rtn=rr,
                         housing_tr=tr, tr_usd=tr_usd, l_tot=np.log1p(tr_usd), l_cash=np.log1p(rr),
                         l_val=-np.log(yd / yd_prev), ryd_l=yd_prev))
        yd_prev = yd
ext = pd.DataFrame(rows)
ch.j = pd.concat([j, ext], ignore_index=True)
if __name__ == '__main__':
    for lag in (0, 1):
        for agg in ('simple', 'logmean'):
            r = {p: ch.world(a, b, lag, agg)[0] for p, (a, b) in {'2021-25': (2021, 2025), '1976-2025': (1976, 2025)}.items()}
            print(f'lag{lag} {agg}'); print(pd.DataFrame(r).T[['total', 'cash', 'valuation', 'needed', 'net', 'net_ex_val']])
    s, a = ch.world(2025, 2025, 1, 'simple')
    w = ch.usd.loc[2025]; w = w / w.sum()
    d = ch.j[ch.j.year == 2025].set_index('iso')
    print('rent yield 2025 (USD GDP 2025 weights) %:', round((w * d.housing_rent_yd).sum() * 100, 2))
