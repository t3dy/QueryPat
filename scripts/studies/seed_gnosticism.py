#!/usr/bin/env python3
"""
Seed the "Gnosticism" study and its six topics into the database from the
durable curation files.

    curation/gnosticism/lexicon.json          term register (hand-authored)
    curation/gnosticism/register.json         lexicon joined to attestations
    curation/gnosticism/dossier_sections.py   editorial prose (hand-authored)
    curation/gnosticism/dossier.json          the assembled artifact

Nothing editorial is hardcoded here. This script reads the artifact that
`scripts/studies/build_gnosticism_study.py` assembles and writes it into the
database, so that a database rebuilt from scratch restores the pages. That is
the point — see docs/PRESERVATION.md.

Idempotent: deletes this study's own rows before reinserting. Register in
build_all.py stage 5, before export_studies, alongside
seed_burroughs_word_virus.py.

Usage:
    python scripts/research/gnostic_lexicon_source.py      # 1. lexicon
    python scripts/research/sweep_gnosticism.py            # 2. sweep corpus
    python scripts/research/build_gnostic_register.py      # 3. join
    python scripts/studies/build_gnosticism_study.py       # 4. assemble
    python scripts/studies/seed_gnosticism.py              # 5. write to DB
    python scripts/safeguard/safe_export.py --exporter studies

    python scripts/studies/seed_gnosticism.py --check      # validate only
"""

import argparse
import json
import sqlite3
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_DB = PROJECT_DIR / 'database' / 'unified.sqlite'
CUR = PROJECT_DIR / 'curation' / 'gnosticism'

STUDY_ID = 'gnosticism'
GENERATOR = 'curation/gnosticism@2026-09-18'
PROVENANCE = 'editorial_curation_from_corpus_sweep'


def load_dossier():
    path = CUR / 'dossier.json'
    if not path.exists():
        raise SystemExit(
            f'{path} not found. Run scripts/studies/build_gnosticism_study.py '
            f'first — it assembles the dossier from the curation sources.')
    return json.loads(path.read_text(encoding='utf-8'))


