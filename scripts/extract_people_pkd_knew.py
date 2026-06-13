"""Build a first-pass People PKD Knew dataset from existing site exports.

This script intentionally favors conservative evidence over flourish. It
collects names already present in curated biography events, archive document
relationship fields, scholar profiles, and the names index, then writes a
sortable public JSON export for the front end.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "site" / "public" / "data"
OUT_DIR = DATA / "people"
OUT_PATH = OUT_DIR / "pkd-knew.json"

PKD_NAMES = {
    "philip k. dick",
    "philip kindred dick",
    "philip dick",
    "pkd",
    "phil",
}

LIKELY_NON_PEOPLE = {
    "valis",
    "zebra",
    "god",
    "christ",
    "logos",
    "acts",
    "rome",
    "california",
    "berkeley",
    "orange county",
    "united states",
    "black iron prison",
}

RELATION_CATEGORY_MAP = {
    "marriage": "spouse_or_partner",
    "divorce": "spouse_or_partner",
    "family": "family",
    "birth": "family",
    "child": "family",
    "friendship": "friend",
    "correspondence": "correspondent",
    "professional_network": "sf_community",
    "employment": "workplace",
    "publication": "publishing",
    "contract": "publishing",
    "convention": "sf_community",
    "interview": "interviewer_or_media",
}

PRIMARY_RELATION_ORDER = [
    "spouse_or_partner",
    "family",
    "correspondent",
    "friend",
    "editor",
    "publisher",
    "agent",
    "fellow_sf_author",
    "doctor_or_therapist",
    "workplace",
    "fan_scholar",
    "scholar",
    "character_inspiration",
    "named_person",
]

EVIDENCE_LABELS = {
    "biography_events": "biography events",
    "archive_documents": "archive documents",
    "scholar_profiles": "scholar profiles",
    "names_index": "indexed name entries",
}


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "unknown"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def clean_name(value: str) -> str:
    value = re.sub(r"\s+", " ", value or "").strip()
    value = value.strip(" .,;:()[]{}\"'")
    return value


def looks_like_person(name: str) -> bool:
    low = name.lower()
    if not name or low in PKD_NAMES or low in LIKELY_NON_PEOPLE:
        return False
    if len(name) < 3:
        return False
    if any(char.isdigit() for char in name):
        return False
    parts = name.split()
    if len(parts) >= 2:
        return True
    return name in {
        "Tessa",
        "Anne",
        "Jane",
        "Dorothy",
        "Edgar",
        "Kleo",
        "Nancy",
        "Joan",
        "Isa",
    }


def source_mix(source_counts: dict[str, int]) -> str:
    parts = []
    for key in ("biography_events", "archive_documents", "scholar_profiles", "names_index"):
        count = source_counts.get(key, 0)
        if count:
            label = EVIDENCE_LABELS.get(key, key)
            parts.append(f"{count} {label}")
    if not parts:
        return "no supporting source links yet"
    if len(parts) == 1:
        return parts[0]
    if len(parts) == 2:
        return f"{parts[0]} and {parts[1]}"
    return ", ".join(parts[:-1]) + f", and {parts[-1]}"


@dataclass
class PersonRecord:
    name: str
    person_id: str
    relationship_categories: Counter[str] = field(default_factory=Counter)
    evidence_sources: Counter[str] = field(default_factory=Counter)
    biography_events: list[dict[str, Any]] = field(default_factory=list)
    archive_documents: list[dict[str, Any]] = field(default_factory=list)
    scholar_profiles: list[dict[str, Any]] = field(default_factory=list)
    name_entry: dict[str, Any] | None = None
    first_year: int | None = None
    last_year: int | None = None
    review_state: str = "machine-drafted"

    def add_year(self, value: str | None) -> None:
        if not value:
            return
        match = re.match(r"c?\.?\s*(\d{4})", value)
        if not match:
            return
        year = int(match.group(1))
        self.first_year = year if self.first_year is None else min(self.first_year, year)
        self.last_year = year if self.last_year is None else max(self.last_year, year)

    def to_json(self) -> dict[str, Any]:
        categories = [cat for cat, _ in self.relationship_categories.most_common()]
        source_counts = dict(sorted(self.evidence_sources.items()))
        event_sample = self.biography_events[:5]
        doc_sample = self.archive_documents[:8]
        scholar_sample = self.scholar_profiles[:5]
        strongest_categories = ", ".join(cat.replace("_", " ") for cat in categories[:4]) if categories else "candidate association"
        summary_parts = []
        if categories:
            summary_parts.append(f"Associated with PKD through {strongest_categories}")
        if self.first_year is not None or self.last_year is not None:
            if self.first_year == self.last_year:
                summary_parts.append(f"association centered on {self.first_year}")
            else:
                summary_parts.append(f"association spans {self.first_year} to {self.last_year}")
        if source_counts:
            summary_parts.append(f"evidence base: {source_mix(source_counts)}")

        card_summary = "; ".join(summary_parts) + "." if summary_parts else "Candidate person record awaiting review."
        strongest = next((cat for cat in PRIMARY_RELATION_ORDER if cat in categories), categories[0] if categories else "candidate")
        score = self.association_score(categories, source_counts)
        page_summary = (
            f"{self.name} is a People PKD Knew entry assembled from biography events, archive documents, scholar profiles, "
            f"and indexed name evidence. The current record draws on {source_mix(source_counts)} and organizes the person "
            f"around the relationship categories {', '.join(categories) if categories else 'not yet classified'}."
        )
        page_summary += (
            "\n\nBiography events and archive documents carry the strongest evidentiary weight; scholar profiles and the "
            "names index extend the record into later interpretive and editorial reception. Where the evidence is indirect "
            "or second-order, the entry should be read as a catalog of association rather than proof of personal acquaintance."
        )
        if self.biography_events:
            event_titles = ", ".join(ev["event"] for ev in self.biography_events[:3])
            page_summary += f"\n\nThe most visible biographical traces involve {event_titles}."
        if self.archive_documents:
            doc_titles = ", ".join(doc["title"] for doc in self.archive_documents[:3])
            page_summary += f"\n\nThe archive documentation most often surfaces in {doc_titles}."

        return {
            "person_id": self.person_id,
            "name": self.name,
            "slug": self.person_id,
            "relationship_categories": categories,
            "relationship_to_pkd": strongest.replace("_", " "),
            "association_score": score,
            "card_summary": card_summary,
            "page_summary": page_summary,
            "first_year": self.first_year,
            "last_year": self.last_year,
            "evidence_counts": source_counts,
            "biography_events": event_sample,
            "archive_documents": doc_sample,
            "scholar_profiles": scholar_sample,
            "name_entry": self.name_entry,
            "review_state": self.review_state,
        }

    @staticmethod
    def association_score(categories: list[str], source_counts: dict[str, int]) -> int:
        score = 0
        for category in categories:
            if category in {"spouse_or_partner", "family"}:
                score += 40
            elif category in {"correspondent", "friend", "editor", "publisher", "agent"}:
                score += 28
            elif category in {"fellow_sf_author", "doctor_or_therapist", "workplace"}:
                score += 20
            elif category in {"fan_scholar", "scholar"}:
                score += 12
            elif category in {"character_inspiration"}:
                score += 10
            elif category in {"biography", "mentioned_in_document", "named_person"}:
                score += 8
            else:
                score += 4
        score += min(sum(source_counts.values()) * 3, 36)
        return score


MANUAL_PEOPLE_OVERRIDES: list[dict[str, Any]] = [
    {
        "person_id": "claudia-bush",
        "name": "Claudia Bush",
        "relationship_categories": {"correspondent": 2, "scholar": 1},
        "evidence_sources": {"biography_events": 1, "archive_documents": 1},
        "review_state": "human-revised",
    },
    {
        "person_id": "tim-powers",
        "name": "Tim Powers",
        "relationship_categories": {"fellow_sf_author": 1},
        "evidence_sources": {"biography_events": 1, "archive_documents": 1},
        "archive_documents": [
            {
                "doc_id": "DOC_ARCH_OCEANOFPDF_COM_SELECTED_LETTERS_OF_PHILI",
                "title": "Selected Letters of Philip K. Dick, 1975-1976",
                "slug": "oceanofpdf-com-selected-letters-of-philip-k-dick-1975-1976-philip-k-dick",
                "category": "letters",
                "date_display": "1975-1976 (published 1992)",
                "is_pkd_authored": True,
            }
        ],
        "review_state": "human-revised",
    },
    {
        "person_id": "k-w-jeter",
        "name": "K. W. Jeter",
        "relationship_categories": {"fellow_sf_author": 1},
        "evidence_sources": {"biography_events": 1},
        "review_state": "human-revised",
    },
    {
        "person_id": "bishop-james-pike",
        "name": "Bishop James Pike",
        "relationship_categories": {
            "character_inspiration": 2,
            "mentioned_in_document": 1,
            "named_person": 1,
        },
        "evidence_sources": {"archive_documents": 1},
        "archive_documents": [
            {
                "doc_id": "DOC_ARCH_OCEANOFPDF_COM_THE_VALIS_TRILOGY_PHILIP_",
                "title": "The VALIS Trilogy",
                "slug": "oceanofpdf-com-the-valis-trilogy-philip-k-dick",
                "category": "novels",
                "date_display": "1981-1982 (Mariner Books edition 2011)",
                "is_pkd_authored": True,
            }
        ],
        "review_state": "human-revised",
    },
    {
        "person_id": "alan-watts",
        "name": "Alan Watts",
        "relationship_categories": {
            "character_inspiration": 2,
            "mentioned_in_document": 1,
            "named_person": 1,
        },
        "evidence_sources": {"archive_documents": 1},
        "archive_documents": [
            {
                "doc_id": "DOC_ARCH_OCEANOFPDF_COM_THE_VALIS_TRILOGY_PHILIP_",
                "title": "The VALIS Trilogy",
                "slug": "oceanofpdf-com-the-valis-trilogy-philip-k-dick",
                "category": "novels",
                "date_display": "1981-1982 (Mariner Books edition 2011)",
                "is_pkd_authored": True,
            }
        ],
        "review_state": "human-revised",
    },
]


def merge_unique_dicts(existing: list[dict[str, Any]], incoming: list[dict[str, Any]], key: str) -> list[dict[str, Any]]:
    seen = {item.get(key) for item in existing}
    merged = list(existing)
    for item in incoming:
        if item.get(key) in seen:
            continue
        merged.append(item)
        seen.add(item.get(key))
    return merged


def apply_manual_override(records: dict[str, PersonRecord], seed: dict[str, Any]) -> None:
    key = seed["person_id"]
    record = records.get(key)
    if record is None:
        record = PersonRecord(name=seed["name"], person_id=key)
        records[key] = record
    else:
        record.name = seed.get("name", record.name)

    for category, count in seed.get("relationship_categories", {}).items():
        record.relationship_categories[category] += count

    for source, count in seed.get("evidence_sources", {}).items():
        record.evidence_sources[source] += count

    record.biography_events = merge_unique_dicts(record.biography_events, seed.get("biography_events", []), "id")
    record.archive_documents = merge_unique_dicts(record.archive_documents, seed.get("archive_documents", []), "doc_id")
    record.scholar_profiles = merge_unique_dicts(record.scholar_profiles, seed.get("scholar_profiles", []), "scholar_id")

    if "name_entry" in seed:
        record.name_entry = seed["name_entry"]
    if "first_year" in seed and seed["first_year"] is not None:
        record.first_year = seed["first_year"] if record.first_year is None else min(record.first_year, seed["first_year"])
    if "last_year" in seed and seed["last_year"] is not None:
        record.last_year = seed["last_year"] if record.last_year is None else max(record.last_year, seed["last_year"])
    if "review_state" in seed and seed["review_state"]:
        record.review_state = seed["review_state"]


def apply_manual_overrides(records: dict[str, PersonRecord]) -> None:
    for seed in MANUAL_PEOPLE_OVERRIDES:
        apply_manual_override(records, seed)


def get_record(records: dict[str, PersonRecord], name: str) -> PersonRecord:
    cleaned = clean_name(name)
    key = slugify(cleaned)
    if key not in records:
        records[key] = PersonRecord(name=cleaned, person_id=key)
    return records[key]


def add_biography_events(records: dict[str, PersonRecord]) -> None:
    path = DATA / "biography" / "curated.json"
    if not path.exists():
        return
    for event in load_json(path):
        category = RELATION_CATEGORY_MAP.get(event.get("category", ""), event.get("category") or "biography")
        for entity in event.get("entities") or []:
            name = clean_name(entity)
            if not looks_like_person(name):
                continue
            record = get_record(records, name)
            record.relationship_categories[category] += 1
            record.evidence_sources["biography_events"] += 1
            record.add_year(event.get("date"))
            record.biography_events.append(
                {
                    "id": event.get("id"),
                    "date": event.get("date"),
                    "category": event.get("category"),
                    "event": event.get("event"),
                    "source": event.get("source"),
                    "importance": event.get("importance"),
                }
            )


def add_archive_docs(records: dict[str, PersonRecord]) -> None:
    docs_dir = DATA / "archive" / "docs"
    if not docs_dir.exists():
        return
    for path in docs_dir.glob("*.json"):
        doc = load_json(path)
        names = doc.get("people_mentioned") or []
        if doc.get("author"):
            names = [*names, doc["author"]]
        for raw_name in names:
            name = clean_name(raw_name)
            if not looks_like_person(name):
                continue
            record = get_record(records, name)
            category = "author" if name == clean_name(doc.get("author", "")) else "mentioned_in_document"
            if doc.get("category") == "letters" or doc.get("doc_type") == "letter":
                category = "correspondent"
            record.relationship_categories[category] += 1
            record.evidence_sources["archive_documents"] += 1
            record.add_year(doc.get("date_start") or doc.get("date_display"))
            record.archive_documents.append(
                {
                    "doc_id": doc.get("doc_id"),
                    "title": doc.get("title"),
                    "slug": doc.get("slug"),
                    "category": doc.get("category"),
                    "date_display": doc.get("date_display"),
                    "is_pkd_authored": doc.get("is_pkd_authored"),
                }
            )


def add_scholars(records: dict[str, PersonRecord]) -> None:
    path = DATA / "scholars.json"
    if not path.exists():
        return
    for scholar in load_json(path):
        name = clean_name(scholar.get("name", ""))
        if not looks_like_person(name):
            continue
        record = get_record(records, name)
        category = "fan_scholar" if "fan" in (scholar.get("role") or "").lower() else "scholar"
        record.relationship_categories[category] += 1
        record.evidence_sources["scholar_profiles"] += 1
        record.scholar_profiles.append(
            {
                "scholar_id": scholar.get("scholar_id"),
                "name": scholar.get("name"),
                "role": scholar.get("role"),
                "tier": scholar.get("tier"),
                "key_works": scholar.get("key_works", [])[:5],
            }
        )


def add_names_index(records: dict[str, PersonRecord]) -> None:
    path = DATA / "names" / "index.json"
    if not path.exists():
        return
    for entry in load_json(path):
        if entry.get("entity_type") != "historical_person":
            continue
        name = clean_name(entry.get("canonical_form", ""))
        if not looks_like_person(name):
            continue
        record = get_record(records, name)
        record.relationship_categories["named_person"] += 1
        record.evidence_sources["names_index"] += 1
        record.name_entry = {
            "name_id": entry.get("name_id"),
            "slug": entry.get("slug"),
            "mention_count": entry.get("mention_count", 0),
            "card_description": entry.get("card_description"),
            "source_type": entry.get("source_type"),
        }


def build_records() -> list[dict[str, Any]]:
    records: dict[str, PersonRecord] = {}
    add_biography_events(records)
    add_archive_docs(records)
    add_scholars(records)
    add_names_index(records)
    apply_manual_overrides(records)

    entries = [record.to_json() for record in records.values()]
    entries.sort(
        key=lambda item: (
            -sum(item["evidence_counts"].values()),
            item["name"].lower(),
        )
    )
    return entries


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=OUT_PATH)
    parser.add_argument("--print-summary", action="store_true")
    args = parser.parse_args()

    entries = build_records()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if args.print_summary:
        categories: defaultdict[str, int] = defaultdict(int)
        for entry in entries:
            for category in entry["relationship_categories"]:
                categories[category] += 1
        print(f"Wrote {len(entries)} people to {args.out}")
        for category, count in sorted(categories.items(), key=lambda item: (-item[1], item[0])):
            print(f"{category}: {count}")


if __name__ == "__main__":
    main()
