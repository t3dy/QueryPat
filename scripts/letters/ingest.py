"""Stage 4 + 5: dedupe candidate events and write into biography_events.

Reads `letter_events_candidate`, groups duplicates by (date_start, event_type, themes),
picks the earliest letter as primary, and inserts one row per unique event into
biography_events with full provenance.

Usage:
    python scripts/letters/ingest.py [--db PATH] [--dry-run]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path


# Add new columns to biography_events if not present.
NEW_COLUMNS = [
    ("source_letter_id", "TEXT"),
    ("corroborating_letters", "TEXT"),
    ("evidence_quote", "TEXT"),
    ("interpretation_lane", "TEXT"),
    ("contradicts_event_id", "TEXT"),
    ("themes", "TEXT"),
    ("notable_correspondence", "TEXT"),
]


def get_columns(con: sqlite3.Connection, table: str) -> set[str]:
    cur = con.execute(f"PRAGMA table_info({table})")
    return {row[1] for row in cur.fetchall()}


def ensure_biography_columns(con: sqlite3.Connection) -> int:
    existing = get_columns(con, "biography_events")
    if not existing:
        print("[error] biography_events table not found", file=sys.stderr)
        return 0
    added = 0
    for name, type_ in NEW_COLUMNS:
        if name not in existing:
            con.execute(f"ALTER TABLE biography_events ADD COLUMN {name} {type_}")
            added += 1
            print(f"  [add] {name} {type_}")
    con.commit()
    return added


def fetch_candidates(con: sqlite3.Connection) -> list[dict]:
    cur = con.execute(
        """SELECT c.candidate_id, c.letter_id, c.summary, c.themes_json, c.date_start,
                  c.date_confidence, c.event_type, c.location, c.people_json,
                  c.evidence_quote, c.interpretation_lane, c.importance,
                  c.notable_correspondence,
                  l.volume_doc_id, l.recipient_raw, l.date_display
           FROM letter_events_candidate c
           JOIN letters l ON l.letter_id = c.letter_id
           ORDER BY c.date_start, c.letter_id, c.candidate_id"""
    )
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


def normalize_summary(s: str) -> str:
    """Lowercase, strip punctuation, collapse whitespace — for fuzzy dedup keys."""
    import re
    s = (s or "").lower()
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def group_key(c: dict) -> tuple:
    """Two events with the same (date, event_type, normalized-summary-prefix) are duplicates."""
    summary = normalize_summary(c.get("summary") or "")
    prefix = " ".join(summary.split()[:8])  # first 8 words
    return (c.get("date_start") or "", c.get("event_type") or "", prefix)


def dedupe(candidates: list[dict]) -> list[dict]:
    """Group by group_key; pick earliest letter as primary; collect corroborators."""
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for c in candidates:
        groups[group_key(c)].append(c)
    deduped = []
    for key, group in groups.items():
        # Sort group by (date_start, letter_id) — earliest letter wins.
        group.sort(key=lambda c: (c.get("date_start") or "", c.get("letter_id") or ""))
        primary = group[0]
        primary["corroborating_letter_ids"] = [c["letter_id"] for c in group[1:] if c["letter_id"] != primary["letter_id"]]
        deduped.append(primary)
    return deduped


def reliability_for(c: dict) -> str:
    """Map our (fact|self_report) to schema's allowed reliability values."""
    lane = c.get("interpretation_lane")
    if lane == "self_report":
        return "unverified"
    return "confirmed"


# Map our richer event_type vocabulary to the schema's allowed CHECK list.
EVENT_TYPE_MAP = {
    "meeting": "correspondence",
    "writing": "publication",
    "reading": "other",
    "listening": "other",
    "creative": "publication",
    "drug_use": "substance_use",
    "speech": "publication",
    "reception": "publication",
}


DATE_CONF_MAP = {
    "month": "approximate",
    "year": "approximate",
    "day": "exact",
    "exact": "exact",
    "approximate": "approximate",
    "circa": "circa",
    "inferred": "inferred",
    "unknown": "unknown",
}


def map_date_conf(dc: str | None) -> str:
    if not dc:
        return "unknown"
    return DATE_CONF_MAP.get(dc, "approximate")


