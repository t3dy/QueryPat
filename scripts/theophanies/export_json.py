"""Export theophanies to per-route JSON for the static site.

Writes:
    site/public/data/theophanies/index.json
    site/public/data/theophanies/{slug}.json
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path


JSON_FIELDS = [
    "pkd_interpretations", "scholar_interpretations", "primary_sources",
    "related_theophany_ids", "related_works", "related_dictionary_terms",
    "related_names", "related_segments",
]


def row_to_dict(cur: sqlite3.Cursor, row: tuple) -> dict:
    cols = [d[0] for d in cur.description]
    out = dict(zip(cols, row))
    for f in JSON_FIELDS:
        if f in out and out[f]:
            try:
                out[f] = json.loads(out[f])
            except (json.JSONDecodeError, TypeError):
                pass
    return out


def export(db_path: Path, out_dir: Path) -> None:
    con = sqlite3.connect(db_path)
    out_dir.mkdir(parents=True, exist_ok=True)

    cur = con.execute(
        """SELECT theophany_id, name, slug, date_start, date_end, date_display,
                  date_confidence, date_basis, experience_type, sensory_modality,
                  duration, summary, description, pkd_interpretations,
                  scholar_interpretations, primary_sources, primary_quote,
                  related_theophany_ids, related_works, related_dictionary_terms,
                  related_names, related_segments, contested_status,
                  contradiction_zone, pkd_doubt_evidence, importance,
                  sequence_in_complex, parent_theophany_id
           FROM theophanies
           ORDER BY date_start, sequence_in_complex"""
    )
    rows = cur.fetchall()
    all_records = [row_to_dict(cur, r) for r in rows]

    # Index — list with summary fields only
    index = {
        "total": len(all_records),
        "theophanies": [
            {
                "theophany_id": r["theophany_id"],
                "name": r["name"],
                "slug": r["slug"],
                "date_display": r["date_display"],
                "date_start": r["date_start"],
                "experience_type": r["experience_type"],
                "summary": r["summary"],
                "importance": r["importance"],
                "contested_status": r["contested_status"],
                "parent_theophany_id": r["parent_theophany_id"],
                "n_pkd_interpretations": len(r["pkd_interpretations"] or []),
                "n_scholar_interpretations": len(r["scholar_interpretations"] or []),
                "related_works": r["related_works"] or [],
            }
            for r in all_records
        ],
    }
    (out_dir / "index.json").write_text(
        json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # Detail — per-theophany files
    for r in all_records:
        (out_dir / f"{r['slug']}.json").write_text(
            json.dumps(r, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    print(f"[done] exported {len(all_records)} theophanies to {out_dir}")
    con.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="C:/QueryPat/database/unified.sqlite")
    ap.add_argument("--out", default="site/public/data/theophanies")
    args = ap.parse_args()
    export(Path(args.db), Path(args.out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
