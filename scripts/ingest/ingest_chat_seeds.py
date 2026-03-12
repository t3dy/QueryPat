"""
Ingest term seeds extracted from PKD LLM Chat PDFs.

Reads: scripts/overrides/term_seeds_from_chats.json
Updates: terms table — creates or promotes terms to 'accepted' status
         with descriptions derived from the chat analysis.
"""

import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from date_norms import make_term_id, make_slug


def run(db: sqlite3.Connection, source_dir: Path):
    print("Ingesting term seeds from LLM chats...")

    seeds_path = Path(__file__).resolve().parent.parent / 'overrides' / 'term_seeds_from_chats.json'
    if not seeds_path.exists():
        print(f"  SKIP: {seeds_path} not found")
        return

    with open(seeds_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    created = 0
    promoted = 0
    enriched = 0

    # Process historical figures
    for figure in data['categories'].get('historical_figures', []):
        name = figure['name']
        term_id = make_term_id(name)
        slug = make_slug(name)
        category = figure.get('category', 'Historical Figure')
        dates = figure.get('dates', '')
        relevance = figure.get('relevance', '')

        description = f"{name}"
        if dates:
            description += f" ({dates})"
        description += f". {relevance}"

        _upsert_term(db, term_id, name, slug, category, description,
                     status='accepted', review_state='machine-drafted',
                     provenance='llm_chat_extraction')
        result = db.execute("SELECT changes()").fetchone()[0]
        if result:
            created += 1

    # Process PKD bespoke terms
    for term in data['categories'].get('pkd_bespoke_terms', []):
        name = term['name']
        term_id = make_term_id(name)
        slug = make_slug(name)
        category = term.get('category', 'PKD Visionary')
        definition = term.get('definition', '')

        _upsert_term(db, term_id, name, slug, category, definition,
                     status='accepted', review_state='machine-drafted',
                     provenance='llm_chat_extraction')
        result = db.execute("SELECT changes()").fetchone()[0]
        if result:
            promoted += 1

    # Process philosophical concepts
    for concept in data['categories'].get('philosophical_concepts', []):
        name = concept['name']
        term_id = make_term_id(name)
        slug = make_slug(name)
        category = concept.get('category', 'Philosophy')
        definition = concept.get('definition', '')

        _upsert_term(db, term_id, name, slug, category, definition,
                     status='accepted', review_state='machine-drafted',
                     provenance='llm_chat_extraction')
        result = db.execute("SELECT changes()").fetchone()[0]
        if result:
            enriched += 1

    db.commit()
    total = created + promoted + enriched
    print(f"  Processed {total} seed terms ({created} figures, {promoted} PKD terms, {enriched} concepts)")


def _upsert_term(db, term_id, name, slug, category, description, status, review_state, provenance):
    """Insert or update a term, always promoting to at least the given status."""
    existing = db.execute("SELECT term_id, status FROM terms WHERE term_id = ?", (term_id,)).fetchone()

    if existing:
        # Update: promote status and add description if missing
        db.execute("""
            UPDATE terms SET
                status = CASE
                    WHEN status IN ('background', 'rejected', 'alias') THEN ?
                    ELSE status
                END,
                review_state = CASE
                    WHEN review_state = 'unreviewed' THEN ?
                    ELSE review_state
                END,
                card_description = CASE
                    WHEN card_description IS NULL OR card_description = '' THEN ?
                    ELSE card_description
                END,
                full_description = CASE
                    WHEN full_description IS NULL OR full_description = '' THEN ?
                    ELSE full_description
                END,
                primary_category = CASE
                    WHEN primary_category IS NULL OR primary_category = '' THEN ?
                    ELSE primary_category
                END,
                provenance = ?,
                updated_at = datetime('now')
            WHERE term_id = ?
        """, (status, review_state, description, description, category, provenance, term_id))
    else:
        # Insert new term
        try:
            db.execute("""
                INSERT INTO terms (
                    term_id, canonical_name, slug,
                    status, review_state,
                    primary_category,
                    card_description, full_description,
                    provenance
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (term_id, name, slug, status, review_state,
                  category, description, description, provenance))
        except sqlite3.IntegrityError:
            # Slug conflict — append suffix
            slug = slug + '-' + term_id[-4:]
            db.execute("""
                INSERT INTO terms (
                    term_id, canonical_name, slug,
                    status, review_state,
                    primary_category,
                    card_description, full_description,
                    provenance
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (term_id, name, slug, status, review_state,
                  category, description, description, provenance))


if __name__ == '__main__':
    db_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('C:/QueryPat/database/unified.sqlite')
    db = sqlite3.connect(str(db_path))
    run(db, Path('C:/ExegesisAnalysis'))
    db.close()
