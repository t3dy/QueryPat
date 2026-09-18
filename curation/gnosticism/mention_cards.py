#!/usr/bin/env python3
"""
Select and build the mention cards for the Gnosticism study.

A mention card is one passage, summarised and quoted, with everything needed to
check it: its lane, its evidentiary register, the segment it was cut from, and
the verbatim excerpt the summary is based on. The dossier prose cites cards by
id with {{card-id}} markers, and the builder refuses to publish a marker that
does not resolve.

Cards are selected from `raw-findings.json` — never invented. Selection prefers
passages where several of a topic's terms co-occur, because those are the
passages where Dick is doing the work rather than using a word in passing.

`context` is editorial. Where CARD_CONTEXT supplies one it is used verbatim;
otherwise a factual, machine-derived line is written and the card is flagged
`context_derived` so the two are never confused.
"""

import json
import re
from pathlib import Path

CUR = Path(__file__).resolve().parent

SOURCE_TYPE = {
    'exegesis': 'exegesis_segment',
    'letters': 'letter',
    'valis_trilogy': 'fiction',
    'valis_trilogy_summaries': 'editorial_summary',
    'scholarship': 'criticism',
}

# Evidentiary register per corpus. A = PKD's own words; C = scholars;
# D = portal-editor prose.
REGISTER = {
    'exegesis': 'A',
    'letters': 'A',
    'valis_trilogy': 'A',
    'valis_trilogy_summaries': 'D',
    'scholarship': 'C',
}

SPEAKER = {
    'exegesis': 'Philip K. Dick',
    'letters': 'Philip K. Dick',
    'valis_trilogy': 'Philip K. Dick',
    'valis_trilogy_summaries': 'Portal editors',
    'scholarship': None,          # falls back to the document's author
}

TOPIC_PREFIX = {
    'what-dick-actually-read': 'READ',
    'sophia': 'SOPH',
    'black-iron-prison': 'BIP',
    'gnosis-and-anamnesis': 'GNOS',
    'valis-trilogy': 'VALIS',
    'orthodoxy-and-gnosis': 'ORTH',
}

MAX_CARDS_PER_TOPIC = 16
MIN_PASSAGE_CHARS = 150


# ---------------------------------------------------------------------------
# Editorial context, written by hand, keyed by card id.
# Anything not listed here gets a derived factual line instead.
# ---------------------------------------------------------------------------
CARD_CONTEXT: dict[str, str] = {}

# Editorial notes, same convention.
CARD_NOTE: dict[str, str] = {}


def pith_of(passage: str, matched: str) -> str:
    """The sentence the passage turns on, verbatim.

    The Exegesis transcription punctuates erratically, so this falls back to a
    window around the match rather than inventing sentence boundaries. Either
    way the result is trimmed to whole words, so a card never opens or closes
    mid-word.
    """
    body = re.sub(r'\s+', ' ', passage.strip('… ')).strip()
    idx = body.lower().find(matched.lower())
    if idx < 0:
        return _trim(body[:240])
    start = _sentence_start(body, idx)
    end = _sentence_end(body, idx)
    out = body[start:end].strip()
    if len(out) < 40:                       # too short to carry a claim
        out = body[max(0, idx - 110):idx + 150]
    return _trim(out)


# "St. Sophia", "e.g.", "v." and bare initials are not sentence ends. Breaking
# on them truncates a card to two useless words.
ABBREV = {'st', 'dr', 'mr', 'mrs', 'ms', 'fr', 'e.g', 'eg', 'i.e', 'ie', 'v',
          'vs', 'cf', 'qv', 'viz', 'ca', 'c', 'no', 'vol', 'ch', 'pp', 'p',
          'jr', 'sr', 'etc', 'ff'}


def _is_break(body: str, pos: int) -> bool:
    """True if the punctuation at pos really ends a sentence."""
    if body[pos] in '?!;':
        return True
    before = body[:pos]
    tok = re.split(r'[\s(\["]', before)[-1].lower().rstrip('.')
    if tok in ABBREV:
        return False
    if len(tok) == 1 and tok.isalpha():      # a bare initial
        return False
    return True


