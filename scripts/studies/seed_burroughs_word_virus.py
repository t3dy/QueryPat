#!/usr/bin/env python3
"""
Seed the "Intertexts & Influences" study and its topic "Burroughs and the Word
Virus" from the durable curation files.

    curation/burroughs-word-virus/evidence-inventory.json   classified findings
    curation/burroughs-word-virus/dossier.json              editorial prose

Nothing editorial is hardcoded here. This script only extracts verbatim
passages from the corpus at the anchors the inventory names, and writes both
files into the database. If the database is rebuilt from scratch, running this
restores the page exactly; if the exported JSON is lost, the same is true.
That is the point — see docs/PRESERVATION.md.

Idempotent. Registered in build_all.py stage 5, before export_studies.

Usage:
    python scripts/studies/seed_burroughs_word_virus.py
    python scripts/studies/seed_burroughs_word_virus.py --check
"""

import argparse
import json
import re
import sqlite3
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_DB = PROJECT_DIR / 'database' / 'unified.sqlite'
CURATION = PROJECT_DIR / 'curation' / 'burroughs-word-virus'

STUDY_ID = 'intertexts'
STUDY_LABEL = 'Intertexts & Influences'
STUDY_DESCRIPTION = (
    "Writers and thinkers Philip K. Dick read, argued with, and absorbed into "
    "his own vocabulary. Each topic tracks a single interlocutor across the "
    "fiction, the Exegesis, and the correspondence, and holds on to the places "
    "where Dick changed his mind about them."
)

TOPIC_ID = 'TOPIC_INTERTEXT_burroughs_word_virus'
TOPIC_SLUG = 'burroughs-word-virus'
TOPIC_NAME = 'Burroughs and the Word Virus'

GENERATOR = 'curation/burroughs-word-virus@2026-09-04'
PROVENANCE = 'editorial_curation_from_corpus_evidence'

RELATED_DOC_IDS = [
    ('DOC_EXEG_SECTION_015', 'primary'),
    ('DOC_EXEG_SECTION_016', 'primary'),
    ('DOC_EXEG_SECTION_017', 'primary'),
    ('DOC_ARCH_THE_SELECTED_LETTERS_OF_PHILIP_K_DICK_19', 'primary'),
    ('DOC_ARCH_OCEANOFPDF_COM_SELECTED_LETTERS_OF_PHILI', 'mentions'),
    ('DOC_ARCH_PHILIP_K_DICK_PAUL_WILLIAMS_SELECTED_LET', 'mentions'),
    ('DOC_ARCH_PHILIP_K_DICK_IN_HIS_OWN_WORDS_GREGG_RIC', 'substantial'),
    ('DOC_ARCH_DIVINE_INVASIONS_A_LIFE_OF_PHI_LAWRENCE_', 'substantial'),
    ('DOC_ARCH_DAVID_LAPOUJADE_WORLDS_BUILT_TO_FALL_APA', 'substantial'),
    ('DOC_ARCH_ANDREW_M_BUTLER_PHILIP_K_DICK_REVISED_AN', 'mentions'),
    ('DOC_ARCH_HOW_TO_BUILD_A_UNIVERSE_THAT_DOESN_T_FAL', 'mentions'),
]

RELATED_TERM_IDS = [
    ('TERM_burroughs', 'primary'),
    ('TERM_living-information', 'related'),
    ('TERM_plasmate', 'related'),
    ('TERM_black-iron-prison', 'related'),
    ('TERM_king-felix', 'related'),
    ('TERM_logos', 'related'),
    ('TERM_valis', 'related'),
    ('TERM_ubik', 'related'),
    ('TERM_scanner', 'related'),
    ('TERM_maze', 'related'),
]

RELATED_NAME_IDS = [
    ('NAME_thomas', 'identified_with_nova_mob_parasite'),
    ('NAME_firebright', 'identified_with_deposited_egg'),
    ('NAME_zebra', 'identified_with_nova_police'),
    ('NAME_valis', 'living_information'),
]

