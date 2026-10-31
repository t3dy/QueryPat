# CLAUDE.md — QueryPat routing layer

**This file is a router, not a knowledge dump.** It tells you what QueryPat is,
where truth lives, what you must never do, and which file to read for the task
in front of you. Read the routed file; do not work from this page alone.

## What QueryPat is

A digital-humanities knowledge portal for Philip K. Dick scholarship: the
Exegesis, his fiction, his letters, the archive of secondary documents, and the
scholarship around them. It is an **evidence system**, not a content site. Its
value is that every statement can be traced to a source, tagged with how
reliable that kind of source is, and held alongside the statements that
contradict it.

## Where canonical truth lives

| Layer | Location | Authority |
|---|---|---|
| Canonical knowledge | `database/unified.sqlite` | **Authoritative** |
| Schema of record | `database/unified_schema.sql` | Authoritative, but **drifted** — see below |
| Staged LLM artifacts | `artifacts/generated/` | Candidate until curated |
| Authored dossiers | `curation/<topic>/` → seeders in `scripts/studies/seed_*.py` | Editorial source of truth for those topics |
| Curated biography | `site/public/data/biography/curated.json`, changed only via `curation/biography/` | **Hand-curated — no exporter writes it** |
| Exported JSON | `site/public/data/` | Mostly generated, but parts are the **only copy** — see `.claude/rules/generated-files.md` |
| Site | `site/src/` | Renders exports only |

`database/unified.sqlite` is git-ignored and rebuilt by `scripts/build_all.py`.

> **Known drift:** the live database contains tables absent from
> `unified_schema.sql` — `claims`, `claim_subjects`, `claim_relations`,
> `letters`, `theophanies`, `theophany_evidence`, `document_topics`,
> `study_topic_claims`, `letter_events_candidate`. Always inspect the live
> schema with `sqlite_master`, never trust the `.sql` file alone.

## Never do these

1. **Never regenerate or hand-edit `site/public/data/` outside the procedures in
   `.claude/rules/generated-files.md`.** Edit the source, export to a scratch
   directory, and hand-place only the files and fields you meant to change.
2. **Never promote an LLM output to canonical knowledge in one step.** It enters
   as a candidate with provenance and a status, and an editorial pass promotes
   it. See `.claude/rules/data-provenance.md`.
3. **Never resolve a contradiction to make retrieval cleaner.** Disagreement
   between sources is the data, not a defect.
4. **Never collapse evidentiary lanes.** Fiction is not testimony.
5. **Never make embeddings the canonical layer.** They are an optional
   retrieval signal over canonical rows.
6. **Never drop or rename an existing ID.** `TERM_*`, `NAME_*`, `SEG_*`,
   `DOC_*`, `EV_*`, `CLAIM_*` are referenced by exports and by the public site.

## Preservation first — read this before running any build step

`site/public/data` is **not** a disposable build artifact. It holds 673 Exegesis close
readings, the study-topic dossier prose, biography relations and works pages that exist
nowhere else. A naive re-export destroys 1,048 of 2,704 files. Full evidence:
[`docs/PRESERVATION_AUDIT.md`](docs/PRESERVATION_AUDIT.md); mechanisms:
[`docs/PRESERVATION.md`](docs/PRESERVATION.md).

**Never run `export_json.py` or `export_studies.py` directly.** Use the guard:

```bash
python scripts/safeguard/safe_export.py --exporter all
```

It snapshots, exports, runs the post-export cleaning passes, and restores anything that
lost content. Before committing:

```bash
python scripts/safeguard/check_data_diff.py --worktree
```

Install the commit guard once per clone:
`python scripts/safeguard/check_data_diff.py --install-hook`.

Editorial discoveries belong in `curation/<topic>/`, which the seeders read — not only
in the exported JSON. Substantive research sessions get a worklog entry; see
[`docs/RESEARCH_WORKLOG.md`](docs/RESEARCH_WORKLOG.md).

