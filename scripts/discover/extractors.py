"""
NER and pattern-matching extractors for corpus discovery.

Each extractor scans text and yields typed candidate mentions with context.
No external NLP libraries — regex heuristics only, tuned for the PKD corpus.

Performance note: extractors operate per-chunk. The pipeline is designed
to batch results across all chunks and deduplicate afterward.
"""

import re
from collections import Counter, defaultdict

from .corpus_reader import CorpusChunk

# ── Context extraction ────────────────────────────────────────────

CONTEXT_CHARS = 150  # chars before/after a match for snippets


def _extract_snippet(text: str, start: int, end: int,
                     context: int = CONTEXT_CHARS) -> str:
    """Extract a text snippet around a match position."""
    s = max(0, start - context)
    e = min(len(text), end + context)
    snippet = text[s:e]
    if s > 0:
        first_space = snippet.find(' ')
        if first_space > 0:
            snippet = '...' + snippet[first_space + 1:]
    if e < len(text):
        last_space = snippet.rfind(' ')
        if last_space > 0:
            snippet = snippet[:last_space] + '...'
    return snippet.strip()


# ── Noise filters ─────────────────────────────────────────────────

_STOP_WORDS = frozenset({
    'the', 'this', 'that', 'these', 'those', 'with', 'from', 'into',
    'about', 'after', 'before', 'between', 'through', 'during', 'where',
    'which', 'would', 'could', 'should', 'their', 'there', 'other',
    'more', 'most', 'such', 'also', 'even', 'both', 'each', 'every',
    'much', 'many', 'some', 'only', 'very', 'just', 'than', 'then',
    'when', 'what', 'been', 'were', 'will', 'does', 'have', 'here',
    'perhaps', 'however', 'although', 'because', 'therefore',
    'since', 'while', 'until', 'unless', 'either', 'neither',
    'whether', 'rather', 'quite', 'another', 'nothing', 'something',
    'everything', 'anything', 'himself', 'itself', 'ourselves',
})

_NOISE_CAPS = frozenset({
    'ISBN', 'JSTOR', 'DOI', 'PDF', 'URL', 'HTML', 'XML', 'OCR',
    'USA', 'UK', 'NYC', 'CIA', 'FBI', 'IRS', 'KGB', 'LSD',
    'AD', 'BC', 'CE', 'BCE', 'AM', 'PM', 'ETC', 'INC', 'LTD',
    'VOL', 'ISS', 'FIG', 'SEE', 'THE', 'AND', 'FOR', 'NOT',
    'HIS', 'HER', 'HAS', 'BUT', 'WAS', 'ARE', 'ALL', 'CAN',
    'HAD', 'HIM', 'OUR', 'DID', 'ONE', 'TWO', 'NEW', 'NOW',
    'OLD', 'OWN', 'SAY', 'SHE', 'HOW', 'ITS', 'LET', 'MAY',
    'WHO', 'GOD', 'MAN', 'WAR', 'WAY',
})

_NOT_PERSON = frozenset({
    'Science Fiction', 'United States', 'Black Iron', 'Iron Prison',
    'Palm Tree', 'Tree Garden', 'Living Information', 'Holy Spirit',
    'Holy Wisdom', 'Pink Beam', 'King Felix', 'Active Living',
    'Roman Empire', 'Dark Haired', 'Haired Girl', 'Solar Lottery',
    'New Testament', 'Old Testament', 'Dead Sea', 'Sea Scrolls',
    'High Castle', 'Electric Sheep', 'Rolling Stone',
    'Ace Books', 'Random House', 'Del Rey',
    'North America', 'South America', 'East Coast', 'West Coast',
    'San Francisco', 'San Rafael', 'San Diego', 'San Jose',
    'Los Angeles', 'Los Altos', 'Las Vegas', 'Fort Morgan',
    'Point Reyes', 'Mount Vernon', 'Monte Vista', 'Santa Ana',
    'North Beach', 'North Hollywood', 'South Lake',
    'Publication Data', 'Copyright Page', 'Title Page',
    'First Edition', 'Second Edition', 'Third Edition',
    'Table Contents', 'All Rights', 'Rights Reserved',
    'Page Numbers', 'Works Cited',
})

