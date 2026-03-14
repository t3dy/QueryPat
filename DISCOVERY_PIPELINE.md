# Discovery Pipeline: Development Log and Technical Documentation

## Overview

The corpus discovery pipeline (`scripts/discover/`) is a Stage 2b addition to the QueryPat build system. It scans all available corpus text to identify candidate entities (terms, people, works, events) that are **not yet present** in the database. Output is JSON review files only; the pipeline never writes to the database.

**Runtime:** ~3.0s against 10.4M chars of corpus text
**Date completed:** 2026-03-13
**Files produced:** 4 JSON discovery files totaling ~2.4MB

---

## Architecture: Batch-by-Substrate

The pipeline was refactored from an initial per-chunk extraction architecture to a **batch-by-substrate** design. The key architectural constraints (specified by the project owner):

1. **Extraction batched by corpus substrate, not by extractor-per-chunk** -- the two text sources are materialized and scanned separately
2. **Provenance preserved** -- every hit is keyed to its `seg_id` or `doc_id`
3. **One corpus loader that materializes all relevant source rows once** -- a single SQL query per substrate
4. **One normalization pass per row** -- text cleaning happens at materialization, not per-matcher
5. **Precompiled matcher sets for each entity family** -- regex patterns compiled once at module import time
6. **Aggregation only after hits are attached to source IDs** -- no premature collapsing of provenance

### What the architecture explicitly avoids

- Collapsing the corpus into a provenance-free global scan
- Recomputing regex patterns inside inner loops
- Treating Exegesis segments and archive documents as the same substrate

---

## Corpus Substrates

### Substrate A: Exegesis Segments (`segments.raw_text`)
- **882 rows**, ~9.8M chars
- Philip K. Dick's Exegesis notebook entries
- Dense philosophical/theological content, heavy use of capitalized terms
- `concise_summary` concatenated into text for richer extraction
- Source IDs: `seg_id` values (e.g., `seg_001`, `seg_002`)

### Substrate B: Archive Documents (`document_texts.text_content`)
- **180 rows**, ~603K chars
- Extracted text from PDFs: biographies, scholarship articles, letters, newspaper clippings
- More conventional prose with biographical narratives
- Filtered to exclude `doc_type = 'exegesis_section'` (avoids double-counting)
- Source IDs: `doc_id` values (e.g., `divine-invasions-a-life-of-phi-lawrence-sutin`)

---

## Pipeline Steps

### Step 1: Materialize corpus text
```
materialize_segments(db)   -> list[(seg_id, title, text)]
materialize_documents(db)  -> list[(doc_id, title, category, text)]
```
One SQL query per substrate. Text is normalized once (control chars stripped, whitespace collapsed).

### Step 2: Load existing entities
```
load_existing_entities(db) -> dict with keys: terms, names, events, term_slugs, name_slugs
```
Loads all existing terms + aliases, names + aliases, and biography events for deduplication filtering.

### Step 3+4: Batched matching
```
scan_substrate(rows, source_type, families, label) -> list[Hit]
```
Iterates over materialized rows, calling `match_all()` from `matchers.py` for each row. All four entity families (terms, people, works, events) run in a single pass per row. Hits carry full provenance (`source_id`, `source_type`).

### Step 5: Aggregation
```
aggregate_hits(hits, segment_titles, document_titles) -> dict[family -> list[candidate]]
```
Groups hits by `(entity_family, normalized_name)`. For each group:
- Picks most frequent surface form as canonical name
- Collects unique source documents with provenance
- Deduplicates snippets (max 5 per candidate)
- Counts frequency and source spread

### Step 6: Filter, score, finalize
```
filter_candidates()   -- frequency thresholds + dedup against existing entities
score_and_finalize()  -- confidence scoring + proposed ID generation
```

---

## Entity Families and Matchers

All matchers are in `scripts/discover/matchers.py`. Patterns are compiled once at module import time.

### People (`match_people`)
- **Regex:** `\b([A-Z][a-z]{1,15})\s+([A-Z][a-z]{2,20})\b`
- Matches "Firstname Lastname" patterns
- **Filters:** Four frozen sets prevent false positives:
  - `NOT_PERSON` (78 entries): Known non-person bigrams ("Science Fiction", "San Francisco", "Scanner Darkly")
  - `AMBIGUOUS_FIRST` (138 entries): Words that start sentences capitalized ("The", "This", "After", "Do", "We", "Is", "Hence")
  - `NOT_SURNAME` (120+ entries): Common nouns/adjectives never used as surnames ("Time", "War", "God", "Gnostic", "Copyright", "Church")
  - `NOT_FIRST_NAME` (48 entries): Words never used as first names ("Dick", "Valis", "Gnostic", "Congress", "British")

### Terms (`match_terms`)
- **RE_TERM_CAP:** Capitalized multi-word phrases (2-3 words): `[A-Z][a-z]+\s+[A-Z][a-z]+`
- **RE_TERM_CAPS:** ALL-CAPS acronyms (3-12 chars): `[A-Z]{3,12}`
- **RE_TERM_HYPHEN:** Hyphenated compounds: `[A-Z][a-z]+-[a-z]+`
- Filters out noise via `is_noise()` (stop words, abbreviations, short strings)
- Skips 2-word capitalized phrases that look like person names

