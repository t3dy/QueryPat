"""
Stage 2: Cross-link and validate the database.

- Build term<->term relationships from co-occurrence in evidence packets
- Build term<->term relationships from see_also fields
- Validate foreign key integrity
- Flag anomalies
"""

import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from date_norms import make_term_id


def build_see_also_links(db: sqlite3.Connection):
    """Create term<->term relationships from see_also JSON arrays."""
    cursor = db.cursor()

    rows = cursor.execute("""
        SELECT term_id, canonical_name, see_also FROM terms
        WHERE see_also IS NOT NULL AND see_also != '[]'
    """).fetchall()

    count = 0
    for term_id, term_name, see_also_json in rows:
        try:
            related = json.loads(see_also_json)
        except json.JSONDecodeError:
            continue

        for related_name in related:
            if not related_name or related_name == term_name:
                continue

            related_id = make_term_id(related_name)

            # Check if related term exists
            exists = db.execute(
                "SELECT 1 FROM terms WHERE term_id = ?", (related_id,)
            ).fetchone()
            if not exists:
                continue

            try:
                db.execute("""
                    INSERT OR IGNORE INTO term_terms (
                        term_id_a, term_id_b, relation_type,
                        link_confidence, link_method
                    ) VALUES (?, ?, ?, ?, ?)
                """, (term_id, related_id, 'related', 3, 'see_also_field'))
                count += 1
            except sqlite3.IntegrityError:
                pass

    db.commit()
    print(f"  Created {count} term<->term links from see_also")
    return count


def validate_integrity(db: sqlite3.Connection):
    """Check for data integrity issues."""
    issues = []

    # Check for segments referencing non-existent documents
    orphan_segs = db.execute("""
        SELECT COUNT(*) FROM segments s
        WHERE NOT EXISTS (SELECT 1 FROM documents d WHERE d.doc_id = s.doc_id)
    """).fetchone()[0]
    if orphan_segs:
        issues.append(f"  WARN: {orphan_segs} segments reference non-existent documents")

    # Check for duplicate slugs in terms
    dup_slugs = db.execute("""
        SELECT slug, COUNT(*) as cnt FROM terms
        GROUP BY slug HAVING cnt > 1
    """).fetchall()
    for slug, cnt in dup_slugs:
        issues.append(f"  WARN: Duplicate term slug '{slug}' ({cnt} terms)")

    # Check for terms with suspiciously high match counts
    high_count = db.execute("""
        SELECT canonical_name, mention_count FROM terms
        WHERE mention_count > 5000
        ORDER BY mention_count DESC
    """).fetchall()
    for name, count in high_count:
        issues.append(f"  NOTE: Very high frequency term '{name}' ({count} mentions)")

    if issues:
        for issue in issues:
            print(issue)
    else:
        print("  No integrity issues found")

    return issues


def run(db: sqlite3.Connection, source_dir: Path):
    print("Stage 2: Linking and validating...")
    build_see_also_links(db)
    validate_integrity(db)


if __name__ == '__main__':
    db_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('C:/QueryPat/database/unified.sqlite')
    db = sqlite3.connect(str(db_path))
    run(db, Path('C:/ExegesisAnalysis'))
    db.close()