_AMBIGUOUS_FIRST = frozenset({
    'The', 'This', 'That', 'His', 'Her', 'Its', 'Our', 'Your',
    'One', 'Two', 'New', 'Old', 'All', 'But', 'Not', 'Yet',
    'Now', 'Did', 'Was', 'Has', 'Had', 'May', 'Can', 'Let',
    'See', 'God', 'Man', 'Sir', 'Dr', 'Mr', 'Mrs', 'Ms',
    'Rev', 'Vol', 'Art', 'Part', 'Chapter', 'Section',
    'So', 'My', 'Then', 'Thus', 'Here', 'There', 'What',
    'When', 'Where', 'How', 'Why', 'Who', 'Some', 'Any',
    'Each', 'Every', 'Both', 'Much', 'Such', 'Very', 'Well',
    'Even', 'Just', 'Also', 'Still', 'Only', 'Most', 'More',
    'Like', 'Over', 'Into', 'Upon', 'From', 'With', 'Under',
    'After', 'Being', 'Going', 'Having', 'Making', 'Taking',
    'Because', 'Before', 'Between', 'Through', 'During',
    'Since', 'While', 'Until', 'Rather', 'Though', 'Whether',
    'Indeed', 'Perhaps', 'First', 'Second', 'Third', 'Last',
    'Next', 'Final', 'Early', 'Late', 'Great', 'Little',
    'Long', 'High', 'Low', 'Real', 'True', 'False', 'Good',
    'Bad', 'Same', 'Other', 'Another', 'Either', 'Neither',
    'Nor', 'For', 'And', 'Or', 'If', 'As', 'At', 'By', 'In',
    'Of', 'On', 'To', 'Up', 'No', 'Yes',
})


def _is_noise(phrase: str) -> bool:
    """Check if a phrase is noise."""
    low = phrase.lower().strip()
    if low in _STOP_WORDS:
        return True
    if phrase in _NOISE_CAPS:
        return True
    if len(low) < 3 or re.match(r'^\d+$', low):
        return True
    if re.match(r'^(?:p\.|pp\.|vol\.|no\.|ch\.|fig\.)', low):
        return True
    return False


# ── Compiled patterns (compile once at import time) ───────────────

# Person: "Firstname Lastname"
_RE_PERSON = re.compile(r'\b([A-Z][a-z]{1,15})\s+([A-Z][a-z]{2,20})\b')

# Terms: capitalized multi-word (2-3 words)
_RE_TERM_CAP = re.compile(
    r'\b([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b'
)

# ALL-CAPS terms (3-12 letters)
_RE_TERM_CAPS = re.compile(r'\b([A-Z]{3,12})\b')

# Hyphenated compounds
_RE_TERM_HYPHEN = re.compile(r'\b([A-Z][a-z]+-[a-z]+(?:-[a-z]+)?)\b')

# Works: *Italic Title* or "Quoted Title"
_RE_WORK_ITALIC = re.compile(r'(?<!\w)[*_]([A-Z][^*_\n]{3,60})[*_](?!\w)')
_RE_WORK_QUOTED = re.compile(r'["\u201c]([A-Z][^"\u201d\n]{3,60})["\u201d]')

# Events: "In YYYY, sentence."
_RE_EVENT_YEAR = re.compile(
    r'(?:[Ii]n|[Dd]uring|[Bb]y|[Aa]round)\s+'
    r'(1[89]\d{2}|20[0-2]\d)'
    r'[,\s]+([A-Z][^.!?]{15,200}[.!?])',
)

# Events: "In Month YYYY, sentence."
_RE_EVENT_MONTH = re.compile(
    r'(?:[Ii]n|[Oo]n|[Dd]uring|[Bb]y)\s+'
    r'((?:January|February|March|April|May|June|July|August|'
    r'September|October|November|December)\s+(?:of\s+)?'
    r'(?:\d{1,2},?\s+)?(1[89]\d{2}|20[0-2]\d))'
    r'[,\s]+([A-Z][^.!?]{10,200}[.!?])',
)

# Events: "Dick verbed ... in YYYY."
_RE_EVENT_PKD = re.compile(
    r'(?:Dick|PKD|Philip)\s+'
    r'([a-z]{3,20}(?:ed|s)?)\s+'
    r'([^.!?]{5,120}?)\s+'
    r'(?:in|during)\s+(1[89]\d{2}|20[0-2]\d)',
)


# ── Extraction functions (per-chunk, fast) ────────────────────────

