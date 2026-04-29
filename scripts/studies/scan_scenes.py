"""
Deterministic scene candidate scanner for PKD fiction texts.

Scans fiction documents (novels, short stories) for co-occurrences of
AI entity markers and interaction-type markers within a 1500-char window.
Writes candidates to ai_scene_candidates table.

No API calls. Pure lexicon-based detection.
"""

import json
import re
import sqlite3
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_DB = PROJECT_DIR / 'database' / 'unified.sqlite'
LEXICON_PATH = Path(__file__).resolve().parent / 'lexicons' / 'scene_markers.json'

COOCCURRENCE_WINDOW = 1500   # chars: AI entity + interaction marker must co-occur within this
CONTEXT_WINDOW = 750         # chars of context on each side of co-occurrence center
MAX_PASSAGE_CHARS = 2000     # hard cap on extracted window


def load_scene_lexicon():
    """Load scene markers lexicon. Returns (entity_pattern, interaction_patterns)."""
    with open(LEXICON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Compile AI entity markers
    entity_terms = data['ai_entity_markers']
    entity_terms.sort(key=len, reverse=True)
    escaped = [re.escape(t) for t in entity_terms]
    entity_pattern = re.compile(r'\b(' + '|'.join(escaped) + r')\b', re.IGNORECASE)

    # Compile interaction markers per type
    interaction_patterns = {}
    for type_slug, lex in data['interaction_markers'].items():
        terms = list(lex.get('primary', []))
        terms.extend(lex.get('aliases', []))
        if not terms:
            continue
        terms.sort(key=len, reverse=True)
        escaped_terms = [re.escape(t) for t in terms]
        match_pattern = re.compile(r'\b(' + '|'.join(escaped_terms) + r')\b', re.IGNORECASE)

        excl_pattern = None
        excl_terms = lex.get('exclusions', [])
        if excl_terms:
            excl_escaped = [re.escape(t) for t in excl_terms]
            excl_pattern = re.compile(r'\b(' + '|'.join(excl_escaped) + r')\b', re.IGNORECASE)

        interaction_patterns[type_slug] = (match_pattern, excl_pattern)

    return entity_pattern, interaction_patterns


def load_fiction_corpus(db: sqlite3.Connection):
    """Load text from fiction documents only (Lane A)."""
    rows = db.execute("""
        SELECT d.doc_id, d.title, dt.text_content
        FROM documents d
        JOIN document_texts dt ON d.doc_id = dt.doc_id
        WHERE d.doc_type IN ('novel', 'short_story')
          AND dt.text_content IS NOT NULL
          AND length(dt.text_content) > 100
    """).fetchall()
    print(f"    Loaded {len(rows)} fiction documents with text")
    return rows


def find_entity_positions(text, entity_pattern):
    """Find all AI entity marker positions in text."""
    return [(m.start(), m.end(), m.group()) for m in entity_pattern.finditer(text)]


def find_interaction_positions(text, interaction_patterns):
    """Find all interaction marker positions with type labels."""
    results = []
    for type_slug, (pattern, excl_pattern) in interaction_patterns.items():
        for m in pattern.finditer(text):
            # Check exclusions
            if excl_pattern:
                context = text[max(0, m.start() - 50):m.end() + 50]
                if excl_pattern.search(context):
                    continue
            results.append((m.start(), m.end(), m.group(), type_slug))
    return results


def find_cooccurrences(entity_positions, interaction_positions, window=COOCCURRENCE_WINDOW):
    """Find co-occurrences of entity + interaction markers within window."""
    candidates = []
    used_ranges = set()

    for e_start, e_end, e_term in entity_positions:
        for i_start, i_end, i_term, i_type in interaction_positions:
            # Check if within window
            center_dist = abs((e_start + e_end) // 2 - (i_start + i_end) // 2)
            if center_dist > window:
                continue

            # Compute bounding range
            range_start = min(e_start, i_start)
            range_end = max(e_end, i_end)
            range_key = (range_start // 200, range_end // 200)  # coarse dedup

            if range_key in used_ranges:
                # Update existing candidate if higher score
                for c in candidates:
                    if (c['_range_key'] == range_key):
                        if e_term not in c['matched_terms']:
                            c['matched_terms'].append(e_term)
                        if i_term not in c['matched_terms']:
                            c['matched_terms'].append(i_term)
                        c['match_score'] += 1
                        if i_type not in c['interaction_types']:
                            c['interaction_types'].append(i_type)
                        break
                continue

            used_ranges.add(range_key)
            candidates.append({
                'range_start': range_start,
                'range_end': range_end,
                'matched_terms': [e_term, i_term],
                'interaction_types': [i_type],
                'match_score': 1,
                '_range_key': range_key,
            })

    return candidates


def extract_scene_window(text, range_start, range_end, context=CONTEXT_WINDOW):
    """Extract a scene text window with context, snapping to sentence boundaries."""
    center = (range_start + range_end) // 2

    # Expand window
    start = max(0, center - context)
    end = min(len(text), center + context)

    # Snap to sentence boundaries (looking outward)
    for i in range(start, min(start + 200, range_start)):
        if text[i] in '.!?\n' and i + 1 < len(text):
            start = i + 1
            break

    for i in range(end, max(end - 200, range_end), -1):
        if i < len(text) and text[i] in '.!?\n':
            end = i + 1
            break

    passage = text[start:end].strip()

    # Hard cap
    if len(passage) > MAX_PASSAGE_CHARS:
        passage = passage[:MAX_PASSAGE_CHARS].rsplit(' ', 1)[0] + '...'

    return passage, start, end


def deduplicate_candidates(candidates):
    """Remove overlapping candidates, keeping the one with highest match_score."""
    if not candidates:
        return candidates

    candidates.sort(key=lambda c: c['char_offset_start'])
    deduped = [candidates[0]]

    for c in candidates[1:]:
        prev = deduped[-1]
        # Check overlap
        if c['char_offset_start'] < prev['char_offset_end']:
            # Overlapping — keep higher score
            if c['match_score'] > prev['match_score']:
                deduped[-1] = c
        else:
            deduped.append(c)

    return deduped


def run(db: sqlite3.Connection, _source: Path = None):
    """Scan fiction corpus for AI scene candidates."""
    print("  Scanning fiction corpus for AI scene candidates...")

    # Ensure tables exist
    schema_path = PROJECT_DIR / 'database' / 'scenes_schema.sql'
    if schema_path.exists():
        db.executescript(schema_path.read_text(encoding='utf-8'))

    entity_pattern, interaction_patterns = load_scene_lexicon()
    fiction_docs = load_fiction_corpus(db)

    if not fiction_docs:
        print("    WARNING: No fiction documents with extracted text found")
        return

    total_candidates = 0

    for doc_id, title, text_content in fiction_docs:
        entity_positions = find_entity_positions(text_content, entity_pattern)
        if not entity_positions:
            continue

        interaction_positions = find_interaction_positions(text_content, interaction_patterns)
        if not interaction_positions:
            continue

        cooccurrences = find_cooccurrences(entity_positions, interaction_positions)
        if not cooccurrences:
            continue

        # Extract windows and build candidate records
        doc_candidates = []
        for co in cooccurrences:
            passage, char_start, char_end = extract_scene_window(
                text_content, co['range_start'], co['range_end']
            )
            best_type = co['interaction_types'][0]  # first detected type

            doc_candidates.append({
                'work_id': doc_id,
                'work_title': title,
                'doc_id': doc_id,
                'char_offset_start': char_start,
                'char_offset_end': char_end,
                'source_window_text': passage,
                'matched_terms': co['matched_terms'],
                'matched_interaction': best_type,
                'match_score': co['match_score'],
            })

        # Deduplicate
        doc_candidates = deduplicate_candidates(doc_candidates)

        # Insert
        for c in doc_candidates:
            db.execute("""
                INSERT INTO ai_scene_candidates
                    (work_id, work_title, doc_id,
                     char_offset_start, char_offset_end,
                     source_window_text, matched_terms, matched_interaction,
                     match_score, detection_method, promotion_status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'lexicon', 'pending')
            """, (
                c['work_id'], c['work_title'], c['doc_id'],
                c['char_offset_start'], c['char_offset_end'],
                c['source_window_text'], json.dumps(c['matched_terms']),
                c['matched_interaction'], c['match_score'],
            ))

        total_candidates += len(doc_candidates)
        if doc_candidates:
            print(f"    {title}: {len(doc_candidates)} candidates")

    db.commit()
    print(f"    Total scene candidates: {total_candidates}")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Scan fiction for AI scene candidates')
    parser.add_argument('--db', type=Path, default=DEFAULT_DB)
    args = parser.parse_args()

    db = sqlite3.connect(str(args.db))
    db.execute("PRAGMA foreign_keys = ON")
    run(db)
    db.close()
