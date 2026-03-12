"""
Stage 1: Ingest PaulPKDarchive catalog into documents and assets tables.

Reads: {source}/PaulPKDarchive/catalog.json → documents (doc_type varies) + assets
"""

import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from date_norms import normalize_date, make_doc_id, make_asset_id, make_slug


# Map archive categories to document doc_types
CATEGORY_TO_DOCTYPE = {
    'scholarship': 'scholarship',
    'novels': 'novel',
    'short stories': 'short_story',
    'letters': 'letter',
    'interviews': 'interview',
    'biographies': 'biography',
    'newspaper & press': 'newspaper',
    'fan publications': 'fan_publication',
    'primary sources': 'archive_pdf',
    'other': 'other',
}

# Default extraction priority by category
CATEGORY_INGEST_LEVEL = {
    'scholarship': 'full',
    'letters': 'full',
    'interviews': 'full',
    'primary sources': 'full',
    'novels': 'metadata_only',
    'short stories': 'metadata_only',
    'biographies': 'metadata_only',
    'newspaper & press': 'partial',
    'fan publications': 'partial',
    'other': 'metadata_only',
}


def ingest_archive(db: sqlite3.Connection, source_dir: Path):
    """Ingest catalog.json into documents and assets."""
    catalog_path = source_dir / 'PaulPKDarchive' / 'catalog.json'
    if not catalog_path.exists():
        print(f"  SKIP: {catalog_path} not found")
        return 0

    with open(catalog_path, 'r', encoding='utf-8') as f:
        entries = json.load(f)

    doc_count = 0
    asset_count = 0

    for entry in entries:
        entry_id = entry.get('id', '').strip()
        if not entry_id:
            continue

        # Skip duplicates
        if entry.get('is_duplicate'):
            continue

        # Skip unprocessed/errored entries
        if not entry.get('processed') or entry.get('error'):
            continue

        # Numeric suffix for doc_id
        doc_id = make_doc_id('ARCH', entry_id.upper().replace('-', '_')[:40])

        category = (entry.get('category') or 'other').lower()
        doc_type = CATEGORY_TO_DOCTYPE.get(category, 'archive_pdf')
        ingest_level = CATEGORY_INGEST_LEVEL.get(category, 'metadata_only')

        nd = normalize_date(
            entry.get('date'),
            basis='archive_catalog',
        )

        is_pkd = 1 if entry.get('is_pkd_authored') else 0

        db.execute("""
            INSERT OR REPLACE INTO documents (
                doc_id, doc_type, title, slug,
                author, recipient,
                date_start, date_end, date_display, date_confidence, date_basis,
                timeline_type,
                ingest_level, extraction_status,
                is_pkd_authored,
                page_count, category,
                card_summary, page_summary,
                source_filename, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            doc_id, doc_type,
            entry.get('display_title', entry_id),
            entry_id,
            entry.get('author'),
            None,  # no recipient for archive docs
            nd.date_start, nd.date_end, nd.date_display,
            nd.date_confidence, nd.date_basis,
            'publication',
            ingest_level,
            'pending',
            is_pkd,
            entry.get('total_pages'),
            category,
            entry.get('card_summary'),
            entry.get('page_summary'),
            entry.get('filename'),
            None,
        ))
        doc_count += 1

        # Create asset for the PDF
        filename = entry.get('filename', '')
        if filename:
            asset_id = make_asset_id(make_slug(entry_id)[:50])
            pdf_path = f"PaulPKDarchive/PKDpdf/{filename}"

            db.execute("""
                INSERT OR REPLACE INTO assets (
                    asset_id, doc_id, asset_type, file_path, mime_type
                ) VALUES (?, ?, ?, ?, ?)
            """, (
                asset_id, doc_id, 'pdf', pdf_path, 'application/pdf',
            ))

            db.execute("""
                INSERT OR IGNORE INTO document_assets (doc_id, asset_id, role)
                VALUES (?, ?, ?)
            """, (doc_id, asset_id, 'source'))

            asset_count += 1

    db.commit()
    print(f"  Ingested {doc_count} archive documents, {asset_count} assets")
    return doc_count


def run(db: sqlite3.Connection, source_dir: Path):
    """Run archive ingestion."""
    print("Stage 1: Ingesting archive catalog...")
    ingest_archive(db, source_dir)


if __name__ == '__main__':
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('C:/ExegesisAnalysis')
    db_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('C:/QueryPat/database/unified.sqlite')
    db = sqlite3.connect(str(db_path))
    run(db, source)
    db.close()
