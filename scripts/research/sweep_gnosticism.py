#!/usr/bin/env python3
"""
Sweep the corpus for every entry in the Gnosticism lexicon.

Reads `curation/gnosticism/lexicon.json` (built by gnostic_lexicon_source.py)
and searches four corpora, recording every attestation with enough context and
identity to cite it:

    Exegesis segments   site/public/data/segments/*.json      lane B
    Selected Letters    selected_letters_analysis.json        lane B
    VALIS trilogy       valis_/divine_invasion_ chapter text  lane A
    Archive scholarship site/public/data/archive/docs/*.json  lane C

Output is machine-generated and regenerable. It is NOT the curated inventory —
relevance is not judged here, only attestation. See
`curation/gnosticism/README.md`.

    python scripts/research/sweep_gnosticism.py \
        --out curation/gnosticism/raw-findings.json --summary
"""

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
CONTEXT = 420          # chars of context kept per hit
DEDUPE_WINDOW = 120    # hits of one entry closer than this collapse


def load_lexicon(path):
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    compiled = []
    for e in data['entries']:
        pats = [re.compile(p, re.IGNORECASE) for p in e['patterns']]
        excl = (re.compile('|'.join(e['exclude']), re.IGNORECASE)
                if e.get('exclude') else None)
        compiled.append((e, pats, excl))
    return data, compiled


