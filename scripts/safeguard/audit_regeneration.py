#!/usr/bin/env python3
"""
Answer the question "what would a full regeneration destroy?" — without
destroying anything.

Runs every exporter into a throwaway directory, then compares the result to the
live `site/public/data`. Any field that is present and populated in the live
tree but absent or empty in the freshly generated one is *orphaned editorial
content*: it exists only in the exported JSON, and a real export would delete
it.

This is a read-only audit. It never writes to site/public/data.

Usage:
    python scripts/safeguard/audit_regeneration.py
    python scripts/safeguard/audit_regeneration.py --write-report
    python scripts/safeguard/audit_regeneration.py --keep-temp
"""

import argparse
import json
import shutil
import sys
import tempfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_DIR / 'site' / 'public' / 'data'
DB_PATH = PROJECT_DIR / 'database' / 'unified.sqlite'
sys.path.insert(0, str(PROJECT_DIR / 'scripts'))


def generate_into(tmp_data: Path):
    """Run every exporter with its output redirected into tmp_data."""
    import sqlite3
    db = sqlite3.connect(str(DB_PATH))

    # studies/export_studies and studies/export_scenes hardcode their output
    # directory, so redirect them by patching the module constant.
    import studies.export_studies as es
    real_studies_out = es.OUTPUT_DIR
    es.OUTPUT_DIR = tmp_data / 'studies'

    import export_json as ej
    # Neutralise the delegating wrappers so they cannot touch the live tree;
    # studies are generated explicitly below, into the temp directory.
    real_studies_wrapper = ej.export_studies
    real_scenes_wrapper = ej.export_scenes_json
    ej.export_studies = lambda db_, data_dir: None
    ej.export_scenes_json = lambda db_, data_dir: None

    tmp_project = tmp_data.parent.parent.parent  # <tmp>/site/public/data -> <tmp>
    try:
        ej.run(db, tmp_project)
        es.run(db)
    finally:
        es.OUTPUT_DIR = real_studies_out
        ej.export_studies = real_studies_wrapper
        ej.export_scenes_json = real_scenes_wrapper
        db.close()


def populated(v) -> bool:
    if v is None:
        return False
    if isinstance(v, str):
        return bool(v.strip())
    if isinstance(v, (list, dict)):
        return len(v) > 0
    return True


def walk(live, fresh, path, losses, depth=0):
    """Record every populated live value that the fresh export lacks."""
    if depth > 8:
        return
    if isinstance(live, dict):
        if not isinstance(fresh, dict):
            if populated(live):
                losses.append((path, 'object replaced by non-object'))
            return
        for k, lv in live.items():
            p = f'{path}.{k}' if path else k
            if k not in fresh:
                if populated(lv):
                    losses.append((p, 'field absent from regenerated output'))
            else:
                walk(lv, fresh[k], p, losses, depth + 1)
        return
    if isinstance(live, list):
        if not isinstance(fresh, list):
            if live:
                losses.append((path, 'array replaced by non-array'))
            return
        if len(fresh) < len(live):
            losses.append((path, f'array shrinks {len(live)} -> {len(fresh)}'))
        for i, lv in enumerate(live[:min(len(fresh), 40)]):
            walk(lv, fresh[i], f'{path}[]', losses, depth + 1)
        return
    if populated(live) and not populated(fresh):
        losses.append((path, 'value emptied'))
    elif isinstance(live, str) and isinstance(fresh, str) \
            and len(live.strip()) > 80 and len(fresh.strip()) < len(live.strip()) * 0.5:
        losses.append((path, f'text shrinks {len(live.strip())} -> {len(fresh.strip())}'))


