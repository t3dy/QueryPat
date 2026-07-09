#!/usr/bin/env python3
"""Merge rewritten work summaries into works/<slug>.json.
Reads *.works.json patch files (JSON arrays of {slug, card_summary, page_summary})
and replaces those two fields per work. Idempotent; reports any slug not found or
any summary that still looks like the old boilerplate."""
import json, os, sys, glob, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKS = os.path.join(ROOT, "site", "public", "data", "works")
BOILER = re.compile(r"canonical works record|single archive manifestation", re.I)


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.environ.get("SCRATCH", ""), "works")
    files = sorted(glob.glob(os.path.join(src, "*.works.json")))
    if not files:
        sys.exit(f"No *.works.json in {src}")
    applied, missing, still_boiler = 0, [], []
    for f in files:
        patches = json.load(open(f, encoding="utf-8"))
        for p in patches:
            slug = p.get("slug")
            target = os.path.join(WORKS, f"{slug}.json")
            if not os.path.exists(target):
                missing.append(slug)
                continue
            d = json.load(open(target, encoding="utf-8"))
            if p.get("card_summary"):
                d["card_summary"] = p["card_summary"].strip()
            if p.get("page_summary"):
                d["page_summary"] = p["page_summary"].strip()
            if BOILER.search((d.get("card_summary") or "") + " " + (d.get("page_summary") or "")):
                still_boiler.append(slug)
            json.dump(d, open(target, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
            applied += 1
    print(f"Applied {applied} work-summary rewrites.")
    if missing:
        print(f"  [!] slugs not found: {missing}")
    if still_boiler:
        print(f"  [!] still boilerplate after merge: {still_boiler}")


if __name__ == "__main__":
    main()
