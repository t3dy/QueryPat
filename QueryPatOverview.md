# QueryPat — Methodology Overview

How the database is built, how the website surfaces it, and what governs the editorial decisions inside both. Companion to [PKDontology.md](PKDontology.md) (the editorial frame), [CONTENT_PLAN_V3.md](CONTENT_PLAN_V3.md) (the writing roadmap), [SITE_DIRECTIONS.md](SITE_DIRECTIONS.md) (the live site-direction addendum), [HANDOVER.md](HANDOVER.md) (current state and queued work), and [README.md](README.md) (project surface).

This document is for someone who needs to understand how QueryPat works end-to-end — the data model, the pipeline, the editorial system, and the rendering layer — without reading the code.

---

## 1. What QueryPat is

QueryPat is a **scholarly knowledge portal about Philip K. Dick** — his life, his fiction, his *Exegesis*, his correspondence, the academic and fan scholarship around him, and the cultural reception of his work. The codename "QueryPat" is the project repository name; the user-facing site is the **Philip K. Dick Knowledge Portal**.

The *Exegesis* is one major source within this larger frame — alongside biography, novels and stories, letters and interviews, scholarly monographs and articles, fan publications, and adaptations. Earlier versions of the site centered the *Exegesis* (the project began as a viewer for that text), but the scope has broadened: the data model already covers the full PKD-as-author surface area, and a current redesign is rebalancing the navigation and dashboard so the *Exegesis* sits as one discrete tab rather than as the project's center of gravity. See [HANDOVER.md](HANDOVER.md) for the active redesign plan.

The codebase integrates three previously separate systems — a chronological text viewer, a term-extraction dictionary pipeline, and a PDF archive catalog — into a single SQLite database, and exposes that database as a static React site deployed via GitHub Pages.

The site answers four standing researcher questions (per [PKDontology §1](PKDontology.md)):

1. What did PKD do, when, and on whose authority?
2. What did PKD mean by *X*?
3. What is the textual evidence for a given claim?
4. What have others said about it, and where do they disagree?

Every methodological choice below is in service of these questions.

---

## 2. Provenance — the three systems merged

QueryPat is a unification of three prior projects:

| Source system | What it contributed |
|---------------|---------------------|
| **ExegesisAnalysis** | A React chronological viewer with chunk-by-chunk LLM-extracted summaries of the *Exegesis* (12 structured fields per segment). |
| **ExegesisBrowser** | A Python pipeline producing a term dictionary with aliases, evidence packets, and segment cross-links from canonical-term lists. |
| **PaulPKDarchive** | A catalog of 228+ PKD-related PDF documents (biographies, scholarship, fan publications, primary sources) with extracted full text. |

The unification was not a copy — the data was re-modeled into a normalized object graph with stable IDs, two-axis term triage, multi-field dates, and an evidence-tiering scheme. The three input systems contribute *records*, not schema; the schema is QueryPat's.

---

## 3. Data model

The canonical store is `database/unified.sqlite`, defined by `database/unified_schema.sql`. Eleven core tables.

### 3.1 Core entity tables

| Table | Records | Purpose |
|-------|---------|---------|
| `documents` | ~474 | Exegesis sections (246) + archive PDFs (228) with evidentiary lane classification |
| `segments` | 1,107 | *Exegesis* text chunks with parsed summary fields and works-referenced links |
| `terms` | 911 | Dictionary entries — historical figures, theological concepts, PKD bespoke vocabulary |
| `names` | 448 | Named entities — characters, places, deities, historical persons |
| `biography_events` | 646 | Life events (curated 119 + auto-extracted) with reliability and source |
| `assets` | per doc | File references for source PDFs |

### 3.2 Join and evidence tables

| Table | Purpose |
|-------|---------|
| `term_segments` | Term-to-segment links (confidence levels 1–5) — ~8,125 rows |
| `term_terms` | Term-to-term relationships: related, synonym, parent, child |
| `evidence_packets` | Structured excerpts with line-range fingerprinting against source text |
| `document_topics` | People, works, and terms linked to archive documents |
| `document_texts` | Extracted full PDF text for archive documents (when available) |

### 3.3 Identity and date conventions

**Stable prefixed IDs.** Every entity has a stable string ID with a domain prefix:

- `DOC_EXEG_*` for *Exegesis* sections
- `DOC_ARCH_*` for archive PDFs
- `SEG_EXEG_*` for *Exegesis* segments
- `TERM_*` for dictionary terms
- `EV_*` for evidence packets
- `NAME_*` for named entities

