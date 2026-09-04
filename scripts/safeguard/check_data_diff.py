#!/usr/bin/env python3
"""
Block a commit that would remove scholarship from `site/public/data`.

Compares what is staged (or the working tree) against git HEAD and reports any
change where content went *away*: a file deleted, a JSON array shortened, a
populated field emptied, or a long text field cut in half. Additions and
genuine edits pass; only losses are flagged.

Also enforces two content invariants that the post-export cleaning passes exist
to maintain, and that a raw export breaks:

  * no `CLM_*` claim ids in reader-facing prose
  * no JSON file that fails to parse

Exit codes: 0 clean, 1 loss detected, 2 usage/environment error.

Usage:
    python scripts/safeguard/check_data_diff.py              # staged vs HEAD
    python scripts/safeguard/check_data_diff.py --worktree   # working tree vs HEAD
    python scripts/safeguard/check_data_diff.py --install-hook
"""

import argparse
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PREFIX = 'site/public/data/'

# Reader-facing fields that must never contain internal claim ids.
PUBLIC_PROSE_FIELDS = {
    'definition', 'interpretive_note', 'visionary_significance',
    'scholarly_caution', 'card_description', 'full_description',
    'pkd_relevance', 'in_the_fiction', 'in_the_exegesis',
    'intellectual_background', 'scholarly_debate', 'chronology_summary',
    'contradictions_summary', 'editorial_notes', 'summary', 'description',
    'page_summary', 'card_summary', 'concise_summary',
}

SHRINK_TOLERANCE = 0.5
BYPASS_FILE = PROJECT_DIR / '.allow-data-loss'


def git(*args, binary=False):
    r = subprocess.run(['git', *args], cwd=PROJECT_DIR,
                       capture_output=True, check=False)
    if r.returncode != 0:
        return None
    return r.stdout if binary else r.stdout.decode('utf-8', 'replace')


def changed_data_files(staged: bool) -> list[str]:
    args = ['diff', '--name-status', '--diff-filter=MDR']
    if staged:
        args.append('--cached')
    args += ['HEAD', '--', DATA_PREFIX]
    out = git(*args)
    if out is None:
        return []
    files = []
    for line in out.splitlines():
        parts = line.split('\t')
        if len(parts) >= 2:
            files.append((parts[0][0], parts[-1]))
    return files


def head_blob(path: str):
    return git('show', f'HEAD:{path}', binary=True)


def working_bytes(path: str, staged: bool):
    if staged:
        return git('show', f':{path}', binary=True)
    p = PROJECT_DIR / path
    return p.read_bytes() if p.exists() else None


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


def find_losses(before, after, path='') -> list[str]:
    out = []
    if isinstance(before, dict) and isinstance(after, dict):
        for k, bv in before.items():
            p = f'{path}.{k}' if path else k
            if k not in after:
                if _size(bv):
                    out.append(f'{p}: field removed')
            else:
                out.extend(find_losses(bv, after[k], p))
        return out
    if isinstance(before, list) and isinstance(after, list):
        # Match elements by identity where possible, so inserting or reordering
        # entries is not mistaken for content loss.
        b_keyed, a_keyed = _index_by_key(before), _index_by_key(after)
        if b_keyed is not None and a_keyed is not None:
            for k, bv in b_keyed.items():
                if k not in a_keyed:
                    out.append(f'{path or "[root]"}: entry {k} removed')
                else:
                    out.extend(find_losses(bv, a_keyed[k], f'{path}[{k}]'))
            return out
        if len(after) < len(before):
            out.append(f'{path or "[root]"}: {len(before)} -> {len(after)} entries')
            return out
        for i, bv in enumerate(before[:len(after)]):
            out.extend(find_losses(bv, after[i], f'{path}[{i}]'))
        return out
    bs, as_ = _size(before), _size(after)
    if bs and not as_:
        out.append(f'{path or "[root]"}: emptied ({bs} -> 0)')
    elif isinstance(before, str) and isinstance(after, str) and bs and as_ < bs:
        # Long fields: flag a big proportional cut. Short fields (titles, authors,
        # dates, slugs) lose meaning in a few characters, so flag any truncation
        # where the new value is a prefix or substring of the old one.
        if bs > 80:
            if as_ < bs * SHRINK_TOLERANCE:
                out.append(f'{path or "[root]"}: text {bs} -> {as_} chars')
        elif after.strip() and after.strip() in before.strip():
            out.append(f'{path or "[root]"}: truncated {before.strip()!r} '
                       f'-> {after.strip()!r}')
    return out


