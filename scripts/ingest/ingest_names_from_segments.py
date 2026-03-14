"""
Harvest proper names from segments.people_entities JSON arrays.

Normalizes raw name strings like:
  "Joe Chip (fictional character in *UBIK*)" → canonical "Joe Chip", entity_type "character"
  "Claudia (Recipient)" → canonical "Claudia", parenthetical stripped
  "Rosemary / Mary (Fairy/Mortal children)" → canonical "Rosemary", alias "Mary"
  "PKD / Thomas" → canonical "PKD", alias "Thomas"

Creates name_segments links at confidence 2 (exact field extraction).
"""

import json
import re
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from date_norms import make_name_id, make_slug


# Known entity type overrides for names that defy pattern matching
ENTITY_TYPE_OVERRIDES = {
    'zebra': 'deity_figure',
    'valis': 'deity_figure',
    'sophia': 'deity_figure',
    'palmer eldritch': 'character',
    'ubik': 'deity_figure',
    'joe chip': 'character',
    'mr. tagomi': 'character',
    'nicholas brady': 'character',
    'angel archer': 'character',
    'horselover fat': 'character',
    'rick deckard': 'character',
    'wilbur mercer': 'character',
    'glen runciter': 'character',
    'bob arctor': 'character',
    'jack bohlen': 'character',
    'ragle gumm': 'character',
    'timothy archer': 'character',
    'herb asher': 'character',
    'emmanuel': 'deity_figure',
    'thomas': 'deity_figure',
    'firebright': 'deity_figure',
    'st. sophia': 'deity_figure',
    'holy wisdom': 'deity_figure',
    'the urgrund': 'deity_figure',
    'demiurge': 'deity_figure',
    'yaldabaoth': 'deity_figure',
    'christ': 'deity_figure',
    'christos': 'deity_figure',
    'jesus': 'deity_figure',
    'elijah': 'deity_figure',
    'asklepios': 'deity_figure',
    'dionysos': 'deity_figure',
    'zagreus': 'deity_figure',
    'apollo': 'deity_figure',
    'athena': 'deity_figure',
    'plato': 'historical_person',
    'plotinus': 'historical_person',
    'heraclitus': 'historical_person',
    'parmenides': 'historical_person',
    'spinoza': 'historical_person',
    'hegel': 'historical_person',
    'whitehead': 'historical_person',
    'tillich': 'historical_person',
    'mani': 'historical_person',
    'simon magus': 'historical_person',
    'meister eckhart': 'historical_person',
    'jakob boehme': 'historical_person',
    'empedocles': 'historical_person',
    'pythagoras': 'historical_person',
    'beethoven': 'historical_person',
    'j.s. bach': 'historical_person',
    'wagner': 'historical_person',
    'shakespeare': 'historical_person',
    'st. paul': 'historical_person',
    'nixon': 'historical_person',
}

# Parenthetical patterns that indicate entity type
CHARACTER_PATTERNS = re.compile(
    r'\b(character|fictional|protagonist|antagonist|novel|story|book)\b', re.I
)
DEITY_PATTERNS = re.compile(
    r'\b(god|deity|divine|spirit|angel|demon|cosmic|entity|archon|aeon)\b', re.I
)
PLACE_PATTERNS = re.compile(
    r'\b(city|country|planet|world|realm|land|region|place)\b', re.I
)
ORG_PATTERNS = re.compile(
    r'\b(church|organization|company|group|party|institution|magazine|publisher)\b', re.I
)

# Parenthetical role annotations to strip but not classify from
ROLE_ANNOTATIONS = re.compile(
    r'\b(recipient|subject|editor|scholar|associated|source|wife|husband|'
    r'son|daughter|friend|cat|pet|colleague|psychologist|quoted|staff|'
    r'dream figure|affectionate|former)\b', re.I
)


