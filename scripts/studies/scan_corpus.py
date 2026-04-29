#!/usr/bin/env python3
"""
Stage 5b: Deterministic corpus scanning for study topics.

Scans corpus text (segments.raw_text + document_texts.text_content) against
topic lexicons and writes matched passages to study_passages.

Architecture (follows discovery_pipeline.py):
  1. Load topic lexicons from JSON files
  2. Compile regex patterns per topic
  3. Materialize corpus text once
  4. Scan all text against all topic patterns
  5. Extract passage windows around matches
  6. Deduplicate overlapping windows
  7. Write to study_passages with lane assignment

Usage:
    python scripts/studies/scan_corpus.py
    python scripts/studies/scan_corpus.py --study ai
    python scripts/studies/scan_corpus.py --study psychology
    python scripts/studies/scan_corpus.py --topic paranoia
"""

import json
import re
import sqlite3
import sys
import time
from collections import defaultdict
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

PROJECT_DIR = SCRIPTS_DIR.parent
DEFAULT_DB = PROJECT_DIR / 'database' / 'unified.sqlite'
LEXICON_DIR = Path(__file__).resolve().parent / 'lexicons'

# Maximum passage length (chars) for fair-use compliance
MAX_PASSAGE_CHARS = 2000
# Context window around a match (chars each side)
CONTEXT_WINDOW = 500


# ── Lexicon loading ───────────────────────────────────────────

def load_lexicons(study_id: str = None):
    """Load topic lexicons from JSON files. Returns {topic_slug: lexicon_dict}."""
    lexicons = {}
    files = []
    if study_id in (None, 'ai'):
        files.append(('ai', LEXICON_DIR / 'ai_topics.json'))
    if study_id in (None, 'psychology'):
        files.append(('psychology', LEXICON_DIR / 'psychology_topics.json'))

    for sid, path in files:
        if not path.exists():
            print(f"    WARNING: Lexicon file not found: {path}")
            continue
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for slug, lex in data.items():
            lex['_study_id'] = sid
            lex['_slug'] = slug
            lexicons[f"{sid}:{slug}"] = lex
    return lexicons


def compile_patterns(lexicons: dict):
    """Compile regex patterns for each topic. Returns {key: (pattern, exclusion_pattern)}."""
    compiled = {}
    for key, lex in lexicons.items():
        # Build match terms (primary + aliases)
        terms = list(lex.get('primary', []))
        terms.extend(lex.get('aliases', []))
        if not terms:
            continue
        # Sort by length descending so longer phrases match first
        terms.sort(key=len, reverse=True)
        # Escape and join
        escaped = [re.escape(t) for t in terms]
        pattern = re.compile(r'\b(' + '|'.join(escaped) + r')\b', re.IGNORECASE)

        # Exclusions
        excl_pattern = None
        excl_terms = lex.get('exclusions', [])
        if excl_terms:
            excl_escaped = [re.escape(t) for t in excl_terms]
            excl_pattern = re.compile(r'\b(' + '|'.join(excl_escaped) + r')\b', re.IGNORECASE)

        compiled[key] = (pattern, excl_pattern)
    return compiled


# ── Corpus materialization ────────────────────────────────────

def materialize_segments(db: sqlite3.Connection):
    """Load all segments with raw text. Returns list of (seg_id, doc_id, text)."""
    rows = db.execute("""
        SELECT s.seg_id, s.doc_id, s.raw_text
        FROM segments s
        WHERE s.raw_text IS NOT NULL AND length(s.raw_text) > 50
    """).fetchall()
    print(f"    Materialized {len(rows)} segments with raw text")
    return rows


def materialize_documents(db: sqlite3.Connection):
    """Load all document texts. Returns list of (doc_id, text, lane)."""
    # Check if evidentiary_lane column exists
    cols = [c[1] for c in db.execute("PRAGMA table_info(documents)").fetchall()]
    has_lane = 'evidentiary_lane' in cols

    lane_col = ", d.evidentiary_lane" if has_lane else ""
    rows = db.execute(f"""
        SELECT dt.doc_id, dt.text_content{lane_col}
        FROM document_texts dt
        JOIN documents d ON dt.doc_id = d.doc_id
        WHERE dt.text_content IS NOT NULL AND length(dt.text_content) > 50
    """).fetchall()
    print(f"    Materialized {len(rows)} documents with extracted text")
    return [(r[0], r[1], r[2] if has_lane and len(r) > 2 else None) for r in rows]


# ── Lane assignment ───────────────────────────────────────────

def get_lane_for_doc(db: sqlite3.Connection, doc_id: str, _cache={}):
    """Get evidentiary lane for a document. Uses cache."""
    if doc_id in _cache:
        return _cache[doc_id]

    row = db.execute("""
        SELECT evidentiary_lane, doc_type FROM documents WHERE doc_id = ?
    """, (doc_id,)).fetchone()

    if not row:
        _cache[doc_id] = None
        return None

    lane = row[0]
    if not lane:
        # Infer from doc_type
        doc_type = row[1]
        if doc_type in ('novel', 'short_story'):
            lane = 'A'
        elif doc_type in ('exegesis_section',):
            lane = 'B'
        else:
            lane = 'C'

    _cache[doc_id] = lane
    return lane


