"""
Stage 0: Import pre-extracted archive PDF text into canonical SQLite.

Reads texts.json (and new_texts*.json) from PaulPKDarchive.
Populates document_texts table and updates document extraction metadata.

Does NOT perform PDF extraction itself — that was already done by
PaulPKDarchive/extract_texts.py using PyMuPDF.
"""

import json
import sqlite3
import string
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from date_norms import make_slug


def compute_extractability(text: str) -> float:
    """Compute extractability score as ratio of printable ASCII to total chars."""
    if not text:
        return 0.0
    printable = sum(1 for c in text if c in string.printable)
    return round(printable / len(text), 3)


def ingest_texts_file(db: sqlite3.Connection, json_path: Path, source_label: str):
    """Import a single texts JSON file into document_texts."""
    if not json_path.exists():
        print(f"  SKIP: {json_path} not found")
        return 0, 0

    with open(json_path, 'r', encoding='utf-8') as f:
        entries = json.load(f)

    imported = 0
    skipped = 0

    for entry in entries:
        entry_id = entry.get('id', '')
        text = entry.get('text')
        is_scanned = entry.get('scanned', False)
        filename = entry.get('filename', '')

        if not entry_id:
            skipped += 1
            continue

        # Find matching document by slug match
        doc_slug = make_slug(entry_id)
        doc = db.execute(
            "SELECT doc_id FROM documents WHERE slug = ? OR source_filename = ?",
            (doc_slug, filename)
        ).fetchone()

        if not doc:
            # Try partial match on source_filename
            if filename:
                doc = db.execute(
                    "SELECT doc_id FROM documents WHERE source_filename LIKE ?",
                    (f'%{filename}%',)
                ).fetchone()

        if not doc:
            skipped += 1
            continue

        doc_id = doc[0]
        text_id = f"TEXT_{doc_slug}"

        if text:
            char_count = len(text)
            score = compute_extractability(text)
            ocr_needed = 0
        else:
            char_count = 0
            score = 0.0
            ocr_needed = 1 if is_scanned else 0

        extraction_status = 'complete' if text else ('failed' if is_scanned else 'pending')

        db.execute("""
            INSERT OR REPLACE INTO document_texts (
                text_id, doc_id, extraction_method, extraction_status,
                extractability_score, ocr_required, text_content, char_count
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            text_id, doc_id, 'pre_extracted', extraction_status,
            score, ocr_needed, text, char_count,
        ))

        # Update document-level extraction metadata
        db.execute("""
            UPDATE documents SET
                extractability_score = ?,
                ocr_required = ?,
                extraction_status = ?,
                text_char_count = ?
            WHERE doc_id = ?
        """, (
            int(score * 100) if score else None,
            ocr_needed,
            extraction_status,
            char_count if char_count else None,
            doc_id,
        ))

        imported += 1

    db.commit()
    print(f"  {source_label}: {imported} imported, {skipped} skipped")
    return imported, skipped


def run(db: sqlite3.Connection, source_dir: Path):
    """Import all available text extraction files."""
    print("Stage 0: Importing archive PDF texts...")

    archive_dir = source_dir / 'PaulPKDarchive'

    total_imported = 0
    total_skipped = 0

    # Main texts.json
    n, s = ingest_texts_file(db, archive_dir / 'texts.json', 'texts.json')
    total_imported += n
    total_skipped += s

    # new_texts batch files
    for batch_file in sorted(archive_dir.glob('new_texts*.json')):
        n, s = ingest_texts_file(db, batch_file, batch_file.name)
        total_imported += n
        total_skipped += s

    # Report extraction coverage
    total_docs = db.execute(
        "SELECT COUNT(*) FROM documents WHERE doc_type != 'exegesis_section'"
    ).fetchone()[0]
    has_text = db.execute(
        "SELECT COUNT(*) FROM document_texts WHERE text_content IS NOT NULL"
    ).fetchone()[0]
    ocr_needed = db.execute(
        "SELECT COUNT(*) FROM document_texts WHERE ocr_required = 1"
    ).fetchone()[0]
    print(f"  Total: {total_imported} texts imported ({total_skipped} unmatched)")
    print(f"  Coverage: {has_text}/{total_docs} archive docs have extracted text")
    print(f"  OCR needed: {ocr_needed} documents flagged as scanned")


if __name__ == '__main__':
    db_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('C:/QueryPat/database/unified.sqlite')
    db = sqlite3.connect(str(db_path))
    run(db, Path('C:/ExegesisAnalysis'))
    db.close()
