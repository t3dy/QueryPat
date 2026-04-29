"""
Prepare batch JSON files for Claude Desktop App processing.

Reads ai_scene_candidates and writes batch files to batches/ directory.
Re-entrant: checks promotion_status and only generates batches for the
current pipeline stage.

Usage:
    python prepare_scene_batches.py --stage validate   # Stage 1
    python prepare_scene_batches.py --stage classify    # Stage 2 (after ingesting validation results)
    python prepare_scene_batches.py --stage summarize   # Stage 3 (after ingesting classification results)
"""

import json
import sqlite3
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_DB = PROJECT_DIR / 'database' / 'unified.sqlite'
BATCHES_DIR = Path(__file__).resolve().parent / 'batches'
RESULTS_DIR = Path(__file__).resolve().parent / 'results'

# Batch sizes tuned for Claude Desktop context window
BATCH_SIZES = {
    'validate': 10,    # short output per item
    'classify': 6,     # medium output per item
    'summarize': 4,    # long output per item
}


def prepare_validate_batches(db: sqlite3.Connection):
    """Stage 1: Prepare validation batches from pending candidates."""
    rows = db.execute("""
        SELECT candidate_id, work_title, source_window_text, matched_terms,
               matched_interaction
        FROM ai_scene_candidates
        WHERE promotion_status = 'pending'
        ORDER BY work_title, candidate_id
    """).fetchall()

    if not rows:
        print("    No pending candidates to validate")
        return

    batch_size = BATCH_SIZES['validate']
    batch_num = 0

    for i in range(0, len(rows), batch_size):
        chunk = rows[i:i + batch_size]
        batch = []
        for cid, title, text, terms_json, interaction in chunk:
            batch.append({
                'candidate_id': cid,
                'work_title': title,
                'source_window_text': text,
                'matched_terms': json.loads(terms_json) if terms_json else [],
                'matched_interaction': interaction,
            })
        batch_num += 1
        out_path = BATCHES_DIR / f'validate_batch_{batch_num:03d}.json'
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(batch, f, indent=2, ensure_ascii=False)

    print(f"    Wrote {batch_num} validation batches ({len(rows)} candidates)")
    print(f"    Location: {BATCHES_DIR}/validate_batch_*.json")
    print(f"    Use prompt: prompts/scene_prompt_1_validate.md")
    print(f"    Save results to: results/validate_batch_NNN_result.json")


def prepare_classify_batches(db: sqlite3.Connection):
    """Stage 2: Prepare classification batches from validated candidates."""
    rows = db.execute("""
        SELECT candidate_id, work_title, source_window_text
        FROM ai_scene_candidates
        WHERE promotion_status = 'validated'
        ORDER BY work_title, candidate_id
    """).fetchall()

    if not rows:
        print("    No validated candidates to classify")
        return

    batch_size = BATCH_SIZES['classify']
    batch_num = 0

    for i in range(0, len(rows), batch_size):
        chunk = rows[i:i + batch_size]
        batch = []
        for cid, title, text in chunk:
            batch.append({
                'candidate_id': cid,
                'work_title': title,
                'source_window_text': text,
            })
        batch_num += 1
        out_path = BATCHES_DIR / f'classify_batch_{batch_num:03d}.json'
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(batch, f, indent=2, ensure_ascii=False)

    print(f"    Wrote {batch_num} classification batches ({len(rows)} candidates)")
    print(f"    Location: {BATCHES_DIR}/classify_batch_*.json")
    print(f"    Use prompt: prompts/scene_prompt_2_classify.md")
    print(f"    Save results to: results/classify_batch_NNN_result.json")


def prepare_summarize_batches(db: sqlite3.Connection):
    """Stage 3: Prepare summarize batches from classified candidates.

    Reads classification results that have already been ingested (stored
    in results/ as classify_batch_*_result.json with participants and types).
    """
    # Load all ingested classification results
    classified = {}
    for rpath in sorted(RESULTS_DIR.glob('classify_batch_*_result.json')):
        with open(rpath, 'r', encoding='utf-8') as f:
            for item in json.load(f):
                classified[item['candidate_id']] = item

    if not classified:
        print("    No classification results found in results/")
        return

    rows = db.execute("""
        SELECT candidate_id, work_title, source_window_text
        FROM ai_scene_candidates
        WHERE promotion_status = 'validated'
          AND candidate_id IN ({})
    """.format(','.join('?' * len(classified))),
        list(classified.keys())
    ).fetchall()

    if not rows:
        print("    No validated candidates with classification results")
        return

    batch_size = BATCH_SIZES['summarize']
    batch_num = 0

    for i in range(0, len(rows), batch_size):
        chunk = rows[i:i + batch_size]
        batch = []
        for cid, title, text in chunk:
            cls = classified.get(cid, {})
            batch.append({
                'candidate_id': cid,
                'work_title': title,
                'source_window_text': text,
                'participants': cls.get('participants', []),
                'interaction_type': cls.get('interaction_type', 'unknown'),
                'interaction_type_secondary': cls.get('interaction_type_secondary'),
            })
        batch_num += 1
        out_path = BATCHES_DIR / f'summarize_batch_{batch_num:03d}.json'
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(batch, f, indent=2, ensure_ascii=False)

    print(f"    Wrote {batch_num} summarize batches ({len(rows)} candidates)")
    print(f"    Location: {BATCHES_DIR}/summarize_batch_*.json")
    print(f"    Use prompt: prompts/scene_prompt_3_summarize.md")
    print(f"    Save results to: results/summarize_batch_NNN_result.json")


def run(db: sqlite3.Connection, _source: Path = None, stage: str = 'validate'):
    """Prepare batches for the specified stage."""
    print(f"  Preparing scene batches (stage: {stage})...")
    BATCHES_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    if stage == 'validate':
        prepare_validate_batches(db)
    elif stage == 'classify':
        prepare_classify_batches(db)
    elif stage == 'summarize':
        prepare_summarize_batches(db)
    else:
        print(f"    ERROR: Unknown stage '{stage}'. Use: validate, classify, summarize")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Prepare scene batches for Claude Desktop')
    parser.add_argument('--db', type=Path, default=DEFAULT_DB)
    parser.add_argument('--stage', choices=['validate', 'classify', 'summarize'],
                        default='validate',
                        help='Pipeline stage to prepare batches for')
    args = parser.parse_args()

    db = sqlite3.connect(str(args.db))
    db.execute("PRAGMA foreign_keys = ON")
    run(db, stage=args.stage)
    db.close()
