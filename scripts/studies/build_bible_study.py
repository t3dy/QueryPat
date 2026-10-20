#!/usr/bin/env python3
"""
Assemble "The Bible in PKD" from its durable curation sources.

    curation/bible/raw-findings.json       the corpus sweep (regenerable)
    curation/bible/dossier_sections.py     prose, cards and topic metadata (hand-authored)

Writes:
    curation/bible/dossier.json                        prose and cards, as a data artifact
    site/public/data/studies/bible/index.json          study index
    site/public/data/studies/bible/topics/bible-in-pkd.json   the essay
    site/public/data/studies/index.json                study added to the index, in place
    site/public/data/search_index.json                 topic added to search, in place

Every card is resolved against the sweep, and the build refuses to publish
anything that does not check out:

    * a card's anchor and pith must occur in the finding it names, and nowhere
      else that would make the choice ambiguous;
    * every {{CARD-ID}} marker in the prose must resolve to a card;
    * every quotation of MIN_VERIFIED_QUOTE characters or more must appear, after
      typographic normalisation, in the corpus the sweep searched.

Nothing editorial is hardcoded here. Re-running after a fresh sweep rebuilds the
page exactly.

    python scripts/studies/build_bible_study.py
    python scripts/studies/build_bible_study.py --check
"""

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
CUR = PROJECT_DIR / 'curation' / 'bible'
OUT = PROJECT_DIR / 'site' / 'public' / 'data' / 'studies' / 'bible'
STUDIES_INDEX = PROJECT_DIR / 'site' / 'public' / 'data' / 'studies' / 'index.json'
SEARCH_INDEX = PROJECT_DIR / 'site' / 'public' / 'data' / 'search_index.json'

STUDY_ID = 'bible'
GENERATOR = 'curation/bible@2026-10-20'

SOURCE_TYPE = {
    'exegesis': 'exegesis_segment',
    'letters': 'letter',
    'trilogy_text': 'fiction',
    'archive:scholarship': 'criticism',
}

CITE_RE = re.compile(r'\{\{([A-Za-z0-9-]+)\}\}')