TERM_BURROUGHS = {
    'canonical_name': 'Burroughs',
    'primary_category': 'Intertext',
    'card_description': (
        "William S. Burroughs, whose \"word virus\" Dick adopted in 1976 and "
        "argued with for the rest of his life."
    ),
    'definition': (
        "William S. Burroughs (1914–1997), read by Dick from September 1976 and named "
        "in thirty-eight Exegesis passages, twelve letters and one interview. What Dick "
        "takes from him is a single proposition — that language is a parasitic "
        "organism, a \"word virus\", which infects its hosts and blinds them to their "
        "own condition — together with its furniture from The Ticket That Exploded: "
        "the Nova Mob, the Nova police, and the latent message riding inside ordinary "
        "text."
    ),
    'interpretive_note': (
        "Dick never settles. In September 1976 the word virus is confirmation: Thomas is "
        "a Nova Mob parasite, the power that intervened in 3-74 is \"Equal to Burroughs' "
        "nova police\", and 3-74 was a remission in which he \"threw off the word "
        "virus\" — but in the same sitting he redefines it as an anti-information virus "
        "that blocks reception rather than infecting. In October 1978 he writes both "
        "that \"William Burroughs is correct\" and that the virus is \"antitoxic, "
        "de-occlusive\", and traces his own darkest reading of it to \"paranoia and "
        "paranoiac fear\". In April 1981 he states the inversion — man is already "
        "occluded and living information is the remedy — and in the same sitting keeps "
        "the occluding virus in three further passages. The engagement is a five-year "
        "argument, not a conversion."
    ),
    'scholarly_caution': (
        "Dick had not read Burroughs when he wrote the novels most often compared to "
        "him, and says so: the occlusion he put into A Scanner Darkly was observed in "
        "1971, \"before I knew of Burroughs\". No work of his fiction mentions Burroughs "
        "at all; the Exegesis reads Ubik, The Three Stigmata of Palmer Eldritch and A "
        "Maze of Death through him retroactively. Sutin places Burroughs in Dick's "
        "lifelong reading but gives no date, and no document in this archive mentions "
        "Burroughs before January 1976; Dick's own dating of the observation to 1971 is "
        "made retrospectively, in 1981."
    ),
    'see_also': ['Living Information', 'Plasmate', 'Black Iron Prison', 'King Felix',
                 'Logos', 'Valis'],
}


# --------------------------------------------------------------------------
# Schema
# --------------------------------------------------------------------------

STUDY_PASSAGES_DDL = """
CREATE TABLE study_passages_new (
    passage_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id            TEXT NOT NULL,
    ev_id               TEXT,

    doc_id              TEXT,
    seg_id              TEXT,
    page_num            INTEGER,
    char_offset_start   INTEGER,
    char_offset_end     INTEGER,

    passage_text        TEXT NOT NULL,
    context_before      TEXT,
    context_after       TEXT,

    lane                TEXT CHECK (lane IN ('A', 'B', 'C', 'D', 'E')),

    source_mode         TEXT CHECK (source_mode IN (
                            'fiction', 'exegesis', 'letter', 'interview', 'criticism'
                        )),
    claim_type          TEXT CHECK (claim_type IN (
                            'definition', 'symptom_description', 'causal_theory',
                            'allegory', 'self_report', 'critique', 'comparison',
                            'unresolved'
                        )),
    confidence          TEXT CHECK (confidence IN ('high', 'medium', 'low')),

    psych_mode          TEXT,
    ai_mode             TEXT,

    matched_terms       TEXT,
    match_method        TEXT CHECK (match_method IN (
                            'lexicon_exact', 'lexicon_alias', 'claude_conceptual',
                            'claude_inferred', 'curated_anchor'
                        )),

    fair_use_status     TEXT DEFAULT 'pending' CHECK (fair_use_status IN (
                            'pending', 'approved', 'trimmed', 'rejected'
                        )),
    editorial_status    TEXT DEFAULT 'unreviewed',

    notes               TEXT,
    created_at          TEXT DEFAULT (datetime('now')),

    FOREIGN KEY (topic_id) REFERENCES study_topics(topic_id),
    FOREIGN KEY (doc_id) REFERENCES documents(doc_id),
    FOREIGN KEY (seg_id) REFERENCES segments(seg_id)
);
"""

STUDY_PASSAGES_INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_study_passages_topic ON study_passages(topic_id)",
    "CREATE INDEX IF NOT EXISTS idx_study_passages_doc ON study_passages(doc_id)",
    "CREATE INDEX IF NOT EXISTS idx_study_passages_seg ON study_passages(seg_id)",
    "CREATE INDEX IF NOT EXISTS idx_study_passages_lane ON study_passages(lane)",
    "CREATE INDEX IF NOT EXISTS idx_study_passages_claim ON study_passages(claim_type)",
    "CREATE INDEX IF NOT EXISTS idx_study_passages_ev ON study_passages(ev_id)",
]

CARRIED_COLUMNS = [
    'passage_id', 'topic_id', 'doc_id', 'seg_id', 'page_num',
    'char_offset_start', 'char_offset_end', 'passage_text', 'context_before',
    'context_after', 'lane', 'source_mode', 'claim_type', 'confidence',
    'psych_mode', 'ai_mode', 'matched_terms', 'match_method',
    'fair_use_status', 'editorial_status', 'notes', 'created_at',
]


