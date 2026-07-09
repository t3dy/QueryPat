#!/usr/bin/env python3
"""Null ALL machine-generated junk prose in dictionary term files.

Two junk generators polluted the term prose:
  - definition / card_description / full_description:
      "A critical conceptual unit within the top term domain..." (triple-repeats
      the mention count, leaks raw truncated segments).
  - interpretive_note / visionary_significance:
      "Primary Source Evidence: ...Last edit ... by Harpax ... Needs Review ..."
      (raw segment dumps with wiki editor metadata).

For any field matching a junk pattern we set it to "". Genuinely hand-written
fields (the ~77 curated theological terms) are left untouched. `card_description`
is rebuilt from `definition` only when the definition is real prose.
Idempotent."""
import json, glob, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TERMS = os.path.join(ROOT, "site", "public", "data", "dictionary", "terms")

JUNK_RE = re.compile(
    r"^A critical conceptual unit within the top term domain"
    r"|^Primary Source Evidence:"
    r"|Last edit over .+ ago by"
    r"|\bNeeds Review\b"
    r"|edited by Harpax",
    re.I,
)
PROSE_FIELDS = ["definition", "interpretive_note", "visionary_significance",
                "scholarly_caution", "card_description", "full_description"]


def is_junk(v):
    return isinstance(v, str) and bool(JUNK_RE.search(v))


def preview(defn, limit=200):
    defn = defn.strip()
    if len(defn) <= limit:
        return defn
    cut = defn[:limit]
    m = list(re.finditer(r"[.!?](?:\s|$)", cut))
    if m and m[-1].end() > limit * 0.5:
        return cut[:m[-1].end()].strip()
    sp = cut.rfind(" ")
    return (cut[:sp] if sp > 0 else cut).strip() + "…"


def main():
    nulled = {k: 0 for k in PROSE_FIELDS}
    rebuilt_card = 0
    for f in sorted(glob.glob(os.path.join(TERMS, "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        touched = False
        for k in PROSE_FIELDS:
            if is_junk(d.get(k)):
                d[k] = ""
                nulled[k] += 1
                touched = True
        # rebuild card_description from a real definition if it's now empty
        if not d.get("card_description") and d.get("definition") and not is_junk(d["definition"]):
            d["card_description"] = preview(d["definition"])
            rebuilt_card += 1
            touched = True
        if touched:
            json.dump(d, open(f, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print("Nulled junk fields:", {k: v for k, v in nulled.items() if v})
    print("Rebuilt card_description from real definitions:", rebuilt_card)

    # residual check
    residual = 0
    for f in glob.glob(os.path.join(TERMS, "*.json")):
        d = json.load(open(f, encoding="utf-8"))
        if any(is_junk(d.get(k)) for k in PROSE_FIELDS):
            residual += 1
    print("Residual junk fields:", residual)


if __name__ == "__main__":
    main()
