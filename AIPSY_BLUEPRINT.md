# AI & Psychology Studies: Implementation Blueprint

## 1. Repo Reuse Analysis

### What Already Exists and Should Be Reused

| Component | Location | Reuse Strategy |
|-----------|----------|----------------|
| **SQLite knowledge DB** | `database/unified.sqlite` | Extend with study tables; do not fork |
| **Segments table** (882 Exegesis chunks with raw text) | `segments` | Primary substrate for Exegesis-lane extraction |
| **Document texts** (180 archive PDFs with extracted text) | `document_texts` | Primary substrate for scholarship/biography-lane extraction |
| **Terms + aliases** (936 entries) | `terms`, `term_aliases` | Cross-reference study topics against existing dictionary |
| **Names + aliases** (491 entities) | `names`, `name_aliases` | Link thinkers/characters to study topics |
| **Evidence packets** | `evidence_packets`, `evidence_excerpts` | Model for study evidence; extend with `study_id` |
| **Term-segment links** | `term_segments` | Reuse link_confidence model (1=exact, 2=alias, 4=conceptual) |
| **Biography events** (646 events) | `biography_events` | Chronology layer for psychology study |
| **Export pipeline** | `scripts/export_json.py` | Add `export_studies()` function following existing two-tier pattern |
| **Search index** | `export_search_index()` | Extend to include study topic entries |
| **Discovery pipeline** | `scripts/discover/` | Reuse `matchers.py` patterns and `scan_substrate()` architecture |
| **Archive metadata** | `documents` table | Already has `doc_type`, `category`; extend with `evidentiary_lane` |
| **Reference data CSVs** | `database/reference_data/` | Extend with psychology and AI reference vocabularies |
| **React site** | `site/src/` | Add new routes and page components following existing patterns |
| **useData hook** | `site/src/hooks/useData.ts` | All new pages use same data-fetching pattern |
| **CSS system** | `site/src/index.css` | Reuse existing `.card`, `.badge`, `.sidebar-layout` classes |

### What Should Be Extended

| Component | Extension |
|-----------|-----------|
| `build_all.py` | Add Stage 5 (study pipeline) after Stage 3 |
| `export_json.py` | Add `export_studies()` with two-tier output |
| `unified_schema.sql` | Add study tables (see Section 3) |
| `App.tsx` | Add `/studies`, `/studies/ai/:slug`, `/studies/psychology/:slug` routes |
| `search_index.json` | Include study topic entries as searchable items |
| `analytics.json` | Add study coverage metrics |

### What Must Be Created New

| Component | Purpose |
|-----------|---------|
| `scripts/study/` | New package for study pipeline scripts |
| `scripts/study/ontology.py` | Topic definitions and controlled vocabulary |
| `scripts/study/passage_classifier.py` | Deterministic passage matching + LLM classification |
| `scripts/study/evidence_builder.py` | Evidence packet assembly per topic |
| `scripts/study/entry_drafter.py` | LLM-assisted topic dossier generation |
| `scripts/study/study_export.py` | Study-specific JSON export (called from export_json.py) |
| `database/reference_data/ai_topics.csv` | AI topic ontology |
| `database/reference_data/psychology_topics.csv` | Psychology topic ontology |
| `site/src/pages/Studies.tsx` | Study index page |
| `site/src/pages/StudyTopic.tsx` | Individual topic dossier page |

---

## 2. Research Architecture

### Four-Lane Evidence Model

The studies adopt the four-lane model from ARCHIVE_SUMMARY_DESIGN.md, adapted from five lanes to four per the AIPSY.txt specification:

| Lane | Label | Sources | Epistemic Status |
|------|-------|---------|------------------|
| **A** | Primary fiction | Novels, stories, essays, screenplays | Requires careful interpretation: fiction ≠ belief |
| **B** | Exegesis & self-theorizing | Exegesis notebooks, letters, interviews | PKD's own voice but internally inconsistent |
| **C** | Biographical & critical scholarship | Biographies, SFS articles, dissertations | Analytical interpretation; check methodology |
| **D** | Synthesis | Dictionary entries, topic dossiers (our output) | Must cite A, B, or C explicitly |

**Mapping to existing data:**

| Lane | Database Source | Query |
|------|---------------|-------|
| A | `segments` where `raw_text` discusses fiction | Exegesis segments referencing novels/stories |
| A | `document_texts` where `documents.category = 'novels'` | Extracted novel text (limited availability) |
| B | `segments` (all Exegesis entries) | Primary Lane B substrate |
| B | `document_texts` where `documents.category IN ('letters', 'interviews')` | PKD correspondence |
| C | `document_texts` where `documents.category IN ('scholarship', 'biographies')` | Secondary literature |
| D | Generated output | Study topic dossiers |

### Evidence Preservation Rules

1. **Never collapse lanes in storage.** Every passage, excerpt, and claim carries its `evidence_lane` tag.
2. **Contradictions are data, not errors.** When PKD says X in a 1975 Exegesis entry and not-X in 1978, both are stored. When a biographer interprets differently from PKD's self-report, both are stored.
3. **Synthesis (Lane D) must cite.** Every claim in a topic dossier must reference at least one Lane A, B, or C passage.
4. **Fiction is not testimony.** Lane A passages are labeled as "represented in fiction" — never used as evidence of PKD's beliefs without corroborating Lane B or C evidence.

### Research Flow

```
Corpus substrates (A, B, C)
    ↓
Deterministic passage matching (regex, lexicon)
    ↓
Passage classification (source_mode, topic_tags, claim_type, confidence)
    ↓
Evidence packet assembly (grouped by topic × lane)
    ↓
Contradiction detection (cross-lane, cross-temporal)
    ↓
Topic dossier drafting (Lane D synthesis)
    ↓
JSON export → site viewer
```

---

## 3. Data Model and Schema Extensions

### New Tables

