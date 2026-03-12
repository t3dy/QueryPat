"""
Export SQLite database to route-specific JSON bundles for the static site.

Output structure:
  site/public/data/
    timeline/index.json
    timeline/years/{year}.json
    dictionary/index.json
    dictionary/terms/{slug}.json
    archive/index.json
    archive/docs/{slug}.json
    segments/{seg_id}.json (lazy-loaded)
    search_index.json
    analytics.json
    graph.json
"""

import json
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def dict_factory(cursor, row):
    return {col[0]: row[i] for i, col in enumerate(cursor.description)}


def export_timeline(db: sqlite3.Connection, data_dir: Path):
    """Export timeline data split by year."""
    print("  Exporting timeline...")
    timeline_dir = data_dir / 'timeline'
    years_dir = timeline_dir / 'years'
    ensure_dir(years_dir)

    # Get all segments with dates, grouped by year
    rows = db.execute("""
        SELECT seg_id, doc_id, slug, title,
               date_start, date_end, date_display, date_confidence,
               concise_summary, recurring_concepts, people_entities, tensions,
               reading_excerpt, word_count
        FROM segments
        WHERE date_start IS NOT NULL
        ORDER BY date_start, position
    """).fetchall()

    years = defaultdict(list)
    for row in rows:
        seg = {
            'seg_id': row[0], 'doc_id': row[1], 'slug': row[2], 'title': row[3],
            'date_start': row[4], 'date_end': row[5], 'date_display': row[6],
            'date_confidence': row[7], 'concise_summary': row[8],
            'recurring_concepts': _parse_json(row[9]),
            'people_entities': _parse_json(row[10]),
            'tensions': _parse_json(row[11]),
            'reading_excerpt': row[12],
            'word_count': row[13],
        }
        year = row[4][:4] if row[4] else 'unknown'
        years[year].append(seg)

    # Write index
    index = [{'year': y, 'count': len(segs)} for y, segs in sorted(years.items())]
    _write_json(timeline_dir / 'index.json', index)

    # Write per-year files
    for year, segs in years.items():
        _write_json(years_dir / f'{year}.json', segs)

    print(f"    {len(rows)} segments across {len(years)} years")


