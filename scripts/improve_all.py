#!/usr/bin/env python3
"""
Execute all 20 improvement plans against the unified database.

Deterministic plans run directly. LLM-dependent plans are prepared
with data extraction and stub generation.

Usage:
    python scripts/improve_all.py [--db database/unified.sqlite]
"""

import sqlite3
import json
import re
import sys
from pathlib import Path
from collections import defaultdict, Counter

SCRIPTS_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPTS_DIR.parent
SITE_DATA = PROJECT_DIR / 'site' / 'public' / 'data'
DEFAULT_DB = PROJECT_DIR / 'database' / 'unified.sqlite'

sys.path.insert(0, str(SCRIPTS_DIR))
from date_norms import make_term_id


def get_db(db_path=None):
    db = sqlite3.connect(str(db_path or DEFAULT_DB))
    db.execute("PRAGMA journal_mode = WAL")
    db.execute("PRAGMA foreign_keys = ON")
    db.row_factory = sqlite3.Row
    return db


# ---------------------------------------------------------------------------
# PLAN 2: Fill related_terms from co-occurrence data
# ---------------------------------------------------------------------------
def plan_02_fill_related_terms(db):
    print("\n" + "=" * 60)
    print("PLAN 2: Fill related_terms from co-occurrence data")
    print("=" * 60)

    # Find terms with <3 relations that are accepted/provisional
    lonely_terms = db.execute("""
        SELECT term_id, canonical_name, status, rel_count FROM (
            SELECT t.term_id, t.canonical_name, t.status,
                (SELECT COUNT(*) FROM term_terms tt
                 WHERE tt.term_id_a = t.term_id OR tt.term_id_b = t.term_id) as rel_count
            FROM terms t
            WHERE t.status IN ('accepted', 'provisional')
        ) WHERE rel_count < 3
        ORDER BY rel_count ASC
    """).fetchall()

    print(f"  Terms with <3 relations: {len(lonely_terms)}")

    # Aggregate co-occurrences by term pair
    cooc_pairs = db.execute("""
        SELECT term_id_a, term_id_b, SUM(weight) as total_weight, COUNT(*) as occurrences
        FROM term_cooccurrences
        GROUP BY term_id_a, term_id_b
        HAVING occurrences >= 3
        ORDER BY total_weight DESC
    """).fetchall()

    # Build lookup: term_id -> [(other_term_id, weight)]
    cooc_map = defaultdict(list)
    for row in cooc_pairs:
        cooc_map[row['term_id_a']].append((row['term_id_b'], row['total_weight']))
        cooc_map[row['term_id_b']].append((row['term_id_a'], row['total_weight']))

    # Get existing relations
    existing = set()
    for row in db.execute("SELECT term_id_a, term_id_b FROM term_terms"):
        existing.add((row['term_id_a'], row['term_id_b']))
        existing.add((row['term_id_b'], row['term_id_a']))

    # Get valid term IDs (accepted/provisional only)
    valid_terms = set(r['term_id'] for r in db.execute(
        "SELECT term_id FROM terms WHERE status IN ('accepted', 'provisional')"))

    added = 0
    for term in lonely_terms:
        tid = term['term_id']
        candidates = cooc_map.get(tid, [])
        # Sort by weight, pick top 5 that aren't already related
        candidates.sort(key=lambda x: x[1], reverse=True)
        for other_tid, weight in candidates[:10]:
            if other_tid == tid:
                continue
            if (tid, other_tid) in existing:
                continue
            if other_tid not in valid_terms:
                continue
            db.execute("""
                INSERT OR IGNORE INTO term_terms
                (term_id_a, term_id_b, relation_type, strength, link_confidence, link_method)
                VALUES (?, ?, 'co_occurs', ?, 2, 'cooccurrence_mining')
            """, (tid, other_tid, weight))
            existing.add((tid, other_tid))
            existing.add((other_tid, tid))
            added += 1
            # Stop after adding enough to reach 3
            current = db.execute("""
                SELECT COUNT(*) as c FROM term_terms
                WHERE term_id_a = ? OR term_id_b = ?
            """, (tid, tid)).fetchone()['c']
            if current >= 5:
                break

    db.commit()
    print(f"  Added {added} new co-occurrence relations")


# ---------------------------------------------------------------------------
# PLAN 11: Tag all documents with evidentiary lanes
# ---------------------------------------------------------------------------
def plan_11_evidentiary_lanes(db):
    print("\n" + "=" * 60)
    print("PLAN 11: Tag documents with evidentiary lanes")
    print("=" * 60)

    # Add columns if they don't exist
    try:
        db.execute("ALTER TABLE documents ADD COLUMN evidentiary_lane TEXT")
        print("  Added evidentiary_lane column")
    except sqlite3.OperationalError:
        pass  # Already exists

    try:
        db.execute("ALTER TABLE documents ADD COLUMN source_reliability TEXT")
        print("  Added source_reliability column")
    except sqlite3.OperationalError:
        pass

    # Deterministic lane assignment
    rules = [
        # Lane A: Fiction
        ("UPDATE documents SET evidentiary_lane = 'A' WHERE category IN ('novels', 'short_stories')", "Lane A (Fiction)"),
        # Lane B: Exegesis
        ("UPDATE documents SET evidentiary_lane = 'B' WHERE doc_type = 'exegesis_section'", "Lane B (Exegesis)"),
        # Lane C: Scholarship
        ("UPDATE documents SET evidentiary_lane = 'C' WHERE category = 'scholarship'", "Lane C (Scholarship)"),
        ("UPDATE documents SET evidentiary_lane = 'C' WHERE category = 'fan_publications'", "Lane C (Fan -> Scholarship)"),
        # Lane D: Synthesis
        ("UPDATE documents SET evidentiary_lane = 'D' WHERE category = 'biographies'", "Lane D (Synthesis/Biographies)"),
        # Lane E: Primary documents
        ("UPDATE documents SET evidentiary_lane = 'E' WHERE category = 'newspaper'", "Lane E (Newspaper)"),
        ("UPDATE documents SET evidentiary_lane = 'E' WHERE category = 'letters'", "Lane E (Letters)"),
        ("UPDATE documents SET evidentiary_lane = 'E' WHERE category = 'interviews'", "Lane E (Interviews)"),
        # Primary PKD writings
        ("UPDATE documents SET evidentiary_lane = 'B' WHERE category = 'primary' AND is_pkd_authored = 1", "Lane B (PKD primary)"),
        ("UPDATE documents SET evidentiary_lane = 'E' WHERE category = 'primary' AND (is_pkd_authored IS NULL OR is_pkd_authored = 0)", "Lane E (Non-PKD primary)"),
        # Other/uncategorized
        ("UPDATE documents SET evidentiary_lane = 'E' WHERE evidentiary_lane IS NULL AND category = 'other'", "Lane E (Other)"),
        ("UPDATE documents SET evidentiary_lane = 'C' WHERE evidentiary_lane IS NULL AND category IS NULL", "Lane C (Uncategorized -> Scholarship default)"),
    ]

    for sql, label in rules:
        try:
            cursor = db.execute(sql)
            if cursor.rowcount > 0:
                print(f"  {label}: {cursor.rowcount} docs")
        except sqlite3.OperationalError as e:
            print(f"  {label}: SKIP ({e})")

    # Source reliability
    reliability_rules = [
        ("UPDATE documents SET source_reliability = 'primary_pkd' WHERE is_pkd_authored = 1", "primary_pkd"),
        ("UPDATE documents SET source_reliability = 'primary_other' WHERE category = 'newspaper' AND source_reliability IS NULL", "primary_other (newspaper)"),
        ("UPDATE documents SET source_reliability = 'primary_other' WHERE category IN ('letters', 'interviews') AND is_pkd_authored != 1 AND source_reliability IS NULL", "primary_other"),
        ("UPDATE documents SET source_reliability = 'secondary_scholarship' WHERE category IN ('scholarship', 'biographies') AND source_reliability IS NULL", "secondary_scholarship"),
        ("UPDATE documents SET source_reliability = 'secondary_popular' WHERE category = 'fan_publications' AND source_reliability IS NULL", "secondary_popular"),
        ("UPDATE documents SET source_reliability = 'secondary_popular' WHERE source_reliability IS NULL", "secondary_popular (default)"),
    ]

    for sql, label in reliability_rules:
        try:
            cursor = db.execute(sql)
            if cursor.rowcount > 0:
                print(f"  Reliability {label}: {cursor.rowcount} docs")
        except sqlite3.OperationalError as e:
            print(f"  Reliability {label}: SKIP ({e})")

    db.commit()

    # Report
    lanes = db.execute("SELECT evidentiary_lane, COUNT(*) as c FROM documents GROUP BY evidentiary_lane ORDER BY evidentiary_lane").fetchall()
    print("  Final lane distribution:")
    for row in lanes:
        print(f"    Lane {row['evidentiary_lane']}: {row['c']} docs")