```sql
-- Study definitions
CREATE TABLE IF NOT EXISTS studies (
    study_id TEXT PRIMARY KEY,           -- 'ai' or 'psychology'
    title TEXT NOT NULL,
    description TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

-- Topic ontology
CREATE TABLE IF NOT EXISTS study_topics (
    topic_id TEXT PRIMARY KEY,            -- e.g. 'ai:android-consciousness'
    study_id TEXT NOT NULL REFERENCES studies(study_id),
    topic_name TEXT NOT NULL,             -- 'Android Consciousness'
    topic_slug TEXT NOT NULL,             -- 'android-consciousness'
    parent_topic_id TEXT REFERENCES study_topics(topic_id),
    definition TEXT,                      -- One-paragraph technical definition
    pkd_relevance TEXT,                   -- Why this matters for PKD studies
    status TEXT DEFAULT 'seed'
        CHECK (status IN ('seed', 'draft', 'reviewed', 'published')),
    sort_order INTEGER DEFAULT 0
);

-- Classified passages
CREATE TABLE IF NOT EXISTS study_passages (
    passage_id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id TEXT NOT NULL REFERENCES study_topics(topic_id),
    source_type TEXT NOT NULL             -- 'segment' or 'document'
        CHECK (source_type IN ('segment', 'document')),
    source_id TEXT NOT NULL,              -- seg_id or doc_id
    evidence_lane TEXT NOT NULL           -- 'A', 'B', 'C'
        CHECK (evidence_lane IN ('A', 'B', 'C')),
    source_mode TEXT                      -- fiction, exegesis, letter, interview, criticism
        CHECK (source_mode IN ('fiction', 'exegesis', 'letter',
               'interview', 'criticism', 'biography')),
    excerpt TEXT NOT NULL,                -- The matched passage (fair-use length)
    char_offset_start INTEGER,
    char_offset_end INTEGER,
    -- Classification fields
    claim_type TEXT
        CHECK (claim_type IN ('definition', 'symptom_description', 'causal_theory',
               'allegory', 'self_report', 'critique', 'comparison', 'unresolved')),
    confidence TEXT DEFAULT 'medium'
        CHECK (confidence IN ('high', 'medium', 'low')),
    match_method TEXT DEFAULT 'lexicon'   -- 'lexicon', 'regex', 'llm', 'manual'
        CHECK (match_method IN ('lexicon', 'regex', 'llm', 'manual')),
    UNIQUE(topic_id, source_type, source_id, char_offset_start)
);

-- Psychology-specific classification
CREATE TABLE IF NOT EXISTS study_passage_psych (
    passage_id INTEGER PRIMARY KEY REFERENCES study_passages(passage_id),
    psych_mode TEXT
        CHECK (psych_mode IN ('clinical', 'psychoanalytic', 'Jungian',
               'existential', 'neuropsychological', 'anti_psychiatric',
               'mystical', 'popular_psychology'))
);

-- Topic evidence packets (aggregated per topic × lane)
CREATE TABLE IF NOT EXISTS study_evidence (
    evidence_id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id TEXT NOT NULL REFERENCES study_topics(topic_id),
    evidence_lane TEXT NOT NULL
        CHECK (evidence_lane IN ('A', 'B', 'C')),
    summary TEXT,                         -- Synthesized summary of this lane's evidence
    passage_count INTEGER DEFAULT 0,
    key_works TEXT,                        -- JSON array of work titles
    key_thinkers TEXT,                     -- JSON array of thinker names
    chronology_start TEXT,
    chronology_end TEXT,
    UNIQUE(topic_id, evidence_lane)
);

-- Contradictions (cross-lane or cross-temporal)
CREATE TABLE IF NOT EXISTS study_contradictions (
    contradiction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id TEXT NOT NULL REFERENCES study_topics(topic_id),
    passage_a_id INTEGER REFERENCES study_passages(passage_id),
    passage_b_id INTEGER REFERENCES study_passages(passage_id),
    description TEXT NOT NULL,
    contradiction_type TEXT DEFAULT 'cross_lane'
        CHECK (contradiction_type IN ('cross_lane', 'cross_temporal',
               'fiction_vs_exegesis', 'scholarly_disagreement'))
);

-- Topic dossier content (Lane D output)
CREATE TABLE IF NOT EXISTS study_dossiers (
    topic_id TEXT PRIMARY KEY REFERENCES study_topics(topic_id),
    -- Structured sections matching the output model
    definition_section TEXT,
    pkd_relevance_section TEXT,
    in_fiction_section TEXT,
    in_exegesis_section TEXT,
    intellectual_background_section TEXT,
    scholarly_debate_section TEXT,
    chronology_section TEXT,
    key_passages_section TEXT,             -- JSON array of passage references
    contradictions_section TEXT,
    related_works_section TEXT,            -- JSON array
    related_thinkers_section TEXT,         -- JSON array
    related_entries_section TEXT,          -- JSON array of term_ids / topic_ids
    editorial_notes TEXT,
    open_questions TEXT,
    draft_status TEXT DEFAULT 'pending'
        CHECK (draft_status IN ('pending', 'drafted', 'reviewed', 'published')),
    last_updated TEXT DEFAULT (datetime('now'))
);

-- Cross-references: topics ↔ existing entities
CREATE TABLE IF NOT EXISTS study_topic_terms (
    topic_id TEXT NOT NULL REFERENCES study_topics(topic_id),
    term_id TEXT NOT NULL REFERENCES terms(term_id),
    relation_type TEXT DEFAULT 'related'
        CHECK (relation_type IN ('primary', 'related', 'contrast')),
    PRIMARY KEY (topic_id, term_id)
);

CREATE TABLE IF NOT EXISTS study_topic_names (
    topic_id TEXT NOT NULL REFERENCES study_topics(topic_id),
    name_id TEXT NOT NULL REFERENCES names(name_id),
    relation_type TEXT DEFAULT 'related'
        CHECK (relation_type IN ('thinker', 'character', 'historical')),
    PRIMARY KEY (topic_id, name_id)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_study_passages_topic ON study_passages(topic_id);
CREATE INDEX IF NOT EXISTS idx_study_passages_source ON study_passages(source_type, source_id);
CREATE INDEX IF NOT EXISTS idx_study_passages_lane ON study_passages(evidence_lane);
CREATE INDEX IF NOT EXISTS idx_study_evidence_topic ON study_evidence(topic_id);
```

### Extension to Existing Tables

```sql
-- Add evidentiary_lane to documents (from ARCHIVE_SUMMARY_DESIGN.md)
ALTER TABLE documents ADD COLUMN evidentiary_lane TEXT
    CHECK (evidentiary_lane IN ('A', 'B', 'C', 'D', 'E'));

ALTER TABLE documents ADD COLUMN source_reliability TEXT
    CHECK (source_reliability IN ('primary_pkd', 'primary_other',
           'secondary_scholarship', 'secondary_popular', 'tertiary'));
```

---

## 4. Pipeline Design

### Stage 5: Study Pipeline (added to `build_all.py`)

