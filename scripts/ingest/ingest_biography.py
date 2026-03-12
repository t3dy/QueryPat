"""
Ingest biographical events from exegesis segment summaries.

Reads: segments.autobiographical (JSON array of narrative strings)
Updates: biography_events table with structured events extracted from the text.
"""

import json
import re
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from date_norms import normalize_date


# Patterns to classify event types from narrative text
EVENT_TYPE_PATTERNS = {
    'vision': (
        r'vision|theophany|pink light|pink beam|2-3-74|3-74|revelation|hallucin|phosphene|hypnagogic'
        r'|dream\b|dreaming|dreamt|dreamed|holy spirit|possession|possessed|communion|communing'
        r'|apparition|mystical|ecstat|transcenden|supernatural|divine\b|sacred'
        r'|saw\b.*\b(?:god|christ|rome|light|entity|presence|figure)'
        r'|experience of|sensation of|hearing.*voice|inner voice|ai voice'
        r'|firebright|zebra|valis|sophia|parousia|holy|spirit.*poured'
        r'|roll-back|rollback|anamnesis|alchemical|homonculus|three-eyed'
        r'|pre-natal instruction|asklepios|elijah|erasmus.*guide'
        r'|march 1974|april 1974|february 1975|2-3-74'
    ),
    'substance_use': r'lsd|acid trip|\bdrug\b|amphetamine|speed|mescaline|marijuana|substance|vitamin.*formula|orthomolecular',
    'marriage': r'married|marriage|wedding|wife|wed\b',
    'divorce': r'divorce|separated|split|separation|break-?up',
    'death': r'\bdied\b|\bdeath\b|funeral|passed away|suicide attempt|killed|lost.*cat|lost.*dog|loss of.*pet',
    'health': (
        r'hospital|illness|psychiatric|breakdown|stroke|panic|anxiety|depression|overdose|surgery'
        r'|hypertension|vertigo|infirmit|physical.*ailment'
    ),
    'publication': (
        r'publish|publication|wrote.*novel|manuscript|story.*written|book.*written'
        r'|\bubik\b|\btears\b|\bvalis\b.*novel|scanner|androids|maze of death'
    ),
    'residence': (
        r'moved to|living in|apartment|house\b.*\b(?:dream|live|reside)'
        r'|residence|santa ana|fullerton|marin|point reyes|san rafael|oakland|berkeley'
        r'|1126 francisco'
    ),
    'relationship': (
        r'girlfriend|relationship|affair|romantic|lover|partner'
        r'|\bnancy\b|\btessa\b|\banne\b|\bkleo\b|\blinda\b|\bdorothy\b|\blaura\b'
        r'|ex-wife|former wife|son christopher|daughter|child\b.*\bbirth|baptism.*son'
    ),
    'correspondence': r'letter\b|wrote to|correspondence|phone call|correspondi|contact with|writing.*to\b',
    'employment': r'\bjob\b|work\b.*at|employed|record store|music shop',
    'travel': r'travel|trip\b|visited|vancouver|metz|france|canada',
    'legal': r'police|fbi|irs|break-?in|burglary|theft|watergate|nixon|impeach',
    'financial': r'money|poverty|debt|royalt|financial|welfare|library.*lost|loss of.*library',
}

# Date extraction patterns
DATE_PATTERNS = [
    (r'\b((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4})\b', 'exact'),
    (r'\b((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4})\b', 'approximate'),
    (r'\b((?:spring|summer|fall|autumn|winter|early|late|mid-?)\s*\d{4})\b', 'circa'),
    (r'\b(\d{4})\b', 'approximate'),
]

# People extraction
KNOWN_PEOPLE = [
    'Tessa', 'Nancy', 'Anne', 'Kleo', 'Linda', 'Claudia', 'Phyllis',
    'Tim Powers', 'K.W. Jeter', 'Norman Spinrad', 'Thomas Disch',
    'Ursula Le Guin', 'Stanislaw Lem', 'Roger Zelazny',
    'Bishop Pike', 'James Pike', 'Jim Pike',
    'Dorothy', 'Edgar', 'Jane',
    'Laura', 'Isa', 'Christopher',
]


def classify_event_type(text: str) -> str:
    """Classify biographical event type from narrative text."""
    text_lower = text.lower()
    for event_type, pattern in EVENT_TYPE_PATTERNS.items():
        if re.search(pattern, text_lower):
            return event_type
    return 'other'


def extract_date_from_text(text: str):
    """Try to extract a date from narrative text."""
    for pattern, confidence in DATE_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            raw = match.group(1)
            normalized = normalize_date(raw)
            return normalized
    return None


def extract_people(text: str) -> list:
    """Extract known people mentioned in text."""
    found = []
    for person in KNOWN_PEOPLE:
        if person.lower() in text.lower():
            found.append(person)
    return found


def run(db: sqlite3.Connection, source_dir: Path):
    print("Ingesting biography events from segments...")

    # Get all segments with autobiographical data
    rows = db.execute("""
        SELECT seg_id, doc_id, autobiographical, date_start, date_display, date_confidence
        FROM segments
        WHERE autobiographical IS NOT NULL AND autobiographical != '[]' AND autobiographical != ''
    """).fetchall()

    created = 0
    for seg_id, doc_id, auto_json, seg_date, seg_date_display, seg_date_conf in rows:
        try:
            events = json.loads(auto_json)
        except (json.JSONDecodeError, TypeError):
            continue

        if not isinstance(events, list):
            continue

        for event_text in events:
            if not event_text or not isinstance(event_text, str):
                continue
            if len(event_text.strip()) < 10:
                continue

            # Classify
            event_type = classify_event_type(event_text)

            # Extract date from text, fall back to segment date
            date_info = extract_date_from_text(event_text)
            if date_info:
                date_start = date_info.date_start
                date_display = date_info.date_display
                date_confidence = date_info.date_confidence
            else:
                date_start = seg_date
                date_display = seg_date_display
                date_confidence = seg_date_conf or 'inferred'

            # Extract people
            people = extract_people(event_text)

            # Check for duplicate
            existing = db.execute("""
                SELECT bio_id FROM biography_events
                WHERE summary = ? AND source_seg_id = ?
            """, (event_text[:500], seg_id)).fetchone()

            if existing:
                continue

            db.execute("""
                INSERT INTO biography_events (
                    event_type, summary,
                    date_start, date_display, date_confidence,
                    source_type, source_seg_id, source_doc_id,
                    people_involved, reliability
                ) VALUES (?, ?, ?, ?, ?, 'exegesis', ?, ?, ?, 'unverified')
            """, (
                event_type, event_text[:500],
                date_start, date_display, date_confidence,
                seg_id, doc_id,
                json.dumps(people) if people else None,
            ))
            created += 1

    db.commit()
    print(f"  Created {created} biography events from {len(rows)} segments")


if __name__ == '__main__':
    db_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('C:/QueryPat/database/unified.sqlite')
    db = sqlite3.connect(str(db_path))
    run(db, Path('C:/ExegesisAnalysis'))
    db.close()
