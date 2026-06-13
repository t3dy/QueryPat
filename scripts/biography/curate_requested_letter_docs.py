"""Curate requested letter/document summaries and biography quote notes.

Adds archive-level document summaries for:
- PKD's March 16, 1977 letter to Julian Jaynes
- PKD's October 2, 1977 Star Wars letter to Eugene Warren
- the Claudia Bush letters as a correspondence corpus
- a pending/unlocated "Maze of Death Theology" document placeholder

Also updates curated biography events with brief fair-use quotation snippets.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import sqlite3
from pathlib import Path


DB_PATH = Path("C:/QueryPat/database/unified.sqlite")
CURATED_PATH = Path("site/public/data/biography/curated.json")


DOCS = [
    {
        "doc_id": "DOC_ARCH_LETTER_TO_JULIAN_JAYNES_1977_03_16",
        "doc_type": "letter",
        "title": "Letter to Julian Jaynes",
        "slug": "letter-to-julian-jaynes-1977-03-16",
        "author": "Philip K. Dick",
        "recipient": "Julian Jaynes",
        "date_start": "1977-03-16",
        "date_end": "1977-03-16",
        "date_display": "March 16, 1977",
        "date_confidence": "exact",
        "date_basis": "Selected Letters editorial date line",
        "timeline_type": "letter",
        "ingest_level": "full",
        "extraction_status": "complete",
        "is_pkd_authored": 1,
        "category": "letters",
        "evidentiary_lane": "E",
        "source_reliability": "primary_pkd",
        "source_letter_id": "LET_1977-03-16_JULIAN_JAYNES_0021",
        "card_summary": "PKD's March 16, 1977 letter to Julian Jaynes responding to The Origin of Consciousness in the Breakdown of the Bicameral Mind. The letter is a key primary witness for how Dick mapped Jaynes's bicameral theory onto VALIS, Zebra, right-hemisphere experience, and the March 1974 theophany.",
        "page_summary": "PKD writes Julian Jaynes after reading The Origin of Consciousness in the Breakdown of the Bicameral Mind and treats the book as immediately relevant to his own post-2-3-74 theorizing. He praises the theory, says he had been \"raving about it\" to his Bantam editor, and compares Jaynes's model of ancient divine voices with his own experience of Zagreus and right-hemisphere activation. The letter is especially important because it joins three evidence lanes at once: primary correspondence, late religious self-interpretation, and PKD's attempt to place VALIS/Zebra within contemporary psychology of consciousness.\n\nResearch uses: bicameral mind, Jaynes reception, VALIS, Zebra, right hemisphere, orthomolecular vitamin context, Deus Irae, A Scanner Darkly, and the shift from private theophany to quasi-scientific explanatory models.",
    },
    {
        "doc_id": "DOC_ARCH_LETTER_ON_STAR_WARS_1977_10_02",
        "doc_type": "letter",
        "title": "Letter on Star Wars",
        "slug": "letter-on-star-wars-1977-10-02",
        "author": "Philip K. Dick",
        "recipient": "Eugene Warren",
        "date_start": "1977-10-02",
        "date_end": "1977-10-02",
        "date_display": "October 2, 1977",
        "date_confidence": "exact",
        "date_basis": "Selected Letters editorial date line",
        "timeline_type": "letter",
        "ingest_level": "full",
        "extraction_status": "complete",
        "is_pkd_authored": 1,
        "category": "letters",
        "evidentiary_lane": "E",
        "source_reliability": "primary_pkd",
        "source_letter_id": "LET_1977-10-02_EUGENE_WARREN_0043",
        "card_summary": "PKD's October 2, 1977 letter to Eugene Warren interpreting Star Wars as a popular religious event. Dick compares Obi-Wan's posthumous voice to the voice he heard during the March 1974 VALIS experience and argues that George Lucas had translated Christian mystery into mass-cultural terms.",
        "page_summary": "Written just after the Metz trip, this letter records PKD's unusually strong theological reading of Star Wars. He compares Luke hearing Obi-Wan with his own report of hearing Jesus Christ when VALIS took him over in March 1974, and he frames Lucas's film as making \"the mystery of our religion\" newly legible through popular science fiction. The postscript is even stronger: Dick identifies his March 1974 experience with the Holy Spirit and says Star Wars has \"sensational importance and value\" because it reaches a secular mass audience.\n\nResearch uses: Star Wars reception, George Lucas, popular religion, VALIS, Holy Spirit, theolepsy, Maze of Death theology, Ubik as theological mediation, and PKD's late view that science fiction could carry religious truth under new names.",
    },
    {
        "doc_id": "DOC_ARCH_CLAUDIA_BUSH_LETTERS_CORPUS",
        "doc_type": "letter",
        "title": "Claudia Bush Letters",
        "slug": "claudia-bush-letters",
        "author": "Philip K. Dick",
        "recipient": "Claudia Bush",
        "date_start": "1975-01-15",
        "date_end": "1979-03-05",
        "date_display": "1975-1979",
        "date_confidence": "exact",
        "date_basis": "Segmented Selected Letters recipients and date lines",
        "timeline_type": "letter",
        "ingest_level": "full",
        "extraction_status": "complete",
        "is_pkd_authored": 1,
        "category": "letters",
        "evidentiary_lane": "E",
        "source_reliability": "primary_pkd",
        "source_letter_id": None,
        "card_summary": "A corpus-level document summary for PKD's letters to Claudia Bush/Bush Krenz, currently 27 segmented letters spanning 1975-1979. The correspondence is a major primary source for Dick's self-explanation after 2-3-74, his readings of his own fiction, and his exchange with a serious early scholar of his work.",
        "page_summary": "The Claudia Bush letters form one of the richest interpretive correspondences in the Selected Letters. Bush wrote seriously about Dick's work, and Dick used the exchange to test explanations of Ubik, Flow My Tears, The Man in the High Castle, The Lathe of Heaven, Zebra, the right hemisphere, the 1971 break-in, and his post-2-3-74 religious model. The corpus is valuable because it shows Dick writing to a knowledgeable reader who was neither merely a fan nor merely an editor: he is often reflective, argumentative, speculative, and autobiographical in the same letter.\n\nCurrent segmentation finds 27 Claudia Bush/Bush Krenz letters from January 1975 through March 1979. This document should be treated as a corpus wrapper; individual high-value letters can still receive their own document records when they become focal evidence.",
    },
    {
        "doc_id": "DOC_ARCH_MAZE_OF_DEATH_THEOLOGY_PENDING",
        "doc_type": "other",
        "title": "Maze of Death Theology",
        "slug": "maze-of-death-theology",
        "author": "Philip K. Dick",
        "recipient": None,
        "date_start": None,
        "date_end": None,
        "date_display": "Undated / source PDF needed",
        "date_confidence": "unknown",
        "date_basis": "User-identified unpublished document; source file not yet located in archive by title search",
        "timeline_type": "unknown",
        "ingest_level": "metadata_only",
        "extraction_status": "pending",
        "is_pkd_authored": 1,
        "category": "primary",
        "evidentiary_lane": "B",
        "source_reliability": "primary_pkd",
        "source_letter_id": None,
        "card_summary": "Pending document summary for the unpublished PKD document referred to as Maze of Death Theology. A title/slug search did not locate a matching PDF in the current archive, so this entry marks the item as a known desideratum for upload, OCR, and summary.",
        "page_summary": "This is a placeholder for an unpublished primary document the project identifies as Maze of Death Theology. It is likely relevant to PKD's explicit theological framing of A Maze of Death and to the larger problem of how pre-1974 theological fiction becomes reinterpreted after 2-3-74. The source PDF has not yet been matched in the local archive by title, slug, or summary search. Once supplied, it should be ingested as a primary PKD document, linked to A Maze of Death, Ubik, VALIS, and the religious-thought biography events, and mined for quotations and claims.",
    },
]


BIO_UPDATES = {
    "pkd_bio_1977_jaynes_letter": {
        "event": "Writes Julian Jaynes after reading The Origin of Consciousness in the Breakdown of the Bicameral Mind, praising the theory and comparing Jaynes's divine-voice model to his own March 1974 right-hemisphere/Zagreus experience.",
        "notes": "Short quotations to foreground in display: \"raving about it\" and \"Zagreus awaken in my right hemisphere.\" Letter id: LET_1977-03-16_JULIAN_JAYNES_0021.",
    },
    "pkd_bio_1977_star_wars_warren": {
        "event": "Writes Eugene Warren that Star Wars has religious importance because it makes Christian mystery available through popular science-fiction imagery, comparing Obi-Wan's voice to the voice he heard when VALIS took him over in March 1974.",
        "notes": "Short quotations to foreground in display: \"mystery of our religion\" and \"Word and Hand of God.\" Letter id: LET_1977-10-02_EUGENE_WARREN_0043.",
    },
}


def word_count(text: str) -> int:
    return len((text or "").split())


def body_for_letter(con: sqlite3.Connection, letter_id: str | None) -> str | None:
    if not letter_id:
        return None
    row = con.execute("SELECT body_md FROM letters WHERE letter_id = ?", (letter_id,)).fetchone()
    return row[0] if row else None


def claudia_corpus_text(con: sqlite3.Connection) -> str:
    rows = con.execute(
        """SELECT letter_id, date_start, recipient_raw, body_md
           FROM letters
           WHERE recipient_raw LIKE 'Claudia Bush%'
           ORDER BY date_start, letter_id"""
    ).fetchall()
    parts = []
    for letter_id, date_start, recipient, body in rows:
        parts.append(f"## {letter_id} | {date_start or 'undated'} | {recipient}\n\n{body}")
    return "\n\n---\n\n".join(parts)


def upsert_document(con: sqlite3.Connection, doc: dict) -> None:
    now = dt.datetime.now(dt.UTC).isoformat(timespec="seconds")
    source_letter_id = doc.pop("source_letter_id", None)
    if doc["doc_id"] == "DOC_ARCH_CLAUDIA_BUSH_LETTERS_CORPUS":
        text = claudia_corpus_text(con)
    elif source_letter_id:
        text = body_for_letter(con, source_letter_id)
    else:
        text = None
    wc = word_count(text or "")
    text_char_count = len(text or "")

    con.execute(
        """INSERT OR REPLACE INTO documents (
            doc_id, doc_type, title, slug, author, recipient,
            date_start, date_end, date_display, date_confidence, date_basis,
            timeline_type, ingest_level, extraction_status, is_pkd_authored,
            word_count, page_count, source_filename, text_char_count,
            card_summary, page_summary, category, notes,
            evidentiary_lane, source_reliability, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            doc["doc_id"], doc["doc_type"], doc["title"], doc["slug"],
            doc["author"], doc["recipient"], doc["date_start"], doc["date_end"],
            doc["date_display"], doc["date_confidence"], doc["date_basis"],
            doc["timeline_type"], doc["ingest_level"], doc["extraction_status"],
            doc["is_pkd_authored"], wc or None, None,
            source_letter_id or "pending-source-pdf" if doc["extraction_status"] == "pending" else source_letter_id,
            text_char_count or None, doc["card_summary"], doc["page_summary"],
            doc["category"], f"Curated from letter_id={source_letter_id}" if source_letter_id else doc.get("notes"),
            doc["evidentiary_lane"], doc["source_reliability"], now,
        ),
    )

    if text is not None:
        con.execute(
            """INSERT OR REPLACE INTO document_texts (
                text_id, doc_id, extraction_method, extraction_status,
                text_content, char_count, created_at,
                markdown_content, markdown_method, markdown_status,
                markdown_char_count, markdown_updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                f"TXT_{doc['doc_id']}", doc["doc_id"], "manual",
                "complete", text, len(text), now, text, "letters_table_curated",
                "complete", len(text), now,
            ),
        )


def update_curated_bio() -> int:
    data = json.loads(CURATED_PATH.read_text(encoding="utf-8"))
    changed = 0
    for event in data:
        patch = BIO_UPDATES.get(event.get("id"))
        if not patch:
            continue
        for key, value in patch.items():
            if event.get(key) != value:
                event[key] = value
                changed += 1
    CURATED_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return changed


def main() -> int:
    con = sqlite3.connect(DB_PATH, timeout=30)
    for raw_doc in DOCS:
        upsert_document(con, dict(raw_doc))
    con.commit()
    con.close()
    changed = update_curated_bio()
    print(f"[done] upserted {len(DOCS)} document summaries")
    print(f"[done] updated {changed} curated biography fields")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
