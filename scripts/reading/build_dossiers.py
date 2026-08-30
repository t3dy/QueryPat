#!/usr/bin/env python3
"""Turn gathered evidence into work dossiers.

Everything a script can establish is filled in: structure, the concepts the
work turns on, where Dick discusses it, where the critics do, and which
characters and places appear and how often. The interpretive layer — synopsis,
movements, motifs, what the work is doing — is left explicitly open, because a
machine counting nouns has not read anything.

So a dossier is born with `reading_status: "pending_close_reading"` and is
filled in by an actual reading. That way coverage of the evidence layers is
corpus-wide immediately, and the reading proceeds work by work without the
dossier pretending to knowledge it does not have.

Hand-written dossiers are never overwritten.

    python scripts/reading/build_dossiers.py
    python scripts/reading/build_dossiers.py --report
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT / "database" / "unified.sqlite"
EVIDENCE_DIR = PROJECT / "artifacts" / "generated" / "reading" / "evidence"
DOSSIER_DIR = PROJECT / "artifacts" / "generated" / "reading" / "dossiers"

# names.entity_type tells a character from a place, which is what separates a
# cast list from a setting list without anyone having to read the story.
PERSON_TYPES = {"character", "historical_person", "deity_figure"}
PLACE_TYPES = {"place"}


def name_types(db: sqlite3.Connection) -> dict[str, str]:
    return {n: t for n, t in db.execute("select name_id, entity_type from names")}


def build_one(evidence: dict, types: dict[str, str]) -> dict:
    slug = evidence["slug"]
    names = evidence["concepts"]["names"]

    people = [n for n in names if types.get(n["entity_id"]) in PERSON_TYPES]
    places = [n for n in names if types.get(n["entity_id"]) in PLACE_TYPES]
    other = [n for n in names
             if types.get(n["entity_id"]) not in PERSON_TYPES | PLACE_TYPES]

    pkd = evidence["pkd_on_this_work"]
    crit = evidence["criticism"]

    return {
        "artifact_id": f"ART_DOSSIER_{slug.upper().replace('-', '_')}",
        "artifact_type": "work_dossier",
        "schema_version": "1.0",
        "source_id": slug,
        "generated_by": "scripts/reading/build_dossiers.py",
        "status": "LLM_CANDIDATE",
        "review_state": "unreviewed",
        "reading_status": "pending_close_reading",
        "note": (
            "Scripted layers are complete. The interpretive layer is open: no "
            "synopsis, movement breakdown or thematic reading appears here "
            "because nobody has read the work yet. Do not cite this as a "
            "summary of the work."
        ),

        "work": {
            "title": evidence["title"],
            "slug": slug,
            "form": evidence["kind"],
            "word_count": evidence["source"]["word_count"],
            "lane": "A",
            "source": evidence["source"],
        },

        "reading": {
            "reading_status": "pending_close_reading",
            "synopsis": None,
            "movements": [],
            "motifs": [],
            "cast_candidates": [
                {"name": n["label"], "name_id": n["entity_id"], "mentions": n["count"]}
                for n in people[:25]
            ],
            "place_candidates": [
                {"name": n["label"], "name_id": n["entity_id"], "mentions": n["count"]}
                for n in places[:15]
            ],
            "other_entities": [
                {"name": n["label"], "name_id": n["entity_id"], "mentions": n["count"]}
                for n in other[:15]
            ],
            "structure": evidence["structure"],
        },

        "concepts": {
            "distinctive_terms": [
                {
                    "label": t["label"],
                    "entity_id": t["entity_id"],
                    "count": t["count"],
                    "distinctiveness": t["distinctiveness"],
                }
                for t in evidence["concepts"]["terms"][:25]
            ],
            "method": (
                "Matched against the dictionary's accepted and provisional terms, "
                "filtered by noise_score, then ranked by how much more often the "
                "term occurs here than across Dick's other fiction."
            ),
        },

        "pkd_on_this_work": {
            "lane": "E/B",
            "total_mentions": pkd["total_mentions"],
            "sources": pkd["sources"],
            "reading": None,
        },

        "criticism": {
            "lane": "C",
            "total_mentions": crit["total_mentions"],
            "sources": crit["sources"],
            "reading": None,
        },

        "contradictions": [],
        "open_questions": [],

        "provenance": {
            "layer_1_reading": "NOT DONE — structural and entity facts only.",
            "layer_2_concepts": "scripts/reading/gather_evidence.py",
            "layer_3_pkd": f"{pkd['total_mentions']} mentions across Dick's letters, Exegesis and essays.",
            "layer_4_criticism": f"{crit['total_mentions']} mentions across the archive scholarship.",
            "not_canonical": (
                "Candidate artifact. Promotion to the database requires an "
                "editorial pass."
            ),
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--force", action="store_true",
                    help="overwrite dossiers that already carry a close reading")
    args = ap.parse_args()

    db = sqlite3.connect(DB_PATH)
    types = name_types(db)
    DOSSIER_DIR.mkdir(parents=True, exist_ok=True)

    written = skipped = 0
    read_done = 0
    rows = []

    for path in sorted(EVIDENCE_DIR.glob("*.evidence.json")):
        evidence = json.loads(path.read_text(encoding="utf-8"))
        slug = evidence["slug"]
        out = DOSSIER_DIR / f"{slug}.dossier.json"

        if out.exists() and not args.force:
            existing = json.loads(out.read_text(encoding="utf-8"))
            if existing.get("reading", {}).get("synopsis"):
                skipped += 1
                read_done += 1
                rows.append((slug, evidence, True))
                continue

        dossier = build_one(evidence, types)
        out.write_text(json.dumps(dossier, indent=1, ensure_ascii=False), encoding="utf-8")
        written += 1
        rows.append((slug, evidence, False))

    print(f"dossiers written : {written}")
    print(f"close readings kept: {skipped}")

    if args.report:
        total = len(rows)
        with_pkd = sum(1 for _, e, _ in rows if e["pkd_on_this_work"]["total_mentions"])
        with_crit = sum(1 for _, e, _ in rows if e["criticism"]["total_mentions"])
        print()
        print(f"works covered            : {total}")
        print(f"  with Dick's own comment: {with_pkd} ({with_pkd/total:.0%})")
        print(f"  with critical comment  : {with_crit} ({with_crit/total:.0%})")
        print(f"  with a close reading   : {read_done} ({read_done/total:.0%})")
        print()
        best = sorted(rows, key=lambda r: -(r[1]["pkd_on_this_work"]["total_mentions"]
                                            + r[1]["criticism"]["total_mentions"]))[:15]
        print("most-discussed works (Dick + critics), the queue for close reading:")
        for slug, e, done in best:
            mark = "read" if done else "    "
            print(f"  {mark}  {e['title'][:40]:<40} "
                  f"pkd={e['pkd_on_this_work']['total_mentions']:>4} "
                  f"crit={e['criticism']['total_mentions']:>4} "
                  f"{e['source']['word_count']:>7,}w")
    return 0


if __name__ == "__main__":
    sys.exit(main())
