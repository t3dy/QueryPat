"""
Stage 2: Ingest term co-occurrence data from evidence packets.

Each evidence passage has a co_occurrences array listing other terms
that appear nearby. This script ingests those as weighted edges in
term_cooccurrences, grounded in actual evidence passages.
"""

import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from date_norms import make_term_id


def run(db: sqlite3.Connection, source_dir: Path):
    """Ingest co-occurrence data from evidence packet JSON files."""
    print("Ingesting evidence co-occurrences...")

    packets_dir = source_dir / 'ExegesisBrowser' / 'data' / 'intermediate' / 'evidence_packets'
    if not packets_dir.exists():
        print(f"  SKIP: {packets_dir} not found")
        return

    # Get set of valid term_ids
    valid_terms = set(
        r[0] for r in db.execute("SELECT term_id FROM terms").fetchall()
    )

    pair_weights = {}  # (term_a, term_b) -> weight
    total_pairs = 0

    for json_path in sorted(packets_dir.glob('*.json')):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue

        term_name = data.get('term', '').strip()
        if not term_name:
            continue

        term_id_a = make_term_id(term_name)
        if term_id_a not in valid_terms:
            continue

        for passage in data.get('passages', []):
            co_terms = passage.get('co_occurrences', [])
            if not co_terms:
                continue

            for co_name in co_terms:
                if not isinstance(co_name, str):
                    continue
                term_id_b = make_term_id(co_name.strip())
                if term_id_b not in valid_terms or term_id_b == term_id_a:
                    continue

                # Normalize pair order for deduplication
                pair = tuple(sorted([term_id_a, term_id_b]))
                pair_weights[pair] = pair_weights.get(pair, 0) + 1.0
                total_pairs += 1

    # Insert co-occurrences
    inserted = 0
    for (term_a, term_b), weight in pair_weights.items():
        db.execute("""
            INSERT OR REPLACE INTO term_cooccurrences
                (term_id_a, term_id_b, weight, co_method)
            VALUES (?, ?, ?, ?)
        """, (term_a, term_b, weight, 'evidence_passage_cooccurrence'))
        inserted += 1

    db.commit()
    print(f"  Processed {total_pairs} raw co-occurrence pairs")
    print(f"  Inserted {inserted} unique co-occurrence edges")
    print(f"  Average weight: {sum(pair_weights.values()) / max(len(pair_weights), 1):.1f}")


if __name__ == '__main__':
    db_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('C:/QueryPat/database/unified.sqlite')
    db = sqlite3.connect(str(db_path))
    run(db, Path('C:/ExegesisAnalysis'))
    db.close()
