# Curation: Philip K. Dick and the Bible

Durable source of truth for `/studies/intertexts/pkd-and-the-bible` and for the
dictionary entries it owns (`bible`, and the promoted `revelation`, `malachi`,
`qumran`). The database and the exported JSON are derived from here.

| File | What it is | Edit? |
|---|---|---|
| `findings.py` | Every published passage: source, verbatim anchor, window, card summary, verbatim pith, date and dating basis, books/themes. Evidence packets. | **Yes** — hand-curated |
| `dossier_sections.py` | Essay sections with `{{finding-id}}` citations, browse groups and facets, contradictions, open questions, structured fields. | **Yes** — hand-authored |
| `evidence-inventory.json` | Generated from `findings.py` by `build_inventory.py`. Same shape as the Burroughs inventory. | No |
| `dossier.json` | Generated from `dossier_sections.py` by `build_dossier.py`. | No |

The raw corpus sweep is not kept here (it is ~30 MB). Its strong tier is archived
at `archive/2026-10-29/research/2026-10-29_pkd-bible-raw-findings.json.gz`;
regenerate it with:

```bash
python scripts/research/sweep_corpus.py --profile bible --summary --out <file>
```

## Rebuild the page

```bash
python curation/pkd-bible/build_inventory.py
python curation/pkd-bible/build_dossier.py
python scripts/studies/seed_pkd_bible.py --check     # verify, write nothing
python scripts/studies/seed_pkd_bible.py
python scripts/safeguard/safe_export.py --exporter studies
```

`--exporter studies` rewrites every study topic; revert the ones you did not
mean to change (see CLAUDE.md, "Why the export is lossy"). The dictionary
entries need `export_json`, which is lossy across the whole dictionary — export
to a temporary directory and hand-place `dictionary/terms/{bible,revelation,
malachi,qumran}.json` and their `dictionary/index.json` rows instead.

## What the seeder enforces

It refuses to build if any anchor fails to resolve, any card pith or any essay
quotation of 40+ characters is not verbatim in its source, any `{{id}}` citation
does not resolve, any browse facet matches no card, or any contradiction's
passages cannot be found.

## Conventions

- **Lanes.** A fiction (characters speaking), B Exegesis, C scholarship,
  D biography (Sutin), E letters, interviews and the 1978 speech.
- **Facets.** A card's `concepts` list is its facet vocabulary: books of the
  Bible first, then themes, editions and Dick's works. The facet list in
  `dossier_sections.py` decides which are browsable chips and where each links.
- **Dating.** Per passage, with a basis: `dateline` (letters), `record` (our
  container date — weak), `folder`, `stamp`, `publication`. Exegesis section 016
  carries the container date 1978-10-10 but runs to late 1980; its passages are
  dated "1978–80" unless a stamp or folder narrows them.
- **Not used.** The 348 machine-extracted `claims` rows that mention the Bible
  are unreviewed rule output and are not cited on the page.
