# QueryPat Studies Blueprint

## Implementation Blueprint for AI Topics & Psychology Topics Research Studies

---

## 1. Repo Reuse Analysis

### Scripts to Reuse Directly

| Script | Purpose | Reuse for Studies |
|--------|---------|-------------------|
| `scripts/build_all.py` | Pipeline orchestrator | Add Stage 5 for study pipeline |
| `scripts/export_json.py` | JSON export to site | Add `export_studies()` function |
| `scripts/discover/discovery_pipeline.py` | Corpus scanning | Model for passage scanning architecture |
| `scripts/discover/matchers.py` | Regex-based entity matching | Template for topic matchers |
| `scripts/discover/scoring.py` | Confidence scoring | Reuse scoring formula directly |
| `scripts/date_norms.py` | Slug/ID generation, date normalization | Reuse `make_slug()`, `make_term_id()` |
| `scripts/link/map_evidence_to_segments.py` | Evidence-to-segment linking | Reuse line-range fingerprinting |
| `scripts/link/ingest_evidence_cooccurrences.py` | Co-occurrence extraction | Model for topic co-occurrence |
| `scripts/ingest/ingest_evidence.py` | Evidence packet assembly | Template for study evidence packets |

### Scripts to Extend

| Script | Extension Needed |
|--------|-----------------|
| `scripts/build_all.py` | Add `run_stage_5()` calling study pipeline, add `--studies-only` flag |
| `scripts/export_json.py` | Add `export_studies()` function for study JSON bundles |
| `scripts/improve_all.py` | Add improvement plans for study data quality |
| `database/unified_schema.sql` | Add study tables (see Section 3) |

### New Scripts Required

| Script | Purpose |
|--------|---------|
| `scripts/studies/study_pipeline.py` | Orchestrator for study-specific stages |
| `scripts/studies/ontology.py` | Topic ontology definitions (both studies) |
| `scripts/studies/scan_corpus.py` | Deterministic passage scanning against topic lexicons |
| `scripts/studies/classify_passages.py` | Claude-assisted passage classification |
| `scripts/studies/build_evidence_packets.py` | Assemble evidence packets per topic |
| `scripts/studies/detect_contradictions.py` | Claude-assisted contradiction detection |
| `scripts/studies/draft_dossiers.py` | Claude-assisted dossier drafting |
| `scripts/studies/link_studies.py` | Cross-link topics to terms, names, archive docs |
| `scripts/studies/review_fair_use.py` | Claude-assisted fair-use passage review |
| `scripts/studies/export_studies.py` | Study-specific JSON export (also callable from export_json.py) |

### Claude Skills Required (New)

| Skill File | Purpose |
|------------|---------|
| `.claude/skills/corpus_auditor.md` | Audit corpus coverage for a topic |
| `.claude/skills/topic_tagger.md` | Tag passages with AI or psychology topics |
| `.claude/skills/passage_classifier.md` | Classify passages by source_mode, psych_mode, claim_type |
| `.claude/skills/evidence_builder.md` | Build evidence packets from classified passages |
| `.claude/skills/contradiction_mapper.md` | Identify contradictions across lanes |
| `.claude/skills/dossier_drafter.md` | Draft scholarly topic dossiers |
| `.claude/skills/chronology_synthesizer.md` | Synthesize chronological development of a topic |
| `.claude/skills/fair_use_reviewer.md` | Review passages for fair-use compliance |

---

## 2. Research Architecture

### Four-Lane Evidence Model

The existing archive lane system (A-E) maps cleanly to the required four-lane model with one adjustment:

| Required Lane | Existing Lane | Sources | Color |
|---------------|---------------|---------|-------|
| A: Fiction | A (Fiction) | Novels, stories, screenplays | Purple |
| B: Exegesis | B (Exegesis) | Notebooks, letters, interviews | Orange |
| C: Scholarship | C + D + E | Biographies, criticism, primary docs | Blue |
| D: Synthesis | (new — our output) | Topic dossiers, dictionary entries | Green |

Lane D is produced by the pipeline. All Lane D claims must cite A, B, or C.

The existing `evidentiary_lane` column on `documents` already classifies sources. The study pipeline reads this field to assign lane labels to matched passages.

### Two-Study Architecture

Both studies share identical infrastructure. The only differences are:

1. **Topic ontology** — different topic lists and lexicons
2. **Classification modes** — psychology study uses `psych_mode`; AI study uses `ai_mode`
3. **Guardrails** — psychology study must never diagnose PKD

The shared infrastructure means one pipeline, one set of tables, one viewer component — parameterized by `study_id`.

### Study Identity

```
study_id: "ai"
study_label: "AI Topics"
study_slug: "ai"

study_id: "psychology"
study_label: "Psychology Topics"
study_slug: "psychology"
```

---

## 3. Data Model and Schema Extensions

### New Tables

