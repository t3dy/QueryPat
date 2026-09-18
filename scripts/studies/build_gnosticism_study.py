#!/usr/bin/env python3
"""
Assemble the Gnosticism study from the durable curation sources.

    curation/gnosticism/lexicon.json          term register (hand-authored)
    curation/gnosticism/register.json         lexicon joined to attestations
    curation/gnosticism/dossier_sections.py   editorial prose (hand-authored)

Writes:
    curation/gnosticism/dossier.json                  prose, as a data artifact
    site/public/data/studies/gnosticism/index.json    topic index
    site/public/data/studies/gnosticism/topics/*.json topic detail
    site/public/data/studies/gnosticism/register.json the Gnostic Lexicon page
    site/public/data/studies/index.json               study added to the index

Nothing editorial is hardcoded here: the prose comes from dossier_sections.py
and every passage is a verbatim excerpt the sweep found in the corpus. Re-running
this after a fresh sweep rebuilds the pages exactly.

    python scripts/studies/build_gnosticism_study.py
    python scripts/studies/build_gnosticism_study.py --check
"""

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
CUR = PROJECT_DIR / 'curation' / 'gnosticism'
OUT = PROJECT_DIR / 'site' / 'public' / 'data' / 'studies' / 'gnosticism'
STUDIES_INDEX = PROJECT_DIR / 'site' / 'public' / 'data' / 'studies' / 'index.json'
SEARCH_INDEX = PROJECT_DIR / 'site' / 'public' / 'data' / 'search_index.json'

STUDY_ID = 'gnosticism'
GENERATOR = 'curation/gnosticism@2026-09-18'

SOURCE_MODE = {
    'exegesis': 'exegesis',
    'letters': 'letters',
    'valis_trilogy': 'fiction',
    'valis_trilogy_summaries': 'editorial_summary',
    'scholarship': 'scholarship',
}


