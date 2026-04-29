#!/usr/bin/env python3
"""
Layer 2 Pilot: Fair-use review — deterministic.
Auto-approves short passages, trims long ones.
"""

import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent.parent / 'database' / 'unified.sqlite'

PILOT_TOPICS = [
    'TOPIC_AI_androids',
    'TOPIC_AI_simulation',
    'TOPIC_PSY_paranoia',
    'TOPIC_PSY_anamnesis',
]

MAX_FAIR_USE_CHARS = 500
AUTO_APPROVE_CHARS = 300


def main():
    db = sqlite3.connect(str(DB))

    for tid in PILOT_TOPICS:
        db.execute("UPDATE study_passages SET fair_use_status = 'pending' WHERE topic_id = ?", (tid,))
    db.commit()

    # Auto-approve short passages
    auto = 0
    for tid in PILOT_TOPICS:
        n = db.execute("""
            UPDATE study_passages SET fair_use_status = 'approved'
            WHERE topic_id = ? AND length(passage_text) <= ? AND fair_use_status = 'pending'
        """, (tid, AUTO_APPROVE_CHARS)).rowcount
        auto += n
    db.commit()
    print(f"  Auto-approved: {auto} passages (<= {AUTO_APPROVE_CHARS} chars)")

    # Trim passages that are too long
    trimmed = 0
    rows = db.execute("""
        SELECT passage_id, passage_text, topic_id
        FROM study_passages
        WHERE topic_id IN (?,?,?,?)
        AND length(passage_text) > ?
        AND fair_use_status = 'pending'
        ORDER BY passage_id
    """, (*PILOT_TOPICS, AUTO_APPROVE_CHARS)).fetchall()

    for pid, text, tid in rows:
        if len(text) <= MAX_FAIR_USE_CHARS:
            # Medium length — approve but note
            db.execute("UPDATE study_passages SET fair_use_status = 'approved' WHERE passage_id = ?", (pid,))
        else:
            # Too long — trim to MAX_FAIR_USE_CHARS at sentence boundary
            trimmed_text = text[:MAX_FAIR_USE_CHARS]
            # Try to end at a sentence
            last_period = trimmed_text.rfind('.')
            if last_period > MAX_FAIR_USE_CHARS * 0.6:
                trimmed_text = trimmed_text[:last_period + 1]
            else:
                trimmed_text = trimmed_text.rsplit(' ', 1)[0] + '...'

            db.execute("""
                UPDATE study_passages SET
                    fair_use_status = 'trimmed',
                    passage_text = ?,
                    notes = COALESCE(notes || '; ', '') || 'Fair-use trimmed from ' || ? || ' to ' || ? || ' chars'
                WHERE passage_id = ?
            """, (trimmed_text, len(text), len(trimmed_text), pid))
            trimmed += 1

    db.commit()

    # Report
    approved_total = db.execute("""
        SELECT COUNT(*) FROM study_passages
        WHERE topic_id IN (?,?,?,?) AND fair_use_status = 'approved'
    """, PILOT_TOPICS).fetchone()[0]

    trimmed_total = db.execute("""
        SELECT COUNT(*) FROM study_passages
        WHERE topic_id IN (?,?,?,?) AND fair_use_status = 'trimmed'
    """, PILOT_TOPICS).fetchone()[0]

    print(f"  Approved: {approved_total}")
    print(f"  Trimmed: {trimmed_total}")
    print(f"  Total trimmed this run: {trimmed}")

    # Show trim details
    trims = db.execute("""
        SELECT passage_id, topic_id, length(passage_text), notes
        FROM study_passages
        WHERE topic_id IN (?,?,?,?) AND fair_use_status = 'trimmed'
        ORDER BY passage_id LIMIT 10
    """, PILOT_TOPICS).fetchall()
    if trims:
        print(f"\n  --- Trim Details (first 10) ---")
        for t in trims:
            print(f"    P{t[0]} ({t[1]}): now {t[2]} chars — {t[3]}")

    print(f"\n=== FAIR-USE REVIEW COMPLETE ===")
    db.close()


if __name__ == '__main__':
    main()
