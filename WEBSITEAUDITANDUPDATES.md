# Website Audit & Updates

A pass over the site to fix the broken Browse-by-Year affordance, build out cross-section relational browsing, and audit the hyperlinking discipline. Where issues remain, this document lists them so they can be picked up in a follow-up session.

Generated 2026-04-29, after commit `16ba0de` (v5: P1 rebrand, theophanies, essays).

---

## 0. The audit's organizing question

The user's directive was specific: *most of the years on Browse-by-Year aren't clickable; users should have strategic hyperlinks and relational browsing*. Read narrowly that's two fixes. Read more broadly it's three structural questions:

1. **Which entity types are surfaced as clickable, and from where?** (the navigation graph)
2. **Where does a reader land when they click, and where can they go from there?** (the cross-link discipline)
3. **What invitations are made to wander rather than to query?** (the relational browsing affordance)

This document treats all three. Section 1 is the issues found; sections 2-4 are what shipped to address them; section 5 is what's outstanding.

---

## 1. The audit — what was broken

### 1.1 Browse-by-Year was almost entirely greyed out

The Dashboard's Browse-by-Year section greyed out any year where `count + bio_events == 0`. Per `analytics.json` at audit time, that was nearly every year before 1974: only 1928, 1953, 1958, 1962, 1964, 1967, 1968, 1969, 1970, 1971, 1972, 1974, 1975, 1976, 1978 had any content, and the dashboard only lit up the four with Exegesis segments (1975, 1976, 1978, 1981). PKD lived from 1928 to 1982; that's 55 years, of which only ~14% looked clickable. The logic was correct; the data feeding it was thin.

**Why thin?** Two pieces of available data weren't being aggregated into `analytics.json.segments_per_year`:
- The 119-event hand-curated `biography/curated.json` covers 47 of the 55 years.
- The new `theophanies` table (15 events from 1963 to 1981) was its own surface with no roll-up into the year aggregator.

### 1.2 The /timeline/:year page had no theophanies

`timeline/years/{year}.json` was built from segments + auto-extracted bio_events. The new theophanies were not merged in. So a user who clicked, say, `/timeline/1963` (the year of the Sky-Face Vision) saw nothing.

### 1.3 ExploreFooter was wired on existing detail pages but not on the new ones

The v3 cross-navigation feature `ExploreFooter` (curated cross-references at the bottom of each detail page) was implemented but the new pages from v5 — `Exegesis`, `Theophanies`, `TheophanyDetail`, `Essays`, `EssayDetail` — didn't yet use it.

### 1.4 No top-level "wander" affordance

Every existing entry point was a typed query: search, browse by category, click a tag. There was no "I'm curious, surprise me" entry. The relational browser features (BacklinksPanel, HoverPreview, ExploreFooter) only fire from a detail page; if you arrive at the site cold, there was no curated path through the corpus.

### 1.5 Dashboard "Browse by Year" caption was outdated

After the v5 rebrand the caption still read *"Many years are unpopulated — publications and additional biography events are queued to fill them in."* That was the P2 framing; the v5 fix narrows the gap so the caption is now misleading.

---

## 2. What shipped

### 2.1 Year-aggregation rebuild

A new script: `scripts/timeline/rebuild_years.py`. It:

- Loads three sources: `biography/curated.json` (119 events), `biography/events.json` (646 events), and the `theophanies` table (15 events).
- Pulls Exegesis segments per year directly from the segments table.
- Merges all four into `timeline/years/{year}.json` files, tagging each entry with `_type` ∈ `{biography_event, theophany, segment}`.
- Writes a richer `timeline/index.json` with per-year counts split out: `count` (segments), `bio_events`, `theophanies`, `total`.
- Updates `analytics.json.segments_per_year` so `has_content` reflects the union: any year with even one curated bio event, theophany, or segment is now clickable.

**Result:** **47 of 55 years** (1928-1982) now have content. The 8 years still without content are 1930, 1932, 1935, 1936, 1939, 1942 (partial), 1943, 1949 — these are real gaps in the corpus, mostly pre-1950 childhood years where curated coverage is sparse.