# ---------------------------------------------------------------------------
# PLAN 16: Add mentioned_in_segments counts to all names
# ---------------------------------------------------------------------------
def plan_16_name_segment_counts(db):
    print("\n" + "=" * 60)
    print("PLAN 16: Compute name segment mention counts")
    print("=" * 60)

    # Add column if not exists
    try:
        db.execute("ALTER TABLE names ADD COLUMN segment_mention_count INTEGER DEFAULT 0")
        print("  Added segment_mention_count column")
    except sqlite3.OperationalError:
        pass

    db.execute("""
        UPDATE names SET segment_mention_count = (
            SELECT COUNT(DISTINCT seg_id) FROM name_segments ns WHERE ns.name_id = names.name_id
        )
    """)
    db.commit()

    top = db.execute("""
        SELECT canonical_form, entity_type, segment_mention_count
        FROM names
        ORDER BY segment_mention_count DESC LIMIT 15
    """).fetchall()
    print("  Top 15 most-mentioned names:")
    for row in top:
        print(f"    {row['canonical_form']} ({row['entity_type']}): {row['segment_mention_count']} segments")


# ---------------------------------------------------------------------------
# PLAN 10: Rewrite Tier 3 summaries from extracted text
# ---------------------------------------------------------------------------
def plan_10_rewrite_tier3_summaries(db):
    print("\n" + "=" * 60)
    print("PLAN 10: Rewrite Tier 3 hedging summaries")
    print("=" * 60)

    # Find docs with hedging language that have extracted text
    hedging_docs = db.execute("""
        SELECT d.doc_id, d.title, d.category, d.card_summary, d.page_summary,
               dt.text_content
        FROM documents d
        LEFT JOIN document_texts dt ON d.doc_id = dt.doc_id
        WHERE (d.card_summary LIKE '%likely contains%'
            OR d.card_summary LIKE '%likely includes%'
            OR d.card_summary LIKE '%appears to be%'
            OR d.card_summary LIKE '%may represent%'
            OR d.card_summary LIKE '%may contain%'
            OR d.card_summary LIKE '%probably%'
            OR d.card_summary LIKE '%possibly%')
    """).fetchall()

    print(f"  Found {len(hedging_docs)} docs with hedging summaries")

    improved = 0
    no_text = 0
    for doc in hedging_docs:
        text = doc['text_content']
        if not text or len(text) < 50:
            no_text += 1
            continue

        # Generate a better summary from actual text
        # Take first ~500 chars as the basis, clean up
        text_clean = re.sub(r'\s+', ' ', text[:2000]).strip()

        # Extract first meaningful sentences (skip headers/metadata)
        sentences = re.split(r'[.!?]\s+', text_clean)
        meaningful = [s.strip() for s in sentences if len(s.strip()) > 30 and not s.strip().isupper()]

        if not meaningful:
            no_text += 1
            continue

        # Build card summary from first 2 meaningful sentences
        card = '. '.join(meaningful[:2])
        if len(card) > 200:
            card = card[:197] + '...'
        if not card.endswith('.'):
            card += '.'

        # Build page summary from first 5 meaningful sentences
        page = '. '.join(meaningful[:5])
        if len(page) > 600:
            page = page[:597] + '...'
        if not page.endswith('.'):
            page += '.'

        # Only update if we got something meaningfully different
        if len(card) > 50:
            db.execute("UPDATE documents SET card_summary = ?, page_summary = ? WHERE doc_id = ?",
                       (card, page, doc['doc_id']))
            improved += 1

    db.commit()
    print(f"  Improved: {improved} summaries")
    print(f"  No text available: {no_text} docs (need OCR)")


# ---------------------------------------------------------------------------
# PLAN 12: Extract people_mentioned from archive documents
# ---------------------------------------------------------------------------
def plan_12_extract_people_from_docs(db):
    print("\n" + "=" * 60)
    print("PLAN 12: Extract people_mentioned from archive documents")
    print("=" * 60)

    # Create document_topics table if not exists
    db.execute("""
        CREATE TABLE IF NOT EXISTS document_topics (
            doc_id TEXT NOT NULL,
            topic_type TEXT NOT NULL,
            topic_value TEXT NOT NULL,
            PRIMARY KEY (doc_id, topic_type, topic_value)
        )
    """)

    # Load existing names for matching
    name_set = set()
    for row in db.execute("SELECT canonical_form FROM names"):
        name_set.add(row['canonical_form'].lower())
    for row in db.execute("SELECT alias_text FROM name_aliases"):
        name_set.add(row['alias_text'].lower())

    # Person regex from discovery pipeline
    RE_PERSON = re.compile(r'\b([A-Z][a-z]{1,15})\s+([A-Z][a-z]{2,20})\b')

    NOT_PERSON = frozenset({
        'Science Fiction', 'San Francisco', 'Los Angeles', 'New York',
        'United States', 'Philip Dick', 'Philip Kindred',
        'Black Iron', 'Palm Tree', 'Holy Spirit', 'Holy Wisdom',
        'High Castle', 'Scanner Darkly', 'Three Stigmata',
    })

    docs = db.execute("""
        SELECT d.doc_id, dt.text_content
        FROM documents d
        JOIN document_texts dt ON d.doc_id = dt.doc_id
        WHERE dt.text_content IS NOT NULL AND length(dt.text_content) > 100
    """).fetchall()

    total_added = 0
    for doc in docs:
        text = doc['text_content'][:50000]  # Cap at 50k chars
        people = Counter()

        for m in RE_PERSON.finditer(text):
            full = m.group(0)
            if full in NOT_PERSON:
                continue
            # Check against known names
            if full.lower() in name_set:
                people[full] += 1

        # Insert top people (mentioned 2+ times)
        for person, count in people.most_common(20):
            if count >= 2:
                try:
                    db.execute("""
                        INSERT OR IGNORE INTO document_topics (doc_id, topic_type, topic_value)
                        VALUES (?, 'person', ?)
                    """, (doc['doc_id'], person))
                    total_added += 1
                except:
                    pass

    db.commit()
    print(f"  Added {total_added} person-document links")

    # Sample
    sample = db.execute("""
        SELECT topic_value, COUNT(*) as doc_count
        FROM document_topics WHERE topic_type = 'person'
        GROUP BY topic_value ORDER BY doc_count DESC LIMIT 10
    """).fetchall()
    print("  Top people across archive docs:")
    for row in sample:
        print(f"    {row['topic_value']}: {row['doc_count']} docs")