def find_clm_leaks(obj, path='') -> list[str]:
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f'{path}.{k}' if path else k
            if k in PUBLIC_PROSE_FIELDS and isinstance(v, str) and 'CLM_' in v:
                out.append(p)
            else:
                out.extend(find_clm_leaks(v, p))
    elif isinstance(obj, list):
        for i, v in enumerate(obj[:200]):
            out.extend(find_clm_leaks(v, f'{path}[{i}]'))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--worktree', action='store_true',
                    help='check the working tree instead of the index')
    ap.add_argument('--install-hook', action='store_true')
    ap.add_argument('--quiet', action='store_true')
    args = ap.parse_args()

    if args.install_hook:
        return install_hook()

    if BYPASS_FILE.exists():
        print(f'check_data_diff: {BYPASS_FILE.name} present — data-loss check '
              f'DISABLED for this commit.')
        return 0

    staged = not args.worktree
    changes = changed_data_files(staged)
    if not changes:
        if not args.quiet:
            print('check_data_diff: no changes under site/public/data')
        return 0

    deleted, losing, leaking, unparseable = [], {}, {}, []

    for status, path in changes:
        if status == 'D':
            deleted.append(path)
            continue
        before_raw, after_raw = head_blob(path), working_bytes(path, staged)
        if before_raw is None or after_raw is None:
            continue
        if not path.endswith('.json'):
            continue
        try:
            before = json.loads(before_raw.decode('utf-8'))
        except Exception:
            before = None
        try:
            after = json.loads(after_raw.decode('utf-8'))
        except Exception:
            unparseable.append(path)
            continue
        leaks = find_clm_leaks(after)
        if leaks:
            leaking[path] = leaks
        if before is not None:
            losses = find_losses(before, after)
            if losses:
                losing[path] = losses

    problems = bool(deleted or losing or leaking or unparseable)
    if not problems:
        if not args.quiet:
            print(f'check_data_diff: {len(changes)} data file(s) changed, '
                  f'no content lost.')
        return 0

    print()
    print('=' * 72)
    print(' REFUSING: this change removes content from site/public/data')
    print('=' * 72)
    if deleted:
        print(f'\n {len(deleted)} file(s) DELETED:')
        for p in deleted[:15]:
            print(f'   {p}')
        if len(deleted) > 15:
            print(f'   ... and {len(deleted) - 15} more')
    if unparseable:
        print(f'\n {len(unparseable)} file(s) no longer parse as JSON:')
        for p in unparseable[:15]:
            print(f'   {p}')
    if losing:
        print(f'\n {len(losing)} file(s) LOSE content:')
        for p, losses in list(losing.items())[:12]:
            print(f'   {p}')
            for l in losses[:3]:
                print(f'       {l}')
            if len(losses) > 3:
                print(f'       ... and {len(losses) - 3} more')
        if len(losing) > 12:
            print(f'   ... and {len(losing) - 12} more files')
    if leaking:
        print(f'\n {len(leaking)} file(s) leak internal CLM_ ids into public prose:')
        for p, fields in list(leaking.items())[:12]:
            print(f'   {p}  ({", ".join(fields[:3])})')
        print('   fix: python scripts/clean_dictionary_claim_leaks.py'
              ' && python scripts/clean_studies_claim_leaks.py')

    print("""
 site/public/data holds editorial work that exists nowhere else — see
 docs/PRESERVATION_AUDIT.md. Losing it is almost never intended.

 If this was an accidental regeneration:
     python scripts/safeguard/safe_export.py --report-only
     git checkout -- site/public/data          # discard, then re-apply your edits

 If the removal really is intended:
     touch .allow-data-loss     # one commit, then delete the file
     or: git commit --no-verify
""")
    return 1


HOOK = """#!/bin/sh
# QueryPat: refuse commits that remove scholarship from site/public/data.
# Installed by scripts/safeguard/check_data_diff.py --install-hook
exec python scripts/safeguard/check_data_diff.py --quiet
"""


def install_hook():
    hooks = PROJECT_DIR / '.git' / 'hooks'
    if not hooks.exists():
        print('No .git/hooks directory — is this a git repository?')
        return 2
    path = hooks / 'pre-commit'
    if path.exists():
        existing = path.read_text(encoding='utf-8', errors='replace')
        if 'check_data_diff' in existing:
            print(f'Hook already installed at {path}')
            return 0
        backup = hooks / 'pre-commit.before-querypat'
        backup.write_text(existing, encoding='utf-8')
        print(f'Existing hook backed up to {backup.name}')
    path.write_text(HOOK, encoding='utf-8')
    path.chmod(path.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    print(f'Installed pre-commit hook: {path}')
    print('Bypass for one commit with `.allow-data-loss` or `git commit --no-verify`.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
