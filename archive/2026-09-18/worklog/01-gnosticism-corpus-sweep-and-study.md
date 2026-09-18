# gnosticism corpus sweep and study

- **Date:** 2026-09-18 03:39 UTC
- **Session:** claude/pkd-gnostic-study-website-osb1ue
- **Status:** complete

## Research question

What is Dick's actual Gnostic vocabulary, where did it come from, and when did
each part of it arrive? The label "Gnostic" does a great deal of interpretive
work in the criticism; this asks whether the corpus supports it, and in what
sense.

## Instruction

"I want a study of gnostic ideas in PKD's Exegesis, Letters, and Valis trilogy,
then build a website to show off the results. we will need a list of all the
gnostic terms scholars and texts that he references."

## Corpus searched

| Corpus | Sources | Lane |
|---|---|---|
| Exegesis segments (`site/public/data/segments/*.json`) | 1,104 | B |
| Selected Letters (`selected_letters_analysis.json`) | 75 | B |
| VALIS trilogy chapter text and summaries | 21 files | A / D |
| Archive catalogue (`site/public/data/archive/docs/*.json`) | 241 | C |

Exegesis coverage is complete: 9,264,014 characters of segment `raw_text`
against 9,156,433 in `exegesis_ordered.txt`. Both `raw_text` and twelve curated
analytical fields were searched, tagged separately as `pkd_text` and
`editor_annotation` and never mixed.

**Not searched**, and this matters:

- The Selected Letters volumes for 1975-76, 1977-79 and 1980-82. They are
  catalogued at full ingest level but their text lives in `unified.sqlite`,
  which cannot be rebuilt in this environment — `build_all.py` stage 1 depends
  on a `C:/ExegesisAnalysis/` source tree. The 75 letters that *are* held are
  all 1972-73, entirely before 2-3-74. **Every statement about the
  correspondence in this study is therefore provisional.** `sweep_gnosticism.py`
  takes `--db` and covers those volumes when a database is present.
- Three malformed segment files, skipped by the JSON parser:
  `SEG_EXEG_1976-09-15_Dorothy_214`, `SEG_EXEG_1978-10-10_SECTION_016_129`,
  `SEG_EXEG_1981-04-16_Pat_149`. Pre-existing fault, not introduced here.
- *The Transmigration of Timothy Archer* beyond chapter summaries.
- Full text of the 241 secondary documents (titles and summaries only).

## Queries

111 lexicon entries, each with its own regex set, defined in
`scripts/research/gnostic_lexicon_source.py` across seven categories: concepts
(34), texts (19), modern scholars (17), teachers (12), pkd coinages (11),
heresiologists and ancient philosophers (10), traditions (8). 48,628
attestations returned.

## Documents examined

The full Exegesis transcription; VALIS chapters 1 and 5-13 and *The Divine
Invasion* chapters 1-5 as primary text; the archive catalogue entries for
J. K. Thomas's 'Coin-Operated Doors and God', Erik Davis's ASE talk on the Hymn
of the Pearl, and Laurie Jui-hua Tseng on the trilogy's literary theology.

## Discoveries

- **(B)** Of 111 register entries, 75 are attested in Dick's own words, 6 appear
  only in portal-editor annotation, and 30 appear nowhere in the corpus.
- **(B)** No primary Gnostic text is named anywhere in the Exegesis. Not the
  Apocryphon of John, the Gospel of Truth, the Gospel of Philip, the Hypostasis
  of the Archons, the Tripartite Tractate, Trimorphic Protennoia, Thunder
  Perfect Mind, the Bruce Codex, the Chaldean Oracles or the Ginza. The Corpus
  Hermeticum occurs only in editor annotation.
- **(B)** No heresiologist is named except Tertullian (3) and Origen (2).
  Irenaeus, Hippolytus, Epiphanius and Clement of Alexandria: zero.
- **(B)** Named Gnostic teachers are near-absent: Valentinus 5 (all in the 1981
  folder), Basilides 1, Marcion 1. Simon Magus, at 29, is the exception.
- **(B)** The concepts are everywhere regardless: Sophia 950, anamnesis 1,045,
  gnosis 293, pleroma 105, demiurge 85.