# ---------------------------------------------------------------------------
# PLAN 13: Extract works_discussed from archive documents
# ---------------------------------------------------------------------------
def plan_13_extract_works_from_docs(db):
    print("\n" + "=" * 60)
    print("PLAN 13: Extract works_discussed from archive documents")
    print("=" * 60)

    # PKD major works for matching
    PKD_WORKS = [
        'Solar Lottery', 'The World Jones Made', 'Eye in the Sky',
        'Time Out of Joint', 'Confessions of a Crap Artist',
        'The Man in the High Castle', 'The Man Who Japed',
        'The Game-Players of Titan', 'Martian Time-Slip',
        'The Simulacra', 'The Penultimate Truth', 'Clans of the Alphane Moon',
        'The Three Stigmata of Palmer Eldritch', 'Dr. Bloodmoney',
        'Now Wait for Last Year', 'The Crack in Space',
        'The Unteleported Man', 'Counter-Clock World',
        'The Zap Gun', 'The Ganymede Takeover',
        'Do Androids Dream of Electric Sheep', 'Ubik',
        'Galactic Pot-Healer', 'Our Friends from Frolix 8',
        'A Maze of Death', 'We Can Build You',
        'Flow My Tears, the Policeman Said', 'Flow My Tears',
        'Deus Irae', 'A Scanner Darkly', 'Scanner Darkly',
        'Radio Free Albemuth', 'VALIS', 'Valis',
        'The Divine Invasion', 'The Transmigration of Timothy Archer',
        'Timothy Archer', 'The Owl in Daylight',
        'Lies, Inc', 'The Exegesis',
        # Major stories
        'Second Variety', 'The Minority Report', 'Minority Report',
        'Adjustment Team', 'Paycheck', 'We Can Remember It for You Wholesale',
        'Total Recall', 'The Electric Ant', 'Faith of Our Fathers',
        'The Days of Perky Pat', 'Impostor', 'Beyond the Door',
        'Autofac', 'The Variable Man', 'Upon the Dull Earth',
        'Human Is', 'Colony', 'The Father-Thing',
    ]

    # Build regex patterns
    work_patterns = []
    for w in PKD_WORKS:
        escaped = re.escape(w)
        work_patterns.append((w, re.compile(r'\b' + escaped + r'\b', re.IGNORECASE)))

    docs = db.execute("""
        SELECT d.doc_id, dt.text_content
        FROM documents d
        JOIN document_texts dt ON d.doc_id = dt.doc_id
        WHERE dt.text_content IS NOT NULL AND length(dt.text_content) > 100
    """).fetchall()

    total_added = 0
    for doc in docs:
        text = doc['text_content'][:50000]
        works_found = Counter()

        for work_name, pattern in work_patterns:
            matches = pattern.findall(text)
            if matches:
                works_found[work_name] += len(matches)

        for work, count in works_found.most_common(15):
            if count >= 1:
                try:
                    db.execute("""
                        INSERT OR IGNORE INTO document_topics (doc_id, topic_type, topic_value)
                        VALUES (?, 'work', ?)
                    """, (doc['doc_id'], work))
                    total_added += 1
                except:
                    pass

    db.commit()
    print(f"  Added {total_added} work-document links")

    sample = db.execute("""
        SELECT topic_value, COUNT(*) as doc_count
        FROM document_topics WHERE topic_type = 'work'
        GROUP BY topic_value ORDER BY doc_count DESC LIMIT 15
    """).fetchall()
    print("  Top works across archive docs:")
    for row in sample:
        print(f"    {row['topic_value']}: {row['doc_count']} docs")


# ---------------------------------------------------------------------------
# PLAN 3: Upgrade provisional terms using corpus evidence
# ---------------------------------------------------------------------------
def plan_03_upgrade_provisional_terms(db):
    print("\n" + "=" * 60)
    print("PLAN 3: Upgrade provisional terms with corpus evidence")
    print("=" * 60)

    # Get provisional terms
    provisional = db.execute("""
        SELECT t.term_id, t.canonical_name, t.slug, t.mention_count,
            (SELECT COUNT(DISTINCT ts.seg_id) FROM term_segments ts WHERE ts.term_id = t.term_id) as seg_count
        FROM terms t
        WHERE t.status = 'provisional'
        ORDER BY seg_count DESC
    """).fetchall()

    print(f"  Provisional terms: {len(provisional)}")

    # Upgrade terms with 5+ segment links
    upgraded = 0
    for term in provisional:
        if term['seg_count'] >= 5:
            db.execute("""
                UPDATE terms SET status = 'accepted',
                    review_state = COALESCE(review_state, 'auto-upgraded')
                WHERE term_id = ?
            """, (term['term_id'],))
            upgraded += 1

    db.commit()
    print(f"  Upgraded to accepted: {upgraded} terms (had 5+ segment links)")

    # Show newly accepted
    if upgraded > 0:
        new_accepted = db.execute("""
            SELECT canonical_name,
                (SELECT COUNT(DISTINCT ts.seg_id) FROM term_segments ts WHERE ts.term_id = t.term_id) as seg_count
            FROM terms t
            WHERE t.status = 'accepted' AND t.review_state = 'auto-upgraded'
            ORDER BY seg_count DESC LIMIT 20
        """).fetchall()
        print("  Top newly accepted terms:")
        for row in new_accepted:
            print(f"    {row['canonical_name']}: {row['seg_count']} segments")


