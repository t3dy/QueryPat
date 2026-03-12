"""
Stage 1: Ingest extraction CSVs into the database.

Reads:
  - {source}/extraction/entity_mentions.csv   → term_segments (conceptual links)
  - {source}/extraction/concept_glossary.csv  → terms (supplements canonical)
  - {source}/extraction/timeline.csv          → timeline_events
"""

import csv
import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from date_norms import normalize_date, make_term_id, make_seg_id, make_event_id, make_slug


def ingest_entity_mentions(db: sqlite3.Connection, source_dir: Path):
    """Ingest entity_mentions.csv as term_segments links."""
    csv_path = source_dir / 'extraction' / 'entity_mentions.csv'
    if not csv_path.exists():
        print(f"  SKIP: {csv_path} not found")
        return 0

    count = 0
    skipped = 0

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            entity_name = row.get('entity_name', '').strip()
            chunk_id = row.get('chunk_id', '').strip()
            if not entity_name or not chunk_id:
                skipped += 1
                continue

            term_id = make_term_id(entity_name)
            seg_id = make_seg_id('EXEG', chunk_id)

            # Only link if both term and segment exist
            term_exists = db.execute(
                "SELECT 1 FROM terms WHERE term_id = ?", (term_id,)
            ).fetchone()
            seg_exists = db.execute(
                "SELECT 1 FROM segments WHERE seg_id = ?", (seg_id,)
            ).fetchone()

            if not term_exists or not seg_exists:
                skipped += 1
                continue

            context = row.get('context_snippet', '')

            try:
                db.execute("""
                    INSERT OR IGNORE INTO term_segments (
                        term_id, seg_id, match_type, link_confidence, link_method,
                        matched_text, context_snippet
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    term_id, seg_id,
                    'conceptual',
                    4,  # summary concept mapping
                    'entity_extraction_csv',
                    entity_name,
                    context[:500] if context else None,
                ))
                count += 1
            except sqlite3.IntegrityError:
                skipped += 1

    db.commit()
    print(f"  Ingested {count} entity mention links ({skipped} skipped)")
    return count


def ingest_concept_glossary(db: sqlite3.Connection, source_dir: Path):
    """Ingest concept_glossary.csv — supplements canonical terms with definitions."""
    csv_path = source_dir / 'extraction' / 'concept_glossary.csv'
    if not csv_path.exists():
        print(f"  SKIP: {csv_path} not found")
        return 0

    count = 0
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            concept_term = row.get('concept_term', '').strip()
            if not concept_term:
                continue

            term_id = make_term_id(concept_term)
            definition = row.get('definition_in_context', '').strip()

            # Update existing term with definition if it doesn't have one
            if definition:
                db.execute("""
                    UPDATE terms SET definition = ?
                    WHERE term_id = ? AND (definition IS NULL OR definition = '')
                """, (definition, term_id))

            # Add variant terms as aliases
            variants = row.get('variant_terms', '').strip()
            if variants:
                for variant in variants.split(','):
                    variant = variant.strip()
                    if variant and variant != concept_term:
                        try:
                            db.execute("""
                                INSERT OR IGNORE INTO term_aliases (term_id, alias_text, alias_type)
                                VALUES (?, ?, ?)
                            """, (term_id, variant, 'alternate_name'))
                        except sqlite3.IntegrityError:
                            pass

            count += 1

    db.commit()
    print(f"  Processed {count} glossary concepts")
    return count


def ingest_timeline(db: sqlite3.Connection, source_dir: Path):
    """Ingest timeline.csv into timeline_events."""
    csv_path = source_dir / 'extraction' / 'timeline.csv'
    if not csv_path.exists():
        print(f"  SKIP: {csv_path} not found")
        return 0

    count = 0
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            timeline_id = row.get('timeline_id', '').strip()
            if not timeline_id:
                continue

            event_id = make_event_id(timeline_id)

            nd = normalize_date(
                row.get('date_text'),
                iso_hint=row.get('iso_date_if_inferable'),
                basis='timeline_extraction',
            )

            # Map event_type to allowed values
            raw_type = row.get('event_type', 'other').strip().lower()
            event_type_map = {
                'mystical': 'vision',
                'autobiographical': 'biographical',
                'philosophical': 'philosophical',
                'literary': 'writing',
                'publication': 'publication',
            }
            event_type = event_type_map.get(raw_type, 'other')

            # Map confidence text
            raw_conf = row.get('confidence', '').strip().lower()
            conf_map = {'high': 'exact', 'medium': 'approximate', 'low': 'inferred'}
            confidence = conf_map.get(raw_conf, 'inferred')

            chunk_id = row.get('chunk_id', '').strip()
            seg_id = make_seg_id('EXEG', chunk_id) if chunk_id else None
            section_id = row.get('section_id', '').strip()

            db.execute("""
                INSERT OR REPLACE INTO timeline_events (
                    event_id, event_type, event_summary,
                    date_start, date_end, date_display, date_confidence, date_basis,
                    seg_id, confidence, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                event_id, event_type,
                row.get('event_summary', ''),
                nd.date_start, nd.date_end, nd.date_display,
                nd.date_confidence, nd.date_basis,
                seg_id,
                confidence,
                None,
            ))
            count += 1

    db.commit()
    print(f"  Ingested {count} timeline events")
    return count


def run(db: sqlite3.Connection, source_dir: Path):
    """Run extraction ingestion."""
    print("Stage 1: Ingesting extraction CSVs...")
    ingest_entity_mentions(db, source_dir)
    ingest_concept_glossary(db, source_dir)
    ingest_timeline(db, source_dir)


if __name__ == '__main__':
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('C:/ExegesisAnalysis')
    db_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('C:/QueryPat/database/unified.sqlite')
    db = sqlite3.connect(str(db_path))
    run(db, source)
    db.close()
