"""Extract Philip K. Dick's own story notes into structured data.

The Collected Stories corpus carries five appendices — one per volume,
each headed "## NOTES" — of Dick's own dated commentary on his stories,
written for The Best of Philip K. Dick (1977) and The Golden Man (1980).
This is the single highest-value "PKD on this work" source available:
first-person, story-specific, and often the only place he addresses a
given piece at all. It was previously going unused because nothing
extracted it out of the running prose of the collection.

Run standalone to refresh artifacts/generated/reading/pkd_story_notes.json
whenever the source corpus changes. gather_evidence.py consults this file
directly so future dossiers pick these notes up automatically instead of
relying on incidental keyword hits elsewhere in the archive.

    python scripts/reading/extract_story_notes.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[2]
SRC = PROJECT / "database" / "extracted_markdown" / "DOC_ARCH_OCEANOFPDF_COM_THE_COLLECTED_STORIES_OF_.md"
OUT = PROJECT / "artifacts" / "generated" / "reading" / "pkd_story_notes.json"

# A heading is an all-caps title (letters, apostrophes, hyphens, spaces only —
# deliberately excluding digits, which belong to the date/magazine info that
# follows and must not be swallowed into the title).
HEADING_RE = re.compile(r"^(?:##\s*)?((?:[A-Z][A-Z'\-]*\s*)+)")
DATE_RE = re.compile(r"^(\d{1,2}/\d{1,2}/\d{2,4})\.?\s*(.*)$")
ALT_TITLE_RE = re.compile(r'\(["“]([^)"”]+)["”]\)')


def find_notes_ranges(lines: list[str]) -> list[tuple[int, int]]:
    starts = [i + 1 for i, l in enumerate(lines) if l.strip().startswith("## **NOTES**")]
    ranges = []
    for i, s in enumerate(starts):
        e = starts[i + 1] - 1 if i + 1 < len(starts) else len(lines)
        ranges.append((s, e))
    return ranges


def extract() -> list[dict]:
    lines = SRC.read_text(encoding="utf-8").split("\n")
    records: list[dict] = []
    current: dict | None = None

    def flush():
        if current and (current["note"] or current["magazine"] or current["written_date"]):
            records.append(current)

    for start, end in find_notes_ranges(lines):
        for raw in lines[start - 1:end]:
            stripped = raw.strip()
            if not stripped or stripped.startswith("## **NOTES**") or "_OceanofPDF.com_" in stripped:
                continue
            is_heading = bool(re.match(r"^(?:##\s*)?[A-Z][A-Z'\-]", stripped)) and not stripped.startswith("_")
            if is_heading:
                m = HEADING_RE.match(stripped)
                if m and len(m.group(1).strip()) >= 3:
                    flush()
                    title = m.group(1).strip()
                    rest = stripped[m.end():].strip()
                    current = {"title": title, "note": "", "magazine": rest,
                               "written_date": None, "alt_title": None}
                    dm = DATE_RE.match(rest)
                    if dm:
                        current["written_date"] = dm.group(1)
                        current["magazine"] = dm.group(2)
                    am = ALT_TITLE_RE.search(rest)
                    if am:
                        current["alt_title"] = am.group(1)
                    continue
            if current is not None:
                current["note"] = f"{current['note']} {stripped}".strip()

    flush()

    for r in records:
        r["note"] = re.sub(r"\s+", " ", r["note"].replace("_", "")).strip()
        if r["magazine"]:
            r["magazine"] = r["magazine"].replace("_", "").strip().rstrip(".")

    return records


def main() -> None:
    records = extract()
    with_notes = sum(1 for r in records if r["note"])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{len(records)} headings parsed, {with_notes} carry an actual PKD note -> {OUT}")


if __name__ == "__main__":
    main()
