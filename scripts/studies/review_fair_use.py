#!/usr/bin/env python3
"""
Stage 5h: Review passages for fair-use compliance.

Sends passages longer than 300 characters to Claude for review.
Claude determines if a passage is too long or too verbatim, and if needed,
produces a fair-use summary (under 200 words).

Usage:
    python scripts/studies/review_fair_use.py
    python scripts/studies/review_fair_use.py --db database/unified.sqlite
"""

import json
import sqlite3
import sys
import time
from pathlib import Path

from anthropic import Anthropic

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

PROJECT_DIR = SCRIPTS_DIR.parent
DEFAULT_DB = PROJECT_DIR / 'database' / 'unified.sqlite'

MODEL = 'claude-sonnet-4-20250514'
BATCH_SIZE = 10
MIN_LENGTH_FOR_REVIEW = 300

FAIR_USE_PROMPT = """\
You are reviewing passages extracted from copyrighted works about Philip K. Dick
for fair-use compliance in a scholarly research tool.

For each passage below, determine:

1. Is the passage too long or too verbatim to qualify as fair use in a scholarly
   research context? Consider:
   - Length relative to the source work
   - Whether it reproduces creative expression vs. factual content
   - Whether a shorter excerpt would serve the same analytical purpose

2. If the passage is acceptable as-is, mark it "approved".
   If it needs trimming, provide a fair-use summary (UNDER 200 words) that:
   - Preserves the analytical value
   - Paraphrases rather than quoting verbatim
   - Retains key terms and concepts
   - Notes the source context

Return a JSON array with one object per passage:
[
  {{
    "passage_id": 123,
    "status": "approved",
    "trimmed_text": null
  }},
  {{
    "passage_id": 456,
    "status": "trimmed",
    "trimmed_text": "In this passage, Dick explores the theme of..."
  }},
  ...
]

Status must be one of: approved | trimmed | rejected
- approved: passage is fine as-is for fair use
- trimmed: passage needs the replacement text provided in trimmed_text
- rejected: passage should not be used at all (e.g., pure creative content
  with no analytical value)

Return ONLY the JSON array, no other text.
"""


def build_batch_prompt(passages):
    """Build prompt for a batch of passages."""
    lines = [FAIR_USE_PROMPT, "\n--- PASSAGES FOR REVIEW ---\n"]
    for p in passages:
        lines.append(f"passage_id: {p[0]}")
        lines.append(f"length: {len(p[1])} chars")
        lines.append(f"lane: {p[2]} | source_mode: {p[3]}")
        lines.append(f"text: {p[1]}")
        lines.append("")
    return "\n".join(lines)


def review_batch(client, passages):
    """Send a batch to Claude for fair-use review."""
    prompt = build_batch_prompt(passages)
    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.content[0].text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            text = text.rsplit("```", 1)[0]
        return json.loads(text)
    except Exception as e:
        print(f"    ERROR in Claude API call: {e}")
        return []


def run(db: sqlite3.Connection, source: Path = None):
    """Review passages for fair-use compliance."""
    print("  Reviewing passages for fair-use compliance...")

    # Query long passages that haven't been reviewed (checkpoint: skip non-pending)
    rows = db.execute("""
        SELECT passage_id, passage_text, lane, source_mode
        FROM study_passages
        WHERE length(passage_text) > ?
        AND fair_use_status = 'pending'
        ORDER BY passage_id
    """, (MIN_LENGTH_FOR_REVIEW,)).fetchall()

    if not rows:
        print("    No passages need fair-use review")
        return

    print(f"    {len(rows)} passages to review")

    # Also auto-approve short passages
    auto_approved = db.execute("""
        UPDATE study_passages
        SET fair_use_status = 'approved'
        WHERE length(passage_text) <= ?
        AND fair_use_status = 'pending'
    """, (MIN_LENGTH_FOR_REVIEW,)).rowcount
    db.commit()
    if auto_approved:
        print(f"    Auto-approved {auto_approved} short passages")

    client = Anthropic()
    total_reviewed = 0
    counts = {'approved': 0, 'trimmed': 0, 'rejected': 0}

    for i in range(0, len(rows), BATCH_SIZE):
        batch = rows[i:i + BATCH_SIZE]
        print(f"    Batch {i // BATCH_SIZE + 1}: passages {batch[0][0]}..{batch[-1][0]}")

        results = review_batch(client, batch)

        for r in results:
            pid = r.get('passage_id')
            status = r.get('status')
            if pid is None or status not in ('approved', 'trimmed', 'rejected'):
                continue

            if status == 'trimmed' and r.get('trimmed_text'):
                db.execute("""
                    UPDATE study_passages SET
                        fair_use_status = 'trimmed',
                        passage_text = ?,
                        notes = COALESCE(notes || '; ', '') || 'Fair-use trimmed by Claude'
                    WHERE passage_id = ?
                """, (r['trimmed_text'], pid))
            else:
                db.execute("""
                    UPDATE study_passages SET fair_use_status = ?
                    WHERE passage_id = ?
                """, (status, pid))

            counts[status] = counts.get(status, 0) + 1
            total_reviewed += 1

        db.commit()
        time.sleep(1)

    print(f"    Reviewed {total_reviewed} passages:")
    for status, count in counts.items():
        if count:
            print(f"      {status}: {count}")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Review passages for fair-use compliance')
    parser.add_argument('--db', type=Path, default=DEFAULT_DB)
    args = parser.parse_args()

    start = time.time()
    db = sqlite3.connect(str(args.db))
    db.execute("PRAGMA foreign_keys = ON")
    run(db)
    db.close()
    elapsed = time.time() - start
    print(f"Done in {elapsed:.1f}s")
