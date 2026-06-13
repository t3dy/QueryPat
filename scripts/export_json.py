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
import re
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

    def _entry_sort_key(entry):
        if isinstance(entry, dict):
            date_start = entry.get('date_start') or ''
            if entry.get('_type') == 'publication':
                rank = 0
                label = entry.get('canonical_title') or entry.get('slug') or ''
            elif entry.get('_type') == 'biography_event':
                rank = 1
                label = entry.get('summary') or entry.get('bio_id') or ''
            elif entry.get('_type') == 'theophany':
                rank = 2
                label = entry.get('name') or entry.get('theophany_id') or ''
            else:
                rank = 3
                label = entry.get('title') or entry.get('seg_id') or ''
            return (date_start, rank, label)
        return ('', 9, '')

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

    # Load canonical works with publication years
    work_rows = db.execute("""
        SELECT work_id, canonical_title, slug, work_type, category,
               date_start, date_display, card_summary, page_summary,
               source_count, page_count
        FROM works
        WHERE date_start IS NOT NULL
          AND length(date_start) >= 4
          AND substr(date_start, 1, 4) BETWEEN '1928' AND '1982'
        ORDER BY date_start, canonical_title
    """).fetchall()
    pub_years = defaultdict(list)
    for wr in work_rows:
        yr = wr[5][:4] if wr[5] else None
        if not yr:
            continue
        pub_years[yr].append({
            '_type': 'publication',
            'work_id': wr[0],
            'canonical_title': wr[1],
            'slug': wr[2],
            'work_type': wr[3],
            'category': wr[4],
            'date_start': wr[5],
            'date_display': wr[6],
            'summary': wr[7] or wr[8] or '',
            'page_summary': wr[8] or wr[7] or '',
            'source_count': wr[9],
            'page_count': wr[10],
        })

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

    # Merge all years (segments + publications + biography events)
    all_year_keys = sorted(set(years.keys()) | set(pub_years.keys()) | set(bio_years.keys()))

    # Write index with both counts
    index = []
    for y in all_year_keys:
        seg_count = len(years.get(y, []))
        pub_count = len(pub_years.get(y, []))
        bio_count = len(bio_years.get(y, []))
        total = seg_count + pub_count + bio_count
        index.append({
            'year': y,
            'count': seg_count,
            'publications': pub_count,
            'bio_events': bio_count,
            'total': total,
        })
    _write_json(timeline_dir / 'index.json', index)

    # Write per-year files (segments + publications + biography events combined)
    for y in all_year_keys:
        year_data = years.get(y, [])
        if pub_years.get(y):
            year_data = year_data + pub_years[y]
        if bio_years.get(y):
            year_data = year_data + bio_years[y]
        year_data.sort(key=_entry_sort_key)
        _write_json(years_dir / f'{y}.json', year_data)

    print(
        f"    {len(rows)} segments + {len(work_rows)} publications + {len(bio_rows)} bio events across {len(all_year_keys)} years"
    )


