"""
Stage 1: Ingest section and chunk manifests into documents and segments tables.

Reads:
  - {source}/manifests/section_manifest.csv → documents (doc_type='exegesis_section')
  - {source}/manifests/chunk_manifest.csv   → segments  (seg_type='chunk')
"""

import csv
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from date_norms import normalize_date, make_doc_id, make_seg_id


def ingest_sections(db: sqlite3.Connection, source_dir: Path):
    """Ingest section_manifest.csv into documents table."""
    csv_path = source_dir / 'manifests' / 'section_manifest.csv'
    if not csv_path.exists():
        print(f"  SKIP: {csv_path} not found")
        return 0

    count = 0
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            section_id = row['section_id']
            doc_id = make_doc_id('EXEG', section_id)

            nd = normalize_date(
                row.get('date_text'),
                iso_hint=row.get('iso_date_if_inferable'),
                basis='manifest_header',
            )

            # Parse word count from notes like "5602 words"
            word_count = None
            notes = row.get('notes', '')
            if notes and 'words' in notes:
                try:
                    word_count = int(notes.replace(' words', '').replace(',', ''))
                except ValueError:
                    pass

            section_type = row.get('section_type', '')
            timeline_type = 'letter' if section_type == 'Letter' else 'composition'

            db.execute("""
                INSERT OR REPLACE INTO documents (
                    doc_id, doc_type, title, slug,
                    author, recipient,
                    date_start, date_end, date_display, date_confidence, date_basis, timeline_type,
                    word_count, section_order, section_type, source_filename, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                doc_id,
                'exegesis_section',
                row.get('section_title', section_id),
                section_id.lower().replace('_', '-'),
                'Philip K. Dick',
                row.get('recipient'),
                nd.date_start, nd.date_end, nd.date_display,
                nd.date_confidence, nd.date_basis,
                timeline_type,
                word_count,
                int(row.get('section_order', 0)),
                section_type,
                row.get('source_filename'),
                notes,
            ))
            count += 1

    db.commit()
    print(f"  Ingested {count} sections into documents")
    return count


def ingest_chunks(db: sqlite3.Connection, source_dir: Path):
    """Ingest chunk_manifest.csv into segments table."""
    csv_path = source_dir / 'manifests' / 'chunk_manifest.csv'
    if not csv_path.exists():
        print(f"  SKIP: {csv_path} not found")
        return 0

    count = 0
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            chunk_id = row['chunk_id']
            section_id = row['section_id']
            doc_id = make_doc_id('EXEG', section_id)
            seg_id = make_seg_id('EXEG', chunk_id)

            nd = normalize_date(
                row.get('date_text'),
                basis='chunk_manifest',
            )

            word_count = None
            wc_raw = row.get('word_count', '')
            if wc_raw:
                try:
                    word_count = int(wc_raw)
                except ValueError:
                    pass

            overlap_prev = int(row.get('overlap_previous', 0) or 0)
            overlap_next = int(row.get('overlap_next', 0) or 0)
            position = int(row.get('chunk_order_within_section', 0) or 0)

            db.execute("""
                INSERT OR REPLACE INTO segments (
                    seg_id, doc_id, seg_type, position, slug,
                    date_start, date_end, date_display, date_confidence, date_basis,
                    title, word_count, overlap_previous, overlap_next, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                seg_id,
                doc_id,
                'chunk',
                position,
                chunk_id.lower().replace('_', '-'),
                nd.date_start, nd.date_end, nd.date_display,
                nd.date_confidence, nd.date_basis,
                row.get('filename', chunk_id),
                word_count,
                overlap_prev,
                overlap_next,
                row.get('notes'),
            ))
            count += 1

    db.commit()
    print(f"  Ingested {count} chunks into segments")
    return count


def run(db: sqlite3.Connection, source_dir: Path):
    """Run manifest ingestion."""
    print("Stage 1: Ingesting manifests...")
    ingest_sections(db, source_dir)
    ingest_chunks(db, source_dir)


if __name__ == '__main__':
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('C:/ExegesisAnalysis')
    db_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('C:/QueryPat/database/unified.sqlite')

    schema_path = db_path.parent / 'unified_schema.sql'
    db = sqlite3.connect(str(db_path))
    if schema_path.exists():
        db.executescript(schema_path.read_text(encoding='utf-8'))
    run(db, source)
    db.close()
