# generated/

Production artifacts land here, one subdirectory per `source_id`. This directory is kept empty
in git (only this README and `.gitkeep`); it is populated when the pipeline runs.

Filename convention within `generated/<source_id>/`:

```
source_metadata.json
raw_extraction.section-001.json
validation.raw_extraction.section-001.json
ontology_tagging.section-001.json
interpretive.section-001.json
curation.json
public_prose.draft.json
```

For a fully worked example of this chain, see `artifacts/fixtures/` — it implements the
complete pipeline for the real source `DOC_ARCH_1974_ROLLING_STONE`.

Validate anything written here with:

```bash
python artifacts/validate_artifacts.py artifacts/generated
```
