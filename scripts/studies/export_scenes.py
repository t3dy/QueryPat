"""
Export ai_scenes to JSON for the static site viewer.

Produces:
    site/public/data/scenes/index.json
    site/public/data/scenes/scenes/{scene_id}.json

Called from export_json.py or standalone.
"""

import json
import sqlite3
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = PROJECT_DIR / 'site' / 'public' / 'data' / 'scenes'


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def export_scenes_index(db: sqlite3.Connection, out_dir: Path):
    """Export scenes/index.json with scene list, interaction types, and work list."""
    scenes = db.execute("""
        SELECT s.scene_id, s.scene_label, s.work_title,
               s.interaction_type, s.interaction_type_secondary,
               s.short_summary, s.editorial_status
        FROM ai_scenes s
        ORDER BY s.work_title, s.char_offset_start
    """).fetchall()

    # Build scene summaries with participant info
    scene_list = []
    for row in scenes:
        sid = row[0]
        participants = db.execute("""
            SELECT participant_label, participant_role
            FROM ai_scene_participants
            WHERE scene_id = ?
        """, (sid,)).fetchall()

        scene_list.append({
            'scene_id': sid,
            'scene_label': row[1],
            'work_title': row[2],
            'interaction_type': row[3],
            'interaction_type_secondary': row[4],
            'participant_count': len(participants),
            'participant_labels': [p[0] for p in participants],
            'short_summary': row[5],
            'editorial_status': row[6],
        })

    # Interaction types with counts
    types = db.execute("""
        SELECT t.type_slug, t.type_label, t.type_description, t.sort_order,
               COUNT(s.scene_id) as scene_count
        FROM ai_interaction_types t
        LEFT JOIN ai_scenes s ON s.interaction_type = t.type_slug
        GROUP BY t.type_slug
        ORDER BY t.sort_order
    """).fetchall()

    type_list = [{
        'type_slug': t[0],
        'type_label': t[1],
        'type_description': t[2],
        'scene_count': t[4],
    } for t in types]

    # Works with counts
    works = db.execute("""
        SELECT work_id, work_title, COUNT(*) as scene_count
        FROM ai_scenes
        GROUP BY work_id, work_title
        ORDER BY scene_count DESC
    """).fetchall()

    work_list = [{
        'work_id': w[0],
        'work_title': w[1],
        'scene_count': w[2],
    } for w in works]

    index = {
        'total_scenes': len(scene_list),
        'scenes': scene_list,
        'interaction_types': type_list,
        'works': work_list,
    }

    ensure_dir(out_dir)
    with open(out_dir / 'index.json', 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    print(f"    scenes/index.json ({len(scene_list)} scenes)")


def export_scene_detail(db: sqlite3.Connection, scene_id: str, out_dir: Path):
    """Export a single scene detail JSON."""
    row = db.execute("""
        SELECT s.scene_id, s.scene_label, s.work_id, s.work_title, s.doc_id,
               s.page_start, s.page_end, s.char_offset_start, s.char_offset_end,
               s.interaction_type, s.interaction_type_secondary,
               s.short_summary, s.significance, s.source_excerpt,
               s.editorial_status
        FROM ai_scenes s
        WHERE s.scene_id = ?
    """, (scene_id,)).fetchone()

    if not row:
        return

    # Interaction type labels
    type_label = db.execute(
        "SELECT type_label FROM ai_interaction_types WHERE type_slug = ?",
        (row[9],)
    ).fetchone()

    sec_label = None
    if row[10]:
        sec_row = db.execute(
            "SELECT type_label FROM ai_interaction_types WHERE type_slug = ?",
            (row[10],)
        ).fetchone()
        if sec_row:
            sec_label = sec_row[0]

    # Participants with name cross-links
    participants = db.execute("""
        SELECT p.participant_label, p.participant_role, p.name_id, n.slug
        FROM ai_scene_participants p
        LEFT JOIN names n ON p.name_id = n.name_id
        WHERE p.scene_id = ?
    """, (scene_id,)).fetchall()

    participant_list = [{
        'label': p[0],
        'role': p[1],
        'name_id': p[2],
        'name_slug': p[3],
    } for p in participants]

    # Related AI topics
    topics = db.execute("""
        SELECT st.topic_id, st.canonical_name, st.slug, st.study_id, ast.relevance
        FROM ai_scene_topics ast
        JOIN study_topics st ON ast.topic_id = st.topic_id
        WHERE ast.scene_id = ?
        ORDER BY ast.relevance, st.canonical_name
    """, (scene_id,)).fetchall()

    topic_list = [{
        'topic_id': t[0],
        'canonical_name': t[1],
        'slug': t[2],
        'study_id': t[3],
        'relevance': t[4],
    } for t in topics]

    detail = {
        'scene_id': row[0],
        'scene_label': row[1],
        'work_id': row[2],
        'work_title': row[3],
        'doc_id': row[4],
        'page_start': row[5],
        'page_end': row[6],
        'interaction_type': row[9],
        'interaction_type_label': type_label[0] if type_label else row[9],
        'interaction_type_secondary': row[10],
        'interaction_type_secondary_label': sec_label,
        'short_summary': row[11],
        'significance': row[12],
        'source_excerpt': row[13],
        'participants': participant_list,
        'related_topics': topic_list,
        'editorial_status': row[14],
    }

    scenes_dir = out_dir / 'scenes'
    ensure_dir(scenes_dir)
    with open(scenes_dir / f'{scene_id}.json', 'w', encoding='utf-8') as f:
        json.dump(detail, f, indent=2, ensure_ascii=False)


def run(db: sqlite3.Connection, _source: Path = None):
    """Export all scene JSON files."""
    print("  Exporting scene JSON...")

    export_scenes_index(db, OUTPUT_DIR)

    scene_ids = db.execute("SELECT scene_id FROM ai_scenes").fetchall()
    for (sid,) in scene_ids:
        export_scene_detail(db, sid, OUTPUT_DIR)

    print(f"    scenes/scenes/ ({len(scene_ids)} scene files)")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Export scene JSON')
    parser.add_argument('--db', type=Path, default=DEFAULT_DB)
    args = parser.parse_args()

    db = sqlite3.connect(str(args.db))
    db.execute("PRAGMA foreign_keys = ON")
    run(db)
    db.close()