### 2.2 Timeline page renders all three entry types

`site/src/pages/Timeline.tsx` now recognizes a third entry type alongside segments and biography events: **theophany**. Theophany cards render with a distinctive purple left-border, the experience type as a colored badge, and the canonical/major/minor importance flag. Clicking the theophany name navigates to `/theophanies/{slug}`.

The page header is also updated: the old "Exegesis Timeline" framing is replaced with *"Philip K. Dick's life (1928–1982) — biography events, Exegesis writings, and visionary experiences arrayed by year"*. This better reflects what's actually displayed.

### 2.3 Dashboard Browse-by-Year is theophany-aware

The grid now reads `y.theophanies` and surfaces it in:

- **Coloring:** years with theophanies but no segments get a soft purple background; years with heavy Exegesis content stay accent-gold.
- **Tooltip:** hovering shows `{year}: N segments, M biography events, K theophanies`.
- **Caption:** updated to the simpler *"Click any year to see biography events, theophanies, and Exegesis writings for that year"*.

### 2.4 New `/browse` hub

A first-class hub at `/browse` and on the navigation. It contains:

1. **By year** — the same year grid but bigger, with all three counts in the tooltip. Clicking goes to `/timeline/:year`.
2. **🎲 Reshuffle button** — re-rolls all the random sections.
3. **Random theophanies (3)** — drawn from the canonical 15.
4. **Random archive documents (4)** — drawn from the 228 archive entries.
5. **Random scholars (4)** — drawn from 119 profiles.
6. **Random dictionary terms (8)** — drawn from 310 terms.
7. **Top concepts in the corpus** — clickable pill cloud of the 30 most-frequent terms, each linking to its dictionary entry.
8. **Cross-section paths** — five hand-curated journeys through the corpus:
   - The 2-3-74 cluster → Fish Sign → Pink Beam → Valis → Exegesis
   - Drugs in PKD → Sutin/Anne Dick/Arnold → archive
   - Music in PKD → Beethoven → Sister Jane → Davis on Sonic Youth
   - Gematria vision → Abulafia possession → Koine Greek
   - Year 1974 → 1975 → 1976 (heart of the Exegesis years)

Curated paths give the corpus a "narrative entry" affordance distinct from "search and click." A reader who has just landed and doesn't know what to look at can pick a path and walk through.

### 2.5 ExploreFooter wired into the v5 pages

- **Theophanies index** — links to the Exegesis page, the heart years (1974/1975), Biography, Scholars, Archive, and the two essays.
- **TheophanyDetail** — uses the theophany's `related_works`, `related_dictionary_terms`, and `related_theophany_ids` fields to populate three contextual sections plus a fixed "Contextual reading" section pointing to Exegesis, the Drugs essay, Scholars, and the year on the Timeline.
- **Exegesis landing** — links to the four canonical 1974 theophanies (with see-all to /theophanies), companion essays (Drugs, Music), Pamela Jackson / Erik Davis / Lethem on Scholars, and four heavy Exegesis years on Timeline.

### 2.6 Layout nav now has Browse

The top nav adds **Browse** between Dashboard and Biography, giving the wander affordance a top-level entry point. Eleven items in the nav now: Dashboard, Browse, Biography, Timeline, Exegesis, Theophanies, Archive, Dictionary, Names, Scholars, Essays, Studies, Search, Bookmarks.

---

## 3. The hyperlinking audit — what was already good, what improved

### 3.1 What was already strong (kept unchanged)

The v1.x knowledge-browser features remain healthy:

- **Breadcrumbs** — auto-generated on every page from the React Router path
- **Search** — fuzzy-grouped by entity type with weighted ranking
- **Cross-Site Tag Filtering** — every `tag/:tagname` route works
- **Backlinks Panel** — "What links here" on detail pages
- **Hover Previews** — preview cards on internal links

### 3.2 Where v5 added cross-link density