- **(B)** Hans Jonas is attested 26 times, only in the 1978 and 1981 folders
  (rates 0.005 and 0.048). Nag Hammadi 29 times, all in 1978.
- **(A)** Dick cites Jonas by argument, not just by name: "the reversing of the
  original fall into ignorance and forgetfulness … as Hans Jonas points out
  about Syrian gnosticism" (October 10, 1978).
- **(B)** Jung is attested 181 times and peaks *earliest*, at 0.379 hits per
  segment in 1975, settling near 0.1 after.
- **(B)** Sophia peaks earliest of all the Gnostic material (1.747 in 1975) and
  declines monotonically to 0.283 in 1981, while general Gnostic vocabulary
  rises from 0.31 to 1.078 across the same span.
- **(B)** The Black Iron Prison is a September 1976 event: 0.023 in the 1975
  folder to 2.247 in 1976, the sharpest transition in the register.
- **(A)** "The Empire never ended" is in the Exegesis in September 1976, five
  years before VALIS: "Rome absorbed - & destroyed - Xtianity. 'The Empire never
  ended.'"
- **(A)** The self-identification is conditional wherever it is direct: "If I am
  a Gnostic -+ my published writing is basically Gnostic- I should believe in
  Simon Magus who founded Gnosticism" (October 10, 1978).
- **(B)** Christian vocabulary outweighs Gnostic vocabulary in every folder
  (2.253 against 0.31 in 1975; still 0.533 against 0.709 in 1981).
- **(A)** **Dick's most-cited source is an encyclopedia.** He names the
  Encyclopaedia Britannica — "the EB" — and the Encyclopedia of Philosophy 128
  times in his own words, more than Hans Jonas, Nag Hammadi and every named
  Gnostic teacher combined. He argues with its articles rather than checking
  facts in it: "The Britannica says that it is an unusual book in that it
  presents wisdom as personified, i.e. as Lady Wisdom" (September 17, 1975);
  "(I learned this from the Britannica)" on the archaic form of the sacraments
  (September 15, 1976). This entry did not exist in the first sweep and was
  added after the mention cards surfaced it.
- **(A)** In September 1976 he reasons from "that EB article I can't find, about
  the gospel of Thomas in which a letter from the man's parents comes" and
  reminds the recipient "of who he is + his task here" — that is the Hymn of the
  Pearl, which is in the Acts of Thomas, not the Gospel. He is working from
  memory of an encyclopedia entry, and the misattribution is the evidence.
- **(A)** Dick calls Jonas's text an **article**, not a book, and in April 1981
  resolves to "reread Hans Jonas' article on Gnosticism". Jonas wrote the
  Gnosticism entry for the Encyclopedia of Philosophy.
- **(A)** He read the Nag Hammadi codices by October 1978 and used them to
  re-read his own fiction: "It is obvious to me after reading in the Nag Hammadi
  codices that Palmer Eldritch is beyond doubt Yaltabaoth" — of a novel
  published in 1965.
- **(A)** In April 1981, in one folder, he both claims the label — "It is as
  Valentinus taught!", "my book 'Valis' is Gnostic + the explanation is Gnostic"
  — and rejects the Gnostic Christology: "I am therefore not a docetist; Christ
  actually suffers + dies as our ransom."
- **(A)** He settles the Black Iron Prison / Palm Tree Garden question against
  himself, in a sentence rarely quoted: "The BIP + PTG are both very real, + are
  antithetical alternatives, with the BIP obtaining, due to the artifact's
  control of this, its world (yaltabaoth)."
- **(A)** The Sethian myth is written out in September 1976, two years before he
  reports reading the codices: the feminine half of the Urgrund "does not
  herself directly enter our world but is separated from it (us) by her
  offspring the artifact (yaldabaoth)".
- **(A)** He distinguishes the traditions accurately and says it matters to him:
  "Here would be the crucial distinction between Neoplatonism and Gnosticism,
  which I feel so strongly about: the former is sort of self-fertilizing … but
  in Gnosticism you have the idea that the Savior is absolutely necessary."
- **(A)** Sophia and his private coinage are identified outright: "Just to spell
  it out: 'Santa Sophia' and 'Firebright' are one and the same."
