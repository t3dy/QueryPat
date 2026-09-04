# Preservation architecture

Why this exists: [`PRESERVATION_AUDIT.md`](PRESERVATION_AUDIT.md). The short
version is that `site/public/data` is not a disposable build artifact. It holds
673 Exegesis close readings, the study-topic dossier prose, biography relations
and works pages that exist **nowhere else**, and a naive re-export deletes them.

## The rule

> Generated artifacts may be regenerated. Research and editorial artifacts are
> append-only, versioned and archived unless a destructive operation is
> deliberately requested.

Until every orphaned field is round-tripped into the database, treat any
populated field in `site/public/data` as potentially irreplaceable.

## Four layers

| Layer | Protects | Mechanism |
|---|---|---|
| 1. Commit guard | committed scholarship | `pre-commit` hook refuses commits that remove content |
| 2. Export guard | uncommitted working tree | `safe_export.py` snapshots, exports, diffs, auto-restores |
| 3. Snapshots | any state, at any time | timestamped manifested zips + committed ledger |
| 4. Archive & worklog | the research process | `archive/<date>/`, `curation/` |

### Layer 1 — commit guard

```bash
python scripts/safeguard/check_data_diff.py --install-hook
```

Compares staged `site/public/data` against `HEAD` and refuses the commit if any
file is deleted, any JSON array loses a keyed entry, any populated field is
emptied, any long text field is halved, any file stops parsing, or any `CLM_*`
id leaks into reader-facing prose. Arrays are matched by identity
(`term_id`, `slug`, `seg_id`, …), so inserting or reordering entries is not
mistaken for loss.

Check without committing:

```bash
python scripts/safeguard/check_data_diff.py --worktree
```

Bypass, deliberately and for one commit only: create `.allow-data-loss`, or
`git commit --no-verify`.

### Layer 2 — export guard

**Never run `export_json.py` or `export_studies.py` directly.** Use:

```bash
python scripts/safeguard/safe_export.py --exporter studies
python scripts/safeguard/safe_export.py --exporter json
python scripts/safeguard/safe_export.py --exporter all
```

It snapshots the data tree (plus curated DB tables), runs the exporter, runs the
six post-export cleaning passes, diffs the result field by field, and
**restores every file that lost content** while keeping additive changes. A
verified live example: `--exporter studies` nulls the dossier prose on 28
psychology and AI topics; the guard detects and rolls back all 28 while keeping
the new Burroughs topic and the new passage fields.

Audit the working tree against the newest snapshot without exporting:

```bash
python scripts/safeguard/safe_export.py --report-only
```

Keep destructive changes only when they are genuinely intended:

```bash
python scripts/safeguard/safe_export.py --exporter json --allow-destructive
```

### Layer 3 — snapshots

```bash
python scripts/safeguard/snapshot.py --label "before X" --include-db
python scripts/safeguard/snapshot.py --list
python scripts/safeguard/snapshot.py --restore 20260904T173141Z_baseline
python scripts/safeguard/snapshot.py --restore <name> --only path/a.json path/b.json
```

Each snapshot is a zip under `archive/snapshots/` containing every data file, a
`manifest.json` with per-file SHA-256 hashes and the git HEAD it was taken at,
and — with `--include-db` — newline-delimited dumps of the 18 curated tables.
About 19 MB per snapshot, so the zips are git-ignored;
`archive/snapshots/INDEX.md` is committed, so the ledger of what was archived
and when survives in git even though the payloads do not.

### Layer 4 — archive and curation

```
archive/
  snapshots/          zips + committed INDEX.md ledger
  YYYY-MM-DD/
    worklog/          one record per substantive research session
    prompts/          the instructions that produced the work
    research/         corpus sweeps, intermediate results, inventories
    drafts/           superseded prose, kept rather than overwritten
    reports/          validation and audit output
curation/
  <topic>/            durable, human-editable source of truth for editorial
                      content, read by the seeders that write the database
```

`curation/` is the structural fix for the orphaning problem. Editorial
discoveries belong there — versioned in git, readable without a database — and
the database and exported JSON are both derived from it. A page whose content
lives only in `site/public/data` is one bad export from being gone.

## Regenerating the audit

```bash
python scripts/safeguard/audit_regeneration.py --write-report
```

Runs every exporter into a throwaway directory and reports what a real
regeneration would destroy. Read-only; it never touches `site/public/data`.

## Workflow

```bash
# before a risky operation
python scripts/safeguard/snapshot.py --label "before <thing>" --include-db

# regenerate safely
python scripts/safeguard/safe_export.py --exporter all

# verify before committing
python scripts/safeguard/check_data_diff.py --worktree
git diff --stat site/public/data
```

A `git diff --stat site/public/data` of hundreds of files means an export ate
curated work. Investigate before committing.

## Known gaps

- Orphaned fields are protected but not yet *fixed*: the database still is not
  the source of truth for the close readings, dossier prose or biography
  relations.
- Snapshots are local to the machine.
- `--allow-destructive` and `--no-verify` remain available by design.
- Three segment JSON files are already malformed and do not parse; see the
  audit's R10.
