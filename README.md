# What a Working Life Holds

Code and derived data for the fourth Capital Census research note:

> Nakanishi, K. (2026). *What a Working Life Holds: The Home, the Pension and the Portfolio in Hours of the World's Work.* Research note, v1.0, 21 October 2026. SSRN 7646578 (https://ssrn.com/abstract=7646578; DOI 10.2139/ssrn.7646578 on approval). Site version: https://thecapitalcensus.github.io/household.html

The note takes the *world hour* (nominal GDP per hour worked across 43 countries) to the household. A household holds
four kinds of claim: a home, a pension, a portfolio and some deposits. The note asks how many hours of work each claim
earns a year, and what a working life ends up holding. It measures the home in 16 countries from 1950 to 2025
(Macrohistory Database, extended to 2025 with OECD house price and rent indices), the household balance sheet in 31 OECD
countries and the United States since 1952 (Fed Z.1), the pay-as-you-go pension claim (Eurostat Table 29) and its
implicit return (growth of total hours worked, Penn World Table; UN projections), and 476 stylised working lives
(16 countries, cohorts entering work 1950–1980) that rent and invest or buy a home. The analysis is exploratory and was
not pre-registered (`docs/PLAN.md` was written before any result was computed).

It builds on the first three notes in the series:

- Nakanishi (2026a), *Owning the Market as It Is*, doi:10.2139/ssrn.7394599 (the GMP index)
- Nakanishi (2026b), *Measuring Assets in Hours of the World's Work*, doi:10.2139/ssrn.7445203 (the world hour)
- Nakanishi (2026d), *What the World's Capital Earns and Pays*, doi:10.2139/ssrn.7515699 (code and data: https://github.com/thecapitalcensus/capital-earns-and-pays)

## Layout

| Path | Content |
|---|---|
| `code/paths.py` | Every input location, with environment-variable overrides (table below); defaults are this repository's folders. |
| `code/fetch_*.py` | Clean the raw public downloads (`data/raw/`) into `inputs/clean/`. Not needed to reproduce the note: the cleaned files are shipped. |
| `code/build_housing.py` | Section 4: housing in world and national hours, 1951–2020; housing beside the GMP and the other Macrohistory claims; the note-3 rent-weight correction. |
| `code/build_housing_ext.py` | Section 4 extension to 2021–2025 with OECD indices; JST vs OECD cross-check. Runs `build_housing.py` first (in its own namespace). |
| `code/build_extras.py` | Two measurement variants of the housing headline and the labour-share series (`output/housing/extras.json`). |
| `code/build_balance.py` | Sections 5–6: balance sheets (OECD, Z.1), PAYG entitlements (Eurostat), hours growth and population projections. |
| `code/build_life.py` | Section 7: the stylised lives, decompositions and robustness grid (design fixed in `docs/SPEC_life.md`). |
| `code/build_paper.py` | Fills `paper_template.html` with all tables and every number quoted in the text; writes `output/paper/household.html`, `numbers_in_text.json`, Figure 5. |
| `code/check/` | Independent checks of Sections 4–7, written before reading the builders, with their reports (`CHECK_4_6.md`, `CHECK_life.md`, `REVIEW_paper.md`) and the second audit (`audit2/`: `AUDIT_code_data.md`, `AUDIT_paper.md`, `VERIFY_fixes.md`, scripts and outputs). |
| `paper_template.html` | The note's text with placeholders. |
| `docs/` | Design records: `PLAN.md` (plan, before results), `SPEC_life.md` (life-cycle design), `OUTLINE.md`, `SPEC_note3_inputs.md` (note-3 conventions reused). |
| `inputs/clean/` | Cleaned public data: OECD, Eurostat, Fed Z.1, PWT 11.0, World Bank, UN WPP 2024. `inputs/SOURCES.md` gives URLs, coverage, quirks and terms. |
| `inputs/raw/pwt/pwt110.xlsx` | Penn World Table 11.0 workbook (read by `build_extras.py` for the labour share). |
| `inputs/engine/`, `inputs/world_hour/`, `inputs/wb_pwt/` | The GMP monthly return (CC-GMP TR), the world hour (CC-WH) and the World Bank / PWT-via-FRED copies, exactly as shipped in the note-3 release. |
| `inputs/public/` | Other public copies: World Bank LCU GDP and labour force, BIS exchange rates, FRED US GDP and nonfarm-business hours. |
| `inputs/note3/` | Note 3's `gmp_components_monthly.csv` (GMP cash and valuation components), from the note-3 release. |
| `output/` | `housing/`, `balance/`, `life/`: every derived table (`*.csv`), figure (`*.png`), build log (`build_log.json`: input checksums, identity checks, headline values) and results note (`RESULTS_*.md`); `paper/`: the note as HTML and PDF. |
| `MANIFEST.md` | SHA-256 of every file here, of every input recorded in the build logs, and of the raw downloads not included (`make_manifest.py`). |

## How to reproduce

Requirements: Python 3.10+ with `pandas`, `numpy`, `matplotlib`, `openpyxl` (checked with Python 3.12, pandas 3.0.2,
numpy 2.4.6, matplotlib 3.10.9, openpyxl 3.1.5). No network access is needed.

1. Download the Macrohistory Database R6 workbook (below) and save it as `data/JSTdatasetR6.xlsx`, or set
   `CC_JST_XLSX=/path/to/JSTdatasetR6.xlsx`.
2. Run, from the repository root, in this order:

```bash
python3 code/build_housing.py       # output/housing/ (1951-2020)
python3 code/build_housing_ext.py   # output/housing/ (2021-2025 extension; re-runs build_housing.py internally)
python3 code/build_extras.py        # output/housing/extras.json
python3 code/build_balance.py       # output/balance/
python3 code/build_life.py          # output/life/
python3 code/build_paper.py         # output/paper/household.html, numbers_in_text.json, img/
```

