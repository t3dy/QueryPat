"""Promote completed reading dossiers into canonical works.

Every dossier whose close reading is finished becomes a work with a card on the
Works tab and a page of its own. Dossiers that only carry scripted evidence
layers (``reading_status: pending_close_reading``) are skipped: a work without a
read summary must not get a card, because an empty card reads as a claim that
there is nothing to say.

Where a dossier's slug already matches a canonical work built from the archive
documents (``a-maze-of-death``, ``ubik``), the dossier enriches that row rather
than creating a second one. Existing ``work_id`` values are never reassigned.

Run standalone during a reading session, or let ``build_canonical_works.py``
call ``apply`` so a full rebuild does not drop the readings.
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DOSSIER_DIR = ROOT / "artifacts" / "generated" / "reading" / "dossiers"
WORKS_DIR = ROOT / "site" / "public" / "data" / "works"
DB_PATH = ROOT / "database" / "unified.sqlite"

# Dossier `form` -> (work_type, display category)
FORM_MAP = {
    "short story": "short_story",
    "short_story": "short_story",
    "novelette": "novelette",
    "novella": "novella",
    "novel": "novel",
    "essay": "essay",
    "non-fiction": "essay",
}

CARD_LIMIT = 300


def card_from_synopsis(text: str) -> str:
    """First whole sentences of the synopsis, up to the card limit.

    Truncating mid-sentence produces a card that misleads; stopping at a
    sentence boundary produces one that is merely short.
    """
    text = re.sub(r"\s+", " ", text or "").strip()
    if not text:
        return ""
    if len(text) <= CARD_LIMIT:
        return text
    out = ""
    for sentence in re.split(r"(?<=[.!?]) ", text):
        if out and len(out) + len(sentence) + 1 > CARD_LIMIT:
            break
        out = f"{out} {sentence}".strip()
    return out or text[:CARD_LIMIT].rsplit(" ", 1)[0] + "…"


def page_summary_from(dossier: dict[str, Any]) -> str:
    reading = dossier.get("reading") or {}
    parts = [reading.get("synopsis") or ""]
    if reading.get("significance"):
        parts.append(f"**Why it matters.** {reading['significance']}")
    if reading.get("closing_note"):
        parts.append(f"*{reading['closing_note']}*")
    return "\n\n".join(p for p in parts if p).strip()


def is_complete(dossier: dict[str, Any]) -> bool:
    # The earliest dossiers predate the reading_status field, so a written
    # synopsis is the test; the status field only ever rules a dossier out.
    status = dossier.get("reading_status") or (dossier.get("reading") or {}).get("reading_status")
    synopsis = (dossier.get("reading") or {}).get("synopsis")
    return bool(synopsis) and status != "pending_close_reading"


def work_from_dossier(dossier: dict[str, Any]) -> dict[str, Any]:
    work = dossier["work"]
    reading = dossier["reading"]
    slug = work["slug"]
    form = (work.get("form") or "short story").lower()
    date = str(work.get("first_publication") or "")
    year = re.search(r"\b(1[89]\d\d|20\d\d)\b", date)

    themes = [
        t["theme"]
        for t in (dossier.get("concepts", {}).get("thematic_links_proposed") or [])
        if t.get("theme")
    ]

    record: dict[str, Any] = {
        "work_id": f"WORK_{slug}",
        "canonical_title": work["title"],
        "slug": slug,
        "author": "Philip K. Dick",
        "work_type": FORM_MAP.get(form, "short_story"),
        "category": {"novel": "novels", "essay": "primary"}.get(FORM_MAP.get(form), "short_stories"),
        "date_display": work.get("first_publication") or "",
        "date_start": year.group(1) if year else "",
        "card_summary": work.get("card_summary") or card_from_synopsis(reading["synopsis"]),
        "page_summary": page_summary_from(dossier),
        "page_count": 0,
        "source_count": 0,
        "related_docs": [],
        "biography_events": [],
        "themes": themes,
        "word_count": work.get("word_count"),
        # Everything below is the close reading itself, and lives only in the
        # per-work file so the index stays small enough to load on the list page.
        "reading": {
            "structure": reading.get("structure"),
            "characters": reading.get("characters"),
            "settings": reading.get("settings"),
            "motifs": reading.get("motifs"),
            "significance": reading.get("significance"),
            "closing_note": reading.get("closing_note"),
        },
        "distinctive_terms": dossier.get("concepts", {}).get("distinctive_terms") or [],
        "pkd_on_this_work": dossier.get("pkd_on_this_work"),
        "criticism": dossier.get("criticism"),
        "contradictions": dossier.get("contradictions") or [],
        "open_questions": dossier.get("open_questions") or [],
        "has_reading_notes": True,
        "reading_provenance": {
            "status": "LLM_CANDIDATE",
            "review_state": dossier.get("review_state", "unreviewed"),
            "note": "Close reading of the primary text plus attributed evidence from the archive. Candidate: not yet promoted to canonical.",
        },
    }
    for optional in ("later_use", "award", "written", "original_title", "critical_caution", "ending_correction"):
        if work.get(optional):
            record[optional] = work[optional]
        elif dossier.get(optional):
            record[optional] = dossier[optional]
    return record


# Fields that belong on the card / list page. Everything else is detail-only.
INDEX_FIELDS = (
    "work_id", "canonical_title", "slug", "author", "work_type", "category",
    "date_display", "date_start", "card_summary", "page_count", "source_count",
    "themes", "has_reading_notes",
)


def load_dossier_works() -> list[dict[str, Any]]:
    works = []
    for path in sorted(DOSSIER_DIR.glob("*.dossier.json")):
        dossier = json.loads(path.read_text(encoding="utf-8"))
        if not is_complete(dossier):
            continue
        works.append(work_from_dossier(dossier))
    return works


def merge(existing: list[dict[str, Any]], dossier_works: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Dossier readings enrich matching works and are added where new.

    An existing work keeps its own identity, dates and archive links; the
    reading supplies what the archive-derived row never had.
    """
    by_slug = {w["slug"]: w for w in existing}
    merged = [dict(w) for w in existing]
    index = {w["slug"]: w for w in merged}

    for reading in dossier_works:
        slug = reading["slug"]
        if slug in index:
            target = index[slug]
            for key, value in reading.items():
                # Never reassign an established id, and never overwrite a
                # curated archive summary with a derived one.
                if key in ("work_id", "canonical_title", "date_display", "date_start",
                           "page_count", "source_count", "related_docs", "first_doc",
                           "biography_events", "work_type", "category"):
                    continue
                if key in ("card_summary", "page_summary") and target.get(key):
                    continue
                if value in (None, [], {}, ""):
                    continue
                target[key] = value
            target["themes"] = sorted({*(target.get("themes") or []), *(reading.get("themes") or [])})
        else:
            merged.append(reading)
    return merged


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def export(works: list[dict[str, Any]]) -> None:
    """Write a lean index for the list page and a full file per work."""
    index = [{k: w.get(k) for k in INDEX_FIELDS if w.get(k) is not None} for w in works]
    write_json(WORKS_DIR / "index.json", index)
    for work in works:
        write_json(WORKS_DIR / f"{work['slug']}.json", work)


