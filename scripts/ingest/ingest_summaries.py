"""
Stage 1: Ingest chunk summary markdown files into segments table.

Reads: {source}/summaries/chunks/*.md
Updates: segments table with parsed summary fields (concise_summary, key_claims, etc.)

Expects segments to already exist from ingest_manifests. If a segment doesn't exist,
creates it with doc_id inferred from the markdown header.
"""

import json
import re
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from date_norms import normalize_date, make_doc_id, make_seg_id


# Section headers to parse from markdown
SECTIONS = [
    'concise_summary',
    'key_claims',
    'recurring_concepts',
    'people_entities',
    'texts_works_referenced',
    'autobiographical_events',
    'theological_philosophical_motifs',
    'literary_self_reference',
    'symbols_images_metaphors',
    'tensions_contradictions',
    'evidence_quotes',
    'uncertainty_flags',
]


def parse_summary_md(filepath: Path) -> dict:
    """Parse a chunk summary markdown file into structured data."""
    text = filepath.read_text(encoding='utf-8')
    lines = text.split('\n')

    result = {
        'chunk_id': None,
        'section_id': None,
        'date_text': None,
        'recipient': None,
        'year': None,
        'reading_excerpt': None,
    }
    for s in SECTIONS:
        result[s] = None

    # Parse header lines (# comments at top)
    for line in lines:
        line = line.strip()
        if not line.startswith('#'):
            continue
        # Skip section headers (## )
        if line.startswith('## '):
            break

        content = line.lstrip('#').strip()

        # Try to match header fields
        if result['chunk_id'] is None and re.match(r'^[\w-]+_\d+$', content):
            result['chunk_id'] = content
        elif result['chunk_id'] is None and re.match(r'^U_\w+_\d+$', content):
            result['chunk_id'] = content
        elif content.startswith('SECTION_'):
            result['section_id'] = content
        elif not result['date_text'] and any(m in content.lower() for m in [
            'january', 'february', 'march', 'april', 'may', 'june',
            'july', 'august', 'september', 'october', 'november', 'december',
            'undated', 'circa',
        ]):
            result['date_text'] = content
        elif not result['recipient'] and content and not content.startswith('SECTION'):
            # Last unmatched header is likely recipient
            result['recipient'] = content

    # Fallback: derive chunk_id from filename
    if not result['chunk_id']:
        result['chunk_id'] = filepath.stem

    # Parse sections
    current_section = None
    current_lines = []

    for line in lines:
        stripped = line.strip()

        # Check for section header
        if stripped.startswith('## '):
            # Save previous section
            if current_section and current_lines:
                result[current_section] = _finalize_section(current_section, current_lines)
            # Start new section
            header = stripped[3:].strip().lower().replace(' ', '_')
            if header in SECTIONS:
                current_section = header
                current_lines = []
            else:
                current_section = None
                current_lines = []
        elif current_section:
            current_lines.append(line)

    # Save last section
    if current_section and current_lines:
        result[current_section] = _finalize_section(current_section, current_lines)

    # Extract reading excerpt (text between last section and end, or from evidence_quotes)
    # Look for a block that starts with > or is indented prose after all sections
    excerpt_match = re.search(r'(?:^|\n)> (.+?)(?:\n\n|\Z)', text, re.DOTALL)
    if excerpt_match:
        result['reading_excerpt'] = excerpt_match.group(1).strip()

    return result


def _finalize_section(section_name: str, lines: list) -> str:
    """Convert collected lines into either a text block or JSON array."""
    text = '\n'.join(lines).strip()
    if not text:
        return None

    # concise_summary is prose, not a list
    if section_name == 'concise_summary':
        return text

    # All other sections are bulleted lists → JSON arrays
    items = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('- ') or stripped.startswith('* '):
            items.append(stripped[2:].strip())
        elif stripped.startswith('  ') and items:
            # Continuation of previous item
            items[-1] += ' ' + stripped.strip()

    if items:
        return json.dumps(items, ensure_ascii=False)

    # Fallback: return raw text
    return text


