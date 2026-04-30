"""EPUB -> markdown via ebooklib + markdownify.

Walks the OPF spine, converts each XHTML doc to markdown, joins with spacers.
"""
from __future__ import annotations

from pathlib import Path

import ebooklib
from ebooklib import epub
from markdownify import markdownify as html_to_md


def convert(path: Path) -> tuple[str, str]:
    book = epub.read_epub(str(path), options={"ignore_ncx": True})
    chunks: list[str] = []
    for item in book.get_items():
        if item.get_type() != ebooklib.ITEM_DOCUMENT:
            continue
        try:
            html = item.get_content().decode("utf-8", errors="replace")
        except Exception:
            continue
        md = html_to_md(html, heading_style="ATX", bullets="-")
        md = md.strip()
        if md:
            chunks.append(md)
    if not chunks:
        raise ValueError("EPUB had no document items")
    body = "\n\n---\n\n".join(chunks)

    # Front matter from EPUB metadata
    title = book.get_metadata("DC", "title")
    author = book.get_metadata("DC", "creator")
    front = []
    if title:
        front.append(f"# {title[0][0]}")
    if author:
        front.append(f"*by {author[0][0]}*")
    if front:
        body = "\n\n".join(front) + "\n\n---\n\n" + body

    return body, "ebooklib+markdownify"
