# Archive → Markdown Ingestion Plan

**Goal:** convert every archive document (228 PDFs/EPUBs/DOCXs/etc.) to clean markdown, store both on disk and in the database, and make the result queryable for downstream LLM work (essay drafting, biography mining, dictionary expansion).

**Scope:** the 228 `DOC_ARCH_*` documents tracked in `documents` table. Excludes the 246 `DOC_EXEG_*` Exegesis sections (those have a separate parsed-segment pipeline and don't need markdown conversion).

---

## Inventory (current state, queried 2026-04-29)

- **228 archive documents** in `documents` table
- **224 have a `document_texts` row** with `extraction_method='pre_extracted'` (PyMuPDF-dumped plain text, no markdown structure)
- **180 have non-trivial text** (>100 chars after extraction)
- **21 marked `ocr_required=1`** — image-only PDFs (Pamela Jackson dissertation among them)
- **26 marked `extraction_status='pending'`** — never attempted
- **18 EPUB assets**, rest mostly PDF

The existing `text_content` is plain text — no headings, no paragraph structure, no table preservation. Markdown conversion gives all of that back and is what downstream LLM work needs.

---

## Architecture decisions

### Where the markdown lives

1. **On disk:** `database/extracted_markdown/{doc_id}.md` — one file per document. Greppable, diffable, viewable in any markdown viewer. Source of truth for human inspection.
2. **In the database:** `document_texts.markdown_content TEXT` — same content, queryable from SQL, exportable to JSON. Source of truth for the build pipeline.

The two are kept in sync by the conversion script. Either can be regenerated from the other.

### Schema migration (additive, non-breaking)

```sql
ALTER TABLE document_texts ADD COLUMN markdown_content TEXT;
ALTER TABLE document_texts ADD COLUMN markdown_method TEXT;       -- pymupdf4llm | pandoc | docx | xlsx | passthrough | ocr+pymupdf4llm
ALTER TABLE document_texts ADD COLUMN markdown_status TEXT;       -- pending | complete | failed | skipped_ocr_required
ALTER TABLE document_texts ADD COLUMN markdown_char_count INTEGER;
ALTER TABLE document_texts ADD COLUMN markdown_error TEXT;
ALTER TABLE document_texts ADD COLUMN markdown_updated_at TEXT;
ALTER TABLE document_texts ADD COLUMN markdown_source_hash TEXT;  -- sha256 of source asset; for cache invalidation
```

All additive. The existing `text_content` column stays untouched (legacy plain-text dump remains for backwards compat).

### Converter selection by source type

| Source extension | Tool | Notes |
|---|---|---|
| `.pdf` (text-extractable) | **pymupdf4llm** | Preserves headings, lists, tables. Standard for PDF→md. |
| `.pdf` (image-only / OCR-required) | **flag as `skipped_ocr_required`** | No tesseract/ocrmypdf installed. Out-of-band OCR pass queued. |
| `.epub` | **ebooklib + markdownify** | Walk OPF spine, convert each XHTML chapter. |
| `.docx` | **python-docx + custom md-emit** | mammoth/pandoc unavailable; build minimal converter. |
| `.xlsx` | **openpyxl → tabular markdown** | Header row + data rows as a `\| ... \|` table. |
| `.txt` | **passthrough with paragraph normalization** | Wrap long lines, preserve blank-line paragraph breaks. |
| `.html` | **bs4 + markdownify** | Strip nav/script, convert body. |

### Idempotency

Each conversion records `markdown_source_hash` (SHA-256 of the source file). On re-run, the script:

1. Checks if `markdown_status='complete'` AND `markdown_source_hash` matches current asset hash.
2. If yes → skip (cache hit).
3. If no → re-convert, overwrite both file and DB.

This means re-running the script is safe and cheap. Adding new documents only converts the new ones.

### Performance

- Sequential by default (PyMuPDF is fast — most PDFs convert in <2s).
- `--workers N` flag for `multiprocessing.Pool`-based parallelism on the PDF batch.
- Progress printed every 10 docs.

### Failure handling

Any conversion exception is caught, logged with traceback to `markdown_error`, status set to `failed`. Script continues. Final report lists failures.

---

## File layout

```
scripts/
  markdown/
    __init__.py
    add_markdown_columns.py       # one-time schema migration (idempotent)
    convert_all.py                # main orchestrator — iterates assets, dispatches
    converters/
      __init__.py
      pdf.py                      # pymupdf4llm
      epub.py                     # ebooklib + markdownify
      docx.py                     # python-docx
      xlsx.py                     # openpyxl
      text.py                     # passthrough
      html.py                     # bs4 + markdownify
    report.py                     # write MARKDOWN_INGEST_REPORT.md
database/
  extracted_markdown/             # one .md per doc_id (NEW, gitignored or tracked? — see below)
    DOC_ARCH_*.md
```

### Should `database/extracted_markdown/` be tracked in git?

**Decision: gitignored.** Reproducible from the database via a one-liner. Adding ~50–100MB of markdown to the repo doesn't help anything. The DB column is the source of truth.

---

## Execution order

1. **Migrate schema** — `python scripts/markdown/add_markdown_columns.py` (instant).
2. **Run conversion** — `python scripts/markdown/convert_all.py` (estimated 5–15 min for ~200 docs sequentially; faster with `--workers 4`).
3. **Inspect report** — `MARKDOWN_INGEST_REPORT.md` enumerates per-doc status.
4. **Spot-check 3–5 documents** by opening their `.md` files and comparing to the source.
5. **Commit scripts** — the markdown files themselves stay gitignored.

---

## Out of scope (queue for later)

- **OCR pass for the 21 image-only PDFs.** Needs tesseract or ocrmypdf installed. Pamela Jackson's 1999 dissertation is the highest-value of these. Queue as a separate task.
- **Quality grading.** Counting headings, comparing markdown char count to source page count, flagging suspiciously thin extractions. Useful but not part of the first ingest.
- **LLM cleanup pass.** PDF→md from a scanned column-formatted PDF produces messy markdown; an LLM pass to fix structure would improve readability. Future.
- **Re-export to JSON.** Once the markdown column is populated, `export_json.py` should add a `markdown_excerpt` field to `archive/docs/{slug}.json`. Future.

---

## Risks

1. **`pymupdf4llm` is new (1.27.x).** Output quality varies with PDF complexity. Spot-check is essential.
2. **DOCX without mammoth/pandoc** — minimal converter only handles paragraphs, headings, lists. Tables and embedded images will be lossy. Acceptable for a first pass.
3. **Source paths in `assets.file_path`** are repo-relative-ish (`PaulPKDarchive/PKDpdf/...`) but the actual file lives at `C:/QueryPat/PaulPKDarchive/PKDpdf/...` (gitignored, outside repo). Need to resolve via a `BASE_PATH = C:/QueryPat/` prefix.
4. **Database location.** The worktree's `database/unified.sqlite` is empty (0 bytes). Real DB is at `C:/QueryPat/database/unified.sqlite` (99MB). The conversion will run against the real DB at the absolute path. The schema migration is additive and reversible (can drop columns).

---

## What success looks like

After running `convert_all.py`:

- `database/unified.sqlite` has 7 new columns on `document_texts`, populated for ≥180 documents (the text-extractable ones).
- `database/extracted_markdown/` has ≥180 `.md` files.
- `MARKDOWN_INGEST_REPORT.md` shows per-document status: complete / failed / skipped_ocr_required / pending-source-missing.
- Re-running the script is a no-op (cache hits on every doc).
- Spot-checking three documents shows readable markdown with proper headings and paragraph structure.
