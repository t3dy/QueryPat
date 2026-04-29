"""
Promote validated, classified, and summarized candidates into ai_scenes.

Reads classification and summary results from results/ directory,
joins them with validated candidates, and inserts into ai_scenes +
ai_scene_participants tables.

Usage:
    python promote_scenes.py [--db path/to/unified.sqlite]
"""

import json
import sqlite3
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_DB = PROJECT_DIR / 'database' / 'unified.sqlite'
RESULTS_DIR = Path(__file__).resolve().parent / 'results'


def load_results(pattern: str) -> dict:
    """Load all result files matching pattern into a dict keyed by candidate_id."""
    merged = {}
    for rpath in sorted(RESULTS_DIR.glob(pattern)):
        with open(rpath, 'r', encoding='utf-8') as f:
            for item in json.load(f):
                cid = item.get('candidate_id')
                if cid is not None:
                    merged[cid] = item
    return merged


def resolve_name_id(db: sqlite3.Connection, label: str, work_title: str):
    """Try to match a participant label to a names table entry."""
    # Exact match on canonical name
    row = db.execute("""
        SELECT name_id FROM names
        WHERE canonical_name = ? AND source_type IN ('fiction', 'both')
        LIMIT 1
    """, (label,)).fetchone()
    if row:
        return row[0]

    # Try alias match
    row = db.execute("""
        SELECT n.name_id FROM names n
        JOIN name_aliases na ON n.name_id = na.name_id
        WHERE na.alias = ? AND n.source_type IN ('fiction', 'both')
        LIMIT 1
    """, (label,)).fetchone()
    if row:
        return row[0]

    return None


def run(db: sqlite3.Connection, _source: Path = None):
    """Promote validated candidates with full enrichment into ai_scenes."""
    print("  Promoting validated scenes...")

    # Load all result sets
    classify_data = load_results('classify_batch_*_result.json')
    summary_data = load_results('summarize_batch_*_result.json')

    if not classify_data or not summary_data:
        print("    ERROR: Need both classification and summary results")
        print(f"    Classification results: {len(classify_data)}")
        print(f"    Summary results: {len(summary_data)}")
        return

    # Get validated candidates
    candidates = db.execute("""
        SELECT candidate_id, work_id, work_title, doc_id,
               page_start, page_end, char_offset_start, char_offset_end,
               source_window_text
        FROM ai_scene_candidates
        WHERE promotion_status = 'validated'
          AND promoted_scene_id IS NULL
    """).fetchall()

    if not candidates:
        print("    No candidates ready for promotion")
        return

    # Determine next scene number
    max_row = db.execute("""
        SELECT scene_id FROM ai_scenes
        ORDER BY scene_id DESC LIMIT 1
    """).fetchone()
    if max_row and max_row[0].startswith('SCENE_'):
        next_num = int(max_row[0].replace('SCENE_', '')) + 1
    else:
        next_num = 1

    promoted = 0
    skipped = 0

    for row in candidates:
        cid = row[0]
        work_id, work_title, doc_id = row[1], row[2], row[3]
        page_start, page_end = row[4], row[5]
        char_start, char_end = row[6], row[7]
        source_text = row[8]

        cls = classify_data.get(cid)
        summ = summary_data.get(cid)

        if not cls or not summ:
            skipped += 1
            continue

        scene_id = f'SCENE_{next_num:03d}'
        next_num += 1

        # Insert scene
        db.execute("""
            INSERT INTO ai_scenes
                (scene_id, candidate_id, scene_label, work_id, work_title, doc_id,
                 page_start, page_end, char_offset_start, char_offset_end,
                 source_window_text,
                 interaction_type, interaction_type_secondary,
                 short_summary, significance, source_excerpt,
                 editorial_status, fair_use_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'machine-drafted', 'pending')
        """, (
            scene_id, cid,
            summ.get('scene_label', 'Untitled scene'),
            work_id, work_title, doc_id,
            page_start, page_end, char_start, char_end,
            source_text,
            cls.get('interaction_type', 'unknown'),
            cls.get('interaction_type_secondary'),
            summ.get('short_summary', ''),
            summ.get('significance'),
            summ.get('source_excerpt'),
        ))

        # Insert participants
        for p in cls.get('participants', []):
            name_id = resolve_name_id(db, p['label'], work_title)
            db.execute("""
                INSERT OR IGNORE INTO ai_scene_participants
                    (scene_id, name_id, participant_label, participant_role)
                VALUES (?, ?, ?, ?)
            """, (scene_id, name_id, p['label'], p.get('role', 'human')))

        # Update candidate with promotion link
        db.execute("""
            UPDATE ai_scene_candidates
            SET promoted_scene_id = ?
            WHERE candidate_id = ?
        """, (scene_id, cid))

        promoted += 1

    db.commit()
    print(f"    Promoted {promoted} scenes, skipped {skipped} (missing results)")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Promote validated candidates to scenes')
    parser.add_argument('--db', type=Path, default=DEFAULT_DB)
    args = parser.parse_args()

    db = sqlite3.connect(str(args.db))
    db.execute("PRAGMA foreign_keys = ON")
    run(db)
    db.close()
