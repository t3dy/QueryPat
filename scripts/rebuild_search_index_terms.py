#!/usr/bin/env python3
"""Refresh the term entries in search_index.json from the cleaned dictionary.
- Drop term entries whose slug is no longer in dictionary/index.json (the
  noise/duplicate terms filtered from browse).
- Replace each surviving term entry's `text` with the current definition
  (fallback card_description / full_description), truncated for the index.
Non-term entries (segment/archive/name) are untouched. Idempotent."""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "site", "public", "data")
SI = os.path.join(DATA, "search_index.json")
TERMS = os.path.join(DATA, "dictionary", "terms")

def term_text(slug):
    p = os.path.join(TERMS, f"{slug}.json")
    if not os.path.exists(p):
        return None
    d = json.load(open(p, encoding="utf-8"))
    for k in ("definition", "card_description", "full_description"):
        v = str(d.get(k) or "").strip()
        if v:
            v = re.sub(r"\s+", " ", v)
            return v[:300]
    return ""   # honest stub -> empty text

def main():
    idx = json.load(open(SI, encoding="utf-8"))
    valid = {e["slug"] for e in json.load(open(os.path.join(DATA, "dictionary", "index.json"), encoding="utf-8"))}
    out = []
    dropped = refreshed = 0
    for e in idx:
        if e.get("type") != "term":
            out.append(e); continue
        slug = e.get("slug")
        if slug not in valid:
            dropped += 1; continue
        nt = term_text(slug)
        if nt is not None and nt != e.get("text"):
            e["text"] = nt; refreshed += 1
        out.append(e)
    json.dump(out, open(SI, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"search_index: {len(idx)} -> {len(out)} entries; dropped {dropped} filtered terms; refreshed {refreshed} term texts")
    # residual junk check
    s = json.dumps(out, ensure_ascii=False)
    for pat in ("A critical conceptual unit", "Needs Review", "Last edit over", "Primary Source Evidence"):
        c = s.count(pat)
        if c: print(f"  RESIDUAL {pat}: {c}")

if __name__ == "__main__":
    main()