def export_dictionary(db: sqlite3.Connection, data_dir: Path):
    """Export dictionary terms."""
    print("  Exporting dictionary...")
    dict_dir = data_dir / 'dictionary'
    terms_dir = dict_dir / 'terms'
    ensure_dir(terms_dir)

    # Index: accepted + provisional terms (summary fields)
    rows = db.execute("""
        SELECT term_id, canonical_name, slug, status, review_state,
               primary_category, mention_count, card_description,
               first_appearance, peak_usage_start
        FROM terms
        WHERE status IN ('accepted', 'provisional')
        ORDER BY mention_count DESC
    """).fetchall()

    index = []
    for row in rows:
        index.append({
            'term_id': row[0], 'canonical_name': row[1], 'slug': row[2],
            'status': row[3], 'review_state': row[4],
            'primary_category': row[5], 'mention_count': row[6],
            'card_description': (row[7] or '')[:300],  # truncate for index
            'first_appearance': row[8], 'peak_usage_start': row[9],
        })
    _write_json(dict_dir / 'index.json', index)

    # Per-term detail files
    for term_row in index:
        term_id = term_row['term_id']
        slug = term_row['slug']

        # Full term data
        full = db.execute("""
            SELECT * FROM terms WHERE term_id = ?
        """, (term_id,)).fetchone()
        cols = [d[0] for d in db.execute("SELECT * FROM terms LIMIT 0").description]
        term_data = dict(zip(cols, full))

        # Parse JSON fields
        for field in ['thematic_categories', 'see_also']:
            term_data[field] = _parse_json(term_data.get(field))

        # Aliases
        aliases = db.execute("""
            SELECT alias_text, alias_type FROM term_aliases WHERE term_id = ?
        """, (term_id,)).fetchall()
        term_data['aliases'] = [{'text': a[0], 'type': a[1]} for a in aliases]

        # Linked segments (confidence <= 3 only for public)
        linked_segs = db.execute("""
            SELECT ts.seg_id, ts.match_type, ts.link_confidence,
                   s.date_display, s.concise_summary, s.title
            FROM term_segments ts
            JOIN segments s ON ts.seg_id = s.seg_id
            WHERE ts.term_id = ? AND ts.link_confidence <= 3
            ORDER BY s.date_start
            LIMIT 50
        """, (term_id,)).fetchall()
        term_data['linked_segments'] = [{
            'seg_id': r[0], 'match_type': r[1], 'confidence': r[2],
            'date_display': r[3], 'summary': (r[4] or '')[:200], 'title': r[5],
        } for r in linked_segs]

        # Related terms
        related = db.execute("""
            SELECT t.canonical_name, t.slug, tt.relation_type, tt.link_confidence
            FROM term_terms tt
            JOIN terms t ON tt.term_id_b = t.term_id
            WHERE tt.term_id_a = ?
            UNION
            SELECT t.canonical_name, t.slug, tt.relation_type, tt.link_confidence
            FROM term_terms tt
            JOIN terms t ON tt.term_id_a = t.term_id
            WHERE tt.term_id_b = ?
        """, (term_id, term_id)).fetchall()
        term_data['related_terms'] = [{
            'name': r[0], 'slug': r[1], 'relation': r[2], 'confidence': r[3],
        } for r in related]

        # Evidence excerpts (top 10)
        excerpts = db.execute("""
            SELECT ee.excerpt_text, ee.line_start, ee.line_end, ee.matched_alias,
                   ep.confidence, ep.source_method
            FROM evidence_excerpts ee
            JOIN evidence_packets ep ON ee.ev_id = ep.ev_id
            WHERE ep.term_id = ?
            LIMIT 10
        """, (term_id,)).fetchall()
        term_data['evidence'] = [{
            'text': r[0][:500], 'line_start': r[1], 'line_end': r[2],
            'matched_alias': r[3], 'confidence': r[4], 'source_method': r[5],
        } for r in excerpts]

        _write_json(terms_dir / f'{slug}.json', term_data)

    print(f"    {len(index)} public terms exported")


def export_archive(db: sqlite3.Connection, data_dir: Path):
    """Export archive documents."""
    print("  Exporting archive...")
    arch_dir = data_dir / 'archive'
    docs_dir = arch_dir / 'docs'
    ensure_dir(docs_dir)

    rows = db.execute("""
        SELECT doc_id, title, slug, author, doc_type, category,
               date_display, date_start, is_pkd_authored,
               card_summary, page_summary, page_count,
               ingest_level, extraction_status
        FROM documents
        WHERE doc_type != 'exegesis_section'
        ORDER BY category, title
    """).fetchall()

    index = []
    for row in rows:
        entry = {
            'doc_id': row[0], 'title': row[1], 'slug': row[2],
            'author': row[3], 'doc_type': row[4], 'category': row[5],
            'date_display': row[6], 'date_start': row[7],
            'is_pkd_authored': bool(row[8]),
            'card_summary': row[9], 'page_count': row[11],
            'ingest_level': row[12], 'extraction_status': row[13],
        }
        index.append(entry)

        # Detail file includes page_summary
        detail = dict(entry)
        detail['page_summary'] = row[10]

        # Get linked assets
        assets = db.execute("""
            SELECT a.file_path, a.asset_type, a.file_size_mb
            FROM document_assets da
            JOIN assets a ON da.asset_id = a.asset_id
            WHERE da.doc_id = ?
        """, (row[0],)).fetchall()
        detail['assets'] = [{'path': a[0], 'type': a[1], 'size_mb': a[2]} for a in assets]

        _write_json(docs_dir / f'{row[2]}.json', detail)

    _write_json(arch_dir / 'index.json', index)
    print(f"    {len(index)} archive documents exported")