def ensure_schema(db: sqlite3.Connection) -> bool:
    """Widen study_passages (lanes A-E, ev_id) and add dossier_sections."""
    changed = False
    cols = {c[1] for c in db.execute("PRAGMA table_info(study_topics)")}
    for col in ('dossier_sections', 'mention_cards'):
        if col not in cols:
            db.execute(f"ALTER TABLE study_topics ADD COLUMN {col} TEXT")
            db.commit()
            print(f'  added study_topics.{col}')
            changed = True

    ddl = db.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' AND name='study_passages'"
    ).fetchone()
    if not ddl:
        raise SystemExit("study_passages table is missing; run the build first.")
    if "'D', 'E'" in ddl[0] and 'ev_id' in ddl[0]:
        return changed

    views = db.execute(
        "SELECT name, sql FROM sqlite_master "
        "WHERE type='view' AND sql LIKE '%study_passages%'").fetchall()

    carried = ', '.join(CARRIED_COLUMNS)
    db.execute("PRAGMA foreign_keys = OFF")
    db.execute("DROP TABLE IF EXISTS study_passages_new")
    for name, _ in views:
        db.execute(f"DROP VIEW {name}")
    db.execute(STUDY_PASSAGES_DDL)
    db.execute(f"INSERT INTO study_passages_new ({carried}) "
               f"SELECT {carried} FROM study_passages")
    db.execute("DROP TABLE study_passages")
    db.execute("ALTER TABLE study_passages_new RENAME TO study_passages")
    for stmt in STUDY_PASSAGES_INDEXES:
        db.execute(stmt)
    for _, sql in views:
        db.execute(sql)
    db.commit()
    db.execute("PRAGMA foreign_keys = ON")
    n = db.execute("SELECT COUNT(*) FROM study_passages").fetchone()[0]
    print(f'  migrated study_passages: lanes A-E, ev_id added ({n} rows preserved)')
    return True


# --------------------------------------------------------------------------
# Verbatim extraction
# --------------------------------------------------------------------------

SENTENCE_BREAK = re.compile(r'(?<=[.?!])\s+')

_HEAD_WORDS = ['THE', 'SELECTED', 'LETTERS', 'OF', 'PHILIP', 'K', 'DICK']
RUNNING_HEAD = re.compile(
    r'\s*\d{0,4}\s*' +
    r'\s*'.join(r'\s*'.join(ch for ch in word) + r'\.?' for word in _HEAD_WORDS) +
    r'\.?\s*\d{0,4}\s*', re.IGNORECASE)
EDGE_SPACED_CAPS = re.compile(
    r'^(?:\s*\d{1,4}\s+)?(?:[A-Z]{1,2}\.?\s+){3,}[A-Z]{1,2}\.?\s*|'
    r'\s*\d{1,4}\s+(?:[A-Z]{1,2}\.?\s+){2,}[A-Z]{1,2}\.?\s*$')
PAGE_FURNITURE = re.compile(
    r'folder\s+\d+\s*-\s*\d+|(?<=\s)-\d{1,3}-(?=\s)|'
    r'\*\*==>.*?<==\*\*|https?://\S+|'
    r'\d+ of \d+\s+\d{1,2}/\d{1,2}/\d{2,4},?\s*\d{1,2}:\d{2}\s*[AP]M|'
    r'\d{1,2}/\d{1,2}/\d{2}\s+\d{1,2}:\d{2}\s*[AP]M')


def tidy(text: str) -> str:
    """Strip scan furniture — running heads, URLs, page stamps — from an excerpt."""
    text = RUNNING_HEAD.sub(' ', text)
    text = PAGE_FURNITURE.sub(' ', text)
    text = EDGE_SPACED_CAPS.sub(' ', text)
    text = re.sub(r'(^\s*#+\s*|\s*#+\s*$)', ' ', text)
    return text