def scan(text, compiled, source, field_class='pkd_text', field=None):
    """Yield attestation records for one text blob.

    `field_class` records WHOSE words these are:
        pkd_text          — Dick's own transcribed words (register A)
        editor_annotation — a portal-editor analytical field (register D)
    Collapsing the two would breach the lane discipline this project runs on.
    """
    out = []
    if not text:
        return out
    # Transcribed handwriting wraps mid-phrase; normalise before matching so
    # that "Nag\nHammadi" is not missed.
    text = re.sub(r'\s+', ' ', text)
    for entry, pats, excl in compiled:
        positions = []
        for pat in pats:
            for m in pat.finditer(text):
                positions.append((m.start(), m.end(), m.group(0)))
        if not positions:
            continue
        positions.sort()
        kept = []
        for start, end, matched in positions:
            if kept and start - kept[-1][0] < DEDUPE_WINDOW:
                continue
            kept.append((start, end, matched))
        for start, end, matched in kept:
            lo = max(0, start - CONTEXT // 2)
            hi = min(len(text), end + CONTEXT // 2)
            ctx = re.sub(r'\s+', ' ', text[lo:hi]).strip()
            if excl and excl.search(ctx):
                continue
            out.append({
                'entry_id': entry['id'],
                'label': entry['label'],
                'category': entry['category'],
                'matched': matched,
                'context': ('…' if lo else '') + ctx + ('…' if hi < len(text) else ''),
                'field_class': field_class,
                'field': field,
                **source,
            })
    return out


# --------------------------------------------------------------------------
# Corpora
# --------------------------------------------------------------------------

# Curated analytical fields on each segment. These are portal-editor
# annotation, not Dick's words, and are recorded as register D.
SEGMENT_ANALYTIC_FIELDS = [
    'key_claims', 'recurring_concepts', 'texts_works', 'theological_motifs',
    'people_entities', 'symbols_images', 'evidence_quotes', 'tensions',
    'literary_self_ref', 'autobiographical', 'uncertainty_flags',
    'concise_summary',
]


def corpus_exegesis(compiled):
    hits, n, bad = [], 0, []
    seg_dir = PROJECT_DIR / 'site' / 'public' / 'data' / 'segments'
    for p in sorted(seg_dir.glob('SEG_*.json')):
        try:
            d = json.loads(p.read_text(encoding='utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            bad.append((p.name, str(exc)))
            continue
        n += 1
        text = d.get('raw_text') or ''
        doc = d.get('document') or {}
        src = {
            'corpus': 'exegesis',
            'lane': 'B',
            'source_id': d.get('seg_id'),
            'doc_id': d.get('doc_id'),
            'title': doc.get('title') or d.get('title'),
            'date': d.get('date_start'),
            'date_display': d.get('date_display'),
            'date_confidence': d.get('date_confidence'),
            'slug': d.get('slug'),
        }
        hits.extend(scan(text, compiled, src, 'pkd_text', 'raw_text'))
        for f in SEGMENT_ANALYTIC_FIELDS:
            v = d.get(f)
            if not v:
                continue
            blob = ' \u2014 '.join(v) if isinstance(v, list) else str(v)
            hits.extend(scan(blob, compiled, src, 'editor_annotation', f))
    if bad:
        print(f'  WARNING: {len(bad)} segment file(s) are malformed JSON '
              f'and were skipped:')
        for name, exc in bad:
            print(f'    {name}: {exc}')
    return hits, n


def corpus_letters(compiled):
    hits, n = [], 0
    p = PROJECT_DIR / 'selected_letters_analysis.json'
    if not p.exists():
        return hits, n
    for L in json.loads(p.read_text(encoding='utf-8')):
        n += 1
        src = {
            'corpus': 'letters',
            'lane': 'B',
            'source_id': L.get('letter_id'),
            'doc_id': None,
            'title': f"Letter to {L.get('recipient')}",
            'date': None,
            'date_display': L.get('date'),
            'date_confidence': 'as_printed',
            'slug': None,
        }
        hits.extend(scan(L.get('summary') or '', compiled, src,
                         'pkd_text', 'letter_text'))
    return hits, n


VALIS_FILES = [
    ('VALIS', 'valis_chapter_{}_text.md', range(1, 14)),
    ('The Divine Invasion', 'divine_invasion_chapter_{}_text.md', range(1, 21)),
]


def corpus_valis(compiled):
    hits, n = [], 0
    for work, tmpl, rng in VALIS_FILES:
        for i in rng:
            p = PROJECT_DIR / tmpl.format(i)
            if not p.exists():
                continue
            n += 1
            src = {
                'corpus': 'valis_trilogy',
                'lane': 'A',
                'source_id': f'{p.stem}',
                'doc_id': None,
                'title': f'{work}, chapter {i}',
                'date': '1981',
                'date_display': '1981',
                'date_confidence': 'publication',
                'slug': None,
            }
            hits.extend(scan(p.read_text(encoding='utf-8', errors='replace'),
                             compiled, src))
    # Chapter summaries cover the chapters whose full text is not in the repo.
    for name, work in [
        ('valis_chapters_2_4_summaries.json', 'VALIS'),
        ('valis_chapters_10_13_summaries.json', 'VALIS'),
        ('valis_chapters_1_5_9_summaries.json', 'VALIS'),
        ('divine_invasion_chapters_6_20_summaries.json', 'The Divine Invasion'),
        ('divine_invasion_chapters_1_5_summaries.json', 'The Divine Invasion'),
        ('transmigration_chapters_all_summaries.json',
         'The Transmigration of Timothy Archer'),
    ]:
        p = PROJECT_DIR / name
        if not p.exists():
            continue
        n += 1
        src = {
            'corpus': 'valis_trilogy_summaries',
            'lane': 'D',          # portal-editor summary, not PKD's words
            'source_id': p.stem,
            'doc_id': None,
            'title': f'{work} — chapter summaries',
            'date': '1981',
            'date_display': '1981-1982',
            'date_confidence': 'publication',
            'slug': None,
        }
        hits.extend(scan(p.read_text(encoding='utf-8', errors='replace'),
                         compiled, src))
    return hits, n


def corpus_scholarship(compiled):
    hits, n = [], 0
    doc_dir = PROJECT_DIR / 'site' / 'public' / 'data' / 'archive' / 'docs'
    for p in sorted(doc_dir.glob('*.json')):
        try:
            d = json.loads(p.read_text(encoding='utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        n += 1
        blob = '\n'.join(str(d.get(k) or '') for k in
                         ('title', 'card_summary', 'page_summary'))
        blob += '\n' + ' '.join(d.get('linked_terms') or [])
        src = {
            'corpus': 'scholarship',
            'lane': d.get('evidentiary_lane') or 'C',
            'source_id': d.get('doc_id'),
            'doc_id': d.get('doc_id'),
            'title': d.get('title'),
            'date': d.get('date_start'),
            'date_display': d.get('date_display'),
            'date_confidence': 'catalogued',
            'slug': d.get('slug'),
            'author': d.get('author'),
        }
        hits.extend(scan(blob, compiled, src))
    return hits, n


# --------------------------------------------------------------------------
# Optional DB-backed corpora.
#
# The Selected Letters volumes covering 1975-1982 are catalogued at
# ingest_level "full", but their text lives in database/unified.sqlite, not in
# the exported JSON. Without the database the letters lane covers only the
# 1972-73 volume, which predates 2-3-74 entirely and is therefore silent on
# Gnosticism by accident of what is held rather than by evidence.
#
# Run with --db to include them.
# --------------------------------------------------------------------------

LETTER_DOC_PATTERNS = ('%Selected Letters%', '%Letters from the Heart%',
                       '%Claudia Bush Letters%')


def corpus_letters_db(compiled, db_path):
    import sqlite3
    hits, n = [], 0
    if not Path(db_path).exists():
        print(f'  (no database at {db_path} — skipping DB-backed letters; '
              f'the 1975-1982 correspondence is NOT covered)')
        return hits, n
    con = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)
    con.row_factory = sqlite3.Row
    cols = {r['name'] for r in con.execute('PRAGMA table_info(document_texts)')}
    textcol = 'text_content' if 'text_content' in cols else 'markdown_content'
    where = ' OR '.join(['d.title LIKE ?'] * len(LETTER_DOC_PATTERNS))
    rows = con.execute(
        f'SELECT d.doc_id, d.title, d.date_display, t.{textcol} AS body '
        f'FROM documents d JOIN document_texts t ON t.doc_id = d.doc_id '
        f'WHERE {where}', LETTER_DOC_PATTERNS).fetchall()
    for r in rows:
        n += 1
        src = {
            'corpus': 'letters',
            'lane': 'B',
            'source_id': r['doc_id'],
            'doc_id': r['doc_id'],
            'title': r['title'],
            'date': None,
            'date_display': r['date_display'],
            'date_confidence': 'volume',
            'slug': None,
        }
        hits.extend(scan(r['body'] or '', compiled, src, 'pkd_text',
                         'document_text'))
    con.close()
    return hits, n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lexicon', default=str(
        PROJECT_DIR / 'curation' / 'gnosticism' / 'lexicon.json'))
    ap.add_argument('--out', default=str(
        PROJECT_DIR / 'curation' / 'gnosticism' / 'raw-findings.json'))
    ap.add_argument('--summary', action='store_true')
    ap.add_argument('--db', default=str(
        PROJECT_DIR / 'database' / 'unified.sqlite'),
        help='sweep the Selected Letters volumes held in the database')
    ap.add_argument('--no-db', action='store_true',
                    help='skip DB-backed corpora even if the database exists')
    ap.add_argument('--max-contexts', type=int, default=25,
                    help='contexts stored per entry per corpus')
    args = ap.parse_args()

    lex, compiled = load_lexicon(args.lexicon)
    print(f'Sweeping for {len(compiled)} lexicon entries')

    all_hits, scanned = [], {}
    for name, fn in [('exegesis', corpus_exegesis), ('letters', corpus_letters),
                     ('valis_trilogy', corpus_valis),
                     ('scholarship', corpus_scholarship)]:
        hits, n = fn(compiled)
        scanned[name] = n
        all_hits.extend(hits)
        print(f'  {name:16s} {n:5d} sources  {len(hits):6d} attestations')

    if not args.no_db:
        hits, n = corpus_letters_db(compiled, args.db)
        if n:
            scanned['letters_volumes'] = n
            all_hits.extend(hits)
            print(f'  {"letters_volumes":16s} {n:5d} sources  '
                  f'{len(hits):6d} attestations')

    # Per-entry aggregates. Counts are exact and cover every hit; the stored
    # contexts are capped so the artifact stays reviewable (see --max-contexts).
    agg = defaultdict(lambda: defaultdict(int))
    # Year histograms are built over EVERY hit, not the capped sample, or the
    # chronology would report only each term's earliest sittings.
    years = defaultdict(lambda: defaultdict(int))
    for h in all_hits:
        a = agg[h['entry_id']]
        a[h['corpus']] += 1
        a['total'] += 1
        a[h['field_class']] += 1
        if h['field_class'] == 'pkd_text' and h['corpus'] == 'exegesis':
            m = re.match(r'(\d{4})', str(h.get('date') or ''))
            if m:
                years[h['entry_id']][m.group(1)] += 1

    kept, seen = [], defaultdict(int)
    for h in sorted(all_hits, key=lambda x: (x['field_class'] != 'pkd_text',
                                             x['entry_id'], x.get('date') or '')):
        cap = (args.max_contexts if h['field_class'] == 'pkd_text'
               else max(2, args.max_contexts // 5))
        key = (h['entry_id'], h['corpus'], h['field_class'])
        if seen[key] >= cap:
            continue
        seen[key] += 1
        kept.append(h)

    entries_out = []
    for e in lex['entries']:
        a = agg.get(e['id'], {})
        entries_out.append({
            'entry_id': e['id'],
            'label': e['label'],
            'category': e['category'],
            'tradition': e['tradition'],
            'total': a.get('total', 0),
            'pkd_text': a.get('pkd_text', 0),
            'editor_annotation': a.get('editor_annotation', 0),
            'exegesis': a.get('exegesis', 0),
            'letters': a.get('letters', 0),
            'valis_trilogy': a.get('valis_trilogy', 0),
            'valis_trilogy_summaries': a.get('valis_trilogy_summaries', 0),
            'scholarship': a.get('scholarship', 0),
            'exegesis_by_year': dict(sorted(years.get(e['id'], {}).items())),
        })

    out = {
        'artifact_type': 'gnosticism_raw_sweep',
        'generator': 'scripts/research/sweep_gnosticism.py',
        'lexicon_entries': len(compiled),
        'sources_scanned': scanned,
        'total_attestations': len(all_hits),
        'stored_contexts': len(kept),
        'max_contexts_per_entry_per_corpus': args.max_contexts,
        'note': ('attestation_counts are exact over the whole corpus; '
                 'the attestations list is a capped sample, PKD-text first. '
                 'field_class distinguishes Dick\'s own words (pkd_text) '
                 'from portal-editor annotation (editor_annotation).'),
        'attestation_counts': sorted(entries_out,
                                     key=lambda r: -r['total']),
        'attestations': kept,
    }
    Path(args.out).write_text(json.dumps(out, indent=1, ensure_ascii=False) + '\n',
                              encoding='utf-8')
    print(f'\nwrote {args.out}  ({len(all_hits)} attestations, '
          f'{len(kept)} contexts stored)')

    if args.summary:
        print('\nTop attested:')
        for r in out['attestation_counts'][:45]:
            if not r['total']:
                continue
            print(f"  {r['total']:5d}  {r['category']:14s} {r['label'][:44]:44s} "
                  f"ex={r['exegesis']} let={r['letters']} "
                  f"valis={r['valis_trilogy']} sch={r['scholarship']}")
        zero = [r for r in out['attestation_counts'] if not r['total']]
        print(f'\nUnattested entries ({len(zero)}):')
        print('  ' + ', '.join(r['label'] for r in zero))


if __name__ == '__main__':
    main()
