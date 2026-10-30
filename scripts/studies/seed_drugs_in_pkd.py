#!/usr/bin/env python3
"""
Seed the topic "Drugs in Philip K. Dick" (study: Psychology) from the durable
curation files.

    curation/drugs-in-pkd/evidence-inventory.json   classified findings (from findings.py)
    curation/drugs-in-pkd/dossier.json              essay, browse config, contradictions

Nothing editorial is hardcoded here beyond the topic's cross-links. The script
extracts verbatim passages at the anchors the inventory names, verifies every
quotation against its source, and writes the topic, its passages, packets,
contradictions and cross-links. Unlike seed_pkd_bible.py it owns no dictionary
entries: the dictionary has none for any substance.

The lexicon-scanned topics psychology/amphetamine-use and psychology/addiction
are left as they are; this topic replaces neither, and links to both.

Shares its extraction and verification code with the other dossier seeders, so
all of them are held to the same standard. Idempotent. Registered in
build_all.py stage 5, before export_studies.

Usage:
    python scripts/studies/seed_drugs_in_pkd.py
    python scripts/studies/seed_drugs_in_pkd.py --check
"""

import argparse
import json
import re
import sqlite3
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from seed_burroughs_word_virus import (  # noqa: E402
    QUOTED, _source_corpus, ensure_schema, normalise, tidy, window,
)

PROJECT_DIR = HERE.parent.parent
DEFAULT_DB = PROJECT_DIR / 'database' / 'unified.sqlite'
CURATION = PROJECT_DIR / 'curation' / 'drugs-in-pkd'
sys.path.insert(0, str(CURATION))

STUDY_ID = 'psychology'
TOPIC_ID = 'TOPIC_PSY_drugs_in_pkd'
TOPIC_SLUG = 'drugs-in-pkd'
TOPIC_NAME = 'Drugs in Philip K. Dick'

GENERATOR = 'curation/drugs-in-pkd@2026-10-29'
PROVENANCE = 'editorial_curation_from_corpus_evidence'

RELATED_TOPICS = ['amphetamine-use', 'addiction', 'paranoia', 'psychosis', 'split-brain']

LEXICON_TOPIC_NOTES = {
    'amphetamine-use': (
        "Passages on this topic are found by matching a word list and have not been "
        "reviewed. Until October 2026 the list included the bare word \"speed\", and "
        "most matches were about velocity or the speed of light; it now matches only "
        "drug terms. For a read and sourced account, with dates and the biographers' "
        "disagreements, see the dossier Drugs in Philip K. Dick."),
    'addiction': (
        "Passages on this topic are found by matching a word list and have not been "
        "reviewed. For a read and sourced account of Dick's drug use, X-Kalay and A "
        "Scanner Darkly, see the dossier Drugs in Philip K. Dick."),
}

RELATED_TERMS = [
    ('TERM_palmer-eldritch', 'related'), ('TERM_anamnesis', 'related'),
    ('TERM_eucharist', 'related'), ('TERM_dionysos', 'related'),
    ('TERM_plasmate', 'related'),
]

RELATED_NAMES = [
    ('NAME_nancy', 'wife_1966_1970'), ('NAME_kleo', 'wife_1950_1959'),
    ('NAME_tessa', 'wife_1973_1977'), ('NAME_ray-nelson', 'lsd_companion'),
    ('NAME_kw-jeter', 'interlocutor'), ('NAME_hal', 'model_for_barris'),
    ('NAME_timothy-leary', 'blamed_in_valis'), ('NAME_john-allegro', 'sacred_mushroom'),
    ('NAME_castaneda', 'psychedelic_precedent'), ('NAME_palmer-eldritch', 'chew_z'),
    ('NAME_bob-arctor', 'substance_d_user'), ('NAME_james-barris', 'substance_d_user'),
    ('NAME_donna', 'dealer_and_informant'), ('NAME_kathy-sweetscent', 'jj180_addict'),
    ('NAME_horselover-fat', 'dick_figure'), ('NAME_gloria-knudson', 'lsd_suicide'),
]


# --------------------------------------------------------------------------
# Extraction
# --------------------------------------------------------------------------

def source_text(db, src):
    """(text, doc_id, seg_id, clean) for an inventory source."""
    stype = src['type']
    if stype == 'exegesis_segment':
        row = db.execute("SELECT raw_text, doc_id FROM segments WHERE seg_id = ?",
                         (src['id'],)).fetchone()
        return ((row[0] or '') if row else ''), (row[1] if row else None), src['id'], None
    if stype == 'letter':
        row = db.execute("SELECT body_md, volume_doc_id FROM letters WHERE letter_id = ?",
                         (src['id'],)).fetchone()
        return ((row[0] or '') if row else ''), (row[1] if row else None), None, tidy
    row = db.execute("SELECT markdown_content, text_content FROM document_texts "
                     "WHERE doc_id = ?", (src['id'],)).fetchone()
    return (((row[0] or row[1]) if row else '') or ''), src['id'], None, tidy


