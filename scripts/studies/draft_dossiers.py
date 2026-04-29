#!/usr/bin/env python3
"""
Stage 5g: Draft dossier sections for each study topic.

For each topic with evidence packets, sends evidence summaries, top passages,
contradiction summaries, and related terms/names to Claude for dossier drafting.

Usage:
    python scripts/studies/draft_dossiers.py
    python scripts/studies/draft_dossiers.py --db database/unified.sqlite
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
MAX_PASSAGES = 20

DOSSIER_PROMPT = """\
You are drafting a scholarly dossier entry for the topic "{topic_name}"
in the {study_label} study of Philip K. Dick's work.

IMPORTANT GUIDELINES:
- Write at a college reading level with an analytical tone.
- Do NOT diagnose Philip K. Dick with any condition. Present depictions,
  themes, and self-reports without clinical judgment.
- Clearly separate evidentiary lanes:
  Lane A (fiction) — what appears in novels and stories
  Lane B (exegesis) — what Dick wrote in the Exegesis
  Lane C (scholarship) — what critics and biographers argue
- Be precise about attribution: "Dick depicts..." vs "Dick writes..." vs
  "Scholar X argues..."

Given the evidence below, draft ALL of the following sections as a JSON object:

1. definition — 1-2 sentences defining this topic in the PKD context
2. pkd_relevance — 2-3 sentences on why this topic matters in Dick's oeuvre
3. in_the_fiction — 2-4 sentences on how this appears in Dick's fiction (Lane A)
4. in_the_exegesis — 2-4 sentences on how this appears in the Exegesis (Lane B)
5. intellectual_background — 2-3 sentences on the intellectual/philosophical context
6. scholarly_debate — 2-3 sentences on what critics and scholars argue (Lane C)
7. chronology_summary — 1-2 sentences on how this topic evolves across Dick's career
8. contradictions_summary — 1-2 sentences on key tensions or contradictions
9. editorial_notes — 1-2 sentences of editorial guidance for researchers
10. open_questions — a JSON array of 2-4 open research questions (strings)
11. card_description — a single-sentence summary for use on a topic card

