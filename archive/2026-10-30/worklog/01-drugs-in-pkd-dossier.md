# Drugs in PKD: a lexicon topic brought up to the authored-dossier standard

- **Date:** 2026-10-30 (session began 2026-10-29)
- **Session:** worktree `claude/drugs-dossier`, cut from origin/main at 56d867bd
- **Status:** done; nothing committed

## Research question

What does the archive actually show about Philip K. Dick's drug use and his
writing about drugs — in his own words, in the Exegesis, in the fiction, and in
the biographies — and where do those sources disagree?

## Instruction

Build a "Drugs in PKD" dossier to the standard of the Bible and Burroughs studies
(docs/STUDY_DOSSIERS.md): hand-classified findings, cards, essay citations,
per-passage dating, browse facets (substances, works, themes, biographers) linked
to existing pages, links.json backlinks, search entries. Fix rather than inherit
the lexicon topic `amphetamine-use` ("speed" false positives), bring in the
fiction, letters, interviews and biographers, and make the biographer
disagreements contradictions. Export only the new topic and links.json.

## Corpus searched

`scripts/research/sweep_corpus.py --profile drugs` (new profile) over every
database corpus: segments (raw and curated fields), document_texts (text and
markdown), page_texts, letters, claims, biography_events, works,
pkd_on_pkd_mentions, evidence_excerpts, annotations, theophanies,
timeline_events; plus portal essays. `database/extracted_markdown` does not
exist in a worktree and was not searched (its content is in document_texts).
10,313 hits; 5,291 strong-tier.

Then targeted reading: all letters volumes; the Exegesis folders of 1975, the
folder filed 15 Sept 1976 and section 016; The Last Interview and Other
Conversations (Vertex 1974, Platt 1979, Rickman 1981–82); PKD Magazine
Interviews (Vertex, Purser 1974, Aquarian 1978, Hour 25); Rickman's In His Own
Words; A Scanner Darkly (in Five Great Novels), Now Wait for Last Year, VALIS;
Sutin, Anne R. Dick, Arnold; Butler; Jameson.

## Queries

Strong: amphetamine(s), meth(amphetamine|edrine), Semoxydrine, Desoxyn,
Dexedrine, Benzedrine, Dexamyl, Stelazine, Librium, Valium, Thorazine,
pentothal/pentathol, LSD, acid trip, mescalin, peyote, psilocybin, psychedelic,
hallucinogen, heroin, junkie, narcotics, marijuana, hashish, cocaine, doper/dope,
speed freak, X-Kalay, Synanon, Substance D, Can-D, Chew-Z, JJ-180, KR-3,
drug(s), pills, stimulant, orthomolecular, vitamin, water-soluble, Sacred
Mushroom, Allegro, Hofmann, Leary, Amanita, ergot, kykeon, Doors of Perception.
Weak: bare "speed", uppers/downers, stoned, loaded, addict, withdrawal, overdose,
flashback, trip, mushroom, soma, prescription, clinic, rehab. Excluded: "speed
of light", velocity, "at high speed", faster than light.

## Documents examined

As above. Not in the archive: the texts of The Three Stigmata of Palmer Eldritch
and Flow My Tears (no Can-D, Chew-Z or KR-3 in any novel text; "The Days of
Perky Pat" has no Can-D); Anthony Peake's biography (title page only, 90
characters). Read and rejected: the many Exegesis uses of "speed" for velocity,
"acid" in chemistry, ledger lines ("Adobe drugs bank"), the lexicon topics'
passages.

## Discoveries

105 findings, lanes A 8, B 24, C 3, D 26, E 44. Highlights (register A unless
marked):
- First amphetamine c. 1952–53, as a cure for agoraphobia (letter to Boucher,
  1962). Semoxydrine is methamphetamine: Dick learns this from a brochure, 1964.
- "I took LSD only twice" (1976); "two times ... That was in 1964" (Platt 1979);
  LSD "had none at all" influence (1973) vs. one passage of A Maze of Death (1976).
- Palmer Eldritch "written before I had ever seen LSD" (Vertex 1974); "an article
  by Aldous Huxley" (1979). Purser 1974: the slot-eyed deity gave him the title A
  Scanner Darkly.
- Mescaline once, May 1970, credited with the love in Flow My Tears.
- X-Kalay: "I owe my life to them" (1972) → "faulty" (1975) → Synanon game =
  brainwashing (Exegesis 1977–79).
- 2-3-74: pentothal, vitamin C, lithium listed as disinhibitors, never as causes;
  "intoxicated, not by LSD" vs "the drugs I took reacted to the plasmate"
  (Exegesis 1978–80).
