# Burroughs / word virus: comprehensive corpus sweep and dossier rewrite

- **Date:** 2026-09-04
- **Session:** claude-opus-5, QueryPat
- **Status:** complete

## Research question

What does the QueryPat archive actually contain on Philip K. Dick and William S.
Burroughs? The v1 dossier was built from a single database column and asserted that no
secondary scholarship existed. Is that true, and what else was missed?

## Instruction

User brief of 2026-09-04, items 5–11, preserved at
`archive/2026-09-04/prompts/02-burroughs-comprehensive-sweep.md`. Explicit instruction
not to limit the search to `document_texts.text_content`, and to classify findings
rather than treat every keyword match as relevant.

## Corpus searched

Via `scripts/research/sweep_corpus.py --profile burroughs`:

`segments.raw_text` and six curated segment fields · `document_texts.text_content`
**and** `markdown_content` · `page_texts.page_text` (OCR) · `letters.body_md` ·
`claims.claim_text` / `source_text` · `biography_events` · `works` ·
`pkd_on_pkd_mentions` · `evidence_excerpts` · `annotations` · `theophanies` ·
`timeline_events` · the 183 files of `database/extracted_markdown/` · portal essays.

**The v1 gap:** v1 searched `text_content` only, which is populated for 2 documents.
`markdown_content` is populated for 34. That single omission hid the biography, the
interviews and all the scholarship.

## Queries

25 strong patterns (Burroughs and variants including the OCR corruption `Eurrough`;
titles; Nova Mob / nova police; word/information/language/verbal/thought/mind virus;
cut-up; Gysin) and 16 weak concept patterns (anti-information, jamming, occlusion,
latent message, contamination, parasite, living information, playback, subliminal).
11 exclusion patterns for Edgar Rice Burroughs and known decoys. Full list in
`curation/burroughs-word-virus/raw-findings.json`.

Result: 7,801 raw findings → 637 strong-tier → 310 unique after deduplication across
representations → 66 inventoried, 59 published.

## Discoveries

### Newly found, register A (PKD's own words)

- **Five further Exegesis segments**, none in v1: `016_13`, `016_265`, `016_284`,
  `016_304`, `Pat_44`, `Pat_46`. Two were missed because the source reads `Eurrough's`
  and `Bur¬roughs` (OCR/hyphenation).
- **`016_13` is the most important single find.** In October 1978 — three years before
  the passage everyone reads as the reversal — Dick already writes that the information
  virus is "not an occluding, toxifying 'virus' … it is an antitoxic, de-occlusive",
  and maps the benign version onto four of his own novels.
- **`016_265` is its opposite, in the same section:** "Burroughs is right", there is an
  occluding life form that "enslaves us and kills us".
- **`016_284`:** "This is no information virus; this is blindness." A third position.
- **`Pat_44` and `Pat_46`** keep the occluding virus *in the same April 1981 sitting*
  that states the reversal.
- **One interview, entirely new:** Gregg Rickman, *Philip K. Dick: In His Own Words*.
  Dick classes the word virus as a malign-conspiracy belief and contrasts it with the
  benign conspiracies he and Robert Anton Wilson prefer.
- **"How to Build a Universe That Doesn't Fall Apart Two Days Later" (1978)** contains
  Dick's clearest language-as-control statement — and credits **Orwell**, not Burroughs.

### Newly found, register C (scholarship) — the v1 claim was simply wrong

- **Sutin, *Divine Invasions*.** Identifies the "KW" of the 1976 entries as **K. W.
  Jeter**, who drew the Burroughs parallel; and records that Dick and Jeter performed a
  **cut-up experiment on Moby Dick, Roderick Thorp's *The Detective*, and the Book of
  Acts** — the same Acts material Dick elsewhere claims generated itself in *Flow My
  Tears*. This answers v1's open question about who put the book in front of him.
- **Lapoujade, *Worlds Built to Fall Apart*.** The only sustained scholarly argument:
  Dick and Burroughs as convergent through a shared reading of **Korzybski**, with
  Burroughs's "Word begets image and image is virus" set beside Dick's "How to Build a
  Universe" passage.
