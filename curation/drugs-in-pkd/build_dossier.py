#!/usr/bin/env python3
"""
Write dossier.json from the authored module dossier_sections.py.

dossier.json is what the seeder reads; the prose and browse configuration live
in Python so they stay readable and diffable.

    python curation/drugs-in-pkd/build_dossier.py
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import dossier_sections as d  # noqa: E402


def main():
    out = {
        'topic': 'drugs-in-pkd',
        'title': d.TITLE,
        'subtitle': d.SUBTITLE,
        'card_description': d.CARD_DESCRIPTION,
        'note': ('Hand-authored editorial prose, generated from dossier_sections.py. '
                 'Citations in {{double braces}} are finding ids from '
                 'evidence-inventory.json. Registers: A = PKD\'s own words, B = '
                 'primary-source fact, C = scholarly argument, D = portal-editor '
                 'inference.'),
        'sections': d.SECTIONS,
        'fields': d.FIELDS,
        'related_thinkers': d.RELATED_THINKERS,
        'open_questions': d.OPEN_QUESTIONS,
        'browse': {
            'intro': d.BROWSE_INTRO,
            'groups': d.GROUPS,
            'facet_kinds': [{'kind': k, 'label': lbl} for k, lbl in d.FACET_KINDS],
            'facets': d.FACETS,
            'see_also': d.SEE_ALSO,
        },
        'contradictions': [
            {'summary': s, 'explanation': e, 'type': t, 'fragment_a': a, 'fragment_b': b}
            for s, e, t, a, b in d.CONTRADICTIONS
        ],
    }
    path = HERE / 'dossier.json'
    path.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding='utf-8')
    words = sum(len(p.split()) for s in d.SECTIONS for p in s['body'])
    print(f'{len(d.SECTIONS)} sections, ~{words:,} words, {len(d.FACETS)} facets, '
          f'{len(d.GROUPS)} groups, {len(d.CONTRADICTIONS)} contradictions')
    for s in d.SECTIONS:
        print(f'  [{s["register"]}] {s["heading"]}')


if __name__ == '__main__':
    main()