- **(B)** A pattern fault found via the cards: Dick spells the demiurge
  **Yaltabaoth** as often as Yaldabaoth (16 and 16). The original pattern missed
  half the occurrences; corrected, the count went from 19 to 30.
- **(C)** J. K. Thomas (2014) sources Dick's Gnosticism to "Hans Jonas's The
  Gnostic Religion and the Encyclopedia of Philosophy"; Erik Davis traces the
  Hymn of the Pearl to him "via Encyclopaedia Britannica and Hans Jonas's
  Gnostic Religion". Two scholars working from the documents reach the same
  conclusion the sweep reaches from the corpus.

## Interpretations

**(D)** Dick's Gnosticism is conceptual and reconstructed rather than textual
and derived. He has the ideas without the library, and the scholarship arrives
after the system it is supposed to explain — Jung early as a frame, the
experience in 1974, the vocabulary consolidating through 1976, Jonas and Nag
Hammadi entering only in 1978. On this reading the 1978 Jonas citations are
Dick finding a name for something already built, not acquiring it.

**(D)** The order of arrival — Sophia first, framework second — suggests the
figure came before the cosmology that explains her, which is the reverse of what
a reading-led account would predict.

## Contradictions and alternatives

Preserved, not resolved:

- Attestation is not knowledge. Dick could have read these texts and never named
  them; absence of a name is weak evidence of absence of reading. Against that:
  six years of private writing with no audience, in which he names Plato 1,066
  times and Parmenides 216, is a context where the silence carries some weight.
- If the system is convergent — derivable by anyone starting from the same
  problem, as Culianu argued — then reconstruction without sources is
  unremarkable rather than striking.
- The Palm Tree Garden and Zebra are not Gnostic ideas. A God camouflaged inside
  creation is the opposite of a God exiled from it. Either Dick misclassified
  his own cosmology, or it was never Gnostic in the strict sense.
- The critical consensus may rest disproportionately on VALIS, against six years
  of Exegesis that does not support it as cleanly.

## Unresolved questions

- Which encyclopedia entry or edition did Dick use before 1978?
- Does the 1975-82 correspondence name sources the Exegesis does not? This is
  the single highest-value follow-up and needs only a built database.
- Erik Davis dates a Hymn of the Pearl engagement to a February 1975 letter; the
  Hymn is attested 7 times in the Exegesis. Does the letter corpus move that?
- What happened between the November 1975 and September 1976 folders? The Black
  Iron Prison jump is the largest in the corpus and the intervening months are
  not represented.

## Decisions

- **Built a new `gnosticism` study rather than extending `religion`.** The
  religion study is a corpus-wide reading guide with one topic; this is an
  evidence-led study with its own register. Keeping them separate preserves
  both.
- **Hand-placed the exported JSON rather than running the exporters.** The
  database cannot be built in this environment, so `safe_export.py` had nothing
  to export from. `build_gnosticism_study.py` writes only this study's files and
  is idempotent; `check_data_diff.py --worktree` reports no content lost.
- **Kept unattested entries in the register instead of dropping them.** "He
  never reached for this word" is the study's central finding and the register
  is the only place it is recorded — the same principle as the Burroughs
  inventory's relevance-4 and -5 findings.
- **Separated `pkd_text` from `editor_annotation` in the sweep.** 28,635 of the
  48,628 attestations are portal-editor annotation. Reporting them together
  would have inflated every count by roughly 150% and breached lane discipline.
- **Reported rates, not raw counts, for chronology.** Exegesis dates are folder
  dates over four unequal batches; raw counts are confounded by folder size.
- **Rejected two patterns after checking them.** `Monad` matched the English
  phrase "the One" (401 false positives against 23 real); `Plato` matched
  `Parmenides`, conflating the dialogue with the Presocratic. Parmenides is now
  its own entry.
- **Did not repair the three malformed segment files.** They are a pre-existing
  fault in `site/public/data`, which this project forbids editing directly, and
  repairing them is outside this brief. Flagged instead.

## Second pass: the essays

The first pass produced a register and topic pages. The second added what the
Burroughs page has and these lacked: a real essay per topic, with the mention
data inside the argument rather than beside it.

- 96 mention cards, 16 per topic, selected from the sweep by round-robin across
  each topic's terms — ranking alone clustered every card on whichever term sat
  in the longest passages (the Sophia page came back 12/16 Adam Kadmon).
