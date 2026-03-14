"""
Stage 2: Map evidence excerpts to segments using line range resolution.

Evidence excerpts have line_start/line_end referencing exegesis_ordered.txt.
This script builds a chunk-to-line mapping by finding each chunk's text
within the ordered text using word-sequence fingerprinting, then resolves
each evidence excerpt to its corresponding segment(s).
"""

import re
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from date_norms import make_seg_id


NGRAM_SIZE = 6


def get_words(text: str) -> list[str]:
    """Extract lowercase alpha words from text."""
    return re.findall(r'[a-z]+', text.lower())


def build_line_mapping(source_dir: Path) -> list[tuple[str, int, int]]:
    """
    Build chunk-to-line-range mapping.

    Returns list of (chunk_id, start_line, end_line) tuples
    where lines are 1-based to match evidence_excerpts.line_start/line_end.
    """
    ordered_path = source_dir / 'exegesis_ordered.txt'
    chunks_dir = source_dir / 'chunks'

    if not ordered_path.exists() or not chunks_dir.exists():
        return []

    # Read ordered text and build word array with line mapping
    with open(ordered_path, 'r', encoding='utf-8') as f:
        ordered_lines = f.readlines()

    ordered_words = []
    word_line_map = []
    for line_num, line in enumerate(ordered_lines):
        words = get_words(line)
        for w in words:
            ordered_words.append(w)
            word_line_map.append(line_num)

    # Build ngram index for fast lookup
    ngram_index = {}
    for i in range(len(ordered_words) - NGRAM_SIZE):
        key = tuple(ordered_words[i:i + NGRAM_SIZE])
        if key not in ngram_index:
            ngram_index[key] = i

    # Map each chunk to its start line
    chunk_starts = {}
    for txt_path in sorted(chunks_dir.glob('*.txt')):
        chunk_id = txt_path.stem
        try:
            text = txt_path.read_text(encoding='utf-8')
        except (UnicodeDecodeError, OSError):
            continue

        words = get_words(text)
        if len(words) < 15:
            continue

        # Find chunk in ordered text via word sequence
        for start in range(8, min(40, len(words) - NGRAM_SIZE)):
            key = tuple(words[start:start + NGRAM_SIZE])
            if key in ngram_index:
                chunk_starts[chunk_id] = word_line_map[ngram_index[key]]
                break

    # Build intervals (convert to 1-based line numbers)
    sorted_chunks = sorted(chunk_starts.items(), key=lambda x: x[1])
    intervals = []
    for i, (chunk_id, start_0) in enumerate(sorted_chunks):
        if i + 1 < len(sorted_chunks):
            end_0 = sorted_chunks[i + 1][1] - 1
        else:
            end_0 = len(ordered_lines) - 1
        # Store as 1-based to match evidence line numbers
        intervals.append((chunk_id, start_0 + 1, end_0 + 1))

    return intervals


def run(db: sqlite3.Connection, source_dir: Path):
    """Map evidence excerpts to segments using line range resolution."""
    print("Mapping evidence excerpts to segments...")

    intervals = build_line_mapping(source_dir)
    if not intervals:
        print("  SKIP: Could not build line mapping")
        return

    print(f"  Built line mapping for {len(intervals)} chunks")

    # Get all evidence excerpts with line ranges but no segment mapping
    excerpts = db.execute("""
        SELECT excerpt_id, line_start, line_end
        FROM evidence_excerpts
        WHERE line_start IS NOT NULL AND line_end IS NOT NULL
    """).fetchall()

    print(f"  Processing {len(excerpts)} evidence excerpts...")

    mapped = 0
    unmapped = 0

    for excerpt_id, line_start, line_end in excerpts:
        # Find which chunk interval contains this excerpt's midpoint
        midpoint = (line_start + line_end) // 2
        seg_id = None

        for chunk_id, chunk_start, chunk_end in intervals:
            if chunk_start <= midpoint <= chunk_end:
                seg_id = make_seg_id('EXEG', chunk_id)
                break

        if seg_id:
            # Verify segment exists
            exists = db.execute(
                "SELECT 1 FROM segments WHERE seg_id = ?", (seg_id,)
            ).fetchone()
            if exists:
                db.execute(
                    "UPDATE evidence_excerpts SET seg_id = ? WHERE excerpt_id = ?",
                    (seg_id, excerpt_id)
                )
                mapped += 1
            else:
                unmapped += 1
        else:
            unmapped += 1

    db.commit()

    print(f"  Mapped {mapped} excerpts to segments ({unmapped} unmapped)")

    # Report coverage
    total = db.execute("SELECT COUNT(*) FROM evidence_excerpts").fetchone()[0]
    with_seg = db.execute(
        "SELECT COUNT(*) FROM evidence_excerpts WHERE seg_id IS NOT NULL"
    ).fetchone()[0]
    print(f"  Total evidence excerpts: {total}")
    print(f"  With segment link: {with_seg}")
    print(f"  Coverage: {with_seg * 100 // total}%")


if __name__ == '__main__':
    db_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('C:/QueryPat/database/unified.sqlite')
    db = sqlite3.connect(str(db_path))
    run(db, Path('C:/ExegesisAnalysis'))
    db.close()