def seed(db, dossier):
    topics = dossier['topics']

    db.execute("""
        INSERT INTO studies (study_id, study_label, study_description, topic_count)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(study_id) DO UPDATE SET
            study_label = excluded.study_label,
            study_description = excluded.study_description,
            topic_count = excluded.topic_count,
            updated_at = CURRENT_TIMESTAMP
    """, (STUDY_ID, dossier['study_label'], dossier['study_description'],
          len(topics)))

    for t in topics:
        tid = t['topic_id']
        for table in ('study_contradictions', 'study_passages',
                      'study_evidence_packets', 'study_topic_docs',
                      'study_topic_terms', 'study_topic_names'):
            db.execute(f'DELETE FROM {table} WHERE topic_id = ?', (tid,))

        db.execute("""
            INSERT OR IGNORE INTO study_topics
                (topic_id, study_id, canonical_name, slug)
            VALUES (?, ?, ?, ?)
        """, (tid, STUDY_ID, t['canonical_name'], t['slug']))

        passages = []
        for pkt in t['evidence_packets']:
            for p in pkt['passages']:
                passages.append((
                    tid, pkt['ev_id'], p.get('doc_id'), p.get('seg_id'),
                    None, None, None,
                    p['passage_text'], None, None,
                    p['lane'], p['source_mode'], p['claim_type'],
                    p['confidence'], None, None,
                    json.dumps(p.get('matched_terms') or []),
                    'corpus_sweep', 'excerpt_within_fair_use', 'reviewed',
                    GENERATOR,
                ))
        if passages:
            db.executemany("""
                INSERT INTO study_passages
                    (topic_id, ev_id, doc_id, seg_id, page_num,
                     char_offset_start, char_offset_end, passage_text,
                     context_before, context_after, lane, source_mode,
                     claim_type, confidence, psych_mode, ai_mode, matched_terms,
                     match_method, fair_use_status, editorial_status, notes)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, passages)

        for pkt in t['evidence_packets']:
            db.execute("""
                INSERT INTO study_evidence_packets
                    (ev_id, topic_id, claim_text, evidence_summary, confidence,
                     source_method, editorial_status, lane_a_count,
                     lane_b_count, lane_c_count, notes)
                VALUES (?,?,?,?,?,?,?,?,?,?,?)
            """, (pkt['ev_id'], tid, pkt['claim_text'], pkt['evidence_summary'],
                  pkt['confidence'], 'corpus_sweep', 'reviewed',
                  pkt['lane_a_count'], pkt['lane_b_count'], pkt['lane_c_count'],
                  GENERATOR))

        for rel in t.get('related_terms') or []:
            db.execute("""
                INSERT OR IGNORE INTO study_topic_terms
                    (topic_id, term_id, relation_type)
                VALUES (?,?,?)
            """, (tid, rel['term_id'], rel.get('relation_type') or 'related'))

        db.execute("""
            INSERT INTO study_topics
                (topic_id, study_id, canonical_name, slug, status, priority,
                 definition, pkd_relevance, in_the_fiction, in_the_exegesis,
                 intellectual_background, scholarly_debate, chronology_summary,
                 contradictions_summary, related_thinkers, editorial_notes,
                 open_questions, card_description, passage_count, evidence_count,
                 contradiction_count, first_appearance, peak_period_start,
                 peak_period_end, related_topics, provenance, notes)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(topic_id) DO UPDATE SET
                study_id = excluded.study_id,
                canonical_name = excluded.canonical_name,
                slug = excluded.slug,
                status = excluded.status,
                priority = excluded.priority,
                definition = excluded.definition,
                pkd_relevance = excluded.pkd_relevance,
                in_the_fiction = excluded.in_the_fiction,
                in_the_exegesis = excluded.in_the_exegesis,
                intellectual_background = excluded.intellectual_background,
                scholarly_debate = excluded.scholarly_debate,
                chronology_summary = excluded.chronology_summary,
                contradictions_summary = excluded.contradictions_summary,
                related_thinkers = excluded.related_thinkers,
                editorial_notes = excluded.editorial_notes,
                open_questions = excluded.open_questions,
                card_description = excluded.card_description,
                passage_count = excluded.passage_count,
                evidence_count = excluded.evidence_count,
                contradiction_count = excluded.contradiction_count,
                first_appearance = excluded.first_appearance,
                peak_period_start = excluded.peak_period_start,
                peak_period_end = excluded.peak_period_end,
                related_topics = excluded.related_topics,
                provenance = excluded.provenance,
                notes = excluded.notes
        """, (
            tid, STUDY_ID, t['canonical_name'], t['slug'], t['status'],
            _priority(dossier, t['slug']),
            t['definition'], t['pkd_relevance'], t.get('in_the_fiction'),
            t.get('in_the_exegesis'), t.get('intellectual_background'),
            t.get('scholarly_debate'), t.get('chronology_summary'),
            t.get('contradictions_summary'),
            json.dumps(t.get('related_thinkers') or []),
            t.get('editorial_notes'),
            json.dumps(t.get('open_questions') or []),
            _card(dossier, t['slug']),
            t['passage_count'], t['evidence_count'], t['contradiction_count'],
            t.get('first_appearance'), t.get('peak_period_start'),
            t.get('peak_period_end'),
            json.dumps([r['slug'] for r in t.get('related_topics') or []]),
            PROVENANCE, GENERATOR,
        ))
        print(f'  {t["slug"]:26s} {t["evidence_count"]:3d} packets  '
              f'{len(passages):3d} passages')

    db.execute("UPDATE studies SET topic_count = "
               "(SELECT COUNT(*) FROM study_topics WHERE study_id = ?) "
               "WHERE study_id = ?", (STUDY_ID, STUDY_ID))


def _find(dossier, slug, key, default=None):
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        'gnostic_dossier', CUR / 'dossier_sections.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    for t in mod.TOPICS:
        if t['slug'] == slug:
            return t.get(key, default)
    return default


def _priority(dossier, slug):
    return _find(dossier, slug, 'priority', 5)


def _card(dossier, slug):
    return _find(dossier, slug, 'card_description', '')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--db', default=str(DEFAULT_DB))
    ap.add_argument('--check', action='store_true',
                    help='validate the curation inputs, write nothing')
    args = ap.parse_args()

    dossier = load_dossier()
    topics = dossier['topics']
    passages = sum(len(p['passages'])
                   for t in topics for p in t['evidence_packets'])
    packets = sum(len(t['evidence_packets']) for t in topics)

    if args.check:
        print(f'dossier OK: {len(topics)} topics, {packets} evidence packets, '
              f'{passages} passages.')
        for t in topics:
            missing = [f for f in ('definition', 'pkd_relevance') if not t.get(f)]
            if missing:
                print(f'  WARNING {t["slug"]}: missing {", ".join(missing)}')
        return 0

    if not Path(args.db).exists():
        print(f'ERROR: no database at {args.db}. Build it first:\n'
              f'    python scripts/build_all.py', file=sys.stderr)
        return 1

    db = sqlite3.connect(args.db)
    try:
        seed(db, dossier)
        db.commit()
    finally:
        db.close()
    print(f'\nSeeded "{STUDY_ID}": {len(topics)} topics, {packets} packets, '
          f'{passages} passages.')
    print('Now: python scripts/safeguard/safe_export.py --exporter studies')
    return 0


if __name__ == '__main__':
    sys.exit(main())
