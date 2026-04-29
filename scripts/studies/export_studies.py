#!/usr/bin/env python3
"""
Stage 5d: Export study data to JSON for the static site viewer.

Produces:
  site/public/data/studies/index.json
  site/public/data/studies/{study_id}/index.json
  site/public/data/studies/{study_id}/topics/{slug}.json

Follows the frozen contracts in STUDY_JSON_CONTRACTS.md.

Usage:
    python scripts/studies/export_studies.py
    python scripts/studies/export_studies.py --db database/unified.sqlite
"""

import json
import sqlite3
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

PROJECT_DIR = SCRIPTS_DIR.parent
DEFAULT_DB = PROJECT_DIR / 'database' / 'unified.sqlite'
OUTPUT_DIR = PROJECT_DIR / 'site' / 'public' / 'data' / 'studies'


def safe_json(val):
    """Parse a JSON string field, return empty list/None if invalid."""
    if not val:
        return []
    try:
        return json.loads(val)
    except (json.JSONDecodeError, TypeError):
        return []


def export_studies_index(db: sqlite3.Connection, out_dir: Path):
    """Export studies/index.json."""
    studies = db.execute("""
        SELECT study_id, study_label, study_description, topic_count
        FROM studies ORDER BY study_id
    """).fetchall()

    index = []
    for sid, label, desc, tc in studies:
        stats = db.execute("""
            SELECT
                COUNT(*) FILTER (WHERE status IN ('drafted', 'reviewed', 'published')),
                COALESCE(SUM(passage_count), 0),
                COALESCE(SUM(evidence_count), 0),
                COALESCE(SUM(contradiction_count), 0)
            FROM study_topics WHERE study_id = ?
        """, (sid,)).fetchone()

        # SQLite may not support FILTER — fallback
        if stats is None or stats[0] is None:
            pub = db.execute("""
                SELECT COUNT(*) FROM study_topics
                WHERE study_id = ? AND status IN ('drafted','reviewed','published')
            """, (sid,)).fetchone()[0]
            tp = db.execute("""
                SELECT COALESCE(SUM(passage_count),0) FROM study_topics WHERE study_id = ?
            """, (sid,)).fetchone()[0]
            te = db.execute("""
                SELECT COALESCE(SUM(evidence_count),0) FROM study_topics WHERE study_id = ?
            """, (sid,)).fetchone()[0]
            tco = db.execute("""
                SELECT COALESCE(SUM(contradiction_count),0) FROM study_topics WHERE study_id = ?
            """, (sid,)).fetchone()[0]
        else:
            pub, tp, te, tco = stats

        index.append({
            'study_id': sid,
            'study_label': label,
            'study_description': desc,
            'topic_count': tc,
            'published_count': pub,
            'total_passages': tp,
            'total_evidence_packets': te,
            'total_contradictions': tco,
        })

    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / 'index.json', 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    print(f"    studies/index.json ({len(index)} studies)")


