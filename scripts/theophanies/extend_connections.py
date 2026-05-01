"""Add theophany edges to site/public/data/connections.json.

Adds five new edge types:
  - theophany_to_segments: theophany_id -> [seg_id, ...]   (from theophany_evidence)
  - theophany_to_terms:    theophany_id -> [term_slug, ...]  (related_dictionary_terms)
  - theophany_to_names:    theophany_id -> [name_slug, ...]  (related_names)
  - theophany_to_works:    theophany_id -> [work_title, ...] (related_works)
  - theophany_to_bio:      theophany_id -> [bio_id, ...]    (from biography_events.theophany_id)

Plus a reverse fan-in:
  - segment_to_theophanies, term_to_theophanies, name_to_theophanies, bio_to_theophany

Idempotent — re-runs overwrite the keys it manages.
"""
from __future__ import annotations

import json
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path


CONN_PATH = Path("site/public/data/connections.json")
DB = Path("C:/QueryPat/database/unified.sqlite")

MANAGED_KEYS = {
    "theophany_to_segments", "theophany_to_terms", "theophany_to_names",
    "theophany_to_works", "theophany_to_bio",
    "segment_to_theophanies", "term_to_theophanies", "name_to_theophanies",
    "bio_to_theophany",
}


def main():
    if not CONN_PATH.exists():
        print(f"[error] {CONN_PATH} not found", file=sys.stderr)
        return 1
    if not DB.exists():
        print(f"[error] {DB} not found", file=sys.stderr)
        return 1

    with CONN_PATH.open(encoding="utf-8") as f:
        conn = json.load(f)

    # Drop managed keys for a clean re-add
    for k in MANAGED_KEYS:
        conn.pop(k, None)

    con = sqlite3.connect(DB)

    # Forward edges from theophanies row data
    cur = con.execute(
        """SELECT theophany_id, related_segments, related_dictionary_terms,
                  related_names, related_works
           FROM theophanies"""
    )
    theophany_to_segments: dict[str, list[str]] = {}
    theophany_to_terms: dict[str, list[str]] = {}
    theophany_to_names: dict[str, list[str]] = {}
    theophany_to_works: dict[str, list[str]] = {}
    seg_to_theos: dict[str, list[str]] = defaultdict(list)
    term_to_theos: dict[str, list[str]] = defaultdict(list)
    name_to_theos: dict[str, list[str]] = defaultdict(list)
    for tid, segs, terms, names, works in cur.fetchall():
        seg_list = json.loads(segs or "[]")
        term_list = json.loads(terms or "[]")
        name_list = json.loads(names or "[]")
        work_list = json.loads(works or "[]")
        if seg_list:
            theophany_to_segments[tid] = seg_list
            for s in seg_list:
                seg_to_theos[s].append(tid)
        if term_list:
            theophany_to_terms[tid] = term_list
            for t in term_list:
                term_to_theos[t].append(tid)
        if name_list:
            theophany_to_names[tid] = name_list
            for n in name_list:
                name_to_theos[n].append(tid)
        if work_list:
            theophany_to_works[tid] = work_list

    # Theophany -> bio events from biography_events.theophany_id
    cur = con.execute(
        """SELECT bio_id, theophany_id FROM biography_events
           WHERE theophany_id IS NOT NULL"""
    )
    theophany_to_bio: dict[str, list[str]] = defaultdict(list)
    bio_to_theophany: dict[str, str] = {}
    for bio_id, tid in cur.fetchall():
        if tid:
            theophany_to_bio[tid].append(bio_id)
            bio_to_theophany[bio_id] = tid

    con.close()

    conn["theophany_to_segments"] = theophany_to_segments
    conn["theophany_to_terms"] = theophany_to_terms
    conn["theophany_to_names"] = theophany_to_names
    conn["theophany_to_works"] = theophany_to_works
    conn["theophany_to_bio"] = dict(theophany_to_bio)
    conn["segment_to_theophanies"] = dict(seg_to_theos)
    conn["term_to_theophanies"] = dict(term_to_theos)
    conn["name_to_theophanies"] = dict(name_to_theos)
    conn["bio_to_theophany"] = bio_to_theophany

    n_edges = (
        sum(len(v) for v in theophany_to_segments.values())
        + sum(len(v) for v in theophany_to_terms.values())
        + sum(len(v) for v in theophany_to_names.values())
        + sum(len(v) for v in theophany_to_works.values())
        + sum(len(v) for v in theophany_to_bio.values())
    )

    with CONN_PATH.open("w", encoding="utf-8") as f:
        json.dump(conn, f, ensure_ascii=False, indent=2)

    print(f"[done] wrote {n_edges} theophany edges across {len(MANAGED_KEYS)} keys")
    print(f"  theophany_to_segments: {len(theophany_to_segments)} theophanies")
    print(f"  theophany_to_terms:    {len(theophany_to_terms)} theophanies")
    print(f"  theophany_to_names:    {len(theophany_to_names)} theophanies")
    print(f"  theophany_to_works:    {len(theophany_to_works)} theophanies")
    print(f"  theophany_to_bio:      {len(theophany_to_bio)} theophanies, {sum(len(v) for v in theophany_to_bio.values())} events")
    print(f"  segment_to_theophanies: {len(seg_to_theos)} segments")
    print(f"  term_to_theophanies:    {len(term_to_theos)} terms")
    print(f"  name_to_theophanies:    {len(name_to_theos)} names")
    return 0


if __name__ == "__main__":
    sys.exit(main())
