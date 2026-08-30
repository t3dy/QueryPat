#!/usr/bin/env python3
"""Check scripts/reading/work_sources.json against the corpus on disk.

The registry is hand-maintained editorial data, so it can drift from the files
it points at. This verifies every claim in it that a machine can verify: the
file exists, the word count still matches, the chapter pattern still finds
chapters, and any work marked `no_primary_text` really has none.

Exit code 0 = registry consistent, 1 = at least one problem.

    python scripts/reading/validate_sources.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[2]
REGISTRY = Path(__file__).resolve().parent / "work_sources.json"

# Word counts shift slightly if the corpus is re-extracted; allow a little drift
# before calling it an error.
TOLERANCE = 0.02


def check_file(entry: dict, problems: list[str], notes: list[str], label: str) -> None:
    rel = entry.get("source_file")
    if rel is None:
        if entry.get("status") != "no_primary_text":
            problems.append(f"{label}: no source_file but status is {entry.get('status')!r}")
        return

    path = PROJECT / rel
    if not path.exists():
        problems.append(f"{label}: source_file missing from disk — {rel}")
        return

    text = path.read_text(encoding="utf-8", errors="replace")
    actual = len(text.split())
    claimed = entry.get("word_count")
    if claimed:
        drift = abs(actual - claimed) / claimed
        if drift > TOLERANCE:
            problems.append(
                f"{label}: word_count says {claimed:,} but the file has {actual:,} "
                f"({drift:.0%} drift)"
            )

    pattern = entry.get("chapter_pattern")
    if pattern:
        hits = len(re.findall(pattern, text, re.M))
        if hits == 0:
            problems.append(f"{label}: chapter_pattern matches nothing — {pattern}")
        elif hits < 5:
            notes.append(f"{label}: chapter_pattern matches only {hits} places")
        else:
            notes.append(f"{label}: {hits} chapters")

    start = entry.get("line_start")
    if start is not None:
        total = text.count("\n")
        if start >= total:
            problems.append(f"{label}: line_start {start} is past the end of the file ({total})")


def main() -> int:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    problems: list[str] = []
    notes: list[str] = []

    counts: dict[str, int] = {}
    for section in ("novels", "story_collections", "pkd_own_voice", "criticism"):
        entries = registry.get(section, [])
        counts[section] = len(entries)
        for entry in entries:
            label = f"{section}/{entry.get('slug') or Path(entry.get('source_file') or '?').stem[:40]}"
            check_file(entry, problems, notes, label)

    # A work marked as having no primary text should not also name a source.
    for entry in registry.get("novels", []):
        if entry.get("status") == "no_primary_text" and entry.get("source_file"):
            problems.append(f"{entry['slug']}: marked no_primary_text but names a source_file")

    valid_status = set(registry["_status_values"])
    for entry in registry.get("novels", []):
        if entry.get("status") not in valid_status:
            problems.append(f"{entry.get('slug')}: unknown status {entry.get('status')!r}")

    for section, n in counts.items():
        print(f"{n:>3}  {section}")
    print()
    for n in notes:
        print(f"  note: {n}")

    by_status: dict[str, int] = {}
    for entry in registry.get("novels", []):
        by_status[entry["status"]] = by_status.get(entry["status"], 0) + 1
    print("\nnovel readiness:")
    for status, n in sorted(by_status.items(), key=lambda kv: -kv[1]):
        print(f"  {n:>3}  {status}")

    if problems:
        print(f"\n{len(problems)} problem(s):")
        for p in problems:
            print(f"  ! {p}")
        return 1
    print("\nRegistry is consistent with the corpus on disk.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
