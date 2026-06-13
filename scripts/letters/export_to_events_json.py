"""Append letter-derived biography_events to site/public/data/biography/events.json.

The Biography page reads from this JSON. After running scripts/letters/ingest.py,
the 18+ letter-derived events sit in the DB but not yet in events.json. This
script pulls them and appends, keyed by bio_id (idempotent).
"""
from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path


def main():
    db = Path("C:/QueryPat/database/unified.sqlite")
    out = Path("site/public/data/biography/events.json")

    if not out.exists():
        print(f"[error] {out} not found", file=sys.stderr)
        return 1

    with out.open(encoding="utf-8") as f:
        existing = json.load(f)
    existing_bio_ids = {ev.get("bio_id") for ev in existing}

    con = sqlite3.connect(db)
    cur = con.execute(
        """SELECT bio_id, summary, detail, date_start, date_end, date_display, date_confidence,
                  event_type, location, source_type, source_name, reliability,
                  source_letter_id, evidence_quote, interpretation_lane, themes,
                  notable_correspondence, theophany_id, people_involved, notes, source_doc_id
           FROM biography_events
           WHERE source_type = 'letter'"""
    )
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]

    # Look up theophany slugs
    cur2 = con.execute("SELECT theophany_id, slug FROM theophanies")
    tid_to_slug = {tid: slug for tid, slug in cur2.fetchall()}

    added = 0
    updated = 0
    for row in rows:
        d = dict(zip(cols, row))
        if d.get("theophany_id"):
            d["theophany_slug"] = tid_to_slug.get(d["theophany_id"]) or ""
        if d["bio_id"] in existing_bio_ids:
            # Update in-place
            for i, ev in enumerate(existing):
                if ev.get("bio_id") == d["bio_id"]:
                    existing[i] = d
                    updated += 1
                    break
        else:
            existing.append(d)
            added += 1

    with out.open("w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    print(f"[done] {added} letter-derived events added; {updated} updated. Total in events.json: {len(existing)}")
    con.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
