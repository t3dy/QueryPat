"""
Search extracted PDF text in the unified database for terms, people, or events.

Usage:
    python scripts/search_pdfs.py --term "VALIS"
    python scripts/search_pdfs.py --term "Plotinus" --category scholarship
    python scripts/search_pdfs.py --terms-file scripts/priority_terms.txt
    python scripts/search_pdfs.py --discover-terms --min-count 3
    python scripts/search_pdfs.py --discover-events --category biographies
"""

import argparse
import json
import re
import sqlite3
import sys
from collections import Counter, defaultdict
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / 'database' / 'unified.sqlite'

# Context window: how many chars before/after a match to extract
CONTEXT_CHARS = 300


def get_db():
    return sqlite3.connect(str(DB_PATH))


def search_term(db, term, category=None, context_chars=CONTEXT_CHARS):
    """Search for a term across all extracted document text."""
    query = """
        SELECT d.doc_id, d.title, d.author, d.category, d.doc_type,
               dt.text_content, dt.char_count
        FROM document_texts dt
        JOIN documents d ON dt.doc_id = d.doc_id
        WHERE dt.text_content IS NOT NULL AND dt.char_count > 0
          AND d.doc_type != 'exegesis_section'
    """
    params = []
    if category:
        query += " AND d.category = ?"
        params.append(category)

    rows = db.execute(query, params).fetchall()
    results = []

    pattern = re.compile(re.escape(term), re.IGNORECASE)

    for row in rows:
        doc_id, title, author, cat, doc_type, text, char_count = row
        matches = list(pattern.finditer(text))
        if not matches:
            continue

        passages = []
        for m in matches[:5]:  # max 5 passages per doc
            start = max(0, m.start() - context_chars)
            end = min(len(text), m.end() + context_chars)
            passage = text[start:end]
            # Clean up passage boundaries
            if start > 0:
                passage = '...' + passage[passage.find(' ') + 1:]
            if end < len(text):
                passage = passage[:passage.rfind(' ')] + '...'
            passages.append({
                'text': passage,
                'char_offset': m.start(),
                'page_estimate': max(1, m.start() // 2000 + 1),
            })

        results.append({
            'doc_id': doc_id,
            'title': title,
            'author': author,
            'category': cat,
            'doc_type': doc_type,
            'match_count': len(matches),
            'passages': passages,
        })

    results.sort(key=lambda r: r['match_count'], reverse=True)
    return results


def discover_terms(db, min_count=3, existing_terms=None):
    """Find capitalized multi-word phrases that appear frequently across documents."""
    if existing_terms is None:
        existing_terms = set()

    query = """
        SELECT d.doc_id, d.title, d.category, dt.text_content
        FROM document_texts dt
        JOIN documents d ON dt.doc_id = d.doc_id
        WHERE dt.text_content IS NOT NULL AND dt.char_count > 0
          AND d.doc_type != 'exegesis_section'
    """
    rows = db.execute(query).fetchall()

    # Patterns for potential terms
    # Capitalized phrases (2-4 words)
    cap_pattern = re.compile(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})\b')
    # ALL CAPS words (acronyms/special terms)
    caps_pattern = re.compile(r'\b([A-Z]{2,})\b')
    # Hyphenated compounds
    hyphen_pattern = re.compile(r'\b([A-Z][a-z]+-[a-z]+(?:-[a-z]+)*)\b')

    term_counts = Counter()
    term_docs = defaultdict(set)

    # Common phrases to exclude
    exclude = {
        'The', 'This', 'That', 'These', 'Those', 'With', 'From', 'Into',
        'About', 'After', 'Before', 'Between', 'Through', 'During',
        'Philip Dick', 'Dick Philip', 'New York', 'Los Angeles',
        'San Francisco', 'Science Fiction', 'United States',
        'University Press', 'Oxford University', 'Cambridge University',
    }

    existing_lower = {t.lower() for t in existing_terms}

    for doc_id, title, category, text in rows:
        for pattern in [cap_pattern, caps_pattern, hyphen_pattern]:
            for m in pattern.finditer(text):
                phrase = m.group(1).strip()
                if phrase in exclude or len(phrase) < 4:
                    continue
                if phrase.lower() in existing_lower:
                    continue
                term_counts[phrase] += 1
                term_docs[phrase].add(doc_id)

    # Filter: must appear in min_count different documents
    candidates = []
    for phrase, count in term_counts.most_common():
        doc_count = len(term_docs[phrase])
        if doc_count >= min_count:
            candidates.append({
                'term': phrase,
                'total_mentions': count,
                'document_count': doc_count,
            })

    return candidates