def export_search_index(db: sqlite3.Connection, data_dir: Path):
    """Export precomputed search index for Fuse.js."""
    print("  Exporting search index...")

    entries = []

    # Segments
    rows = db.execute("""
        SELECT seg_id, slug, title, date_display, concise_summary
        FROM segments
        WHERE concise_summary IS NOT NULL
    """).fetchall()
    for row in rows:
        entries.append({
            'type': 'segment',
            'id': row[0], 'slug': row[1], 'title': row[2],
            'date': row[3],
            'text': (row[4] or '')[:300],
        })

    # Terms
    rows = db.execute("""
        SELECT term_id, slug, canonical_name, card_description, primary_category
        FROM terms
        WHERE status IN ('accepted', 'provisional')
    """).fetchall()
    for row in rows:
        entries.append({
            'type': 'term',
            'id': row[0], 'slug': row[1], 'title': row[2],
            'text': (row[3] or '')[:300],
            'category': row[4],
        })

    # Archive docs
    rows = db.execute("""
        SELECT doc_id, slug, title, author, card_summary, category
        FROM documents
        WHERE doc_type != 'exegesis_section'
    """).fetchall()
    for row in rows:
        entries.append({
            'type': 'archive',
            'id': row[0], 'slug': row[1], 'title': row[2],
            'author': row[3],
            'text': (row[4] or '')[:300],
            'category': row[5],
        })

    _write_json(data_dir / 'search_index.json', entries)
    print(f"    {len(entries)} search entries")


def export_analytics(db: sqlite3.Connection, data_dir: Path):
    """Export precomputed analytics data."""
    print("  Exporting analytics...")

    analytics = {}

    # Term frequency top 30
    rows = db.execute("""
        SELECT canonical_name, mention_count, primary_category
        FROM terms WHERE status IN ('accepted', 'provisional')
        ORDER BY mention_count DESC LIMIT 30
    """).fetchall()
    analytics['top_terms'] = [{'name': r[0], 'count': r[1], 'category': r[2]} for r in rows]

    # Segments per year
    rows = db.execute("""
        SELECT SUBSTR(date_start, 1, 4) AS year, COUNT(*) AS cnt
        FROM segments
        WHERE date_start IS NOT NULL
        GROUP BY year ORDER BY year
    """).fetchall()
    analytics['segments_per_year'] = [{'year': r[0], 'count': r[1]} for r in rows]

    # Category distribution (terms)
    rows = db.execute("""
        SELECT primary_category, COUNT(*) AS cnt
        FROM terms WHERE status IN ('accepted', 'provisional')
        GROUP BY primary_category ORDER BY cnt DESC
    """).fetchall()
    analytics['term_categories'] = [{'category': r[0] or 'Uncategorized', 'count': r[1]} for r in rows]

    # Archive by category
    rows = db.execute("""
        SELECT category, COUNT(*) AS cnt
        FROM documents WHERE doc_type != 'exegesis_section'
        GROUP BY category ORDER BY cnt DESC
    """).fetchall()
    analytics['archive_categories'] = [{'category': r[0] or 'Other', 'count': r[1]} for r in rows]

    # Totals
    analytics['totals'] = {
        'documents': db.execute("SELECT COUNT(*) FROM documents").fetchone()[0],
        'segments': db.execute("SELECT COUNT(*) FROM segments").fetchone()[0],
        'terms_public': db.execute("SELECT COUNT(*) FROM terms WHERE status IN ('accepted', 'provisional')").fetchone()[0],
        'terms_total': db.execute("SELECT COUNT(*) FROM terms").fetchone()[0],
        'evidence_packets': db.execute("SELECT COUNT(*) FROM evidence_packets").fetchone()[0],
        'archive_docs': db.execute("SELECT COUNT(*) FROM documents WHERE doc_type != 'exegesis_section'").fetchone()[0],
        'timeline_events': db.execute("SELECT COUNT(*) FROM timeline_events").fetchone()[0],
    }

    _write_json(data_dir / 'analytics.json', analytics)