# ---------------------------------------------------------------------------
# PLAN 4: Add Exegesis context to term details
# ---------------------------------------------------------------------------
def plan_04_exegesis_context(db):
    print("\n" + "=" * 60)
    print("PLAN 4: Add Exegesis context sections to terms")
    print("=" * 60)

    # For each accepted term, find top 3 linked segments by confidence
    accepted = db.execute("""
        SELECT term_id, canonical_name FROM terms WHERE status = 'accepted'
    """).fetchall()

    added = 0
    for term in accepted:
        top_segs = db.execute("""
            SELECT s.seg_id, s.title, s.concise_summary, s.date_display,
                   ts.link_confidence, ts.match_type
            FROM term_segments ts
            JOIN segments s ON ts.seg_id = s.seg_id
            WHERE ts.term_id = ?
            ORDER BY ts.link_confidence ASC, s.date_start ASC
            LIMIT 5
        """, (term['term_id'],)).fetchall()

        if not top_segs:
            continue

        # Build context string
        context_parts = []
        for seg in top_segs:
            summary = seg['concise_summary'] or ''
            if summary and len(summary) > 10:
                date = seg['date_display'] or 'undated'
                context_parts.append(f"[{date}] {summary[:200]}")

        if context_parts:
            context = ' | '.join(context_parts[:3])
            # Store as annotation
            db.execute("""
                INSERT OR REPLACE INTO annotations
                (target_type, target_id, annotation_type, content, provenance)
                VALUES ('term', ?, 'note', ?, 'auto_plan04')
            """, (term['term_id'], 'EXEGESIS_CONTEXT: ' + context))
            added += 1

    db.commit()
    print(f"  Added Exegesis context for {added} terms")


# ---------------------------------------------------------------------------
# PLAN 5: Cross-link dictionary terms to archive documents
# ---------------------------------------------------------------------------
def plan_05_term_archive_links(db):
    print("\n" + "=" * 60)
    print("PLAN 5: Cross-link terms to archive documents")
    print("=" * 60)

    accepted = db.execute("""
        SELECT term_id, canonical_name FROM terms WHERE status = 'accepted'
    """).fetchall()

    # Also get aliases
    alias_map = defaultdict(set)
    for row in db.execute("SELECT term_id, alias_text FROM term_aliases"):
        alias_map[row['term_id']].add(row['alias_text'].lower())

    total_links = 0
    for term in accepted:
        tid = term['term_id']
        name = term['canonical_name']
        search_terms = {name.lower()} | alias_map.get(tid, set())

        # Search document texts
        for search in search_terms:
            if len(search) < 3:
                continue
            pattern = f'%{search}%'
            docs = db.execute("""
                SELECT d.doc_id, dt.text_content
                FROM documents d
                JOIN document_texts dt ON d.doc_id = dt.doc_id
                WHERE LOWER(dt.text_content) LIKE ?
                AND d.doc_type != 'exegesis_section'
            """, (pattern,)).fetchall()

            for doc in docs:
                # Count actual mentions (case-insensitive)
                text_lower = doc['text_content'].lower()
                count = text_lower.count(search)
                if count >= 3:
                    try:
                        db.execute("""
                            INSERT OR IGNORE INTO document_topics
                            (doc_id, topic_type, topic_value)
                            VALUES (?, 'term', ?)
                        """, (doc['doc_id'], name))
                        total_links += 1
                    except:
                        pass

    db.commit()
    print(f"  Added {total_links} term-document links")

    sample = db.execute("""
        SELECT topic_value, COUNT(*) as doc_count
        FROM document_topics WHERE topic_type = 'term'
        GROUP BY topic_value ORDER BY doc_count DESC LIMIT 10
    """).fetchall()
    print("  Top terms across archive docs:")
    for row in sample:
        print(f"    {row['topic_value']}: {row['doc_count']} docs")


# ---------------------------------------------------------------------------
# PLAN 6: Mine biographies for missing events 1928-1958
# ---------------------------------------------------------------------------
def plan_06_mine_early_events(db):
    print("\n" + "=" * 60)
    print("PLAN 6: Mine biographies for missing early events (1928-1958)")
    print("=" * 60)

    # Get biography document texts
    bio_docs = db.execute("""
        SELECT d.doc_id, d.title, dt.text_content
        FROM documents d
        JOIN document_texts dt ON d.doc_id = dt.doc_id
        WHERE d.category = 'biographies'
        AND dt.text_content IS NOT NULL AND length(dt.text_content) > 500
    """).fetchall()

    print(f"  Biography documents with text: {len(bio_docs)}")

    # Date patterns for early years
    RE_YEAR = re.compile(r'\b(19[2-5]\d)\b')
    RE_EVENT = re.compile(
        r'(?:in|In|during|During|by)\s+(19[2-5]\d)[,.]?\s+([A-Z][^.]{20,120}\.)',
        re.MULTILINE
    )
    RE_MONTH_EVENT = re.compile(
        r'(?:in|In)\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(19[2-5]\d)[,.]?\s+([A-Z][^.]{15,120}\.)',
        re.MULTILINE
    )

    # Get existing events in 1928-1958 range
    existing = set()
    for row in db.execute("""
        SELECT summary FROM biography_events
        WHERE date_start >= '1928' AND date_start < '1959'
    """):
        existing.add(row['summary'].lower()[:50])

    candidates = []
    for doc in bio_docs:
        text = doc['text_content']

        # Find year-anchored events
        for m in RE_EVENT.finditer(text):
            year = m.group(1)
            sentence = m.group(2).strip()
            if int(year) < 1928 or int(year) > 1958:
                continue
            # Check if PKD-related
            if not any(kw in sentence.lower() for kw in ['dick', 'philip', 'pkd', 'twin', 'jane', 'dorothy', 'edgar']):
                continue
            if sentence.lower()[:50] not in existing:
                candidates.append({
                    'year': year,
                    'sentence': sentence,
                    'source': doc['title'][:50],
                    'doc_id': doc['doc_id']
                })

        for m in RE_MONTH_EVENT.finditer(text):
            month = m.group(1)
            year = m.group(2)
            sentence = m.group(3).strip()
            if int(year) < 1928 or int(year) > 1958:
                continue
            if not any(kw in sentence.lower() for kw in ['dick', 'philip', 'pkd', 'twin', 'jane', 'dorothy', 'edgar']):
                continue
            if sentence.lower()[:50] not in existing:
                candidates.append({
                    'year': year,
                    'month': month,
                    'sentence': sentence,
                    'source': doc['title'][:50],
                    'doc_id': doc['doc_id']
                })

    # Deduplicate by similarity
    seen = set()
    unique = []
    for c in candidates:
        key = c['sentence'].lower()[:40]
        if key not in seen:
            seen.add(key)
            unique.append(c)

    print(f"  Found {len(unique)} candidate early events")

    # Insert as biography events
    month_map = {'January': '01', 'February': '02', 'March': '03', 'April': '04',
                 'May': '05', 'June': '06', 'July': '07', 'August': '08',
                 'September': '09', 'October': '10', 'November': '11', 'December': '12'}

    added = 0
    for c in unique[:50]:  # Cap at 50
        year = c['year']
        month = c.get('month')
        if month:
            date_start = f"{year}-{month_map[month]}"
            date_display = f"{month} {year}"
            precision = 'month'
        else:
            date_start = year
            date_display = year
            precision = 'year'

        # Clean up summary to PKD bio style
        summary = c['sentence']
        if len(summary) > 120:
            summary = summary[:117] + '...'

        bio_id = f"pkd_bio_{year}_mined_{added}"
        try:
            db.execute("""
                INSERT OR IGNORE INTO biography_events
                (bio_id, event_type, summary, date_start, date_display,
                 date_confidence, source_name, source_doc_id, reliability)
                VALUES (?, 'biographical', ?, ?, ?, ?, ?, ?, 'secondary')
            """, (bio_id, summary, date_start, date_display, precision,
                  c['source'], c['doc_id']))
            added += 1
        except Exception as e:
            pass

    db.commit()
    print(f"  Added {added} new early biography events")


