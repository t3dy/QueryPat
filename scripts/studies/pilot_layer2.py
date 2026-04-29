#!/usr/bin/env python3
"""
Layer 2 Pilot: Run Claude-assisted pipeline on 4 seed topics only.

Topics:
  TOPIC_AI_androids
  TOPIC_AI_empathy_testing
  TOPIC_PSY_paranoia
  TOPIC_PSY_anamnesis

Usage:
    python scripts/studies/pilot_layer2.py --step classify
    python scripts/studies/pilot_layer2.py --step evidence
    python scripts/studies/pilot_layer2.py --step contradictions
    python scripts/studies/pilot_layer2.py --step dossiers
    python scripts/studies/pilot_layer2.py --step fair_use
    python scripts/studies/pilot_layer2.py --step all
"""

import json
import sqlite3
import sys
import time
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

PROJECT_DIR = SCRIPTS_DIR.parent
DEFAULT_DB = PROJECT_DIR / 'database' / 'unified.sqlite'

PILOT_TOPICS = [
    'TOPIC_AI_androids',
    'TOPIC_AI_empathy_testing',
    'TOPIC_PSY_paranoia',
    'TOPIC_PSY_anamnesis',
]

from anthropic import Anthropic

# ── Reuse prompts from the pipeline scripts ───────────────────
from studies.classify_passages import CLASSIFICATION_PROMPT, MODEL, BATCH_SIZE as CLASS_BATCH
from studies.build_evidence_packets import EVIDENCE_PROMPT
from studies.detect_contradictions import CONTRADICTION_PROMPT
from studies.draft_dossiers import DOSSIER_PROMPT, gather_topic_context, MAX_PASSAGES
from studies.review_fair_use import FAIR_USE_PROMPT, MIN_LENGTH_FOR_REVIEW


def scope_where(topic_ids):
    """SQL IN clause for pilot topics."""
    placeholders = ','.join('?' * len(topic_ids))
    return f"topic_id IN ({placeholders})", list(topic_ids)


# ── Step 1: Classify ─────────────────────────────────────────

