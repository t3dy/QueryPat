"""
Cross-link fiction characters to Exegesis segments.

Scans segments.raw_text and segments.people_entities for mentions of
fiction character names. Creates name_segments links at confidence 3
(heuristic text match) for raw_text matches and confidence 2 for
people_entities matches.
"""

import json
import re
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from date_norms import make_name_id


def run(db: sqlite3.Connection, source_dir: Path):
    print("Linking fiction characters to segments...")

    # Get all fiction characters
    characters = db.execute("""
        SELECT name_id, canonical_form, slug
        FROM names
        WHERE entity_type = 'character'
          AND canonical_form IS NOT NULL
    """).fetchall()

    if not characters:
        print("  No fiction characters found — skipping")
        return

    # Build search patterns: only match names with 2+ chars, skip very short/ambiguous ones
    SKIP_NAMES = {
        'Phil', 'Nick', 'Beth', 'David', 'Kevin', 'Curt', 'Mali', 'Nina',
        'Klaus', 'Mission', 'Emmanuel', 'Belial', 'Thomas (apostle)',
    }

    search_chars = []
    for name_id, canonical, slug in characters:
        # Skip very short or ambiguous names
        if canonical in SKIP_NAMES:
            continue
        # Need at least a surname or distinctive name (5+ chars)
        if len(canonical) < 5:
            continue
        # Build word-boundary regex for the canonical name
        # Handle parenthetical names like "Isidore (J.R.)"
        search_name = re.sub(r'\s*\([^)]*\)\s*', '', canonical).strip()
        if not search_name or len(search_name) < 4:
            continue
        search_chars.append((name_id, canonical, search_name))

    print(f"  Searching for {len(search_chars)} character names in segments...")

    # Get all segments with raw_text
    segments = db.execute("""
        SELECT seg_id, raw_text, people_entities
        FROM segments
        WHERE raw_text IS NOT NULL OR people_entities IS NOT NULL
    """).fetchall()

    # Pre-compile patterns
    patterns = []
    for name_id, canonical, search_name in search_chars:
        # Escape regex special chars in name
        escaped = re.escape(search_name)
        try:
            pat = re.compile(r'\b' + escaped + r'\b', re.IGNORECASE)
            patterns.append((name_id, canonical, search_name, pat))
        except re.error:
            continue

    links_added = 0
    links_skipped = 0

    for seg_id, raw_text, pe_json in segments:
        text = raw_text or ''
        pe_text = pe_json or ''

        for name_id, canonical, search_name, pat in patterns:
            # Check people_entities first (higher confidence)
            if search_name.lower() in pe_text.lower():
                try:
                    db.execute("""
                        INSERT OR IGNORE INTO name_segments
                            (name_id, seg_id, match_type, link_confidence,
                             link_method, matched_text)
                        VALUES (?, ?, 'exact_mention', 2,
                                'fiction_character_pe_match', ?)
                    """, (name_id, seg_id, search_name))
                    links_added += 1
                except sqlite3.IntegrityError:
                    links_skipped += 1
                continue

            # Check raw_text (lower confidence)
            if text and pat.search(text):
                match = pat.search(text)
                # Extract a small context snippet
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                snippet = text[start:end].strip()

                try:
                    db.execute("""
                        INSERT OR IGNORE INTO name_segments
                            (name_id, seg_id, match_type, link_confidence,
                             link_method, matched_text, context_snippet)
                        VALUES (?, ?, 'text_mention', 3,
                                'fiction_character_text_match', ?, ?)
                    """, (name_id, seg_id, search_name, snippet))
                    links_added += 1
                except sqlite3.IntegrityError:
                    links_skipped += 1

    db.commit()
    print(f"  Links added: {links_added}, skipped (existing): {links_skipped}")


if __name__ == '__main__':
    db_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('C:/QueryPat/database/unified.sqlite')
    db = sqlite3.connect(str(db_path))
    run(db, Path('C:/ExegesisAnalysis'))
    db.close()