def get_segment_lane(db: sqlite3.Connection, seg_id: str, doc_id: str):
    """Segments are always Exegesis (Lane B) in QueryPat."""
    # All segments in QueryPat are from the Exegesis
    return 'B'


# ── Passage extraction ────────────────────────────────────────

def extract_passage_window(text: str, match_start: int, match_end: int,
                           window: int = CONTEXT_WINDOW):
    """Extract a passage window around a match with context."""
    # Find sentence boundary before match
    start = max(0, match_start - window)
    # Try to start at a sentence boundary
    for i in range(start, match_start):
        if text[i] in '.!?\n' and i + 1 < len(text):
            start = i + 1
            break

    # Find sentence boundary after match
    end = min(len(text), match_end + window)
    for i in range(match_end, end):
        if text[i] in '.!?\n':
            end = i + 1
            break

    passage = text[start:end].strip()

    # Cap length
    if len(passage) > MAX_PASSAGE_CHARS:
        passage = passage[:MAX_PASSAGE_CHARS].rsplit(' ', 1)[0] + '...'

    # Context snippets
    ctx_before = text[max(0, start - 100):start].strip() if start > 0 else None
    ctx_after = text[end:min(len(text), end + 100)].strip() if end < len(text) else None

    return passage, ctx_before, ctx_after, start, end


# ── Deduplication ─────────────────────────────────────────────

def deduplicate_passages(passages: list):
    """Remove passages with substantially overlapping text windows."""
    if not passages:
        return passages

    # Sort by (source_id, char_offset_start)
    passages.sort(key=lambda p: (p.get('doc_id', '') or p.get('seg_id', ''),
                                  p.get('char_offset_start', 0)))

    deduped = [passages[0]]
    for p in passages[1:]:
        prev = deduped[-1]
        same_source = (p.get('doc_id') == prev.get('doc_id') and
                       p.get('seg_id') == prev.get('seg_id'))
        if same_source:
            # Check overlap
            prev_end = prev.get('char_offset_end', 0)
            curr_start = p.get('char_offset_start', 0)
            if curr_start < prev_end:
                # Overlapping — keep the one with more matched terms
                if len(p.get('matched_terms', [])) > len(prev.get('matched_terms', [])):
                    deduped[-1] = p
                continue
        deduped.append(p)

    return deduped


# ── Topic ID lookup ───────────────────────────────────────────

def load_topic_ids(db: sqlite3.Connection):
    """Load mapping of (study_id, slug) → topic_id."""
    rows = db.execute("SELECT topic_id, study_id, slug FROM study_topics").fetchall()
    return {(r[1], r[2]): r[0] for r in rows}


# ── Main scan ─────────────────────────────────────────────────