def _sentence_start(body: str, idx: int) -> int:
    for m in reversed(list(re.finditer(r'[.?!;]', body[:idx]))):
        if _is_break(body, m.start()):
            return m.start() + 1
    return 0


def _sentence_end(body: str, idx: int) -> int:
    for m in re.finditer(r'[.?!;]', body[idx:]):
        pos = idx + m.start()
        if _is_break(body, pos):
            return pos + 1
    return min(len(body), idx + 220)


def _trim(text: str) -> str:
    """Drop partial words at either end, and mark the elision."""
    t = text.strip()
    if not t:
        return t
    if t[0].islower() or t[0].isalnum():
        # If we cut into a word, walk forward to the next boundary.
        sp = t.find(' ')
        if sp > 0 and not t[:sp].endswith(('.', ',', ';')) and len(t[:sp]) < 3:
            t = t[sp + 1:]
    words = t.split(' ')
    if len(words) > 2 and len(words[0]) <= 2 and words[0].isalpha() \
            and words[0].islower():
        words = words[1:]
    t = ' '.join(words).strip()
    if t and t[-1] not in '.?!;"\')':
        t = t.rstrip(' ,-–—') + '…'
    if t and t[0].islower():
        t = '…' + t
    return t


def build(raw, register, topics):
    """Return {topic_slug: [card, ...]}."""
    by_entry = {}
    for h in raw['attestations']:
        by_entry.setdefault(h['entry_id'], []).append(h)

    reg_index = {r['entry_id']: r for r in register['entries']}
    label_of = {r['entry_id']: r['label'] for r in register['entries']}

    # Every lexicon label, for detecting co-occurrence inside a passage.
    all_labels = [(r['entry_id'], r['label']) for r in register['entries']]

    out = {}
    for topic in topics:
        slug = topic['slug']
        focus = topic.get('lexicon_focus', [])
        focus_set = set(focus)

        pool = {}
        for eid in focus:
            for h in by_entry.get(eid, []):
                if h['field_class'] != 'pkd_text' and h['corpus'] != 'scholarship':
                    continue
                if len(h['context']) < MIN_PASSAGE_CHARS:
                    continue
                key = (h['source_id'], h['context'][:80])
                rec = pool.setdefault(key, {'hit': h, 'terms': set()})
                rec['terms'].add(eid)

        # Which corpus a topic should draw from first. The trilogy topic wants
        # the novels; everything else wants the Exegesis, where Dick is
        # reasoning rather than dramatising.
        pref = topic.get('corpus_preference') or [
            'exegesis', 'valis_trilogy', 'letters', 'scholarship']

        def score(rec):
            h = rec['hit']
            try:
                rank = pref.index(h['corpus'])
            except ValueError:
                rank = len(pref)
            return (
                -len(rec['terms'] & focus_set),      # co-occurrence first
                rank,
                -len(h['context']),
            )

        # Round-robin across the topic's focus terms so that a page shows the
        # range of its vocabulary. Ranking alone clusters every card on
        # whichever term happens to sit in the longest passages.
        per_term = {eid: [] for eid in focus}
        for rec in sorted(pool.values(), key=score):
            for eid in sorted(rec['terms'] & focus_set):
                per_term[eid].append(rec)

        chosen, seen_src, seen_text, taken = [], {}, set(), set()
        for round_no in range(MAX_CARDS_PER_TOPIC):
            progressed = False
            for eid in focus:
                if len(chosen) >= MAX_CARDS_PER_TOPIC:
                    break
                queue = per_term.get(eid) or []
                while queue:
                    rec = queue.pop(0)
                    key = id(rec)
                    if key in taken:
                        continue
                    src = rec['hit']['source_id']
                    if seen_src.get(src, 0) >= 2:
                        continue
                    # The transcription duplicates passages across adjacent
                    # segments; a repeat is not new evidence.
                    fingerprint = re.sub(r'[^a-z0-9]+', '',
                                         rec['hit']['context'].lower())[:160]
                    if fingerprint in seen_text:
                        continue
                    seen_text.add(fingerprint)
                    seen_src[src] = seen_src.get(src, 0) + 1
                    taken.add(key)
                    chosen.append(rec)
                    progressed = True
                    break
            if len(chosen) >= MAX_CARDS_PER_TOPIC or not progressed:
                break

        # Chronological within the topic, undated last.
        chosen.sort(key=lambda r: (r['hit'].get('date') or '9999',
                                   r['hit']['source_id']))

        cards = []
        for i, rec in enumerate(chosen, 1):
            h = rec['hit']
            corpus = h['corpus']
            cid = f"GN-{TOPIC_PREFIX.get(slug, 'X')}-{i:02d}"
            passage = h['context']

            concepts = sorted({
                lbl for eid, lbl in all_labels
                if eid in rec['terms']
            })
            others = [label_of[e] for e in sorted(rec['terms'] - focus_set)]

            if cid in CARD_CONTEXT:
                context, derived = CARD_CONTEXT[cid], False
            else:
                r = reg_index.get(sorted(rec['terms'] & focus_set)[0]) \
                    if rec['terms'] & focus_set else None
                where = {
                    'exegesis': 'A passage from the Exegesis folder transcription',
                    'letters': 'A letter',
                    'valis_trilogy': 'From the published novel',
                    'scholarship': 'From the secondary literature',
                    'valis_trilogy_summaries': 'A portal-editor chapter summary',
                }.get(corpus, 'A passage')
                named = ', '.join(concepts[:4])
                context = (
                    f"{where}"
                    + (f" dated {h['date_display']}" if h.get('date_display') else '')
                    + f". Names {named}"
                    + (f", with {len(concepts) - 4} further register terms"
                       if len(concepts) > 4 else '')
                    + '.'
                )
                derived = True

            speaker = SPEAKER.get(corpus)
            if speaker is None:
                speaker = h.get('author') or h.get('title') or 'Secondary source'

            cards.append({
                'id': cid,
                'citation': _citation(h, corpus),
                'date': h.get('date'),
                'source_type': SOURCE_TYPE.get(corpus, corpus),
                'published_folio': None,
                'seg_id': h['source_id'] if corpus == 'exegesis' else None,
                'doc_id': h.get('doc_id'),
                'lane': h['lane'],
                'register': REGISTER.get(corpus, 'D'),
                'relevance': 1 if rec['terms'] & focus_set else 2,
                'concepts': concepts,
                'context': context,
                'context_derived': derived,
                'pith': pith_of(passage, h['matched']),
                'speaker': speaker,
                'editorial_note': CARD_NOTE.get(cid),
                'dated': h.get('date_display'),
                'dating_basis': _basis(corpus, h),
                'passage': passage,
                'also_names': others,
            })
        out[slug] = cards
    return out


