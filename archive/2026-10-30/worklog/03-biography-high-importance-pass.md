# Biography: the last 28 unchecked importance 4–5 events

- **Date:** 2026-10-30
- **Session:** worktree `claude/drugs-dossier`, after 02-biography-and-system-files
- **Status:** applied to `curated.json`; not committed

## Research question

Do the 28 importance 4–5 curated events that still carried a "Generated
curation note" survive a check of dates, places and claims against Sutin, Anne
R. Dick, Arnold, the Selected Letters and the Exegesis in
`database/unified.sqlite`?

## Instruction

"Biography: work down the curated events whose notes still begin 'Generated
curation note' … For each, check dates and claims against Sutin, Anne R. Dick,
Arnold and the letters … Prefer APPEND and REPLACE over replacing lists. Never
rename an id."

## Method

A keyword-in-context search over the three biographies (`document_texts`), the
`letters` table and the Exegesis `segments`; Sutin's chapter headings, with their
year spans, extracted to check locators. Changes in
`curation/biography/high_importance.py`; applied with `--verify` (48 touched
events, every quote verbatim), then `--audit` (61 of 61 quotes on the page pass).

## What was wrong

| Event id | Was | Is | Basis |
|---|---|---|---|
| `pkd_bio_1929_incubator` | incubator "weeks after" Jane died | the same day, Jan 26, 1929; Jane died on the way to the hospital | Sutin (Dorothy's letter), Arnold, Anne R. Dick |
| `pkd_bio_1950_marriage_kleo` | gave way "in the mid-1950s" to Anne | Point Reyes, September 1958; Anne that year | Sutin |
| `pkd_bio_1951_first_story_sales` | year only; *Planet Stories*, *If* | October 1951, "Roog", to Boucher at F&SF | Sutin, quoting Dick |
| `pkd_bio_1964_three_stigmata` | Oakland; "most frightened by" (unsourced) | Point Reyes, mailed March 1964; Exegesis "Palmer Eldritch in the Sun" | Sutin; Exegesis |
| `pkd_bio_1973_csuf_talk` | recorded a talk, July 1973 | not attested; lecturing to McNelly's classes from 1972 | letters Aug 30, 1972; May 26 and July 30, 1973; CSUF finding aid |
| `pkd_bio_1974_exegesis_begin` | Arnold's stressors: surgery, amphetamine baseline, break-in, Jane | Arnold: IRS, poverty, new baby, botched tooth extraction, Percodan, BP drugs, possibly lithium, alleged speed Tessa did not see | Arnold ch. 7 |
| `pkd_bio_1974_03_zebra` | named Zebra in March 1974; "the first of the many names" | named December 1976; VALIS is older (Sept 1975 folder) | Sutin; letter to Hurst, Feb 11, 1977 |
| `pkd_bio_1981_blade_runner_visit` | visited the production | June 1981 news clip; November private effects-reel screening, photographed with Scott | Sutin; letters |
| `pkd_bio_1982_death` | "his body" taken to Fort Morgan | his ashes | Anne R. Dick |
| four 1976–81 events | Fullerton | Santa Ana | Sutin; Selected Letters chronology |
| 16 events | Sutin/Arnold chapter locators | corrected (most one chapter off) | chapter headings |

Ids were kept, including `pkd_bio_1973_csuf_talk` and `pkd_bio_1981_blade_runner_visit`
whose names no longer describe the event.

## Contradiction recorded, not resolved

`pkd_bio_1972_ubc_lecture`: Sutin and Dick's letters say February 1972 ("I flew
to Canada in February of last year, made my two speeches"); the CSUF finding
aid catalogues the speech as delivered in March 1972. Now a `dispute`.

## Confirmed as they stand

Birth (Dec 16, 1928); the 1940 *Stirring Science Stories* discovery; Marlin
1948; Solar Lottery 1955 (title Wollheim's); High Castle (Putnam 1962, plotted
with the I Ching); Hugo (now dated September 1963); Androids (w. 1966, p. 1968);
Ubik (w. 1966, p. 1969; the novel Dick returns to most in the transcribed
Exegesis: 425 segments to Palmer Eldritch's 60); Vancouver (now February 1972);
Christopher (July 25, 1973); the iron prison as an early image (letter to
Gillespie, Jan 28, 1975); living information; The Divine Invasion (Simon &
Schuster, 1981); death on March 2, 1982, under the shared "Twins" gravestone
(Arnold).

## Mechanism change

`apply_biography_curation.py` gained `AMEND` (set fields on the one list item
matching given fields), so a wrong `locator` is fixed without replacing a
`sources` list; and `--verify` now also covers events touched only by `REPLACE`
or `AMEND`. The pre-commit guard read an amended source as a removed one; it now
pairs an unmatched old entry with a same-shaped edited entry and passes the edit
if nothing in it was emptied or cut (`_is_edit_of` in `check_data_diff.py`).

## System files simplified (owner's request)

"I don't even want to be in a separate environment from the original query pat
or making all these weird branches." Worktrees and feature branches are dropped:
CLAUDE.md and `environment.md` now say to work in `C:\QueryPat` on `main` and to
stage only one's own files, since other windows share the checkout.
`scripts/dev/setup_worktree.py` is deleted. This branch's work was brought into
the main checkout.

## Unresolved

- 75 events still carry generated notes, all at importance 3 or below.
- Whether Dick attended the 1963 Worldcon; the archive does not say.
- The Biography page was not opened in the preview after this pass; the change
  is data-only and uses existing fields (`dispute`, `quotes`, `sources`).
