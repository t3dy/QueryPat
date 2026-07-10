#!/usr/bin/env python3
"""Repair the 37 segment JSON files broken by unescaped quotes (json_repair),
clean their ZebraPedia wiki artifacts, and re-serialize as valid indent-2 JSON.
Per-file integrity guard: the repaired evidence_excerpts count must equal the
raw 'matched_alias' occurrence count, else the file is left untouched."""
import json, glob, os, re
from json_repair import repair_json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEG = os.path.join(ROOT, "site", "public", "data", "segments")
LINE = re.compile(r"[^\n]*Last edit over[^\n]*")
TOK = re.compile(r"\b(?:Needs Review|Indexed)\b")
def clean(t):
    if not isinstance(t, str): return t
    t = LINE.sub("", t); t = TOK.sub("", t)
    t = re.sub(r"\n{3,}", "\n\n", t); t = re.sub(r"[ \t]{2,}", " ", t)
    return t.strip()

def main():
    repaired = skipped = 0
    for f in sorted(glob.glob(os.path.join(SEG, "*.json"))):
        raw = open(f, encoding="utf-8").read()
        try:
            json.loads(raw); continue          # already valid
        except Exception:
            pass
        try:
            d = json.loads(repair_json(raw))
        except Exception as e:
            print(f"  UNREPAIRABLE {os.path.basename(f)}: {e}"); skipped += 1; continue
        raw_excerpts = raw.count("matched_alias")
        got = len(d.get("evidence_excerpts", []) or [])
        if got != raw_excerpts:
            print(f"  SKIP {os.path.basename(f)}: excerpt count {got} != raw {raw_excerpts}")
            skipped += 1; continue
        for ev in d.get("evidence_excerpts", []) or []:
            if isinstance(ev, dict) and isinstance(ev.get("text"), str):
                ev["text"] = clean(ev["text"])
        if isinstance(d.get("concise_summary"), str):
            d["concise_summary"] = clean(d["concise_summary"])
        json.dump(d, open(f, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        # final strict validation
        json.load(open(f, encoding="utf-8"))
        repaired += 1
    print(f"repaired {repaired} files; skipped {skipped}")

if __name__ == "__main__":
    main()