- 35 essay sections across the six topics, each with its evidentiary register,
  citing 76 cards inline with `{{card-id}}` markers.
- `build_gnosticism_study.py` now refuses to build on an unresolved marker. It
  caught one on the first run — a Sophia section citing a card belonging to the
  trilogy page — which is exactly the failure it exists to prevent.
- `MentionCards.tsx` had the Burroughs groups hardcoded; grouping is now driven
  by `card.group_key` with the old groups kept as the fallback, so the Burroughs
  page renders identically (verified: 72 citations, 64 cards, its own seven
  group labels).
- Card summaries are marked `derived` on the page where a script wrote them
  rather than an editor, so the two can never be confused.

### Quotation verification, and what it caught

The Burroughs seeder verifies its essay quotations against source on every
build; this study did not, and the essays quote heavily. Added the same check:
every quotation of 40+ characters in the prose is matched against the swept
corpus, folding typography — quote style, dashes, soft hyphens, words broken
across a line, case, spacing — but never words. 74 quotations are checked and
the build fails, naming the section, if one does not resolve.

It failed ten times on first run and every failure was real. In each case the
prose had silently tidied the transcription: `develation` written as
`revelation`, `Peacable` as `Peaceable` (twice), `Pythagorian` as `Pythagorean`,
`contraversy` as `controversy`, `Hermetic t Kaballist` as `Hermetic +
Kaballist`, `it his yet to be overthrown` as `has yet to be overthrown`,
`Encyclopedia Britannica` as `Encyclopaedia` inside a quotation of Erik Davis;
plus a dropped `understood`, a verb silently conjugated, and a stray editorial
`A` deleted from between two sentences rather than elided.

None changed an argument, and that is the point: they are exactly the errors
that survive review, because nothing about them looks wrong. A page whose claim
is that every statement can be checked cannot quietly correct its sources, so
the check belongs in the build rather than in a reviewer's attention.

## Files changed

Curation (new):
- `curation/gnosticism/README.md`, `lexicon.json`, `raw-findings.json`,
  `register.json`, `dossier_sections.py`, `mention_cards.py`, `dossier.json`

Scripts (new):
- `scripts/research/gnostic_lexicon_source.py`
- `scripts/research/sweep_gnosticism.py`
- `scripts/research/build_gnostic_register.py`
- `scripts/studies/build_gnosticism_study.py`
- `scripts/studies/seed_gnosticism.py`

Scripts (modified):
- `scripts/build_all.py` — seeder registered in stage 5

Site (new):
- `site/src/pages/GnosticLexicon.tsx`
- `site/public/data/studies/gnosticism/` (index, register, 6 topics)

Site (modified):
- `site/src/App.tsx` — route; `site/src/components/Layout.tsx` — nav;
  `site/src/App.css` — register and card styles
- `site/src/components/studies/MentionCards.tsx` — grouping made data-driven
- `site/src/pages/TopicDetail.tsx` — passes groups and wording through
- `site/public/data/studies/index.json` — study registered
- `site/public/data/search_index.json` — 6 topics + 111 terms

## Validation

- `python scripts/safeguard/check_data_diff.py --worktree` → "2 data file(s)
  changed, no content lost."
- `npm run build --prefix site` → tsc + vite clean.
- Rendered in headless Chromium: lexicon (112 rows), study index, studies
  index, and topic pages. `what-dick-actually-read` renders 7 sections, 16
  citations, 16 cards in 7 groups; `orthodoxy-and-gnosis` 6/14/16. Clicking a
  citation scrolls to its card and flashes it. The Burroughs page is unchanged
  (72 citations, 64 cards, 7 groups, 14 sections). No console errors beyond a
  pre-existing `/vite.svg` favicon 404.
- `build_gnosticism_study.py` re-run twice: search index stable at 111 + 6, no
  duplicates.
- `seed_gnosticism.py --check` → 6 topics, 49 packets, 127 passages. The
  database write path is **untested** — no database can be built here.

## Artifacts archived

`curation/gnosticism/raw-findings.json` is the sweep output and is regenerable;
it is committed rather than archived because the register is derived from it.
