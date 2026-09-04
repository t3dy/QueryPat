#!/usr/bin/env python3
"""
Archive the current state of the generated site data (and, optionally, the
curated database tables) before anything is allowed to overwrite it.

Snapshots are content-manifested zips under `archive/snapshots/`. Each one
records the git HEAD it was taken at, so a snapshot can always be tied back to
a commit. `archive/snapshots/INDEX.md` is a committed ledger of every snapshot
ever taken, so the history survives even though the zips themselves are too
large to keep in git.

Usage:
    python scripts/safeguard/snapshot.py --label "before export_json"
    python scripts/safeguard/snapshot.py --label pre-export --include-db
    python scripts/safeguard/snapshot.py --list
    python scripts/safeguard/snapshot.py --restore 20260904T181500Z_pre-export
"""

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_DIR / 'site' / 'public' / 'data'
ARCHIVE_DIR = PROJECT_DIR / 'archive' / 'snapshots'
INDEX_PATH = ARCHIVE_DIR / 'INDEX.md'
DB_PATH = PROJECT_DIR / 'database' / 'unified.sqlite'

# Tables whose contents are editorial rather than derivable by re-running the
# pipeline. Dumped alongside a snapshot when --include-db is passed.
CURATED_TABLES = [
    'terms', 'term_aliases', 'names', 'name_aliases', 'studies', 'study_topics',
    'study_evidence_packets', 'study_contradictions', 'study_passages',
    'study_topic_docs', 'study_topic_terms', 'study_topic_names',
    'evidence_packets', 'theophanies', 'biography_events', 'works',
    'documents', 'annotations',
]


def git(*args) -> str:
    try:
        return subprocess.run(['git', *args], cwd=PROJECT_DIR, capture_output=True,
                              text=True, check=True).stdout.strip()
    except Exception:
        return ''


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()


def manifest_for(root: Path) -> dict:
    files = {}
    for p in sorted(root.rglob('*')):
        if p.is_file():
            files[str(p.relative_to(root)).replace('\\', '/')] = {
                'sha256': file_hash(p), 'bytes': p.stat().st_size,
            }
    return files


def dump_curated_tables(dest: Path) -> int:
    """Write each curated table to newline-delimited JSON. Returns row count."""
    import sqlite3
    if not DB_PATH.exists():
        return 0
    db = sqlite3.connect(str(DB_PATH))
    db.row_factory = sqlite3.Row
    dest.mkdir(parents=True, exist_ok=True)
    total = 0
    for table in CURATED_TABLES:
        try:
            rows = db.execute(f'SELECT * FROM "{table}"').fetchall()
        except Exception:
            continue
        with open(dest / f'{table}.jsonl', 'w', encoding='utf-8') as f:
            for r in rows:
                f.write(json.dumps(dict(r), ensure_ascii=False) + '\n')
        total += len(rows)
    db.close()
    return total


def create(label: str, include_db: bool = False) -> Path:
    if not DATA_DIR.exists():
        raise SystemExit(f'No data directory at {DATA_DIR}')

    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    safe_label = ''.join(ch if ch.isalnum() or ch in '-_' else '-'
                         for ch in (label or 'snapshot'))[:60].strip('-')
    name = f'{stamp}_{safe_label}'
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    files = manifest_for(DATA_DIR)
    meta = {
        'name': name,
        'created_utc': stamp,
        'label': label,
        'git_head': git('rev-parse', 'HEAD'),
        'git_branch': git('rev-parse', '--abbrev-ref', 'HEAD'),
        'git_dirty': bool(git('status', '--porcelain')),
        'data_file_count': len(files),
        'data_bytes': sum(f['bytes'] for f in files.values()),
        'files': files,
    }

    zip_path = ARCHIVE_DIR / f'{name}.zip'
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for rel in files:
            z.write(DATA_DIR / rel, f'data/{rel}')
        if include_db:
            tmp = ARCHIVE_DIR / f'.{name}_db'
            n = dump_curated_tables(tmp)
            meta['curated_rows'] = n
            for p in sorted(tmp.glob('*.jsonl')):
                z.write(p, f'db/{p.name}')
            shutil.rmtree(tmp, ignore_errors=True)
        z.writestr('manifest.json', json.dumps(meta, indent=1, ensure_ascii=False))

    append_index(meta, zip_path)
    print(f'snapshot {name}')
    print(f'  {len(files)} files, {meta["data_bytes"]/1e6:.1f} MB source '
          f'-> {zip_path.stat().st_size/1e6:.1f} MB zip')
    if include_db:
        print(f'  curated db rows: {meta.get("curated_rows", 0)}')
    print(f'  {zip_path}')
    return zip_path


