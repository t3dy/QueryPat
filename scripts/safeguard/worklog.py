#!/usr/bin/env python3
"""
Create and archive research worklog entries.

Convention: docs/RESEARCH_WORKLOG.md

Usage:
    python scripts/safeguard/worklog.py new "burroughs corpus sweep"
    python scripts/safeguard/worklog.py archive-draft site/public/data/studies/.../x.json
    python scripts/safeguard/worklog.py list
"""

import argparse
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
ARCHIVE = PROJECT_DIR / 'archive'

TEMPLATE = """# {title}

- **Date:** {date}
- **Session:** {session}
- **Status:** in progress

## Research question

## Instruction

<!-- the brief that started this, or a link to archive/{day}/prompts/ -->

## Corpus searched

<!-- which tables, columns, files, formats. Say what you did NOT search. -->

## Queries

## Documents examined

## Discoveries

<!-- Mark each with its register: A = PKD's own words, B = primary-source fact,
     C = scholarly argument, D = portal-editor inference. -->

## Interpretations

## Contradictions and alternatives

## Unresolved questions

## Decisions

<!-- what was chosen, what was rejected, and why -->

## Files changed

## Validation

## Artifacts archived
"""


def day_dir(day: str | None = None) -> Path:
    d = day or datetime.now(timezone.utc).strftime('%Y-%m-%d')
    return ARCHIVE / d


def slugify(text: str) -> str:
    out = ''.join(ch.lower() if ch.isalnum() else '-' for ch in text)
    while '--' in out:
        out = out.replace('--', '-')
    return out.strip('-')[:60] or 'entry'


def cmd_new(title: str, session: str):
    d = day_dir() / 'worklog'
    d.mkdir(parents=True, exist_ok=True)
    n = len(list(d.glob('*.md'))) + 1
    path = d / f'{n:02d}-{slugify(title)}.md'
    if path.exists():
        print(f'Already exists: {path}')
        return 1
    path.write_text(TEMPLATE.format(
        title=title,
        date=datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC'),
        session=session or 'unspecified',
        day=day_dir().name,
    ), encoding='utf-8')
    for sub in ('prompts', 'research', 'drafts', 'reports'):
        (day_dir() / sub).mkdir(parents=True, exist_ok=True)
    print(path.relative_to(PROJECT_DIR))
    return 0


def cmd_archive_draft(paths: list[str], note: str):
    d = day_dir() / 'drafts'
    d.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime('%H%M%SZ')
    for raw in paths:
        src = Path(raw)
        if not src.is_absolute():
            src = PROJECT_DIR / raw
        if not src.exists():
            print(f'  missing: {raw}')
            continue
        base = src.name
        existing = len(list(d.glob(f'{Path(base).stem}.v*')))
        dest = d / f'{Path(base).stem}.v{existing + 1}.{stamp}{src.suffix}'
        shutil.copy2(src, dest)
        print(f'  archived {raw} -> {dest.relative_to(PROJECT_DIR)}')
        if note:
            (d / f'{dest.stem}.note.txt').write_text(note + '\n', encoding='utf-8')
    return 0


def cmd_list():
    if not ARCHIVE.exists():
        print('no archive yet')
        return 0
    for day in sorted(p for p in ARCHIVE.iterdir() if p.is_dir() and p.name[0].isdigit()):
        entries = sorted((day / 'worklog').glob('*.md')) if (day / 'worklog').exists() else []
        counts = {sub: len(list((day / sub).glob('*')))
                  for sub in ('research', 'drafts', 'prompts', 'reports')
                  if (day / sub).exists()}
        print(f'{day.name}  worklog={len(entries)}  ' +
              '  '.join(f'{k}={v}' for k, v in counts.items()))
        for e in entries:
            first = e.read_text(encoding='utf-8').splitlines()[0].lstrip('# ')
            print(f'    {e.name}  {first}')
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)

    p_new = sub.add_parser('new', help='start a worklog entry')
    p_new.add_argument('title')
    p_new.add_argument('--session', default='', help='agent/session identifier')

    p_arch = sub.add_parser('archive-draft', help='archive a file before replacing it')
    p_arch.add_argument('paths', nargs='+')
    p_arch.add_argument('--note', default='', help='why it is being replaced')

    sub.add_parser('list', help='list archived sessions')

    args = ap.parse_args()
    if args.cmd == 'new':
        return cmd_new(args.title, args.session)
    if args.cmd == 'archive-draft':
        return cmd_archive_draft(args.paths, args.note)
    return cmd_list()


if __name__ == '__main__':
    sys.exit(main())