def extract_people(chunk: CorpusChunk) -> list[tuple[str, str]]:
    """
    Extract person names. Returns list of (name, snippet) tuples.
    Only returns the first occurrence per name per chunk.
    """
    results = []
    seen = set()

    for m in _RE_PERSON.finditer(chunk.text):
        first, last = m.group(1), m.group(2)
        full = f'{first} {last}'

        if full in _NOT_PERSON or first in _AMBIGUOUS_FIRST:
            continue
        key = full.lower()
        if key in seen:
            continue
        seen.add(key)

        snippet = _extract_snippet(chunk.text, m.start(), m.end())
        results.append((full, snippet))

    return results


def extract_terms(chunk: CorpusChunk) -> list[tuple[str, str, str]]:
    """
    Extract candidate terms. Returns list of (name, match_type, snippet) tuples.
    Only first occurrence per name per chunk.
    """
    results = []
    seen = set()

    for pattern, mtype in [(_RE_TERM_CAP, 'cap'), (_RE_TERM_CAPS, 'caps'),
                            (_RE_TERM_HYPHEN, 'hyphen')]:
        for m in pattern.finditer(chunk.text):
            phrase = m.group(1).strip()
            if _is_noise(phrase):
                continue
            # Skip 2-word cap phrases that look like person names
            if mtype == 'cap':
                words = phrase.split()
                if len(words) == 2 and all(
                    w[0].isupper() and len(w) > 1 and w[1:].islower()
                    for w in words
                ):
                    continue

            key = phrase.lower()
            if key in seen:
                continue
            seen.add(key)

            snippet = _extract_snippet(chunk.text, m.start(), m.end())
            results.append((phrase, mtype, snippet))

    return results


def extract_works(chunk: CorpusChunk) -> list[tuple[str, str, str]]:
    """
    Extract work titles. Returns list of (title, match_type, snippet) tuples.
    """
    results = []
    seen = set()

    for pattern, mtype in [(_RE_WORK_ITALIC, 'italic'),
                            (_RE_WORK_QUOTED, 'quoted')]:
        for m in pattern.finditer(chunk.text):
            title = m.group(1).strip()
            if len(title) < 4 or _is_noise(title):
                continue
            key = title.lower()
            if key in seen:
                continue
            seen.add(key)

            snippet = _extract_snippet(chunk.text, m.start(), m.end())
            results.append((title, mtype, snippet))

    return results


def extract_events(chunk: CorpusChunk) -> list[dict]:
    """
    Extract date-anchored events. Returns list of event dicts.
    """
    results = []
    seen = set()

    # Pattern 1: "In YYYY, sentence."
    for m in _RE_EVENT_YEAR.finditer(chunk.text):
        year = m.group(1)
        desc = m.group(2).strip()
        if not 1920 <= int(year) <= 1985:
            continue
        key = f'{year}:{desc[:40].lower()}'
        if key in seen:
            continue
        seen.add(key)
        results.append({
            'year': year, 'date_raw': year,
            'description': desc[:200],
            'snippet': _extract_snippet(chunk.text, m.start(), m.end()),
        })

    # Pattern 2: "In Month YYYY, sentence."
    for m in _RE_EVENT_MONTH.finditer(chunk.text):
        date_raw = m.group(1).strip()
        year = m.group(2)
        desc = m.group(3).strip()
        if not 1920 <= int(year) <= 1985:
            continue
        key = f'{year}:{desc[:40].lower()}'
        if key in seen:
            continue
        seen.add(key)
        results.append({
            'year': year, 'date_raw': date_raw,
            'description': desc[:200],
            'snippet': _extract_snippet(chunk.text, m.start(), m.end()),
        })

    # Pattern 3: "Dick verbed ... in YYYY."
    for m in _RE_EVENT_PKD.finditer(chunk.text):
        verb = m.group(1)
        fragment = m.group(2).strip()
        year = m.group(3)
        if not 1920 <= int(year) <= 1985:
            continue
        desc = f'Dick {verb} {fragment}'
        key = f'{year}:{desc[:40].lower()}'
        if key in seen:
            continue
        seen.add(key)
        results.append({
            'year': year, 'date_raw': year,
            'description': desc[:200],
            'snippet': _extract_snippet(chunk.text, m.start(), m.end()),
        })

    return results