def append_index(meta: dict, zip_path: Path):
    """Keep a committed ledger even though the zips themselves are ignored."""
    if not INDEX_PATH.exists():
        INDEX_PATH.write_text(
            '# Snapshot ledger\n\n'
            'Every snapshot taken of `site/public/data` (and curated DB tables).\n'
            'The zips live beside this file and are git-ignored; this ledger is\n'
            'committed so the history of what was archived, and when, survives.\n\n'
            '| Snapshot | Files | MB | git HEAD | dirty | Label |\n'
            '|---|---|---|---|---|---|\n', encoding='utf-8')
    with open(INDEX_PATH, 'a', encoding='utf-8') as f:
        f.write(f'| `{meta["name"]}` | {meta["data_file_count"]} | '
                f'{zip_path.stat().st_size/1e6:.1f} | '
                f'`{(meta["git_head"] or "?")[:9]}` | '
                f'{"yes" if meta["git_dirty"] else "no"} | {meta["label"]} |\n')


def list_snapshots():
    if not ARCHIVE_DIR.exists():
        print('no snapshots yet')
        return
    zips = sorted(ARCHIVE_DIR.glob('*.zip'))
    if not zips:
        print('no snapshots yet')
        return
    for z in zips:
        with zipfile.ZipFile(z) as zf:
            meta = json.loads(zf.read('manifest.json'))
        print(f'{meta["name"]:<48} {meta["data_file_count"]:>5} files  '
              f'{z.stat().st_size/1e6:>6.1f} MB  {(meta["git_head"] or "?")[:9]}  '
              f'{meta["label"]}')


def load_manifest(name: str) -> tuple[Path, dict]:
    zip_path = ARCHIVE_DIR / (name if name.endswith('.zip') else f'{name}.zip')
    if not zip_path.exists():
        matches = sorted(ARCHIVE_DIR.glob(f'*{name}*.zip'))
        if len(matches) == 1:
            zip_path = matches[0]
        else:
            raise SystemExit(f'No snapshot matching {name!r}'
                             + (f' ({len(matches)} candidates)' if matches else ''))
    with zipfile.ZipFile(zip_path) as zf:
        return zip_path, json.loads(zf.read('manifest.json'))


def restore(name: str, only: list[str] | None = None, dry_run: bool = False):
    zip_path, meta = load_manifest(name)
    with zipfile.ZipFile(zip_path) as zf:
        targets = only if only else list(meta['files'])
        restored = 0
        for rel in targets:
            if rel not in meta['files']:
                print(f'  not in snapshot: {rel}')
                continue
            dest = DATA_DIR / rel
            if dry_run:
                print(f'  would restore {rel}')
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(zf.read(f'data/{rel}'))
            restored += 1
    print(f'{"would restore" if dry_run else "restored"} {restored} files '
          f'from {meta["name"]}')


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--label', default='manual', help='what this snapshot is for')
    ap.add_argument('--include-db', action='store_true',
                    help='also dump curated database tables into the snapshot')
    ap.add_argument('--list', action='store_true', help='list existing snapshots')
    ap.add_argument('--restore', metavar='NAME', help='restore a snapshot in full')
    ap.add_argument('--only', nargs='*', help='with --restore: only these paths')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    if args.list:
        list_snapshots()
    elif args.restore:
        restore(args.restore, args.only, args.dry_run)
    else:
        create(args.label, args.include_db)


if __name__ == '__main__':
    sys.exit(main())