# ---------------------------------------------------------------------------
# PLAN 7: Add source cross-references to existing events
# ---------------------------------------------------------------------------
def plan_07_cross_reference_sources(db):
    print("\n" + "=" * 60)
    print("PLAN 7: Cross-reference biography event sources")
    print("=" * 60)

    # Get all events with single sources
    events = db.execute("""
        SELECT bio_id, summary, date_start, source_name
        FROM biography_events
        WHERE source_name IS NOT NULL AND source_name NOT LIKE '%,%'
    """).fetchall()

    # Get biography texts for searching
    bio_texts = {}
    for row in db.execute("""
        SELECT d.doc_id, d.title, dt.text_content
        FROM documents d
        JOIN document_texts dt ON d.doc_id = dt.doc_id
        WHERE d.category = 'biographies'
        AND dt.text_content IS NOT NULL
    """):
        bio_texts[row['doc_id']] = {
            'title': row['title'],
            'text': row['text_content'].lower()
        }

    # Source name to doc matching
    source_to_docs = {}
    for doc_id, info in bio_texts.items():
        title = info['title'].lower()
        if 'sutin' in title:
            source_to_docs['Sutin'] = doc_id
        elif 'arnold' in title:
            source_to_docs['Arnold'] = doc_id
        elif 'anne' in title and 'dick' in title:
            source_to_docs['Anne Dick'] = doc_id
        elif 'peake' in title:
            source_to_docs['Peake'] = doc_id
        elif 'rickman' in title:
            source_to_docs['Rickman'] = doc_id

    print(f"  Matched biography sources: {list(source_to_docs.keys())}")
    print(f"  Events to cross-reference: {len(events)}")

    updated = 0
    for event in events:
        existing_source = event['source_name']
        summary_words = event['summary'].lower().split()
        # Take 3-4 distinctive words from summary for searching
        search_words = [w for w in summary_words if len(w) > 4 and w.isalpha()][:4]
        if not search_words:
            continue

        new_sources = [existing_source]
        for source_name, doc_id in source_to_docs.items():
            if source_name == existing_source:
                continue
            if doc_id not in bio_texts:
                continue
            text = bio_texts[doc_id]['text']
            # Check if most search words appear near each other
            matches = sum(1 for w in search_words if w in text)
            if matches >= 3:
                new_sources.append(source_name)

        if len(new_sources) > 1:
            combined = ', '.join(sorted(set(new_sources)))
            db.execute("UPDATE biography_events SET source_name = ? WHERE bio_id = ?",
                       (combined, event['bio_id']))
            updated += 1

    db.commit()
    print(f"  Updated {updated} events with additional sources")


# ---------------------------------------------------------------------------
# PLAN 8: Fill location gaps in biography events
# ---------------------------------------------------------------------------
def plan_08_fill_locations(db):
    print("\n" + "=" * 60)
    print("PLAN 8: Fill location gaps in biography events")
    print("=" * 60)

    # PKD's known residences by period
    RESIDENCE_PERIODS = [
        ('1928', '1928', 'Chicago, Illinois'),
        ('1929', '1938', 'Berkeley, California'),
        ('1938', '1940', 'Washington, D.C.'),
        ('1940', '1947', 'Berkeley, California'),
        ('1947', '1948', 'Berkeley, California'),
        ('1948', '1950', 'Berkeley, California'),
        ('1950', '1958', 'Berkeley, California'),
        ('1958', '1963', 'Point Reyes Station, California'),
        ('1963', '1964', 'Oakland, California'),
        ('1964', '1971', 'San Rafael, California'),
        ('1971', '1972', 'Vancouver, Canada'),
        ('1972', '1976', 'Fullerton, California'),
        ('1976', '1982', 'Santa Ana, California'),
    ]

    # Check if location column exists
    cols = [c[1] for c in db.execute('PRAGMA table_info(biography_events)').fetchall()]
    if 'location' not in cols:
        # Location isn't in the schema — store in notes or add column
        try:
            db.execute("ALTER TABLE biography_events ADD COLUMN location TEXT")
            print("  Added location column")
        except:
            print("  Could not add location column, storing in notes")
            return

    # Fill based on date periods
    filled = 0
    for start, end, location in RESIDENCE_PERIODS:
        cursor = db.execute("""
            UPDATE biography_events
            SET location = ?
            WHERE (location IS NULL OR location = '')
            AND date_start >= ? AND date_start <= ?
        """, (location, start, end + '-12-31'))
        filled += cursor.rowcount

    db.commit()
    print(f"  Filled {filled} events with location based on residence periods")


# ---------------------------------------------------------------------------
# PLAN 9: Discover drug/health events from biographies
# ---------------------------------------------------------------------------
def plan_09_drug_health_events(db):
    print("\n" + "=" * 60)
    print("PLAN 9: Discover drug/health events from biographies")
    print("=" * 60)

    bio_docs = db.execute("""
        SELECT d.doc_id, d.title, dt.text_content
        FROM documents d
        JOIN document_texts dt ON d.doc_id = dt.doc_id
        WHERE d.category = 'biographies'
        AND dt.text_content IS NOT NULL
    """).fetchall()

    HEALTH_KEYWORDS = re.compile(
        r'(amphetamine|barbiturate|hospitali[sz]|psychiatric|suicide|overdose|'
        r'breakdown|therapy|therapist|psychiatrist|medication|prescription|'
        r'drug[s]?\b|addiction|withdrawal|hallucination|panic\s+attack|'
        r'manic|depression|tachycardia|agoraphobia|vertigo)',
        re.IGNORECASE
    )

    RE_HEALTH_EVENT = re.compile(
        r'(?:in|In|during|During|by)\s+(19[4-8]\d)[,.]?\s+([A-Z][^.]{20,150}\.)',
        re.MULTILINE
    )

    existing = set()
    for row in db.execute("""
        SELECT summary FROM biography_events
        WHERE event_type IN ('health', 'drug_use')
    """):
        existing.add(row['summary'].lower()[:50])

    candidates = []
    for doc in bio_docs:
        text = doc['text_content']
        for m in RE_HEALTH_EVENT.finditer(text):
            year = m.group(1)
            sentence = m.group(2).strip()
            if not HEALTH_KEYWORDS.search(sentence):
                continue
            if not any(kw in sentence.lower() for kw in ['dick', 'philip', 'he ', 'his ']):
                continue
            if sentence.lower()[:50] not in existing:
                # Classify
                event_type = 'health'
                if any(kw in sentence.lower() for kw in ['amphetamine', 'drug', 'addiction', 'barbiturate']):
                    event_type = 'drug_use'
                candidates.append({
                    'year': year,
                    'sentence': sentence,
                    'event_type': event_type,
                    'source': doc['title'][:50],
                    'doc_id': doc['doc_id']
                })

    # Dedup
    seen = set()
    unique = []
    for c in candidates:
        key = c['sentence'].lower()[:40]
        if key not in seen:
            seen.add(key)
            unique.append(c)

    print(f"  Found {len(unique)} candidate health/drug events")

    added = 0
    for c in unique[:30]:
        summary = c['sentence'][:120]
        bio_id = f"pkd_bio_{c['year']}_health_{added}"
        try:
            db.execute("""
                INSERT OR IGNORE INTO biography_events
                (bio_id, event_type, summary, date_start, date_display,
                 date_confidence, source_name, source_doc_id, reliability)
                VALUES (?, ?, ?, ?, ?, 'year', ?, ?, 'secondary')
            """, (bio_id, c['event_type'], summary, c['year'], c['year'],
                  c['source'], c['doc_id']))
            added += 1
        except:
            pass

    db.commit()
    print(f"  Added {added} health/drug events")


