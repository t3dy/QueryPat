#!/usr/bin/env python3
"""Gather the deterministic evidence behind a work's dossier.

This is the scripted half of the reading. It does the things a machine does
better than a reader — exhaustive matching, counting, locating — and leaves
interpretation to the reading pass that follows.

Four layers, matching the dossier structure:

  1. structure   chapter/section spans and their sizes
  2. concepts    dictionary TERM_* and NAME_* matched in the work's own text
  3. pkd_voice   where Dick discusses the work, in the Exegesis, letters, essays
  4. criticism   where critics discuss it, in the archive scholarship

Quotations are short keyword-in-context windows with a file-and-line locator,
in the manner of the existing evidence_excerpts table: enough to see what is
being said and to go and read it, never enough to stand in for the source.

    python scripts/reading/gather_evidence.py --work ubik
    python scripts/reading/gather_evidence.py --all-pilot
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT / "database" / "unified.sqlite"
REGISTRY = Path(__file__).resolve().parent / "work_sources.json"
CORPUS_DIR = PROJECT / "database" / "extracted_markdown"
OUT_DIR = PROJECT / "artifacts" / "generated" / "reading" / "evidence"

# Keep quotation to a locator-plus-glimpse. Scholarly citation scale, not text.
KWIC_CHARS = 220
MAX_QUOTES_PER_SOURCE = 12

# Concept matching runs over n-grams of this length and below.
MAX_NGRAM = 4

# Terms this short are ordinary English and match everything; require the
# alias to be longer, or the term to be multi-word, before trusting a hit.
MIN_TERM_CHARS = 4

# The dictionary carries a noise_score, and it is a good filter: the 61 terms
# at 0.6-0.75 are function words ("Perhaps", "Because", "Could"), while 0.0-0.15
# holds the scholarly vocabulary (Shekhina, Orphism, Xenophanes, Timaeus).
MAX_NOISE_SCORE = 0.15

# Below this, a term is no more common in the work than in general prose.
MIN_DISTINCTIVENESS = 1.5

# A residual few score cleanly but are still ordinary English, so they would
# otherwise dominate any narrative text.
STOP_TERMS = {
    "himself", "herself", "itself", "themselves", "actually", "certainly",
    "nonetheless", "living", "real", "ground", "voice", "secret", "love",
    "one", "two", "man", "men", "way", "day", "time", "life", "world", "thing",
    "part", "form", "kind", "case", "fact", "hand", "eye", "eyes", "word",
    "words", "book", "state", "order", "place", "point", "end", "side",
    "complete", "indexed", "indexed folder", "the man", "the one",
}


def norm(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]+", " ", text)


def tokenize(text: str) -> list[str]:
    return norm(text).split()


# ── vocabulary ──────────────────────────────────────────────────────────

def load_vocabulary(db: sqlite3.Connection) -> dict[str, tuple[str, str, str]]:
    """phrase -> (entity_type, entity_id, display_name).

    Built from the dictionary's own terms and aliases and from the names table,
    so every concept hit resolves to an ID the rest of QueryPat already uses.
    """
    vocab: dict[str, tuple[str, str, str]] = {}

    def add(phrase: str, kind: str, ident: str, display: str) -> None:
        key = " ".join(tokenize(phrase))
        if not key or len(key) < MIN_TERM_CHARS:
            return
        if key in STOP_TERMS:
            return
        if len(key.split()) > MAX_NGRAM:
            return
        vocab.setdefault(key, (kind, ident, display))

    kept = db.execute(
        "select term_id, canonical_name from terms "
        " where status in ('accepted','provisional')"
        "   and coalesce(noise_score, 1.0) <= ?",
        (MAX_NOISE_SCORE,),
    ).fetchall()
    names_by_id = {t: n for t, n in kept}
    for term_id, name in kept:
        add(name, "term", term_id, name)
    for term_id, alias in db.execute("select term_id, alias_text from term_aliases"):
        if term_id in names_by_id:
            add(alias, "term", term_id, names_by_id[term_id])
    for name_id, form in db.execute(
        "select name_id, canonical_form from names where status in ('accepted','provisional')"
    ):
        add(form, "name", name_id, form)
    for name_id, alias in db.execute("select name_id, alias_text from name_aliases"):
        row = db.execute(
            "select canonical_form from names where name_id=?", (name_id,)
        ).fetchone()
        if row:
            add(alias, "name", name_id, row[0])
    return vocab


def count_vocabulary(text: str, vocab: dict) -> Counter:
    """Count every vocabulary phrase occurring in the text."""
    tokens = tokenize(text)
    hits: Counter[tuple[str, str, str]] = Counter()
    n = len(tokens)
    for size in range(MAX_NGRAM, 0, -1):
        for i in range(n - size + 1):
            phrase = " ".join(tokens[i : i + size])
            found = vocab.get(phrase)
            if found:
                hits[found] += 1
    return hits


def build_background(registry: dict, vocab: dict) -> tuple[Counter, int]:
    """Vocabulary frequencies across a general slice of the corpus.

    Terms like "Well" and "Look" score cleanly in the dictionary but occur
    everywhere, so raw counts inside one novel say nothing.

    The comparison has to be against other fiction, not against criticism.
    Measured against academic prose, ordinary dialogue ("Okay", "Anyhow",
    "Wait") looks highly distinctive simply because critics do not write
    dialogue. Measured against Dick's own stories, it washes out and what
    remains is the vocabulary this work actually turns on.
    """
    background: Counter = Counter()
    words = 0
    for entry in registry["story_collections"][:2]:
        path = PROJECT / entry["source_file"]
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        background += count_vocabulary(text, vocab)
        words += len(text.split())
    return background, words


def match_concepts(text: str, vocab: dict, background: Counter,
                   background_words: int) -> list[dict]:
    """Vocabulary hits, ranked by how distinctive they are to this text."""
    hits = count_vocabulary(text, vocab)
    work_words = max(1, len(text.split()))

    out = []
    for key, count in hits.items():
        kind, ident, label = key
        work_rate = count / work_words * 1_000_000
        bg_rate = (background.get(key, 0) / max(1, background_words)) * 1_000_000
        # +5 per million keeps a term that is merely absent from the background
        # from scoring infinitely high on a single occurrence.
        lift = work_rate / (bg_rate + 5.0)
        out.append({
            "entity_type": kind,
            "entity_id": ident,
            "label": label,
            "count": count,
            "per_million": round(work_rate, 1),
            "background_per_million": round(bg_rate, 1),
            "distinctiveness": round(lift, 2),
        })
    out.sort(key=lambda c: -c["distinctiveness"])
    return out


# ── discussion of a work elsewhere in the corpus ────────────────────────

def title_patterns(title: str, extra: list[str]) -> re.Pattern:
    forms = {title, *extra}
    # "The Game-Players of Titan" is also written without its hyphen or article.
    bare = re.sub(r"^(the|a|an)\s+", "", title, flags=re.I)
    forms.add(bare)
    forms.add(title.replace("-", " "))
    forms.add(bare.replace("-", " "))
    alts = sorted({re.escape(f.strip()) for f in forms if len(f.strip()) > 3}, key=len, reverse=True)
    # Tolerate the hyphen/space difference and runs of whitespace in scans.
    joined = "|".join(a.replace(r"\-", r"[-\s]").replace(r"\ ", r"\s+") for a in alts)
    return re.compile(rf"\b({joined})\b", re.I)


def kwic(text: str, match: re.Match, width: int = KWIC_CHARS) -> str:
    start = max(0, match.start() - width // 2)
    end = min(len(text), match.end() + width // 2)
    snippet = text[start:end].replace("\n", " ")
    snippet = re.sub(r"\s+", " ", snippet).strip()
    return ("…" if start > 0 else "") + snippet + ("…" if end < len(text) else "")


def find_discussion(sources: list[dict], pattern: re.Pattern, lane: str) -> list[dict]:
    out: list[dict] = []
    for entry in sources:
        path = PROJECT / entry["source_file"]
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        # Map character offsets to line numbers once per file.
        line_starts = [0]
        for m in re.finditer(r"\n", text):
            line_starts.append(m.end())

        found = list(pattern.finditer(text))
        if not found:
            continue

        quotes = []
        for m in found[:MAX_QUOTES_PER_SOURCE]:
            lineno = sum(1 for s in line_starts if s <= m.start())
            quotes.append({"line": lineno, "quote": kwic(text, m)})

        out.append({
            "source_file": entry["source_file"],
            "author": entry.get("author"),
            "lane": entry.get("lane", lane),
            "mention_count": len(found),
            "quotes": quotes,
            "quotes_truncated": max(0, len(found) - MAX_QUOTES_PER_SOURCE),
        })
    out.sort(key=lambda e: -e["mention_count"])
    return out


# ── work text ───────────────────────────────────────────────────────────

def read_work_text(entry: dict) -> tuple[str, list[dict]]:
    """Return the work's text and its chapter spans (may be empty)."""
    path = PROJECT / entry["source_file"]
    lines = path.read_text(encoding="utf-8", errors="replace").split("\n")

    start = entry.get("line_start") or 0
    end = entry.get("line_end") or len(lines) - 1
    lines = lines[start : end + 1]

    chapters: list[dict] = []
    pattern = entry.get("chapter_pattern")
    if pattern:
        rx = re.compile(pattern)
        marks = [(i, rx.match(l)) for i, l in enumerate(lines)]
        marks = [(i, m) for i, m in marks if m]
        for idx, (i, m) in enumerate(marks):
            stop = marks[idx + 1][0] - 1 if idx + 1 < len(marks) else len(lines) - 1
            body = lines[i + 1 : stop + 1]
            chapters.append({
                "label": m.group(1) if m.groups() else str(idx + 1),
                "line_start": start + i,
                "line_end": start + stop,
                "word_count": sum(len(l.split()) for l in body),
            })
    return "\n".join(lines), chapters


