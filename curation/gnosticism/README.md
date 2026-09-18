# Curation: Gnosticism

Durable source of truth for the `/studies/gnosticism` dossier and the
`/studies/gnosticism/lexicon` register.

This directory exists so that editorial discoveries do **not** live only in
`site/public/data`. The database and the exported JSON are both derived from
here; a regeneration can rebuild every page from this directory alone.

| File | What it is |
|---|---|
| `lexicon.json` | The register of 111 Gnostic terms, teachers, texts, traditions and modern scholars. Hand-authored, emitted from `scripts/research/gnostic_lexicon_source.py`. |
| `raw-findings.json` | Machine output of the corpus sweep. Regenerable, not hand-edited. |
| `register.json` | `lexicon.json` joined to its attestations: counts, chronology, exemplar passages. |
| `dossier_sections.py` | The editorial prose, topic by topic. Hand-authored; the thing to edit. |
| `dossier.json` | The assembled artifact the seeder writes into the database. |

## Rebuilding

The four steps run in order. Each reads only the step before it, so any of them
can be re-run alone after an edit.

```bash
python scripts/research/gnostic_lexicon_source.py    # 1. lexicon.json
python scripts/research/sweep_gnosticism.py --summary # 2. raw-findings.json
python scripts/research/build_gnostic_register.py    # 3. register.json
python scripts/studies/build_gnosticism_study.py     # 4. dossier.json + site JSON
```

Step 4 writes `site/public/data/studies/gnosticism/` and adds the study to
`studies/index.json` and `search_index.json` directly, and is idempotent — it
removes its own previous rows before writing. It does **not** touch any other
study's files. Verify before committing:

```bash
python scripts/safeguard/check_data_diff.py --worktree
```

To write the study into a built database instead (which is what a full rebuild
does, via `build_all.py` stage 5):

```bash
python scripts/studies/seed_gnosticism.py
python scripts/safeguard/safe_export.py --exporter studies
```

## Corpus coverage

The sweep searched:

| Corpus | Sources | Lane | Note |
|---|---|---|---|
| Exegesis segments | 1,104 | B | `raw_text` (Dick's words) plus twelve curated analytical fields, tracked separately |
| Selected Letters | 75 | B | **1972-73 only** — see the gap below |
| VALIS trilogy | 21 files | A | VALIS ch. 1, 5-13 and *The Divine Invasion* ch. 1-5 as full text; the rest as summaries |
| Archive scholarship | 241 | C | Titles and summaries; full text lives in the database |

The Exegesis coverage is complete: the 1,104 segments hold 9,264,014 characters
against 9,156,433 in `exegesis_ordered.txt`. An entry marked **unattested** was
therefore genuinely not written by Dick anywhere in the Exegesis as transcribed,
which is a finding rather than a gap.

### Known gaps

- **The letters lane is 1972-73 only**, which predates 2-3-74 entirely. The
  Selected Letters volumes for 1975-76, 1977-79 and 1980-82 are catalogued in
  the archive at full ingest level but their text lives in the database, not in
  the exported JSON. `sweep_gnosticism.py` takes `--db` and will sweep them
  whenever a built database is present. Until then, no statement about the
  correspondence in this study covers the years that matter.
- **Three segment files are malformed JSON** and are skipped by the sweep:
  `SEG_EXEG_1976-09-15_Dorothy_214`, `SEG_EXEG_1978-10-10_SECTION_016_129`,
  `SEG_EXEG_1981-04-16_Pat_149`. Pre-existing fault; the counts are three
  segments short.
- **The Transmigration of Timothy Archer** is held only as chapter summaries.

## Evidence states

Independently of category, each register entry carries the state of its
evidence.

| State | Meaning |
|---|---|
| `attested` | Dick uses the word himself, in the Exegesis, the letters or the fiction |
| `annotation_only` | The word occurs only in portal-editor analytical fields, never in his text |
| `unattested` | The word occurs nowhere in the corpus swept |

Unattested entries are kept, not dropped. "Dick never reached for this word" is
a finding about Dick, and this register is the only place it is recorded — the
same principle as the Burroughs inventory's relevance-4 and -5 findings.

## Evidentiary register

Per `docs/RESEARCH_WORKLOG.md`:

| Register | Meaning |
|---|---|
| A | What PKD says himself |
| B | What primary-source evidence establishes |
| C | What scholars argue |
| D | What portal editors infer |

The sweep tags every hit with a `field_class` — `pkd_text` or
`editor_annotation` — and the two are never mixed. Counts on the site headline
Dick's own words; annotation counts are shown separately and labelled.

## Reading the chronology

Exegesis dates are **folder dates**: every segment in a transcription batch
inherits one date, and there are only four batches — 87 segments dated 1975,
243 in 1976, 399 in 1978, 375 in 1981. Raw yearly counts are therefore
confounded by folder size. `register.json` carries `by_year_rate` (hits per
segment) beside `by_year`, and every comparison in the dossier uses the rate.

## Known false positives, and what was done about them

Pattern work is editorial. Two corrections are already baked into
`gnostic_lexicon_source.py` and are recorded here so they are not re-introduced:

- **Monad** originally matched the ordinary English phrase `the One` and
  returned 401 false positives against 23 real ones. That pattern was removed.
- **Plato** originally matched `Parmenides`, conflating the dialogue with the
  Presocratic. Parmenides is now a separate entry, which is the better reading
  anyway: Dick's interest is in Eleatic monism, not in Plato's dialogue.

The `Sophia` pattern deliberately matches Hagia Sophia and St Sophia as well as
the aeon, because Dick's own usage runs the three together and separating them
by regex would impose a distinction he does not make.
