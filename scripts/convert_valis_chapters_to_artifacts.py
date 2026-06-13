#!/usr/bin/env python3
"""
Convert VALIS chapter summaries to chapter_summary artifacts.
Handles chapters 1, 5-9 from the new analysis file.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

def convert_valis_chapters():
    input_file = Path("C:\\QueryPat\\valis_chapters_1_5_9_summaries.json")
    output_dir = Path("C:\\QueryPat\\artifacts\\generated\\DOC_ARCH_OCEANOFPDF_COM_THE_VALIS_TRILOGY_PHILIP_")
    work_db = Path("C:\\QueryPat\\site\\public\\data\\works\\valis.json")

    # Load the input analysis
    with open(input_file) as f:
        chapters = json.load(f)

    print(f"[*] Processing {len(chapters)} chapters from {input_file.name}")

    # Track what we're updating
    created_artifacts = []

    for chapter_data in chapters:
        chapter_num = chapter_data["chapter_number"]

        # Create artifact
        artifact = {
            "artifact_id": f"ART_CHAPTER_SUMMARY_{chapter_num:03d}",
            "artifact_type": "chapter_summary",
            "version": "2020-12",
            "source_id": "DOC_ARCH_OCEANOFPDF_COM_THE_VALIS_TRILOGY_PHILIP_",
            "generated_at": datetime.now().isoformat(),
            "generated_by": "reading_notes_agent",
            "work_id": "WORK_valis",
            "chapter_number": chapter_num,
            "chapter_title": chapter_data["chapter_title"],
            "summary": chapter_data["summary"],
            "locations": [{"name": loc} for loc in chapter_data.get("locations_mentioned", [])],
            "characters": [{"name": char} for char in chapter_data.get("characters_appearing", [])],
            "themes": [{"name": theme} for theme in chapter_data.get("themes_explored", [])],
            "theological_concepts": [
                {"name": concept} for concept in chapter_data.get("theological_concepts", [])
            ],
            "philosophical_concepts": [
                {"name": concept} for concept in chapter_data.get("philosophical_concepts", [])
            ],
            "key_events": chapter_data.get("key_events", []),
            "narrative_observations": chapter_data.get("narrative_observations", "")
        }

        # Write artifact
        artifact_file = output_dir / f"chapter_summary.{chapter_num:03d}.json"
        with open(artifact_file, 'w') as f:
            json.dump(artifact, f, indent=2)

        created_artifacts.append({
            "chapter_number": chapter_num,
            "file": artifact_file.name
        })
        print(f"[OK] Chapter {chapter_num}: {artifact_file.name}")

    # Update work database
    if work_db.exists():
        with open(work_db) as f:
            work_data = json.load(f)
    else:
        work_data = {
            "work_id": "WORK_valis",
            "title": "VALIS",
            "author": "Philip K. Dick",
            "year_published": 1981,
            "chapter_summaries": [],
            "all_locations": [],
            "all_themes": [],
            "all_characters_mentioned": [],
            "reading_notes_artifacts": []
        }

    # Update chapter summaries
    for chapter_data in chapters:
        chapter_num = chapter_data["chapter_number"]

        # Check if already exists
        existing = [c for c in work_data["chapter_summaries"] if c.get("chapter_number") == chapter_num]

        chapter_entry = {
            "chapter_number": chapter_num,
            "chapter_title": chapter_data["chapter_title"],
            "locations": chapter_data.get("locations_mentioned", []),
            "themes": chapter_data.get("themes_explored", []),
            "characters": chapter_data.get("characters_appearing", []),
            "artifact_id": f"ART_CHAPTER_SUMMARY_{chapter_num:03d}"
        }

        if existing:
            # Update existing
            work_data["chapter_summaries"] = [
                chapter_entry if c.get("chapter_number") == chapter_num else c
                for c in work_data["chapter_summaries"]
            ]
        else:
            # Add new
            work_data["chapter_summaries"].append(chapter_entry)

    # Consolidate unique locations, themes, characters
    all_locations = set()
    all_themes = set()
    all_characters = set()

    for chapter in work_data["chapter_summaries"]:
        all_locations.update(chapter.get("locations", []))
        all_themes.update(chapter.get("themes", []))
        all_characters.update(chapter.get("characters", []))

    work_data["all_locations"] = sorted(list(all_locations))
    work_data["all_themes"] = sorted(list(all_themes))
    work_data["all_characters_mentioned"] = sorted([
        {"name": char} for char in list(all_characters)
    ], key=lambda x: x["name"])

    work_data["reading_notes_artifacts"] = [
        f"ART_CHAPTER_SUMMARY_{c.get('chapter_number'):03d}"
        for c in sorted(work_data["chapter_summaries"], key=lambda x: x.get("chapter_number", 0))
    ]

    # Write updated work database
    with open(work_db, 'w') as f:
        json.dump(work_data, f, indent=2)

    print(f"\n[OK] Updated {work_db}")
    print(f"  - {len(work_data['chapter_summaries'])} chapters total")
    print(f"  - {len(work_data['all_locations'])} unique locations")
    print(f"  - {len(work_data['all_themes'])} unique themes")
    print(f"  - {len(work_data['all_characters_mentioned'])} unique characters")

if __name__ == "__main__":
    convert_valis_chapters()
