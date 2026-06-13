"""Audit short-card and detail-page coverage across public data exports.

The goal is not to block work on every legacy gap. It gives each session a
cheap, repeatable map of what still needs rich metadata before the site can
support dense sorting, tabs, and relational browsing.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "site" / "public" / "data"


@dataclass(frozen=True)
class Contract:
    label: str
    index_path: Path
    id_field: str
    title_field: str
    required_index_fields: tuple[str, ...]
    detail_dir: Path | None = None
    detail_slug_field: str | None = None
    required_detail_fields: tuple[str, ...] = ()


CONTRACTS: tuple[Contract, ...] = (
    Contract(
        label="archive documents",
        index_path=DATA / "archive" / "index.json",
        id_field="doc_id",
        title_field="title",
        required_index_fields=(
            "doc_id",
            "title",
            "slug",
            "category",
            "date_display",
            "card_summary",
            "evidentiary_lane",
            "source_reliability",
        ),
        detail_dir=DATA / "archive" / "docs",
        detail_slug_field="slug",
        required_detail_fields=(
            "page_summary",
            "people_mentioned",
            "works_discussed",
            "linked_terms",
        ),
    ),
    Contract(
        label="dictionary terms",
        index_path=DATA / "dictionary" / "index.json",
        id_field="term_id",
        title_field="canonical_name",
        required_index_fields=(
            "term_id",
            "canonical_name",
            "slug",
            "status",
            "review_state",
            "primary_category",
            "mention_count",
            "card_description",
        ),
        detail_dir=DATA / "dictionary" / "terms",
        detail_slug_field="slug",
        required_detail_fields=("full_description", "related_terms", "linked_segments"),
    ),
    Contract(
        label="scholars and fan-scholars",
        index_path=DATA / "scholars.json",
        id_field="scholar_id",
        title_field="name",
        required_index_fields=(
            "scholar_id",
            "name",
            "role",
            "tier",
            "key_works",
            "interpretive_stance",
            "relevance",
            "archive_pdfs",
        ),
    ),
    Contract(
        label="biography events",
        index_path=DATA / "biography" / "curated.json",
        id_field="id",
        title_field="event",
        required_index_fields=(
            "id",
            "date",
            "date_precision",
            "event",
            "category",
            "entities",
            "location",
            "source",
            "importance",
            "notes",
        ),
    ),
    Contract(
        label="names",
        index_path=DATA / "names" / "index.json",
        id_field="name_id",
        title_field="canonical_form",
        required_index_fields=(
            "name_id",
            "canonical_form",
            "slug",
            "entity_type",
            "source_type",
            "status",
            "review_state",
            "mention_count",
            "card_description",
        ),
        detail_dir=DATA / "names" / "entities",
        detail_slug_field="slug",
        required_detail_fields=("full_description", "linked_segments", "related_terms"),
    ),
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def is_missing(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip() or value.strip().lower() in {"unknown", "full summary pending."}
    if isinstance(value, (list, dict)):
        return len(value) == 0
    return False


def audit_contract(contract: Contract, sample_limit: int) -> dict[str, Any]:
    entries = load_json(contract.index_path)
    missing: dict[str, list[str]] = {}
    detail_missing: dict[str, list[str]] = {}

    for entry in entries:
        label = str(entry.get(contract.title_field) or entry.get(contract.id_field) or "unknown")
        for field in contract.required_index_fields:
            if is_missing(entry.get(field)):
                missing.setdefault(field, []).append(label)

        if contract.detail_dir and contract.detail_slug_field:
            slug = entry.get(contract.detail_slug_field)
            if not slug:
                detail_missing.setdefault("detail_file", []).append(label)
                continue
            detail_path = contract.detail_dir / f"{slug}.json"
            if not detail_path.exists():
                detail_missing.setdefault("detail_file", []).append(label)
                continue
            detail = load_json(detail_path)
            for field in contract.required_detail_fields:
                if is_missing(detail.get(field)):
                    detail_missing.setdefault(field, []).append(label)

    def summarize(m: dict[str, list[str]]) -> dict[str, Any]:
        return {
            field: {
                "missing_count": len(items),
                "sample": items[:sample_limit],
            }
            for field, items in sorted(m.items(), key=lambda item: (-len(item[1]), item[0]))
        }

    return {
        "label": contract.label,
        "entry_count": len(entries),
        "index_missing": summarize(missing),
        "detail_missing": summarize(detail_missing),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    parser.add_argument("--sample-limit", type=int, default=8)
    args = parser.parse_args()

    report = [audit_contract(contract, args.sample_limit) for contract in CONTRACTS]
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return

    for section in report:
        print(f"\n{section['label']} ({section['entry_count']} entries)")
        for bucket in ("index_missing", "detail_missing"):
            if not section[bucket]:
                print(f"  {bucket}: ok")
                continue
            print(f"  {bucket}:")
            for field, result in section[bucket].items():
                sample = "; ".join(result["sample"])
                print(f"    - {field}: {result['missing_count']} missing")
                if sample:
                    print(f"      sample: {sample}")


if __name__ == "__main__":
    main()
