"""Segment a Selected Letters volume into individual letters.

Reads the markdown_content from document_texts for the six letters volumes,
splits each into individual letters, and writes a `letters` table row per
letter.

Usage:
    python scripts/letters/segment.py [--db PATH] [--volume DOC_ID]
    # default: process all six volumes
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sqlite3
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

LETTERS_VOLUMES = [
    "DOC_ARCH_OCEANOFPDF_COM_THE_SELECTED_LETTERS_VOLU",
    "DOC_ARCH_PHILIP_K_DICK_THE_SELECTED_LETTERS_OF_PH",
    "DOC_ARCH_OCEANOFPDF_COM_SELECTED_LETTERS_OF_PHILI",
    "DOC_ARCH_PHILIP_K_DICK_PAUL_WILLIAMS_SELECTED_LET",
    "DOC_ARCH_THE_SELECTED_LETTERS_OF_PHILIP_K_DICK_19",
    "DOC_ARCH_PKD_CORRESPONDENCE_THE_DARK_HAIRED_GIRL",
]

# ---------------------------------------------------------------------------
# Date parsing


MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12,
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "jun": 6, "jul": 7, "aug": 8,
    "sept": 9, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}

# Editorial header that opens each letter in the Selected Letters volumes:
#   [TO ANDRZEJ KURZ, MARIA KANIOWA, _Editors, Wydawnictwo Literackie, Poland]_
# The "TO" word may be followed by a comma+editorial-context blob.
LETTER_HEADER_RE = re.compile(
    r"(?:\[\s*TO\s+(?P<recipient>[^\]\n]{2,200}?)\s*\]_?"
    r"|^\s*#{1,4}\s*I?TO\s+(?P<recipient_ocr>[A-Z][A-Z0-9 .,&'\-]{2,200}?)[j\]]?\s*$)",
    re.IGNORECASE | re.MULTILINE,
)

# OCR-tolerant month tokens. The published volumes have many character-corruption
# artifacts ("]anuary" for "January", "Februar^/" for "February", etc.).
MONTH_PATTERN = (
    r"(?:[\]\[\(\)\{\}\|\\/\*]?[A-Za-z][a-z]+[\]\[\(\)\{\}\|\\/\*]?\.?)"
)

# Date line as italicized text after a [TO ...] header. Tolerates OCR errors.
DATE_LINE_RE = re.compile(
    r"_?\s*"                                     # leading italic marker
    r"(?P<month>" + MONTH_PATTERN + r")\s+"     # OCR'd month
    r"(?P<day>\d{1,2})\s*,?\s*"                 # day
    r"(?P<year>(?:19|20)\d{2})"                  # 4-digit year
    r"\s*_?",                                    # trailing italic marker
)

# Numeric / ISO date (1972-03-14)
ISO_DATE_RE = re.compile(
    r"(?P<year>(?:19|20)\d{2})-(?P<month_num>\d{1,2})-(?P<day>\d{1,2})"
)

# Slash date: 3/14/72 or 1/26/1975 — common in letterheads
SLASH_DATE_RE = re.compile(
    r"_?\s*(?P<month_num>\d{1,2})/(?P<day>\d{1,2})/(?P<year>\d{2,4})\s*_?"
)

# Standalone date heading (legacy support for "March 14, 1972" on its own line)
DATE_HEADING_RE = re.compile(
    r"""
    ^\s*\#{0,4}\s*_?\s*
    (?:
        (?P<m1>""" + MONTH_PATTERN + r""")\s+(?P<d1>\d{1,2})(?:,)?\s+(?P<y1>\d{4})
        |
        (?P<d2>\d{1,2})\s+(?P<m2>""" + MONTH_PATTERN + r""")\s+(?P<y2>\d{4})
        |
        (?P<y3>\d{4})-(?P<mn3>\d{2})-(?P<d3>\d{2})
    )
    \s*_?\s*$
    """,
    re.VERBOSE | re.MULTILINE,
)

SALUTATION_RE = re.compile(
    r"^\s*Dear\s+(?P<recipient>[A-Z][A-Za-z'\-\.&,\s]{1,80}?)[,:]?\s*$",
    re.MULTILINE,
)


# OCR fixups for month tokens — strip non-alpha characters, lowercase.
def normalize_month_token(tok: str) -> str:
    return re.sub(r"[^A-Za-z]", "", tok).lower()


# OCR-resilient month lookup: strips non-alpha, then tries:
#   1. exact match in MONTHS
#   2. unique substring match (e.g. "anuary" -> January, "ebruary" -> February)
def fuzzy_month_lookup(tok: str) -> int | None:
    norm = normalize_month_token(tok)
    if not norm:
        return None
    if norm in MONTHS:
        return MONTHS[norm]
    # Substring fallback: find a full month name where `norm` is a 4+-char suffix.
    if len(norm) >= 4:
        candidates = {m: v for m, v in MONTHS.items() if len(m) > 4 and norm in m}
        # Distinct months only (skip alias collisions where the value is the same)
        unique_values = set(candidates.values())
        if len(unique_values) == 1:
            return next(iter(unique_values))
    return None


def _try_parse(month_tok: str | None, day: str | None, year: str | None,
               month_num: str | None = None, raw: str = "") -> tuple[str, str, str, str]:
    """Try to construct an ISO date from parts. Tolerate OCR'd months."""
    try:
        if month_tok and not month_num:
            m = fuzzy_month_lookup(month_tok)
            if not m:
                return ("", "", raw, "approximate")
        else:
            m = int(month_num) if month_num else None
        if not m:
            return ("", "", raw, "approximate")
        d = int(day) if day else None
        y = int(year) if year else None
        if not (d and y):
            return ("", "", raw, "year")
        iso = dt.date(y, m, d).isoformat()
        return (iso, iso, raw, "exact")
    except (ValueError, TypeError):
        return ("", "", raw, "approximate")


