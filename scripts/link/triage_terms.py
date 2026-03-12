"""
Stage 2: Triage terms based on evidence quality, frequency, and descriptions.

Applies status rules:
  - Terms with hand-written descriptions (>200 chars, human-revised) → 'accepted'
  - Terms with LLM descriptions (>100 chars) → 'provisional'
  - Terms with high frequency (>=50) but no description → 'provisional'
  - Terms with moderate frequency (10-49) → 'background'
  - Terms with low frequency (<10) and no evidence → 'rejected'
  - Known aliases → 'alias'
"""

import sqlite3
import sys
from pathlib import Path


def run(db: sqlite3.Connection, source_dir: Path):
    print("Stage 2: Triaging terms...")

    cursor = db.cursor()

    # Step 1: Promote terms with substantial descriptions to accepted
    cursor.execute("""
        UPDATE terms SET status = 'accepted'
        WHERE review_state IN ('human-revised', 'publication-ready')
        AND (full_description IS NOT NULL AND length(full_description) > 200)
    """)
    accepted = cursor.rowcount
    print(f"  Accepted (human-revised with descriptions): {accepted}")

    # Step 2: Terms with LLM descriptions → provisional
    cursor.execute("""
        UPDATE terms SET status = 'provisional'
        WHERE status NOT IN ('accepted')
        AND review_state = 'machine-drafted'
        AND (card_description IS NOT NULL AND length(card_description) > 100)
    """)
    provisional_desc = cursor.rowcount
    print(f"  Provisional (machine-drafted descriptions): {provisional_desc}")

    # Step 3: High-frequency terms without descriptions → provisional
    cursor.execute("""
        UPDATE terms SET status = 'provisional'
        WHERE status NOT IN ('accepted', 'provisional')
        AND mention_count >= 50
    """)
    provisional_freq = cursor.rowcount
    print(f"  Provisional (high frequency >=50): {provisional_freq}")

    # Step 4: Moderate frequency → background
    cursor.execute("""
        UPDATE terms SET status = 'background'
        WHERE status NOT IN ('accepted', 'provisional')
        AND mention_count >= 10
    """)
    background = cursor.rowcount
    print(f"  Background (moderate frequency 10-49): {background}")

    # Step 5: Low frequency with no evidence at all → rejected
    cursor.execute("""
        UPDATE terms SET status = 'rejected'
        WHERE status NOT IN ('accepted', 'provisional', 'background')
        AND mention_count < 5
        AND term_id NOT IN (SELECT DISTINCT term_id FROM evidence_packets)
        AND term_id NOT IN (SELECT DISTINCT term_id FROM term_segments)
    """)
    rejected = cursor.rowcount
    print(f"  Rejected (low frequency, no evidence): {rejected}")

    # Step 6: Mark alias terms
    # Find terms that are aliases of other terms via the term_aliases table
    cursor.execute("""
        UPDATE terms SET status = 'alias'
        WHERE canonical_name IN (
            SELECT alias_text FROM term_aliases
        )
        AND status NOT IN ('accepted', 'provisional')
    """)
    aliased = cursor.rowcount
    print(f"  Alias (name matches another term's alias): {aliased}")

    db.commit()

    # Summary
    for status in ['accepted', 'provisional', 'background', 'alias', 'rejected']:
        count = db.execute("SELECT COUNT(*) FROM terms WHERE status = ?", (status,)).fetchone()[0]
        print(f"    Total {status}: {count}")


if __name__ == '__main__':
    db_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('C:/QueryPat/database/unified.sqlite')
    db = sqlite3.connect(str(db_path))
    run(db, Path('C:/ExegesisAnalysis'))
    db.close()
