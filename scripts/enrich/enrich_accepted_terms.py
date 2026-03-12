"""
Enrich accepted dictionary terms with fuller descriptions.

For each accepted term, generates a full_description by combining:
- The existing card_description (seed from LLM chat extraction)
- Evidence excerpts from the Exegesis
- Linked segment summaries
- Related term context

This is a deterministic enrichment (no LLM calls) that assembles
existing data into a richer description.
"""

import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def run(db: sqlite3.Connection, source_dir: Path):
    print("Enriching accepted term descriptions...")

    terms = db.execute("""
        SELECT term_id, canonical_name, card_description, full_description,
               primary_category, mention_count, first_appearance
        FROM terms
        WHERE status = 'accepted'
        ORDER BY mention_count DESC
    """).fetchall()

    enriched = 0
    for term_id, name, card_desc, full_desc, category, mentions, first_app in terms:
        # Skip if already has a longer full_description
        if full_desc and len(full_desc) > len(card_desc or '') + 50:
            continue

        parts = []

        # 1. Card description as opening
        if card_desc:
            parts.append(card_desc.rstrip('.') + '.')

        # 2. Category context
        if category:
            parts.append(f"\n\n**Category:** {category}")

        # 3. Mention frequency
        if mentions and mentions > 0:
            parts.append(f"\n\n**Frequency in the Exegesis:** {mentions} mentions across the corpus.")

        # 4. First appearance
        if first_app:
            parts.append(f" First appears in segments dated {first_app}.")

        # 5. Evidence excerpts (top 5, truncated)
        excerpts = db.execute("""
            SELECT ee.excerpt_text, ep.confidence
            FROM evidence_excerpts ee
            JOIN evidence_packets ep ON ee.ev_id = ep.ev_id
            WHERE ep.term_id = ?
            ORDER BY ee.excerpt_id
            LIMIT 5
        """, (term_id,)).fetchall()

        if excerpts:
            parts.append("\n\n**From the Exegesis:**")
            for exc_text, conf in excerpts:
                # Truncate long excerpts
                text = exc_text.strip()
                if len(text) > 300:
                    text = text[:297] + '...'
                parts.append(f'\n> {text}')

        # 6. Linked segment context (top 3 summaries)
        linked = db.execute("""
            SELECT s.concise_summary, s.date_display
            FROM term_segments ts
            JOIN segments s ON ts.seg_id = s.seg_id
            WHERE ts.term_id = ? AND s.concise_summary IS NOT NULL
            ORDER BY ts.link_confidence, s.date_start
            LIMIT 3
        """, (term_id,)).fetchall()

        if linked:
            parts.append("\n\n**Key segment contexts:**")
            for summary, date_disp in linked:
                if summary:
                    s = summary.strip()
                    if len(s) > 200:
                        s = s[:197] + '...'
                    parts.append(f"\n- ({date_disp}) {s}")

        # 7. Related terms
        related = db.execute("""
            SELECT t.canonical_name, tt.relation_type
            FROM term_terms tt
            JOIN terms t ON tt.term_id_b = t.term_id
            WHERE tt.term_id_a = ? AND t.status IN ('accepted', 'provisional')
            UNION
            SELECT t.canonical_name, tt.relation_type
            FROM term_terms tt
            JOIN terms t ON tt.term_id_a = t.term_id
            WHERE tt.term_id_b = ? AND t.status IN ('accepted', 'provisional')
            LIMIT 10
        """, (term_id, term_id)).fetchall()

        if related:
            related_names = [f"{r[0]} ({r[1]})" for r in related]
            parts.append(f"\n\n**Related terms:** {', '.join(related_names)}")

        # 8. Aliases
        aliases = db.execute("""
            SELECT alias_text FROM term_aliases WHERE term_id = ?
        """, (term_id,)).fetchall()

        if aliases:
            alias_list = ', '.join(a[0] for a in aliases)
            parts.append(f"\n\n**Also known as:** {alias_list}")

        full_description = ''.join(parts)

        # Only update if we generated meaningful content beyond the card description
        if len(full_description) > len(card_desc or '') + 20:
            db.execute("""
                UPDATE terms SET
                    full_description = ?,
                    review_state = CASE
                        WHEN review_state = 'unreviewed' THEN 'machine-drafted'
                        ELSE review_state
                    END,
                    updated_at = datetime('now')
                WHERE term_id = ?
            """, (full_description, term_id))
            enriched += 1

    db.commit()
    print(f"  Enriched {enriched} of {len(terms)} accepted terms")


if __name__ == '__main__':
    db_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('C:/QueryPat/database/unified.sqlite')
    db = sqlite3.connect(str(db_path))
    run(db, Path('C:/ExegesisAnalysis'))
    db.close()
