# Study dossiers: the authored-topic standard

Two kinds of study topic coexist in `site/public/data/studies/`:

- **Lexicon-scanned topics** (most of `ai/` and `psychology/`): passages found by
  matching a word list against the corpus, grouped into one or a few evidence
  packets, with machine-drafted dossier fields. Many are `scanning` status.
- **Authored dossiers** (`intertexts/burroughs-word-virus`,
  `intertexts/pkd-and-the-bible`, `psychology/drugs-in-pkd`, the `gnosticism/`
  topics): every passage chosen
  by reading it, summarised on a card, quoted verbatim, dated with its basis,
  cited inline from an essay, and seeded from `curation/<topic>/`.

This page describes what an authored dossier carries and how it plugs into
search and relational browsing, so a lexicon topic can be brought up to it.

## What a dossier carries

| Piece | Where it is authored | Where it lands |
|---|---|---|
| Findings: anchor, window, card context, verbatim pith, date + basis, concepts | `curation/<topic>/findings.py` (Bible) or `build_inventory.py` + `mention_cards.py` (Burroughs) | `study_passages`, `study_topics.mention_cards` |
| Essay with `{{finding-id}}` citations and a register per section | `dossier_sections.py` | `study_topics.dossier_sections` |
| Contradictions as passage pairs | the seeder or `dossier_sections.py` | `study_contradictions` |
| Browse config: groups and facets | `dossier_sections.py` or `dossier.json` → `browse` | `study_topics.browse_config` → topic JSON `browse` |

The seeders refuse to build if an anchor fails, a pith or a 40+ character essay
quotation is not verbatim in its source, or a citation does not resolve.

## Browse config

```json
{
  "intro": "{n} passages ...",
  "groups": [{"key": "ex1976", "label": "...", "blurb": "..."}],
  "facet_kinds": [{"kind": "book", "label": "Books of the Bible"}],
  "facets": [{"label": "Acts", "kind": "book", "link": "/dictionary/acts",
              "aliases": ["Book of Acts"]}]
}
```

- A facet matches a card when its label or an alias is in the card's `concepts`.
- `groups` is optional; cards carry `group`. Without it the topic's
  `mention_groups` (cards carry `group_key`), then the Burroughs defaults, apply.
- Filters live in the URL (`?facet=Acts&lane=E`), so a filtered view is a link.
- The site runs on a **HashRouter**: in-page anchors must scroll in JS, and the
  anchor is `useLocation().hash`, never `window.location.hash`.

## How a dossier reaches the rest of the portal

- `studies/links.json` (written by `export_studies.export_links`) maps term,
  name, segment, archive-document and Exegesis-work slugs to the dossiers that
  discuss them. A facet with a `link` gives that page a precise backlink
  ("15 passages on Acts", opening the dossier filtered). `StudyBacklinks`
  renders it on those five page types.
- `scripts/index_study_search.py` (a post-export pass in `safe_export.py`) adds a
  `study` entry per dossier and a `passage` entry per card to the search index;
  a passage result opens on its card.
- Only topics with `mention_cards` are indexed in either, so every backlink and
  passage result lands on something an editor has read.

## Bringing a lexicon topic up to standard

1. Sweep (`scripts/research/sweep_corpus.py --profile <name>`) and classify by
   reading; record false positives rather than publishing them.
2. Write findings and cards; date each with a basis.
3. Write the essay with citations and registers; record contradictions.
4. Author `browse` facets that link to existing dictionary, name and work pages.
5. Seed, `--check`, export the topic file directly, run the post-export passes,
   and hand-place — never a bare re-export (see CLAUDE.md).
6. Fix the lexicon topic the dossier supersedes rather than leaving it to
   contradict the dossier: narrow its word list, rescan it, give it an
   `editorial_notes` line and a `related_topics` link to the dossier (see
   `.claude/rules/lexicon-topics.md`; the drugs seeder does this for
   `amphetamine-use` and `addiction`).
7. Correct and link the curated biography events the dossier touches
   (`curation/biography/`, `.claude/rules/biography.md`).

The schema constraints, the export procedure and the pitfalls met so far are in
`.claude/rules/study-dossiers.md`. The newest complete example is
`curation/drugs-in-pkd/` with `scripts/studies/seed_drugs_in_pkd.py`.