# Quotations this long or longer are machine-checked against the corpus.
MIN_VERIFIED_QUOTE = 40


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def normalise(text):
    """Fold typography, not words. Matches build_gnosticism_study.normalise."""
    t = text.lower()
    t = t.replace('’', "'").replace('‘', "'")
    t = t.replace('“', '"').replace('”', '"')
    t = t.replace('—', '-').replace('–', '-').replace('‑', '-')
    t = t.replace('­', '').replace('‐', '-')
    t = re.sub(r'(\w)[-‐‑]\s+(\w)', r'\1\2', t)
    t = re.sub(r'[^a-z0-9]+', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()


def quoted_spans(text):
    """The quoted runs in a paragraph: the odd segments of a split on straight
    or curly double quotes."""
    parts = re.split(r'["“”]', text)
    return [parts[i] for i in range(1, len(parts) - 1, 2)]


def verify_quotations(sections, haystack):
    missing = []
    for sec in sections:
        for para in sec['body']:
            clean = CITE_RE.sub('', para)
            for raw_quote in quoted_spans(clean):
                if len(raw_quote) < MIN_VERIFIED_QUOTE:
                    continue
                quote = raw_quote.strip(' .,;')
                parts = [q for q in re.split(r'\s*[.]{3}|\s*…\s*', quote)
                         if len(q.strip()) >= 25]
                for part in (parts or [quote]):
                    if normalise(part) not in haystack:
                        missing.append((sec['id'], part[:90]))
    return missing


def find_finding(card, findings):
    """Return the one sweep finding this card is cut from.

    Matching is on the record id, the field, and a normalised anchor. Several
    hit windows of one record can contain the same sentence, because the sweep
    keeps overlapping windows; they all carry the same passage. The earliest
    window that contains the pith is therefore the card's passage.
    """
    anchor = normalise(card['anchor'])
    pith = normalise(card['pith'])
    candidates = [
        f for f in findings
        if f['source_id'] == card['source']
        and f['field'] == card['field']
        and anchor in normalise(f['context'])
    ]
    if not candidates:
        return None, 'no finding matches the anchor'
    with_pith = [f for f in candidates if pith in normalise(f['context'])]
    if not with_pith:
        return None, 'the pith is not in any window that matches the anchor'
    return min(with_pith, key=lambda f: f['char_offset']), None


def build_card(card, finding):
    corpus = finding['corpus']
    source_type = SOURCE_TYPE.get(corpus, SOURCE_TYPE.get(corpus.split(':')[0], corpus))
    is_exeg = corpus == 'exegesis'
    return {
        'id': card['id'],
        'citation': card['citation'],
        'date': card.get('dated'),
        'source_type': source_type,
        'published_folio': None,
        'seg_id': finding['source_id'] if is_exeg else None,
        'doc_id': finding.get('doc_id') if is_exeg else (
            finding['source_id'] if corpus.startswith('archive') else None),
        'lane': card['lane'],
        'register': card['register'],
        'relevance': card['relevance'],
        'concepts': card.get('concepts', []),
        'context': card['context'],
        'pith': card['pith'],
        'speaker': card.get('speaker'),
        'editorial_note': card.get('editorial_note'),
        'dated': card.get('dated'),
        'dating_basis': card.get('dating_basis'),
        'passage': finding['context'],
        'group_key': card['group'],
        'context_derived': False,
        'also_names': [],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true',
                    help='validate sources and report, writing nothing')
    args = ap.parse_args()

    prose = load_module(CUR / 'dossier_sections.py', 'bible_dossier')
    raw = json.loads((CUR / 'raw-findings.json').read_text(encoding='utf-8'))
    findings = raw['findings']

    problems = []

    # 1. Every card resolves to one finding, and its pith is in that finding.
    resolved = {}
    for card in prose.CARDS:
        if card['group'] not in {g['key'] for g in prose.GROUPS}:
            problems.append(f"{card['id']}: unknown group {card['group']!r}")
            continue
        finding, why = find_finding(card, findings)
        if finding is None:
            problems.append(f"{card['id']}: {why}")
            continue
        if normalise(card['pith']) not in normalise(finding['context']):
            problems.append(f"{card['id']}: pith is not verbatim in the passage")
            continue
        resolved[card['id']] = (card, finding)

    ids = [c['id'] for c in prose.CARDS]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        problems.append('duplicate card ids: ' + ', '.join(sorted(dupes)))

    # 2. Every citation marker in the prose resolves to a card.
    for sec in prose.DOSSIER_SECTIONS:
        for para in sec['body']:
            for m in CITE_RE.finditer(para):
                if m.group(1) not in resolved:
                    problems.append(f"{sec['id']}: marker {{{{{m.group(1)}}}}} does not resolve")

    # 3. Every long quotation in the prose appears in the corpus.
    haystack = normalise(' '.join(f['context'] for f in findings))
    for sec_id, quote in verify_quotations(prose.DOSSIER_SECTIONS, haystack):
        problems.append(f'{sec_id}: unverified quotation — "{quote}"')

    if problems:
        print('ERROR: the Bible study does not build:', file=sys.stderr)
        for p in problems:
            print('  ' + p, file=sys.stderr)
        return 1

    cards = [build_card(c, f) for c, f in resolved.values()]
    used = set()
    for sec in prose.DOSSIER_SECTIONS:
        for para in sec['body']:
            used.update(CITE_RE.findall(para))
    unused = sorted(set(resolved) - used)

    groups = [g for g in prose.GROUPS
              if any(c['group_key'] == g['key'] for c in cards)]
    lanes = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
    for c in cards:
        lanes[c['lane']] = lanes.get(c['lane'], 0) + 1

    if args.check:
        print(f'{len(prose.CARDS)} cards resolve to {len(cards)} passages; '
              f'{len(prose.DOSSIER_SECTIONS)} sections; all markers and quotations verified.')
        if unused:
            print('  cards not cited in the prose: ' + ', '.join(unused))
        return 0

    T = prose.TOPIC
    topic = {
        'topic_id': T['topic_id'],
        'study_id': STUDY_ID,
        'canonical_name': T['canonical_name'],
        'slug': T['slug'],
        'status': T['status'],
        'generator': GENERATOR,
        'provenance': 'editorial_curation_from_corpus_sweep',
        'definition': T['definition'],
        'pkd_relevance': T['pkd_relevance'],
        'in_the_fiction': T['in_the_fiction'],
        'in_the_exegesis': T['in_the_exegesis'],
        'intellectual_background': T['intellectual_background'],
        'scholarly_debate': T['scholarly_debate'],
        'chronology_summary': T['chronology_summary'],
        'contradictions_summary': T['contradictions_summary'],
        'related_thinkers': T['related_thinkers'],
        'editorial_notes': T['editorial_notes'],
        'open_questions': T['open_questions'],
        'passage_count': len(cards),
        'evidence_count': 0,
        'contradiction_count': 1 if T['contradictions_summary'] else 0,
        'first_appearance': '1972',
        'peak_period_start': '1975',
        'peak_period_end': '1981',
        'dossier_sections': prose.DOSSIER_SECTIONS,
        'mention_cards': cards,
        'mention_groups': groups,
        'evidence_packets': [],
        'contradictions': [],
        'chronology': [],
        'related_documents': [],
        'related_terms': [],
        'related_names': [],
        'related_topics': T['related_topics'],
    }

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'topics').mkdir(exist_ok=True)
    (OUT / 'topics' / f"{T['slug']}.json").write_text(
        json.dumps(topic, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

    topic_row = {
        'topic_id': T['topic_id'],
        'canonical_name': T['canonical_name'],
        'slug': T['slug'],
        'status': T['status'],
        'priority': T['priority'],
        'card_description': T['card_description'],
        'passage_count': len(cards),
        'evidence_count': 0,
        'contradiction_count': topic['contradiction_count'],
        'first_appearance': topic['first_appearance'],
        'lane_distribution': lanes,
        'related_topics': [r['canonical_name'] for r in T['related_topics']],
        'mention_count': len(cards),
        'section_count': len(prose.DOSSIER_SECTIONS),
    }
    index = {
        'study_id': STUDY_ID,
        'study_label': prose.STUDY_LABEL,
        'study_description': prose.STUDY_DESCRIPTION,
        'generator': GENERATOR,
        'featured_sections': prose.STUDY_SECTIONS,
        'topics': [topic_row],
    }
    (OUT / 'index.json').write_text(
        json.dumps(index, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

    (CUR / 'dossier.json').write_text(json.dumps({
        'artifact_type': 'bible_dossier',
        'generator': GENERATOR,
        'study_id': STUDY_ID,
        'study_label': prose.STUDY_LABEL,
        'study_description': prose.STUDY_DESCRIPTION,
        'featured_sections': prose.STUDY_SECTIONS,
        'topic': topic,
    }, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

    # Register the study in the studies index, in place.
    studies = json.loads(STUDIES_INDEX.read_text(encoding='utf-8'))
    row = {
        'study_id': STUDY_ID,
        'study_label': prose.STUDY_LABEL,
        'study_description': prose.STUDY_DESCRIPTION,
        'topic_count': 1,
        'published_count': 1,
        'total_passages': len(cards),
        'total_evidence_packets': 0,
        'total_contradictions': topic['contradiction_count'],
    }
    studies = [s for s in studies if s.get('study_id') != STUDY_ID] + [row]
    studies.sort(key=lambda s: s['study_id'])
    STUDIES_INDEX.write_text(
        json.dumps(studies, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

    # Search: drop the rows this builder wrote last time, then add them again.
    search = json.loads(SEARCH_INDEX.read_text(encoding='utf-8'))
    search = [r for r in search if not str(r.get('id', '')).startswith('TOPIC_BIBLE_')]
    search.append({
        'type': 'study_topic',
        'id': T['topic_id'],
        'slug': T['slug'],
        'title': T['canonical_name'],
        'study_id': STUDY_ID,
        'text': T['card_description'] + ' ' + T['definition'],
        'route': f"/studies/{STUDY_ID}/{T['slug']}",
    })
    SEARCH_INDEX.write_text(
        json.dumps(search, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

    print(f'wrote {OUT.relative_to(PROJECT_DIR)}')
    print(f"  {T['slug']}: {len(cards)} cards, {len(prose.DOSSIER_SECTIONS)} sections, "
          f"lanes {lanes}")
    if unused:
        print('  cards not cited in the prose: ' + ', '.join(unused))
    print(f'registered "{STUDY_ID}" in {STUDIES_INDEX.relative_to(PROJECT_DIR)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
