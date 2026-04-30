# PKD Knowledge Portal — Artifact Catalog

A complete map of every artifact produced or queued in the current expansion of the QueryPat / Philip K. Dick Knowledge Portal. Organized by *what it is* (data, schema, code, prose, web surface), *where it lives* (DB column, file path, route), *how it gets generated* (deterministic, LLM-assisted, hand-authored, hybrid), and *what state it is in* (shipped, partial, queued).

This document exists because the portal has grown enough domains that a single map of the moving parts is required to operate it. Read it top-to-bottom for orientation; jump to a section to find a specific artifact.

---

## 0. The pipeline at a glance

```
SOURCE MATERIALS (gitignored, off-disk-of-repo)
  C:/ExegesisAnalysis/PaulPKDarchive/     228+ PDFs/EPUBs/DOCXs
  C:/QueryPat/PKD stuff to add/           supplementary drops (xlsx, zip, pdf)
                              │
                              ▼
STAGE A — MARKDOWN INGESTION
  scripts/markdown/{converters/, convert_all.py, add_markdown_columns.py, report.py}
  → database/extracted_markdown/{doc_id}.md     (one .md per archive doc)
  → document_texts.markdown_content              (DB-stored)
  → MARKDOWN_INGEST_REPORT.md                    (status report)
                              │
                              ▼
STAGE B — LETTERS SEGMENTATION
  scripts/letters/segment.py
  → letters table                                (per-letter rows, body_md per letter)
                              │
                              ▼
STAGE C — EVENT EXTRACTION (THE LLM PASS)
  scripts/letters/extract_llm.py    (script-based, needs API key)
  scripts/letters/ingest_handextracted.py  (in-conversation extraction → JSON → DB)
  → letter_events_candidate                       (raw extracted events with provenance)
                              │
                              ▼
STAGE D — DEDUPE + PROMOTION TO BIOGRAPHY
  scripts/letters/ingest.py
  → biography_events (new rows)                   (with theme tags, lane, evidence quote)
                              │
                              ▼
STAGE E — THEOPHANY SEEDING
  scripts/theophanies/seed.py
  → theophanies table (canonical 15 + parent cluster)
  → theophany_evidence linking table
                              │
                              ▼
STAGE F — JSON EXPORT TO STATIC SITE
  scripts/theophanies/export_json.py
  scripts/export_json.py  (existing, regenerates archive/biography/segments/etc)
  → site/public/data/theophanies/{index.json, *.json}
  → site/public/data/essays/{index.json, *.md}
  → site/public/data/biography/* (regenerated)
                              │
                              ▼
STAGE G — STATIC SITE
  site/src/pages/{Theophanies, TheophanyDetail, Essays, EssayDetail, Exegesis, ...}
  site/src/App.tsx                                (HashRouter routing)
  site/src/components/Layout.tsx                  (navigation)
  → GitHub Pages deploy
```

---

## 1. Database — what's in the SQLite file

`database/unified.sqlite` (~99 MB after ingestion) — the canonical store. Every table below is in this one file.

### 1.1 Existing tables (unchanged)

| Table | Records | Notes |
|---|---:|---|
| `documents` | 246 | Exegesis sections (18) + archive PDFs (228) |
| `segments` | 1,107 | Exegesis text chunks with parsed summary fields |
| `terms` | 911 | Dictionary entries |
| `names` | 448→592 | Named entities |
| `biography_events` | 646→growing | Life events |
| `evidence_packets` | 506 | Structured excerpts |
| `term_segments` | 8,125 | Term↔segment links |
| `term_terms` | — | Term↔term relationships |
| `document_topics` | — | Doc↔people/works/terms |
| `assets` | per doc | File-path references |

### 1.2 Tables added in this expansion

