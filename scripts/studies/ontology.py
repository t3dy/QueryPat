#!/usr/bin/env python3
"""
Stage 5a: Seed study ontologies into the database.

Creates rows in `studies` and `study_topics` for both the AI and Psychology studies.
Topic definitions and priority levels are hardcoded here as the canonical source.

Usage:
    python scripts/studies/ontology.py
    python scripts/studies/ontology.py --db database/unified.sqlite
"""

import json
import sqlite3
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

from date_norms import make_slug

PROJECT_DIR = SCRIPTS_DIR.parent
DEFAULT_DB = PROJECT_DIR / 'database' / 'unified.sqlite'

# ── Study definitions ─────────────────────────────────────────

STUDIES = [
    {
        'study_id': 'ai',
        'study_label': 'AI Topics',
        'study_description': (
            'Representations of artificial intelligence, androids, simulation, '
            'and machine consciousness across Philip K. Dick\'s fiction, Exegesis, '
            'and critical scholarship.'
        ),
    },
    {
        'study_id': 'psychology',
        'study_label': 'Psychology Topics',
        'study_description': (
            'Representations of psychological experience — paranoia, psychosis, '
            'identity, memory, and altered states — as depicted in PKD\'s fiction, '
            'theorized in the Exegesis, and reconstructed by biographers and critics.'
        ),
    },
]

# ── AI Topics ─────────────────────────────────────────────────
# (canonical_name, priority)  priority 10 = first-wave seed topic

AI_TOPICS = [
    ('AI', 5),
    ('Robots', 5),
    ('Androids', 10),
    ('Artificial Persons', 5),
    ('Simulation', 10),
    ('Machine Intelligence', 10),
    ('Control Systems', 5),
    ('Automation', 5),
    ('Cybernetics', 10),
    ('Surveillance', 5),
    ('Bureaucratic Control', 5),
    ('Programming', 5),
    ('Counterfeit Humanity', 10),
    ('Empathy Testing', 10),
    ('Implanted Memory', 10),
    ('Fabricated Identity', 5),
    ('Posthuman Cognition', 5),
    ('Simulation of Mind', 5),
    ('Labor Automation', 5),
    ('Technological Domination', 5),
    ('Reality Testing', 5),
    ('False Reality', 5),
    ('Android Affect', 10),
]

# ── Psychology Topics ─────────────────────────────────────────

PSYCHOLOGY_TOPICS = [
    ('Paranoia', 10),
    ('Schizophrenia', 10),
    ('Psychosis', 5),
    ('Empathy', 10),
    ('Trauma', 5),
    ('Addiction', 10),
    ('Amphetamine Use', 5),
    ('Identity Diffusion', 10),
    ('Double / Doppelgänger', 10),
    ('Dream Interpretation', 10),
    ('Jung', 10),
    ('Synchronicity', 5),
    ('Archetype', 5),
    ('Split-Brain', 5),
    ('Memory', 5),
    ('False Memory', 10),
    ('Therapy / Psychiatry', 5),
    ('Anamnesis', 10),
    ('Hypnagogic State', 10),
    ('Hypnopompic State', 5),
    ('Dream Rituals of Asclepius', 5),
    ('Twin Motif', 5),
    ('Gaslighting / Brainwashing', 5),
]


def make_topic_id(study_id: str, name: str) -> str:
    prefix = 'TOPIC_AI' if study_id == 'ai' else 'TOPIC_PSY'
    slug = make_slug(name)
    return f"{prefix}_{slug.replace('-', '_')}"


def run(db: sqlite3.Connection, _source: Path = None):
    """Seed studies and study_topics tables."""
    print("  Seeding study ontologies...")

    # Seed studies
    for s in STUDIES:
        db.execute("""
            INSERT OR IGNORE INTO studies (study_id, study_label, study_description)
            VALUES (?, ?, ?)
        """, (s['study_id'], s['study_label'], s['study_description']))

    # Seed AI topics
    ai_count = 0
    for name, priority in AI_TOPICS:
        topic_id = make_topic_id('ai', name)
        slug = make_slug(name)
        db.execute("""
            INSERT OR IGNORE INTO study_topics
                (topic_id, study_id, canonical_name, slug, priority, status)
            VALUES (?, 'ai', ?, ?, ?, 'seed')
        """, (topic_id, name, slug, priority))
        ai_count += 1

    # Seed Psychology topics
    psy_count = 0
    for name, priority in PSYCHOLOGY_TOPICS:
        topic_id = make_topic_id('psychology', name)
        slug = make_slug(name)
        db.execute("""
            INSERT OR IGNORE INTO study_topics
                (topic_id, study_id, canonical_name, slug, priority, status)
            VALUES (?, 'psychology', ?, ?, ?, 'seed')
        """, (topic_id, name, slug, priority))
        psy_count += 1

    # Update topic counts
    db.execute("UPDATE studies SET topic_count = ? WHERE study_id = 'ai'", (ai_count,))
    db.execute("UPDATE studies SET topic_count = ? WHERE study_id = 'psychology'", (psy_count,))

    db.commit()
    print(f"    AI study: {ai_count} topics seeded")
    print(f"    Psychology study: {psy_count} topics seeded")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Seed study ontologies')
    parser.add_argument('--db', type=Path, default=DEFAULT_DB)
    args = parser.parse_args()

    db = sqlite3.connect(str(args.db))
    db.execute("PRAGMA foreign_keys = ON")
    run(db)
    db.close()
    print("Done.")