- (B, via Sutin) stepfather's notes, 1971: Dick says he has been "on Benzedrine
  and other drugs since 1951, when Kleo's physician father gave him a
  prescription" — against Kleo's denial in the same book.
- (C/D) Arnold: paranoia "most parsimoniously" amphetamine psychosis; "the wrong
  drug: LSD". Rickman: LSD "not 'til about 1967"; novels from imagination.
  Anne R. Dick: two Semoxydrine a day at Point Reyes, recreational use only after
  1964, one LSD trip, Palmer Eldritch from mushroom reading.

## Interpretations

(D) Dick's invented drugs share a structure: addictive, owned by someone, and a
transfer of control over the user's reality. Dick drew the same conclusion
himself in section 016 ({{DRG-EX-1978-OCCLUSION}}). (D) In every causal account of
2-3-74, chemicals disinhibit rather than produce.

## Contradictions and alternatives

Twenty, recorded in `dossier_sections.py`. Biographer vs biographer: Point Reyes
doses (Anne R. Dick / Arnold), LSD count (Sutin / Anne R. Dick), speed after 1972
(Sutin / Arnold), imagination vs drugs (Rickman / Arnold). Others: LSD date (Dick
/ Rickman), Palmer Eldritch and LSD (Dick / Ellison via Sutin), Huxley vs
mushrooms, the 1963 vision and drugs, Oui's "early fifties", Kleo vs the
stepfather, X-Kalay a month vs three weeks, vitamin C dose, pot, and Dick against
himself on LSD's influence, 2-3-74, A Scanner Darkly's subject, and X-Kalay.

## Unresolved questions

Peake's position (text absent); the drugs before the 1963 vision; the date and
count of LSD trips; amphetamines after 1972 (Arnold's unnamed sources); the
length of the X-Kalay stay; which passage of A Maze of Death is the LSD vision;
the drug in Flow My Tears. All in OPEN_QUESTIONS.

## Decisions

- Placed in the Psychology study (`TOPIC_PSY_drugs_in_pkd`), beside
  amphetamine-use and addiction, which are left untouched and linked as related
  topics. Not a replacement: deleting or rewriting them was not asked for.
- The Author's Note is lane E (Dick's own signed words), not fiction.
- Contradiction types and claim types mapped onto the schema's CHECK values
  rather than widening the schema; "between biographers" goes in the summary.
- No substance facet links: the dictionary has no substance entries. Biographer
  facets link to the books' archive pages.
- The portal's older essay (`essays/drugs-in-pkd.md`) was not edited. Claims in it
  this session could not verify: Peake's position (text absent) and a
  temporal-lobe hypothesis attributed to Arnold (not in Arnold's text in the
  archive, whose only "seizure" is a withdrawal symptom).

## Files changed

- `scripts/research/sweep_corpus.py` — `drugs` profile.
- `curation/drugs-in-pkd/` — findings.py, dossier_sections.py, build_inventory.py,
  build_dossier.py, README.md, generated evidence-inventory.json and dossier.json.
- `scripts/studies/seed_drugs_in_pkd.py` — new seeder; registered in
  `scripts/build_all.py` stage 5 after the Bible seeder.
- `site/src/components/studies/CitedText.tsx` — citation labels for `biography`
  and `paratext` cards; year regex accepts 20xx.
- `site/public/data/studies/psychology/topics/drugs-in-pkd.json` (new),
  `studies/links.json` and `studies/psychology/index.json` (additions only),
  `studies/index.json` (psychology row counts, by hand), `search_index.json`
  (1 study + 105 passage entries, via index_study_search).

## Validation

- `seed_drugs_in_pkd.py --check`: 105 passages resolve; every pith verbatim; 5
  long essay quotations verified; essay cites 105 of 105 findings; every facet
  matches cards; all 20 contradictions resolve (each checked by hand to land on
  the intended pair).
- Post-export passes from safe_export.py: no changes outside the new topic.
- `check_data_diff.py --worktree`: 4 data files changed, no content lost.
- `npm run build --prefix site`: passes.
- Browser (dev server on the worktree): page, essay citations, facet filter
  (`?facet=Kyle Arnold` → 5 of 105), contradictions, open questions, backlink on
  /exegesis/works/a-scanner-darkly, search entries; no console errors.

## Artifacts archived

- `archive/2026-10-30/research/2026-10-30_drugs-raw-findings.json.gz` — strong
  tier of the sweep (5,285 findings).