```sql
-- ============================================================
-- STUDIES: Topic Dossiers
-- ============================================================

CREATE TABLE studies (
    study_id            TEXT PRIMARY KEY,           -- "ai" or "psychology"
    study_label         TEXT NOT NULL,
    study_description   TEXT,
    topic_count         INTEGER DEFAULT 0,
    created_at          TEXT DEFAULT (datetime('now')),
    updated_at          TEXT DEFAULT (datetime('now'))
);

CREATE TABLE study_topics (
    topic_id            TEXT PRIMARY KEY,           -- TOPIC_AI_* or TOPIC_PSY_*
    study_id            TEXT NOT NULL,
    canonical_name      TEXT NOT NULL,
    slug                TEXT NOT NULL,

    -- Classification
    status              TEXT NOT NULL DEFAULT 'seed' CHECK (status IN (
                            'seed', 'scanning', 'evidence_built', 'drafted',
                            'reviewed', 'published'
                        )),
    priority            INTEGER DEFAULT 0,          -- higher = process first

    -- Dossier content (populated by Claude drafting)
    definition          TEXT,
    pkd_relevance       TEXT,
    in_the_fiction      TEXT,
    in_the_exegesis     TEXT,
    intellectual_background TEXT,
    scholarly_debate    TEXT,
    chronology_summary  TEXT,
    contradictions_summary TEXT,
    related_thinkers    TEXT,                       -- JSON array
    editorial_notes     TEXT,
    open_questions      TEXT,                       -- JSON array

    -- Card-level fields
    card_description    TEXT,                       -- short description for index grid

    -- Metadata
    passage_count       INTEGER DEFAULT 0,
    evidence_count      INTEGER DEFAULT 0,
    contradiction_count INTEGER DEFAULT 0,

    -- Chronology
    first_appearance    TEXT,                       -- ISO date
    peak_period_start   TEXT,
    peak_period_end     TEXT,

    -- Cross-linking
    related_topics      TEXT,                       -- JSON array of topic_ids
    related_terms       TEXT,                       -- JSON array of term slugs
    related_names       TEXT,                       -- JSON array of name slugs

    provenance          TEXT,
    notes               TEXT,
    created_at          TEXT DEFAULT (datetime('now')),
    updated_at          TEXT DEFAULT (datetime('now')),

    FOREIGN KEY (study_id) REFERENCES studies(study_id),
    UNIQUE (study_id, slug)
);

CREATE INDEX idx_study_topics_study ON study_topics(study_id);
CREATE INDEX idx_study_topics_status ON study_topics(status);
CREATE INDEX idx_study_topics_slug ON study_topics(slug);

-- ============================================================

CREATE TABLE study_passages (
    passage_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id            TEXT NOT NULL,

    -- Source location
    doc_id              TEXT,                       -- FK to documents
    seg_id              TEXT,                       -- FK to segments (Exegesis)
    page_num            INTEGER,                    -- for archive PDFs
    char_offset_start   INTEGER,
    char_offset_end     INTEGER,

    -- Passage content
    passage_text        TEXT NOT NULL,              -- the matched text (fair-use length)
    context_before      TEXT,                       -- surrounding context
    context_after       TEXT,

    -- Evidentiary lane (derived from document)
    lane                TEXT CHECK (lane IN ('A', 'B', 'C')),

    -- Classification (Claude-assigned)
    source_mode         TEXT CHECK (source_mode IN (
                            'fiction', 'exegesis', 'letter', 'interview', 'criticism'
                        )),
    claim_type          TEXT CHECK (claim_type IN (
                            'definition', 'symptom_description', 'causal_theory',
                            'allegory', 'self_report', 'critique', 'comparison',
                            'unresolved'
                        )),
    confidence          TEXT CHECK (confidence IN ('high', 'medium', 'low')),

    -- Psychology-specific classification
    psych_mode          TEXT CHECK (psych_mode IN (
                            'clinical', 'psychoanalytic', 'jungian', 'existential',
                            'neuropsychological', 'anti_psychiatric', 'mystical',
                            'popular_psychology', NULL
                        )),

    -- AI-specific classification
    ai_mode             TEXT CHECK (ai_mode IN (
                            'technological', 'philosophical', 'satirical',
                            'dystopian', 'empathic', 'ontological', NULL
                        )),

    -- Matching metadata
    matched_terms       TEXT,                       -- JSON array of matched lexicon terms
    match_method        TEXT CHECK (match_method IN (
                            'lexicon_exact', 'lexicon_alias', 'claude_conceptual',
                            'claude_inferred'
                        )),

    -- Review
    fair_use_status     TEXT DEFAULT 'pending' CHECK (fair_use_status IN (
                            'pending', 'approved', 'trimmed', 'rejected'
                        )),
    editorial_status    TEXT DEFAULT 'unreviewed',

    notes               TEXT,
    created_at          TEXT DEFAULT (datetime('now')),

    FOREIGN KEY (topic_id) REFERENCES study_topics(topic_id),
    FOREIGN KEY (doc_id) REFERENCES documents(doc_id),
    FOREIGN KEY (seg_id) REFERENCES segments(seg_id)
);

CREATE INDEX idx_study_passages_topic ON study_passages(topic_id);
CREATE INDEX idx_study_passages_doc ON study_passages(doc_id);
CREATE INDEX idx_study_passages_seg ON study_passages(seg_id);
CREATE INDEX idx_study_passages_lane ON study_passages(lane);
CREATE INDEX idx_study_passages_claim ON study_passages(claim_type);

-- ============================================================

CREATE TABLE study_evidence_packets (
    ev_id               TEXT PRIMARY KEY,           -- SEV_*
    topic_id            TEXT NOT NULL,

    claim_text          TEXT,
    evidence_summary    TEXT,
    confidence          TEXT CHECK (confidence IN (
                            'strong', 'moderate', 'weak', 'speculative'
                        )),
    source_method       TEXT CHECK (source_method IN (
                            'deterministic', 'heuristic', 'llm', 'editorial'
                        )),
    editorial_status    TEXT DEFAULT 'unreviewed',

    -- Lane breakdown
    lane_a_count        INTEGER DEFAULT 0,          -- fiction passages
    lane_b_count        INTEGER DEFAULT 0,          -- exegesis passages
    lane_c_count        INTEGER DEFAULT 0,          -- scholarship passages

    notes               TEXT,
    created_at          TEXT DEFAULT (datetime('now')),
    updated_at          TEXT DEFAULT (datetime('now')),

    FOREIGN KEY (topic_id) REFERENCES study_topics(topic_id)
);

CREATE INDEX idx_study_ev_topic ON study_evidence_packets(topic_id);

-- ============================================================

CREATE TABLE study_contradictions (
    contradiction_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id            TEXT NOT NULL,

    -- The two sides
    passage_id_a        INTEGER NOT NULL,
    passage_id_b        INTEGER NOT NULL,

    -- Description
    summary             TEXT NOT NULL,              -- what the contradiction is
    explanation         TEXT,                       -- interpretive note

    -- Classification
    contradiction_type  TEXT CHECK (contradiction_type IN (
                            'factual', 'interpretive', 'chronological',
                            'self_vs_critic', 'fiction_vs_exegesis',
                            'early_vs_late'
                        )),

    notes               TEXT,
    created_at          TEXT DEFAULT (datetime('now')),

    FOREIGN KEY (topic_id) REFERENCES study_topics(topic_id),
    FOREIGN KEY (passage_id_a) REFERENCES study_passages(passage_id),
    FOREIGN KEY (passage_id_b) REFERENCES study_passages(passage_id)
);

CREATE INDEX idx_study_contra_topic ON study_contradictions(topic_id);

-- ============================================================

CREATE TABLE study_topic_terms (
    topic_id            TEXT NOT NULL,
    term_id             TEXT NOT NULL,
    relation_type       TEXT DEFAULT 'related' CHECK (relation_type IN (
                            'primary', 'related', 'contrasts', 'subsumes'
                        )),
    PRIMARY KEY (topic_id, term_id),
    FOREIGN KEY (topic_id) REFERENCES study_topics(topic_id),
    FOREIGN KEY (term_id) REFERENCES terms(term_id)
);

CREATE TABLE study_topic_names (
    topic_id            TEXT NOT NULL,
    name_id             TEXT NOT NULL,
    relation_type       TEXT DEFAULT 'related',
    PRIMARY KEY (topic_id, name_id),
    FOREIGN KEY (topic_id) REFERENCES study_topics(topic_id),
    FOREIGN KEY (name_id) REFERENCES names(name_id)
);

CREATE TABLE study_topic_docs (
    topic_id            TEXT NOT NULL,
    doc_id              TEXT NOT NULL,
    relevance           TEXT DEFAULT 'mentions' CHECK (relevance IN (
                            'primary', 'substantial', 'mentions'
                        )),
    passage_count       INTEGER DEFAULT 0,
    PRIMARY KEY (topic_id, doc_id),
    FOREIGN KEY (topic_id) REFERENCES study_topics(topic_id),
    FOREIGN KEY (doc_id) REFERENCES documents(doc_id)
);
```

