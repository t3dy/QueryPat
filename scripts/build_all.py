#!/usr/bin/env python3
"""
QueryPat Build Orchestrator

Runs the full ingest → link → enrich → export pipeline.

Usage:
    python build_all.py [OPTIONS]

Options:
    --source DIR           Source data directory (default: C:/ExegesisAnalysis)
    --db PATH              SQLite database path (default: database/unified.sqlite)
    --deterministic-only   Run stages 1-2 only (no LLM enrichment)
    --skip-llm             Run stages 1-2 + export (no LLM enrichment)
    --export-only          JSON export from existing SQLite
    --audit-only           Validation report only
    --fresh                Drop and recreate database before running
"""

import argparse
import sqlite3
import sys
import time
from pathlib import Path

# Ensure scripts directory is importable
SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS_DIR))

PROJECT_DIR = SCRIPTS_DIR.parent
DEFAULT_SOURCE = Path('C:/ExegesisAnalysis')
DEFAULT_DB = PROJECT_DIR / 'database' / 'unified.sqlite'


def init_db(db_path: Path, fresh: bool = False) -> sqlite3.Connection:
    """Initialize the database with schema."""
    schema_path = PROJECT_DIR / 'database' / 'unified_schema.sql'

    if fresh and db_path.exists():
        db_path.unlink()
        print(f"Removed existing database: {db_path}")

    db = sqlite3.connect(str(db_path))
    db.execute("PRAGMA journal_mode = WAL")
    db.execute("PRAGMA foreign_keys = ON")

    if fresh or not db_path.exists():
        if schema_path.exists():
            db.executescript(schema_path.read_text(encoding='utf-8'))
            print(f"Initialized database from {schema_path}")
        else:
            print(f"ERROR: Schema not found at {schema_path}")
            sys.exit(1)

    return db


def run_stage_1(db: sqlite3.Connection, source: Path):
    """Stage 1: Deterministic extraction."""
    print("\n" + "=" * 60)
    print("STAGE 1: DETERMINISTIC EXTRACTION")
    print("=" * 60)

    from ingest.ingest_manifests import run as ingest_manifests
    from ingest.ingest_summaries import run as ingest_summaries
    from ingest.ingest_canonical import run as ingest_canonical
    from ingest.ingest_extraction import run as ingest_extraction
    from ingest.ingest_evidence import run as ingest_evidence
    from ingest.ingest_archive import run as ingest_archive

    ingest_manifests(db, source)
    ingest_summaries(db, source)
    ingest_canonical(db, source)
    ingest_extraction(db, source)
    ingest_evidence(db, source)
    ingest_archive(db, source)

    from ingest.ingest_chat_seeds import run as ingest_chat_seeds
    ingest_chat_seeds(db, source)

    from ingest.ingest_biography import run as ingest_biography
    ingest_biography(db, source)


def run_stage_2(db: sqlite3.Connection, source: Path):
    """Stage 2: Heuristic linking."""
    print("\n" + "=" * 60)
    print("STAGE 2: HEURISTIC LINKING")
    print("=" * 60)

    try:
        from link.triage_terms import run as triage_terms
        triage_terms(db, source)
    except ImportError:
        print("  SKIP: triage_terms not yet implemented")

    try:
        from link.compute_chronology import run as compute_chronology
        compute_chronology(db, source)
    except ImportError:
        print("  SKIP: compute_chronology not yet implemented")

    try:
        from link.link_and_validate import run as link_and_validate
        link_and_validate(db, source)
    except ImportError:
        print("  SKIP: link_and_validate not yet implemented")


def run_stage_3(db: sqlite3.Connection, source: Path):
    """Stage 3: LLM enrichment (skippable)."""
    print("\n" + "=" * 60)
    print("STAGE 3: LLM ENRICHMENT")
    print("=" * 60)
    print("  (Not yet implemented — skipping)")


def run_stage_4(db: sqlite3.Connection, source: Path):
    """Stage 4: Editorial overrides."""
    print("\n" + "=" * 60)
    print("STAGE 4: EDITORIAL OVERRIDES")
    print("=" * 60)

    overrides_path = SCRIPTS_DIR / 'overrides' / 'term_overrides.json'
    if not overrides_path.exists():
        print("  No overrides file found — skipping")
        return

    import json
    with open(overrides_path, 'r', encoding='utf-8') as f:
        overrides = json.load(f)

    from date_norms import make_term_id

    applied = 0
    for override in overrides:
        term_name = override.get('term', '')
        term_id = make_term_id(term_name)
        op = override.get('operation', '')

        if op == 'replace_definition':
            db.execute("UPDATE terms SET full_description = ?, review_state = 'human-revised' WHERE term_id = ?",
                       (override.get('value'), term_id))
            applied += 1
        elif op == 'set_status':
            db.execute("UPDATE terms SET status = ? WHERE term_id = ?",
                       (override.get('value'), term_id))
            applied += 1
        elif op == 'add_note':
            db.execute("""
                INSERT INTO annotations (target_type, target_id, annotation_type, content, provenance)
                VALUES ('term', ?, 'note', ?, 'editorial_override')
            """, (term_id, override.get('value')))
            applied += 1

    db.commit()
    print(f"  Applied {applied} editorial overrides")


