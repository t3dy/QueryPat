"""Inject markdown_excerpt into each site/public/data/archive/docs/{slug}.json.

For each archive document with `markdown_status='complete'`, add the first ~3000
characters of `markdown_content` (skipping the front-matter block) to the
per-doc JSON so the Archive detail page can render it.

Usage:
    python scripts/markdown/inject_archive_excerpts.py [--db PATH] [--data-dir PATH]
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path


EXCERPT_CHARS = 3000


def strip_frontmatter(md: str) -> str:
    """Remove the leading title + meta block we wrote during conversion (ends at first '---' line)."""
    parts = md.split("\n---\n", 1)
    if len(parts) == 2:
        return parts[1].lstrip()
    return md


def run(db_path: Path, data_dir: Path) -> dict:
    con = sqlite3.connect(db_path)
    docs_dir = data_dir / "archive" / "docs"
    if not docs_dir.exists():
        print(f"[error] {docs_dir} not found", file=sys.stderr)
        return {"error": "no_docs_dir"}

    cur = con.execute(
        """SELECT d.doc_id, d.slug, dt.markdown_content, dt.markdown_status,
                  dt.markdown_method, dt.markdown_char_count
           FROM documents d
           JOIN document_texts dt ON dt.doc_id = d.doc_id
           WHERE d.doc_id LIKE 'DOC_ARCH_%'
             AND dt.markdown_status = 'complete'
             AND dt.markdown_content IS NOT NULL"""
    )
    rows = cur.fetchall()
    print(f"[load] {len(rows)} archive docs with complete markdown")

    n_updated = 0
    n_missing_json = 0
    for doc_id, slug, md, status, method, char_count in rows:
        if not slug:
            continue
        json_path = docs_dir / f"{slug}.json"
        if not json_path.exists():
            n_missing_json += 1
            continue
        try:
            with json_path.open(encoding="utf-8") as f:
                doc = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue

        body = strip_frontmatter(md or "")
        # Take first EXCERPT_CHARS without truncating mid-word
        excerpt = body[:EXCERPT_CHARS]
        # Backtrack to last whitespace if we cut mid-word
        if len(body) > EXCERPT_CHARS and excerpt:
            last_space = max(excerpt.rfind("\n\n"), excerpt.rfind(". "))
            if last_space > EXCERPT_CHARS - 500:
                excerpt = excerpt[:last_space + 1]
            excerpt = excerpt.rstrip() + "\n\n*[…excerpt continues — full text available in the database]*"

        doc["markdown_excerpt"] = excerpt
        doc["markdown_method"] = method
        doc["markdown_char_count_total"] = char_count
        doc["markdown_excerpt_truncated"] = len(body) > EXCERPT_CHARS

        with json_path.open("w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=2)
        n_updated += 1

    con.close()
    print(f"[done] updated {n_updated} doc JSON files; {n_missing_json} JSON files missing")
    return {"updated": n_updated, "missing_json": n_missing_json}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="C:/QueryPat/database/unified.sqlite")
    ap.add_argument("--data-dir", default="site/public/data")
    args = ap.parse_args()
    run(Path(args.db), Path(args.data_dir))
    return 0


if __name__ == "__main__":
    sys.exit(main())