def normalise_field(path: str) -> str:
    """Collapse array indices so many rows aggregate into one finding."""
    return path.replace('[]', '[]')


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--write-report', action='store_true',
                    help='write docs/PRESERVATION_AUDIT_DATA.md')
    ap.add_argument('--keep-temp', action='store_true')
    args = ap.parse_args()

    if not DB_PATH.exists():
        raise SystemExit(f'Database not found: {DB_PATH}')

    tmp_root = Path(tempfile.mkdtemp(prefix='querypat_audit_'))
    tmp_data = tmp_root / 'site' / 'public' / 'data'
    tmp_data.mkdir(parents=True, exist_ok=True)
    print(f'Generating a throwaway export into {tmp_root}')
    try:
        generate_into(tmp_data)

        live_files = {str(p.relative_to(DATA_DIR)).replace('\\', '/')
                      for p in DATA_DIR.rglob('*.json')}
        fresh_files = {str(p.relative_to(tmp_data)).replace('\\', '/')
                       for p in tmp_data.rglob('*.json')}

        missing = sorted(live_files - fresh_files)
        gained = sorted(fresh_files - live_files)

        by_field = defaultdict(lambda: {'count': 0, 'examples': []})
        files_with_loss = {}

        for rel in sorted(live_files & fresh_files):
            try:
                live = json.loads((DATA_DIR / rel).read_text(encoding='utf-8'))
                fresh = json.loads((tmp_data / rel).read_text(encoding='utf-8'))
            except Exception:
                continue
            losses = []
            walk(live, fresh, '', losses)
            if losses:
                files_with_loss[rel] = losses
                for p, kind in losses:
                    top = rel.split('/')[0]
                    key = f'{top}:{normalise_field(p)}  ({kind})'
                    e = by_field[key]
                    e['count'] += 1
                    if len(e['examples']) < 3:
                        e['examples'].append(rel)

        print()
        print(f'  live JSON files                 {len(live_files)}')
        print(f'  regenerated JSON files          {len(fresh_files)}')
        print(f'  files a regeneration would NOT produce at all   {len(missing)}')
        print(f'  files that would LOSE content   {len(files_with_loss)}')
        print(f'  distinct orphaned field paths   {len(by_field)}')
        print()
        print('  Orphaned editorial fields (exist only in the exported JSON):')
        for key, e in sorted(by_field.items(), key=lambda x: -x[1]['count'])[:30]:
            print(f'    {e["count"]:>5}x  {key}')
            print(f'            e.g. {e["examples"][0]}')
        if missing:
            print()
            print('  Files that no exporter produces (orphaned entirely):')
            for m in missing[:20]:
                print(f'    {m}')
            if len(missing) > 20:
                print(f'    ... and {len(missing) - 20} more')

        if args.write_report:
            write_report(by_field, files_with_loss, missing, gained,
                         len(live_files), len(fresh_files))
    finally:
        if not args.keep_temp:
            shutil.rmtree(tmp_root, ignore_errors=True)
        else:
            print(f'\nTemp export kept at {tmp_root}')
    return 0


def write_report(by_field, files_with_loss, missing, gained, n_live, n_fresh):
    out = PROJECT_DIR / 'docs' / 'PRESERVATION_AUDIT_DATA.md'
    out.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    lines = [
        '# Regeneration loss audit (machine-generated)',
        '',
        f'Generated {ts} by `scripts/safeguard/audit_regeneration.py`.',
        '',
        'Every exporter was run into a throwaway directory and the result compared',
        'to the live `site/public/data`. Anything listed here is populated in the',
        'committed tree and absent or impoverished in a fresh export — that is,',
        'editorial content with no source in the database.',
        '',
        '## Totals',
        '',
        f'- live JSON files: **{n_live}**',
        f'- regenerated JSON files: **{n_fresh}**',
        f'- files a regeneration would not produce at all: **{len(missing)}**',
        f'- files that would lose content: **{len(files_with_loss)}**',
        f'- distinct orphaned field paths: **{len(by_field)}**',
        '',
        '## Orphaned editorial fields',
        '',
        '| Files affected | Field path | Example |',
        '|---:|---|---|',
    ]
    for key, e in sorted(by_field.items(), key=lambda x: -x[1]['count']):
        field, _, kind = key.partition('  (')
        lines.append(f'| {e["count"]} | `{field}` — {kind.rstrip(")")} | `{e["examples"][0]}` |')
    if missing:
        lines += ['', '## Files no exporter produces', '']
        lines += [f'- `{m}`' for m in missing[:200]]
    if gained:
        lines += ['', '## Files only a fresh export produces', '']
        lines += [f'- `{g}`' for g in gained[:60]]
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'\n  wrote {out.relative_to(PROJECT_DIR)}')


if __name__ == '__main__':
    sys.exit(main())