def parse_name_string(raw: str) -> dict:
    """
    Parse a raw name string from people_entities into structured data.

    Returns dict with keys: canonical, aliases, entity_type, parenthetical, work_hint
    """
    raw = raw.strip()
    result = {
        'canonical': None,
        'aliases': [],
        'entity_type': None,
        'parenthetical': None,
        'work_hint': None,
    }

    # Extract parenthetical if present
    paren_match = re.search(r'\(([^)]+)\)\s*$', raw)
    parenthetical = None
    name_part = raw
    if paren_match:
        parenthetical = paren_match.group(1)
        name_part = raw[:paren_match.start()].strip()
        result['parenthetical'] = parenthetical

    # Handle slash-separated aliases: "Rosemary / Mary", "PKD / Thomas"
    if ' / ' in name_part:
        parts = [p.strip() for p in name_part.split(' / ')]
        result['canonical'] = parts[0]
        result['aliases'] = parts[1:]
    elif ' aka ' in name_part.lower():
        parts = re.split(r'\s+aka\s+', name_part, flags=re.I)
        result['canonical'] = parts[0]
        result['aliases'] = parts[1:]
    else:
        result['canonical'] = name_part

    # Strip markdown italics from canonical: *UBIK* → UBIK
    result['canonical'] = re.sub(r'\*([^*]+)\*', r'\1', result['canonical']).strip()
    result['aliases'] = [re.sub(r'\*([^*]+)\*', r'\1', a).strip() for a in result['aliases']]

    # Skip empty canonicals
    if not result['canonical']:
        return None

    # Classify entity type from parenthetical
    if parenthetical:
        if CHARACTER_PATTERNS.search(parenthetical):
            result['entity_type'] = 'character'
            # Try to extract work name from parenthetical
            work_match = re.search(r'in\s+\*?([^*),]+)\*?', parenthetical)
            if work_match:
                result['work_hint'] = work_match.group(1).strip()
        elif DEITY_PATTERNS.search(parenthetical):
            result['entity_type'] = 'deity_figure'
        elif PLACE_PATTERNS.search(parenthetical):
            result['entity_type'] = 'place'
        elif ORG_PATTERNS.search(parenthetical):
            result['entity_type'] = 'organization'

    # Check overrides
    canonical_lower = result['canonical'].lower().strip()
    if canonical_lower in ENTITY_TYPE_OVERRIDES:
        result['entity_type'] = ENTITY_TYPE_OVERRIDES[canonical_lower]

    # Default: historical_person (most Exegesis names are people PKD discusses)
    if not result['entity_type']:
        result['entity_type'] = 'historical_person'

    return result


