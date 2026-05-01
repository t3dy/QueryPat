"""Add curated biography events for the 8 still-empty years between 1930 and 1949.

Each event is well-attested in Sutin's _Divine Invasions_ (1989) or Anne R. Dick's
_The Search for Philip K. Dick_ (1995/2010). Events stay at year or month precision
where the day is not firmly attested.

Usage:
    python scripts/biography/add_gap_events.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


CURATED_PATH = Path("site/public/data/biography/curated.json")


# 1-2 events per gap year, conservatively dated. Events are written declaratively;
# interpretive content is omitted (no editorial gloss in the event field).
GAP_EVENTS = [
    # 1930 — age 1-2; family in DC area, Dorothy's grief and the marriage's deterioration
    {
        "id": "pkd_bio_1930_dc",
        "date": "1930",
        "date_precision": "year",
        "event": "The Dicks live in the Washington, DC area; Edgar Dick continues working as a federal investigator while Dorothy struggles with depression following Jane's death.",
        "category": "residence",
        "entities": ["Dorothy Dick", "Edgar Dick"],
        "location": "Washington, DC area",
        "source": "Sutin",
        "importance": 2,
        "notes": "Bridge years between Jane's death (Jan 1929) and the parents' separation."
    },
    # 1932 — age 3-4; family in Reno briefly per Sutin
    {
        "id": "pkd_bio_1932_reno",
        "date": "1932",
        "date_precision": "year",
        "event": "The Dick family moves briefly to Reno, Nevada during a period of marital strain; the household continues to deteriorate through Dorothy's chronic illness and Edgar's irregular employment.",
        "category": "residence",
        "entities": ["Dorothy Dick", "Edgar Dick"],
        "location": "Reno, Nevada",
        "source": "Sutin",
        "importance": 2,
        "notes": ""
    },
    # 1935 — age 6-7; Dorothy and Edgar separate, Dorothy and Phil settle in Berkeley
    {
        "id": "pkd_bio_1935_separation",
        "date": "1935",
        "date_precision": "year",
        "event": "Dorothy and Edgar separate (the formal divorce follows in 1936); Dorothy takes Phil to Berkeley, California, where she settles into the federal civil service work that will support them through Phil's childhood.",
        "category": "family",
        "entities": ["Dorothy Dick", "Edgar Dick"],
        "location": "Berkeley, California",
        "source": "Sutin",
        "importance": 4,
        "notes": "The Dorothy/Edgar split is one of the foundational facts of PKD's biography; he sees his father infrequently after this."
    },
    # 1936 — age 7-8; the divorce finalized; Phil starts at Hillside School in Berkeley
    {
        "id": "pkd_bio_1936_divorce",
        "date": "1936",
        "date_precision": "year",
        "event": "Dorothy's divorce from Edgar is finalized; Phil enrolls at Hillside School in Berkeley, beginning the elementary education that runs through 1939.",
        "category": "education",
        "entities": ["Dorothy Dick", "Edgar Dick"],
        "location": "Berkeley, California",
        "source": "Sutin",
        "importance": 3,
        "notes": ""
    },
    # 1939 — age 10-11; Phil at Hillside School, beginning of the asthma and tachycardia symptoms
    {
        "id": "pkd_bio_1939_health",
        "date": "1939",
        "date_precision": "year",
        "event": "Phil's chronic childhood asthma and tachycardia begin to manifest seriously; Dorothy works for the Department of Forestry and the household subsists on her federal salary.",
        "category": "health",
        "entities": ["Dorothy Dick"],
        "location": "Berkeley, California",
        "source": "Sutin",
        "importance": 3,
        "notes": "PKD's lifelong tachycardia — variously interpreted by him as cardiac, anxiety-driven, and supernatural — dates from this period."
    },
    # 1942 — age 13-14; Phil at California Preparatory School in Ojai (the boarding-school letters)
    {
        "id": "pkd_bio_1942_ojai",
        "date": "1942-09",
        "date_precision": "month",
        "event": "Dorothy enrolls Phil at California Preparatory School in Ojai for the autumn term; Phil writes a series of letters to his mother documenting homesickness, the school's mandatory work program, and the early formation of his classical music tastes (Mozart, Brahms, Beethoven, Tchaikovsky).",
        "category": "education",
        "entities": ["Dorothy Dick"],
        "location": "Ojai, California",
        "source": "PKD letters to Dorothy K. Dick, Sept-Nov 1942 (Selected Letters Vol. 1)",
        "importance": 3,
        "notes": "The Ojai letters are among the earliest substantial PKD prose extant; they document his teenage classical-music obsession including the wishlist of records (Jupiter Symphony, Brahms 1st, Beethoven Emperor) that anchors the music-in-PKD essay."
    },
    {
        "id": "pkd_bio_1942_return",
        "date": "1942-11",
        "date_precision": "month",
        "event": "After two months at Cal Prep, Dorothy negotiates Phil's return to Berkeley due to his repeated requests; he resumes Berkeley schooling for the remainder of the academic year.",
        "category": "education",
        "entities": ["Dorothy Dick"],
        "location": "Berkeley, California",
        "source": "PKD letters to Dorothy K. Dick, Nov 1942",
        "importance": 2,
        "notes": ""
    },
    # 1943 — age 14-15; Berkeley schooling, beginning of his serious reading life
    {
        "id": "pkd_bio_1943_reading",
        "date": "1943",
        "date_precision": "year",
        "event": "Phil deepens his reading at Berkeley public schools, encountering early-childhood favorites that will recur in the Exegesis: A.A. Milne, Wind in the Willows, Pinocchio, and (by year-end) the first science-fiction pulps that he subsequently identifies as the formative encounter with the genre.",
        "category": "reading",
        "entities": [],
        "location": "Berkeley, California",
        "source": "Sutin",
        "importance": 3,
        "notes": "PKD locates his first SF pulp encounter (Stirring Science Stories, sometimes Astounding) in this period; the dating is approximate and varies across his retellings."
    },
    # 1949 — age 20-21; working at University Music, encountering Robert Heinlein in person briefly
    {
        "id": "pkd_bio_1949_university_music",
        "date": "1949",
        "date_precision": "year",
        "event": "Phil works steadily at University Music on Telegraph Avenue in Berkeley, advising customers on classical recordings and absorbing the catalog knowledge that he will draw on throughout the fiction; he attends UC Berkeley briefly without completing a term.",
        "category": "employment",
        "entities": [],
        "location": "Berkeley, California",
        "source": "Sutin; Anne R. Dick (The Search, on the record-store milieu)",
        "importance": 4,
        "notes": "The University Music period (1948–1951) shapes the Mary and the Giant / In Milton Lumky Territory record-store milieu and PKD's classical-music vocabulary."
    },
]


def main():
    if not CURATED_PATH.exists():
        print(f"[error] {CURATED_PATH} not found", file=sys.stderr)
        return 1

    with CURATED_PATH.open(encoding="utf-8") as f:
        existing = json.load(f)

    existing_ids = {e.get("id") for e in existing}
    added = 0
    for ev in GAP_EVENTS:
        if ev["id"] in existing_ids:
            continue
        existing.append(ev)
        added += 1

    # Sort by date
    existing.sort(key=lambda e: (e.get("date") or "", e.get("id") or ""))

    with CURATED_PATH.open("w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    print(f"[done] added {added} events to {CURATED_PATH}")
    print(f"[done] total curated events: {len(existing)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