# ---------------------------------------------------------------------------
# PLAN 14: Enrich scholar entries from their publications
# ---------------------------------------------------------------------------
def plan_14_enrich_scholars(db):
    print("\n" + "=" * 60)
    print("PLAN 14: Enrich scholar entries from their publications")
    print("=" * 60)

    # Find scholars who are also archive document authors
    scholars = db.execute("""
        SELECT n.name_id, n.canonical_form, n.entity_type
        FROM names n
        WHERE n.entity_type = 'scholar'
        OR n.canonical_form IN (
            SELECT DISTINCT source_name FROM biography_events WHERE source_name IS NOT NULL
        )
    """).fetchall()

    # Match scholars to their documents
    enriched = 0
    for scholar in scholars:
        name = scholar['canonical_form']
        name_parts = name.lower().split()
        if len(name_parts) < 2:
            continue
        surname = name_parts[-1]

        # Find docs by this author
        docs = db.execute("""
            SELECT d.doc_id, d.title, d.card_summary
            FROM documents d
            WHERE LOWER(d.title) LIKE ? OR LOWER(d.title) LIKE ?
        """, (f'%{surname}%', f'%{name.lower()}%')).fetchall()

        if docs:
            pub_titles = [d['title'][:60] for d in docs[:5]]
            pub_summary = '; '.join(pub_titles)

            # Store as annotation
            db.execute("""
                INSERT OR REPLACE INTO annotations
                (target_type, target_id, annotation_type, content, provenance)
                VALUES ('name', ?, 'note', ?, 'auto_plan14')
            """, (scholar['name_id'], 'PUBLICATIONS: ' + pub_summary))
            enriched += 1

    db.commit()
    print(f"  Enriched {enriched} scholars with publication data")


# ---------------------------------------------------------------------------
# PLAN 15: Triage top 50 discovered people into names table
# ---------------------------------------------------------------------------
def plan_15_triage_discovered_people(db):
    print("\n" + "=" * 60)
    print("PLAN 15: Triage discovered people into names table")
    print("=" * 60)

    discovery_file = SCRIPTS_DIR / 'discover' / 'output' / 'discovered_people.json'
    if not discovery_file.exists():
        print("  Discovery output not found, skipping")
        return

    with open(discovery_file, 'r', encoding='utf-8') as f:
        discovered = json.load(f)

    # Sort by frequency
    discovered.sort(key=lambda x: x.get('frequency', 0), reverse=True)

    # Get existing names
    existing_names = set()
    for row in db.execute("SELECT LOWER(canonical_form) FROM names"):
        existing_names.add(row[0])
    for row in db.execute("SELECT LOWER(alias_text) FROM name_aliases"):
        existing_names.add(row[0])

    added = 0
    for person in discovered[:100]:
        name = person['name']
        if name.lower() in existing_names:
            continue
        if person.get('frequency', 0) < 5:
            continue

        # Determine entity type
        entity_type = person.get('proposed_entity_type', 'historical_person')
        is_scholar = person.get('is_scholar', False)

        name_id = f"NAME_{make_term_id(name).replace('TERM_', '')}"
        slug = name.lower().replace(' ', '-').replace('.', '')

        try:
            db.execute("""
                INSERT OR IGNORE INTO names
                (name_id, canonical_form, slug, entity_type, provenance, notes)
                VALUES (?, ?, ?, ?, 'discovery_pipeline', ?)
            """, (name_id, name, slug,
                  'scholar' if is_scholar else entity_type,
                  f"Auto-discovered, frequency={person.get('frequency', 0)}"))
            existing_names.add(name.lower())
            added += 1
        except Exception as e:
            pass

        if added >= 50:
            break

    db.commit()
    print(f"  Added {added} new names from discovery pipeline")


# ---------------------------------------------------------------------------
# PLAN 17: Improve date confidence for approximate segments
# ---------------------------------------------------------------------------
def plan_17_improve_date_confidence(db):
    print("\n" + "=" * 60)
    print("PLAN 17: Improve date confidence for approximate segments")
    print("=" * 60)

    # Find segments with approximate/inferred dates that have raw text with date mentions
    approx = db.execute("""
        SELECT seg_id, title, date_start, date_confidence, raw_text
        FROM segments
        WHERE date_confidence IN ('approximate', 'inferred', 'folder_inferred')
        AND raw_text IS NOT NULL
    """).fetchall()

    print(f"  Segments with approximate dates: {len(approx)}")

    RE_DATE_INTERNAL = re.compile(
        r'(?:today is|this is|I (?:am )?writ(?:e|ing)|dated?)\s+'
        r'(?:(\d{1,2})\s+)?(January|February|March|April|May|June|July|'
        r'August|September|October|November|December)\s+(\d{4})',
        re.IGNORECASE
    )

    RE_YEAR_MENTION = re.compile(
        r'(?:this year|in|now|currently)\s+(19[67][0-9]|198[0-2])',
        re.IGNORECASE
    )

    upgraded = 0
    for seg in approx:
        text = seg['raw_text'][:3000]  # Check first 3k chars

        # Try to find explicit date
        m = RE_DATE_INTERNAL.search(text)
        if m:
            day = m.group(1)
            month = m.group(2)
            year = m.group(3)
            month_map = {'january': '01', 'february': '02', 'march': '03', 'april': '04',
                         'may': '05', 'june': '06', 'july': '07', 'august': '08',
                         'september': '09', 'october': '10', 'november': '11', 'december': '12'}
            month_num = month_map.get(month.lower(), '01')
            new_date = f"{year}-{month_num}"
            if day:
                new_date = f"{year}-{month_num}-{day.zfill(2)}"
                new_confidence = 'internal_reference'
            else:
                new_confidence = 'month'

            db.execute("""
                UPDATE segments SET date_confidence = ?, date_basis = 'internal_text_date'
                WHERE seg_id = ?
            """, (new_confidence, seg['seg_id']))
            upgraded += 1

    db.commit()
    print(f"  Upgraded date confidence for {upgraded} segments")


