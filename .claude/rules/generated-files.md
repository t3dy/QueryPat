# Rule: `site/public/data/` and `artifacts/generated/`

`site/public/data/` is nominally generated, but parts of it are the **only copy** of
curated work. Treat every file there as editorial until proven otherwise.

## What is generated, what is curated

| Path | Produced by | Edit how |
|---|---|---|
| `dictionary/`, `names/`, `segments/`, `archive/`, `search_index.json` | `scripts/export_json.py` + post-export passes | Write the DB, export to a scratch dir, hand-place only the files you meant to change |
| `studies/<study>/topics/*.json` | `scripts/studies/export_studies.py` | Same; a raw export **nulls machine-drafted topic prose** (`definition`, `pkd_relevance`, …) that exists only in the JSON |
| `studies/links.json` | `export_studies.export_links` | Export to scratch, diff, copy if it differs only by your topic |
| `studies/index.json` | `export_studies.export_studies_index` | **Hand-edit** the one study row; a DB without every study drops the others' rows |
| `biography/curated.json` | Nobody — hand-curated | `curation/biography/*.py` + `scripts/biography/apply_biography_curation.py --verify` (see `biography.md`) |
| `biography/events.json` | `export_json.py` (lossy: drops `related_works`, `related_letters`, `related_exegesis_entries`) | Do not regenerate |
| `essays/*.md` | Nobody — hand-written, no source elsewhere | Do not edit casually; corrections belong in the dossier that supersedes the essay |

## The procedure

1. Never run `export_json.py` or `export_studies.py` bare. Use
   `python scripts/safeguard/safe_export.py --exporter all`, or call the single
   exporter function you need into a scratch directory.
2. Diff the scratch output against the committed file. Copy it only if it differs
   by your change alone; otherwise hand-place the owned fields into the committed
   JSON, preserving its formatting (`json.dumps(obj, indent=2, ensure_ascii=False)`
   round-trips every studies file checked so far — assert it before writing).
3. Run the post-export passes from `POST_EXPORT_PASSES` in
   `scripts/safeguard/safe_export.py` — at least `index_study_search` after any
   study change.
4. `python scripts/safeguard/check_data_diff.py --worktree`.

## When the guard refuses

`check_data_diff.py` refuses any loss of content — removed entries, emptied
fields, shrunk text. A list entry corrected in place (same keys, most values
unchanged, nothing emptied) counts as an edit and passes, so ordinary
corrections need no override.
- An accidental regeneration: discard and redo by hand-placing.
- A reseed renumbered ids (`passage_id`, `contradiction_id`): the content is
  unchanged but the guard sees removals. Hand-place the small change instead of
  re-exporting.
- An intended removal (false-positive passages, a wrong source entry): write
  `.allow-data-loss` (git-ignored) listing only the affected paths relative to
  `site/public/data/`, commit, delete the file. Ask the owner first; never use
  `--no-verify`.
