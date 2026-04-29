#!/usr/bin/env python3
"""
Layer 2 Pilot: Build evidence packets deterministically.

Groups classified passages into evidence packets by claim_type clusters,
preserving lane separation. No API calls.
"""

import json
import sqlite3
from collections import defaultdict
from pathlib import Path

DB = Path(__file__).resolve().parent.parent.parent / 'database' / 'unified.sqlite'

PILOT_TOPICS = [
    'TOPIC_AI_androids',
    'TOPIC_AI_simulation',
    'TOPIC_PSY_paranoia',
    'TOPIC_PSY_anamnesis',
]


def build_packets_for_topic(db, topic_id):
    """Group passages into evidence packets by claim_type + lane."""
    name = db.execute("SELECT canonical_name, study_id, slug FROM study_topics WHERE topic_id = ?",
                      (topic_id,)).fetchone()
    canonical_name, study_id, slug = name

    passages = db.execute("""
        SELECT passage_id, lane, source_mode, claim_type, confidence,
               substr(passage_text, 1, 300)
        FROM study_passages
        WHERE topic_id = ? AND source_mode IS NOT NULL
        ORDER BY lane, claim_type, passage_id
    """, (topic_id,)).fetchall()

    if not passages:
        return 0

    # Group by claim_type
    by_claim = defaultdict(list)
    for p in passages:
        by_claim[p[3]].append(p)

    # Build one packet per claim_type (if it has enough passages)
    packets = []
    for claim_type, plist in sorted(by_claim.items(), key=lambda x: -len(x[1])):
        if len(plist) < 1:
            continue

        lane_a = sum(1 for p in plist if p[1] == 'A')
        lane_b = sum(1 for p in plist if p[1] == 'B')
        lane_c = sum(1 for p in plist if p[1] == 'C')

        # Determine confidence based on passage count and diversity
        total = len(plist)
        lanes_present = sum(1 for x in [lane_a, lane_b, lane_c] if x > 0)
        high_conf = sum(1 for p in plist if p[4] == 'high')

        if total >= 10 and lanes_present >= 2:
            conf = 'strong'
        elif total >= 5 or high_conf >= 3:
            conf = 'moderate'
        elif total >= 2:
            conf = 'weak'
        else:
            conf = 'speculative'

        # Build claim text and evidence summary
        claim_text = _make_claim_text(canonical_name, claim_type, plist)
        evidence_summary = _make_evidence_summary(claim_type, plist, lane_a, lane_b, lane_c)

        packets.append({
            'claim_type': claim_type,
            'claim_text': claim_text,
            'evidence_summary': evidence_summary,
            'confidence': conf,
            'lane_a': lane_a,
            'lane_b': lane_b,
            'lane_c': lane_c,
            'passage_count': total,
        })

    # Clear existing and write
    db.execute("DELETE FROM study_evidence_packets WHERE topic_id = ?", (topic_id,))

    for idx, pkt in enumerate(packets, 1):
        ev_id = f"SEV_{study_id.upper()}_{slug.replace('-', '_')}_{idx:03d}"
        db.execute("""
            INSERT INTO study_evidence_packets
                (ev_id, topic_id, claim_text, evidence_summary, confidence,
                 source_method, lane_a_count, lane_b_count, lane_c_count)
            VALUES (?, ?, ?, ?, ?, 'heuristic', ?, ?, ?)
        """, (ev_id, topic_id, pkt['claim_text'], pkt['evidence_summary'],
              pkt['confidence'], pkt['lane_a'], pkt['lane_b'], pkt['lane_c']))

    db.execute("""
        UPDATE study_topics SET evidence_count = ?, status = 'evidence_built',
            updated_at = datetime('now')
        WHERE topic_id = ?
    """, (len(packets), topic_id))
    db.commit()

    print(f"\n  {canonical_name}: {len(packets)} evidence packets from {len(passages)} passages")
    for idx, pkt in enumerate(packets, 1):
        print(f"    [{idx}] {pkt['confidence']}: {pkt['claim_text'][:100]}")
        print(f"        A={pkt['lane_a']} B={pkt['lane_b']} C={pkt['lane_c']} ({pkt['passage_count']} passages)")

    return len(packets)


def _make_claim_text(topic_name, claim_type, passages):
    """Generate a claim summary based on claim_type and passage characteristics."""
    n = len(passages)
    templates = {
        'causal_theory': f"PKD develops theoretical explanations for {topic_name.lower()}, with {n} passages proposing causal or metaphysical frameworks.",
        'self_report': f"PKD provides first-person accounts of experiencing or encountering {topic_name.lower()} across {n} passages.",
        'definition': f"The concept of {topic_name.lower()} is defined or characterized across {n} passages.",
        'critique': f"Scholars and critics analyze PKD's treatment of {topic_name.lower()} across {n} passages.",
        'comparison': f"PKD or scholars compare {topic_name.lower()} with other concepts across {n} passages.",
        'allegory': f"{topic_name} functions allegorically in PKD's fiction across {n} passages.",
        'symptom_description': f"Characteristics of {topic_name.lower()} are described across {n} passages.",
        'unresolved': f"The relationship to {topic_name.lower()} remains ambiguous across {n} passages.",
    }
    return templates.get(claim_type, f"{topic_name} is discussed in {n} passages classified as {claim_type}.")


def _make_evidence_summary(claim_type, passages, la, lb, lc):
    """Generate evidence summary with lane breakdown."""
    parts = []
    if la:
        parts.append(f"{la} fiction passage{'s' if la > 1 else ''} (Lane A)")
    if lb:
        parts.append(f"{lb} Exegesis passage{'s' if lb > 1 else ''} (Lane B)")
    if lc:
        parts.append(f"{lc} scholarly passage{'s' if lc > 1 else ''} (Lane C)")

    lane_str = ", ".join(parts)

    # Sample some high-confidence passages for the summary
    high = [p for p in passages if p[4] == 'high']
    sample_texts = []
    for p in (high or passages)[:3]:
        snippet = p[5].strip()[:150].replace('\n', ' ')
        sample_texts.append(f'"{snippet}..."')

    summary = f"Evidence from {lane_str}. "
    if sample_texts:
        summary += "Representative: " + "; ".join(sample_texts[:2])

    return summary


def main():
    db = sqlite3.connect(str(DB))
    db.execute("PRAGMA journal_mode = WAL")

    total = 0
    for tid in PILOT_TOPICS:
        total += build_packets_for_topic(db, tid)

    print(f"\n=== TOTAL EVIDENCE PACKETS: {total} ===")
    db.close()


if __name__ == '__main__':
    main()
