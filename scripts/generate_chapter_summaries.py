#!/usr/bin/env python3
"""
Generate chapter_summary artifacts for PKD novels.
Reads extracted markdown files and creates structured artifacts.
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime, timezone

# Add artifacts to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'artifacts'))
from artifact_types import make_artifact_id, utc_now, write_artifact, SCHEMA_VERSION

def extract_chapters_from_ubik(markdown_path):
    """Parse Ubik markdown and extract chapter structure."""
    with open(markdown_path, 'r', encoding='utf-8') as f:
        content = f.read()

    chapters = []
    # Split by chapter headers
    parts = re.split(r'## \*\*Chapter (\d+)\*\*', content)

    for i in range(1, len(parts), 2):
        if i + 1 < len(parts):
            chapter_num = int(parts[i])
            chapter_text = parts[i + 1]

            # Extract chapter content (first 3000 chars for preview)
            chapter_content = chapter_text[:3000].strip()

            # Try to find advertising slogan at start
            slogan_match = re.match(r'^([^.!?]+[.!?])\s*', chapter_text)
            slogan = slogan_match.group(1) if slogan_match else "Unknown"

            chapters.append({
                'number': chapter_num,
                'slogan': slogan,
                'content_preview': chapter_content,
                'full_length': len(chapter_text)
            })

    return chapters

def main():
    ubik_path = Path('C:/QueryPat/database/extracted_markdown/DOC_ARCH_BOOK_PKD_UBIK.md')

    if not ubik_path.exists():
        print(f"Error: {ubik_path} not found")
        return 1

    print(f"Reading {ubik_path}...")
    chapters = extract_chapters_from_ubik(ubik_path)
    print(f"Extracted {len(chapters)} chapters from Ubik")

    # Print chapter summaries
    for ch in chapters[:5]:
        print(f"\nChapter {ch['number']}")
        print(f"  Slogan: {ch['slogan'][:80]}")
        print(f"  Content length: {ch['full_length']} characters")

    return 0

if __name__ == '__main__':
    sys.exit(main())
