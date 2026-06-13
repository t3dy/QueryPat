"""Fill repeatable metadata holes in public JSON bundles.

This is intentionally conservative: it does not invent new source claims. It
adds useful fallback prose and empty-but-present relationship fields so the site
can render dense cards/pages while deeper human curation continues.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "site" / "public" / "data"


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def clean_label(value: str | None) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def infer_entities(text: str, known: set[str], limit: int = 8) -> list[str]:
    hits: list[str] = []
    seen: set[str] = set()
    normalized_text = f" {re.sub(r'[^A-Za-z0-9]+', ' ', text)} "
    for name in sorted(known, key=len, reverse=True):
        if len(hits) >= limit:
            break
        if len(name) < 3:
            continue
        pattern = rf"(?<![A-Za-z0-9]){re.escape(name)}(?![A-Za-z0-9])"
        if re.search(pattern, normalized_text, flags=re.I):
            key = name.lower()
            if key not in seen:
                hits.append(name)
                seen.add(key)
    return hits


def fill_biography() -> dict[str, int]:
    path = DATA / "biography" / "curated.json"
    rows = read_json(path)
    known_entities = {
        ent
        for row in rows
        for ent in (row.get("entities") or [])
        if isinstance(ent, str) and ent.strip()
    }

    notes_filled = 0
    entities_filled = 0
    for row in rows:
        if row.get("entities") is None:
            row["entities"] = []
        if not row.get("entities"):
            inferred = infer_entities(row.get("event", ""), known_entities)
            row["entities"] = inferred
            if inferred:
                entities_filled += 1

        if not clean_label(row.get("notes")):
            source = clean_label(row.get("source")) or "the project chronology"
            category = clean_label(row.get("category")).replace("_", " ") or "biographical"
            precision = clean_label(row.get("date_precision")) or "dated"
            row["notes"] = (
                f"Generated curation note: a {precision} {category} entry retained from {source}. "
                "Use the source field and linked entities for deeper verification."
            )
            notes_filled += 1

    write_json(path, rows)
    return {"biography_notes_filled": notes_filled, "biography_entities_filled": entities_filled}


def scholar_source_phrase(scholar: dict[str, Any]) -> str:
    works = [clean_label(w) for w in scholar.get("key_works") or [] if clean_label(w)]
    if works:
        return f"especially {', '.join(works[:3])}"
    role = clean_label(scholar.get("role")) or "PKD scholarship"
    return f"through work categorized here as {role}"


def fill_scholars() -> dict[str, int]:
    path = DATA / "scholars.json"
    rows = read_json(path)
    stance_filled = 0
    archive_filled = 0

    for scholar in rows:
        if scholar.get("archive_pdfs") is None:
            scholar["archive_pdfs"] = []
        if not isinstance(scholar.get("archive_pdfs"), list):
            scholar["archive_pdfs"] = []
        if not scholar["archive_pdfs"]:
            scholar["archive_pdfs"] = [{
                "title": (scholar.get("key_works") or ["No local archive PDF linked yet"])[0],
                "filename": None,
                "category": "not_yet_linked",
                "date": None,
                "pages": None,
                "is_pkd_authored": False,
            }]
            archive_filled += 1

        if not clean_label(scholar.get("interpretive_stance")):
            name = clean_label(scholar.get("name")) or "This source"
            role = clean_label(scholar.get("role")) or "scholar or source"
            tier = scholar.get("tier")
            tier_clause = f" Tier {tier}" if tier else ""
            scholar["interpretive_stance"] = (
                f"{name} is indexed as a {role.lower()} in QueryPat's scholar/source layer.{tier_clause} "
                f"The profile is most useful for orientation {scholar_source_phrase(scholar)}. "
                "A fuller interpretive account remains a curation target."
            )
            stance_filled += 1

        if not clean_label(scholar.get("relevance")):
            scholar["relevance"] = (
                "Use this profile as a pointer into the secondary-source network and compare it with "
                "higher-detail scholar records before treating it as an interpretive authority."
            )

    write_json(path, rows)
    return {"scholar_stances_filled": stance_filled, "scholar_archive_arrays_normalized": archive_filled}


def fill_name_placeholders() -> dict[str, int]:
    entities_dir = DATA / "names" / "entities"
    filled = 0
    for path in entities_dir.glob("*.json"):
        row = read_json(path)
        if not row.get("linked_segments"):
            row["linked_segments"] = [{
                "seg_id": None,
                "match_type": "unlinked",
                "confidence": None,
                "matched_text": row.get("canonical_form"),
                "date_display": None,
                "summary": "No public segment link has been promoted for this name yet.",
                "title": "Unlinked name evidence",
            }]
            filled += 1
            write_json(path, row)
    return {"name_segment_placeholders_filled": filled}


def main() -> None:
    summary = {}
    summary.update(fill_biography())
    summary.update(fill_scholars())
    summary.update(fill_name_placeholders())
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
