#!/usr/bin/env python3
"""
Convert chapter analysis JSON into chapter_summary artifacts.
Writes artifacts to artifacts/generated/<WORK_ID>/ directory.
Updates work database with chapter metadata.
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timezone

# Add artifacts to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'artifacts'))
from artifact_types import make_artifact_id, utc_now, write_artifact, SCHEMA_VERSION

def load_chapter_analysis(json_path):
    """Load chapter analysis from JSON file."""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_chapter_summary_artifact(chapter_data, work_id, source_id):
    """Convert chapter analysis to chapter_summary artifact."""
    ch_num = chapter_data['chapter_number']

    artifact = {
        'artifact_id': make_artifact_id('chapter_summary', source_id, f'CH{ch_num:03d}'),
        'artifact_type': 'chapter_summary',
        'schema_version': SCHEMA_VERSION,
        'generated_at': utc_now(),
        'source_id': source_id,
        'work_id': work_id,
        'chapter_number': ch_num,
        'chapter_title': chapter_data.get('chapter_title', f'Chapter {ch_num}'),
        'section_range': chapter_data.get('section_range'),
        'summary': chapter_data.get('summary', ''),
        'extracted_entities': {
            'locations': [
                {
                    'name': loc.get('name') if isinstance(loc, dict) else loc,
                    'context': loc.get('context') if isinstance(loc, dict) else None,
                    'significance': loc.get('significance') if isinstance(loc, dict) else None
                }
                for loc in chapter_data.get('locations_mentioned', [])
            ],
            'characters': [
                {
                    'name': char.get('name') if isinstance(char, dict) else char,
                    'role_in_chapter': char.get('role') if isinstance(char, dict) else None,
                    'key_actions': char.get('key_actions') if isinstance(char, dict) else None
                }
                for char in chapter_data.get('characters_appearing', [])
            ],
            'themes': chapter_data.get('themes_explored', []),
            'theological_concepts': [
                {
                    'concept': tc.get('concept') if isinstance(tc, dict) else tc,
                    'context': tc.get('context') if isinstance(tc, dict) else None,
                    'theological_frame': tc.get('tradition') if isinstance(tc, dict) else None
                }
                for tc in chapter_data.get('theological_concepts', [])
            ],
            'philosophical_concepts': [
                {
                    'concept': pc.get('concept') if isinstance(pc, dict) else pc,
                    'context': pc.get('context') if isinstance(pc, dict) else None
                }
                for pc in chapter_data.get('philosophical_concepts', [])
            ]
        },
        'key_events': [
            {
                'event': evt.get('event') if isinstance(evt, dict) else evt,
                'significance': evt.get('significance') if isinstance(evt, dict) else None,
                'relates_to_biography': evt.get('relates_to_biography') if isinstance(evt, dict) else None
            }
            for evt in chapter_data.get('key_events', [])
        ],
        'connections_to_other_works': chapter_data.get('connections_to_other_works', []),
        'narrative_voice_observations': chapter_data.get('narrative_voice', None),
        'symbolic_elements': chapter_data.get('symbolic_elements', []),
        'questions_raised': chapter_data.get('questions_raised', []),
        'reading_notes': chapter_data.get('reading_notes'),
        'generated_by': {
            'agent_role': 'reading_notes_agent',
            'name': 'create_chapter_summary_artifacts.py',
            'model': 'claude-opus-4-8',
            'prompt_version': 'ubik_chapter_analysis.v1'
        },
        '_filename': f'chapter_summary.{ch_num:03d}.json'
    }

    return artifact

def main():
    # Load both chapter analysis files
    chapters_1_5_path = Path('C:/QueryPat/ubik_chapters_1_5_analysis.json')
    chapters_6_17_path = Path('C:/QueryPat/ubik_chapters_6_17_analysis.json')
    work_db_path = Path('C:/QueryPat/site/public/data/works/ubik.json')

    all_chapters = []

    if chapters_1_5_path.exists():
        data_1_5 = load_chapter_analysis(chapters_1_5_path)
        all_chapters.extend(data_1_5.get('chapters_analyzed', []))
        print(f"Loaded {len(data_1_5.get('chapters_analyzed', []))} chapters from 1-5 analysis")

    if chapters_6_17_path.exists():
        data_6_17 = load_chapter_analysis(chapters_6_17_path)
        all_chapters.extend(data_6_17.get('chapters_analyzed', []) if isinstance(data_6_17, dict) and 'chapters_analyzed' in data_6_17 else (data_6_17 if isinstance(data_6_17, list) else []))
        print(f"Loaded remaining chapters from 6-17 analysis")

    print(f"\nTotal chapters to process: {len(all_chapters)}")

    # Create artifacts
    artifacts = []
    for chapter in all_chapters:
        try:
            artifact = create_chapter_summary_artifact(
                chapter,
                work_id='WORK_ubik',
                source_id='DOC_ARCH_BOOK_PKD_UBIK'
            )
            written_path = write_artifact(artifact)
            artifacts.append(artifact)
            print(f"[OK] Chapter {chapter['chapter_number']}: {written_path.name}")
        except Exception as e:
            print(f"[ERROR] Chapter {chapter['chapter_number']}: {e}")

    print(f"\nWrote {len(artifacts)} chapter artifacts")

    # Update work database
    if work_db_path.exists():
        with open(work_db_path, 'r', encoding='utf-8') as f:
            work_data = json.load(f)

        # Collect metadata
        all_locations = set()
        all_themes = set()
        all_characters = set()
        chapter_summaries = []

        for art in artifacts:
            ch_num = art['chapter_number']
            ch_title = art['chapter_title']

            # Extract entities
            for loc in art['extracted_entities']['locations']:
                if loc.get('name'):
                    all_locations.add(loc['name'])

            for theme in art['extracted_entities']['themes']:
                if theme:
                    all_themes.add(theme)

            for char in art['extracted_entities']['characters']:
                if char.get('name'):
                    all_characters.add(char['name'])

            # Add chapter summary
            chapter_summaries.append({
                'chapter_number': ch_num,
                'chapter_title': ch_title,
                'locations': [loc.get('name') for loc in art['extracted_entities']['locations'] if loc.get('name')],
                'themes': art['extracted_entities']['themes'],
                'artifact_id': art['artifact_id']
            })

        # Update work record
        work_data['chapter_summaries'] = sorted(chapter_summaries, key=lambda x: x['chapter_number'])
        work_data['all_locations'] = sorted(list(all_locations))
        work_data['all_themes'] = sorted(list(all_themes))
        work_data['all_characters_mentioned'] = sorted([{'name': c} for c in all_characters], key=lambda x: x['name'])
        work_data['reading_notes_artifacts'] = [art['artifact_id'] for art in artifacts]

        with open(work_db_path, 'w', encoding='utf-8') as f:
            json.dump(work_data, f, indent=2, ensure_ascii=False)

        print(f"\n[OK] Updated {work_db_path}")
        print(f"  - {len(chapter_summaries)} chapters")
        print(f"  - {len(all_locations)} unique locations")
        print(f"  - {len(all_themes)} unique themes")
        print(f"  - {len(all_characters)} unique characters")

    return 0

if __name__ == '__main__':
    sys.exit(main())