```
Stage 5a: Topic ontology loading         [deterministic]
Stage 5b: Passage extraction             [deterministic + LLM]
Stage 5c: Passage classification          [LLM-assisted]
Stage 5d: Evidence packet assembly        [deterministic]
Stage 5e: Contradiction detection         [deterministic + LLM]
Stage 5f: Dossier drafting               [LLM]
Stage 5g: Cross-linking                  [deterministic]
```

### Stage 5a: Topic Ontology Loading

**Script:** `scripts/study/ontology.py`

**Deterministic.** Loads topic definitions from CSV reference files and populates `study_topics` table.

**Inputs:**
- `database/reference_data/ai_topics.csv`
- `database/reference_data/psychology_topics.csv`

**CSV format:**
```csv
topic_id,study_id,topic_name,parent_topic_id,definition,pkd_relevance,sort_order
ai:android-consciousness,ai,Android Consciousness,,Whether androids can possess genuine consciousness or only simulate it,Central question of Do Androids Dream and the Voigt-Kampff test,1
```

**AI Topics Ontology (22 topics):**

| Topic ID | Topic Name | Key PKD Works |
|----------|-----------|---------------|
| `ai:android-consciousness` | Android Consciousness | *Do Androids Dream*, *We Can Build You* |
| `ai:empathy-testing` | Empathy Testing | *Do Androids Dream* (Voigt-Kampff) |
| `ai:counterfeit-humanity` | Counterfeit Humanity | *Do Androids Dream*, *Impostor*, *Second Variety* |
| `ai:simulation` | Simulation & Constructed Reality | *Time Out of Joint*, *Eye in the Sky* |
| `ai:machine-intelligence` | Machine Intelligence | *Vulcan's Hammer*, *A Maze of Death* |
| `ai:cybernetics` | Cybernetics & Control Systems | *The Penultimate Truth*, *The Simulacra* |
| `ai:surveillance` | Surveillance & Bureaucratic Control | *A Scanner Darkly*, *Flow My Tears* |
| `ai:automation` | Labor Automation | *Autofac*, *The Variable Man* |
| `ai:implanted-memory` | Implanted Memory | *We Can Remember It for You Wholesale*, *Blade Runner* |
| `ai:fabricated-identity` | Fabricated Identity | *A Scanner Darkly*, *Impostor* |
| `ai:posthuman` | Posthuman Cognition | *The Three Stigmata*, Exegesis |
| `ai:reality-testing` | Reality Testing | *Ubik*, *Time Out of Joint*, *Eye in the Sky* |
| `ai:false-reality` | False Reality | *Time Out of Joint*, *The Penultimate Truth* |
| `ai:android-affect` | Android Affect & Emotion | *Do Androids Dream*, *We Can Build You* |
| `ai:precognition-tech` | Precognition Technology | *Minority Report*, *The World Jones Made* |
| `ai:programming` | Programming & Determinism | *A Maze of Death*, Exegesis |
| `ai:tech-domination` | Technological Domination | *The Penultimate Truth*, *Vulcan's Hammer* |
| `ai:robot-labor` | Robots & Mechanical Labor | *Second Variety*, *Autofac* |
| `ai:simulation-of-mind` | Simulation of Mind | Exegesis, *VALIS* |
| `ai:control-systems` | Control Systems | *The Simulacra*, *Solar Lottery* |
| `ai:turing-test` | Turing Test Analogues | *Do Androids Dream*, *Impostor* |
| `ai:information-theory` | Information Theory & Entropy | Exegesis, *Ubik* |

**Psychology Topics Ontology (22 topics):**

| Topic ID | Topic Name | Key PKD Context |
|----------|-----------|-----------------|
| `psych:paranoia` | Paranoia | *A Scanner Darkly*, *Clans of the Alphane Moon* |
| `psych:schizophrenia` | Schizophrenia | *Clans of the Alphane Moon*, *Martian Time-Slip* |
| `psych:psychosis` | Psychosis | *The Three Stigmata*, *VALIS* |
| `psych:empathy` | Empathy | *Do Androids Dream*, Exegesis |
| `psych:identity-diffusion` | Identity Diffusion | *A Scanner Darkly*, *Flow My Tears* |
| `psych:double` | Double / Doppelgänger | *A Scanner Darkly*, *Dr. Bloodmoney* |
| `psych:trauma` | Trauma | Biography, *VALIS* |
| `psych:twin-motif` | Twin Motif | Jane Dick's death, *Dr. Bloodmoney*, Exegesis |
| `psych:addiction` | Addiction | *A Scanner Darkly*, biography |
| `psych:amphetamine` | Amphetamine Use | Biography, *A Scanner Darkly* |
| `psych:dream-interpretation` | Dream Interpretation | Exegesis, letters |
| `psych:jung` | Jung & Analytical Psychology | Exegesis (extensive engagement) |
| `psych:synchronicity` | Synchronicity | Exegesis, *The Man in the High Castle* |
| `psych:archetype` | Archetype | Exegesis, *VALIS* |
| `psych:split-brain` | Split-Brain | Exegesis, *A Scanner Darkly* |
| `psych:memory` | Memory | *We Can Remember It*, *Ubik*, *A Scanner Darkly* |
| `psych:false-memory` | False Memory | *We Can Remember It*, *Total Recall* |
| `psych:gaslighting` | Gaslighting / Brainwashing | *Time Out of Joint*, *The Penultimate Truth* |
| `psych:therapy` | Therapy & Psychiatry | *Clans of the Alphane Moon*, biography |
| `psych:anamnesis` | Anamnesis | Exegesis (core concept) |
| `psych:hypnagogic` | Hypnagogic State | Exegesis, 2-3-74 experience |
| `psych:hypnopompic` | Hypnopompic State | Exegesis, 2-3-74 experience |
| `psych:asclepius-dreams` | Dream Rituals of Asclepius | Exegesis references to temple incubation |

### Stage 5b: Passage Extraction

**Script:** `scripts/study/passage_classifier.py`

**Architecture:** Reuses the discovery pipeline's batch-by-substrate model.

**Deterministic layer:**
1. Materialize Substrate A (segments.raw_text) — reuse `materialize_segments()` from discovery pipeline
2. Materialize Substrate B (document_texts.text_content) — reuse `materialize_documents()`
3. For each topic, compile a lexicon of search terms (synonyms, variants, related phrases)
4. Scan both substrates using precompiled regex patterns
5. Extract passage windows (300 chars before and after match, capped at paragraph boundaries)
6. Assign `evidence_lane` based on source metadata:
   - Segments → Lane B (Exegesis)
   - Documents with `category = 'novels'` or `'short_stories'` → Lane A
   - Documents with `category = 'scholarship'` or `'biographies'` → Lane C
   - Documents with `is_pkd_authored = 1` and `category = 'letters'` → Lane B

