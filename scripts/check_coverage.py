"""Check PDF text extraction coverage in the database."""
import sqlite3

db = sqlite3.connect('database/unified.sqlite')

total_archive = db.execute(
    "SELECT COUNT(*) FROM documents WHERE doc_type != 'exegesis_section'"
).fetchone()[0]

has_text = db.execute(
    "SELECT COUNT(*) FROM document_texts WHERE text_content IS NOT NULL AND char_count > 0"
).fetchone()[0]

failed = db.execute(
    "SELECT COUNT(*) FROM document_texts WHERE extraction_status = 'failed'"
).fetchone()[0]

pending = db.execute(
    "SELECT COUNT(*) FROM document_texts WHERE extraction_status = 'pending'"
).fetchone()[0]

print(f"Archive docs: {total_archive}")
print(f"With extracted text: {has_text}")
print(f"Failed extraction: {failed}")
print(f"Pending extraction: {pending}")
print()

# Top docs by text length
rows = db.execute("""
    SELECT d.title, d.author, d.category, dt.char_count
    FROM document_texts dt
    JOIN documents d ON dt.doc_id = d.doc_id
    WHERE dt.text_content IS NOT NULL AND dt.char_count > 0
    ORDER BY dt.char_count DESC
    LIMIT 20
""").fetchall()

print("Top 20 docs by text length:")
for r in rows:
    title = (r[0] or "?")[:60]
    author = (r[1] or "?")[:30]
    print(f"  {r[3]:>8} chars | {author:30s} | {title}")

print()

# Category breakdown
cats = db.execute("""
    SELECT d.category,
           COUNT(*),
           SUM(CASE WHEN dt.text_content IS NOT NULL AND dt.char_count > 0 THEN 1 ELSE 0 END)
    FROM documents d
    LEFT JOIN document_texts dt ON d.doc_id = dt.doc_id
    WHERE d.doc_type != 'exegesis_section'
    GROUP BY d.category
""").fetchall()

print("Category coverage:")
for c in cats:
    cat = (c[0] or "uncategorized")[:25]
    print(f"  {cat:25s} total={c[1]:3d}  with_text={c[2]:3d}")

# Check if the 6 priority biographies have text
print()
print("Priority biographies:")
priority_authors = ['Sutin', 'Anne Dick', 'Rickman', 'Arnold', 'Peake']
for author in priority_authors:
    rows = db.execute("""
        SELECT d.title, d.author, dt.char_count, dt.extraction_status
        FROM documents d
        LEFT JOIN document_texts dt ON d.doc_id = dt.doc_id
        WHERE d.author LIKE ? AND d.doc_type != 'exegesis_section'
    """, (f"%{author}%",)).fetchall()
    for r in rows:
        chars = r[2] or 0
        status = r[3] or "no text entry"
        print(f"  {r[1]:30s} | {chars:>8} chars | {status:10s} | {r[0][:50]}")

db.close()