def story_entry(manifest: dict, title_key: str) -> dict | None:
    for unit in manifest["story_units"]:
        if unit["title_key"] == title_key:
            return unit
    return None


# ── main ────────────────────────────────────────────────────────────────

def gather(slug: str, db: sqlite3.Connection, registry: dict, vocab: dict,
           manifest: dict, background: Counter, background_words: int) -> dict:
    entry = next((n for n in registry["novels"] if n["slug"] == slug), None)
    kind = "novel"
    if entry is None:
        entry = story_entry(manifest, slug)
        kind = "story"
    if entry is None:
        raise SystemExit(f"No source registered for {slug!r}")
    if entry.get("status") == "no_primary_text":
        raise SystemExit(f"{slug}: {entry['verified']}")

    title = entry.get("title") or entry.get("title")
    text, chapters = read_work_text(entry)
    words = len(text.split())

    pattern = title_patterns(title, [])
    pkd = find_discussion(registry["pkd_own_voice"], pattern, lane="B")
    crit = find_discussion(registry["criticism"], pattern, lane="C")

    concepts = [
        c for c in match_concepts(text, vocab, background, background_words)
        if c["distinctiveness"] >= MIN_DISTINCTIVENESS
    ]

    return {
        "slug": slug,
        "title": title,
        "kind": kind,
        "generated_by": "scripts/reading/gather_evidence.py",
        "source": {
            "file": entry["source_file"],
            "line_start": entry.get("line_start", 0),
            "line_end": entry.get("line_end"),
            "word_count": words,
            "status": entry.get("status", "ready"),
        },
        "structure": {
            "chapter_count": len(chapters),
            "chapters": chapters,
        },
        "concepts": {
            "terms": [c for c in concepts if c["entity_type"] == "term"][:60],
            "names": [c for c in concepts if c["entity_type"] == "name"][:60],
            "distinct_terms": sum(1 for c in concepts if c["entity_type"] == "term"),
            "distinct_names": sum(1 for c in concepts if c["entity_type"] == "name"),
        },
        "pkd_on_this_work": {
            "sources": pkd,
            "total_mentions": sum(s["mention_count"] for s in pkd),
        },
        "criticism": {
            "sources": crit,
            "total_mentions": sum(s["mention_count"] for s in crit),
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", help="registry slug, or a story title_key")
    ap.add_argument("--all-pilot", action="store_true",
                    help="run the three pilot works")
    args = ap.parse_args()

    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    manifest = json.loads(
        (PROJECT / "artifacts/generated/reading/corpus_manifest.json").read_text(encoding="utf-8")
    )
    db = sqlite3.connect(DB_PATH)
    vocab = load_vocabulary(db)
    print(f"vocabulary: {len(vocab):,} phrases resolving to TERM_*/NAME_* ids")
    background, background_words = build_background(registry, vocab)
    print(f"background: {background_words:,} words of general prose for comparison")

    slugs = ["ubik", "the-game-players-of-titan", "second-variety"] if args.all_pilot \
        else [args.work]
    if not slugs or slugs == [None]:
        ap.error("pass --work or --all-pilot")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for slug in slugs:
        ev = gather(slug, db, registry, vocab, manifest, background, background_words)
        out = OUT_DIR / f"{slug}.evidence.json"
        out.write_text(json.dumps(ev, indent=1, ensure_ascii=False), encoding="utf-8")
        print(
            f"  {slug:<28} {ev['source']['word_count']:>7,}w"
            f"  chapters={ev['structure']['chapter_count']:>3}"
            f"  terms={ev['concepts']['distinct_terms']:>4}"
            f"  names={ev['concepts']['distinct_names']:>4}"
            f"  pkd={ev['pkd_on_this_work']['total_mentions']:>4}"
            f"  crit={ev['criticism']['total_mentions']:>4}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
