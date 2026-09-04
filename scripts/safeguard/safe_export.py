#!/usr/bin/env python3
"""
Run an exporter without letting it destroy curated work.

The QueryPat exporters are not safe to run wholesale: several editorial passes
wrote prose directly into `site/public/data`, and their source files are gone,
so a full re-export nulls fields that exist nowhere else. See CLAUDE.md,
"The export is lossy".

This wrapper makes the exporters safe to run anyway:

  1. snapshot `site/public/data`
  2. run the exporter
  3. compare every file, field by field, against the snapshot
  4. classify each change as ADDITIVE, BENIGN or DESTRUCTIVE
  5. restore anything DESTRUCTIVE, unless you explicitly opt in

DESTRUCTIVE means content went away: a file was deleted, a JSON array lost
entries, or a non-empty string/list/dict field became null, empty or shorter
than `--shrink-tolerance` of its previous length. That is exactly the shape of
the damage a full export does.

Usage:
    python scripts/safeguard/safe_export.py --exporter studies
    python scripts/safeguard/safe_export.py --exporter json
    python scripts/safeguard/safe_export.py --exporter all --report-only
    python scripts/safeguard/safe_export.py --exporter json --allow-destructive
"""

import argparse
import json
import subprocess
import sys
import zipfile
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_DIR / 'site' / 'public' / 'data'
sys.path.insert(0, str(PROJECT_DIR / 'scripts'))
sys.path.insert(0, str(PROJECT_DIR / 'scripts' / 'safeguard'))

import snapshot as snap  # noqa: E402

# Post-export passes that must run before the diff, because the committed data
# is the product of export *plus* these. Order matters.
POST_EXPORT_PASSES = [
    'clean_dictionary_claim_leaks',
    'clean_dictionary_junk_descriptions',
    'clean_studies_claim_leaks',
    'clean_segment_wiki_artifacts',
    'rebuild_search_index_terms',
    'fix_dead_links',
]

TEXTLIKE = (str, list, dict)


def run_exporter(which: str):
    import sqlite3
    db_path = PROJECT_DIR / 'database' / 'unified.sqlite'
    if not db_path.exists():
        raise SystemExit(f'Database not found: {db_path}')
    db = sqlite3.connect(str(db_path))
    if which in ('studies', 'all'):
        from studies.export_studies import run as export_studies
        export_studies(db)
    if which in ('json', 'all'):
        from export_json import run as export_json
        export_json(db, PROJECT_DIR)
    db.close()


def run_post_export_passes():
    for name in POST_EXPORT_PASSES:
        script = PROJECT_DIR / 'scripts' / f'{name}.py'
        if not script.exists():
            print(f'  (skipped missing pass: {name})')
            continue
        r = subprocess.run([sys.executable, str(script)], cwd=PROJECT_DIR,
                           capture_output=True, text=True)
        tail = (r.stdout or r.stderr or '').strip().splitlines()
        print(f'  {name}: {tail[-1] if tail else "ok"}')


ID_KEYS = ('term_id', 'topic_id', 'ev_id', 'seg_id', 'doc_id', 'name_id',
           'work_id', 'bio_id', 'passage_id', 'contradiction_id', 'theophany_id',
           'id', 'slug', 'study_id', 'letter_id')


def _key_of(item):
    """Stable identity for a list element, so reordering is not read as loss."""
    if isinstance(item, dict):
        for k in ID_KEYS:
            v = item.get(k)
            if isinstance(v, (str, int)) and str(v):
                return f'{k}={v}'
    return None


def _index_by_key(seq):
    keyed, ok = {}, True
    for it in seq:
        k = _key_of(it)
        if k is None or k in keyed:
            ok = False
            break
        keyed[k] = it
    return (keyed if ok and keyed else None)


def _size(v) -> int:
    if v is None:
        return 0
    if isinstance(v, str):
        return len(v.strip())
    if isinstance(v, (list, dict)):
        return len(v)
    return 1


def compare_json(before, after, shrink_tol: float, path='') -> list[str]:
    """Return human-readable descriptions of destructive changes only."""
    losses = []

    if isinstance(before, dict) and isinstance(after, dict):
        for k, bv in before.items():
            p = f'{path}.{k}' if path else k
            if k not in after:
                if _size(bv):
                    losses.append(f'{p}: field removed')
                continue
            losses.extend(compare_json(bv, after[k], shrink_tol, p))
        return losses

    if isinstance(before, list) and isinstance(after, list):
        b_keyed, a_keyed = _index_by_key(before), _index_by_key(after)
        if b_keyed is not None and a_keyed is not None:
            for k, bv in b_keyed.items():
                if k not in a_keyed:
                    losses.append(f'{path or "[root]"}: entry {k} removed')
                else:
                    losses.extend(compare_json(bv, a_keyed[k], shrink_tol, f'{path}[{k}]'))
            return losses
        if len(after) < len(before):
            losses.append(f'{path or "[root]"}: {len(before)} -> {len(after)} entries')
            return losses
        for i, bv in enumerate(before[:len(after)]):
            losses.extend(compare_json(bv, after[i], shrink_tol, f'{path}[{i}]'))
        return losses

    bs, as_ = _size(before), _size(after)
    if bs and not as_:
        losses.append(f'{path or "[root]"}: emptied ({bs} -> 0)')
    elif isinstance(before, TEXTLIKE) and bs and as_ < bs * shrink_tol:
        losses.append(f'{path or "[root]"}: shrank {bs} -> {as_}')
    return losses


