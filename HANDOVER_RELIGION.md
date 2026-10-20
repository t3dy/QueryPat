# Handover: the religion study, the Bible study, and the full archive

Read this first in a new session. It says where the work stands, what to do
with the full PKD archive, and what is known to be wrong. Read `CLAUDE.md` too:
its rules still apply, and this document does not repeat all of them.

## State at handover

- Repository: `t3dy/QueryPat`. Branch: `ccr-fda7e7ae-uh4a55`.
- Commits this work produced:
  - `d3791c4` The Bible in PKD study, reached from a Bible tab.
  - `1045fd5` Religion study: subsections, a relational database, and browsing.
- No pull request has been opened. Open one only when asked.
- Working tree was clean at handover.

Two studies now exist on the site, and they overlap:

| Study | Route | Built from | Status |
|---|---|---|---|
| The Bible in PKD | `/studies/bible/bible-in-pkd` (nav tab "Bible") | `curation/bible/` | Essay: 14 sections, 39 cards, all citations and quotations verified against the corpus |
| Religion in PKD | `/studies/religion/browse` (nav tab "Religion") and `/studies/religion/<topic>` | `curation/religion/` | Data and browse only: 14 topics, 34 subsections, no interpretive prose except the Bible-related pages |

The religion study's label is still **"Religion in PKD's Fiction"**. The
data-loss guard refused a shortened label, so the original was kept. Renaming it
is an editor's decision.

## Non-negotiable rules (from CLAUDE.md, restated where they bite)

- Never hand-edit `site/public/data/`. Generators write there; check the diff.
- Never run `scripts/export_json.py` or `scripts/studies/export_studies.py`
  directly. Use `python scripts/safeguard/safe_export.py --exporter all`.
- Run `python scripts/safeguard/check_data_diff.py --worktree` before every
  commit that touches `site/public/data`. It has refused once already this session.
- Never drop or rename an existing ID (`TERM_*`, `NAME_*`, `SEG_*`, `DOC_*`, `EV_*`, `CLAIM_*`).
- Keep lanes separate. Dick's words (A) are not scholarship (C) and not editor
  paraphrase (D). Lane D stays out of the browse export on purpose.
- LLM output is a candidate until curated.
- Do not resolve contradictions to make the data cleaner.
- Commit trailers: the session used `Co-Authored-By: Claude <noreply@anthropic.com>`
  without a model name, because the system prompt forbids model identifiers in commits.

## The religion pipeline (what runs, in order)

```bash
python scripts/research/sweep_religion.py --summary --out curation/religion/raw-findings.json
python scripts/research/build_religion_db.py          # -> curation/religion/religion.sqlite
python scripts/studies/build_religion_study.py         # -> site/public/data/studies/religion/
python scripts/research/religion_review.py summary
```

Files:

| File | Role | Committed |
|---|---|---|
| `curation/religion/taxonomy.py` | Topics, subsections, strong/weak/exclude patterns. Edit this to change tags. | yes |
| `scripts/research/sweep_religion.py` | Corpus sweep. Tags each hit with every subsection whose pattern matches the matched span. Finding id = hash(corpus, source_id, field, offset, match). | yes |
| `curation/religion/raw-findings.json` | Sweep output, 36 MB. Regenerable. | **no** (git-ignored) |
| `scripts/research/build_religion_db.py` | Builds SQLite: topics, subsections, sources, findings, finding_subsections, FTS5, views. | yes |
| `curation/religion/religion.sqlite` | Derived database. | **no** (git-ignored) |
| `curation/religion/editorial.json` | Human relevance and status decisions, keyed by finding id. Currently `{}`. | yes |
| `scripts/research/religion_review.py` | `summary`, `next`, `show`, `decide`. Writes `editorial.json`. | yes |
| `scripts/research/ingest_pdfs.py` | Stages archive PDFs as text under `curation/religion/pdf-text/`, records them in `pdf-manifest.json`. OCR where tesseract exists. | yes |
| `curation/religion/pdf-manifest.json` | One entry: `PDF_MAZE_NOTES`, lane **D, unassigned**. | yes |
| `scripts/studies/build_religion_study.py` | Exports browse lanes A and C to site JSON. Keeps the existing study label, description, featured sections and the old topic. | yes |
| `site/src/pages/ReligionBrowse.tsx` | Browse page. Filters are URL params (`topic`, `sub`, `lane`, `decade`, `tier`, `status`, `q`, `page`). | yes |
| `site/src/pages/TopicDetail.tsx` | Shows the subsection list on topic pages. Mention cards render only when present. | yes |

Baselines to check a rebuild against (current corpus):