### ID Policy Extension

```
TOPIC_AI_*     AI study topic
TOPIC_PSY_*    Psychology study topic
SEV_*          Study evidence packet
```

### Views

```sql
CREATE VIEW v_study_topic_summary AS
SELECT st.*,
       s.study_label,
       COUNT(DISTINCT sp.passage_id) AS total_passages,
       COUNT(DISTINCT CASE WHEN sp.lane = 'A' THEN sp.passage_id END) AS fiction_passages,
       COUNT(DISTINCT CASE WHEN sp.lane = 'B' THEN sp.passage_id END) AS exegesis_passages,
       COUNT(DISTINCT CASE WHEN sp.lane = 'C' THEN sp.passage_id END) AS scholarship_passages,
       COUNT(DISTINCT sc.contradiction_id) AS contradictions
FROM study_topics st
JOIN studies s ON st.study_id = s.study_id
LEFT JOIN study_passages sp ON st.topic_id = sp.topic_id
LEFT JOIN study_contradictions sc ON st.topic_id = sc.topic_id
WHERE st.status IN ('drafted', 'reviewed', 'published')
GROUP BY st.topic_id;
```

---

## 4. Pipeline Design

### Overall Flow

```
Stage 5: Studies Pipeline
    5a. Ontology seeding       (deterministic)
    5b. Corpus scanning        (deterministic)
    5c. Passage classification (Claude-assisted, batched)
    5d. Evidence assembly      (deterministic)
    5e. Contradiction detection (Claude-assisted, batched)
    5f. Dossier drafting       (Claude-assisted, per-topic)
    5g. Fair-use review        (Claude-assisted, batched)
    5h. Cross-linking          (deterministic)
    5i. JSON export            (deterministic)
```

### Stage 5a: Ontology Seeding

**Script**: `scripts/studies/ontology.py`
**Type**: Deterministic
**Input**: Hardcoded topic lists (from this blueprint)
**Output**: Rows in `studies` and `study_topics` tables

Seeds both studies with topic records in `status='seed'`. Each topic gets:
- `topic_id` (e.g., `TOPIC_AI_androids`, `TOPIC_PSY_paranoia`)
- `canonical_name`
- `slug`
- `priority` (seed topics get priority 10; others get 5)
- A `lexicon` JSON blob stored in a companion file `scripts/studies/lexicons/` containing:
  - Primary terms (exact match)
  - Alias terms (alternate spellings, related phrases)
  - Exclusion terms (false positives to filter)
  - Context markers (terms that boost confidence when co-occurring)

**Lexicon file structure** (`scripts/studies/lexicons/ai_topics.json`):
```json
{
  "androids": {
    "primary": ["android", "androids"],
    "aliases": ["artificial person", "artificial human", "humanoid robot", "simulacrum"],
    "exclusions": ["Android phone", "Android OS"],
    "context_markers": ["Deckard", "Voigt-Kampff", "empathy test", "bounty hunter"],
    "related_topics": ["empathy_testing", "counterfeit_humanity"]
  }
}
```

### Stage 5b: Corpus Scanning

**Script**: `scripts/studies/scan_corpus.py`
**Type**: Deterministic
**Input**: SQLite corpus (segments.raw_text + document_texts.text_content + page_texts.page_text)
**Output**: Rows in `study_passages` table with `match_method='lexicon_exact'` or `'lexicon_alias'`

Architecture follows `discovery_pipeline.py`:
1. Materialize corpus text once (segments + document_texts + page_texts)
2. For each topic, compile regex from lexicon
3. Scan all text, extract passage windows (±500 chars around match)
4. Record passage with source location (doc_id, seg_id, page_num, char offsets)
5. Assign `lane` from document's `evidentiary_lane` column
6. Deduplicate overlapping windows
7. Set `status` on topic to `'scanning'`

**Text segmentation rules**:
- **Fiction**: Chapter or scene-level windows (use page_texts, ±2 pages around match)
- **Exegesis**: Segment-level (use segments.raw_text, full segment if match found)
- **Criticism**: Paragraph cluster (use document_texts, ±500 chars)

**Passage length cap**: 2000 chars max per passage_text (fair-use guardrail)

### Stage 5c: Passage Classification

**Script**: `scripts/studies/classify_passages.py`
**Type**: Claude-assisted
**Input**: Unclassified passages from `study_passages`
**Output**: Updated `source_mode`, `claim_type`, `confidence`, `psych_mode`/`ai_mode` fields

**Batching strategy**:
- Group passages by topic_id
- Send batches of 10 passages per Claude call
- Include topic definition and classification ontology in system prompt
- Claude returns structured JSON with fields for each passage

**Claude prompt structure**:
```
You are classifying passages from Philip K. Dick's corpus for the topic "{topic_name}".

For each passage, provide:
- source_mode: fiction | exegesis | letter | interview | criticism
- claim_type: definition | symptom_description | causal_theory | allegory | self_report | critique | comparison | unresolved
- confidence: high | medium | low
- {psych_mode or ai_mode}: {mode options}
- brief_note: 1-sentence classification rationale

IMPORTANT: Do not diagnose Philip K. Dick. Describe representations, not conditions.

Passages:
[batch of 10 passage texts with IDs]
```

**Token efficiency**: ~500 tokens per passage input, ~100 tokens per classification output. At 10 per batch: ~6000 tokens per call. For 5000 passages: ~500 calls.

### Stage 5d: Evidence Assembly

**Script**: `scripts/studies/build_evidence_packets.py`
**Type**: Deterministic
**Input**: Classified passages
**Output**: Rows in `study_evidence_packets`

