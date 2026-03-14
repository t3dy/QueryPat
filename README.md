# QueryPat — Exegesis Knowledge Portal

A unified scholarly browser for Philip K. Dick's *Exegesis*, integrating text analysis, a term dictionary, a PDF archive catalog, biographical event tracking, and entity-linked navigation into a single static site.

**Live site (v2.0):** [t3dy.github.io/QueryPat](https://t3dy.github.io/QueryPat/)
**Previous version (v1.0):** [t3dy.github.io/QueryPat/v1](https://t3dy.github.io/QueryPat/v1/)

---

## What's in the Database

| Domain | Count | Description |
|--------|-------|-------------|
| Exegesis Segments | 1,107 | Chronological text chunks with summaries, key claims, recurring concepts, and theological motifs |
| Dictionary Terms | 310 published (302 accepted) | Theological concepts, philosophical figures, PKD's bespoke vocabulary — with evidence linking and cross-references |
| Biography Events | 646 (448 with location) | Events extracted from autobiographical passages, classified by type and reliability |
| Named Entities | 448 | Characters, places, deities, historical persons from PKD's works and the Exegesis |
| Archive Documents | 228 (246 lane-tagged) | Biographies, interviews, scholarship, novels, letters, newspapers, fan publications |
| Scholars | 105 | PKD scholars across 5 tiers, with interpretive stances and key works |

---

## Site Features

### v1.0 — Database Viewer
- **Timeline** — Browse the *Exegesis* chronologically (1974-1982) with segment summaries
- **Dictionary** — 310 terms with definitions, aliases, linked segments, evidence passages, and related terms
- **Archive** — Searchable catalog sorted by category (biographies, scholarship, interviews, etc.)
- **Biography** — Curated and auto-extracted events with filtering by era, category, and importance
- **Names** — Entity database with etymologies, allusion domains, and linked Exegesis passages
- **Scholars** — Tiered scholar profiles with key works and interpretive stances
- **Search** — Full-text fuzzy search across all entity types with Fuse.js
- **Analytics** — Term frequency charts, segment distribution, and category breakdowns

### v1.x — Knowledge Browser
Eight features transform the viewer into a relational knowledge browser:

1. **Entity Page Template** (`EntityLayout.tsx`) — Shared detail page skeleton with title, badges, tags, bookmark star, content zone, and footer slots
2. **Breadcrumb Navigation** (`Breadcrumbs.tsx`) — Auto-generated from React Router path; collapses to back link on mobile
3. **Grouped Search Results** (`Search.tsx`) — Results grouped by entity type with weighted ranking (titles 3x, categories 2x)
4. **Cross-Site Tag Filtering** (`TagResults.tsx`) — Clicking any tag navigates to a global results page gathering all related content
5. **Explore Further Footer** (`ExploreFooter.tsx`) — Curated cross-references from other sections at the bottom of each detail page
6. **Backlinks Panel** (`BacklinksPanel.tsx`) — "What Links Here" with grouped, expandable backlinks
7. **User Bookmarks** (`useBookmarks.ts`, `Bookmarks.tsx`) — localStorage-backed bookmark system with cross-component sync
8. **Hover Previews** (`HoverPreview.tsx`) — Preview cards on internal links with in-memory cache; hidden on mobile

All features use no new dependencies, add under 3 KB gzipped, and degrade gracefully on mobile.

### v2.0 — Data Enrichment & Cross-Linking

Twenty improvement plans executed against the database and viewer:

**Database enrichments:**
- 252 provisional terms upgraded to accepted status (corpus evidence threshold)
- 248 terms annotated with Exegesis context passages
- 790 term-to-archive document cross-links added
- 735 segments tagged with works_referenced (VALIS in 547, Ubik in 423)
- 297 work-to-document links (VALIS discussed in 23 docs)
- 246 archive documents classified by evidentiary lane (A: Fiction, B: Exegesis, C: Scholarship, D: Synthesis, E: Primary)
- 448 biography events enriched with location data from PKD residence periods
- 38 new named entities added from discovery pipeline
- 18 hedging archive summaries rewritten from extracted text
- Cross-entity connections export (678 KB) linking terms, segments, documents, and names

**Viewer enhancements:**
- Archive cards show evidentiary lane badges (color-coded) and entity counts
- Archive detail pages display People Mentioned, Works Discussed, and Linked Terms sections
- Timeline bio events show location
- Analytics page adds Evidentiary Lanes distribution chart and Data Quality dashboard
- Biography events searchable by location

---

## Architecture

### Data Pipeline

```
Stage 0: CORPUS EXTRACTION
  Pre-extracted PDF text (PyMuPDF) -> document_texts table
  Raw Exegesis chunk files -> segments with raw text

Stage 1: DETERMINISTIC EXTRACTION (14 scripts)
  Manifests -> documents + segments tables
  Chunk summaries -> 12 parsed fields per segment
  Canonical terms -> terms + aliases
  Entity mentions -> term-segment links
  Evidence packets -> structured excerpts
  Archive catalog -> document + asset records
  LLM chat seeds -> 70 expert-curated dictionary entries
  Biography extraction -> events from autobiographical fields
  Names extraction -> from segments and biography narratives

Stage 2: HEURISTIC LINKING (7 scripts)
  Term triage -> status assignment (accepted/provisional/background/rejected)
  Chronology -> first_appearance and peak_usage dates
  Cross-linking -> term-term relationships
  Name-segment linking -> match names to Exegesis passages
  Evidence mapping -> line-range fingerprinting against source text

Stage 3: LLM ENRICHMENT (5 scripts, optional)
  Dictionary descriptions, name etymologies, biography enrichment

Stage 4: EDITORIAL OVERRIDES
  Patch-style JSON overrides for definitions, statuses, notes

Stage 5: CORPUS IMPROVEMENT (v2.0)
  improve_all.py -> 20 automated improvement plans
  Evidentiary lane tagging, term upgrading, cross-linking,
  location filling, summary rewriting, quality scoring

EXPORT & AUDIT
  Route-specific JSON bundles + validation report
```

Run the full pipeline:
```bash
python scripts/build_all.py --fresh
```

Flags: `--deterministic-only`, `--skip-llm`, `--export-only`, `--audit-only`

### PDF Search

A search script queries extracted PDF text from the SQLite database:

```bash
# Search for a term across all archive documents
python scripts/search_pdfs.py --term "VALIS"

# Batch search for multiple terms
python scripts/search_pdfs.py --terms-file scripts/priority_terms.txt --output results.json

# Discover candidate terms not yet in the dictionary
python scripts/search_pdfs.py --discover-terms --min-count 3

# Find date-anchored events in biography PDFs
python scripts/search_pdfs.py --discover-events --category biographies
```

Current extraction coverage: 181 of 228 archive documents have text (79%). Text is truncated to ~6,000 chars per document.

### Canonical Database

SQLite (`database/unified.sqlite`) with schema in `database/unified_schema.sql`. Core tables:

| Table | Purpose |
|-------|---------|
| `documents` | Exegesis sections (246) and archive PDFs (228), with evidentiary lane classification |
| `segments` | 1,107 text chunks with 12 parsed summary fields and works_referenced |
| `terms` | 911 dictionary entries with two-axis triage |
| `term_segments` | Term-to-segment links with confidence levels (1-5) |
| `term_terms` | Term-to-term relationships (related, synonym, parent/child) |
| `evidence_packets` | Structured evidence with excerpts and line-range tracking |
| `biography_events` | 646 events with source, reliability, type, and location |
| `names` | 448 named entities with etymologies, allusion domains, and segment mention counts |
| `document_texts` | Extracted PDF text for archive documents |
| `document_topics` | People, works, and terms linked to archive documents |
| `assets` | File references for source PDFs |

**ID policy:** Stable prefixed IDs (`DOC_EXEG_*`, `SEG_EXEG_*`, `TERM_*`, `EV_*`, `NAME_*`) — slugs are derived separately for URLs.

**Date model:** Multi-field (`date_start`, `date_end`, `date_display`, `date_confidence`, `date_basis`) — supports exact, approximate, and inferred dates.

**Term triage:** Two orthogonal axes — *status* (accepted/provisional/alias/background/rejected) and *review state* (unreviewed/machine-drafted/human-revised/publication-ready).

### JSON Export

Route-specific bundles (not monoliths):

```
site/public/data/
  timeline/index.json, years/{year}.json
  dictionary/index.json, terms/{slug}.json
  archive/index.json, docs/{slug}.json
  biography/index.json, events.json, curated.json
  names/index.json, entities/{slug}.json
  segments/{seg_id}.json
  search_index.json, analytics.json, graph.json, connections.json
```

### Static Site

- **React 19 + TypeScript + Vite** — fast builds, type safety
- **HashRouter** — GitHub Pages compatible (no server-side routing)
- **react-markdown** — renders Markdown descriptions and summaries
- **Fuse.js** — client-side fuzzy search with weighted keys
- **CSS custom properties** — parchment/scholarly color theme
- **No global state library** — bookmarks use localStorage with listener pattern; everything else is local state or URL-derived

---

## PDF Archive

The project integrates a catalog of 228+ PKD-related documents:

| Category | Count | Examples |
|----------|-------|---------|
| Scholarship | 64 | Science Fiction Studies articles, doctoral theses, critical collections |
| Newspaper | 45 | Berkeley Gazette, Point Reyes Light, Oakland Tribune clippings |
| Novels | 35 | First editions, annotated copies, screenplay adaptations |
| Fan Publications | 19 | Niekas, SFC, PKD Otaku, Journey Planet |
| Primary Sources | 16 | Cosmogony and Cosmology, The Android and the Human |
| Short Stories | 15 | Collected Stories volumes, individual publications |
| Letters | 10 | Selected Letters volumes (1938-1982) |
| Biographies | 7 | Sutin, Anne Dick, Rickman, Arnold, Peake, Dufty |
| Interviews | 5 | Last Interview, magazine compilations |
| Other | 12 | Finding aids, research notes, legal documents |

Source PDFs are stored externally (`C:/ExegesisAnalysis/PaulPKDarchive/`). Text extraction uses PyMuPDF, with results imported into the `document_texts` table.

---

## Data Quality

### v2.0 Improvements
- 302 accepted dictionary terms (up from 50 in v1.0), 99% with descriptions, 82.5% with evidence links
- 448 of 646 biography events have location data (69%)
- All 228 archive documents classified by evidentiary lane (100%)
- 735 segments tagged with referenced works
- 790 term-to-document cross-links
- 297 work-to-document links
- Quality scores computed across all content areas

### Known Gaps
- 900 of 1,107 segments lack parsed summaries (manifest-only entries)
- Timeline covers 4 years with Exegesis segments (1975, 1976, 1978, 1981); biography events span full life
- PDF text extraction truncated to ~6,000 chars; 21 documents need OCR
- Graph edge weights are unpopulated

### Audit Outputs
- `AUDIT_REPORT.md` — 14 data integrity issues, 8 viewer bugs, 5 cross-navigation gaps
- `IMPROVEMENT_PLAN.md` — Prioritized content improvement roadmap across 5 channels
- `scripts/pdf_search_findings.md` — PDF search coverage and candidate term discovery results

---

## How It Was Built

This project was built through iterative collaboration between a human researcher and Claude (Anthropic's AI assistant):

1. **Three prior systems merged** — A React chronological viewer (ExegesisAnalysis), a Python dictionary pipeline (ExegesisBrowser), and a PDF archive catalog (PaulPKDarchive) were unified into a single SQLite database with a normalized object model.

2. **Architecture through dialogue** — The data model emerged from extensive back-and-forth: stable prefixed IDs, two-axis term triage, multi-field dates, evidence tiering, and a four-stage build pipeline. The researcher shaped the ID policy, join table design, evidence structure, and export contract.

3. **LLM-assisted curation** — Prior conversations about PKD's philosophical vocabulary yielded 70 seed terms promoted to accepted dictionary status. A PDF search pipeline was built to mine the archive for evidence to improve term descriptions.

4. **Biography extraction** — Autobiographical passages from Exegesis chunk summaries were parsed with regex classifiers to extract 646 events, then 119 curated entries were written to a biographical style guide.

5. **Knowledge browser features** — Eight cross-navigation features (entity layout, breadcrumbs, grouped search, tags, explore footer, backlinks, bookmarks, hover previews) were designed and implemented to transform the viewer into a relational knowledge browser.

6. **v2.0 corpus enrichment** — Twenty automated improvement plans were designed and executed in a single session, mining extracted PDF text to upgrade 252 terms, add evidentiary lanes to all archive documents, fill biography locations, cross-link terms to documents, tag segments with referenced works, and compute quality scores across all content areas.

---

## Development

### Prerequisites

- Python 3.10+
- Node.js 18+
- Source data in `C:/ExegesisAnalysis` (manifests, summaries, evidence packets, archive catalog)

### Build pipeline

```bash
# Full rebuild (drops and recreates database)
python scripts/build_all.py --fresh

# Export only (from existing database)
python scripts/build_all.py --export-only

# Stages 1-2 only, then export
python scripts/build_all.py --skip-llm
```

### Dev server

```bash
cd site
npm install
npm run dev
```

### Production build

```bash
cd site
npm run build
```

Output goes to `site/dist/`, deployed to GitHub Pages via GitHub Actions.

---

## Project Structure

```
QueryPat/
  database/
    unified_schema.sql        # Canonical DDL
    unified.sqlite            # Built database (~9 MB)
    reference_data/           # Biblical, classical, Gnostic, philosophical name CSVs
  scripts/
    build_all.py              # Pipeline orchestrator (4 stages + export)
    export_json.py            # Route-specific JSON export
    improve_all.py            # v2.0: 20 automated improvement plans
    search_pdfs.py            # PDF text search and term discovery
    improve_terms.py          # Dictionary description improvement
    date_norms.py             # Date normalization constants
    check_coverage.py         # PDF extraction coverage report
    ingest/                   # Stage 1: 14 deterministic extraction scripts
    link/                     # Stage 2: 7 heuristic linking scripts
    enrich/                   # Stage 3: 5 LLM enrichment scripts
    discover/                 # Term and event discovery scripts
    overrides/                # Stage 4: editorial patches + seed data
  site/
    src/
      pages/                  # React page components (12 pages)
      components/             # EntityLayout, Breadcrumbs, BookmarkButton, ExploreFooter,
                              # BacklinksPanel, HoverPreview, Layout
      hooks/                  # useData, useBookmarks
      utils/                  # formatTitle
    public/data/              # Exported JSON bundles (~15 MB)
    public/v1/                # Frozen v1.0 site snapshot
    vite.config.ts
  AIPSY_BLUEPRINT.md           # AI & Psychology study implementation blueprint
  v1x.md                      # v1.x changelog (8 features)
  toolcalls.md                 # How tool orchestration works under the hood
  AUDIT_REPORT.md              # Data quality audit
  IMPROVEMENT_PLAN.md          # Content improvement roadmap
  DESIGN_STUDY.md              # UI/UX design study
```

---

## Project Documentation

| File | Purpose |
|------|---------|
| `AIPSY_BLUEPRINT.md` | Implementation blueprint for AI & Psychology topic studies |
| `v1x.md` | Detailed changelog for the v1.x knowledge browser features |
| `toolcalls.md` | How Claude Code orchestrates tool calls during development |
| `AUDIT_REPORT.md` | Comprehensive data quality audit across all entity types |
| `IMPROVEMENT_PLAN.md` | Prioritized content improvement roadmap (5 channels) |
| `DESIGN_STUDY.md` | UI/UX design study for future features (graph view, linked panes, etc.) |

---

## License

Research project. Source data from Philip K. Dick's *Exegesis* is copyrighted material used for scholarly analysis.