def discover_events(db, category='biographies'):
    """Find date-anchored biographical events in biography PDFs."""
    query = """
        SELECT d.doc_id, d.title, d.author, dt.text_content
        FROM document_texts dt
        JOIN documents d ON dt.doc_id = d.doc_id
        WHERE dt.text_content IS NOT NULL AND dt.char_count > 0
          AND d.category = ?
    """
    rows = db.execute(query, (category,)).fetchall()

    # Pattern: year (1920-1985) near biographical narrative
    year_pattern = re.compile(
        r'(?:in|In|during|During|by|By|around|circa|c\.|ca\.)\s+'
        r'(1[89]\d{2}|20[0-2]\d)'
        r'[,\s]+([^.]{20,200}\.)',
        re.MULTILINE
    )

    # Also match: "In March 1974, ..." style
    month_pattern = re.compile(
        r'(?:In|in|On|on|During|By)\s+'
        r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+'
        r'(?:of\s+)?'
        r'(1[89]\d{2}|20[0-2]\d)'
        r'[,\s]+([^.]{10,200}\.)',
        re.MULTILINE
    )

    events = []
    for doc_id, title, author, text in rows:
        for pattern in [year_pattern, month_pattern]:
            for m in pattern.finditer(text):
                year = m.group(1)
                description = m.group(2).strip()
                # Filter out non-biographical content
                if int(year) < 1920 or int(year) > 1985:
                    continue
                if len(description) < 20:
                    continue
                events.append({
                    'year': year,
                    'description': description[:200],
                    'source': author or title,
                    'doc_id': doc_id,
                })

    events.sort(key=lambda e: e['year'])
    return events


def get_existing_terms(db):
    """Get all existing term names from the database."""
    rows = db.execute("SELECT canonical_name FROM terms").fetchall()
    terms = {r[0] for r in rows}
    # Also get aliases
    alias_rows = db.execute("SELECT alias_text FROM term_aliases").fetchall()
    terms.update(r[0] for r in alias_rows)
    return terms


def main():
    parser = argparse.ArgumentParser(description='Search extracted PDF text')
    parser.add_argument('--term', help='Search for a specific term')
    parser.add_argument('--terms-file', help='File with one term per line')
    parser.add_argument('--category', help='Filter by document category')
    parser.add_argument('--discover-terms', action='store_true',
                        help='Find candidate terms not in the dictionary')
    parser.add_argument('--discover-events', action='store_true',
                        help='Find date-anchored events in biographies')
    parser.add_argument('--min-count', type=int, default=3,
                        help='Min document count for term discovery (default: 3)')
    parser.add_argument('--output', help='Output JSON file')
    args = parser.parse_args()

    db = get_db()

    if args.discover_terms:
        existing = get_existing_terms(db)
        candidates = discover_terms(db, min_count=args.min_count, existing_terms=existing)
        print(f"Found {len(candidates)} candidate terms (appearing in {args.min_count}+ docs)")
        for c in candidates[:50]:
            print(f"  {c['term']:40s}  mentions={c['total_mentions']:3d}  docs={c['document_count']:2d}")
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(candidates, f, indent=2, ensure_ascii=False)
            print(f"Saved to {args.output}")

    elif args.discover_events:
        events = discover_events(db, category=args.category or 'biographies')
        print(f"Found {len(events)} date-anchored events")
        for e in events[:30]:
            print(f"  {e['year']} | {e['description'][:80]}... [{e['source']}]")
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(events, f, indent=2, ensure_ascii=False)
            print(f"Saved to {args.output}")

    elif args.term:
        results = search_term(db, args.term, category=args.category)
        print(f"'{args.term}': found in {len(results)} documents")
        for r in results[:10]:
            print(f"  [{r['match_count']}x] {r['author'] or '?':30s} | {r['title'][:50]}")
            if r['passages']:
                print(f"       {r['passages'][0]['text'][:120]}...")
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)

    elif args.terms_file:
        terms_path = Path(args.terms_file)
        if not terms_path.exists():
            print(f"File not found: {args.terms_file}")
            sys.exit(1)
        terms = [line.strip() for line in terms_path.read_text().splitlines() if line.strip()]
        all_results = {}
        for term in terms:
            results = search_term(db, term, category=args.category)
            all_results[term] = results
            doc_count = len(results)
            total_matches = sum(r['match_count'] for r in results)
            print(f"  {term:40s}  docs={doc_count:3d}  mentions={total_matches:4d}")
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(all_results, f, indent=2, ensure_ascii=False)
            print(f"Saved to {args.output}")

    else:
        parser.print_help()

    db.close()


if __name__ == '__main__':
    main()
