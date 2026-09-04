# Preservation architecture audit and build

- **Date:** 2026-09-04
- **Session:** claude-opus-5, QueryPat
- **Status:** complete

## Research question

Where in the QueryPat pipeline can a regeneration step overwrite, delete, null or
otherwise lose existing scholarship — and what preservation architecture would make
that difficult rather than routine?

## Instruction

User brief of 2026-09-04, preserved verbatim at
`archive/2026-09-04/prompts/01-preservation-architecture.md`. Triggered by a real
incident earlier the same session: running `export_json.py` to publish one new
dictionary term silently nulled dossier prose on 28 study topics and stripped
`related_works` / `related_letters` / `related_exegesis_entries` from
`biography/events.json`. Caught only because `git diff --stat` showed 1,393 changed
files.

## Corpus searched

Not a text corpus this time — the pipeline itself.

- All 46 scripts under `scripts/` that reference `site/public/data`
- All destructive SQL (`DELETE FROM`, `DROP TABLE`, `UPDATE … SET`) across the pipeline
- `database/unified_schema.sql` vs. the live `sqlite_master`
- `scripts/build_all.py` stage graph
- The six post-export cleaning passes
- The `merge_*.py` family and their (missing) source files

**Not searched:** the `.claude/worktrees/` copies; runtime behaviour of the
LLM-enrichment stages, which were not executed.

## Method

Rather than reasoning about the code, I measured. `scripts/safeguard/audit_regeneration.py`
runs every exporter into a throwaway directory and diffs the result against the live
tree field by field. Read-only; it never writes to `site/public/data`.

## Discoveries

- **(B) `site/public/data` is not a generated artifact.** 43 scripts write into it;
  only 2 are exporters. The rest are enrichment, merge, cleaning and repair passes that
  write editorial prose into the exported JSON and never back into the database.
- **(B) A full regeneration would damage 1,048 of 2,704 files** and fail to produce
  376 at all. 426 distinct field paths are orphaned.
- **(B) 673 Exegesis close readings exist only in the exported JSON.** The database has
  `concise_summary` for 207 segments; the export has 880. Spot-checked
  `SEG_EXEG_1975-11-05_SECTION_013_01`: a full scholarly reading of the Gene Savoy
  letter — summary, key claims, named entities, cited scriptures, evidence quotation —
  every field `NULL` in the database.
- **(B) Study-topic dossier prose is orphaned.** Written into the JSON by
  `merge_studies_topics.py` from `*.studies.json` files that are no longer in the
  repository. Confirmed by `find`: zero matches.
- **(B) Works pages carry content for slugs with no row in the `works` table**, and
  fields (`critical_caution`) the table has no column for. `exegesis/works/*.json`
  has no backing table at all.
- **(B) `CLM_*` claim ids live in the database's own `terms.definition`** and are
  stripped only after export. Exporting without the cleaning pass republishes them.
- **(B) Three segment JSON files are already malformed** and do not parse:
  `Dorothy_214`, `SECTION_016_129`, `Pat_149`. Their pages are broken on the live site.

## Interpretations

**(D)** The `CLAUDE.md` model — source → database → generated JSON → site — describes
an intention, not the repository. In practice the JSON is a working editorial store
that the database is a partial index of. Every safeguard here follows from taking the
actual topology seriously rather than the documented one.

## Decisions

- **Measure, don't assume.** The audit tool exists so the risk register is evidence,
  and so it can be re-derived after the pipeline changes.
- **Four layers, not one.** Commit guard (protects committed work), export guard
  (protects the working tree), snapshots (protect any state), curation directory
  (removes the orphaning at source). Rejected: rewriting the exporters to be more
  careful — the brief explicitly ruled it out, and it would not have protected the
  1,048 files whose content the exporters have no source for.
- **Auto-restore rather than refuse.** `safe_export.py` runs the export, then rolls
  back only what lost content. Refusing to export at all would have made the tool
  unusable, since every export is destructive today.
- **Array comparison by identity, not position.** First version false-alarmed on an
  insertion into a sorted array (`dictionary/index.json`). A guard that cries wolf gets
  disabled, so elements are now matched on `term_id` / `slug` / `seg_id` etc.
- **`--allow-path` rather than `--allow-destructive`.** A deliberate rewrite of one
  page should not require switching off protection for everything else.
- **Snapshots git-ignored, ledger committed.** 19.5 MB per snapshot is too much for
  git; losing the record of what was archived is worse than losing the payload.

## Files changed

- New: `scripts/safeguard/{snapshot,safe_export,check_data_diff,audit_regeneration,worklog}.py`
- New: `docs/{PRESERVATION,PRESERVATION_AUDIT,RESEARCH_WORKLOG}.md`, `docs/PRESERVATION_AUDIT_DATA.md`
- New: `archive/` tree, `curation/` tree, `.git/hooks/pre-commit`
- Modified: `.gitignore`, `scripts/clean_studies_claim_leaks.py` (crashed on
  `studies/index.json`, which is a list not a dict — pre-existing, hit while running
  the documented pipeline)

## Validation

- `safe_export.py --exporter studies` on a known-destructive regeneration: 28 topic
  dossiers detected as emptied and auto-restored; additive changes kept. Run three
  times across the session, same result.
- **Deliberate loss test:** planted a marker string in
  `studies/psychology/topics/trauma.json` — content existing *only* in the exported
  JSON — then ran a full studies regeneration. Marker survived. This is the exact
  failure mode from this morning, now non-silent and self-healing.
- `check_data_diff.py --worktree`: clean, after the identity-keying fix.
- Pre-commit hook installed and verified to fire.

## Artifacts archived

- `archive/snapshots/20260904T173141Z_baseline-before-preservation-work.zip`
  (2,724 files, 19.5 MB, includes 11,350 curated DB rows) plus five later snapshots;
  ledger at `archive/snapshots/INDEX.md`
- `archive/2026-09-04/reports/2026-09-04_regeneration-loss-audit.md`

## Unresolved

- The orphaned fields are protected but not fixed. Round-tripping the 673 close
  readings, the dossier prose and the biography relations into `unified.sqlite` is the
  real repair and has not been attempted.
- The three malformed segment files are untouched; repairing them means reconstructing
  content that may itself be irreplaceable.
- Snapshots are local to this machine.