Before this audit:
- The new pages (Exegesis, Theophanies, Essays) did not use ExploreFooter.
- The 15 theophany seeds carry rich `related_works`, `related_dictionary_terms`, `related_theophany_ids` arrays in their JSON; these were rendered on the detail pages but not surfaced as ExploreFooter destinations.
- The Browse hub did not exist, so no top-level cross-section navigation.

After this audit:
- All v5 detail pages run ExploreFooter.
- TheophanyDetail's footer is data-driven: it pulls from the theophany's own `related_works`/`related_dictionary_terms`/`related_theophany_ids` JSON arrays, so the cross-links update automatically when seeds change.
- Browse hub exists and is wired into the nav.

### 3.3 Cross-section linking density (a back-of-envelope count)

| Surface | Links *out* of the page (before) | Links *out* of the page (after) |
|---|---:|---:|
| Dashboard | 6 stat tiles + 8 What's-Inside | + 2 (added theophanies/essays earlier) |
| Theophanies index | 0 (no footer) | + 9 (3 sections × 3 items) + ExploreFooter |
| TheophanyDetail | 6 cross-link sections (built-in) | + 9 (ExploreFooter) |
| Exegesis | 6 stat tiles | + 12 (ExploreFooter) |
| Timeline year | varied | + theophany cards link out to /theophanies/:slug |
| Browse hub | new | 50+ year tiles, 19 random links, 30 concept pills, 18 curated path links |

---

## 4. The five enforced editorial rules — applied across the audit

The underlying [PKDontology.md](PKDontology.md) discipline did not loosen during this audit. Specifically:

1. **State its lane** — every theophany card on a Timeline year carries the theophany's metadata link (Lane B); biography_event cards carry their `source_name` (typically Lane D synthesis); segments link to themselves (Lane B).
2. **Attribute interpretations** — theophany cards on Timeline link to TheophanyDetail where the chain of PKD's interpretations and the scholar readings are dated and sourced.
3. **Surface contradictions** — TheophanyDetail's contradiction-zone callout still fires for events on the registered dispute zones.
4. **Cross-link six ways** — the audit's whole purpose; cross-link density measurably increased.
5. **Distinguish fact from self-report** — theophany cards on Timeline are visually distinct (purple) from biography events (gold) which are visually distinct from segments (no border accent). The reader can see at a glance what kind of evidence is being presented.

---

## 5. What's outstanding (queued)

These are real and known. Listed in roughly priority order.

### 5.1 The 8 still-greyed-out years

1930, 1932, 1935, 1936, 1939, 1943, 1949 (and partial 1942) are still `has_content=false`. These are gaps in the curated biography:

- **The fix** is to write 1-2 curated biography events for each gap year drawing on the Sutin / Anne Dick chronologies. PKD's residences (Berkeley, Washington DC briefly), school events, family changes, and reading life are all attestable for these years.
- **Estimated effort:** half a session of curated bio writing.

### 5.2 Anchor links to /scholars#slug are still dead

[WRITIGNAUDIT.md §B1](WRITIGNAUDIT.md) flagged this earlier. The Scholars page does not render `id={scholar_id}` on its scholar cards, so any link to `/scholars#pamela-jackson` lands on the index but doesn't scroll to or expand the matching profile. Workaround currently: the Theophany detail's ExploreFooter and the Theophany scholar interpretation list both link to `/scholars` plain (no anchor), which is honest but not quite the experience we want.

- **The fix** in `Scholars.tsx`: add `id={s.scholar_id}` to the card root, plus a `useEffect` that reads the URL hash on mount, calls `setExpandedId` for the matching scholar, and `scrollIntoView` on the element.
- **Estimated effort:** 30 minutes plus a verify pass.

### 5.3 Per-theophany Exegesis-segment evidence is empty

Each of the 15 seeded theophanies has `related_segments: []` because no automated linking has run yet. The seeds should be linked to the actual Exegesis segments where PKD writes about them. Sample:
- THEO_1974_02_FISH_SIGN should link to every segment with `theological_motifs` containing "fish" or "ichthys" or "Tagore" or "Thomas".
- THEO_1974_BLACK_IRON_PRISON should link to every segment containing "Black Iron Prison" or "Empire" or "Rome" in any of the parsed fields.