def _citation(h, corpus):
    if corpus == 'exegesis':
        return f"Exegesis, {h.get('date_display') or 'undated'}"
    if corpus == 'letters':
        return f"{h.get('title') or 'Letter'}, {h.get('date_display') or 'undated'}"
    if corpus == 'valis_trilogy':
        return h.get('title') or h['source_id']
    if corpus == 'valis_trilogy_summaries':
        return f"{h.get('title') or h['source_id']} (editorial summary)"
    return h.get('title') or h['source_id']


def _basis(corpus, h):
    if corpus == 'exegesis':
        return 'folder'
    if corpus == 'letters':
        return 'dateline'
    if corpus in ('valis_trilogy', 'valis_trilogy_summaries'):
        return 'publication'
    return 'publication'


def load_all():
    raw = json.loads((CUR / 'raw-findings.json').read_text(encoding='utf-8'))
    reg = json.loads((CUR / 'register.json').read_text(encoding='utf-8'))
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        'gnostic_dossier', CUR / 'dossier_sections.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return raw, reg, mod.TOPICS


if __name__ == '__main__':
    raw, reg, topics = load_all()
    cards = build(raw, reg, topics)
    for slug, cs in cards.items():
        print(f'\n{"=" * 78}\n{slug}  ({len(cs)} cards)\n{"=" * 78}')
        for c in cs:
            print(f"\n[{c['id']}] {c['citation']}  lane={c['lane']} reg={c['register']}")
            print(f"  concepts: {', '.join(c['concepts'][:6])}")
            print(f"  PITH: {c['pith'][:300]}")