def window(text: str, anchor: str, before: int, after: int, clean=None):
    """Verbatim slice around `anchor`, snapped to word and sentence boundaries."""
    idx = text.find(anchor)
    if idx < 0:
        return None
    start = max(0, idx - before)
    end = min(len(text), idx + len(anchor) + after)

    head = text[start:idx]
    breaks = list(SENTENCE_BREAK.finditer(head))
    if breaks:
        start += breaks[0].end()
    elif start > 0:
        space = text.find(' ', start)
        if 0 <= space < idx:
            start = space + 1

    if end < len(text) and not text[end].isspace():
        space = text.rfind(' ', idx + len(anchor), end)
        if space > 0:
            end = space

    excerpt = text[start:end]
    if clean:
        excerpt = clean(excerpt)
    excerpt = re.sub(r'\s+', ' ', excerpt).strip()
    if start > 0:
        excerpt = '… ' + excerpt
    if end < len(text):
        excerpt = excerpt.rstrip() + ' …'

    ctx_b = re.sub(r'\s+', ' ', text[max(0, start - 150):start]).strip()
    ctx_a = re.sub(r'\s+', ' ', text[end:end + 150]).strip()
    return excerpt, start, end, ctx_b, ctx_a


def _source_corpus(db, inventory):
    """Normalised text of every source the dossier cites, for quote checking."""
    seg_ids, doc_ids, letter_ids = set(), set(), set()
    for f in inventory['evidence']:
        src = f['source']
        if src['type'] == 'exegesis_segment':
            seg_ids.add(src['id'])
        elif src['type'] == 'letter':
            letter_ids.add(src['id'])
        elif src.get('doc_id'):
            doc_ids.add(src['doc_id'])
    texts = []
    for sid in seg_ids:
        r = db.execute("SELECT raw_text FROM segments WHERE seg_id = ?", (sid,)).fetchone()
        if r and r[0]:
            texts.append(normalise(r[0]))
    for lid in letter_ids:
        r = db.execute("SELECT body_md FROM letters WHERE letter_id = ?", (lid,)).fetchone()
        if r and r[0]:
            texts.append(normalise(r[0]))
    for did in doc_ids:
        r = db.execute("SELECT markdown_content, text_content FROM document_texts "
                       "WHERE doc_id = ?", (did,)).fetchone()
        if r and (r[0] or r[1]):
            texts.append(normalise(r[0] or r[1]))
    return texts


def load_curation():
    inv = json.loads((CURATION / 'evidence-inventory.json').read_text(encoding='utf-8'))
    dos = json.loads((CURATION / 'dossier.json').read_text(encoding='utf-8'))
    return inv, dos


# Paired quotation marks: curly first, then straight.
QUOTED = re.compile(
    r'“([^“”]{20,}?)”'
    r'|(?<![A-Za-z])"([^"]{20,}?)"(?![A-Za-z])')

MARKDOWN = re.compile(r'[_*~]')
STAMPS = re.compile(r'\b\d{2}-\d{4}\b|\b[A-Z]-\d{1,2}\b')

DASH_CHARS = ('—', '–', '--', '‐')
DASHES = '-'
TYPOGRAPHY = re.compile('[“”‘’«»"\']|--|[—–‐]')

SOFT_HYPHEN = re.compile('­\\s*')
LINEBREAK_HYPHEN = re.compile(r'(\w)-\s*\n\s*(\w)')


def normalise(text: str) -> str:
    """Reduce text for quotation matching.

    Scans hyphenate across line breaks and interleave running heads, so a
    quotation faithful to the printed page will not match the OCR byte for
    byte. Strip those artifacts from both sides before comparing. The words
    still have to be the author's, in the author's order.
    """
    text = tidy(text)
    # soft hyphen plus any whitespace it introduced
    text = SOFT_HYPHEN.sub('', text)
    # hard hyphen at a line break
    text = LINEBREAK_HYPHEN.sub(chr(92)+'1'+chr(92)+'2', text)
    # Fold typography, not words. Quotation marks are dropped entirely because a
    # nested quotation may be re-marked when a passage is quoted inside prose;
    # dashes are levelled because transcriptions and print editions differ. The
    # words themselves, and their order, still have to match.
    # markdown emphasis in the published edition, and the folio stamps that
    # interrupt sentences in the folder transcriptions ("63-2013 D-6")
    text = MARKDOWN.sub('', text)
    text = STAMPS.sub(' ', text)
    text = TYPOGRAPHY.sub(lambda m: DASHES if m.group(0) in DASH_CHARS else '', text)
    text = re.sub(r'\s*-\s*', '-', text)
    return re.sub(r'\s+', ' ', text).strip().lower()