For each topic:
1. Group passages by lane (A, B, C)
2. Select representative passages (highest confidence, best coverage across works)
3. Cap at 5 fiction, 5 exegesis, 5 scholarship passages per evidence packet
4. Compute lane breakdown counts
5. Generate `claim_text` from passage statistics
6. Set topic `status` to `'evidence_built'`

### Stage 5e: Contradiction Detection

**Script**: `scripts/studies/detect_contradictions.py`
**Type**: Claude-assisted
**Input**: Evidence packets with passages across lanes
**Output**: Rows in `study_contradictions`

**Strategy**: For each topic with passages in 2+ lanes, send representative passages to Claude with prompt:

```
Given these passages about "{topic_name}" from different sources, identify contradictions.

A contradiction exists when:
- PKD says one thing in fiction but another in the Exegesis
- Different biographers give conflicting accounts
- PKD's position changes over time (early vs. late)
- A critic challenges PKD's self-account

Do NOT resolve contradictions. Describe both sides neutrally.

[passages grouped by lane]
```

**Batching**: Per-topic, not batched across topics. Each topic gets one Claude call.

### Stage 5f: Dossier Drafting

**Script**: `scripts/studies/draft_dossiers.py`
**Type**: Claude-assisted
**Input**: Evidence packets, contradictions, cross-links
**Output**: Populated dossier fields on `study_topics`

**Per-topic Claude call** with structured prompt:

```
You are drafting a scholarly topic dossier for "{topic_name}" in a study of {study_label} in Philip K. Dick's work.

Write at a college reading level. Be analytical and evidence-based. Avoid dense jargon.
Do NOT diagnose PKD. Describe representations, not conditions.
Do NOT reproduce long copyrighted passages. Paraphrase and cite.
Clearly separate what appears in fiction (Lane A), what PKD theorized (Lane B), and what scholars argue (Lane C).

Evidence:
[fiction passages]
[exegesis passages]
[scholarship passages]

Contradictions:
[contradiction summaries]

Related topics: [list]
Related dictionary terms: [list]
Related figures: [list]

Generate these sections:
1. definition (2-3 sentences)
2. pkd_relevance (1 paragraph)
3. in_the_fiction (1-2 paragraphs, cite works)
4. in_the_exegesis (1-2 paragraphs, cite notebook dates)
5. intellectual_background (1 paragraph, cite thinkers)
6. scholarly_debate (1 paragraph, cite scholars)
7. chronology_summary (timeline of topic across PKD's career)
8. contradictions_summary (preserve both sides)
9. related_thinkers (JSON array of names)
10. editorial_notes (notes on evidence gaps)
11. open_questions (JSON array of unresolved questions)
12. card_description (1-sentence summary for grid card)
```

**Token budget**: ~3000 input + ~2000 output per topic. For 45 topics: ~45 calls, ~225K tokens.

### Stage 5g: Fair-Use Review

**Script**: `scripts/studies/review_fair_use.py`
**Type**: Claude-assisted
**Input**: All passage_text entries
**Output**: Updated `fair_use_status` field

Flags passages that are too long or too verbatim. Trims or rejects as needed. Checks:
- No passage exceeds 300 words
- No passage reproduces more than 2 consecutive sentences from a source
- Passages are used for commentary, not reproduction

### Stage 5h: Cross-Linking

**Script**: `scripts/studies/link_studies.py`
**Type**: Deterministic
**Input**: Study topics, existing terms/names/documents
**Output**: Rows in `study_topic_terms`, `study_topic_names`, `study_topic_docs`

1. Match topic canonical_name and lexicon terms against `terms.canonical_name` and `term_aliases.alias_text`
2. Match against `names.canonical_form` and `name_aliases.alias_text`
3. Aggregate `study_passages.doc_id` to populate `study_topic_docs` with passage counts
4. Compute `related_topics` within same study (by passage co-occurrence)

### Stage 5i: JSON Export

**Script**: `scripts/studies/export_studies.py` (also called from `export_json.py`)
**Type**: Deterministic
**Output**: JSON bundles in `site/public/data/studies/`

```
site/public/data/studies/
    index.json                              # [{study_id, label, topic_count}]
    ai/
        index.json                          # [{topic_id, name, slug, card_description, passage_count, status}]
        topics/
            {slug}.json                     # Full dossier + evidence + contradictions + cross-links
    psychology/
        index.json
        topics/
            {slug}.json
```

**Per-topic detail JSON** (`{slug}.json`):
```json
{
  "topic_id": "TOPIC_PSY_paranoia",
  "study_id": "psychology",
  "canonical_name": "Paranoia",
  "slug": "paranoia",
  "status": "published",

  "definition": "...",
  "pkd_relevance": "...",
  "in_the_fiction": "...",
  "in_the_exegesis": "...",
  "intellectual_background": "...",
  "scholarly_debate": "...",
  "chronology_summary": "...",
  "contradictions_summary": "...",
  "related_thinkers": ["R.D. Laing", "Carl Jung"],
  "editorial_notes": "...",
  "open_questions": ["...", "..."],

  "card_description": "...",
  "passage_count": 47,

  "chronology": {
    "first_appearance": "1955",
    "peak_period": "1964-1970",
    "timeline": [
      {"year": "1955", "event": "First paranoid protagonist in Solar Lottery"},
      {"year": "1964", "event": "The Three Stigmata explores paranoid cosmology"}
    ]
  },

  "evidence": {
    "fiction": [
      {"text": "...", "work": "A Scanner Darkly", "page": 42, "claim_type": "allegory", "confidence": "high"}
    ],
    "exegesis": [
      {"text": "...", "date": "1978-03", "seg_id": "SEG_EXEG_042", "claim_type": "self_report", "confidence": "high"}
    ],
    "scholarship": [
      {"text": "...", "doc_id": "DOC_ARCH_015", "author": "Fitting", "claim_type": "critique", "confidence": "high"}
    ]
  },

  "contradictions": [
    {
      "summary": "PKD describes his paranoia as both pathological and visionary",
      "side_a": {"passage": "...", "lane": "B", "date": "1974"},
      "side_b": {"passage": "...", "lane": "B", "date": "1978"},
      "type": "early_vs_late"
    }
  ],

  "related_topics": [
    {"slug": "schizophrenia", "name": "Schizophrenia", "relation": "related"},
    {"slug": "false-reality", "name": "False Reality", "relation": "related"}
  ],
  "related_terms": [
    {"slug": "black-iron-prison", "name": "Black Iron Prison"},
    {"slug": "valis", "name": "VALIS"}
  ],
  "related_names": [
    {"slug": "horselover-fat", "name": "Horselover Fat"}
  ],
  "related_docs": [
    {"slug": "fitting-paranoia-pkd", "title": "Fitting on Paranoia in PKD", "passage_count": 3}
  ]
}
```