# ---------------------------------------------------------------------------
# PLAN 18: Add key_works_referenced to segments
# ---------------------------------------------------------------------------
def plan_18_segment_works(db):
    print("\n" + "=" * 60)
    print("PLAN 18: Add key_works_referenced to segments")
    print("=" * 60)

    # Major PKD work titles
    PKD_WORKS = {
        'VALIS': 'VALIS', 'Ubik': 'Ubik',
        'Scanner Darkly': 'A Scanner Darkly', 'A Scanner Darkly': 'A Scanner Darkly',
        'Three Stigmata': 'The Three Stigmata of Palmer Eldritch',
        'Palmer Eldritch': 'The Three Stigmata of Palmer Eldritch',
        'High Castle': 'The Man in the High Castle',
        'Man in the High Castle': 'The Man in the High Castle',
        'Flow My Tears': 'Flow My Tears, the Policeman Said',
        'Maze of Death': 'A Maze of Death',
        'Do Androids Dream': 'Do Androids Dream of Electric Sheep?',
        'Electric Sheep': 'Do Androids Dream of Electric Sheep?',
        'Androids Dream': 'Do Androids Dream of Electric Sheep?',
        'Divine Invasion': 'The Divine Invasion',
        'Timothy Archer': 'The Transmigration of Timothy Archer',
        'Transmigration': 'The Transmigration of Timothy Archer',
        'Martian Time-Slip': 'Martian Time-Slip',
        'Martian Time Slip': 'Martian Time-Slip',
        'Time Out of Joint': 'Time Out of Joint',
        'Penultimate Truth': 'The Penultimate Truth',
        'Eye in the Sky': 'Eye in the Sky',
        'Galactic Pot-Healer': 'Galactic Pot-Healer',
        'Radio Free Albemuth': 'Radio Free Albemuth',
        'Clans of the Alphane Moon': 'Clans of the Alphane Moon',
        'Dr. Bloodmoney': 'Dr. Bloodmoney',
        'Deus Irae': 'Deus Irae',
        'Simulacra': 'The Simulacra',
        'Minority Report': 'The Minority Report',
        'Second Variety': 'Second Variety',
        'Owl in Daylight': 'The Owl in Daylight',
    }

    # Compile patterns
    work_patterns = []
    for trigger, canonical in PKD_WORKS.items():
        pattern = re.compile(r'\b' + re.escape(trigger) + r'\b', re.IGNORECASE)
        work_patterns.append((pattern, canonical))

    # Add column if needed
    try:
        db.execute("ALTER TABLE segments ADD COLUMN works_referenced TEXT")
        print("  Added works_referenced column")
    except:
        pass

    segments = db.execute("SELECT seg_id, raw_text, concise_summary FROM segments WHERE raw_text IS NOT NULL").fetchall()

    updated = 0
    for seg in segments:
        text = (seg['raw_text'] or '') + ' ' + (seg['concise_summary'] or '')
        works_found = set()
        for pattern, canonical in work_patterns:
            if pattern.search(text):
                works_found.add(canonical)

        if works_found:
            works_json = json.dumps(sorted(works_found))
            db.execute("UPDATE segments SET works_referenced = ? WHERE seg_id = ?",
                       (works_json, seg['seg_id']))
            updated += 1

    db.commit()
    print(f"  Tagged {updated} segments with works_referenced")

    # Top works
    work_counts = Counter()
    for row in db.execute("SELECT works_referenced FROM segments WHERE works_referenced IS NOT NULL"):
        for w in json.loads(row['works_referenced']):
            work_counts[w] += 1

    print("  Most referenced works in Exegesis:")
    for work, count in work_counts.most_common(15):
        print(f"    {work}: {count} segments")


# ---------------------------------------------------------------------------
# PLAN 20: Generate analytics quality scores
# ---------------------------------------------------------------------------
def plan_20_quality_scores(db):
    print("\n" + "=" * 60)
    print("PLAN 20: Analytics quality scores per content area")
    print("=" * 60)

    scores = {}

    # Dictionary quality
    total_terms = db.execute("SELECT COUNT(*) as c FROM terms WHERE status = 'accepted'").fetchone()['c']
    terms_with_desc = db.execute("""
        SELECT COUNT(*) as c FROM terms
        WHERE status = 'accepted' AND full_description IS NOT NULL AND length(full_description) > 100
    """).fetchone()['c']
    terms_with_evidence = db.execute("""
        SELECT COUNT(DISTINCT t.term_id) as c FROM terms t
        JOIN evidence_packets ep ON ep.term_id = t.term_id
        WHERE t.status = 'accepted'
    """).fetchone()['c']
    terms_with_relations = db.execute("""
        SELECT COUNT(DISTINCT t.term_id) as c FROM terms t
        WHERE t.status = 'accepted'
        AND EXISTS (SELECT 1 FROM term_terms tt WHERE tt.term_id_a = t.term_id OR tt.term_id_b = t.term_id)
    """).fetchone()['c']

    scores['dictionary'] = {
        'total': total_terms,
        'with_description_100plus': terms_with_desc,
        'with_evidence': terms_with_evidence,
        'with_relations': terms_with_relations,
        'pct_described': round(terms_with_desc / max(total_terms, 1) * 100, 1),
        'pct_evidenced': round(terms_with_evidence / max(total_terms, 1) * 100, 1),
    }

    # Biography quality
    total_events = db.execute("SELECT COUNT(*) as c FROM biography_events").fetchone()['c']
    events_with_date = db.execute("SELECT COUNT(*) as c FROM biography_events WHERE date_start IS NOT NULL").fetchone()['c']
    try:
        events_with_location = db.execute("SELECT COUNT(*) as c FROM biography_events WHERE location IS NOT NULL AND location != ''").fetchone()['c']
    except:
        events_with_location = 0
    events_multi_source = db.execute("SELECT COUNT(*) as c FROM biography_events WHERE source_name LIKE '%,%'").fetchone()['c']

    scores['biography'] = {
        'total': total_events,
        'with_date': events_with_date,
        'with_location': events_with_location,
        'multi_source': events_multi_source,
        'pct_dated': round(events_with_date / max(total_events, 1) * 100, 1),
        'pct_located': round(events_with_location / max(total_events, 1) * 100, 1),
    }

    # Archive quality
    total_docs = db.execute("SELECT COUNT(*) as c FROM documents").fetchone()['c']
    docs_with_text = db.execute("SELECT COUNT(*) as c FROM document_texts WHERE text_content IS NOT NULL AND length(text_content) > 100").fetchone()['c']
    try:
        docs_with_lane = db.execute("SELECT COUNT(*) as c FROM documents WHERE evidentiary_lane IS NOT NULL").fetchone()['c']
    except:
        docs_with_lane = 0
    docs_with_topics = db.execute("SELECT COUNT(DISTINCT doc_id) as c FROM document_topics").fetchone()['c']

    scores['archive'] = {
        'total': total_docs,
        'with_extracted_text': docs_with_text,
        'with_evidentiary_lane': docs_with_lane,
        'with_topic_tags': docs_with_topics,
        'pct_text_extracted': round(docs_with_text / max(total_docs, 1) * 100, 1),
        'pct_lane_tagged': round(docs_with_lane / max(total_docs, 1) * 100, 1),
    }

    # Names quality
    total_names = db.execute("SELECT COUNT(*) as c FROM names").fetchone()['c']
    names_with_segs = db.execute("SELECT COUNT(DISTINCT name_id) as c FROM name_segments").fetchone()['c']
    names_with_refs = db.execute("SELECT COUNT(DISTINCT n.name_id) as c FROM names n WHERE n.reference_id IS NOT NULL").fetchone()['c']

    scores['names'] = {
        'total': total_names,
        'with_segment_links': names_with_segs,
        'with_references': names_with_refs,
        'pct_linked': round(names_with_segs / max(total_names, 1) * 100, 1),
    }

    # Segments quality
    total_segs = db.execute("SELECT COUNT(*) as c FROM segments").fetchone()['c']
    segs_with_text = db.execute("SELECT COUNT(*) as c FROM segments WHERE raw_text IS NOT NULL").fetchone()['c']
    segs_with_summary = db.execute("SELECT COUNT(*) as c FROM segments WHERE concise_summary IS NOT NULL").fetchone()['c']
    try:
        segs_with_works = db.execute("SELECT COUNT(*) as c FROM segments WHERE works_referenced IS NOT NULL").fetchone()['c']
    except:
        segs_with_works = 0

    scores['segments'] = {
        'total': total_segs,
        'with_raw_text': segs_with_text,
        'with_summary': segs_with_summary,
        'with_works_tagged': segs_with_works,
        'pct_summarized': round(segs_with_summary / max(total_segs, 1) * 100, 1),
    }

    print("  Quality scores:")
    for area, data in scores.items():
        print(f"\n  {area.upper()}:")
        for k, v in data.items():
            print(f"    {k}: {v}")

    return scores