URL slugs are derived separately and are not the IDs — slugs can change for readability without breaking references. The ID-vs-slug separation is the central durability decision in the schema.

**Multi-field dates.** Dates have five fields rather than one: `date_start`, `date_end`, `date_display`, `date_confidence`, `date_basis`. This supports exact dates ("1974-03-20"), partial dates ("1962", "spring 1974"), inferred dates from textual cues, and ranges ("c. 1975–1976"). The display field is human-authored; the start/end fields are machine-comparable.

**Term triage on two axes.** Every term has both a `status` (`accepted` / `provisional` / `alias` / `background` / `rejected`) and a `review_state` (`unreviewed` / `machine-drafted` / `human-revised` / `publication-ready`). The two are orthogonal: an accepted term can be unreviewed, and a rejected term can be human-revised. This separation lets editorial and lexical judgments be tracked independently.

### 3.4 The evidentiary lanes

Per [PKDontology §3](PKDontology.md), every claim is sourced to a lane. The lanes live on the `documents.evidentiary_lane` column:

| Lane | Source class | What it can settle |
|------|--------------|---------------------|
| **A** | Fiction (novels, stories) | What PKD wrote in the works |
| **B** | Exegesis | What PKD theorized about himself |
| **C** | Scholarship (academic) | What trained readers have argued |
| **D** | Synthesis (biographies, encyclopedias) | Consensus narrative |
| **E** | Primary (letters, interviews, manuscripts) | What PKD said and signed at a given moment |

A claim's lane must be visible in the entry. This is the structural way the database refuses to flatten distinctions between "what the work says," "what PKD said about himself," "what scholars argued," and "what the documentary record shows."

---

## 4. The build pipeline

Source data lives in `C:/ExegesisAnalysis/` (manifests, summaries, evidence packets, archive catalog). The pipeline runs in five stages, orchestrated by `scripts/build_all.py`.

### Stage 0 — Corpus extraction (one-time)
Pre-extracted PDF text from PyMuPDF feeds the `document_texts` table. Raw *Exegesis* chunk files feed segment raw text. This stage runs out-of-band and produces `document_texts` ready for ingest.

### Stage 1 — Deterministic extraction (14 scripts in `scripts/ingest/`)
- Manifests → `documents` and `segments` tables
- Chunk summaries → 12 parsed fields per segment (concise_summary, key_claims, recurring_concepts, people_entities, theological_motifs, etc.)
- Canonical terms → `terms` and aliases
- Entity mentions → term-segment links
- Evidence packets → structured excerpts
- Archive catalog → document and asset records
- LLM chat seeds → 70 expert-curated dictionary entries (from prior conversations)
- Biography extraction → events from autobiographical fields
- Names extraction → from segments and biography narratives

This stage is purely deterministic — given the same input it produces the same output. Re-runs are idempotent.

### Stage 2 — Heuristic linking (7 scripts in `scripts/link/`)
- Term triage → status assignment (accepted / provisional / background / rejected)
- Chronology → first_appearance and peak_usage dates per term
- Cross-linking → term-term relationships
- Name-segment linking → match named entities to *Exegesis* passages
- Evidence mapping → line-range fingerprinting against source text

Heuristic, not deterministic — uses thresholds, rule chains, and approximate matching. Outputs are recorded with confidence levels.

### Stage 3 — LLM enrichment (5 scripts in `scripts/enrich/`, optional)
- Dictionary descriptions
- Name etymologies
- Biography enrichment

Cached by `input_hash + prompt_version + model_name`. Editorial overrides (Stage 4) take precedence over LLM output. Every LLM-generated record starts at `review_state = machine-drafted`.

### Stage 4 — Editorial overrides (`scripts/overrides/`)
Patch-style JSON overrides for definitions, statuses, notes, and term seeds. Human edits can pin a value against the next pipeline run. Overrides are how a human reviewer's revisions persist across rebuilds.

### Stage 5 — Corpus improvement (`scripts/improve_all.py`, v2.0)
Twenty automated improvement plans run against the post-Stage-4 database:
- Evidentiary lane tagging (all 246 archive documents)
- Term upgrading (provisional → accepted by corpus evidence)
- Cross-linking (term-to-document, term-to-term, work-to-document)
- Location filling (biography events → residence periods)
- Summary rewriting (extracted text → human-readable summaries)
- Quality scoring across all content areas

