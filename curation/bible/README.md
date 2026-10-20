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
python curation/bible/sweep_bible.py --summary --out curation/bible/raw-findings.json
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
| VALIS | Chapters 1 and 5–13, full text | A |
| The Divine Invasion | Chapters 1–5, full text. Chapters 6–20 are summaries only. | A |
| Selected Letters, 1972–73 | 75 letters, **excerpts**. Each record's `summary` is capped at about 1,500 characters, and in a few records the body sits in the `recipient` field. A letter search is a floor, not a census. | A |
| Stories | 30 stories, **editorial summaries only** | D |
| Novels other than the trilogy | Chapter analyses and summaries | D |
| Interviews | 5 archive records, each with a card and a summary. **No transcript is held**, and no summary mentions the Bible. | — |
| Scholarship | 70 archive records, summaries only | C |

The Exegesis is the largest body of Dick's own text on the Bible. The trilogy
chapters are the only fiction held as full text. The interviews are the largest gap: the absence of Bible references in them is a
finding about the archive, not about Dick.

The `selected_letters_analysis.json` file is also the source of the letter
coverage note in `curation/gnosticism/README.md`. That note describes the letters
as the 1972–73 volume without mentioning the excerpt cap, which is worth knowing
before drawing a conclusion from them.

## Dating

Exegesis dates are **batch dates**. Every segment in a transcription folder
inherits one date. The 10 October 1978 folder holds entries that refer to late
1980, and the cards say so. Use the folder date only to order batches, not to
date a single entry.
