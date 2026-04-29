#!/usr/bin/env python3
"""
Search the PKD archive for all mentions of 'homeopape' (and related terms).
Extracts surrounding paragraph context and outputs a Markdown report.
"""

import sqlite3
import json
import os
import re
import fitz  # PyMuPDF

SEARCH_TERMS = ["homeopape", "homeostatic newspaper", "homeo-pape"]
DB_PATH = "C:/QueryPat/database/unified.sqlite"
ARCHIVE_PDF = "C:/ExegesisAnalysis/PaulPKDarchive/PKDpdf"
ARCHIVE_JSON = "C:/ExegesisAnalysis/PaulPKDarchive"
EXEGESIS_PATH = "C:/QueryPat/exegesis_ordered.txt"
OUTPUT_MD = "C:/QueryPat/site/public/homeopape_report.md"

# Known PKD novels likely to contain homeopape references
PRIORITY_PDFS = [
    "Book_PKD_Ubik.pdf",
    "Dick, Philip Kindred - The Simulacra - libgen.li.pdf",
    "Dick, Philip Kindred - The Penultimate Truth - libgen.li.pdf",
    "Dick, Philip K. - Clans of the Alphane Moon (1964, Ace Books) - libgen.li.pdf",
]


def split_paragraphs(text):
    """Split text into paragraphs (double newline or significant whitespace breaks)."""
    # Normalize line endings
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    # Split on double+ newlines
    paras = re.split(r'\n\s*\n', text)
    # Clean up each paragraph
    paras = [re.sub(r'\s+', ' ', p).strip() for p in paras if p.strip()]
    return paras


def search_text(text, source_title, source_type):
    """Search text for terms, return list of matches with paragraph context."""
    matches = []
    paragraphs = split_paragraphs(text)

    for term in SEARCH_TERMS:
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        for i, para in enumerate(paragraphs):
            if pattern.search(para):
                # Get surrounding paragraphs
                before = paragraphs[i - 1] if i > 0 else None
                after = paragraphs[i + 1] if i < len(paragraphs) - 1 else None
                matches.append({
                    'term': term,
                    'source_title': source_title,
                    'source_type': source_type,
                    'paragraph': para,
                    'before': before,
                    'after': after,
                    'para_index': i,
                })
    return matches


def extract_pdf_text(pdf_path):
    """Extract full text from a PDF using PyMuPDF."""
    try:
        doc = fitz.open(pdf_path)
        pages = []
        for page in doc:
            pages.append(page.get_text())
        doc.close()
        return '\n\n'.join(pages)
    except Exception as e:
        print(f"  [WARN] Could not read {pdf_path}: {e}")
        return ""


def search_database():
    """Search the SQLite database for homeopape mentions."""
    matches = []
    if not os.path.exists(DB_PATH):
        print("[SKIP] Database not found")
        return matches

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Search document_texts
    for term in SEARCH_TERMS:
        cur.execute(
            "SELECT dt.doc_id, d.title, dt.text_content "
            "FROM document_texts dt JOIN documents d ON dt.doc_id=d.doc_id "
            "WHERE dt.text_content LIKE ? COLLATE NOCASE",
            (f'%{term}%',)
        )
        for row in cur.fetchall():
            doc_id, title, text = row
            results = search_text(text, title, "database")
            matches.extend(results)

    # Search segments (Exegesis)
    for term in SEARCH_TERMS:
        cur.execute(
            "SELECT s.seg_id, s.raw_text, d.title "
            "FROM segments s JOIN documents d ON s.doc_id=d.doc_id "
            "WHERE s.raw_text LIKE ? COLLATE NOCASE",
            (f'%{term}%',)
        )
        for row in cur.fetchall():
            seg_id, text, title = row
            source = f"{title} (segment {seg_id})"
            if text:
                results = search_text(text, source, "exegesis_segment")
                matches.extend(results)

    conn.close()
    return matches


