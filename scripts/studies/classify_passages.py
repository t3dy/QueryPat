#!/usr/bin/env python3
"""
Stage 5d: Claude-assisted passage classification.

Classifies each unclassified study passage with source_mode, claim_type,
confidence, and mode-specific fields (psych_mode / ai_mode).

Processes in batches of 10 passages per Claude call with checkpointing.

Usage:
    python scripts/studies/classify_passages.py
    python scripts/studies/classify_passages.py --db database/unified.sqlite
"""

import json
import sqlite3
import sys
import time
from pathlib import Path

from anthropic import Anthropic

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

PROJECT_DIR = SCRIPTS_DIR.parent
DEFAULT_DB = PROJECT_DIR / 'database' / 'unified.sqlite'

MODEL = 'claude-sonnet-4-20250514'
BATCH_SIZE = 10

CLASSIFICATION_PROMPT = """\
You are classifying passages from a scholarly archive about Philip K. Dick.
Each passage was extracted from a corpus document and matched to a study topic.

For each passage, determine:

1. source_mode — the genre of the source document:
   fiction | exegesis | letter | interview | criticism

2. claim_type — what kind of claim the passage makes:
   definition | symptom_description | causal_theory | allegory | self_report | critique | comparison | unresolved

3. confidence — how confident you are in this classification:
   high | medium | low

4. psych_mode — (ONLY for psychology study topics) the psychological framework:
   clinical | psychoanalytic | Jungian | existential | neuropsychological | anti-psychiatric | mystical | popular_psychology
   Set to null if not a psychology topic.

5. ai_mode — (ONLY for AI study topics) the AI discourse mode:
   engineering | philosophical | literary | sociological | theological
   Set to null if not an AI topic.

Return a JSON array with one object per passage, keyed by passage_id:
[
  {
    "passage_id": 123,
    "source_mode": "fiction",
    "claim_type": "allegory",
    "confidence": "high",
    "psych_mode": null,
    "ai_mode": "literary"
  },
  ...
]

Return ONLY the JSON array, no other text.
"""


def build_batch_prompt(passages, topic_meta):
    """Build the user prompt for a batch of passages."""
    lines = [CLASSIFICATION_PROMPT, "\n--- PASSAGES ---\n"]
    for p in passages:
        meta = topic_meta.get(p[1], {})
        lines.append(f"passage_id: {p[0]}")
        lines.append(f"topic: {meta.get('canonical_name', 'unknown')} (study: {meta.get('study_id', 'unknown')})")
        lines.append(f"lane: {p[2] or 'unknown'}")
        lines.append(f"text: {p[3][:1500]}")
        lines.append("")
    return "\n".join(lines)


def classify_batch(client, passages, topic_meta):
    """Send a batch to Claude and parse the classification response."""
    prompt = build_batch_prompt(passages, topic_meta)
    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.content[0].text.strip()
        # Strip markdown fences if present
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            text = text.rsplit("```", 1)[0]
        return json.loads(text)
    except Exception as e:
        print(f"    ERROR in Claude API call: {e}")
        return []


def run(db: sqlite3.Connection, source: Path = None):
    """Classify unclassified passages using Claude."""
    print("  Classifying passages with Claude...")

    # Load topic metadata for context
    topics = db.execute("""
        SELECT topic_id, study_id, canonical_name FROM study_topics
    """).fetchall()
    topic_meta = {t[0]: {'study_id': t[1], 'canonical_name': t[2]} for t in topics}

    # Query unclassified passages (checkpointing: skip already-classified)
    rows = db.execute("""
        SELECT passage_id, topic_id, lane, passage_text
        FROM study_passages
        WHERE source_mode IS NULL
        ORDER BY topic_id, passage_id
    """).fetchall()

    if not rows:
        print("    No unclassified passages found")
        return

    print(f"    {len(rows)} unclassified passages to process")

    client = Anthropic()
    total_classified = 0

    for i in range(0, len(rows), BATCH_SIZE):
        batch = rows[i:i + BATCH_SIZE]
        print(f"    Batch {i // BATCH_SIZE + 1}: passages {batch[0][0]}..{batch[-1][0]}")

        results = classify_batch(client, batch, topic_meta)

        for r in results:
            pid = r.get('passage_id')
            if pid is None:
                continue
            db.execute("""
                UPDATE study_passages SET
                    source_mode = ?,
                    claim_type = ?,
                    confidence = ?,
                    psych_mode = ?,
                    ai_mode = ?
                WHERE passage_id = ?
            """, (
                r.get('source_mode'),
                r.get('claim_type'),
                r.get('confidence'),
                r.get('psych_mode'),
                r.get('ai_mode'),
                pid,
            ))
            total_classified += 1

        db.commit()
        time.sleep(1)

    print(f"    Classified {total_classified} passages")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Classify study passages with Claude')
    parser.add_argument('--db', type=Path, default=DEFAULT_DB)
    args = parser.parse_args()

    start = time.time()
    db = sqlite3.connect(str(args.db))
    db.execute("PRAGMA foreign_keys = ON")
    run(db)
    db.close()
    elapsed = time.time() - start
    print(f"Done in {elapsed:.1f}s")
