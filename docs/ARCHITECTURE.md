# QueryPat architecture

Current-state map, written from inspection of the live database and scripts on
2026-08-28. Where this document and `database/unified_schema.sql` disagree,
inspect the live database — the `.sql` file has drifted.

## Pipeline

```
SOURCE                PDFs, Exegesis text, letters, scholarship
  │                   (PKD stuff to add/, database/source_pdfs/, exegesis_ordered.txt)
  ▼
INGESTION             scripts/ingest/*  — 14 deterministic extractors
  │                   scripts/link/*    — 7 heuristic linkers
  │                   scripts/enrich/*  — 5 LLM enrichment passes
  │                   scripts/build_all.py orchestrates stages 0–5
  ▼
DATABASE              database/unified.sqlite   ← CANONICAL
  │                   44 tables; see docs/ONTOLOGY.md
  ▼
KNOWLEDGE / ONTOLOGY  terms, names, claims, evidence_packets, study_topics,
  │                   theophanies, biography_events, works
  ▼
EXPORT                scripts/export_json.py → site/public/data/*.json
  │                   ~15 MB of route-shaped bundles
  ▼
SEARCH / RETRIEVAL    site/public/data/search_index.json + Fuse.js in the browser
  │
  ▼
UI                    site/src — React 19 + Vite + HashRouter
```

A parallel track, `artifacts/`, stages LLM-assisted work as typed JSON
artifacts before anything reaches the database. See
`docs/MEMORY_CONSOLIDATION.md`.

## Where the substrate already supports semantic memory

The schema anticipates far more than the data currently realizes. Row counts
from the live database:

| Table | Rows | What it already is |
|---|---:|---|
| `terms` | 911 | Concept memory: definition, interpretive note, visionary significance, scholarly caution, `see_also`, and `*_claim_ids` / `*_generator` columns grounding each prose field |
| `term_aliases` | 25 | Concept aliases |
| `term_terms` | 3,992 | Typed concept graph — vocabulary allows nine relation types |
| `term_segments` | 137,132 | Concept → source-segment index with match type and 1–5 confidence |
| `claims` | 38,411 | Claim memory with lane, confidence, extraction method, review state |
| `claim_subjects` | 98,896 | Claim → entity links with subject/object/attribute/mentioned roles |
| `claim_relations` | 0 | Claim-to-claim graph — supports/contradicts/elaborates/restates/qualifies/sequels |
| `evidence_packets` | 506 | Term-scoped evidence with confidence and editorial status |
| `evidence_excerpts` | 10,047 | Verbatim excerpts bound to segments |
| `study_contradictions` | 25 | Typed contradictions between passages |
| `theophanies` | 15 | Includes `contested_status`, `contradiction_zone`, `pkd_doubt_evidence` |
| `names` | 592 | Entity memory for characters, places, deities, historical people |
| `segments` | 1,107 | Addressable source units |

## Where it does not

Profiling the same tables shows the vocabulary is largely unexercised:

- **`claim_subjects.role` is 100% `mentioned`.** No claim has a populated
  subject/object structure, so the subject–predicate–object triple is nominal.
- **`term_terms.relation_type` is 100% `related`.** Eight other typed relations
  are permitted and none are used. The concept graph is untyped in practice.
- **`claim_relations` is empty.** There is no claim-to-claim contradiction
  graph, despite `contradicts` being in the vocabulary.
- **`claims.review_state` is 100% `unreviewed`**, and lanes are 99.6% `B`.
  Only three of eight `claim_type` values occur.
- **No FTS index exists.** Lexical search is Fuse.js over a 1,243-entry JSON
  file in the browser.
- **`search_index.json` covers 4 of the 8 types the UI can render** — segments,
  terms, names, archive documents. Essays, theophanies, biography events, and
  scholars are declared in `site/src/pages/Search.tsx` but never indexed, so
  those result groups can never appear.

The work of semantic memory is therefore mostly **populating and typing what
already exists**, plus building a retrieval layer that can read it. It is not
a new data model.

## Conflict to resolve (editorial, not technical)

Two incompatible definitions of the evidentiary lanes are committed:

- `artifacts/schemas/controlled_vocabulary.json` — A fiction, B Exegesis,
  C scholarship, **D synthesis (biographies, encyclopedias)**, **E primary
  (letters, interviews, contracts, manuscripts, period press)**.
- `AIPSY_BLUEPRINT.md` — A fiction, B Exegesis *and letters and interviews*,
  C biographical and critical scholarship, **D synthesis (our own output)**,
  no E.

`claims` uses lane E for 136 rows, which only the first vocabulary defines.
`study_passages.lane` is constrained to A/B/C only. This needs a human ruling;
`docs/PROVENANCE.md` records the interim position.

## Frontend

React 19, TypeScript, Vite, HashRouter, `react-markdown`, Fuse.js. No global
state library. Deployed to GitHub Pages via Actions and to Vercel via
`vercel.json`. An optional Supabase-backed community layer adds comments,
contributor profiles, and moderation; it is feature-flagged off when its two
build variables are absent (`site/src/lib/supabase.ts`).
