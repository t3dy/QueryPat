#!/usr/bin/env python3
"""
Study Pipeline Orchestrator

Runs the full study pipeline with checkpointing.
Supports both deterministic-only and Claude-assisted modes.

Usage:
    python scripts/studies/study_pipeline.py                    # full pipeline
    python scripts/studies/study_pipeline.py --deterministic    # no Claude calls
    python scripts/studies/study_pipeline.py --study ai         # one study only
    python scripts/studies/study_pipeline.py --step classify    # one step only
"""

import argparse
import sqlite3
import sys
import time
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

PROJECT_DIR = SCRIPTS_DIR.parent
DEFAULT_DB = PROJECT_DIR / 'database' / 'unified.sqlite'

STEPS = [
    # (step_name, module_path, is_deterministic, description)
    ('ontology',      'studies.ontology',             True,  'Seed study ontologies'),
    ('scan',          'studies.scan_corpus',           True,  'Scan corpus for topic matches'),
    ('link',          'studies.link_studies',           True,  'Cross-link topics to terms/names/docs'),
    ('classify',      'studies.classify_passages',     False, 'Classify passages with Claude'),
    ('evidence',      'studies.build_evidence_packets', False, 'Build evidence packets with Claude'),
    ('contradictions', 'studies.detect_contradictions', False, 'Detect contradictions with Claude'),
    ('dossiers',      'studies.draft_dossiers',        False, 'Draft topic dossiers with Claude'),
    ('fair_use',      'studies.review_fair_use',       False, 'Review fair-use compliance'),
    ('export',        'studies.export_studies',         True,  'Export study JSON'),
]


def run_step(step_name: str, module_path: str, db: sqlite3.Connection,
             source: Path = None):
    """Import and run a single pipeline step."""
    try:
        parts = module_path.rsplit('.', 1)
        mod = __import__(module_path, fromlist=[parts[-1]])
        mod.run(db, source)
        return True
    except ImportError as e:
        print(f"    SKIP: {step_name} not available ({e})")
        return False
    except Exception as e:
        print(f"    ERROR in {step_name}: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(description='Study Pipeline Orchestrator')
    parser.add_argument('--db', type=Path, default=DEFAULT_DB)
    parser.add_argument('--source', type=Path, default=Path('C:/ExegesisAnalysis'))
    parser.add_argument('--deterministic', action='store_true',
                        help='Run deterministic steps only (no Claude)')
    parser.add_argument('--study', type=str, choices=['ai', 'psychology'],
                        help='Process one study only')
    parser.add_argument('--step', type=str,
                        choices=[s[0] for s in STEPS],
                        help='Run a single step')

    args = parser.parse_args()

    print("=" * 60)
    print("STUDY PIPELINE")
    print("=" * 60)
    print(f"  Database: {args.db}")
    print(f"  Mode: {'deterministic' if args.deterministic else 'full'}")
    if args.study:
        print(f"  Study: {args.study}")
    if args.step:
        print(f"  Step: {args.step}")

    start = time.time()
    db = sqlite3.connect(str(args.db))
    db.execute("PRAGMA journal_mode = WAL")
    db.execute("PRAGMA foreign_keys = ON")

    steps_to_run = STEPS
    if args.step:
        steps_to_run = [s for s in STEPS if s[0] == args.step]
    if args.deterministic:
        steps_to_run = [s for s in steps_to_run if s[2]]

    results = {}
    for step_name, module_path, is_det, desc in steps_to_run:
        print(f"\n--- {desc} ---")
        step_start = time.time()
        ok = run_step(step_name, module_path, db, args.source)
        step_elapsed = time.time() - step_start
        results[step_name] = {'ok': ok, 'time': step_elapsed}
        print(f"    {'OK' if ok else 'FAILED'} ({step_elapsed:.1f}s)")

    db.close()
    elapsed = time.time() - start

    print("\n" + "=" * 60)
    print("PIPELINE SUMMARY")
    print("=" * 60)
    for name, r in results.items():
        status = 'OK' if r['ok'] else 'FAILED'
        print(f"  {name:20s} {status:8s} {r['time']:6.1f}s")
    print(f"\nTotal: {elapsed:.1f}s")


if __name__ == '__main__':
    main()
