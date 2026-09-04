# Worklog — 2026-09-04 — card summaries, per-passage dating, grid width

## What was asked

> "I'd like the summaries of the contents of the passages in the cards to be a
> bit longer. I like how the passages can be opened accordion style"

following on from:

> "make sure that the summaries cover all the content of Dick's remarks in all
> the evidence provided."

## What was done

**1. All 64 mention-card summaries rewritten and expanded.**

The old summaries were one or two sentences apiece — enough to say what a passage
was about, not enough to say what Dick actually argued in it. Each card now
carries 140–220 words covering the whole of the passage's content: the argument
Dick is making, the works and figures he invokes on the way, the qualification or
reversal he attaches, and where the passage sits against the ones around it.

Written in two batches through a temporary generator (`_expand_contexts.py`,
`_expand_contexts2.py`) that re-emitted `mention_cards.py` deterministically with
group comments, so the diff stayed readable. Both helpers were deleted once the
last batch landed; they exist only in this session's history.

Card word counts: min 138, median 172, max 220.

**2. Dating extended to the letters and the secondary sources.**

`DATING` in `build_inventory.py` previously covered only the Exegesis passages, so
37 of 64 cards carried a date badge. Added two new bases:

- `dateline` — the letter's own date as printed in the *Selected Letters*
  volumes. Thirteen cards. These are the firmest dates in the dossier and the
  reason the essay can be chronological at all.
- `publication` — the year of a secondary source, which is emphatically *not* the
  year of Dick's remark. Six cards (Sutin 1989, the 2011 Jackson & Lethem
  glossary).

Deliberately left undated: Lapoujade, Butler, the Davis blurb, the Rickman
interview and `BWV-EXP-90-6A`'s underlying folio — our citations for these carry
no year, and the badge means *attested by the source*, not *guessed by us*.

Coverage is now 56 of 64.

**3. The badge tooltip now says how the date was arrived at.**

It used to read "dated from the record", which told a reader nothing. Each basis
now has a sentence — `DATING_BASIS` in `MentionCards.tsx` — and the two that
carry a warning say so: `record` notes that nothing in the passage confirms it,
`publication` notes that the year belongs to the scholar, not to Dick.

**4. Grid width.**

At ~200 words per summary the existing `minmax(330px, 1fr)` produced three narrow
columns and cards a thousand pixels tall. Now `minmax(min(100%, 26rem), 1fr)`:
two 511px tracks, cards ~700px, line lengths that can actually be read. Cards
still stretch to equal heights per row, which keeps the bordered boxes tidy.

## Verification

- Seeder gates all passed: 64 passages resolve to their anchors, every pith
  verbatim against source text, every essay quotation ≥40 chars verbatim, all 64
  `{{id}}` citations resolve, no orphan evidence packets.
- `safe_export.py --exporter studies --allow-path studies/intertexts/` — the
  studies exporter *still* nulls dossier prose on 28 unrelated topics; all 28
  were auto-restored from the pre-export snapshot and only the Burroughs file
  changed. The underlying exporter bug is unfixed and documented in
  `docs/PRESERVATION_AUDIT.md`; the guard is what makes it survivable.
- `npm run build --prefix site` — clean.
- `scripts/audit.py` — no new warnings.
- Browser check against the dev server: two-column grid, folio and date badges,
  accordion opens, tooltip text correct.

## Known, not fixed here

- `artifacts/validate_artifacts.py` crashes with
  `AttributeError: 'list' object has no attribute 'get'` at line 288 — an
  artifact file whose top level is a list rather than an object. Pre-existing;
  nothing in `artifacts/` was touched by this work.
- Screenshots taken deep into this page (~30,000px document) come back blank
  from the browser pane's capture. The DOM is laid out correctly at those
  offsets; it is a capture limitation, not a page defect. Verified instead by
  measuring `getBoundingClientRect` and by temporarily hiding the essay so the
  cards sat near the top of the document.
