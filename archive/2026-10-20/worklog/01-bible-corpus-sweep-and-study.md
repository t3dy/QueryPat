# The Bible in PKD: corpus sweep and study

- **Date:** 2026-10-20
- **Session:** ccr-fda7e7ae-uh4a55
- **Status:** complete, pending review of the essay prose

## Research question

What does Philip K. Dick say about the Bible across the Exegesis, the novels and
stories, the interviews and the letters, and how does his use of scripture change
over time? Output: an essay page built on the same pattern as the Burroughs and
Gnostic Lexicon pages.

## Instruction

See `prompts/01-bible-study.md`.

## Corpus searched

Searched (repository files, not a database; `database/unified.sqlite` is not
present in this container, so the sweep reads the exported JSON and markdown):

- Exegesis: `site/public/data/segments/*.json`, `raw_text` plus the analytic fields.
  1,104 files read; 3 malformed JSON files skipped (named in the curation README).
- VALIS chapters 1 and 5–13 and Divine Invasion chapters 1–5, full text.
- `selected_letters_analysis.json`: 75 letters, 1972–73. **Excerpts**, not full
  text: each `summary` is capped at about 1,500 characters, and the body of some
  letters sits in `recipient`. Both fields were scanned.
- Editorial analysis: fiction chapter summaries, the 30-story analysis, biography
  events, the Exegesis entry analysis.
- Archive records (247: interviews, scholarship, letters, novels) and portal essays.

Not searched, or not searchable here: the interview transcripts (not held), the
story texts (not held), the novels other than VALIS and Divine Invasion 1–5 (not
held as text), letters after 1973 (not held as text), and the database itself.

## Queries

`curation/bible/sweep_bible.py`. Strong patterns: Bible, biblical, Scripture(s),
Old/New Testament, Gospel(s), Torah, Septuagint, King James, Vulgate, unambiguous
book names, and verse citations (for example `John 3:1`). Weak patterns, which an
editor must read: names that are also words (Mark, John, Acts, Daniel, Ruth),
`revelation`, lowercase `gospel` and `testament`, and `Pauline`.

## Documents examined

Every strong hit in the Exegesis batches of February and November 1975, 15
September 1976, 10 October 1978 and 16 April 1981 was read in a short window; the
1976, 1978 and 1981 batches account for most of the material. The trilogy chapter
hits were read in full. The scholarship and interview records were read by their
summaries. The story analysis was scanned for religious vocabulary (six of 30
summaries use it, none names the Bible).

## Discoveries