---

## 5. Claude Skills Design

### Skill 1: Corpus Auditor

**Purpose**: Audit corpus coverage for a specific topic before scanning.
**Inputs**: topic_name, lexicon terms, corpus statistics
**Outputs**: Coverage report (estimated passages per lane, corpus gaps, suggested additional lexicon terms)
**Guardrails**: Read-only; no DB writes
**Deterministic before**: Count lexicon matches in document_texts and segments
**Deterministic after**: Store audit report as JSON artifact

### Skill 2: Topic Tagger (AI + Psychology variants)

**Purpose**: Tag passages with topic relevance scores and mode classification.
**Inputs**: Batch of 10 passages with source metadata
**Outputs**: Structured JSON with source_mode, claim_type, confidence, mode-specific fields
**Guardrails**: Must not diagnose PKD. Must not resolve contradictions. Must assign exactly one claim_type per passage.
**Deterministic before**: Pre-filter passages by lexicon match confidence
**Deterministic after**: Validate output schema, write to study_passages

### Skill 3: Passage Classifier

**Purpose**: Detailed classification of passages using the full ontology.
**Inputs**: Single passage with topic context
**Outputs**: source_mode, psych_mode/ai_mode, claim_type, confidence, rationale
**Guardrails**: Same as Topic Tagger
**Deterministic before**: Extract lane from document metadata
**Deterministic after**: Schema validation, DB update

### Skill 4: Evidence Packet Builder

**Purpose**: Select representative passages and synthesize evidence summary.
**Inputs**: All classified passages for a topic, grouped by lane
**Outputs**: Evidence summary text, representative passage selection, confidence assessment
**Guardrails**: Max 5 passages per lane. Must include all lanes with available data.
**Deterministic before**: Group and sort passages by confidence and coverage
**Deterministic after**: Create study_evidence_packets row

### Skill 5: Contradiction Mapper

**Purpose**: Identify and describe contradictions across lanes and time periods.
**Inputs**: Representative passages from 2+ lanes for a topic
**Outputs**: List of contradictions with summaries, passage references, contradiction types
**Guardrails**: Must preserve both sides. Must not resolve. Must not diagnose.
**Deterministic before**: Identify passage pairs from different lanes/dates
**Deterministic after**: Create study_contradictions rows

### Skill 6: Dossier Drafter

**Purpose**: Draft the full scholarly dossier for a topic.
**Inputs**: Evidence packets, contradictions, cross-links, topic metadata
**Outputs**: 12 structured text sections (see Stage 5f prompt)
**Guardrails**: College reading level. No diagnosis. Fair-use compliant. Lane separation.
**Deterministic before**: Assemble all inputs into structured prompt
**Deterministic after**: Parse output sections, update study_topics row

### Skill 7: Chronology Synthesizer

**Purpose**: Build a chronological timeline of how a topic develops across PKD's career.
**Inputs**: All dated passages for a topic, biography events, publication dates
**Outputs**: Timeline entries with year, event description, source reference
**Guardrails**: Must cite sources. Must not invent dates.
**Deterministic before**: Sort passages by date, merge with biography_events and document dates
**Deterministic after**: Store as chronology JSON in study_topics

### Skill 8: Fair-Use Reviewer

**Purpose**: Review passages for copyright compliance.
**Inputs**: Batch of passages with source metadata
**Outputs**: fair_use_status per passage (approved/trimmed/rejected), trimmed text if applicable
**Guardrails**: No passage > 300 words. No verbatim runs > 2 sentences. Commentary context required.
**Deterministic before**: Flag passages > 300 words automatically
**Deterministic after**: Update fair_use_status, replace passage_text if trimmed

---

## 6. Prompt Swarm Architecture

### Agent Roles

```
┌─────────────────────────────────────────────────────┐
│                   ORCHESTRATOR                       │
│            (study_pipeline.py)                       │
│  Manages phases, checkpointing, token budgets        │
└──────────┬──────────┬──────────┬────────────────────┘
           │          │          │
    ┌──────▼──┐ ┌─────▼────┐ ┌──▼──────────┐
    │ Phase 1  │ │ Phase 2   │ │ Phase 3     │
    │ SCAN     │ │ CLASSIFY  │ │ SYNTHESIZE  │
    │(determ.) │ │(Claude)   │ │(Claude)     │
    └──────────┘ └──────────┘ └─────────────┘
```

### Phase 1: Scan (Deterministic, Parallel)

| Agent | Task | Parallelism |
|-------|------|-------------|
| Corpus Scanner (AI) | Scan all substrates for AI lexicon matches | Parallel with PSY scanner |
| Corpus Scanner (PSY) | Scan all substrates for PSY lexicon matches | Parallel with AI scanner |
| Cross-Linker | Pre-compute term/name/doc links for all topics | After both scanners |

**Batch strategy**: Process corpus in chunks of 100 segments or 50 documents. Each chunk is independent.

### Phase 2: Classify (Claude-Assisted, Batched)

| Agent | Task | Parallelism |
|-------|------|-------------|
| Topic Tagger (AI) | Classify AI passages in batches of 10 | Parallel with PSY tagger |
| Topic Tagger (PSY) | Classify PSY passages in batches of 10 | Parallel with AI tagger |
| Fair-Use Reviewer | Review all passages for compliance | After both taggers |

**Batch strategy**: 10 passages per Claude call. Process topics in priority order. Checkpoint after each topic completes.

**Token budget**: ~6000 tokens per batch (10 passages). For 5000 total passages: ~3M tokens for classification.

### Phase 3: Synthesize (Claude-Assisted, Per-Topic)

| Agent | Task | Parallelism |
|-------|------|-------------|
| Evidence Builder | Build evidence packets per topic | Sequential within study |
| Contradiction Mapper | Detect contradictions per topic | After evidence builder |
| Chronology Synthesizer | Build timeline per topic | Parallel with contradiction mapper |
| Dossier Drafter | Draft full dossier per topic | After all above |
| Reviewer | Quality check drafted dossiers | After drafter |

**Batch strategy**: Process one topic at a time through the full synthesis pipeline. Topics processed in priority order.

**Token budget**: ~5000 tokens per topic for synthesis. For 45 topics: ~225K tokens.

### Checkpointing and Restart

