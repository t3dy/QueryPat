#!/usr/bin/env python3
"""Merge human/subagent-written write-ups into the Exegesis-work data files.

Reads every <slug>.written.json in the given dir (default: the writeups scratchpad),
each shaped:
  { "theological_headline": "...", "intro": "...", "theological_synthesis": "...",
    "see_also": {...}, "glosses": { "<entry_id>": "..." } }
and merges into site/public/data/exegesis/works/<slug>.json by entry_id.
Then regenerates index.json via build_exegesis_works so headlines/has_writeup propagate.
Idempotent; reports any gloss keys that don't match a mention."""
import json, os, sys, glob, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKS_DIR = os.path.join(ROOT, "site", "public", "data", "exegesis", "works")


def merge_one(written_path):
    slug = os.path.basename(written_path).replace(".written.json", "")
    target = os.path.join(WORKS_DIR, f"{slug}.json")
    if not os.path.exists(target):
        print(f"  SKIP {slug}: no target {slug}.json")
        return
    w = json.load(open(written_path, encoding="utf-8"))
    d = json.load(open(target, encoding="utf-8"))
    ment_ids = {m["entry_id"] for m in d["mentions"]}
    glosses = w.get("glosses", {})
    unmatched = [k for k in glosses if k not in ment_ids]
    missing = [i for i in ment_ids if i not in glosses]

    for f in ("theological_headline", "intro", "theological_synthesis"):
        if w.get(f):
            d[f] = w[f]
    if w.get("see_also"):
        d["see_also"] = w["see_also"]
    covered = 0
    for m in d["mentions"]:
        g = glosses.get(m["entry_id"])
        if g:
            m["gloss"] = g
            covered += 1
    json.dump(d, open(target, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    flag = ""
    if unmatched:
        flag += f"  [!] {len(unmatched)} unmatched gloss keys"
    if missing:
        flag += f"  [!] {len(missing)} mentions without gloss"
    print(f"  {slug}: {covered}/{len(ment_ids)} glossed{flag}")


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.environ.get("SCRATCH", ""), "writeups")
    files = sorted(glob.glob(os.path.join(src, "*.written.json")))
    if not files:
        sys.exit(f"No *.written.json in {src}")
    print(f"Merging {len(files)} write-ups from {src}")
    for f in files:
        merge_one(f)
    # regenerate index so headlines + has_writeup propagate
    subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "build_exegesis_works.py")],
                   check=True, capture_output=True)
    print("Regenerated index.json")


if __name__ == "__main__":
    main()
