"""
Date normalization constants and utilities for QueryPat pipeline.

All ingest scripts MUST use these functions for date handling.
No ad-hoc date parsing elsewhere in the codebase.
"""

import re
from dataclasses import dataclass
from typing import Optional

# Month name → number mapping
MONTHS = {
    'january': '01', 'february': '02', 'march': '03', 'april': '04',
    'may': '05', 'june': '06', 'july': '07', 'august': '08',
    'september': '09', 'october': '10', 'november': '11', 'december': '12',
    'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
    'jun': '06', 'jul': '07', 'aug': '08', 'sep': '09',
    'oct': '10', 'nov': '11', 'dec': '12',
}

# Confidence levels
EXACT = 'exact'
APPROXIMATE = 'approximate'
CIRCA = 'circa'
INFERRED = 'inferred'
UNKNOWN = 'unknown'

# Timeline types
COMPOSITION = 'composition'
PUBLICATION = 'publication'
LETTER = 'letter'
EVENT_DISCUSSED = 'event_discussed'
INTERVIEW = 'interview'
TIMELINE_UNKNOWN = 'unknown'


@dataclass
class NormalizedDate:
    """Canonical date representation. All fields are Optional[str]."""
    date_start: Optional[str]       # ISO partial: 1977, 1977-03, 1977-03-14
    date_end: Optional[str]         # for ranges; same as start if not a range
    date_display: str               # human-readable: "circa 1977", "March 14, 1977"
    date_confidence: str            # exact, approximate, circa, inferred, unknown
    date_basis: Optional[str]       # how determined

    def to_dict(self) -> dict:
        return {
            'date_start': self.date_start,
            'date_end': self.date_end,
            'date_display': self.date_display,
            'date_confidence': self.date_confidence,
            'date_basis': self.date_basis,
        }


def normalize_date(
    raw: Optional[str],
    iso_hint: Optional[str] = None,
    basis: Optional[str] = None,
) -> NormalizedDate:
    """
    Normalize a raw date string into canonical form.

    Args:
        raw: The raw date text (e.g. "February 27, 1975", "circa 1977", "1979-1980")
        iso_hint: An ISO date if already known (from manifests)
        basis: How the date was determined (e.g. "manuscript header")

    Returns:
        NormalizedDate with all fields populated.

    Examples:
        normalize_date(None)
          → NormalizedDate(None, None, "Unknown", "unknown", None)

        normalize_date("February 27, 1975")
          → NormalizedDate("1975-02-27", "1975-02-27", "February 27, 1975", "exact", None)

        normalize_date("circa 1977")
          → NormalizedDate("1977", "1977", "circa 1977", "circa", None)

        normalize_date("1979-1980")
          → NormalizedDate("1979", "1980", "circa 1979-1980", "circa", None)

        normalize_date("March 1977")
          → NormalizedDate("1977-03", "1977-03", "March 1977", "approximate", None)
    """
    if not raw and not iso_hint:
        return NormalizedDate(None, None, "Unknown", UNKNOWN, basis)

    # If we have a clean ISO hint, use it
    if iso_hint and re.match(r'^\d{4}-\d{2}-\d{2}$', iso_hint):
        display = raw if raw else iso_hint
        return NormalizedDate(iso_hint, iso_hint, display, EXACT, basis)

    if not raw:
        return NormalizedDate(iso_hint, iso_hint, iso_hint or "Unknown", INFERRED, basis)

    text = raw.strip()

    # "circa YYYY" or "c. YYYY"
    m = re.match(r'(?:circa|c\.?)\s+(\d{4})(?:\s*[-–]\s*(\d{4}))?', text, re.IGNORECASE)
    if m:
        start = m.group(1)
        end = m.group(2) or start
        return NormalizedDate(start, end, text, CIRCA, basis)

    # Range: "YYYY-YYYY" or "YYYY–YYYY"
    m = re.match(r'^(\d{4})\s*[-–]\s*(\d{4})$', text)
    if m:
        return NormalizedDate(m.group(1), m.group(2), f"circa {text}", CIRCA, basis)

    # Full date: "Month DD, YYYY"
    m = re.match(r'^(\w+)\s+(\d{1,2}),?\s+(\d{4})$', text)
    if m:
        month_name = m.group(1).lower()
        day = m.group(2).zfill(2)
        year = m.group(3)
        month_num = MONTHS.get(month_name)
        if month_num:
            iso = f"{year}-{month_num}-{day}"
            return NormalizedDate(iso, iso, text, EXACT, basis)

    # Month + Year: "March 1977"
    m = re.match(r'^(\w+)\s+(\d{4})$', text)
    if m:
        month_name = m.group(1).lower()
        year = m.group(2)
        month_num = MONTHS.get(month_name)
        if month_num:
            iso = f"{year}-{month_num}"
            return NormalizedDate(iso, iso, text, APPROXIMATE, basis)

    # Year only: "1977"
    m = re.match(r'^(\d{4})$', text)
    if m:
        return NormalizedDate(m.group(1), m.group(1), text, APPROXIMATE, basis)

    # ISO date: "1977-03-14"
    m = re.match(r'^(\d{4}-\d{2}-\d{2})$', text)
    if m:
        return NormalizedDate(m.group(1), m.group(1), text, EXACT, basis)

    # ISO partial: "1977-03"
    m = re.match(r'^(\d{4}-\d{2})$', text)
    if m:
        return NormalizedDate(m.group(1), m.group(1), text, APPROXIMATE, basis)

    # Fallback: preserve raw text, mark as inferred
    return NormalizedDate(None, None, text, INFERRED, basis)


def make_slug(text: str) -> str:
    """Convert text to a URL-safe slug."""
    slug = text.lower().strip()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'[\s-]+', '-', slug)
    slug = slug.strip('-')
    return slug


def make_term_id(canonical_name: str) -> str:
    """Generate a stable term ID from canonical name."""
    return f"TERM_{make_slug(canonical_name)}"


def make_doc_id(doc_type: str, identifier: str) -> str:
    """Generate a document ID. doc_type is 'EXEG' or 'ARCH'."""
    return f"DOC_{doc_type}_{identifier}"


def make_seg_id(seg_type: str, identifier: str) -> str:
    """Generate a segment ID. seg_type is 'EXEG' or 'ARCH'."""
    return f"SEG_{seg_type}_{identifier}"


def make_event_id(slug: str) -> str:
    """Generate a timeline event ID."""
    return f"TL_{slug}"


def make_asset_id(slug: str) -> str:
    """Generate an asset ID."""
    return f"ASSET_{slug}"


def make_evidence_id(term_slug: str, seg_id: str) -> str:
    """Generate an evidence packet ID."""
    return f"EV_{term_slug}_{seg_id}"