def collect(db, inventory, group_of):
    rows, missing, unverified, cards = [], [], [], []
    for f in inventory['evidence']:
        if not f['on_public_page']:
            continue
        src = f['source']
        text, doc_id, seg_id, clean = source_text(db, src)
        w = window(text, f['anchor'], f['window'][0], f['window'][1], clean=clean)
        if not w:
            missing.append((f['id'], src['type'], src['id'], f['anchor']))
            continue
        excerpt, start, end, cb, ca = w
        card = f['card']
        if normalise(card['pith']) not in normalise(text):
            unverified.append((f['id'], card['pith'][:70]))
        cards.append({
            'id': f['id'],
            'citation': src['citation'],
            'date': None,
            'source_type': src['type'],
            'published_folio': None,
            'seg_id': seg_id,
            'doc_id': doc_id,
            'lane': f['lane'],
            'register': f['register'],
            'relevance': f['relevance'],
            'concepts': f['concepts'],
            'context': card['context'],
            'pith': card['pith'],
            'speaker': card['speaker'],
            'editorial_note': f.get('editorial_note'),
            'dated': f.get('dated'),
            'dating_basis': f.get('dating_basis'),
            'group': group_of(src['type'], f.get('dated')),
            'packet': f['evidence_packet'],
            'passage': excerpt,
        })
        rows.append((
            TOPIC_ID, f['evidence_packet'], doc_id, seg_id, None, start, end,
            excerpt, cb, ca, f['lane'], f['source_mode'], f['claim_type'],
            f['confidence'], None, None, json.dumps(f['concepts']),
            'curated_anchor', 'approved', 'curated', src['citation'],
        ))
    return rows, missing, unverified, cards


def verify_essay(db, inventory, dossier):
    """Every 40+ char quotation verbatim in a cited source; every {{id}} resolves."""
    corpus = _source_corpus(db, inventory)
    bad_quotes, checked = [], 0
    for sec in dossier['sections']:
        for para in sec['body']:
            for groups in QUOTED.findall(para):
                q = (groups[0] or groups[1]).strip()
                if '{{' in q or not q[:1].isalpha() or len(q) < 40:
                    continue
                checked += 1
                probe = normalise(q.rstrip(' .,;'))
                if not any(probe in t for t in corpus):
                    bad_quotes.append((sec['id'], q[:70]))
    ids = {f['id'] for f in inventory['evidence'] if f['on_public_page']}
    cited, bad_cites = set(), []
    for sec in dossier['sections']:
        for para in sec['body']:
            for cid in re.findall(r'\{\{([A-Za-z0-9\-]+)\}\}', para):
                cited.add(cid)
                if cid not in ids:
                    bad_cites.append((sec['id'], cid))
    return bad_quotes, checked, bad_cites, cited, ids


# --------------------------------------------------------------------------
# Seeding
# --------------------------------------------------------------------------

