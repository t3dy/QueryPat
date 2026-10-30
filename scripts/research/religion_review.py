#!/usr/bin/env python3
"""
Review religion findings: list them, and record an editorial decision on each.

    python scripts/research/religion_review.py summary
    python scripts/research/religion_review.py next --subsection sophia --limit 10
    python scripts/research/religion_review.py next --subsection sophia --lane A --unreviewed
    python scripts/research/religion_review.py decide REL_1a2b3c... --relevance 1 --note "..."
    python scripts/research/religion_review.py decide REL_1a2b3c... --status excluded --relevance 5
    python scripts/research/religion_review.py show REL_1a2b3c...

Decisions are written to curation/religion/editorial.json, keyed by finding id.
That file is the durable record and is committed. The database is rebuilt from it
by build_religion_db.py, so a decision survives every re-sweep that leaves the
text unchanged (finding ids are hashes of corpus, record, field, offset and match).

Relevance codes match curation/bible and curation/burroughs-word-virus:
    1 direct engagement   2 used as a tool, or dramatised   3 passing mention
    4 thematic parallel   5 false positive
"""

import argparse
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
CUR = PROJECT_DIR / 'curation' / 'religion'
DB = CUR / 'religion.sqlite'
EDITORIAL = CUR / 'editorial.json'


def connect():
    if not DB.exists():
        print('ERROR: no database. Run build_religion_db.py first.', file=sys.stderr)
        sys.exit(1)
    db = sqlite3.connect(str(DB))
    db.row_factory = sqlite3.Row
    return db


def cmd_summary(db, args):
    rows = db.execute("""
        SELECT s.topic_id, s.subsection_id, s.label,
               COUNT(DISTINCT f.finding_id) AS total,
               SUM(f.review_status = 'reviewed') AS reviewed,
               SUM(f.review_status = 'excluded') AS excluded,
               SUM(f.relevance = 1) AS r1, SUM(f.relevance = 2) AS r2
        FROM subsections s
        LEFT JOIN finding_subsections fs ON fs.subsection_id = s.subsection_id
        LEFT JOIN findings f ON f.finding_id = fs.finding_id AND f.lane IN ('A', 'C')
        GROUP BY s.subsection_id ORDER BY s.topic_id, s.position
    """).fetchall()
    print(f"{'subsection':<22}{'A+C':>7}{'reviewed':>10}{'excluded':>10}{'rel 1':>7}{'rel 2':>7}")
    for r in rows:
        print(f"{r['subsection_id']:<22}{r['total'] or 0:>7}{r['reviewed'] or 0:>10}"
              f"{r['excluded'] or 0:>10}{r['r1'] or 0:>7}{r['r2'] or 0:>7}")


def cmd_next(db, args):
    where, params = ['fs.subsection_id = ?'], [args.subsection]
    if args.lane:
        where.append('f.lane = ?')
        params.append(args.lane)
    else:
        where.append("f.lane IN ('A', 'C')")
    if args.unreviewed:
        where.append("f.review_status = 'unreviewed'")
    if args.strong_only:
        where.append("fs.tier = 'strong'")
    rows = db.execute(f"""
        SELECT f.finding_id, f.lane, f.date, f.matched_text, f.context, f.relevance,
               f.review_status, src.title, src.source_id
        FROM finding_subsections fs
        JOIN findings f USING (finding_id)
        JOIN sources src ON src.source_key = f.source_key
        WHERE {' AND '.join(where)}
        ORDER BY f.date, f.finding_id LIMIT ?""", (*params, args.limit)).fetchall()
    for r in rows:
        print(f"{r['finding_id']}  [{r['lane']}] {r['date'] or '----'}  {r['title']}  "
              f"({r['source_id']})")
        print(f"    match: {r['matched_text']!r}  status: {r['review_status']}"
              + (f"  relevance: {r['relevance']}" if r['relevance'] else ''))
        print(f"    {r['context'][:300]}")
    if not rows:
        print('No findings match.')


def cmd_show(db, args):
    r = db.execute("""
        SELECT f.*, src.title, src.source_id, src.corpus,
               (SELECT group_concat(subsection_id, ', ') FROM finding_subsections
                WHERE finding_id = f.finding_id) AS subs
        FROM findings f JOIN sources src ON src.source_key = f.source_key
        WHERE f.finding_id = ?""", (args.finding_id,)).fetchone()
    if r is None:
        print('No such finding.', file=sys.stderr)
        return 1
    for k in ('finding_id', 'corpus', 'source_id', 'title', 'date', 'lane', 'field',
              'matched_text', 'subs', 'tier', 'relevance', 'review_status', 'editorial_note'):
        print(f'{k:>15}: {r[k]}')
    print(f"{'context':>15}: {r['context']}")
    return 0


def cmd_decide(db, args):
    if args.relevance is not None and args.relevance not in (1, 2, 3, 4, 5):
        print('relevance must be 1 to 5', file=sys.stderr)
        return 2
    exists = db.execute('SELECT 1 FROM findings WHERE finding_id = ?', (args.finding_id,)).fetchone()
    if exists is None:
        print(f'No such finding: {args.finding_id}', file=sys.stderr)
        return 1
    decisions = json.loads(EDITORIAL.read_text(encoding='utf-8')) if EDITORIAL.exists() else {}
    prev = decisions.get(args.finding_id, {})
    status = args.status or 'reviewed'
    decisions[args.finding_id] = {
        **prev,
        'relevance': args.relevance if args.relevance is not None else prev.get('relevance'),
        'status': status,
        'note': args.note if args.note is not None else prev.get('note'),
        'reviewer': args.reviewer,
        'reviewed_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'),
    }
    EDITORIAL.write_text(json.dumps(decisions, indent=2, ensure_ascii=False, sort_keys=True) + '\n',
                         encoding='utf-8')
    print(f"recorded {args.finding_id}: relevance {decisions[args.finding_id]['relevance']}, "
          f"status {status}. Rebuild with build_religion_db.py.")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)

    sub.add_parser('summary')

    p = sub.add_parser('next')
    p.add_argument('--subsection', required=True)
    p.add_argument('--lane', choices=['A', 'B', 'C', 'D'])
    p.add_argument('--limit', type=int, default=10)
    p.add_argument('--unreviewed', action='store_true')
    p.add_argument('--strong-only', action='store_true')

    p = sub.add_parser('show')
    p.add_argument('finding_id')

    p = sub.add_parser('decide')
    p.add_argument('finding_id')
    p.add_argument('--relevance', type=int)
    p.add_argument('--status', choices=['reviewed', 'excluded'])
    p.add_argument('--note')
    p.add_argument('--reviewer', default='editor')

    args = ap.parse_args()
    db = connect()
    handler = {'summary': cmd_summary, 'next': cmd_next, 'show': cmd_show,
               'decide': cmd_decide}[args.cmd]
    return handler(db, args) or 0


if __name__ == '__main__':
    sys.exit(main())