def load_cards():
    spec = importlib.util.spec_from_file_location(
        'gnostic_mention_cards', CUR / 'mention_cards.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# Cards are grouped on the page by where they come from and when. Exegesis
# folders get their own group because the folder IS the unit of dating.
def group_cards(cards):
    """Assign each card a group key, and return the group definitions used."""
    defs, order = {}, []
    for c in cards:
        st = c['source_type']
        if st == 'exegesis_segment':
            key = 'exeg-' + (c.get('dated') or 'undated').replace(' ', '-').replace(',', '')
            label = f"The Exegesis — {c.get('dated') or 'undated'}"
            blurb = ('One folder of the transcription. Every segment in a batch '
                     'carries the same date, so this is a sitting, not a day.')
        elif st == 'fiction':
            key, label = 'fiction', 'The novels'
            blurb = 'Published text of the VALIS trilogy, as held in this repository.'
        elif st == 'letter':
            key, label = 'letters', 'Letters'
            blurb = ('Correspondence. The letters held here as full text are the '
                     '1972-73 volume, which predates 2-3-74.')
        elif st == 'criticism':
            key, label = 'scholarship', 'Biography and scholarship'
            blurb = 'What scholars argue — not Dick.'
        elif st == 'editorial_summary':
            key, label = 'summaries', 'Portal-editor chapter summaries'
            blurb = ('Lane D. Editorial prose about the novels, never quoted as '
                     "Dick's words.")
        else:
            key, label, blurb = st, st, ''
        c['group_key'] = key
        if key not in defs:
            defs[key] = {'key': key, 'label': label, 'blurb': blurb}
            order.append(key)
    # Exegesis folders first and in date order, then fiction, then the rest.
    def rank(k):
        if k.startswith('exeg-'):
            return (0, next(c['date'] or '' for c in cards if c['group_key'] == k))
        return ({'fiction': 1, 'letters': 2, 'summaries': 3,
                 'scholarship': 4}.get(k, 5), k)
    return [defs[k] for k in sorted(order, key=rank)]


CITE_RE = re.compile(r'\{\{([A-Za-z0-9-]+)\}\}')

# Quotations of this length or more are machine-checked against the corpus on
# every build, the way the Burroughs dossier checks its own. Shorter fragments
# are too common to verify usefully.
MIN_VERIFIED_QUOTE = 40


def quoted_spans(text):
    """The quoted runs in a paragraph.

    Straight quotes open and close alike, so the quoted runs are the odd
    segments of a split. Matching a regex across a pair would capture the
    narration between two quotations instead.
    """
    parts = text.split('"')
    return [parts[i] for i in range(1, len(parts), 2)]


def normalise(text):
    """Fold typography, not words.

    The transcription varies in quote style, dashes, soft hyphens, spacing and
    case; none of that is a difference in what Dick wrote. Anything else is.
    """
    t = text.lower()
    t = t.replace('\u2019', "'").replace('\u2018', "'")
    t = t.replace('\u201c', '"').replace('\u201d', '"')
    t = t.replace('\u2014', '-').replace('\u2013', '-').replace('\u2011', '-')
    t = t.replace('\u00ad', '').replace('\u2010', '-')
    # A word broken across a line: "demi- urge" is "demiurge", not two words.
    t = re.sub(r'(\w)[-\u2010\u2011]\s+(\w)', r'\1\2', t)
    t = re.sub(r'[^a-z0-9]+', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()


def verify_quotations(sections, haystack):
    """Return the quotations in these sections that are not in the corpus."""
    missing = []
    for sec in sections:
        for para in sec['body']:
            # Strip citation markers first; they are not part of the quotation.
            clean = CITE_RE.sub('', para)
            for raw_quote in quoted_spans(clean):
                if len(raw_quote) < MIN_VERIFIED_QUOTE:
                    continue
                quote = raw_quote.strip(' .,;')
                # Ellipses mark an elision, so check the parts either side.
                parts = [q for q in re.split(r'\s*[.]{3}|\s*\u2026\s*', quote)
                         if len(q.strip()) >= 25]
                for part in (parts or [quote]):
                    if normalise(part) not in haystack:
                        missing.append((sec['id'], part[:90]))
    return missing


def check_citations(slug, sections, cards):
    """Every {{marker}} must resolve to a card on this same topic."""
    ids = {c['id'] for c in cards}
    bad = []
    for sec in sections:
        for para in sec['body']:
            for m in CITE_RE.finditer(para):
                if m.group(1) not in ids:
                    bad.append((sec['id'], m.group(1)))
    return bad


def load_prose():
    spec = importlib.util.spec_from_file_location(
        'gnostic_dossier', CUR / 'dossier_sections.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def topic_id(slug):
    return 'TOPIC_GNOS_' + slug.replace('-', '_')


def build_packets(topic, reg_index, counter):
    """One evidence packet per focus term, carrying its exemplar passages."""
    packets = []
    for entry_id in topic.get('lexicon_focus', []):
        r = reg_index.get(entry_id)
        if not r:
            continue
        a = r['attestations']
        passages = []
        for x in r['exemplars']:
            counter[0] += 1
            passages.append({
                'passage_id': counter[0],
                'lane': x['lane'],
                'source_mode': SOURCE_MODE.get(x['corpus'], x['corpus']),
                'doc_id': x.get('doc_id'),
                'doc_title': x.get('title'),
                'passage_text': x['passage'],
                'matched_terms': [x['matched']],
                'claim_type': 'attestation',
                'confidence': 'high' if a['pkd_text'] else 'low',
                'seg_id': x['source_id'],
                'citation': f"{x.get('title') or x['source_id']}"
                            + (f" — {x['date_display']}" if x.get('date_display') else ''),
                'date': x.get('date_display'),
                'slug': x.get('slug'),
            })
        if r['status'] == 'unattested':
            claim = (f"{r['label']} is never named in Dick's own words anywhere "
                     f"in the corpus swept.")
            summary = (f"Zero attestations across 1,104 Exegesis segments, the "
                       f"letters held here and the trilogy chapters. "
                       f"{r['why_pkd']}")
            conf = 'strong'
        elif r['status'] == 'annotation_only':
            claim = (f"{r['label']} appears only in portal-editor annotation, "
                     f"never in Dick's own words.")
            summary = (f"{a['editor_annotation']} occurrences in analytical "
                       f"fields, none in his text. {r['why_pkd']}")
            conf = 'moderate'
        else:
            bits = []
            if a['exegesis']:
                bits.append(f"{a['exegesis']} in the Exegesis")
            if a['valis_trilogy']:
                bits.append(f"{a['valis_trilogy']} in the trilogy")
            if a['letters']:
                bits.append(f"{a['letters']} in the letters")
            if a['scholarship']:
                bits.append(f"{a['scholarship']} in secondary literature")
            claim = (f"{r['label']} is attested {a['pkd_text']} times in Dick's "
                     f"own words" +
                     (f", {r['first_attested']}-{r['last_attested']}."
                      if r['first_attested'] else '.'))
            summary = ('; '.join(bits) + '. ' + r['why_pkd']) if bits else r['why_pkd']
            conf = 'strong' if a['pkd_text'] >= 20 else 'moderate'

        packets.append({
            'ev_id': f"PKT_GNOS_{entry_id.replace('GNOS_', '').upper()}",
            'claim_text': claim,
            'evidence_summary': summary,
            'confidence': conf,
            'source_method': 'corpus_sweep',
            'lane_a_count': sum(1 for p in passages if p['lane'] == 'A'),
            'lane_b_count': sum(1 for p in passages if p['lane'] == 'B'),
            'lane_c_count': sum(1 for p in passages if p['lane'] == 'C'),
            'passages': passages,
            'term': {
                'entry_id': r['entry_id'],
                'label': r['label'],
                'slug': r['slug'],
                'category': r['category'],
                'tradition': r['tradition'],
                'greek': r.get('greek'),
                'gloss': r['gloss'],
                'status': r['status'],
                'attestations': a,
                'by_year': r['by_year'],
                'by_year_rate': r['by_year_rate'],
                'key_sources': r['key_sources'],
            },
        })
    return packets


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true',
                    help='validate sources and report, writing nothing')
    args = ap.parse_args()

    prose = load_prose()
    lex = json.loads((CUR / 'lexicon.json').read_text(encoding='utf-8'))
    reg = json.loads((CUR / 'register.json').read_text(encoding='utf-8'))
    reg_index = {r['entry_id']: r for r in reg['entries']}

    missing = [fid for t in prose.TOPICS for fid in t.get('lexicon_focus', [])
               if fid not in reg_index]
    if missing:
        print('ERROR: topics reference unknown lexicon entries: '
              + ', '.join(sorted(set(missing))))
        return 1
    if args.check:
        print(f'lexicon {len(lex["entries"])} entries; register '
              f'{reg["entry_count"]} rows; {len(prose.TOPICS)} topics; '
              f'all focus terms resolve.')
        return 0

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'topics').mkdir(exist_ok=True)

    mc = load_cards()
    raw = json.loads((CUR / 'raw-findings.json').read_text(encoding='utf-8'))
    cards_by_topic = mc.build(raw, reg, prose.TOPICS)

    # Refuse to publish a citation that does not resolve. A stale marker must
    # fail the build, not reach the page as a dead superscript.
    failures = []
    for t in prose.TOPICS:
        secs = getattr(prose, 'DOSSIER_SECTIONS', {}).get(t['slug']) or []
        for sec_id, marker in check_citations(
                t['slug'], secs, cards_by_topic.get(t['slug'], [])):
            failures.append(f"{t['slug']}/{sec_id}: {{{{{marker}}}}}")
    # Every long quotation in the prose must appear verbatim in the corpus.
    haystack = normalise(' '.join(
        h['context'] for h in raw['attestations']))
    for t in prose.TOPICS:
        secs = getattr(prose, 'DOSSIER_SECTIONS', {}).get(t['slug']) or []
        for sec_id, quote in verify_quotations(secs, haystack):
            failures.append(f"{t['slug']}/{sec_id}: unverified quotation \u2014 "
                            f"\"{quote}\"")

    if failures:
        print('ERROR: unresolved citation markers or unverified quotations:',
              file=sys.stderr)
        for f in failures:
            print('  ' + f, file=sys.stderr)
        return 1

    counter = [0]
    topic_rows, dossier_topics = [], []

    for t in prose.TOPICS:
        topic_cards = cards_by_topic.get(t['slug'], [])
        groups = group_cards(topic_cards)
        packets = build_packets(t, reg_index, counter)
        passage_count = sum(len(p['passages']) for p in packets)
        lanes = {'A': 0, 'B': 0, 'C': 0}
        for p in packets:
            for pg in p['passages']:
                if pg['lane'] in lanes:
                    lanes[pg['lane']] += 1
        focus = [reg_index[f] for f in t.get('lexicon_focus', [])]
        firsts = sorted(r['first_attested'] for r in focus if r['first_attested'])

        detail = {
            'topic_id': topic_id(t['slug']),
            'study_id': STUDY_ID,
            'canonical_name': t['canonical_name'],
            'slug': t['slug'],
            'status': t['status'],
            'generator': GENERATOR,
            'provenance': 'editorial_curation_from_corpus_sweep',
            'definition': t['definition'],
            'pkd_relevance': t['pkd_relevance'],
            'in_the_fiction': t.get('in_the_fiction'),
            'in_the_exegesis': t.get('in_the_exegesis'),
            'intellectual_background': t.get('intellectual_background'),
            'scholarly_debate': t.get('scholarly_debate'),
            'chronology_summary': t.get('chronology_summary'),
            'contradictions_summary': t.get('contradictions_summary'),
            'related_thinkers': t.get('related_thinkers', []),
            'editorial_notes': t.get('editorial_notes'),
            'open_questions': t.get('open_questions', []),
            'passage_count': passage_count,
            'evidence_count': len(packets),
            'contradiction_count': 1 if t.get('contradictions_summary') else 0,
            'first_appearance': firsts[0] if firsts else None,
            'peak_period_start': firsts[0] if firsts else None,
            'peak_period_end': max(
                (r['last_attested'] for r in focus if r['last_attested']),
                default=None),
            'dossier_sections': getattr(prose, 'DOSSIER_SECTIONS', {}).get(
                t['slug']) or [],
            'mention_cards': topic_cards,
            'mention_groups': groups,
            'evidence_packets': packets,
            'contradictions': [],
            'chronology': [],
            'related_documents': [],
            'related_terms': [
                {'term_id': r['entry_id'], 'canonical_name': r['label'],
                 'slug': r['slug'], 'relation_type': 'primary'}
                for r in focus
            ],
            'related_names': [],
            'related_topics': [
                {'topic_id': topic_id(o['slug']),
                 'canonical_name': o['canonical_name'],
                 'slug': o['slug'], 'study_id': STUDY_ID}
                for o in prose.TOPICS if o['slug'] != t['slug']
            ],
        }
        (OUT / 'topics' / f"{t['slug']}.json").write_text(
            json.dumps(detail, indent=2, ensure_ascii=False) + '\n',
            encoding='utf-8')
        dossier_topics.append(detail)

        topic_rows.append({
            'topic_id': detail['topic_id'],
            'canonical_name': t['canonical_name'],
            'slug': t['slug'],
            'status': t['status'],
            'priority': t['priority'],
            'card_description': t['card_description'],
            'passage_count': passage_count,
            'evidence_count': len(packets),
            'contradiction_count': detail['contradiction_count'],
            'first_appearance': detail['first_appearance'],
            'lane_distribution': lanes,
            'related_topics': [o['canonical_name'] for o in prose.TOPICS
                               if o['slug'] != t['slug']],
            'mention_count': len(topic_cards),
            'section_count': len(detail['dossier_sections']),
        })

    topic_rows.sort(key=lambda r: (-r['priority'], r['canonical_name']))

    index = {
        'study_id': STUDY_ID,
        'study_label': prose.STUDY_LABEL,
        'study_description': prose.STUDY_DESCRIPTION,
        'generator': GENERATOR,
        'featured_sections': [
            {'title': s['title'], 'body': s['body']} for s in prose.STUDY_SECTIONS
        ],
        'register_summary': {
            'entry_count': reg['entry_count'],
            'by_category': reg['by_category'],
            'by_status': reg['by_status'],
            'corpus_coverage': reg['corpus_coverage'],
        },
        'topics': topic_rows,
    }
    (OUT / 'index.json').write_text(
        json.dumps(index, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

    # The Gnostic Lexicon page renders the register directly.
    (OUT / 'register.json').write_text(
        json.dumps(reg, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

    # Durable prose artifact.
    (CUR / 'dossier.json').write_text(json.dumps({
        'artifact_type': 'gnosticism_dossier',
        'generator': GENERATOR,
        'study_id': STUDY_ID,
        'study_label': prose.STUDY_LABEL,
        'study_description': prose.STUDY_DESCRIPTION,
        'featured_sections': prose.STUDY_SECTIONS,
        'topics': dossier_topics,
    }, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

    # Register the study in the studies index, in place.
    studies = json.loads(STUDIES_INDEX.read_text(encoding='utf-8'))
    row = {
        'study_id': STUDY_ID,
        'study_label': prose.STUDY_LABEL,
        'study_description': prose.STUDY_DESCRIPTION,
        'topic_count': len(topic_rows),
        'published_count': sum(1 for r in topic_rows
                               if r['status'] in ('published', 'reviewed')),
        'total_passages': sum(r['passage_count'] for r in topic_rows),
        'total_evidence_packets': sum(r['evidence_count'] for r in topic_rows),
        'total_contradictions': sum(r['contradiction_count'] for r in topic_rows),
    }
    studies = [s for s in studies if s.get('study_id') != STUDY_ID] + [row]
    studies.sort(key=lambda s: s['study_id'])
    STUDIES_INDEX.write_text(
        json.dumps(studies, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

    # Search entries, per STUDY_JSON_CONTRACTS.md section 6. Idempotent: this
    # drops the rows it wrote last time before adding them again, so re-running
    # never duplicates. scripts/rebuild_search_index_terms.py rewrites the
    # "term" rows only and leaves these alone.
    search = json.loads(SEARCH_INDEX.read_text(encoding='utf-8'))
    search = [r for r in search
              if not str(r.get('id', '')).startswith(('TOPIC_GNOS_', 'GNOS_'))]
    for t, row in zip(prose.TOPICS, topic_rows):
        search.append({
            'type': 'study_topic',
            'id': row['topic_id'],
            'slug': t['slug'],
            'title': t['canonical_name'],
            'study_id': STUDY_ID,
            'text': t['card_description'] + ' ' + t['definition'],
            'route': f"/studies/{STUDY_ID}/{t['slug']}",
        })
    for r in reg['entries']:
        search.append({
            'type': 'gnostic_term',
            'id': r['entry_id'],
            'slug': r['slug'],
            'title': r['label'],
            'study_id': STUDY_ID,
            'text': f"{r['tradition']}. {r['gloss']} {r['why_pkd']}",
            'route': f"/studies/{STUDY_ID}/lexicon",
        })
    SEARCH_INDEX.write_text(
        json.dumps(search, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(f'search_index.json: +{len(prose.TOPICS)} topics, '
          f'+{reg["entry_count"]} lexicon entries')

    print(f'wrote {OUT}')
    for r in topic_rows:
        print(f"  {r['slug']:26s} {r['evidence_count']:3d} packets  "
              f"{r['passage_count']:3d} passages  {r['mention_count']:3d} cards  "
              f"{r['section_count']:2d} sections")
    print(f'  register.json  {reg["entry_count"]} lexicon entries')
    print(f'registered "{STUDY_ID}" in {STUDIES_INDEX}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
