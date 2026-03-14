"""
Deterministic enrichment of names with card_descriptions.

Assembles descriptions from:
- Reference match data (etymology, domain, significance)
- Entity type context
- Linked segment summaries
- Related dictionary terms
- Mention frequency
"""

import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def run(db: sqlite3.Connection, source_dir: Path):
    print("Enriching name descriptions...")

    names = db.execute("""
        SELECT name_id, canonical_form, entity_type, source_type,
               etymology, origin_language, allusion_type, reference_id,
               mention_count, first_work, work_list
        FROM names
        ORDER BY mention_count DESC
    """).fetchall()

    enriched = 0
    for (name_id, canonical, entity_type, source_type,
         etymology, origin_lang, allusion_type, ref_id,
         mentions, first_work, work_list) in names:

        parts = []

        # Also fetch wordplay_note for fiction characters
        wordplay_note = db.execute(
            "SELECT wordplay_note FROM names WHERE name_id = ?", (name_id,)
        ).fetchone()
        wordplay = wordplay_note[0] if wordplay_note and wordplay_note[0] else None

        # 1. Opening line — fiction characters get a different template
        is_fiction = (entity_type == 'character' and source_type in ('fiction', 'both'))

        if is_fiction and first_work:
            # Fiction character: lead with the work title
            works = json.loads(work_list) if work_list else [first_work]
            work_str = f"*{works[0]}*"
            if etymology:
                parts.append(f"{canonical} (meaning \"{etymology}\") is a character in Philip K. Dick's {work_str}.")
            else:
                parts.append(f"{canonical} is a character in Philip K. Dick's {work_str}.")
        else:
            type_labels = {
                'character': 'fictional character',
                'deity_figure': 'divine or mythological figure',
                'historical_person': 'historical figure',
                'place': 'place name',
                'organization': 'organization',
                'other': 'name',
            }
            type_label = type_labels.get(entity_type, 'name')

            if etymology and origin_lang:
                parts.append(f"{canonical} ({origin_lang}: \"{etymology}\") is a {type_label} appearing in Philip K. Dick's Exegesis.")
            elif etymology:
                parts.append(f"{canonical} (meaning \"{etymology}\") is a {type_label} appearing in Philip K. Dick's Exegesis.")
            else:
                parts.append(f"{canonical} is a {type_label} referenced in Philip K. Dick's Exegesis.")

        # 2. Reference context
        if ref_id:
            ref = db.execute("""
                SELECT brief, significance, domain, source_text
                FROM name_references WHERE ref_id = ?
            """, (ref_id,)).fetchone()
            if ref:
                brief, significance, domain, source_text = ref
                if domain == 'literary' and brief:
                    # Fiction reference: use brief as role description
                    parts.append(f" {brief}.")
                    if wordplay:
                        parts.append(f" Name note: {wordplay}.")
                    if significance:
                        parts.append(f" {significance}.")
                elif brief:
                    parts.append(f" In the {domain} tradition, {canonical} is {brief.lower() if brief[0].isupper() and not brief.startswith('The') else brief}.")
                    if significance:
                        parts.append(f" {significance}.")

        # 3. Mention frequency
        if mentions and mentions > 1:
            parts.append(f" Appears in {mentions} Exegesis passages.")

        # 4. Work appearances
        if first_work:
            works = json.loads(work_list) if work_list else [first_work]
            if len(works) == 1:
                parts.append(f" First appears in *{works[0]}*.")
            elif len(works) <= 3:
                parts.append(f" Appears in {', '.join(f'*{w}*' for w in works)}.")

        # 5. Related dictionary terms (top 5)
        related = db.execute("""
            SELECT t.canonical_name, nt.relation_type
            FROM name_terms nt
            JOIN terms t ON nt.term_id = t.term_id
            WHERE nt.name_id = ? AND nt.link_confidence <= 3
            ORDER BY nt.link_confidence
            LIMIT 5
        """, (name_id,)).fetchall()
        if related:
            term_names = [r[0] for r in related]
            parts.append(f" Associated with dictionary terms: {', '.join(term_names)}.")

        # 6. Top segment context (1 sentence from most relevant segment)
        seg = db.execute("""
            SELECT s.concise_summary
            FROM name_segments ns
            JOIN segments s ON ns.seg_id = s.seg_id
            WHERE ns.name_id = ? AND s.concise_summary IS NOT NULL
            ORDER BY ns.link_confidence, s.date_start
            LIMIT 1
        """, (name_id,)).fetchone()
        if seg and seg[0]:
            # Take first sentence of summary
            summary = seg[0].strip()
            first_sentence = summary.split('.')[0].strip()
            if first_sentence and len(first_sentence) > 20:
                parts.append(f" Context: \"{first_sentence}.\"")

        card_desc = ''.join(parts).strip()

        if len(card_desc) > 30:
            db.execute("""
                UPDATE names SET
                    card_description = ?,
                    review_state = CASE
                        WHEN review_state = 'unreviewed' THEN 'machine-drafted'
                        ELSE review_state
                    END,
                    updated_at = datetime('now')
                WHERE name_id = ?
            """, (card_desc, name_id))
            enriched += 1

    db.commit()
    print(f"  Enriched {enriched} of {len(names)} names with card descriptions")


if __name__ == '__main__':
    db_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('C:/QueryPat/database/unified.sqlite')
    db = sqlite3.connect(str(db_path))
    run(db, Path('C:/ExegesisAnalysis'))
    db.close()