def export_study_index(db: sqlite3.Connection, study_id: str, out_dir: Path):
    """Export studies/{study_id}/index.json."""
    study = db.execute("""
        SELECT study_id, study_label, study_description
        FROM studies WHERE study_id = ?
    """, (study_id,)).fetchone()

    topics = db.execute("""
        SELECT topic_id, canonical_name, slug, status, priority,
               card_description, passage_count, evidence_count,
               contradiction_count, first_appearance, related_topics
        FROM study_topics
        WHERE study_id = ? AND passage_count > 0
        ORDER BY priority DESC, passage_count DESC
    """, (study_id,)).fetchall()

    topic_list = []
    for row in topics:
        (tid, name, slug, status, priority, card_desc, pc, ec, cc,
         first_app, rel_topics) = row

        # Lane distribution
        lanes = db.execute("""
            SELECT lane, COUNT(*) FROM study_passages
            WHERE topic_id = ? GROUP BY lane
        """, (tid,)).fetchall()
        lane_dist = {l: c for l, c in lanes}

        topic_list.append({
            'topic_id': tid,
            'canonical_name': name,
            'slug': slug,
            'status': status,
            'priority': priority,
            'card_description': card_desc,
            'passage_count': pc,
            'evidence_count': ec,
            'contradiction_count': cc,
            'first_appearance': first_app,
            'lane_distribution': lane_dist,
            'related_topics': safe_json(rel_topics),
        })

    study_dir = out_dir / study_id
    study_dir.mkdir(parents=True, exist_ok=True)

    result = {
        'study_id': study[0],
        'study_label': study[1],
        'study_description': study[2],
        'topics': topic_list,
    }

    with open(study_dir / 'index.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"    studies/{study_id}/index.json ({len(topic_list)} topics)")


def export_topic_detail(db: sqlite3.Connection, topic_id: str,
                         study_id: str, slug: str, out_dir: Path):
    """Export studies/{study_id}/topics/{slug}.json."""
    topic = db.execute("""
        SELECT topic_id, study_id, canonical_name, slug, status,
               definition, pkd_relevance, in_the_fiction, in_the_exegesis,
               intellectual_background, scholarly_debate,
               chronology_summary, contradictions_summary,
               related_thinkers, editorial_notes, open_questions,
               passage_count, evidence_count, contradiction_count,
               first_appearance, peak_period_start, peak_period_end
        FROM study_topics WHERE topic_id = ?
    """, (topic_id,)).fetchone()

    if not topic:
        return

    # Evidence packets with nested passages
    ev_packets = []
    evs = db.execute("""
        SELECT ev_id, claim_text, evidence_summary, confidence,
               source_method, lane_a_count, lane_b_count, lane_c_count
        FROM study_evidence_packets WHERE topic_id = ?
    """, (topic_id,)).fetchall()

    for ev in evs:
        ev_id = ev[0]
        # Get passages linked to this evidence packet (via topic for now)
        passages = db.execute("""
            SELECT sp.passage_id, sp.lane, sp.source_mode, sp.doc_id,
                   d.title, sp.passage_text, sp.matched_terms,
                   sp.claim_type, sp.confidence
            FROM study_passages sp
            LEFT JOIN documents d ON sp.doc_id = d.doc_id
            WHERE sp.topic_id = ?
            ORDER BY sp.lane, sp.char_offset_start
            LIMIT 20
        """, (topic_id,)).fetchall()

        passage_list = [{
            'passage_id': p[0], 'lane': p[1], 'source_mode': p[2],
            'doc_id': p[3], 'doc_title': p[4],
            'passage_text': (p[5] or '')[:500],
            'matched_terms': safe_json(p[6]),
            'claim_type': p[7], 'confidence': p[8],
        } for p in passages]

        ev_packets.append({
            'ev_id': ev_id, 'claim_text': ev[1],
            'evidence_summary': ev[2], 'confidence': ev[3],
            'source_method': ev[4],
            'lane_a_count': ev[5], 'lane_b_count': ev[6], 'lane_c_count': ev[7],
            'passages': passage_list,
        })

    # If no evidence packets yet, export raw passages grouped by lane
    if not ev_packets:
        passages = db.execute("""
            SELECT sp.passage_id, sp.lane, sp.source_mode, sp.doc_id,
                   d.title, sp.passage_text, sp.matched_terms,
                   sp.claim_type, sp.confidence
            FROM study_passages sp
            LEFT JOIN documents d ON sp.doc_id = d.doc_id
            WHERE sp.topic_id = ?
            ORDER BY sp.lane, sp.char_offset_start
        """, (topic_id,)).fetchall()

        passage_list = [{
            'passage_id': p[0], 'lane': p[1], 'source_mode': p[2],
            'doc_id': p[3], 'doc_title': p[4],
            'passage_text': (p[5] or '')[:500],
            'matched_terms': safe_json(p[6]),
            'claim_type': p[7], 'confidence': p[8],
        } for p in passages]

        # Create a synthetic evidence packet from raw passages
        lane_counts = {}
        for p in passage_list:
            lane_counts[p['lane']] = lane_counts.get(p['lane'], 0) + 1

        ev_packets = [{
            'ev_id': f'SEV_RAW_{topic_id}',
            'claim_text': None,
            'evidence_summary': None,
            'confidence': None,
            'source_method': 'deterministic',
            'lane_a_count': lane_counts.get('A', 0),
            'lane_b_count': lane_counts.get('B', 0),
            'lane_c_count': lane_counts.get('C', 0),
            'passages': passage_list,
        }]

    # Contradictions
    contras = db.execute("""
        SELECT sc.contradiction_id, sc.summary, sc.explanation,
               sc.contradiction_type,
               sc.passage_id_a, sc.passage_id_b
        FROM study_contradictions sc
        WHERE sc.topic_id = ?
    """, (topic_id,)).fetchall()

    contradiction_list = []
    for c in contras:
        pa = db.execute("""
            SELECT sp.passage_id, sp.lane, d.title, sp.passage_text, sp.source_mode
            FROM study_passages sp
            LEFT JOIN documents d ON sp.doc_id = d.doc_id
            WHERE sp.passage_id = ?
        """, (c[4],)).fetchone()
        pb = db.execute("""
            SELECT sp.passage_id, sp.lane, d.title, sp.passage_text, sp.source_mode
            FROM study_passages sp
            LEFT JOIN documents d ON sp.doc_id = d.doc_id
            WHERE sp.passage_id = ?
        """, (c[5],)).fetchone()

        contradiction_list.append({
            'contradiction_id': c[0],
            'summary': c[1], 'explanation': c[2],
            'contradiction_type': c[3],
            'passage_a': {
                'passage_id': pa[0], 'lane': pa[1], 'doc_title': pa[2],
                'passage_text': (pa[3] or '')[:500], 'source_mode': pa[4],
            } if pa else None,
            'passage_b': {
                'passage_id': pb[0], 'lane': pb[1], 'doc_title': pb[2],
                'passage_text': (pb[3] or '')[:500], 'source_mode': pb[4],
            } if pb else None,
        })

    # Chronology (from passage dates via document dates)
    chrono = db.execute("""
        SELECT DISTINCT d.date_start, d.title, d.doc_type, d.doc_id, d.slug
        FROM study_passages sp
        JOIN documents d ON sp.doc_id = d.doc_id
        WHERE sp.topic_id = ? AND d.date_start IS NOT NULL
        ORDER BY d.date_start
    """, (topic_id,)).fetchall()

    chronology = [{
        'year': c[0][:4] if c[0] else None,
        'date': c[0],
        'doc_title': c[1],
        'event_type': c[2],
        'doc_id': c[3],
        'doc_slug': c[4],
    } for c in chrono]

    # Related documents
    rel_docs = db.execute("""
        SELECT std.doc_id, d.title, d.doc_type, std.relevance,
               std.passage_count, d.slug
        FROM study_topic_docs std
        JOIN documents d ON std.doc_id = d.doc_id
        WHERE std.topic_id = ?
        ORDER BY std.passage_count DESC
    """, (topic_id,)).fetchall()

    related_documents = [{
        'doc_id': r[0], 'title': r[1], 'doc_type': r[2],
        'relevance': r[3], 'passage_count': r[4], 'slug': r[5],
    } for r in rel_docs]

    # Related terms
    rel_terms = db.execute("""
        SELECT stt.term_id, t.canonical_name, t.slug, stt.relation_type
        FROM study_topic_terms stt
        JOIN terms t ON stt.term_id = t.term_id
        WHERE stt.topic_id = ?
    """, (topic_id,)).fetchall()

    related_terms = [{
        'term_id': r[0], 'canonical_name': r[1],
        'slug': r[2], 'relation_type': r[3],
    } for r in rel_terms]

    # Related names
    rel_names = db.execute("""
        SELECT stn.name_id, n.canonical_form, n.slug, stn.relation_type
        FROM study_topic_names stn
        JOIN names n ON stn.name_id = n.name_id
        WHERE stn.topic_id = ?
    """, (topic_id,)).fetchall()

    related_names = [{
        'name_id': r[0], 'display_name': r[1],
        'slug': r[2], 'relation_type': r[3],
    } for r in rel_names]

    # Related topics (same study)
    rel_topic_slugs = safe_json(topic[13]) if topic[13] else []
    related_topics = []
    for rslug in rel_topic_slugs:
        rt = db.execute("""
            SELECT topic_id, canonical_name, slug, study_id
            FROM study_topics WHERE slug = ? AND study_id = ?
        """, (rslug, study_id)).fetchone()
        if rt:
            related_topics.append({
                'topic_id': rt[0], 'canonical_name': rt[1],
                'slug': rt[2], 'study_id': rt[3],
            })

    # Assemble
    detail = {
        'topic_id': topic[0],
        'study_id': topic[1],
        'canonical_name': topic[2],
        'slug': topic[3],
        'status': topic[4],

        'definition': topic[5],
        'pkd_relevance': topic[6],
        'in_the_fiction': topic[7],
        'in_the_exegesis': topic[8],
        'intellectual_background': topic[9],
        'scholarly_debate': topic[10],
        'chronology_summary': topic[11],
        'contradictions_summary': topic[12],
        'related_thinkers': safe_json(topic[13]),
        'editorial_notes': topic[14],
        'open_questions': safe_json(topic[15]),

        'passage_count': topic[16],
        'evidence_count': topic[17],
        'contradiction_count': topic[18],
        'first_appearance': topic[19],
        'peak_period_start': topic[20],
        'peak_period_end': topic[21],

        'evidence_packets': ev_packets,
        'contradictions': contradiction_list,
        'chronology': chronology,
        'related_documents': related_documents,
        'related_terms': related_terms,
        'related_names': related_names,
        'related_topics': related_topics,
    }

    topics_dir = out_dir / study_id / 'topics'
    topics_dir.mkdir(parents=True, exist_ok=True)

    with open(topics_dir / f'{slug}.json', 'w', encoding='utf-8') as f:
        json.dump(detail, f, indent=2, ensure_ascii=False)


def run(db: sqlite3.Connection, _source: Path = None):
    """Export all study JSON files."""
    print("  Exporting study JSON...")

    export_studies_index(db, OUTPUT_DIR)

    studies = db.execute("SELECT study_id FROM studies").fetchall()
    for (sid,) in studies:
        export_study_index(db, sid, OUTPUT_DIR)

        # Export each topic with passages
        topics = db.execute("""
            SELECT topic_id, slug FROM study_topics
            WHERE study_id = ? AND passage_count > 0
        """, (sid,)).fetchall()

        for tid, slug in topics:
            export_topic_detail(db, tid, sid, slug, OUTPUT_DIR)

        print(f"    studies/{sid}/topics/ ({len(topics)} topic files)")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Export study JSON')
    parser.add_argument('--db', type=Path, default=DEFAULT_DB)
    args = parser.parse_args()

    db = sqlite3.connect(str(args.db))
    db.execute("PRAGMA foreign_keys = ON")
    run(db)
    db.close()
    print("Done.")
