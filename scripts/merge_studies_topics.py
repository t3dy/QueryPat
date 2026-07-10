#!/usr/bin/env python3
"""Merge written studies-topic prose into topic files.
Reads *.studies.json (arrays of {slug, definition, pkd_relevance, in_the_fiction,
in_the_exegesis, intellectual_background, scholarly_debate}); sets those fields
on the matching studies/*/topics/<slug>.json. Idempotent."""
import json, os, sys, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ROOT, "site", "public", "data", "studies")
FIELDS = ["definition", "pkd_relevance", "in_the_fiction", "in_the_exegesis",
          "intellectual_background", "scholarly_debate"]
def find(slug):
    hits = glob.glob(os.path.join(BASE, "*", "topics", f"{slug}.json"))
    return hits[0] if hits else None
def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "."
    files = sorted(glob.glob(os.path.join(src, "*.studies.json")))
    applied = 0; miss = []
    for f in files:
        for p in json.load(open(f, encoding="utf-8")):
            t = find(p.get("slug"))
            if not t: miss.append(p.get("slug")); continue
            d = json.load(open(t, encoding="utf-8"))
            for k in FIELDS:
                if p.get(k): d[k] = p[k].strip()
            json.dump(d, open(t, "w", encoding="utf-8"), indent=2, ensure_ascii=False); applied += 1
    print(f"applied {applied} topic write-ups" + (f"; MISSING {miss}" if miss else ""))
if __name__ == "__main__": main()
