#!/usr/bin/env python3
"""
Stage 2b: Corpus Discovery Pipeline

Analyzes text from two corpus substrates:
  Substrate A: segments.raw_text     (Exegesis chunks, ~9.7M chars)
  Substrate B: document_texts.text_content   (archive PDFs, ~605K chars)

Identifies candidate entities not already present in the database:
  - terms        Theological concepts, PKD-specific vocabulary
  - people       Scholars, historical figures, contacts
  - works        Novel titles, article titles, referenced texts
  - events       Date-anchored biographical events

Architecture:
  1. Materialize all source rows once per substrate (one SQL query each)
  2. Normalize each row (strip control chars, collapse whitespace)
  3. Run precompiled matcher sets against each row (all families in one pass)
  4. Record hits keyed to source_id (seg_id or doc_id)
  5. Aggregate after all rows are processed
  6. Filter against existing entities, score, write JSON

This stage does NOT write to the database. It produces review files:
  scripts/discover/output/discovered_terms.json
  scripts/discover/output/discovered_people.json
  scripts/discover/output/discovered_works.json
  scripts/discover/output/discovered_events.json

Usage:
    python scripts/discover/discovery_pipeline.py
    python scripts/discover/discovery_pipeline.py --min-frequency 3 --min-sources 2
    python scripts/discover/discovery_pipeline.py --types terms,people
    python scripts/discover/discovery_pipeline.py --segments-only
    python scripts/discover/discovery_pipeline.py --documents-only
"""

import argparse
import json
import re
import sqlite3
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

# Ensure scripts/ is importable
SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

from date_norms import make_slug, make_term_id, make_name_id
from discover.matchers import Hit, match_all

PROJECT_DIR = SCRIPTS_DIR.parent
DEFAULT_DB = PROJECT_DIR / 'database' / 'unified.sqlite'
OUTPUT_DIR = Path(__file__).resolve().parent / 'output'

# PKD domain markers for scoring
_PKD_MARKERS = re.compile(
    r'(?:Dick|PKD|Philip\s+K|Exegesis|VALIS|Ubik|Zebra|'
    r'2-3-74|Black\s+Iron|Palm\s+Tree|Gnostic|plasmate|'
    r'homoplasmate|demiurge|anamnesis)',
    re.IGNORECASE,
)


# ── Step 1: Corpus materialization ────────────────────────────────

def _normalize_text(text: str) -> str:
    """Normalize a corpus text row: strip control chars, collapse runs of whitespace."""
    if not text:
        return ''
    # Replace control chars (except newline/tab) with space
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', ' ', text)
    # Collapse runs of whitespace (but preserve single newlines)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def materialize_segments(db: sqlite3.Connection, min_chars: int = 100):
    """
    Materialize all Exegesis segment texts in one query.

    Returns list of (seg_id, title, normalized_text) tuples.
    Concatenates concise_summary into text for richer extraction.
    """
    rows = db.execute("""
        SELECT s.seg_id, s.title, s.raw_text, s.concise_summary
        FROM segments s
        WHERE s.raw_text IS NOT NULL AND LENGTH(s.raw_text) >= ?
    """, (min_chars,)).fetchall()

    result = []
    for seg_id, title, raw_text, summary in rows:
        text = raw_text
        if summary:
            text = summary + '\n\n' + raw_text
        text = _normalize_text(text)
        if len(text) >= min_chars:
            result.append((seg_id, title or seg_id, text))

    return result


def materialize_documents(db: sqlite3.Connection, min_chars: int = 100):
    """
    Materialize all archive document texts in one query.

    Returns list of (doc_id, title, category, normalized_text) tuples.
    """
    rows = db.execute("""
        SELECT d.doc_id, d.title, d.category, dt.text_content
        FROM document_texts dt
        JOIN documents d ON dt.doc_id = d.doc_id
        WHERE dt.text_content IS NOT NULL AND dt.char_count >= ?
          AND d.doc_type != 'exegesis_section'
    """, (min_chars,)).fetchall()

    result = []
    for doc_id, title, category, text in rows:
        text = _normalize_text(text)
        if len(text) >= min_chars:
            result.append((doc_id, title or doc_id, category, text))

    return result


# ── Step 2: Load existing entities for dedup ──────────────────────

