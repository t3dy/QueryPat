# Rule: authored study dossiers

The standard is `docs/STUDY_DOSSIERS.md`. Working examples, newest first:
`curation/drugs-in-pkd/` (+ `scripts/studies/seed_drugs_in_pkd.py`),
`curation/pkd-bible/`, `curation/burroughs-word-virus/`. Copy the drugs dossier:
its README records every pitfall below.

## Method

1. Sweep: add a profile to `scripts/research/sweep_corpus.py` (strong / weak /
   exclude). Keep ambiguous words weak. Archive the strong tier as
   `archive/<date>/research/<date>_<topic>-raw-findings.json.gz`.
2. Read and classify by hand. Record false positives in the worklog.
3. `curation/<topic>/findings.py`: anchor (verbatim, no soft hyphens or curly
   quotes — `str.find` must hit the raw text), window, card context, verbatim pith,
   concepts, `dated` + `dating_basis`, speaker.
4. `dossier_sections.py`: essay with `{{finding-id}}` citations and a register per
   section; facets with `link`s to existing dictionary, name, Exegesis-work, work
   or archive pages; groups; contradictions; open questions.
5. Seed with `--check` until clean, then seed, export the topic file and
   `links.json` only (see `generated-files.md`), run the post-export passes, verify
   in the browser, write the worklog.

## Schema constraints (the database refuses anything else)

- `study_passages.claim_type`: definition, symptom_description, causal_theory,
  allegory, self_report, critique, comparison, unresolved.
- `study_passages.source_mode`: fiction, exegesis, letter, interview, criticism.
- `study_contradictions.contradiction_type`: factual, interpretive, chronological,
  self_vs_critic, fiction_vs_exegesis, early_vs_late. Put "between biographers" in
  the summary text, not the type.

## Pitfalls already paid for

- The Bible `doc()` helper took `speaker` positionally; omitting it shifted the
  date into the speaker and left `dated` null. Check card `dated` and `speaker`
  after every build.
- A contradiction fragment resolves to the *first* passage containing it; map each
  contradiction back to its finding ids after seeding.
- Reseeding renumbers passage and contradiction ids, so a later re-export looks
  like content loss. Hand-place small follow-up changes.
- Facets match a card only by exact label in `concepts` (aliases are not checked by
  the seeder).
- `TopicDetail.tsx` still says "Browse all N passages by book & theme";
  `archive/2026-10-30/drafts/topicdetail-toc-label.patch` makes it read
  `browse.toc_label`.
- Texts absent from the archive (Peake's biography, Kinman's music catalogue,
  *Palmer Eldritch*, *Flow My Tears*) cannot be quoted. Say so on the page.
