# Curation: Religion in PKD

The religion study, as a research database and a browsable site.

Every religious tradition Dick engages with is a **topic**, and each topic is
divided into **subsections**. Every mention of a subsection in the sources held
here is a **finding**, with its lane, date, decade, matched term, context, and
editorial status. A finding can belong to several subsections, and the site links
between them, so the material can be browsed by tradition, by subsection, by lane,
by decade, or by review state.

## Topics

| Topic | Subsections |
|---|---|
| Christianity | Christ and Jesus · Paul, Acts and the early church · Apocalypse and the Second Advent · The Church and Rome · Scripture and the Bible |
| Gnosticism | Sophia · The Demiurge · Anamnesis · Gnostic texts · Gnostic (general) |
| Zoroastrianism and Mazdaism | Zoroaster · Dualism and Manichaeism · Mithraism |
| Judaism and the Torah | The Torah · Essenes and Qumran · Prophets: Elijah, Malachi, Daniel |
| Kabbalah | General · Sefirot, Malkuth, Tree of Life · The Zohar |
| Logos | The Logos as Word · The Logos as information |
| Mercerism | Wilbur Mercer · Mercerism as religion |
| Platonism, Neoplatonism, Hermeticism | Plato and Pythagoras · Plotinus and the Neoplatonists · Hermetic writings |
| Mystery religions | Dionysus, Zagreus and the Bacchae · Eleusis and Orphism |
| Mysticism | Mystical experience |
| Buddhism | Buddhism and the Bardo |
| Hinduism | Brahman, Atman and the Upanishads · Hindu deities |
| Taoism | The Tao |
| Islam | Islam and Sufism |

The taxonomy is `taxonomy.py`. It is the thing to edit when a subsection or
pattern changes. Each subsection has `strong` terms (the subject itself), `weak`
terms (ordinary words or first names, which must be read), and `exclude` patterns.

## Pipeline

```
taxonomy.py ──┐
raw corpus ───┼─► sweep_religion.py ─► raw-findings.json ─┐
PDF text ─────┘                                            ├─► build_religion_db.py ─► religion.sqlite
manifest ─────────────────────────────────────────────────┘           ▲
editorial.json ───────────────────────────────────────────────────────┘
                                                                     │
                                  build_religion_study.py ◄──────────┘
                                          │
                                          ▼
              site/public/data/studies/religion/  (index, topics, findings per subsection, facets)
```

```bash
python scripts/research/sweep_religion.py --summary --out curation/religion/raw-findings.json
python scripts/research/build_religion_db.py
python scripts/studies/build_religion_study.py
python scripts/research/religion_review.py summary
```

`raw-findings.json` and `religion.sqlite` are derived and git-ignored. They rebuild
from the committed inputs in about a minute. `editorial.json` is the one file that
records human judgement, and it is committed.

## The database

`religion.sqlite`, schema defined in `build_religion_db.py`:

| Table | One row per |
|---|---|
| `topics` | tradition |
| `subsections` | subsection, with its patterns as JSON |
| `sources` | corpus record: a segment, chapter, letter, document, or staged PDF |
| `findings` | hit, with lane, tier, date, decade, context, relevance, review status |
| `finding_subsections` | (finding, subsection) pair: the many-to-many link |
| `findings_fts` | full-text index over context and matched term (FTS5) |
| `v_subsection_lane`, `v_subsection_decade` | counts, for queries |
| `build_info` | when the database was built, and from what |

Example queries:

```sql
-- Sophia mentions in Dick's own words, by decade
SELECT f.decade, COUNT(*) FROM finding_subsections fs
JOIN findings f USING (finding_id)
WHERE fs.subsection_id = 'sophia' AND f.lane = 'A' GROUP BY f.decade;

-- Findings tagged with both Gnosticism's anamnesis and Platonism's Plato
SELECT f.finding_id, f.context FROM findings f
WHERE f.finding_id IN (SELECT finding_id FROM finding_subsections WHERE subsection_id = 'anamnesis')
  AND f.finding_id IN (SELECT finding_id FROM finding_subsections WHERE subsection_id = 'plato-pythagoras');

-- Full-text search across every subsection
SELECT f.finding_id, f.matched_text FROM findings_fts
JOIN findings f ON f.rowid = findings_fts.rowid WHERE findings_fts MATCH 'Mercer';
```