**LLM layer (optional, run with `--classify` flag):**
7. For each extracted passage, classify:
   - `claim_type`: definition / symptom_description / causal_theory / allegory / self_report / critique / comparison / unresolved
   - `confidence`: high / medium / low
   - `psych_mode` (psychology topics only): clinical / psychoanalytic / Jungian / existential / neuropsychological / anti_psychiatric / mystical
8. LLM prompt template:

```
You are classifying a passage from a Philip K. Dick-related text for a research database.

Topic: {topic_name}
Source: {source_title} ({source_mode})
Evidence lane: {lane} ({lane_description})

Passage:
---
{excerpt}
---

Classify this passage:
1. claim_type: [definition|symptom_description|causal_theory|allegory|self_report|critique|comparison|unresolved]
2. confidence: [high|medium|low] — how clearly does this passage relate to {topic_name}?
3. psych_mode (if psychology topic): [clinical|psychoanalytic|Jungian|existential|neuropsychological|anti_psychiatric|mystical|popular_psychology]

Respond as JSON only.
```

**Lexicon examples:**

For `psych:paranoia`:
```python
PARANOIA_LEXICON = [
    r'\bparanoi[ad]\b', r'\bparanoid\b', r'\bsuspicio[nu]s?\b',
    r'\bconspiracy\b', r'\bsurveill\w+\b', r'\bwatching\b',
    r'\bbeing followed\b', r'\bthey.{0,20}(watching|following|listening)\b',
    r'\btap(ped|ping)?\b.*\bphone\b',
]
```

For `ai:android-consciousness`:
```python
ANDROID_CONSCIOUSNESS_LEXICON = [
    r'\bandroid\w*\b', r'\breplicant\b', r'\bsimulacr\w+\b',
    r'\bartificial.{0,10}(person|being|life|intelligence)\b',
    r'\bmachine.{0,10}(consciousness|awareness|sentien\w+)\b',
    r'\bVoigt.?Kampff\b', r'\bempathy.{0,10}test\b',
    r'\bcan.{0,20}(feel|think|dream|love)\b',
]
```

### Stage 5c: Evidence Packet Assembly

**Script:** `scripts/study/evidence_builder.py`

**Deterministic.** Groups classified passages into evidence packets per topic per lane.

For each `(topic_id, evidence_lane)` combination:
1. Collect all passages
2. Sort chronologically (by segment date or document date)
3. Select representative passages (max 10 per lane, prefer high-confidence)
4. Extract key works mentioned (cross-reference with `documents` and fiction catalog)
5. Extract key thinkers mentioned (cross-reference with `names` table)
6. Compute chronology range
7. Write to `study_evidence` table

### Stage 5d: Contradiction Detection

**Script:** `scripts/study/contradiction_detector.py`

**Deterministic + LLM.**

Deterministic triggers (flag for review):
- Same topic, same concept, different lanes, opposite sentiment words
- Same topic, Lane B passages from different years making incompatible claims
- Lane C passages from different scholars reaching different conclusions

LLM review (optional):
- For flagged passage pairs, ask Claude to confirm whether a genuine contradiction exists and describe it

### Stage 5e: Dossier Drafting

**Script:** `scripts/study/entry_drafter.py`

**LLM-required.** For each topic with sufficient evidence (≥3 passages across ≥2 lanes):

1. Assemble context package:
   - Topic definition and PKD relevance (from ontology)
   - All evidence packets (organized by lane)
   - All contradictions
   - Related dictionary terms (from `study_topic_terms`)
   - Related names (from `study_topic_names`)
   - Chronology of relevant biography events

2. Generate dossier sections using structured prompt:

```
You are drafting a scholarly topic dossier for a PKD research portal.

Topic: {topic_name}
Study: {study_title}

## Evidence by Lane

### Lane A (Fiction):
{fiction_passages}

### Lane B (Exegesis):
{exegesis_passages}

### Lane C (Scholarship):
{scholarship_passages}

### Contradictions:
{contradictions}

### Chronology:
{chronology}

Write the following sections. Use college reading level. Be analytical and evidence-based.
Do NOT diagnose PKD. Do NOT reproduce long passages (fair use: ≤50 words per quote).
Explicitly distinguish what PKD wrote in fiction vs. what he theorized in the Exegesis vs.
what scholars have argued.

Sections to write:
1. Definition (1 paragraph)
2. PKD Relevance (1 paragraph)
3. In the Fiction (2-3 paragraphs, cite specific works)
4. In the Exegesis (2-3 paragraphs, cite specific entries where possible)
5. Intellectual Background (1-2 paragraphs: who influenced PKD on this topic?)
6. Scholarly Debate (1-2 paragraphs: what do critics say?)
7. Chronology (bullet list of key dated events)
8. Key Passages (list of 3-5 passage references with brief context)
9. Contradictions (if any, describe without resolving)
10. Related Works (JSON array of PKD work titles)
11. Related Thinkers (JSON array of thinker names)
12. Related Entries (JSON array of term_ids or topic_ids)
13. Editorial Notes (any caveats about evidence quality)
14. Open Questions (2-3 unanswered research questions)

Respond as JSON with section keys matching above.
```

3. Store output in `study_dossiers` table
4. Mark `draft_status = 'drafted'`

### Stage 5f: Cross-linking

**Script:** `scripts/study/cross_linker.py`

**Deterministic.**

1. Link topics to dictionary terms:
   - Match topic names against `terms.term_name` and `term_aliases.alias`
   - E.g., `psych:anamnesis` → term `anamnesis`
   - Write to `study_topic_terms`

2. Link topics to names:
   - Match thinker references in dossiers against `names.display_name` and `name_aliases`
   - E.g., `psych:jung` → name `Carl Jung`
   - Write to `study_topic_names`

3. Link topics to archive documents:
   - Match topic keywords against `documents.card_summary`
   - Surface relevant scholarship for each topic

---

## 5. Claude Skills Design

### Skill 1: Corpus Auditor

**Purpose:** Assess corpus coverage for a specific study topic before extraction begins.

**Inputs:** `topic_id`, database connection

**Outputs:** Coverage report (how many segments/documents mention this topic, by lane)

**Guardrails:** Read-only; never modifies database