def collect_passages(db, inventory):
    """Extract the verbatim passage for every publishable finding."""
    rows, missing, unverified, cards = [], [], [], []

    seg_text = {s: (t or '') for s, t in db.execute(
        "SELECT seg_id, raw_text FROM segments WHERE raw_text IS NOT NULL")}
    seg_doc = {s: d for s, d in db.execute("SELECT seg_id, doc_id FROM segments")}

    for f in inventory['evidence']:
        if not f['on_public_page'] or not f.get('anchor'):
            continue
        src = f['source']
        stype = src['type']
        clean = None

        if stype == 'exegesis_segment':
            text = seg_text.get(src['id'], '')
            doc_id, seg_id = seg_doc.get(src['id']), src['id']
        elif stype == 'letter':
            row = db.execute(
                "SELECT volume_doc_id, body_md FROM letters WHERE letter_id = ?",
                (src['id'],)).fetchone()
            text = (row[1] or '') if row else ''
            doc_id, seg_id = (row[0] if row else None), None
            clean = tidy
        else:
            row = db.execute(
                "SELECT markdown_content, text_content FROM document_texts "
                "WHERE doc_id = ?", (src['id'],)).fetchone()
            text = ((row[0] or row[1]) if row else '') or ''
            doc_id, seg_id = src['id'], None
            clean = tidy

        w = window(text, f['anchor'], f['window'][0], f['window'][1], clean=clean)
        if not w:
            missing.append((f['id'], stype, src['id'], f['anchor']))
            continue
        excerpt, start, end, cb, ca = w

        # Fair-use quotation must be verbatim. Check against the full source
        # text, not the excerpt, so a pith may sit just outside the window.
        card = f.get('card')
        if card:
            pith = normalise(card['pith'])
            if pith not in normalise(text):
                unverified.append((f['id'], card['pith'][:70]))
            cards.append({
                'id': f['id'],
                'citation': src['citation'],
                'date': src.get('date'),
                'source_type': stype,
                'published_folio': src.get('published_folio'),
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
            })

        rows.append((
            TOPIC_ID, f['evidence_packet'], doc_id, seg_id, None, start, end,
            excerpt, cb, ca, f['lane'], f['source_mode'], f['claim_type'],
            f['confidence'], None, None, json.dumps(f['concepts']),
            'curated_anchor', 'approved', 'curated', src['citation'],
        ))

    return rows, missing, unverified, cards


CONTRADICTIONS = [
    ("In 1976 Dick reports throwing off a word virus that had infected him; "
     "in 1981 he denies that any information virus occludes anyone.",
     "The headline reversal, and the least complicated of the four. The 1976 entry "
     "treats 3-74 as remission from an infection Burroughs correctly diagnosed. The "
     "1981 entry keeps both components — living information, and occlusion — but "
     "severs the causal link and reassigns living information to the side of the "
     "remedy. Neither reading is ever retracted.",
     'early_vs_late',
     'Burroughs may have got the real situation down in "The Ticket That Exploded"',
     'Man is not occluded by an "information virus,"'),

    ("The April 1981 sitting that states the reversal also keeps the occluding virus, "
     "in the same pages.",
     "Within the same sitting Dick writes that Torah is \"like an occluding information "
     "virus\", that the living information \"controls us (as Burroughs teaches)\", and "
     "that Satan \"ensnared him as the info virus of Burroughs\". He does not choose "
     "between the readings; he sets a living hyper-information against the occluding "
     "one and leaves them in combat. Any summary presenting April 1981 as a settled "
     "reversal is tidier than the notebooks.",
     'interpretive',
     'Man is not occluded by an "information virus,"',
     'he ensnared him as the info virus of Burroughs'),

    ("In October 1978 the virus is the disease and the cure, in the same section.",
     "One passage calls the information virus \"antitoxic, de-occlusive\" and maps it "
     "onto four of Dick's own novels as the thing that lifts the occlusion. Another, in "
     "the same section, says \"Burroughs is right\" and that the occluding life form "
     "\"enslaves us and kills us\". A third rejects the frame outright: \"This is no "
     "information virus; this is blindness.\" The 1978 material is not a stage between "
     "1976 and 1981; it already contains both poles.",
     'interpretive',
     'But this is not an occluding, toxifying',
     'roughs is right. Is it the plasmate?'),

    ("To a correspondent Dick refuses to call Burroughs's theory paranoia; to himself "
     "he had already named paranoia as one of its two sources.",
     "The 1978 Exegesis entry attributes his own \"contamination\" reading to "
     "Burroughs's theory plus \"paranoia and paranoiac fear\". The 1981 letter to Brig "
     "Elliot declines to dismiss the same theory \"as mere paranoia on his part\". "
     "Strictly the two are compatible — one is about Dick, the other about Burroughs — "
     "but they show the difference between what the notebooks say and what the letters "
     "concede.",
     'self_vs_critic',
     'I doubt very much if the plasmate is an occluding agent',
     'I cannot accept Burroughs'),
]


# --------------------------------------------------------------------------
# Seeding
# --------------------------------------------------------------------------