Return a JSON object with these exact keys. Return ONLY the JSON, no other text.
"""


def gather_topic_context(db, topic_id):
    """Gather all context needed for dossier drafting."""
    # Evidence packets
    packets = db.execute("""
        SELECT ev_id, claim_text, evidence_summary, confidence,
               lane_a_count, lane_b_count, lane_c_count
        FROM study_evidence_packets
        WHERE topic_id = ?
    """, (topic_id,)).fetchall()

    # Top passages (limited)
    passages = db.execute("""
        SELECT passage_id, lane, source_mode, claim_type, passage_text
        FROM study_passages
        WHERE topic_id = ? AND source_mode IS NOT NULL
        ORDER BY
            CASE confidence WHEN 'high' THEN 1 WHEN 'medium' THEN 2 ELSE 3 END,
            passage_id
        LIMIT ?
    """, (topic_id, MAX_PASSAGES)).fetchall()

    # Contradictions
    contradictions = db.execute("""
        SELECT summary, explanation, contradiction_type
        FROM study_contradictions
        WHERE topic_id = ?
    """, (topic_id,)).fetchall()

    # Related terms and names
    related_terms = db.execute("""
        SELECT t.canonical_name FROM study_topic_terms stt
        JOIN terms t ON stt.term_id = t.term_id
        WHERE stt.topic_id = ?
    """, (topic_id,)).fetchall()

    related_names = db.execute("""
        SELECT n.canonical_form FROM study_topic_names stn
        JOIN names n ON stn.name_id = n.name_id
        WHERE stn.topic_id = ?
    """, (topic_id,)).fetchall()

    return packets, passages, contradictions, related_terms, related_names


def build_prompt(topic_name, study_label, packets, passages, contradictions,
                 related_terms, related_names):
    """Build the full dossier drafting prompt."""
    prompt = DOSSIER_PROMPT.format(topic_name=topic_name, study_label=study_label)
    lines = [prompt]

    lines.append("\n--- EVIDENCE PACKETS ---\n")
    for p in packets:
        lines.append(f"[{p[0]}] (confidence: {p[3]})")
        lines.append(f"Claim: {p[1]}")
        lines.append(f"Evidence: {p[2]}")
        lines.append(f"Lanes: A={p[4]}, B={p[5]}, C={p[6]}")
        lines.append("")

    lines.append("\n--- TOP PASSAGES ---\n")
    for p in passages:
        lines.append(f"passage_id: {p[0]} | lane: {p[1]} | mode: {p[2]} | type: {p[3]}")
        lines.append(f"text: {p[4][:800]}")
        lines.append("")

    if contradictions:
        lines.append("\n--- CONTRADICTIONS ---\n")
        for c in contradictions:
            lines.append(f"[{c[2]}] {c[0]}")
            if c[1]:
                lines.append(f"  Explanation: {c[1][:300]}")
            lines.append("")

    if related_terms:
        lines.append(f"\nRelated dictionary terms: {', '.join(t[0] for t in related_terms)}")
    if related_names:
        lines.append(f"Related names: {', '.join(n[0] for n in related_names)}")

    return "\n".join(lines)


def draft_topic(client, topic_name, study_label, packets, passages,
                contradictions, related_terms, related_names):
    """Send context to Claude and get dossier draft."""
    prompt = build_prompt(topic_name, study_label, packets, passages,
                          contradictions, related_terms, related_names)
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
        return None


def run(db: sqlite3.Connection, source: Path = None):
    """Draft dossiers for topics with evidence packets."""
    print("  Drafting dossiers with Claude...")

    # Get topics with evidence packets that haven't been drafted yet (checkpoint)
    topics = db.execute("""
        SELECT st.topic_id, st.study_id, st.canonical_name, s.study_label
        FROM study_topics st
        JOIN studies s ON st.study_id = s.study_id
        WHERE st.topic_id IN (
            SELECT DISTINCT topic_id FROM study_evidence_packets
        )
        AND st.status NOT IN ('drafted', 'reviewed', 'published')
        ORDER BY st.priority DESC, st.topic_id
    """).fetchall()

    if not topics:
        print("    No topics need dossier drafting")
        return

    print(f"    {len(topics)} topics to draft")

    client = Anthropic()
    total_drafted = 0

    for topic_id, study_id, canonical_name, study_label in topics:
        print(f"    Drafting: {canonical_name}")

        packets, passages, contradictions, related_terms, related_names = \
            gather_topic_context(db, topic_id)

        if not packets:
            continue

        result = draft_topic(client, canonical_name, study_label,
                             packets, passages, contradictions,
                             related_terms, related_names)

        if not result:
            continue

        # Handle open_questions — store as JSON string
        open_questions = result.get('open_questions')
        if isinstance(open_questions, list):
            open_questions = json.dumps(open_questions)

        db.execute("""
            UPDATE study_topics SET
                definition = ?,
                pkd_relevance = ?,
                in_the_fiction = ?,
                in_the_exegesis = ?,
                intellectual_background = ?,
                scholarly_debate = ?,
                chronology_summary = ?,
                contradictions_summary = ?,
                editorial_notes = ?,
                open_questions = ?,
                card_description = ?,
                status = 'drafted',
                updated_at = datetime('now')
            WHERE topic_id = ?
        """, (
            result.get('definition'),
            result.get('pkd_relevance'),
            result.get('in_the_fiction'),
            result.get('in_the_exegesis'),
            result.get('intellectual_background'),
            result.get('scholarly_debate'),
            result.get('chronology_summary'),
            result.get('contradictions_summary'),
            result.get('editorial_notes'),
            open_questions,
            result.get('card_description'),
            topic_id,
        ))

        db.commit()
        total_drafted += 1
        time.sleep(1)

    print(f"    Drafted {total_drafted} topic dossiers")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Draft topic dossiers with Claude')
    parser.add_argument('--db', type=Path, default=DEFAULT_DB)
    args = parser.parse_args()

    start = time.time()
    db = sqlite3.connect(str(args.db))
    db.execute("PRAGMA foreign_keys = ON")
    run(db)
    db.close()
    elapsed = time.time() - start
    print(f"Done in {elapsed:.1f}s")
