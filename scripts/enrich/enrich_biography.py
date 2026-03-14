"""
Improve biography event classification and add detail text.

1. Reclassifies 'other' events using expanded pattern matching
2. Generates detail text from the event summary + segment context
"""

import json
import re
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


# Expanded classification patterns beyond what ingest_biography uses
# Valid event_types from schema: birth, death, marriage, divorce, residence,
# employment, publication, vision, health, relationship, legal, financial,
# travel, substance_use, correspondence, other
RECLASSIFY_PATTERNS = {
    'publication': (
        r'\bwrit(?:ing|es|ten)\b|novel|story|stories|manuscript|draft|book\b'
        r'|fiction|chapter|essay|article|script|composition|compose'
        r'|typewriter|typing|literary|prose|narrative|plot\b'
        r'|\bpublish|published|publication|printed|issue[ds]?\b'
        r'|editor|magazine|journal\b|submitted|acceptance|rejection'
        r'|galley|proof|anthology|collection\b|paperback|hardcover'
    ),
    'vision': (
        r'vision|theophany|pink light|pink beam|2-3-74|3-74|revelation|hallucin|phosphene|hypnagogic'
        r'|dream\b|dreaming|dreamt|dreamed|holy spirit|possession|possessed|communion|communing'
        r'|apparition|mystical|ecstat|transcenden|supernatural|divine\b|sacred'
        r'|saw\b.*\b(?:god|christ|rome|light|entity|presence|figure)'
        r'|experience of|sensation of|hearing.*voice|inner voice|ai voice'
        r'|firebright|zebra|valis|sophia|parousia|holy|spirit.*poured'
        r'|anamnesis|alchemical|homonculus|three-eyed'
        r'|pre-natal instruction|asklepios|elijah|erasmus.*guide'
        r'|march 1974|april 1974|february 1975'
        r'|prophetic|prophecy|premonition|precognit|déjà vu|deja vu'
        r'|astral|out.of.body|meditation|prayer|contemplat'
        r'|cosmic|universe|reality\b.*\b(?:shift|change|break|crack)'
        r'|enlighten|satori|gnosis|illuminat|epiphany|awakening'
    ),
    'health': (
        r'\bhealth|hospital|doctor|medical|illness|sick|pain\b|disease|diagnos'
        r'|therap|psychiatr|psycholog|mental\b|depress|anxiety|panic'
        r'|medication|drug\b.*\bprescri|overdose|suicide|attempt'
        r'|tooth|dental|surgery|operation|injur'
        r'|insomnia|sleep|fatigue|exhaust'
    ),
    'substance_use': (
        r'\bdrug|amphetamine|speed|LSD|acid\b|marijuana|cannabis'
        r'|alcohol|drunk|drinking|wine|beer|bourbon'
        r'|intoxicat|stoned|high\b.*\bdrug|substance|addict|withdrawal'
    ),
    'relationship': (
        r'\bmarr(?:y|ied|iage)|wife|husband|divorce|separate|lover|affair'
        r'|girlfriend|boyfriend|romantic|dating|engagement|wedding'
        r'|child|son|daughter|father|mother|parent|family'
        r'|friend|friendship|companion|partner'
    ),
    'residence': (
        r'\bmov(?:e|ed|ing)\b.*\b(?:to|from|house|apartment|home)'
        r'|resid|living\b.*\bin\b|relocat|address\b|neighborhood'
        r'|San Francisco|Berkeley|Marin|Fullerton|Point Reyes|Santa Ana'
        r'|Orange County|Los Angeles|Vancouver|Canada'
    ),
    'financial': (
        r'\bmoney|financial|debt|poverty|broke\b|income|royalt|payment'
        r'|rent\b|welfare|IRS|tax\b|bankrupt|evict'
    ),
    'legal': (
        r'\bpolice|FBI|arrest|court|lawsuit|attorney|legal\b'
        r'|break.in|burglary|theft|stolen|investig|search\b.*\bwarrant'
    ),
    'travel': (
        r'\btravel|trip|flew|flight|drove|driving\b.*\bto\b'
        r'|convention|conference|visit(?:ed|ing)\b|journey'
    ),
    'correspondence': (
        r'\bletter|wrote\b.*\bto\b|correspond|mail|postal'
        r'|replied|response\b.*\bfrom\b|sending'
    ),
    'employment': (
        r'\bjob\b|work(?:ed|ing)\b.*\b(?:at|for)\b|employed|career|occupation'
        r'|record store|music shop|hired|fired|quit\b.*\bjob'
    ),
}


