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
               reading_excerpt, word_count,
               CASE WHEN raw_text IS NOT NULL THEN 1 ELSE 0 END AS has_raw_text
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
            'has_raw_text': bool(row[14]),
        }
        year = row[4][:4] if row[4] else 'unknown'
        years[year].append(seg)

    # Load biography events per year
    bio_rows = db.execute("""
        SELECT bio_id, summary, date_start, date_end,
               event_type, source_name, date_confidence
        FROM biography_events
        WHERE date_start IS NOT NULL
        ORDER BY date_start
    """).fetchall()
    bio_years = defaultdict(list)
    for br in bio_rows:
        yr = br[2][:4] if br[2] else None
        if yr and 1928 <= int(yr) <= 1982:
            bio_years[yr].append({
                'bio_id': br[0], 'summary': br[1],
                'date_start': br[2], 'date_end': br[3],
                'event_type': br[4], 'source_name': br[5],
                'date_confidence': br[6],
                '_type': 'biography_event',
            })

    # Merge all years (segments + biography events)
    all_year_keys = sorted(set(years.keys()) | set(bio_years.keys()))

    # Write index with both counts
    index = []
    for y in all_year_keys:
        seg_count = len(years.get(y, []))
        bio_count = len(bio_years.get(y, []))
        index.append({'year': y, 'count': seg_count, 'bio_events': bio_count})
    _write_json(timeline_dir / 'index.json', index)

    # Write per-year files (segments + biography events combined)
    for y in all_year_keys:
        year_data = years.get(y, [])
        if bio_years.get(y):
            year_data = year_data + bio_years[y]
        _write_json(years_dir / f'{y}.json', year_data)

    print(f"    {len(rows)} segments + {len(bio_rows)} bio events across {len(all_year_keys)} years")


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

    # Check for new columns
    doc_cols = [c[1] for c in db.execute("PRAGMA table_info(documents)").fetchall()]
    has_lane = 'evidentiary_lane' in doc_cols
    has_reliability = 'source_reliability' in doc_cols

    # Load document_topics if table exists
    doc_topics = defaultdict(lambda: defaultdict(list))
    try:
        for t in db.execute("SELECT doc_id, topic_type, topic_value FROM document_topics"):
            doc_topics[t[0]][t[1]].append(t[2])
    except sqlite3.OperationalError:
        pass

    lane_col = ", evidentiary_lane, source_reliability" if has_lane else ""
    rows = db.execute(f"""
        SELECT doc_id, title, slug, author, doc_type, category,
               date_display, date_start, is_pkd_authored,
               card_summary, page_summary, page_count,
               ingest_level, extraction_status{lane_col}
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
        if has_lane:
            entry['evidentiary_lane'] = row[14]
            entry['source_reliability'] = row[15]
        index.append(entry)

        # Detail file includes page_summary and topics
        detail = dict(entry)
        detail['page_summary'] = row[10]
        topics = doc_topics.get(row[0], {})
        if topics:
            detail['people_mentioned'] = topics.get('person', [])
            detail['works_discussed'] = topics.get('work', [])
            detail['linked_terms'] = topics.get('term', [])

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


def export_segments(db: sqlite3.Connection, data_dir: Path):
    """Export individual segment detail files with raw text."""
    print("  Exporting segment detail files...")
    seg_dir = data_dir / 'segments'
    ensure_dir(seg_dir)

    # Check for works_referenced column
    seg_cols_info = [c[1] for c in db.execute("PRAGMA table_info(segments)").fetchall()]
    has_works_ref = 'works_referenced' in seg_cols_info
    works_col = ", works_referenced" if has_works_ref else ""

    rows = db.execute(f"""
        SELECT seg_id, doc_id, slug, title, position,
               date_start, date_end, date_display, date_confidence, date_basis,
               concise_summary, key_claims, recurring_concepts, people_entities,
               texts_works, autobiographical, theological_motifs, literary_self_ref,
               symbols_images, tensions, evidence_quotes, uncertainty_flags,
               reading_excerpt, word_count,
               raw_text, raw_text_char_count{works_col}
        FROM segments
        ORDER BY date_start NULLS LAST, position
    """).fetchall()

    cols = ['seg_id', 'doc_id', 'slug', 'title', 'position',
            'date_start', 'date_end', 'date_display', 'date_confidence', 'date_basis',
            'concise_summary', 'key_claims', 'recurring_concepts', 'people_entities',
            'texts_works', 'autobiographical', 'theological_motifs', 'literary_self_ref',
            'symbols_images', 'tensions', 'evidence_quotes', 'uncertainty_flags',
            'reading_excerpt', 'word_count',
            'raw_text', 'raw_text_char_count']
    if has_works_ref:
        cols.append('works_referenced')

    json_fields = {'key_claims', 'recurring_concepts', 'people_entities',
                   'texts_works', 'autobiographical', 'theological_motifs',
                   'literary_self_ref', 'symbols_images', 'tensions',
                   'evidence_quotes', 'uncertainty_flags', 'works_referenced'}

    exported = 0
    for row in rows:
        seg = dict(zip(cols, row))
        seg_id = seg['seg_id']

        # Parse JSON array fields
        for field in json_fields:
            seg[field] = _parse_json(seg.get(field))

        # Get linked terms (all confidence levels, sorted)
        linked_terms = db.execute("""
            SELECT ts.term_id, t.canonical_name, t.slug,
                   ts.match_type, ts.link_confidence, ts.matched_text
            FROM term_segments ts
            JOIN terms t ON ts.term_id = t.term_id
            WHERE ts.seg_id = ?
            ORDER BY ts.link_confidence, t.canonical_name
        """, (seg_id,)).fetchall()
        seg['linked_terms'] = [{
            'term_id': r[0], 'name': r[1], 'slug': r[2],
            'match_type': r[3], 'confidence': r[4], 'matched_text': r[5],
        } for r in linked_terms]

        # Get linked names
        linked_names = db.execute("""
            SELECT ns.name_id, n.canonical_form, n.slug,
                   ns.match_type, ns.link_confidence
            FROM name_segments ns
            JOIN names n ON ns.name_id = n.name_id
            WHERE ns.seg_id = ?
            ORDER BY ns.link_confidence
        """, (seg_id,)).fetchall()
        seg['linked_names'] = [{
            'name_id': r[0], 'name': r[1], 'slug': r[2],
            'match_type': r[3], 'confidence': r[4],
        } for r in linked_names]

        # Get evidence excerpts linked to this segment
        evidence = db.execute("""
            SELECT ee.excerpt_text, ee.matched_alias,
                   ep.term_id, t.canonical_name, t.slug
            FROM evidence_excerpts ee
            JOIN evidence_packets ep ON ee.ev_id = ep.ev_id
            JOIN terms t ON ep.term_id = t.term_id
            WHERE ee.seg_id = ?
            LIMIT 20
        """, (seg_id,)).fetchall()
        seg['evidence_excerpts'] = [{
            'text': r[0][:500], 'matched_alias': r[1],
            'term_id': r[2], 'term_name': r[3], 'term_slug': r[4],
        } for r in evidence]

        # Get neighbor segments
        if seg.get('doc_id') and seg.get('position') is not None:
            neighbors = db.execute("""
                SELECT seg_id, title, position FROM segments
                WHERE doc_id = ? AND position IN (?, ?)
                ORDER BY position
            """, (seg['doc_id'], seg['position'] - 1, seg['position'] + 1)).fetchall()
            seg['neighbors'] = [{'seg_id': r[0], 'title': r[1], 'position': r[2]} for r in neighbors]

        # Get parent document info
        doc = db.execute("""
            SELECT title, doc_type, author, date_display
            FROM documents WHERE doc_id = ?
        """, (seg['doc_id'],)).fetchone()
        if doc:
            seg['document'] = {
                'title': doc[0], 'doc_type': doc[1],
                'author': doc[2], 'date_display': doc[3],
            }

        _write_json(seg_dir / f'{seg_id}.json', seg)
        exported += 1

    print(f"    {exported} segment detail files exported")


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

    # Names
    try:
        rows = db.execute("""
            SELECT name_id, slug, canonical_form, card_description, entity_type, etymology
            FROM names
            WHERE status IN ('accepted', 'provisional', 'unreviewed')
        """).fetchall()
        for row in rows:
            entries.append({
                'type': 'name',
                'id': row[0], 'slug': row[1], 'title': row[2],
                'text': (row[3] or row[5] or '')[:300],
                'category': row[4],
            })
    except sqlite3.OperationalError:
        pass  # names table doesn't exist yet

    _write_json(data_dir / 'search_index.json', entries)
    print(f"    {len(entries)} search entries")


def export_analytics(db: sqlite3.Connection, data_dir: Path):
    """Export precomputed analytics data."""
    print("  Exporting analytics...")

    analytics = {}

    # Term frequency top 30 (exclude non-Exegesis terms like Toso)
    _excluded_terms = {'Toso', 'Indexed', 'Complete'}
    rows = db.execute("""
        SELECT canonical_name, mention_count, primary_category
        FROM terms WHERE status IN ('accepted', 'provisional')
        ORDER BY mention_count DESC LIMIT 60
    """).fetchall()
    analytics['top_terms'] = [
        {'name': r[0], 'count': r[1], 'category': r[2]}
        for r in rows if r[0] not in _excluded_terms
    ][:30]

    # Segments per year
    rows = db.execute("""
        SELECT SUBSTR(date_start, 1, 4) AS year, COUNT(*) AS cnt
        FROM segments
        WHERE date_start IS NOT NULL
        GROUP BY year ORDER BY year
    """).fetchall()
    seg_by_year = {r[0]: r[1] for r in rows}

    # Biography events per year
    bio_rows = db.execute("""
        SELECT SUBSTR(date_start, 1, 4) AS year, COUNT(*) AS cnt
        FROM biography_events
        WHERE date_start IS NOT NULL
        GROUP BY year ORDER BY year
    """).fetchall()
    bio_by_year = {r[0]: r[1] for r in bio_rows}

    # Build full year range (1928-1982 = PKD's lifetime)
    all_years = []
    for y in range(1928, 1983):
        yr = str(y)
        segs = seg_by_year.get(yr, 0)
        bios = bio_by_year.get(yr, 0)
        all_years.append({
            'year': yr,
            'count': segs,
            'bio_events': bios,
            'has_content': segs > 0 or bios > 0,
        })
    analytics['segments_per_year'] = all_years

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

    # Substrate coverage
    try:
        analytics['totals']['segments_with_raw_text'] = db.execute(
            "SELECT COUNT(*) FROM segments WHERE raw_text IS NOT NULL"
        ).fetchone()[0]
        analytics['totals']['segments_with_summary'] = db.execute(
            "SELECT COUNT(*) FROM segments WHERE concise_summary IS NOT NULL"
        ).fetchone()[0]
        analytics['totals']['archive_docs_with_text'] = db.execute(
            "SELECT COUNT(*) FROM document_texts WHERE text_content IS NOT NULL"
        ).fetchone()[0]
        analytics['totals']['evidence_mapped_to_segments'] = db.execute(
            "SELECT COUNT(*) FROM evidence_excerpts WHERE seg_id IS NOT NULL"
        ).fetchone()[0]
        analytics['totals']['term_cooccurrences'] = db.execute(
            "SELECT COUNT(*) FROM term_cooccurrences"
        ).fetchone()[0]

        # Link confidence distribution
        conf_rows = db.execute("""
            SELECT link_confidence, COUNT(*) FROM term_segments
            GROUP BY link_confidence ORDER BY link_confidence
        """).fetchall()
        analytics['link_confidence_dist'] = [
            {'confidence': r[0], 'count': r[1]} for r in conf_rows
        ]
    except sqlite3.OperationalError:
        pass

    # Add names analytics if table exists
    try:
        analytics['totals']['names'] = db.execute("SELECT COUNT(*) FROM names").fetchone()[0]
        rows = db.execute("""
            SELECT entity_type, COUNT(*) FROM names GROUP BY entity_type ORDER BY COUNT(*) DESC
        """).fetchall()
        analytics['names_by_type'] = [{'type': r[0], 'count': r[1]} for r in rows]
        rows = db.execute("""
            SELECT source_type, COUNT(*) FROM names GROUP BY source_type ORDER BY COUNT(*) DESC
        """).fetchall()
        analytics['names_by_source'] = [{'type': r[0] or 'unknown', 'count': r[1]} for r in rows]
    except sqlite3.OperationalError:
        pass

    # Evidentiary lane distribution
    try:
        lane_rows = db.execute("""
            SELECT evidentiary_lane, COUNT(*) FROM documents
            WHERE evidentiary_lane IS NOT NULL
            GROUP BY evidentiary_lane ORDER BY evidentiary_lane
        """).fetchall()
        lane_labels = {'A': 'Fiction', 'B': 'Exegesis', 'C': 'Scholarship', 'D': 'Synthesis', 'E': 'Primary'}
        analytics['evidentiary_lanes'] = [
            {'lane': r[0], 'label': lane_labels.get(r[0], r[0]), 'count': r[1]} for r in lane_rows
        ]
    except sqlite3.OperationalError:
        pass

    # Quality scores
    try:
        total_accepted = db.execute("SELECT COUNT(*) FROM terms WHERE status = 'accepted'").fetchone()[0]
        analytics['quality'] = {
            'terms_accepted': total_accepted,
            'terms_with_evidence': db.execute(
                "SELECT COUNT(DISTINCT t.term_id) FROM terms t JOIN evidence_packets ep ON ep.term_id = t.term_id WHERE t.status = 'accepted'"
            ).fetchone()[0],
            'archive_with_text': db.execute(
                "SELECT COUNT(*) FROM document_texts WHERE text_content IS NOT NULL AND length(text_content) > 100"
            ).fetchone()[0],
            'archive_with_lanes': db.execute(
                "SELECT COUNT(*) FROM documents WHERE evidentiary_lane IS NOT NULL"
            ).fetchone()[0] if 'evidentiary_lane' in [c[1] for c in db.execute("PRAGMA table_info(documents)").fetchall()] else 0,
            'segments_with_works': db.execute(
                "SELECT COUNT(*) FROM segments WHERE works_referenced IS NOT NULL"
            ).fetchone()[0] if 'works_referenced' in [c[1] for c in db.execute("PRAGMA table_info(segments)").fetchall()] else 0,
            'biography_with_location': db.execute(
                "SELECT COUNT(*) FROM biography_events WHERE location IS NOT NULL AND location != ''"
            ).fetchone()[0] if 'location' in [c[1] for c in db.execute("PRAGMA table_info(biography_events)").fetchall()] else 0,
        }
    except Exception:
        pass

    _write_json(data_dir / 'analytics.json', analytics)


def export_biography(db: sqlite3.Connection, data_dir: Path):
    """Export biography events."""
    print("  Exporting biography...")
    bio_dir = data_dir / 'biography'
    ensure_dir(bio_dir)

    bio_cols_info = [c[1] for c in db.execute("PRAGMA table_info(biography_events)").fetchall()]
    has_location = 'location' in bio_cols_info
    loc_col = ", location" if has_location else ""

    rows = db.execute(f"""
        SELECT bio_id, event_type, summary, detail,
               date_start, date_end, date_display, date_confidence,
               source_type, source_name, source_doc_id, source_seg_id,
               contradicted_by, contradiction_note, reliability,
               people_involved, notes{loc_col}
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
        if has_location:
            event['location'] = row[17]
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


def export_names(db: sqlite3.Connection, data_dir: Path):
    """Export names data for the Names tab."""
    print("  Exporting names...")
    names_dir = data_dir / 'names'
    entities_dir = names_dir / 'entities'
    ensure_dir(entities_dir)

    # Check if names table exists
    try:
        db.execute("SELECT 1 FROM names LIMIT 1")
    except sqlite3.OperationalError:
        print("    SKIP: names table not found")
        return

    # Index: all public names
    # Check for segment_mention_count
    name_cols_info = [c[1] for c in db.execute("PRAGMA table_info(names)").fetchall()]
    has_seg_count = 'segment_mention_count' in name_cols_info
    seg_count_col = ", segment_mention_count" if has_seg_count else ""

    rows = db.execute(f"""
        SELECT name_id, canonical_form, slug, entity_type, source_type,
               status, review_state, mention_count, card_description,
               etymology, allusion_type, first_work{seg_count_col}
        FROM names
        WHERE status IN ('accepted', 'provisional', 'unreviewed')
        ORDER BY mention_count DESC
    """).fetchall()

    index = []
    for row in rows:
        entry = {
            'name_id': row[0], 'canonical_form': row[1], 'slug': row[2],
            'entity_type': row[3], 'source_type': row[4],
            'status': row[5], 'review_state': row[6],
            'mention_count': row[7],
            'card_description': (row[8] or '')[:300],
            'etymology': row[9],
            'allusion_type': _parse_json(row[10]),
            'first_work': row[11],
        }
        if has_seg_count:
            entry['segment_mention_count'] = row[12] or 0
        index.append(entry)
    _write_json(names_dir / 'index.json', index)

    # Per-name detail files
    for name_row in index:
        name_id = name_row['name_id']
        slug = name_row['slug']

        # Full name data
        full = db.execute("SELECT * FROM names WHERE name_id = ?", (name_id,)).fetchone()
        cols = [d[0] for d in db.execute("SELECT * FROM names LIMIT 0").description]
        name_data = dict(zip(cols, full))

        # Parse JSON fields
        for field in ['allusion_type', 'work_list']:
            name_data[field] = _parse_json(name_data.get(field))

        # Aliases
        aliases = db.execute("""
            SELECT alias_text, alias_type FROM name_aliases WHERE name_id = ?
        """, (name_id,)).fetchall()
        name_data['aliases'] = [{'text': a[0], 'type': a[1]} for a in aliases]

        # Linked segments (confidence <= 3)
        linked_segs = db.execute("""
            SELECT ns.seg_id, ns.match_type, ns.link_confidence, ns.matched_text,
                   s.date_display, s.concise_summary, s.title
            FROM name_segments ns
            JOIN segments s ON ns.seg_id = s.seg_id
            WHERE ns.name_id = ? AND ns.link_confidence <= 3
            ORDER BY s.date_start
            LIMIT 50
        """, (name_id,)).fetchall()
        name_data['linked_segments'] = [{
            'seg_id': r[0], 'match_type': r[1], 'confidence': r[2],
            'matched_text': r[3], 'date_display': r[4],
            'summary': (r[5] or '')[:200], 'title': r[6],
        } for r in linked_segs]

        # Related terms (via name_terms)
        related_terms = db.execute("""
            SELECT t.canonical_name, t.slug, nt.relation_type, nt.link_confidence
            FROM name_terms nt
            JOIN terms t ON nt.term_id = t.term_id
            WHERE nt.name_id = ?
            ORDER BY nt.link_confidence
        """, (name_id,)).fetchall()
        name_data['related_terms'] = [{
            'name': r[0], 'slug': r[1], 'relation': r[2], 'confidence': r[3],
        } for r in related_terms]

        # Reference match
        if name_data.get('reference_id'):
            ref = db.execute("""
                SELECT canonical_form, domain, brief, etymology, origin_language,
                       significance, source_text
                FROM name_references WHERE ref_id = ?
            """, (name_data['reference_id'],)).fetchone()
            if ref:
                name_data['reference'] = {
                    'canonical_form': ref[0], 'domain': ref[1], 'brief': ref[2],
                    'etymology': ref[3], 'origin_language': ref[4],
                    'significance': ref[5], 'source_text': ref[6],
                }

        _write_json(entities_dir / f'{slug}.json', name_data)

    print(f"    {len(index)} names exported")


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
    export_names(db, data_dir)
    export_segments(db, data_dir)
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
