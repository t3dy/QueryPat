#!/usr/bin/env python3
"""
Apply the biography curation modules in curation/biography/ to
site/public/data/biography/curated.json.

curated.json is hand-curated: no exporter writes it, so this script and the
other scripts in scripts/biography/ are how it changes. Each module under
curation/biography/ defines

    CORRECTIONS  {event_id: {field: value}}   fields set on an existing event;
                                              `links` is merged, not replaced
    APPEND       {event_id: {path: [items]}}  items added to a list on an existing
                                              event, if not already there; `path`
                                              may be dotted ('dispute.positions')
    REPLACE      {event_id: {field: (old, new)}}  replace one passage of a text
                                              field; skipped once `new` is there,
                                              refused if neither is
    AMEND        {event_id: {list: [(match, set), ...]}}  set fields on the one
                                              list item whose fields equal `match`
                                              (e.g. a wrong source locator);
                                              skipped once applied, refused if no
                                              item or several items match
    NEW_EVENTS   [event, ...]                 appended if the id is absent

Prefer APPEND to CORRECTIONS for sources, quotes and dispute positions: a
replaced list drops whatever the earlier curator put there, and the pre-commit
guard (scripts/safeguard/check_data_diff.py) will refuse it.

Idempotent: running it twice changes nothing the second time. Existing event
order is kept; new events are inserted before the first later-dated event.
Refuses to run if a correction names an id that does not exist.

Usage:
    python scripts/biography/apply_biography_curation.py            # all modules
    python scripts/biography/apply_biography_curation.py drug_years # one module
    python scripts/biography/apply_biography_curation.py --check    # report only
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
CURATED_PATH = PROJECT_DIR / 'site' / 'public' / 'data' / 'biography' / 'curated.json'
CURATION_DIR = PROJECT_DIR / 'curation' / 'biography'


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def merge_links(old: dict | None, new: dict) -> dict:
    out = dict(old or {})
    for key, val in new.items():
        if isinstance(val, list):
            have = list(out.get(key) or [])
            for item in val:
                if item not in have:
                    have.append(item)
            out[key] = have
        else:
            out[key] = val
    return out


def apply(events: list, mod) -> tuple[int, int]:
    by_id = {e['id']: e for e in events}
    named = (list(getattr(mod, 'CORRECTIONS', {})) + list(getattr(mod, 'APPEND', {}))
             + list(getattr(mod, 'REPLACE', {})) + list(getattr(mod, 'AMEND', {})))
    missing = [i for i in named if i not in by_id]
    if missing:
        raise SystemExit(f'[error] {mod.__name__}: corrections for unknown ids: {missing}')

    changed = 0
    for event_id, fields in getattr(mod, 'CORRECTIONS', {}).items():
        ev = by_id[event_id]
        for key, val in fields.items():
            new = merge_links(ev.get('links'), val) if key == 'links' else val
            if ev.get(key) != new:
                ev[key] = new
                changed += 1

    for event_id, fields in getattr(mod, 'REPLACE', {}).items():
        for key, (old, new) in fields.items():
            text = by_id[event_id].get(key) or ''
            if new in text:
                continue
            if old not in text:
                raise SystemExit(f'[error] {mod.__name__}: {event_id}.{key} has neither the '
                                 f'old nor the new text: {old[:60]!r}')
            by_id[event_id][key] = text.replace(old, new, 1)
            changed += 1

    def matches(item, want):
        return isinstance(item, dict) and all(item.get(k) == v for k, v in want.items())

    for event_id, lists in getattr(mod, 'AMEND', {}).items():
        for key, edits in lists.items():
            items = by_id[event_id].get(key) or []
            for want, new in edits:
                hits = [it for it in items if matches(it, want)]
                if not hits and any(matches(it, {**want, **new}) for it in items):
                    continue
                if len(hits) != 1:
                    raise SystemExit(f'[error] {mod.__name__}: {event_id}.{key}: {len(hits)} '
                                     f'items match {want!r}')
                hits[0].update(new)
                changed += 1

    for event_id, paths in getattr(mod, 'APPEND', {}).items():
        for path, items in paths.items():
            *parents, leaf = path.split('.')
            node = by_id[event_id]
            for key in parents:
                node = node.setdefault(key, {})
            have = node.setdefault(leaf, [])
            for item in items:
                if item not in have:
                    have.append(item)
                    changed += 1

    added = 0
    for new in getattr(mod, 'NEW_EVENTS', []):
        if new['id'] in by_id:
            continue
        pos = next((i for i, e in enumerate(events) if (e.get('date') or '') > new['date']),
                   len(events))
        events.insert(pos, new)
        by_id[new['id']] = new
        added += 1
    return changed, added


def verify_quotes(events: list, ids: set) -> list:
    """Quotes on the given events that are not verbatim anywhere in the corpus.

    Uses the dossier seeders' normalise(), so OCR hyphenation, running heads and
    typography do not count against a quotation, but the words must match. An
    elision ("..." or "…") is allowed when every fragment appears, in order,
    in one source text; a quote whose fragments are reordered fails.
    """
    import re
    import sqlite3
    sys.path.insert(0, str(PROJECT_DIR / 'scripts' / 'studies'))
    from seed_burroughs_word_virus import normalise

    db = sqlite3.connect(str(PROJECT_DIR / 'database' / 'unified.sqlite'))
    texts = [t for (t,) in db.execute("SELECT body_md FROM letters")]
    texts += [t for (t,) in db.execute("SELECT raw_text FROM segments")]
    texts += [t for (t,) in db.execute(
        "SELECT COALESCE(markdown_content, text_content) FROM document_texts")]
    corpus = [normalise(t) for t in texts if t]
    joined = '\n'.join(corpus)

    def found(quote: str) -> bool:
        parts = [normalise(f) for f in re.split(r'\.\.\.+|…', quote)]
        parts = [f.strip(' .,;') for f in parts if f.strip(' .,;')]
        if len(parts) <= 1:
            return normalise(quote).strip(' .') in joined
        if any(part not in joined for part in parts):
            return False
        for text in corpus:
            pos = 0
            for part in parts:
                pos = text.find(part, pos)
                if pos < 0:
                    break
                pos += len(part)
            else:
                return True
        return False

    return [(e['id'], q['text']) for e in events if e['id'] in ids
            for q in e.get('quotes') or [] if not found(q['text'])]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('modules', nargs='*', help='module names in curation/biography/')
    ap.add_argument('--check', action='store_true', help='report changes, write nothing')
    ap.add_argument('--verify', action='store_true',
                    help='refuse to write unless every quote on a touched event is '
                         'verbatim in database/unified.sqlite')
    ap.add_argument('--audit', action='store_true',
                    help='check every quote in curated.json, apply nothing, exit 1 on failure')
    args = ap.parse_args()

    if args.audit:
        events = json.loads(CURATED_PATH.read_text(encoding='utf-8'))
        with_quotes = {e['id'] for e in events if e.get('quotes')}
        bad = verify_quotes(events, with_quotes)
        for event_id, text in bad:
            print(f'  NOT VERBATIM  {event_id}: {text[:80]!r}')
        n = sum(len(e['quotes']) for e in events if e.get('quotes'))
        print(f'  {n - len(bad)} of {n} quotes on {len(with_quotes)} events are verbatim')
        return 1 if bad else 0

    paths = ([CURATION_DIR / f'{m}.py' for m in args.modules] if args.modules
             else sorted(p for p in CURATION_DIR.glob('*.py') if not p.name.startswith('_')))
    raw = CURATED_PATH.read_text(encoding='utf-8')
    events = json.loads(raw)
    before = len(events)

    touched = set()
    for path in paths:
        mod = load_module(path)
        changed, added = apply(events, mod)
        touched |= set(getattr(mod, 'CORRECTIONS', {})) | set(getattr(mod, 'APPEND', {}))
        touched |= set(getattr(mod, 'REPLACE', {})) | set(getattr(mod, 'AMEND', {}))
        touched |= {e['id'] for e in getattr(mod, 'NEW_EVENTS', [])}
        print(f'  {path.stem}: {changed} field(s) changed, {added} event(s) added')

    if args.verify:
        bad = verify_quotes(events, touched)
        for event_id, text in bad:
            print(f'  NOT VERBATIM  {event_id}: {text[:80]!r}')
        if bad:
            print('[error] quotations not found in the corpus; nothing written')
            return 1
        print(f'  every quote on {len(touched)} touched event(s) is verbatim in the corpus')

    out = json.dumps(events, ensure_ascii=False, indent=2)
    if raw.endswith('\n'):
        out += '\n'
    if out == raw:
        print('  curated.json already up to date')
        return 0
    if args.check:
        print(f'  would write curated.json ({before} -> {len(events)} events)')
        return 0
    CURATED_PATH.write_text(out, encoding='utf-8')
    print(f'  wrote curated.json ({before} -> {len(events)} events)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
