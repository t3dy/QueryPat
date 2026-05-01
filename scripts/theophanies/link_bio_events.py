"""Link biography_events to theophanies by date overlap + vocabulary match.

A bio event is linked to a theophany if:
  1. The bio event's date falls within the theophany's date_start..date_end
  2. The bio event's summary contains any of the theophany's keyword vocabulary

Updates biography_events.theophany_id in-place. Also patches
site/public/data/biography/curated.json and events.json with the new field
so the Biography page can render the link.

Usage:
    python scripts/theophanies/link_bio_events.py [--db PATH]
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from pathlib import Path

# Reuse the same per-theophany keyword vocabulary as the segment linker.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from scripts.theophanies.link_segments import THEOPHANY_KEYWORDS  # noqa: E402


def date_within(date_str: str, start: str, end: str) -> bool:
    """Crude date overlap. Accepts YYYY, YYYY-MM, or YYYY-MM-DD."""
    if not date_str:
        return False
    s = (start or "")[:7] or (start or "")[:4]
    e = (end or start or "")[:7] or (end or start or "")[:4]
    d = date_str[:7] if len(date_str) >= 7 else date_str[:4]
    if not (s and d):
        return False
    return s[:4] <= d[:4] <= (e[:4] or s[:4])


def link_bio_events(db_path: Path) -> dict:
    con = sqlite3.connect(db_path)

    cur = con.execute(
        """SELECT theophany_id, name, slug, date_start, date_end, summary
           FROM theophanies"""
    )
    theos = [dict(zip([d[0] for d in cur.description], r)) for r in cur.fetchall()]
    # Build a global ID -> slug lookup for the patcher
    global TID_TO_SLUG
    TID_TO_SLUG = {t["theophany_id"]: t["slug"] for t in theos}

    cur = con.execute(
        """SELECT bio_id, summary, date_start, event_type FROM biography_events"""
    )
    bios = [dict(zip([d[0] for d in cur.description], r)) for r in cur.fetchall()]
    print(f"[load] {len(bios)} bio events; {len(theos)} theophanies")

    n_linked = 0
    bio_to_theo: dict[str, str] = {}
    for bio in bios:
        date = bio.get("date_start") or ""
        body = (bio.get("summary") or "").lower()
        if not body:
            continue

        best_match = None
        best_score = 0
        for t in theos:
            # Date filter
            if not date_within(date, t.get("date_start") or "", t.get("date_end") or ""):
                continue
            # Vocabulary match
            keywords = THEOPHANY_KEYWORDS.get(t["theophany_id"], [])
            if not keywords:
                continue
            score = 0
            for kw in keywords:
                kw_low = kw.lower().strip()
                if len(kw_low) >= 8:
                    if kw_low in body:
                        score += 1
                else:
                    if re.search(r"\b" + re.escape(kw_low) + r"\b", body):
                        score += 1
            if score > best_score:
                best_score = score
                best_match = t["theophany_id"]

        if best_match and best_score >= 1:
            bio_to_theo[bio["bio_id"]] = best_match

    print(f"[match] {len(bio_to_theo)} bio events linked to a theophany")

    # Update DB
    for bio_id, tid in bio_to_theo.items():
        con.execute(
            "UPDATE biography_events SET theophany_id = ? WHERE bio_id = ?",
            (tid, bio_id),
        )
        n_linked += 1
    con.commit()
    con.close()

    # Patch the JSON files too — the static site reads from these
    patch_curated(bio_to_theo)
    patch_events(bio_to_theo)

    print(f"[done] {n_linked} biography_events.theophany_id rows updated")
    return {"linked": n_linked}


def patch_curated(bio_to_theo: dict[str, str]) -> None:
    p = Path("site/public/data/biography/curated.json")
    if not p.exists():
        return
    with p.open(encoding="utf-8") as f:
        data = json.load(f)
    n = 0
    for ev in data:
        eid = ev.get("id") or ""
        if eid in bio_to_theo:
            tid = bio_to_theo[eid]
            ev["theophany_id"] = tid
            ev["theophany_slug"] = TID_TO_SLUG.get(tid) or ""
            n += 1
    if n:
        with p.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[patch] curated.json: {n} events linked")


def patch_events(bio_to_theo: dict[str, str]) -> None:
    p = Path("site/public/data/biography/events.json")
    if not p.exists():
        return
    with p.open(encoding="utf-8") as f:
        data = json.load(f)
    n = 0
    for ev in data:
        eid = ev.get("bio_id") or ""
        if eid in bio_to_theo:
            tid = bio_to_theo[eid]
            ev["theophany_id"] = tid
            ev["theophany_slug"] = TID_TO_SLUG.get(tid) or ""
            n += 1
    if n:
        with p.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[patch] events.json: {n} events linked")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="C:/QueryPat/database/unified.sqlite")
    args = ap.parse_args()
    link_bio_events(Path(args.db))
    return 0


if __name__ == "__main__":
    sys.exit(main())