**Deterministic steps:**
- Before: query `segments` and `document_texts` with topic lexicon
- After: format report as structured JSON

### Skill 2: Topic Candidate Extractor

**Purpose:** Discover sub-topics or related concepts not yet in the ontology.

**Inputs:** Study ID, corpus text for one substrate

**Outputs:** List of candidate topics with frequency and source spread

**Guardrails:** Output is review-only JSON; never writes to `study_topics`

**Deterministic steps:**
- Before: materialize corpus text, load existing topics
- After: deduplicate against existing ontology, score by frequency

### Skill 3: AI-Topic Tagger

**Purpose:** Tag a passage with AI topic classifications.

**Inputs:** Passage text, source metadata, topic lexicon

**Outputs:** `{ topic_ids: [...], confidence: "high"|"medium"|"low", claim_type: "..." }`

**Guardrails:** Must return structured JSON; must not invent topic IDs not in ontology

**Deterministic steps:**
- Before: lexicon matching to propose candidate topics
- After: validate topic_ids against `study_topics` table

### Skill 4: Psychology-Topic Tagger

**Purpose:** Tag a passage with psychology topic classifications including `psych_mode`.

**Inputs:** Passage text, source metadata, topic lexicon

**Outputs:** `{ topic_ids: [...], psych_mode: "...", confidence: "...", claim_type: "..." }`

**Guardrails:** Must not diagnose PKD; must distinguish fictional representation from self-report

**Deterministic steps:**
- Before: lexicon matching
- After: validate against controlled vocabulary for `psych_mode`

### Skill 5: Passage Classifier

**Purpose:** Full classification of a matched passage (combines tagger + claim_type + confidence).

**Inputs:** Passage text, topic_id, source metadata

**Outputs:** Complete `study_passages` row as JSON

**Guardrails:** Confidence must be explicitly justified; passages with ambiguous relevance default to "low"

**Deterministic steps:**
- Before: verify passage is within fair-use length (≤300 words)
- After: validate all enum fields against schema CHECK constraints

### Skill 6: Evidence Packet Builder

**Purpose:** Assemble evidence for one topic across all lanes.

**Inputs:** `topic_id`, all classified passages for that topic

**Outputs:** `study_evidence` rows (one per lane) with summary, key works, key thinkers

**Guardrails:** Must include passages from ≥2 lanes to produce a packet; single-lane topics get flagged

**Deterministic steps:**
- Before: group passages by lane, sort chronologically
- After: validate passage counts, compute chronology range

### Skill 7: Contradiction Mapper

**Purpose:** Identify and describe contradictions within a topic's evidence.

**Inputs:** Evidence packets for one topic (all lanes)

**Outputs:** List of `study_contradictions` with descriptions

**Guardrails:** Must preserve contradictions, never resolve them; must cite both passages

**Deterministic steps:**
- Before: identify passage pairs from different lanes or different dates
- After: validate that both passage_ids exist in database

### Skill 8: Topic-Entry Drafter

**Purpose:** Draft a complete topic dossier from evidence packets.

**Inputs:** Topic definition, evidence packets, contradictions, related entities

**Outputs:** Complete `study_dossiers` row as JSON

**Guardrails:**
- College reading level
- No jargon density
- No PKD diagnosis
- Fair use: ≤50 words per quoted passage
- Explicitly separate Lane A/B/C evidence in prose

**Deterministic steps:**
- Before: assemble full context package
- After: validate all section fields are present, check quote lengths

### Skill 9: Chronology Synthesizer

**Purpose:** Build a chronological narrative for one topic across PKD's life.

**Inputs:** Topic passages sorted by date, biography events, publication dates

**Outputs:** Chronology section for dossier (bullet list with dates)

**Guardrails:** Only include dated events; flag undated passages separately

**Deterministic steps:**
- Before: merge passage dates with biography_events dates
- After: sort chronologically, remove duplicates

### Skill 10: Fair-Use Reviewer

**Purpose:** Review a drafted dossier for copyright compliance.

**Inputs:** Complete dossier text, list of quoted passages with sources

**Outputs:** Pass/fail with specific violations noted

**Guardrails:** Flag any quote >50 words; flag any section that paraphrases a single source too closely

**Deterministic steps:**
- Before: extract all quoted text, measure word counts
- After: if violations found, truncate quotes and flag for revision

### Skill 11: Viewer Integration Planner

**Purpose:** Generate the JSON export spec for a study's viewer data.

**Inputs:** Study schema, existing export patterns

**Outputs:** Export function specification with file paths and data shapes

**Guardrails:** Must follow existing two-tier export pattern (index.json + detail files)

---

## 6. Agent Swarm Architecture

### Task Dependency Graph

```
[Ontology Load]
      ↓
[Corpus Audit] ←── parallelizable per topic
      ↓
[Passage Extraction] ←── parallelizable per substrate × topic batch
      ↓
[Passage Classification] ←── parallelizable per passage batch
      ↓
[Evidence Assembly] ←── parallelizable per topic (but sequential after classification)
      ↓
[Contradiction Detection] ←── parallelizable per topic
      ↓
[Dossier Drafting] ←── parallelizable per topic (but sequential after evidence + contradictions)
      ↓
[Cross-linking] ←── sequential (needs all dossiers)
      ↓
[Fair-Use Review] ←── parallelizable per dossier
      ↓
[JSON Export]
```

### Agent Roles

| Agent | Parallelizable | Token Budget | Batch Size |
|-------|---------------|-------------|------------|
| **Corpus Scanner** | Yes (per substrate) | Low (deterministic) | All segments or all documents |
| **Topic Candidate Detector** | Yes (per topic) | ~2K tokens/topic | 5 topics per batch |
| **Passage Classifier** | Yes (per passage batch) | ~500 tokens/passage | 20 passages per batch |
| **Evidence Packet Builder** | Yes (per topic) | ~3K tokens/topic | 5 topics per batch |
| **Entry Synthesizer** | Sequential per topic | ~8K tokens/topic | 1 topic at a time |
| **Reviewer** | Yes (per dossier) | ~2K tokens/dossier | 3 dossiers per batch |

### Batch Processing Strategy

**Phase 1 — Deterministic (no LLM, runs in seconds):**
1. Load ontology (44 topics)
2. Compile lexicons (44 lexicon sets)
3. Materialize corpus (882 segments + 180 documents)
4. Scan all substrates for all topics simultaneously
5. Extract passage windows
6. Assign evidence lanes

