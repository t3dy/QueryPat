"""Stage 3: LLM-targeted biography-event extraction from segmented letters.

Reads `letters` table, calls Claude per letter with the prompt at
`scripts/letters/prompts/extract_events.md`, writes results to a new
`letter_events_candidate` table for Stage 4 (dedupe) to consume.

Caching: skips letters whose (letter_id, prompt_version) row already exists
in `letter_events_candidate_runs`.

Usage:
    python scripts/letters/extract_llm.py [--db PATH] [--limit N] [--workers N]
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import sqlite3
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import anthropic

PROMPT_VERSION = "2026-04-29-v1"
MODEL = "claude-sonnet-4-5"
PROMPT_PATH = Path(__file__).resolve().parent / "prompts" / "extract_events.md"

SCHEMA = """
CREATE TABLE IF NOT EXISTS letter_events_candidate (
    candidate_id TEXT PRIMARY KEY,
    letter_id TEXT NOT NULL,
    summary TEXT,
    themes_json TEXT,         -- JSON array of theme strings
    date_start TEXT,
    date_confidence TEXT,
    event_type TEXT,
    location TEXT,
    people_json TEXT,         -- JSON array
    evidence_quote TEXT,
    interpretation_lane TEXT,
    importance TEXT,
    notable_correspondence TEXT,  -- jaynes|star_wars|fbi_letter|lem_affair|71_break_in|2_3_74|pike|galen|powers|jeter|metz|blade_runner|festschrift|stroke
    raw_json TEXT,            -- the original record from the LLM
    prompt_version TEXT,
    model TEXT,
    created_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_lec_letter ON letter_events_candidate(letter_id);
CREATE INDEX IF NOT EXISTS idx_lec_themes ON letter_events_candidate(themes_json);

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


def load_prompt_template() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


def already_done(con: sqlite3.Connection, letter_id: str) -> bool:
    cur = con.execute(
        "SELECT 1 FROM letter_events_candidate_runs WHERE letter_id=? AND prompt_version=? AND model=?",
        (letter_id, PROMPT_VERSION, MODEL),
    )
    return cur.fetchone() is not None


def call_llm(client: anthropic.Anthropic, body: str, date_display: str, recipient: str) -> tuple[list[dict], str | None]:
    template = load_prompt_template()
    prompt = template.format(date=date_display or "unknown", recipient=recipient or "unknown", body=body[:24000])
    msg = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )
    text = "".join(b.text for b in msg.content if hasattr(b, "text"))
    text = text.strip()
    # Tolerate ```json ... ``` or stray prose
    if text.startswith("```"):
        text = text.split("```", 2)[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.rstrip("`").strip()
    try:
        events = json.loads(text)
        if not isinstance(events, list):
            return [], f"non-array response: {text[:100]}"
        return events, None
    except json.JSONDecodeError as e:
        return [], f"json error: {e}; text starts: {text[:120]}"


def insert_candidates(con: sqlite3.Connection, letter_id: str, events: list[dict]) -> int:
    now = dt.datetime.now(dt.UTC).isoformat(timespec="seconds")
    n = 0
    for i, e in enumerate(events, 1):
        cid = f"CAND_{letter_id}_{i:03d}"
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
             json.dumps(e), PROMPT_VERSION, MODEL, now),
        )
        n += 1
    return n


def record_run(con: sqlite3.Connection, letter_id: str, n: int, err: str | None, dur_ms: int) -> None:
    now = dt.datetime.now(dt.UTC).isoformat(timespec="seconds")
    con.execute(
        """INSERT OR REPLACE INTO letter_events_candidate_runs
        (letter_id, prompt_version, model, n_events, error, duration_ms, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (letter_id, PROMPT_VERSION, MODEL, n, err, dur_ms, now),
    )


def process_letter(client: anthropic.Anthropic, letter_id: str, body_md: str,
                   date_display: str, recipient_raw: str) -> tuple[str, list[dict], str | None, int]:
    t0 = time.time()
    events, err = call_llm(client, body_md, date_display, recipient_raw)
    dur_ms = int((time.time() - t0) * 1000)
    return letter_id, events, err, dur_ms


def run(db_path: Path, limit: int | None, workers: int) -> dict:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("[error] ANTHROPIC_API_KEY not set", file=sys.stderr)
        return {"error": "no_api_key"}

    con = sqlite3.connect(db_path)
    ensure_schema(con)

    cur = con.execute(
        """SELECT letter_id, body_md, date_display, recipient_raw, word_count
           FROM letters
           WHERE word_count >= 80         -- skip telegram-stub replies
           ORDER BY date_start, sequence_in_volume"""
    )
    rows = [(lid, body, dd, rr) for lid, body, dd, rr, _ in cur.fetchall()]
    if limit:
        rows = rows[:limit]
    print(f"[plan] {len(rows)} letters in DB; checking cache...")

    pending = [(lid, body, dd, rr) for lid, body, dd, rr in rows if not already_done(con, lid)]
    cached = len(rows) - len(pending)
    print(f"[plan] {cached} cached; {len(pending)} to call LLM on")

    if not pending:
        return {"cached": cached, "called": 0, "events": 0, "errors": 0}

    client = anthropic.Anthropic()
    total_events = 0
    errors = 0

    def handle(letter_id: str, events: list[dict], err: str | None, dur_ms: int) -> None:
        nonlocal total_events, errors
        if err:
            errors += 1
            record_run(con, letter_id, 0, err, dur_ms)
        else:
            n = insert_candidates(con, letter_id, events)
            total_events += n
            record_run(con, letter_id, n, None, dur_ms)
        con.commit()

    if workers <= 1:
        for i, (lid, body, dd, rr) in enumerate(pending, 1):
            try:
                lid_, ev, err, dur = process_letter(client, lid, body, dd, rr)
                handle(lid_, ev, err, dur)
            except Exception as e:
                handle(lid, [], f"unhandled: {type(e).__name__}: {e}", 0)
            if i % 10 == 0 or i == len(pending):
                print(f"  [{i}/{len(pending)}] events_so_far={total_events} errors={errors}")
    else:
        with ThreadPoolExecutor(max_workers=workers) as ex:
            futures = {ex.submit(process_letter, client, lid, body, dd, rr): lid
                       for lid, body, dd, rr in pending}
            for i, fut in enumerate(as_completed(futures), 1):
                try:
                    lid_, ev, err, dur = fut.result()
                    handle(lid_, ev, err, dur)
                except Exception as e:
                    handle(futures[fut], [], f"unhandled: {type(e).__name__}: {e}", 0)
                if i % 10 == 0 or i == len(pending):
                    print(f"  [{i}/{len(pending)}] events_so_far={total_events} errors={errors}")

    con.close()
    return {"cached": cached, "called": len(pending), "events": total_events, "errors": errors}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="C:/QueryPat/database/unified.sqlite")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    summary = run(Path(args.db), args.limit, args.workers)
    print()
    print("Summary:", summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