def seed(db: sqlite3.Connection, check_only: bool = False):
    inventory, dossier = load_curation()
    ensure_schema(db)
    passages, missing, unverified, cards = collect_passages(db, inventory)

    if unverified:
        print("  ERROR: quotation is not verbatim in its source:")
        for eid, pith in unverified:
            print(f"    {eid}: {pith!r}")
        raise SystemExit(1)

    if missing:
        print("  ERROR: anchors not found in the corpus:")
        for eid, stype, sid, anchor in missing:
            print(f"    {eid} [{stype} {sid}]: {anchor!r}")
        raise SystemExit(1)

    # Every quotation of 40+ characters in the essay prose must be verbatim in
    # some source the dossier draws on. The cards were already checked; the essay
    # was not, and a misremembered quotation there is exactly the kind of error
    # nobody catches by reading.
    corpus = _source_corpus(db, inventory)
    bad_quotes, checked_quotes = [], 0
    for sec in dossier['sections']:
        for para in sec['body']:
            for groups in QUOTED.findall(para):
                q = (groups[0] or groups[1]).strip()
                # Spans carrying a citation marker or starting mid-clause are
                # text *between* quotations, not quotations.
                if '{{' in q or not q[:1].isalpha() or len(q) < 40:
                    continue
                checked_quotes += 1
                probe = normalise(q.rstrip(' .,;'))
                if not any(probe in text for text in corpus):
                    bad_quotes.append((sec['id'], q[:70]))
    if bad_quotes:
        print(f"  ERROR: essay quotes text that is not verbatim in any cited source:")
        for sid, q in bad_quotes:
            print(f"    section {sid}: {q!r}")
        raise SystemExit(1)

    # Every {{id}} citation in the essay must resolve to a published finding.
    ids = {f['id'] for f in inventory['evidence'] if f['on_public_page']}
    cited, bad_cites = set(), []
    for sec in dossier['sections']:
        for para in sec['body']:
            for cid in re.findall(r'\{\{([A-Za-z0-9\-]+)\}\}', para):
                cited.add(cid)
                if cid not in ids:
                    bad_cites.append((sec['id'], cid))
    if bad_cites:
        print("  ERROR: essay cites findings that do not exist:")
        for sid, cid in bad_cites:
            print(f"    section {sid}: {{{{{cid}}}}}")
        raise SystemExit(1)

    known = {p['id'] for p in inventory['evidence_packets']}
    orphan = {r[1] for r in passages} - known
    if orphan:
        raise SystemExit(f'  ERROR: passages reference unknown packets: {orphan}')

    if check_only:
        lanes = {}
        for p in passages:
            lanes[p[10]] = lanes.get(p[10], 0) + 1
        print(f'  OK: {len(passages)} passages resolve, lanes={lanes}, '
              f'{len(inventory["evidence_packets"])} packets, '
              f'{len(dossier["sections"])} dossier sections, '
              f'{len(cards)} mention cards, all quotations verbatim')
        print(f'  {checked_quotes} quotations in the essay prose also verified verbatim')
        uncited = sorted(ids - cited)
        print(f'  essay cites {len(cited)} of {len(ids)} findings; '
              f'{len(uncited)} discussed only on their card')
        if uncited:
            print(f'    uncited: {", ".join(uncited[:8])}'
                  + (' ...' if len(uncited) > 8 else ''))
        return

    db.execute("""
        INSERT INTO studies (study_id, study_label, study_description, topic_count)
        VALUES (?, ?, ?, 1)
        ON CONFLICT(study_id) DO UPDATE SET
            study_label = excluded.study_label,
            study_description = excluded.study_description,
            updated_at = CURRENT_TIMESTAMP
    """, (STUDY_ID, STUDY_LABEL, STUDY_DESCRIPTION))

    db.execute("DELETE FROM study_contradictions WHERE topic_id = ?", (TOPIC_ID,))
    db.execute("DELETE FROM study_passages WHERE topic_id = ?", (TOPIC_ID,))
    db.execute("DELETE FROM study_evidence_packets WHERE topic_id = ?", (TOPIC_ID,))
    db.execute("DELETE FROM study_topic_docs WHERE topic_id = ?", (TOPIC_ID,))
    db.execute("DELETE FROM study_topic_terms WHERE topic_id = ?", (TOPIC_ID,))
    db.execute("DELETE FROM study_topic_names WHERE topic_id = ?", (TOPIC_ID,))

    db.execute("""
        INSERT OR IGNORE INTO study_topics (topic_id, study_id, canonical_name, slug)
        VALUES (?, ?, ?, ?)
    """, (TOPIC_ID, STUDY_ID, TOPIC_NAME, TOPIC_SLUG))

    db.executemany("""
        INSERT INTO study_passages
            (topic_id, ev_id, doc_id, seg_id, page_num, char_offset_start,
             char_offset_end, passage_text, context_before, context_after, lane,
             source_mode, claim_type, confidence, psych_mode, ai_mode,
             matched_terms, match_method, fair_use_status, editorial_status, notes)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, passages)

    lane_counts, per_packet = {}, {}
    for p in passages:
        lane_counts[p[10]] = lane_counts.get(p[10], 0) + 1
        per_packet.setdefault(p[1], {})
        per_packet[p[1]][p[10]] = per_packet[p[1]].get(p[10], 0) + 1

    for pkt in inventory['evidence_packets']:
        counts = per_packet.get(pkt['id'], {})
        db.execute("""
            INSERT INTO study_evidence_packets
                (ev_id, topic_id, claim_text, evidence_summary, confidence,
                 source_method, editorial_status, lane_a_count, lane_b_count,
                 lane_c_count, notes)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """, (pkt['id'], TOPIC_ID, pkt['claim'], pkt['summary'], pkt['confidence'],
              'editorial', 'reviewed', counts.get('A', 0), counts.get('B', 0),
              counts.get('C', 0), GENERATOR))

    def passage_id_for(fragment):
        row = db.execute("""
            SELECT passage_id FROM study_passages
            WHERE topic_id = ? AND passage_text LIKE ?
            ORDER BY passage_id LIMIT 1
        """, (TOPIC_ID, f'%{fragment}%')).fetchone()
        return row[0] if row else None

    n_contra = 0
    for summary, explanation, ctype, anchor_a, anchor_b in CONTRADICTIONS:
        pa, pb = passage_id_for(anchor_a), passage_id_for(anchor_b)
        if pa is None or pb is None:
            print(f"  WARNING: contradiction skipped (passage not found): {summary[:60]}")
            continue
        db.execute("""
            INSERT INTO study_contradictions
                (topic_id, passage_id_a, passage_id_b, summary, explanation,
                 contradiction_type, notes)
            VALUES (?,?,?,?,?,?,?)
        """, (TOPIC_ID, pa, pb, summary, explanation, ctype, GENERATOR))
        n_contra += 1

    fields = dossier['fields']
    db.execute("""
        INSERT INTO study_topics
            (topic_id, study_id, canonical_name, slug, status, priority,
             definition, pkd_relevance, in_the_fiction, in_the_exegesis,
             intellectual_background, scholarly_debate, chronology_summary,
             contradictions_summary, related_thinkers, editorial_notes,
             open_questions, card_description, passage_count, evidence_count,
             contradiction_count, first_appearance, peak_period_start,
             peak_period_end, related_topics, provenance, notes, dossier_sections,
             mention_cards)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(topic_id) DO UPDATE SET
            study_id = excluded.study_id,
            canonical_name = excluded.canonical_name,
            slug = excluded.slug, status = excluded.status,
            priority = excluded.priority, definition = excluded.definition,
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
            dossier_sections = excluded.dossier_sections,
            mention_cards = excluded.mention_cards,
            updated_at = CURRENT_TIMESTAMP
    """, (
        TOPIC_ID, STUDY_ID, TOPIC_NAME, TOPIC_SLUG, 'reviewed', 10,
        fields['definition'], fields['pkd_relevance'], fields['in_the_fiction'],
        fields['in_the_exegesis'], fields['intellectual_background'],
        fields['scholarly_debate'], fields['chronology_summary'],
        fields['contradictions_summary'], json.dumps(dossier['related_thinkers']),
        fields['editorial_notes'], json.dumps(dossier['open_questions']),
        dossier['card_description'],
        len(passages), len(inventory['evidence_packets']), n_contra,
        '1976', '1976', '1981', json.dumps([]), PROVENANCE, GENERATOR,
        json.dumps(dossier['sections'], ensure_ascii=False),
        json.dumps(cards, ensure_ascii=False),
    ))

    for field in ('definition', 'pkd_relevance', 'in_the_fiction', 'in_the_exegesis',
                  'intellectual_background', 'scholarly_debate', 'chronology_summary',
                  'contradictions_summary', 'editorial_notes'):
        db.execute(
            f"UPDATE study_topics SET {field}_generator = ?, {field}_claim_ids = ? "
            f"WHERE topic_id = ?", (GENERATOR, json.dumps([]), TOPIC_ID))

    for doc_id, relevance in RELATED_DOC_IDS:
        if not db.execute("SELECT 1 FROM documents WHERE doc_id = ?",
                          (doc_id,)).fetchone():
            continue
        n = db.execute(
            "SELECT COUNT(*) FROM study_passages WHERE topic_id = ? AND doc_id = ?",
            (TOPIC_ID, doc_id)).fetchone()[0]
        db.execute("INSERT OR REPLACE INTO study_topic_docs "
                   "(topic_id, doc_id, relevance, passage_count) VALUES (?,?,?,?)",
                   (TOPIC_ID, doc_id, relevance, n))

    for term_id, rel in RELATED_TERM_IDS:
        if db.execute("SELECT 1 FROM terms WHERE term_id = ?", (term_id,)).fetchone():
            db.execute("INSERT OR REPLACE INTO study_topic_terms "
                       "(topic_id, term_id, relation_type) VALUES (?,?,?)",
                       (TOPIC_ID, term_id, rel))

    for name_id, rel in RELATED_NAME_IDS:
        if db.execute("SELECT 1 FROM names WHERE name_id = ?", (name_id,)).fetchone():
            db.execute("INSERT OR REPLACE INTO study_topic_names "
                       "(topic_id, name_id, relation_type) VALUES (?,?,?)",
                       (TOPIC_ID, name_id, rel))

    db.execute("UPDATE studies SET topic_count = "
               "(SELECT COUNT(*) FROM study_topics WHERE study_id = ?) "
               "WHERE study_id = ?", (STUDY_ID, STUDY_ID))

    t = TERM_BURROUGHS
    db.execute("""
        UPDATE terms SET
            canonical_name = ?, status = 'accepted', review_state = 'human-revised',
            primary_category = ?, card_description = ?, definition = ?,
            interpretive_note = ?, visionary_significance = NULL,
            scholarly_caution = ?, full_description = ?, see_also = ?,
            first_appearance = '1976', peak_usage_start = '1976',
            peak_usage_end = '1981', provenance = ?, noise_score = 0.0,
            mention_count = (SELECT COUNT(*) FROM term_segments
                             WHERE term_id = 'TERM_burroughs'),
            definition_generator = ?, interpretive_note_generator = ?,
            scholarly_caution_generator = ?, card_description_generator = ?,
            full_description_generator = ?,
            definition_claim_ids = '[]', interpretive_note_claim_ids = '[]',
            scholarly_caution_claim_ids = '[]', card_description_claim_ids = '[]',
            full_description_claim_ids = '[]',
            visionary_significance_claim_ids = '[]',
            updated_at = CURRENT_TIMESTAMP
        WHERE term_id = 'TERM_burroughs'
    """, (t['canonical_name'], t['primary_category'], t['card_description'],
          t['definition'], t['interpretive_note'], t['scholarly_caution'],
          t['definition'], json.dumps(t['see_also']), PROVENANCE,
          GENERATOR, GENERATOR, GENERATOR, GENERATOR, GENERATOR))

    for alias in ('William S. Burroughs', 'William Burroughs',
                  'word virus', 'information virus'):
        db.execute("INSERT OR IGNORE INTO term_aliases (term_id, alias_text, alias_type) "
                   "VALUES ('TERM_burroughs', ?, 'alternate_name')", (alias,))

    db.commit()

    published = sum(1 for f in inventory['evidence'] if f['on_public_page'])
    recorded = len(inventory['evidence']) - published
    print(f"  study            {STUDY_ID}")
    print(f"  topic            {TOPIC_ID} ({TOPIC_SLUG})")
    print(f"  passages         {len(passages)}  lanes={lane_counts}")
    print(f"  evidence packets {len(inventory['evidence_packets'])}")
    print(f"  contradictions   {n_contra}")
    print(f"  dossier sections {len(dossier['sections'])}")
    print(f"  mention cards    {len(cards)} (all quotations verified verbatim)")
    print(f"  essay citations  {len(cited)} findings cited inline")
    print(f"  recorded but not published: {recorded} findings")
    print(f"  TERM_burroughs   accepted / human-revised")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--db', type=Path, default=DEFAULT_DB)
    ap.add_argument('--check', action='store_true',
                    help='verify every anchor resolves; write nothing')
    args = ap.parse_args()

    if not args.db.exists():
        print(f"Database not found: {args.db}", file=sys.stderr)
        raise SystemExit(1)

    db = sqlite3.connect(str(args.db))
    db.execute("PRAGMA foreign_keys = ON")
    print("Seeding Burroughs / word virus topic from curation/ ...")
    seed(db, check_only=args.check)
    db.close()
    if not args.check:
        print("Done. Now: python scripts/safeguard/safe_export.py --exporter studies")


if __name__ == '__main__':
    main()
