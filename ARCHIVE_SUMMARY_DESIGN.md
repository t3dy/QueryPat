# Archive Summary Improvement: Design Document

## 1. Current State Analysis

### Coverage
- **228 documents** in the archive, all with both `card_summary` and `page_summary`
- Coverage is 100% but quality varies dramatically by category

### Quality Tiers

**Tier 1 -- Strong summaries (biographies, scholarship, primary texts: ~90 docs)**
These name specific people, describe arguments, cite structure. Example: the Andrew M. Butler PhD thesis summary names the institution (Hull), year (1995), theoretical framework (Jameson, postmodernism), and specific works analyzed.

**Tier 2 -- Adequate summaries (novels, fan publications, letters: ~90 docs)**
These give genre, period, and general relevance but lack specifics about what claims or arguments the document makes. Functional for browsing but not for research indexing.

**Tier 3 -- Weak/speculative summaries (newspaper clippings, some archive PDFs: ~48 docs)**
These use hedging language ("likely contains," "appears to be," "may represent") because they were generated from metadata alone, without access to extracted text. Newspaper clippings are the worst category -- 45 of them describe what the clipping "likely" says rather than what it actually says.

### Placeholder Issue
At least one document (`science-fiction-studies-1983-jul-vol-10-iss-2`) has a literal placeholder page_summary ("Full summary pending.") despite being marked as `ingest_level: "full"` with `extraction_status: "complete"`.

### Unexported Metadata
The database has fields that could improve archive entries but aren't in the JSON exports:
- `word_count`, `text_char_count` -- document size indicators
- `extractability_score`, `relevance_score` -- quality metrics (0-100)
- `date_confidence`, `date_basis` -- how certain dates are
- `document_texts.text_content` -- full extracted text (available for 180 docs)

---

## 2. Design Goal: Summaries as Research Infrastructure

Archive summaries should serve as a **research index** for the corpus, not just browsing labels. Each summary should answer:

1. **What kind of document is this?** (biography, scholarship article, newspaper clipping, letter, fan publication)
2. **What PKD topics does it discuss?** (specific works, periods, themes, concepts)
3. **Why is it relevant?** (primary source, secondary analysis, biographical evidence, historical context)
4. **What people, works, and concepts appear?** (structured entity references, not just prose)

### The Research Indexing Standard

A good archive summary should enable a researcher to:
- Find all documents discussing a specific PKD work or concept
- Identify which biographies cover which periods of PKD's life
- Locate scholarship on specific philosophical/theological themes
- Understand what a newspaper clipping actually says before opening the PDF

---

## 3. Proposed Structured Metadata Fields

Add the following structured fields to archive document JSON, alongside the existing prose summaries:

```json
{
  "topics": ["VALIS", "2-3-74 experience", "Gnostic theology"],
  "people_mentioned": ["Ursula Le Guin", "Theodore Sturgeon"],
  "works_discussed": ["VALIS", "The Three Stigmata of Palmer Eldritch"],
  "schools_of_thought": ["Gnosticism", "Neoplatonism", "Process theology"],
  "time_periods_covered": ["1974-1982"],
  "evidentiary_lane": "C",
  "psychology_topics": [],
  "ai_topics": [],
  "source_reliability": "secondary_scholarship"
}
```

### Field Definitions

**topics** (array of strings): Key themes or subjects discussed. Draw from existing dictionary terms where possible.

**people_mentioned** (array of strings): People discussed in the document. Cross-reference with `names` table.

**works_discussed** (array of strings): PKD works (novels, stories, essays) analyzed or referenced.

**schools_of_thought** (array of strings): Philosophical, theological, or literary schools engaged with. Controlled vocabulary:
- Gnosticism, Neoplatonism, Platonism, Hermeticism
- Process theology, Teilhardism, Zen Buddhism, Taoism
- Jungian psychology, Existentialism, Phenomenology
- Postmodernism, Science fiction studies, Marxist criticism

**time_periods_covered** (array of strings): What era of PKD's life or work the document covers. Format: "YYYY" or "YYYY-YYYY".