- **Butler, *Philip K. Dick*.** Compares the Author's Note of *A Scanner Darkly* to the
  preface of *Junky*.

### Newly confirmed negatives

- **No work of PKD's fiction mentions Burroughs.** Swept every novel, story collection
  and screenplay in the archive. Every apparent hit is ordinary English — "junkie",
  "cut up".
- **No pre-1976 reference exists.** The earliest is 12 January 1976, and it is about a
  Doubleday blurb, not ideas.
- Spinrad, Kripal, TechGnosis, Jameson, Anne R. Dick, the Bergson study and the
  *Essays of the Here and Now* collection mention Burroughs without connecting him to
  Dick. "Nova Mob" in *SF Commentary* is a Melbourne fan group.

## Interpretations

**(D)** The v1 arc — 1976 adoption, 1978 qualification, 1981 reversal — is too clean and
should be retired. Both the 1978 and the 1981 material contain the optimistic and the
pessimistic reading *simultaneously*. The honest shape is a five-year oscillation in
which Dick never gives up Burroughs's vocabulary, including in the sentences that deny
his thesis.

**(D)** The decisive move happens on day one: redefining the virus as *anti*-information,
a block on reception rather than an infection. Everything after 1976 is a consequence.

## Contradictions and alternatives preserved

Four contradiction records on the page, up from three; the two new ones are internal to
single sittings rather than between periods. The v1 reading is preserved in
`archive/2026-09-04/drafts/burroughs-word-virus.v1.173746Z.json`.

## Unresolved questions

Six, recorded on the page. Chief among them: when Dick first read Burroughs (three
sources give three compatible-but-different chronologies); whether the 15 April letter
produced the 16 April entry or recorded it; and whether there is any direct evidence
Dick read Korzybski, on which Lapoujade's argument rests.

## Decisions

- **Registers A/B/C/D marked per section on the public page.** Lapoujade's Korzybski
  claim and Dick's Orwell attribution are both true and are different kinds of claim;
  the page says so rather than merging them.
- **The fiction absence is published as a finding**, not omitted as a null result.
- **Seven negative findings recorded but not published**, so the next researcher does
  not re-derive that "junkie" is ordinary English.
- **The page is now generated from `curation/`**, not from hardcoded Python. This was
  the architectural fix: v1's evidence existed only in a script and in the exported
  JSON.
- **Short quotations only.** The evidence panel carries the passages with citation and
  a link to the source segment; the prose quotes a phrase at a time.

## Files changed

- New: `curation/burroughs-word-virus/{README.md,build_inventory.py,evidence-inventory.json,dossier.json,raw-findings.json}`
- New: `scripts/research/sweep_corpus.py`
- Rewritten: `scripts/studies/seed_burroughs_word_virus.py` (now reads `curation/`)
- Modified: `scripts/studies/export_studies.py`, `site/src/pages/TopicDetail.tsx`,
  `site/src/App.css`, `site/src/components/studies/*`
- Data: `studies/intertexts/`, `dictionary/terms/burroughs.json`,
  `dictionary/index.json`, `search_index.json`, `studies/index.json`

## Validation

- All 59 anchors resolve against the live corpus (`seed --check`).
- 59 passages, 0 bad segment or document references, 0 missing citations, 0 dead
  related-document or related-term links.
- 0 `CLM_*` leaks in public prose.
- 0 other study topics lost prose or relations.
- `npm run build` clean; page renders 11 sections, 4 lanes, 11 packets, 4 contradictions.
- Search finds the material for both "Burroughs" and "word virus".

## Artifacts archived

- `archive/2026-09-04/research/2026-09-04_{exegesis-segment,letters-claims-passages,markdown-corpus}-sweep.txt`
- `archive/2026-09-04/drafts/{burroughs-word-virus,burroughs}.v1.*.json`,
  `seed_burroughs_word_virus.v1.*.py`, each with a note on why it was superseded
- `curation/burroughs-word-virus/raw-findings.json` (10.2 MB, regenerable)
