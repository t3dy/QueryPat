"""Ingest the local Maze Notes PDF as The Maze of Death Theology.

Source file expected at:
    C:/QueryPat/database/source_pdfs/Maze notes.pdf

This document is treated as an unpublished PKD primary source and an early
Exegesis-adjacent theological/composition document for A Maze of Death.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
import sqlite3
from pathlib import Path

import fitz


DB_PATH = Path("C:/QueryPat/database/unified.sqlite")
PDF_PATH = Path("C:/QueryPat/database/source_pdfs/Maze notes.pdf")
MD_PATH = Path("C:/QueryPat/database/extracted_markdown/DOC_ARCH_MAZE_OF_DEATH_THEOLOGY.md")
CURATED_PATH = Path("C:/QueryPat/site/public/data/biography/curated.json")

DOC_ID = "DOC_ARCH_MAZE_OF_DEATH_THEOLOGY"
PENDING_DOC_ID = "DOC_ARCH_MAZE_OF_DEATH_THEOLOGY_PENDING"
ASSET_ID = "ASSET_MAZE_OF_DEATH_THEOLOGY_PDF"


CARD_SUMMARY = (
    "Unpublished PKD notes titled \"Notes on the Tench Novel,\" ingested as The Maze of Death Theology. "
    "The 16-page document sketches the colony/Delmak premise behind A Maze of Death and develops an "
    "explicit theological system of gods, entropy, the Manufacturer, decay, form-destruction, and the "
    "problem of evil."
)

PAGE_SUMMARY = """This unpublished primary-source document is titled "Notes on the Tench Novel" in the PDF itself, but is entered here under the project title The Maze of Death Theology because it is the theological/conceptual notes packet behind A Maze of Death. The document is a 16-page set of draft notes, likely from the 1968 composition period, in which PKD works from a colony-survival premise toward the metaphysical architecture of the novel.

The opening pages imagine an Earth colony on a distant planet undergoing social, economic, psychological, and entropic breakdown. PKD lists character types, possible names, occupations, breakdown modes, and plot alternatives: rotating authority, ruined instructions, isolation from Earth, possible monitoring devices, and the suspicion that the colonists may be experimental subjects. The early title-world is "Tench" and then Delmar/Delmak; the later novel's movement from mission plot to metaphysical uncertainty is already visible.

The central theological material appears as the notes turn from plot mechanics toward ontology. PKD imagines a world where each person's worldview shapes perceived reality, yet the gods remain the only communicable constant across subjective worlds. The notes propose gods no longer on Earth, a compact between Earth and the gods, a "Walker-on-earth," a "Manufacturer," a decay or form-destroying power, and a theological account in which evil is treated as unreality, decay, or form-loss. This makes the document an important pre-1974 witness to PKD's religious imagination before the Exegesis proper.

Research significance: The document belongs with A Maze of Death, the William Sarill theology connection named in the novel's foreword, and the later Exegesis concern with entropy, form, orthogonal realities, living information, divine plurality, and the problem of evil. It should be treated as an early Exegesis-adjacent primary document, not merely a discarded plot outline.

Sarill context: PKD later wrote that A Maze of Death stemmed from an attempt by William Sarill and himself to develop an abstract logical system of religious thought based on the arbitrary postulate that God exists. Sarill later remembered first meeting PKD in 1968 and spending over a month as his houseguest, but he did not recall the same kind of religious or visionary discussion; project notes should preserve that tension rather than harmonize it. The user's current research note adds that Sarill remembered bringing Dick an article by a physicist on multiple universes, possibly connected to Wheeler/Everett-style many-worlds discussions; this remains a lead needing source confirmation."""