def run_classify(db, client):
    print("\n=== STEP 1: CLASSIFY PASSAGES ===")
    where, params = scope_where(PILOT_TOPICS)

    # Reset classifications for pilot topics so we can re-run
    db.execute(f"""
        UPDATE study_passages SET source_mode = NULL, claim_type = NULL,
            confidence = NULL, psych_mode = NULL, ai_mode = NULL
        WHERE {where}
    """, params)
    db.commit()

    rows = db.execute(f"""
        SELECT passage_id, topic_id, lane, passage_text
        FROM study_passages
        WHERE {where} AND source_mode IS NULL
        ORDER BY topic_id, passage_id
    """, params).fetchall()

    print(f"  {len(rows)} passages to classify")

    topics = db.execute("SELECT topic_id, study_id, canonical_name FROM study_topics").fetchall()
    topic_meta = {t[0]: {'study_id': t[1], 'canonical_name': t[2]} for t in topics}

    classified = 0
    batch_size = 10

    for i in range(0, len(rows), batch_size):
        batch = rows[i:i + batch_size]
        prompt_lines = [CLASSIFICATION_PROMPT, "\n--- PASSAGES ---\n"]
        for p in batch:
            meta = topic_meta.get(p[1], {})
            prompt_lines.append(f"passage_id: {p[0]}")
            prompt_lines.append(f"topic: {meta.get('canonical_name', '?')} (study: {meta.get('study_id', '?')})")
            prompt_lines.append(f"lane: {p[2] or '?'}")
            prompt_lines.append(f"text: {p[3][:1500]}")
            prompt_lines.append("")

        try:
            resp = client.messages.create(
                model=MODEL, max_tokens=4096,
                messages=[{"role": "user", "content": "\n".join(prompt_lines)}],
            )
            text = resp.content[0].text.strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[1].rsplit("```", 1)[0]
            results = json.loads(text)
        except Exception as e:
            print(f"  ERROR batch {i // batch_size + 1}: {e}")
            time.sleep(2)
            continue

        for r in results:
            pid = r.get('passage_id')
            if pid is None:
                continue
            db.execute("""
                UPDATE study_passages SET
                    source_mode = ?, claim_type = ?, confidence = ?,
                    psych_mode = ?, ai_mode = ?
                WHERE passage_id = ?
            """, (r.get('source_mode'), r.get('claim_type'), r.get('confidence'),
                  r.get('psych_mode'), r.get('ai_mode'), pid))
            classified += 1

        db.commit()
        print(f"  Batch {i // batch_size + 1}: classified {len(results)} passages")
        time.sleep(1)

    print(f"\n  Total classified: {classified}")

    # Report
    print("\n  --- Classification Summary ---")
    for tid in PILOT_TOPICS:
        name = topic_meta[tid]['canonical_name']
        total = db.execute("SELECT COUNT(*) FROM study_passages WHERE topic_id = ?", (tid,)).fetchone()[0]
        done = db.execute("SELECT COUNT(*) FROM study_passages WHERE topic_id = ? AND source_mode IS NOT NULL", (tid,)).fetchone()[0]
        print(f"  {name}: {done}/{total} classified")

    print("\n  --- By source_mode ---")
    for row in db.execute(f"""
        SELECT source_mode, COUNT(*) FROM study_passages
        WHERE {where} AND source_mode IS NOT NULL
        GROUP BY source_mode ORDER BY COUNT(*) DESC
    """, params).fetchall():
        print(f"    {row[0]}: {row[1]}")

    print("\n  --- By claim_type ---")
    for row in db.execute(f"""
        SELECT claim_type, COUNT(*) FROM study_passages
        WHERE {where} AND claim_type IS NOT NULL
        GROUP BY claim_type ORDER BY COUNT(*) DESC
    """, params).fetchall():
        print(f"    {row[0]}: {row[1]}")

    print("\n  --- By confidence ---")
    for row in db.execute(f"""
        SELECT confidence, COUNT(*) FROM study_passages
        WHERE {where} AND confidence IS NOT NULL
        GROUP BY confidence ORDER BY COUNT(*) DESC
    """, params).fetchall():
        print(f"    {row[0]}: {row[1]}")

    # 10 sample passages
    print("\n  --- 10 Sample Classified Passages ---")
    samples = db.execute(f"""
        SELECT sp.passage_id, st.canonical_name, sp.lane, sp.source_mode,
               sp.claim_type, sp.confidence, sp.psych_mode, sp.ai_mode,
               substr(sp.passage_text, 1, 150)
        FROM study_passages sp
        JOIN study_topics st ON sp.topic_id = st.topic_id
        WHERE sp.topic_id IN (?,?,?,?) AND sp.source_mode IS NOT NULL
        ORDER BY RANDOM() LIMIT 10
    """, PILOT_TOPICS).fetchall()

    for s in samples:
        print(f"  P{s[0]} | {s[1]} | Lane {s[2]} | mode={s[3]} | type={s[4]} | conf={s[5]} | psych={s[6]} | ai={s[7]}")
        print(f"    {s[8]}...")
        print()


# ── Step 2: Evidence Packets ─────────────────────────────────