def audit(zip_path: Path, meta: dict, shrink_tol: float):
    """Compare the working tree against the snapshot. Returns (report, restorable)."""
    added, modified, destructive, deleted = [], [], {}, []
    current = snap.manifest_for(DATA_DIR)

    for rel, info in meta['files'].items():
        if rel not in current:
            deleted.append(rel)
            continue
        if current[rel]['sha256'] == info['sha256']:
            continue
        if not rel.endswith('.json'):
            modified.append(rel)
            continue
        with zipfile.ZipFile(zip_path) as zf:
            try:
                before = json.loads(zf.read(f'data/{rel}'))
            except Exception:
                modified.append(rel)
                continue
        try:
            after = json.loads((DATA_DIR / rel).read_text(encoding='utf-8'))
        except Exception:
            destructive[rel] = ['file no longer parses as JSON']
            continue
        losses = compare_json(before, after, shrink_tol)
        (destructive.setdefault(rel, losses) if losses else modified.append(rel))

    for rel in current:
        if rel not in meta['files']:
            added.append(rel)

    return {'added': added, 'modified': modified,
            'destructive': destructive, 'deleted': deleted}


def print_report(rep: dict, limit: int = 12):
    print()
    print(f'  added        {len(rep["added"])}')
    print(f'  modified     {len(rep["modified"])}   (no content lost)')
    print(f'  deleted      {len(rep["deleted"])}')
    print(f'  DESTRUCTIVE  {len(rep["destructive"])}')
    for rel, losses in list(rep['destructive'].items())[:limit]:
        print(f'    {rel}')
        for l in losses[:4]:
            print(f'        {l}')
        if len(losses) > 4:
            print(f'        ... and {len(losses) - 4} more')
    if len(rep['destructive']) > limit:
        print(f'    ... and {len(rep["destructive"]) - limit} more files')
    for rel in rep['deleted'][:limit]:
        print(f'    DELETED {rel}')


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--exporter', choices=['studies', 'json', 'all'], default='studies')
    ap.add_argument('--label', default=None, help='snapshot label')
    ap.add_argument('--skip-post-passes', action='store_true',
                    help='do not run the post-export cleaning passes')
    ap.add_argument('--allow-destructive', action='store_true',
                    help='keep ALL destructive changes instead of restoring them')
    ap.add_argument('--allow-path', action='append', default=[], metavar='PREFIX',
                    help='permit content loss under this path prefix — for a '
                         'deliberate rewrite of one page. Repeatable. Everything '
                         'else is still protected.')
    ap.add_argument('--report-only', action='store_true',
                    help='audit the working tree against the newest snapshot; '
                         'run no exporter')
    ap.add_argument('--shrink-tolerance', type=float, default=0.5,
                    help='a text field shrinking below this fraction of its '
                         'previous length counts as destructive (default 0.5)')
    args = ap.parse_args()

    if args.report_only:
        zips = sorted((PROJECT_DIR / 'archive' / 'snapshots').glob('*.zip'))
        if not zips:
            raise SystemExit('No snapshot to compare against. Run snapshot.py first.')
        zip_path, meta = snap.load_manifest(zips[-1].stem)
        print(f'Auditing working tree against {meta["name"]}')
        print_report(audit(zip_path, meta, args.shrink_tolerance))
        return 0

    label = args.label or f'pre-export-{args.exporter}'
    print(f'1. snapshotting site/public/data ...')
    zip_path = snap.create(label, include_db=True)
    _, meta = snap.load_manifest(zip_path.stem)

    print(f'\n2. running exporter: {args.exporter}')
    run_exporter(args.exporter)

    if not args.skip_post_passes:
        print('\n3. running post-export passes')
        run_post_export_passes()

    print('\n4. auditing what changed')
    rep = audit(zip_path, meta, args.shrink_tolerance)
    print_report(rep)

    allowed = [rel for rel in list(rep['destructive']) + rep['deleted']
               if any(rel.startswith(pfx) for pfx in args.allow_path)]
    lost = [rel for rel in list(rep['destructive']) + rep['deleted']
            if rel not in allowed]
    if allowed:
        print(f'\n  {len(allowed)} file(s) allowed to change by --allow-path:')
        for rel in allowed[:10]:
            print(f'    {rel}')
        print('  (the pre-change state is preserved in the snapshot above)')
    if not lost:
        print('\nNo curated content lost.')
        return 0

    if args.allow_destructive:
        print(f'\n--allow-destructive set: keeping {len(lost)} destructive changes.')
        print(f'Snapshot {meta["name"]} holds the previous state if you need it back.')
        return 0

    print(f'\n5. restoring {len(lost)} file(s) that lost content')
    snap.restore(zip_path.stem, only=lost)
    print('\nDone. Additive and benign changes kept; destructive ones rolled back.')
    print('Re-run with --allow-destructive only if the removals are intended.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
