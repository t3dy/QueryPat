#!/usr/bin/env python3
"""
Stage 5c: Cross-link study topics to existing terms, names, and documents.

Populates:
  study_topic_terms   — topics ↔ dictionary terms
  study_topic_names   — topics ↔ named entities
  study_topic_docs    — topics ↔ archive documents (with passage counts)

Usage:
    python scripts/studies/link_studies.py
"""

import json
import sqlite3
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

PROJECT_DIR = SCRIPTS_DIR.parent
DEFAULT_DB = PROJECT_DIR / 'database' / 'unified.sqlite'


def link_topics_to_terms(db: sqlite3.Connection):
    """Match study topics to dictionary terms by name similarity."""
    topics = db.execute("""
        SELECT topic_id, canonical_name, slug FROM study_topics
    """).fetchall()

    terms = db.execute("""
        SELECT term_id, canonical_name, slug FROM terms
    """).fetchall()

    # Build term lookup (lowercase name → term_id)
    term_by_name = {}
    term_by_slug = {}
    for tid, name, slug in terms:
        term_by_name[name.lower()] = tid
        term_by_slug[slug] = tid
        # Also index without common suffixes
        for word in name.lower().split():
            if word not in term_by_name:
                term_by_name[word] = tid

    linked = 0
    for topic_id, topic_name, topic_slug in topics:
        # Try exact match first
        matched_term = None
        relation = 'primary'

        # Exact name match
        if topic_name.lower() in term_by_name:
            matched_term = term_by_name[topic_name.lower()]
        # Slug match
        elif topic_slug in term_by_slug:
            matched_term = term_by_slug[topic_slug]
        else:
            # Try individual words from topic name
            for word in topic_name.lower().replace('/', ' ').replace('-', ' ').split():
                if len(word) > 3 and word in term_by_name:
                    matched_term = term_by_name[word]
                    relation = 'related'
                    break

        if matched_term:
            db.execute("""
                INSERT OR IGNORE INTO study_topic_terms (topic_id, term_id, relation_type)
                VALUES (?, ?, ?)
            """, (topic_id, matched_term, relation))
            linked += 1

    db.commit()
    print(f"    Linked {linked} topics to dictionary terms")


def link_topics_to_names(db: sqlite3.Connection):
    """Match study topics to named entities."""
    topics = db.execute("""
        SELECT topic_id, canonical_name FROM study_topics
    """).fetchall()

    names = db.execute("""
        SELECT name_id, canonical_form FROM names
    """).fetchall()

    name_lookup = {n[1].lower(): n[0] for n in names}

    linked = 0
    for topic_id, topic_name in topics:
        # Check if topic name matches a named entity (e.g., "Jung")
        if topic_name.lower() in name_lookup:
            db.execute("""
                INSERT OR IGNORE INTO study_topic_names (topic_id, name_id, relation_type)
                VALUES (?, ?, 'primary')
            """, (topic_id, name_lookup[topic_name.lower()]))
            linked += 1

        # Check related_thinkers field
        row = db.execute("""
            SELECT related_thinkers FROM study_topics WHERE topic_id = ?
        """, (topic_id,)).fetchone()
        if row and row[0]:
            try:
                thinkers = json.loads(row[0])
                for thinker in thinkers:
                    if thinker.lower() in name_lookup:
                        db.execute("""
                            INSERT OR IGNORE INTO study_topic_names
                                (topic_id, name_id, relation_type)
                            VALUES (?, ?, 'related')
                        """, (topic_id, name_lookup[thinker.lower()]))
                        linked += 1
            except (json.JSONDecodeError, TypeError):
                pass

    db.commit()
    print(f"    Linked {linked} topic-name associations")


def link_topics_to_docs(db: sqlite3.Connection):
    """Build topic ↔ document links from passage data."""
    # Aggregate passage counts per (topic, doc)
    rows = db.execute("""
        SELECT topic_id, doc_id, COUNT(*) as cnt
        FROM study_passages
        WHERE doc_id IS NOT NULL
        GROUP BY topic_id, doc_id
    """).fetchall()

    linked = 0
    for topic_id, doc_id, cnt in rows:
        # Determine relevance level
        if cnt >= 10:
            relevance = 'primary'
        elif cnt >= 3:
            relevance = 'substantial'
        else:
            relevance = 'mentions'

        db.execute("""
            INSERT OR REPLACE INTO study_topic_docs
                (topic_id, doc_id, relevance, passage_count)
            VALUES (?, ?, ?, ?)
        """, (topic_id, doc_id, relevance, cnt))
        linked += 1

    db.commit()
    print(f"    Linked {linked} topic-document associations")


def update_topic_metadata(db: sqlite3.Connection):
    """Update aggregate counts and cross-references on study_topics."""
    topics = db.execute("SELECT topic_id FROM study_topics").fetchall()

    for (topic_id,) in topics:
        # Passage count
        pc = db.execute("""
            SELECT COUNT(*) FROM study_passages WHERE topic_id = ?
        """, (topic_id,)).fetchone()[0]

        # Evidence count
        ec = db.execute("""
            SELECT COUNT(*) FROM study_evidence_packets WHERE topic_id = ?
        """, (topic_id,)).fetchone()[0]

        # Contradiction count
        cc = db.execute("""
            SELECT COUNT(*) FROM study_contradictions WHERE topic_id = ?
        """, (topic_id,)).fetchone()[0]

        # Related terms as JSON
        rt = db.execute("""
            SELECT t.slug FROM study_topic_terms stt
            JOIN terms t ON stt.term_id = t.term_id
            WHERE stt.topic_id = ?
        """, (topic_id,)).fetchall()
        related_terms_json = json.dumps([r[0] for r in rt]) if rt else None

        # Related names as JSON
        rn = db.execute("""
            SELECT n.canonical_form FROM study_topic_names stn
            JOIN names n ON stn.name_id = n.name_id
            WHERE stn.topic_id = ?
        """, (topic_id,)).fetchall()
        related_names_json = json.dumps([r[0] for r in rn]) if rn else None

        # Update status based on passage count
        status = db.execute("""
            SELECT status FROM study_topics WHERE topic_id = ?
        """, (topic_id,)).fetchone()[0]
        if pc > 0 and status == 'seed':
            status = 'scanning'

        db.execute("""
            UPDATE study_topics SET
                passage_count = ?,
                evidence_count = ?,
                contradiction_count = ?,
                related_terms = ?,
                related_names = ?,
                status = ?,
                updated_at = datetime('now')
            WHERE topic_id = ?
        """, (pc, ec, cc, related_terms_json, related_names_json, status, topic_id))

    db.commit()
    print(f"    Updated metadata for {len(topics)} topics")


def run(db: sqlite3.Connection, _source: Path = None):
    """Run all cross-linking steps."""
    print("  Cross-linking study topics...")

    # Clear existing links
    db.execute("DELETE FROM study_topic_terms")
    db.execute("DELETE FROM study_topic_names")
    db.execute("DELETE FROM study_topic_docs")
    db.commit()

    link_topics_to_terms(db)
    link_topics_to_names(db)
    link_topics_to_docs(db)
    update_topic_metadata(db)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Cross-link study topics')
    parser.add_argument('--db', type=Path, default=DEFAULT_DB)
    args = parser.parse_args()

    db = sqlite3.connect(str(args.db))
    db.execute("PRAGMA foreign_keys = ON")
    run(db)
    db.close()
    print("Done.")
