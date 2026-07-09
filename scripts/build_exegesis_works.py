#!/usr/bin/env python3
"""
build_exegesis_works.py

Mine exegesis_entries_analysis.json (860 analyzed Exegesis entries) for every
mention of each PKD novel/short story, group by work, and emit the data spine
for the "Works in the Exegesis" pages:

    site/public/data/exegesis/works/index.json
    site/public/data/exegesis/works/<slug>.json

The script fills the EXTRACTED fields (entry_id, folder_page, date_range,
summary, quotes, claims). The WRITTEN fields (intro, theological_synthesis,
each mention's gloss) are left as empty strings for a careful human pass — see
Documentation/BIOGRAPHY_AND_EXEGESIS_WORKS_METHOD.md §B.3.

Idempotent: re-running regenerates the spine but PRESERVES any human-written
intro/theological_synthesis/gloss already present in an existing <slug>.json.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANALYSIS = os.path.join(ROOT, "exegesis_entries_analysis.json")
OUT_DIR = os.path.join(ROOT, "site", "public", "data", "exegesis", "works")

# Curated, work-specific patterns. Anchored to avoid false positives
# (e.g. bare \btears\b or \bscanner\b over-match). Spot-checked against output.
WORKS = [
    ("ubik", "Ubik", r"\bubik\b"),
    ("valis", "VALIS", r"\bvalis\b"),
    ("a-scanner-darkly", "A Scanner Darkly", r"scanner darkly|substance d\b|bob arctor|\barctor\b"),
    ("the-three-stigmata-of-palmer-eldritch", "The Three Stigmata of Palmer Eldritch",
     r"palmer eldritch|three stigmata|\bchew-?z\b|\bcan-d\b|perky pat"),
    ("flow-my-tears-the-policeman-said", "Flow My Tears, the Policeman Said",
     r"flow my tears|policeman said|jason taverner|felix buckman|\bbuckman\b"),
    ("time-out-of-joint", "Time Out of Joint", r"time out of joint|ragle gumm|\bgumm\b"),
    ("a-maze-of-death", "A Maze of Death", r"maze of death"),
    ("radio-free-albemuth", "Radio Free Albemuth", r"albemuth|radio free"),
    ("martian-time-slip", "Martian Time-Slip", r"martian time.?slip"),
    ("galactic-pot-healer", "Galactic Pot-Healer", r"pot.?healer|glimmung"),
    ("the-divine-invasion", "The Divine Invasion", r"divine invasion"),
    ("deus-irae", "Deus Irae", r"deus irae"),
    ("the-cosmic-puppets", "The Cosmic Puppets", r"cosmic puppets"),
    ("do-androids-dream-of-electric-sheep", "Do Androids Dream of Electric Sheep?",
     r"do androids dream|electric sheep|\bdeckard\b"),
]

# Which works have a canonical /works/:slug record (checked against works/index.json).
WORK_LINK = {}


def clean_dates(s):
    if not s:
        return s
    s = s.replace("**", "").strip()
    # collapse any non-ASCII run (mojibake dashes, U+FFFD) to an en-dash
    s = re.sub(r"[^\x00-\x7F]+", "–", s)
    s = re.sub(r"\s*[-–—]\s*", "–", s)
    return s.strip("– ").strip()


def year_span(mentions):
    """Robust date label: min–max 4-digit year across all mentions."""
    years = []
    for m in mentions:
        years += [int(y) for y in re.findall(r"\b(19[0-9]{2})\b", m.get("date_range", "") or "")]
    if not years:
        return "1974–1982"
    lo, hi = min(years), max(years)
    return f"{lo}–{hi}" if lo != hi else str(lo)


def folder_sort_key(fp):
    m = re.findall(r"\d+", fp or "")
    return tuple(int(x) for x in m) if m else (9999,)


def work_context(summary, pattern):
    """Return the sentence(s) of the summary that mention the work — a clean,
    display-ready quote, unlike the broken key_quotes offsets."""
    sentences = re.split(r"(?<=[.!?])\s+", summary)
    hits = [s.strip() for s in sentences if re.search(pattern, s, re.I)]
    return hits[:3]


def load_work_links():
    idx_path = os.path.join(ROOT, "site", "public", "data", "works", "index.json")
    try:
        idx = json.load(open(idx_path, encoding="utf-8"))
        slugs = {w.get("slug") for w in idx if isinstance(w, dict)}
        for slug, _title, _pat in WORKS:
            WORK_LINK[slug] = f"/works/{slug}" if slug in slugs else None
    except Exception:
        for slug, _t, _p in WORKS:
            WORK_LINK[slug] = None


def load_existing_written(path):
    """Preserve human-written fields across regeneration."""
    written = {"intro": "", "theological_synthesis": "", "theological_headline": "",
               "see_also": None, "glosses": {}}
    if os.path.exists(path):
        try:
            old = json.load(open(path, encoding="utf-8"))
            written["intro"] = old.get("intro", "") or ""
            written["theological_synthesis"] = old.get("theological_synthesis", "") or ""
            written["theological_headline"] = old.get("theological_headline", "") or ""
            if old.get("see_also"):
                written["see_also"] = old["see_also"]
            for m in old.get("mentions", []):
                if m.get("gloss"):
                    written["glosses"][m["entry_id"]] = m["gloss"]
        except Exception:
            pass
    return written


def main():
    if not os.path.exists(ANALYSIS):
        sys.exit(f"Missing {ANALYSIS}")
    data = json.load(open(ANALYSIS, encoding="utf-8"))
    os.makedirs(OUT_DIR, exist_ok=True)
    load_work_links()

    index_works = []
    report = []

    for slug, title, pat in WORKS:
        rx = re.compile(pat, re.I)
        by_id = {}  # dedup by entry_id, keep the richest (longest summary) instance
        for e in data:
            summary = e.get("summary", "") or ""
            claims = e.get("philosophical_claims", []) or []
            claim_blob = " ".join(claims) if isinstance(claims, list) else str(claims)
            if rx.search(summary) or rx.search(claim_blob):
                eid = e.get("entry_id")
                prev = by_id.get(eid)
                if prev and len(prev.get("summary", "")) >= len(summary):
                    continue
                by_id[eid] = {
                    "entry_id": eid,
                    "folder_page": e.get("folder_page"),
                    "date_range": clean_dates(e.get("date_range")),
                    "summary": summary.strip(),
                    "quotes": work_context(summary, pat),
                    "claims": [c for c in claims if isinstance(c, str)][:6],
                    "gloss": "",  # WRITTEN by human pass
                }
        mentions = sorted(by_id.values(),
                          key=lambda m: (folder_sort_key(m["folder_page"]), m["entry_id"] or ""))

        if not mentions:
            report.append(f"  (skip) {title}: 0 mentions")
            continue

        path = os.path.join(OUT_DIR, f"{slug}.json")
        written = load_existing_written(path)
        for m in mentions:
            if m["entry_id"] in written["glosses"]:
                m["gloss"] = written["glosses"][m["entry_id"]]

        date_span = year_span(mentions)

        doc = {
            "slug": slug,
            "title": title,
            "work_link": WORK_LINK.get(slug),
            "mention_count": len(mentions),
            "date_range": date_span,
            "match_pattern": pat,
            "theological_headline": written["theological_headline"],
            "intro": written["intro"],
            "theological_synthesis": written["theological_synthesis"],
            "mentions": mentions,
            "see_also": written["see_also"] or {"essays": [], "themes": [], "dictionary": []},
        }
        json.dump(doc, open(path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

        index_works.append({
            "slug": slug,
            "title": title,
            "mention_count": len(mentions),
            "date_range": date_span,
            "work_link": WORK_LINK.get(slug),
            "theological_headline": written["theological_headline"],
            "has_writeup": bool(written["intro"]),
        })
        report.append(f"  {title}: {len(mentions)} mentions -> {slug}.json"
                      + ("  [has write-up]" if written["intro"] else ""))

    index_works.sort(key=lambda w: -w["mention_count"])
    index = {
        "generated_from": "exegesis_entries_analysis.json",
        "total_analyzed_entries": len(data),
        "works": index_works,
    }
    json.dump(index, open(os.path.join(OUT_DIR, "index.json"), "w", encoding="utf-8"),
              indent=2, ensure_ascii=False)

    print(f"Analyzed {len(data)} Exegesis entries.")
    print("\n".join(report))
    print(f"\nWrote {len(index_works)} work files + index.json to {OUT_DIR}")


if __name__ == "__main__":
    main()
