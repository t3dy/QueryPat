#!/usr/bin/env python3
"""Strip leaked inline claim-IDs "(CLM_S_xxx, ...)" from studies topic/index
prose fields (same defect as the dictionary). Idempotent."""
import json, glob, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ROOT, "site", "public", "data", "studies")
PROSE = ["definition", "pkd_relevance", "in_the_fiction", "in_the_exegesis",
         "intellectual_background", "scholarly_debate", "chronology_summary",
         "contradictions_summary", "editorial_notes", "summary", "description"]
PAREN = re.compile(r"\s*\((?:CLM_[A-Za-z0-9_]+(?:\s*,\s*)?)+\)")
BARE = re.compile(r"\s*\bCLM_[A-Za-z0-9_]{6,}\b")
def clean(t):
    t = PAREN.sub("", t); t = BARE.sub("", t)
    t = re.sub(r"\s+([.;,])", r"\1", t); t = re.sub(r"[ \t]{2,}", " ", t)
    return t.strip()
def main():
    files = glob.glob(os.path.join(BASE, "**", "*.json"), recursive=True)
    nf = nfields = 0
    for f in files:
        d = json.load(open(f, encoding="utf-8"))
        if not isinstance(d, dict): continue
        touched = False
        for k in PROSE:
            v = d.get(k)
            if isinstance(v, str) and "CLM_" in v:
                nv = clean(v)
                if nv != v: d[k] = nv; nfields += 1; touched = True
        if touched:
            json.dump(d, open(f, "w", encoding="utf-8"), indent=2, ensure_ascii=False); nf += 1
    print(f"cleaned {nfields} fields in {nf} study files")
    res = sum(1 for f in files if any("CLM_" in str(json.load(open(f,encoding='utf-8')).get(k) or '') for k in PROSE))
    print("residual files with CLM:", res)
if __name__ == "__main__": main()