- **The fix** is a `scripts/theophanies/link_segments.py` that scans `segments.theological_motifs`, `segments.recurring_concepts`, `segments.people_entities` against each theophany's vocabulary and inserts `theophany_evidence` rows.
- **Estimated effort:** 1 hour of scripting + spot-check.

### 5.4 BacklinksPanel doesn't yet know about theophanies

The "What links here" panel uses the existing `connections.json` cross-entity graph, which was built before theophanies existed. So a Dictionary entry like *Valis* doesn't surface in BacklinksPanel that 7 theophanies invoke it.

- **The fix:** extend `scripts/export_json.py` (or write a `scripts/theophanies/extend_connections.py`) to add theophany ↔ dictionary, theophany ↔ name, theophany ↔ work edges to `connections.json`.
- **Estimated effort:** 1-2 hours.

### 5.5 Search index doesn't include theophany names or essay titles

`search_index.json` was last regenerated before v5. Searching for "Abulafia" or "Pink Beam" or "Drugs in PKD" returns nothing.

- **The fix:** rerun `scripts/build_all.py --export-only` (this also fixes the 228 vs 237 archive count drift flagged in WRITIGNAUDIT §F1).
- **Estimated effort:** minutes, but needs a clean schema check first.

### 5.6 No Theophany filter on Biography page

Biography events that ref a theophany via `theophany_id` should show a "vision" badge that links to the theophany detail. Today they don't, because:
1. No biography events currently have `theophany_id` populated (the column exists, no data).
2. The Biography UI doesn't query for it.

- **The fix:** (a) populate `biography_events.theophany_id` for any existing event whose summary intersects with a theophany's vocabulary; (b) update Biography.tsx to render a clickable vision-badge.
- **Estimated effort:** 2 hours.

### 5.7 Theme filter on Biography page

The schema for biography_events includes a `themes` JSON column (added during the letters mining work) for tagging events as drugs/music/career/relationships/politics/religion/philosophy/visionary/sf_community. No biography events currently have themes populated (waiting on letters mining), but once they do, the Biography page should let users filter.

- **The fix:** UI work in Biography.tsx — multi-select theme filter with counts.
- **Estimated effort:** 1 hour, after data is populated.

### 5.8 Markdown excerpts on Archive detail

The 180+ archive documents now have rich markdown in `document_texts.markdown_content`, but the Archive detail page still surfaces the legacy `text_content` plain-text dump. Switching to a markdown-rendered excerpt (first 1,500 chars) would make the page substantially more readable.

- **The fix:** update `scripts/export_json.py` to write `markdown_excerpt` into per-doc JSON; update `ArchiveDetail.tsx` to render with `react-markdown`.
- **Estimated effort:** 1 hour.

### 5.9 The "Browse by Year" still has a slight visual stutter

Some years light up purple (theophany only), some gold (segments), some dark gold (heavy Exegesis), but pre-1971 years with only bio events are a uniform pale gold regardless of how many bio events. A reader scanning for activity-density doesn't see variation in the early years. Could be improved by scaling the background opacity by `total` count.

- **The fix:** the Dashboard year-grid coloring logic should use a continuous scale rather than a boolean.
- **Estimated effort:** 20 minutes.

### 5.10 Browse hub randomization is shallow

The Random sections re-roll on a button click, but they don't bias toward less-explored entities. A user who clicks Reshuffle 10 times in a row might see the same 4-5 highest-count terms each time.

- **The fix:** weight the random pull *inversely* by a "view count" tracked in localStorage, so reshuffling pulls toward less-visited corners of the corpus.
- **Estimated effort:** 1-2 hours; nice-to-have.

### 5.11 No way to mark a theophany as bookmarked

