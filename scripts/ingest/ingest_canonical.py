"""
Stage 1: Ingest canonical terms and aliases into terms and term_aliases tables.

Reads:
  - {source}/ExegesisBrowser/data/intermediate/canonical_terms.csv → terms + term_aliases
  - {source}/ExegesisBrowser/data/intermediate/dictionary_expanded.json → term descriptions
"""

import csv
import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from date_norms import make_term_id, make_slug


def ingest_canonical_terms(db: sqlite3.Connection, source_dir: Path):
    """Ingest canonical_terms.csv into terms and term_aliases."""
    csv_path = source_dir / 'ExegesisBrowser' / 'data' / 'intermediate' / 'canonical_terms.csv'
    if not csv_path.exists():
        print(f"  SKIP: {csv_path} not found")
        return 0

    count = 0
    alias_count = 0

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            term_name = row['Term'].strip()
            if not term_name:
                continue

            term_id = make_term_id(term_name)
            slug = make_slug(term_name)

            mention_count = int(row.get('Count', 0) or 0)
            score = float(row.get('Score', 0) or 0)
            primary_cat = row.get('Primary Category', '')
            thematic_cats = row.get('Thematic Categories', '')

            # Initial status based on score and count
            if score >= 4:
                status = 'provisional'
            elif mention_count >= 50:
                status = 'provisional'
            elif mention_count >= 10:
                status = 'background'
            else:
                status = 'background'

            thematic_json = json.dumps([c.strip() for c in thematic_cats.split('/') if c.strip()]) if thematic_cats else None

            db.execute("""
                INSERT OR REPLACE INTO terms (
                    term_id, canonical_name, slug,
                    status, review_state,
                    primary_category, thematic_categories,
                    mention_count, score
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                term_id, term_name, slug,
                status, 'unreviewed',
                primary_cat, thematic_json,
                mention_count, score,
            ))
            count += 1

            # Parse aliases
            aliases_raw = row.get('Aliases', '').strip()
            if aliases_raw:
                for alias in aliases_raw.split(','):
                    alias = alias.strip()
                    if alias and alias != term_name:
                        try:
                            db.execute("""
                                INSERT OR IGNORE INTO term_aliases (term_id, alias_text, alias_type)
                                VALUES (?, ?, ?)
                            """, (term_id, alias, 'alternate_name'))
                            alias_count += 1
                        except sqlite3.IntegrityError:
                            pass

    db.commit()
    print(f"  Ingested {count} canonical terms, {alias_count} aliases")
    return count


def enrich_from_dictionary(db: sqlite3.Connection, source_dir: Path):
    """Enrich terms with descriptions from dictionary_expanded.json."""
    # Try multiple known locations
    candidates = [
        source_dir / 'ExegesisBrowser' / 'docs' / 'assets' / 'data' / 'dictionary_expanded.json',
        source_dir / 'ExegesisBrowser' / 'data' / 'intermediate' / 'dictionary_expanded.json',
    ]

    dict_path = None
    for c in candidates:
        if c.exists():
            dict_path = c
            break

    if not dict_path:
        print("  SKIP: dictionary_expanded.json not found")
        return 0

    with open(dict_path, 'r', encoding='utf-8') as f:
        entries = json.load(f)

    enriched = 0
    for entry in entries:
        term_name = entry.get('term', '').strip()
        if not term_name:
            continue

        term_id = make_term_id(term_name)

        # Check if term exists
        row = db.execute("SELECT term_id FROM terms WHERE term_id = ?", (term_id,)).fetchone()
        if not row:
            continue

        card_desc = entry.get('card_description', '')
        tech_def = entry.get('technical_definition', '')
        interp = entry.get('interpretive_note', '')
        see_also = entry.get('see_also', [])
        evidence_count = entry.get('evidence_count', 0)

        # If there's a substantial card_description, upgrade status
        review_state = 'unreviewed'
        status_update = None
        if card_desc and len(card_desc) > 100:
            review_state = 'machine-drafted'
            status_update = 'provisional'

        see_also_json = json.dumps(see_also) if see_also else None

        updates = {
            'definition': tech_def or None,
            'interpretive_note': interp or None,
            'card_description': card_desc or None,
            'full_description': card_desc or None,
            'see_also': see_also_json,
            'review_state': review_state,
        }

        set_clauses = ', '.join(f"{k} = ?" for k in updates)
        values = list(updates.values()) + [term_id]

        db.execute(f"UPDATE terms SET {set_clauses} WHERE term_id = ?", values)

        if status_update:
            db.execute("UPDATE terms SET status = ? WHERE term_id = ? AND status = 'background'",
                       (status_update, term_id))

        enriched += 1

    db.commit()
    print(f"  Enriched {enriched} terms from dictionary")
    return enriched


def run(db: sqlite3.Connection, source_dir: Path):
    """Run canonical term ingestion."""
    print("Stage 1: Ingesting canonical terms...")
    ingest_canonical_terms(db, source_dir)
    enrich_from_dictionary(db, source_dir)


if __name__ == '__main__':
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('C:/ExegesisAnalysis')
    db_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('C:/QueryPat/database/unified.sqlite')
    db = sqlite3.connect(str(db_path))
    run(db, source)
    db.close()