- Sweep: 43,258 findings. Lane A 16,235, lane C 71, lane D 26,952.
- Browsable rows (lanes A and C): 16,306 across 34 subsections.
- Largest subsections: christology 8,570 raw hits; pauline-acts 4,743; anamnesis 2,686; gnostic-general 2,640; sophia 2,508 (A+C: 1,001).
- Site religion data: about 8.7 MB, one file per subsection, loaded on demand.

## The Bible pipeline

```bash
python curation/bible/sweep_bible.py --summary --out curation/bible/raw-findings.json
python scripts/studies/build_bible_study.py --check
python scripts/studies/build_bible_study.py
```

- `curation/bible/dossier_sections.py` is the single source: sections with
  `{{CARD-ID}}` markers, 39 cards (each located by `source` + `field` + `anchor` +
  `pith`, never by line), and topic metadata.
- The builder refuses to publish an unresolved marker, an anchor/pith that is not in
  the corpus, or a quotation of 40+ characters that is not in the corpus.
- The Bible study is **separate** from the religion study. It should eventually be
  reconciled: `Christianity > Scripture and the Bible` points at it in text only.

## Full-archive access: do this first

This repository holds only part of the archive. The current sweeps read exported
JSON and a few text files; they do **not** read the database. Once the full
archive is available:

1. **Locate the archive.** Check `database/` (here it held only `reference_data/`,
   `scenes_schema.sql`, `unified_schema.sql` and `source_pdfs/Maze notes.pdf`),
   `database/extracted_markdown/` (empty here, 183 files expected per the Burroughs
   curation README), and any path given by the user.
2. **Inventory the database.** `unified.sqlite` is git-ignored and built by
   `scripts/build_all.py`. The live schema drifts from `unified_schema.sql`
   (CLAUDE.md lists tables such as `claims`, `letters`, `theophanies`). Inspect with
   `sqlite_master` before querying. `scripts/research/sweep_corpus.py` already queries
   these tables (`segments`, `document_texts`, `page_texts`, `letters.body_md`,
   `claims`, `biography_events`, `works`, `pkd_on_pkd_mentions`, `evidence_excerpts`,
   `annotations`, `theophanies`, `timeline_events`). Reuse its `sweep_database` pattern.
3. **Add a database corpus to `sweep_religion.py`.** Priority order:
   - `letters.body_md`: this replaces the 1,500-character letter excerpts. It is
     the single most important upgrade. The Bible and religion findings from letters
     are currently a floor.
   - `document_texts.text_content` and `markdown_content`: the interviews, novels,
     stories and scholarship as full text. Interview transcripts are currently absent.
   - `page_texts.page_text`: per-page OCR of archive PDFs.
   - `claims` and `evidence_excerpts`: keep lanes as recorded in the table; do not collapse.
   - Keep the Exegesis analytic fields as lane D.
   Each new corpus needs a `lane` and `field_class`, as the existing corpora do.
4. **Repair the three malformed segment JSON files**, currently skipped:
   `SEG_EXEG_1976-09-15_Dorothy_214`, `SEG_EXEG_1978-10-10_SECTION_016_129`,
   `SEG_EXEG_1981-04-16_Pat_149`. `scripts/repair_malformed_segments.py` exists. Run it
   through the safeguard, not directly against `site/public/data`.
5. **Re-source the Bible sweep the same way**, or make the Bible study's findings a
   view over the religion database. The Bible study's card anchors will need checking
   after any re-sweep, because `build_bible_study.py` fails loudly if they move.
6. **Ingest the PDFs.**
   ```bash
   python scripts/research/ingest_pdfs.py --check
   python scripts/research/ingest_pdfs.py --src <archive dir> --doc-type <type> --lane <A|C|D>
   ```
   Install `tesseract-ocr` for image-only pages, then re-run with `--ocr force` on
   those documents. OCR is **untested** (tesseract was absent here).
   Assign lanes deliberately. Each lane change is an editorial decision.
   `Maze notes.pdf` reads like Dick's own notes; confirm before assigning lane A.
7. **Rebuild**: sweep, DB, study export, then `safe_export.py --exporter studies`
   if the studies exporter is what changed, then `check_data_diff.py --worktree`.

## Known problems and caveats

- **Letters.** `selected_letters_analysis.json` caps each `summary` at about 1,500
  characters, and a few letters keep their body in the `recipient` field. Every
  letter-based claim in the Bible study and the religion data is a floor. **Gnosticism
  README** describes the 1972–73 letters as a full corpus without mentioning the cap;
  that claim should be corrected.
- **Interviews.** Five archive records, each with a card and a summary. None mentions
  the Bible. No transcript is held. The Missouri Review interview has no summary at
  all. Any statement about what Dick said in interview is currently unsupported.
