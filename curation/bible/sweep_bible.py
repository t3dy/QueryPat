#!/usr/bin/env python3
"""
Sweep the corpus for every kind of reference to the Bible: named books, the
words Bible / Scripture / Testament, verse citations, and the biblical
translations and commentaries Dick is known to have used.

    python curation/bible/sweep_bible.py --summary \\
        --out curation/bible/raw-findings.json

Corpora, and the register each is recorded under (see curation/bible/README.md):

    Exegesis segments      site/public/data/segments/*.json   raw_text         A
    VALIS / Divine Invasion  valis_chapter_*_text.md          full text         A
    Editorial analysis     the fiction, stories, letters and
                           exegesis analysis files             summaries         D
    Scholarship and        archive docs, portal essays         page summaries    C / D

Only the Exegesis and the trilogy chapters are Dick's own words in full. The
fiction, letter and interview entries here are editorial summaries; they are
searched so that the absence of a finding can be stated, and they are never
quoted as Dick.

Output is machine-generated and regenerable. Relevance is NOT judged here —
every hit is recorded, and the editor classifies it by reading the passage.
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
DATA = PROJECT_DIR / 'site' / 'public' / 'data'

CONTEXT = 420          # characters of context kept per hit
DEDUPE_WINDOW = 240    # hits of one pattern closer than this collapse

# --------------------------------------------------------------------------
# Patterns. Strong patterns are unambiguous references to the Bible as a text.
# Weak patterns are book names that are also ordinary words or first names
# (Mark, John, Daniel, Acts, Judges...) and need an editor to read the passage.
# Book names are matched case-sensitively, so "acts" the verb does not match.
# --------------------------------------------------------------------------

BOOKS_SPECIFIC = [
    'Genesis', 'Leviticus', 'Deuteronomy', 'Joshua', 'Samuel', 'Chronicles',
    'Nehemiah', 'Ecclesiastes', 'Isaiah', 'Jeremiah', 'Lamentations',
    'Ezekiel', 'Hosea', 'Zechariah', 'Malachi', 'Habakkuk', 'Zephaniah',
    'Obadiah', 'Nahum', 'Haggai', 'Corinthians', 'Galatians', 'Ephesians',
    'Philippians', 'Colossians', 'Thessalonians', 'Hebrews', 'Philemon',
    'Matthew', 'Psalms?', 'Proverbs', 'Song of Songs',
    'Maccabees', 'Tobit', 'Apocrypha', 'Apocalypse of',
]

BOOKS_AMBIGUOUS = [
    'Exodus', 'Revelations?', 'Numbers', 'Judges', 'Ruth', 'Kings', 'Ezra', 'Esther', 'Job',
    'Daniel', 'Joel', 'Amos', 'Jonah', 'Micah', 'Mark', 'Luke', 'John',
    'Acts', 'Romans', 'James', 'Peter', 'Jude', 'Titus', 'Timothy', 'Paul',
]

VERSE_RE = (r'\b(?:Gen|Ex|Exod|Lev|Num|Deut|Josh|Judg|Ps|Psa|Prov|Eccl|Isa|'
            r'Jer|Lam|Ezek|Dan|Hos|Joel|Amos|Jon|Mic|Hab|Zech|Mal|Matt|Mk|Mark|'
            r'Lk|Luke|Jn|John|Acts|Rom|Cor|Gal|Eph|Phil|Col|Thess|Heb|Rev)'
            r'\.?\s?\d{1,3}[:.]\d{1,3}\b')

PATTERNS = {
    # Strong: the Bible named as a text, its parts, or its versions.
    'strong': [
        (r'\bBible\w*', 0),
        (r'\bbiblical\b', re.I),
        (r'\bScriptures?\b', re.I),
        (r'\b(?:Old|New) Testament\b', 0),
        (r'\bKing James\b', 0),
        (r'\bKJV\b', 0),
        (r'\bVulgate\b', 0),
        (r'\bSeptuagint\b', re.I),
        (r'\bHebrew Bible\b|\bTorah\b', 0),
        (r'\bGospels?\b', 0),
        (VERSE_RE, 0),
        (r'\b(?:%s)\b' % '|'.join(BOOKS_SPECIFIC), 0),
    ],
    # Weak: names and words that need an editor's reading.
    'weak': [
        (r'\b(?:%s)\b' % '|'.join(BOOKS_AMBIGUOUS), 0),
        (r'\bPauline\b|\bJohannine\b|\bSynoptic\b', 0),
        (r'\bparables?\b|\bepistles?\b', re.I),
        (r'\bgospels?\b|\btestaments?\b', 0),
    ],
}

# Contexts that are certainly not the Bible. Matched against a window around
# the hit; a hit that matches is kept but flagged, not dropped.
EXCLUDE = re.compile(
    r'Mark Hall|Mark Rifkin|Hubert Selby|Bible Belt|Biblioteca|'
    r'Ruth Ozeki|Jane Austen|George Eliot|Johnny Carson|Dr\. John',
    re.I)


def compile_patterns():
    out = {}
    for tier, pats in PATTERNS.items():
        out[tier] = [(src, re.compile(src, flags)) for src, flags in pats]
    return out


def scan(text, compiled, source):
    """Yield one finding per distinct hit in one blob of text."""
    if not text:
        return
    text = re.sub(r'\s+', ' ', text)
    for tier in ('strong', 'weak'):
        for src, rx in compiled[tier]:
            last = -DEDUPE_WINDOW
            for m in rx.finditer(text):
                if m.start() - last < DEDUPE_WINDOW:
                    continue
                last = m.start()
                lo = max(0, m.start() - CONTEXT // 2)
                hi = min(len(text), m.end() + CONTEXT // 2)
                ctx = text[lo:hi].strip()
                yield {
                    **source,
                    'tier': tier,
                    'pattern': src,
                    'matched_text': m.group(0),
                    'char_offset': m.start(),
                    'context': ('…' if lo else '') + ctx
                               + ('…' if hi < len(text) else ''),
                    'auto_excluded': bool(EXCLUDE.search(
                        text[max(0, m.start() - 80):m.end() + 80])),
                    'relevance': None,          # editorial: see README
                    'editorial_note': None,
                }


# --------------------------------------------------------------------------
# Corpora
# --------------------------------------------------------------------------

SEGMENT_ANALYTIC_FIELDS = [
    'concise_summary', 'key_claims', 'recurring_concepts', 'texts_works',
    'theological_motifs', 'symbols_images', 'evidence_quotes', 'tensions',
    'literary_self_ref', 'autobiographical', 'uncertainty_flags',
]


def corpus_exegesis(compiled):
    hits, n, bad = [], 0, []
    for p in sorted((DATA / 'segments').glob('SEG_*.json')):
        try:
            d = json.loads(p.read_text(encoding='utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            bad.append((p.name, str(exc)))
            continue
        n += 1
        doc = d.get('document') or {}
        src = {
            'corpus': 'exegesis',
            'lane': 'A',
            'source_id': d.get('seg_id'),
            'doc_id': d.get('doc_id'),
            'title': doc.get('title') or d.get('title'),
            'date': d.get('date_start'),
            'date_display': d.get('date_display'),
            'field_class': 'pkd_text',
            'field': 'raw_text',
        }
        hits.extend(scan(d.get('raw_text') or '', compiled, src))
        for f in SEGMENT_ANALYTIC_FIELDS:
            v = d.get(f)
            if not v:
                continue
            blob = ' — '.join(v) if isinstance(v, list) else str(v)
            hits.extend(scan(blob, compiled,
                             {**src, 'lane': 'D', 'field_class': 'editor_annotation',
                              'field': f}))
    if bad:
        print(f'  WARNING: {len(bad)} segment file(s) are malformed JSON '
              f'and were skipped:')
        for name, exc in bad:
            print(f'    {name}: {exc}')
    return hits, n


TRILOGY_FILES = [
    ('VALIS', 'valis_chapter_{}_text.md', range(1, 14)),
    ('The Divine Invasion', 'divine_invasion_chapter_{}_text.md', range(1, 21)),
]


def corpus_trilogy_text(compiled):
    hits, n = [], 0
    for work, tmpl, rng in TRILOGY_FILES:
        for i in rng:
            p = PROJECT_DIR / tmpl.format(i)
            if not p.exists():
                continue
            n += 1
            src = {'corpus': 'trilogy_text', 'lane': 'A', 'source_id': p.stem,
                   'title': f'{work}, chapter {i}', 'date': '1981',
                   'date_display': '1981', 'field_class': 'pkd_text',
                   'field': 'chapter_text'}
            hits.extend(scan(p.read_text(encoding='utf-8', errors='replace'),
                             compiled, src))
    return hits, n


# Editorial analysis files. Each is walked for its string fields; the lane is
# always D, because these are portal-editor summaries, never Dick's words.
ANALYSIS_FILES = [
    ('do_androids_dream_chapters_all.json', 'Do Androids Dream of Electric Sheep?', 'novel_summary'),
    ('man_in_high_castle_chapters_all.json', 'The Man in the High Castle', 'novel_summary'),
    ('maze_of_death_chapters_all.json', 'A Maze of Death', 'novel_summary'),
    ('ubik_chapters_1_5_analysis.json', 'Ubik', 'novel_summary'),
    ('ubik_chapters_6_17_analysis.json', 'Ubik', 'novel_summary'),
    ('valis_chapter_analysis.json', 'VALIS', 'novel_summary'),
    ('valis_chapters_1_5_9_summaries.json', 'VALIS', 'novel_summary'),
    ('valis_chapters_2_4_summaries.json', 'VALIS', 'novel_summary'),
    ('valis_chapters_10_13_summaries.json', 'VALIS', 'novel_summary'),
    ('divine_invasion_chapters_1_5_summaries.json', 'The Divine Invasion', 'novel_summary'),
    ('divine_invasion_chapters_6_20_summaries.json', 'The Divine Invasion', 'novel_summary'),
    ('transmigration_chapters_all_summaries.json', 'The Transmigration of Timothy Archer', 'novel_summary'),
    ('pkd_stories_all.json', 'Short stories', 'story_summary'),
    ('pkd_stories_analysis.json', 'Short stories', 'story_summary'),
    ('pkd_biography_events.json', 'Biography', 'biography'),
    ('biography_events_from_letters.json', 'Biography', 'biography'),
    ('exegesis_entries_analysis.json', 'Exegesis (editorial entry analysis)', 'exegesis_summary'),
]


def corpus_letters(compiled):
    """The Selected Letters, 1972-73: Dick's own words (lane A), but held as
    excerpts. Each record's `summary` is capped at 1,500 characters, and in a
    few records the body of the letter sits in `recipient` (the field that
    otherwise holds a name). Both are scanned; a name is too short to matter.
    The letters are therefore a floor for this search, not a census."""
    hits, n = [], 0
    p = PROJECT_DIR / 'selected_letters_analysis.json'
    if not p.exists():
        return hits, n
    for L in json.loads(p.read_text(encoding='utf-8')):
        n += 1
        src = {'corpus': 'letters', 'lane': 'A', 'source_id': L.get('letter_id'),
               'title': f"Letter to {L.get('recipient', '').split(chr(10))[0][:40]}",
               'date': L.get('date'), 'date_display': L.get('date'),
               'field_class': 'pkd_text', 'field': 'letter_text'}
        for key in ('summary', 'recipient'):
            text = L.get(key) or ''
            if key == 'recipient' and len(text) < 200:
                continue
            hits.extend(scan(text, compiled, {**src, 'field': key}))
    return hits, n


def walk_strings(obj, path=''):
    """Yield (path, string) for every string in a JSON value."""
    if isinstance(obj, str):
        yield path, obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk_strings(v, f'{path}.{k}' if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk_strings(v, f'{path}[{i}]')


def corpus_analysis(compiled):
    hits, n = [], 0
    for name, work, kind in ANALYSIS_FILES:
        p = PROJECT_DIR / name
        if not p.exists():
            continue
        n += 1
        data = json.loads(p.read_text(encoding='utf-8'))
        for path, text in walk_strings(data):
            if len(text) < 20:
                continue
            src = {'corpus': kind, 'lane': 'D', 'source_id': f'{p.stem}:{path}',
                   'title': work, 'field_class': 'editor_annotation',
                   'field': path}
            hits.extend(scan(text, compiled, src))
    return hits, n


def corpus_documents(compiled):
    """Archive records and portal essays: scholarship (C) and editorial (D)."""
    hits, n = [], 0
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
        src = {'corpus': f'archive:{dtype}', 'lane': lane,
               'source_id': d.get('doc_id'), 'title': d.get('title'),
               'author': d.get('author'), 'date': d.get('date_display'),
               'field_class': 'editor_annotation', 'field': 'record'}
        for key in ('card_summary', 'page_summary', 'editorial_notes',
                    'summary', 'description'):
            if isinstance(d.get(key), str):
                hits.extend(scan(d[key], compiled, {**src, 'field': key}))
    for p in sorted((DATA / 'essays').glob('*.md')):
        n += 1
        src = {'corpus': 'portal_essay', 'lane': 'D', 'source_id': p.stem,
               'title': p.stem, 'field_class': 'editor_annotation',
               'field': 'essay'}
        hits.extend(scan(p.read_text(encoding='utf-8', errors='replace'),
                         compiled, src))
    return hits, n


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out', default=None, help='write the inventory here')
    ap.add_argument('--summary', action='store_true')
    args = ap.parse_args()

    compiled = compile_patterns()
    print('Sweeping corpus for the Bible')
    findings, counts = [], {}
    for label, fn in (('exegesis segments', corpus_exegesis),
                      ('trilogy chapter text', corpus_trilogy_text),
                      ('letters, 1972-73', corpus_letters),
                      ('editorial analysis files', corpus_analysis),
                      ('archive records and essays', corpus_documents)):
        hits, n = fn(compiled)
        findings += hits
        counts[label] = n
        print(f'  {label:<28} {n:>5} sources  {len(hits):>5} hits')

    strong = [f for f in findings if f['tier'] == 'strong' and not f['auto_excluded']]
    print(f'\n  total hits       {len(findings)}')
    print(f'    strong tier    {sum(1 for f in findings if f["tier"] == "strong")}')
    print(f'    weak tier      {sum(1 for f in findings if f["tier"] == "weak")}')
    print(f'    auto-excluded  {sum(1 for f in findings if f["auto_excluded"])}')

    if args.summary:
        by_lane = defaultdict(int)
        by_pat = defaultdict(int)
        for f in strong:
            by_lane[f['lane']] += 1
            by_pat[f['matched_text'].lower()] += 1
        print('\n  strong hits by lane:')
        for k in sorted(by_lane):
            print(f'    {k}  {by_lane[k]:>5}')
        print('\n  strong hits by matched text (top 25):')
        for k, v in sorted(by_pat.items(), key=lambda x: -x[1])[:25]:
            print(f'    {v:>5}  {k}')

    if args.out:
        out = PROJECT_DIR / args.out
        out.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            'profile': 'bible',
            'generated_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'patterns': {t: [src for src, _ in PATTERNS[t]] for t in PATTERNS},
            'exclude': EXCLUDE.pattern,
            'corpora': counts,
            'counts': {'total': len(findings),
                       'strong': sum(1 for f in findings if f['tier'] == 'strong'),
                       'auto_excluded': sum(1 for f in findings if f['auto_excluded'])},
            'findings': findings,
        }
        out.write_text(json.dumps(payload, indent=1, ensure_ascii=False),
                       encoding='utf-8')
        print(f'\n  wrote {out.relative_to(PROJECT_DIR)} '
              f'({out.stat().st_size / 1e6:.1f} MB)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