**evidentiary_lane** (string): Which evidence stream this document belongs to:
- **A** = Fiction (novels, stories, screenplays)
- **B** = Exegesis (PKD's own philosophical writing)
- **C** = Scholarship (academic analysis, criticism, reviews)
- **D** = Synthesis (biographies, documentaries, retrospectives)
- **E** = Primary documents (letters, legal records, newspaper articles)

**psychology_topics** (array of strings): Psychology-related themes. Controlled vocabulary:
- schizophrenia, dissociation, paranoia, amphetamine_psychosis
- Jungian_individuation, shadow_integration, anima_animus
- altered_states, religious_experience, temporal_lobe_epilepsy
- identity_fragmentation, reality_testing, false_memory
- drug_experience, withdrawal, therapeutic_relationship
- creativity_and_madness, autobiographical_fiction

**ai_topics** (array of strings): AI/technology themes. Controlled vocabulary:
- android_consciousness, Turing_test, artificial_empathy
- simulation_theory, virtual_reality, constructed_reality
- cybernetics, information_theory, entropy
- precognition_technology, pre-crime, determinism
- robot_labor, automation, technocracy
- artificial_memory, identity_verification, Voigt-Kampff

**source_reliability** (string): How to weight this source:
- `primary_pkd` -- PKD's own writing (letters, Exegesis, essays)
- `primary_other` -- Contemporary documents (newspaper articles, legal records)
- `secondary_scholarship` -- Academic analysis
- `secondary_popular` -- Popular journalism, fan writing
- `tertiary` -- Reference works, bibliographies

---

## 4. Evidentiary Lane Integration

The four-lane evidence model tracks how claims about PKD's thought flow from source to interpretation:

| Lane | Source Type | Example | Reliability |
|------|-----------|---------|-------------|
| A | Fiction | *VALIS*, *Ubik*, *Scanner Darkly* | Needs careful interpretation -- fiction ≠ belief |
| B | Exegesis | Folder entries, letters | PKD's own voice but not always consistent |
| C | Scholarship | SFS articles, Butler thesis | Analytical interpretation, check methodology |
| D | Synthesis | Sutin biography, Arnold book | Composite accounts, check sourcing |
| E | Primary documents | Newspaper clippings, legal records | Raw evidence, limited interpretation |

Each archive document maps to exactly one lane. The lane assignment enables filtering: "Show me all primary source documents from 1974" or "Show me all scholarship discussing Gnosticism."

---

## 5. Integration with Upcoming Study Sections

### AI and Robots Study
The `ai_topics` field feeds the planned AI/Robots section of the site. Archive documents tagged with AI topics become the evidence base for mini-essays on themes like android consciousness, simulation theory, and precognition technology. The pipeline:
1. Tag archive documents with `ai_topics`
2. Cross-reference with dictionary terms about AI/technology
3. Link to specific Exegesis segments where PKD discusses these themes
4. Generate study section content grounded in this evidence chain

### Psychology Study
The `psychology_topics` field feeds the planned Psychology section. Archive documents tagged with psychology topics connect PKD's biographical mental health history with his fiction and philosophical writing. The pipeline:
1. Tag archive documents with `psychology_topics`
2. Cross-reference with biography events (health, drug_use, visionary_experience)
3. Link to dictionary terms about psychological concepts
4. Generate study section content with proper evidentiary sourcing

---

## 6. Implementation Strategy

### Phase 1: Fix Weak Summaries (Tier 3 documents)
For the ~48 documents with speculative/hedging summaries:
- Check if `document_texts.text_content` exists for each
- If text exists: regenerate card_summary and page_summary from actual content
- If text doesn't exist (OCR needed): mark explicitly as `"summary_quality": "metadata_only"`
- Remove all "likely contains" hedging language

### Phase 2: Add Structured Metadata
For all 228 documents:
- Assign `evidentiary_lane` (can be done deterministically from `doc_type` and `category`)
- Assign `source_reliability` (can be done deterministically)
- For documents with extracted text: extract `topics`, `people_mentioned`, `works_discussed` using the discovery pipeline matchers
- For documents without text: populate from existing card_summary using pattern matching

### Phase 3: Add Study-Specific Tags
- Tag `psychology_topics` for biographies, scholarship on PKD's mental health, relevant fiction
- Tag `ai_topics` for scholarship on PKD's technology themes, relevant fiction
- Tag `schools_of_thought` for scholarship and Exegesis-related documents

### Phase 4: Export Pipeline Update
- Add new fields to `export_json.py` archive export
- Add structured metadata to both index.json and per-doc detail files
- Expose `word_count` and `extraction_status` in exports

---

## 7. Schema Changes Required

### Documents table additions
```sql
ALTER TABLE documents ADD COLUMN evidentiary_lane TEXT
  CHECK (evidentiary_lane IN ('A','B','C','D','E'));
ALTER TABLE documents ADD COLUMN source_reliability TEXT
  CHECK (source_reliability IN ('primary_pkd','primary_other',
    'secondary_scholarship','secondary_popular','tertiary'));
ALTER TABLE documents ADD COLUMN summary_quality TEXT DEFAULT 'machine_generated'
  CHECK (summary_quality IN ('machine_generated','metadata_only',
    'text_derived','human_reviewed'));
```

### New table: document_topics
```sql
CREATE TABLE IF NOT EXISTS document_topics (
  doc_id TEXT NOT NULL REFERENCES documents(doc_id),
  topic_type TEXT NOT NULL
    CHECK (topic_type IN ('topic','person','work','school','psychology','ai')),
  topic_value TEXT NOT NULL,
  PRIMARY KEY (doc_id, topic_type, topic_value)
);
```

---

## 8. Deterministic Lane Assignment Rules

These can be applied immediately without LLM involvement:

```
category = 'novels' or 'short_stories'  ->  lane A (Fiction)
doc_type = 'exegesis_section'           ->  lane B (Exegesis)
category = 'scholarship'               ->  lane C (Scholarship)
category = 'biographies'               ->  lane D (Synthesis)
category = 'newspaper'                 ->  lane E (Primary documents)
category = 'letters'                   ->  lane E (Primary documents)
category = 'interviews'                ->  lane E (Primary documents)
category = 'fan_publications'          ->  lane C (Scholarship, treat as secondary)
category = 'primary'                   ->  lane B or E (depends on is_pkd_authored)
```

Source reliability follows similar rules:
```
is_pkd_authored = 1                    ->  primary_pkd
category = 'newspaper'                 ->  primary_other
category = 'scholarship'              ->  secondary_scholarship
category = 'fan_publications'          ->  secondary_popular
category = 'biographies'              ->  secondary_scholarship (if academic) or secondary_popular
```

---

## Priority Order

1. **Highest:** Fix the ~48 Tier 3 summaries that use hedging language (directly hurts usability)
2. **High:** Add evidentiary_lane and source_reliability (deterministic, no LLM needed)
3. **Medium:** Extract structured topics from documents with text (can use discovery pipeline matchers)
4. **Lower:** Add psychology_topics and ai_topics (needs the study sections to be designed first)
5. **Lowest:** Human review of machine-generated summaries