- **Stories.** Summaries only (30 stories). Six use religious vocabulary. None names
  the Bible. Full text needed.
- **Dates.** Exegesis dates are folder/batch dates. The 1978 folder (`SECTION_016`,
  10 October 1978) contains entries dated up to 12-29-80. Do not date single entries
  from the folder date.
- **Weak patterns are noisy.** `Elias`, `Paul`, `Law`, `Wisdom`, `Tao`, `fusion` (for
  Mercerism) and `demiurge` (Dick uses it generically) need reading. The browse page
  filters on tier. Expect a large share of false positives in the weak tier.
- **Christology volume.** "Christ" and "Jesus" produce about 8,500 raw hits. A full
  review needs sampling or a strategy (for example: review strong-tier, lane-A
  findings first, by decade).
- **Lane D is not browsed.** It is in the database. Do not add it to the site export
  without a decision: it paraphrases Dick.
- **No review decisions exist yet.** `editorial.json` is `{}`. Every browsed finding is
  shown as "unreviewed". The page says so; keep it that way until decisions exist.
- **Subsections have no prose.** Only the Bible study has an essay. Topic pages say
  "interpretive prose is not yet written".
- **Study label.** "Religion in PKD's Fiction" understates the study. An editor
  should rename it, by hand, in `site/public/data/studies/religion/index.json` via a
  reviewed change (the guard will object to a shortened label; a rename that
  lengthens or replaces the text may still need `--no-verify` or an allowlist
  entry, which needs the user's approval).
- **Maze notes lane.** Unassigned (lane D). Reads like Dick's notes.
- **Pre-existing 404.** `/vite.svg` is referenced by `index.html` and not present.
  Not caused by this work.
- **Gitignore.** `curation/religion/raw-findings.json` and `religion.sqlite` are
  ignored. A fresh clone must run the sweep and DB build before the religion
  development tools work. The site data is committed, so the site builds without them.

## Things already verified (do not redo unless the corpus changes)

- All 39 Bible cards resolve; all 14 Bible section markers resolve; every
  quotation of 40+ characters in the Bible prose appears in the corpus.
- All taxonomy patterns compile; all `related` topics resolve.
- The religion DB builds; FTS5 search works; the README's example SQL runs.
- `npm run build --prefix site` passes (typecheck + bundle).
- Headless Chromium: the Bible page renders 14 sections and 39 links; the religion
  browse page loads `sophia` with 1,001 rows in 40-row pages; the topic page lists
  subsections; no console errors beyond the `/vite.svg` 404.
- `check_data_diff.py --worktree` passed on the final religion commit.

## Environment notes for a new session

- `site/node_modules` is not present in a fresh container: run `npm ci --prefix site`.
- Chromium is at `/opt/pw-browsers/chromium`. Use `playwright-core` (install it
  in a scratch directory, not the repo). The site's `vite.config.ts` sets
  `base: '/QueryPat/'`, so a preview server must be opened at
  `http://localhost:4173/QueryPat/#/...`.
- Stop preview servers by port (`fuser -k 4173/tcp`). `pkill -f "vite preview"` kills
  the shell running the command.
- Scratch outputs go to the session scratchpad, not the repo. A stray file in
  `curation/bible/` was caught and removed once. Check `git status` before committing.

## Suggested order of work for the new session

1. Read `CLAUDE.md`, this file, and `curation/religion/README.md`.
2. Find the full archive; inventory `unified.sqlite` (`sqlite_master`) and `extracted_markdown`.
3. Add the database corpora to `sweep_religion.py` (letters first). Re-run the sweep; record the new baselines in this file.
4. Re-run the Bible sweep and checks; update card anchors if needed.
5. Ingest PDFs with lane decisions the user approves; install tesseract and test OCR.
6. Start review: `religion_review.py next --subsection <id> --lane A --unreviewed --strong-only`.
   Record decisions, rebuild, export, check.
7. Decide with the user: the study label; whether the Bible study folds into religion;
   whether lane D is ever browsed.
8. Write interpretive prose per topic, using the Bible study's section pattern and
   `{{CARD}}` citations. This needs a builder like `build_bible_study.py`, not hand edits.

## Files to read first

- `CLAUDE.md`, `docs/PRESERVATION.md`, `docs/RESEARCH_WORKLOG.md`
- `curation/religion/README.md`, `curation/religion/taxonomy.py`
- `curation/bible/README.md`, `curation/bible/dossier_sections.py`
- `curation/gnosticism/README.md` (the pattern the Bible study copied)
- `archive/2026-10-20/worklog/01-bible-corpus-sweep-and-study.md` and
  `archive/2026-10-20/worklog/02-religion-subsections-and-relational-browse.md`
