# QueryPat Content Improvement Plan

## Overview

This plan addresses writing quality across all text channels in the portal, prioritized by visibility and scholarly value. The project was built by integrating three prior systems (ExegesisAnalysis chunk summaries, ExegesisBrowser dictionary pipeline, PaulPKDarchive catalog) into a unified SQLite database with a React static site. The researcher's core interests are: PKD's philosophical and theological vocabulary, the biographical reality behind the visionary claims, and critical engagement with contradictions across sources.

---

## Channel 1: Dictionary Entries (terms table)

**Current state:** 50 accepted, 260 provisional, 601 background. Most entries have only machine-extracted card_description (1-2 sentences). Full scholarly descriptions are missing for nearly all terms.

### Priority A — 50 Accepted Terms (highest visibility)
These are the terms promoted via LLM chat seed extraction: historical figures (Plotinus, Meister Eckhart, Jakob Böhme, Mani, Simon Magus...), PKD bespoke terms (Zebra, VALIS, The Empire Never Ended, homoplasmate...), and philosophical concepts (anamnesis, hypostasis, the Forms...).

**Improvement approach:**
- For each accepted term, generate a full_description (500-1500 words) structured as:
  1. Technical/historical definition
  2. How PKD uses or transforms the concept in the Exegesis
  3. Key passages where the term appears (linked to segments)
  4. Relationship to other terms in the dictionary
  5. Scholarly caution / interpretive note where appropriate
- Source: Cross-reference the Exegesis chunk summaries, evidence packets, and the LLM chat PDFs where these terms were discussed in depth
- Review state: machine-drafted → human-revised after editorial pass

### Priority B — 260 Provisional Terms
These have machine-extracted descriptions from dictionary_expanded.json but lack the PKD-specific interpretive layer.

**Improvement approach:**
- Batch enrich: for terms with ≥10 segment links, generate a card_description that contextualizes the term within PKD's usage
- For terms with <10 links, review for possible demotion to background or promotion to accepted
- Focus especially on: theological terms (Gnostic, Neoplatonic, Christian mystical), literary references (works PKD cites), and people (correspondents, philosophers, theologians)

### Priority C — 601 Background Terms
Many are noise (common words extracted by entity recognition). Some are genuine concepts that deserve promotion.

**Improvement approach:**
- Triage pass: identify terms that appear in the LLM chat discussions or in the key biographical sources
- Promote genuine philosophical/theological terms to provisional with descriptions
- Reject or merge clear duplicates and noise terms

---

## Channel 2: Biography Events (biography_events table)

**Current state:** 646 events extracted from autobiographical fields in chunk summaries. All sourced from the Exegesis (source_type: 'exegesis'). All marked 'unverified'. Classification is regex-based and imperfect (395 classified as 'other').

### Priority A — Reclassify and Deduplicate
- Many events classified as 'other' are actually visions, publications, or relationships that the regex missed
- LLM pass to reclassify event_type more accurately
- Merge near-duplicate events that describe the same incident from different segments
- Extract specific dates from narrative text more aggressively

### Priority B — Ingest from Biographies and Interviews
The archive contains 24 priority documents for biographical extraction:
- **Lawrence Sutin, *Divine Invasions*** (554pp) — the standard biography
- **Anne Dick, *The Search for Philip K. Dick*** (256pp) — ex-wife's account, contradicts PKD on many points
- **Gregg Rickman, *In His Own Words*** (288pp) — extended interviews, PKD's self-reporting
- **Kyle Arnold, *The Divine Madness*** (249pp) — psychological/psychiatric perspective
- **Anthony Peake, *A Life of Philip K. Dick*** (448pp) — recent comprehensive biography
- ***The Last Interview and Other Conversations*** (114pp) — compiled interviews 1955-1982

**Improvement approach:**
- Deep-extract biographical events from each source with source_type and source_name attribution
- For events that appear in multiple sources, flag where accounts diverge
- Populate contradicted_by and contradiction_note fields for key disputed events (the break-in, the Vancouver episode, the nature of 2-3-74, substance use history)
- Set reliability: confirmed (multiple independent sources agree), likely (one credible source), disputed (sources disagree), contradicted (directly contradicted by another source)

### Priority C — Biography Page Narrative
- Generate connecting narrative text between event clusters to create a readable biographical timeline
- Add decade-level summaries that contextualize the events
- Highlight the major interpretive controversies (was the break-in real or staged? was 2-3-74 a psychotic episode or genuine mystical experience? how reliable is PKD's self-reporting?)

---

## Channel 3: Segment Summaries (segments table)

**Current state:** 207 segments have full parsed summaries (concise_summary + 12 structured fields). 900 segments have no summaries at all (manifest-only entries without corresponding chunk analysis).

### Priority A — Fill Missing Summaries
- The 900 unsummarized segments represent the majority of the Exegesis text
- Generate at minimum: concise_summary, key_claims, recurring_concepts, people_entities for each
- This requires access to the source chunk text files (in ExegesisAnalysis)

### Priority B — Improve Existing Summaries
- The 207 existing summaries vary in quality and depth
- Standardize the concise_summary format: 2-3 sentences, always stating the date context, main topic, and key claim
- Enrich recurring_concepts to use canonical term names (link to dictionary)
- Improve reading_excerpt selection — currently some are empty or poorly chosen

### Priority C — Cross-linking
- Currently all 8,125 term-segment links are confidence 4-5 (weak, from entity extraction CSV)
- Generate confidence 2-3 links by matching exact term names and aliases against segment text
- This would dramatically improve the term detail pages (which currently show no linked segments at confidence ≤3)

---

## Channel 4: Archive Descriptions (documents table)

**Current state:** 225 of 228 archive documents have card_summary and page_summary. 3 are missing summaries (the newly added Rickman articles).

### Priority A — Fill Missing Summaries
- Generate card_summary + page_summary for the 3 new Rickman Science Fiction Studies articles

### Priority B — Enrich Biography-Priority Documents
- For the 24 priority biographical documents, generate richer page_summary that:
  - Lists specific biographical claims made
  - Notes the author's relationship to PKD
  - Flags potential biases or perspectives
  - Cross-references with other sources in the archive

### Priority C — Extract Terms from Archive
- For scholarship documents with ingest_level 'full', extract term mentions and create term-segment links
- This would connect the dictionary to the secondary literature, not just the Exegesis itself

---

## Channel 5: Timeline & Analytics Text

**Current state:** Timeline shows segment cards with concise_summary. Analytics shows charts with no interpretive text.

### Improvement approach:
- Add year-level introductions to the timeline (what was happening in PKD's life, what themes dominate)
- Add interpretive captions to analytics charts (what the term frequency distribution reveals, what the segment-per-year pattern tells us about PKD's writing intensity)

---

## Implementation Order

1. **Dictionary accepted terms** — highest visibility, most scholarly value
2. **Biography reclassification** — fixes the 395 'other' events, improves the biography page immediately
3. **Cross-linking confidence upgrade** — improves term detail pages without new content
4. **Missing archive summaries** — quick wins, only 3 documents
5. **Biography deep extraction** — requires reading priority PDFs, biggest new content addition
6. **Segment summary gap-fill** — largest task, requires source text access
7. **Archive enrichment** — secondary literature connections
8. **Timeline/analytics narrative** — polish layer

---

## Technical Requirements

- Stage 3 (LLM enrichment) pipeline with caching by input_hash + prompt_version + model_name
- Batch processing with rate limiting for API calls
- Review state tracking: all LLM output starts as 'machine-drafted'
- Editorial override mechanism for human corrections (Stage 4)
- Incremental rebuild support (don't regenerate cached enrichments)
