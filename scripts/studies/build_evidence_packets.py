#!/usr/bin/env python3
"""
Stage 5e: Build evidence packets from classified passages.

Groups classified passages into evidence packets — distinct claims with
supporting evidence — for each study topic. Claude identifies 3-8 claims
per topic and assigns evidence IDs.

Usage:
    python scripts/studies/build_evidence_packets.py
    python scripts/studies/build_evidence_packets.py --db database/unified.sqlite
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
BATCH_SIZE = 30  # passages per Claude call

EVIDENCE_PROMPT = """\
You are building evidence packets for a scholarly study of Philip K. Dick.

Given the classified passages below for the topic "{topic_name}" (study: {study_id}),
identify 3 to 8 distinct claims that emerge from the evidence.

For each claim, provide:
1. slug — a short lowercase slug (no spaces, use underscores) identifying the claim
2. claim_text — a one-sentence statement of the claim
3. evidence_summary — a 2-3 sentence summary of the supporting evidence
4. confidence — strong | moderate | weak | speculative
5. lane_a_count — how many fiction (Lane A) passages support this
6. lane_b_count — how many exegesis (Lane B) passages support this
7. lane_c_count — how many scholarship (Lane C) passages support this

Return a JSON array:
[
  {{
    "slug": "android_empathy_test",
    "claim_text": "Empathy testing serves as...",
    "evidence_summary": "Multiple passages from...",
    "confidence": "strong",
    "lane_a_count": 5,
    "lane_b_count": 2,
    "lane_c_count": 1
  }},
  ...
]

Return ONLY the JSON array, no other text.
"""


def build_batch_prompt(topic_name, study_id, passages):
    """Build the prompt for evidence extraction."""
    prompt = EVIDENCE_PROMPT.format(topic_name=topic_name, study_id=study_id)
    lines = [prompt, "\n--- CLASSIFIED PASSAGES ---\n"]
    for p in passages:
        lines.append(f"passage_id: {p[0]}")
        lines.append(f"lane: {p[1]} | source_mode: {p[2]} | claim_type: {p[3]}")
        lines.append(f"text: {p[4][:1200]}")
        lines.append("")
    return "\n".join(lines)


def extract_evidence(client, topic_name, study_id, passages):
    """Send passages to Claude and extract evidence packets."""
    prompt = build_batch_prompt(topic_name, study_id, passages)
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
    """Build evidence packets for all topics with classified passages."""
    print("  Building evidence packets with Claude...")

    # Get topics that have classified passages but no evidence packets yet (checkpoint)
    topics = db.execute("""
        SELECT st.topic_id, st.study_id, st.canonical_name, st.slug
        FROM study_topics st
        WHERE st.topic_id IN (
            SELECT DISTINCT topic_id FROM study_passages WHERE source_mode IS NOT NULL
        )
        AND st.topic_id NOT IN (
            SELECT DISTINCT topic_id FROM study_evidence_packets
        )
        ORDER BY st.priority DESC, st.topic_id
    """).fetchall()

    if not topics:
        print("    No topics need evidence packets")
        return

    print(f"    {len(topics)} topics to process")

    client = Anthropic()
    total_packets = 0

    for topic_id, study_id, canonical_name, slug in topics:
        # Get classified passages for this topic
        passages = db.execute("""
            SELECT passage_id, lane, source_mode, claim_type, passage_text
            FROM study_passages
            WHERE topic_id = ? AND source_mode IS NOT NULL
            ORDER BY lane, passage_id
        """, (topic_id,)).fetchall()

        if not passages:
            continue

        print(f"    Topic: {canonical_name} ({len(passages)} passages)")

        # Process in batches if many passages
        all_passages = passages[:BATCH_SIZE]  # Cap at BATCH_SIZE for single call
        results = extract_evidence(client, canonical_name, study_id, all_passages)

        for idx, r in enumerate(results, 1):
            claim_slug = r.get('slug', f'claim_{idx}')
            ev_id = f"SEV_{study_id.upper()}_{slug.replace('-', '_')}_{idx:03d}"

            db.execute("""
                INSERT OR IGNORE INTO study_evidence_packets
                    (ev_id, topic_id, claim_text, evidence_summary, confidence,
                     source_method, lane_a_count, lane_b_count, lane_c_count)
                VALUES (?, ?, ?, ?, ?, 'llm', ?, ?, ?)
            """, (
                ev_id, topic_id,
                r.get('claim_text'),
                r.get('evidence_summary'),
                r.get('confidence'),
                r.get('lane_a_count', 0),
                r.get('lane_b_count', 0),
                r.get('lane_c_count', 0),
            ))
            total_packets += 1

        # Update topic evidence count and status
        db.execute("""
            UPDATE study_topics SET
                evidence_count = ?,
                status = CASE WHEN status = 'scanning' THEN 'evidence_built' ELSE status END,
                updated_at = datetime('now')
            WHERE topic_id = ?
        """, (len(results), topic_id))

        db.commit()
        time.sleep(1)

    print(f"    Created {total_packets} evidence packets")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Build evidence packets with Claude')
    parser.add_argument('--db', type=Path, default=DEFAULT_DB)
    args = parser.parse_args()

    start = time.time()
    db = sqlite3.connect(str(args.db))
    db.execute("PRAGMA foreign_keys = ON")
    run(db)
    db.close()
    elapsed = time.time() - start
    print(f"Done in {elapsed:.1f}s")