| Table | Created by | Purpose |
|---|---|---|
| `document_texts.markdown_content` (column) + 6 sibling cols | `scripts/markdown/add_markdown_columns.py` | Holds the markdown form of each archive doc |
| `letters` | `scripts/letters/segment.py` | One row per individual letter parsed out of a Selected Letters volume |
| `letter_events_candidate` | `scripts/letters/extract_llm.py` and `ingest_handextracted.py` | Raw LLM-extracted events, pre-dedup, with provenance back to letter |
| `letter_events_candidate_runs` | same | Cache table — keys on (letter_id, prompt_version, model) so re-runs skip done work |
| `theophanies` | `scripts/theophanies/seed.py` | Canonical theophany registry |
| `theophany_evidence` | same | Linking table (theophany ↔ exegesis segments / letters / biographies / scholarship) |
| `biography_events.theophany_id` (column) + 6 other cols | `scripts/letters/ingest.py`, `scripts/theophanies/seed.py` | Cross-link bio events to theophanies; carry theme tags, evidence quotes, interpretation lane |

### 1.3 New `biography_events` columns (additive, non-breaking)

```sql
ALTER TABLE biography_events ADD COLUMN source_letter_id TEXT;
ALTER TABLE biography_events ADD COLUMN corroborating_letters TEXT;   -- JSON array
ALTER TABLE biography_events ADD COLUMN evidence_quote TEXT;
ALTER TABLE biography_events ADD COLUMN interpretation_lane TEXT;     -- 'fact' | 'self_report'
ALTER TABLE biography_events ADD COLUMN contradicts_event_id TEXT;
ALTER TABLE biography_events ADD COLUMN themes TEXT;                  -- JSON array, theme controlled vocabulary
ALTER TABLE biography_events ADD COLUMN notable_correspondence TEXT;  -- jaynes|star_wars|fbi_letter|lem_affair|71_break_in|2_3_74|pike|galen|powers|jeter|metz|blade_runner|festschrift|stroke
ALTER TABLE biography_events ADD COLUMN theophany_id TEXT;            -- FK to theophanies
```

### 1.4 New `document_texts` columns

```sql
ALTER TABLE document_texts ADD COLUMN markdown_content TEXT;
ALTER TABLE document_texts ADD COLUMN markdown_method TEXT;       -- pymupdf4llm | ebooklib+markdownify | python-docx | openpyxl | passthrough | bs4+markdownify
ALTER TABLE document_texts ADD COLUMN markdown_status TEXT;       -- pending | complete | failed | skipped_ocr_required | skipped_source_missing | skipped_no_converter
ALTER TABLE document_texts ADD COLUMN markdown_char_count INTEGER;
ALTER TABLE document_texts ADD COLUMN markdown_error TEXT;
ALTER TABLE document_texts ADD COLUMN markdown_updated_at TEXT;
ALTER TABLE document_texts ADD COLUMN markdown_source_hash TEXT;  -- sha256 of source asset for cache invalidation
```

---

## 2. Files on disk — outside the database

### 2.1 Markdown corpus (regenerable, gitignored)

`database/extracted_markdown/` — one `.md` file per converted archive document.

- 180+ files written from the conversion run
- Each file starts with a front-matter block (title, author, doc_id, source path) followed by `---` then the markdown body
- Total size: ~37 MB of markdown across the corpus
- Re-running `convert_all.py` is idempotent (cache hits via `markdown_source_hash`)

### 2.2 Letters bodies (in-database, exported on demand)

