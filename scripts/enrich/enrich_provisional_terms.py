"""
Deterministic enrichment of provisional terms with card_descriptions.

For provisional terms that lack descriptions, assembles them from:
- Evidence packet claims and excerpts
- Linked segment summaries
- Related term context
- Category information
- Frequency and chronology data
"""

import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def run(db: sqlite3.Connection, source_dir: Path):
    print("Enriching provisional term descriptions...")

    terms = db.execute("""
        SELECT term_id, canonical_name, primary_category, mention_count,
               card_description, first_appearance, definition
        FROM terms
        WHERE status = 'provisional'
            AND (card_description IS NULL OR length(card_description) < 20)
        ORDER BY mention_count DESC
    """).fetchall()

    enriched = 0
    for term_id, name, category, mentions, existing_desc, first_app, definition in terms:
        parts = []

        # 1. Opening from definition if available
        if definition and len(definition) > 10:
            parts.append(definition.rstrip('.') + '.')
        else:
            # Generate opening based on category
            if category:
                parts.append(f"{name} is a concept in the domain of {category} that appears in Philip K. Dick's Exegesis.")
            else:
                parts.append(f"{name} is a term appearing in Philip K. Dick's Exegesis.")

        # 2. Frequency
        if mentions and mentions > 0:
            parts.append(f" Referenced {mentions} times across the corpus.")

        # 3. First appearance
        if first_app:
            parts.append(f" First appears in segments dated {first_app}.")

        # 4. Evidence claims (top 2)
        claims = db.execute("""
            SELECT claim_text FROM evidence_packets
            WHERE term_id = ? AND claim_text IS NOT NULL
            ORDER BY CASE confidence
                WHEN 'strong' THEN 1 WHEN 'moderate' THEN 2
                WHEN 'weak' THEN 3 ELSE 4 END
            LIMIT 2
        """, (term_id,)).fetchall()
        if claims:
            for (claim,) in claims:
                claim = claim.strip()
                if claim and len(claim) > 15:
                    # Take first sentence
                    first = claim.split('.')[0].strip()
                    if len(first) > 15 and len(first) < 300:
                        parts.append(f" {first}.")

        # 5. Best evidence excerpt (1, truncated)
        excerpt = db.execute("""
            SELECT ee.excerpt_text
            FROM evidence_excerpts ee
            JOIN evidence_packets ep ON ee.ev_id = ep.ev_id
            WHERE ep.term_id = ?
            ORDER BY ee.excerpt_id
            LIMIT 1
        """, (term_id,)).fetchall()
        if excerpt and excerpt[0][0]:
            text = excerpt[0][0].strip()
            if len(text) > 30:
                if len(text) > 200:
                    text = text[:197] + '...'
                parts.append(f' From the Exegesis: "{text}"')

        # 6. Top linked segment summary (first sentence)
        seg = db.execute("""
            SELECT s.concise_summary
            FROM term_segments ts
            JOIN segments s ON ts.seg_id = s.seg_id
            WHERE ts.term_id = ? AND s.concise_summary IS NOT NULL
            ORDER BY ts.link_confidence, s.date_start
            LIMIT 1
        """, (term_id,)).fetchone()
        if seg and seg[0]:
            summary = seg[0].strip()
            first_sentence = summary.split('.')[0].strip()
            if first_sentence and len(first_sentence) > 20 and len(first_sentence) < 250:
                parts.append(f" Segment context: \"{first_sentence}.\"")

        # 7. Related terms (top 5)
        related = db.execute("""
            SELECT t.canonical_name
            FROM term_terms tt
            JOIN terms t ON tt.term_id_b = t.term_id
            WHERE tt.term_id_a = ? AND t.status IN ('accepted', 'provisional')
            UNION
            SELECT t.canonical_name
            FROM term_terms tt
            JOIN terms t ON tt.term_id_a = t.term_id
            WHERE tt.term_id_b = ? AND t.status IN ('accepted', 'provisional')
            LIMIT 5
        """, (term_id, term_id)).fetchall()
        if related:
            rel_names = [r[0] for r in related]
            parts.append(f" Related to: {', '.join(rel_names)}.")

        card_desc = ''.join(parts).strip()

        # Only update if we generated meaningful content
        if len(card_desc) > 40:
            db.execute("""
                UPDATE terms SET
                    card_description = ?,
                    review_state = CASE
                        WHEN review_state = 'unreviewed' THEN 'machine-drafted'
                        ELSE review_state
                    END,
                    updated_at = datetime('now')
                WHERE term_id = ?
            """, (card_desc, term_id))
            enriched += 1

    db.commit()
    print(f"  Enriched {enriched} of {len(terms)} provisional terms with card descriptions")

    # Also generate full_description for provisional terms that have enough material
    prov_with_desc = db.execute("""
        SELECT term_id, canonical_name, card_description, primary_category,
               mention_count, first_appearance
        FROM terms
        WHERE status = 'provisional'
            AND card_description IS NOT NULL AND length(card_description) > 40
            AND (full_description IS NULL OR length(full_description) < length(card_description) + 50)
        ORDER BY mention_count DESC
    """).fetchall()

    full_enriched = 0
    for term_id, name, card_desc, category, mentions, first_app in prov_with_desc:
        parts = []

        # Card description as opening
        if card_desc:
            parts.append(card_desc.rstrip('.') + '.')

        # Category
        if category:
            parts.append(f"\n\n**Category:** {category}")

        # Frequency
        if mentions and mentions > 0:
            parts.append(f"\n\n**Frequency:** {mentions} mentions.")

        # First appearance
        if first_app:
            parts.append(f" First appears {first_app}.")

        # Evidence excerpts (top 3)
        excerpts = db.execute("""
            SELECT ee.excerpt_text, ep.confidence
            FROM evidence_excerpts ee
            JOIN evidence_packets ep ON ee.ev_id = ep.ev_id
            WHERE ep.term_id = ?
            ORDER BY ee.excerpt_id
            LIMIT 3
        """, (term_id,)).fetchall()
        if excerpts:
            parts.append("\n\n**From the Exegesis:**")
            for text, conf in excerpts:
                text = text.strip()
                if len(text) > 300:
                    text = text[:297] + '...'
                parts.append(f'\n> {text}')

        # Linked segments (top 3)
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

        # Related terms
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
            related_strs = [f"{r[0]} ({r[1]})" for r in related]
            parts.append(f"\n\n**Related terms:** {', '.join(related_strs)}")

        # Aliases
        aliases = db.execute(
            "SELECT alias_text FROM term_aliases WHERE term_id = ?", (term_id,)
        ).fetchall()
        if aliases:
            parts.append(f"\n\n**Also known as:** {', '.join(a[0] for a in aliases)}")

        full_desc = ''.join(parts)
        if len(full_desc) > len(card_desc or '') + 50:
            db.execute("""
                UPDATE terms SET
                    full_description = ?,
                    review_state = CASE
                        WHEN review_state = 'unreviewed' THEN 'machine-drafted'
                        ELSE review_state
                    END,
                    updated_at = datetime('now')
                WHERE term_id = ?
            """, (full_desc, term_id))
            full_enriched += 1

    db.commit()
    print(f"  Generated full descriptions for {full_enriched} provisional terms")


if __name__ == '__main__':
    db_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('C:/QueryPat/database/unified.sqlite')
    db = sqlite3.connect(str(db_path))
    run(db, Path('C:/ExegesisAnalysis'))
    db.close()
