"""
Stage 2: Compute chronological data for terms.

- First appearance date (earliest segment where term appears)
- Peak usage period (year range with highest frequency)
"""

import sqlite3
import sys
from pathlib import Path


def run(db: sqlite3.Connection, source_dir: Path):
    print("Stage 2: Computing chronology...")

    cursor = db.cursor()

    # Compute first appearance for each term
    cursor.execute("""
        UPDATE terms SET first_appearance = (
            SELECT MIN(s.date_start)
            FROM term_segments ts
            JOIN segments s ON ts.seg_id = s.seg_id
            WHERE ts.term_id = terms.term_id
            AND s.date_start IS NOT NULL
        )
        WHERE term_id IN (
            SELECT DISTINCT ts.term_id
            FROM term_segments ts
            JOIN segments s ON ts.seg_id = s.seg_id
            WHERE s.date_start IS NOT NULL
        )
    """)
    first_app = cursor.rowcount
    print(f"  Set first_appearance for {first_app} terms")

    # Compute peak usage year for each term
    # Find the year with the most segment links
    cursor.execute("""
        WITH year_counts AS (
            SELECT
                ts.term_id,
                SUBSTR(s.date_start, 1, 4) AS year,
                COUNT(*) AS cnt
            FROM term_segments ts
            JOIN segments s ON ts.seg_id = s.seg_id
            WHERE s.date_start IS NOT NULL
            GROUP BY ts.term_id, year
        ),
        peak_years AS (
            SELECT
                term_id,
                year,
                cnt,
                ROW_NUMBER() OVER (PARTITION BY term_id ORDER BY cnt DESC) AS rn
            FROM year_counts
        )
        UPDATE terms SET
            peak_usage_start = (
                SELECT year FROM peak_years
                WHERE peak_years.term_id = terms.term_id AND rn = 1
            ),
            peak_usage_end = (
                SELECT year FROM peak_years
                WHERE peak_years.term_id = terms.term_id AND rn = 1
            )
        WHERE term_id IN (SELECT term_id FROM peak_years WHERE rn = 1)
    """)
    peak = cursor.rowcount
    print(f"  Set peak_usage for {peak} terms")

    db.commit()


if __name__ == '__main__':
    db_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('C:/QueryPat/database/unified.sqlite')
    db = sqlite3.connect(str(db_path))
    run(db, Path('C:/ExegesisAnalysis'))
    db.close()