BIO_EVENTS = [
    {
        "id": "pkd_bio_1968_sarill_houseguest_maze",
        "date": "1968",
        "date_precision": "year",
        "event": "William Sarill first meets PKD and later spends more than a month as his houseguest during the period associated with the theology behind A Maze of Death.",
        "category": "friendship",
        "entities": ["William Sarill", "A Maze of Death"],
        "location": "California",
        "source": "William Sarill, Will the Real Ubik Please Stand Up?; A Maze of Death foreword",
        "importance": 4,
        "notes": "Sarill confirms the 1968 meeting and extended houseguest period; PKD's Maze foreword credits Sarill as co-developer of the abstract religious system behind the novel."
    },
    {
        "id": "pkd_bio_1968_maze_theology_notes",
        "date": "1968",
        "date_precision": "inferred",
        "event": "PKD drafts the Maze/Tench theology notes that develop the colony plot, Delmak setting, divine plurality, the Manufacturer, decay, and the form-destroying principle later associated with A Maze of Death.",
        "category": "religious_thought",
        "entities": ["A Maze of Death", "The Maze of Death Theology", "William Sarill"],
        "location": "California",
        "source": "The Maze of Death Theology (Maze notes PDF)",
        "importance": 5,
        "notes": "Entered as an early Exegesis-adjacent primary document. The Sarill/multiple-universes/Wheeler lead remains a source-confirmation task."
    },
    {
        "id": "pkd_bio_1977_sarill_reencounter_maze",
        "date": "1977-07-27",
        "date_precision": "inferred",
        "event": "After several years without contact, PKD encounters William Sarill again and discusses how their theologies have changed since the Maze of Death period.",
        "category": "correspondence",
        "entities": ["William Sarill", "Eugene Warren", "A Maze of Death"],
        "location": "Santa Ana, California",
        "source": "Selected Letters 1977-1979, letter to Eugene Warren, July 28, 1977",
        "importance": 4,
        "notes": "PKD writes that the encounter occurred the night before Warren's article arrived; he links Sarill to the theology in Maze and then describes his 1974 Trinitarian conversion."
    },
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def extract_markdown(pdf_path: Path) -> str:
    doc = fitz.open(pdf_path)
    parts = []
    front = (
        "# The Maze of Death Theology\n\n"
        "*by Philip K. Dick*\n\n"
        f"category: primary - doc_id: `{DOC_ID}` - source: `Maze notes.pdf`\n\n"
        "---\n\n"
    )
    for i, page in enumerate(doc, 1):
        text = page.get_text("text").replace("\r\n", "\n").replace("\r", "\n")
        text = (
            text.replace("â€”", "--")
            .replace("\u2014", "--")
            .replace("\u2013", "-")
            .replace("â€“", "-")
            .replace("â€™", "'")
            .replace("â€œ", '"')
            .replace("â€", '"')
            .replace("â€˜", "'")
            .replace("Â", "")
        )
        lines = [ln.rstrip() for ln in text.split("\n")]
        cleaned = "\n".join(lines).strip()
        cleaned = re.sub(r"\n{4,}", "\n\n\n", cleaned)
        parts.append(f"## Page {i}\n\n{cleaned}")
    return front + "\n\n".join(parts) + "\n"


def add_curated_events() -> int:
    data = json.loads(CURATED_PATH.read_text(encoding="utf-8"))
    existing = {event.get("id") for event in data}
    added = 0
    for event in BIO_EVENTS:
        if event["id"] in existing:
            continue
        data.append(event)
        added += 1
    data.sort(key=lambda e: (e.get("date") or "", e.get("id") or ""))
    CURATED_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return added


def main() -> int:
    if not PDF_PATH.exists():
        raise SystemExit(f"missing source PDF: {PDF_PATH}")

    markdown = extract_markdown(PDF_PATH)
    MD_PATH.parent.mkdir(parents=True, exist_ok=True)
    MD_PATH.write_text(markdown, encoding="utf-8")
    now = dt.datetime.now(dt.UTC).isoformat(timespec="seconds")
    source_hash = sha256(PDF_PATH)

    con = sqlite3.connect(DB_PATH, timeout=30)
    con.execute("DELETE FROM document_texts WHERE doc_id = ?", (PENDING_DOC_ID,))
    con.execute("DELETE FROM document_assets WHERE doc_id = ?", (PENDING_DOC_ID,))
    con.execute("DELETE FROM assets WHERE doc_id = ?", (PENDING_DOC_ID,))
    con.execute("DELETE FROM documents WHERE doc_id = ?", (PENDING_DOC_ID,))

    con.execute(
        """INSERT OR REPLACE INTO documents (
            doc_id, doc_type, title, slug, author, recipient,
            date_start, date_end, date_display, date_confidence, date_basis,
            timeline_type, ingest_level, extractability_score, relevance_score,
            ocr_required, extraction_status, is_pkd_authored, word_count,
            page_count, source_filename, text_char_count, card_summary,
            page_summary, category, notes, evidentiary_lane, source_reliability,
            updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            DOC_ID, "archive_pdf", "The Maze of Death Theology",
            "maze-of-death-theology", "Philip K. Dick", None,
            "1968", None, "circa 1968", "inferred",
            "Inferred from A Maze of Death composition/Sarill context; PDF itself is undated",
            "composition", "full", 95, 95, 0, "complete", 1,
            len(markdown.split()), 16, "Maze notes.pdf", len(markdown),
            CARD_SUMMARY, PAGE_SUMMARY, "primary",
            "PDF title line reads 'NOTES ON THE TENCH NOVEL'; project title retained as The Maze of Death Theology.",
            "B", "primary_pkd", now,
        ),
    )
    con.execute(
        """INSERT OR REPLACE INTO assets (
            asset_id, doc_id, asset_type, file_path, file_size_mb, mime_type, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (
            ASSET_ID, DOC_ID, "pdf", "database/source_pdfs/Maze notes.pdf",
            round(PDF_PATH.stat().st_size / (1024 * 1024), 3), "application/pdf",
            "Copied from C:/Users/PC/Downloads/Maze notes (1).pdf on ingestion.",
        ),
    )
    con.execute(
        """INSERT OR REPLACE INTO document_assets (doc_id, asset_id, role)
           VALUES (?, ?, ?)""",
        (DOC_ID, ASSET_ID, "source"),
    )
    con.execute(
        """INSERT OR REPLACE INTO document_texts (
            text_id, doc_id, extraction_method, extraction_status,
            extractability_score, ocr_required, text_content, char_count,
            created_at, markdown_content, markdown_method, markdown_status,
            markdown_char_count, markdown_updated_at, markdown_source_hash
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            f"TEXT_{DOC_ID}", DOC_ID, "pymupdf", "complete",
            0.95, 0, markdown, len(markdown), now, markdown,
            "pymupdf_text_pages", "complete", len(markdown), now, source_hash,
        ),
    )
    con.commit()
    con.close()

    added = add_curated_events()
    print(f"[done] wrote markdown: {MD_PATH} ({len(markdown)} chars)")
    print(f"[done] ingested document {DOC_ID}")
    print(f"[done] added {added} curated biography events")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