def export_dictionary(db: sqlite3.Connection, data_dir: Path):
    """Export dictionary terms."""
    print("  Exporting dictionary...")
    dict_dir = data_dir / 'dictionary'
    terms_dir = dict_dir / 'terms'
    ensure_dir(terms_dir)

    # Index: accepted + provisional terms (summary fields)
    # noise_score and a quick claim-coverage flag let the site grade entries
    # without re-fetching their detail JSON.
    has_noise = 'noise_score' in [
        c[1] for c in db.execute("PRAGMA table_info(terms)").fetchall()
    ]
    has_def_cids = 'definition_claim_ids' in [
        c[1] for c in db.execute("PRAGMA table_info(terms)").fetchall()
    ]
    cols_select = ("term_id, canonical_name, slug, status, review_state, "
                   "primary_category, mention_count, card_description, "
                   "first_appearance, peak_usage_start")
    if has_noise:
        cols_select += ", noise_score"
    if has_def_cids:
        cols_select += (", definition_claim_ids, interpretive_note_claim_ids")
    rows = db.execute(f"""
        SELECT {cols_select}
        FROM terms
        WHERE status IN ('accepted', 'provisional')
        ORDER BY mention_count DESC
    """).fetchall()

    index = []
    for row in rows:
        entry = {
            'term_id': row[0], 'canonical_name': row[1], 'slug': row[2],
            'status': row[3], 'review_state': row[4],
            'primary_category': row[5], 'mention_count': row[6],
            'card_description': (row[7] or '')[:300],  # truncate for index
            'first_appearance': row[8], 'peak_usage_start': row[9],
        }
        idx = 10
        if has_noise:
            entry['noise_score'] = row[idx]
            idx += 1
        if has_def_cids:
            def_cids = _parse_json(row[idx]); idx += 1
            int_cids = _parse_json(row[idx]); idx += 1
            entry['claim_backed'] = bool(
                (def_cids and len(def_cids) > 0)
                or (int_cids and len(int_cids) > 0)
            )
        index.append(entry)
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

        # Parse new prose-provenance arrays (added by claim_ir migration).
        prose_fields = ['definition', 'interpretive_note',
                        'visionary_significance', 'scholarly_caution',
                        'card_description', 'full_description']
        all_cited_ids: set[str] = set()
        for pf in prose_fields:
            cid_col = f'{pf}_claim_ids'
            if cid_col in term_data:
                arr = _parse_json(term_data.get(cid_col))
                term_data[cid_col] = arr or []
                if arr:
                    all_cited_ids.update(arr)

        # Embed cited-claim metadata so the site can render citation popovers
        # without a separate fetch. Keys are claim_ids; values are minimal
        # display-shape records.
        cited_claims = {}
        if all_cited_ids:
            placeholders = ",".join("?" * len(all_cited_ids))
            for r in db.execute(
                f"""SELECT c.claim_id, c.claim_text, c.claim_type, c.lane,
                           c.polarity, c.speaker, c.confidence,
                           c.source_type, c.source_id,
                           c.char_start, c.char_end, c.doc_id,
                           d.title AS doc_title, d.slug AS doc_slug,
                           COALESCE(d.date_display, d.date_start) AS date
                    FROM claims c JOIN documents d ON c.doc_id = d.doc_id
                    WHERE c.claim_id IN ({placeholders})""",
                tuple(all_cited_ids),
            ):
                cited_claims[r[0]] = {
                    'claim_id':   r[0],
                    'claim_text': r[1],
                    'claim_type': r[2],
                    'lane':       r[3],
                    'polarity':   r[4],
                    'speaker':    r[5],
                    'confidence': r[6],
                    'source_type': r[7],
                    'source_id':   r[8],
                    'char_start':  r[9],
                    'char_end':    r[10],
                    'doc_id':      r[11],
                    'doc_title':   r[12],
                    'doc_slug':    r[13],
                    'date':        r[14],
                }
        term_data['cited_claims'] = cited_claims

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

        if not term_data['linked_segments']:
            term_data['linked_segments'] = [{
                'seg_id': None,
                'match_type': 'unlinked',
                'confidence': None,
                'date_display': None,
                'summary': 'No public segment link has been promoted for this term yet.',
                'title': 'Unlinked term evidence',
            }]
        if not term_data['related_terms']:
            term_data['related_terms'] = [{
                'name': term_data.get('canonical_name') or slug,
                'slug': slug,
                'relation': 'self',
                'confidence': 5,
            }]

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

    work_aliases = _load_work_aliases(db)
    term_aliases = _load_term_aliases(db)

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
            'date_display': _display_date(row[6]), 'date_start': row[7],
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
        detail['page_summary'] = _fallback_page_summary(
            title=row[1],
            doc_type=row[4],
            category=row[5],
            author=row[3],
            card_summary=row[9],
            page_summary=row[10],
        )
        topics = doc_topics.get(row[0], {})
        detail['people_mentioned'] = _unique_list(topics.get('person', []))
        if row[3]:
            detail['people_mentioned'] = _unique_list([*detail['people_mentioned'], row[3]])
        elif row[8]:
            detail['people_mentioned'] = _unique_list([*detail['people_mentioned'], 'Philip K. Dick'])
        detail['works_discussed'] = _unique_list(
            topics.get('work', []) or _infer_labels_from_text(
                [row[1], row[9], row[10]],
                work_aliases,
                limit=8,
            )
        )
        if not detail['works_discussed']:
            detail['works_discussed'] = ['Philip K. Dick'] if not row[8] else [row[1]]
        detail['linked_terms'] = _unique_list(
            topics.get('term', []) or _infer_labels_from_text(
                [row[1], row[9], row[10]],
                term_aliases,
                limit=12,
            )
        )
        if not detail['linked_terms']:
            detail['linked_terms'] = [_category_label(row[5] or row[4])]

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
    pub_rows = db.execute("""
        SELECT SUBSTR(date_start, 1, 4) AS year, COUNT(*) AS cnt
        FROM works
        WHERE date_start IS NOT NULL
          AND length(date_start) >= 4
          AND substr(date_start, 1, 4) BETWEEN '1928' AND '1982'
        GROUP BY year ORDER BY year
    """).fetchall()
    pub_by_year = {r[0]: r[1] for r in pub_rows}

    all_years = []
    for y in range(1928, 1983):
        yr = str(y)
        segs = seg_by_year.get(yr, 0)
        bios = bio_by_year.get(yr, 0)
        pubs = pub_by_year.get(yr, 0)
        all_years.append({
            'year': yr,
            'count': segs,
            'bio_events': bios,
            'publications': pubs,
            'has_content': segs > 0 or bios > 0 or pubs > 0,
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

        if not name_data.get('full_description'):
            name_data['full_description'] = _build_name_full_description(name_data)
        if not name_data.get('linked_segments'):
            name_data['linked_segments'] = []
        if not name_data.get('related_terms'):
            name_data['related_terms'] = _fallback_related_terms(name_data)

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


def _display_date(value):
    if value and str(value).strip().lower() != 'unknown':
        return value
    return 'Undated'


def _category_label(value):
    label = clean = str(value or 'archive document').replace('_', ' ').replace('&', 'and').strip()
    return label.title() if clean else 'Archive Document'


def _unique_list(items):
    out = []
    seen = set()
    for item in items or []:
        if not item:
            continue
        label = str(item).strip()
        key = label.lower()
        if label and key not in seen:
            out.append(label)
            seen.add(key)
    return out


def _slug_label(text):
    return re.sub(r"[^a-z0-9]+", " ", (text or "").lower()).strip()


def _load_work_aliases(db):
    try:
        rows = db.execute("""
            SELECT canonical_title, slug
            FROM works
            WHERE canonical_title IS NOT NULL
            ORDER BY length(canonical_title) DESC
        """).fetchall()
    except sqlite3.OperationalError:
        return []
    aliases = []
    for title, slug in rows:
        candidates = {title, (slug or '').replace('-', ' ')}
        if title and title.lower().startswith(('the ', 'a ', 'an ')):
            candidates.add(re.sub(r'^(the|a|an)\s+', '', title, flags=re.I))
        for candidate in candidates:
            normalized = _slug_label(candidate)
            if normalized and len(normalized) > 3:
                aliases.append((title, normalized))
    return aliases


def _load_term_aliases(db):
    try:
        rows = db.execute("""
            SELECT canonical_name, slug
            FROM terms
            WHERE status IN ('accepted', 'provisional')
            ORDER BY mention_count DESC
        """).fetchall()
    except sqlite3.OperationalError:
        return []
    aliases = []
    for name, slug in rows:
        normalized = _slug_label(name or (slug or '').replace('-', ' '))
        if normalized and len(normalized) > 3:
            aliases.append((name, normalized))
    return aliases


def _infer_labels_from_text(parts, aliases, limit):
    haystack = _slug_label(' '.join(str(part or '') for part in parts))
    if not haystack:
        return []
    labels = []
    seen = set()
    for label, alias in aliases:
        if len(labels) >= limit:
            break
        if not alias or label.lower() in seen:
            continue
        if re.search(rf"(?<![a-z0-9]){re.escape(alias)}(?![a-z0-9])", haystack):
            labels.append(label)
            seen.add(label.lower())
    return labels


def _fallback_page_summary(title, doc_type, category, author, card_summary, page_summary):
    if page_summary and str(page_summary).strip() and str(page_summary).strip().lower() != 'full summary pending.':
        return page_summary
    if card_summary and str(card_summary).strip():
        return card_summary
    kind = (category or doc_type or 'archive document').replace('_', ' ')
    author_clause = f" by {author}" if author else ""
    return (
        f"{title} is cataloged as a {kind}{author_clause}. "
        "This generated summary preserves the archive record while the document awaits a fuller reading pass."
    )


def _entity_type_label(value):
    return {
        'character': 'fictional character',
        'deity_figure': 'divine or mythological figure',
        'historical_person': 'historical figure',
        'place': 'place',
        'organization': 'organization',
        'other': 'named entity',
    }.get(value or '', 'named entity')


def _build_name_full_description(name_data):
    canonical = name_data.get('canonical_form') or 'This name'
    desc = name_data.get('card_description') or ''
    parts = [desc] if desc else [
        f"{canonical} is a {_entity_type_label(name_data.get('entity_type'))} in the QueryPat names index."
    ]
    mentions = name_data.get('mention_count') or 0
    if mentions:
        parts.append(
            f"The entry currently has {mentions} indexed mention"
            f"{'s' if mentions != 1 else ''}, so it is useful for tracing where the name recurs across the corpus."
        )
    aliases = [a.get('text') for a in name_data.get('aliases') or [] if a.get('text')]
    if aliases:
        parts.append(f"Recorded aliases or related forms include {', '.join(aliases[:8])}.")
    linked = name_data.get('linked_segments') or []
    if linked:
        summaries = [seg.get('summary') for seg in linked[:3] if seg.get('summary')]
        if summaries:
            parts.append("Representative segment contexts: " + " ".join(summaries))
    related = name_data.get('related_terms') or []
    if related:
        terms = [item.get('name') for item in related[:8] if item.get('name')]
        if terms:
            parts.append(f"Related dictionary terms include {', '.join(terms)}.")
    return "\n\n".join(part.strip() for part in parts if part and part.strip())


def _fallback_related_terms(name_data):
    related = []
    canonical = (name_data.get('canonical_form') or '').strip()
    slug = (name_data.get('slug') or '').strip()
    for label, term_slug in ((canonical, slug),):
        if label and term_slug:
            related.append({
                'name': label,
                'slug': term_slug,
                'relation': 'same_label',
                'confidence': 5,
            })
    return related


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
    export_pkd_on_pkd(db, data_dir)
    export_studies(db, data_dir)
    export_scenes_json(db, data_dir)

    print("  Export complete")


def export_studies(db: sqlite3.Connection, data_dir: Path):
    """Export study JSON bundles (delegates to studies/export_studies.py)."""
    print("  Exporting studies...")
    try:
        from studies.export_studies import run as export_studies_run
        export_studies_run(db)
    except ImportError as e:
        print(f"    SKIP: studies export not available ({e})")
    except Exception as e:
        print(f"    ERROR: studies export failed ({e})")


def export_scenes_json(db: sqlite3.Connection, data_dir: Path):
    """Export scene JSON bundles (delegates to studies/export_scenes.py)."""
    print("  Exporting scenes...")
    try:
        from studies.export_scenes import run as export_scenes_run
        export_scenes_run(db)
    except ImportError as e:
        print(f"    SKIP: scenes export not available ({e})")
    except Exception as e:
        print(f"    ERROR: scenes export failed ({e})")


def export_pkd_on_pkd(db: sqlite3.Connection, data_dir: Path):
    """Export the PKD on PKD novel-mention catalog."""
    print("  Exporting PKD on PKD...")
    try:
        from build_pkd_on_pkd import run as build_pkd_on_pkd
        build_pkd_on_pkd(db, seed_db=True)
    except ImportError as e:
        print(f"    SKIP: PKD on PKD export not available ({e})")
    except Exception as e:
        print(f"    ERROR: PKD on PKD export failed ({e})")


if __name__ == '__main__':
    db_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('C:/QueryPat/database/unified.sqlite')
    project_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('C:/QueryPat')
    db = sqlite3.connect(str(db_path))
    run(db, project_dir)
    db.close()
