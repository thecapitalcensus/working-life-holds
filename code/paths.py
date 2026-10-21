# -*- coding: utf-8 -*-
"""Release version: every input location in one place.  Defaults are this repository's folders; environment variables
override them (all optional except that the Macrohistory workbook must exist somewhere, see README).

  CC_JST_XLSX     Macrohistory Database R6 workbook          default data/JSTdatasetR6.xlsx (not redistributed)
  CC_CLEAN_DIR    cleaned public data (fetch_*.py output)    default inputs/clean
  CC_RAW_DIR      raw downloads read by fetch_*.py           default data/raw (not redistributed)
  CC_PWT_XLSX     Penn World Table 11.0 workbook             default inputs/raw/pwt/pwt110.xlsx
  GMP_ENGINE_DIR  folder with four_series_returns_corrected.csv (CC-GMP TR)          default inputs/engine
  CC_WH_DIR       folder with the world hour (CC-WH) files                           default inputs/world_hour
  CC_WB_PWT_DIR   folder with World Bank / PWT-via-FRED copies (as in note 3)        default inputs/wb_pwt
  CC_PUBLIC_DIR   folder with the other public copies (World Bank, BIS, FRED)        default inputs/public
  CC_NOTE3_DIR    folder with note 3's gmp_components_monthly.csv                    default inputs/note3
  CC_SITE_CSS     style sheet copied next to the HTML                                default output/paper/style.css (kept)

Build logs key each input by the path it had in the author's working tree (the labels printed in the note's
Appendix B, e.g. 'composite_numeraire/output/world_yardsticks_usd.csv'); label() maps a file here to that label."""
import os

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # repository root
B = R
IN = os.path.join(R, "inputs")
JSTF = os.environ.get("CC_JST_XLSX", os.path.join(R, "data", "JSTdatasetR6.xlsx"))
DC = os.environ.get("CC_CLEAN_DIR", os.path.join(IN, "clean"))
RAW = os.environ.get("CC_RAW_DIR", os.path.join(R, "data", "raw"))
PWTX = os.environ.get("CC_PWT_XLSX", os.path.join(IN, "raw", "pwt", "pwt110.xlsx"))
ENG = os.environ.get("GMP_ENGINE_DIR", os.path.join(IN, "engine")); GMPR = os.path.join(ENG, "four_series_returns_corrected.csv")
CN = os.environ.get("CC_WH_DIR", os.path.join(IN, "world_hour"))
CND_DIRS = [os.environ.get("CC_WB_PWT_DIR", os.path.join(IN, "wb_pwt")), os.environ.get("CC_PUBLIC_DIR", os.path.join(IN, "public"))]
N3 = os.environ.get("CC_NOTE3_DIR", os.path.join(IN, "note3")); GMPC = os.path.join(N3, "gmp_components_monthly.csv")
SITE_CSS = os.environ.get("CC_SITE_CSS", os.path.join(R, "output", "paper", "style.css"))


def cnd(f):
    """A public copy (World Bank, PWT via FRED, BIS, FRED) from the first folder in CND_DIRS that holds it."""
    for d in CND_DIRS:
        if os.path.exists(os.path.join(d, f)): return os.path.join(d, f)
    return os.path.join(CND_DIRS[0], f)


def label(p):
    """The input's label in the build logs (its path in the author's working tree, relative to the home folder)."""
    p = os.path.abspath(p); d, f = os.path.dirname(p), os.path.basename(p)
    fixed = {os.path.abspath(JSTF): "gmp_income/data/JSTdatasetR6.xlsx", os.path.abspath(GMPC): "gmp_income/output_v2/gmp_components_monthly.csv",
             os.path.abspath(GMPR): "gmp_bt_b61/four_series_returns_corrected.csv", os.path.abspath(PWTX): "gmp_household/data/raw/pwt/pwt110.xlsx"}
    if p in fixed: return fixed[p]
    if d == os.path.abspath(CN): return "composite_numeraire/output/" + f
    if d in [os.path.abspath(x) for x in CND_DIRS]: return "composite_numeraire/data/" + f
    if d == os.path.abspath(DC): return "gmp_household/data/clean/" + f
    if p.startswith(R + os.sep): return "gmp_household/" + os.path.relpath(p, R).replace(os.sep, "/")
    return p
