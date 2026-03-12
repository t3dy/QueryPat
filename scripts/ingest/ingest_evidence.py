"""
Stage 1: Ingest evidence packets into evidence_packets and evidence_excerpts tables.

Reads: {source}/ExegesisBrowser/data/intermediate/evidence_packets/*.json
"""

import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from date_norms import make_term_id, make_slug


def ingest_evidence_packets(db: sqlite3.Connection, source_dir: Path):
    """Ingest evidence packet JSON files."""
    packets_dir = source_dir / 'ExegesisBrowser' / 'data' / 'intermediate' / 'evidence_packets'
    if not packets_dir.exists():
        print(f"  SKIP: {packets_dir} not found")
        return 0

    packet_count = 0
    excerpt_count = 0

    for json_path in sorted(packets_dir.glob('*.json')):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError):
            print(f"  WARN: Could not parse {json_path.name}")
            continue

        term_name = data.get('term', '').strip()
        if not term_name:
            continue

        term_id = make_term_id(term_name)
        term_slug = make_slug(term_name)

        # Check if term exists
        row = db.execute("SELECT 1 FROM terms WHERE term_id = ?", (term_id,)).fetchone()
        if not row:
            continue

        passages = data.get('passages', [])
        total_count = data.get('count', len(passages))

        # Create one evidence packet per term (aggregated)
        ev_id = f"EV_{term_slug}_corpus"

        db.execute("""
            INSERT OR REPLACE INTO evidence_packets (
                ev_id, term_id, claim_text, evidence_summary,
                confidence, source_method, editorial_status
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            ev_id, term_id,
            f"{term_name} appears {total_count} times in the Exegesis corpus",
            f"Extracted {len(passages)} representative passages via frequency mining",
            'moderate',
            'deterministic',
            'unreviewed',
        ))
        packet_count += 1

        # Insert individual excerpts
        for i, passage in enumerate(passages):
            excerpt_text = passage.get('excerpt', '').strip()
            if not excerpt_text:
                continue

            line_start = passage.get('line_start')
            line_end = passage.get('line_end')
            folder_id = passage.get('folder_id', '')
            matched_alias = passage.get('matched_alias', term_name)

            db.execute("""
                INSERT INTO evidence_excerpts (
                    ev_id, excerpt_text, line_start, line_end,
                    folder_id, matched_alias
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                ev_id,
                excerpt_text[:2000],  # cap length
                line_start,
                line_end,
                folder_id if folder_id and folder_id != 'Unknown' else None,
                matched_alias,
            ))
            excerpt_count += 1

    db.commit()
    print(f"  Ingested {packet_count} evidence packets, {excerpt_count} excerpts")
    return packet_count


def run(db: sqlite3.Connection, source_dir: Path):
    """Run evidence packet ingestion."""
    print("Stage 1: Ingesting evidence packets...")
    ingest_evidence_packets(db, source_dir)


if __name__ == '__main__':
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('C:/ExegesisAnalysis')
    db_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('C:/QueryPat/database/unified.sqlite')
    db = sqlite3.connect(str(db_path))
    run(db, source)
    db.close()
