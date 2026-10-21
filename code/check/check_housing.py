"""Independent check of note-4 section 4 (housing in world hours) -- written without reading builders' code.
Usage: python3 check_housing.py
"""
import numpy as np, pandas as pd
import os as _os, sys as _sys; _C = _os.path.dirname(_os.path.abspath(__file__)); _sys.path.insert(0, _os.path.abspath(_os.path.join(_C, '..')))
from paths import R as _R, RAW as _RAW, DC as _DC, CN as _CN, JSTF as _JSTF, GMPR as _GMPR, cnd as _cnd, PWTX   # release: repository-relative paths (code/paths.py)
H = _R
j = pd.read_excel(_JSTF)
C16 = ['AUS','BEL','CHE','DEU','DNK','ESP','FIN','FRA','GBR','ITA','JPN','NLD','NOR','PRT','SWE','USA']
j = j[j.iso.isin(C16)].sort_values(['iso','year']).copy()
wb = pd.read_csv(f'{_DC}/worldbank_gdp.csv')
usd = wb[wb.variable=='NY.GDP.MKTP.CD'].pivot(index='year', columns='iso3', values='value')[C16]

# --- per-country USD returns
j['xr_l'] = j.groupby('iso').xrusd.shift(1)
j['ryd_l'] = j.groupby('iso').housing_rent_yd.shift(1)
j['fx'] = j.xr_l / j.xrusd                         # USD per LCU growth, Dec-to-Dec (xrusd end-year)
j['tr_usd'] = (1 + j.housing_tr) * j.fx - 1
j['l_tot'] = np.log1p(j.tr_usd)
j['l_cash'] = np.log1p(j.housing_rent_rtn)
j['l_val'] = -(np.log(j.housing_rent_yd) - np.log(j.ryd_l))

# world hour, December values
g = pd.read_csv(f'{_CN}/world_yardsticks_usd.csv', index_col=0, parse_dates=True)['gdph']
dec = g[g.index.month == 12]; dec.index = dec.index.year
need = np.log(dec).diff()

def world(y0, y1, wlag=0, agg='simple'):
    rows = []
    for y in range(y0, y1 + 1):
        d = j[j.year == y].set_index('iso')
        d = d[d.l_tot.notna()]
        w = usd.loc[y - wlag, d.index]; w = w / w.sum()
        if agg == 'simple':   # portfolio: log of weighted simple return; cash as weighted simple rent return
            tot = np.log((w * (1 + d.tr_usd)).sum())
            cash = np.log1p((w * d.housing_rent_rtn).sum())
            # valuation: -dlog of weighted rent yield, same weights both years (pure yield change)
            val = -(np.log((w * d.housing_rent_yd).sum()) - np.log((w * d.ryd_l).sum()))
        else:                 # weighted mean of country logs
            tot = (w * d.l_tot).sum(); cash = (w * d.l_cash).sum(); val = (w * d.l_val).sum()
        rows.append(dict(year=y, total=tot, cash=cash, val=val, need=need.loc[y]))
    a = pd.DataFrame(rows).set_index('year')
    m = a.mean() * 1000
    out = dict(total=m.total, cash=m.cash, price=m.total - m.cash, valuation=m.val,
               price_ex_val=m.total - m.cash - m.val, needed=m.need,
               net=m.total - m.need, net_ex_val=m.total - m.need - m.val)
    return pd.Series(out).round(1), a

if __name__ == '__main__':
    print('coverage 1976-2020 by country (n obs with housing_tr):')
    print(j[(j.year >= 1976) & (j.year <= 2020)].groupby('iso').housing_tr.count().to_dict())
    print('identity rent_rtn vs rent_yd*(1+capgain): max abs',
          (j.housing_rent_rtn - j.housing_rent_yd * (1 + j.housing_capgain)).abs()[j.year >= 1951].max())
    print('identity rent_rtn vs rent_yd_{t-1}: max abs',
          (j.housing_rent_rtn - j.ryd_l).abs()[j.year >= 1951].max())
    res = {}
    for lag in (0, 1):
        for agg in ('simple', 'logmean'):
            s, a = world(1976, 2020, lag, agg); res[f'lag{lag}_{agg}'] = s
    print(pd.DataFrame(res))
    # GMP total/net in world hours
    gm = pd.read_csv(_GMPR, index_col=0, parse_dates=True).iloc[:, 0]
    ly = np.log1p(gm).groupby(gm.index.year).sum()
    for y1 in (2020,):
        t = ly.loc[1976:y1].mean() * 1000; n = need.loc[1976:y1].mean() * 1000
        print(f'GMP 1976-{y1}: total {t:.1f} needed {n:.1f} net {t-n:.1f}')
    print('needed 1976-2025 (Dec-to-Dec):', round(need.loc[1976:2025].mean() * 1000, 1))
    print('needed by period', {p: round(need.loc[a:b].mean()*1000, 1) for p, (a, b) in
          {'76-81': (1976, 1981), '82-00': (1982, 2000), '01-20': (2001, 2020), '21-25': (2021, 2025)}.items()})
    # GMP to 2025
    t = ly.loc[1976:2025].mean()*1000; n = need.loc[1976:2025].mean()*1000
    print(f'GMP 1976-2025: total {t:.1f} net {t-n:.1f}')
    # sub-periods housing, main variant
    for p, (a, b) in {'76-81': (1976, 1981), '82-00': (1982, 2000), '01-20': (2001, 2020)}.items():
        print(p, world(a, b, 0, 'simple')[0][['total', 'cash', 'valuation', 'net', 'net_ex_val']].to_dict())
    # Rent-yield weighting, note 3 sec 7 check
    print('\nRent yield % (weighted): year, gdp/xrusd (note-3 method), WB USD GDP, equal')
    for y in (1976, 2000, 2020):
        d = j[(j.year == y) & j.housing_rent_yd.notna()].set_index('iso')
        w3 = d.gdp / d.xrusd; w3 /= w3.sum()
        wu = usd.loc[y, d.index]; wu /= wu.sum()
        print(y, round((w3 * d.housing_rent_yd).sum() * 100, 2), round((wu * d.housing_rent_yd).sum() * 100, 2),
              round(d.housing_rent_yd.mean() * 100, 2), ' note3 top weights:', w3.sort_values(ascending=False).head(3).round(2).to_dict(),
              ' JPN/USA/DEU w3:', w3[['JPN', 'USA', 'DEU']].round(4).to_dict())