def load_existing_entities(db: sqlite3.Connection) -> dict:
    """Load all existing terms, names, and events for dedup filtering."""
    existing = {}

    # Terms + aliases
    terms = {}
    for term_id, name, slug, status in db.execute(
        "SELECT term_id, canonical_name, slug, status FROM terms"
    ).fetchall():
        terms[name.lower()] = term_id
    for alias_text, in db.execute(
        "SELECT alias_text FROM term_aliases"
    ).fetchall():
        terms[alias_text.lower()] = None
    existing['terms'] = terms

    # Names + aliases
    names = {}
    for name_id, form, slug in db.execute(
        "SELECT name_id, canonical_form, slug FROM names"
    ).fetchall():
        names[form.lower()] = name_id
    for alias_text, in db.execute(
        "SELECT alias_text FROM name_aliases"
    ).fetchall():
        names[alias_text.lower()] = None
    existing['names'] = names

    # Term slugs + name slugs (for slug-based dedup)
    existing['term_slugs'] = {make_slug(k) for k in terms}
    existing['name_slugs'] = {make_slug(k) for k in names}

    # Events (year:summary_prefix)
    events = set()
    for row in db.execute(
        "SELECT date_start, summary FROM biography_events WHERE date_start IS NOT NULL"
    ).fetchall():
        year = row[0][:4] if row[0] else ''
        summary = (row[1] or '')[:30].lower()
        events.add(f'{year}:{summary}')
    existing['events'] = events

    return existing


# ── Step 3+4: Batched matching ────────────────────────────────────

def scan_substrate(
    rows: list[tuple],
    source_type: str,
    families: set[str],
    label: str,
) -> list[Hit]:
    """
    Run matchers against all rows of a single substrate.

    Args:
        rows: Materialized text rows. Tuples where the last element is text,
              and the first element is source_id.
        source_type: 'segment' or 'document'
        families: Set of entity families to match
        label: Label for progress reporting

    Returns:
        List of Hit objects, each keyed to its source_id.
    """
    all_hits = []
    total = len(rows)

    for i, row in enumerate(rows):
        source_id = row[0]
        text = row[-1]  # text is always last column

        hits = match_all(text, source_id, source_type, families)
        all_hits.extend(hits)

        if (i + 1) % 200 == 0:
            print(f"    [{label}] scanned {i + 1}/{total} rows, {len(all_hits)} hits")

    print(f"    [{label}] done: {total} rows, {len(all_hits)} hits")
    return all_hits


# ── Step 5+6: Aggregation and filtering ───────────────────────────

def aggregate_hits(
    hits: list[Hit],
    segment_titles: dict[str, str],
    document_titles: dict[str, str],
) -> dict[str, list[dict]]:
    """
    Aggregate raw hits into deduplicated candidates per entity family.

    Groups hits by (entity_family, normalized_name), picks the most frequent
    surface form as canonical, collects unique source documents and snippets.
    """
    # Group by family → normalized name
    family_groups: dict[str, dict[str, list[Hit]]] = defaultdict(lambda: defaultdict(list))

    for hit in hits:
        norm = re.sub(r'\s+', ' ', hit.name.strip().lower())
        family_groups[hit.entity_family][norm].append(hit)

    # Build candidates per family
    result = {}
    title_lookup = {**segment_titles, **document_titles}

    for family, groups in family_groups.items():
        candidates = []
        for norm, group in groups.items():
            # Canonical = most frequent surface form
            form_counts = Counter(h.name for h in group)
            canonical = form_counts.most_common(1)[0][0]

            # Unique sources with provenance
            sources = {}
            for h in group:
                if h.source_id not in sources:
                    sources[h.source_id] = {
                        'source_id': h.source_id,
                        'source_type': h.source_type,
                        'source_title': title_lookup.get(h.source_id, ''),
                    }

            # Unique snippets (max 5, deduplicated by prefix)
            seen_snips = set()
            snippets = []
            for h in group:
                if h.snippet and h.snippet[:60] not in seen_snips:
                    seen_snips.add(h.snippet[:60])
                    snippets.append(h.snippet)
                if len(snippets) >= 5:
                    break

            # Match types
            match_types = list(set(h.match_type for h in group))

            candidate = {
                'name': canonical,
                'frequency': len(group),
                'source_count': len(sources),
                'source_documents': list(sources.values()),
                'example_snippets': snippets,
                'match_types': match_types,
            }

            # Carry through extra data for events
            if family == 'events' and group:
                candidate['year'] = group[0].extra.get('year', '')
                candidate['date_raw'] = group[0].extra.get('date_raw', '')
                candidate['description'] = canonical

            candidates.append(candidate)

        result[family] = candidates

    return result


