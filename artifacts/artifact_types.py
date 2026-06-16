#!/usr/bin/env python3
"""
Artifact registry + helpers for the QueryPat staged scholarly data pipeline.

This module is the single source of truth for:
  - the known artifact types and which schema validates each,
  - the agent roles and the produce/consume contract between stages,
  - small helpers for minting artifact_ids and stamping `generated_at`.

It deliberately has no third-party dependencies (stdlib only), matching the
rest of the scripts/ pipeline. See Documentation/ARTIFACT_PIPELINE.md and
Documentation/AGENT_ARTIFACT_RULES.md for the prose specification.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ARTIFACTS_DIR = Path(__file__).resolve().parent
SCHEMAS_DIR = ARTIFACTS_DIR / "schemas"
FIXTURES_DIR = ARTIFACTS_DIR / "fixtures"
GENERATED_DIR = ARTIFACTS_DIR / "generated"

SCHEMA_VERSION = "1.0"
ONTOLOGY_VERSION = "1.0"

# artifact_type -> schema filename
ARTIFACT_TYPES = {
    "source_metadata": "source_metadata.schema.json",
    "raw_extraction": "raw_extraction.schema.json",
    "validation": "validation.schema.json",
    "ontology_tagging": "ontology_tagging.schema.json",
    "interpretive": "interpretive.schema.json",
    "curation": "curation.schema.json",
    "public_prose": "public_prose.schema.json",
    "text_comparison": "text_comparison.schema.json",
    "scholar_citation": "scholar_citation.schema.json",
    "chapter_summary": "chapter_summary.schema.json",
    "exegesis_chunk_analysis": "exegesis_chunk_analysis.schema.json",
    "letter_annotation": "letter_annotation.schema.json",
}

# Pipeline order (linear backbone; specialized types attach where noted).
PIPELINE_ORDER = [
    "source_metadata",
    "raw_extraction",
    "validation",
    "ontology_tagging",
    "interpretive",
    "curation",
    "public_prose",
    "chapter_summary",
    "exegesis_chunk_analysis",
    "letter_annotation",
]

# agent_role -> {produces: [...], consumes: [...]}
# Enforced narratively by docs; checked structurally by validate_artifacts.py.
AGENT_ROLES = {
    "extraction_agent": {
        "produces": ["raw_extraction"],
        "consumes": ["source_metadata"],
    },
    "validation_agent": {
        "produces": ["validation"],
        "consumes": ["raw_extraction", "ontology_tagging", "interpretive", "public_prose"],
    },
    "ontology_agent": {
        "produces": ["ontology_tagging"],
        "consumes": ["raw_extraction"],
    },
    "interpretation_agent": {
        "produces": ["interpretive"],
        "consumes": ["raw_extraction", "ontology_tagging", "scholar_citation"],
    },
    "curation_agent": {
        "produces": ["curation"],
        "consumes": ["source_metadata", "ontology_tagging", "interpretive"],
    },
    "writing_agent": {
        "produces": ["public_prose"],
        "consumes": ["interpretive", "curation", "ontology_tagging", "raw_extraction", "validation"],
    },
    "comparison_agent": {
        "produces": ["text_comparison"],
        "consumes": ["source_metadata", "raw_extraction"],
    },
    "bibliography_agent": {
        "produces": ["scholar_citation"],
        "consumes": ["source_metadata"],
    },
    "reading_notes_agent": {
        "produces": ["chapter_summary", "exegesis_chunk_analysis", "letter_annotation"],
        "consumes": ["source_metadata"],
    },
}

# Fields every artifact must carry (the "artifact contract" core).
REQUIRED_CONTRACT_FIELDS = [
    "artifact_id",
    "artifact_type",
    "schema_version",
    "source_id",
    "generated_at",
]


def utc_now() -> str:
    """RFC3339 / ISO-8601 UTC timestamp for `generated_at`."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def make_artifact_id(artifact_type: str, source_id: str, discriminator: str = "") -> str:
    """Mint a stable, unique-by-construction artifact_id.

    e.g. make_artifact_id("raw_extraction", "DOC_ARCH_1974_ROLLING_STONE", "S001")
         -> "ART_RAW_EXTRACTION_DOC_ARCH_1974_ROLLING_STONE_S001"
    """
    if artifact_type not in ARTIFACT_TYPES:
        raise ValueError(f"Unknown artifact_type: {artifact_type!r}")
    parts = ["ART", artifact_type.upper(), source_id]
    if discriminator:
        parts.append(discriminator)
    return "_".join(parts)


def load_schema(artifact_type: str) -> dict:
    fname = ARTIFACT_TYPES[artifact_type]
    return json.loads((SCHEMAS_DIR / fname).read_text(encoding="utf-8"))


def write_artifact(artifact: dict, base_dir: Path | None = None) -> Path:
    """Persist an artifact to artifacts/generated/<source_id>/<filename>.json.

    Filenames follow the convention in ARTIFACT_PIPELINE.md, e.g.
    raw_extraction.section-001.json, validation.raw_extraction.section-001.json.
    The caller supplies the trailing filename via artifact['_filename'] if it
    needs a non-default name; otherwise <artifact_type>.json is used.
    """
    base_dir = base_dir or GENERATED_DIR
    source_id = artifact["source_id"]
    filename = artifact.pop("_filename", f"{artifact['artifact_type']}.json")
    out_dir = base_dir / source_id
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / filename
    out_path.write_text(json.dumps(artifact, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return out_path


if __name__ == "__main__":
    print(f"schema_version={SCHEMA_VERSION} ontology_version={ONTOLOGY_VERSION}")
    print(f"{len(ARTIFACT_TYPES)} artifact types:")
    for t, f in ARTIFACT_TYPES.items():
        print(f"  - {t:18s} -> schemas/{f}")
    print(f"{len(AGENT_ROLES)} agent roles defined.")