### Export & audit
`scripts/export_json.py` writes route-specific JSON bundles to `site/public/data/`. `scripts/audit.py` produces `AUDIT_REPORT.md` with data integrity checks, viewer bug reports, and cross-navigation gaps.

```bash
# Full rebuild (drops and recreates database)
python scripts/build_all.py --fresh

# Export only (from existing database)
python scripts/build_all.py --export-only

# Stages 1–2 only, then export
python scripts/build_all.py --skip-llm
```

---

## 5. Editorial methodology

The pipeline produces *records*. The editorial system produces *prose*. Both are part of the methodology.

### 5.1 The ontology — what we record
[PKDontology.md](PKDontology.md) defines ten core domains (biography events, works, visions, people, places, themes, vocabulary, influences, adaptations, documents) and a list of nine known dispute zones that always require contradiction-surfacing rather than silent adjudication (the November 1971 break-in, the 2-3-74 events, drug-use chronology, Vancouver, Anne Dick marriage breakdown, Exegesis composition order, Bishop Pike, agoraphobia onset, Lem / "committee" claims).

### 5.2 The plan — what we write next
[CONTENT_PLAN_V3.md](CONTENT_PLAN_V3.md) succeeds the v2.0 [IMPROVEMENT_PLAN.md](IMPROVEMENT_PLAN.md) and governs prose density: scholar profile expansion, document summary rewriting, dictionary entry deepening, biography event extraction, theme and vision entity creation. v3 prioritizes writing quality and scholarly density over structural population.

### 5.3 The templates — how we write
[scripts/overrides/templates/](scripts/overrides/templates/) holds ten editorial templates, one per content type. Each template encodes:
- A required structure (sections, with target lengths)
- A tone rule (verbs over adjectives; attribute interpretations; surface contradictions)
- A non-negotiables list (cross-references, lane tagging, fact-vs-interpretation discipline)
- A lint checklist enforceable in CI

| Template | Use |
|----------|-----|
| `template_doc_scholarship.md` | Academic articles, dissertations, monographs |
| `template_doc_biography.md` | Full biographies, memoirs, psychobiographies |
| `template_doc_interview.md` | Interviews and compilations |
| `template_doc_primary.md` | PKD's own works (fiction and nonfiction) |
| `template_doc_fan.md` | Fanzines and fan-press monographs |
| `template_doc_newspaper.md` | Newspaper clippings |
| `template_doc_finding_aid.md` | Archives and special collections |
| `template_scholar.md` | Scholar profile entries |
| `template_dictionary.md` | Dictionary term entries |
| `template_biography_event.md` | Biography events |

### 5.4 The five enforced rules (per [CONTENT_PLAN_V3 §2](CONTENT_PLAN_V3.md))

Every entry, regardless of type:

1. **State its lane.** A scholar profile is C; a biography summary is D; an interview citation is E.
2. **Attribute interpretations.** No claim that PKD "really" meant something — always whose reading.
3. **Surface contradictions.** When the literature disagrees, name the disagreement.
4. **Cross-link six ways.** Terms, events, documents, segments, names, works.
5. **Distinguish fact from self-report.** Lane B (*Exegesis*) is autobiography by an unreliable narrator; treat it as such.

These are non-negotiable. The templates build them in by structure.

---

## 6. JSON export contract

The build pipeline writes route-specific JSON bundles, not monoliths. The site fetches only what the current route needs:

```
site/public/data/
  timeline/
    index.json               # year aggregates
    years/{year}.json        # one file per year
  dictionary/
    index.json               # term aggregates
    terms/{slug}.json        # one file per term
  archive/
    index.json               # document aggregates
    docs/{slug}.json         # one file per document
  biography/
    index.json
    events.json
    curated.json             # 119 hand-written events
  names/
    index.json
    entities/{slug}.json
  segments/{seg_id}.json
  scholars.json              # full scholar list (115 entries)
  search_index.json          # Fuse.js index
  analytics.json             # chart data
  graph.json                 # entity-relation graph
  connections.json           # cross-entity links (~678 KB)
```

Per-entity JSON (rather than monolithic) keeps individual page loads cheap and lets the static-site host (GitHub Pages) cache aggressively.

---

## 7. The static site

`site/` is a React 19 + TypeScript + Vite application. It deploys to GitHub Pages via GitHub Actions on push to `main`.

