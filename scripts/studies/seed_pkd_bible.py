#!/usr/bin/env python3
"""
Seed the topic "Philip K. Dick and the Bible" (study: Intertexts & Influences)
from the durable curation files.

    curation/pkd-bible/evidence-inventory.json   classified findings (from findings.py)
    curation/pkd-bible/dossier.json              essay, browse config, contradictions

Nothing editorial is hardcoded here beyond the dictionary entries this topic
owns. The script extracts verbatim passages at the anchors the inventory names,
verifies every quotation against its source, and writes the topic, its passages,
packets, contradictions and cross-links. It also rewrites the Bible dictionary
entry and promotes three biblical terms the dossier links to.

Shares its extraction and verification code with the Burroughs seeder, so both
dossiers are held to the same standard. Idempotent. Registered in build_all.py
stage 5, before export_studies.

Usage:
    python scripts/studies/seed_pkd_bible.py
    python scripts/studies/seed_pkd_bible.py --check
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
    QUOTED, STUDY_DESCRIPTION, STUDY_ID, STUDY_LABEL, _source_corpus,
    ensure_schema, normalise, tidy, window,
)

PROJECT_DIR = HERE.parent.parent
DEFAULT_DB = PROJECT_DIR / 'database' / 'unified.sqlite'
CURATION = PROJECT_DIR / 'curation' / 'pkd-bible'
sys.path.insert(0, str(CURATION))

TOPIC_ID = 'TOPIC_INTERTEXT_pkd_and_the_bible'
TOPIC_SLUG = 'pkd-and-the-bible'
TOPIC_NAME = 'Philip K. Dick and the Bible'

GENERATOR = 'curation/pkd-bible@2026-10-29'
PROVENANCE = 'editorial_curation_from_corpus_evidence'

RELATED_TERMS = [
    ('TERM_bible', 'primary'),
    ('TERM_acts', 'subsumes'), ('TERM_daniel', 'subsumes'),
    ('TERM_revelation', 'subsumes'), ('TERM_malachi', 'subsumes'),
    ('TERM_torah', 'subsumes'), ('TERM_wisdom', 'subsumes'),
    ('TERM_john', 'subsumes'), ('TERM_gospel', 'subsumes'),
    ('TERM_elijah', 'related'), ('TERM_hagia-sophia', 'related'),
    ('TERM_logos', 'related'), ('TERM_paul', 'related'), ('TERM_moses', 'related'),
    ('TERM_qumran', 'related'), ('TERM_plasmate', 'related'),
    ('TERM_empire', 'related'), ('TERM_black-iron-prison', 'related'),
    ('TERM_king-felix', 'related'), ('TERM_parousia', 'related'),
    ('TERM_paraclete', 'related'), ('TERM_holy-spirit', 'related'),
    ('TERM_gnosticism', 'contrasts'),
]

RELATED_NAMES = [
    ('NAME_elijah', 'prophet_of_malachi'), ('NAME_elias-tate', 'elijah_in_fiction'),
    ('NAME_malachi', 'prophet'), ('NAME_daniel', 'prophet'),
    ('NAME_moses', 'yhwh_of_moses'), ('NAME_yhwh', 'which_god'),
    ('NAME_paul', 'author_of_1_corinthians'), ('NAME_philo', 'living_torah'),
    ('NAME_father-rasch', 'identified_acts_parallel'),
    ('NAME_felix-buckman', 'felix_of_acts'), ('NAME_jason-taverner', 'jason_of_acts'),
    ('NAME_thomas', 'apostolic_christian'), ('NAME_julian-jaynes', 'correspondent'),
    ('NAME_horselover-fat', 'fictional_exegete'), ('NAME_kevin', 'reads_daniel'),
    ('NAME_emmanuel', 'reads_holographic_bible'), ('NAME_timothy-archer', 'misuses_scripture'),
    ('NAME_sophia', 'holy_wisdom'),
]

# The Bible's own dictionary entry: the definition the old machine draft lacked,
# and the related terms it should have had instead of co-occurring function words.
TERM_BIBLE = {
    'card_description': (
        "The text Dick argued with longest: known since junior high, read after 1974 "
        "as a book of the future, a code, and a living organism."),
    'definition': (
        "The scriptures of Judaism and Christianity, which Philip K. Dick read in at "
        "least five translations — King James, the Jehovah's Witnesses' New World "
        "Translation, the New English Bible, the Jerusalem Bible and the Vulgate — "
        "together with the Septuagint's apocrypha. Familiar to him from junior high, "
        "and the source of the title of A Scanner Darkly (1 Corinthians 13:12), it "
        "became after 1974 the main framework of the Exegesis."),
    'interpretive_note': (
        "Dick read the Bible in four incompatible ways and never chose between them: "
        "as a book of the future (\"The Bible is a book of the future\", February "
        "1975); as a cipher describing the present (\"The Bible is code\", 1976–79); "
        "as a living organism, Philo's Torah and the plasmate (1978–80); and as a "
        "source his own novels had reproduced without his knowing — Acts in Flow My "
        "Tears. The books that do most work are Acts, Daniel, Revelation, Malachi, "
        "the Wisdom of Solomon, John and 1 Corinthians."),
    'scholarly_caution': (
        "Dick's own statements about his prior knowledge conflict. In 1976 he wrote "
        "that in 1974 he was \"almost totally unfamiliar with the Bible\"; his "
        "letters of 1962–73 quote it, title a novel from it, and compare its "
        "translations. Treat claims that the 1974 visions were independent of his "
        "reading with caution. The Exegesis section dated October 1978 contains "
        "passages from as late as 1980."),
    'see_also': ['Acts', 'Daniel', 'Revelation', 'Malachi', 'Elijah', 'Torah',
                 'Wisdom', 'Hagia Sophia', 'Logos', 'John', 'Paul', 'Qumran'],
    'related': ['TERM_acts', 'TERM_daniel', 'TERM_revelation', 'TERM_malachi',
                'TERM_elijah', 'TERM_torah', 'TERM_wisdom', 'TERM_hagia-sophia',
                'TERM_logos', 'TERM_john', 'TERM_paul', 'TERM_gospel', 'TERM_moses',
                'TERM_qumran', 'TERM_plasmate', 'TERM_empire', 'TERM_black-iron-prison',
                'TERM_king-felix', 'TERM_parousia', 'TERM_paraclete',
                'TERM_holy-spirit', 'TERM_gnosticism', 'TERM_christ', 'TERM_jesus'],
    'aliases': ['Scripture', 'Scriptures', 'Old Testament', 'New Testament',
                'Holy Bible'],
}

# Biblical terms the dossier's facets link to, which were background-only
# (no public page). Each gets a short reviewed entry pointing at the dossier.
PROMOTED_TERMS = {
    'TERM_revelation': {
        'card_description': (
            "The Book of Revelation, which Dick read with Daniel as a description of "
            "the present Empire."),
        'definition': (
            "The Book of Revelation, the last book of the New Testament. Dick paired "
            "it with Daniel as \"the two apocalyptic books of the Bible\", identified "
            "its beast with Rome and the Empire he believed fell in 1974, and read "
            "the old king on horseback of the Flow My Tears dream as Revelation's "
            "risen judge."),
        'see_also': ['Bible', 'Daniel', 'Empire', 'Parousia', 'Black Iron Prison'],
    },
    'TERM_malachi': {
        'card_description': (
            "The last Old Testament prophet, whose promise of Elijah's return Dick "
            "used to name what possessed him."),
        'definition': (
            "The Book of Malachi, the last book of the Christian Old Testament, which "
            "promises that Elijah will be sent before the day of the Lord and that "
            "the sun of righteousness will rise with healing in its wings. Dick "
            "equated Malachi's returning Spirit of Elijah with the Christian Holy "
            "Spirit, and quotes the healing verse in the Exegesis and in VALIS."),
        'see_also': ['Bible', 'Elijah', 'Holy Spirit', 'Paraclete'],
    },
    'TERM_qumran': {
        'card_description': (
            "The site of the Dead Sea Scrolls, which Dick imagined as carriers of "
            "living information."),
        'definition': (
            "Qumran, the site of the Dead Sea Scrolls. Dick's 1975 novel outline To "
            "Scare the Dead has an Essene from the Qumran wadi revive in a modern "
            "man; in the Exegesis Thomas slumbers \"in a jar at Qumran\" and the "
            "scrolls Bishop James Pike studied pass to Dick as plasmate. The "
            "Zadokite fragments drive the plot of The Transmigration of Timothy "
            "Archer."),
        'see_also': ['Bible', 'Plasmate', 'Thomas', 'Gnosticism'],
    },
}


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
    from dossier_sections import group_of  # curation/pkd-bible

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

    db.execute("""
        INSERT INTO studies (study_id, study_label, study_description, topic_count)
        VALUES (?, ?, ?, 1)
        ON CONFLICT(study_id) DO UPDATE SET
            study_label = excluded.study_label,
            study_description = excluded.study_description,
            updated_at = CURRENT_TIMESTAMP
    """, (STUDY_ID, STUDY_LABEL, STUDY_DESCRIPTION))

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
            first_appearance = '1962', peak_period_start = '1975',
            peak_period_end = '1981', related_topics = ?, provenance = ?, notes = ?,
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
          json.dumps(['burroughs-word-virus']), PROVENANCE, GENERATOR,
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

    # Dictionary entries this topic owns. Promotions run first so the term links
    # below only ever point at terms with a public page.
    for term_id, t in PROMOTED_TERMS.items():
        db.execute("""
            UPDATE terms SET status = 'accepted', review_state = 'human-revised',
                primary_category = 'Biblical Text', card_description = ?,
                definition = ?, full_description = ?, see_also = ?,
                interpretive_note = NULL, scholarly_caution = NULL,
                visionary_significance = NULL, provenance = ?, noise_score = 0.0,
                definition_generator = ?, card_description_generator = ?,
                full_description_generator = ?,
                definition_claim_ids = '[]', card_description_claim_ids = '[]',
                full_description_claim_ids = '[]', interpretive_note_claim_ids = '[]',
                scholarly_caution_claim_ids = '[]', visionary_significance_claim_ids = '[]',
                updated_at = CURRENT_TIMESTAMP
            WHERE term_id = ?
        """, (t['card_description'], t['definition'], t['definition'],
              json.dumps(t['see_also']), PROVENANCE, GENERATOR, GENERATOR, GENERATOR,
              term_id))

    t = TERM_BIBLE
    db.execute("""
        UPDATE terms SET status = 'accepted', review_state = 'human-revised',
            primary_category = 'Biblical Text', card_description = ?, definition = ?,
            interpretive_note = ?, visionary_significance = NULL, scholarly_caution = ?,
            full_description = ?, see_also = ?, first_appearance = '1962',
            peak_usage_start = '1975', peak_usage_end = '1981', provenance = ?,
            noise_score = 0.0,
            definition_generator = ?, interpretive_note_generator = ?,
            scholarly_caution_generator = ?, card_description_generator = ?,
            full_description_generator = ?,
            definition_claim_ids = '[]', interpretive_note_claim_ids = '[]',
            scholarly_caution_claim_ids = '[]', card_description_claim_ids = '[]',
            full_description_claim_ids = '[]', visionary_significance_claim_ids = '[]',
            updated_at = CURRENT_TIMESTAMP
        WHERE term_id = 'TERM_bible'
    """, (t['card_description'], t['definition'], t['interpretive_note'],
          t['scholarly_caution'], t['definition'], json.dumps(t['see_also']),
          PROVENANCE, GENERATOR, GENERATOR, GENERATOR, GENERATOR, GENERATOR))
    for alias in t['aliases']:
        db.execute("INSERT OR IGNORE INTO term_aliases (term_id, alias_text, alias_type) "
                   "VALUES ('TERM_bible', ?, 'alternate_name')", (alias,))

    # Replace the Bible's co-occurrence links (Because, Like, Since ...) with the
    # curated set, in both directions.
    db.execute("DELETE FROM term_terms WHERE term_id_a = 'TERM_bible' OR term_id_b = 'TERM_bible'")
    for other in t['related']:
        if db.execute("SELECT 1 FROM terms WHERE term_id = ? AND status = 'accepted'",
                      (other,)).fetchone():
            db.execute("INSERT OR IGNORE INTO term_terms (term_id_a, term_id_b, relation_type, "
                       "strength, link_confidence, link_method) VALUES ('TERM_bible', ?, "
                       "'related', 1.0, 1, ?)", (other, GENERATOR))

    for term_id, rel in RELATED_TERMS:
        if db.execute("SELECT 1 FROM terms WHERE term_id = ? AND status = 'accepted'",
                      (term_id,)).fetchone():
            db.execute("INSERT OR REPLACE INTO study_topic_terms (topic_id, term_id, "
                       "relation_type) VALUES (?,?,?)", (TOPIC_ID, term_id, rel))
    for name_id, rel in RELATED_NAMES:
        if db.execute("SELECT 1 FROM names WHERE name_id = ?", (name_id,)).fetchone():
            db.execute("INSERT OR REPLACE INTO study_topic_names (topic_id, name_id, "
                       "relation_type) VALUES (?,?,?)", (TOPIC_ID, name_id, rel))

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
    print(f"  terms            TERM_bible rewritten; promoted "
          f"{', '.join(PROMOTED_TERMS)}")


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
    print("Seeding 'Philip K. Dick and the Bible' from curation/ ...")
    seed(db, check_only=args.check)
    db.close()
    if not args.check:
        print("Done. Now: python scripts/safeguard/safe_export.py --exporter studies")


if __name__ == '__main__':
    main()