**Phase 2 — LLM Classification (batched):**
1. Group passages by topic (expect 50-200 passages per topic for well-represented topics)
2. Batch 20 passages per LLM call
3. Estimated total: ~2,000-4,000 passages → 100-200 LLM calls
4. Checkpoint after each batch (write classified passages to DB immediately)

**Phase 3 — LLM Synthesis (sequential per topic):**
1. Process topics in priority order (seed topics first)
2. One dossier draft per LLM call (~8K tokens each)
3. 44 topics → 44 LLM calls
4. Checkpoint after each dossier

### Checkpointing

All intermediate results are written to SQLite immediately:
- After passage extraction: `study_passages` rows with `match_method = 'lexicon'`
- After classification: update `claim_type`, `confidence`, `psych_mode`
- After evidence assembly: `study_evidence` rows
- After contradiction detection: `study_contradictions` rows
- After dossier drafting: `study_dossiers` rows

Pipeline can be restarted from any checkpoint. The `--resume` flag skips steps where output already exists.

### Token Efficiency

- Deterministic steps (5a, 5c assembly, 5f) use zero LLM tokens
- Classification (5b LLM layer): ~500 tokens per passage × ~3,000 passages = ~1.5M tokens
- Dossier drafting (5e): ~8K tokens per topic × 44 topics = ~352K tokens
- Contradiction detection (5d LLM): ~1K tokens per pair × ~100 pairs = ~100K tokens
- **Total estimated: ~2M tokens** (~$6 at Claude Sonnet pricing)

---

## 7. Website Viewer Architecture

### Route Structure: Option A (Recommended)

**Option A: Top-level Studies section** is the right choice for QueryPat because:

1. The two studies share the same evidence model, viewer components, and cross-linking patterns
2. A unified Studies section allows comparison across AI and psychology themes
3. It keeps the nav clean (one "Studies" entry rather than two)
4. Future studies (e.g., "Religion & Metaphysics") slot in naturally

```
/studies                       → Studies index (both studies)
/studies/ai                    → AI Study overview + topic list
/studies/ai/:slug              → AI topic dossier page
/studies/psychology            → Psychology Study overview + topic list
/studies/psychology/:slug      → Psychology topic dossier page
```

### New Components

**1. `site/src/pages/Studies.tsx`** — Study Index

```
┌──────────────────────────────────────────┐
│ Research Studies                          │
│ Thematic analyses across PKD's corpus    │
├──────────────────────────────────────────┤
│                                          │
│ ┌─────────────────┐ ┌─────────────────┐  │
│ │ AI & Robots     │ │ Psychology      │  │
│ │ 22 topics       │ │ 22 topics       │  │
│ │ 1,247 passages  │ │ 892 passages    │  │
│ │ Explore →       │ │ Explore →       │  │
│ └─────────────────┘ └─────────────────┘  │
│                                          │
└──────────────────────────────────────────┘
```

**2. `site/src/pages/StudyOverview.tsx`** — Per-Study Landing

```
┌──────────────────────────────────────────┐
│ AI & Robots Study                        │
│ How PKD imagined artificial minds        │
├────────────┬─────────────────────────────┤
│ Topics     │                             │
│            │ Topic cards grid:           │
│ • Android  │ ┌─────────┐ ┌─────────┐    │
│   Consc.   │ │ Android │ │ Empathy │    │
│ • Empathy  │ │ Consc.  │ │ Testing │    │
│   Testing  │ │ 45 pass │ │ 23 pass │    │
│ • Counter- │ │ 3 works │ │ 2 works │    │
│   feit ... │ └─────────┘ └─────────┘    │
│ • Simul... │                             │
│            │ Lane filter: [A][B][C][All] │
│ Filter by: │                             │
│ [All lanes]│                             │
│ [Fiction]  │                             │
│ [Exegesis] │                             │
│ [Scholars] │                             │
└────────────┴─────────────────────────────┘
```

**3. `site/src/pages/StudyTopic.tsx`** — Topic Dossier Page

```
┌──────────────────────────────────────────┐
│ ← AI & Robots Study                     │
│ Android Consciousness                    │
│ badge: 45 passages · 3 lanes · 8 works  │
├──────────────────────────────────────────┤
│                                          │
│ ## Definition                            │
│ [paragraph]                              │
│                                          │
│ ## PKD Relevance                         │
│ [paragraph]                              │
│                                          │
│ ## In the Fiction  [Lane A]              │
│ [2-3 paragraphs with work references]    │
│                                          │
│ ## In the Exegesis [Lane B]              │
│ [2-3 paragraphs with segment links]      │
│                                          │
│ ## Intellectual Background               │
│ [paragraph with thinker links]           │
│                                          │
│ ## Scholarly Debate [Lane C]             │
│ [paragraph with archive doc links]       │
│                                          │
│ ## Chronology                            │
│ • 1966: Do Androids Dream drafted        │
│ • 1968: Published by Doubleday           │
│ • 1974: Exegesis entry on machine...     │
│                                          │
│ ## Key Passages                          │
│ [passage cards with source attribution]  │
│                                          │
│ ## Contradictions                        │
│ [if any, described with both sides]      │
│                                          │
│ ┌─ Related ─────────────────────────┐    │
│ │ Works: Do Androids Dream, ...     │    │
│ │ Thinkers: Turing, Descartes, ...  │    │
│ │ Dictionary: empathy, android, ... │    │
│ │ Other topics: Empathy Testing, ..│    │
│ │ Archive: [linked documents]       │    │
│ └───────────────────────────────────┘    │
│                                          │
│ ## Editorial Notes                       │
│ [caveats]                                │
│                                          │
│ ## Open Questions                        │
│ [research questions]                     │
│                                          │
└──────────────────────────────────────────┘
```

### Data Flow: JSON Exports

```
site/public/data/studies/
├── index.json                    ← study list with stats
├── ai/
│   ├── index.json                ← AI topic list with passage counts
│   └── topics/
│       ├── android-consciousness.json  ← full dossier + evidence
│       ├── empathy-testing.json
│       └── ...
└── psychology/
    ├── index.json                ← Psychology topic list
    └── topics/
        ├── paranoia.json
        ├── schizophrenia.json
        └── ...
```

