#!/usr/bin/env python3
"""Strip leaked inline claim-IDs (e.g. "(CLM_S_1226c6fbc4, CLM_S_f13effba11)")
from the DISPLAYED prose fields of dictionary terms. The IDs remain tracked in
the structured *_claim_ids / cited_claims fields, which are NOT touched.
Idempotent. Only edits the six rendered prose fields."""
import json, glob, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TERMS = os.path.join(ROOT, "site", "public", "data", "dictionary", "terms")

DISPLAY_FIELDS = ["definition", "interpretive_note", "visionary_significance",
                  "scholarly_caution", "card_description", "full_description"]

PAREN = re.compile(r"\s*\((?:CLM_[A-Za-z0-9_]+(?:\s*,\s*)?)+\)")
BARE = re.compile(r"\s*\bCLM_[A-Za-z0-9_]{6,}\b")


def clean(text):
    text = PAREN.sub("", text)          # remove "(CLM_x, CLM_y)" parentheticals
    text = BARE.sub("", text)           # remove any stray bare CLM ids
    text = re.sub(r"\s+([.;,])", r"\1", text)   # fix " ." -> "."
    text = re.sub(r"[ \t]{2,}", " ", text)      # collapse double spaces
    return text.strip()


def main():
    changed_files = 0
    changed_fields = 0
    for f in sorted(glob.glob(os.path.join(TERMS, "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        touched = False
        for k in DISPLAY_FIELDS:
            v = d.get(k)
            if isinstance(v, str) and "CLM_" in v:
                nv = clean(v)
                if nv != v:
                    d[k] = nv
                    touched = True
                    changed_fields += 1
        if touched:
            json.dump(d, open(f, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
            changed_files += 1
    print(f"Cleaned {changed_fields} fields across {changed_files} term files.")

    # verify none remain in displayed fields
    remaining = 0
    for f in glob.glob(os.path.join(TERMS, "*.json")):
        d = json.load(open(f, encoding="utf-8"))
        for k in DISPLAY_FIELDS:
            if isinstance(d.get(k), str) and "CLM_" in d[k]:
                remaining += 1
                print(f"  STILL LEAKING: {os.path.basename(f)}:{k}")
    print(f"Remaining leaks in displayed fields: {remaining}")


if __name__ == "__main__":
    main()
