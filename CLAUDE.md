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
| Exported JSON | `site/public/data/` | **Generated — never edit** |
| Site | `site/src/` | Renders exports only |

`database/unified.sqlite` is git-ignored and rebuilt by `scripts/build_all.py`.

> **Known drift:** the live database contains tables absent from
> `unified_schema.sql` — `claims`, `claim_subjects`, `claim_relations`,
> `letters`, `theophanies`, `theophany_evidence`, `document_topics`,
> `study_topic_claims`, `letter_events_candidate`. Always inspect the live
> schema with `sqlite_master`, never trust the `.sql` file alone.

## Never do these

1. **Never edit anything in `site/public/data/`.** It is generated from the
   database. Edit the source and re-export.
2. **Never promote an LLM output to canonical knowledge in one step.** It enters
   as a candidate with provenance and a status, and an editorial pass promotes
   it. See `.claude/rules/semantic-memory.md`.
3. **Never resolve a contradiction to make retrieval cleaner.** Disagreement
   between sources is the data, not a defect.
4. **Never collapse evidentiary lanes.** Fiction is not testimony.
5. **Never make embeddings the canonical layer.** They are an optional
   retrieval signal over canonical rows.
6. **Never drop or rename an existing ID.** `TERM_*`, `NAME_*`, `SEG_*`,
   `DOC_*`, `EV_*`, `CLAIM_*` are referenced by exports and by the public site.

## Route by task

| If you are working on… | Read |
|---|---|
| Database, schema, migrations | `.claude/rules/architecture.md`, `.claude/rules/data-provenance.md` |
| Semantic memory (concepts, claims, episodes, edges) | `.claude/rules/semantic-memory.md` |
| Search, ranking, retrieval | `.claude/rules/retrieval.md` |
| Anything under `site/public/data/` or `artifacts/generated/` | `.claude/rules/generated-files.md` |
| Provenance, lanes, confidence, review states | `.claude/rules/data-provenance.md` |
| Tests, golden queries, validation | `.claude/rules/testing.md` |
| The site's community/comment features | `USERSNEXTSTEPS.md`, `supabase/schema.sql` |

Compact task context packs live in `.claude/context/` — load the smallest one
that covers your task rather than reading all of `docs/`.

Long-form architecture lives in `docs/`:
`ARCHITECTURE.md`, `SEMANTIC_MEMORY_ARCHITECTURE.md`, `DATA_FLOW.md`,
`ONTOLOGY.md`, `RETRIEVAL.md`, `PROVENANCE.md`, `MEMORY_CONSOLIDATION.md`.

## How to validate a change

```bash
python scripts/validate_semantic_memory.py     # semantic memory integrity
python artifacts/validate_artifacts.py         # staged artifact contracts
python scripts/audit.py                        # corpus-wide data audit
npm run build --prefix site                    # site typecheck + build
```

If you changed retrieval, also run the golden-query regression:

```bash
python -m pytest tests/semantic_memory -q
```

## When you learn something architectural

Write it down where it will outlive this conversation: a rule file if it
constrains future work, a `docs/` page if it explains the system, and
`HANDOVER_SEMANTIC_MEMORY.md` if it changes what someone should do next.
Chat and commit messages are not memory.