def run_evidence(db, client):
    print("\n=== STEP 2: BUILD EVIDENCE PACKETS ===")

    # Clear existing packets for pilot topics
    for tid in PILOT_TOPICS:
        db.execute("DELETE FROM study_evidence_packets WHERE topic_id = ?", (tid,))
    db.commit()

    topics = db.execute("""
        SELECT st.topic_id, st.study_id, st.canonical_name, st.slug
        FROM study_topics st
        WHERE st.topic_id IN (?,?,?,?)
    """, PILOT_TOPICS).fetchall()

    total_packets = 0
    for topic_id, study_id, name, slug in topics:
        passages = db.execute("""
            SELECT passage_id, lane, source_mode, claim_type, passage_text
            FROM study_passages
            WHERE topic_id = ? AND source_mode IS NOT NULL
            ORDER BY lane, passage_id LIMIT 30
        """, (topic_id,)).fetchall()

        if not passages:
            print(f"  {name}: no classified passages, skipping")
            continue

        prompt = EVIDENCE_PROMPT.format(topic_name=name, study_id=study_id)
        lines = [prompt, "\n--- CLASSIFIED PASSAGES ---\n"]
        for p in passages:
            lines.append(f"passage_id: {p[0]}")
            lines.append(f"lane: {p[1]} | source_mode: {p[2]} | claim_type: {p[3]}")
            lines.append(f"text: {p[4][:1200]}")
            lines.append("")

        try:
            resp = client.messages.create(
                model=MODEL, max_tokens=4096,
                messages=[{"role": "user", "content": "\n".join(lines)}],
            )
            text = resp.content[0].text.strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[1].rsplit("```", 1)[0]
            results = json.loads(text)
        except Exception as e:
            print(f"  ERROR for {name}: {e}")
            time.sleep(2)
            continue

        for idx, r in enumerate(results, 1):
            ev_id = f"SEV_{study_id.upper()}_{slug.replace('-', '_')}_{idx:03d}"
            db.execute("""
                INSERT OR IGNORE INTO study_evidence_packets
                    (ev_id, topic_id, claim_text, evidence_summary, confidence,
                     source_method, lane_a_count, lane_b_count, lane_c_count)
                VALUES (?, ?, ?, ?, ?, 'llm', ?, ?, ?)
            """, (ev_id, topic_id, r.get('claim_text'), r.get('evidence_summary'),
                  r.get('confidence'), r.get('lane_a_count', 0),
                  r.get('lane_b_count', 0), r.get('lane_c_count', 0)))
            total_packets += 1

        db.execute("""
            UPDATE study_topics SET evidence_count = ?,
                status = 'evidence_built', updated_at = datetime('now')
            WHERE topic_id = ?
        """, (len(results), topic_id))
        db.commit()

        print(f"  {name}: {len(results)} evidence packets")
        for idx, r in enumerate(results[:2], 1):
            print(f"    [{idx}] {r.get('confidence', '?')}: {r.get('claim_text', '?')[:100]}")

        time.sleep(1)

    print(f"\n  Total packets: {total_packets}")


# ── Step 3: Contradictions ────────────────────────────────────

