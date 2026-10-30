# Curation: Drugs in Philip K. Dick

Durable source of truth for `/studies/psychology/drugs-in-pkd`. The database and
the exported JSON are derived from here. The topic owns no dictionary entries
(the dictionary has none for any substance).

| File | What it is | Edit? |
|---|---|---|
| `findings.py` | Every published passage: source, verbatim anchor, window, card summary, verbatim pith, date and dating basis, concepts (facet vocabulary), speaker. Evidence packets. | **Yes**, hand-curated |
| `dossier_sections.py` | Essay sections with `{{finding-id}}` citations, browse groups and facets, contradictions, open questions, structured fields. | **Yes**, hand-authored |
| `build_inventory.py` | Writes `evidence-inventory.json` from `findings.py`. | Code |
| `build_dossier.py` | Writes `dossier.json` from `dossier_sections.py`. | Code |
| `evidence-inventory.json` | Generated. Same shape as the Bible and Burroughs inventories. | No |
| `dossier.json` | Generated. | No |

The raw corpus sweep is not kept here. Its strong tier is archived at
`archive/2026-10-30/research/2026-10-30_drugs-raw-findings.json.gz`; regenerate
it with:

```bash
python scripts/research/sweep_corpus.py --profile drugs --summary --out <file>
```

The `drugs` profile treats the bare word "speed" as weak and excludes "speed of
light", "velocity" and similar. The lexicon topic `psychology/amphetamine-use`
matched "speed" as a strong term, so most of its 116 passages are about velocity;
it is not a source for this dossier.

## Rebuild the page

```bash
python curation/drugs-in-pkd/build_inventory.py
python curation/drugs-in-pkd/build_dossier.py
python scripts/studies/seed_drugs_in_pkd.py --check     # verify, write nothing
python scripts/studies/seed_drugs_in_pkd.py
```

Then export **only** this topic and the cross-link file. Do not run
`export_studies.py` bare: it rewrites every study topic and nulls curated prose
(see CLAUDE.md). Export to a scratch directory and hand-place:

```python
import sqlite3, sys
from pathlib import Path
sys.path.insert(0, 'scripts/studies')
import export_studies as ex
out = Path('<scratch dir>')
db = sqlite3.connect('database/unified.sqlite')
ex.export_study_index(db, 'psychology', out)
ex.export_topic_detail(db, 'TOPIC_PSY_drugs_in_pkd', 'psychology', 'drugs-in-pkd', out)
ex.export_links(db, out)
```

Copy `psychology/topics/drugs-in-pkd.json` into `site/public/data/studies/`.
Diff `links.json` and `psychology/index.json` against the committed files before
copying: on 2026-10-30 both differed only by this topic's entries. Update the
psychology row of `studies/index.json` by hand (topic count, passages, packets,
contradictions); a database without the gnosticism and religion studies would
drop their rows if the file were exported. Then run the post-export passes listed
in `scripts/safeguard/safe_export.py` (at least `index_study_search`) and
`python scripts/safeguard/check_data_diff.py --worktree`.

## What the seeder enforces

It refuses to build if any anchor fails to resolve, any card pith or any essay
quotation of 40+ characters is not verbatim in its source, any `{{id}}` citation
does not resolve, any browse facet matches no card, or any contradiction's
passages cannot be found. `study_passages` and `study_contradictions` have CHECK
constraints on `claim_type`, `source_mode` and `contradiction_type`; the
findings use only the allowed values.

## Conventions

- **Lanes.** A fiction (characters speaking), B Exegesis, C criticism (Rickman's
  introduction, Butler, Jameson), D biography (Sutin, Anne R. Dick, Arnold), E
  letters, interviews, and A Scanner Darkly's Author's Note.
- **The Author's Note** is kind `paratext`: lane E because it is Dick under his
  own signature, `source_mode` `fiction` because it is printed in the novel and
  the schema has no paratext mode.
- **Speakers.** Interviews and the Author's Note are Dick; a biography card's
  speaker is its author unless the pith quotes a witness (Cindy, Nancy Hackett,
  Doris Sauter, Tim Powers), which `SPEAKER` in `findings.py` records. Every
  fiction card names the character or narrator.
- **Dating.** Per passage, with a basis: `dateline` (letters; several letters are
  catalogued as undated but carry a dateline in the body), `record` (container
  date, weak), `internal` (the entry dates itself, e.g. "30 months" after
  2-3-74, or a reference to the May 1979 Platt interview), `stamp`,
  `publication`. The Exegesis folder filed under 15 September 1976 runs to 1979;
  section 016, filed under 10 October 1978, runs to 1980.
- **Facets.** A card's `concepts` list is its facet vocabulary: substances,
  Dick's works, themes, people and characters, biographers. Biographer facets
  link to the book's archive page; work facets to Exegesis-work or work pages;
  people to name pages.
- **Contradictions** are kept, not resolved. Four are between biographers (Point
  Reyes doses; LSD count; speed after 1972; what caused the paranoia).
- **Not represented.** Anthony Peake's biography is catalogued but only its title
  page is in the archive. The texts of The Three Stigmata of Palmer Eldritch and
  Flow My Tears, the Policeman Said are not in the archive either; those novels
  appear through Dick's comments and criticism.
- **Not used.** The machine-extracted `claims` rows and the lexicon topics
  `amphetamine-use` and `addiction`.

## Pending frontend change

`browse.toc_label` ("substance, novel & theme") is in the exported topic but not
yet read: `TopicDetail.tsx` hardcodes "Browse all N passages by book & theme".
`archive/2026-10-30/drafts/topicdetail-toc-label.patch` adds an optional
`toc_label` to `BrowseConfig` and makes TopicDetail use it, falling back to the
current wording, so the Bible and Burroughs pages are unchanged. It applies to
origin/main at 56d867bd and builds. It was held back because TopicDetail.tsx and
MentionCards.tsx were being merged by another session; apply it with
`git apply` once that merge has landed.

Reseeding deletes and reinserts this topic's passages and contradictions, so
their database ids change. A re-export then differs from the committed file in
every `passage_id` and `contradiction_id`, and the pre-commit guard reads that as
content loss. For a change that does not touch passages (a browse key, a field),
hand-place the change into the committed JSON instead of re-exporting it.
