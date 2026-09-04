#!/usr/bin/env python3
"""
Search every representation of the PKD archive that exists in this repository
and emit a machine-readable finding inventory.

Corpora searched (all of them, not just document_texts.text_content):

  * segments.raw_text and every curated segment field
  * document_texts.text_content  AND  document_texts.markdown_content
  * page_texts.page_text                     (per-page OCR)
  * letters.body_md                          (individual letters)
  * claims.claim_text / claims.source_text
  * biography_events, works, pkd_on_pkd_mentions, annotations,
    evidence_excerpts, theophanies, timeline_events
  * database/extracted_markdown/*.md         (on-disk markdown corpus)
  * site/public/data/essays/*.md             (portal essays)
  * any additional --extra-dir of text/markdown

Output: one JSON inventory of findings, each with source, corpus location,
snippet, matched pattern, and a slot for relevance classification. Nothing is
classified automatically beyond obvious false-positive filters; classification
is an editorial act recorded by hand in the inventory.

Usage:
    python scripts/research/sweep_corpus.py --profile burroughs \\
        --out curation/burroughs-word-virus/raw-findings.json
    python scripts/research/sweep_corpus.py --profile burroughs --summary
"""

import argparse
import json
import re
import sqlite3
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = PROJECT_DIR / 'database' / 'unified.sqlite'
MARKDOWN_DIR = PROJECT_DIR / 'database' / 'extracted_markdown'
ESSAY_DIR = PROJECT_DIR / 'site' / 'public' / 'data' / 'essays'

# --------------------------------------------------------------------------
# Search profiles. `strong` terms are near-certain topic hits; `weak` terms are
# concept language that needs editorial judgement; `exclude` kills known false
# positives outright.
# --------------------------------------------------------------------------

PROFILES = {
    'burroughs': {
        'strong': [
            r'\bBurroughs\b', r'\bBurrough\b', r'\bEurrough',      # OCR variant
            r'William S\.? Burroughs', r'W\.\s?S\.\s?Burroughs',
            r'\bword[\s\-]?virus\b', r'\binformation virus\b',
            r'\blanguage virus\b', r'\blinguistic virus\b',
            r'\bverbal virus\b', r'\bthought virus\b', r'\bmind virus\b',
            r'\bNova Mob\b', r'\bnova police\b', r'\bNova Express\b',
            r'Naked Lunch', r'Ticket That Exploded', r'Soft Machine',
            r'\bWild Boys\b', r'\bJunky\b', r'\bJunkie\b',
            r'\bcut[\s\-]?up\b', r'\bcut[\s\-]?ups\b',
            r'\bBrion Gysin\b', r'\bGysin\b',
        ],
        'weak': [
            r'\banti[\s\-]?information\b', r'\bcounter[\s\-]?information\b',
            r'\blatent (?:message|information)', r'\bsubliminal\b',
            r'\bjamming\b', r'\bjammed\b', r'\bscrambl',
            r'\bcontaminat', r'\bparasit', r'\bpossession\b',
            r'\blanguage as (?:control|weapon|parasite)\b',
            r'\bliving information\b', r'\binfo(?:rmation)? life form\b',
            r'\bplayback\b', r'\btape recorder\b',
            r'\bocclu',              # occlusion / occluded — Dick's key term
        ],
        # Contexts that are certainly not William S. Burroughs.
        'exclude': [
            r'Edgar Rice Burroughs', r'\bERB\b', r'Chessmen of Mars',
            r'Tarzan', r'Barsoom', r'John Carter', r'Warrior of the Dawn',
            r'Return of Tharn', r'Burroughs Corporation',
            r'Lou Reed', r'Hubert Selby',
        ],
    },
}

CONTEXT = 900
DEDUPE_WINDOW = 400


def compile_profile(p):
    return (
        [(pat, re.compile(pat, re.IGNORECASE)) for pat in p['strong']],
        [(pat, re.compile(pat, re.IGNORECASE)) for pat in p['weak']],
        re.compile('|'.join(p['exclude']), re.IGNORECASE) if p.get('exclude') else None,
    )


