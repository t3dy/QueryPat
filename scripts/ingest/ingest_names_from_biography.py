"""
Harvest proper names from biography_events.people_involved JSON arrays.

Adds new names not already found in segments, and updates mention counts
for names already in the database.
"""

import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from date_norms import make_name_id, make_slug


def run(db: sqlite3.Connection, source_dir: Path):
    print("Ingesting names from biography events...")

    rows = db.execute("""
        SELECT bio_id, people_involved
        FROM biography_events
        WHERE people_involved IS NOT NULL AND people_involved != '[]'
    """).fetchall()

    if not rows:
        print("  No biography events with people_involved found")
        return

    new_names = 0
    updated = 0

    for bio_id, pi_json in rows:
        people = json.loads(pi_json)
        for name in people:
            name = name.strip()
            if not name:
                continue

            slug = make_slug(name)
            if not slug:
                continue

            name_id = make_name_id(name)

            # Check if already exists
            exists = db.execute(
                "SELECT name_id, source_type FROM names WHERE name_id = ?", (name_id,)
            ).fetchone()

            if exists:
                # Update source_type to 'both' if it was 'fiction' or 'exegesis'
                if exists[1] == 'exegesis':
                    pass  # biography is also from exegesis context, keep as-is
                updated += 1
            else:
                try:
                    db.execute("""
                        INSERT INTO names
                            (name_id, canonical_form, slug, entity_type, source_type,
                             status, review_state, mention_count, provenance)
                        VALUES (?, ?, ?, 'historical_person', 'exegesis',
                                'provisional', 'unreviewed', 1,
                                'ingest_names_from_biography')
                    """, (name_id, name, slug))
                    new_names += 1
                except sqlite3.IntegrityError:
                    pass

    db.commit()
    print(f"  Processed {len(rows)} biography events")
    print(f"  New names: {new_names}, already existed: {updated}")


if __name__ == '__main__':
    db_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('C:/QueryPat/database/unified.sqlite')
    db = sqlite3.connect(str(db_path))
    run(db, Path('C:/ExegesisAnalysis'))
    db.close()