The `letters` table stores `body_md` (each letter's text) directly. Currently no on-disk per-letter file — we can add that with a small `export_letters_to_disk.py` if needed.

### 2.3 Static-site JSON bundles

`site/public/data/` — what the React site fetches.

| Bundle | Generated by | Size |
|---|---|---|
| `theophanies/index.json` + 15 `*.json` | `scripts/theophanies/export_json.py` | small (~50 KB) |
| `essays/index.json` + `drugs-in-pkd.md` + `music-in-pkd.md` | hand-authored | ~80 KB |
| `analytics.json` | existing build pipeline | ~200 KB |
| `archive/index.json` + 228 `docs/*.json` | existing build pipeline | ~3 MB |
| `biography/index.json` + `events.json` + `curated.json` | existing build pipeline; needs regen after letter mining | varies |
| `dictionary/`, `names/`, `scholars.json`, `segments/`, `search_index.json` | existing | varies |

### 2.4 Methodology / governance documents (tracked in git)

- [QueryPatOverview.md](QueryPatOverview.md) — end-to-end methodology
- [PKDontology.md](PKDontology.md) — editorial frame, evidentiary lanes A-E
- [PKD_THEOPHANY_ONTOLOGY.md](PKD_THEOPHANY_ONTOLOGY.md) — theophany domain ontology (NEW)
- [CONTENT_PLAN_V3.md](CONTENT_PLAN_V3.md) — writing roadmap
- [HANDOVER.md](HANDOVER.md) — session continuity
- [MARKDOWN_INGEST_PLAN.md](MARKDOWN_INGEST_PLAN.md) — markdown conversion architecture (NEW)
- [LETTERS_MINING_PLAN.md](LETTERS_MINING_PLAN.md) — letter-mining architecture (NEW)
- [WRITIGNAUDIT.md](WRITIGNAUDIT.md) — writing audit on Dashboard/Exegesis prose (NEW)
- [MARKDOWN_INGEST_REPORT.md](MARKDOWN_INGEST_REPORT.md) — interim ingestion report (NEW)
- This file: `PKDARTIFACTS.md`

---

## 3. Scripts — the pipeline code

```
scripts/
├─ build_all.py                    (existing orchestrator, drives stages 1-5 + export)
├─ export_json.py                  (existing JSON exporter)
├─ improve_all.py                  (existing v2.0 improvements)
├─ markdown/                       (NEW, this expansion)
│  ├─ __init__.py
│  ├─ add_markdown_columns.py     idempotent schema migration
│  ├─ convert_all.py              orchestrator with parallel workers
│  ├─ report.py                   writes MARKDOWN_INGEST_REPORT.md
│  └─ converters/
│     ├─ pdf.py                   pymupdf4llm; raises OCRRequired for scanned PDFs
│     ├─ epub.py                  ebooklib + markdownify
│     ├─ docx.py                  python-docx (paragraphs, headings, tables)
│     ├─ xlsx.py                  openpyxl → tabular markdown
│     ├─ text.py                  passthrough with paragraph normalization
│     └─ html.py                  bs4 + markdownify
├─ letters/                       (NEW)
│  ├─ segment.py                  splits volumes into individual letters
│  ├─ extract_llm.py              LLM event extraction (Anthropic SDK)
│  ├─ ingest_handextracted.py     ingest hand-extracted events from JSON
│  ├─ ingest.py                   dedupe + write to biography_events
│  ├─ report.py                   writes LETTERS_MINING_REPORT.md
│  └─ prompts/
│     └─ extract_events.md        the 9-theme extraction prompt
└─ theophanies/                   (NEW)
   ├─ seed.py                     creates table + 15 canonical seeds
   └─ export_json.py              writes theophanies/{index, *}.json
```

### 3.1 Generation modes

Every artifact in this catalog is one of:

- **Deterministic** — same input → same output, no model. Reproducible from source. Caches via content hash.
  - Markdown conversion (`pdf.py`, `epub.py`, etc.)
  - Letter segmentation (`segment.py`)
  - JSON exports
  - Reports

- **LLM-assisted (script)** — model call from a script, results cached by `(input_id, prompt_version, model)`. Re-runs are free after the first.
  - Letter event extraction via `extract_llm.py` (queued; needs API key)
  - The existing v3 scholar-profile and document-summary work

- **LLM-in-conversation** — a model in a chat session reads the source and emits structured output, which is then pickled into the database via a helper.
  - The drugs and music essays (`drugs-in-pkd.md`, `music-in-pkd.md`)
  - The 15 seed theophanies (this conversation, persisted via `seed.py`)
  - The theophany scholar interpretations
  - Biography events extracted from individual letters (queued for in-conversation batches)

- **Hand-authored** — human-written prose stored as markdown; no model in the loop.
  - The methodology and governance documents
  - The `extract_events.md` prompt itself
  - Style-guide templates in `scripts/overrides/templates/`

The portal records *which mode produced each artifact* — `letter_events_candidate_runs.model` carries the model name (or `claude-in-conversation` for in-session work); theophany rows carry their `pkd_interpretations` with source provenance.

---

## 4. Web surface — what users see

### 4.1 Routes

```
/                            Dashboard (rebrand: PKD Portal)
/biography                   Biography events (646+, will grow with letter mining)
/timeline                    Chronological viewer (Exegesis + bio + future publications)
/exegesis                    NEW — Exegesis landing page
/theophanies                 NEW — index of canonical theophanies
/theophanies/:slug           NEW — per-theophany detail with PKD interpretation chain
/archive                     228 archive documents with lane badges
/archive/:slug               Archive document detail
/dictionary                  310 terms
/dictionary/:slug            Term detail
/names                       592 named entities
/names/:slug                 Name detail
/scholars                    119 scholar profiles
/essays                      NEW — index of long-form essays
/essays/:slug                NEW — essay detail (markdown rendered)
/studies                     v4 topic studies
/studies/...                 study detail trees
/search                      Fuzzy search
/bookmarks                   localStorage bookmarks
/tag/:tagname                Cross-site tag aggregator
```

### 4.2 Pages added in this expansion

| Page | File | What it does |
|---|---|---|
| Exegesis landing | `site/src/pages/Exegesis.tsx` | Frames the Exegesis as Lane B; surfaces year breakdown, recurring vocabulary, key scholars |
| Essays index | `site/src/pages/Essays.tsx` | Lists long-form essays with metadata (lanes, sources, word count) |
| Essay detail | `site/src/pages/EssayDetail.tsx` | Markdown renderer with React Router-aware internal links |
| Theophanies index | `site/src/pages/Theophanies.tsx` | Filterable list with experience-type and importance facets |
| Theophany detail | `site/src/pages/TheophanyDetail.tsx` | PKD interpretation chain (timeline of his shifting hypotheses), scholar readings, primary sources, cross-links, contradiction-zone callout |

### 4.3 Pages updated

- `Dashboard.tsx` — rebranded to "Philip K. Dick Knowledge Portal"; six rebalanced stat tiles; "What's inside" includes Theophanies and Essays
- `Layout.tsx` — added Exegesis, Theophanies, Essays nav links; brand changed to "PKD Portal"

---

## 5. Editorial artifacts — the prose

### 5.1 Essays (Lane-aware long-form)

`site/public/data/essays/`

- **drugs-in-pkd.md** (~1,750 words) — Lanes B, C, D, A. Sources: Sutin, Anne Dick, Arnold, Peake, *A Scanner Darkly*, the PSY-passages corpus. Surfaces the Anne Dick / Sutin chronology dispute and the Vancouver / Substance D ambiguity rather than resolving them.
- **music-in-pkd.md** (~1,850 words) — Lanes A, B, C, D. Sources: Kinman's 2,067-reference *Music in PKD* catalog (top composers Beethoven 150, Wagner 122, Bach 93, Dowland 44; top genre Classical 555), the Exegesis Beethoven cluster, the Dowland title of *Flow My Tears*, the Linda Fox / Linda Ronstadt pairing in *Divine Invasion*, Erik Davis on Sonic Youth's *Sister*.

Both essays terminate in a "See also" section with cross-links to dictionary, scholars, archive, companion essay, and an explicit lane-sourcing footer.

### 5.2 Theophany interpretation chains

Each of the 15 seed theophanies carries:

- **PKD interpretation chain** — JSON array of `{date, source, hypothesis_label, interpretation, lane}` items. Earlier readings are *not retracted* by later ones — they coexist and are dated. The same vision can carry 3–6 mutually incompatible PKD readings.
- **Scholar interpretations** — JSON array of `{scholar_slug, interpretation, source_doc_id, lane}`. Sutin (Lane D, biographer), Arnold (Lane C, clinical psychologist), Peake (Lane C, anomalous-cognition researcher), McKee (Lane C, theological), Davis (Lane C, comparative-religious), Kripal (Lane C, religious studies), Lethem and Jackson (Lane C, editorial). Different scholars genuinely disagree; the portal records the disagreement.
- **Primary sources** — JSON array linking back to letters, exegesis segments, novels, interviews.
- **Contradiction-zone callout** — flag if the theophany sits on one of the nine known dispute zones in [PKDontology §4](PKDontology.md).
- **PKD's own doubt** — separate field for the cases where PKD himself acknowledged uncertainty (most theophanies, especially 2-3-74).

### 5.3 Methodology documents (the rules of the system)

- `PKD_THEOPHANY_ONTOLOGY.md` — domain definition, schema, controlled-vocabulary hypothesis labels (~20 of them), the canonical 15-theophany list, display recommendations, and the five enforced editorial rules adapted to the theophany domain.
- `MARKDOWN_INGEST_PLAN.md` — converter selection per source type, idempotency strategy, schema migration, performance estimates.
- `LETTERS_MINING_PLAN.md` — the six pipeline stages, the 9-theme extraction taxonomy, the 14-tag `notable_correspondence` controlled vocabulary (jaynes, star_wars, fbi_letter, lem_affair, 71_break_in, 2_3_74, pike, galen, powers, jeter, metz, blade_runner, festschrift, stroke), schema additions, cost/runtime estimates, risks.
- `WRITIGNAUDIT.md` — writing audit on the Dashboard/Exegesis prose; 9 issues found, all fixed.

---

## 6. Coverage and counts (snapshot, 2026-04-29)

| Domain | Records | Notes |
|---|---:|---|
| Archive documents | 228 | 224 with `document_texts` row |
| Markdown-converted archive docs | ~180 | 9 OCR-required (skipped), 21 source-missing (gitignored at `C:/ExegesisAnalysis/`) |
| Total markdown chars in DB | ~37,000,000 | ~385 KB/doc avg |
| Letters segmented | 510 | from Selected Letters Vol 1 (1938-1971) and Vol 4 (1975-1976); other volumes: TODO |
| Letters with parsed dates | 246 (81% of Vol 4) | OCR-tolerant date parser for `]anuary` etc.; legacy date headings; slash dates |
| Letter event candidates | 0 | LLM extraction step queued (in-conversation batches and/or API-key script) |
| Theophanies (canonical seeds) | 15 + 1 cluster parent | seeded; expansion queued |
| Theophany interpretation entries | ~50 | across the 15 seed records |
| Essays | 2 | drugs, music |
| Scholar profiles | 119 | 37 with rich profiles |
| Dictionary terms | 310 (302 accepted) | unchanged |
| Biography events | 646 | will grow with letter mining |
| Exegesis segments | 1,107 | unchanged; 207 with parsed summaries |

---

## 7. What's queued (clearly outstanding)

### 7.1 Markdown ingestion follow-ups

- **OCR pass** for 21 image-only PDFs (Pamela Jackson 1999 dissertation among them); needs `tesseract` + `ocrmypdf` install.
- **21 source-missing docs**: the asset paths in DB point to files no longer at `C:/ExegesisAnalysis/`. Could be re-acquired or marked permanently missing.
- **Quality grader**: count headings per doc, flag suspiciously thin extractions, surface in the report. Future.
- **Schema export**: `scripts/export_json.py` should add `markdown_excerpt` to per-document JSON so the site can render extracts. Future.

### 7.2 Letter mining follow-ups

- **Convert remaining letters volumes**: Vol 2 (1972–1973), Vol 3 (1974, *missing from archive*), Vol 5 (1977–1979), Vol 6 (1980–1982), and the *Dark-Haired Girl* volume.
- **Re-segment all 6** with the OCR-tolerant date parser (currently only Vol 1 + Vol 4 are segmented).
- **Run event extraction**: either via `extract_llm.py` with `ANTHROPIC_API_KEY` set, or via in-conversation batches feeding `ingest_handextracted.py`.
- **Run dedup + ingest**: `scripts/letters/ingest.py` writes new biography_events with theme tags.
- **Re-export** `biography/index.json` and `events.json` so the Biography page picks up the new entries.

### 7.3 Theophany expansion

- **Seed expansion**: the canonical 15 are seeded; bring up to ~30 by adding minor theophanies (the daily Exegesis "small visions," dream-of-the-monkey, the Mary Wilson January 1981 episode, etc.).
- **Theophany ↔ Exegesis segment linking**: populate `theophany_evidence` rows by querying segments whose `theological_motifs` field matches each theophany's vocabulary.
- **Theophany ↔ biography_event linking**: every existing biography_event tagged "visionary_experience" should resolve to a `theophany_id`.
- **Mining theophanies from interviews**: the Rickman interviews and the Last Testament have additional theophanies (the gematria vision, Abulafia possession) currently captured only at the level of summary; a deeper read would expand the interpretation chains.
- **Editorial pass on the 15 seeds**: scholar interpretations are currently 1–4 per theophany; the templates call for 4–6 per canonical theophany.

### 7.4 Site features

- **Theophany filter on Biography page**: when bio events have `theophany_id`, surface a filter "Show only events tied to a theophany."
- **Theme filter on Biography page**: drugs/music/career/relationships/politics/religion/philosophy/visionary/sf_community.
- **Anchor-scroll on Scholars page**: `/scholars#slug` should scroll and expand the matching scholar; currently anchors are dead (flagged in WRITIGNAUDIT.md).
- **Markdown excerpt on archive detail**: surface the first 1,500 chars of `markdown_content` instead of the legacy `text_content` plain-text dump.
- **Search index**: regenerate `search_index.json` to include theophany names and essay titles.

### 7.5 Data hygiene

- The 228 vs 237 archive-count drift between `analytics.json` and the README — needs `python scripts/build_all.py --export-only` to regenerate.

---

## 8. The five enforced editorial rules (applied throughout)

Every artifact in this catalog follows:

1. **State its lane** — A (fiction), B (Exegesis), C (scholarship), D (synthesis biography), E (primary letter/interview).
2. **Attribute interpretations** — never "PKD really meant X" without saying which letter, segment, or interview.
3. **Surface contradictions** — when the literature disagrees, name the disagreement; when PKD himself disagrees with himself, show the chain.
4. **Cross-link six ways** — every entry links back to terms, events, documents, segments, names, works.
5. **Distinguish fact from self-report** — Lane B is autobiography by an unreliable narrator; treat it as such.

The theophany schema makes rule 5 *first-class* — the entire `pkd_interpretations` chain is the unreliable narrator on the record.

---

## 9. Reproducibility — how to rebuild from scratch

```bash
# 1. Acquire source materials
#    Place archive PDFs at C:/ExegesisAnalysis/PaulPKDarchive/
#    Place supplementary materials at C:/QueryPat/PKD stuff to add/

# 2. Build the unified database (existing pipeline)
python scripts/build_all.py --fresh

# 3. Convert archive to markdown
python scripts/markdown/add_markdown_columns.py --db database/unified.sqlite
python scripts/markdown/convert_all.py --db database/unified.sqlite \
    --source-root C:/ExegesisAnalysis --workers 4
python scripts/markdown/report.py --db database/unified.sqlite

# 4. Segment Selected Letters volumes
python scripts/letters/segment.py --db database/unified.sqlite

# 5. Extract letter events
#    Either:
ANTHROPIC_API_KEY=... python scripts/letters/extract_llm.py --db database/unified.sqlite --workers 4
#    Or feed in-conversation batches via ingest_handextracted.py
python scripts/letters/ingest_handextracted.py --input batch.json --db database/unified.sqlite

# 6. Promote candidates to biography events
python scripts/letters/ingest.py --db database/unified.sqlite

# 7. Seed theophanies
python scripts/theophanies/seed.py --db database/unified.sqlite

# 8. Export site JSON
python scripts/theophanies/export_json.py
python scripts/build_all.py --export-only

# 9. Build site
cd site && npm install && npm run build
```

Every stage is idempotent. Re-running cost is dominated by the LLM stage (which caches per-letter), then by markdown conversion of any newly-added source documents.