def seed_db(works: list[dict[str, Any]]) -> int:
    if not DB_PATH.exists():
        return 0
    db = sqlite3.connect(str(DB_PATH))
    written = 0
    for work in works:
        db.execute(
            """INSERT INTO works (work_id, canonical_title, slug, author, work_type,
                   category, date_start, date_display, card_summary, page_summary,
                   source_count, page_count, provenance)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
               ON CONFLICT(work_id) DO UPDATE SET
                   card_summary=excluded.card_summary,
                   page_summary=excluded.page_summary,
                   provenance=excluded.provenance""",
            (
                work["work_id"], work["canonical_title"], work["slug"], work["author"],
                work["work_type"], work["category"], work.get("date_start"),
                work.get("date_display"), work.get("card_summary"), work.get("page_summary"),
                work.get("source_count", 0), work.get("page_count", 0),
                "reading_dossier" if work.get("has_reading_notes") else None,
            ),
        )
        written += 1
    db.commit()
    db.close()
    return written


def apply(works: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Hook for build_canonical_works: fold readings into freshly built rows."""
    return merge(works, load_dossier_works())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed-db", action="store_true", help="also upsert into the works table")
    parser.add_argument("--report", action="store_true", help="show coverage only")
    args = parser.parse_args()

    dossier_works = load_dossier_works()
    total_dossiers = len(list(DOSSIER_DIR.glob("*.dossier.json")))

    if args.report:
        print(f"{len(dossier_works)} of {total_dossiers} dossiers have a completed close reading")
        return

    existing = json.loads((WORKS_DIR / "index.json").read_text(encoding="utf-8"))
    # Reload full detail for existing works so the lean index does not erase them.
    full = []
    for entry in existing:
        detail_path = WORKS_DIR / f"{entry['slug']}.json"
        full.append(json.loads(detail_path.read_text(encoding="utf-8")) if detail_path.exists() else entry)

    works = merge(full, dossier_works)
    export(works)
    seeded = seed_db(dossier_works) if args.seed_db else 0
    with_reading = sum(1 for w in works if w.get("has_reading_notes"))
    print(
        f"{len(works)} works exported "
        f"({with_reading} with close readings, {total_dossiers - len(dossier_works)} dossiers still pending)"
        + (f"; {seeded} rows upserted" if seeded else "")
    )


if __name__ == "__main__":
    main()
