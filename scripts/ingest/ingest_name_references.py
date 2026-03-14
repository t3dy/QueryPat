"""
Load mini knowledge base from curated CSV files in database/reference_data/.

These are reference entries for biblical, classical, gnostic, and philosophical
names that PKD may allude to. They provide etymology, origin language, and
scholarly context for cross-referencing against extracted names.
"""

import csv
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from date_norms import make_ref_id


# Map of CSV filename stems to domain values
DOMAIN_FILES = {
    'biblical_names': 'biblical',
    'classical_names': 'classical',
    'gnostic_names': 'gnostic',
    'philosophical_names': 'philosophical',
}


def run(db: sqlite3.Connection, source_dir: Path):
    print("Loading name reference knowledge base...")

    # Ensure table exists
    db.execute("""
        CREATE TABLE IF NOT EXISTS name_references (
            ref_id TEXT PRIMARY KEY, canonical_form TEXT NOT NULL,
            domain TEXT NOT NULL, brief TEXT NOT NULL,
            etymology TEXT, origin_language TEXT,
            significance TEXT, source_text TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)

    ref_dir = Path('C:/QueryPat/database/reference_data')
    if not ref_dir.exists():
        print(f"  SKIP: {ref_dir} not found")
        return

    total = 0
    for stem, domain in DOMAIN_FILES.items():
        csv_path = ref_dir / f"{stem}.csv"
        if not csv_path.exists():
            print(f"  SKIP: {csv_path.name} not found")
            continue

        count = 0
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                canonical = row['canonical_form'].strip()
                if not canonical:
                    continue

                ref_id = make_ref_id(domain, canonical)

                try:
                    db.execute("""
                        INSERT OR REPLACE INTO name_references
                            (ref_id, canonical_form, domain, brief,
                             etymology, origin_language, significance, source_text)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        ref_id, canonical, domain,
                        row.get('brief', '').strip(),
                        row.get('etymology', '').strip() or None,
                        row.get('origin_language', '').strip() or None,
                        row.get('significance', '').strip() or None,
                        row.get('source_text', '').strip() or None,
                    ))
                    count += 1
                except sqlite3.IntegrityError as e:
                    print(f"    WARN: {canonical}: {e}")

        total += count
        print(f"  {domain}: {count} entries from {csv_path.name}")

    db.commit()
    print(f"  Total reference entries: {total}")


if __name__ == '__main__':
    db_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('C:/QueryPat/database/unified.sqlite')
    db = sqlite3.connect(str(db_path))
    run(db, Path('C:/ExegesisAnalysis'))
    db.close()
