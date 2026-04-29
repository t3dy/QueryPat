"""Seed the ai_interaction_types ontology table."""

import sqlite3
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_DB = PROJECT_DIR / 'database' / 'unified.sqlite'

INTERACTION_TYPES = [
    ('empathy_testing',         'Empathy Testing',          'Formal or informal test of whether an entity is human or artificial', 1),
    ('interrogation',           'Interrogation',            'Questioning an AI/android to extract information or assess nature', 2),
    ('deception',               'Deception',                'AI/android passing as human, or human deceiving an AI', 3),
    ('empathy_failure',         'Empathy Failure',          'Expected empathic response absent or unconvincingly simulated', 4),
    ('bureaucratic_enforcement','Bureaucratic Enforcement',  'AI/machine system enforcing rules or social order', 5),
    ('labor_replacement',       'Labor Replacement',        'Automation replacing human work, dramatized through character experience', 6),
    ('therapeutic_exchange',    'Therapeutic/Advisory',      'AI providing counsel, therapy, or guidance', 7),
    ('romantic_ambiguity',      'Romantic/Intimate Ambiguity','Romantic or sexual interaction with uncertain humanity', 8),
    ('identity_uncertainty',    'Identity Uncertainty',     'Character\'s human/artificial status genuinely unclear', 9),
    ('suspicion',               'Suspicion/Testing',        'Informal suspicion that someone may not be human', 10),
    ('surveillance',            'Surveillance/Monitoring',  'AI system observing, recording, or controlling humans', 11),
    ('memory_manipulation',     'Memory/Reality Manipulation','AI system altering memories, perceptions, or reality', 12),
    ('revolt',                  'Revolt/Resistance',        'AI entity resisting control, asserting autonomy, rebelling', 13),
    ('companionship',           'Companionship',            'Non-romantic bonding, alliance, or dependency', 14),
    ('creation',                'Creation/Awakening',       'AI entity created, activated, or becoming self-aware', 15),
    ('destruction',             'Destruction/Retirement',   'Killing, deactivating, or dismantling an AI entity', 16),
]


def run(db: sqlite3.Connection, _source: Path = None):
    """Seed ai_interaction_types table."""
    print("  Seeding interaction-type ontology...")

    for slug, label, desc, order in INTERACTION_TYPES:
        db.execute("""
            INSERT OR IGNORE INTO ai_interaction_types
                (type_slug, type_label, type_description, sort_order)
            VALUES (?, ?, ?, ?)
        """, (slug, label, desc, order))

    db.commit()
    print(f"    {len(INTERACTION_TYPES)} interaction types seeded")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Seed AI interaction types')
    parser.add_argument('--db', type=Path, default=DEFAULT_DB)
    args = parser.parse_args()

    db = sqlite3.connect(str(args.db))
    db.execute("PRAGMA foreign_keys = ON")

    # Ensure table exists
    schema_path = PROJECT_DIR / 'database' / 'scenes_schema.sql'
    if schema_path.exists():
        db.executescript(schema_path.read_text(encoding='utf-8'))

    run(db)
    db.close()