def run(db: sqlite3.Connection, source_dir: Path):
    print("Ingesting names from segment people_entities...")

    # Ensure tables exist
    db.execute("""
        CREATE TABLE IF NOT EXISTS names (
            name_id TEXT PRIMARY KEY, canonical_form TEXT NOT NULL UNIQUE,
            slug TEXT NOT NULL UNIQUE, entity_type TEXT NOT NULL,
            source_type TEXT, status TEXT NOT NULL DEFAULT 'unreviewed',
            review_state TEXT NOT NULL DEFAULT 'unreviewed',
            etymology TEXT, origin_language TEXT, allusion_type TEXT,
            allusion_target TEXT, wordplay_note TEXT, symbolic_note TEXT,
            card_description TEXT, full_description TEXT,
            mention_count INTEGER DEFAULT 0, first_work TEXT, work_list TEXT,
            reference_id TEXT, provenance TEXT, notes TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now'))
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS name_aliases (
            alias_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_id TEXT NOT NULL, alias_text TEXT NOT NULL,
            alias_type TEXT DEFAULT 'spelling',
            FOREIGN KEY (name_id) REFERENCES names(name_id),
            UNIQUE (name_id, alias_text)
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS name_segments (
            name_id TEXT NOT NULL, seg_id TEXT NOT NULL,
            match_type TEXT NOT NULL, link_confidence INTEGER NOT NULL,
            link_method TEXT NOT NULL, matched_text TEXT, context_snippet TEXT,
            PRIMARY KEY (name_id, seg_id, match_type),
            FOREIGN KEY (name_id) REFERENCES names(name_id),
            FOREIGN KEY (seg_id) REFERENCES segments(seg_id)
        )
    """)

    # Gather all people_entities from segments
    rows = db.execute("""
        SELECT seg_id, people_entities
        FROM segments
        WHERE people_entities IS NOT NULL AND people_entities != '[]'
    """).fetchall()

    # Track: canonical_lower → {parsed data, seg_ids, raw_strings}
    name_registry = {}  # slug → accumulated data
    total_mentions = 0
    skipped = 0

    for seg_id, pe_json in rows:
        entities = json.loads(pe_json)
        for raw_name in entities:
            parsed = parse_name_string(raw_name)
            if not parsed or not parsed['canonical']:
                skipped += 1
                continue

            canonical = parsed['canonical']
            slug = make_slug(canonical)
            if not slug:
                skipped += 1
                continue

            total_mentions += 1

            if slug not in name_registry:
                name_registry[slug] = {
                    'canonical': canonical,
                    'slug': slug,
                    'entity_type': parsed['entity_type'],
                    'aliases': set(),
                    'seg_ids': set(),
                    'work_hints': set(),
                    'raw_strings': set(),
                    'mention_count': 0,
                }

            entry = name_registry[slug]
            entry['mention_count'] += 1
            entry['seg_ids'].add(seg_id)
            entry['raw_strings'].add(raw_name)

            # Collect aliases
            for alias in parsed['aliases']:
                if alias and alias != canonical:
                    entry['aliases'].add(alias)

            # Collect work hints
            if parsed.get('work_hint'):
                entry['work_hints'].add(parsed['work_hint'])

            # Upgrade entity type if we get a more specific classification
            if parsed['entity_type'] != 'historical_person' and entry['entity_type'] == 'historical_person':
                entry['entity_type'] = parsed['entity_type']

    # Insert into database
    inserted_names = 0
    inserted_aliases = 0
    inserted_links = 0

    for slug, entry in name_registry.items():
        name_id = make_name_id(entry['canonical'])
        first_work = sorted(entry['work_hints'])[0] if entry['work_hints'] else None
        work_list = json.dumps(sorted(entry['work_hints'])) if entry['work_hints'] else None

        try:
            db.execute("""
                INSERT OR IGNORE INTO names
                    (name_id, canonical_form, slug, entity_type, source_type,
                     status, review_state, mention_count, first_work, work_list,
                     provenance)
                VALUES (?, ?, ?, ?, 'exegesis', 'provisional', 'unreviewed',
                        ?, ?, ?, 'ingest_names_from_segments')
            """, (name_id, entry['canonical'], slug, entry['entity_type'],
                  entry['mention_count'], first_work, work_list))
            inserted_names += 1
        except sqlite3.IntegrityError:
            # Update mention count if already exists
            db.execute("""
                UPDATE names SET
                    mention_count = mention_count + ?,
                    updated_at = datetime('now')
                WHERE name_id = ?
            """, (entry['mention_count'], name_id))

        # Insert aliases
        for alias in entry['aliases']:
            try:
                db.execute("""
                    INSERT OR IGNORE INTO name_aliases (name_id, alias_text, alias_type)
                    VALUES (?, ?, 'alternate_form')
                """, (name_id, alias))
                inserted_aliases += 1
            except sqlite3.IntegrityError:
                pass

        # Insert name_segments links
        for seg_id in entry['seg_ids']:
            try:
                db.execute("""
                    INSERT OR IGNORE INTO name_segments
                        (name_id, seg_id, match_type, link_confidence, link_method, matched_text)
                    VALUES (?, ?, 'exact_mention', 2, 'people_entities_field', ?)
                """, (name_id, seg_id, entry['canonical']))
                inserted_links += 1
            except sqlite3.IntegrityError:
                pass

    db.commit()
    print(f"  Processed {total_mentions} mentions from {len(rows)} segments (skipped {skipped})")
    print(f"  Inserted {inserted_names} names, {inserted_aliases} aliases, {inserted_links} segment links")

    # Report entity type distribution
    dist = db.execute("""
        SELECT entity_type, COUNT(*) FROM names GROUP BY entity_type ORDER BY COUNT(*) DESC
    """).fetchall()
    for etype, count in dist:
        print(f"    {etype}: {count}")


if __name__ == '__main__':
    db_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('C:/QueryPat/database/unified.sqlite')
    db = sqlite3.connect(str(db_path))
    run(db, Path('C:/ExegesisAnalysis'))
    db.close()
