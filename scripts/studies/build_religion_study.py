#!/usr/bin/env python3
"""
Export the religion study from the relational database to the site.

    python scripts/studies/build_religion_study.py

Reads curation/religion/religion.sqlite (built by build_religion_db.py) and writes:

    site/public/data/studies/religion/index.json                 study index, subsections listed per topic
    site/public/data/studies/religion/topics/<topic>.json        one page per tradition
    site/public/data/studies/religion/findings/<subsection>.json every browsable finding in that subsection
    site/public/data/studies/religion/facets.json                counts for the browse page's filters
    site/public/data/studies/index.json                          the study's row, in place
    site/public/data/search_index.json                           topic rows, in place

What is browsed: lanes A (Dick's own words) and C (scholarship). Lane D
(editorial analysis, including the Exegesis analytic fields) stays in the
database. Those fields paraphrase Dick's own transcribed text, and presenting a
paraphrase as a finding would make the portal's words look like evidence.

The existing study data is preserved: the featured sections and the topic
"Religion in PKD's Fiction" in index.json are kept, and its topic file is not
touched.
"""

import json
import sqlite3
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
DB = PROJECT_DIR / 'curation' / 'religion' / 'religion.sqlite'
OUT = PROJECT_DIR / 'site' / 'public' / 'data' / 'studies' / 'religion'
STUDIES_INDEX = PROJECT_DIR / 'site' / 'public' / 'data' / 'studies' / 'index.json'
SEARCH_INDEX = PROJECT_DIR / 'site' / 'public' / 'data' / 'search_index.json'

STUDY_ID = 'religion'
BROWSE_LANES = ('A', 'C')
CONTEXT_CHARS = 280
PREFIX = 'TOPIC_REL_'

STUDY_LABEL = "Religion in PKD"
STUDY_DESCRIPTION = (
    "Philip K. Dick's engagement with religious traditions across the fiction, the "
    "Exegesis, the correspondence and the criticism: Christianity, Gnosticism, "
    "Zoroastrianism, Judaism and the Torah, Kabbalah, the Logos, Mercerism, "
    "Platonism and Hermeticism, the mystery religions, and the Eastern traditions. "
    "Each tradition is divided into subsections, and every mention in the sources "
    "held here is browsable by subsection, lane, decade, and editorial status."
)


def rows_for(db, sub_id):
    """Browse rows for one subsection, in date order."""
    q = """
        SELECT f.finding_id, f.lane, f.field_class, f.date, f.decade, f.matched_text,
               f.tier, f.context, f.relevance, f.review_status, f.editorial_note,
               src.corpus, src.source_id, src.doc_id, src.title, src.date_display,
               fs.tier AS sub_tier,
               (SELECT group_concat(x.subsection_id, ',') FROM finding_subsections x
                WHERE x.finding_id = f.finding_id) AS subs
        FROM finding_subsections fs
        JOIN findings f USING (finding_id)
        JOIN sources src ON src.source_key = f.source_key
        WHERE fs.subsection_id = ? AND f.lane IN ({lanes})
        ORDER BY f.date IS NULL, f.date, f.finding_id
    """.format(lanes=','.join('?' * len(BROWSE_LANES)))
    out = []
    for r in db.execute(q, (sub_id, *BROWSE_LANES)):
        ctx = r['context']
        if len(ctx) > CONTEXT_CHARS:
            ctx = ctx[:CONTEXT_CHARS].rstrip() + '…'
        row = {
            'id': r['finding_id'],
            'lane': r['lane'],
            'corpus': r['corpus'],
            'src': r['source_id'],
            'title': r['title'],
            'date': r['date'],
            'dd': r['date_display'],
            'decade': r['decade'],
            'm': r['matched_text'],
            'tier': r['sub_tier'],
            'c': ctx,
            'st': r['review_status'],
        }
        row['subs'] = (r['subs'] or '').split(',')
        if r['doc_id']:
            row['doc'] = r['doc_id']
        if r['relevance'] is not None:
            row['rel'] = r['relevance']
        if r['editorial_note']:
            row['n'] = r['editorial_note']
        out.append(row)
    return out