Each stage writes to SQLite. Topic `status` field tracks progress:
- `seed` → ontology loaded
- `scanning` → corpus scan started
- `evidence_built` → passages classified, evidence assembled
- `drafted` → dossier drafted by Claude
- `reviewed` → quality-checked
- `published` → ready for viewer

On restart, the pipeline checks each topic's status and resumes from the earliest incomplete stage. No work is repeated.

**Checkpoint file**: `scripts/studies/checkpoint.json`
```json
{
  "last_run": "2026-03-14T10:30:00",
  "phase": "classify",
  "topics_completed": ["paranoia", "schizophrenia", "androids"],
  "topics_in_progress": ["empathy"],
  "total_tokens_used": 1250000
}
```

### Token Efficiency Strategy

1. **Lexicon pre-filtering**: Only send passages with lexicon matches to Claude (reduces volume by ~80%)
2. **Batch classification**: 10 passages per call instead of 1 (reduces overhead by ~90%)
3. **Structured output**: Request JSON-only responses (no prose preamble)
4. **Progressive detail**: Scan all → classify high-priority → synthesize top 20 → expand
5. **Shared context**: AI and PSY taggers share corpus materialization
6. **Caching**: Store Claude responses alongside passages for audit trail

### Artifact Outputs

Each phase produces checkpointable artifacts:

| Phase | Artifact | Location |
|-------|----------|----------|
| Scan | Passage records | `study_passages` table |
| Classify | Classification fields | `study_passages` table (updated) |
| Evidence | Evidence packets | `study_evidence_packets` table |
| Contradictions | Contradiction records | `study_contradictions` table |
| Synthesis | Dossier text | `study_topics` table (updated) |
| Export | JSON bundles | `site/public/data/studies/` |

---

## 7. Website Viewer Architecture

### Navigation Structure

**Recommended**: Top-level "Studies" section with sub-navigation.

```
Home
Archive
Dictionary
Timeline
Biography
Studies ← new top-level nav item
  AI Study
  Psychology Study
Scholars
Names
```

**Rationale**: Studies are a major research output, not a sub-feature. They deserve top-level nav placement. However, putting both studies as separate top-level items would crowd the nav bar (already 8 items). A "Studies" parent with sub-navigation keeps the nav clean while giving studies proper prominence. The Studies landing page also serves as a gateway that explains both research programs.

### Routes

```
/studies                    → StudiesIndex (overview of both studies)
/studies/ai                 → StudyIndex (AI topic grid)
/studies/psychology         → StudyIndex (Psychology topic grid)
/studies/ai/:slug           → TopicDetail (AI topic dossier)
/studies/psychology/:slug   → TopicDetail (Psychology topic dossier)
```

### New Components

| Component | File | Purpose |
|-----------|------|---------|
| `StudiesIndex` | `site/src/pages/StudiesIndex.tsx` | Landing page for both studies |
| `StudyIndex` | `site/src/pages/StudyIndex.tsx` | Topic grid for one study (parameterized by study_id) |
| `TopicDetail` | `site/src/pages/TopicDetail.tsx` | Full dossier page for one topic |
| `EvidencePanel` | `site/src/components/EvidencePanel.tsx` | Lane-organized evidence display |
| `ContradictionCard` | `site/src/components/ContradictionCard.tsx` | Side-by-side contradiction display |
| `LaneFilter` | `site/src/components/LaneFilter.tsx` | Filter passages by evidentiary lane |
| `TopicChronology` | `site/src/components/TopicChronology.tsx` | Timeline visualization for topic |

### StudiesIndex Page

Displays both studies as cards with:
- Study title and description
- Topic count
- Sample topics (top 5 by passage count)
- Link to full study index

### StudyIndex Page

Grid of topic cards (reuses `.card-grid` pattern from Dictionary):
- Topic name
- Card description (1 sentence)
- Passage count badge
- Lane breakdown (colored dots: purple/orange/blue)
- Status badge

**Filters**:
- Text search (Fuse.js)
- Lane filter (show topics with fiction / exegesis / scholarship passages)
- Status filter (published / drafted)

### TopicDetail Page

Uses `EntityLayout` component with study-specific content:

```
EntityLayout
  title: "Paranoia"
  entityType: "topic"
  entityId: "TOPIC_PSY_paranoia"
  badges: [{label: "Psychology Study"}, {label: "47 passages"}]
  tags: [{label: "Lane A", to: ...}, {label: "Lane B"}, ...]

  Content:
    ├── Definition section
    ├── PKD Relevance section
    ├── In the Fiction section (with archive cross-links)
    ├── In the Exegesis section (with segment cross-links)
    ├── Intellectual Background section
    ├── Scholarly Debate section
    ├── Chronology section (TopicChronology component)
    ├── Key Passages section (EvidencePanel component)
    │   ├── Lane A tab (fiction passages)
    │   ├── Lane B tab (exegesis passages)
    │   └── Lane C tab (scholarship passages)
    ├── Contradictions section (ContradictionCard components)
    ├── Related Topics section (links to other topic pages)
    ├── Related Terms section (links to dictionary)
    ├── Related Names section (links to names)
    ├── Related Works section (links to archive)
    ├── Editorial Notes section
    └── Open Questions section

  Footer:
    ExploreFooter (related topics, terms, archive docs)
    BacklinksPanel (what links here)
```

### EvidencePanel Component

Tabbed display organized by lane:

```
┌──────────────────────────────────────────────────┐
│  [Fiction (12)]  [Exegesis (23)]  [Scholarship (8)] │
├──────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────┐ │
│  │ 📖 A Scanner Darkly, ch. 7                  │ │
│  │ "Bob Arctor watches himself through..."      │ │
│  │ claim: allegory | confidence: high           │ │
│  │ → View in Archive                            │ │
│  └─────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────┐ │
│  │ 📖 VALIS, ch. 2                             │ │
│  │ "Fat began to think he was losing..."        │ │
│  │ claim: self_report | confidence: high        │ │
│  │ → View in Archive                            │ │
│  └─────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────┘
```

### ContradictionCard Component

Side-by-side display:

```
┌──────────────────────────────────────────────────┐
│ ⚡ Contradiction: PKD on paranoia as pathology   │
│    vs. spiritual insight                         │
├────────────────────┬─────────────────────────────┤
│  Lane B (1974)     │  Lane B (1978)              │
│  "My paranoid      │  "What I took for paranoia  │
│   episodes were    │   was actually a form of    │
│   clearly..."      │   gnosis..."                │
│                    │                              │
│  → Segment 042     │  → Segment 187              │
├────────────────────┴─────────────────────────────┤
│  Type: early_vs_late                             │
└──────────────────────────────────────────────────┘
```

