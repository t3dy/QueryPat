#!/usr/bin/env python3
"""
Build the relational religion database from the sweep, the taxonomy, the PDF
manifest and the editorial decisions.

    python scripts/research/build_religion_db.py

Inputs:
    curation/religion/taxonomy.py            topics, subsections, patterns
    curation/religion/raw-findings.json      the sweep (regenerable; not committed)
    curation/religion/pdf-manifest.json      staged archive documents
    curation/religion/editorial.json         editorial decisions, keyed by finding id (committed)

Output:
    curation/religion/religion.sqlite        derived; rebuilt every time; not committed

Schema (all keys are plain text or integer, so the file can be opened in any SQL tool):

    topics              one row per tradition
    subsections         one row per subsection, with its patterns as JSON
    sources             one row per corpus record (segment, chapter, letter, document)
    findings            one row per hit: lane, tier, date, decade, context, review state
    finding_subsections many-to-many: a finding can belong to several subsections
    findings_fts        full-text search over context and matched text (FTS5), if available
    v_subsection_lane   counts by subsection and lane
    v_subsection_decade counts by subsection and decade
    build_info          when and from what this database was built

Editorial relevance uses the Burroughs codes, so that the two studies can be
compared directly:

    1  direct engagement with the subject (names it, quotes it, argues about it)
    2  the subject used as a tool for another argument, or dramatised in fiction
    3  passing mention
    4  thematic parallel, no evidence of contact
    5  false positive: keyword match only
"""

import importlib.util
import json
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
CUR = PROJECT_DIR / 'curation' / 'religion'
RAW = CUR / 'raw-findings.json'
EDITORIAL = CUR / 'editorial.json'
MANIFEST = CUR / 'pdf-manifest.json'
DB = CUR / 'religion.sqlite'

SCHEMA = """
CREATE TABLE topics (
    topic_id     TEXT PRIMARY KEY,
    label        TEXT NOT NULL,
    description  TEXT,
    position     INTEGER NOT NULL,
    related      TEXT                     -- JSON array of topic ids
);
CREATE TABLE subsections (
    subsection_id TEXT PRIMARY KEY,
    topic_id      TEXT NOT NULL REFERENCES topics(topic_id),
    label         TEXT NOT NULL,
    description   TEXT,
    position      INTEGER NOT NULL,
    strong        TEXT,                   -- JSON array of patterns
    weak          TEXT,
    exclude       TEXT
);
CREATE TABLE sources (
    source_key   TEXT PRIMARY KEY,        -- corpus|source_id
    corpus       TEXT NOT NULL,
    source_id    TEXT,
    doc_id       TEXT,
    title        TEXT,
    author       TEXT,
    doc_type     TEXT,
    lane         TEXT NOT NULL,
    lane_assigned INTEGER NOT NULL DEFAULT 1,
    date         TEXT,
    date_display TEXT,
    file         TEXT
);
CREATE TABLE findings (
    finding_id    TEXT PRIMARY KEY,
    source_key    TEXT NOT NULL REFERENCES sources(source_key),
    field         TEXT,
    field_class   TEXT NOT NULL,
    lane          TEXT NOT NULL,
    char_offset   INTEGER,
    matched_text  TEXT NOT NULL,
    tier          TEXT NOT NULL,           -- strong if any pattern for its subsections is strong
    date          TEXT,
    decade        TEXT,
    context       TEXT NOT NULL,
    relevance     INTEGER,                 -- 1..5, NULL until reviewed
    review_status TEXT NOT NULL DEFAULT 'unreviewed',  -- unreviewed | reviewed | excluded
    editorial_note TEXT,
    reviewer      TEXT,
    reviewed_utc  TEXT
);
CREATE TABLE finding_subsections (
    finding_id    TEXT NOT NULL REFERENCES findings(finding_id),
    subsection_id TEXT NOT NULL REFERENCES subsections(subsection_id),
    tier          TEXT NOT NULL,
    PRIMARY KEY (finding_id, subsection_id)
);
CREATE INDEX idx_fs_sub ON finding_subsections(subsection_id);
CREATE INDEX idx_findings_lane ON findings(lane);
CREATE INDEX idx_findings_decade ON findings(decade);
CREATE INDEX idx_findings_source ON findings(source_key);
CREATE VIEW v_subsection_lane AS
    SELECT fs.subsection_id, f.lane, COUNT(*) AS n
    FROM finding_subsections fs JOIN findings f USING (finding_id)
    GROUP BY fs.subsection_id, f.lane;
CREATE VIEW v_subsection_decade AS
    SELECT fs.subsection_id, f.decade, COUNT(*) AS n
    FROM finding_subsections fs JOIN findings f USING (finding_id)
    WHERE f.decade IS NOT NULL
    GROUP BY fs.subsection_id, f.decade;
CREATE TABLE build_info (
    key   TEXT PRIMARY KEY,
    value TEXT
);
"""


