#!/usr/bin/env python3
"""Add the authored study dossiers to search_index.json.

Two entry types, both rebuilt from the exported study JSON on every run:
- `study`:   one per dossier topic (title, card description)
- `passage`: one per mention card — the citation, its books and themes, the
             verbatim pith and the editorial summary — so a search for
             "Malachi" or "glass darkly" lands on the exact card.

Only topics with mention cards are indexed. Existing study/passage entries are
dropped first, so the pass is idempotent. Runs after export_json, which owns
the rest of the index; registered in safe_export's post-export passes.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "site", "public", "data")
SI = os.path.join(DATA, "search_index.json")
STUDIES = os.path.join(DATA, "studies")


def clip(text, n):
    text = re.sub(r"\s+", " ", text or "").strip()
    return text if len(text) <= n else text[: n - 1].rstrip() + "…"


def main():
    idx = json.load(open(SI, encoding="utf-8"))
    kept = [e for e in idx if e.get("type") not in ("study", "passage")]
    added = []
    studies = json.load(open(os.path.join(STUDIES, "index.json"), encoding="utf-8"))
    for st in studies:
        sid = st["study_id"]
        tdir = os.path.join(STUDIES, sid, "topics")
        if not os.path.isdir(tdir):
            continue
        for fn in sorted(os.listdir(tdir)):
            topic = json.load(open(os.path.join(tdir, fn), encoding="utf-8"))
            cards = topic.get("mention_cards") or []
            if not cards:
                continue
            slug = topic["slug"]
            added.append({
                "type": "study", "id": topic["topic_id"], "slug": f"{sid}/{slug}",
                "title": topic["canonical_name"],
                "text": clip(topic.get("definition") or "", 300),
                "category": st.get("study_label"),
            })
            for c in cards:
                added.append({
                    "type": "passage", "id": c["id"], "slug": f"{sid}/{slug}",
                    "title": c["citation"],
                    "date": c.get("dated"),
                    "category": topic["canonical_name"],
                    "tags": c.get("concepts") or [],
                    "text": clip(f'“{c["pith"]}” — {c["context"]}', 400),
                })
    out = kept + added
    json.dump(out, open(SI, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    n_topics = sum(1 for e in added if e["type"] == "study")
    print(f"search_index: {len(kept)} base + {n_topics} study + "
          f"{len(added) - n_topics} passage entries")


if __name__ == "__main__":
    main()