def parse_date_text(text: str) -> tuple[str, str, str, str]:
    """Find the first parseable date in `text`, return (start, end, display, confidence)."""
    iso_m = ISO_DATE_RE.search(text)
    if iso_m:
        return _try_parse(None, iso_m.group("day"), iso_m.group("year"),
                          month_num=iso_m.group("month_num"), raw=iso_m.group(0))
    line_m = DATE_LINE_RE.search(text)
    if line_m:
        return _try_parse(line_m.group("month"), line_m.group("day"),
                          line_m.group("year"), raw=line_m.group(0).strip())
    slash_m = SLASH_DATE_RE.search(text)
    if slash_m:
        # Expand 2-digit years: PKD active 1938-1982 -> add "19"
        year = slash_m.group("year")
        if len(year) == 2:
            year = "19" + year if int(year) >= 38 else "20" + year
        return _try_parse(None, slash_m.group("day"), year,
                          month_num=slash_m.group("month_num"), raw=slash_m.group(0).strip())
    return ("", "", "", "approximate")


def parse_date(match: re.Match) -> tuple[str, str, str, str]:
    """Legacy: parse from a DATE_HEADING_RE match (standalone heading lines)."""
    g = match.groupdict()
    raw = match.group(0).strip()
    if g.get("y1"):
        return _try_parse(g["m1"], g["d1"], g["y1"], raw=raw)
    if g.get("y2"):
        return _try_parse(g["m2"], g["d2"], g["y2"], raw=raw)
    if g.get("y3"):
        return _try_parse(None, g["d3"], g["y3"], month_num=g["mn3"], raw=raw)
    return ("", "", raw, "approximate")


# ---------------------------------------------------------------------------
# Segmentation


@dataclass
class Letter:
    letter_id: str
    volume_doc_id: str
    sequence_in_volume: int
    date_start: str
    date_end: str
    date_display: str
    date_confidence: str
    recipient_raw: str
    recipient_canonical: str  # filled later by name resolver
    sender_location: str
    word_count: int
    body_md: str


def slugify(s: str, maxlen: int = 30) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_").upper()
    return s[:maxlen] or "UNKNOWN"


def segment_volume(volume_doc_id: str, md: str) -> list[Letter]:
    """Split a volume markdown into letters.

    Strategy:
      1. Primary: split on `[TO RECIPIENT]` editorial headers (the published
         Selected Letters edition uses these consistently).
      2. Fallback: standalone date heading lines (works for some volumes /
         some custom collections).
      3. The salutation regex inside the slice records the recipient form.
    """
    headers = list(LETTER_HEADER_RE.finditer(md))
    if len(headers) < 5:
        # Volume doesn't use [TO ...] format — fall back to date headings.
        return _segment_by_date_heading(volume_doc_id, md)

    letters: list[Letter] = []
    for i, h in enumerate(headers):
        # Slice from this header's END to the next header's START (or EOF).
        body_start = h.end()
        body_end = headers[i + 1].start() if i + 1 < len(headers) else len(md)
        block = md[body_start:body_end]

        # The first 600 chars after the header should contain the date line + salutation.
        head_window = block[:800]
        date_start, date_end, date_display, date_conf = parse_date_text(head_window)

        # Recipient: prefer the [TO X] header (clean), fall back to the salutation.
        recipient_raw = (h.group("recipient") or h.group("recipient_ocr") or "").strip()
        # Strip trailing "_]" italic markup and editorial parentheticals like
        # "ANDRZEJ KURZ, MARIA KANIOWA, _Editors, Wydawnictwo Literackie, Poland_"
        # — keep up to the first comma followed by an italicized blob.
        recipient_clean = re.split(r",\s*_", recipient_raw, maxsplit=1)[0].strip()
        # Title-case if everything is uppercase (the volumes use ALL CAPS)
        if recipient_clean.isupper():
            recipient_clean = recipient_clean.title()

        body = block.strip()
        word_count = len(body.split())
        if word_count < 30:
            continue

        seq = len(letters) + 1
        slug = slugify(recipient_clean or "UNKNOWN")
        date_part = date_start or "UNDATED"
        letter_id = f"LET_{date_part}_{slug}_{seq:04d}"

        letters.append(Letter(
            letter_id=letter_id,
            volume_doc_id=volume_doc_id,
            sequence_in_volume=seq,
            date_start=date_start,
            date_end=date_end,
            date_display=date_display or recipient_clean,
            date_confidence=date_conf,
            recipient_raw=recipient_clean,
            recipient_canonical="",
            sender_location="",
            word_count=word_count,
            body_md=body,
        ))
    return letters


