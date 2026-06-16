# artifacts/

Staged scholarly data pipeline for QueryPat. Every LLM-assisted workflow produces durable,
typed, inspectable artifacts at each stage — extraction → validation → ontology tagging →
interpretation → curation → public writing — instead of jumping from source material to prose.

Full specification: **`Documentation/ARTIFACT_PIPELINE.md`**.
Agent rules: **`Documentation/AGENT_ARTIFACT_RULES.md`**.
Curation criteria: **`Documentation/CURATION_CRITERIA.md`**.

## Layout

- `schemas/` — JSON Schema (Draft 2020-12), one per artifact type, plus
  `controlled_vocabulary.json`.
- `fixtures/` — worked example artifacts (a full chain for `DOC_ARCH_1974_ROLLING_STONE`,
  plus `text_comparison` and `scholar_citation` examples). These are validated by the tests.
- `generated/` — production output, one subdir per `source_id` (empty in git; populated at build).
- `artifact_types.py` — the registry: artifact types, agent produce/consume roles, and helpers
  (`make_artifact_id`, `utc_now`, `write_artifact`).
- `validate_artifacts.py` — schema + contract validator (CLI and test entrypoint).

## Validate

```bash
python artifacts/validate_artifacts.py            # validate fixtures/ + generated/
python artifacts/validate_artifacts.py <path...>  # validate specific dirs/files
```

Uses `jsonschema` if installed, otherwise a built-in stdlib validator (no hard dependency).
Exit code 0 = all pass (warnings allowed), 1 = at least one failure.

## Mint and write an artifact (Python)

```python
from artifacts import artifact_types as at   # or: import artifact_types (run from artifacts/)

art = {
    "artifact_id": at.make_artifact_id("raw_extraction", "DOC_ARCH_1974_ROLLING_STONE", "S001"),
    "artifact_type": "raw_extraction",
    "schema_version": at.SCHEMA_VERSION,
    "generated_at": at.utc_now(),
    "source_id": "DOC_ARCH_1974_ROLLING_STONE",
    "generated_by": {"agent_role": "extraction_agent", "name": "my_script.py",
                     "model": "claude-sonnet-4-6", "prompt_version": "raw_extraction.v1"},
    "extraction_scope": "pages 1-3",
    # ... stage-specific fields ...
    "_filename": "raw_extraction.section-001.json",
}
at.write_artifact(art)   # -> artifacts/generated/DOC_ARCH_1974_ROLLING_STONE/raw_extraction.section-001.json
```