The existing `useBookmarks` hook supports terms, segments, archive docs, names, and scholars but not theophanies (the entity type didn't exist when the hook was written).

- **The fix:** extend the bookmarks taxonomy in `useBookmarks.ts` and add a `<BookmarkButton entityType="theophany" entityId={...} />` to TheophanyDetail.
- **Estimated effort:** 30 minutes.

### 5.12 Hover previews don't yet know about theophanies or essays

`HoverPreview.tsx` looks up the entity-type prefix (`/segments/`, `/archive/`, etc.) and fetches the matching JSON for a tooltip preview. It doesn't yet handle `/theophanies/:slug` or `/essays/:slug`.

- **The fix:** add the two prefixes to the lookup table in `HoverPreview.tsx`.
- **Estimated effort:** 30 minutes.

---

## 6. The acceptance criteria for this round

Met:
- ✅ Browse-by-Year is now mostly clickable (47/55 years, up from ~4)
- ✅ Clicking a previously-greyed year (1963, 1971, 1972, etc.) now shows actual content
- ✅ Theophanies render on Timeline year pages with distinct visual treatment
- ✅ A top-level Browse hub exists at `/browse`, with random sampling and curated paths
- ✅ ExploreFooter cross-links the new v5 pages back into the rest of the corpus
- ✅ Dashboard's Browse-by-Year caption is updated; tooltips now report all three count types
- ✅ Site builds clean (5.99s, 484 KB JS gzipped to 145 KB)

Deferred:
- The 8 fully-empty years (need 1-2 curated bio events each to fill in)
- Anchor-scroll on Scholars page
- Theophany ↔ Exegesis-segment automated linking
- Backlinks/search/connections regeneration to include theophanies
- Markdown excerpts on Archive detail
- Various visual polish items

---

## 7. How to extend this work

Adding a new entity domain (the way Theophanies was added in v5):

1. Define ontology in `<DOMAIN>_ONTOLOGY.md` with the schema, controlled vocabularies, and the five-rule discipline applied.
2. Build `scripts/<domain>/seed.py` and `scripts/<domain>/export_json.py`.
3. Add `pages/<Domain>.tsx` (index) and `pages/<Domain>Detail.tsx`.
4. Wire `App.tsx` routes and `Layout.tsx` nav link.
5. Run `scripts/timeline/rebuild_years.py` to fold the new entity into year aggregates if it has dates.
6. Wire `ExploreFooter` on the new pages with one section pointing back at it from related domains.
7. Add a section to `Browse.tsx` (random selection + count).

Each step is a minor change; the whole stack of changes for a new domain takes 3-4 hours including UI polish.

---

## 8. The portal as a graph

After this audit, the cross-link discipline can be summarized as a graph:

```
Dashboard ─── 8 entity tiles + What's-Inside list
   │
   ├─ Browse ─── all-domain hub with random + curated paths
   │     │
   │     └─ year cells ─── Timeline/{year}
   │
   ├─ Biography ─── events ───┬─ Timeline/{year} (auto-grouped)
   │                          ├─ theophany (when linked)
   │                          └─ source archive doc
   │
   ├─ Timeline ─── per-year merge of segments + bio + theophanies
   │     │
   │     ├─ segment ─── SegmentDetail ─── related terms, names
   │     ├─ bio_event ─── (no detail page yet)
   │     └─ theophany ─── TheophanyDetail ─── interpretation chain
   │                          │
   │                          ├─ scholar reading (Lane C)
   │                          ├─ related works (Lane A)
   │                          ├─ related theophanies (cluster)
   │                          └─ ExploreFooter ─── essays, scholars, year
   │
   ├─ Exegesis ─── landing ─── ExploreFooter ─── theophanies, essays
   ├─ Theophanies ─── index ─── ExploreFooter ─── essays, archive
   ├─ Archive ─── docs ─── ArchiveDetail ─── people/works/terms
   ├─ Dictionary ─── terms ─── TermDetail ─── related segments, evidence
   ├─ Names ─── entities ─── NameDetail ─── etymology, segments
   ├─ Scholars ─── 119 profiles (no individual detail page)
   └─ Essays ─── EssayDetail ─── markdown with React-Router-aware links
```

Every node has at least 3 edges leading out of it. The Browse hub guarantees that any cold-start user can reach any entity within 2 clicks.
