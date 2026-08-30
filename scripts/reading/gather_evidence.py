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


def build_background(registry: dict, vocab: dict) -> tuple[Counter, int, Counter]:
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
    chunks: list[str] = []
    for entry in registry["story_collections"][:2]:
        loaded = load_corpus_file(entry["source_file"])
        if loaded is None:
            continue
        text = loaded[0]
        background += count_vocabulary(text, vocab)
        words += len(text.split())
        chunks.append(text)
    unigrams: Counter = Counter()
    for chunk in chunks:
        unigrams.update(tokenize(chunk))
    return background, words, unigrams


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

# Above this rate in ordinary fiction, a title is an ordinary phrase and
# "mentions" of it are mostly the language, not discussion of the work.
# "Presents" and "Colony" fail this; "Ubik" and "Second Variety" pass easily.
MAX_TITLE_RATE_PER_MILLION = 8.0


def looks_like_citation(matched: str) -> bool:
    """True when the matched text is capitalised the way a title is.

    A work referred to by name is capitalised — "Presents", "The Gun" — while
    the same words used ordinarily are not: "Dick's work presents", "he drew
    the gun". Searching case-insensitively and then keeping only the
    capitalised hits separates the two exactly, which no frequency heuristic
    managed to do. Titles inside a fully upper-case run (running heads, index
    lines) are also rejected.
    """
    words = [w for w in re.split(r"[\s-]+", matched.strip()) if w]
    if not words:
        return False
    if matched.isupper() and len(matched) > 3:
        return False
    lead = [w for w in words if w.lower() not in {"the", "a", "an", "of", "and", "for"}]
    return bool(lead) and all(w[:1].isupper() for w in lead)


def title_patterns(title: str, extra: list[str]) -> re.Pattern | None:
    """Search only for the title as written.

    An earlier version also searched for the title stripped of its article,
    which is what turned "The Gun" into a match on every "gun" in the archive.
    """
    if len(title.strip()) < 3:
        return None
    forms = {title.strip(), *extra}
    forms.add(title.strip().replace("-", " "))
    alts = sorted({re.escape(f) for f in forms if len(f) > 2}, key=len, reverse=True)
    joined = "|".join(
        a.replace(r"\-", r"[-\s]").replace(r"\ ", r"\s+") for a in alts
    )
    return re.compile(r"\b(" + joined + r")\b", re.I)


def kwic(text: str, match: re.Match, width: int = KWIC_CHARS) -> str:
    start = max(0, match.start() - width // 2)
    end = min(len(text), match.end() + width // 2)
    snippet = text[start:end].replace("\n", " ")
    snippet = re.sub(r"\s+", " ", snippet).strip()
    return ("…" if start > 0 else "") + snippet + ("…" if end < len(text) else "")


# file path -> (text, line_start_offsets). Reading the letters, the Exegesis and
# eight critical books once instead of once per work is the difference between
# a corpus-wide run taking minutes and taking hours.
_CORPUS_CACHE: dict[str, tuple[str, list[int]]] = {}


def load_corpus_file(rel: str) -> tuple[str, list[int]] | None:
    if rel in _CORPUS_CACHE:
        return _CORPUS_CACHE[rel]
    path = PROJECT / rel
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8", errors="replace")
    starts = [0]
    for m in re.finditer(r"\n", text):
        starts.append(m.end())
    _CORPUS_CACHE[rel] = (text, starts)
    return _CORPUS_CACHE[rel]


def line_of(starts: list[int], offset: int) -> int:
    """Binary search the line number for a character offset."""
    lo, hi = 0, len(starts) - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if starts[mid] <= offset:
            lo = mid
        else:
            hi = mid - 1
    return lo + 1


def find_discussion(sources: list[dict], pattern: re.Pattern, lane: str) -> list[dict]:
    out: list[dict] = []
    for entry in sources:
        loaded = load_corpus_file(entry["source_file"])
        if loaded is None:
            continue
        text, line_starts = loaded

        found = [m for m in pattern.finditer(text) if looks_like_citation(m.group(0))]
        if not found:
            continue

        quotes = []
        for m in found[:MAX_QUOTES_PER_SOURCE]:
            quotes.append({"line": line_of(line_starts, m.start()), "quote": kwic(text, m)})

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
    loaded = load_corpus_file(entry["source_file"])
    if loaded is None:
        raise SystemExit(f"missing corpus file: {entry['source_file']}")
    lines = loaded[0].split("\n")

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
           manifest: dict, background: Counter, background_words: int,
           unigrams: Counter) -> dict:
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
    if pattern is None:
        pkd, crit = [], []
    else:
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
        "title_search": {
            "method": (
                "Case-insensitive search for the title as written, keeping only "
                "matches capitalised as a citation. This is what separates the "
                "story 'Presents' from the verb 'presents'."
            ),
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
    ap.add_argument("--all-stories", action="store_true",
                    help="run every story in the corpus manifest")
    ap.add_argument("--all-novels", action="store_true",
                    help="run every novel with readable primary text")
    ap.add_argument("--min-words", type=int, default=1200,
                    help="skip units shorter than this (default 1200)")
    args = ap.parse_args()

    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    manifest = json.loads(
        (PROJECT / "artifacts/generated/reading/corpus_manifest.json").read_text(encoding="utf-8")
    )
    db = sqlite3.connect(DB_PATH)
    vocab = load_vocabulary(db)
    print(f"vocabulary: {len(vocab):,} phrases resolving to TERM_*/NAME_* ids")
    background, background_words, unigrams = build_background(registry, vocab)
    print(f"background: {background_words:,} words of general prose for comparison")

    slugs: list[str] = []
    if args.all_pilot:
        slugs = ["ubik", "the-game-players-of-titan", "second-variety"]
    if args.all_novels:
        slugs += [
            n["slug"] for n in registry["novels"]
            if n.get("status") in {"ready", "needs_structure"}
        ]
    if args.all_stories:
        slugs += [
            u["title_key"] for u in manifest["story_units"]
            if u["word_count"] >= args.min_words
        ]
    if args.work:
        slugs.append(args.work)
    slugs = list(dict.fromkeys(slugs))
    if not slugs:
        ap.error("pass --work, --all-pilot, --all-stories or --all-novels")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    verbose = len(slugs) <= 6
    done = failed = 0
    for i, slug in enumerate(slugs, 1):
        try:
            ev = gather(slug, db, registry, vocab, manifest, background,
                        background_words, unigrams)
        except SystemExit as exc:
            print(f"  ! {slug}: {exc}")
            failed += 1
            continue
        out = OUT_DIR / f"{slug}.evidence.json"
        out.write_text(json.dumps(ev, indent=1, ensure_ascii=False), encoding="utf-8")
        done += 1
        if verbose:
            print(
                f"  {slug:<28} {ev['source']['word_count']:>7,}w"
                f"  chapters={ev['structure']['chapter_count']:>3}"
                f"  terms={ev['concepts']['distinct_terms']:>4}"
                f"  names={ev['concepts']['distinct_names']:>4}"
                f"  pkd={ev['pkd_on_this_work']['total_mentions']:>4}"
                f"  crit={ev['criticism']['total_mentions']:>4}"
            )
        elif i % 25 == 0 or i == len(slugs):
            print(f"  {i}/{len(slugs)} gathered")
    print(f"\nwrote {done} evidence files to {OUT_DIR.relative_to(PROJECT)}"
          + (f"; {failed} failed" if failed else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
