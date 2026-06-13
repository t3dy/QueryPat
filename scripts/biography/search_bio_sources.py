"""Search segmented letters and biographical sources for biography mining leads.

The script is intentionally deterministic: it records which terms were searched,
which sources were in scope, and sample contexts for each hit. It is meant to be
run before hand extraction so high-priority gaps do not depend on memory.

Usage:
    python scripts/biography/search_bio_sources.py --out BIO_SOURCE_SEARCH_REPORT.md
    python scripts/biography/search_bio_sources.py --json-out scratch/bio_hits.json
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
from dataclasses import asdict, dataclass
from pathlib import Path


DEFAULT_DB = Path("C:/QueryPat/database/unified.sqlite")
DEFAULT_OUT = Path("BIO_SOURCE_SEARCH_REPORT.md")

LETTER_VOLUME_IDS = [
    "DOC_ARCH_OCEANOFPDF_COM_THE_SELECTED_LETTERS_VOLU",
    "DOC_ARCH_PHILIP_K_DICK_THE_SELECTED_LETTERS_OF_PH",
    "DOC_ARCH_OCEANOFPDF_COM_SELECTED_LETTERS_OF_PHILI",
    "DOC_ARCH_PHILIP_K_DICK_PAUL_WILLIAMS_SELECTED_LET",
    "DOC_ARCH_THE_SELECTED_LETTERS_OF_PHILIP_K_DICK_19",
]

BIO_SOURCE_PATTERNS = [
    "%Divine Madness%",
    "%Divine Invasions%",
    "%Search for Philip K. Dick%",
    "%In Pursuit of VALIS%",
]

SEARCH_GROUPS = {
    "priority_requested": [
        "Julian Jaynes", "Jaynes", "Star Wars", "George Lucas",
    ],
    "sf_authors": [
        "Ursula", "Le Guin", "Roger Zelazny", "Zelazny", "Harlan Ellison",
        "Robert Heinlein", "Heinlein", "John Brunner", "Brian Aldiss",
        "Thomas Disch", "Theodore Sturgeon", "Isaac Asimov", "Fritz Leiber",
    ],
    "religion_visionary": [
        "2-3-74", "3-74", "pink light", "pink beam", "fish sign", "Zebra",
        "VALIS", "AI voice", "Sophia", "Holy Spirit", "anamnesis",
        "Black Iron Prison", "Bishop Pike", "Julian Jaynes",
    ],
    "drugs_health": [
        "amphetamine", "amphetamines", "speed", "LSD", "sodium pentothal",
        "X-Kalay", "Synanon", "overdose", "suicide", "psychiatrist",
        "hospital", "pancreatitis",
    ],
    "relationships_places_work": [
        "Nancy", "Tessa", "Anne", "Kleo", "Joan Simpson", "Linda Levy",
        "Doris Sauter", "University Radio", "Art Music", "Berkeley High",
        "California Preparatory", "Ojai", "Point Reyes", "Vancouver",
        "Fullerton", "Santa Ana",
    ],
    "works_periods": [
        "Solar Lottery", "The Man in the High Castle", "The Three Stigmata",
        "Do Androids Dream", "Ubik", "A Maze of Death", "Flow My Tears",
        "A Scanner Darkly", "VALIS", "The Divine Invasion",
        "The Transmigration of Timothy Archer", "The Owl in Daylight",
        "Deus Irae", "To Scare the Dead",
    ],
}


@dataclass
class Hit:
    scope: str
    group: str
    term: str
    source_id: str
    title: str
    date: str
    recipient: str
    context: str


def clean_context(text: str, term: str, width: int) -> str:
    idx = text.lower().find(term.lower())
    if idx < 0:
        idx = 0
    start = max(0, idx - width)
    end = min(len(text), idx + len(term) + width)
    context = re.sub(r"\s+", " ", text[start:end]).strip()
    return context


def fetch_bio_doc_ids(con: sqlite3.Connection) -> list[str]:
    doc_ids: list[str] = []
    for pattern in BIO_SOURCE_PATTERNS:
        rows = con.execute(
            """SELECT doc_id FROM documents
               WHERE title LIKE ? OR slug LIKE ? OR author LIKE ?
               ORDER BY doc_id""",
            (pattern, pattern, pattern),
        ).fetchall()
        doc_ids.extend(row[0] for row in rows)
    return sorted(set(doc_ids))


def search_letters(con: sqlite3.Connection, group: str, term: str, limit: int, width: int) -> list[Hit]:
    rows = con.execute(
        """SELECT letter_id, date_start, recipient_raw, body_md
           FROM letters
           WHERE volume_doc_id IN ({})
             AND (body_md LIKE ? OR recipient_raw LIKE ?)
           ORDER BY date_start, letter_id
           LIMIT ?""".format(",".join("?" for _ in LETTER_VOLUME_IDS)),
        (*LETTER_VOLUME_IDS, f"%{term}%", f"%{term}%", limit),
    ).fetchall()
    hits = []
    for letter_id, date, recipient, body in rows:
        hits.append(Hit(
            scope="letters",
            group=group,
            term=term,
            source_id=letter_id,
            title="Selected Letters",
            date=date or "",
            recipient=recipient or "",
            context=clean_context(body or recipient or "", term, width),
        ))
    return hits


def search_biographies(con: sqlite3.Connection, group: str, term: str, doc_ids: list[str], limit: int, width: int) -> list[Hit]:
    if not doc_ids:
        return []
    rows = con.execute(
        """SELECT d.doc_id, d.title, COALESCE(d.date_display, d.date_start, ''),
                  COALESCE(dt.markdown_content, dt.text_content, '')
           FROM document_texts dt
           JOIN documents d ON d.doc_id = dt.doc_id
           WHERE d.doc_id IN ({})
             AND COALESCE(dt.markdown_content, dt.text_content, '') LIKE ?
           ORDER BY d.title, d.doc_id
           LIMIT ?""".format(",".join("?" for _ in doc_ids)),
        (*doc_ids, f"%{term}%", limit),
    ).fetchall()
    hits = []
    for doc_id, title, date, text in rows:
        hits.append(Hit(
            scope="biographies",
            group=group,
            term=term,
            source_id=doc_id,
            title=title or "",
            date=date or "",
            recipient="",
            context=clean_context(text or "", term, width),
        ))
    return hits


def run(db_path: Path, per_term_limit: int, width: int) -> list[Hit]:
    con = sqlite3.connect(db_path)
    bio_doc_ids = fetch_bio_doc_ids(con)
    hits: list[Hit] = []
    for group, terms in SEARCH_GROUPS.items():
        for term in terms:
            hits.extend(search_letters(con, group, term, per_term_limit, width))
            hits.extend(search_biographies(con, group, term, bio_doc_ids, per_term_limit, width))
    con.close()
    return hits


def write_markdown(hits: list[Hit], out_path: Path) -> None:
    grouped: dict[tuple[str, str], list[Hit]] = {}
    for hit in hits:
        grouped.setdefault((hit.group, hit.term), []).append(hit)

    lines = [
        "# Biography Source Search Report\n\n",
        "Deterministic search over segmented Selected Letters plus key biography sources.\n\n",
        "## Hit Summary\n\n",
        "| Group | Term | Hits |\n|---|---|---:|\n",
    ]
    for (group, term), group_hits in sorted(grouped.items()):
        lines.append(f"| {group} | `{term}` | {len(group_hits)} |\n")

    lines.append("\n## Contexts\n\n")
    for (group, term), group_hits in sorted(grouped.items()):
        lines.append(f"### {group}: `{term}`\n\n")
        for hit in group_hits:
            label = hit.source_id
            if hit.scope == "letters":
                label += f" to {hit.recipient}"
            lines.append(f"- **{hit.scope}** `{label}` {hit.date}\n")
            lines.append(f"  {hit.context}\n")
        lines.append("\n")

    out_path.write_text("".join(lines), encoding="utf-8")
    print(f"[done] wrote {out_path} ({len(hits)} hits)")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DEFAULT_DB))
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    ap.add_argument("--json-out", default="")
    ap.add_argument("--per-term-limit", type=int, default=12)
    ap.add_argument("--width", type=int, default=260)
    args = ap.parse_args()

    hits = run(Path(args.db), args.per_term_limit, args.width)
    write_markdown(hits, Path(args.out))
    if args.json_out:
        Path(args.json_out).write_text(
            json.dumps([asdict(hit) for hit in hits], ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"[done] wrote {args.json_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