def search_exegesis_file():
    """Search the ordered exegesis text file."""
    matches = []
    if not os.path.exists(EXEGESIS_PATH):
        print("[SKIP] Exegesis file not found")
        return matches

    print(f"Searching exegesis_ordered.txt...")
    with open(EXEGESIS_PATH, 'r', encoding='utf-8', errors='replace') as f:
        text = f.read()
    matches = search_text(text, "Exegesis (ordered compilation)", "exegesis")
    print(f"  Found {len(matches)} match(es)")
    return matches


def search_pdfs():
    """Search PDF files in the archive for homeopape mentions."""
    matches = []
    if not os.path.exists(ARCHIVE_PDF):
        print("[SKIP] PDF archive not found")
        return matches

    # Search priority PDFs first, then all others
    searched = set()
    all_pdfs = []

    for name in PRIORITY_PDFS:
        path = os.path.join(ARCHIVE_PDF, name)
        if os.path.exists(path):
            all_pdfs.insert(0, (name, path))
            searched.add(name)

    # Add remaining PDFs
    for name in os.listdir(ARCHIVE_PDF):
        if name.endswith('.pdf') and name not in searched:
            all_pdfs.append((name, os.path.join(ARCHIVE_PDF, name)))

    for name, path in all_pdfs:
        print(f"  Scanning: {name}...")
        text = extract_pdf_text(path)
        if not text:
            continue
        has_match = any(t.lower() in text.lower() for t in SEARCH_TERMS)
        if has_match:
            # Derive a cleaner title from filename
            title = name.replace('.pdf', '').replace(' - libgen.li', '')
            title = re.sub(r'^Dick,?\s*Philip\s*(K\.?|Kindred)\s*-?\s*', '', title).strip()
            if not title:
                title = name
            results = search_text(text, title, "pdf")
            matches.extend(results)
            print(f"    >> {len(results)} match(es) in {title}")

    return matches


def search_json_files():
    """Search JSON text files in the archive."""
    matches = []
    if not os.path.exists(ARCHIVE_JSON):
        return matches

    for jf in ['texts.json', 'summary_batch_6.json']:
        path = os.path.join(ARCHIVE_JSON, jf)
        if not os.path.exists(path):
            continue
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list):
            for item in data:
                text = item.get('text', '') or ''
                if any(t.lower() in text.lower() for t in SEARCH_TERMS):
                    title = item.get('filename', item.get('id', jf))
                    results = search_text(text, title, "json_archive")
                    matches.extend(results)
    return matches


def search_passage_files():
    """Search AIpassages.md and PSYpassages.md."""
    matches = []
    for fname in ['AIpassages.md', 'PSYpassages.md']:
        path = os.path.join("C:/QueryPat", fname)
        if not os.path.exists(path):
            continue
        print(f"Searching {fname}...")
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            text = f.read()
        results = search_text(text, fname, "passages")
        if results:
            matches.extend(results)
            print(f"  Found {len(results)} match(es)")
    return matches


def deduplicate(matches):
    """Remove duplicate matches based on paragraph content."""
    seen = set()
    unique = []
    for m in matches:
        key = (m['paragraph'][:200], m['source_title'])
        if key not in seen:
            seen.add(key)
            unique.append(m)
    return unique