def map_event_type(et: str | None) -> str:
    if not et:
        return "other"
    return EVENT_TYPE_MAP.get(et, et if et in {
        "birth", "death", "marriage", "divorce", "residence",
        "employment", "publication", "vision", "health",
        "relationship", "legal", "financial", "travel",
        "substance_use", "correspondence", "other",
    } else "other")


def make_bio_id(c: dict, n: int) -> str:
    date = (c.get("date_start") or "UNDATED").replace("-", "")
    et = (c.get("event_type") or "EVENT").upper().replace("_", "")
    return f"BIO_LETTER_{date}_{et}_{n:04d}"


def insert_biography_event(con: sqlite3.Connection, c: dict, bio_id: str) -> None:
    now = dt.datetime.now(dt.UTC).isoformat(timespec="seconds")
    themes = c.get("themes_json") or "[]"
    corroborating = json.dumps(c.get("corroborating_letter_ids") or [])

    # First check if we already inserted this letter event (idempotent dedup)
    existing = con.execute(
        "SELECT bio_id FROM biography_events WHERE source_letter_id = ? AND summary = ?",
        (c.get("letter_id"), c.get("summary")),
    ).fetchone()
    if existing:
        # Update in place
        con.execute(
            """UPDATE biography_events SET
                date_start=?, date_end=?, date_display=?, date_confidence=?,
                event_type=?, location=?, source_type=?, source_name=?,
                reliability=?, corroborating_letters=?, evidence_quote=?,
                interpretation_lane=?, themes=?, notable_correspondence=?
               WHERE bio_id=?""",
            (
                c.get("date_start"), c.get("date_start"),
                c.get("date_start"), map_date_conf(c.get("date_confidence")),
                map_event_type(c.get("event_type")), c.get("location"),
                "letter",
                f"Selected Letters ({c.get('volume_doc_id', '')})",
                reliability_for(c),
                corroborating,
                c.get("evidence_quote"),
                c.get("interpretation_lane"),
                themes,
                c.get("notable_correspondence"),
                existing[0],
            ),
        )
        return
    # Else: fresh insert (let SQLite auto-assign integer bio_id)
    con.execute(
        """INSERT INTO biography_events
        (summary, date_start, date_end, date_display, date_confidence,
         event_type, location, source_type, source_name,
         reliability,
         source_letter_id, corroborating_letters, evidence_quote,
         interpretation_lane, themes, notable_correspondence, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            c.get("summary"),
            c.get("date_start"),
            c.get("date_start"),
            c.get("date_start"),
            map_date_conf(c.get("date_confidence")),
            map_event_type(c.get("event_type")),
            c.get("location"),
            "letter",
            f"Selected Letters ({c.get('volume_doc_id', '')})"[:80],
            reliability_for(c),
            c.get("letter_id"),
            corroborating,
            c.get("evidence_quote"),
            c.get("interpretation_lane"),
            themes,
            c.get("notable_correspondence"),
            now,
        ),
    )


def run(db_path: Path, dry_run: bool) -> dict:
    con = sqlite3.connect(db_path)
    ensure_biography_columns(con)

    candidates = fetch_candidates(con)
    print(f"[plan] {len(candidates)} candidate events from letters")

    deduped = dedupe(candidates)
    print(f"[plan] {len(deduped)} unique events after dedup ({len(candidates) - len(deduped)} merged as corroborating)")

    by_theme: dict[str, int] = defaultdict(int)
    for c in deduped:
        for t in json.loads(c.get("themes_json") or "[]"):
            by_theme[t] += 1
    print("\nEvents by theme:")
    for theme, count in sorted(by_theme.items(), key=lambda kv: -kv[1]):
        print(f"  {theme:16s} {count}")

    if dry_run:
        print("\n[dry-run] not inserting into biography_events")
        return {"candidates": len(candidates), "unique": len(deduped), "by_theme": dict(by_theme)}

    n_inserted = 0
    for i, c in enumerate(deduped, 1):
        bio_id = make_bio_id(c, i)
        insert_biography_event(con, c, bio_id)
        n_inserted += 1
        if i % 100 == 0:
            print(f"  [{i}/{len(deduped)}] inserted")
    con.commit()
    con.close()

    return {"candidates": len(candidates), "unique": len(deduped),
            "inserted": n_inserted, "by_theme": dict(by_theme)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="C:/QueryPat/database/unified.sqlite")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    summary = run(Path(args.db), args.dry_run)
    print()
    print("Summary:", summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