# ---------------------------------------------------------------------------
# PLAN 19: Build connections export
# ---------------------------------------------------------------------------
def plan_19_connections_export(db):
    print("\n" + "=" * 60)
    print("PLAN 19: Build connections export")
    print("=" * 60)

    connections = {
        'term_to_segments': {},
        'term_to_terms': {},
        'term_to_docs': {},
        'name_to_segments': {},
        'name_to_terms': {},
    }

    # Term -> segments (top 5 per term)
    for row in db.execute("""
        SELECT ts.term_id, ts.seg_id, ts.link_confidence
        FROM term_segments ts
        JOIN terms t ON ts.term_id = t.term_id
        WHERE t.status = 'accepted'
        ORDER BY ts.term_id, ts.link_confidence ASC
    """):
        tid = row['term_id']
        if tid not in connections['term_to_segments']:
            connections['term_to_segments'][tid] = []
        if len(connections['term_to_segments'][tid]) < 10:
            connections['term_to_segments'][tid].append({
                'seg_id': row['seg_id'],
                'confidence': row['link_confidence']
            })

    # Term -> terms
    for row in db.execute("""
        SELECT term_id_a, term_id_b, relation_type, link_confidence
        FROM term_terms
        WHERE link_confidence >= 2
    """):
        a = row['term_id_a']
        if a not in connections['term_to_terms']:
            connections['term_to_terms'][a] = []
        connections['term_to_terms'][a].append({
            'term_id': row['term_id_b'],
            'relation': row['relation_type'],
            'confidence': row['link_confidence']
        })

    # Term -> docs (from document_topics)
    try:
        for row in db.execute("""
            SELECT dt.topic_value, dt.doc_id
            FROM document_topics dt WHERE dt.topic_type = 'term'
        """):
            val = row['topic_value']
            if val not in connections['term_to_docs']:
                connections['term_to_docs'][val] = []
            connections['term_to_docs'][val].append(row['doc_id'])
    except:
        pass

    # Name -> segments
    for row in db.execute("""
        SELECT ns.name_id, ns.seg_id
        FROM name_segments ns
    """):
        nid = row['name_id']
        if nid not in connections['name_to_segments']:
            connections['name_to_segments'][nid] = []
        if len(connections['name_to_segments'][nid]) < 10:
            connections['name_to_segments'][nid].append(row['seg_id'])

    # Summary
    print(f"  term->segment connections: {sum(len(v) for v in connections['term_to_segments'].values())}")
    print(f"  term->term connections: {sum(len(v) for v in connections['term_to_terms'].values())}")
    print(f"  term->doc connections: {sum(len(v) for v in connections['term_to_docs'].values())}")
    print(f"  name->segment connections: {sum(len(v) for v in connections['name_to_segments'].values())}")

    # Write connections file
    out_path = SITE_DATA / 'connections.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(connections, f, indent=1)
    print(f"  Written to {out_path} ({out_path.stat().st_size // 1024}KB)")


# ===========================================================================
# MAIN
# ===========================================================================
def main():
    import argparse
    parser = argparse.ArgumentParser(description='Execute all 20 improvement plans')
    parser.add_argument('--db', type=Path, default=DEFAULT_DB)
    args = parser.parse_args()

    db = get_db(args.db)

    print("=" * 60)
    print("QUERYPAT: EXECUTING ALL IMPROVEMENT PLANS")
    print("=" * 60)

    # Phase 1: Pure SQL / deterministic (no text search needed)
    plan_02_fill_related_terms(db)
    plan_11_evidentiary_lanes(db)
    plan_16_name_segment_counts(db)

    # Phase 2: Text search against corpus
    plan_10_rewrite_tier3_summaries(db)
    plan_12_extract_people_from_docs(db)
    plan_13_extract_works_from_docs(db)

    # Phase 3: Term improvements
    plan_03_upgrade_provisional_terms(db)
    plan_04_exegesis_context(db)
    plan_05_term_archive_links(db)

    # Phase 4: Biography improvements
    plan_06_mine_early_events(db)
    plan_07_cross_reference_sources(db)
    plan_08_fill_locations(db)
    plan_09_drug_health_events(db)

    # Phase 5: Names/scholars
    plan_14_enrich_scholars(db)
    plan_15_triage_discovered_people(db)

    # Phase 6: Segments
    plan_17_improve_date_confidence(db)
    plan_18_segment_works(db)

    # Phase 7: Analytics and exports
    quality_scores = plan_20_quality_scores(db)

    # Phase 8: Connections export
    plan_19_connections_export(db)

    db.close()

    print("\n" + "=" * 60)
    print("ALL PLANS COMPLETE")
    print("=" * 60)
    print("\nNext step: run export to regenerate JSON files:")
    print("  python scripts/build_all.py --export-only")


if __name__ == '__main__':
    main()