The whole sequence takes about a minute. The PDF was rendered from the HTML with headless Chrome:
`"Google Chrome" --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf=output/paper/household.pdf file://$PWD/output/paper/household.html`.

Optional: `python3 code/fetch_*.py` re-cleans the raw downloads (put them under `data/raw/` first; see `data/README.md`).
Refreshed downloads will differ from the vintage the note used, which is identified by the checksums in `MANIFEST.md`.
The checks in `code/check/` run in place (`python3 code/check/check_housing.py`, …); `check_balance.py` fetches US GDP
from FRED, `audit2/a1_raw_dims.py` and `a2_trace_values.py` need the raw downloads, and `audit2/a5_housing_timing.py`
re-executes the housing builders and so rewrites `output/housing/` (run it on a copy).

Environment variables (all optional): `CC_JST_XLSX`, `CC_CLEAN_DIR`, `CC_RAW_DIR`, `CC_PWT_XLSX`, `GMP_ENGINE_DIR`,
`CC_WH_DIR`, `CC_WB_PWT_DIR`, `CC_PUBLIC_DIR`, `CC_NOTE3_DIR`, `CC_SITE_CSS` (see `code/paths.py`).

### Reproduction check (21 October 2026)

A copy of this repository was run from scratch (all generated outputs deleted first) with the network disabled and
`CC_JST_XLSX` pointing at the R6 workbook. Of the 83 regenerated files (CSV, PNG, JSON, HTML), 78 are byte-identical to the shipped ones. The other five, the
build logs (`output/{housing,balance,life}/build_log.json`, `output/housing/extras.json`) and `household.html`, differ only in two checksum lines: the world-hour files shipped here (and in the note-3 release)
keep only the `gdph` column, while the author's working copies, whose checksums the note prints in Appendix B, also hold
the other yardsticks. The `gdph` values are identical, and so is every number. With `CC_WH_DIR` pointing at the
author's full files, every output including `household.html` is byte-identical. `household.pdf` and the `RESULTS_*.md`
notes are not regenerated by the pipeline.

Differences from the code that produced v1.0: input paths are read from `code/paths.py` instead of being hard-coded, the
build logs key inputs with `label()` (which reproduces the original labels), `build_paper.py` keeps the shipped
`style.css` instead of copying the site's, and the check scripts use the same paths. No numerical logic was changed.

## Inputs, and what is not included

Included: the cleaned public data and copies listed above, under their sources' terms (`LICENSE.md`, class 6).

Not included:

1. **The Macrohistory Database workbook** (`JSTdatasetR6.xlsx`). Jordà–Schularick–Taylor Macrohistory Database,
   release 6: https://www.macrohistory.net/database/ (CC BY-NC-SA 4.0; accept the terms there and cite it as required).
   Expected at `data/JSTdatasetR6.xlsx` (or `CC_JST_XLSX`); its SHA-256 is in `MANIFEST.md`
   (`c1bb91fe…` in the build logs under the label `gmp_income/data/JSTdatasetR6.xlsx`).
2. **The raw downloads** behind `inputs/clean/` (OECD Table 720 and 9B and house price CSVs, Eurostat SDMX files, the
   Fed Z.1 zip and FRED Z.1 copies, World Bank JSON, UN WPP CSV): their terms allow redistribution, but they are large
   (about 170 MB) and the cleaned extracts carry everything the pipeline uses. Their URLs are in `inputs/SOURCES.md`
   and their checksums in `inputs/raw_downloads_sha256.txt`. The PWT workbook is the exception and is included.
3. **The author's full world-hour files** (`world_yardsticks_usd.csv` with all six yardsticks): only the `gdph` column is
   used, and the note-3 release's `gdph`-only copies are shipped instead (see the reproduction check).
4. **The superseded first version of the life-cycle builder** (`build_life_v1_anchor2000.py`, replaced when the design
   was corrected once after seeing results; Section 7). Its anchor is kept as a variant in `build_life.py`
   (`life_cohorts_anchor2000.csv`, `summary_anchor2000.csv`).

No source used by the note forbids redistribution; nothing was excluded on those grounds. No index-vendor or proprietary
data is used.

Two check outputs are records of the audit as it ran and are not refreshed: `code/check/audit2/a6_balance_checks.json`
predates fix W5 in `audit2/AUDIT_code_data.md` (it shows the pre-fix PAYG median of 271.5% of GDP; re-running gives
270.2, the value in the note).

## Licence

See `LICENSE.md`. In short: code MIT; the note's text (`paper_template.html`, `output/paper/household.{html,pdf}`)
CC BY-NC-ND 4.0; every series that depends on the Macrohistory Database (all housing and life outputs, the claim
comparisons, the national hour before 1961, note 3's GMP components) CC BY-NC-SA 4.0; the CC-GMP TR and CC-WH inputs,
and the balance-sheet series in world hours that use no Macrohistory data, CC BY-NC 4.0; balance-sheet, PAYG and
population series built only from public data CC BY 4.0; copies of public data under their sources' terms.

## Citation

```
Nakanishi, K. (2026). What a Working Life Holds: The Home, the Pension and the Portfolio in Hours of the
World's Work. Research note, v1.0, 21 October 2026. SSRN 7646578 (https://ssrn.com/abstract=7646578; DOI 10.2139/ssrn.7646578 on approval).
Code and data: https://github.com/thecapitalcensus/working-life-holds
```

A machine-readable version is in `CITATION.cff`.

## Contact

Keisuke Nakanishi, independent researcher — thecapitalcensus@gmail.com — ORCID 0009-0000-3780-9450
