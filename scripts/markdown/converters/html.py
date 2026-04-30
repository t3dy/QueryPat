"""HTML -> markdown via bs4 + markdownify."""
from __future__ import annotations

from pathlib import Path

from bs4 import BeautifulSoup
from markdownify import markdownify as html_to_md


def convert(path: Path) -> tuple[str, str]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(raw, "html.parser")
    # Strip noise
    for tag in soup(["script", "style", "nav", "header", "footer", "aside", "noscript"]):
        tag.decompose()
    body = soup.body or soup
    md = html_to_md(str(body), heading_style="ATX", bullets="-")
    return md.strip(), "bs4+markdownify"
