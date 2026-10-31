# Biography corrections, research leads, and the agent system files

- **Date:** 2026-10-30
- **Session:** worktree `claude/drugs-dossier`, continuing 01-drugs-in-pkd-dossier
- **Status:** done; not yet committed

## Research question

Using what the Drugs in PKD dossier established, what is wrong or missing in the
curated biography? And what does the next agent need to know to repeat this
work without re-learning it?

## Instruction

"Do a bit of each [AI voice, Music, break-in], generally work on improving the
biography section and entries, and update our system files for future agentic
coding efforts and environment."

## Biography: what was wrong

Read `site/public/data/biography/curated.json` (190 events; the page's content)
and `events.json` (746 machine-extracted events, 198 with no date or an
impossible one — e.g. 1126, from the street address "1126 Francisco St"; not
shown on the page except its letter events, and not touched).

Errors found in curated events, each checked against the corpus:

| Event id | Was | Is | Basis |
|---|---|---|---|
| `pkd_bio_1956_marriage_anne` | 1956, Berkeley | April 1, 1959, Ensenada | Sutin; Anne R. Dick |
| `pkd_bio_1963_marriage_hackett` | 1963 | July 1966 | Sutin ("In July 1966 Phil and Nancy were married"); Isa born March 15, 1967 |
| `pkd_bio_1972_suicide_attempt` | "after the X-Kalay convention" | after VCon; X-Kalay was the rehab house | letters |
| `pkd_bio_1972_vancouver_x_kalay_arnold` | Arnold reads it as "a misfit refuge … search for structure and belonging" | Arnold describes a dictatorial program that broke residents down | Arnold's text in the archive says nothing like the old framing |
| `pkd_bio_1973_gutter_years_narrative` | dated 1970-01-01; quote "I embraced" | 1970–72 range; the letter says "I embrace", and describes a pattern after each marriage | letter to Diane Cleaver, Sept 5, 1973 |
| `pkd_bio_1971_burglary` | "No one was ever charged." | police reported an arrest (Jerry Wade, with Dick's stolen Ruger .22) in Feb 1972 | letter to Inspector Shine, Nov 4, 1972 |

Two thin drug events (`1964_amphetamine`, `1967_paranoia_drugs`) gained narrative,
sources, quotes and a dispute. Six events were added: first Semoxydrine
(1952–53), first LSD (1964, with the count/date dispute), mescaline (May 1970),
the Stanford ward (May 1971), the orthomolecular vitamins (March 1974), speed for
Metz (Sept 1977). Thirteen events link to the dossier with a facet filter.

Ids were not renamed, even where the year in the id is wrong.

## Mechanism

`curated.json` has no exporter; earlier scripts in `scripts/biography/` patched it
directly. The changes now live in `curation/biography/{drug_years,breakin_1971}.py`
and are applied by the new `scripts/biography/apply_biography_curation.py`
(CORRECTIONS / REPLACE / APPEND / NEW_EVENTS; idempotent; `--verify` refuses to
write unless every quote on a touched event is verbatim in the corpus — all 14
touched events pass). `Biography.tsx` renders `links.studies`.

The first attempt replaced whole `sources` and `dispute` lists and the guard
caught it: an existing dispute on the suicide attempt and sources with chapter
locators would have been lost. Hence APPEND and REPLACE. The guard now reports
only two intended replacements: the source entries whose own text was wrong
("the 1963 marriage…", Arnold's "misfit refuge"). Committing them needs a scoped
`.allow-data-loss` for `biography/curated.json`.

## AI voice: a fix tried and reverted

`ai/ai` has 717 passages; about 600 contain "AI voice". Treated as false
positives (like "speed"), an exclusion cut the topic to 101. Then the topic's
reviewed prose was read: it defines "AI" in the late Exegesis as the AI voice —
St. Sophia, the Logos — explicitly "not artificial intelligence in the technical
sense". The passages are the topic. Reverted lexicon, database and JSON. The
proposed "AI voice dossier" session was withdrawn. Lesson recorded in
`.claude/rules/lexicon-topics.md`: read the prose before calling a dominant term a
false positive. `ai/surveillance` and `ai/automation` are the same kind.

## Music and the break-in: research leads only

New sweep profiles `music` and `breakin` in `sweep_corpus.py`; strong tiers
archived; findings and pitfalls in `curation/music-in-pkd/RESEARCH_NOTES.md` and
`curation/breakin-1971/RESEARCH_NOTES.md`. Key leads: the Heinlein letter of Aug
5, 1975 (Wagner, a Karl Muck *Parsifal* found in a record-store storeroom); the
Inspector Shine letter (the arrest); Dick's January 1975 letters to Senators
Church, Cranston, Proxmire, Baker and Representative Dellums. Kinman's music
catalogue is not in the archive.

## System files

CLAUDE.md routed every task to `.claude/rules/*.md` and `.claude/context/`, none
of which had ever existed, and named four docs, a validation script and a test
suite that do not exist. Now:

- `.claude/rules/`: generated-files, data-provenance, study-dossiers,
  lexicon-topics, biography, environment, testing — each written from what this
  work verified.
- CLAUDE.md: routing table points only at files that exist; "Start here"
  (worktree + setup script); validation commands that exist; Exported JSON no
  longer described as "never edit" when parts are the only copy.
- `docs/STUDY_DOSSIERS.md`: committed (was untracked in the main checkout), with
  steps 6–7 (fix the superseded lexicon topic; correct the biography).
- `scripts/dev/setup_worktree.py`: copies the database, runs `npm ci`, prints the
  preview entry for the main checkout's `.claude/launch.json`.
- `scripts/audit.py` defaulted to `C:/QueryPat` for both database and report
  output, so a worktree audited the main checkout and wrote into it; now relative
  to the script. (Its reports there are git-ignored; nothing tracked was touched.)
- `artifacts/validate_artifacts.py` crashed on a top-level JSON list; now reports
  it. It then shows 1,009 failures among 1,381 artifacts on `main` — pre-existing,
  recorded in `testing.md`, not fixed.

## Unresolved

- The pull in `C:\QueryPat` will refuse until its untracked
  `docs/STUDY_DOSSIERS.md` is moved aside (git refuses even an identical copy).
- 108 curated biography events still carry "Generated curation note".
- `addiction` and `double-doppelganger` lexicon terms; the artifact schema drift.

## Second pass: key dates and every quote

Worked through the 33 unchecked importance 4–5 events (`curation/biography/key_dates.py`):

- Exact dates from the biographies: Jane's death January 26, 1929 (Sutin); Laura
  born February 25, 1960 (Sutin, Anne R. Dick, with Phil's "Now my sister is made
  up for"); the stroke found Thursday, February 18, 1982 (Anne R. Dick; the
  narrative's "a neighbor, alarmed at not hearing from him" replaced by the
  Perezes, named by both Sutin and Anne R. Dick).
- The marriage to Tessa: Sutin April 1973, Arnold 1972 — recorded as a dispute;
  the day "19" is not in the biographies and is flagged unverified.
- The 1958 Point Reyes crisis gained its primary source: the 1962 letter to
  Boucher (the bridge over Papermill Creek; "a momentary psychosis").
- Confirmed unchanged: Jeanette Marlin 1948, Kleo June 1950, Christopher July
  25, 1973, death March 2, 1982, the UBC talk before VCon.

The applier's `--verify` (and a new `--audit` over the whole page) found two
pre-existing quotes that were not verbatim: one on Jane's death reversed the two
halves of an April 1981 Exegesis sentence around an ellipsis; one on the fish
sign had "magnet-like" for the transcription's "magnet like". Both corrected. The
verifier now accepts an in-order elision and rejects a reordered one. All 46
quotes on the Biography page pass. 103 events still carry generated notes, 28 of
them at importance 4–5.