def export_biography(db: sqlite3.Connection, data_dir: Path):
    """Export biography events."""
    print("  Exporting biography...")
    bio_dir = data_dir / 'biography'
    ensure_dir(bio_dir)

    rows = db.execute("""
        SELECT bio_id, event_type, summary, detail,
               date_start, date_end, date_display, date_confidence,
               source_type, source_name, source_doc_id, source_seg_id,
               contradicted_by, contradiction_note, reliability,
               people_involved, notes
        FROM biography_events
        ORDER BY date_start NULLS LAST, bio_id
    """).fetchall()

    events = []
    type_counts = defaultdict(int)
    for row in rows:
        event = {
            'bio_id': row[0], 'event_type': row[1],
            'summary': row[2], 'detail': row[3],
            'date_start': row[4], 'date_end': row[5],
            'date_display': row[6], 'date_confidence': row[7],
            'source_type': row[8], 'source_name': row[9],
            'source_doc_id': row[10], 'source_seg_id': row[11],
            'contradicted_by': _parse_json(row[12]),
            'contradiction_note': row[13],
            'reliability': row[14],
            'people_involved': _parse_json(row[15]),
            'notes': row[16],
        }
        events.append(event)
        type_counts[row[1]] += 1

    # Index with counts by type and date range
    index = {
        'total': len(events),
        'by_type': [{'type': t, 'count': c} for t, c in sorted(type_counts.items(), key=lambda x: -x[1])],
        'reliability_counts': {},
    }

    # Reliability distribution
    for row in db.execute("""
        SELECT reliability, COUNT(*) FROM biography_events GROUP BY reliability
    """).fetchall():
        index['reliability_counts'][row[0] or 'unknown'] = row[1]

    _write_json(bio_dir / 'index.json', index)
    _write_json(bio_dir / 'events.json', events)

    print(f"    {len(events)} biography events exported")


def export_graph(db: sqlite3.Connection, data_dir: Path):
    """Export precomputed graph data for Cytoscape.js."""
    print("  Exporting graph...")

    nodes = []
    edges = []

    # Nodes: public terms
    rows = db.execute("""
        SELECT term_id, canonical_name, slug, primary_category, mention_count
        FROM terms WHERE status IN ('accepted', 'provisional')
    """).fetchall()
    for row in rows:
        nodes.append({
            'id': row[0], 'label': row[1], 'slug': row[2],
            'category': row[3], 'weight': row[4],
        })

    # Edges: term-term relations
    rows = db.execute("""
        SELECT tt.term_id_a, tt.term_id_b, tt.relation_type, tt.strength
        FROM term_terms tt
        JOIN terms t1 ON tt.term_id_a = t1.term_id
        JOIN terms t2 ON tt.term_id_b = t2.term_id
        WHERE t1.status IN ('accepted', 'provisional')
        AND t2.status IN ('accepted', 'provisional')
    """).fetchall()
    for row in rows:
        edges.append({
            'source': row[0], 'target': row[1],
            'relation': row[2], 'weight': row[3],
        })

    _write_json(data_dir / 'graph.json', {'nodes': nodes, 'edges': edges})
    print(f"    {len(nodes)} nodes, {len(edges)} edges")


def _parse_json(val):
    """Parse a JSON string, returning the parsed value or the original."""
    if not val:
        return None
    try:
        return json.loads(val)
    except (json.JSONDecodeError, TypeError):
        return val


def _write_json(path: Path, data):
    """Write JSON with consistent formatting."""
    ensure_dir(path.parent)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def run(db: sqlite3.Connection, project_dir: Path):
    """Run all JSON exports."""
    print("Exporting JSON bundles...")
    data_dir = project_dir / 'site' / 'public' / 'data'
    ensure_dir(data_dir)

    export_timeline(db, data_dir)
    export_dictionary(db, data_dir)
    export_archive(db, data_dir)
    export_biography(db, data_dir)
    export_search_index(db, data_dir)
    export_analytics(db, data_dir)
    export_graph(db, data_dir)

    print("  Export complete")


if __name__ == '__main__':
    db_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('C:/QueryPat/database/unified.sqlite')
    project_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('C:/QueryPat')
    db = sqlite3.connect(str(db_path))
    run(db, project_dir)
    db.close()
