# Worklog — 2026-10-29 — reconciling the two Bible studies

## What was asked

> "Yes, reconcile them" — the unmerged branch `bible-religion-continue`
> (2026-10-20: "The Bible in PKD" study at `/studies/bible/bible-in-pkd`, and the
> Religion browse layer) with the live dossier `/studies/intertexts/pkd-and-the-bible`.

## What the branch held

- A Bible study: 20 sections, 64 cards, its own builder (`build_bible_study.py`)
  writing JSON directly, a 16 MB committed sweep file, a "Bible" nav tab.
- A Religion study: 14 topics, 34 subsections, ~16,300 browsable lexicon findings
  (all unreviewed), `ReligionBrowse.tsx`, a "Religion" nav tab.
- Built in a cloud container without `unified.sqlite`: letters were read from
  summaries capped at ~1,500 characters (its handover says so), so its letter
  findings were a floor.

## Decision

One Bible study, the live database-backed one, keeping its URL. The branch's
Bible cards were checked against the full texts and merged into it; the Religion
browse layer was merged as built, and cross-linked.

## How the 64 cards were handled

Each pith was searched in `segments.raw_text`, `letters.body_md` and
`document_texts`; each passage was read against its card summary.

- 50 ported into `curation/pkd-bible/findings.py` (section 9), with new ids,
  exact anchors, the dossier's facet vocabulary, evidence packets and dating rules.
- 10 duplicated passages the dossier already had.
- 3 did not resolve in this archive's texts (the Davis talk on the Acts of Thomas,
  the Theory, Culture & Society quotation, the "Ruah" interview line); recorded as
  an open question.
- 1 dropped (a Rosicrucian archive record restating the VALIS appendix).

Corrections the full sources forced:

- The rhymed-couplets letter is to **Patrice Duvic, 28 November 1972**, not Roger
  Zelazny on 1 December (the excerpt file had misattributed it).
- "I had never read Acts" sits in a segment filed with September 1976 but refers
  to cracking a message "3 weeks ago (June 1978)": dated mid-1978.

## What the essay gained

Two new sections — *Recombinant scripture and a third testament* and *The Torah,
and a turn to Judaism* — and additions throughout: the 1964 priest's formula (which
Deus Irae gives to Pete), the first Bible he read being the Old Testament,
"unmistakable material from Acts", Luke–Acts, the Bible as a world (1975 and 1981),
the Living Torah, the encoding-decoding grid, "Letters from home", Hertz's
Pentateuch as a sixth edition, the lost Trinitarianism, the short stories.

Three contradictions added: Dick's two answers on whether he had read Acts; the Old
Testament scorned (1975) and revered (1980–81); "switched from Christianity to
Judaism" against "finally got back to Christianity".

Totals: 126 cards, 15 sections, 13 packets, 10 contradictions; 33 essay quotations
of 40+ characters verified verbatim.

## Site changes

- `/studies/bible/*` redirects to the dossier; the separate `studies/bible/` output
  and the 16 MB sweep file were not carried over (sweep git-ignored, as the
  religion sweep already was).
- Nav: one Bible tab (the dossier) and the Religion tab.
- Bible browse panel gains "See also" links to Religion (Scripture and the Bible,
  Judaism, Hebrew prophets), Gnosticism and Burroughs; the Religion
  *Scripture and the Bible* subsection now points at the dossier.
- `index_study_search.py` indexes every study topic (Religion, AI, psychology
  included) and drops the branch's unrouted `study_topic` entries.
- `build_bible_study.py` refuses to run without `--force`; `curation/bible/README.md`
  explains the supersession.

## Not done

- The Religion study is still JSON-only (not in the `studies` table), so a bare
  studies export would drop it from `studies/index.json`; the guard would restore it.
- Religion findings are unreviewed lexicon hits; the browse page says so.
- The Religion study's label, "Religion in PKD's Fiction", understates it; left for
  an editor.