def generate_markdown(matches):
    """Generate the Markdown report."""
    lines = []
    lines.append("# Homeopape in Philip K. Dick's Archive")
    lines.append("")
    lines.append(f"*Search terms: {', '.join(SEARCH_TERMS)}*")
    lines.append(f"*Total matches found: {len(matches)}*")
    lines.append("")

    lines.append("## Background")
    lines.append("")
    lines.append("The **homeopape** (short for *homeostatic newspaper*) is a recurring ")
    lines.append("concept in Philip K. Dick's fiction. It refers to an automated, ")
    lines.append("self-generating news-delivery system that produces personalized ")
    lines.append("newspapers without human journalists. The device gathers information ")
    lines.append("autonomously and fabricates or reports news based on algorithmic ")
    lines.append("processes. PKD used this concept to explore themes of media ")
    lines.append("manipulation, information control, and the nature of truth.")
    lines.append("")

    # Group by source
    by_source = {}
    for m in matches:
        key = m['source_title']
        if key not in by_source:
            by_source[key] = []
        by_source[key].append(m)

    lines.append("## Table of Contents")
    lines.append("")
    for i, (source, items) in enumerate(by_source.items(), 1):
        anchor = re.sub(r'[^a-z0-9]+', '-', source.lower()).strip('-')
        lines.append(f"{i}. [{source}](#{anchor}) ({len(items)} mention{'s' if len(items) != 1 else ''})")
    lines.append("")

    lines.append("---")
    lines.append("")

    for source, items in by_source.items():
        lines.append(f"## {source}")
        lines.append(f"*Source type: {items[0]['source_type']}*")
        lines.append("")

        for j, m in enumerate(items, 1):
            lines.append(f"### Mention {j}")
            lines.append(f"*Matched term: **{m['term']}** | Paragraph index: {m['para_index']}*")
            lines.append("")

            if m['before']:
                lines.append("**Preceding paragraph:**")
                lines.append(f"> {m['before']}")
                lines.append("")

            lines.append("**Matching paragraph:**")
            # Highlight the search term
            highlighted = m['paragraph']
            for term in SEARCH_TERMS:
                highlighted = re.sub(
                    f'({re.escape(term)})',
                    r'**\1**',
                    highlighted,
                    flags=re.IGNORECASE
                )
            lines.append(f"> {highlighted}")
            lines.append("")

            if m['after']:
                lines.append("**Following paragraph:**")
                lines.append(f"> {m['after']}")
                lines.append("")

            lines.append("---")
            lines.append("")

    # Perry Kinman article note
    lines.append("## Notable Reference: \"Homeopape Malfunction\" by Perry Kinman")
    lines.append("")
    lines.append("The essay *Homeopape Malfunction* by Perry Kinman appears in ")
    lines.append("*The Palm Tree Garden of Philip K. Dick* (edited by Paul Rydeen, 1999). ")
    lines.append("The full text of this essay was not available for extraction in the ")
    lines.append("current archive, but it is listed in the table of contents and represents ")
    lines.append("dedicated scholarship on the homeopape concept in PKD's fiction.")
    lines.append("")

    lines.append("## Known PKD Works Featuring Homeopape")
    lines.append("")
    lines.append("| Work | Year | Notes |")
    lines.append("|------|------|-------|")
    lines.append("| *Ubik* | 1969 | Hotel homeopape machine produces personalized news |")
    lines.append("| *The Simulacra* | 1964 | Homeostatic newspaper as government propaganda tool |")
    lines.append("| *The Penultimate Truth* | 1964 | Underground society deceived by fabricated media |")
    lines.append("| *If There Were No Benny Cemoli* | 1963 | Short story centered on a homeostatic newspaper |")
    lines.append("| *Clans of the Alphane Moon* | 1964 | Media and information control themes |")
    lines.append("")

    return '\n'.join(lines)


def main():
    print("=" * 60)
    print("PKD Archive Search: homeopape")
    print("=" * 60)

    all_matches = []

    print("\n[1/5] Searching SQLite database...")
    all_matches.extend(search_database())

    print("\n[2/5] Searching Exegesis file...")
    all_matches.extend(search_exegesis_file())

    print("\n[3/5] Searching PDF archive...")
    all_matches.extend(search_pdfs())

    print("\n[4/5] Searching JSON archive files...")
    all_matches.extend(search_json_files())

    print("\n[5/5] Searching passage files...")
    all_matches.extend(search_passage_files())

    # Deduplicate
    all_matches = deduplicate(all_matches)
    print(f"\n{'=' * 60}")
    print(f"Total unique matches: {len(all_matches)}")

    # Generate report
    md = generate_markdown(all_matches)
    os.makedirs(os.path.dirname(OUTPUT_MD), exist_ok=True)
    with open(OUTPUT_MD, 'w', encoding='utf-8') as f:
        f.write(md)
    print(f"Report written to: {OUTPUT_MD}")

    return all_matches


if __name__ == '__main__':
    main()