def run_contradictions(db, client):
    print("\n=== STEP 3: DETECT CONTRADICTIONS ===")

    for tid in PILOT_TOPICS:
        db.execute("DELETE FROM study_contradictions WHERE topic_id = ?", (tid,))
    db.commit()

    topics = db.execute("""
        SELECT st.topic_id, st.canonical_name
        FROM study_topics st WHERE st.topic_id IN (?,?,?,?)
    """, PILOT_TOPICS).fetchall()

    total_contradictions = 0
    for topic_id, name in topics:
        passages = db.execute("""
            SELECT passage_id, lane, source_mode, claim_type, passage_text
            FROM study_passages
            WHERE topic_id = ? AND source_mode IS NOT NULL
            ORDER BY lane, passage_id LIMIT 30
        """, (topic_id,)).fetchall()

        lanes = set(p[1] for p in passages if p[1])
        if len(lanes) < 2:
            print(f"  {name}: only {len(lanes)} lane(s), skipping")
            continue

        prompt = CONTRADICTION_PROMPT.format(topic_name=name)
        lines = [prompt, "\n--- PASSAGES ---\n"]
        for p in passages:
            lines.append(f"passage_id: {p[0]}")
            lines.append(f"lane: {p[1]} | source_mode: {p[2]} | claim_type: {p[3]}")
            lines.append(f"text: {p[4][:1200]}")
            lines.append("")

        try:
            resp = client.messages.create(
                model=MODEL, max_tokens=4096,
                messages=[{"role": "user", "content": "\n".join(lines)}],
            )
            text = resp.content[0].text.strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[1].rsplit("```", 1)[0]
            results = json.loads(text)
        except Exception as e:
            print(f"  ERROR for {name}: {e}")
            time.sleep(2)
            continue

        valid_ids = {p[0] for p in passages}
        inserted = 0
        for r in results:
            pid_a = r.get('passage_id_a')
            pid_b = r.get('passage_id_b')
            if pid_a not in valid_ids or pid_b not in valid_ids:
                continue
            db.execute("""
                INSERT INTO study_contradictions
                    (topic_id, passage_id_a, passage_id_b, summary, explanation, contradiction_type)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (topic_id, pid_a, pid_b, r.get('summary', ''),
                  r.get('explanation'), r.get('contradiction_type')))
            inserted += 1
            total_contradictions += 1

        cc = db.execute("SELECT COUNT(*) FROM study_contradictions WHERE topic_id = ?",
                        (topic_id,)).fetchone()[0]
        db.execute("UPDATE study_topics SET contradiction_count = ? WHERE topic_id = ?",
                    (cc, topic_id))
        db.commit()

        print(f"  {name}: {inserted} contradictions (from {len(passages)} passages, {len(lanes)} lanes)")
        for r in results[:2]:
            if r.get('passage_id_a') in valid_ids and r.get('passage_id_b') in valid_ids:
                print(f"    [{r.get('contradiction_type', '?')}] {r.get('summary', '?')[:120]}")

        time.sleep(1)

    print(f"\n  Total contradictions: {total_contradictions}")


# ── Step 4: Draft Dossiers ────────────────────────────────────

def run_dossiers(db, client):
    print("\n=== STEP 4: DRAFT DOSSIERS ===")

    topics = db.execute("""
        SELECT st.topic_id, st.study_id, st.canonical_name, s.study_label
        FROM study_topics st
        JOIN studies s ON st.study_id = s.study_id
        WHERE st.topic_id IN (?,?,?,?)
    """, PILOT_TOPICS).fetchall()

    total_drafted = 0
    for topic_id, study_id, name, study_label in topics:
        packets, passages, contradictions, related_terms, related_names = \
            gather_topic_context(db, topic_id)

        if not packets:
            print(f"  {name}: no evidence packets, skipping")
            continue

        # Build prompt
        prompt = DOSSIER_PROMPT.format(topic_name=name, study_label=study_label)
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

        try:
            resp = client.messages.create(
                model=MODEL, max_tokens=4096,
                messages=[{"role": "user", "content": "\n".join(lines)}],
            )
            text = resp.content[0].text.strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[1].rsplit("```", 1)[0]
            result = json.loads(text)
        except Exception as e:
            print(f"  ERROR for {name}: {e}")
            time.sleep(2)
            continue

        open_questions = result.get('open_questions')
        if isinstance(open_questions, list):
            open_questions = json.dumps(open_questions)

        db.execute("""
            UPDATE study_topics SET
                definition = ?, pkd_relevance = ?, in_the_fiction = ?,
                in_the_exegesis = ?, intellectual_background = ?,
                scholarly_debate = ?, chronology_summary = ?,
                contradictions_summary = ?, editorial_notes = ?,
                open_questions = ?, card_description = ?,
                status = 'drafted', updated_at = datetime('now')
            WHERE topic_id = ?
        """, (result.get('definition'), result.get('pkd_relevance'),
              result.get('in_the_fiction'), result.get('in_the_exegesis'),
              result.get('intellectual_background'), result.get('scholarly_debate'),
              result.get('chronology_summary'), result.get('contradictions_summary'),
              result.get('editorial_notes'), open_questions,
              result.get('card_description'), topic_id))
        db.commit()
        total_drafted += 1

        print(f"  {name}: drafted ({len(result)} sections)")
        for key in ['definition', 'pkd_relevance', 'card_description']:
            val = result.get(key, '')
            if val:
                print(f"    {key}: {val[:120]}...")

        time.sleep(1)

    print(f"\n  Total drafted: {total_drafted}")


# ── Step 5: Fair Use ──────────────────────────────────────────

def run_fair_use(db, client):
    print("\n=== STEP 5: FAIR-USE REVIEW ===")
    where, params = scope_where(PILOT_TOPICS)

    # Reset fair_use_status for pilot topics
    db.execute(f"UPDATE study_passages SET fair_use_status = 'pending' WHERE {where}", params)
    db.commit()

    # Auto-approve short passages
    auto = db.execute(f"""
        UPDATE study_passages SET fair_use_status = 'approved'
        WHERE {where} AND length(passage_text) <= {MIN_LENGTH_FOR_REVIEW}
        AND fair_use_status = 'pending'
    """, params).rowcount
    db.commit()
    print(f"  Auto-approved {auto} short passages")

    rows = db.execute(f"""
        SELECT passage_id, passage_text, lane, source_mode
        FROM study_passages
        WHERE {where} AND length(passage_text) > {MIN_LENGTH_FOR_REVIEW}
        AND fair_use_status = 'pending'
        ORDER BY passage_id
    """, params).fetchall()

    print(f"  {len(rows)} long passages to review")

    counts = {'approved': 0, 'trimmed': 0, 'rejected': 0}
    batch_size = 10

    for i in range(0, len(rows), batch_size):
        batch = rows[i:i + batch_size]
        prompt_lines = [FAIR_USE_PROMPT, "\n--- PASSAGES FOR REVIEW ---\n"]
        for p in batch:
            prompt_lines.append(f"passage_id: {p[0]}")
            prompt_lines.append(f"length: {len(p[1])} chars")
            prompt_lines.append(f"lane: {p[2]} | source_mode: {p[3]}")
            prompt_lines.append(f"text: {p[1]}")
            prompt_lines.append("")

        try:
            resp = client.messages.create(
                model=MODEL, max_tokens=4096,
                messages=[{"role": "user", "content": "\n".join(prompt_lines)}],
            )
            text = resp.content[0].text.strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[1].rsplit("```", 1)[0]
            results = json.loads(text)
        except Exception as e:
            print(f"  ERROR batch {i // batch_size + 1}: {e}")
            time.sleep(2)
            continue

        for r in results:
            pid = r.get('passage_id')
            status = r.get('status')
            if pid is None or status not in ('approved', 'trimmed', 'rejected'):
                continue
            if status == 'trimmed' and r.get('trimmed_text'):
                db.execute("""
                    UPDATE study_passages SET fair_use_status = 'trimmed',
                        passage_text = ?,
                        notes = COALESCE(notes || '; ', '') || 'Fair-use trimmed by Claude'
                    WHERE passage_id = ?
                """, (r['trimmed_text'], pid))
                print(f"    TRIMMED P{pid}: {len(r['trimmed_text'])} chars")
            else:
                db.execute("""
                    UPDATE study_passages SET fair_use_status = ? WHERE passage_id = ?
                """, (status, pid))
            counts[status] = counts.get(status, 0) + 1

        db.commit()
        time.sleep(1)

    print(f"\n  Results: {counts}")


# ── Main ──────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Layer 2 pilot on 4 topics')
    parser.add_argument('--step', required=True,
                        choices=['classify', 'evidence', 'contradictions',
                                 'dossiers', 'fair_use', 'all'])
    parser.add_argument('--db', type=Path, default=DEFAULT_DB)
    args = parser.parse_args()

    db = sqlite3.connect(str(args.db))
    db.execute("PRAGMA journal_mode = WAL")
    db.execute("PRAGMA foreign_keys = ON")

    client = Anthropic()
    start = time.time()

    if args.step in ('classify', 'all'):
        run_classify(db, client)
    if args.step in ('evidence', 'all'):
        run_evidence(db, client)
    if args.step in ('contradictions', 'all'):
        run_contradictions(db, client)
    if args.step in ('dossiers', 'all'):
        run_dossiers(db, client)
    if args.step in ('fair_use', 'all'):
        run_fair_use(db, client)

    db.close()
    elapsed = time.time() - start
    print(f"\nDone in {elapsed:.1f}s")


if __name__ == '__main__':
    main()