def ingest_summaries(db: sqlite3.Connection, source_dir: Path):
    """Ingest all summary markdown files."""
    summaries_dir = source_dir / 'summaries' / 'chunks'
    if not summaries_dir.exists():
        print(f"  SKIP: {summaries_dir} not found")
        return 0

    md_files = sorted(summaries_dir.glob('*.md'))
    updated = 0
    created = 0

    for md_path in md_files:
        data = parse_summary_md(md_path)
        chunk_id = data['chunk_id']
        if not chunk_id:
            continue

        seg_id = make_seg_id('EXEG', chunk_id)

        # Check if segment exists
        row = db.execute("SELECT seg_id FROM segments WHERE seg_id = ?", (seg_id,)).fetchone()

        if row:
            # Update existing segment with summary data
            db.execute("""
                UPDATE segments SET
                    concise_summary = ?,
                    key_claims = ?,
                    recurring_concepts = ?,
                    people_entities = ?,
                    texts_works = ?,
                    autobiographical = ?,
                    theological_motifs = ?,
                    literary_self_ref = ?,
                    symbols_images = ?,
                    tensions = ?,
                    evidence_quotes = ?,
                    uncertainty_flags = ?,
                    reading_excerpt = ?,
                    updated_at = datetime('now')
                WHERE seg_id = ?
            """, (
                data.get('concise_summary'),
                data.get('key_claims'),
                data.get('recurring_concepts'),
                data.get('people_entities'),
                data.get('texts_works_referenced'),
                data.get('autobiographical_events'),
                data.get('theological_philosophical_motifs'),
                data.get('literary_self_reference'),
                data.get('symbols_images_metaphors'),
                data.get('tensions_contradictions'),
                data.get('evidence_quotes'),
                data.get('uncertainty_flags'),
                data.get('reading_excerpt'),
                seg_id,
            ))
            updated += 1
        else:
            # Create new segment (summary exists but no manifest entry)
            section_id = data.get('section_id', 'SECTION_001')
            doc_id = make_doc_id('EXEG', section_id)

            # Ensure parent document exists
            doc_exists = db.execute(
                "SELECT 1 FROM documents WHERE doc_id = ?", (doc_id,)
            ).fetchone()
            if not doc_exists:
                slug = (section_id or 'unknown').lower().replace('_', '-')
                db.execute("""
                    INSERT OR IGNORE INTO documents (doc_id, doc_type, title, slug)
                    VALUES (?, 'exegesis_section', ?, ?)
                """, (doc_id, section_id or 'Unknown', slug))

            nd = normalize_date(
                data.get('date_text'),
                basis='summary_header',
            )

            db.execute("""
                INSERT INTO segments (
                    seg_id, doc_id, seg_type, slug,
                    date_start, date_end, date_display, date_confidence, date_basis,
                    title,
                    concise_summary, key_claims, recurring_concepts,
                    people_entities, texts_works, autobiographical,
                    theological_motifs, literary_self_ref, symbols_images,
                    tensions, evidence_quotes, uncertainty_flags,
                    reading_excerpt
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                seg_id, doc_id, 'chunk',
                chunk_id.lower().replace('_', '-'),
                nd.date_start, nd.date_end, nd.date_display,
                nd.date_confidence, nd.date_basis,
                chunk_id,
                data.get('concise_summary'),
                data.get('key_claims'),
                data.get('recurring_concepts'),
                data.get('people_entities'),
                data.get('texts_works_referenced'),
                data.get('autobiographical_events'),
                data.get('theological_philosophical_motifs'),
                data.get('literary_self_reference'),
                data.get('symbols_images_metaphors'),
                data.get('tensions_contradictions'),
                data.get('evidence_quotes'),
                data.get('uncertainty_flags'),
                data.get('reading_excerpt'),
            ))
            created += 1

    db.commit()
    print(f"  Updated {updated} segments, created {created} new segments from summaries")
    return updated + created


def run(db: sqlite3.Connection, source_dir: Path):
    """Run summary ingestion."""
    print("Stage 1: Ingesting summaries...")
    ingest_summaries(db, source_dir)


if __name__ == '__main__':
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('C:/ExegesisAnalysis')
    db_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('C:/QueryPat/database/unified.sqlite')
    db = sqlite3.connect(str(db_path))
    run(db, source)
    db.close()
