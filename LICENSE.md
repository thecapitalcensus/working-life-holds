# Licences

This repository combines material under several licences. Each file falls into exactly one of the classes below. Where a
folder is not split, the whole folder is in one class.

| Class | Licence | Files |
|---|---|---|
| 1 | MIT | all `*.py` (`code/`, `code/check/`, `code/check/audit2/`, `make_manifest.py`) |
| 2 | CC BY-NC-ND 4.0 | the note's text: `paper_template.html`, `output/paper/household.html`, `output/paper/household.pdf`, `output/paper/style.css`, `code/check/audit2/key_contexts.txt` |
| 3 | CC BY-NC-SA 4.0 | everything derived from the Macrohistory Database (list below), the design records in `docs/`, the check reports `code/check/*.md` and `code/check/audit2/*.md`, the results notes `output/*/RESULTS_*.md`, and note 3's `inputs/note3/gmp_components_monthly.csv` |
| 4 | CC BY-NC 4.0 | the author's input series `inputs/engine/` (CC-GMP TR) and `inputs/world_hour/` (CC-WH), and outputs that depend on them but not on the Macrohistory Database (list below) |
| 5 | CC BY 4.0 | outputs that depend only on public data whose terms allow it (list below), and the repository's own documentation (`README.md`, `LICENSE.md`, `CITATION.cff`, `MANIFEST.md`, `data/README.md`, `inputs/SOURCES.md`, `inputs/raw_downloads_sha256.txt`, `.gitignore`) |
| 6 | the source's own terms | copies of third-party public data in `inputs/clean/`, `inputs/raw/`, `inputs/wb_pwt/`, `inputs/public/`, `code/check/fx/`, `output/housing/ext_inputs/` |

## 1. Code — MIT

Copyright (c) 2026 Keisuke Nakanishi

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## 2. The note's text — CC BY-NC-ND 4.0

https://creativecommons.org/licenses/by-nc-nd/4.0/ — Any SSRN posting of the note is governed by SSRN's terms, with
copyright retained by the author. The figures embedded in the note (`output/paper/img/`) keep the licence of the series
they show (classes 3 and 5 below).

## 3. Series derived from the Macrohistory Database — CC BY-NC-SA 4.0

https://creativecommons.org/licenses/by-nc-sa/4.0/

The housing returns and rent yields, the equity, bond and bill returns, the national hour before 1961 and the stylised
lives of Section 7 are built from the Jordà–Schularick–Taylor Macrohistory Database (release 6), which is licensed
CC BY-NC-SA 4.0. Under its share-alike condition, series derived from it are released only on the same terms and are not
offered under any commercial licence. Note 3's GMP cash and valuation components (`inputs/note3/gmp_components_monthly.csv`)
also depend on it (the world dividend–price ratio), so everything built from them is in this class too.

Files in this class:

- `output/housing/` — every file except `world_hour_growth_annual.csv` (class 4) and `ext_inputs/` (class 6), i.e. all
  housing tables and figures, `gmp_annual.csv`, `table_gmp_world_hours.csv`, `extras.json`, `build_log.json`.
- `output/life/` — every file.
- `output/balance/` — `table_claims_hour_return_with_payg.csv`, `table_balance_sheet_hour_return_by_country.csv`,
  `fig3_four_claims_payg_decades.png`, `build_log.json`, `RESULTS_balance.md`.
- `output/paper/numbers_in_text.json`; `output/paper/img/h_fig1.png`, `h_fig2.png`, `h_fig5.png`, `h_fig6.png`, `h_fig7.png`.
- `code/check/life_check_mine_*.csv`, `code/check/audit2/a5_housing_timing.json`, `a6_balance_checks.json`, `a7_valuation_variants.json`.

Use of the Macrohistory Database requires the following citations:

- Jordà, Ò., Schularick, M. and Taylor, A. M. (2017). "Macrofinancial History and the New Business Cycle Facts." In *NBER Macroeconomics Annual 2016*, vol. 31, University of Chicago Press.
- Jordà, Ò., Knoll, K., Kuvshinov, D., Schularick, M. and Taylor, A. M. (2019). "The Rate of Return on Everything, 1870–2015." *Quarterly Journal of Economics*, 134(3), 1225–1298.