def load_taxonomy():
    spec = importlib.util.spec_from_file_location('religion_taxonomy', CUR / 'taxonomy.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def decade_of(date):
    m = re.match(r'(\d{3})\d', date or '')
    return f'{m.group(1)}0s' if m else None


def main():
    if not RAW.exists():
        print(f'ERROR: {RAW.relative_to(PROJECT_DIR)} is missing. Run sweep_religion.py first.',
              file=sys.stderr)
        return 1
    tax = load_taxonomy()
    raw = json.loads(RAW.read_text(encoding='utf-8'))
    editorial = json.loads(EDITORIAL.read_text(encoding='utf-8')) if EDITORIAL.exists() else {}
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8')) if MANIFEST.exists() else {'documents': []}
    lanes_by_doc = {d['doc_id']: d for d in manifest['documents']}

    if DB.exists():
        DB.unlink()
    db = sqlite3.connect(str(DB))
    db.executescript(SCHEMA)

    for pos, t in enumerate(tax.TOPICS):
        db.execute('INSERT INTO topics VALUES (?,?,?,?,?)',
                   (t['id'], t['label'], t['description'], pos,
                    json.dumps(t.get('related', []))))
        for spos, s in enumerate(t['subsections']):
            db.execute('INSERT INTO subsections VALUES (?,?,?,?,?,?,?,?)',
                       (s['id'], t['id'], s['label'], s['description'], spos,
                        json.dumps(s['strong']), json.dumps(s['weak']),
                        json.dumps(s.get('exclude', []))))

    sub_ids = {s['id'] for _, s in tax.all_subsections()}
    known_sources = set()
    fts = True
    try:
        db.execute('CREATE VIRTUAL TABLE findings_fts USING fts5(context, matched_text, '
                   'content="findings", content_rowid="rowid")')
    except sqlite3.OperationalError:
        fts = False

    dropped = 0
    rows = 0
    for f in raw['findings']:
        source_key = f"{f['corpus']}|{f.get('source_id')}"
        if source_key not in known_sources:
            known_sources.add(source_key)
            doc = lanes_by_doc.get(f.get('doc_id') or '', {})
            db.execute('INSERT INTO sources VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', (
                source_key, f['corpus'], f.get('source_id'), f.get('doc_id'),
                doc.get('title') or f.get('title'), doc.get('author') or f.get('author'),
                doc.get('doc_type') or f.get('doc_type'), f['lane'],
                1 if (f['lane'] != 'D' or doc.get('lane_assigned', True)) else 0,
                f.get('date'), f.get('date_display'), doc.get('file')))
        ed = editorial.get(f['finding_id'], {})
        tiers = f['subsections']
        overall = 'strong' if 'strong' in tiers.values() else 'weak'
        db.execute('INSERT INTO findings (finding_id, source_key, field, field_class, lane, '
                   'char_offset, matched_text, tier, date, decade, context, relevance, '
                   'review_status, editorial_note, reviewer, reviewed_utc) '
                   'VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (
                       f['finding_id'], source_key, f.get('field'), f['field_class'],
                       f['lane'], f['char_offset'], f['matched_text'], overall,
                       f.get('date'), decade_of(f.get('date')), f['context'],
                       ed.get('relevance'), ed.get('status', 'unreviewed'),
                       ed.get('note'), ed.get('reviewer'), ed.get('reviewed_utc')))
        for sub_id, tier in tiers.items():
            if sub_id not in sub_ids:
                dropped += 1
                continue
            db.execute('INSERT INTO finding_subsections VALUES (?,?,?)',
                       (f['finding_id'], sub_id, tier))
        rows += 1

    if fts:
        db.execute("INSERT INTO findings_fts(rowid, context, matched_text) "
                   "SELECT rowid, context, matched_text FROM findings")

    now = datetime.now(timezone.utc).isoformat(timespec='seconds')
    for k, v in {
        'built_utc': now,
        'findings': str(rows),
        'subsection_links': str(db.execute('SELECT COUNT(*) FROM finding_subsections').fetchone()[0]),
        'sources': str(len(known_sources)),
        'editorial_decisions': str(len(editorial)),
        'fts5': 'yes' if fts else 'no',
        'taxonomy_dropped_links': str(dropped),
        'sweep_generated_utc': raw.get('generated_utc', ''),
    }.items():
        db.execute('INSERT INTO build_info VALUES (?,?)', (k, v))
    db.commit()

    print(f'wrote {DB.relative_to(PROJECT_DIR)}')
    for (name,) in db.execute('SELECT name FROM sqlite_master WHERE type="table" ORDER BY name'):
        n = db.execute(f'SELECT COUNT(*) FROM "{name}"').fetchone()[0]
        print(f'  {name:<22} {n:>7}')
    db.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())
