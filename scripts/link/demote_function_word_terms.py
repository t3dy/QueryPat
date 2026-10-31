"""
Demote English function words that triage promoted to dictionary terms.

Frequency-based triage (triage_terms.py) promotes any capitalised token that
recurs often enough, so sentence-initial words — Because, Since, Therefore,
However, Well, Maybe — became `accepted` terms. Their alphabetical `see_also`
lists then fan out through link_and_validate.py into `term_terms`, which is
why almost every dictionary page listed them as "related terms".

The list below is a closed-class stop-word list (pronouns, determiners,
conjunctions, prepositions, auxiliaries/modals) plus sentence adverbs and
discourse markers. It is matched against `terms.canonical_name` exactly
(case-insensitive, whole name), so multi-word terms are never touched.

For every matching term this script:
  1. sets status 'accepted'/'provisional' -> 'background' (IDs are kept;
     human-revised or publication-ready terms are left alone);
  2. deletes its `term_terms` rows with link_method 'see_also_field'
     (curated links from other methods are left alone);
  3. strips it from every term's `see_also` JSON array, so a re-run of
     link_and_validate cannot recreate the links.

Idempotent: a second run changes nothing. Registered in build_all.py
stage 2, immediately after link_and_validate.

Usage: python scripts/link/demote_function_word_terms.py [--db PATH] [--dry-run]
"""

import argparse
import json
import sqlite3
from pathlib import Path

DEFAULT_DB = Path(__file__).resolve().parents[2] / 'database' / 'unified.sqlite'

FUNCTION_WORDS = frozenset("""
    a about above across after afterwards again against all almost along
    already also although always am among an and another any anyhow anyone
    anything anyway anywhere are around as at
    be became because become been before beforehand behind below beside
    besides between beyond both but by
    can cannot could
    did do does doing done down during
    each either else elsewhere enough even ever every everyone everything
    everywhere except
    few for from further furthermore
    had has have having he hence her here hers herself him himself his how
    however
    i if in indeed instead into is it its itself
    just
    less like
    many may maybe me meanwhile might mine more moreover most much must my
    myself
    namely neither never nevertheless no nobody none nonetheless nor not
    nothing now nowhere
    of off often on once one only onto or other others otherwise our ours
    ourselves out over
    per perhaps
    quite
    rather
    same several shall she should since so some somebody somehow someone
    something sometimes somewhat somewhere still such
    than that the their theirs them themselves then thence there thereafter
    thereby therefore these they this those though through throughout thus
    to together too toward towards
    under unless until up upon us
    very via
    was we were what whatever when whenever where whereas wherever whether
    which while who whoever whom whose why will with within without would
    yet you your yours yourself yourselves

    actually apparently basically certainly clearly consider evidently
    finally hopefully incidentally look obviously okay ok possibly
    presumably probably really suppose surely wait well yes
""".split())

# Stop-list words that are also real concepts in this corpus, left alone on
# purpose: "Being" is Heidegger's Sein (see the accepted terms Sein and
# Dasein); "Will" is Schopenhauer's Wille (see Arthur Schopenhauer).
CONCEPT_EXCEPTIONS = frozenset({'being', 'will'})

CURATED_REVIEW_STATES = ('human-revised', 'publication-ready')


def find_function_word_terms(db: sqlite3.Connection):
    rows = db.execute(
        "SELECT term_id, canonical_name, status, review_state FROM terms"
    ).fetchall()
    return [
        r for r in rows
        if r[1].strip().lower() in FUNCTION_WORDS
        and r[1].strip().lower() not in CONCEPT_EXCEPTIONS
    ]


def run(db: sqlite3.Connection, source=None, dry_run: bool = False):
    """Demote function-word terms and unlink them. Returns a summary dict."""
    print("  Demoting function-word terms...")
    matches = find_function_word_terms(db)
    ids = [r[0] for r in matches]
    names = {r[1].strip().lower() for r in matches}

    to_demote = [r for r in matches
                 if r[2] in ('accepted', 'provisional')
                 and r[3] not in CURATED_REVIEW_STATES]
    skipped = [r for r in matches
               if r[2] in ('accepted', 'provisional')
               and r[3] in CURATED_REVIEW_STATES]

    marks = ','.join('?' * len(ids)) or "''"
    links = db.execute(f"""
        SELECT COUNT(*) FROM term_terms
        WHERE link_method = 'see_also_field'
          AND (term_id_a IN ({marks}) OR term_id_b IN ({marks}))
    """, ids + ids).fetchone()[0]

    see_also_updates = []
    for term_id, see_also in db.execute(
            "SELECT term_id, see_also FROM terms "
            "WHERE see_also IS NOT NULL AND see_also != '[]'").fetchall():
        try:
            arr = json.loads(see_also)
        except json.JSONDecodeError:
            continue
        if not isinstance(arr, list):
            continue
        kept = [s for s in arr
                if not (isinstance(s, str) and s.strip().lower() in names)]
        if len(kept) != len(arr):
            see_also_updates.append((json.dumps(kept), term_id))

    if not dry_run:
        db.executemany(
            "UPDATE terms SET status = 'background', updated_at = datetime('now') "
            "WHERE term_id = ?", [(r[0],) for r in to_demote])
        db.execute(f"""
            DELETE FROM term_terms
            WHERE link_method = 'see_also_field'
              AND (term_id_a IN ({marks}) OR term_id_b IN ({marks}))
        """, ids + ids)
        db.executemany("UPDATE terms SET see_also = ? WHERE term_id = ?",
                       see_also_updates)
        db.commit()

    would = '(dry run) ' if dry_run else ''
    print(f"    {len(matches)} function-word terms matched")
    print(f"    {would}Demoted {len(to_demote)} to background: "
          + ', '.join(sorted(r[1] for r in to_demote)))
    if skipped:
        print(f"    Left {len(skipped)} curated terms public: "
              + ', '.join(r[1] for r in skipped))
    print(f"    {would}Removed {links} see_also_field links")
    print(f"    {would}Cleaned see_also on {len(see_also_updates)} terms")
    return {
        'matched': [r[1] for r in matches],
        'demoted': [r[0] for r in to_demote],
        'links_removed': links,
        'see_also_cleaned': len(see_also_updates),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('--db', type=Path, default=DEFAULT_DB)
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()
    db = sqlite3.connect(str(args.db))
    try:
        run(db, dry_run=args.dry_run)
    finally:
        db.close()


if __name__ == '__main__':
    main()