def filter_candidates(
    candidates: dict[str, list[dict]],
    existing: dict,
    min_frequency: int = 3,
    min_sources: int = 2,
) -> dict[str, list[dict]]:
    """
    Filter candidates: frequency thresholds + dedup against existing entities.
    """
    result = {}
    existing_terms = existing['terms']
    existing_names = existing['names']
    existing_term_slugs = existing['term_slugs']
    existing_name_slugs = existing['name_slugs']
    existing_events = existing['events']

    def _not_existing(name, entity_set, slug_set):
        return (name.lower() not in entity_set
                and make_slug(name) not in slug_set)

    # Terms
    if 'terms' in candidates:
        terms = candidates['terms']
        terms = [c for c in terms
                 if c['frequency'] >= min_frequency
                 and c['source_count'] >= min_sources]
        terms = [c for c in terms
                 if _not_existing(c['name'], existing_terms, existing_term_slugs)
                 and _not_existing(c['name'], existing_names, existing_name_slugs)]
        result['terms'] = terms

    # People
    if 'people' in candidates:
        people = candidates['people']
        people = [c for c in people
                  if c['frequency'] >= max(2, min_frequency - 1)
                  and c['source_count'] >= min_sources]
        people = [c for c in people
                  if _not_existing(c['name'], existing_names, existing_name_slugs)
                  and _not_existing(c['name'], existing_terms, existing_term_slugs)]
        result['people'] = people

    # Works
    if 'works' in candidates:
        works = candidates['works']
        works = [c for c in works
                 if c['frequency'] >= max(2, min_frequency - 1)
                 and c['source_count'] >= 1]
        works = [c for c in works
                 if _not_existing(c['name'], existing_terms, existing_term_slugs)]
        result['works'] = works

    # Events
    if 'events' in candidates:
        events = candidates['events']
        new_events = []
        for e in events:
            year = e.get('year', '')
            desc = e.get('description', '')
            key = f"{year}:{desc[:30].lower()}"
            is_dup = any(
                year in ek and any(
                    word in ek for word in desc[:30].lower().split()
                    if len(word) > 4
                )
                for ek in existing_events
            )
            if not is_dup:
                new_events.append(e)
        result['events'] = new_events

    return result


def score_and_finalize(candidates: dict[str, list[dict]]) -> dict[str, list[dict]]:
    """Score candidates and add proposed IDs."""
    result = {}

    for family, items in candidates.items():
        if not items:
            result[family] = items
            continue

        if family == 'events':
            # Event scoring
            for e in items:
                score = 0.3
                desc_lower = e.get('description', '').lower()
                if any(w in desc_lower for w in ['dick', 'pkd', 'philip']):
                    score += 0.3
                if any(w in desc_lower for w in
                       ['married', 'moved', 'wrote', 'published', 'born', 'died',
                        'divorced', 'met', 'began', 'completed', 'finished']):
                    score += 0.2
                e['confidence_score'] = round(min(1.0, score), 3)
            items.sort(key=lambda e: e.get('confidence_score', 0), reverse=True)
            result[family] = items
            continue

        # Entity scoring (terms, people, works)
        max_freq = max(c['frequency'] for c in items) or 1
        max_src = max(c['source_count'] for c in items) or 1

        for c in items:
            freq_norm = min(1.0, c['frequency'] / max_freq)
            spread_norm = min(1.0, c['source_count'] / max_src)
            snippets = c.get('example_snippets', [])
            pkd_count = sum(1 for s in snippets if _PKD_MARKERS.search(s)) if snippets else 0
            ctx = pkd_count / len(snippets) if snippets else 0.0
            domain = 0.5 if _PKD_MARKERS.search(c['name']) else 0.0
            score = 0.30 * freq_norm + 0.25 * spread_norm + 0.25 * ctx + 0.20 * domain
            c['confidence_score'] = round(score, 3)

        items.sort(key=lambda c: c['confidence_score'], reverse=True)

        # Add proposed IDs
        if family == 'terms':
            for c in items:
                c['proposed_slug'] = make_slug(c['name'])
                c['proposed_id'] = make_term_id(c['name'])
        elif family == 'people':
            for c in items:
                c['proposed_slug'] = make_slug(c['name'])
                c['proposed_id'] = make_name_id(c['name'])
                c['proposed_entity_type'] = 'historical_person'
                for snip in c.get('example_snippets', []):
                    if any(w in snip.lower() for w in
                           ['argues', 'contends', 'suggests', 'interprets',
                            'proposes', 'analyzes', 'writes', 'notes']):
                        c['is_scholar'] = True
                        break
        elif family == 'works':
            for c in items:
                c['proposed_slug'] = make_slug(c['name'])

        result[family] = items

    return result


# ── Main entry point ──────────────────────────────────────────────

