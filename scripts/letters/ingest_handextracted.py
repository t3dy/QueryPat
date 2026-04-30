"""Ingest hand-extracted letter events from a JSON file.

Input format: a JSON array of {letter_id, events: [...]} entries.
Each event dict matches the prompt schema in prompts/extract_events.md.

Usage:
    python scripts/letters/ingest_handextracted.py --input PATH [--db PATH]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sqlite3
import sys
from pathlib import Path

HAND_PROMPT_VERSION = "2026-04-29-handextract-v1"
HAND_MODEL = "claude-in-conversation"

SCHEMA = """
CREATE TABLE IF NOT EXISTS letter_events_candidate (
    candidate_id TEXT PRIMARY KEY,
    letter_id TEXT NOT NULL,
    summary TEXT,
    themes_json TEXT,
    date_start TEXT,
    date_confidence TEXT,
    event_type TEXT,
    location TEXT,
    people_json TEXT,
    evidence_quote TEXT,
    interpretation_lane TEXT,
    importance TEXT,
    notable_correspondence TEXT,
    raw_json TEXT,
    prompt_version TEXT,
    model TEXT,
    created_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_lec_letter ON letter_events_candidate(letter_id);

CREATE TABLE IF NOT EXISTS letter_events_candidate_runs (
    letter_id TEXT NOT NULL,
    prompt_version TEXT NOT NULL,
    model TEXT NOT NULL,
    n_events INTEGER,
    error TEXT,
    duration_ms INTEGER,
    created_at TEXT,
    PRIMARY KEY (letter_id, prompt_version, model)
);
"""


def ensure_schema(con: sqlite3.Connection) -> None:
    con.executescript(SCHEMA)


def ingest(db_path: Path, input_path: Path) -> dict:
    con = sqlite3.connect(db_path)
    ensure_schema(con)

    data = json.loads(input_path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        print("[error] input must be a JSON array", file=sys.stderr)
        return {"error": "bad_format"}

    n_letters = 0
    n_events = 0
    now = dt.datetime.now(dt.UTC).isoformat(timespec="seconds")

    for entry in data:
        letter_id = entry.get("letter_id")
        events = entry.get("events") or []
        if not letter_id:
            continue
        n_letters += 1

        # Insert candidate events
        for i, e in enumerate(events, 1):
            cid = f"CAND_{letter_id}_HAND_{i:03d}"
            con.execute(
                """INSERT OR REPLACE INTO letter_events_candidate
                (candidate_id, letter_id, summary, themes_json, date_start, date_confidence,
                 event_type, location, people_json, evidence_quote, interpretation_lane,
                 importance, notable_correspondence, raw_json, prompt_version, model, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (cid, letter_id, e.get("summary"), json.dumps(e.get("themes") or []),
                 e.get("date_start"), e.get("date_confidence"), e.get("event_type"),
                 e.get("location"), json.dumps(e.get("people") or []),
                 e.get("evidence_quote"), e.get("interpretation_lane"),
                 e.get("importance"), e.get("notable_correspondence"),
                 json.dumps(e), HAND_PROMPT_VERSION, HAND_MODEL, now),
            )
            n_events += 1

        # Record run
        con.execute(
            """INSERT OR REPLACE INTO letter_events_candidate_runs
            (letter_id, prompt_version, model, n_events, error, duration_ms, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (letter_id, HAND_PROMPT_VERSION, HAND_MODEL, len(events), None, 0, now),
        )

    con.commit()
    con.close()

    print(f"[done] ingested {n_events} events from {n_letters} letters")
    return {"letters": n_letters, "events": n_events}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--db", default="C:/QueryPat/database/unified.sqlite")
    args = ap.parse_args()
    summary = ingest(Path(args.db), Path(args.input))
    print("Summary:", summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