### LaneFilter Component

Reusable filter strip:

```
[All] [◉ Fiction] [◉ Exegesis] [◉ Scholarship]
```

Color-coded to match existing lane badge colors from Archive.

### Layout.tsx Changes

Add "Studies" nav item:
```tsx
<NavLink to="/studies">Studies</NavLink>
```

### App.tsx Route Changes

```tsx
<Route path="studies" element={<StudiesIndex />} />
<Route path="studies/:studyId" element={<StudyIndex />} />
<Route path="studies/:studyId/:slug" element={<TopicDetail />} />
```

### Search Integration

Add study topics to `search_index.json`:
```json
{
  "type": "topic",
  "id": "TOPIC_PSY_paranoia",
  "slug": "paranoia",
  "title": "Paranoia",
  "text": "...",
  "category": "Psychology Study",
  "study": "psychology"
}
```

### Bookmarks Integration

Study topics are bookmarkable using existing `BookmarkButton` with `entityType: "topic"`.

---

## 8. Fair-Use and Scholarly Style Guide

### Passage Length Limits

| Source Type | Max Passage Length | Rationale |
|------------|-------------------|-----------|
| Fiction (novels/stories) | 150 words | Most restrictive — commercial works |
| Exegesis (notebooks) | 250 words | Scholarly source, unpublished |
| Letters/Interviews | 200 words | Semi-public primary sources |
| Criticism/Scholarship | 150 words | Published academic work |

### Fair-Use Principles

1. **Transformative purpose**: All passages serve analytical commentary. Never reproduce for its own sake.
2. **Proportionality**: Never reproduce more than is necessary for the analytical point.
3. **No market substitution**: Dossiers must not serve as a substitute for reading the source.
4. **Attribution**: Every passage cites its source (work title, date, page/segment).

### Writing Style

1. **College reading level**: Assume an intelligent reader without specialist training.
2. **Analytical, not diagnostic**: Describe how PKD represents paranoia; do not diagnose PKD with paranoid disorders.
3. **Evidence-based**: Every claim cites a lane (A, B, or C).
4. **Lane separation**: Make clear whether a claim comes from fiction, the Exegesis, or scholarship.
5. **Contradiction preservation**: Present both sides of contradictions without resolving them.
6. **No jargon without definition**: If a technical term (e.g., "anamnesis") is used, define it on first use.
7. **Active voice preferred**: "PKD portrays paranoia as..." not "Paranoia is portrayed by PKD as..."

### Psychology Study Guardrails

1. Never state that PKD "had" or "suffered from" a condition. Use "PKD depicted" or "PKD described experiencing."
2. When discussing substance use, frame as biographical fact documented by biographers, not as clinical diagnosis.
3. When discussing psychosis or schizophrenia, distinguish between:
   - Fictional representations (Lane A)
   - PKD's self-theorizing (Lane B — the Exegesis is not clinical evidence)
   - Biographer/critic interpretations (Lane C)
4. Use the phrase "as represented in" or "as theorized by PKD" rather than "PKD's paranoia" or "PKD's schizophrenia."

### AI Study Guardrails

1. Do not conflate PKD's fictional robots/androids with modern AI systems.
2. Contextualize PKD's ideas within mid-20th century cybernetics, not 21st century machine learning.
3. When discussing PKD's ideas about simulation, distinguish between fictional premise and philosophical argument.

---

## 9. First-Wave Build Order

### Phase 1: Foundation (deterministic, no Claude)

| Step | Task | Script | Output |
|------|------|--------|--------|
| 1.1 | Define schema extensions | `database/unified_schema.sql` | New tables created |
| 1.2 | Define topic ontologies | `scripts/studies/ontology.py` | Seed rows in study_topics |
| 1.3 | Write topic lexicons | `scripts/studies/lexicons/*.json` | Lexicon files |
| 1.4 | Build corpus scanner | `scripts/studies/scan_corpus.py` | Passages in study_passages |
| 1.5 | Build cross-linker | `scripts/studies/link_studies.py` | Cross-link rows |

### Phase 2: Classification (Claude-assisted)

| Step | Task | Script | Output |
|------|------|--------|--------|
| 2.1 | Build passage classifier | `scripts/studies/classify_passages.py` | Classified passages |
| 2.2 | Build evidence assembler | `scripts/studies/build_evidence_packets.py` | Evidence packets |
| 2.3 | Build fair-use reviewer | `scripts/studies/review_fair_use.py` | Reviewed passages |

### Phase 3: Synthesis (Claude-assisted)

| Step | Task | Script | Output |
|------|------|--------|--------|
| 3.1 | Build contradiction detector | `scripts/studies/detect_contradictions.py` | Contradiction records |
| 3.2 | Build dossier drafter | `scripts/studies/draft_dossiers.py` | Dossier content |
| 3.3 | Build chronology synthesizer | (integrated into draft_dossiers) | Timeline data |

### Phase 4: Export and Viewer

| Step | Task | Script | Output |
|------|------|--------|--------|
| 4.1 | Build study JSON export | `scripts/studies/export_studies.py` | JSON bundles |
| 4.2 | Extend export_json.py | `scripts/export_json.py` | Integration |
| 4.3 | Extend build_all.py | `scripts/build_all.py` | Stage 5 integration |
| 4.4 | Build StudiesIndex page | `site/src/pages/StudiesIndex.tsx` | Landing page |
| 4.5 | Build StudyIndex page | `site/src/pages/StudyIndex.tsx` | Topic grid |
| 4.6 | Build TopicDetail page | `site/src/pages/TopicDetail.tsx` | Dossier viewer |
| 4.7 | Build EvidencePanel | `site/src/components/EvidencePanel.tsx` | Evidence display |
| 4.8 | Build ContradictionCard | `site/src/components/ContradictionCard.tsx` | Contradiction display |
| 4.9 | Build LaneFilter | `site/src/components/LaneFilter.tsx` | Lane filtering |
| 4.10 | Update Layout nav | `site/src/components/Layout.tsx` | Studies nav link |
| 4.11 | Update App routes | `site/src/App.tsx` | Study routes |
| 4.12 | Update search index | `scripts/export_json.py` | Topics in search |

### Seed Topic Priority (First 20)

**Psychology Study (12 seed topics)**:
1. paranoia
2. schizophrenia
3. empathy
4. identity-diffusion
5. double-doppelganger
6. addiction
7. trauma
8. false-memory
9. jung
10. anamnesis
11. dream-interpretation
12. hypnagogic-state