## Why the export is lossy

`site/public/data/` is nominally generated, but a full re-export **destroys
committed content**. Verified 2026-09-04:

- `scripts/export_json.py` drops `related_works`, `related_letters` and
  `related_exegesis_entries` from `biography/events.json`, and re-introduces
  leaked `CLM_*` ids into dictionary prose.
- `scripts/studies/export_studies.py` nulls the dossier prose on most topics
  (`definition`, `pkd_relevance`, `in_the_fiction`, …), because that prose was
  written into the JSON after export by `scripts/merge_studies_topics.py` and
  its `*.studies.json` source files no longer exist in the repo.
- Several passes run *after* export and only over the JSON:
  `clean_dictionary_claim_leaks.py`, `clean_dictionary_junk_descriptions.py`,
  `clean_studies_claim_leaks.py`, `clean_segment_wiki_artifacts.py`,
  `rebuild_search_index_terms.py`, `fix_dead_links.py`.

So: for a change that touches one entity, write the DB, run the exporter,
then **revert every file you did not intend to change** and hand-place the few
you did. Diff `site/public/data` before committing; a diff of hundreds of files
means the export ate curated work. Until the post-export prose is round-tripped
back into the database, the committed JSON is the only copy of some of it.

## Start here

Work directly in `C:\QueryPat` on `main`. No worktrees, no feature branches.
Other windows may have uncommitted work in the same checkout: stage and commit
only the files you changed (`git add <paths>`, never `git add -A`), and leave
theirs alone. Details: `.claude/rules/environment.md`.

## Route by task

| If you are working on… | Read |
|---|---|
| Anything under `site/public/data/`, any exporter, the pre-commit guard | `.claude/rules/generated-files.md` |
| Lanes, registers, dating, review states, contradictions | `.claude/rules/data-provenance.md` |
| An authored study dossier (new or existing) | `.claude/rules/study-dossiers.md`, then `docs/STUDY_DOSSIERS.md` |
| A lexicon-scanned study topic, `scan_corpus.py`, lexicons | `.claude/rules/lexicon-topics.md` |
| The Biography page, `curated.json` | `.claude/rules/biography.md` |
| Shared checkout, preview server, deploy, encoding | `.claude/rules/environment.md` |
| Validating anything | `.claude/rules/testing.md` |
| Research sessions and their records | `docs/RESEARCH_WORKLOG.md` |
| Database, schema, the pipeline, semantic memory | `docs/ARCHITECTURE.md`; inspect the live schema with `sqlite_master` (no rule file yet) |
| The site's community/comment features | `USERSNEXTSTEPS.md`, `supabase/schema.sql` |

Long-form docs that exist: `docs/ARCHITECTURE.md`, `docs/PRESERVATION.md`,
`docs/PRESERVATION_AUDIT.md`, `docs/RESEARCH_WORKLOG.md`,
`docs/STUDY_DOSSIERS.md`, `scripts/studies/STUDY_JSON_CONTRACTS.md`.

## How to validate a change

```bash
python scripts/safeguard/check_data_diff.py --worktree      # no curated content lost
python scripts/studies/seed_<topic>.py --check              # a dossier: anchors, verbatim quotes
python scripts/biography/apply_biography_curation.py --verify
python scripts/audit.py                                     # corpus-wide data audit
npm run build --prefix site                                 # site typecheck + build
```

Then look at what you changed in the preview. Which check applies to which
change, and the known failures on `main`: `.claude/rules/testing.md`.

## When you learn something architectural

Write it down where it will outlive this conversation: a rule file in
`.claude/rules/` if it constrains future work (and a row in the routing table
above), a `docs/` page if it explains the system, a worklog entry under
`archive/<date>/worklog/` for what a research session found and decided. Chat
and commit messages are not memory. Keep this file a router: if a section grows
past a paragraph, move it to a rule file.