### 7.1 Architecture decisions

- **HashRouter, not BrowserRouter.** GitHub Pages does not support server-side routing rewrites; HashRouter sidesteps this without infrastructure cost.
- **No global state library.** Bookmarks use `localStorage` with a listener pattern; everything else is local component state or URL-derived. The schema decision (per-route JSON bundles) makes this tractable.
- **Markdown rendering with `react-markdown`.** Dictionary descriptions and document summaries are stored as Markdown; the renderer handles them uniformly.
- **Fuse.js for fuzzy search.** Client-side, weighted keys (titles 3×, categories 2×). Static index loaded once.
- **CSS custom properties for theming.** Parchment / scholarly palette; no CSS-in-JS framework.
- **No new dependencies for v1.x knowledge-browser features.** Each cross-navigation feature stayed under 3 KB gzipped.

### 7.2 Pages (12, in `site/src/pages/`)

| Page | What it is |
|------|------------|
| **Dashboard** | Entry point — counts, key concepts by frequency, browse-by-year |
| **Timeline** | Chronological *Exegesis* segments (1974–1982), with biography events overlaid |
| **Dictionary** | 310 published terms with definitions, aliases, evidence, related terms |
| **Archive** | 228 documents with category, evidentiary lane, and entity counts |
| **ArchiveDetail** | Per-document summary + linked terms, works, people |
| **Biography** | Curated and auto-extracted events with era / category / importance filters |
| **Names** | 448 named entities with etymologies and segment counts |
| **NameDetail** | Per-entity description, allusion domain, mentions |
| **Scholars** | 115 scholar profiles, tiered, with new fields (key_arguments, scholarly_lineage, disputes) |
| **Search** | Fuzzy search grouped by entity type, weighted ranking |
| **TagResults** | Cross-site tag aggregator — every clickable tag yields a results page |
| **Analytics** | Term frequency charts, segment distribution, lane breakdowns, data quality dashboard |
| **Bookmarks** | localStorage-backed bookmarks with cross-component sync |
| **SegmentDetail** | Per-segment full summary with all 12 parsed fields |
| **TermDetail** | Per-term full description with linked segments and related terms |

### 7.3 Cross-navigation features (v1.x — eight features)

The v1.x release transformed the database viewer into a relational knowledge browser. Each feature was implemented as a shared component and used everywhere relevant:

1. **EntityLayout** (`components/EntityLayout.tsx`) — a shared detail-page skeleton: title, badges, tags, bookmark star, content zone, footer slots. Every detail page uses it.
2. **Breadcrumbs** (`components/Breadcrumbs.tsx`) — auto-generated from React Router path; collapses to a back link on mobile.
3. **Grouped Search Results** (`pages/Search.tsx`) — results bucketed by entity type with weighted ranking.
4. **Cross-Site Tag Filtering** (`pages/TagResults.tsx`) — every tag is a link to a global results page.
5. **Explore Further Footer** (`components/ExploreFooter.tsx`) — curated cross-references at the bottom of each detail page.
6. **Backlinks Panel** (`components/BacklinksPanel.tsx`) — "What Links Here," grouped and expandable.
7. **User Bookmarks** (`hooks/useBookmarks.ts`, `pages/Bookmarks.tsx`) — localStorage-backed with cross-component sync.
8. **Hover Previews** (`components/HoverPreview.tsx`) — preview cards on internal links with in-memory cache; hidden on mobile.

All eight features added under 3 KB gzipped total and degrade gracefully on mobile.

### 7.4 v2.0 corpus enrichment surface

v2.0's database changes manifested in the viewer as:

- Archive cards show evidentiary lane badges (color-coded) and entity counts
- Archive detail pages show People Mentioned, Works Discussed, and Linked Terms sections
- Timeline biography events show location
- Analytics adds the Evidentiary Lanes distribution chart and a Data Quality dashboard
- Biography events are searchable by location

### 7.5 v2.1 (current) — Names and PKD fiction characters

191 PKD fiction characters were added with etymology, wordplay, and cross-links. The Names page now distinguishes real-world referents (Plato, Mani, Eckhart) from fictional characters (Manfred Steiner, Joe Chip, Glen Runciter), each with their own etymological treatment.

### 7.6 v3 (in progress, per [CONTENT_PLAN_V3.md](CONTENT_PLAN_V3.md))

