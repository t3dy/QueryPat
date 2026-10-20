#!/usr/bin/env python3
"""
Sweep the corpus for every religion subsection in curation/religion/taxonomy.py,
and write one finding per distinct hit, tagged with every subsection it belongs to.

    python scripts/research/sweep_religion.py --summary \\
        --out curation/religion/raw-findings.json

Corpora searched, with the lane each is recorded under:

    Exegesis segments        site/public/data/segments/*.json   raw_text            A
                             (analytic fields of the same segments)                 D
    VALIS / Divine Invasion  valis_chapter_*_text.md, divine_invasion_*  full text  A
    Selected Letters 1972–73 selected_letters_analysis.json      excerpts            A
    Editorial analysis       fiction, stories, biography, analysis files            D
    Archive records, essays  site/public/data/archive/docs, essays/                 C / D
    Staged PDF text          curation/religion/pdf-manifest.json (see ingest_pdfs.py)  as recorded

A finding is one hit: a corpus record, a field, a character offset and a matched
span. The same hit can carry several subsection tags, and its id is stable across
re-sweeps of unchanged text, so editorial decisions keyed on it survive.

Relevance is NOT judged here. Every hit is recorded, and an editor classifies it
with scripts/research/religion_review.py.
"""

import argparse
import hashlib
import importlib.util
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
DATA = PROJECT_DIR / 'site' / 'public' / 'data'
CUR = PROJECT_DIR / 'curation' / 'religion'

CONTEXT = 360          # characters of context stored per hit
DEDUPE_WINDOW = 240    # hits of one subsection in one field closer than this collapse
EXCLUDE_SPAN = 80      # an exclusion pattern is checked this far either side of a hit