### Works (`match_works`)
- **RE_WORK_ITALIC:** `*Italic Title*` or `_Italic Title_` patterns
- **RE_WORK_QUOTED:** `"Quoted Title"` or Unicode quote patterns
- Minimum title length: 4 chars

### Events (`match_events`)
- **RE_EVENT_YEAR:** "In YYYY, sentence." patterns
- **RE_EVENT_MONTH:** "In Month YYYY, sentence." patterns
- **RE_EVENT_PKD:** "Dick verbed ... in YYYY" patterns
- Year range filtered to 1920-1985 (PKD's lifetime + context)

---

## Confidence Scoring

### Entity scoring (terms, people, works)
```
score = 0.30 * freq_norm + 0.25 * spread_norm + 0.25 * context + 0.20 * domain
```
- **freq_norm** (30%): Frequency normalized against max in family
- **spread_norm** (25%): Source count normalized against max in family
- **context** (25%): Proportion of snippets containing PKD domain markers
- **domain** (20%): 0.5 if candidate name itself contains PKD markers, else 0.0

### Event scoring
- Base score 0.3
- +0.3 if description mentions Dick/PKD/Philip
- +0.2 if description contains biographical verbs (married, moved, wrote, published, etc.)

### PKD domain markers
```
Dick|PKD|Philip K|Exegesis|VALIS|Ubik|Zebra|2-3-74|Black Iron|Palm Tree|
Gnostic|plasmate|homoplasmate|demiurge|anamnesis
```

---

## Output Files

All output goes to `scripts/discover/output/`.

### discovered_terms.json (264 candidates, 729KB)
Each entry:
```json
{
  "name": "BIP",
  "frequency": 213,
  "source_count": 213,
  "source_documents": [{"source_id": "...", "source_type": "segment", "source_title": "..."}],
  "example_snippets": ["...context around match..."],
  "match_types": ["caps"],
  "confidence_score": 0.700,
  "proposed_slug": "bip",
  "proposed_id": "TERM_bip"
}
```
**Top 10:** BIP, Palm Tree Garden, The Black Iron, MITHC, PKDS, Ubik-like, Philip Kindred Dick, The Palm Tree, Publication Data Dick, Real Ubik Please

### discovered_people.json (524 candidates, 789KB)
Each entry adds:
```json
{
  "proposed_entity_type": "historical_person",
  "is_scholar": true
}
```
**Top 10:** Le Guin, Gregg Rickman, Robert Anton (Wilson), Roger Zelazny, Erik Davis, Philip Kindred, St Elmo, Timothy Archer, Tessa Dick, Pat Conley

Includes both real people (scholars, PKD contacts) and PKD fictional characters.

### discovered_works.json (600 candidates, 830KB)
**Top 5:** MITHC, Faith of, Valis Regained, Palm Tree Garden, I am Ubik

### discovered_events.json (34 candidates, 35KB)
Each entry adds:
```json
{
  "year": "1928",
  "date_raw": "1928",
  "description": "Dick was born in Chicago"
}
```
**Top events:** 1928 birth, 1982 death, 1971 San Rafael move, 1974 Exegesis references, 1975 Umbrella of Light

---

## File Inventory

### Active pipeline files
| File | Size | Purpose |
|------|------|---------|
| `scripts/discover/__init__.py` | 32B | Package init |
| `scripts/discover/matchers.py` | 17KB | Precompiled regex matchers, Hit class, noise filter sets |
| `scripts/discover/discovery_pipeline.py` | 22KB | Main pipeline: materialization, scanning, aggregation, scoring |

### Legacy/superseded files (still present, no longer imported)
| File | Size | Status |
|------|------|--------|
| `scripts/discover/corpus_reader.py` | 5.4KB | Superseded by materialization functions in discovery_pipeline.py |
| `scripts/discover/extractors.py` | 12KB | Superseded by matchers.py |
| `scripts/discover/scoring.py` | 6.6KB | Logic moved inline into discovery_pipeline.py |

### Output files
| File | Size | Candidates |
|------|------|------------|
| `scripts/discover/output/discovered_terms.json` | 729KB | 264 |
| `scripts/discover/output/discovered_people.json` | 789KB | 524 |
| `scripts/discover/output/discovered_works.json` | 830KB | 600 |
| `scripts/discover/output/discovered_events.json` | 35KB | 34 |

---

## Development History

### Phase 1: Initial implementation
- Built `corpus_reader.py` to read text from SQLite
- Built `extractors.py` with per-chunk extractors returning dicts
- Built `scoring.py` for dedup and confidence scoring
- Built `discovery_pipeline.py` orchestrating all three
- **Problem:** First run timed out after 5 minutes processing 10M chars
- **Fix:** Rewrote extractors to return lightweight tuples, reduced snippet context from 200 to 150 chars
- **Result:** 2.3s runtime, valid JSON output

### Phase 2: Noise filtering iterations
- **Problem:** People extractor matched "So Valis", "My God", "Then Valis" as person names
- **Fix:** Expanded `AMBIGUOUS_FIRST` frozenset to include common English words that start sentences capitalized
- **Problem:** "Publication Data", "San Francisco" matched as person names
- **Fix:** Expanded `NOT_PERSON` frozenset with geographic names and publishing metadata

### Phase 3: Architectural refactoring (user-directed)
The project owner specified a batch-by-substrate architecture. Complete rewrite:
- Created `matchers.py` with precompiled patterns, Hit class, and `match_all()` entry point
- Rewrote `discovery_pipeline.py` with `materialize_segments()`, `materialize_documents()`, `scan_substrate()`, `aggregate_hits()`, `filter_candidates()`, `score_and_finalize()`
- Old modules (`corpus_reader.py`, `extractors.py`, `scoring.py`) superseded but not deleted

### Phase 4: People matcher quality tuning (current session)
After verifying the refactored pipeline ran correctly (3.0s, 22,428 hits), inspected output quality:

**Iteration 1:** Top 20 people included "Scanner Darkly", "Do Androids", "We Can", "Congress Cataloging", "Inc Stable", "Is Valis", "Hence Valis", "Therefore Valis"
- Added these to `NOT_PERSON`
- Added "Do", "We", "Is", "He", "She", "It", "Hence", "Therefore" etc. to `AMBIGUOUS_FIRST`
- People dropped from 835 to 786

**Iteration 2:** Top 20 still had "Hermetic Gnostic", "Gnostic Kerygma", "Dick The", "Valis Regained", "Oh God", "Martian Time", "Build You", "Dick Copyright"
- Created `NOT_SURNAME` frozenset (common nouns/adjectives that are never surnames)
- Created `NOT_FIRST_NAME` frozenset (words that are never first names)
- Added filtering logic: `first in NOT_FIRST_NAME or last in NOT_SURNAME`
- People dropped from 786 to 627

**Iteration 3:** "Marin County", "Qua Zebra", "Gnostic Xtian", "Anamnesis Then", "Dick Cover", "Dick Essays" still present
- Massively expanded `NOT_SURNAME` (120+ entries covering places, religion terms, publishing metadata, fiction terms)
- Expanded `NOT_FIRST_NAME` (48 entries covering nationalities, PKD terms, metadata words)
- People dropped from 627 to 524

**Final result:** Top 25 people are all legitimate -- real PKD-orbit people (Le Guin, Gregg Rickman, Roger Zelazny, Erik Davis, Norman Spinrad, Lawrence Sutin, Kyle Arnold, Patricia Warrick, Umberto Rossi, Charles Platt, Frank Bertrand, Scott Meredith) plus PKD characters (Timothy Archer, Pat Conley, Bob Arctor, Ella Runciter).

---

## Usage

### Basic run (all families, default thresholds)
```bash
python scripts/discover/discovery_pipeline.py
```

### Custom thresholds
```bash
python scripts/discover/discovery_pipeline.py --min-frequency 5 --min-sources 3
```

### Specific entity types
```bash
python scripts/discover/discovery_pipeline.py --types terms,people
```

### Single substrate
```bash
python scripts/discover/discovery_pipeline.py --segments-only    # Exegesis only
python scripts/discover/discovery_pipeline.py --documents-only   # Archive PDFs only
```

### Custom database
```bash
python scripts/discover/discovery_pipeline.py --db path/to/other.sqlite
```

### Integration with build_all.py
```python
from discover.discovery_pipeline import run as run_discovery
run_discovery(db, source_dir)
```
The `run()` function accepts the same `(db, source_dir)` signature as other Stage 2 scripts.

---

## Known Limitations

1. **People matcher is regex-based** -- relies on "Firstname Lastname" pattern, which catches any two capitalized words. Precision depends on extensive blocklists. Some noise remains below rank 25.

2. **Works matcher has false positives** -- "Faith of" (from *Faith of Our Fathers*), quoted sentence fragments, and Exegesis-style italicized phrases all match.

3. **Event extraction is sparse** -- only 34 candidates found, because the date-anchored patterns require specific syntactic frames ("In YYYY, ..." or "Dick verbed ... in YYYY").

4. **No lemmatization or NLP** -- purely regex-based. A spaCy/stanza NER pass would dramatically improve people detection but add a heavy dependency.

5. **Term dedup is name-based only** -- "Palm Tree Garden" and "The Palm Tree" are separate candidates because normalization doesn't strip articles or attempt semantic dedup.

6. **Legacy files remain** -- `corpus_reader.py`, `extractors.py`, and `scoring.py` are superseded but still on disk. They can be safely deleted.

---

## Existing Database Entity Counts (at time of run)

| Entity | Count | Notes |
|--------|-------|-------|
| Terms + aliases | 936 | 310 published + 601 background + aliases |
| Names + aliases | 491 | 410 entities + aliases |
| Biography events | 431 | 646 total, 431 with dates |
| Segments | 882 | Exegesis chunks |
| Documents with text | 180 | Archive PDFs with extracted text |