def _write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def run(db: sqlite3.Connection, source_dir: Path,
        types: list[str] | None = None,
        min_frequency: int = 3,
        min_sources: int = 2,
        segments_only: bool = False,
        documents_only: bool = False):
    """
    Run the full discovery pipeline.

    Entry point for build_all.py integration:
        from discover.discovery_pipeline import run as run_discovery
        run_discovery(db, source_dir)
    """
    print("\n" + "=" * 60)
    print("STAGE 2b: CORPUS DISCOVERY")
    print("=" * 60)

    start = time.time()

    families = set(types) if types else {'terms', 'people', 'works', 'events'}

    # ── Step 1: Materialize corpus substrates ──
    print("  Materializing corpus text...")

    segment_rows = []
    document_rows = []

    if not documents_only:
        segment_rows = materialize_segments(db)
        seg_chars = sum(len(r[2]) for r in segment_rows)
        print(f"    Substrate A (segments): {len(segment_rows)} rows, {seg_chars:,} chars")

    if not segments_only:
        document_rows = materialize_documents(db)
        doc_chars = sum(len(r[3]) for r in document_rows)
        print(f"    Substrate B (documents): {len(document_rows)} rows, {doc_chars:,} chars")

    # Build title lookups for provenance
    segment_titles = {r[0]: r[1] for r in segment_rows}
    document_titles = {r[0]: r[1] for r in document_rows}

    # ── Step 2: Load existing entities ──
    print("  Loading existing entities...")
    existing = load_existing_entities(db)
    print(f"    Terms: {len(existing['terms'])}, Names: {len(existing['names'])}, "
          f"Events: {len(existing['events'])}")

    # ── Step 3+4: Batched matching per substrate ──
    print("  Scanning substrates...")
    all_hits = []

    if segment_rows:
        # Segments: tuples are (seg_id, title, text)
        seg_hits = scan_substrate(segment_rows, 'segment', families, 'segments')
        all_hits.extend(seg_hits)

    if document_rows:
        # Documents: tuples are (doc_id, title, category, text)
        doc_hits = scan_substrate(document_rows, 'document', families, 'documents')
        all_hits.extend(doc_hits)

    print(f"    Total hits: {len(all_hits)}")

    # ── Step 5: Aggregation ──
    print("  Aggregating hits...")
    candidates = aggregate_hits(all_hits, segment_titles, document_titles)
    for family, items in candidates.items():
        print(f"    {family}: {len(items)} unique candidates")

    # ── Step 6: Filter, score, finalize ──
    print("  Filtering and scoring...")
    candidates = filter_candidates(candidates, existing,
                                    min_frequency=min_frequency,
                                    min_sources=min_sources)
    for family, items in candidates.items():
        print(f"    {family}: {len(items)} after filtering")

    candidates = score_and_finalize(candidates)

    # ── Write output ──
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for family, items in candidates.items():
        output_path = OUTPUT_DIR / f'discovered_{family}.json'
        _write_json(output_path, items)
        print(f"\n  Wrote {len(items)} {family} -> {output_path}")

    # ── Summary ──
    elapsed = time.time() - start
    print(f"\n{'=' * 60}")
    print(f"Discovery complete in {elapsed:.1f}s")
    for family, items in candidates.items():
        if family == 'events':
            top3 = ', '.join(
                f"{e.get('year', '?')}: {e.get('description', '')[:25]}"
                for e in items[:3]
            ) if items else '(none)'
        else:
            top3 = ', '.join(c['name'] for c in items[:3]) if items else '(none)'
        print(f"  {family:10s}: {len(items):4d} candidates  top: {top3}")
    print(f"{'=' * 60}")

    return candidates


def main():
    parser = argparse.ArgumentParser(
        description='Stage 2b: Corpus Discovery Pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/discover/discovery_pipeline.py
  python scripts/discover/discovery_pipeline.py --min-frequency 5 --min-sources 3
  python scripts/discover/discovery_pipeline.py --types terms,people
  python scripts/discover/discovery_pipeline.py --segments-only
  python scripts/discover/discovery_pipeline.py --documents-only
        """,
    )
    parser.add_argument('--db', type=Path, default=DEFAULT_DB,
                        help='SQLite database path')
    parser.add_argument('--min-frequency', type=int, default=3,
                        help='Minimum total mentions (default: 3)')
    parser.add_argument('--min-sources', type=int, default=2,
                        help='Minimum distinct sources (default: 2)')
    parser.add_argument('--types', type=str, default=None,
                        help='Comma-separated entity types: terms,people,works,events')
    parser.add_argument('--segments-only', action='store_true',
                        help='Only scan Exegesis segment text (Substrate A)')
    parser.add_argument('--documents-only', action='store_true',
                        help='Only scan archive document text (Substrate B)')
    args = parser.parse_args()

    types = args.types.split(',') if args.types else None

    db = sqlite3.connect(str(args.db))
    db.execute("PRAGMA journal_mode = WAL")

    try:
        run(db, PROJECT_DIR,
            types=types,
            min_frequency=args.min_frequency,
            min_sources=args.min_sources,
            segments_only=args.segments_only,
            documents_only=args.documents_only)
    finally:
        db.close()


if __name__ == '__main__':
    main()