def scan_text(text, strong, weak, exclude, source):
    """Yield finding dicts for one blob of text."""
    if not text:
        return
    seen = set()
    for tier, pats in (('strong', strong), ('weak', weak)):
        for pat_src, rx in pats:
            for m in rx.finditer(text):
                bucket = (tier, m.start() // DEDUPE_WINDOW)
                if bucket in seen:
                    continue
                seen.add(bucket)
                s = max(0, m.start() - CONTEXT // 2)
                e = min(len(text), m.end() + CONTEXT // 2)
                snippet = re.sub(r'\s+', ' ', text[s:e]).strip()
                excluded = bool(exclude and exclude.search(
                    text[max(0, m.start() - 120):m.end() + 120]))
                yield {
                    **source,
                    'tier': tier,
                    'pattern': pat_src,
                    'matched_text': m.group(0),
                    'char_offset': m.start(),
                    'snippet': snippet,
                    'auto_excluded': excluded,
                    'relevance': None,       # editorial: 1..5, see README
                    'confidence': None,
                    'concepts': [],
                    'on_public_page': False,
                    'editorial_note': None,
                }


def sweep_database(strong, weak, exclude):
    findings = []
    if not DB_PATH.exists():
        print(f'  ! database not found: {DB_PATH}', file=sys.stderr)
        return findings
    db = sqlite3.connect(str(DB_PATH))
    db.row_factory = sqlite3.Row

    def add(rows, corpus, id_field, text_field, extra=None):
        n = 0
        for r in rows:
            src = {
                'corpus': corpus,
                'source_id': r[id_field],
                'field': text_field,
            }
            for k, col in (extra or {}).items():
                src[k] = r[col] if col in r.keys() else None
            for f in scan_text(r[text_field], strong, weak, exclude, src):
                findings.append(f)
                n += 1
        print(f'    {corpus:<28} {n:>5} findings')

    add(db.execute("""SELECT s.seg_id, s.raw_text, s.date_display, s.title, s.doc_id
                      FROM segments s WHERE s.raw_text IS NOT NULL"""),
        'exegesis_segment', 'seg_id', 'raw_text',
        {'date': 'date_display', 'title': 'title', 'doc_id': 'doc_id'})

    for col in ('concise_summary', 'key_claims', 'recurring_concepts',
                'texts_works', 'people_entities', 'evidence_quotes'):
        add(db.execute(f"""SELECT seg_id, {col}, date_display, doc_id FROM segments
                           WHERE {col} IS NOT NULL"""),
            f'segment_curated:{col}', 'seg_id', col,
            {'date': 'date_display', 'doc_id': 'doc_id'})

    add(db.execute("""SELECT dt.doc_id, dt.text_content, d.title, d.doc_type,
                             d.evidentiary_lane, d.date_display, d.author, d.slug
                      FROM document_texts dt JOIN documents d ON d.doc_id = dt.doc_id
                      WHERE dt.text_content IS NOT NULL"""),
        'document_text', 'doc_id', 'text_content',
        {'title': 'title', 'doc_type': 'doc_type', 'lane': 'evidentiary_lane',
         'date': 'date_display', 'author': 'author', 'slug': 'slug'})

    add(db.execute("""SELECT dt.doc_id, dt.markdown_content, d.title, d.doc_type,
                             d.evidentiary_lane, d.date_display, d.author, d.slug
                      FROM document_texts dt JOIN documents d ON d.doc_id = dt.doc_id
                      WHERE dt.markdown_content IS NOT NULL"""),
        'document_markdown', 'doc_id', 'markdown_content',
        {'title': 'title', 'doc_type': 'doc_type', 'lane': 'evidentiary_lane',
         'date': 'date_display', 'author': 'author', 'slug': 'slug'})

    add(db.execute("""SELECT pt.page_text_id, pt.page_text, pt.doc_id, pt.page_num,
                             d.title, d.doc_type, d.evidentiary_lane
                      FROM page_texts pt LEFT JOIN documents d ON d.doc_id = pt.doc_id
                      WHERE pt.page_text IS NOT NULL"""),
        'page_ocr', 'page_text_id', 'page_text',
        {'doc_id': 'doc_id', 'page': 'page_num', 'title': 'title',
         'doc_type': 'doc_type', 'lane': 'evidentiary_lane'})

    add(db.execute("""SELECT letter_id, body_md, date_display, recipient_raw,
                             recipient_canonical, volume_doc_id
                      FROM letters WHERE body_md IS NOT NULL"""),
        'letter', 'letter_id', 'body_md',
        {'date': 'date_display', 'recipient': 'recipient_raw',
         'doc_id': 'volume_doc_id'})

    for col in ('claim_text', 'source_text'):
        add(db.execute(f"""SELECT claim_id, {col}, doc_id, lane, source_id
                           FROM claims WHERE {col} IS NOT NULL"""),
            f'claim:{col}', 'claim_id', col,
            {'doc_id': 'doc_id', 'lane': 'lane', 'seg_id': 'source_id'})

    add(db.execute("""SELECT bio_id, summary, date_display, source_name, event_type
                      FROM biography_events WHERE summary IS NOT NULL"""),
        'biography_event', 'bio_id', 'summary',
        {'date': 'date_display', 'author': 'source_name', 'doc_type': 'event_type'})

    for col in ('card_summary', 'page_summary'):
        add(db.execute(f"""SELECT work_id, {col}, canonical_title, slug, date_display
                           FROM works WHERE {col} IS NOT NULL"""),
            f'work:{col}', 'work_id', col,
            {'title': 'canonical_title', 'slug': 'slug', 'date': 'date_display'})

    add(db.execute("""SELECT mention_id, context_snippet, doc_title, doc_slug,
                             doc_type, date_display, work_id
                      FROM pkd_on_pkd_mentions WHERE context_snippet IS NOT NULL"""),
        'pkd_on_pkd', 'mention_id', 'context_snippet',
        {'title': 'doc_title', 'slug': 'doc_slug', 'doc_type': 'doc_type',
         'date': 'date_display'})

    add(db.execute("""SELECT excerpt_id, excerpt_text, ev_id, seg_id, matched_alias
                      FROM evidence_excerpts WHERE excerpt_text IS NOT NULL"""),
        'evidence_excerpt', 'excerpt_id', 'excerpt_text',
        {'seg_id': 'seg_id', 'title': 'matched_alias'})

    for tbl, idc, cols in (
        ('annotations', 'ann_id', ('content',)),
        ('theophanies', 'theophany_id',
         ('summary', 'description', 'pkd_interpretations',
          'scholar_interpretations', 'primary_quote', 'primary_sources')),
        ('timeline_events', 'event_id', ('event_summary', 'notes')),
    ):
        try:
            available = {r[1] for r in db.execute(f'PRAGMA table_info({tbl})')}
        except Exception:
            continue
        if idc not in available:
            idc = next(iter(available))
        for col in cols:
            if col not in available:
                continue
            add(db.execute(f"""SELECT {idc}, {col} FROM {tbl} WHERE {col} IS NOT NULL"""),
                f'{tbl}:{col}', idc, col)

    db.close()
    return findings


def sweep_files(strong, weak, exclude, extra_dirs):
    findings = []
    groups = [('extracted_markdown', MARKDOWN_DIR, '*.md'),
              ('portal_essay', ESSAY_DIR, '*.md')]
    for d in extra_dirs or []:
        groups.append(('extra', Path(d), '*'))
    for corpus, root, pattern in groups:
        if not root.exists():
            print(f'    {corpus:<28} (missing: {root})')
            continue
        n = 0
        for p in sorted(root.rglob(pattern)):
            if not p.is_file() or p.suffix.lower() not in ('.md', '.txt', ''):
                continue
            try:
                text = p.read_text(encoding='utf-8', errors='replace')
            except Exception:
                continue
            src = {'corpus': corpus, 'source_id': p.stem,
                   'field': 'file', 'path': str(p.relative_to(PROJECT_DIR))}
            for f in scan_text(text, strong, weak, exclude, src):
                findings.append(f)
                n += 1
        print(f'    {corpus:<28} {n:>5} findings')
    return findings


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--profile', default='burroughs', choices=sorted(PROFILES))
    ap.add_argument('--out', default=None, help='write the inventory here')
    ap.add_argument('--extra-dir', action='append', default=[])
    ap.add_argument('--summary', action='store_true')
    ap.add_argument('--include-weak', action='store_true',
                    help='keep weak-tier findings in the output (default: yes)')
    args = ap.parse_args()

    prof = PROFILES[args.profile]
    strong, weak, exclude = compile_profile(prof)

    print(f'Sweeping corpus for profile "{args.profile}"')
    print(f'  {len(prof["strong"])} strong patterns, {len(prof["weak"])} weak, '
          f'{len(prof.get("exclude", []))} exclusions')
    print('  database corpora:')
    findings = sweep_database(strong, weak, exclude)
    print('  file corpora:')
    findings += sweep_files(strong, weak, exclude, args.extra_dir)

    strong_n = sum(1 for f in findings if f['tier'] == 'strong')
    excl_n = sum(1 for f in findings if f['auto_excluded'])
    print(f'\n  total findings   {len(findings)}')
    print(f'    strong tier    {strong_n}')
    print(f'    weak tier      {len(findings) - strong_n}')
    print(f'    auto-excluded  {excl_n}  (Edgar Rice Burroughs etc.)')

    if args.summary:
        by = defaultdict(int)
        for f in findings:
            if f['tier'] == 'strong' and not f['auto_excluded']:
                by[f['corpus']] += 1
        print('\n  strong findings by corpus:')
        for k, v in sorted(by.items(), key=lambda x: -x[1]):
            print(f'    {v:>5}  {k}')

    if args.out:
        out = PROJECT_DIR / args.out
        out.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            'profile': args.profile,
            'generated_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'patterns': {'strong': prof['strong'], 'weak': prof['weak'],
                         'exclude': prof.get('exclude', [])},
            'counts': {'total': len(findings), 'strong': strong_n,
                       'auto_excluded': excl_n},
            'findings': findings,
        }
        out.write_text(json.dumps(payload, indent=1, ensure_ascii=False),
                       encoding='utf-8')
        print(f'\n  wrote {out.relative_to(PROJECT_DIR)} '
              f'({out.stat().st_size / 1e6:.1f} MB)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
