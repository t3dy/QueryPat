# Artifact Pipeline

QueryPat treats scholarly content production as a **staged pipeline of durable, typed,
inspectable artifacts**, not as a jump from source material to polished prose. Each stage
has its own schema, storage location, validation rules, and explicit downstream consumers.

```
source material
  → SourceMetadataArtifact      (A) ingested object, before interpretation
  → RawExtractionArtifact       (B) what the source explicitly says, with locators
  → ValidationArtifact          (C) is the extraction grounded, complete, schema-valid?
  → OntologyTaggingArtifact     (D) map onto controlled vocabulary (classify, do not write)
  → InterpretiveArtifact        (E) bounded scholarly readings, each with evidence
  → CurationArtifact            (F) should this appear? how? (portal + news aggregator)
  → PublicProseArtifact         (G) reader-facing prose, generated FROM prior artifacts
```

Two specialized types attach to the backbone:

- **TextComparisonArtifact (H)** — compare two versions of a text (edition vs edition,
  draft vs published, e.g. *Radio Free Albemuth* vs *VALIS*, or Agrippa 1510 vs 1533).
- **ScholarCitationArtifact (I)** — capture what a scholar says about a text/passage/issue;
  feeds `InterpretiveArtifact.evidence_links` as a lane-C source.

## Why stages are not collapsed

The point is the **evidence trail**. An agent that reads a PDF and emits an essay leaves no
inspectable record of *what was actually in the source* vs *what was inferred* vs *what was
editorialised*. Splitting description (B), classification (D), interpretation (E), and editorial
work (F, G) into separate durable artifacts means every public sentence can be traced back to a
located claim in a source — or flagged as speculative.

This complements the existing editorial spine in `PKDontology.md` (evidentiary lanes A–E,
fact-vs-interpretation rule, contradiction registry). The artifact pipeline is the *mechanism*
that operationalises those rules per item.

## Storage layout

```
artifacts/
  schemas/                       JSON Schema (Draft 2020-12), one per artifact type
    source_metadata.schema.json
    raw_extraction.schema.json
    validation.schema.json
    ontology_tagging.schema.json
    interpretive.schema.json
    curation.schema.json
    public_prose.schema.json
    text_comparison.schema.json
    scholar_citation.schema.json
    controlled_vocabulary.json   shared vocabularies (lanes, esoteric domains, methods, ...)
  fixtures/                      worked example artifacts (validated by tests)
  generated/                     production output, one subdir per source_id
    <source_id>/
      source_metadata.json
      raw_extraction.section-001.json
      validation.raw_extraction.section-001.json
      ontology_tagging.section-001.json
      interpretive.section-001.json
      curation.json
      public_prose.draft.json
  artifact_types.py              registry: types, agent roles, id/timestamp helpers, writer
  validate_artifacts.py          schema + contract validator (CLI + test entrypoint)
```

`artifacts/generated/<source_id>/` mirrors how the existing pipeline already keys everything
by stable IDs (`DOC_ARCH_…`, `WORK_…`, `THEO_…`, `PERSON_…`). The `fixtures/` chain is a fully
worked example for the real source `DOC_ARCH_1974_ROLLING_STONE`.

## Artifact principles (enforced or documented)

1. **Durable** — written to `artifacts/generated/<source_id>/`, not passed transiently.
2. **Typed** — every artifact has `artifact_type` (validated against a known set).
3. **Versioned** — every artifact has `schema_version` and `generated_at`.
4. **Provenance** — `source_id` + `generated_by` on every artifact; `source_uri`/`local_path`/
   `source_title` on the SourceMetadataArtifact.
5. **Evidence** — claims point back to source locations via the shared `evidence_location`
   object (page / section / paragraph / line / timestamp / url_fragment / excerpt).
6. **Separated work** — description (B), classification (D), interpretation (E), and editorial
   (F, G) are different artifacts.
7. **Reusable** — later stages consume prior artifact IDs (`input_artifact_id(s)`), not the raw source.
8. **Validatable** — `validate_artifacts.py` checks every artifact (see Testing).
9. **Inspectable** — readable JSON; prose lives in named fields, not as the whole artifact.
10. **No prose bloat** — structured fields first; prose summaries are specific fields.

## The artifact contract

- No artifact may omit `artifact_id`, `artifact_type`, `schema_version`, `source_id`, and
  `generated_at` unless there is a specific documented reason.
- No interpretive artifact may include a claim without `evidence_links`, `confidence`, and
  `limitations` — *or* the claim must be explicitly marked `speculative`.
- No public-prose artifact may be marked `reviewed` or `published` unless its
  `input_artifact_ids` include at least one **extraction** artifact and one **validation** artifact.
- No curation artifact may mark an item `publish` or `feature` without `reasons_for_inclusion`.
- Validation **warnings** do not block work; validation **failures** prevent publishing
  (a `published` prose artifact for a source with a `fail` validation is a contract violation).
- Public prose must be generated from prior artifacts, **not** directly from unstructured
  source material, except in explicitly marked `prototype_mode` (which can never be
  `reviewed`/`published`).

All of the above are checked by `validate_artifacts.py`.

## The news-aggregator pipeline

For curated podcast / article / video items the same backbone applies, abbreviated:

```
podcast/article/video source
  → SourceMetadataArtifact     (source_type: podcast_episode | youtube_video | article | webpage)
  → RawExtractionArtifact      (from title / description / transcript / body, with timestamp/url locators)
  → OntologyTaggingArtifact    (tags + content_class signals)
  → CurationArtifact           (relevance_status + content_class: serious vs pop-occult/spam)
  → PublicProseArtifact        (a link card)
```

The **link card** is a `PublicProseArtifact` whose fields carry: `title`, source (in
`citations_or_source_links`), date (`generated_from`/source metadata), URL, `summary`
("short summary"), `tags`, an editorial "why it matters" line (`dek_or_short_description`),
relevance status (from the linked CurationArtifact), and an optional editorial note
(`revision_notes`). See `Documentation/CURATION_CRITERIA.md` for how the aggregator separates
serious historical/scholarly esoteric studies content from pop-occult lifestyle, vague
spirituality, AI spam, and low-relevance pop content.

## Writing standard for public prose

Public prose generated at stage G should be: accessible to intelligent non-specialists;
grounded in evidence (every claim traceable to a prior artifact); neutral but not bland;
historiographically aware; clear about uncertainty; resistant to overinterpretation; and
explicit about the line between source description and scholarly interpretation. The worked
fixture `fixtures/example_public_prose.json` is deliberately written this way (it states what
the source *is*, refuses to assert what the unread article *says*, and surfaces a dating
discrepancy rather than smoothing it over).

## Testing

```
python artifacts/validate_artifacts.py            # validate fixtures/ + generated/
python artifacts/validate_artifacts.py <path...>  # validate specific dirs/files
```

The validator uses `jsonschema` if installed and otherwise falls back to a built-in
stdlib validator, so it runs in the dependency-light environment the rest of `scripts/` assumes.
It checks: schema validity per type; the 5 core contract fields; unique `artifact_id`s;
interpretive claims carry evidence or are speculative; curation publish/feature carries reasons;
reviewed/published prose references an extraction + a validation artifact; no unknown
`artifact_type`; and that a `fail` validation blocks publishing for that source.
