"""
Scoring, deduplication, and candidate ranking for discovery results.

Candidates are scored on:
  - frequency: raw mention count across the corpus
  - spread: number of distinct sources mentioning the candidate
  - context_quality: how informative the surrounding text is
  - domain_relevance: presence of PKD-specific markers
"""

import re
from collections import Counter, defaultdict
from difflib import SequenceMatcher


# ── PKD domain relevance markers ──────────────────────────────────

_PKD_MARKERS = re.compile(
    r'(?:Dick|PKD|Philip\s+K|Exegesis|VALIS|Ubik|Zebra|'
    r'2-3-74|Black\s+Iron|Palm\s+Tree|Gnostic|plasmate|'
    r'homoplasmate|demiurge|anamnesis)',
    re.IGNORECASE,
)

_SCHOLARLY_MARKERS = re.compile(
    r'(?:argues|suggests|contends|interprets|analyzes|explores|'
    r'discusses|identifies|proposes|theorizes|observes)',
    re.IGNORECASE,
)


def _context_quality(snippet: str) -> float:
    """Score 0.0-1.0 for how informative a snippet is."""
    if not snippet:
        return 0.0
    score = 0.0
    # Has PKD-relevant markers
    if _PKD_MARKERS.search(snippet):
        score += 0.4
    # Has scholarly analysis language
    if _SCHOLARLY_MARKERS.search(snippet):
        score += 0.3
    # Has reasonable length (not too short, not just metadata)
    word_count = len(snippet.split())
    if 10 <= word_count <= 100:
        score += 0.2
    # Has sentence structure (capital start, period end)
    if re.search(r'[A-Z].*[.!?]', snippet):
        score += 0.1
    return min(1.0, score)


def _domain_relevance(name: str, snippets: list[str]) -> float:
    """Score 0.0-1.0 for how relevant a candidate is to PKD studies."""
    score = 0.0
    # Name itself contains PKD markers
    if _PKD_MARKERS.search(name):
        score += 0.5
    # Snippets contain PKD context
    pkd_snippets = sum(1 for s in snippets if _PKD_MARKERS.search(s))
    if snippets:
        score += 0.5 * (pkd_snippets / len(snippets))
    return min(1.0, score)


# ── Deduplication ─────────────────────────────────────────────────

def _normalize_name(name: str) -> str:
    """Normalize a name for dedup comparison."""
    return re.sub(r'\s+', ' ', name.strip().lower())


def _names_match(a: str, b: str, threshold: float = 0.85) -> bool:
    """Check if two names are similar enough to be the same entity."""
    na, nb = _normalize_name(a), _normalize_name(b)
    if na == nb:
        return True
    # Check if one is a substring of the other
    if na in nb or nb in na:
        return True
    # Fuzzy match
    return SequenceMatcher(None, na, nb).ratio() >= threshold


def deduplicate_candidates(
    mentions: list[dict],
    name_key: str = 'name',
) -> list[dict]:
    """
    Merge mentions into unique candidates.

    Groups mentions by normalized name, picks the most frequent form
    as canonical, and aggregates source documents and snippets.
    """
    # Group by normalized name
    groups: dict[str, list[dict]] = defaultdict(list)
    canonical_map: dict[str, str] = {}  # normalized → best form

    for mention in mentions:
        name = mention[name_key]
        norm = _normalize_name(name)

        # Check if this matches an existing group (fuzzy)
        matched = None
        for existing_norm in list(groups.keys()):
            if _names_match(norm, existing_norm):
                matched = existing_norm
                break

        if matched:
            groups[matched].append(mention)
            # Update canonical if this form appears more
        else:
            groups[norm].append(mention)
            canonical_map[norm] = name

    # Build deduplicated candidates
    candidates = []
    for norm, group in groups.items():
        # Pick most frequent surface form as canonical
        form_counts = Counter(m[name_key] for m in group)
        canonical = form_counts.most_common(1)[0][0]

        # Unique sources
        sources = {}
        for m in group:
            sid = m['source_id']
            if sid not in sources:
                sources[sid] = {
                    'source_id': sid,
                    'source_type': m.get('source_type', 'unknown'),
                    'source_title': m.get('source_title', ''),
                }

        # Collect unique snippets (max 5)
        seen_snippets = set()
        snippets = []
        for m in group:
            snip = m.get('snippet', '')
            if snip and snip[:80] not in seen_snippets:
                seen_snippets.add(snip[:80])
                snippets.append(snip)
            if len(snippets) >= 5:
                break

        candidates.append({
            'name': canonical,
            'frequency': len(group),
            'source_count': len(sources),
            'source_documents': list(sources.values()),
            'example_snippets': snippets,
            'match_types': list(set(m.get('match_type', 'unknown') for m in group)),
        })

    return candidates


# ── Scoring ───────────────────────────────────────────────────────

def score_candidates(
    candidates: list[dict],
    max_frequency: int | None = None,
) -> list[dict]:
    """
    Assign confidence_score (0.0-1.0) to each candidate.

    Score formula:
      0.30 * frequency_normalized
    + 0.25 * source_spread_normalized
    + 0.25 * context_quality_avg
    + 0.20 * domain_relevance
    """
    if not candidates:
        return candidates

    if max_frequency is None:
        max_frequency = max(c['frequency'] for c in candidates) or 1

    max_sources = max(c['source_count'] for c in candidates) or 1

    for c in candidates:
        freq_norm = min(1.0, c['frequency'] / max_frequency)
        spread_norm = min(1.0, c['source_count'] / max_sources)

        ctx_scores = [_context_quality(s) for s in c.get('example_snippets', [])]
        ctx_avg = sum(ctx_scores) / len(ctx_scores) if ctx_scores else 0.0

        domain = _domain_relevance(c['name'], c.get('example_snippets', []))

        score = (0.30 * freq_norm
                 + 0.25 * spread_norm
                 + 0.25 * ctx_avg
                 + 0.20 * domain)

        c['confidence_score'] = round(score, 3)

    # Sort by score descending
    candidates.sort(key=lambda c: c['confidence_score'], reverse=True)
    return candidates
