> **Superseded (2026-10-29).** This study was merged into the database-backed
> dossier **Philip K. Dick and the Bible** (`/studies/intertexts/pkd-and-the-bible`,
> sources in `curation/pkd-bible/`). Its 64 cards were checked against the full
> letters, interviews and novel texts in `unified.sqlite`: 50 were ported there
> with corrected sources and dates (e.g. the rhymed-couplets letter is to Patrice
> Duvic, 28 November 1972, not Roger Zelazny), 10 duplicated passages the dossier
> already had, 3 did not resolve in the corpus (the Davis talk, the Theory, Culture
> & Society quotation, the "Ruah" interview line) and 1 (a Rosicrucian archive
> record restating the VALIS appendix) was dropped as too thin. This directory is kept as the record of that
> work; `build_bible_study.py` now refuses to run without `--force`.

# Curation: The Bible in PKD

Durable source of truth for the `/studies/bible/bible-in-pkd` essay, reached from
the **Bible** tab in the site navigation.

This directory exists so that editorial discoveries do **not** live only in
`site/public/data`. The site JSON is derived from here; a regeneration can rebuild
the page from this directory alone.

| File | What it is |
|---|---|
| `sweep_bible.py` | Searches the corpus for Bible vocabulary. Machine only: it judges nothing. |
| `raw-findings.json` | Output of the sweep. Regenerable, not hand-edited. |
| `dossier_sections.py` | The essay, the mention cards it cites, and the topic metadata. **The thing to edit.** |
| `dossier.json` | Written by the builder. The essay and cards as one data artifact. |

## Rebuilding

```bash
python curation/bible/sweep_bible.py --summary --out curation/bible/raw-findings.json   # add --db <path> if the database is elsewhere
python scripts/studies/build_bible_study.py --check     # validate, write nothing
python scripts/studies/build_bible_study.py            # write the site JSON
python scripts/safeguard/check_data_diff.py --worktree # before committing
```

The builder writes only the `bible` study folder, adds one row each to
`studies/index.json` and `search_index.json`, and writes `dossier.json`. It does
not run any exporter, so nothing already in `site/public/data` is regenerated.

## The essay and its citations

Prose cites a passage with a `{{BIB-…}}` marker, which the site renders as a link
to that mention card. Each card names the sweep finding it is cut from by its
record id, field and a verbatim **anchor**, and quotes the sentence it turns on
as its **pith**. Neither is a line number, so a re-sweep cannot silently move a
card onto the wrong passage.

The builder refuses to publish if:

- a card's anchor or pith is not found in the finding it names;
- a `{{marker}}` in the prose does not resolve to a card;
- a quotation of 40 characters or more is not in the corpus the sweep searched
  (typography is normalised; words are not).

## Relevance codes

| Code | Meaning |
|---|---|
| 1 | **Direct engagement** — Dick quotes, names or argues about a biblical text or book |
| 2 | **Biblical material as a tool** — scripture or a biblical figure used to support another claim, or a fictional scene that dramatises one |

Passing mentions are recorded in `raw-findings.json` and not carded. The sweep
finds about 9,000 hits across 1,104 Exegesis segments and the rest of the corpus;
most are repeated across overlapping windows, or are analytic fields that restate
Dick's own transcription. The cards are a selection, and the selection is editorial.

## Evidentiary register

| Register | Meaning |
|---|---|
| A | What PKD says himself (Exegesis, trilogy text, letters) |
| B | What primary-source evidence establishes (archive facts about a record) |
| C | What scholars argue (archive records of secondary work) |
| D | What portal editors infer (summaries, analysis, the essay's own synthesis) |

Story and novel **summaries** are analysis, not text. They are searched so that
an absence can be stated, and they are never quoted as Dick.

## Corpus coverage, and what it cannot show

| Corpus | What is held | Lane |
|---|---|---|
| Exegesis segments | 1,104 transcribed segments, full `raw_text`. Three malformed JSON files are skipped (`SEG_EXEG_1976-09-15_Dorothy_214`, `SEG_EXEG_1978-10-10_SECTION_016_129`, `SEG_EXEG_1981-04-16_Pat_149`). | A |
| VALIS and The Divine Invasion, chapters | VALIS chapters 1 and 5–13; The Divine Invasion chapters 1–5. Full text, read from the chapter files. | A |
| Letters, excerpts (`letters`) | 75 letters from the 1972–73 excerpt file. `summary` is capped at about 1,500 characters, and some bodies sit in `recipient`. Kept because cards are cut from it. | A |
| Letters, full text (`letters_full`) | 1,175 letters from the Selected Letters volumes, `letters.body_md` in the database. Searched in full. | A |
| Novels, full text (`novel_text`) | Full text from the database, except VALIS and The Divine Invasion, which are searched chapter by chapter. | A (fiction) |
| Short stories, full text (`archive_pdf_text`) | The Collected Stories (vols 1–5) and the Selected Stories, held in the database as archive PDFs. The lane is the one the database records (A). | A (fiction) |
| Interviews, full text (`interview_text`) | Five transcripts. The database records them as lane E, unassigned; this sweep treats them as lane A because the speech is Dick's. **That lane choice is an editorial decision still to be confirmed.** | A |
| Scholarship, full text (`scholarship_text`) | 64 secondary works, full text. Searched, and carded only where a card bears on Dick's own words. | C |
| Archive PDFs (`archive_pdf_text`) | 96 PDFs, lane as recorded in the database (A, B, C or E). The published Exegesis is recorded as lane B and is searched but not carded. | per record |
| Editorial analysis files (`novel_summary`, `story_summary`, ...) | Summaries and analysis, searched so that an absence can be stated. | D |
| Not held as text | The 1974 Vertex interview. | — |

The database corpora are read from `database/unified.sqlite`, which is git-ignored and built by `scripts/build_all.py`. Pass `--db` to point elsewhere. Without the file the sweep still runs on the repository files and prints a NOTE. Characters the database lost in extraction (U+FFFD) are read as apostrophes.

The Exegesis is still the largest body of Dick's own text on the Bible. The letters, interviews and stories are now held as full text, so the earlier notes that called them excerpts or summaries no longer apply to them. The interviews and the full letters are the two corpora whose lane is set by this sweep, not recorded in the database (the database records the interview documents as lane E and gives letters no lane). Both choices need editorial confirmation.

## Dating

Exegesis dates are **batch dates**. Every segment in a transcription folder
inherits one date. The 10 October 1978 folder holds entries that refer to late
1980, and the cards say so. Use the folder date only to order batches, not to
date a single entry.
