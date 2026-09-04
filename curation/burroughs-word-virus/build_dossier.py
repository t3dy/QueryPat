#!/usr/bin/env python3
"""
Merge the authored essay in dossier_sections.py into dossier.json.

dossier.json stays the file the seeder reads; the prose lives in a Python module
so it is readable and diffable. Everything else in dossier.json — the structured
fields, the related thinkers, the open questions — is preserved as it stands.

    python curation/burroughs-word-virus/build_dossier.py
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from dossier_sections import SECTIONS, SUBTITLE  # noqa: E402


def main():
    path = HERE / 'dossier.json'
    d = json.loads(path.read_text(encoding='utf-8'))
    d['subtitle'] = SUBTITLE
    d['sections'] = SECTIONS
    path.write_text(json.dumps(d, indent=1, ensure_ascii=False), encoding='utf-8')
    words = sum(len(p.split()) for s in SECTIONS for p in s['body'])
    print(f'{len(SECTIONS)} sections, '
          f'{sum(len(s["body"]) for s in SECTIONS)} paragraphs, ~{words:,} words')
    for s in SECTIONS:
        print(f'  [{s["register"]}] {s["heading"]}')


if __name__ == '__main__':
    main()
