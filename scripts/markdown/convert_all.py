"""Convert every archive document to markdown; store on disk and in the database.

Usage:
    python scripts/markdown/convert_all.py [--db PATH] [--source-root PATH] [--workers N] [--limit N] [--only DOC_ID]

Default DB:          database/unified.sqlite
Default source root: C:/QueryPat/  (assets.file_path is relative to this)
Default workers:     1
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import os
import sqlite3
import sys
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

# Make the converters package importable when run as `python scripts/markdown/convert_all.py`
THIS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(THIS_DIR.parent.parent))

from scripts.markdown.converters import pdf as conv_pdf  # noqa: E402
from scripts.markdown.converters import epub as conv_epub  # noqa: E402
from scripts.markdown.converters import docx as conv_docx  # noqa: E402
from scripts.markdown.converters import xlsx as conv_xlsx  # noqa: E402
from scripts.markdown.converters import text as conv_text  # noqa: E402
from scripts.markdown.converters import html as conv_html  # noqa: E402


# ---------------------------------------------------------------------------
# Routing


EXT_TO_CONVERTER = {
    ".pdf": conv_pdf.convert,
    ".epub": conv_epub.convert,
    ".docx": conv_docx.convert,
    ".doc": None,  # legacy .doc — no converter
    ".xlsx": conv_xlsx.convert,
    ".xls": None,
    ".txt": conv_text.convert,
    ".md": conv_text.convert,
    ".html": conv_html.convert,
    ".htm": conv_html.convert,
}


def file_hash(path: Path, block: int = 65536) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            buf = f.read(block)
            if not buf:
                break
            h.update(buf)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Worker


@dataclass
class Job:
    doc_id: str
    asset_path: Path  # absolute
    title: str
    author: str | None
    category: str | None


@dataclass
class Result:
    doc_id: str
    status: str  # complete | failed | skipped_ocr_required | skipped_no_converter | skipped_source_missing
    method: str | None
    char_count: int | None
    source_hash: str | None
    error: str | None
    md_path: str | None


def convert_one(job: Job, out_dir: Path) -> Result:
    if not job.asset_path.exists():
        return Result(job.doc_id, "skipped_source_missing", None, None, None,
                      f"asset not found: {job.asset_path}", None)

    ext = job.asset_path.suffix.lower()
    fn = EXT_TO_CONVERTER.get(ext)
    if fn is None:
        return Result(job.doc_id, "skipped_no_converter", None, None, None,
                      f"no converter registered for extension {ext!r}", None)

    try:
        src_hash = file_hash(job.asset_path)
        md_text, method = fn(job.asset_path)
    except conv_pdf.OCRRequired as e:
        return Result(job.doc_id, "skipped_ocr_required", None, None, None, str(e), None)
    except Exception as e:
        return Result(job.doc_id, "failed", None, None, None,
                      f"{type(e).__name__}: {e}\n{traceback.format_exc()}", None)

    # Front matter
    front = [f"# {job.title}"]
    if job.author:
        front.append(f"*by {job.author}*")
    meta_line = []
    if job.category:
        meta_line.append(f"category: {job.category}")
    meta_line.append(f"doc_id: `{job.doc_id}`")
    meta_line.append(f"source: `{job.asset_path.name}`")
    front.append(" — ".join(meta_line))
    full_md = "\n\n".join(front) + "\n\n---\n\n" + md_text

    md_path = out_dir / f"{job.doc_id}.md"
    md_path.write_text(full_md, encoding="utf-8")

    return Result(
        doc_id=job.doc_id,
        status="complete",
        method=method,
        char_count=len(full_md),
        source_hash=src_hash,
        error=None,
        md_path=str(md_path.relative_to(out_dir.parent.parent) if md_path.is_relative_to(out_dir.parent.parent) else md_path),
    )


# ---------------------------------------------------------------------------
# DB I/O


def load_jobs(con: sqlite3.Connection, source_root: Path,
              only: str | None, limit: int | None) -> list[Job]:
    sql = """
        SELECT d.doc_id, a.file_path, d.title, d.author, d.category
        FROM documents d
        JOIN assets a ON a.doc_id = d.doc_id
        WHERE d.doc_id LIKE 'DOC_ARCH_%'
    """
    params: list = []
    if only:
        sql += " AND d.doc_id = ?"
        params.append(only)
    sql += " ORDER BY d.doc_id"
    if limit:
        sql += f" LIMIT {int(limit)}"
    cur = con.execute(sql, params)
    jobs: list[Job] = []
    seen: set[str] = set()
    for doc_id, file_path, title, author, category in cur.fetchall():
        if doc_id in seen:  # one job per doc; first asset wins
            continue
        seen.add(doc_id)
        # file_path is repo-relative (e.g., "PaulPKDarchive/PKDpdf/foo.pdf"); join under source_root
        abs_path = (source_root / file_path).resolve()
        jobs.append(Job(doc_id=doc_id, asset_path=abs_path, title=title or doc_id,
                        author=author, category=category))
    return jobs


def already_converted(con: sqlite3.Connection, doc_id: str, expected_hash: str) -> bool:
    cur = con.execute(
        "SELECT markdown_status, markdown_source_hash FROM document_texts WHERE doc_id = ?",
        (doc_id,),
    )
    row = cur.fetchone()
    if not row:
        return False
    status, src_hash = row
    return status == "complete" and src_hash == expected_hash


def upsert_result(con: sqlite3.Connection, result: Result, md_text: str | None) -> None:
    """Update or insert a row in document_texts with markdown columns."""
    now = dt.datetime.utcnow().isoformat(timespec="seconds")
    cur = con.execute("SELECT text_id FROM document_texts WHERE doc_id = ?", (result.doc_id,))
    row = cur.fetchone()
    if row:
        con.execute(
            """
            UPDATE document_texts
            SET markdown_content = ?,
                markdown_method = ?,
                markdown_status = ?,
                markdown_char_count = ?,
                markdown_error = ?,
                markdown_updated_at = ?,
                markdown_source_hash = ?
            WHERE doc_id = ?
            """,
            (md_text, result.method, result.status, result.char_count,
             result.error, now, result.source_hash, result.doc_id),
        )
    else:
        # No document_texts row yet — insert a thin one.
        text_id = f"TXT_{result.doc_id[len('DOC_'):]}"
        con.execute(
            """
            INSERT INTO document_texts
                (text_id, doc_id, extraction_method, extraction_status,
                 text_content, char_count, created_at,
                 markdown_content, markdown_method, markdown_status,
                 markdown_char_count, markdown_error, markdown_updated_at,
                 markdown_source_hash)
            VALUES (?, ?, 'manual', ?, NULL, NULL, ?,
                    ?, ?, ?, ?, ?, ?, ?)
            """,
            (text_id, result.doc_id, result.status, now,
             md_text, result.method, result.status,
             result.char_count, result.error, now, result.source_hash),
        )


# ---------------------------------------------------------------------------
# Orchestration


def run(db_path: Path, source_root: Path, workers: int,
        limit: int | None, only: str | None) -> dict:
    con = sqlite3.connect(db_path)
    out_dir = db_path.parent / "extracted_markdown"
    out_dir.mkdir(parents=True, exist_ok=True)

    jobs = load_jobs(con, source_root, only=only, limit=limit)
    print(f"[plan] {len(jobs)} archive documents to consider; output -> {out_dir}")

    # Skip already-converted via cache check
    pending: list[Job] = []
    skipped_cached = 0
    for job in jobs:
        if not job.asset_path.exists():
            pending.append(job)
            continue
        try:
            h = file_hash(job.asset_path)
        except Exception:
            pending.append(job)
            continue
        if already_converted(con, job.doc_id, h):
            skipped_cached += 1
            continue
        pending.append(job)
    print(f"[plan] {skipped_cached} cached (skipped); {len(pending)} to convert")

    counters = {
        "complete": 0,
        "failed": 0,
        "skipped_ocr_required": 0,
        "skipped_no_converter": 0,
        "skipped_source_missing": 0,
        "cached": skipped_cached,
    }
    failures: list[Result] = []

    def handle(result: Result) -> None:
        # Re-read the md file (worker wrote it) so we can store in DB.
        md_text = None
        if result.status == "complete":
            md_path = out_dir / f"{result.doc_id}.md"
            try:
                md_text = md_path.read_text(encoding="utf-8")
            except Exception:
                pass
        upsert_result(con, result, md_text)
        counters[result.status] = counters.get(result.status, 0) + 1
        if result.status in ("failed",):
            failures.append(result)

    if workers <= 1:
        for i, job in enumerate(pending, 1):
            r = convert_one(job, out_dir)
            handle(r)
            if i % 10 == 0 or i == len(pending):
                print(f"  [{i}/{len(pending)}] {r.doc_id} -> {r.status}"
                      f"{' (' + (r.method or '') + ')' if r.method else ''}")
            con.commit()
    else:
        with ProcessPoolExecutor(max_workers=workers) as ex:
            futures = {ex.submit(convert_one, job, out_dir): job for job in pending}
            for i, fut in enumerate(as_completed(futures), 1):
                r = fut.result()
                handle(r)
                if i % 10 == 0 or i == len(pending):
                    print(f"  [{i}/{len(pending)}] {r.doc_id} -> {r.status}"
                          f"{' (' + (r.method or '') + ')' if r.method else ''}")
                con.commit()

    con.commit()
    con.close()

    return {"counters": counters, "failures": failures, "out_dir": str(out_dir)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="database/unified.sqlite")
    ap.add_argument("--source-root", default="C:/QueryPat",
                    help="Directory under which assets.file_path is resolved")
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--limit", type=int, default=None,
                    help="Only process the first N documents (testing)")
    ap.add_argument("--only", default=None, help="Process only this doc_id")
    args = ap.parse_args()

    summary = run(Path(args.db), Path(args.source_root), args.workers, args.limit, args.only)
    print()
    print("=" * 60)
    print("Summary:")
    for k, v in summary["counters"].items():
        print(f"  {k:32s} {v}")
    if summary["failures"]:
        print(f"\n{len(summary['failures'])} failures:")
        for r in summary["failures"][:10]:
            err_first = (r.error or "").splitlines()[0] if r.error else ""
            print(f"  - {r.doc_id}: {err_first}")
        if len(summary["failures"]) > 10:
            print(f"  ... + {len(summary['failures']) - 10} more")
    print(f"\nMarkdown output: {summary['out_dir']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
