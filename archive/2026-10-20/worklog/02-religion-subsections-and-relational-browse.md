# Religion in PKD: subsections, a relational database, and browsing

- **Date:** 2026-10-20
- **Status:** complete for the sources held here; the PDF archive is not held

## Research question

Can every mention of each religious tradition in Dick's work be found, tagged by
subsection, and browsed relationally with its metadata? And, where the PDF
archive is not held, can the software be built now and run later?

## Instruction

See `prompts/02-religion-subsections.md`.

## Corpus searched

Exegesis segments (1,104; raw text and analytic fields), VALIS chapters 1 and 5–13,
Divine Invasion chapters 1–5 (full text), the 1972–73 Selected Letters (excerpts),
editorial analysis files, 247 archive records and the portal essays. The staged
PDF text: one document, `Maze notes.pdf`, unassigned.

Not searched: the PDF archive (not in the repository), interview transcripts (not
held), story texts (not held), trilogy chapters other than those above (summaries
only), and letters after 1973 (not held as text).

## Method

- Fourteen traditions and 34 subsections, in `curation/religion/taxonomy.py`. Each
  subsection has strong terms, weak terms, and exclusion patterns.
- A finding is one hit, tagged with every subsection whose pattern matches the
  matched span. Ids are hashes of corpus, record, field, offset and match.
- Lanes: Exegesis raw text and VALIS / DI full text are lane A; letters are lane A
  excerpts; archive scholarship is lane C; editorial analysis and the Exegesis
  analytic fields are lane D and stay in the database.

## Results

43,258 findings in total. Lane A and C findings (16,306 subsection rows) are
browsable on the site. Lane D (26,952) is in the database only.

Subsection counts are highest where the terms are everyday: Christ and Jesus
(3,691 in A and C), Logos, Sophia, anamnesis and Plato. Terms that are also
ordinary words are weak: `Elias`, `Paul`, `Wisdom`, `Law`, `Tao` in some contexts.
The weak tier is flagged on every finding and filterable on the site.

Mercer: 26 findings for the figure and 314 for Mercerism as religion, most of the
latter via the phrase "fusion" and should be read before being counted.

## Decisions

- **Lane D is not browsed.** The Exegesis analytic fields restate Dick's text in
  the portal's words. Showing them as findings would present paraphrase as evidence.
- **The religion study is now registered.** Its previous topic, "Religion in PKD's
  Fiction", is kept and its file untouched. The study's label and description are
  kept as they were: the data-loss guard refused a shortened label, and renaming the
  study is an editor's decision. The label therefore understates the study, which now
  covers the Exegesis and the criticism too; an editor should rename it.
- **Relevance uses the Burroughs codes**, so the religion and Burroughs studies can be
  compared directly.
- **Derived files are git-ignored**: `raw-findings.json` (36 MB) and
  `religion.sqlite`. They rebuild from committed inputs. `editorial.json` is committed.
- **PDFs are staged, not classified.** A document without an assigned lane is lane D
  and marked unassigned. `Maze notes.pdf` reads like Dick's own notes; its lane is
  left for someone to confirm.
- **Tesseract is absent here**, so image-only pages would be recorded as needing OCR.
  None were found: the one PDF has a full text layer.

## Software

- `curation/religion/taxonomy.py`: topics, subsections and patterns.
- `scripts/research/sweep_religion.py`: sweep, with per-subsection tags.
- `scripts/research/build_religion_db.py`: relational database, with FTS5.
- `scripts/research/religion_review.py`: review workflow; decisions to `editorial.json`.
- `scripts/research/ingest_pdfs.py`: stages archive PDFs, OCRs image-only pages where
  tesseract is installed, and records them in `pdf-manifest.json`.
- `scripts/studies/build_religion_study.py`: exports the site JSON from the database.
- `site/src/pages/ReligionBrowse.tsx`: browse page, with filters that are linkable URLs.
- `site/src/pages/TopicDetail.tsx`: subsection list on each topic page.

## Validation

- Pattern compilation: all taxonomy patterns compile; every `related` topic resolves.
- Sweep: 43,258 findings; per-subsection counts in the sweep summary.
- Database: `PRAGMA`-level counts match the sweep; FTS5 search for "Mercer" returns
  its hits; the three SQL examples in the README run.
- Review: a test decision was recorded and read back, then deleted so no review is
  committed as if it were real.
- Ingest: `Maze notes.pdf` staged as 16 pages, 26,427 characters, lane D unassigned.
- `npm run build --prefix site` passes. The browse page loads `sophia` with 1,001
  findings in 40-row pages; the topic page lists its subsections; no console errors
  apart from the existing `/vite.svg` favicon 404.

## Unresolved

- Every finding is unreviewed. The browse page shows the sweep's output, not a
  judgement, and says so.
- Interview transcripts, story texts, the full letters and the PDF archive are needed
  before the study can say what Dick said in those sources.
- Interpretive prose for most traditions is not written. Each topic page says so.
