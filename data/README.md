# data/ — inputs you obtain yourself

Nothing in this folder is redistributed. Put these files here (or point the environment variables in `code/paths.py` elsewhere):

| File | Source | How |
|---|---|---|
| `JSTdatasetR6.xlsx` | Jordà–Schularick–Taylor Macrohistory Database, release 6 | https://www.macrohistory.net/database/ — download after accepting its CC BY-NC-SA 4.0 terms and save the R6 Excel workbook under this name, or set `CC_JST_XLSX` to its path. Needed by `build_housing.py`, `build_housing_ext.py`, `build_extras.py`, `build_life.py` and four of the checks. The SHA-256 of the copy the note used is in `MANIFEST.md`. |
| `raw/…` | OECD, Eurostat, Federal Reserve, World Bank, UN | Only needed to re-run the cleaning scripts `code/fetch_*.py`; the cleaned extracts they produce are shipped in `inputs/clean/`. URLs are in `inputs/SOURCES.md`, expected file names and checksums in `inputs/raw_downloads_sha256.txt`. Unzip the Fed file to `raw/fred_z1/fed_zip/csv/` and `raw/fred_z1/fed_zip/data_dictionary/`. |
