"""Write MARKDOWN_INGEST_REPORT.md summarizing the conversion run.

Usage:
    python scripts/markdown/report.py [--db PATH] [--out PATH]
"""
from __future__ import annotations

import argparse
import sqlite3
from collections import defaultdict
from pathlib import Path


def fmt_int(n) -> str:
    return f"{n:,}" if isinstance(n, int) else str(n)


def write_report(db_path: Path, out_path: Path) -> None:
    con = sqlite3.connect(db_path)

    sections: list[str] = ["# Markdown Ingestion Report\n\n"]
    sections.append("Summary of `scripts/markdown/convert_all.py` against `documents` + `assets`.\n\n")

    # Status counts
    sections.append("## Status counts\n\n")
    cur = con.execute(
        """SELECT markdown_status, count(*)
           FROM document_texts
           WHERE doc_id LIKE 'DOC_ARCH_%'
           GROUP BY markdown_status
           ORDER BY count(*) DESC"""
    )
    sections.append("| Status | Documents |\n|---|---:|\n")
    total = 0
    for status, n in cur.fetchall():
        sections.append(f"| {status or '(null)'} | {fmt_int(n)} |\n")
        total += n
    sections.append(f"| **TOTAL** | **{fmt_int(total)}** |\n\n")

    # By extraction method
    sections.append("## Extraction methods used\n\n")
    cur = con.execute(
        """SELECT markdown_method, count(*)
           FROM document_texts
           WHERE doc_id LIKE 'DOC_ARCH_%' AND markdown_status='complete'
           GROUP BY markdown_method ORDER BY count(*) DESC"""
    )
    sections.append("| Method | Documents |\n|---|---:|\n")
    for method, n in cur.fetchall():
        sections.append(f"| {method or '(null)'} | {fmt_int(n)} |\n")
    sections.append("\n")

    # By category (joined with documents)
    sections.append("## Coverage by category\n\n")
    cur = con.execute(
        """SELECT d.category,
                  count(*) AS total,
                  sum(CASE WHEN dt.markdown_status='complete' THEN 1 ELSE 0 END) AS complete,
                  sum(CASE WHEN dt.markdown_status='skipped_ocr_required' THEN 1 ELSE 0 END) AS ocr,
                  sum(CASE WHEN dt.markdown_status='failed' THEN 1 ELSE 0 END) AS failed
           FROM documents d
           LEFT JOIN document_texts dt ON dt.doc_id = d.doc_id
           WHERE d.doc_id LIKE 'DOC_ARCH_%'
           GROUP BY d.category
           ORDER BY total DESC"""
    )
    sections.append("| Category | Total | Complete | OCR-needed | Failed |\n|---|---:|---:|---:|---:|\n")
    for cat, total, comp, ocr, failed in cur.fetchall():
        sections.append(f"| {cat or '(none)'} | {fmt_int(total)} | {fmt_int(comp or 0)} "
                        f"| {fmt_int(ocr or 0)} | {fmt_int(failed or 0)} |\n")
    sections.append("\n")

    # Total markdown char count
    cur = con.execute(
        """SELECT sum(markdown_char_count), count(*)
           FROM document_texts
           WHERE markdown_status='complete' AND markdown_char_count IS NOT NULL"""
    )
    chars, n = cur.fetchone()
    if chars:
        sections.append(f"## Total markdown characters\n\n")
        sections.append(f"- **{fmt_int(chars)}** characters across {fmt_int(n)} complete documents\n")
        sections.append(f"- Average: {fmt_int(int(chars / n))} chars/doc\n\n")

    # Failures
    cur = con.execute(
        """SELECT doc_id, markdown_error
           FROM document_texts
           WHERE markdown_status='failed' AND markdown_error IS NOT NULL
           LIMIT 15"""
    )
    rows = cur.fetchall()
    if rows:
        sections.append("## Failures (first 15)\n\n")
        for doc_id, err in rows:
            err_first = (err or "").splitlines()[0] if err else ""
            sections.append(f"- `{doc_id}`: {err_first[:200]}\n")
        sections.append("\n")

    # OCR-required list
    cur = con.execute(
        """SELECT doc_id FROM document_texts
           WHERE markdown_status='skipped_ocr_required'
           ORDER BY doc_id LIMIT 30"""
    )
    rows = cur.fetchall()
    if rows:
        sections.append("## Documents skipped (OCR required)\n\n")
        sections.append("These need a scanned-PDF OCR pass (out of scope for this ingest):\n\n")
        for (doc_id,) in rows:
            sections.append(f"- `{doc_id}`\n")
        sections.append("\n")

    # Source-missing list
    cur = con.execute(
        """SELECT doc_id FROM document_texts
           WHERE markdown_status='skipped_source_missing'
           ORDER BY doc_id LIMIT 15"""
    )
    rows = cur.fetchall()
    if rows:
        sections.append("## Documents skipped (source file missing)\n\n")
        sections.append("Asset paths in the DB pointed to files not present at the source root.\n\n")
        for (doc_id,) in rows:
            sections.append(f"- `{doc_id}`\n")
        sections.append("\n")

    out_path.write_text("".join(sections), encoding="utf-8")
    print(f"[done] wrote {out_path}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="C:/QueryPat/database/unified.sqlite")
    ap.add_argument("--out", default="MARKDOWN_INGEST_REPORT.md")
    args = ap.parse_args()
    write_report(Path(args.db), Path(args.out))
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
