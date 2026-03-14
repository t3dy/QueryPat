"""
Stage 2: Upgrade term-segment link confidence using actual text matching.

Scans segment raw_text and concise_summary for exact term name and alias
matches. Promotes existing confidence-4 links to confidence 1-2 when
text evidence is found, and creates new high-confidence links where
text mentions exist but no link was recorded.

Confidence model:
  1 = exact canonical name match in raw_text
  2 = alias exact match or match in summary/key_claims
  3 = fuzzy/normalized match
  4 = imported conceptual link (no text validation)
  5 = speculative/weak
"""

import json
import re
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def build_term_patterns(db: sqlite3.Connection) -> list[tuple[str, str, list[str]]]:
    """Build search patterns for each term: (term_id, canonical_name, [aliases])."""
    terms = []

    rows = db.execute("""
        SELECT t.term_id, t.canonical_name
        FROM terms t
        WHERE t.status IN ('accepted', 'provisional', 'background')
    """).fetchall()

    for term_id, canonical_name in rows:
        aliases = []
        alias_rows = db.execute(
            "SELECT alias_text FROM term_aliases WHERE term_id = ?",
            (term_id,)
        ).fetchall()
        for (alias_text,) in alias_rows:
            if alias_text and alias_text.lower() != canonical_name.lower():
                aliases.append(alias_text)

        terms.append((term_id, canonical_name, aliases))

    return terms


def text_contains_term(text: str, term_name: str) -> str | None:
    """
    Check if text contains the term as a word boundary match.
    Returns the matched text if found, None otherwise.
    Skips very short terms (< 3 chars) to avoid false positives.
    """
    if not text or not term_name or len(term_name) < 3:
        return None

    # Escape regex special chars in term name
    escaped = re.escape(term_name)

    # Word boundary match, case-insensitive
    pattern = r'\b' + escaped + r'\b'
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(0)
    return None


def run(db: sqlite3.Connection, source_dir: Path):
    """Upgrade term-segment links using text evidence."""
    print("Upgrading term-segment link confidence...")

    terms = build_term_patterns(db)
    print(f"  {len(terms)} terms with patterns to match")

    # Get segments with text content
    segments = db.execute("""
        SELECT seg_id, raw_text, concise_summary, key_claims
        FROM segments
        WHERE raw_text IS NOT NULL OR concise_summary IS NOT NULL
    """).fetchall()
    print(f"  {len(segments)} segments with searchable text")

    # Build segment text cache: seg_id -> (raw_text, summary_text)
    seg_texts = {}
    for seg_id, raw_text, summary, key_claims in segments:
        summary_text = summary or ''
        if key_claims:
            try:
                claims = json.loads(key_claims)
                if isinstance(claims, list):
                    summary_text += ' ' + ' '.join(
                        c for c in claims if isinstance(c, str)
                    )
            except (json.JSONDecodeError, TypeError):
                pass
        seg_texts[seg_id] = (raw_text or '', summary_text)

    # Get existing links for fast lookup
    existing_links = set()
    rows = db.execute("""
        SELECT term_id, seg_id, match_type, link_confidence
        FROM term_segments
    """).fetchall()
    for term_id, seg_id, match_type, confidence in rows:
        existing_links.add((term_id, seg_id, match_type))

    print(f"  {len(existing_links)} existing term-segment links")

    upgraded = 0
    new_links = 0
    batch = []

    for term_id, canonical_name, aliases in terms:
        # Skip very short or generic terms
        if len(canonical_name) < 3:
            continue

        for seg_id, (raw_text, summary_text) in seg_texts.items():
            # Check canonical name in raw text (confidence 1)
            matched = text_contains_term(raw_text, canonical_name)
            if matched:
                key = (term_id, seg_id, 'exact_mention')
                if key not in existing_links:
                    batch.append((
                        term_id, seg_id, 'exact_mention', 1,
                        'text_string_match', matched
                    ))
                    existing_links.add(key)
                    new_links += 1
                else:
                    # Upgrade existing link confidence
                    db.execute("""
                        UPDATE term_segments
                        SET link_confidence = MIN(link_confidence, 1),
                            matched_text = ?
                        WHERE term_id = ? AND seg_id = ? AND match_type = 'exact_mention'
                    """, (matched, term_id, seg_id))
                    upgraded += 1
                continue  # Found canonical match, no need to check aliases

            # Check canonical name in summary (confidence 2)
            matched = text_contains_term(summary_text, canonical_name)
            if matched:
                key = (term_id, seg_id, 'exact_mention')
                if key not in existing_links:
                    batch.append((
                        term_id, seg_id, 'exact_mention', 2,
                        'summary_string_match', matched
                    ))
                    existing_links.add(key)
                    new_links += 1
                else:
                    db.execute("""
                        UPDATE term_segments
                        SET link_confidence = MIN(link_confidence, 2),
                            matched_text = ?
                        WHERE term_id = ? AND seg_id = ? AND match_type = 'exact_mention'
                    """, (matched, term_id, seg_id))
                    upgraded += 1
                continue

            # Check aliases in raw text (confidence 2)
            for alias in aliases:
                matched = text_contains_term(raw_text, alias)
                if matched:
                    key = (term_id, seg_id, 'alias_mention')
                    if key not in existing_links:
                        batch.append((
                            term_id, seg_id, 'alias_mention', 2,
                            'alias_text_match', matched
                        ))
                        existing_links.add(key)
                        new_links += 1
                    break

        # Batch insert periodically
        if len(batch) >= 5000:
            db.executemany("""
                INSERT OR IGNORE INTO term_segments
                    (term_id, seg_id, match_type, link_confidence, link_method, matched_text)
                VALUES (?, ?, ?, ?, ?, ?)
            """, batch)
            db.commit()
            batch = []

    # Insert remaining
    if batch:
        db.executemany("""
            INSERT OR IGNORE INTO term_segments
                (term_id, seg_id, match_type, link_confidence, link_method, matched_text)
            VALUES (?, ?, ?, ?, ?, ?)
        """, batch)

    db.commit()

    print(f"  Upgraded {upgraded} existing links to higher confidence")
    print(f"  Created {new_links} new text-confirmed links")

    # Report confidence distribution
    dist = db.execute("""
        SELECT link_confidence, COUNT(*) FROM term_segments
        GROUP BY link_confidence ORDER BY link_confidence
    """).fetchall()
    for conf, count in dist:
        labels = {1: 'exact text', 2: 'alias/summary', 3: 'fuzzy',
                  4: 'conceptual CSV', 5: 'speculative'}
        print(f"    Confidence {conf} ({labels.get(conf, '?')}): {count}")


if __name__ == '__main__':
    db_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('C:/QueryPat/database/unified.sqlite')
    db = sqlite3.connect(str(db_path))
    run(db, Path('C:/ExegesisAnalysis'))
    db.close()
