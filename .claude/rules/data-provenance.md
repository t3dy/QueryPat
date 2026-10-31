# Rule: provenance, lanes, registers, review states

## Lanes (what kind of source a passage is)

| Lane | Source | Note |
|---|---|---|
| A | Fiction | Characters speaking. Never testimony about Dick's life. |
| B | Exegesis | Dick theorising, mostly after 1974. |
| C | Criticism and scholarship | The studies code also files biographies here by default. |
| D | Biography | Sutin, Anne R. Dick, Arnold. Dossiers set this explicitly. |
| E | Letters, interviews, speeches, and Dick's own signed paratext (e.g. *A Scanner Darkly*'s Author's Note) | Dick under his own name. |

`scan_corpus.py` maps archive lanes D and E to C; authored dossiers keep them
apart. Never collapse lanes to make a page tidier.

## Registers (what kind of statement an essay sentence is)

A = PKD's own words, B = primary-source fact, C = scholarly argument, D =
portal-editor inference. Every dossier essay section declares one.

## Dating a passage

Every authored passage carries `dated` and `dating_basis`: `dateline` (letters;
many letters catalogued as undated carry a dateline in the body), `stamp` (a date
written in the entry), `internal` (the entry dates itself: "30 months" after
2-3-74, a reference to a datable interview), `record` (the container's date —
weak), `publication`. Exegesis containers run long: the folder filed under
1976-09-15 runs to 1979; section 016, filed under 1978-10-10, runs to 1980.

## Review states

- Lexicon topics (`status` scanning / drafted / mapped) are machine scans. Their
  passages are unreviewed; their prose is machine-drafted and unchecked.
- Authored dossiers (`status` reviewed, with `mention_cards`) were read passage by
  passage. Only they feed `studies/links.json` backlinks and passage search.
- The `claims` table is unreviewed rule output. Do not cite it on a page.
- An LLM output never becomes canonical in one step: it enters as a candidate with
  provenance and a status, and an editorial pass promotes it.

## Contradictions

Disagreement between sources is the data. Record it (`study_contradictions`, a
`dispute` on a biography event); never resolve it to make retrieval cleaner. A
contradiction names both passages; the seeders refuse to build if either is
missing.
