#!/usr/bin/env python3
"""
Build the Gnosticism register: the lexicon joined to its corpus attestations.

    curation/gnosticism/lexicon.json        what each term means (hand-authored)
    curation/gnosticism/raw-findings.json   where it occurs (machine sweep)
        -> curation/gnosticism/register.json

The register is what the site's Gnostic Lexicon page renders. Every row carries
its own evidence: how often Dick used the word, in which corpus, when he first
and last used it, and two or three exemplar passages with their segment ids.

An entry with zero attestations is kept, not dropped. "Dick never wrote this
word" is a finding about Dick, and the register is the only place it is
recorded — see curation/gnosticism/README.md.

    python scripts/research/build_gnostic_register.py
"""

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
CUR = PROJECT_DIR / 'curation' / 'gnosticism'

# Exemplars are chosen from Dick's own words, never from editor annotation.
MAX_EXEMPLARS = 3
MIN_EXEMPLAR_CHARS = 120


# The Exegesis transcription carries folder dates, not per-entry dates: every
# segment in a batch inherits one date. The four batches differ in size, so raw
# per-year counts are confounded by how much text each folder holds. Rates are
# reported alongside counts, and comparisons should use the rates.
def folder_sizes():
    sizes = Counter()
    seg_dir = PROJECT_DIR / 'site' / 'public' / 'data' / 'segments'
    for p in seg_dir.glob('SEG_*.json'):
        try:
            d = json.loads(p.read_text(encoding='utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        ds = str(d.get('date_start') or '')
        if re.match(r'\d{4}', ds):
            sizes[ds[:4]] += 1
    return dict(sizes)


def year_of(rec):
    d = rec.get('date') or ''
    m = re.match(r'(\d{4})', str(d))
    return m.group(1) if m else None


def pick_exemplars(hits):
    """Prefer long, dated, Exegesis-or-fiction contexts in Dick's own words."""
    cands = [h for h in hits
             if h['field_class'] == 'pkd_text'
             and len(h['context']) >= MIN_EXEMPLAR_CHARS]
    if not cands:
        cands = [h for h in hits if h['field_class'] == 'pkd_text'] or hits

    def key(h):
        return (
            0 if h['corpus'] in ('exegesis', 'valis_trilogy', 'letters') else 1,
            0 if h.get('date') else 1,
            -len(h['context']),
        )

    out, seen_src = [], set()
    for h in sorted(cands, key=key):
        if h['source_id'] in seen_src:
            continue          # spread exemplars across different sittings
        seen_src.add(h['source_id'])
        out.append({
            'corpus': h['corpus'],
            'lane': h['lane'],
            'source_id': h['source_id'],
            'doc_id': h.get('doc_id'),
            'slug': h.get('slug'),
            'title': h.get('title'),
            'date_display': h.get('date_display'),
            'matched': h['matched'],
            'passage': h['context'],
        })
        if len(out) >= MAX_EXEMPLARS:
            break
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lexicon', default=str(CUR / 'lexicon.json'))
    ap.add_argument('--findings', default=str(CUR / 'raw-findings.json'))
    ap.add_argument('--out', default=str(CUR / 'register.json'))
    args = ap.parse_args()

    sizes = folder_sizes()
    lex = json.loads(Path(args.lexicon).read_text(encoding='utf-8'))
    raw = json.loads(Path(args.findings).read_text(encoding='utf-8'))

    counts = {r['entry_id']: r for r in raw['attestation_counts']}
    by_entry = defaultdict(list)
    for h in raw['attestations']:
        by_entry[h['entry_id']].append(h)

    rows = []
    for e in lex['entries']:
        c = counts.get(e['id'], {})
        hits = by_entry.get(e['id'], [])
        pkd_hits = [h for h in hits if h['field_class'] == 'pkd_text']

        # Exact, from the full sweep — not from the capped context sample.
        yc = Counter(c.get('exegesis_by_year') or {})
        years = sorted(yc)

        total = c.get('total', 0)
        direct = c.get('pkd_text', 0)
        if direct:
            status = 'attested'
        elif total:
            status = 'annotation_only'
        else:
            status = 'unattested'

        rows.append({
            'entry_id': e['id'],
            'label': e['label'],
            'slug': re.sub(r'[^a-z0-9]+', '-',
                           e['label'].lower()).strip('-'),
            'category': e['category'],
            'tradition': e['tradition'],
            'greek': e.get('greek'),
            'gloss': e['gloss'],
            'why_pkd': e['why_pkd'],
            'key_sources': e['key_sources'],
            'status': status,
            'attestations': {
                'total': total,
                'pkd_text': direct,
                'editor_annotation': c.get('editor_annotation', 0),
                'exegesis': c.get('exegesis', 0),
                'letters': c.get('letters', 0),
                'valis_trilogy': c.get('valis_trilogy', 0),
                'scholarship': c.get('scholarship', 0),
            },
            'first_attested': years[0] if years else None,
            'last_attested': years[-1] if years else None,
            'peak_year': (max(yc.items(), key=lambda kv: (kv[1], kv[0]))[0]
                          if yc else None),
            'by_year': dict(sorted(yc.items())),
            # hits per segment in that folder — the comparable figure
            'by_year_rate': {y: round(n / sizes[y], 3)
                             for y, n in sorted(yc.items()) if sizes.get(y)},
            'exemplars': pick_exemplars(hits),
        })

    rows.sort(key=lambda r: (-r['attestations']['pkd_text'], r['label']))
    by_cat = Counter(r['category'] for r in rows)
    by_status = Counter(r['status'] for r in rows)

    out = {
        'artifact_type': 'gnostic_register',
        'generator': 'scripts/research/build_gnostic_register.py',
        'sources': {
            'lexicon': 'curation/gnosticism/lexicon.json',
            'findings': 'curation/gnosticism/raw-findings.json',
        },
        'corpus_coverage': raw['sources_scanned'],
        'exegesis_folder_sizes': sizes,
        'chronology_caveat': (
            'Exegesis dates are folder dates: every segment in a transcription '
            'batch inherits one date, and the four batches differ in size. '
            'Compare by_year_rate (hits per segment), not by_year.'),
        'entry_count': len(rows),
        'by_category': dict(by_cat),
        'by_status': dict(by_status),
        'entries': rows,
    }
    Path(args.out).write_text(
        json.dumps(out, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(f'wrote {args.out}  ({len(rows)} entries)')
    for k, v in sorted(by_status.items()):
        print(f'  {k:18s} {v}')
    print(f'\nAttested in Dick\'s own words, by category:')
    att = Counter(r['category'] for r in rows if r['status'] == 'attested')
    for k in sorted(att):
        print(f'  {k:16s} {att[k]}/{by_cat[k]}')


if __name__ == '__main__':
    main()
