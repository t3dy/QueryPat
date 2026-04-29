#!/usr/bin/env python3
"""
Deterministic passage classifier for Layer 2 pilot.
No API calls. Uses lane, doc_id, seg_id, and keyword heuristics.

Pilot topics:
  TOPIC_AI_androids, TOPIC_AI_simulation,
  TOPIC_PSY_paranoia, TOPIC_PSY_anamnesis
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

# ── source_mode ───────────────────────────────────────────────

def classify_source_mode(lane, doc_id, seg_id, text):
    """Determine source_mode from lane + doc metadata."""
    doc = (doc_id or '').upper()
    seg = (seg_id or '').upper()
    t = text[:500].lower()

    # Lane B with Exegesis segment → exegesis
    if lane == 'B' and 'SEG_EXEG' in seg:
        return 'exegesis'
    if lane == 'B':
        return 'exegesis'

    # Lane A → fiction
    if lane == 'A':
        # Some Lane A docs are actually anthologies with criticism intros
        if any(k in t for k in ['scholarly', 'argues that', 'according to', 'bibliography', 'footnote']):
            return 'criticism'
        return 'fiction'

    # Lane C → usually criticism, but check for fiction anthologies or interviews
    if lane == 'C':
        if any(k in t for k in ['interview', 'q:', 'q.', 'interviewer:']):
            return 'interview'
        if any(k in t for k in ['dear ', 'sincerely', 'yours truly', 'best wishes']):
            return 'letter'
        # Check if it's actually fiction text embedded in an anthology
        if any(k in doc for k in ['READER', 'STORIES', 'COLLECTED', 'NOVEL']):
            if not any(k in t for k in ['argues', 'scholar', 'critic', 'analysis', 'bibliography']):
                return 'fiction'
        return 'criticism'

    return 'criticism'


# ── claim_type ────────────────────────────────────────────────

# Keyword patterns for claim_type detection
DEFINITION_PAT = re.compile(
    r'\b(is defined as|means that|refers to|the concept of|by .* [Ii] mean|'
    r'what is|definition of|denotes|signifies)\b', re.I)
SELF_REPORT_PAT = re.compile(
    r'\b(I (saw|felt|experienced|realized|remembered|recalled|perceived|sensed|knew)|'
    r'my (experience|vision|perception|memory)|it came to me|I was aware|'
    r'happened to me|I suddenly|in 2-3-74|in Feb\.? 1974|March 1974|'
    r'I remember|I had a|I began to|I found myself)\b', re.I)
CAUSAL_THEORY_PAT = re.compile(
    r'\b(because|therefore|thus|hence|the reason|this means|this implies|'
    r'it follows|the cause|caused by|due to|results from|explains why|'
    r'mechanism|hypothesis|theory|if .* then)\b', re.I)
ALLEGORY_PAT = re.compile(
    r'\b(metaphor|allegory|symbol|represents|stands for|embodies|'
    r'personif|analogous|parable|figurative)\b', re.I)
CRITIQUE_PAT = re.compile(
    r'\b(argues that|according to|scholar|critic|commentary|interpretation|'
    r'analysis|Dick\'s (work|fiction|novel|writing)|literary|Sutin|'
    r'Rickman|Carrère|Mackey|Fitting|Warrick|Jameson|Freedman)\b', re.I)
COMPARISON_PAT = re.compile(
    r'\b(like|unlike|similar to|in contrast|compared to|whereas|'
    r'on the other hand|distinction between|differs from|resembles)\b', re.I)
SYMPTOM_PAT = re.compile(
    r'\b(symptom|manifest|characterized by|exhibits|displays|'
    r'behavior|affect|presentation|signs of|features of)\b', re.I)


def classify_claim_type(source_mode, text, topic_id):
    t = text[:1500]

    # Criticism source → usually critique
    if source_mode == 'criticism':
        if DEFINITION_PAT.search(t):
            return 'definition'
        if COMPARISON_PAT.search(t):
            return 'comparison'
        return 'critique'

    # Interview → self_report or comparison
    if source_mode == 'interview':
        if SELF_REPORT_PAT.search(t):
            return 'self_report'
        return 'comparison'

    # Fiction → allegory or symptom_description
    if source_mode == 'fiction':
        if ALLEGORY_PAT.search(t):
            return 'allegory'
        if SYMPTOM_PAT.search(t):
            return 'symptom_description'
        return 'allegory'

    # Exegesis — richest classification
    if source_mode == 'exegesis':
        if DEFINITION_PAT.search(t):
            return 'definition'
        if SELF_REPORT_PAT.search(t):
            return 'self_report'
        if CAUSAL_THEORY_PAT.search(t):
            return 'causal_theory'
        if COMPARISON_PAT.search(t):
            return 'comparison'
        if ALLEGORY_PAT.search(t):
            return 'allegory'
        # Default for Exegesis: causal_theory (PKD is usually theorizing)
        return 'causal_theory'

    return 'unresolved'


# ── confidence ────────────────────────────────────────────────

# Per-topic high-confidence keywords
CONFIDENCE_KEYWORDS = {
    'TOPIC_AI_androids': [
        'android', 'androids', 'simulacr', 'artificial person', 'artificial human',
        'humanoid', 'replicant', 'andy', 'Voigt-Kampff',
    ],
    'TOPIC_AI_simulation': [
        'simulat', 'simulated', 'simulation', 'virtual reality', 'fake world',
        'illusory world', 'Black Iron Prison', 'BIP', 'hologram', 'dokos',
        'Maya', 'veil', 'counterfeit reality',
    ],
    'TOPIC_PSY_paranoia': [
        'paranoi', 'paranoid', 'persecution', 'conspira', 'they are watching',
        'being followed', 'suspicion', 'suspicious', 'break-in', 'break in',
    ],
    'TOPIC_PSY_anamnesis': [
        'anamnesis', 'anamnetic', 'unforgetting', 'Platonic recollection',
        'remembering', 'recalled', 'pre-exist', 'prior life', 'amnesia',
        'Plato', 'Meno',
    ],
}


def classify_confidence(text, topic_id):
    t = text[:1500].lower()
    keywords = CONFIDENCE_KEYWORDS.get(topic_id, [])

    high_count = sum(1 for k in keywords if k.lower() in t)

    if high_count >= 2:
        return 'high'
    elif high_count == 1:
        return 'medium'
    else:
        return 'low'


# ── psych_mode / ai_mode ─────────────────────────────────────

PSYCH_KEYWORDS = {
    'clinical': ['DSM', 'diagnosis', 'clinical', 'disorder', 'medication', 'treatment',
                  'hospitali', 'symptom', 'patholog'],
    'psychoanalytic': ['Freud', 'Freudian', 'unconscious', 'repression', 'libido',
                        'ego', 'superego', 'id ', 'Oedipal', 'castration'],
    'Jungian': ['Jung', 'Jungian', 'archetype', 'collective unconscious', 'individuation',
                'anima', 'animus', 'shadow', 'mandala', 'synchronicity'],
    'existential': ['existential', 'Heidegger', 'being-in-the-world', 'Dasein',
                     'angst', 'authenticity', 'alienation', 'absurd', 'Sartre', 'Kierkegaard'],
    'mystical': ['mystical', 'divine', 'God', 'Christ', 'Holy Spirit', 'Paraclete',
                  'Logos', 'theophany', 'gnostic', 'gnosis', 'transcend', 'sacred',
                  'Zebra', 'VALIS', 'Sophia', 'Shekinah', '2-3-74', 'Nag Hammadi'],
    'anti-psychiatric': ['anti-psychiatr', 'Laing', 'Szasz', 'madness as', 'sane',
                          'insane', 'labeling', 'institution'],
    'neuropsychological': ['brain', 'hemisphere', 'neural', 'cortex', 'neurotransmitter',
                            'dopamine', 'split-brain', 'bicameral'],
    'popular_psychology': ['self-help', 'personality type', 'coping', 'stress'],
}

AI_KEYWORDS = {
    'theological': ['God', 'Christ', 'divine', 'sacred', 'Logos', 'demiurge', 'gnostic',
                     'gnosis', 'salvation', 'soul', 'spirit', 'transcend', 'Zebra', 'VALIS',
                     'Sophia', 'Holy Spirit', 'Paraclete'],
    'philosophical': ['consciousness', 'personhood', 'ontolog', 'epistemolog', 'Descartes',
                       'Kant', 'Plato', 'Spinoza', 'substance', 'mind-body', 'qualia',
                       'phenomenol', 'being', 'existence'],
    'literary': ['novel', 'story', 'character', 'narrative', 'plot', 'fiction', 'genre',
                  'science fiction', 'SF', 'text', 'reader', 'author', 'writing',
                  'literary', 'prose', 'thematic'],
    'sociological': ['society', 'social', 'capitalis', 'labor', 'class', 'power',
                      'political', 'control', 'surveillance', 'authoritar', 'totalitar'],
    'engineering': ['circuit', 'program', 'algorithm', 'compute', 'machine', 'robot',
                     'mechanism', 'technical', 'cybernetic', 'feedback', 'system'],
}


def classify_psych_mode(text, topic_id):
    """For psychology topics only."""
    if 'PSY' not in topic_id:
        return None
    t = text[:1500].lower()
    scores = {}
    for mode, keywords in PSYCH_KEYWORDS.items():
        scores[mode] = sum(1 for k in keywords if k.lower() in t)
    best = max(scores, key=scores.get)
    if scores[best] == 0:
        # Default by topic
        if 'anamnesis' in topic_id:
            return 'mystical'
        if 'paranoia' in topic_id:
            return 'existential'
        return 'clinical'
    return best


def classify_ai_mode(text, topic_id):
    """For AI topics only."""
    if 'AI' not in topic_id:
        return None
    t = text[:1500].lower()
    scores = {}
    for mode, keywords in AI_KEYWORDS.items():
        scores[mode] = sum(1 for k in keywords if k.lower() in t)
    best = max(scores, key=scores.get)
    if scores[best] == 0:
        if 'simulation' in topic_id:
            return 'philosophical'
        if 'androids' in topic_id:
            return 'philosophical'
        return 'literary'
    return best


# ── Main ──────────────────────────────────────────────────────

def main():
    db = sqlite3.connect(str(DB))
    db.execute("PRAGMA journal_mode = WAL")

    # Reset pilot passages
    for tid in PILOT_TOPICS:
        db.execute("""
            UPDATE study_passages SET source_mode = NULL, claim_type = NULL,
                confidence = NULL, psych_mode = NULL, ai_mode = NULL
            WHERE topic_id = ?
        """, (tid,))
    db.commit()

    total = 0
    for tid in PILOT_TOPICS:
        rows = db.execute("""
            SELECT passage_id, lane, passage_text, doc_id, seg_id
            FROM study_passages WHERE topic_id = ?
            ORDER BY passage_id
        """, (tid,)).fetchall()

        name = db.execute("SELECT canonical_name FROM study_topics WHERE topic_id = ?",
                          (tid,)).fetchone()[0]
        print(f"\n--- {name} ({tid}): {len(rows)} passages ---")

        updates = []
        for pid, lane, text, doc_id, seg_id in rows:
            sm = classify_source_mode(lane, doc_id, seg_id, text)
            ct = classify_claim_type(sm, text, tid)
            conf = classify_confidence(text, tid)
            pm = classify_psych_mode(text, tid)
            am = classify_ai_mode(text, tid)
            updates.append((sm, ct, conf, pm, am, pid))

        # Batch update
        db.executemany("""
            UPDATE study_passages SET
                source_mode = ?, claim_type = ?, confidence = ?,
                psych_mode = ?, ai_mode = ?
            WHERE passage_id = ?
        """, updates)
        db.commit()
        total += len(updates)

        # Summary
        for label, col in [('source_mode', 'source_mode'), ('claim_type', 'claim_type'),
                            ('confidence', 'confidence')]:
            dist = db.execute(f"""
                SELECT {col}, COUNT(*) FROM study_passages
                WHERE topic_id = ? AND {col} IS NOT NULL
                GROUP BY {col} ORDER BY COUNT(*) DESC
            """, (tid,)).fetchall()
            print(f"  {label}: {dict(dist)}")

        mode_col = 'psych_mode' if 'PSY' in tid else 'ai_mode'
        dist = db.execute(f"""
            SELECT {mode_col}, COUNT(*) FROM study_passages
            WHERE topic_id = ? AND {mode_col} IS NOT NULL
            GROUP BY {mode_col} ORDER BY COUNT(*) DESC
        """, (tid,)).fetchall()
        print(f"  {mode_col}: {dict(dist)}")

        # 3 samples
        samples = db.execute("""
            SELECT passage_id, lane, source_mode, claim_type, confidence,
                   psych_mode, ai_mode, substr(passage_text, 1, 120)
            FROM study_passages WHERE topic_id = ?
            ORDER BY RANDOM() LIMIT 3
        """, (tid,)).fetchall()
        for s in samples:
            print(f"  P{s[0]} L={s[1]} sm={s[2]} ct={s[3]} c={s[4]} pm={s[5]} am={s[6]}")
            print(f"    {s[7]}...")

    # Grand summary
    print(f"\n=== TOTAL CLASSIFIED: {total} ===")

    print("\n--- 10 Random Samples Across All Pilot Topics ---")
    samples = db.execute("""
        SELECT sp.passage_id, st.canonical_name, sp.lane, sp.source_mode,
               sp.claim_type, sp.confidence, sp.psych_mode, sp.ai_mode,
               substr(sp.passage_text, 1, 150)
        FROM study_passages sp
        JOIN study_topics st ON sp.topic_id = st.topic_id
        WHERE sp.topic_id IN (?,?,?,?) AND sp.source_mode IS NOT NULL
        ORDER BY RANDOM() LIMIT 10
    """, PILOT_TOPICS).fetchall()
    for s in samples:
        print(f"  P{s[0]} | {s[1]} | Lane {s[2]} | sm={s[3]} ct={s[4]} c={s[5]} pm={s[6]} am={s[7]}")
        print(f"    {s[8]}...")
        print()

    db.close()


if __name__ == '__main__':
    main()
