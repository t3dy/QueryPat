# Systematic Reading and Note-Taking System

## Overview

This document describes the system for comprehensively reading and annotating PKD's novels, stories, letters, biography, and Exegesis without re-reading. Each reading produces durable artifacts that feed back into the database and website entries.

## Artifact Types for Reading Notes

### 1. ChapterSummaryArtifact
**Used for:** Novels, novellas, stories, extended works.

**Captures:**
- Chapter/section number and title
- Plot summary (paragraph-length)
- All locations mentioned with context
- Characters appearing with their actions
- Themes explored
- Theological and philosophical concepts
- Key events and their significance
- Connections to other works
- Symbolic elements
- Narrative voice observations
- Questions raised by the text

**Location:** `artifacts/generated/<WORK_ID>/chapter_summary.<chapter_number>.json`

**Prevents re-reading by:** Full paragraph summary, explicit extraction of entities and themes, connections noted, so returning to this artifact requires no source re-reading.

### 2. ExegesisCunkAnalysisArtifact
**Used for:** The Exegesis entries/chunks (3-74, entries, dated sections, etc.)

**Captures:**
- Chunk identifier (entry number, date, folder reference)
- What PKD is discussing (summary)
- Theological themes with tradition context (Gnosticism, Christian theology, Neoplatonism, etc.)
- Philosophical concepts developed
- Mystical experiences discussed
- Connections to published works (thematic source, character inspiration, plot element)
- Key figures mentioned
- Spiritual claims and confidence levels
- Contradictions or revisions of earlier positions
- Theological influences evident (Christian, Gnostic, Buddhist, etc.)
- Questions posed
- How this relates to other Exegesis sections

**Location:** `artifacts/generated/<EXEGESIS_SOURCE_ID>/exegesis_chunk_analysis.<date_or_entry>.json`

**Prevents re-reading by:** Complete capture of theological argument, tracked contradictions, evidence excerpts, connections mapped.

### 3. LetterAnnotationArtifact
**Used for:** PKD's letters (from Selected Letters, other collections)

**Captures:**
- Letter date and recipient
- Summary of content
- Biographical events mentioned
- Relationship with recipient and tone
- Literary/intellectual discussions
- Works mentioned with context
- Locations referenced
- People mentioned
- Theological/spiritual content
- Personal struggles
- Health/substance references
- Connections to Exegesis themes
- Key quotes with significance

**Location:** `artifacts/generated/<LETTERS_SOURCE_ID>/letter_annotation.<date>.json`

**Prevents re-reading by:** Full summary, extracted entities, quote collection, so all essential information is preserved structurally.

## Database Updates

### Work JSON Files (`site/public/data/works/<work-id>.json`)

Each work record will have these fields added/updated:

```json
{
  "work_id": "WORK_ubik",
  "canonical_title": "Ubik",
  "chapter_summaries": [
    {
      "chapter_number": 1,
      "chapter_title": "Runciter",
      "locations": ["Luna"],
      "themes": ["consciousness", "identity"],
      "artifact_id": "ART_CHAPTER_SUMMARY_WORK_ubik_001"
    }
  ],
  "all_locations": ["location1", "location2"],
  "all_themes": ["theme1", "theme2"],
  "all_characters_mentioned": [{"name": "character", "role": "protagonist"}],
  "connected_biographical_events": [
    {
      "bio_id": "pkd_bio_1969_ubik",
      "description": "event"
    }
  ],
  "reading_notes_artifacts": [
    "ART_CHAPTER_SUMMARY_WORK_ubik_001",
    "ART_CHAPTER_SUMMARY_WORK_ubik_002"
  ]
}
```

### Biography Event Records (`site/public/data/biography/events.json`)

Biography events will have these fields:

```json
{
  "bio_id": "pkd_bio_1968_androids",
  "date": "1968",
  "category": "publication",
  "event": "Publishes Do Androids Dream of Electric Sheep? through Doubleday",
  "source": "Sutin",
  "source_type": "curated",
  "related_works": ["WORK_do_androids_dream_of_electric_sheep"],
  "related_letters": ["letter_date_1"],
  "related_exegesis_entries": ["exegesis_chunk_entry_42"],
  "locations": ["New York", "Beverly Hills"],
  "themes": ["publication", "relationship_with_publishers"]
}
```

## Reading Workflow

1. **Inventory** — List all novels, stories, letters, Exegesis chunks to read
2. **Priority** — Group by type (novels first, then stories, then letters, then Exegesis)
3. **Read** — Go through each source, create chapter_summary / letter_annotation / exegesis_chunk_analysis artifacts
4. **Extract** — Build list of:
   - All unique locations across all sources
   - All unique themes
   - All unique character/people names
   - All biographical events
   - All theological/philosophical concepts
5. **Cross-Link** — Update work JSON files with chapter summary info and connections
6. **Update Biography** — Ensure events have work/letter/Exegesis connections
7. **Validate** — Run `artifacts/validate_artifacts.py` to ensure all artifacts are valid

## Implementation Notes

- **No re-reading:** Once an artifact is created, the source is no longer needed for reference purposes. All extracted information lives in the artifact.
- **Evidence preservation:** Each artifact contains locators (page ranges, entry dates) so if clarification is needed, the source can be pinpointed without full re-reading.
- **Incremental:** Can be done one work/section at a time. Artifacts are durable and persist.
- **Cross-references:** As artifacts are created, the system notes connections (e.g., "this theme appears in Chapter 5 of Ubik and in Exegesis Entry 42").

## Validation

All generated artifacts must pass schema validation:

```bash
python artifacts/validate_artifacts.py artifacts/generated/
```

Validation checks:
- Schema compliance (required fields, types, enums)
- Required fields present
- Evidence locations properly formatted (if applicable)
- Agent roles match produces/consumes contract