def main():
    if not DB.exists():
        print('ERROR: run build_religion_db.py first.', file=sys.stderr)
        return 1
    db = sqlite3.connect(str(DB))
    db.row_factory = sqlite3.Row

    topics = db.execute('SELECT * FROM topics ORDER BY position').fetchall()
    subs_by_topic = {}
    for s in db.execute('SELECT * FROM subsections ORDER BY position'):
        subs_by_topic.setdefault(s['topic_id'], []).append(s)

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'topics').mkdir(exist_ok=True)
    (OUT / 'findings').mkdir(exist_ok=True)

    facets = {'subsections': {}, 'generated_from': 'curation/religion/religion.sqlite'}
    topic_rows = []
    total_browse = 0

    for t in topics:
        sub_summaries = []
        for s in subs_by_topic.get(t['topic_id'], []):
            rows = rows_for(db, s['subsection_id'])
            total_browse += len(rows)
            (OUT / 'findings' / f"{s['subsection_id']}.json").write_text(
                json.dumps({'subsection_id': s['subsection_id'], 'topic_id': t['topic_id'],
                            'rows': rows}, ensure_ascii=False, separators=(',', ':')),
                encoding='utf-8')

            lanes = {}
            for x in db.execute('SELECT f.lane, COUNT(*) AS n FROM finding_subsections fs '
                                'JOIN findings f USING (finding_id) WHERE fs.subsection_id = ? '
                                'GROUP BY f.lane', (s['subsection_id'],)):
                lanes[x['lane']] = x['n']
            decades = {x['decade']: x['n'] for x in db.execute(
                'SELECT f.decade, COUNT(*) AS n FROM finding_subsections fs '
                'JOIN findings f USING (finding_id) WHERE fs.subsection_id = ? '
                'AND f.lane IN (\'A\',\'C\') AND f.decade IS NOT NULL GROUP BY f.decade',
                (s['subsection_id'],))}
            reviewed = sum(1 for r in rows if r['st'] == 'reviewed')
            excluded = sum(1 for r in rows if r['st'] == 'excluded')
            summary = {
                'subsection_id': s['subsection_id'],
                'label': s['label'],
                'description': s['description'],
                'browse_count': len(rows),
                'lanes': lanes,
                'decades': decades,
                'reviewed': reviewed,
                'excluded': excluded,
            }
            sub_summaries.append(summary)
            facets['subsections'][s['subsection_id']] = {
                'topic_id': t['topic_id'], 'label': s['label'],
                'lanes': lanes, 'decades': decades,
                'reviewed': reviewed, 'excluded': excluded, 'browse_count': len(rows),
            }

        browse_total = sum(x['browse_count'] for x in sub_summaries)
        related = json.loads(t['related'] or '[]')
        topic = {
            'topic_id': PREFIX + t['topic_id'],
            'study_id': STUDY_ID,
            'canonical_name': t['label'],
            'slug': t['topic_id'],
            'status': 'mapped',
            'provenance': 'corpus_sweep_with_editorial_review',
            'definition': t['description'],
            'pkd_relevance': None,
            'in_the_fiction': None,
            'in_the_exegesis': None,
            'intellectual_background': None,
            'scholarly_debate': None,
            'chronology_summary': None,
            'contradictions_summary': None,
            'related_thinkers': [],
            'editorial_notes': ('Every mention is listed by subsection, with its lane, date and '
                                'editorial status. Interpretive prose for this tradition is not '
                                'yet written; see the subsections for the material.'),
            'open_questions': [],
            'passage_count': browse_total,
            'evidence_count': 0,
            'contradiction_count': 0,
            'first_appearance': min((d for x in sub_summaries for d in x['decades']),
                                    default=None),
            'peak_period_start': None,
            'peak_period_end': None,
            'dossier_sections': [],
            'mention_cards': [],
            'mention_groups': None,
            'subsections': sub_summaries,
            'evidence_packets': [],
            'contradictions': [],
            'chronology': [],
            'related_documents': [],
            'related_terms': [],
            'related_names': [],
            'related_topics': [
                {'topic_id': PREFIX + r, 'canonical_name': next(
                    (x['label'] for x in topics if x['topic_id'] == r), r),
                 'slug': r, 'study_id': STUDY_ID}
                for r in related
            ],
        }
        (OUT / 'topics' / f"{t['topic_id']}.json").write_text(
            json.dumps(topic, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        topic_rows.append({
            'topic_id': topic['topic_id'],
            'canonical_name': t['label'],
            'slug': t['topic_id'],
            'status': 'mapped',
            'priority': 0,
            'card_description': t['description'],
            'passage_count': browse_total,
            'evidence_count': 0,
            'contradiction_count': 0,
            'first_appearance': topic['first_appearance'],
            'lane_distribution': {
                lane: sum(x['lanes'].get(lane, 0) for x in sub_summaries) for lane in 'ABCD'},
            'related_topics': [r for r in related],
            'mention_count': browse_total,
            'section_count': 0,
            'subsections': [{'subsection_id': x['subsection_id'], 'label': x['label'],
                             'browse_count': x['browse_count']} for x in sub_summaries],
        })

    (OUT / 'facets.json').write_text(json.dumps(facets, indent=1, ensure_ascii=False) + '\n',
                                     encoding='utf-8')

    # Study index: keep the existing featured sections and existing topics.
    existing = {}
    index_path = OUT / 'index.json'
    if index_path.exists():
        existing = json.loads(index_path.read_text(encoding='utf-8'))
    keep_topics = [t for t in existing.get('topics', [])
                   if not str(t.get('topic_id', '')).startswith(PREFIX)]
    featured = [{
        'title': 'How to browse',
        'body': [
            "Choose a tradition, then a subsection. Each finding shows the sentence it was cut "
            "from, the record it belongs to, its date and its lane. Lane A is Dick's own words; "
            "lane C is scholarship. A finding can belong to several subsections, and its tags "
            "link it to each of them.",
            "Editorial status is shown on every finding. Relevance follows the Burroughs "
            "codes: 1 direct engagement, 2 used as a tool or dramatised, 3 passing mention, "
            "4 thematic parallel, 5 false positive. Unreviewed findings are the sweep's output, "
            "not a judgement.",
        ],
    }]
    featured += [s for s in existing.get('featured_sections', []) if s.get('title') != 'How to browse']
    # The existing label and description are editorial text, so they are kept.
    # The data-loss guard refuses to shorten them; renaming the study is an
    # editor's decision, made by changing them in this file's index by hand.
    label = existing.get('study_label', STUDY_LABEL)
    description = existing.get('study_description', STUDY_DESCRIPTION)
    index = {
        **{k: v for k, v in existing.items() if k not in ('topics', 'featured_sections')},
        'study_id': STUDY_ID,
        'study_label': label,
        'study_description': description,
        'featured_sections': featured,
        'topics': keep_topics + topic_rows,
    }
    index_path.write_text(json.dumps(index, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

    studies = json.loads(STUDIES_INDEX.read_text(encoding='utf-8'))
    all_topics = index['topics']
    row = {
        'study_id': STUDY_ID,
        'study_label': label,
        'study_description': description,
        'topic_count': len(all_topics),
        'published_count': 0,
        'total_passages': sum(t.get('passage_count', 0) for t in all_topics),
        'total_evidence_packets': 0,
        'total_contradictions': 0,
    }
    studies = [s for s in studies if s.get('study_id') != STUDY_ID] + [row]
    studies.sort(key=lambda s: s['study_id'])
    STUDIES_INDEX.write_text(json.dumps(studies, indent=2, ensure_ascii=False) + '\n',
                             encoding='utf-8')

    search = json.loads(SEARCH_INDEX.read_text(encoding='utf-8'))
    search = [r for r in search if not str(r.get('id', '')).startswith(PREFIX)]
    for tr in topic_rows:
        search.append({
            'type': 'study_topic', 'id': tr['topic_id'], 'slug': tr['slug'],
            'title': tr['canonical_name'], 'study_id': STUDY_ID,
            'text': tr['card_description'],
            'route': f"/studies/{STUDY_ID}/{tr['slug']}",
        })
    SEARCH_INDEX.write_text(json.dumps(search, indent=2, ensure_ascii=False) + '\n',
                            encoding='utf-8')

    print(f'wrote {OUT.relative_to(PROJECT_DIR)}')
    print(f'  {len(topic_rows)} topics, {sum(len(v) for v in subs_by_topic.values())} subsections, '
          f'{total_browse} subsection rows (lanes {"/".join(BROWSE_LANES)})')
    return 0


if __name__ == '__main__':
    sys.exit(main())
