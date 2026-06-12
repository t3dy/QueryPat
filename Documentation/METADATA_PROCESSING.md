# Metadata Processing System

This document defines how QueryPat enriches its source catalog with **locations**,
**themes**, and **summaries**, and — critically — how it avoids re-reading a novel,
story, letter, or Exegesis chunk that has already been processed.

It exists so any future session can answer, in one command, *"what is already cooked
in, and what still needs doing?"* before touching a source.

---

## 1. The anti-re-reading system

Two layers, by design:

### 1a. Derived coverage (the source of truth)
`scripts/processing/coverage.py` computes coverage **directly from the data the site
serves** (`site/public/data/`). A source unit counts as processed only if the metadata
is actually present in the exported JSON — so the report can never drift from reality.

```bash
python3 scripts/processing/coverage.py                 # summary table
python3 scripts/processing/coverage.py --remaining exegesis    # seg_ids still to summarize
python3 scripts/processing/coverage.py --remaining works       # works missing locations
python3 scripts/processing/coverage.py --remaining biography   # events missing a location
python3 scripts/processing/coverage.py --check-ledger          # ledger vs. data
```

**Rule:** before reading any source to extract metadata, run `--remaining` for that
domain and work only the units it lists. Never re-open a unit that is not listed.

### 1b. Declared read-ledger (`scripts/processing/ledger.json`)
Some facts can't be derived from the output — chiefly *"has this full text been read at
all,"* and *"is the source text even available in this environment."* The ledger records,
per source unit: `type`, `source_text_available`, a `passes` map
(`locations` / `themes` / `summary` / `themes_figures` / `chapter_summaries` →
`done|partial|pending|blocked|n/a`), a free-text `note`, and `updated`.

`coverage.py --check-ledger` flags contradictions (e.g. a pass marked `done` on a unit
whose source text is unavailable).

When you finish a pass on a full-text source, update its ledger entry in the same commit.

---

## 2. Source-text availability (the hard constraint)

The repository deliberately excludes large copyrighted source materials
(`.gitignore`: `database/extracted_markdown/`, `PKD stuff to add/`) and the SQLite DB
(`database/unified.sqlite`) that the JSON is exported from. In a fresh clone:

| Source | Text available here? | What is groundable now |
|---|---|---|
| **Exegesis** | ✅ `exegesis_ordered.txt` + `raw_text` in 882/1107 segment JSONs | Per-segment summaries with full theme/figure tagging |
| **Novels & stories** | ❌ full texts gitignored/external | Work-LEVEL locations + themes (from documented settings/scholarship). **Chapter summaries are blocked** — they would require the texts. |
| **Letters** | ⚠️ volumes external; hand-extracted batches + letters quoted inside the Exegesis are usable | Letter events already extracted; location tagging where text exists |
| **Biography** | ✅ structured event records | Per-event locations (a string field) |

> Producing chapter-level fiction summaries **without** the source text would mean
> fabricating, which violates the project's evidence discipline. Such passes are marked
> `blocked` in the ledger until a session has the texts (or `extracted_markdown/` is
> regenerated from the source PDFs).

---

## 3. Metadata schema

### 3a. Exegesis segments (`site/public/data/segments/SEG_*.json`)
Fields (all already in the `segments` schema; populate the nulls):

| Field | Type | Contents |
|---|---|---|
| `concise_summary` | string | 2-5 sentence prose summary. Italicize work titles (`*Ubik*`). |
| `key_claims` | string[] | The segment's distinct assertions, often `Label: explanation`. |
| `recurring_concepts` | string[] | The motifs this chunk turns on. |
| `people_entities` | string[] | **Every** person, deity, figure, or named dream-entity mentioned. |
| `texts_works` | string[] | Every text/work cited (scripture, philosophy, PKD's own fiction). |
| `theological_motifs` | string[] | **Every** theological *or philosophical* theme/figure — this list is meant to be exhaustive per the editorial direction. |
| `symbols_images` | string[] | Concrete images, dream-objects, and symbols. |
| `tensions` | string[] | The contradictions/oppositions the chunk holds open. |

The 224 segments lacking `raw_text` need their text recovered (from
`exegesis_ordered.txt` by date/position, or a DB re-export) before they can be summarized.

### 3b. Works catalog (`site/public/data/works/*.json`)
- `themes` (string[]) — already present on 46 works; vocabulary is the existing controlled
  set (`reality-breakdown`, `illusionary-realities`, `empire-control`, `authentic-human`,
  `time`, `religion-gnosis`, `suburbia-domesticity`, …). Reuse before coining new tags.
- **`locations`** (object[]) — **new** field. Each: `{ "name", "kind" (real|fictional|
  composite), "real_world" (geocodable place or null), "lat", "lng", "role" (primary|
  secondary|mentioned), "note" }`. Work-level settings, groundable from documented
  scholarship. These can feed the geography map alongside `pkdGeography.ts`.

### 3c. Biography events (`site/public/data/biography/{events,curated}.json`)
- `location` (string) — already a per-event field; fill the 198 `events.json` gaps.

---

## 4. Workflow for a processing pass

1. `python3 scripts/processing/coverage.py` — read the current state.
2. Pick a domain and get its TODO list: `--remaining {exegesis|works|biography}`.
3. Confirm `source_text_available` for the unit in `ledger.json`. If `false`, the
   summary/chapter pass is **blocked** — do the groundable passes only.
4. Read the source text (segment `raw_text`, or `exegesis_ordered.txt`), extract metadata
   into the schema above, write it into the exported JSON.
5. Update the unit's `ledger.json` entry; re-run `coverage.py` to confirm the count moved.
6. Commit data + ledger together.

For scale, the per-segment work parallelizes cleanly: hand a worker a contiguous
`--remaining exegesis` range and the schema in §3a; the coverage tool reconciles the
result regardless of who produced it.

---

## 5. Status at last update (2026-06-12)

- Exegesis: 213 / 1107 summarized; 670 processable (have `raw_text`); 224 blocked on text.
- Works: 0 / 149 carry `locations` (greenfield); 46 carry `themes`.
- Biography: 489 / 687 events and 162 / 162 curated events carry a location.
- Exemplar batch landed: `SECTION_013` positions 1-6 (1975-11-05, the Gene Savoy /
  St. Sophia cluster), establishing the §3a schema.
