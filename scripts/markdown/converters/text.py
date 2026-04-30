"""Plain text -> markdown.

Mostly passthrough; collapse runs of >2 blank lines to exactly 2.
"""
from __future__ import annotations

from pathlib import Path
import re


def convert(path: Path) -> tuple[str, str]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    # Normalize line endings, collapse triple+ blank lines.
    text = raw.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip(), "passthrough"