**AI Study (8 seed topics)**:
1. androids
2. empathy-testing
3. simulation
4. counterfeit-humanity
5. implanted-memory
6. cybernetics
7. machine-intelligence
8. android-affect

---

## 10. Concrete Repo Implementation Plan

### Directory Structure (New Files)

```
scripts/
    studies/
        __init__.py
        study_pipeline.py           # Orchestrator for all study stages
        ontology.py                 # Topic ontology definitions + seeding
        scan_corpus.py              # Deterministic passage scanning
        classify_passages.py        # Claude-assisted classification
        build_evidence_packets.py   # Evidence assembly
        detect_contradictions.py    # Claude-assisted contradiction detection
        draft_dossiers.py           # Claude-assisted dossier drafting
        review_fair_use.py          # Claude-assisted fair-use review
        link_studies.py             # Cross-linking to terms/names/docs
        export_studies.py           # JSON export for viewer
        checkpoint.json             # Pipeline state tracking
        lexicons/
            ai_topics.json          # AI study lexicon
            psychology_topics.json  # Psychology study lexicon

.claude/
    skills/
        corpus_auditor.md
        topic_tagger.md
        passage_classifier.md
        evidence_builder.md
        contradiction_mapper.md
        dossier_drafter.md
        chronology_synthesizer.md
        fair_use_reviewer.md

site/
    src/
        pages/
            StudiesIndex.tsx         # Studies landing page
            StudyIndex.tsx           # Per-study topic grid
            TopicDetail.tsx          # Topic dossier detail page
        components/
            EvidencePanel.tsx        # Lane-tabbed evidence display
            ContradictionCard.tsx    # Side-by-side contradiction
            LaneFilter.tsx          # Lane filter strip
            TopicChronology.tsx     # Topic timeline display
    public/
        data/
            studies/
                index.json
                ai/
                    index.json
                    topics/
                psychology/
                    index.json
                    topics/
```

### Files to Modify

| File | Change |
|------|--------|
| `database/unified_schema.sql` | Add study tables at end of file |
| `scripts/build_all.py` | Add `run_stage_5()`, add `--studies-only` flag |
| `scripts/export_json.py` | Add `export_studies()` call in `run()` |
| `site/src/App.tsx` | Add study routes |
| `site/src/components/Layout.tsx` | Add "Studies" nav link |
| `site/src/hooks/useData.ts` | No changes needed (already generic) |
| `site/src/App.css` | Add lane badge colors, contradiction card styles |

### build_all.py Extension

```python
def run_stage_5(db: sqlite3.Connection, source: Path):
    """Stage 5: Studies pipeline."""
    print("\n" + "=" * 60)
    print("STAGE 5: RESEARCH STUDIES")
    print("=" * 60)

    from studies.study_pipeline import run as run_studies
    run_studies(db, source)
```

Add `--studies-only` flag to argparse.

### export_json.py Extension

```python
def export_studies(db: sqlite3.Connection, data_dir: Path):
    """Export study data for the Studies viewer."""
    from studies.export_studies import run as export_studies_data
    export_studies_data(db, data_dir)
```

Add `export_studies(db, data_dir)` call in `run()`.

---

## Next Files to Generate

These are the first files to create, in order, with rationale:

### 1. `database/unified_schema.sql` (modify)

**Why first**: All pipeline scripts depend on the schema. Add study tables at the end of the file. Without these tables, no script can write study data. The schema is the contract that every other file depends on.

### 2. `scripts/studies/__init__.py`

**Why second**: Creates the Python package. Empty file but required for imports.

### 3. `scripts/studies/ontology.py`

**Why third**: Seeds the `studies` and `study_topics` tables with the topic definitions from this blueprint. This is the foundation record — every subsequent script queries `study_topics` to know what to scan for. Must be runnable independently (`python scripts/studies/ontology.py`).

### 4. `scripts/studies/lexicons/ai_topics.json` and `scripts/studies/lexicons/psychology_topics.json`

**Why fourth**: The lexicons define what the corpus scanner searches for. They are data files, not code, so they can be authored quickly. The scanner script (next) reads these files.

### 5. `scripts/studies/scan_corpus.py`

**Why fifth**: The deterministic corpus scanner is the most reusable component. It reads the lexicons, scans segments.raw_text and document_texts.text_content, and writes to `study_passages`. This gives the pipeline its raw material — everything Claude-assisted depends on having passages to classify. Modeled on `discovery_pipeline.py`.

### 6. `scripts/studies/export_studies.py`

**Why sixth**: Even before classification or dossier drafting, exporting the scan results to JSON lets you build and test the viewer against real passage data. Stub out the dossier fields as empty strings and test the frontend with passage counts and cross-links only. This enables parallel frontend development.

### 7. `site/src/pages/StudiesIndex.tsx`

**Why seventh**: The simplest viewer page. Reads `studies/index.json` and renders two cards. Getting this working validates the data flow end-to-end: schema → scan → export → viewer.

### 8. `site/src/pages/StudyIndex.tsx`

**Why eighth**: The topic grid. Reads `studies/{studyId}/index.json` and renders topic cards. Validates the per-study index export.

### 9. `site/src/pages/TopicDetail.tsx`

**Why ninth**: The dossier viewer. Initially renders only available data (passage counts, cross-links, empty dossier sections). As the Claude pipeline fills in dossier content, the page progressively shows more. No frontend changes needed when new content arrives — just re-export JSON.

### 10. `scripts/studies/classify_passages.py`

**Why tenth**: The first Claude-assisted script. By this point, the deterministic pipeline and viewer are working end-to-end. Classification adds the interpretive layer that makes the data scholarly rather than merely mechanical.

---

## Summary

This blueprint extends QueryPat with two research studies (AI Topics and Psychology Topics) by:

1. **Adding 7 new database tables** to the existing SQLite schema
2. **Creating 10 new Python scripts** in `scripts/studies/` that follow existing pipeline patterns
3. **Defining 8 Claude Skills** for interpretive analysis tasks
4. **Building 4 new React pages** and 4 new components for the viewer
5. **Extending 3 existing scripts** (build_all, export_json, schema)
6. **Modifying 3 existing frontend files** (App.tsx, Layout.tsx, App.css)

The architecture reuses every relevant existing system (pipeline orchestration, evidence packets, entity linking, lane classification, JSON export, EntityLayout component, search index, bookmarks) and extends them with study-specific parameterization. No existing functionality is replaced or redesigned.