**Topic detail JSON shape:**
```json
{
  "topic_id": "ai:android-consciousness",
  "study_id": "ai",
  "topic_name": "Android Consciousness",
  "topic_slug": "android-consciousness",
  "definition": "...",
  "pkd_relevance": "...",
  "status": "published",
  "passage_count": 45,
  "evidence_lanes": {
    "A": { "count": 18, "summary": "...", "key_works": [...] },
    "B": { "count": 20, "summary": "...", "key_thinkers": [...] },
    "C": { "count": 7, "summary": "...", "key_works": [...] }
  },
  "dossier": {
    "definition_section": "...",
    "in_fiction_section": "...",
    "in_exegesis_section": "...",
    "intellectual_background_section": "...",
    "scholarly_debate_section": "...",
    "chronology_section": [...],
    "key_passages": [
      {
        "excerpt": "...",
        "source_title": "Do Androids Dream of Electric Sheep?",
        "evidence_lane": "A",
        "source_mode": "fiction",
        "claim_type": "allegory"
      }
    ],
    "contradictions": [...],
    "related_works": ["Do Androids Dream", "We Can Build You"],
    "related_thinkers": ["Alan Turing", "Descartes"],
    "related_entries": ["empathy", "android", "Voigt-Kampff"],
    "related_topics": ["ai:empathy-testing", "ai:counterfeit-humanity"],
    "editorial_notes": "...",
    "open_questions": [...]
  },
  "linked_archive_docs": [
    { "doc_id": "...", "title": "...", "card_summary": "..." }
  ],
  "linked_dictionary_terms": [
    { "term_id": "...", "term_name": "...", "slug": "..." }
  ],
  "linked_segments": [
    { "seg_id": "...", "title": "...", "date_display": "..." }
  ]
}
```

### Cross-Navigation

Study topics integrate with the existing site through:

1. **Dictionary → Study:** Term detail pages show "Appears in studies" section linking to relevant topic dossiers
2. **Study → Dictionary:** Dossier pages link to dictionary terms in "Related Entries"
3. **Study → Archive:** Dossier pages link to archive documents used as Lane C evidence
4. **Study → Segments:** Dossier key passages link to original Exegesis segments
5. **Study → Names:** Dossier "Related Thinkers" links to the Names section
6. **Study → Biography:** Chronology entries link to biography events
7. **Search:** Study topics appear in global search results
8. **Tags:** Study topics contribute to the tag system (e.g., `/tag/paranoia` shows the topic + related segments + related terms)

### Nav Update

```tsx
// App.tsx nav additions
<NavLink to="/studies">Studies</NavLink>
```

The Studies nav item replaces nothing — it's a new top-level section. The nav order becomes:
`Timeline · Dictionary · Names · Studies · Archive · Biography · Scholars · Search`

---

## 8. Fair-Use and Scholarly Style Guide

### Copyright Rules

1. **Maximum quote length:** 50 words per quoted passage in dossier prose.
2. **Passage excerpts in database:** Up to 300 words for internal indexing (not displayed verbatim to users).
3. **Displayed excerpts:** Truncated to 100 words with "[...]" and source attribution.
4. **No full chapter/section reproduction:** Never display a complete chapter, essay, or article section.
5. **Transformative use:** All quotes must appear within analytical context that adds scholarly value.
6. **Attribution:** Every quote must cite author, work title, and approximate location.

### Prose Style Rules

1. **Reading level:** College undergraduate (clear, analytical, avoids excessive jargon).
2. **Voice:** Third person, present tense for analysis ("Dick explores..." not "Dick explored...").
3. **Lane separation:** Always distinguish "In the fiction, androids are..." from "In the Exegesis, Dick theorizes..." from "Scholars have argued..."
4. **No diagnosis:** Never state or imply that PKD "had" or "suffered from" a specific psychological condition. Use language like "PKD explored themes of paranoia in his fiction and self-reflection" rather than "PKD's paranoia manifested in..."
5. **Contradiction preservation:** Present opposing views without resolving them. Use "However," "By contrast," "In tension with this view," rather than "The correct interpretation is..."
6. **Evidentiary modesty:** Use "suggests," "indicates," "appears to" rather than "proves" or "demonstrates" for interpretive claims.

### Structured Attribution Format

```
[Lane A] In *Do Androids Dream of Electric Sheep?* (1968), Dick presents...
[Lane B] In a 1978 Exegesis entry (Folder 18), Dick writes: "[≤50 word quote]"
[Lane C] As Warrick (1987) argues, "[≤50 word quote]"
```

---

## 9. First-Wave Build Order

### Wave 1: Infrastructure (no LLM required)

| Step | Script | Output | Estimated Time |
|------|--------|--------|----------------|
| 1.1 | Apply schema extensions | New tables in SQLite | 2 min |
| 1.2 | Create `ai_topics.csv` + `psychology_topics.csv` | Reference data files | 15 min |
| 1.3 | Write `scripts/study/ontology.py` | Populated `study_topics` table (44 rows) | 30 min |
| 1.4 | Write `scripts/study/passage_classifier.py` (deterministic layer only) | Populated `study_passages` table (est. 2,000-4,000 rows) | 1 hr |

### Wave 2: Evidence Assembly (no LLM required)

| Step | Script | Output | Estimated Time |
|------|--------|--------|----------------|
| 2.1 | Write `scripts/study/evidence_builder.py` | Populated `study_evidence` table (est. ~88 rows: 44 topics × 2 lanes avg) | 45 min |
| 2.2 | Write `scripts/study/cross_linker.py` | Populated `study_topic_terms` and `study_topic_names` | 30 min |
| 2.3 | Add `export_studies()` to `export_json.py` | JSON files in `site/public/data/studies/` | 30 min |

### Wave 3: Site Viewer (no LLM required)

| Step | Component | Output | Estimated Time |
|------|-----------|--------|----------------|
| 3.1 | `Studies.tsx` | Study index page | 20 min |
| 3.2 | `StudyOverview.tsx` | Per-study topic listing with lane filters | 30 min |
| 3.3 | `StudyTopic.tsx` | Topic dossier page (initially showing evidence only, no prose dossier) | 45 min |
| 3.4 | Route additions in `App.tsx` | New routes registered | 5 min |
| 3.5 | Search index integration | Study topics searchable | 15 min |

### Wave 4: LLM-Assisted Enrichment

| Step | Script | Output | Estimated Time |
|------|--------|--------|----------------|
| 4.1 | Passage classification (LLM layer) | `claim_type` + `confidence` + `psych_mode` filled in | Variable (API calls) |
| 4.2 | Contradiction detection | `study_contradictions` populated | Variable |
| 4.3 | Dossier drafting (20 seed topics) | `study_dossiers` for priority topics | Variable |

**Priority seed topics for first draft (10 psychology + 10 AI):**

