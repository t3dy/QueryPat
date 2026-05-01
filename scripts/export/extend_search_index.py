"""Extend site/public/data/search_index.json with theophany + essay + scholar entries.

The existing index has 1,337 records (segments, terms, archive docs, names) but
no theophanies, essays, or scholars. This script appends those without disturbing
existing rows; idempotent (drops any rows of types it would re-add before adding).

Usage:
    python scripts/export/extend_search_index.py
"""
from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path


DB = Path("C:/QueryPat/database/unified.sqlite")
INDEX = Path("site/public/data/search_index.json")
ESSAYS = Path("site/public/data/essays/index.json")


ADDED_TYPES = {"theophany", "essay", "scholar"}


def theophany_records(con: sqlite3.Connection) -> list[dict]:
    cur = con.execute(
        """SELECT theophany_id, name, slug, summary, description, date_display
           FROM theophanies"""
    )
    out = []
    for tid, name, slug, summary, desc, date in cur.fetchall():
        text = " ".join(filter(None, [summary, desc])).strip()[:1500]
        out.append({
            "type": "theophany",
            "id": tid,
            "slug": slug,
            "title": name,
            "date": date or "",
            "text": text,
        })
    return out


def essay_records() -> list[dict]:
    if not ESSAYS.exists():
        return []
    with ESSAYS.open(encoding="utf-8") as f:
        ix = json.load(f)
    out = []
    for e in ix.get("essays", []):
        out.append({
            "type": "essay",
            "id": e["slug"],
            "slug": e["slug"],
            "title": e["title"],
            "date": e.get("date_drafted", ""),
            "text": " ".join([
                e.get("subtitle", ""),
                ", ".join(e.get("key_sources") or [])
            ]).strip()[:1500],
        })
    return out


def scholar_records() -> list[dict]:
    sc_path = Path("site/public/data/scholars.json")
    if not sc_path.exists():
        return []
    with sc_path.open(encoding="utf-8") as f:
        scholars = json.load(f)
    out = []
    for s in scholars:
        text = " ".join(filter(None, [
            s.get("interpretive_stance") or "",
            s.get("relevance") or "",
            ", ".join(s.get("key_works") or []),
        ])).strip()[:1500]
        out.append({
            "type": "scholar",
            "id": s["scholar_id"],
            "slug": s["scholar_id"],
            "title": s["name"],
            "date": "",
            "text": text,
        })
    return out


def main():
    if not INDEX.exists():
        print(f"[error] {INDEX} not found", file=sys.stderr)
        return 1
    with INDEX.open(encoding="utf-8") as f:
        existing = json.load(f)

    # Drop any pre-existing rows of the types we're about to add (idempotent re-run)
    cleaned = [r for r in existing if r.get("type") not in ADDED_TYPES]
    print(f"[plan] {len(existing)} existing rows; {len(existing) - len(cleaned)} dropped for re-add")

    con = sqlite3.connect(DB)
    new_rows: list[dict] = []
    new_rows.extend(theophany_records(con))
    new_rows.extend(essay_records())
    new_rows.extend(scholar_records())
    con.close()

    by_type = {}
    for r in new_rows:
        by_type[r["type"]] = by_type.get(r["type"], 0) + 1
    for t, n in by_type.items():
        print(f"[add] {t}: {n}")

    out = cleaned + new_rows
    with INDEX.open("w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"[done] wrote {len(out)} records to {INDEX} (was {len(existing)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
