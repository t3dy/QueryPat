"""Write LETTERS_MINING_REPORT.md summarizing what was extracted.

Usage:
    python scripts/letters/report.py [--db PATH] [--out PATH]
"""
from __future__ import annotations

import argparse
import json
import sqlite3
from collections import defaultdict
from pathlib import Path


REPORT_TEMPLATE_HEADER = """# Letters Mining Report

Generated from `letter_events_candidate` and `biography_events` after running
`scripts/letters/segment.py` → `extract_llm.py` → `ingest.py`.

"""


def fmt_int(n) -> str:
    return f"{n:,}" if isinstance(n, int) else str(n)


def write_report(db_path: Path, out_path: Path) -> None:
    con = sqlite3.connect(db_path)

    sections: list[str] = [REPORT_TEMPLATE_HEADER]

    # 1. Volumes summary
    sections.append("## Volumes processed\n")
    cur = con.execute(
        """SELECT volume_doc_id, count(*), min(date_display), max(date_display),
                  sum(word_count)
           FROM letters
           GROUP BY volume_doc_id
           ORDER BY min(date_start)"""
    )
    rows = cur.fetchall()
    sections.append("| Volume | Letters | First | Last | Words |\n|---|---:|---|---|---:|\n")
    for vol, n, first, last, words in rows:
        sections.append(f"| `{vol[:48]}` | {fmt_int(n)} | {first or '?'} | {last or '?'} | {fmt_int(words or 0)} |\n")
    sections.append("\n")

    # 2. Candidate events summary
    cur = con.execute("SELECT count(*) FROM letter_events_candidate")
    total_cand = cur.fetchone()[0]
    cur = con.execute("SELECT count(*) FROM biography_events WHERE source_type='letter'")
    total_bio = cur.fetchone()[0]
    sections.append("## Extraction totals\n\n")
    sections.append(f"- **Candidate events** (LLM raw): {fmt_int(total_cand)}\n")
    sections.append(f"- **Biography events** (after dedup, inserted): {fmt_int(total_bio)}\n")
    if total_cand:
        sections.append(f"- **Dedup ratio**: {(1 - total_bio/total_cand)*100:.1f}% of candidates merged as corroborating\n\n")

    # 3. Events by theme
    sections.append("## Events by theme\n\n")
    theme_counts: dict[str, int] = defaultdict(int)
    cur = con.execute("SELECT themes FROM biography_events WHERE source_type='letter'")
    for (themes_json,) in cur.fetchall():
        try:
            for t in json.loads(themes_json or "[]"):
                theme_counts[t] += 1
        except json.JSONDecodeError:
            continue
    sections.append("| Theme | Events |\n|---|---:|\n")
    for theme, n in sorted(theme_counts.items(), key=lambda kv: -kv[1]):
        sections.append(f"| {theme} | {fmt_int(n)} |\n")
    sections.append("\n")

    # 4. Notable correspondence
    sections.append("## Notable correspondence captured\n\n")
    cur = con.execute(
        """SELECT notable_correspondence, count(*)
           FROM biography_events
           WHERE source_type='letter' AND notable_correspondence IS NOT NULL
           GROUP BY notable_correspondence
           ORDER BY count(*) DESC"""
    )
    rows = cur.fetchall()
    if rows:
        sections.append("| Tag | Events |\n|---|---:|\n")
        for tag, n in rows:
            sections.append(f"| `{tag}` | {fmt_int(n)} |\n")
        sections.append("\n")
    else:
        sections.append("*(none yet — set `notable_correspondence` field via LLM prompt)*\n\n")

    # 5. Top recipients
    sections.append("## Top correspondents (by letter count)\n\n")
    cur = con.execute(
        """SELECT recipient_raw, count(*) FROM letters
           WHERE recipient_raw IS NOT NULL AND recipient_raw != ''
           GROUP BY recipient_raw ORDER BY count(*) DESC LIMIT 25"""
    )
    sections.append("| Recipient | Letters |\n|---|---:|\n")
    for r, n in cur.fetchall():
        sections.append(f"| {r} | {fmt_int(n)} |\n")
    sections.append("\n")

    # 6. High-importance events sample
    sections.append("## Sample high-importance events (first 30 by date)\n\n")
    cur = con.execute(
        """SELECT date_start, summary, themes, notable_correspondence, evidence_quote
           FROM biography_events
           WHERE source_type='letter' AND importance='high'
           ORDER BY date_start
           LIMIT 30"""
    )
    for date, summary, themes, nc, quote in cur.fetchall():
        themes_str = ", ".join(json.loads(themes or "[]"))
        nc_str = f" [{nc}]" if nc else ""
        sections.append(f"- **{date}** ({themes_str}){nc_str}: {summary}\n")
        if quote:
            q = (quote or "").replace("\n", " ")
            sections.append(f"  > {q[:200]}\n")
    sections.append("\n")

    # 7. Run errors
    sections.append("## LLM-call errors\n\n")
    cur = con.execute(
        """SELECT count(*), count(error) FROM letter_events_candidate_runs"""
    )
    runs, errs = cur.fetchone()
    sections.append(f"- {fmt_int(runs)} letters processed; {fmt_int(errs)} errored\n\n")
    if errs:
        cur = con.execute(
            """SELECT letter_id, error FROM letter_events_candidate_runs
               WHERE error IS NOT NULL LIMIT 5"""
        )
        sections.append("First 5 errors:\n\n")
        for lid, err in cur.fetchall():
            sections.append(f"- `{lid}`: {(err or '')[:200]}\n")

    out_path.write_text("".join(sections), encoding="utf-8")
    print(f"[done] wrote {out_path}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="C:/QueryPat/database/unified.sqlite")
    ap.add_argument("--out", default="LETTERS_MINING_REPORT.md")
    args = ap.parse_args()
    write_report(Path(args.db), Path(args.out))
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