Psychology:
1. paranoia
2. schizophrenia
3. empathy
4. identity-diffusion
5. addiction
6. jung
7. anamnesis
8. twin-motif
9. double
10. hypnagogic

AI:
1. android-consciousness
2. empathy-testing
3. simulation
4. false-reality
5. implanted-memory
6. surveillance
7. counterfeit-humanity
8. reality-testing
9. cybernetics
10. precognition-tech

### Wave 5: Cross-Navigation

| Step | Files Modified | Change |
|------|---------------|--------|
| 5.1 | `TermDetail.tsx` | Add "Appears in Studies" section |
| 5.2 | `ArchiveDetail.tsx` | Add "Referenced in Studies" section |
| 5.3 | `SegmentDetail.tsx` | Add "Study Topics" linked from this segment |
| 5.4 | `NameDetail.tsx` | Add "Related Study Topics" for thinkers |
| 5.5 | `Search.tsx` | Add study topics to search results |

---

## 10. Concrete Repo Implementation Plan

### New Files to Create

```
scripts/study/
├── __init__.py
├── ontology.py                    # Topic definitions loader
├── passage_classifier.py          # Deterministic + LLM passage extraction
├── evidence_builder.py            # Evidence packet assembly
├── contradiction_detector.py      # Cross-lane contradiction detection
├── entry_drafter.py               # LLM dossier generation
├── cross_linker.py                # Topic ↔ term/name/archive linking
└── study_export.py                # JSON export for studies

database/reference_data/
├── ai_topics.csv                  # AI topic ontology (22 rows)
└── psychology_topics.csv          # Psychology topic ontology (22 rows)

site/src/pages/
├── Studies.tsx                    # Study index page
├── StudyOverview.tsx              # Per-study landing page
└── StudyTopic.tsx                 # Topic dossier viewer

site/public/data/studies/
├── index.json
├── ai/
│   ├── index.json
│   └── topics/*.json
└── psychology/
    ├── index.json
    └── topics/*.json
```

### Existing Files to Modify

| File | Change |
|------|--------|
| `database/unified_schema.sql` | Add study tables (Section 3 SQL) |
| `scripts/build_all.py` | Add `run_stage_5()` for study pipeline |
| `scripts/export_json.py` | Add `export_studies()` function |
| `site/src/App.tsx` | Add `/studies/*` routes |
| `site/src/pages/TermDetail.tsx` | Add "Appears in Studies" cross-link |
| `site/src/pages/ArchiveDetail.tsx` | Add "Referenced in Studies" cross-link |
| `site/src/pages/SegmentDetail.tsx` | Add "Study Topics" cross-link |
| `site/src/pages/NameDetail.tsx` | Add "Related Study Topics" cross-link |
| `site/src/pages/Search.tsx` | Add study topics to search index |

### Build Command Integration

```bash
# Full pipeline including studies
python scripts/build_all.py --skip-llm --studies

# Studies only (assumes existing DB)
python scripts/build_all.py --studies-only

# Studies with LLM classification
python scripts/build_all.py --studies --classify

# Studies with full LLM (classification + dossier drafting)
python scripts/build_all.py --studies --classify --draft

# Export only (regenerate JSON from existing DB data)
python scripts/build_all.py --export-only
```

### Verification Checklist

- [ ] Schema extensions apply cleanly to existing database
- [ ] Ontology loads 44 topics (22 AI + 22 psychology) without errors
- [ ] Passage extraction finds ≥100 passages per well-represented topic
- [ ] Evidence packets have ≥2 lanes per topic for ≥30 of 44 topics
- [ ] JSON export produces valid files matching expected structure
- [ ] `npm run build` passes with new components
- [ ] Study index page renders with topic counts
- [ ] Topic dossier page displays evidence organized by lane
- [ ] Cross-links from dictionary terms to study topics work
- [ ] Search finds study topics
- [ ] No quote in displayed output exceeds 50 words
- [ ] No dossier text diagnoses PKD

---

## Appendix A: Passage Classification Ontology Reference

### source_mode values
| Value | Description |
|-------|-------------|
| `fiction` | From a novel, story, or screenplay |
| `exegesis` | From the Exegesis notebooks |
| `letter` | From PKD's correspondence |
| `interview` | From recorded interviews |
| `criticism` | From academic scholarship |
| `biography` | From biographical accounts |

### claim_type values
| Value | Description |
|-------|-------------|
| `definition` | Passage defines or explains the concept |
| `symptom_description` | Passage describes psychological symptoms or behaviors |
| `causal_theory` | Passage proposes why something happens |
| `allegory` | Passage uses the concept metaphorically or symbolically |
| `self_report` | PKD describing his own experience |
| `critique` | Scholar critiquing or analyzing the concept |
| `comparison` | Passage compares concepts or draws parallels |
| `unresolved` | Passage raises questions without answering |

### psych_mode values (psychology study only)
| Value | Description |
|-------|-------------|
| `clinical` | Medical/psychiatric framework |
| `psychoanalytic` | Freudian framework |
| `Jungian` | Jungian analytical psychology |
| `existential` | Existentialist psychology |
| `neuropsychological` | Brain science / neurology |
| `anti_psychiatric` | R.D. Laing-style critique of psychiatry |
| `mystical` | Religious / mystical experience framework |
| `popular_psychology` | Everyday psychological concepts |

### confidence values
| Value | Criteria |
|-------|---------|
| `high` | Passage explicitly discusses the topic by name |
| `medium` | Passage clearly relates to the topic but doesn't name it |
| `low` | Passage may relate to the topic; connection is interpretive |

## Appendix B: Lexicon Compilation Strategy

Each topic gets a lexicon compiled from three sources:

1. **Core terms:** Direct name and common synonyms
2. **PKD-specific terms:** How PKD refers to this concept (from Exegesis vocabulary)
3. **Scholarly terms:** How critics discuss this concept

Example for `psych:paranoia`:

```python
PARANOIA_LEXICON = {
    'core': [r'\bparanoi[ad]\b', r'\bparanoid\b', r'\bpersecutory\b'],
    'pkd': [r'\bthey.{0,15}watching\b', r'\bcovert\s+action\b', r'\bblack\s+iron\b'],
    'scholarly': [r'\bpersecutory\s+delusion\b', r'\bparanoid\s+schizophren\b',
                  r'\bparanoid\s+ideation\b'],
}
```

Lexicons are stored in `scripts/study/ontology.py` as Python data structures (not external files) to keep them versioned with the code and easily editable.
