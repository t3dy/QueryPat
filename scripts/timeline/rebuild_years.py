"""Rebuild timeline/years/{year}.json so every year that has *any* content lights up.

Merges three sources into per-year files:
  1. Exegesis segments (from existing year files / segments table)
  2. Biography events (curated.json + events.json)
  3. Theophanies (from theophanies table)

Also updates analytics.json's segments_per_year so has_content reflects the union.

Usage:
    python scripts/timeline/rebuild_years.py [--db PATH] [--data-dir PATH]
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path


PKD_BIRTH = 1928
PKD_DEATH = 1982


def parse_year(date_str: str | None) -> str | None:
    """Return YYYY string or None."""
    if not date_str:
        return None
    s = str(date_str).strip()
    # Try first 4 chars as year
    head = s[:4]
    if head.isdigit():
        y = int(head)
        if PKD_BIRTH <= y <= PKD_DEATH:
            return head
    return None


def load_curated(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def load_events(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def load_theophanies(con: sqlite3.Connection) -> list[dict]:
    cur = con.execute(
        """SELECT theophany_id, name, slug, date_start, date_end, date_display,
                  date_confidence, summary, importance, contested_status,
                  experience_type, parent_theophany_id
           FROM theophanies"""
    )
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, r)) for r in rows]


def existing_segments_for_year(con: sqlite3.Connection, year: str) -> list[dict]:
    """Pull all segments whose date_start starts with {year}-."""
    cur = con.execute(
        """SELECT seg_id, doc_id, slug, title, date_start, date_end, date_display,
                  date_confidence, concise_summary, recurring_concepts,
                  people_entities, tensions, reading_excerpt, word_count
           FROM segments
           WHERE date_start LIKE ?
           ORDER BY date_start, seg_id""",
        (f"{year}-%",),
    )
    out: list[dict] = []
    for row in cur.fetchall():
        cols = [d[0] for d in cur.description]
        d = dict(zip(cols, row))
        # JSON-decode list fields if they're stored as JSON strings
        for k in ("recurring_concepts", "people_entities", "tensions"):
            if isinstance(d[k], str) and d[k]:
                try:
                    d[k] = json.loads(d[k])
                except json.JSONDecodeError:
                    pass
        d["has_raw_text"] = bool(d.get("reading_excerpt"))
        # Drop reading_excerpt to keep year files small (kept on segments/{seg_id}.json)
        d.pop("reading_excerpt", None)
        out.append(d)
    return out


def normalize_curated_event(ev: dict) -> dict:
    """Convert curated.json schema to the year-file biography_event format."""
    return {
        "_type": "biography_event",
        "bio_id": ev.get("id") or f"BIO_CUR_{ev.get('date','UNDATED')}_{abs(hash(ev.get('event','')))%10000:04d}",
        "summary": ev.get("event") or "",
        "date_start": ev.get("date") or "",
        "date_end": ev.get("date") or "",
        "date_display": ev.get("date") or "",
        "date_confidence": ev.get("date_precision") or "year",
        "event_type": ev.get("category") or "other",
        "source_name": ev.get("source") or "curated",
        "source_type": "curated",
        "location": ev.get("location") or None,
        "importance": str(ev.get("importance", "")) if ev.get("importance") is not None else None,
        "notes": ev.get("notes") or None,
        "entities": ev.get("entities") or [],
    }


def normalize_event(ev: dict) -> dict:
    """Convert events.json (auto-extracted) schema to year-file format."""
    return {
        "_type": "biography_event",
        "bio_id": ev.get("bio_id") or "",
        "summary": ev.get("summary") or "",
        "date_start": ev.get("date_start") or "",
        "date_end": ev.get("date_end") or ev.get("date_start") or "",
        "date_display": ev.get("date_display") or ev.get("date_start") or "",
        "date_confidence": ev.get("date_confidence") or "year",
        "event_type": ev.get("event_type") or "other",
        "source_name": ev.get("source_name") or "auto-extracted",
        "source_type": ev.get("source_type") or "extracted",
        "location": ev.get("location") or None,
        "importance": ev.get("importance"),
    }


def normalize_theophany(t: dict) -> dict:
    """Theophany → year-file entry with _type='theophany'."""
    return {
        "_type": "theophany",
        "theophany_id": t["theophany_id"],
        "name": t["name"],
        "slug": t["slug"],
        "summary": t.get("summary") or "",
        "date_start": t.get("date_start") or "",
        "date_end": t.get("date_end") or "",
        "date_display": t.get("date_display") or "",
        "date_confidence": t.get("date_confidence") or "year",
        "experience_type": t.get("experience_type") or "vision",
        "importance": t.get("importance") or "minor",
        "contested_status": t.get("contested_status") or "",
        "parent_theophany_id": t.get("parent_theophany_id"),
    }


def expand_theophany_to_years(t: dict) -> list[str]:
    """Return list of YYYY strings the theophany covers (date_start..date_end)."""
    y_start = parse_year(t.get("date_start"))
    y_end = parse_year(t.get("date_end"))
    if not y_start:
        return []
    if not y_end or y_end == y_start:
        return [y_start]
    a, b = sorted([int(y_start), int(y_end)])
    return [str(y) for y in range(a, b + 1)]


def run(db_path: Path, data_dir: Path) -> dict:
    con = sqlite3.connect(db_path)

    curated = load_curated(data_dir / "biography" / "curated.json")
    events = load_events(data_dir / "biography" / "events.json")
    theophanies = load_theophanies(con)

    print(f"[load] {len(curated)} curated bio events, {len(events)} extracted bio events, {len(theophanies)} theophanies")

    # Group everything by year
    by_year: dict[str, list[dict]] = defaultdict(list)

    # Curated bio events (these cover the breadth of PKD's life)
    for ev in curated:
        y = parse_year(ev.get("date"))
        if y:
            by_year[y].append(normalize_curated_event(ev))

    # Auto-extracted bio events (mostly Exegesis-period)
    for ev in events:
        y = parse_year(ev.get("date_start"))
        if y:
            by_year[y].append(normalize_event(ev))

    # Theophanies
    for t in theophanies:
        for y in expand_theophany_to_years(t):
            by_year[y].append(normalize_theophany(t))

    # Existing segments per year — pull from segments table directly
    print("[load] segments per year from DB...")
    for y in [str(year) for year in range(PKD_BIRTH, PKD_DEATH + 1)]:
        segs = existing_segments_for_year(con, y)
        if segs:
            for s in segs:
                by_year[y].append(s)

    # Sort within each year by date_start, then by type
    for y in by_year:
        by_year[y].sort(key=lambda e: (e.get("date_start") or "", e.get("_type", "segment") or ""))

    # Write per-year files
    years_dir = data_dir / "timeline" / "years"
    years_dir.mkdir(parents=True, exist_ok=True)
    for y, entries in by_year.items():
        (years_dir / f"{y}.json").write_text(
            json.dumps(entries, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    # Build/update timeline index
    index_entries = []
    for y in sorted(by_year.keys()):
        entries = by_year[y]
        n_seg = sum(1 for e in entries if "_type" not in e)  # segments don't have _type
        n_bio = sum(1 for e in entries if e.get("_type") == "biography_event")
        n_theo = sum(1 for e in entries if e.get("_type") == "theophany")
        index_entries.append({
            "year": y,
            "count": n_seg,
            "bio_events": n_bio,
            "theophanies": n_theo,
            "total": len(entries),
        })
    (data_dir / "timeline" / "index.json").write_text(
        json.dumps(index_entries, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # Update analytics.json's segments_per_year
    analytics_path = data_dir / "analytics.json"
    if analytics_path.exists():
        with analytics_path.open(encoding="utf-8") as f:
            analytics = json.load(f)
        # Build a per-year dict
        new_spy = []
        index_map = {ie["year"]: ie for ie in index_entries}
        for year_int in range(PKD_BIRTH, PKD_DEATH + 1):
            y = str(year_int)
            ie = index_map.get(y)
            if ie:
                new_spy.append({
                    "year": y,
                    "count": ie["count"],
                    "bio_events": ie["bio_events"],
                    "theophanies": ie["theophanies"],
                    "has_content": ie["total"] > 0,
                })
            else:
                new_spy.append({
                    "year": y,
                    "count": 0,
                    "bio_events": 0,
                    "theophanies": 0,
                    "has_content": False,
                })
        analytics["segments_per_year"] = new_spy
        with analytics_path.open("w", encoding="utf-8") as f:
            json.dump(analytics, f, ensure_ascii=False, indent=2)

    summary = {
        "years_with_content": sum(1 for ie in index_entries if ie["total"] > 0),
        "total_years": PKD_DEATH - PKD_BIRTH + 1,
        "year_files_written": len(by_year),
    }
    print(f"[done] {summary['years_with_content']}/{summary['total_years']} years have content; "
          f"{summary['year_files_written']} per-year files written")

    con.close()
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="C:/QueryPat/database/unified.sqlite")
    ap.add_argument("--data-dir", default="site/public/data")
    args = ap.parse_args()
    run(Path(args.db), Path(args.data_dir))
    return 0


if __name__ == "__main__":
    sys.exit(main())