def run(db: sqlite3.Connection, source_dir: Path):
    print("Enriching biography events...")

    # 1. Reclassify 'other' events
    others = db.execute("""
        SELECT bio_id, summary FROM biography_events WHERE event_type = 'other'
    """).fetchall()

    reclassified = 0
    for bio_id, summary in others:
        if not summary:
            continue

        new_type = None
        for etype, pattern in RECLASSIFY_PATTERNS.items():
            if re.search(pattern, summary, re.IGNORECASE):
                new_type = etype
                break

        if new_type:
            db.execute(
                "UPDATE biography_events SET event_type = ? WHERE bio_id = ?",
                (new_type, bio_id)
            )
            reclassified += 1

    db.commit()
    remaining = db.execute(
        "SELECT COUNT(*) FROM biography_events WHERE event_type = 'other'"
    ).fetchone()[0]
    print(f"  Reclassified {reclassified} 'other' events ({remaining} remaining)")

    # 2. Generate detail text for events that lack it
    events = db.execute("""
        SELECT be.bio_id, be.summary, be.event_type, be.source_seg_id,
               be.date_display, be.people_involved
        FROM biography_events be
        WHERE be.detail IS NULL
        ORDER BY be.date_start NULLS LAST
    """).fetchall()

    detailed = 0
    for bio_id, summary, event_type, seg_id, date_display, people_json in events:
        if not summary:
            continue

        parts = []

        # Event type context
        type_contexts = {
            'vision': 'Visionary or mystical experience',
            'writing': 'Writing and creative work',
            'publication': 'Publication event',
            'health': 'Health and medical',
            'substance_use': 'Substance use',
            'relationship': 'Personal relationship',
            'residence': 'Residence and living situation',
            'financial': 'Financial matter',
            'legal': 'Legal matter',
            'travel': 'Travel',
            'correspondence': 'Correspondence',
            'employment': 'Employment',
            'death': 'Death',
            'birth': 'Birth',
            'marriage': 'Marriage',
            'divorce': 'Divorce',
        }
        context_label = type_contexts.get(event_type, '')
        if context_label:
            parts.append(f"**{context_label}**")
            if date_display:
                parts.append(f" ({date_display})")
            parts.append(f": {summary}")
        else:
            parts.append(summary)

        # People context
        if people_json:
            try:
                people = json.loads(people_json)
                if people:
                    parts.append(f"\n\nPeople involved: {', '.join(people)}.")
            except (json.JSONDecodeError, TypeError):
                pass

        # Linked segment context
        if seg_id:
            seg = db.execute("""
                SELECT concise_summary, key_claims, date_display
                FROM segments WHERE seg_id = ?
            """, (seg_id,)).fetchone()
            if seg and seg[0]:
                parts.append(f"\n\nSource passage ({seg[2]}): {seg[0]}")
                if seg[1]:
                    try:
                        claims = json.loads(seg[1])
                        if claims and len(claims) > 0:
                            # Add first 2 key claims
                            claim_texts = [c.strip() for c in claims[:2] if isinstance(c, str) and len(c.strip()) > 10]
                            if claim_texts:
                                parts.append("\n\nKey claims from this passage:")
                                for c in claim_texts:
                                    parts.append(f"\n- {c}")
                    except (json.JSONDecodeError, TypeError):
                        pass

        detail = ''.join(parts).strip()
        if len(detail) > len(summary) + 20:
            db.execute(
                "UPDATE biography_events SET detail = ? WHERE bio_id = ?",
                (detail, bio_id)
            )
            detailed += 1

    db.commit()
    print(f"  Added detail text to {detailed} of {len(events)} events")

    # Report final distribution
    dist = db.execute("""
        SELECT event_type, COUNT(*) FROM biography_events
        GROUP BY event_type ORDER BY COUNT(*) DESC
    """).fetchall()
    for etype, count in dist:
        print(f"    {etype}: {count}")


if __name__ == '__main__':
    db_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('C:/QueryPat/database/unified.sqlite')
    db = sqlite3.connect(str(db_path))
    run(db, Path('C:/ExegesisAnalysis'))
    db.close()
