# -*- coding: utf-8 -*-
"""Write MANIFEST.md: SHA-256 and size of every tracked file; every input recorded in the build logs (and whether this
repository holds a byte-identical copy); and the recorded checksums of the raw downloads that are not included."""
import hashlib, json, os, subprocess, datetime
B = os.path.dirname(os.path.abspath(__file__))
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
try: files = subprocess.check_output(["git", "ls-files"], cwd=B, text=True).split("\n")
except Exception: files = [os.path.relpath(os.path.join(r, f), B) for r, _, fs in os.walk(B) for f in fs if ".git" not in r]
files = sorted(f for f in files if f and f != "MANIFEST.md")
S = {f: sha(os.path.join(B, f)) for f in files}; BY = {}
for f, h in S.items(): BY.setdefault(h, []).append(f)
O = os.path.join(B, "output")
H = {}
for p in ["housing/build_log.json", "balance/build_log.json", "life/build_log.json", "housing/extras.json"]:
    L = json.load(open(os.path.join(O, p))); H.update(L["inputs_sha256"])
    if "extension_2021_2025" in L: H.update(L["extension_2021_2025"]["inputs_sha256"])
lines = ["# Manifest", "", f"Generated {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} by `make_manifest.py`.", "",
         f"## Files in this repository ({len(files)})", "", "| file | bytes | sha256 |", "|---|---|---|"]
lines += [f"| `{f}` | {os.path.getsize(os.path.join(B, f)):,} | `{S[f]}` |" for f in files]
lines += ["", f"## Inputs recorded in the build logs ({len(H)}; labels are paths in the author's working tree, as in Appendix B of the note)", "",
          "| label | sha256 | byte-identical copy here |", "|---|---|---|"]
for k, v in sorted(H.items()):
    here = ", ".join(f"`{x}`" for x in BY.get(v, [])) or "**not included** (see README)"
    lines.append(f"| `{k}` | `{v}` | {here} |")
RAW = os.path.join(B, "inputs", "raw_downloads_sha256.txt")
lines += ["", "## Raw downloads behind `inputs/clean/` (not included except the PWT workbook)", "", "| file | bytes | sha256 |", "|---|---|---|"]
for ln in open(RAW, encoding="utf-8"):
    if ln.startswith("#") or not ln.strip(): continue
    h, n, f = ln.split(None, 2); lines.append(f"| `{f.strip()}` | {int(n):,} | `{h}` |")
open(os.path.join(B, "MANIFEST.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n"); print(len(files), "files;", len(H), "logged inputs")