def scan_corpus(db: sqlite3.Connection, study_id: str = None, topic_slug: str = None):
    """Scan the corpus for study topic matches."""
    print("  Loading lexicons...")
    lexicons = load_lexicons(study_id)
    if topic_slug:
        lexicons = {k: v for k, v in lexicons.items() if v['_slug'] == topic_slug}

    if not lexicons:
        print("    No lexicons to scan")
        return

    print(f"    {len(lexicons)} topic lexicons loaded")

    print("  Compiling patterns...")
    patterns = compile_patterns(lexicons)

    print("  Materializing corpus...")
    segments = materialize_segments(db)
    documents = materialize_documents(db)

    topic_ids = load_topic_ids(db)

    # Collect all passages before writing
    all_passages = defaultdict(list)  # topic_key → [passage_dicts]
    total_matches = 0

    # Scan segments (Exegesis — Lane B)
    print("  Scanning segments...")
    for seg_id, doc_id, text in segments:
        for key, (pattern, excl_pattern) in patterns.items():
            for match in pattern.finditer(text):
                # Check exclusions
                if excl_pattern:
                    # Check if the match context triggers an exclusion
                    ctx_start = max(0, match.start() - 50)
                    ctx_end = min(len(text), match.end() + 50)
                    context = text[ctx_start:ctx_end]
                    if excl_pattern.search(context):
                        continue

                passage_text, ctx_before, ctx_after, p_start, p_end = \
                    extract_passage_window(text, match.start(), match.end())

                lex = lexicons[key]
                matched_term = match.group(0)
                is_primary = matched_term.lower() in [t.lower() for t in lex.get('primary', [])]

                all_passages[key].append({
                    'doc_id': doc_id,
                    'seg_id': seg_id,
                    'page_num': None,
                    'char_offset_start': p_start,
                    'char_offset_end': p_end,
                    'passage_text': passage_text,
                    'context_before': ctx_before,
                    'context_after': ctx_after,
                    'lane': 'B',
                    'matched_terms': [matched_term],
                    'match_method': 'lexicon_exact' if is_primary else 'lexicon_alias',
                })
                total_matches += 1

    # Scan documents (Archive — Lane A, C, or E)
    print("  Scanning documents...")
    for doc_id, text, doc_lane in documents:
        lane = doc_lane
        if not lane:
            lane = get_lane_for_doc(db, doc_id)
        # Map archive lanes to study lanes
        if lane in ('D', 'E'):
            lane = 'C'  # Synthesis and Primary → Scholarship for study purposes

        for key, (pattern, excl_pattern) in patterns.items():
            for match in pattern.finditer(text):
                if excl_pattern:
                    ctx_start = max(0, match.start() - 50)
                    ctx_end = min(len(text), match.end() + 50)
                    context = text[ctx_start:ctx_end]
                    if excl_pattern.search(context):
                        continue

                passage_text, ctx_before, ctx_after, p_start, p_end = \
                    extract_passage_window(text, match.start(), match.end())

                lex = lexicons[key]
                matched_term = match.group(0)
                is_primary = matched_term.lower() in [t.lower() for t in lex.get('primary', [])]

                all_passages[key].append({
                    'doc_id': doc_id,
                    'seg_id': None,
                    'page_num': None,
                    'char_offset_start': p_start,
                    'char_offset_end': p_end,
                    'passage_text': passage_text,
                    'context_before': ctx_before,
                    'context_after': ctx_after,
                    'lane': lane,
                    'matched_terms': [matched_term],
                    'match_method': 'lexicon_exact' if is_primary else 'lexicon_alias',
                })
                total_matches += 1

    print(f"    {total_matches} raw matches found across {len(all_passages)} topics")

    # Deduplicate and write
    print("  Deduplicating and writing passages...")
    total_written = 0
    for key, passages in all_passages.items():
        lex = lexicons[key]
        sid = lex['_study_id']
        slug = lex['_slug']
        topic_id = topic_ids.get((sid, slug))
        if not topic_id:
            print(f"    WARNING: No topic_id for {sid}:{slug}")
            continue

        deduped = deduplicate_passages(passages)

        for p in deduped:
            db.execute("""
                INSERT INTO study_passages
                    (topic_id, doc_id, seg_id, page_num,
                     char_offset_start, char_offset_end,
                     passage_text, context_before, context_after,
                     lane, matched_terms, match_method)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                topic_id, p['doc_id'], p['seg_id'], p['page_num'],
                p['char_offset_start'], p['char_offset_end'],
                p['passage_text'], p['context_before'], p['context_after'],
                p['lane'], json.dumps(p['matched_terms']), p['match_method'],
            ))
            total_written += 1

        # Update topic passage count and status
        db.execute("""
            UPDATE study_topics SET passage_count = ?, status = 'scanning'
            WHERE topic_id = ?
        """, (len(deduped), topic_id))

    db.commit()
    print(f"    {total_written} passages written after deduplication")

    # Summary by study
    for sid in ('ai', 'psychology'):
        count = db.execute("""
            SELECT COUNT(*) FROM study_passages sp
            JOIN study_topics st ON sp.topic_id = st.topic_id
            WHERE st.study_id = ?
        """, (sid,)).fetchone()[0]
        topic_count = db.execute("""
            SELECT COUNT(*) FROM study_topics
            WHERE study_id = ? AND passage_count > 0
        """, (sid,)).fetchone()[0]
        print(f"    {sid}: {count} passages across {topic_count} topics")


def run(db: sqlite3.Connection, source: Path = None,
        study_id: str = None, topic_slug: str = None):
    """Run corpus scan."""
    print("  Scanning corpus for study topics...")

    # Clear existing passages if re-running
    if topic_slug:
        # Clear specific topic
        topic_ids = load_topic_ids(db)
        for (sid, slug), tid in topic_ids.items():
            if slug == topic_slug:
                db.execute("DELETE FROM study_passages WHERE topic_id = ?", (tid,))
    elif study_id:
        # Clear specific study
        db.execute("""
            DELETE FROM study_passages WHERE topic_id IN (
                SELECT topic_id FROM study_topics WHERE study_id = ?
            )
        """, (study_id,))
    else:
        # Clear all
        db.execute("DELETE FROM study_passages")
    db.commit()

    scan_corpus(db, study_id, topic_slug)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Scan corpus for study topics')
    parser.add_argument('--db', type=Path, default=DEFAULT_DB)
    parser.add_argument('--study', type=str, choices=['ai', 'psychology'],
                        help='Scan only one study')
    parser.add_argument('--topic', type=str,
                        help='Scan only one topic slug')
    args = parser.parse_args()

    start = time.time()
    db = sqlite3.connect(str(args.db))
    db.execute("PRAGMA foreign_keys = ON")
    run(db, study_id=args.study, topic_slug=args.topic)
    db.close()
    elapsed = time.time() - start
    print(f"Done in {elapsed:.1f}s")
