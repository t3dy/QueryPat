"""
Generate reading_excerpt for segments from evidence_quotes.

Selects the most compelling quote from each segment's evidence_quotes
JSON array to serve as a representative excerpt for display.

Selection criteria:
- Prefers quotes 50-200 characters (readable length)
- Avoids very short fragments or very long passages
- Picks the first quote that meets criteria, or the best available
"""

import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def select_best_excerpt(quotes: list) -> str | None:
    """Select the best reading excerpt from a list of quote strings."""
    if not quotes:
        return None

    # Clean quotes: strip outer quotes and whitespace
    cleaned = []
    for q in quotes:
        if not isinstance(q, str):
            continue
        q = q.strip()
        if q.startswith('"') and q.endswith('"'):
            q = q[1:-1]
        if q.startswith("'") and q.endswith("'"):
            q = q[1:-1]
        q = q.strip()
        if len(q) > 15:
            cleaned.append(q)

    if not cleaned:
        return None

    # Prefer quotes in the sweet spot (50-250 chars)
    ideal = [q for q in cleaned if 50 <= len(q) <= 250]
    if ideal:
        return ideal[0]

    # Fall back to moderate length (30-400 chars)
    moderate = [q for q in cleaned if 30 <= len(q) <= 400]
    if moderate:
        q = moderate[0]
        if len(q) > 250:
            # Truncate at sentence boundary
            sentences = q.split('.')
            result = sentences[0] + '.'
            if len(result) > 30:
                return result
            if len(sentences) > 1:
                result += ' ' + sentences[1] + '.'
                return result
        return q

    # Last resort: take whatever we have
    q = cleaned[0]
    if len(q) > 250:
        return q[:247] + '...'
    return q


def run(db: sqlite3.Connection, source_dir: Path):
    print("Generating reading excerpts from evidence quotes...")

    rows = db.execute("""
        SELECT seg_id, evidence_quotes
        FROM segments
        WHERE evidence_quotes IS NOT NULL
            AND evidence_quotes != '[]'
            AND (reading_excerpt IS NULL OR length(reading_excerpt) < 10)
    """).fetchall()

    updated = 0
    for seg_id, eq_json in rows:
        try:
            quotes = json.loads(eq_json)
        except (json.JSONDecodeError, TypeError):
            continue

        excerpt = select_best_excerpt(quotes)
        if excerpt:
            db.execute(
                "UPDATE segments SET reading_excerpt = ? WHERE seg_id = ?",
                (excerpt, seg_id)
            )
            updated += 1

    db.commit()
    print(f"  Generated reading excerpts for {updated} of {len(rows)} segments")

    # Also try to generate excerpts from key_claims for segments with no evidence_quotes
    remaining = db.execute("""
        SELECT seg_id, key_claims
        FROM segments
        WHERE key_claims IS NOT NULL
            AND key_claims != '[]'
            AND (reading_excerpt IS NULL OR length(reading_excerpt) < 10)
    """).fetchall()

    from_claims = 0
    for seg_id, kc_json in remaining:
        try:
            claims = json.loads(kc_json)
        except (json.JSONDecodeError, TypeError):
            continue

        # Use first substantive claim
        for claim in claims:
            if isinstance(claim, str) and len(claim.strip()) > 30:
                db.execute(
                    "UPDATE segments SET reading_excerpt = ? WHERE seg_id = ?",
                    (claim.strip(), seg_id)
                )
                from_claims += 1
                break

    db.commit()
    print(f"  Generated {from_claims} additional excerpts from key_claims")

    total = db.execute(
        "SELECT COUNT(*) FROM segments WHERE reading_excerpt IS NOT NULL AND length(reading_excerpt) > 10"
    ).fetchone()[0]
    print(f"  Total segments with reading excerpts: {total}")


if __name__ == '__main__':
    db_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('C:/QueryPat/database/unified.sqlite')
    db = sqlite3.connect(str(db_path))
    run(db, Path('C:/ExegesisAnalysis'))
    db.close()
