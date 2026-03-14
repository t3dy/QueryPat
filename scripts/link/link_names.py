"""
Link names to reference entries and dictionary terms.

Three linking passes:
1. Names → name_references: match canonical forms, copy etymology
2. Names → terms: string-match against term names and aliases
3. Name co-occurrence: names in same segment get co_occurs links
"""

import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from date_norms import make_slug


def run(db: sqlite3.Connection, source_dir: Path):
    print("Linking names to references and terms...")

    ref_matched = 0
    term_linked = 0
    cooccur_linked = 0

    # ── Pass 1: Match names to reference entries ──
    # Build lookup from reference canonical forms (case-insensitive)
    refs = db.execute("""
        SELECT ref_id, canonical_form, etymology, origin_language, domain
        FROM name_references
    """).fetchall()

    ref_lookup = {}  # lowercase canonical → (ref_id, etymology, origin_language, domain)
    for ref_id, canonical, etym, lang, domain in refs:
        ref_lookup[canonical.lower().strip()] = (ref_id, etym, lang, domain)

    # Match each name against references
    names = db.execute("""
        SELECT name_id, canonical_form, etymology, reference_id
        FROM names
    """).fetchall()

    for name_id, canonical, existing_etym, existing_ref in names:
        key = canonical.lower().strip()
        match = ref_lookup.get(key)

        # Also try without "St. " prefix
        if not match and key.startswith('st. '):
            match = ref_lookup.get(key[4:])
        # Try adding "St. "
        if not match:
            match = ref_lookup.get('st. ' + key)

        if match:
            ref_id, etym, lang, domain = match
            updates = []
            params = []

            if not existing_ref:
                updates.append("reference_id = ?")
                params.append(ref_id)
            if not existing_etym and etym:
                updates.append("etymology = ?")
                params.append(etym)
                updates.append("origin_language = ?")
                params.append(lang)

            # Set allusion_type based on domain
            if domain:
                updates.append("allusion_type = ?")
                params.append(f'["{domain}"]')

            if updates:
                params.append(name_id)
                db.execute(f"""
                    UPDATE names SET {', '.join(updates)}, updated_at = datetime('now')
                    WHERE name_id = ?
                """, params)
                ref_matched += 1

    db.commit()
    print(f"  Pass 1: Matched {ref_matched} names to reference entries")

    # ── Pass 2: Match names to dictionary terms ──
    # Build term lookup
    term_names = db.execute("""
        SELECT term_id, canonical_name FROM terms
        WHERE status IN ('accepted', 'provisional')
    """).fetchall()
    term_lookup = {}  # lowercase name → term_id
    for term_id, tname in term_names:
        term_lookup[tname.lower().strip()] = term_id

    # Also include term aliases
    term_aliases = db.execute("""
        SELECT ta.term_id, ta.alias_text
        FROM term_aliases ta
        JOIN terms t ON ta.term_id = t.term_id
        WHERE t.status IN ('accepted', 'provisional')
    """).fetchall()
    for term_id, alias in term_aliases:
        key = alias.lower().strip()
        if key not in term_lookup:
            term_lookup[key] = term_id

    # Ensure name_terms table exists
    db.execute("""
        CREATE TABLE IF NOT EXISTS name_terms (
            name_id TEXT NOT NULL, term_id TEXT NOT NULL,
            relation_type TEXT NOT NULL,
            link_confidence INTEGER, link_method TEXT,
            PRIMARY KEY (name_id, term_id, relation_type),
            FOREIGN KEY (name_id) REFERENCES names(name_id),
            FOREIGN KEY (term_id) REFERENCES terms(term_id)
        )
    """)

    for name_id, canonical, _, _ in names:
        key = canonical.lower().strip()
        term_id = term_lookup.get(key)

        if term_id:
            try:
                db.execute("""
                    INSERT OR IGNORE INTO name_terms
                        (name_id, term_id, relation_type, link_confidence, link_method)
                    VALUES (?, ?, 'discussed_alongside', 2, 'string_match')
                """, (name_id, term_id))
                term_linked += 1
            except sqlite3.IntegrityError:
                pass

    db.commit()
    print(f"  Pass 2: Linked {term_linked} names to dictionary terms")

    # ── Pass 3: Co-occurrence linking ──
    # Find names that appear in the same segment and create name_terms co_occurs
    # (only for names that are also linked to terms)
    name_segs = db.execute("""
        SELECT name_id, seg_id FROM name_segments
    """).fetchall()

    # Build seg_id → set of name_ids
    seg_to_names = {}
    for name_id, seg_id in name_segs:
        seg_to_names.setdefault(seg_id, set()).add(name_id)

    # For segments with multiple names, check if any pair links to terms
    name_to_terms = {}
    nt_rows = db.execute("SELECT name_id, term_id FROM name_terms").fetchall()
    for name_id, term_id in nt_rows:
        name_to_terms.setdefault(name_id, set()).add(term_id)

    # Create co-occurrence links between names that share segments
    seen_pairs = set()
    for seg_id, name_set in seg_to_names.items():
        name_list = sorted(name_set)
        for i, n1 in enumerate(name_list):
            for n2 in name_list[i+1:]:
                pair = (n1, n2)
                if pair in seen_pairs:
                    continue
                seen_pairs.add(pair)

                # Only link if both have terms (otherwise too noisy)
                if n1 in name_to_terms or n2 in name_to_terms:
                    # Check if n2 has any terms we can link n1 to
                    for term_id in name_to_terms.get(n2, set()):
                        try:
                            db.execute("""
                                INSERT OR IGNORE INTO name_terms
                                    (name_id, term_id, relation_type, link_confidence, link_method)
                                VALUES (?, ?, 'co_occurs', 4, 'segment_cooccurrence')
                            """, (n1, term_id))
                            cooccur_linked += 1
                        except sqlite3.IntegrityError:
                            pass
                    for term_id in name_to_terms.get(n1, set()):
                        try:
                            db.execute("""
                                INSERT OR IGNORE INTO name_terms
                                    (name_id, term_id, relation_type, link_confidence, link_method)
                                VALUES (?, ?, 'co_occurs', 4, 'segment_cooccurrence')
                            """, (n2, term_id))
                            cooccur_linked += 1
                        except sqlite3.IntegrityError:
                            pass

    db.commit()
    print(f"  Pass 3: Created {cooccur_linked} co-occurrence links")

    # Summary
    total_names = db.execute("SELECT COUNT(*) FROM names").fetchone()[0]
    total_refs = db.execute("SELECT COUNT(*) FROM names WHERE reference_id IS NOT NULL").fetchone()[0]
    total_nt = db.execute("SELECT COUNT(*) FROM name_terms").fetchone()[0]
    print(f"  Summary: {total_names} names, {total_refs} with references, {total_nt} name-term links")


if __name__ == '__main__':
    db_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('C:/QueryPat/database/unified.sqlite')
    db = sqlite3.connect(str(db_path))
    run(db, Path('C:/ExegesisAnalysis'))
    db.close()
