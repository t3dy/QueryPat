# Rule: validating a change

Run what applies. All of these exist. As of 2026-10-30 they pass on `main`
except `validate_artifacts.py`, which reports 1,009 failures among 1,381 staged
artifacts (mostly a missing `schema_version` and chapter-summary schema drift) —
a pre-existing state, so judge a change by whether it adds failures.

| Change | Check |
|---|---|
| Any `site/public/data` change | `python scripts/safeguard/check_data_diff.py --worktree` |
| A study dossier | `python scripts/studies/seed_<topic>.py --check` (anchors, verbatim piths and essay quotes, citations, facets, contradictions) |
| Biography curation | `python scripts/biography/apply_biography_curation.py --verify`, and `--audit` for every quote on the page |
| Staged LLM artifacts | `python artifacts/validate_artifacts.py` |
| Corpus-wide counts and anomalies | `python scripts/audit.py` (writes `audit_report.md` / `.json` in the checkout it runs from; before 2026-10-30 it always used `C:/QueryPat`) |
| Frontend | `npm run build --prefix site` (typecheck + build) |
| Anything rendered | Open it in the preview (see `environment.md`): the page, its citations and filters, the browser console |

There is no automated test suite for retrieval yet; CLAUDE.md's earlier
`tests/semantic_memory` and `scripts/validate_semantic_memory.py` do not exist.
