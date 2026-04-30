"""Idempotent schema migration: add markdown columns to document_texts.

Usage:
    python scripts/markdown/add_markdown_columns.py [--db PATH]

Default DB: database/unified.sqlite (relative to CWD).
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

NEW_COLUMNS = [
    ("markdown_content", "TEXT"),
    ("markdown_method", "TEXT"),
    ("markdown_status", "TEXT"),
    ("markdown_char_count", "INTEGER"),
    ("markdown_error", "TEXT"),
    ("markdown_updated_at", "TEXT"),
    ("markdown_source_hash", "TEXT"),
]


def get_existing_columns(con: sqlite3.Connection, table: str) -> set[str]:
    cur = con.execute(f"PRAGMA table_info({table})")
    return {row[1] for row in cur.fetchall()}


def migrate(db_path: Path) -> int:
    if not db_path.exists():
        print(f"[error] DB not found: {db_path}", file=sys.stderr)
        return 1
    con = sqlite3.connect(db_path)
    existing = get_existing_columns(con, "document_texts")
    if not existing:
        print(f"[error] table 'document_texts' not found in {db_path}", file=sys.stderr)
        return 1

    added = 0
    for name, type_ in NEW_COLUMNS:
        if name in existing:
            print(f"  [skip] {name} already exists")
            continue
        con.execute(f"ALTER TABLE document_texts ADD COLUMN {name} {type_}")
        print(f"  [add]  {name} {type_}")
        added += 1

    # Mark all existing rows as "pending" markdown so the converter knows what to do.
    if added > 0:
        con.execute(
            "UPDATE document_texts SET markdown_status='pending' WHERE markdown_status IS NULL"
        )
    con.commit()
    con.close()
    print(f"\n[done] {added} columns added to document_texts in {db_path}")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="database/unified.sqlite")
    args = ap.parse_args()
    return migrate(Path(args.db))


if __name__ == "__main__":
    sys.exit(main())
