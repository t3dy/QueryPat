"""
Precompiled matcher sets for corpus discovery.

Each matcher family (people, terms, works, events) is a set of compiled
regex patterns with extraction logic. Matchers are built once at module
load time and reused across all corpus rows.
"""

import re

# ── Context extraction ────────────────────────────────────────────

CONTEXT_CHARS = 150


def extract_snippet(text: str, start: int, end: int,
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


# ── Noise filters (frozen sets, evaluated once) ───────────────────

NOISE_CAPS = frozenset({
    'ISBN', 'JSTOR', 'DOI', 'PDF', 'URL', 'HTML', 'XML', 'OCR',
    'USA', 'NYC', 'CIA', 'FBI', 'IRS', 'KGB', 'LSD',
    'VOL', 'ISS', 'FIG', 'SEE', 'THE', 'AND', 'FOR', 'NOT',
    'HIS', 'HER', 'HAS', 'BUT', 'WAS', 'ARE', 'ALL', 'CAN',
    'HAD', 'HIM', 'OUR', 'DID', 'ONE', 'TWO', 'NEW', 'NOW',
    'OLD', 'OWN', 'SAY', 'SHE', 'HOW', 'ITS', 'LET', 'MAY',
    'WHO', 'GOD', 'MAN', 'WAR', 'WAY',
})

STOP_WORDS_LOWER = frozenset({
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

NOT_PERSON = frozenset({
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
    # PKD work title fragments
    'Scanner Darkly', 'Blade Runner', 'Time Out',
    'Dick Society', 'Dick Philip', 'Philip Dick',
    'Iron Empire', 'Iron Cage',
    # False positive phrases from corpus
    'Congress Cataloging', 'Library Congress', 'Internet Archive',
    'Gnostic Christianity', 'Gnostic Xtianity', 'Alexandrian Logos',
    'Stable Diffusion', 'Inc Stable',
})

AMBIGUOUS_FIRST = frozenset({
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
    # Verbs and adverbs that start sentences
    'Do', 'We', 'Is', 'It', 'He', 'She', 'They', 'You',
    'Hence', 'Therefore', 'Moreover', 'Furthermore', 'However',
    'Although', 'Whereas', 'Nevertheless', 'Nonetheless',
    'Certainly', 'Clearly', 'Obviously', 'Apparently',
    'Essentially', 'Basically', 'Actually', 'Already',
    'Again', 'Once', 'Never', 'Always', 'Often', 'Quite',
    'Enough', 'Less', 'Least', 'Whole', 'Whose', 'Which',
    'An', 'Oh', 'Without', 'Within', 'Beyond', 'Above',
    'Below', 'Toward', 'Towards', 'Against', 'Along',
})

# Common English nouns/adjectives/verbs that appear capitalized but aren't surnames
NOT_SURNAME = frozenset({
    # Time/place/thing nouns
    'Time', 'War', 'World', 'Man', 'God', 'Life', 'Day', 'Year',
    'Part', 'Way', 'Book', 'Page', 'Chapter', 'Press', 'House',
    'Land', 'Age', 'Side', 'End', 'Sign', 'Mind', 'Word', 'Form',
    'Body', 'Soul', 'Death', 'Light', 'Dark', 'Night', 'Fall',
    'View', 'Type', 'System', 'Thing', 'Point', 'Kind', 'Sense',
    # Places
    'County', 'City', 'State', 'Lane', 'Street', 'Avenue', 'Road',
    'Kingdom', 'Empire', 'Mission', 'Land', 'Ellen', 'Omega',
    # Pronouns
    'You', 'The', 'This', 'That', 'Which', 'What', 'Who',
    # Adjectives
    'Bad', 'Good', 'Made', 'Active', 'Living', 'Golden', 'Holy',
    'Total', 'Special', 'Imperial', 'Western', 'Eastern',
    'Sacred', 'Cosmic', 'Vast', 'Apart', 'Recall',
    # Philosophical/religious terms (PKD corpus)
    'Darkly', 'Gnostic', 'Gnosis', 'Kerygma', 'Gospel', 'Logos',
    'Xtian', 'Gnosticism', 'Christianity', 'Buddhism', 'Hinduism',
    'Christ', 'Naturans', 'Bumat', 'Reborn', 'Unbound',
    'Consciousness', 'Intelligence', 'Civilization', 'Absconditus',
    'Cakkhu', 'Dei', 'Chamber',
    # Publishing/metadata
    'Copyright', 'Includes', 'Award', 'Introduction', 'Society',
    'Edition', 'Volume', 'Number', 'Series', 'Review', 'Journal',
    'University', 'College', 'Institute', 'Library', 'Archive',
    'Cover', 'Essays', 'Frontispiece', 'Foreword', 'Preface',
    'Index', 'Notes', 'Appendix', 'Bibliography', 'Clothbound',
    'Contents', 'Title', 'Collections', 'Sandwich',
    # Works/fiction terms
    'Fields', 'Syndrome', 'Artifact', 'Fish', 'Iron', 'Tree',
    'Regained', 'Returns', 'Revisited', 'Millenial',
    'Zebra', 'Ubik', 'Valis',
    # Verbs/adverbs
    'Then', 'Thus', 'States',
    # More false positives from corpus
    'Himself', 'Herself', 'Itself', 'Themselves',
    'Church', 'Publishing', 'Free', 'Lives', 'Epigraph',
    'Cataloguing', 'Cataloging', 'Greece', 'Bells',
    'Healer', 'Captivity', 'Past', 'Computer', 'Layers',
    'Pantocrator', 'Tristigistos', 'Britannica', 'Brotherhood',
    'Carmel', 'Pigspurt', 'Ysabel',
})

# First words that are never first names
NOT_FIRST_NAME = frozenset({
    'Qua', 'Maybe', 'Specifically', 'Valis', 'Valist', 'Exegesis',
    'Marin', 'Jewish', 'Gnostic', 'Hermetic', 'Anamnesis',
    'Xtian', 'Dick', 'Portuguese', 'British', 'French', 'German',
    'Italian', 'Spanish', 'Russian', 'Chinese', 'Japanese',
    'American', 'European', 'African', 'Asian', 'Ancient',
    'Millenial', 'Megiddo', 'Dibba', 'Atman', 'Jesus',
    'Contents', 'Crap', 'Ham', 'Signal', 'Ave',
    'Fish', 'World', 'Cosmic', 'Imperial',
    'Inner', 'Dedication', 'Radio', 'Attic', 'Easter',
    'Congress', 'Encyclopaedia', 'Babylonian', 'Binary',
    'Harcourt', 'Onion', 'Pansophiaist', 'Xtians',
    'Christ', 'Christian', 'Pot', 'America',
    'Things', 'Santa',
})


def is_noise(phrase: str) -> bool:
    """Check if a phrase is noise that should be filtered out."""
    low = phrase.lower().strip()
    if low in STOP_WORDS_LOWER:
        return True
    if phrase in NOISE_CAPS:
        return True
    if len(low) < 3 or re.match(r'^\d+$', low):
        return True
    if re.match(r'^(?:p\.|pp\.|vol\.|no\.|ch\.|fig\.)', low):
        return True
    return False


# ── Compiled regex patterns (built once at import time) ───────────

# People: "Firstname Lastname"
RE_PERSON = re.compile(r'\b([A-Z][a-z]{1,15})\s+([A-Z][a-z]{2,20})\b')

# Terms: capitalized multi-word (2-3 words)
RE_TERM_CAP = re.compile(
    r'\b([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b'
)
RE_TERM_CAPS = re.compile(r'\b([A-Z]{3,12})\b')
RE_TERM_HYPHEN = re.compile(r'\b([A-Z][a-z]+-[a-z]+(?:-[a-z]+)?)\b')

# Works: *Italic Title* or "Quoted Title"
RE_WORK_ITALIC = re.compile(r'(?<!\w)[*_]([A-Z][^*_\n]{3,60})[*_](?!\w)')
RE_WORK_QUOTED = re.compile(r'["\u201c]([A-Z][^"\u201d\n]{3,60})["\u201d]')

# Events: date-anchored patterns
RE_EVENT_YEAR = re.compile(
    r'(?:[Ii]n|[Dd]uring|[Bb]y|[Aa]round)\s+'
    r'(1[89]\d{2}|20[0-2]\d)'
    r'[,\s]+([A-Z][^.!?]{15,200}[.!?])',
)
RE_EVENT_MONTH = re.compile(
    r'(?:[Ii]n|[Oo]n|[Dd]uring|[Bb]y)\s+'
    r'((?:January|February|March|April|May|June|July|August|'
    r'September|October|November|December)\s+(?:of\s+)?'
    r'(?:\d{1,2},?\s+)?(1[89]\d{2}|20[0-2]\d))'
    r'[,\s]+([A-Z][^.!?]{10,200}[.!?])',
)
RE_EVENT_PKD = re.compile(
    r'(?:Dick|PKD|Philip)\s+'
    r'([a-z]{3,20}(?:ed|s)?)\s+'
    r'([^.!?]{5,120}?)\s+'
    r'(?:in|during)\s+(1[89]\d{2}|20[0-2]\d)',
)


# ── Hit dataclass ─────────────────────────────────────────────────

class Hit:
    """A single extraction hit, tied to its source row."""
    __slots__ = ('entity_family', 'name', 'match_type', 'snippet',
                 'source_id', 'source_type', 'extra')

    def __init__(self, entity_family: str, name: str, match_type: str,
                 snippet: str, source_id: str, source_type: str,
                 extra: dict | None = None):
        self.entity_family = entity_family
        self.name = name
        self.match_type = match_type
        self.snippet = snippet
        self.source_id = source_id
        self.source_type = source_type
        self.extra = extra or {}


# ── Batch matchers (one call per text row) ────────────────────────

def match_people(text: str, source_id: str, source_type: str) -> list[Hit]:
    """Match person names in a single text. Returns deduplicated hits."""
    hits = []
    seen = set()
    for m in RE_PERSON.finditer(text):
        first, last = m.group(1), m.group(2)
        full = f'{first} {last}'
        if (full in NOT_PERSON or first in AMBIGUOUS_FIRST
                or last in NOT_SURNAME or first in NOT_FIRST_NAME):
            continue
        key = full.lower()
        if key in seen:
            continue
        seen.add(key)
        snippet = extract_snippet(text, m.start(), m.end())
        hits.append(Hit('people', full, 'person_name', snippet,
                        source_id, source_type))
    return hits


def match_terms(text: str, source_id: str, source_type: str) -> list[Hit]:
    """Match candidate terms in a single text."""
    hits = []
    seen = set()

    for pattern, mtype in [(RE_TERM_CAP, 'cap'), (RE_TERM_CAPS, 'caps'),
                            (RE_TERM_HYPHEN, 'hyphen')]:
        for m in pattern.finditer(text):
            phrase = m.group(1).strip()
            if is_noise(phrase):
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
            snippet = extract_snippet(text, m.start(), m.end())
            hits.append(Hit('terms', phrase, mtype, snippet,
                            source_id, source_type))
    return hits


def match_works(text: str, source_id: str, source_type: str) -> list[Hit]:
    """Match work titles in a single text."""
    hits = []
    seen = set()

    for pattern, mtype in [(RE_WORK_ITALIC, 'italic'),
                            (RE_WORK_QUOTED, 'quoted')]:
        for m in pattern.finditer(text):
            title = m.group(1).strip()
            if len(title) < 4 or is_noise(title):
                continue
            key = title.lower()
            if key in seen:
                continue
            seen.add(key)
            snippet = extract_snippet(text, m.start(), m.end())
            hits.append(Hit('works', title, mtype, snippet,
                            source_id, source_type))
    return hits


def match_events(text: str, source_id: str, source_type: str) -> list[Hit]:
    """Match date-anchored events in a single text."""
    hits = []
    seen = set()

    # Pattern 1: "In YYYY, sentence."
    for m in RE_EVENT_YEAR.finditer(text):
        year = m.group(1)
        desc = m.group(2).strip()
        if not 1920 <= int(year) <= 1985:
            continue
        key = f'{year}:{desc[:40].lower()}'
        if key in seen:
            continue
        seen.add(key)
        snippet = extract_snippet(text, m.start(), m.end())
        hits.append(Hit('events', desc[:200], 'year_anchor', snippet,
                        source_id, source_type,
                        {'year': year, 'date_raw': year}))

    # Pattern 2: "In Month YYYY, sentence."
    for m in RE_EVENT_MONTH.finditer(text):
        date_raw = m.group(1).strip()
        year = m.group(2)
        desc = m.group(3).strip()
        if not 1920 <= int(year) <= 1985:
            continue
        key = f'{year}:{desc[:40].lower()}'
        if key in seen:
            continue
        seen.add(key)
        snippet = extract_snippet(text, m.start(), m.end())
        hits.append(Hit('events', desc[:200], 'month_anchor', snippet,
                        source_id, source_type,
                        {'year': year, 'date_raw': date_raw}))

    # Pattern 3: "Dick verbed ... in YYYY."
    for m in RE_EVENT_PKD.finditer(text):
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
        snippet = extract_snippet(text, m.start(), m.end())
        hits.append(Hit('events', desc[:200], 'pkd_subject', snippet,
                        source_id, source_type,
                        {'year': year, 'date_raw': year}))

    return hits


def match_all(text: str, source_id: str, source_type: str,
              families: set[str] | None = None) -> list[Hit]:
    """
    Run all requested matcher families against a single text row.
    This is the main entry point for batched matching.

    Args:
        text: The text to scan
        source_id: seg_id or doc_id
        source_type: 'segment' or 'document'
        families: Set of families to run (default: all)
    """
    if families is None:
        families = {'people', 'terms', 'works', 'events'}

    hits = []
    if 'people' in families:
        hits.extend(match_people(text, source_id, source_type))
    if 'terms' in families:
        hits.extend(match_terms(text, source_id, source_type))
    if 'works' in families:
        hits.extend(match_works(text, source_id, source_type))
    if 'events' in families:
        hits.extend(match_events(text, source_id, source_type))
    return hits
