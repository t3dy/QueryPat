# Agent Artifact Rules

Rules for any agent (human or LLM) that contributes to the QueryPat data pipeline.
These govern **which artifact types each role may produce and consume**, and the hard
boundaries between stages. The canonical machine-readable version is `AGENT_ROLES` in
`artifacts/artifact_types.py`; this file is the prose specification.

See also `Documentation/ARTIFACT_PIPELINE.md` (the stages and contract) and `PKDontology.md`
(the editorial spine: lanes, fact-vs-interpretation, contradiction registry).

## The one non-negotiable rule

> **No agent may go from source material straight to public prose.**

Public prose (stage G) must be generated from prior artifacts. The only exception is an
explicitly marked `prototype_mode: true` PublicProseArtifact, which may exist as a `draft`
but may **never** be marked `reviewed` or `published`. Anything else is a contract violation
and will fail `validate_artifacts.py`.

## Role → produce / consume

| Agent role            | Produces             | Consumes (prior artifacts)                                    |
|-----------------------|----------------------|--------------------------------------------------------------|
| extraction_agent      | `raw_extraction`     | `source_metadata`                                            |
| validation_agent      | `validation`         | any target artifact (`raw_extraction`, `ontology_tagging`, `interpretive`, `public_prose`) |
| ontology_agent        | `ontology_tagging`   | `raw_extraction`                                            |
| interpretation_agent  | `interpretive`       | `raw_extraction` + `ontology_tagging` (+ `scholar_citation`) |
| curation_agent        | `curation`           | `source_metadata` + `ontology_tagging` + `interpretive`     |
| writing_agent         | `public_prose`       | prior artifacts (must include an extraction + a validation)  |
| comparison_agent      | `text_comparison`    | `source_metadata` + `raw_extraction`                        |
| bibliography_agent    | `scholar_citation`   | `source_metadata`                                           |

An agent **produces only the type(s) in its row**. If a workflow needs another type, hand off
to the appropriate role rather than letting one agent emit several stages at once — that is how
the evidence trail stays inspectable.

## Per-stage boundaries

- **Extraction agents** describe what is *present in the source*. They must **not** make
  high-level historiographical claims unless the source explicitly makes them. Empty is fine:
  if the source can't be read, say so (see the Rolling Stone fixture) rather than inventing.
  Every claim and important passage carries an `evidence_location`.
- **Validation agents** judge grounding, completeness, and schema-validity of a *target*
  artifact. They emit `pass` / `warn` / `fail`. They do not rewrite content.
- **Ontology agents** classify against the controlled vocabulary
  (`artifacts/schemas/controlled_vocabulary.json`). They **do not write public prose**.
- **Interpretation agents** make bounded readings. Every `interpretive_claim` must carry
  `evidence_links` + `confidence`, or be marked `speculative: true`. Always attribute a
  reading (`attributed_to`) and record `limitations`. Never adopt one of PKD's own theories,
  or a contested biographical claim, as settled (per `PKDontology.md` §3–§5).
- **Curation agents** decide inclusion and audience fit, and separate serious scholarship from
  pop-occult / spam (`content_class`). A `publish` or `feature` decision requires
  `reasons_for_inclusion`.
- **Writing agents** produce reader-facing prose only after the prior stages exist, and must
  list `input_artifact_ids` and `generated_from_artifacts`. To reach `reviewed`/`published`
  the inputs must include at least one extraction and one validation artifact, and no
  validation artifact for the source may be `fail`.

## Provenance every agent must stamp

Every artifact an agent writes carries:

- `artifact_id` (use `artifact_types.make_artifact_id(...)`),
- `artifact_type`, `schema_version` (`"1.0"`), `generated_at` (`artifact_types.utc_now()`),
- `source_id`,
- `generated_by`: `{ agent_role, name (script/agent), model, prompt_version }`.

Write with `artifact_types.write_artifact(artifact)` so files land in the conventional
`artifacts/generated/<source_id>/` location, then validate with `validate_artifacts.py`.

## Quick checklist before emitting any artifact

1. Am I allowed to produce this type in my role? (table above)
2. Did I consume the required prior artifact(s) by ID rather than re-reading the raw source?
3. Are the 5 core contract fields present?
4. Do my claims carry evidence locations / links, or are they marked speculative?
5. Did I keep description, classification, interpretation, and editorial work in their own
   artifacts?
6. Does `python artifacts/validate_artifacts.py` pass on what I wrote?
