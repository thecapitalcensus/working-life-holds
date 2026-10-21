"""Independent check: national-hours housing net (USA, JPN, DEU) and PAYG implicit return (hours growth)."""
import numpy as np, pandas as pd
import check_housing as ch
import os as _os, sys as _sys; _C = _os.path.dirname(_os.path.abspath(__file__)); _sys.path.insert(0, _os.path.abspath(_os.path.join(_C, '..')))
from paths import R as _R, RAW as _RAW, DC as _DC, CN as _CN, JSTF as _JSTF, GMPR as _GMPR, cnd as _cnd, PWTX   # release: repository-relative paths (code/paths.py)
H = _R
wb = pd.read_csv(f'{_DC}/worldbank_gdp.csv')
lcu = wb[wb.variable == 'NY.GDP.MKTP.CN'].pivot(index='year', columns='iso3', values='value')
usd = wb[wb.variable == 'NY.GDP.MKTP.CD'].pivot(index='year', columns='iso3', values='value')
pw = pd.read_csv(f'{_DC}/pwt110_hours.csv')
hrs = pw[pw.variable == 'hours_total_m'].pivot(index='year', columns='iso3', values='value')
emp = pw[pw.variable == 'emp'].pivot(index='year', columns='iso3', values='value')

print('National-hours housing, 1976-2020, per 1,000 h (hour = WB LCU GDP / PWT hours; calendar-year growth)')
for c in ['USA', 'JPN', 'DEU']:
    nh = lcu[c] / hrs[c]
    need = np.log(nh).diff().loc[1976:2020].mean() * 1000
    d = ch.j[(ch.j.iso == c) & ch.j.year.between(1976, 2020)].set_index('year')
    tot = np.log1p(d.housing_tr).mean() * 1000
    cash = np.log1p(d.housing_rent_rtn).mean() * 1000
    val = (-(np.log(d.housing_rent_yd) - np.log(d.ryd_l))).mean() * 1000
    # alt: JST gdp per head for the hour (cross-check of definitions)
    jj = ch.j[ch.j.iso == c].set_index('year')
    needp = np.log(jj.gdp / jj['pop']).diff().loc[1976:2020].mean() * 1000
    print(f'{c}: total {tot:.1f} cash {cash:.1f} val {val:.1f} needed {need:.1f} net {tot-need:.1f} '
          f'net_ex_val {tot-need-val:.1f} | needed via JST gdp/head {needp:.1f}')

# PAYG: GDP-weighted growth of total hours
g = np.log(hrs).diff()
def world_hours(y0, y1, countries=None, lag=1):
    out = {}
    for y in range(y0, y1 + 1):
        gy = g.loc[y].dropna()
        if countries is not None: gy = gy[gy.index.isin(countries)]
        wy = max(y - lag, 1960)
        w = usd.loc[wy].reindex(gy.index).dropna(); gy = gy[w.index]
        out[y] = (w * gy).sum() / w.sum(); out[(y, 'n')] = len(gy)
    s = pd.Series({k: v for k, v in out.items() if not isinstance(k, tuple)})
    return s.mean() * 1000, int(np.mean([v for k, v in out.items() if isinstance(k, tuple)]))
for lag in (0, 1):
    print(f'PAYG weights lag{lag}: 1951-2023 all', world_hours(1951, 2023, lag=lag),
          '1976-2020 all', world_hours(1976, 2020, lag=lag), ' JST16 1976-2020', world_hours(1976, 2020, ch.C16, lag=lag))
for c in ['DEU', 'JPN', 'FRA', 'ITA', 'USA']:
    print(c, '1976-2020 hours growth per 1,000:', round(g[c].loc[1976:2020].mean() * 1000, 1),
          ' 1951-2023:', round(g[c].loc[1951:2023].mean() * 1000, 1))