def _segment_by_date_heading(volume_doc_id: str, md: str) -> list[Letter]:
    """Fallback: split on standalone date heading lines."""
    matches = list(DATE_HEADING_RE.finditer(md))
    letters: list[Letter] = []
    for i, m in enumerate(matches):
        body_start = m.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(md)
        body = md[body_start:body_end].strip()
        if len(body) < 50:
            continue
        date_start, date_end, date_display, date_conf = parse_date(m)
        sal = SALUTATION_RE.search(body[:600])
        recipient_raw = sal.group("recipient").strip() if sal else ""
        word_count = len(body.split())
        if word_count < 30:
            continue
        seq = len(letters) + 1
        slug = slugify(recipient_raw or "UNKNOWN")
        date_part = date_start or "UNDATED"
        letter_id = f"LET_{date_part}_{slug}_{seq:04d}"
        letters.append(Letter(
            letter_id=letter_id, volume_doc_id=volume_doc_id, sequence_in_volume=seq,
            date_start=date_start, date_end=date_end, date_display=date_display,
            date_confidence=date_conf, recipient_raw=recipient_raw,
            recipient_canonical="", sender_location="", word_count=word_count, body_md=body,
        ))
    return letters


# ---------------------------------------------------------------------------
# DB I/O


SCHEMA = """
CREATE TABLE IF NOT EXISTS letters (
    letter_id TEXT PRIMARY KEY,
    volume_doc_id TEXT NOT NULL,
    sequence_in_volume INTEGER,
    date_start TEXT,
    date_end TEXT,
    date_display TEXT,
    date_confidence TEXT,
    recipient_raw TEXT,
    recipient_canonical TEXT,
    sender_location TEXT,
    word_count INTEGER,
    body_md TEXT,
    created_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_letters_date ON letters(date_start);
CREATE INDEX IF NOT EXISTS idx_letters_recipient ON letters(recipient_canonical);
"""


def ensure_schema(con: sqlite3.Connection) -> None:
    con.executescript(SCHEMA)


def upsert_letter(con: sqlite3.Connection, L: Letter) -> None:
    now = dt.datetime.now(dt.UTC).isoformat(timespec="seconds")
    con.execute(
        """INSERT OR REPLACE INTO letters
        (letter_id, volume_doc_id, sequence_in_volume, date_start, date_end,
         date_display, date_confidence, recipient_raw, recipient_canonical,
         sender_location, word_count, body_md, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (L.letter_id, L.volume_doc_id, L.sequence_in_volume, L.date_start, L.date_end,
         L.date_display, L.date_confidence, L.recipient_raw, L.recipient_canonical,
         L.sender_location, L.word_count, L.body_md, now),
    )


def fetch_volume_md(con: sqlite3.Connection, doc_id: str) -> str | None:
    cur = con.execute(
        "SELECT markdown_content FROM document_texts WHERE doc_id = ? AND markdown_content IS NOT NULL",
        (doc_id,),
    )
    row = cur.fetchone()
    return row[0] if row else None


# ---------------------------------------------------------------------------


def run(db_path: Path, volume_filter: str | None) -> dict:
    con = sqlite3.connect(db_path)
    ensure_schema(con)

    targets = [volume_filter] if volume_filter else LETTERS_VOLUMES
    summary = {}
    for vol in targets:
        md = fetch_volume_md(con, vol)
        if md is None:
            print(f"[skip] {vol}: no markdown_content available yet")
            summary[vol] = {"status": "no_markdown", "letters": 0}
            continue
        letters = segment_volume(vol, md)
        con.execute("DELETE FROM letters WHERE volume_doc_id = ?", (vol,))
        for L in letters:
            upsert_letter(con, L)
        con.commit()
        summary[vol] = {"status": "ok", "letters": len(letters),
                        "first": letters[0].date_display if letters else "",
                        "last": letters[-1].date_display if letters else ""}
        print(f"[done] {vol}: {len(letters)} letters segmented "
              f"({summary[vol]['first']} -> {summary[vol]['last']})")

    con.close()
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="C:/QueryPat/database/unified.sqlite")
    ap.add_argument("--volume", default=None)
    args = ap.parse_args()
    summary = run(Path(args.db), args.volume)
    total = sum(v.get("letters", 0) for v in summary.values())
    print(f"\nTotal letters segmented: {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
