"""Auto-link theophanies to Exegesis segments by scanning segment vocabulary fields.

For each theophany, walk all segments and score them against the theophany's
vocabulary (related_dictionary_terms + related_names + a per-theophany keyword
boost list). Segments scoring above threshold get linked via theophany_evidence.

Also writes the related_segments JSON array on each theophany row so the
detail-page sidebar shows them.

Usage:
    python scripts/theophanies/link_segments.py [--db PATH] [--threshold N]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path


# Per-theophany keyword boost vocabulary (extends related_dictionary_terms / related_names).
# Strings here are checked as case-insensitive substrings against segment fields.
THEOPHANY_KEYWORDS: dict[str, list[str]] = {
    "THEO_1963_PALMER_ELDRITCH_FACE": [
        "palmer eldritch", "stigmata", "sky-face", "face in the sky",
        "metallic face", "antichrist",
    ],
    "THEO_1971_11_BREAK_IN_FOREKNOWLEDGE": [
        "break-in", "break in", "santa venetia", "1971",
        "fbi", "kgb", "stanislaw lem", "lem",
    ],
    "THEO_1972_03_VANCOUVER_DESPAIR": [
        "vancouver", "x-kalay", "android and the human", "suicide",
        "rehab", "rehabilitation",
    ],
    "THEO_1974_02_FISH_SIGN": [
        "fish sign", "ichthys", "fish necklace", "delivery girl",
        "anamnesis", "thomas", "pharmacy", "sodium pentothal",
        "first century", "early christian", "feb 1974", "february 1974",
    ],
    "THEO_1974_02_PINK_BEAM": [
        "pink beam", "pink light", "music-color-math", "music color math",
        "triune", "illuminated manuscript", "transmission",
        "valis", "satellite",
    ],
    "THEO_1974_03_CHRISTOPHER_BIRTH": [
        "christopher", "hernia", "inguinal", "infant son",
        "medical info", "diagnosis",
    ],
    "THEO_1974_03_AI_VOICE": [
        "ai voice", "ai-voice", "voice", "sophia", "hagia sophia",
        "jane", "twin sister", "audition",
    ],
    "THEO_1974_03_KOINE_GREEK": [
        "koine", "koine greek", "acts of the apostles", "greek",
        "thomas", "first century", "phylogenic anamnesis",
    ],
    "THEO_1974_BLACK_IRON_PRISON": [
        "black iron prison", "bip", "empire", "rome", "70 ad",
        "70 a.d.", "first century", "nixon", "tyranny", "prison",
        "the empire never ended",
    ],
    "THEO_1974_SUMMER_ZEBRA": [
        "zebra", "mimicry", "camouflage", "camouflaged", "biological mimicry",
    ],
    "THEO_1975_NUMERIC_LETTER_GEMATRIA": [
        "gematria", "hebrew letters", "letter permutation",
        "numbers and letters", "numerology",
    ],
    "THEO_1976_ABULAFIA_POSSESSION": [
        "abulafia", "abraham abulafia", "tseruf", "kabbalah",
        "kabbalistic", "sefer yetzirah",
    ],
    "THEO_1977_METZ_2_3_75": [
        "metz", "metz speech", "metz france", "if you find this world bad",
        "phil from future", "phil-from-future",
    ],
    "THEO_1981_SISTER_DREAM": [
        "jane", "twin sister", "sister jane", "jane dick",
        "dead twin", "infant sister",
    ],
    "THEO_1974_2_3_74_CLUSTER": [
        "2-3-74", "2/3/74", "2.3.74", "feb-mar 74", "february-march 1974",
        "march 1974", "march of 1974", "march, 1974", "march of'74",
        "the experience", "the visions", "the savior", "religious experience",
        "encounter with the savior", "3-74", "3/74", "tachyon",
        "great mechanic", "theological experiences",
    ],
}


THEOPHANY_PARENT_THRESHOLD = 2  # min score for cluster parent
THEOPHANY_DEFAULT_THRESHOLD = 2


def score_segment(segment: dict, vocabulary: set[str]) -> tuple[int, list[str]]:
    """Return (score, matched_terms). Score = number of distinct matched vocab tokens."""
    fields = []
    for f in ("concise_summary", "key_claims", "recurring_concepts",
              "people_entities", "theological_motifs", "symbols_images",
              "texts_works", "autobiographical", "literary_self_ref"):
        v = segment.get(f) or ""
        if v:
            fields.append(v.lower())
    blob = " ".join(fields)

    matched = []
    for term in vocabulary:
        t = term.lower().strip()
        if not t or len(t) < 3:
            continue
        # word-boundary match for short tokens; substring for longer
        if len(t) >= 8:
            if t in blob:
                matched.append(term)
        else:
            if re.search(r"\b" + re.escape(t) + r"\b", blob):
                matched.append(term)
    return len(matched), matched


def vocabulary_for(theophany: dict) -> set[str]:
    """Build the vocabulary set: keywords + related dict terms + related names."""
    vocab: set[str] = set()
    keywords = THEOPHANY_KEYWORDS.get(theophany["theophany_id"], [])
    vocab.update(keywords)
    for f in ("related_dictionary_terms", "related_names"):
        try:
            for x in json.loads(theophany.get(f) or "[]"):
                vocab.add(str(x).replace("-", " "))
        except (json.JSONDecodeError, TypeError):
            continue
    return vocab


def run(db_path: Path, threshold: int) -> dict:
    con = sqlite3.connect(db_path)
    cur = con.execute(
        """SELECT theophany_id, name, related_dictionary_terms, related_names,
                  parent_theophany_id, related_theophany_ids
           FROM theophanies"""
    )
    theos = [dict(zip([d[0] for d in cur.description], r)) for r in cur.fetchall()]
    print(f"[load] {len(theos)} theophanies")

    cur = con.execute(
        """SELECT seg_id, doc_id, slug, date_start, date_display,
                  concise_summary, key_claims, recurring_concepts,
                  people_entities, theological_motifs, symbols_images,
                  texts_works, autobiographical, literary_self_ref
           FROM segments
           WHERE concise_summary IS NOT NULL AND length(concise_summary) > 30"""
    )
    segs = [dict(zip([d[0] for d in cur.description], r)) for r in cur.fetchall()]
    print(f"[load] {len(segs)} segments with parsed summary")

    # Score every segment against every theophany
    matches_by_theo: dict[str, list[tuple[dict, int, list[str]]]] = defaultdict(list)
    for t in theos:
        vocab = vocabulary_for(t)
        thresh = THEOPHANY_PARENT_THRESHOLD if t.get("parent_theophany_id") is None and "CLUSTER" in t["theophany_id"] else threshold
        for s in segs:
            score, matched = score_segment(s, vocab)
            if score >= thresh:
                matches_by_theo[t["theophany_id"]].append((s, score, matched))

    # Insert evidence rows + update related_segments JSON
    now = dt.datetime.now(dt.UTC).isoformat(timespec="seconds")
    n_evidence = 0
    n_links = 0
    # Wipe existing auto-generated evidence rows so re-runs are idempotent
    con.execute("DELETE FROM theophany_evidence WHERE source_type = 'exegesis_segment_auto'")

    for tid, hits in matches_by_theo.items():
        # Sort by score desc, then date asc
        hits.sort(key=lambda h: (-h[1], h[0].get("date_start") or ""))
        # Take top 30 per theophany
        top = hits[:30]

        seg_ids = []
        for s, score, matched in top:
            ev_id = f"EV_THEO_{tid[5:][:30]}_{s['seg_id'][:30]}"
            con.execute(
                """INSERT OR REPLACE INTO theophany_evidence
                (evidence_id, theophany_id, source_type, source_doc_id, source_seg_id,
                 source_letter_id, page_or_locator, excerpt, excerpt_lane, notes, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    ev_id, tid, "exegesis_segment_auto", s.get("doc_id"), s["seg_id"],
                    None, s.get("date_display") or "",
                    (s.get("concise_summary") or "")[:400],
                    "B",
                    f"score={score}; matched={', '.join(matched[:5])}",
                    now,
                ),
            )
            n_evidence += 1
            seg_ids.append(s["seg_id"])

        # Update related_segments JSON on the theophany row
        con.execute(
            "UPDATE theophanies SET related_segments = ?, updated_at = ? WHERE theophany_id = ?",
            (json.dumps(seg_ids[:25]), now, tid),
        )
        n_links += len(seg_ids[:25])
        print(f"  {tid:48s}: {len(top)} segments matched (top score {top[0][1] if top else 0})")

    con.commit()
    con.close()

    print(f"\n[done] {n_evidence} evidence rows; {n_links} segment links across {len(matches_by_theo)} theophanies")
    return {"evidence": n_evidence, "links": n_links, "theophanies": len(matches_by_theo)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="C:/QueryPat/database/unified.sqlite")
    ap.add_argument("--threshold", type=int, default=THEOPHANY_DEFAULT_THRESHOLD)
    args = ap.parse_args()
    run(Path(args.db), args.threshold)
    return 0


if __name__ == "__main__":
    sys.exit(main())
