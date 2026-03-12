# QueryPat — Exegesis Knowledge Portal

A unified scholarly browser for Philip K. Dick's *Exegesis*, integrating text analysis, a term dictionary, a PDF archive catalog, and biographical event tracking into a single static site.

**Live site:** [t3dy.github.io/QueryPat](https://t3dy.github.io/QueryPat/)

---

## What This Project Does

QueryPat merges three independent analysis systems into one:

1. **ExegesisAnalysis** — Chunked summaries of the *Exegesis* with entity extraction, key claims, recurring concepts, and theological motifs across 1,107 text segments
2. **ExegesisBrowser** — A dictionary of 911 terms (theological concepts, philosophical figures, PKD's bespoke vocabulary) with evidence packets linking terms to source passages
3. **PaulPKDarchive** — A catalog of 228+ PDFs: biographies, interviews, scholarship, novels, letters, newspaper articles, and fan publications

The unified system provides:

- **Timeline** — Browse the *Exegesis* chronologically (1974–1982), with segment summaries, key claims, and reading excerpts
- **Dictionary** — 310 public terms with definitions, aliases, linked segments, evidence passages, and related terms
- **Archive** — Searchable catalog of PKD-related documents sorted by category (biographies, scholarship, interviews, etc.)
- **Biography** — 646 biographical events extracted from the *Exegesis*, classified by type and reliability
- **Search** — Three-scope full-text search across segments, terms, and archive documents
- **Analytics** — Term frequency charts, segment distribution, and category breakdowns

---

## Architecture

### Data Pipeline

The build pipeline runs in four stages, controlled by CLI flags:

```
Stage 1: DETERMINISTIC EXTRACTION
  Manifests → documents + segments tables
  Chunk summaries → 12 parsed fields per segment
  Canonical terms → terms + aliases
  Entity mentions → term-segment links
  Evidence packets → structured excerpts
  Archive catalog → document + asset records
  LLM chat seeds → 70 expert-curated dictionary entries
  Biography extraction → events from autobiographical fields

Stage 2: HEURISTIC LINKING
  Term triage → status assignment (accepted/provisional/background/rejected)
  Chronology → first_appearance and peak_usage dates
  Cross-linking → term-term relationships from see_also fields

Stage 3: LLM ENRICHMENT (future)
  Dictionary descriptions, summaries, archive term extraction

Stage 4: EDITORIAL OVERRIDES
  Patch-style JSON overrides for term definitions, statuses, notes
```

Run the full pipeline:
```bash
python scripts/build_all.py --fresh
```

Flags: `--deterministic-only`, `--skip-llm`, `--export-only`, `--audit-only`

### Canonical Database

A SQLite database (`database/unified_schema.sql`) serves as the single source of truth. Core tables:

| Table | Purpose |
|-------|---------|
| `documents` | Exegesis sections and archive PDFs |
| `segments` | Text chunks with 12 parsed summary fields |
| `terms` | Dictionary entries with status/review triage |
| `term_segments` | Term-to-segment links with confidence levels |
| `term_terms` | Term-to-term relationships |
| `evidence_packets` | Structured evidence with excerpts |
| `biography_events` | Biographical events with source/reliability tracking |
| `timeline_events` | Dated events from the Exegesis |
| `assets` | File references for PDFs |
| `annotations` | Editorial notes and overrides |

**ID policy:** Stable prefixed IDs (`DOC_EXEG_*`, `SEG_EXEG_*`, `TERM_*`, `EV_*`, etc.) — slugs are derived separately for URLs.

**Date model:** Multi-field (`date_start`, `date_end`, `date_display`, `date_confidence`, `date_basis`) — no single "date" column.

**Term triage:** Two orthogonal axes — *status* (accepted/provisional/alias/background/rejected) and *review state* (unreviewed/machine-drafted/human-revised/publication-ready).

### JSON Export

The export script produces route-specific bundles (not monoliths):

```
site/public/data/
  timeline/index.json, years/{year}.json
  dictionary/index.json, terms/{slug}.json
  archive/index.json, docs/{slug}.json
  biography/index.json, events.json
  segments/{seg_id}.json
  search_index.json, analytics.json, graph.json
```

### Static Site

- **React 19 + TypeScript + Vite** — fast builds, type safety
- **HashRouter** — GitHub Pages compatible (no server-side routing)
- **react-markdown** — renders Markdown descriptions and summaries
- **Fuse.js** — client-side fuzzy search across three scopes
- **CSS variables** — parchment/scholarly color theme

---

## How It Was Built

This project was built through an iterative collaboration between a human researcher and Claude (Anthropic's AI assistant), combining:

1. **Existing analysis work** — The researcher had previously built three separate tools for studying the *Exegesis*: a React-based chronological viewer, a Python entity extraction and dictionary pipeline, and a PDF archive catalog with LLM-generated summaries.

2. **Architecture design** — Through detailed back-and-forth, a unified data model was designed with a canonical SQLite database, normalized object model, term triage system, evidence tiering, and multi-field date handling. The researcher provided extensive feedback shaping the ID policy, join table design, evidence structure, and export contract.

3. **LLM-assisted term curation** — The researcher's prior conversations with Claude about PKD's philosophical vocabulary were used to extract 70 seed terms (historical figures like Plotinus and Meister Eckhart, PKD's bespoke concepts like "Zebra" and "The Empire Never Ended", and philosophical terms like "anamnesis" and "hypostasis") that were promoted to accepted dictionary status.

4. **Biography extraction** — Autobiographical narrative passages from the *Exegesis* chunk summaries were parsed with regex-based classifiers to extract 646 biographical events, categorized by type (vision, marriage, publication, substance use, etc.) with reliability tracking.

5. **PDF archive integration** — A catalog of 228+ PKD-related PDFs was ingested with category classification, extractability scoring, and metadata. Priority documents (biographies by Sutin, Anne Dick, Rickman; interview collections) are flagged for future deep extraction.

---

## Development

### Prerequisites

- Python 3.10+
- Node.js 18+
- Source data in `C:/ExegesisAnalysis` (manifests, summaries, evidence packets, archive catalog)

### Build pipeline

```bash
# Full rebuild
python scripts/build_all.py --fresh

# Export only (from existing database)
python scripts/build_all.py --export-only
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
    unified_schema.sql     # Canonical DDL
  scripts/
    build_all.py           # Pipeline orchestrator
    date_norms.py          # Date normalization constants
    export_json.py         # Route-specific JSON export
    audit.py               # Validation reports
    ingest/                # Stage 1: deterministic extraction
    link/                  # Stage 2: heuristic linking
    overrides/             # Stage 4: editorial patches + seed data
  site/
    src/
      pages/               # React page components
      components/           # Layout, shared components
      hooks/                # useData fetch hook
    public/data/            # Exported JSON bundles
    vite.config.ts
```

---

## License

Research project. Source data from Philip K. Dick's *Exegesis* is copyrighted material used for scholarly analysis.
