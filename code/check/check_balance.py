"""Independent check: OECD 2023 composition, US Z.1 NW/GDP 1952 vs 2026, Eurostat PAYG 2021."""
import numpy as np, pandas as pd, io, urllib.request
import os as _os, sys as _sys; _C = _os.path.dirname(_os.path.abspath(__file__)); _sys.path.insert(0, _os.path.abspath(_os.path.join(_C, '..')))
from paths import R as _R, RAW as _RAW, DC as _DC, CN as _CN, JSTF as _JSTF, GMPR as _GMPR, cnd as _cnd, PWTX   # release: repository-relative paths (code/paths.py)
H = _R
f = pd.read_csv(f'{_DC}/oecd_hh_financial_bs.csv')
f = f[(f.sector == 'S1M') & f.maturity.isin(['_Z', 'T']) & (f.currency_denom == '_T')]
nf = pd.read_csv(f'{_DC}/oecd_hh_nonfinancial_bs.csv'); nf = nf[nf.sector == 'S1M']
wb = pd.read_csv(f'{_DC}/worldbank_gdp.csv')
usd = wb[wb.variable == 'NY.GDP.MKTP.CD'].pivot(index='year', columns='iso3', values='value')
lcu = wb[wb.variable == 'NY.GDP.MKTP.CN'].pivot(index='year', columns='iso3', values='value')

def comp(y):
    a = f[(f.entry == 'A') & (f.year == y)].pivot_table(index='iso3', columns='instrument', values='value', aggfunc='first')
    l = f[(f.entry == 'L') & (f.year == y) & (f.instrument == 'F')].set_index('iso3').value
    n = nf[nf.year == y].pivot_table(index='iso3', columns='instrument', values='value', aggfunc='first')
    df = pd.DataFrame({'F': a['F'], 'F2': a.get('F2'), 'F3': a.get('F3'), 'F5': a['F5'], 'F6': a['F6'],
                       'dw': n.get('N111N'), 'land': n.get('N211N')}).join(l.rename('L'))
    df = df[df.F.notna() & df.dw.notna()]
    df['land0'] = df.land.fillna(0)
    df['gross'] = df.F + df.dw + df.land0
    s = pd.DataFrame({'dwellings_land': (df.dw + df.land0) / df.gross,
                      'F6': df.F6 / df.gross, 'F5': df.F5 / df.gross,
                      'F2F3': (df.F2.fillna(0) + df.F3.fillna(0)) / df.gross,
                      'liab': df.L / df.gross}) * 100
    s['nw_gdp'] = (df.gross - df.L) / lcu.loc[y].reindex(df.index)
    w = usd.loc[y].reindex(s.index); w = w / w.sum()
    return s, w, df
s, w, df = comp(2023)
print('2023 countries', len(s), sorted(s.index))
print('GDP-weighted:', (s.drop(columns='nw_gdp').mul(w, axis=0).sum()).round(1).to_dict())
print('median     :', s.median().round(1).to_dict())

# US Z.1
z = pd.read_csv(f'{_DC}/us_z1_b101_households.csv')
nw = z[z.series_id.str.startswith('FL152090005')].set_index('period').value
gdp = pd.read_csv(io.StringIO(urllib.request.urlopen('https://fred.stlouisfed.org/graph/fredgraph.csv?id=GDP').read().decode()),
                  parse_dates=[0], index_col=0).iloc[:, 0]
ga = gdp.groupby(gdp.index.year).mean()
print('US NW/GDP 1952Q4 / GDP1952:', round(nw['1952:Q4'] / ga[1952], 2),
      '| 2026Q2 / mean GDP 2026H1:', round(nw['2026:Q2'] / ga[2026], 2), ' (last GDP obs', gdp.index[-1].date(), ')')

# Eurostat PAYG 2021
e = pd.read_csv(f'{_DC}/eurostat_pension_entitlements_F63.csv')
e = e[(e.year == 2021) & (e.variable == 'F63_LE') & (e.dataset == 'nasa_10_pens1')]
ps = e[(e.scheme == 'S13PS')]
pg = ps[ps.unit == 'MIO_NAC'].set_index('iso3').value / lcu.loc[2021].reindex(ps[ps.unit=='MIO_NAC'].iso3).values * 1e8  # % of WB LCU GDP
print('S13PS % GDP 2021: n', pg.notna().sum(), 'median', pg.median(), 'min', pg.idxmin(), pg.min(), 'max', pg.idxmax(), pg.max())
pn = ps[ps.unit == 'MIO_NAC'].set_index('iso3').value
s21, w21, df21 = comp(2021)
nw21 = (df21.gross - df21.L)
r = (pn / nw21 * 100).dropna()
print('S13PS % household NW (S1M, OECD) 2021: n', len(r), 'median', round(r.median(), 1),
      {c: round(r[c]) for c in ['BEL', 'DEU', 'FRA', 'ITA', 'ESP', 'FIN', 'POL', 'ROU'] if c in r})

# Variant B (after reading builder code): gross assets also include other non-financial assets
def comp_b(y):
    s, w, df = comp(y)
    n = nf[nf.year == y].pivot_table(index='iso3', columns='instrument', values='value', aggfunc='first').reindex(df.index)
    prod = n['N11N'] + n.get('N12N', 0).fillna(0) + n.get('N13N', 0).fillna(0)
    nn = n.get('NN')
    oth = (prod - df.dw).fillna(0) + (n['N2N'] - df.land).where(n['N2N'].notna() & df.land.notna(), 0).fillna(0)
    if nn is not None: oth = (nn - df.dw - df.land0).where(nn.notna(), oth)
    g2 = df.gross + oth
    s2 = pd.DataFrame({'dwellings_land': (df.dw + df.land0) / g2, 'F6': df.F6 / g2, 'F5': df.F5 / g2,
                       'F2F3': (df.F2.fillna(0) + df.F3.fillna(0)) / g2, 'liab': df.L / g2}) * 100
    return s2, w, g2 - df.L
s2, w2, nwb = comp_b(2023)
print('B 2023 GDP-weighted:', s2.mul(w2, axis=0).sum().round(1).to_dict(), ' median:', s2.median().round(1).to_dict())
_, _, nwb21 = comp_b(2021)
rb = (pn / nwb21 * 100).dropna()
print('B S13PS % NW 2021: n', len(rb), 'median', round(rb.median(), 1),
      {c: round(rb[c]) for c in ['BEL', 'DEU', 'FRA', 'ITA', 'ESP', 'FIN', 'POL', 'ROU'] if c in rb})
