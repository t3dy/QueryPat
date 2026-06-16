#!/usr/bin/env python3
"""
Validate QueryPat pipeline artifacts against their JSON Schemas and the
project "artifact contract".

Usage:
    python artifacts/validate_artifacts.py                 # validate fixtures/ + generated/
    python artifacts/validate_artifacts.py path/to/dir     # validate a specific tree
    python artifacts/validate_artifacts.py file1.json ...  # validate specific files

Exit code 0 = all pass (warnings allowed), 1 = at least one failure.

No third-party dependency is required: if `jsonschema` is importable it is used
for structural validation, otherwise a small built-in validator covers the
subset of JSON Schema these schemas use (type, required, properties,
additionalProperties:false, enum, const, items, $ref to local $defs, minItems,
minLength, maxLength, minimum, maximum, format date/date-time, pattern).

On top of structural validation it enforces the cross-artifact CONTRACT:
  - every artifact carries the 5 core contract fields
  - artifact_type is known
  - artifact_ids are globally unique
  - interpretive claims carry evidence_links + confidence, or are marked speculative
  - public_prose reviewed/published references >=1 extraction and >=1 validation artifact
  - curation publish/feature carries reasons_for_inclusion
  - validation 'fail' on an artifact blocks publishing of public_prose for that source
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ARTIFACTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ARTIFACTS_DIR))

from artifact_types import (  # noqa: E402
    ARTIFACT_TYPES,
    REQUIRED_CONTRACT_FIELDS,
    SCHEMAS_DIR,
    FIXTURES_DIR,
    GENERATED_DIR,
    load_schema,
)

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DATETIME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})$")


# ── Built-in minimal JSON Schema validator (fallback) ─────────────────────────

def _type_ok(value, t) -> bool:
    if t == "object":
        return isinstance(value, dict)
    if t == "array":
        return isinstance(value, list)
    if t == "string":
        return isinstance(value, str)
    if t == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if t == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if t == "boolean":
        return isinstance(value, bool)
    if t == "null":
        return value is None
    return True


def _resolve_ref(ref: str, root: dict):
    # only local refs like "#/$defs/foo"
    assert ref.startswith("#/"), f"unsupported $ref: {ref}"
    node = root
    for part in ref[2:].split("/"):
        node = node[part]
    return node


def _validate(value, schema, root, path, errors):
    if "$ref" in schema:
        schema = _resolve_ref(schema["$ref"], root)

    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: expected const {schema['const']!r}, got {value!r}")

    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: {value!r} not in enum {schema['enum']}")

    if "type" in schema:
        types = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(_type_ok(value, t) for t in types):
            errors.append(f"{path}: expected type {schema['type']}, got {type(value).__name__}")
            return  # further checks meaningless

    if isinstance(value, str):
        if "minLength" in schema and len(value) < schema["minLength"]:
            errors.append(f"{path}: shorter than minLength {schema['minLength']}")
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            errors.append(f"{path}: longer than maxLength {schema['maxLength']}")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append(f"{path}: does not match pattern {schema['pattern']}")
        fmt = schema.get("format")
        if fmt == "date" and not DATE_RE.match(value):
            errors.append(f"{path}: not a valid date (YYYY-MM-DD): {value!r}")
        if fmt == "date-time" and not DATETIME_RE.match(value):
            errors.append(f"{path}: not a valid date-time: {value!r}")

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: {value} < minimum {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{path}: {value} > maximum {schema['maximum']}")

    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errors.append(f"{path}: fewer than minItems {schema['minItems']}")
        if "items" in schema:
            for i, item in enumerate(value):
                _validate(item, schema["items"], root, f"{path}[{i}]", errors)

    if isinstance(value, dict):
        props = schema.get("properties", {})
        for req in schema.get("required", []):
            if req not in value:
                errors.append(f"{path}: missing required field '{req}'")
        if schema.get("additionalProperties") is False:
            for k in value:
                if k not in props:
                    errors.append(f"{path}: unexpected field '{k}'")
        for k, v in value.items():
            if k in props:
                _validate(v, props[k], root, f"{path}.{k}", errors)


def validate_structural(artifact: dict, schema: dict) -> list[str]:
    """Return list of structural error strings ([] = valid)."""
    try:
        import jsonschema  # type: ignore
        validator = jsonschema.Draft202012Validator(schema)
        return [f"{'/'.join(str(p) for p in e.path) or '<root>'}: {e.message}"
                for e in validator.iter_errors(artifact)]
    except ImportError:
        errors: list[str] = []
        _validate(artifact, schema, schema, "<root>", errors)
        return errors


# ── Artifact loading ──────────────────────────────────────────────────────────

def find_artifact_files(targets: list[Path]) -> list[Path]:
    files: list[Path] = []
    for t in targets:
        if t.is_dir():
            files.extend(sorted(t.rglob("*.json")))
        elif t.is_file() and t.suffix == ".json":
            files.append(t)
    # skip schema/vocab files if a schemas dir is accidentally included
    return [f for f in files if "schemas" not in f.parts]


def load_artifact(path: Path):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data, None
    except json.JSONDecodeError as e:
        return None, f"invalid JSON: {e}"


# ── Contract checks (cross-artifact) ──────────────────────────────────────────

def check_contract(artifacts: list[tuple[Path, dict]]) -> tuple[list[str], list[str]]:
    """Return (failures, warnings)."""
    failures: list[str] = []
    warnings: list[str] = []

    by_id: dict[str, dict] = {}
    seen_ids: dict[str, Path] = {}

    for path, a in artifacts:
        atype = a.get("artifact_type")
        name = path.name

        # core contract fields
        for f in REQUIRED_CONTRACT_FIELDS:
            if f not in a:
                failures.append(f"{name}: missing core contract field '{f}'")

        # known artifact type
        if atype not in ARTIFACT_TYPES:
            failures.append(f"{name}: unknown artifact_type {atype!r}")

        # unique ids
        aid = a.get("artifact_id")
        if aid:
            if aid in seen_ids:
                failures.append(f"{name}: duplicate artifact_id {aid!r} (also in {seen_ids[aid].name})")
            else:
                seen_ids[aid] = path
                by_id[aid] = a

    # type-specific contract rules
    for path, a in artifacts:
        atype = a.get("artifact_type")
        name = path.name

        if atype == "interpretive":
            for i, claim in enumerate(a.get("interpretive_claims", [])):
                speculative = claim.get("speculative") is True or claim.get("confidence") == "speculative"
                has_evidence = bool(claim.get("evidence_links"))
                if not has_evidence and not speculative:
                    failures.append(
                        f"{name}: interpretive_claims[{i}] has no evidence_links and is not marked speculative")
                if "confidence" not in claim:
                    failures.append(f"{name}: interpretive_claims[{i}] missing 'confidence'")

        if atype == "curation":
            if a.get("relevance_status") in ("publish", "feature") and not a.get("reasons_for_inclusion"):
                failures.append(
                    f"{name}: relevance_status={a.get('relevance_status')} requires non-empty reasons_for_inclusion")

        if atype == "public_prose":
            status = a.get("editorial_status")
            if status in ("reviewed", "published"):
                if a.get("prototype_mode") is True:
                    failures.append(f"{name}: prototype_mode prose may not be {status}")
                referenced = [by_id.get(i, {}).get("artifact_type")
                              for i in a.get("input_artifact_ids", [])]
                # also accept generated_from_artifacts declarations
                referenced += [g.get("artifact_type") for g in a.get("generated_from_artifacts", [])]
                if "raw_extraction" not in referenced:
                    failures.append(
                        f"{name}: {status} prose must reference >=1 extraction artifact in input_artifact_ids")
                if "validation" not in referenced:
                    failures.append(
                        f"{name}: {status} prose must reference >=1 validation artifact in input_artifact_ids")

    # validation FAIL blocks publishing for the same source
    failed_sources: dict[str, list[str]] = {}
    for path, a in artifacts:
        if a.get("artifact_type") == "validation" and a.get("validation_status") == "fail":
            failed_sources.setdefault(a.get("source_id"), []).append(a.get("target_artifact_id"))
    for path, a in artifacts:
        if a.get("artifact_type") == "public_prose" and a.get("editorial_status") == "published":
            src = a.get("source_id")
            if src in failed_sources:
                failures.append(
                    f"{path.name}: published prose for source {src} but a validation artifact for that "
                    f"source has status 'fail' ({failed_sources[src]})")

    return failures, warnings


# ── Main ──────────────────────────────────────────────────────────────────────

def main(argv: list[str]) -> int:
    if argv:
        targets = [Path(a) for a in argv]
    else:
        targets = [FIXTURES_DIR, GENERATED_DIR]

    files = find_artifact_files(targets)
    if not files:
        print("No artifact JSON files found.")
        return 0

    try:
        import jsonschema  # noqa: F401
        backend = "jsonschema"
    except ImportError:
        backend = "built-in"

    print(f"Validating {len(files)} artifact file(s) [schema backend: {backend}]\n")

    loaded: list[tuple[Path, dict]] = []
    n_fail = 0
    n_warn = 0

    for path in files:
        rel = path.relative_to(ARTIFACTS_DIR) if ARTIFACTS_DIR in path.parents else path
        data, err = load_artifact(path)
        if err:
            print(f"  FAIL  {rel}: {err}")
            n_fail += 1
            continue

        atype = data.get("artifact_type")
        if atype not in ARTIFACT_TYPES:
            print(f"  FAIL  {rel}: unknown or missing artifact_type {atype!r}")
            n_fail += 1
            continue

        schema = load_schema(atype)
        errs = validate_structural(data, schema)
        if errs:
            print(f"  FAIL  {rel}  [{atype}]")
            for e in errs:
                print(f"          - {e}")
            n_fail += 1
        else:
            print(f"  ok    {rel}  [{atype}]")
        loaded.append((path, data))

    # contract checks across the whole set
    failures, warnings = check_contract(loaded)
    if failures or warnings:
        print("\nContract checks:")
        for w in warnings:
            print(f"  WARN  {w}")
            n_warn += 1
        for f in failures:
            print(f"  FAIL  {f}")
            n_fail += 1
    else:
        print("\nContract checks: all passed.")

    print(f"\nSummary: {len(loaded)} validated, {n_fail} failure(s), {n_warn} warning(s).")
    return 1 if n_fail else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
