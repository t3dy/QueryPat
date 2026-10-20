#!/usr/bin/env python3
"""
Stage PDFs from the archive as searchable text, and record each one in a manifest.

    python scripts/research/ingest_pdfs.py --src database/source_pdfs
    python scripts/research/ingest_pdfs.py --src /path/to/archive --lane C --doc-type scholarship
    python scripts/research/ingest_pdfs.py --src DIR --ocr force     # rasterise and OCR every page

For each PDF this script:

  1. reads the page count (pdfinfo) and the text layer (pdftotext, one page
     break marker per page);
  2. if a page has almost no text and tesseract is installed, OCRs that page
     (pdftoppm then tesseract); if tesseract is missing, records the page as
     needing OCR rather than pretending it is empty;
  3. writes curation/religion/pdf-text/<doc_id>.txt, the text the sweep reads;
  4. adds or updates the document in curation/religion/pdf-manifest.json, keyed
     by doc_id. Editor-set fields (lane, doc_type, author, date, title) are kept
     on re-ingest; only the extraction fields are rewritten.

A document whose lane has not been assigned is staged with lane "D" and
flagged `lane_assigned: false`. The sweep treats it as editorial until someone
decides what it is. Nothing is classified automatically.

Requires: pdfinfo and pdftotext (poppler-utils). Optional: pdftoppm and tesseract
for OCR. Check with --check.
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
CUR = PROJECT_DIR / 'curation' / 'religion'
TEXT_DIR = CUR / 'pdf-text'
MANIFEST = CUR / 'pdf-manifest.json'

# A page with fewer characters than this has no usable text layer.
MIN_CHARS_PER_PAGE = 120
LANES = {'A', 'B', 'C', 'D'}


def tool_status():
    return {t: shutil.which(t) is not None
            for t in ('pdfinfo', 'pdftotext', 'pdftoppm', 'tesseract')}


def doc_id_for(path):
    slug = re.sub(r'[^A-Za-z0-9]+', '_', path.stem).strip('_').upper()
    return f'PDF_{slug}'


def page_count(path):
    out = subprocess.run(['pdfinfo', str(path)], capture_output=True, text=True)
    m = re.search(r'^Pages:\s+(\d+)', out.stdout, re.M)
    if not m:
        raise RuntimeError(f'pdfinfo could not read {path.name}: {out.stderr.strip()}')
    return int(m.group(1))


def page_text(path, page):
    out = subprocess.run(['pdftotext', '-layout', '-f', str(page), '-l', str(page),
                          str(path), '-'], capture_output=True, text=True)
    return out.stdout


def ocr_page(path, page, workdir):
    stem = workdir / f'p{page:04d}'
    subprocess.run(['pdftoppm', '-r', '300', '-f', str(page), '-l', str(page), '-png',
                    str(path), str(stem)], check=True, capture_output=True)
    png = sorted(workdir.glob(f'p{page:04d}*.png'))[-1]
    out = subprocess.run(['tesseract', str(png), '-', '-l', 'eng'],
                         capture_output=True, text=True)
    png.unlink(missing_ok=True)
    return out.stdout


def extract(path, ocr_mode, have):
    """Return (text, pages, ocr_pages, pages_needing_ocr)."""
    pages = page_count(path)
    chunks, ocr_done, needs_ocr = [], [], []
    workdir = TEXT_DIR / '.ocr-tmp'
    for p in range(1, pages + 1):
        text = '' if ocr_mode == 'force' else page_text(path, p)
        if ocr_mode == 'force' or (ocr_mode != 'off' and len(text.strip()) < MIN_CHARS_PER_PAGE):
            if have['tesseract'] and have['pdftoppm']:
                workdir.mkdir(parents=True, exist_ok=True)
                text = ocr_page(path, p, workdir)
                ocr_done.append(p)
            else:
                needs_ocr.append(p)
        chunks.append(f'\n\f[page {p}]\n{text.strip()}\n')
    if workdir.exists():
        shutil.rmtree(workdir, ignore_errors=True)
    return ''.join(chunks), pages, ocr_done, needs_ocr


def load_manifest():
    if MANIFEST.exists():
        return json.loads(MANIFEST.read_text(encoding='utf-8'))
    return {'generator': 'scripts/research/ingest_pdfs.py', 'documents': []}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--src', help='directory of PDFs to ingest')
    ap.add_argument('--file', action='append', default=[],
                    help='a single PDF to ingest (repeatable)')
    ap.add_argument('--lane', choices=sorted(LANES), default=None,
                    help='the evidentiary lane to record for these PDFs')
    ap.add_argument('--doc-type', default=None,
                    help='notes, letter, interview, scholarship, novel, archive_pdf ...')
    ap.add_argument('--title', default=None, help='title, for a single --file')
    ap.add_argument('--author', default=None)
    ap.add_argument('--date', default=None)
    ap.add_argument('--ocr', choices=['auto', 'off', 'force'], default='auto')
    ap.add_argument('--check', action='store_true',
                    help='report which tools are available and exit')
    args = ap.parse_args()

    have = tool_status()
    if args.check:
        for k, v in have.items():
            print(f'  {k:<12} {"yes" if v else "MISSING"}')
        if not have['tesseract']:
            print('  OCR is unavailable: image-only pages will be recorded as needing OCR.')
        return 0 if have['pdfinfo'] and have['pdftotext'] else 2
    if not (have['pdfinfo'] and have['pdftotext']):
        print('ERROR: pdfinfo and pdftotext are required (poppler-utils).', file=sys.stderr)
        return 2

    paths = [Path(f) for f in args.file]
    if args.src:
        paths += sorted(Path(args.src).rglob('*.pdf'))
    if not paths:
        print('No PDFs given. Use --src DIR or --file PATH.', file=sys.stderr)
        return 2

    TEXT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = load_manifest()
    by_id = {d['doc_id']: d for d in manifest['documents']}
    now = datetime.now(timezone.utc).isoformat(timespec='seconds')

    for path in paths:
        path = path.resolve()
        doc_id = doc_id_for(path)
        try:
            text, pages, ocr_done, needs_ocr = extract(path, args.ocr, have)
        except (RuntimeError, subprocess.CalledProcessError) as exc:
            print(f'  FAILED {path.name}: {exc}', file=sys.stderr)
            continue
        text_rel = f'pdf-text/{doc_id}.txt'
        (CUR / text_rel).write_text(text, encoding='utf-8')
        chars = len(text.strip())

        prev = by_id.get(doc_id, {})
        entry = {
            **prev,
            'doc_id': doc_id,
            'file': str(path.relative_to(PROJECT_DIR)) if PROJECT_DIR in path.parents
                    else str(path),
            'text_file': text_rel,
            'pages': pages,
            'text_chars': chars,
            'pages_ocred': ocr_done,
            'pages_needing_ocr': needs_ocr,
            'extracted_utc': now,
        }
        entry.setdefault('title', args.title or path.stem.replace('-', ' ').replace('_', ' '))
        if args.title and len(paths) == 1:
            entry['title'] = args.title
        if args.author:
            entry['author'] = args.author
        if args.date:
            entry['date'] = args.date
        if args.doc_type:
            entry['doc_type'] = args.doc_type
        if args.lane:
            entry['lane'] = args.lane
            entry['lane_assigned'] = True
        entry.setdefault('lane', 'D')
        entry.setdefault('lane_assigned', False)
        entry.setdefault('doc_type', 'archive_pdf')
        by_id[doc_id] = entry

        status = (f'{pages} pages, {chars} chars'
                  + (f', OCR {len(ocr_done)} page(s)' if ocr_done else '')
                  + (f', {len(needs_ocr)} page(s) NEED OCR' if needs_ocr else ''))
        print(f'  {path.name}: {doc_id}  {status}  lane {entry["lane"]}'
              + ('' if entry['lane_assigned'] else ' (unassigned)'))

    manifest['documents'] = sorted(by_id.values(), key=lambda d: d['doc_id'])
    manifest['updated_utc'] = now
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n',
                        encoding='utf-8')
    print(f'manifest: {MANIFEST.relative_to(PROJECT_DIR)} ({len(by_id)} document(s))')
    return 0


if __name__ == '__main__':
    sys.exit(main())
