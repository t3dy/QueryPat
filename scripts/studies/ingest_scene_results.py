"""
Ingest Claude Desktop App results back into the database.

Reads JSON result files from results/ directory and updates
ai_scene_candidates accordingly.

Usage:
    python ingest_scene_results.py --stage validate
    python ingest_scene_results.py --stage classify
    python ingest_scene_results.py --stage summarize
"""

import json
import sqlite3
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_DB = PROJECT_DIR / 'database' / 'unified.sqlite'
RESULTS_DIR = Path(__file__).resolve().parent / 'results'


def ingest_validation_results(db: sqlite3.Connection):
    """Ingest validation results: update promotion_status on candidates."""
    result_files = sorted(RESULTS_DIR.glob('validate_batch_*_result.json'))
    if not result_files:
        print("    No validation result files found")
        return

    validated = 0
    rejected = 0

    for rpath in result_files:
        with open(rpath, 'r', encoding='utf-8') as f:
            results = json.load(f)

        for item in results:
            cid = item['candidate_id']
            if item.get('is_valid'):
                db.execute("""
                    UPDATE ai_scene_candidates
                    SET promotion_status = 'validated'
                    WHERE candidate_id = ?
                """, (cid,))
                validated += 1
            else:
                db.execute("""
                    UPDATE ai_scene_candidates
                    SET promotion_status = 'rejected',
                        rejection_reason = ?
                    WHERE candidate_id = ?
                """, (item.get('rejection_reason', 'unknown'), cid))
                rejected += 1

    db.commit()
    print(f"    Validation: {validated} validated, {rejected} rejected")


def ingest_classification_results(db: sqlite3.Connection):
    """Ingest classification results. Stored in result files for later use by promote_scenes.py."""
    result_files = sorted(RESULTS_DIR.glob('classify_batch_*_result.json'))
    if not result_files:
        print("    No classification result files found")
        return

    total = 0
    for rpath in result_files:
        with open(rpath, 'r', encoding='utf-8') as f:
            results = json.load(f)
        total += len(results)

    print(f"    Classification: {total} results available in {len(result_files)} files")
    print("    (Classification data is read directly by promote_scenes.py)")


def ingest_summarize_results(db: sqlite3.Connection):
    """Ingest summarize results. Stored in result files for later use by promote_scenes.py."""
    result_files = sorted(RESULTS_DIR.glob('summarize_batch_*_result.json'))
    if not result_files:
        print("    No summarize result files found")
        return

    total = 0
    for rpath in result_files:
        with open(rpath, 'r', encoding='utf-8') as f:
            results = json.load(f)
        total += len(results)

    print(f"    Summarize: {total} results available in {len(result_files)} files")
    print("    (Summary data is read directly by promote_scenes.py)")


def run(db: sqlite3.Connection, _source: Path = None, stage: str = 'validate'):
    """Ingest results for the specified stage."""
    print(f"  Ingesting scene results (stage: {stage})...")

    if stage == 'validate':
        ingest_validation_results(db)
    elif stage == 'classify':
        ingest_classification_results(db)
    elif stage == 'summarize':
        ingest_summarize_results(db)
    else:
        print(f"    ERROR: Unknown stage '{stage}'")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Ingest Claude Desktop results')
    parser.add_argument('--db', type=Path, default=DEFAULT_DB)
    parser.add_argument('--stage', choices=['validate', 'classify', 'summarize'],
                        default='validate')
    args = parser.parse_args()

    db = sqlite3.connect(str(args.db))
    db.execute("PRAGMA foreign_keys = ON")
    run(db, stage=args.stage)
    db.close()