def seed(db: sqlite3.Connection, check_only: bool = False):
    from dossier_sections import group_of  # curation/drugs-in-pkd

    inventory = json.loads((CURATION / 'evidence-inventory.json').read_text(encoding='utf-8'))
    dossier = json.loads((CURATION / 'dossier.json').read_text(encoding='utf-8'))
    ensure_schema(db)

    passages, missing, unverified, cards = collect(db, inventory, group_of)
    if missing:
        print("  ERROR: anchors not found in the corpus:")
        for m in missing:
            print(f"    {m[0]} [{m[1]} {m[2]}]: {m[3]!r}")
        raise SystemExit(1)
    if unverified:
        print("  ERROR: quotation is not verbatim in its source:")
        for eid, pith in unverified:
            print(f"    {eid}: {pith!r}")
        raise SystemExit(1)

    bad_quotes, checked, bad_cites, cited, ids = verify_essay(db, inventory, dossier)
    if bad_quotes:
        print("  ERROR: essay quotes text that is not verbatim in any cited source:")
        for sid, q in bad_quotes:
            print(f"    section {sid}: {q!r}")
        raise SystemExit(1)
    if bad_cites:
        print("  ERROR: essay cites findings that do not exist:")
        for sid, cid in bad_cites:
            print(f"    section {sid}: {{{{{cid}}}}}")
        raise SystemExit(1)

    # Every facet must match at least one card, and every card concept that is a
    # facet must be spelled the same way — otherwise a chip would show zero.
    concepts = Counter(c for card in cards for c in card['concepts'])
    empty = [f['label'] for f in dossier['browse']['facets'] if not concepts.get(f['label'])]
    if empty:
        raise SystemExit(f"  ERROR: facets with no cards: {empty}")

    known = {p['id'] for p in inventory['evidence_packets']}
    orphan = {r[1] for r in passages} - known
    if orphan:
        raise SystemExit(f'  ERROR: passages reference unknown packets: {orphan}')

    def find(fragment):
        hits = [i for i, r in enumerate(passages) if fragment in r[7]]
        return hits[0] if hits else None

    for c in dossier['contradictions']:
        if find(c['fragment_a']) is None or find(c['fragment_b']) is None:
            raise SystemExit(f"  ERROR: contradiction passage not found: {c['summary'][:60]}")

    if check_only:
        lanes = Counter(p[10] for p in passages)
        print(f'  OK: {len(passages)} passages resolve, lanes={dict(sorted(lanes.items()))}, '
              f'{len(inventory["evidence_packets"])} packets, '
              f'{len(dossier["sections"])} sections, {len(cards)} cards, '
              f'{len(dossier["contradictions"])} contradictions')
        print(f'  {checked} essay quotations verified verbatim; essay cites '
              f'{len(cited)} of {len(ids)} findings')
        uncited = sorted(ids - cited)
        if uncited:
            print(f'    discussed only on their card: {", ".join(uncited)}')
        return

    if not db.execute("SELECT 1 FROM studies WHERE study_id = ?", (STUDY_ID,)).fetchone():
        raise SystemExit(f"  ERROR: study {STUDY_ID!r} does not exist")

    for table in ('study_contradictions', 'study_passages', 'study_evidence_packets',
                  'study_topic_docs', 'study_topic_terms', 'study_topic_names'):
        db.execute(f"DELETE FROM {table} WHERE topic_id = ?", (TOPIC_ID,))

    db.execute("INSERT OR IGNORE INTO study_topics (topic_id, study_id, canonical_name, slug) "
               "VALUES (?, ?, ?, ?)", (TOPIC_ID, STUDY_ID, TOPIC_NAME, TOPIC_SLUG))

    db.executemany("""
        INSERT INTO study_passages
            (topic_id, ev_id, doc_id, seg_id, page_num, char_offset_start,
             char_offset_end, passage_text, context_before, context_after, lane,
             source_mode, claim_type, confidence, psych_mode, ai_mode,
             matched_terms, match_method, fair_use_status, editorial_status, notes)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, passages)

    per_packet = {}
    for p in passages:
        per_packet.setdefault(p[1], Counter())[p[10]] += 1
    for pkt in inventory['evidence_packets']:
        counts = per_packet.get(pkt['id'], Counter())
        db.execute("""
            INSERT INTO study_evidence_packets
                (ev_id, topic_id, claim_text, evidence_summary, confidence,
                 source_method, editorial_status, lane_a_count, lane_b_count,
                 lane_c_count, notes)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """, (pkt['id'], TOPIC_ID, pkt['claim'],
              pkt['summary'], pkt['confidence'], 'editorial', 'reviewed',
              counts['A'], counts['B'], counts['C'], GENERATOR))

    def passage_id_for(fragment):
        row = db.execute("""
            SELECT passage_id FROM study_passages
            WHERE topic_id = ? AND instr(passage_text, ?) > 0
            ORDER BY passage_id LIMIT 1
        """, (TOPIC_ID, fragment)).fetchone()
        return row[0] if row else None

    for c in dossier['contradictions']:
        db.execute("""
            INSERT INTO study_contradictions
                (topic_id, passage_id_a, passage_id_b, summary, explanation,
                 contradiction_type, notes)
            VALUES (?,?,?,?,?,?,?)
        """, (TOPIC_ID, passage_id_for(c['fragment_a']), passage_id_for(c['fragment_b']),
              c['summary'], c['explanation'], c['type'], GENERATOR))

    fields = dossier['fields']
    db.execute("""
        UPDATE study_topics SET
            study_id = ?, canonical_name = ?, slug = ?, status = 'reviewed',
            priority = 10, definition = ?, pkd_relevance = ?, in_the_fiction = ?,
            in_the_exegesis = ?, intellectual_background = ?, scholarly_debate = ?,
            chronology_summary = ?, contradictions_summary = ?, related_thinkers = ?,
            editorial_notes = ?, open_questions = ?, card_description = ?,
            passage_count = ?, evidence_count = ?, contradiction_count = ?,
            first_appearance = '1962', peak_period_start = '1964',
            peak_period_end = '1972', related_topics = ?, provenance = ?, notes = ?,
            dossier_sections = ?, mention_cards = ?, browse_config = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE topic_id = ?
    """, (STUDY_ID, TOPIC_NAME, TOPIC_SLUG,
          fields['definition'], fields['pkd_relevance'], fields['in_the_fiction'],
          fields['in_the_exegesis'], fields['intellectual_background'],
          fields['scholarly_debate'], fields['chronology_summary'],
          fields['contradictions_summary'], json.dumps(dossier['related_thinkers']),
          fields['editorial_notes'], json.dumps(dossier['open_questions']),
          dossier['card_description'], len(passages),
          len(inventory['evidence_packets']), len(dossier['contradictions']),
          json.dumps(RELATED_TOPICS), PROVENANCE, GENERATOR,
          json.dumps(dossier['sections'], ensure_ascii=False),
          json.dumps(cards, ensure_ascii=False),
          json.dumps(dossier['browse'], ensure_ascii=False), TOPIC_ID))
    for field in ('definition', 'pkd_relevance', 'in_the_fiction', 'in_the_exegesis',
                  'intellectual_background', 'scholarly_debate', 'chronology_summary',
                  'contradictions_summary', 'editorial_notes'):
        db.execute(f"UPDATE study_topics SET {field}_generator = ?, {field}_claim_ids = '[]' "
                   f"WHERE topic_id = ?", (GENERATOR, TOPIC_ID))

    # Documents: relevance from how many published passages each contributes.
    per_doc = Counter(p[2] for p in passages if p[2])
    for doc_id, n in per_doc.items():
        if not db.execute("SELECT 1 FROM documents WHERE doc_id = ?", (doc_id,)).fetchone():
            continue
        rel = 'primary' if n >= 4 else 'substantial' if n >= 2 else 'mentions'
        db.execute("INSERT OR REPLACE INTO study_topic_docs "
                   "(topic_id, doc_id, relevance, passage_count) VALUES (?,?,?,?)",
                   (TOPIC_ID, doc_id, rel, n))

    for term_id, rel in RELATED_TERMS:
        if db.execute("SELECT 1 FROM terms WHERE term_id = ? AND status = 'accepted'",
                      (term_id,)).fetchone():
            db.execute("INSERT OR REPLACE INTO study_topic_terms (topic_id, term_id, "
                       "relation_type) VALUES (?,?,?)", (TOPIC_ID, term_id, rel))
    for name_id, rel in RELATED_NAMES:
        if db.execute("SELECT 1 FROM names WHERE name_id = ?", (name_id,)).fetchone():
            db.execute("INSERT OR REPLACE INTO study_topic_names (topic_id, name_id, "
                       "relation_type) VALUES (?,?,?)", (TOPIC_ID, name_id, rel))

    # Point the lexicon-scanned drug topics at this dossier. They are machine
    # scans with unreviewed passages; this is the read account of the same ground.
    for slug, note in LEXICON_TOPIC_NOTES.items():
        row = db.execute("SELECT topic_id, related_topics FROM study_topics "
                         "WHERE study_id = ? AND slug = ?", (STUDY_ID, slug)).fetchone()
        if not row:
            continue
        related = json.loads(row[1]) if row[1] else []
        if TOPIC_SLUG not in related:
            related.insert(0, TOPIC_SLUG)
        db.execute("UPDATE study_topics SET related_topics = ?, editorial_notes = ?, "
                   "updated_at = CURRENT_TIMESTAMP WHERE topic_id = ?",
                   (json.dumps(related), note, row[0]))

    db.execute("UPDATE studies SET topic_count = "
               "(SELECT COUNT(*) FROM study_topics WHERE study_id = ?) WHERE study_id = ?",
               (STUDY_ID, STUDY_ID))
    db.commit()

    lanes = Counter(p[10] for p in passages)
    print(f"  topic            {TOPIC_ID} ({STUDY_ID}/{TOPIC_SLUG})")
    print(f"  passages         {len(passages)}  lanes={dict(sorted(lanes.items()))}")
    print(f"  evidence packets {len(inventory['evidence_packets'])}")
    print(f"  contradictions   {len(dossier['contradictions'])}")
    print(f"  mention cards    {len(cards)} (all quotations verified verbatim)")
    print(f"  essay            {len(dossier['sections'])} sections, {checked} long "
          f"quotations verified, {len(cited)} findings cited")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--db', type=Path, default=DEFAULT_DB)
    ap.add_argument('--check', action='store_true',
                    help='verify every anchor and quotation; write nothing')
    args = ap.parse_args()
    if not args.db.exists():
        print(f"Database not found: {args.db}", file=sys.stderr)
        raise SystemExit(1)
    db = sqlite3.connect(str(args.db))
    db.execute("PRAGMA foreign_keys = ON")
    print("Seeding 'Drugs in Philip K. Dick' from curation/ ...")
    seed(db, check_only=args.check)
    db.close()
    if not args.check:
        print("Done. Now: export the topic file only; see curation/drugs-in-pkd/README.md")


if __name__ == '__main__':
    main()
