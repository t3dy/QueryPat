#!/usr/bin/env python3
"""
Stage 5f: Detect contradictions between passages within each topic.

For each topic, sends representative passages from different evidentiary
lanes to Claude, which identifies contradictory pairs and classifies them.

Usage:
    python scripts/studies/detect_contradictions.py
    python scripts/studies/detect_contradictions.py --db database/unified.sqlite
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
MAX_PASSAGES_PER_TOPIC = 30

CONTRADICTION_PROMPT = """\
You are analyzing passages from a scholarly archive about Philip K. Dick
for the topic "{topic_name}".

The passages come from different evidentiary lanes:
  Lane A = fiction (novels, short stories)
  Lane B = exegesis (Dick's own theoretical writing)
  Lane C = scholarship (critics, biographers)

Identify pairs of passages that contradict each other. For each contradiction:

1. passage_id_a — the passage_id of the first passage
2. passage_id_b — the passage_id of the second passage
3. summary — a one-sentence description of the contradiction
4. explanation — a 2-3 sentence explanation of why these passages conflict
5. contradiction_type — one of:
   factual | interpretive | chronological | self_vs_critic | fiction_vs_exegesis | early_vs_late

Return a JSON array (may be empty if no contradictions found):
[
  {{
    "passage_id_a": 101,
    "passage_id_b": 205,
    "summary": "Dick's fiction portrays X while his exegesis claims Y",
    "explanation": "In the novel...",
    "contradiction_type": "fiction_vs_exegesis"
  }},
  ...
]

Return ONLY the JSON array, no other text.
"""


def build_prompt(topic_name, passages):
    """Build the prompt for contradiction detection."""
    prompt = CONTRADICTION_PROMPT.format(topic_name=topic_name)
    lines = [prompt, "\n--- PASSAGES ---\n"]
    for p in passages:
        lines.append(f"passage_id: {p[0]}")
        lines.append(f"lane: {p[1]} | source_mode: {p[2]} | claim_type: {p[3]}")
        lines.append(f"text: {p[4][:1200]}")
        lines.append("")
    return "\n".join(lines)


def detect_for_topic(client, topic_name, passages):
    """Send passages to Claude for contradiction detection."""
    prompt = build_prompt(topic_name, passages)
    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.content[0].text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            text = text.rsplit("```", 1)[0]
        return json.loads(text)
    except Exception as e:
        print(f"    ERROR in Claude API call: {e}")
        return []


def run(db: sqlite3.Connection, source: Path = None):
    """Detect contradictions for all topics with classified passages."""
    print("  Detecting contradictions with Claude...")

    # Get topics that have classified passages but no contradictions yet (checkpoint)
    topics = db.execute("""
        SELECT st.topic_id, st.canonical_name
        FROM study_topics st
        WHERE st.topic_id IN (
            SELECT DISTINCT topic_id FROM study_passages WHERE source_mode IS NOT NULL
        )
        AND st.topic_id NOT IN (
            SELECT DISTINCT topic_id FROM study_contradictions
        )
        ORDER BY st.priority DESC, st.topic_id
    """).fetchall()

    if not topics:
        print("    No topics need contradiction detection")
        return

    print(f"    {len(topics)} topics to process")

    client = Anthropic()
    total_contradictions = 0

    for topic_id, canonical_name in topics:
        # Get classified passages, sampling across lanes
        passages = db.execute("""
            SELECT passage_id, lane, source_mode, claim_type, passage_text
            FROM study_passages
            WHERE topic_id = ? AND source_mode IS NOT NULL
            ORDER BY lane, passage_id
            LIMIT ?
        """, (topic_id, MAX_PASSAGES_PER_TOPIC)).fetchall()

        if len(passages) < 2:
            continue

        # Check if passages come from multiple lanes (contradictions need diversity)
        lanes = set(p[1] for p in passages if p[1])
        if len(lanes) < 2:
            continue

        print(f"    Topic: {canonical_name} ({len(passages)} passages, {len(lanes)} lanes)")

        results = detect_for_topic(client, canonical_name, passages)

        # Validate passage_ids exist in this topic
        valid_ids = {p[0] for p in passages}

        for r in results:
            pid_a = r.get('passage_id_a')
            pid_b = r.get('passage_id_b')
            if pid_a not in valid_ids or pid_b not in valid_ids:
                continue

            db.execute("""
                INSERT INTO study_contradictions
                    (topic_id, passage_id_a, passage_id_b, summary,
                     explanation, contradiction_type)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                topic_id, pid_a, pid_b,
                r.get('summary', ''),
                r.get('explanation'),
                r.get('contradiction_type'),
            ))
            total_contradictions += 1

        # Update topic contradiction count
        cc = db.execute("""
            SELECT COUNT(*) FROM study_contradictions WHERE topic_id = ?
        """, (topic_id,)).fetchone()[0]
        db.execute("""
            UPDATE study_topics SET
                contradiction_count = ?,
                updated_at = datetime('now')
            WHERE topic_id = ?
        """, (cc, topic_id))

        db.commit()
        time.sleep(1)

    print(f"    Detected {total_contradictions} contradictions")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Detect contradictions with Claude')
    parser.add_argument('--db', type=Path, default=DEFAULT_DB)
    args = parser.parse_args()

    start = time.time()
    db = sqlite3.connect(str(args.db))
    db.execute("PRAGMA foreign_keys = ON")
    run(db)
    db.close()
    elapsed = time.time() - start
    print(f"Done in {elapsed:.1f}s")
