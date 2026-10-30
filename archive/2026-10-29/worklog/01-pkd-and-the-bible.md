# Worklog — 2026-10-29 — Philip K. Dick and the Bible

## What was asked

> "How can we improve our page on PKD and the Bible"

then, after a written assessment:

> "I'll trust you to go ahead and make the various improvements be sure that we
> are featuring every aspect about what's interesting about PKD's approach to the
> bible in our presentation of frontend functionality like search and clicking
> around and relational browsing of various aspects"

## Starting point

The only page was `/dictionary/bible`, a machine-drafted term entry: a generic
definition, an unsourced one-line interpretive note, no caution, `first_appearance`
1975-02-27 (the earliest *Exegesis* hit, though letters mention the Bible from
1962), and 74 related terms that were mostly co-occurring function words
(Because, Like, Since, Therefore, These, Well). No study topic existed.

## Corpus searched

`scripts/research/sweep_corpus.py` gained a `bible` profile (Bible, scripture,
Testament, named editions, named books, Qumran/Nag Hammadi; weak tier for Torah,
gospel, prophets, verse references). Full sweep: 23,285 findings, 7,766 strong.
Strong tier archived as `research/2026-10-29_pkd-bible-raw-findings.json.gz`.

Read directly, theme by theme: Exegesis segments (sections 010–017), all 47
letters naming the Bible, the 1978 speech, the Rickman interview, the VALIS
trilogy text (VALIS, The Divine Invasion, The Transmigration of Timothy Archer),
Ubik, A Scanner Darkly, Deus Irae, and the scholarship hits (Sutin, Butler,
Theory Culture & Society 2008, Tseng, Extrapolation 2011, Davis, Kripal).

Not used: the 348 rule-extracted `claims` rows mentioning the Bible — all
`unreviewed`, extractor `claim-ir@0.1.0-prototype`.

## Discoveries

- **Dick knew the Bible well before 2-3-74**, against his own 1976 statement to
  his mother that he was "almost totally unfamiliar with the Bible" in 1974: the
  Elijah radio serial in junior high (Rickman interview; corroborated by Sutin's
  Bible Club anecdote), Paul's "glass darkly" in a 1962 letter to Boucher, the
  rhymed-couplets Bible joke of 1972–73, the Scanner Darkly title explained as a
  pun on Paul (31 March 1973), and three translations of 1 Cor 15:51 compared for
  his agent (11 September 1973).
- **Five translations in use**: King James, the Jehovah's Witnesses' New World
  Translation, the New English Bible, the Jerusalem Bible (cited in the
  Transmigration bibliography and quoted with its notes in January 1981), the
  Vulgate (Dilexi, his wished-for epitaph).
- **The Acts discovery's dated trail**: earliest dated statement in this archive
  is the 11 July 1975 letter to Göran Bengtson; public version in the 1978 speech.
- **Wisdom of Solomon** reached him via the Episcopal Church's recommendation of
  the apocrypha (letter of 17 September 1975), and supplies St. Sophia.
- **Bible-as-code appears first in fiction** — the To Scare the Dead outline to
  Ornstein (4 March 1975) — before the Exegesis states it (1976–79).

## Contradictions kept (7)

Prior knowledge (1976 letter vs 1962–73 letters); had he read Acts (Dick allows a
forgotten reading, Butler denies any); Bible dispensable (Jan 1975) vs alive
(1978–80); code vs incomplete code; which God (1977 / late 1980 / April 1981);
Bishop Archer as Christ figure vs lawyer; one Jason in the Bible (Dick) or two
(Butler).

## Decisions

- **Study placement.** A `religion` study exists only as orphaned JSON under
  `site/public/data/studies/religion/` — not in the `studies` table, not in
  `studies/index.json`, so not reachable from the site. Rather than entangle the
  new topic with it, the topic went into `intertexts`, whose description was
  widened from "writers and thinkers" to "writers, thinkers and texts".
- **Dating.** Section 016's container date (1978-10-10) is known wrong for many
  passages; its cards say "1978–80" unless a stamp (`11-17-80` → "After November
  1980") or folder (21 → Autumn 1978) narrows them. `SEG_EXEG_1976-09-15_Dorothy_81`
  carries 11/19/77 and 3/25/79 stamps, so its two cards are "1976–79".
- **Browse config is data, not code.** The Burroughs page's card groups are
  hardcoded in `MentionCards.tsx`. The Bible page's groups and facets are authored
  in `dossier_sections.py`, stored in a new `study_topics.browse_config` column,
  and exported as `browse`. Burroughs keeps its legacy groups.
- **Fiction is lane A.** Cards from novels quote characters, never Dick; Dick's
  later claims *about* the novels stay in his own lanes.
- **Promoted three background terms** (Revelation, Malachi, Qumran) with short
  reviewed definitions so facet chips do not link to missing pages.

## Files changed

Curation: `curation/pkd-bible/` (findings, essay, builders, README).
Pipeline: `scripts/studies/seed_pkd_bible.py` (new; reuses the Burroughs
extraction/verification code), `scripts/studies/export_studies.py` (`browse`
field; new `studies/links.json` reverse index), `scripts/index_study_search.py`
(new post-export pass: `study` and `passage` search entries),
`scripts/safeguard/safe_export.py`, `scripts/build_all.py`,
`scripts/research/sweep_corpus.py`, `database/unified_schema.sql`.
Site: `MentionCards.tsx` (facet chips, lane filter, URL-backed filters, deep links
under the HashRouter), new `StudyBacklinks.tsx` (term, name, segment, archive and
Exegesis-work pages), `TopicDetail.tsx` (contents nav), `CitedText.tsx`,
`Search.tsx`, `App.css`.
Data: new topic JSON, `studies/links.json`, three new term files; `bible.json`
and four `dictionary/index.json` rows hand-placed; search index extended.

## Validation

- `seed_pkd_bible.py --check`: 76 passages resolve; every pith and all 13 essay
  quotations of 40+ chars verbatim; 75 of 76 findings cited in the essay.
- `safe_export.py --exporter all`: 1,081 destructive changes auto-restored; the
  remaining diff hand-reviewed and reverted to the intended files only.
- Post-export passes: 0 claim leaks, 0 junk descriptions, 0 dead links.
- `check_data_diff.py --worktree`: flags only the intended removals (Bible's
  machine card text, see_also and junk related terms).
- `npm run build`: passes.
- Browser: dossier renders; Acts chip filters to 15 cards and writes
  `?facet=Acts`; search "glass darkly" returns 4 dossier passages that open on
  their card; backlinks on /dictionary/acts, /dictionary/malachi, Flow My Tears,
  a segment and /names/elijah; no console errors; no horizontal scroll at 375px.

## Unresolved

See the dossier's open questions: his pre-1974 Bible editions, whether he read
Acts before 1974, the Doris/Sherri duplicate letter, the source of the Philo
quotation, the 1978/1980 split of section 016, "Paul's" Acts.