def load_taxonomy():
    spec = importlib.util.spec_from_file_location('religion_taxonomy', CUR / 'taxonomy.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def compile_taxonomy(tax):
    """Return [(topic_id, sub_id, [(tier, regex)], exclude_regex_or_None)]."""
    compiled = []
    for topic_id, sub in tax.all_subsections():
        pats = [('strong', re.compile(p, re.I)) for p in sub['strong']]
        pats += [('weak', re.compile(p, re.I)) for p in sub['weak']]
        excl = re.compile('|'.join(sub['exclude']), re.I) if sub.get('exclude') else None
        compiled.append((topic_id, sub['id'], pats, excl))
    return compiled


def finding_id(corpus, source_id, field, offset, matched):
    key = f'{corpus}|{source_id}|{field}|{offset}|{matched}'
    return 'REL_' + hashlib.sha1(key.encode('utf-8')).hexdigest()[:14]


class Collector:
    """Accumulates findings keyed by their id, merging subsection tags."""

    def __init__(self, compiled):
        self.compiled = compiled
        self.by_id = {}

    def scan(self, text, source):
        if not text:
            return
        text = re.sub(r'\s+', ' ', text)
        for topic_id, sub_id, pats, excl in self.compiled:
            last_by_tier = {}
            for tier, rx in pats:
                for m in rx.finditer(text):
                    if m.start() - last_by_tier.get(sub_id, -DEDUPE_WINDOW) < DEDUPE_WINDOW:
                        continue
                    if excl and excl.search(text[max(0, m.start() - EXCLUDE_SPAN):
                                                 m.end() + EXCLUDE_SPAN]):
                        continue
                    last_by_tier[sub_id] = m.start()
                    fid = finding_id(source['corpus'], source['source_id'],
                                     source['field'], m.start(), m.group(0))
                    f = self.by_id.get(fid)
                    if f is None:
                        lo = max(0, m.start() - CONTEXT // 2)
                        hi = min(len(text), m.end() + CONTEXT // 2)
                        f = {
                            'finding_id': fid,
                            **source,
                            'matched_text': m.group(0),
                            'char_offset': m.start(),
                            'context': ('…' if lo else '')
                                       + text[lo:hi].strip()
                                       + ('…' if hi < len(text) else ''),
                            'subsections': {},
                        }
                        self.by_id[fid] = f
                    # A subsection's tier is strong if any of its patterns is strong here.
                    prev = f['subsections'].get(sub_id)
                    if prev != 'strong':
                        f['subsections'][sub_id] = tier
                    f.setdefault('topics', [])
                    if topic_id not in f['topics']:
                        f['topics'].append(topic_id)


# --------------------------------------------------------------------------
# Corpora
# --------------------------------------------------------------------------

ANALYTIC_FIELDS = [
    'concise_summary', 'key_claims', 'recurring_concepts', 'texts_works',
    'theological_motifs', 'symbols_images', 'evidence_quotes', 'tensions',
    'literary_self_ref', 'autobiographical', 'uncertainty_flags',
]


def corpus_exegesis(col):
    n, bad = 0, []
    for p in sorted((DATA / 'segments').glob('SEG_*.json')):
        try:
            d = json.loads(p.read_text(encoding='utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            bad.append(p.name)
            continue
        n += 1
        doc = d.get('document') or {}
        base = {
            'corpus': 'exegesis', 'lane': 'A', 'source_id': d.get('seg_id'),
            'doc_id': d.get('doc_id'),
            'title': doc.get('title') or d.get('title'),
            'date': d.get('date_start'), 'date_display': d.get('date_display'),
            'field_class': 'pkd_text', 'field': 'raw_text',
        }
        col.scan(d.get('raw_text') or '', base)
        for f in ANALYTIC_FIELDS:
            v = d.get(f)
            if not v:
                continue
            blob = ' — '.join(v) if isinstance(v, list) else str(v)
            col.scan(blob, {**base, 'lane': 'D', 'field_class': 'editor_annotation',
                            'field': f})
    if bad:
        print(f'  WARNING: {len(bad)} segment file(s) malformed and skipped: '
              + ', '.join(bad))
    return n


TRILOGY = [
    ('VALIS', 'valis_chapter_{}_text.md', range(1, 14)),
    ('The Divine Invasion', 'divine_invasion_chapter_{}_text.md', range(1, 21)),
]


def corpus_trilogy(col):
    n = 0
    for work, tmpl, rng in TRILOGY:
        for i in rng:
            p = PROJECT_DIR / tmpl.format(i)
            if not p.exists():
                continue
            n += 1
            col.scan(p.read_text(encoding='utf-8', errors='replace'), {
                'corpus': 'trilogy_text', 'lane': 'A', 'source_id': p.stem,
                'doc_id': None, 'title': f'{work}, chapter {i}',
                'date': '1981', 'date_display': '1981',
                'field_class': 'pkd_text', 'field': 'chapter_text'})
    return n


def corpus_letters(col):
    n = 0
    p = PROJECT_DIR / 'selected_letters_analysis.json'
    if not p.exists():
        return n
    for L in json.loads(p.read_text(encoding='utf-8')):
        n += 1
        for key in ('summary', 'recipient'):
            text = L.get(key) or ''
            if key == 'recipient' and len(text) < 200:
                continue
            col.scan(text, {
                'corpus': 'letters', 'lane': 'A', 'source_id': L.get('letter_id'),
                'doc_id': None,
                'title': f"Letter to {(L.get('recipient') or '').split(chr(10))[0][:40]}",
                'date': L.get('date'), 'date_display': L.get('date'),
                'field_class': 'pkd_text', 'field': 'letter_text'})
    return n


ANALYSIS_FILES = [
    'do_androids_dream_chapters_all.json', 'man_in_high_castle_chapters_all.json',
    'maze_of_death_chapters_all.json', 'ubik_chapters_1_5_analysis.json',
    'ubik_chapters_6_17_analysis.json', 'valis_chapter_analysis.json',
    'valis_chapters_1_5_9_summaries.json', 'valis_chapters_2_4_summaries.json',
    'valis_chapters_10_13_summaries.json', 'divine_invasion_chapters_1_5_summaries.json',
    'divine_invasion_chapters_6_20_summaries.json',
    'transmigration_chapters_all_summaries.json', 'pkd_stories_all.json',
    'pkd_stories_analysis.json', 'pkd_biography_events.json',
    'biography_events_from_letters.json', 'exegesis_entries_analysis.json',
]


def walk_strings(obj, path=''):
    if isinstance(obj, str):
        yield path, obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk_strings(v, f'{path}.{k}' if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk_strings(v, f'{path}[{i}]')


def corpus_analysis(col):
    n = 0
    for name in ANALYSIS_FILES:
        p = PROJECT_DIR / name
        if not p.exists():
            continue
        n += 1
        for path, text in walk_strings(json.loads(p.read_text(encoding='utf-8'))):
            if len(text) < 20:
                continue
            col.scan(text, {'corpus': 'editorial_analysis', 'lane': 'D',
                            'source_id': f'{p.stem}:{path}', 'doc_id': None,
                            'title': p.stem, 'date': None, 'date_display': None,
                            'field_class': 'editor_annotation', 'field': path})
    return n


def corpus_archive(col):
    n = 0
    for p in sorted((DATA / 'archive' / 'docs').glob('*.json')):
        try:
            d = json.loads(p.read_text(encoding='utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        if not isinstance(d, dict):
            continue
        n += 1
        dtype = d.get('doc_type')
        lane = 'C' if dtype in ('scholarship', 'biography') else 'D'
        base = {'corpus': f'archive:{dtype}', 'lane': lane,
                'source_id': d.get('doc_id'), 'doc_id': d.get('doc_id'),
                'title': d.get('title'), 'author': d.get('author'),
                'date': d.get('date_display'), 'date_display': d.get('date_display'),
                'field_class': 'scholarship' if lane == 'C' else 'editor_annotation'}
        for key in ('card_summary', 'page_summary', 'editorial_notes', 'summary'):
            if isinstance(d.get(key), str):
                col.scan(d[key], {**base, 'field': key})
    for p in sorted((DATA / 'essays').glob('*.md')):
        n += 1
        col.scan(p.read_text(encoding='utf-8', errors='replace'), {
            'corpus': 'portal_essay', 'lane': 'D', 'source_id': p.stem, 'doc_id': None,
            'title': p.stem, 'date': None, 'date_display': None,
            'field_class': 'editor_annotation', 'field': 'essay'})
    return n


def corpus_staged_pdfs(col):
    """Text staged by ingest_pdfs.py, described by pdf-manifest.json."""
    manifest = CUR / 'pdf-manifest.json'
    if not manifest.exists():
        return 0
    n = 0
    for entry in json.loads(manifest.read_text(encoding='utf-8'))['documents']:
        path = CUR / entry['text_file']
        if not path.exists():
            continue
        n += 1
        lane = entry['lane']
        field_class = {'A': 'pkd_text', 'C': 'scholarship'}.get(lane, 'editor_annotation')
        col.scan(path.read_text(encoding='utf-8', errors='replace'), {
            'corpus': 'pdf_archive', 'lane': lane, 'source_id': entry['doc_id'],
            'doc_id': entry['doc_id'], 'title': entry['title'],
            'author': entry.get('author'), 'date': entry.get('date'),
            'date_display': entry.get('date'), 'doc_type': entry.get('doc_type'),
            'field_class': field_class, 'field': 'text'})
    return n


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out', default=None)
    ap.add_argument('--summary', action='store_true')
    args = ap.parse_args()

    tax = load_taxonomy()
    col = Collector(compile_taxonomy(tax))
    counts = {}
    for label, fn in (('exegesis segments', corpus_exegesis),
                      ('trilogy chapter text', corpus_trilogy),
                      ('letters, 1972-73 excerpts', corpus_letters),
                      ('editorial analysis', corpus_analysis),
                      ('archive records and essays', corpus_archive),
                      ('staged PDF text', corpus_staged_pdfs)):
        n = fn(col)
        counts[label] = n
        print(f'  {label:<28} {n:>5} sources')

    findings = sorted(col.by_id.values(),
                      key=lambda f: (f['corpus'], str(f.get('source_id')), f['char_offset']))
    for f in findings:
        f.setdefault('topics', [])

    by_sub = Counter(s for f in findings for s in f['subsections'])
    print(f'\n  findings {len(findings)}')
    if args.summary:
        print('  findings per subsection:')
        for topic_id, sub in tax.all_subsections():
            print(f"    {by_sub.get(sub['id'], 0):>6}  {topic_id}/{sub['id']}")

    if args.out:
        out = PROJECT_DIR / args.out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({
            'generator': 'scripts/research/sweep_religion.py',
            'generated_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'corpora': counts,
            'findings': findings,
        }, ensure_ascii=False, indent=1), encoding='utf-8')
        print(f'  wrote {out.relative_to(PROJECT_DIR)} ({out.stat().st_size / 1e6:.1f} MB)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
