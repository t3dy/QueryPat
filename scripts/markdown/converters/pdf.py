"""PDF -> markdown via pymupdf4llm.

Returns (markdown_text, method_label) or raises.
For OCR-required (image-only) PDFs, raises OCRRequired so the caller can flag.
"""
from __future__ import annotations

from pathlib import Path

import pymupdf4llm
import fitz  # PyMuPDF


class OCRRequired(Exception):
    """PDF is image-only; no extractable text via PyMuPDF."""


def looks_image_only(path: Path) -> bool:
    """Heuristic: open a few pages, if extracted text < 200 chars total, treat as OCR-required."""
    try:
        doc = fitz.open(path)
    except Exception:
        return False
    sample_pages = min(5, doc.page_count)
    total_chars = 0
    for i in range(sample_pages):
        total_chars += len(doc[i].get_text("text"))
        if total_chars >= 200:
            doc.close()
            return False
    doc.close()
    # Got through 5 pages with <200 chars — likely scanned.
    return True


def convert(path: Path) -> tuple[str, str]:
    if looks_image_only(path):
        raise OCRRequired(f"{path.name} appears to be image-only (no text in first 5 pages)")
    md = pymupdf4llm.to_markdown(str(path))
    return md, "pymupdf4llm"