The active phase. Templates committed; ~36 scholar profiles rewritten with the new fields (`key_arguments`, `scholarly_lineage`, `disputes`, `quotable_lines`); 5 Tier-1 biography document summaries fully rewritten per the scholarship template (Robinson's monograph, Sutin's *Divine Invasions*, Anne Dick's *Search*, Arnold's *Divine Madness*, Peake's *A Life of PKD*); 10 missing scholars added from web research; the Scholars.tsx page extended to render the new fields.

---

## 8. How AI assists curation (and where it doesn't)

Three places where LLMs work in the pipeline:

1. **Stage 1 (deterministic) — chunk summaries.** The original *Exegesis* segments were summarized by an LLM into 12 structured fields. Output is treated as primary data; subsequent stages parse it.
2. **Stage 3 (optional) — enrichment.** Dictionary descriptions, name etymologies, and biography enrichment can be LLM-assisted with caching by `input_hash + prompt_version + model_name`. All output starts at `review_state = machine-drafted` and is subject to Stage 4 override.
3. **v3 editorial drafting (current).** Scholar profiles, document summaries, and template authorship are drafted with LLM assistance against the templates in `scripts/overrides/templates/`. Output is tagged in `review_state` and reviewed by the human researcher before publication.

Three places where LLMs do *not* work:

1. **Term triage (Stage 2).** Status assignment is heuristic-rule-based, not LLM-judgment-based. The decision rules are auditable and reproducible.
2. **Editorial override (Stage 4).** Human edits pin values against pipeline regeneration. There is no automatic "improvement" of human-revised content.
3. **The ontology and content plan.** [PKDontology.md](PKDontology.md) and [CONTENT_PLAN_V3.md](CONTENT_PLAN_V3.md) are human-authored editorial governance documents, not LLM-generated.

The methodological commitment is that *the rules are human, the records can be machine-assisted, and the prose is in mixed authorship under explicit attribution.*

---

## 9. Data quality and audit

Three audit outputs travel with the database:

| Output | Contents |
|--------|----------|
| `AUDIT_REPORT.md` | Data integrity issues (14), viewer bugs (8), cross-navigation gaps (5) |
| `IMPROVEMENT_PLAN.md` | v2.0 prioritized roadmap across five content channels |
| `scripts/pdf_search_findings.md` | PDF extraction coverage, candidate term discovery results |

Quality scoring is computed across all content areas at the end of Stage 5 and surfaced on the Analytics page's Data Quality dashboard.

### 9.1 Known gaps (current)

- 900 of 1,107 segments lack parsed summaries (manifest-only entries without corresponding chunk analysis)
- *Exegesis* segments span four years (1975, 1976, 1978, 1981); biography events span the full life
- PDF text extraction truncated to ~6,000 chars per document; 21 documents need OCR (including the Pamela Jackson 1999 dissertation, which is image-only)
- Graph edge weights unpopulated
- 76 of 115 scholars still have empty or thin `interpretive_stance` fields awaiting v3 expansion

---

## 10. The methodology in one sentence

QueryPat treats Philip K. Dick studies as a contested archive: it records claims with their evidentiary lane, attributes interpretations to whoever holds them, surfaces contradictions where the literature diverges, and cross-links every entry six ways so a researcher can move from "what did Sutin say happened" to "what does Anne Dick contest" to "what *Exegesis* segments touch this" to "what dictionary terms is it indexed under" without leaving the site or losing the chain of attribution.

---

## 11. Where to read more

| For | Read |
|-----|------|
| The editorial frame | [PKDontology.md](PKDontology.md) |
| The current writing plan | [CONTENT_PLAN_V3.md](CONTENT_PLAN_V3.md) |
| The previous (executed) plan | [IMPROVEMENT_PLAN.md](IMPROVEMENT_PLAN.md) |
| The style-guide templates | [scripts/overrides/templates/](scripts/overrides/templates/) |
| The audit | [AUDIT_REPORT.md](AUDIT_REPORT.md) |
| The v1.x knowledge-browser features | [v1x.md](v1x.md) |
| The UI/UX design study | [DESIGN_STUDY.md](DESIGN_STUDY.md) |
| The discovery pipeline | [DISCOVERY_PIPELINE.md](DISCOVERY_PIPELINE.md) |
| The AIPSY topic study | [AIPSY_BLUEPRINT.md](AIPSY_BLUEPRINT.md) |
| Project surface | [README.md](README.md) |