## Lanes

| Lane | Meaning | Browsed on the site |
|---|---|---|
| A | Dick's own words: Exegesis, VALIS and Divine Invasion chapters, letters, and any PDF assigned lane A | yes |
| C | Scholarship: archive records and PDFs assigned lane C | yes |
| D | Portal editorial analysis: summaries, and the Exegesis analytic fields that paraphrase Dick's text | database only |

Lane D (about 27,000 findings, most from the Exegesis analytic fields) restates Dick's own text in the
portal's words. They stay in the database, so they can be searched, but they are not
shown as evidence on the site.

## Editorial review

Every finding starts `unreviewed`. Review records a relevance code and a status in
`editorial.json`, keyed by finding id. The codes match the Burroughs study's:

| Code | Meaning |
|---|---|
| 1 | direct engagement with the subject |
| 2 | used as a tool for another argument, or dramatised in fiction |
| 3 | passing mention |
| 4 | thematic parallel, no evidence of contact |
| 5 | false positive |

```bash
python scripts/research/religion_review.py next --subsection sophia --lane A --unreviewed --limit 10
python scripts/research/religion_review.py show REL_…
python scripts/research/religion_review.py decide REL_… --relevance 3 --note "name only, no argument"
python scripts/research/religion_review.py decide REL_… --status excluded --relevance 5
```

Finding ids are hashes of the corpus record, the field, the character offset and
the matched text. A decision survives re-sweeps that leave the text unchanged.
If a source is edited, its decisions are kept in `editorial.json` but will not
match the new findings; the database shows them as unreviewed again, and nothing is
lost.

## Archive PDFs: when they are available

The repository holds one archive PDF, `database/source_pdfs/Maze notes.pdf`. The
wider archive is not in the repository, so the research software is built to run
against it as soon as it is. To ingest a PDF:

```bash
python scripts/research/ingest_pdfs.py --check        # which tools are installed
python scripts/research/ingest_pdfs.py --src DIR --doc-type scholarship --lane C
python scripts/research/ingest_pdfs.py --file "Maze notes.pdf" --lane A --doc-type notes \
    --title "Maze notes" --date "1976"
```

`ingest_pdfs.py`:

1. reads each page's text layer with `pdftotext`;
2. OCRs any page with almost no text, if `pdftoppm` and `tesseract` are installed;
   otherwise records the page in `pages_needing_ocr` rather than leaving it empty;
3. writes `pdf-text/<doc_id>.txt`, with a `[page N]` marker at each page break;
4. records the document in `pdf-manifest.json`, keyed by doc id. Editor-set fields
   (lane, doc type, author, date, title) survive re-ingest; only extraction fields
   are rewritten.

A document with no lane is staged as lane D and marked `lane_assigned: false`. It
is not treated as Dick's words or as scholarship until someone assigns a lane.
Assigning the lane is an editorial decision. The `Maze notes` PDF, for example,
reads like Dick's own notes, and its lane is left unassigned until someone confirms it.

Tesseract is not installed in this container. Image-only pages are therefore
listed as needing OCR. Install `tesseract-ocr` and re-run with `--ocr force` to OCR
them.

Once PDFs are ingested, rerun the sweep, the database build and the export. The
sweep reads the manifest automatically.

## Limits

- The Exegesis is the largest body of Dick's own text here. The VALIS chapters
  held as full text are 1 and 5–13, and Divine Invasion 1–5. The other trilogy
  chapters and the other novels are summaries.
- The letters are 1,500-character excerpts of the 1972–73 volume, with some bodies
  in the wrong field. A search of them is a floor, not a census.
- The interviews are catalogue entries and summaries. No interview transcript is
  held, so a finding about what Dick said in interview cannot be made from here.
- The stories are summaries only.
- Exegesis dates are folder dates. Each folder is a transcription batch and can
  contain entries written across several years, so decades are batch decades.
- Patterns are a first pass. Weak terms (for example `Elias`, `Paul`, `Law`)
  produce findings that are often not about the tradition at all. Read them before
  relying on them, or filter to strong terms.
