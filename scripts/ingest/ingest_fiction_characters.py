"""
Ingest PKD fiction characters from curated CSV reference file.

Reads database/reference_data/fiction_characters.csv and creates:
  - names rows with entity_type='character', source_type='fiction'
  - name_references rows with domain='literary'
  - Deduplicates against existing names (updates if already present)
  - Aggregates work_list for characters appearing in multiple works
"""

import csv
import json
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from date_norms import make_name_id, make_slug, make_ref_id


def run(db: sqlite3.Connection, source_dir: Path):
    print("Ingesting fiction characters from CSV...")

    csv_path = Path('C:/QueryPat/database/reference_data/fiction_characters.csv')
    if not csv_path.exists():
        print(f"  SKIP: {csv_path} not found")
        return

    # Read and aggregate by character (some appear in multiple works)
    characters = {}  # slug → aggregated data
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            canonical = row['canonical_form'].strip()
            if not canonical:
                continue

            slug = make_slug(canonical)
            work = row.get('work', '').strip()

            if slug not in characters:
                characters[slug] = {
                    'canonical': canonical,
                    'slug': slug,
                    'etymology': row.get('etymology', '').strip() or None,
                    'wordplay_note': row.get('wordplay_note', '').strip() or None,
                    'brief': row.get('brief', '').strip() or None,
                    'significance': row.get('significance', '').strip() or None,
                    'works': [],
                }

            if work and work not in characters[slug]['works']:
                characters[slug]['works'].append(work)

    inserted = 0
    updated = 0
    refs_added = 0

    for slug, char in characters.items():
        name_id = make_name_id(char['canonical'])
        first_work = char['works'][0] if char['works'] else None
        work_list = json.dumps(char['works']) if char['works'] else None

        # Check if name already exists
        existing = db.execute(
            "SELECT name_id, entity_type, source_type FROM names WHERE name_id = ?",
            (name_id,)
        ).fetchone()

        if existing:
            # Update existing entry: upgrade to character type, add fiction data
            updates = []
            params = []

            # Only upgrade entity_type if not already character
            if existing[1] != 'character':
                updates.append("entity_type = 'character'")

            # Set source_type to 'both' if it was 'exegesis', otherwise 'fiction'
            if existing[2] == 'exegesis':
                updates.append("source_type = 'both'")
            elif existing[2] is None:
                updates.append("source_type = 'fiction'")

            # Always update these fields from the CSV
            if char['etymology']:
                updates.append("etymology = ?")
                params.append(char['etymology'])
            if char['wordplay_note']:
                updates.append("wordplay_note = ?")
                params.append(char['wordplay_note'])
            if first_work:
                updates.append("first_work = COALESCE(first_work, ?)")
                params.append(first_work)
            if work_list:
                updates.append("work_list = ?")
                params.append(work_list)

            updates.append("updated_at = datetime('now')")

            if updates:
                sql = f"UPDATE names SET {', '.join(updates)} WHERE name_id = ?"
                params.append(name_id)
                db.execute(sql, params)
                updated += 1
        else:
            # Insert new character
            try:
                db.execute("""
                    INSERT INTO names
                        (name_id, canonical_form, slug, entity_type, source_type,
                         status, review_state, etymology, wordplay_note,
                         mention_count, first_work, work_list, provenance)
                    VALUES (?, ?, ?, 'character', 'fiction',
                            'provisional', 'machine-drafted', ?, ?,
                            0, ?, ?, 'ingest_fiction_characters')
                """, (name_id, char['canonical'], slug,
                      char['etymology'], char['wordplay_note'],
                      first_work, work_list))
                inserted += 1
            except sqlite3.IntegrityError as e:
                print(f"    WARN: {char['canonical']}: {e}")

        # Create/update reference entry
        ref_id = make_ref_id('literary', char['canonical'])
        if char['brief']:
            try:
                db.execute("""
                    INSERT OR REPLACE INTO name_references
                        (ref_id, canonical_form, domain, brief,
                         etymology, origin_language, significance, source_text)
                    VALUES (?, ?, 'literary', ?, ?, NULL, ?, ?)
                """, (ref_id, char['canonical'], char['brief'],
                      char['etymology'], char['significance'],
                      ', '.join(char['works']) if char['works'] else None))
                refs_added += 1
            except sqlite3.IntegrityError as e:
                print(f"    WARN ref: {char['canonical']}: {e}")

        # Link the reference to the name
        db.execute("""
            UPDATE names SET reference_id = ? WHERE name_id = ? AND reference_id IS NULL
        """, (ref_id, name_id))

    db.commit()
    print(f"  Fiction characters: {inserted} inserted, {updated} updated")
    print(f"  Reference entries: {refs_added} added")
    print(f"  Total processed: {len(characters)}")


if __name__ == '__main__':
    db_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('C:/QueryPat/database/unified.sqlite')
    db = sqlite3.connect(str(db_path))
    run(db, Path('C:/ExegesisAnalysis'))
    db.close()