def run_audit(db: sqlite3.Connection):
    """Run validation audit."""
    print("\n" + "=" * 60)
    print("AUDIT")
    print("=" * 60)

    try:
        from audit import run as audit
        audit(db, PROJECT_DIR)
    except ImportError:
        # Inline basic audit
        checks = [
            ("Documents", "SELECT COUNT(*) FROM documents"),
            ("Segments", "SELECT COUNT(*) FROM segments"),
            ("Terms", "SELECT COUNT(*) FROM terms"),
            ("  - accepted", "SELECT COUNT(*) FROM terms WHERE status = 'accepted'"),
            ("  - provisional", "SELECT COUNT(*) FROM terms WHERE status = 'provisional'"),
            ("  - background", "SELECT COUNT(*) FROM terms WHERE status = 'background'"),
            ("  - alias", "SELECT COUNT(*) FROM terms WHERE status = 'alias'"),
            ("  - rejected", "SELECT COUNT(*) FROM terms WHERE status = 'rejected'"),
            ("Term aliases", "SELECT COUNT(*) FROM term_aliases"),
            ("Term-segment links", "SELECT COUNT(*) FROM term_segments"),
            ("Evidence packets", "SELECT COUNT(*) FROM evidence_packets"),
            ("Evidence excerpts", "SELECT COUNT(*) FROM evidence_excerpts"),
            ("Timeline events", "SELECT COUNT(*) FROM timeline_events"),
            ("Assets", "SELECT COUNT(*) FROM assets"),
            ("Annotations", "SELECT COUNT(*) FROM annotations"),
            ("", ""),
            ("Orphan terms (no evidence)", "SELECT COUNT(*) FROM terms t WHERE NOT EXISTS (SELECT 1 FROM evidence_packets ep WHERE ep.term_id = t.term_id) AND NOT EXISTS (SELECT 1 FROM term_segments ts WHERE ts.term_id = t.term_id)"),
            ("Segments without dates", "SELECT COUNT(*) FROM segments WHERE date_start IS NULL"),
            ("Documents without dates", "SELECT COUNT(*) FROM documents WHERE date_start IS NULL"),
        ]

        for label, query in checks:
            if not query:
                print()
                continue
            try:
                result = db.execute(query).fetchone()[0]
                print(f"  {label}: {result}")
            except Exception as e:
                print(f"  {label}: ERROR - {e}")


def run_export(db: sqlite3.Connection):
    """Export JSON artifacts."""
    print("\n" + "=" * 60)
    print("JSON EXPORT")
    print("=" * 60)

    try:
        from export_json import run as export_json
        export_json(db, PROJECT_DIR)
    except ImportError:
        print("  SKIP: export_json not yet implemented")


def main():
    parser = argparse.ArgumentParser(description='QueryPat Build Orchestrator')
    parser.add_argument('--source', type=Path, default=DEFAULT_SOURCE,
                        help='Source data directory')
    parser.add_argument('--db', type=Path, default=DEFAULT_DB,
                        help='SQLite database path')
    parser.add_argument('--deterministic-only', action='store_true',
                        help='Run stages 1-2 only')
    parser.add_argument('--skip-llm', action='store_true',
                        help='Run stages 1-2 + export, no LLM enrichment')
    parser.add_argument('--export-only', action='store_true',
                        help='JSON export from existing SQLite')
    parser.add_argument('--audit-only', action='store_true',
                        help='Validation report only')
    parser.add_argument('--fresh', action='store_true',
                        help='Drop and recreate database')

    args = parser.parse_args()

    print(f"QueryPat Build Pipeline")
    print(f"  Source: {args.source}")
    print(f"  Database: {args.db}")
    print(f"  Mode: {'fresh' if args.fresh else 'incremental'}")

    start = time.time()

    if args.audit_only:
        db = sqlite3.connect(str(args.db))
        run_audit(db)
        db.close()
        return

    if args.export_only:
        db = sqlite3.connect(str(args.db))
        run_export(db)
        db.close()
        return

    db = init_db(args.db, fresh=args.fresh)

    # Stage 1: always run
    run_stage_1(db, args.source)

    # Stage 2: always run
    run_stage_2(db, args.source)

    if args.deterministic_only:
        run_audit(db)
        db.close()
        elapsed = time.time() - start
        print(f"\nDone (deterministic only) in {elapsed:.1f}s")
        return

    if not args.skip_llm:
        run_stage_3(db, args.source)

    run_stage_4(db, args.source)
    run_audit(db)
    run_export(db)

    db.close()
    elapsed = time.time() - start
    print(f"\nDone in {elapsed:.1f}s")


if __name__ == '__main__':
    main()
