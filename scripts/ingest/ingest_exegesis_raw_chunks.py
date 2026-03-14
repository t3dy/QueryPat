"""
Stage 0: Import raw Exegesis chunk text into segments.raw_text.

Reads all .txt files from {source}/chunks/ and populates raw_text
for existing segments. Creates new segment records for chunks that
exist as text files but aren't in the manifest.
"""

import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from date_norms import make_seg_id, normalize_date


def run(db: sqlite3.Connection, source_dir: Path):
    """Import all raw chunk text files into segments."""
    print("Stage 0: Importing raw Exegesis chunk texts...")

    chunks_dir = source_dir / 'chunks'
    if not chunks_dir.exists():
        print(f"  SKIP: {chunks_dir} not found")
        return

    txt_files = sorted(chunks_dir.glob('*.txt'))
    print(f"  Found {len(txt_files)} text chunk files")

    updated = 0
    created = 0
    errors = 0

    for txt_path in txt_files:
        chunk_id = txt_path.stem  # e.g. "1975-02-27_Claudia_01"
        seg_id = make_seg_id('EXEG', chunk_id)

        try:
            text = txt_path.read_text(encoding='utf-8')
        except (UnicodeDecodeError, OSError):
            try:
                text = txt_path.read_text(encoding='latin-1')
            except OSError:
                errors += 1
                continue

        char_count = len(text)

        # Check if segment exists
        existing = db.execute(
            "SELECT seg_id FROM segments WHERE seg_id = ?", (seg_id,)
        ).fetchone()

        if existing:
            # Update raw_text on existing segment
            db.execute("""
                UPDATE segments SET
                    raw_text = ?,
                    raw_text_source = ?,
                    raw_text_char_count = ?
                WHERE seg_id = ?
            """, (text, str(txt_path.name), char_count, seg_id))
            updated += 1
        else:
            # Create new segment for orphan chunk — find a valid parent doc
            nd = normalize_date(None)
            doc_id = None

            # Parse filename pattern: YYYY-MM-DD_Name_NN or U_Name_NN
            parts = chunk_id.split('_')
            if len(parts) >= 3 and len(parts[0]) == 10:
                nd = normalize_date(parts[0], basis='chunk_filename')

            # Try to find parent doc from SECTION in filename
            for part in parts:
                if part.startswith('SECTION'):
                    candidate = f'DOC_EXEG_{part}'
                    if db.execute("SELECT 1 FROM documents WHERE doc_id = ?", (candidate,)).fetchone():
                        doc_id = candidate
                        break

            # Skip if no valid parent doc found (FK constraint)
            if not doc_id:
                errors += 1
                continue

            db.execute("""
                INSERT OR IGNORE INTO segments (
                    seg_id, doc_id, seg_type, slug, title,
                    date_start, date_end, date_display, date_confidence, date_basis,
                    raw_text, raw_text_source, raw_text_char_count
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                seg_id, doc_id, 'chunk',
                chunk_id.lower().replace('_', '-'),
                txt_path.name,
                nd.date_start, nd.date_end, nd.date_display,
                nd.date_confidence, nd.date_basis,
                text, str(txt_path.name), char_count,
            ))
            created += 1

    db.commit()

    # Report coverage
    total_segs = db.execute("SELECT COUNT(*) FROM segments").fetchone()[0]
    has_raw = db.execute(
        "SELECT COUNT(*) FROM segments WHERE raw_text IS NOT NULL"
    ).fetchone()[0]
    has_summary = db.execute(
        "SELECT COUNT(*) FROM segments WHERE concise_summary IS NOT NULL"
    ).fetchone()[0]

    print(f"  Updated {updated} existing segments with raw text")
    print(f"  Created {created} new segments from orphan chunks")
    if errors:
        print(f"  Errors: {errors} files could not be read")
    print(f"  Coverage: {has_raw}/{total_segs} segments have raw text")
    print(f"  Summaries: {has_summary}/{total_segs} segments have summaries")


if __name__ == '__main__':
    db_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('C:/QueryPat/database/unified.sqlite')
    db = sqlite3.connect(str(db_path))
    run(db, Path('C:/ExegesisAnalysis'))
    db.close()
