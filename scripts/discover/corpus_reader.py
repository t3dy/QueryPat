"""
Read corpus text from SQLite for discovery analysis.

Two text sources:
  - segments.raw_text    Exegesis chunks (~9.7M chars across 882 segments)
  - document_texts.text_content   Archive PDF text (~605K chars across 181 docs)
"""

import sqlite3
from dataclasses import dataclass, field


@dataclass
class CorpusChunk:
    """A unit of corpus text with provenance."""
    source_id: str          # seg_id or doc_id
    source_type: str        # 'segment' or 'document'
    title: str
    text: str
    char_count: int
    date_start: str | None = None
    category: str | None = None
    doc_type: str | None = None


def read_segment_texts(db: sqlite3.Connection, min_chars: int = 50) -> list[CorpusChunk]:
    """Read all segment raw texts above a minimum size."""
    rows = db.execute("""
        SELECT s.seg_id, s.title, s.raw_text, s.raw_text_char_count,
               s.date_start, s.concise_summary
        FROM segments s
        WHERE s.raw_text IS NOT NULL AND LENGTH(s.raw_text) >= ?
    """, (min_chars,)).fetchall()

    chunks = []
    for seg_id, title, raw_text, char_count, date_start, summary in rows:
        # Concatenate summary into text for richer extraction
        full_text = raw_text
        if summary:
            full_text = summary + '\n\n' + raw_text
        chunks.append(CorpusChunk(
            source_id=seg_id,
            source_type='segment',
            title=title or seg_id,
            text=full_text,
            char_count=len(full_text),
            date_start=date_start,
        ))
    return chunks


def read_document_texts(db: sqlite3.Connection, min_chars: int = 50) -> list[CorpusChunk]:
    """Read all archive document extracted texts above a minimum size."""
    rows = db.execute("""
        SELECT d.doc_id, d.title, dt.text_content, dt.char_count,
               d.date_start, d.category, d.doc_type
        FROM document_texts dt
        JOIN documents d ON dt.doc_id = d.doc_id
        WHERE dt.text_content IS NOT NULL AND dt.char_count >= ?
          AND d.doc_type != 'exegesis_section'
    """, (min_chars,)).fetchall()

    chunks = []
    for doc_id, title, text, char_count, date_start, category, doc_type in rows:
        chunks.append(CorpusChunk(
            source_id=doc_id,
            source_type='document',
            title=title or doc_id,
            text=text,
            char_count=char_count or len(text),
            date_start=date_start,
            category=category,
            doc_type=doc_type,
        ))
    return chunks


def read_all_corpus(db: sqlite3.Connection, min_chars: int = 50) -> list[CorpusChunk]:
    """Read all corpus text from both sources."""
    segments = read_segment_texts(db, min_chars)
    documents = read_document_texts(db, min_chars)
    return segments + documents


def read_existing_terms(db: sqlite3.Connection) -> dict[str, dict]:
    """
    Load all existing terms and aliases as a lookup dict.
    Keys: lowercased canonical names and alias texts.
    Values: dict with term_id, canonical_name, status.
    """
    lookup = {}

    rows = db.execute("""
        SELECT term_id, canonical_name, slug, status, mention_count
        FROM terms
    """).fetchall()
    for term_id, name, slug, status, count in rows:
        lookup[name.lower()] = {
            'term_id': term_id, 'canonical_name': name,
            'slug': slug, 'status': status, 'mention_count': count,
        }

    alias_rows = db.execute("""
        SELECT ta.alias_text, ta.term_id, t.canonical_name, t.status
        FROM term_aliases ta
        JOIN terms t ON ta.term_id = t.term_id
    """).fetchall()
    for alias_text, term_id, name, status in alias_rows:
        lookup[alias_text.lower()] = {
            'term_id': term_id, 'canonical_name': name,
            'slug': None, 'status': status,
        }

    return lookup


def read_existing_names(db: sqlite3.Connection) -> dict[str, dict]:
    """
    Load all existing names and aliases as a lookup dict.
    Keys: lowercased canonical forms and alias texts.
    """
    lookup = {}

    rows = db.execute("""
        SELECT name_id, canonical_form, slug, entity_type, status, mention_count
        FROM names
    """).fetchall()
    for name_id, form, slug, etype, status, count in rows:
        lookup[form.lower()] = {
            'name_id': name_id, 'canonical_form': form,
            'slug': slug, 'entity_type': etype, 'status': status,
            'mention_count': count,
        }

    alias_rows = db.execute("""
        SELECT na.alias_text, na.name_id, n.canonical_form, n.entity_type
        FROM name_aliases na
        JOIN names n ON na.name_id = n.name_id
    """).fetchall()
    for alias_text, name_id, form, etype in alias_rows:
        lookup[alias_text.lower()] = {
            'name_id': name_id, 'canonical_form': form,
            'entity_type': etype,
        }

    return lookup


def read_existing_events(db: sqlite3.Connection) -> list[dict]:
    """Load existing biography events for dedup checking."""
    rows = db.execute("""
        SELECT bio_id, summary, date_start, date_end, event_type, source_name
        FROM biography_events
    """).fetchall()
    return [
        {'bio_id': r[0], 'summary': r[1], 'date_start': r[2],
         'date_end': r[3], 'event_type': r[4], 'source_name': r[5]}
        for r in rows
    ]