Register A: the Exegesis and the trilogy (Dick's own words).

- 1 December 1972 letter to Roger Zelazny: a dream about having "set the Bible
  into rhymed couplets" (`BIB-LET-72-01`). The earliest Bible passage the sweep finds.
- 27 February and 5 November 1975: "The Bible is a book of the future"; the Old
  Testament as monotheism borrowed from Akhenaten; "The world of the Bible was
  suddenly around me"; the Jerusalem Bible notes on Rome.
- 15 September 1976: the claim that *Flow My Tears, the Policeman Said* (which the
  Exegesis calls "Tears") contains "unmistakable material from Acts"; Father
  Rasch's identification of the Philip and the black man scene; Dick's own
  admission that he had never read Acts when he wrote the novel; "In the Bible
  isn't about the past; it's code to describe our world."
- 10 October 1978 folder: the Torah as "the Living Torah, the informational basis
  of reality"; Jesus "depreciated the Torah"; "herewith I just lost my
  Trinitarianism"; "New Scriptures are needed". This folder holds entries dated
  as late as 1980, so its date is a batch date.
- 16 April 1981: "the Bible is not a verbal description of a world; it is a
  world"; "recombinant scripture"; "an unprecedented third testament"; "Torah does
  not know everything. Christ does."
- Trilogy: Sherri on "the corrupt parts of the Bible" (VALIS 5); Kevin reads Daniel
  for Nixon (VALIS 10); the holoscope with "the Bible expressed as layers at
  different depths" (DI 2); "I am the Torah" (DI 4); Emmanuel's addendum he does
  not make (DI 2).

Register C: scholarship. Davis on the Hymn of the Pearl in the apocryphal Acts of
Thomas; Burton on Bergson and "the theology of Saint Paul"; the VALIS appendix
naming Paul of Tarsus among those said to know a great secret.

Register B and D: the interview records contain no Bible reference. The story and
novel summaries record little; that is a finding about the summaries, not the
stories.

## Interpretations

Register D. Dick's Bible moves in three steps: a text to be played with (1972),
a text about the present (1975–76), and a world that is itself a text (1981).
The step in 1976 is the one the rest depends on; it is first made in the 15
September sitting and refined afterwards. The trilogy stages the Exegesis's
arguments in voices that disagree with each other; the Exegesis has one reader
who is certain.

## Contradictions and alternatives

Preserved, not resolved:

- In 1976 the Bible is "not about the past"; in 1978 the Torah is timeless; in
  1981 the Bible is "the real world". These are three claims about the same text.
- Dick says he recognised the Acts material in *Tears* only after the novel
  appeared (1976), and that he had never read Acts when he wrote it. These can be
  read as a claim of revelation or of a later reading. The essay gives both.
- The trilogy's Emmanuel refrains from adding to the Bible; the Exegesis's Dick
  is sure he may add to it ("recombinant scripture"). Recorded as a difference of
  voice, not a contradiction.

## Unresolved questions

- What Dick said about the Bible in interviews. The transcripts are not held.
- Which Bible he used. "The J. Bible" and "Decoded New Testament" are named, with
  no edition.
- Whether the Acts material in *Tears* existed before 1974. The typescript would
  settle it.
- What the letters after 1973 say. Only excerpts of 1972–73 are held, and some
  bodies are in the wrong field.
- Whether the stories contain biblical references the summaries miss.

## Decisions

- **New study, not a topic in `religion`.** The `religion` study is not listed in
  `studies/index.json`, and its one topic is a generic overview. A separate
  `bible` study follows the Gnosticism precedent and keeps the change additive.
- **Cards cut by anchor and pith, not by line.** A re-sweep cannot move a card
  onto a different passage without the build failing.
- **Letters are a floor.** The 1,500-character cap and the misplaced bodies are
  stated on the page and in the README, not hidden.
- **Interviews say nothing.** The page states the absence and what would test it.
  No interview is paraphrased.
- **Folder dates are batch dates**, stated on each card where an entry refers to
  a later date.
- **Relevance codes 1 and 2 only.** The Bible study has no code 3–5 tier: passing
  mentions stay in `raw-findings.json`.
- **Registers**: the trilogy is lane A; the summaries are D and never quoted as
  Dick; scholarship is C.

## Files changed

- `curation/bible/` (new): `sweep_bible.py`, `raw-findings.json`,
  `dossier_sections.py`, `dossier.json`, `README.md`
- `scripts/studies/build_bible_study.py` (new)
- `site/public/data/studies/bible/` (new, generated)
- `site/public/data/studies/index.json` (one row added)
- `site/public/data/search_index.json` (one row added)
- `site/src/components/Layout.tsx` (Bible nav tab)

## Validation

- `python curation/bible/sweep_bible.py --summary` — 9,059 hits; 3,800 strong.
- `python scripts/studies/build_bible_study.py --check` — 39 cards resolve to
  passages; 14 sections; every citation marker and every quotation of 40
  characters or more is in the corpus.
- `python scripts/safeguard/check_data_diff.py --worktree` — 2 data files changed,
  no content lost.
- `npm run build --prefix site` (typecheck and bundle) — passes.
- Headless Chromium on the built site: the page renders with 14 sections, 39
  citation links and the Bible nav tab. The one console 404 is `/vite.svg`, a
  favicon reference that predates this change.

## Artifacts archived

- `prompts/01-bible-study.md`: the instruction.
- The sweep output is `curation/bible/raw-findings.json`, not copied here. It is
  regenerable and the same convention as the Burroughs and Gnosticism folders.
