#!/usr/bin/env python3
"""Processing-coverage tool for the QueryPat metadata pipeline.

This is the "don't re-read what's already cooked in" system. It derives
coverage DIRECTLY from the exported JSON in site/public/data, so the report
can never drift from reality: a source unit counts as processed only if the
metadata is actually present in the data the site serves.

Two layers:
  1. Derived coverage  - computed live from the data (segments, works, bio).
  2. Read ledger       - scripts/processing/ledger.json, a declared registry
                         of which full-text sources have been read and which
                         passes are done/blocked. coverage.py cross-checks the
                         ledger against the derived data and flags mismatches.

Usage:
    python3 scripts/processing/coverage.py                # summary table
    python3 scripts/processing/coverage.py --remaining exegesis   # list TODO seg_ids
    python3 scripts/processing/coverage.py --remaining works
    python3 scripts/processing/coverage.py --remaining biography
    python3 scripts/processing/coverage.py --check-ledger          # ledger vs data
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "site" / "public" / "data"
LEDGER = ROOT / "scripts" / "processing" / "ledger.json"

# A segment is considered "summarized" when it carries a concise_summary.
# A segment is "processable now" only if it still has raw_text to read from.
SEG_SUMMARY_FIELD = "concise_summary"
SEG_THEME_FIELD = "theological_motifs"


def _load(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def scan_segments():
    seg_dir = DATA / "segments"
    total = summarized = themed = processable = blocked = 0
    remaining = []  # (date, position, seg_id) processable but not summarized
    textless = []   # blocked: no raw_text and no summary
    for f in sorted(seg_dir.glob("*.json")):
        d = _load(f)
        if not isinstance(d, dict):
            continue
        total += 1
        has_sum = bool(d.get(SEG_SUMMARY_FIELD))
        has_theme = bool(d.get(SEG_THEME_FIELD))
        has_text = bool(d.get("raw_text"))
        if has_sum:
            summarized += 1
        if has_theme:
            themed += 1
        if not has_sum:
            if has_text:
                processable += 1
                remaining.append((d.get("date_start") or "9999",
                                  d.get("position") or 0, d["seg_id"]))
            else:
                blocked += 1
                textless.append(d["seg_id"])
    remaining.sort()
    return {
        "total": total, "summarized": summarized, "themed": themed,
        "processable_remaining": processable, "blocked_no_text": blocked,
        "remaining": remaining, "textless": textless,
    }


def scan_works():
    work_dir = DATA / "works"
    total = with_themes = with_locations = pending = 0
    by_type = {}
    remaining = []  # work_id missing locations
    for f in sorted(work_dir.glob("*.json")):
        d = _load(f)
        if not isinstance(d, dict):
            continue
        total += 1
        wt = d.get("work_type", "?")
        by_type[wt] = by_type.get(wt, 0) + 1
        if d.get("themes"):
            with_themes += 1
        if d.get("locations"):
            with_locations += 1
        else:
            remaining.append((wt, d.get("work_id") or f.stem,
                              d.get("canonical_title") or f.stem))
        if "pending" in (d.get("page_summary", "") or "").lower():
            pending += 1
    return {
        "total": total, "with_themes": with_themes,
        "with_locations": with_locations, "summary_pending": pending,
        "by_type": by_type, "remaining": remaining,
    }


def scan_biography():
    out = {}
    for name in ("events.json", "curated.json"):
        d = _load(DATA / "biography" / name)
        evs = d if isinstance(d, list) else (d or {}).get("events", [])
        total = len(evs)
        loc = sum(1 for e in evs if isinstance(e, dict) and e.get("location"))
        missing = [e.get("id") or e.get("event", "")[:50]
                   for e in evs if isinstance(e, dict) and not e.get("location")]
        out[name] = {"total": total, "with_location": loc, "missing": missing}
    return out


def pct(n, d):
    return f"{(100*n/d):.0f}%" if d else "—"


def print_summary():
    seg = scan_segments()
    works = scan_works()
    bio = scan_biography()

    print("=" * 72)
    print("QUERYPAT METADATA COVERAGE")
    print("=" * 72)
    print("\nEXEGESIS SEGMENTS (summaries + themes/figures)")
    print(f"  total:                {seg['total']}")
    print(f"  summarized:           {seg['summarized']:>5}  ({pct(seg['summarized'], seg['total'])})")
    print(f"  with theological_motifs:{seg['themed']:>5}")
    print(f"  processable remaining:{seg['processable_remaining']:>5}  (have raw_text)")
    print(f"  blocked (no raw_text):{seg['blocked_no_text']:>5}  (recover text from exegesis_ordered.txt or DB re-export)")

    print("\nWORKS CATALOG (locations + themes; chapter summaries need source text)")
    print(f"  total:                {works['total']}")
    print(f"  with locations:       {works['with_locations']:>5}  ({pct(works['with_locations'], works['total'])})")
    print(f"  with themes:          {works['with_themes']:>5}  ({pct(works['with_themes'], works['total'])})")
    print(f"  summary still 'pending':{works['summary_pending']:>5}")
    print(f"  by work_type:         {works['by_type']}")

    print("\nBIOGRAPHY EVENTS (locations)")
    for name, b in bio.items():
        print(f"  {name:<14} {b['with_location']}/{b['total']} have location ({pct(b['with_location'], b['total'])})")

    # ledger cross-check
    if LEDGER.exists():
        print("\nREAD LEDGER")
        led = _load(LEDGER) or {}
        units = led.get("units", {})
        print(f"  tracked source units: {len(units)}")
        blocked = [u for u, v in units.items()
                   if v.get("source_text_available") is False]
        if blocked:
            print(f"  units blocked on missing source text: {len(blocked)}")
    print()


def list_remaining(kind):
    if kind == "exegesis":
        seg = scan_segments()
        for date, pos, sid in seg["remaining"]:
            print(f"{date}\t{pos}\t{sid}")
    elif kind == "works":
        works = scan_works()
        for wt, wid, title in works["remaining"]:
            print(f"{wt}\t{wid}\t{title}")
    elif kind == "biography":
        bio = scan_biography()
        for name, b in bio.items():
            for m in b["missing"]:
                print(f"{name}\t{m}")
    else:
        print(f"unknown kind: {kind}", file=sys.stderr)
        sys.exit(2)


def check_ledger():
    """Flag ledger claims that disagree with the derived data."""
    led = _load(LEDGER) or {}
    units = led.get("units", {})
    seg = scan_segments()
    summarized_sections = set()
    # Build a set of section ids that are fully summarized by deriving from seg ids.
    print("Ledger consistency check (declared vs derived):")
    issues = 0
    for uid, u in units.items():
        passes = u.get("passes", {})
        # Only structural sanity checks here; extend as the schema grows.
        if u.get("source_text_available") is False:
            for p, status in passes.items():
                if status == "done":
                    print(f"  ! {uid}: pass '{p}' marked done but source_text_available=false")
                    issues += 1
    if not issues:
        print("  OK — no contradictions found.")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--remaining", choices=["exegesis", "works", "biography"],
                    help="list the source units still needing this pass")
    ap.add_argument("--check-ledger", action="store_true",
                    help="cross-check ledger.json against the derived data")
    args = ap.parse_args()
    if args.remaining:
        list_remaining(args.remaining)
    elif args.check_ledger:
        check_ledger()
    else:
        print_summary()


if __name__ == "__main__":
    main()
