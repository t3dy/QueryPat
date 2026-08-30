#!/usr/bin/env python3
"""Build an index of readable primary fiction text.

The reading corpus (``database/extracted_markdown/``) is local, git-ignored and
regenerable. This script does **not** copy any of it. It emits a manifest of
*locators* — file, line range, word count — so later reading passes can open
exactly the span they need without the text itself ever entering the canonical
database, the exports, or version control.

Outputs ``artifacts/generated/reading/corpus_manifest.json`` (derived data;
delete and re-run to rebuild).

Usage:
    python scripts/reading/corpus_index.py            # build manifest
    python scripts/reading/corpus_index.py --report   # build + print coverage
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import unicodedata
from dataclasses import asdict, dataclass
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[2]
CORPUS_DIR = PROJECT / "database" / "extracted_markdown"
DB_PATH = PROJECT / "database" / "unified.sqlite"
OUT_PATH = PROJECT / "artifacts" / "generated" / "reading" / "corpus_manifest.json"

# Headings that look like story titles but are front/back matter.
NON_STORY_HEADINGS = {
    "contents", "preface", "introduction", "foreword", "afterword",
    "in memory", "of", "philip k. dick", "all rights reserved",
    "oceanofpdf.com", "u/m", "notes", "acknowledgments", "acknowledgements",
    "about the author", "copyright", "dedication", "index", "appendix",
    "bibliography", "a note on the text", "editor's note", "publication history",
}

# A heading introducing a story is followed by prose; front matter is not.
MIN_STORY_WORDS = 400

# Volume/part dividers inside an omnibus.
DIVIDER_RE = re.compile(
    r"^\**\s*(volume|part|book)\s+(one|two|three|four|five|six|\d+)\b", re.I
)


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return re.sub(r"-{2,}", "-", text)


# A heading that trails into punctuation is a line of prose the PDF-to-markdown
# conversion promoted by accident, not a title.
BAD_TAIL = (":", "?", '"', "\u201d", ",", ";", "\u2014", "-")


def heading_is_titlelike(raw: str) -> bool:
    """Story titles in these scans are set in full capitals.

    That single fact removes most of the false headings the conversion
    introduces (dialogue lines, running heads, catalogue copy). Checked on the
    raw heading, before it is title-cased for display.
    """
    core = re.sub(r"^#{1,6}\s*", "", raw).strip()
    core = re.sub(r"[*_`]+", "", core).strip()
    if not core or core.endswith(BAD_TAIL):
        return False
    alpha = "".join(c for c in core if c.isalpha())
    return bool(alpha) and alpha.isupper()


def clean_heading(raw: str) -> str:
    """`## **BEYOND LIES THE WUB** ` -> `Beyond Lies the Wub`."""
    text = re.sub(r"^#{1,6}\s*", "", raw).strip()
    text = re.sub(r"[*_`]+", "", text).strip()
    text = re.sub(r"\s+", " ", text)
    # Titles in these scans are shouted; title-case them but keep real acronyms.
    if text.isupper():
        text = " ".join(
            w if (len(w) <= 3 and w.isalpha() and w in {"PKD", "SF", "UM"}) else w.capitalize()
            for w in text.split()
        )
    return text


@dataclass
class Unit:
    """One readable span: a whole novel, or one story inside a collection."""

    unit_id: str
    title: str
    kind: str  # story | novel | collection_front_matter
    source_file: str  # relative to project root
    line_start: int
    line_end: int
    word_count: int
    container: str | None = None  # collection this story sits in
    reject_reason: str = ""  # why a heading was not treated as a story


def split_headed_file(path: Path, container_title: str | None) -> list[Unit]:
    """Split a markdown file into units at `##` headings."""
    rel = path.relative_to(PROJECT).as_posix()
    lines = path.read_text(encoding="utf-8", errors="replace").split("\n")

    heads: list[tuple[int, str, bool]] = [
        (i, clean_heading(l), heading_is_titlelike(l))
        for i, l in enumerate(lines)
        if re.match(r"^#{2}\s", l)
    ]
    if not heads:
        words = sum(len(l.split()) for l in lines)
        return [
            Unit(
                unit_id=f"UNIT_{slugify(path.stem)}",
                title=container_title or path.stem,
                kind="novel",
                source_file=rel,
                line_start=0,
                line_end=len(lines) - 1,
                word_count=words,
                container=None,
            )
        ]

    units: list[Unit] = []
    for idx, (line_no, title, titlelike) in enumerate(heads):
        end = heads[idx + 1][0] - 1 if idx + 1 < len(heads) else len(lines) - 1
        body = lines[line_no + 1 : end + 1]
        words = sum(len(l.split()) for l in body)

        norm = title.lower().strip()
        if norm in NON_STORY_HEADINGS or DIVIDER_RE.match(title) or not norm:
            kind = "collection_front_matter"
            reason = "front matter or divider"
        elif not titlelike:
            kind = "rejected"
            reason = "heading was not set in capitals"
        elif words < MIN_STORY_WORDS:
            kind = "rejected"
            reason = f"only {words} words follow the heading"
        else:
            kind = "story"
            reason = ""

        units.append(
            Unit(
                unit_id=f"UNIT_{slugify(path.stem)[:28]}_{slugify(title)[:40] or idx}",
                title=title,
                kind=kind,
                source_file=rel,
                line_start=line_no,
                line_end=end,
                word_count=words,
                container=container_title,
            )
        )
        if kind == "rejected":
            units[-1].reject_reason = reason
    return units


def classify_source(path: Path) -> str:
    """Rough bucket for a corpus file, from its name."""
    n = path.stem.upper()
    if "COLLECTED_STORIES" in n or "SELECTED_STORIES" in n or "MEGAPACK" in n \
            or "PHILIP_K_DICK_READER" in n or "MINORITY_REPORT_AND_OTHER" in n:
        return "fiction_collection"
    if "EXEGESIS" in n:
        return "pkd_exegesis"
    if "SELECTED_LETTERS" in n or "LETTERS" in n:
        return "pkd_letters"
    if "IN_PURSUIT_OF_VALIS" in n or "HOW_TO_BUILD" in n or "SHIFTING_REALITIES" in n:
        return "pkd_nonfiction"
    return "other"


def build(db: sqlite3.Connection) -> dict:
    if not CORPUS_DIR.exists():
        raise SystemExit(
            f"Reading corpus not found at {CORPUS_DIR}.\n"
            "It is git-ignored and regenerable — rebuild it before indexing."
        )

    files = sorted(CORPUS_DIR.glob("*.md"))
    units: list[Unit] = []
    sources: list[dict] = []

    for path in files:
        bucket = classify_source(path)
        size = path.stat().st_size
        sources.append({"file": path.relative_to(PROJECT).as_posix(),
                        "bucket": bucket, "bytes": size})
        if bucket == "fiction_collection":
            units.extend(split_headed_file(path, container_title=clean_heading(path.stem)))

    stories = [u for u in units if u.kind == "story"]

    # Collapse the same story appearing in several collections; keep the
    # longest span, remember every place it occurs.
    by_title: dict[str, list[Unit]] = {}
    for u in stories:
        by_title.setdefault(slugify(u.title), []).append(u)

    # A heading the conversion dropped leaves its story fused onto the one
    # before it. Length is the tell: PKD short stories run to a few thousand
    # words, so anything far above that is probably two stories in one span.
    # Flagged rather than dropped — several genuine novellas live up here.
    SUSPECT_WORDS = 9000

    deduped = []
    for key, group in sorted(by_title.items()):
        group.sort(key=lambda u: -u.word_count)
        best = asdict(group[0])
        if best["word_count"] >= SUSPECT_WORDS:
            best["needs_review"] = (
                f"{best['word_count']:,} words is long for a short story - "
                "check whether a missing heading fused two stories together"
            )
        best["also_in"] = [
            {"source_file": g.source_file, "line_start": g.line_start,
             "line_end": g.line_end, "word_count": g.word_count}
            for g in group[1:]
        ]
        best["title_key"] = key
        deduped.append(best)

    rejects = sorted(
        (asdict(u) for u in units if u.kind == "rejected"),
        key=lambda u: -u["word_count"],
    )

    return {
        "generated_by": "scripts/reading/corpus_index.py",
        "note": (
            "Locators only. No primary text is stored here; open the source file "
            "at the given line range to read a unit."
        ),
        "source_files": sources,
        "story_units": deduped,
        "front_matter_skipped": sum(1 for u in units if u.kind == "collection_front_matter"),
        "rejected_headings": rejects,
    }


def report(manifest: dict, db: sqlite3.Connection) -> None:
    stories = manifest["story_units"]
    words = sum(s["word_count"] for s in stories)
    print(f"Corpus files scanned : {len(manifest['source_files'])}")
    buckets: dict[str, int] = {}
    for s in manifest["source_files"]:
        buckets[s["bucket"]] = buckets.get(s["bucket"], 0) + 1
    for b, n in sorted(buckets.items(), key=lambda kv: -kv[1]):
        print(f"  {n:>4}  {b}")
    print()
    print(f"Distinct stories found: {len(stories)}")
    print(f"Total story words     : {words:,}")
    print(f"Front matter skipped  : {manifest['front_matter_skipped']}")
    print(f"Headings rejected     : {len(manifest['rejected_headings'])}"
          "  (listed in the manifest for review)")
    flagged = [s for s in stories if s.get("needs_review")]
    print(f"Units flagged for review: {len(flagged)}")
    if stories:
        longest = sorted(stories, key=lambda s: -s["word_count"])[:5]
        print("\nLongest units:")
        for s in longest:
            print(f"  {s['word_count']:>7,}w  {s['title'][:56]}")
        shortest = sorted(stories, key=lambda s: s["word_count"])[:5]
        print("Shortest units (check these for mis-splits):")
        for s in shortest:
            print(f"  {s['word_count']:>7,}w  {s['title'][:56]}")

    have = {s["title_key"] for s in stories}
    rows = db.execute(
        "select canonical_title, slug from works where category='short_stories'"
    ).fetchall()
    matched = [r for r in rows if slugify(r[0]) in have]
    print(f"\nworks rows in category 'short_stories': {len(rows)}"
          f"  (of which individual stories matched in corpus: {len(matched)})")
    print("NOTE: most of those rows are collections, not individual stories.")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true", help="print coverage summary")
    args = ap.parse_args()

    db = sqlite3.connect(DB_PATH)
    manifest = build(db)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(manifest, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {OUT_PATH.relative_to(PROJECT)}")
    if args.report:
        print()
        report(manifest, db)


if __name__ == "__main__":
    main()
