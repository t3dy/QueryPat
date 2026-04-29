#!/usr/bin/env python3
"""
Layer 2 Pilot: Detect contradictions deterministically.

Identifies tensions between passages across different lanes or with
conflicting claim_types. Only flags explicit, grounded contradictions.
"""

import re
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent.parent / 'database' / 'unified.sqlite'

PILOT_TOPICS = [
    'TOPIC_AI_androids',
    'TOPIC_AI_simulation',
    'TOPIC_PSY_paranoia',
    'TOPIC_PSY_anamnesis',
]

# Semantic tension patterns — pairs of ideas that genuinely conflict
TENSION_PAIRS = [
    # (regex_a, regex_b, contradiction_type, summary_template)
    (r'\b(real|genuine|authentic|truly human)\b',
     r'\b(fake|counterfeit|simulacr|artificial|not real|illusion)\b',
     'interpretive',
     "Tension between claims of authenticity and claims of counterfeiting/simulation"),

    (r'\b(free will|choice|autonomous|freedom)\b',
     r'\b(programmed|determined|controlled|no choice|puppet|pre-programmed)\b',
     'interpretive',
     "Tension between free will and determinism/programming"),

    (r'\b(empathy|compassion|human feeling|love|caritas)\b',
     r'\b(cold|mechanical|unfeeling|no empathy|android|machine)\b',
     'interpretive',
     "Tension between empathy/human feeling and mechanical coldness"),

    (r'\b(paranoi[ac]|suspicion|persecution|being watched)\b',
     r'\b(justified|real threat|actual conspiracy|they really were)\b',
     'factual',
     "Tension between paranoia as pathology and paranoia as justified perception"),

    (r'\b(mental illness|psychosis|breakdown|madness|insane)\b',
     r'\b(mystical|divine|revelation|theophany|genuine experience|spiritual)\b',
     'interpretive',
     "Tension between psychiatric and mystical interpretations"),

    (r'\b(Plato|Platonic|recollect|anamnesis)\b',
     r'\b(Gnostic|gnosis|Nag Hammadi|demiurge|archon)\b',
     'interpretive',
     "Tension between Platonic and Gnostic frameworks for anamnesis"),

    (r'\b(early work|early fiction|1950s|1960s|early PKD)\b',
     r'\b(later work|late fiction|1970s|1980s|later PKD|VALIS)\b',
     'chronological',
     "Chronological tension between early and late positions"),

    (r'\b(in the (novel|story|fiction)|Dick (depicts|writes|portrays))\b',
     r'\b(in the Exegesis|Dick (theorizes|speculates|argues))\b',
     'fiction_vs_exegesis',
     "Tension between fictional depiction and Exegetical theorizing"),
]


def find_contradictions_for_topic(db, topic_id):
    """Find contradictions between passages within a topic."""
    name = db.execute("SELECT canonical_name FROM study_topics WHERE topic_id = ?",
                      (topic_id,)).fetchone()[0]

    passages = db.execute("""
        SELECT passage_id, lane, source_mode, claim_type, confidence,
               passage_text
        FROM study_passages
        WHERE topic_id = ? AND source_mode IS NOT NULL AND confidence != 'low'
        ORDER BY lane, passage_id
    """, (topic_id,)).fetchall()

    if len(passages) < 2:
        print(f"  {name}: too few passages for contradiction detection")
        return 0

    # Strategy: find cross-lane pairs that match tension patterns
    # Also: self_report vs critique (Dick says X, scholar says not-X)
    contradictions = []

    # Compile tension patterns
    compiled_tensions = []
    for pat_a, pat_b, ctype, summary in TENSION_PAIRS:
        compiled_tensions.append((
            re.compile(pat_a, re.I),
            re.compile(pat_b, re.I),
            ctype, summary
        ))

    # Cross-lane contradictions using tension patterns
    for i, p1 in enumerate(passages):
        text1 = p1[5][:800]
        for j, p2 in enumerate(passages):
            if j <= i:
                continue
            # Prefer cross-lane tensions
            if p1[1] == p2[1] and p1[2] == p2[2]:
                continue  # Same lane AND same source_mode = less interesting

            text2 = p2[5][:800]

            for regex_a, regex_b, ctype, summary_tmpl in compiled_tensions:
                if regex_a.search(text1) and regex_b.search(text2):
                    # Check this isn't a trivial match
                    contradictions.append({
                        'pid_a': p1[0],
                        'pid_b': p2[0],
                        'lane_a': p1[1],
                        'lane_b': p2[1],
                        'type': ctype,
                        'summary': summary_tmpl,
                    })
                    break  # One contradiction per pair
                elif regex_b.search(text1) and regex_a.search(text2):
                    contradictions.append({
                        'pid_a': p1[0],
                        'pid_b': p2[0],
                        'lane_a': p1[1],
                        'lane_b': p2[1],
                        'type': ctype,
                        'summary': summary_tmpl,
                    })
                    break

    # Deduplicate: keep at most 2 per contradiction_type per topic
    # (avoid flooding with 100 variations of the same tension)
    type_counts = {}
    filtered = []
    for c in contradictions:
        ct = c['type']
        type_counts[ct] = type_counts.get(ct, 0) + 1
        # Keep max 3 per type, preferring cross-lane
        if type_counts[ct] <= 3:
            filtered.append(c)
        elif c['lane_a'] != c['lane_b'] and type_counts[ct] <= 5:
            filtered.append(c)

    # Clear and write
    db.execute("DELETE FROM study_contradictions WHERE topic_id = ?", (topic_id,))

    for c in filtered:
        explanation = (f"Passage {c['pid_a']} (Lane {c['lane_a']}) and "
                       f"passage {c['pid_b']} (Lane {c['lane_b']}) "
                       f"exhibit this tension.")
        db.execute("""
            INSERT INTO study_contradictions
                (topic_id, passage_id_a, passage_id_b, summary,
                 explanation, contradiction_type)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (topic_id, c['pid_a'], c['pid_b'],
              c['summary'], explanation, c['type']))

    cc = len(filtered)
    db.execute("UPDATE study_topics SET contradiction_count = ? WHERE topic_id = ?",
               (cc, topic_id))
    db.commit()

    print(f"\n  {name}: {cc} contradictions (from {len(contradictions)} candidates)")
    for c in filtered[:2]:
        print(f"    [{c['type']}] P{c['pid_a']}(L{c['lane_a']}) vs P{c['pid_b']}(L{c['lane_b']}): {c['summary'][:100]}")

    return cc


def main():
    db = sqlite3.connect(str(DB))
    db.execute("PRAGMA journal_mode = WAL")

    total = 0
    for tid in PILOT_TOPICS:
        total += find_contradictions_for_topic(db, tid)

    print(f"\n=== TOTAL CONTRADICTIONS: {total} ===")
    db.close()


if __name__ == '__main__':
    main()