## 4. The author's input series and series that depend on them — CC BY-NC 4.0

https://creativecommons.org/licenses/by-nc/4.0/ — the same terms as the CC-GMP TR and CC-WH series on https://thecapitalcensus.github.io.

- `inputs/engine/four_series_returns_corrected.csv` (first column is the CC-GMP TR monthly return) and `inputs/world_hour/*` (the CC-WH world hour), copied unchanged from the note-3 release (https://github.com/thecapitalcensus/capital-earns-and-pays).
- Outputs expressed in world hours that use no Macrohistory data: `output/housing/world_hour_growth_annual.csv`;
  `output/balance/balance_sheet_oecd_s1m_country_year.csv`, `table_composition_latest_2023.csv`,
  `timepath_nw_world_hours_by_country.csv`, `us_z1_balance_sheet_1952_2026.csv`.

## 5. Outputs from public data only — CC BY 4.0

https://creativecommons.org/licenses/by/4.0/

These depend only on OECD, Eurostat, Federal Reserve Z.1, Penn World Table, World Bank, UN World Population Prospects,
BIS and FRED data, all of which allow reuse with attribution. Please also credit those sources (`inputs/SOURCES.md`).

- `output/balance/`: `table_payg_entitlements_all_years.csv`, `table_payg_entitlements_2021.csv`, `payg_world_annual_per_1000h.csv`,
  `table_payg_return_by_decade_world.csv`, `table_payg_return_by_country.csv`, `table_payg_return_by_country_decade.csv`,
  `table_pop2064_projection.csv`, `timepath_balanced_panel_gdp_weighted.csv`, `timepath_nw_years_of_work_by_country.csv`,
  `fig1_composition_latest.png`, `fig2_us_composition_years.png`.
- `output/paper/img/h_fig3.png`, `h_fig4.png` (copies of the two balance-sheet figures).
- `code/check/audit2/a2_trace_values.csv`, `a8_pwt_breaks.csv`.

## 6. Copies of third-party public data — their sources' terms

Included as convenience copies; the retrieval date is 21 October 2026 unless noted, and checksums are in `MANIFEST.md`.

| Path | Source | Terms |
|---|---|---|
| `inputs/clean/oecd_house_prices.csv`, `oecd_hh_financial_bs.csv`, `oecd_hh_nonfinancial_bs.csv` | OECD (analytical house price indicators; Tables 720 and 9B) | OECD Terms and Conditions, reuse with attribution (https://www.oecd.org/en/about/terms-conditions.html) |
| `inputs/clean/eurostat_*.csv` | Eurostat (nasa_10_pens1/2, nama_10_gdp) | CC BY 4.0, © European Union |
| `inputs/clean/us_z1_b101_households.csv` | Board of Governors of the Federal Reserve System, Z.1 B.101 | public data, attribution |
| `inputs/clean/pwt110_hours.csv`, `inputs/raw/pwt/pwt110.xlsx` | Penn World Table 11.0, Groningen Growth and Development Centre (doi:10.34894/FABVLR) | CC BY 4.0 |
| `inputs/clean/worldbank_gdp.csv`, `inputs/public/wb_ngdp_lcu.json`, `inputs/public/wb_lf.json`, `inputs/wb_pwt/wb_*.json` | World Bank, World Development Indicators | CC BY 4.0 |
| `inputs/wb_pwt/EMPENG*.csv`, `AVHWPE*.csv` | Penn World Table via FRED (as in the note-3 release; retrieved September 2026) | CC BY 4.0 |
| `inputs/clean/unwpp2024_population_workingage.csv` | United Nations, World Population Prospects 2024 | CC BY 3.0 IGO |
| `inputs/public/bis_xru.csv` | Bank for International Settlements, exchange rates (WS_XRU) | BIS terms of use, reuse with attribution |
| `inputs/public/GDP.csv` (BEA), `inputs/public/HOANBS.csv` (BLS), `output/housing/ext_inputs/CUUR0000SEHA.csv` (BLS CPI rent), `code/check/fx/EX*.csv` (Federal Reserve H.10) | via FRED, Federal Reserve Bank of St. Louis | public-domain US government data, attribution |

Not included at all: the Macrohistory workbook and the raw downloads behind `inputs/clean/` (see README).
