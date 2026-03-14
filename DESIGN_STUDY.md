# QueryPat Design Study — Interface & Architecture Decisions

Prepared in response to 20 design questions about making QueryPat into an accessible, beautiful relational browser for the PKD Exegesis database. Organized by topic.

---

## 1. Graph View vs. Relational Linking

**Current state:** QueryPat uses text-based relational linking — clicking an entity tag on a biography card navigates to the dictionary, clicking a term shows linked segments, etc. This is linear navigation.

**What a graph view would add:**
A graph view (like Obsidian's) renders entities as nodes and their connections as edges in an interactive visualization. For QueryPat, nodes would be dictionary terms, biography events, names, segments, and archive documents. Edges would represent co-occurrence, cross-reference, or thematic connection.

**Arguments for graph view:**
- **Discovery:** Users can visually spot clusters they wouldn't find by browsing. For example, a cluster around "Gnosticism" would show Valentinus, Nag Hammadi, Black Iron Prison, and the segments where Dick connects them — revealing his intellectual network at a glance.
- **Context:** When reading about VALIS, a graph shows it connected to Zebra, Logos, 2-3-74, Teilhard de Chardin, and specific 1978 segments — giving the user a map of Dick's conceptual landscape.
- **Scholarly value:** Researchers studying Dick's intellectual influences could use the graph to identify under-explored connections (e.g., a surprisingly strong link between Empedocles and Dick's cosmology).

**Arguments against (or for deferring):**
- Graph views are computationally expensive with 1,100+ segments, 310 terms, 119 biography events, and 500+ names. Performance on mobile would suffer.
- Without careful filtering, large graphs become "hairball" visualizations that are visually impressive but practically useless.
- The relational linking already provides the same information in a more readable, accessible format.

**Recommendation:** Defer full graph view to a later phase. Instead, consider a small "local graph" widget (like Obsidian's) on detail pages showing only the immediate neighbors of the current item (5-15 nodes). This gives the discovery benefit without the performance cost. Libraries: `react-force-graph-2d` or `d3-force` (both lightweight).

---

## 2. Linked Panes / Split View

**The idea:** Like Obsidian, users could open two items side by side — e.g., a dictionary term on the left and a biography entry on the right.

**Implementation approach:**
The simplest version uses CSS grid with a main pane and an optional "peek" pane. When a user Ctrl+clicks (or clicks a special icon) on any internal link, instead of navigating, the target opens in the side pane. The URL stays on the main item; the side pane is ephemeral.

**Technical considerations:**
- React Router doesn't natively support two simultaneous routes. The side pane would need to be a separate data-fetching component that loads JSON directly, not a routed page.
- On mobile, the side pane would need to become a bottom sheet or overlay instead of a side-by-side layout.
- State management: which item is in the side pane? A simple `useState` in the Layout component, passed via context.

**Risk of overengineering:** This adds significant complexity. A simpler first step: "hover preview" cards (like Wikipedia's page previews) that show a summary popup when hovering over any internal link. This gives 80% of the benefit with 20% of the complexity.

---

## 3. Backlinks Panel — Argument For and Against

**What it is:** A section at the bottom of every page showing "What links here" — every other page in the site that references the current item.

**Argument for:**
- Backlinks are the core of Obsidian's power. They turn a collection of pages into a knowledge graph without requiring manual curation.
- For QueryPat, a term like "Logos" would show: 47 Exegesis segments that discuss it, 3 biography events where Dick encountered the concept, 12 related dictionary terms, and any archive documents that reference it. This is enormously useful for researchers.
- It's the single most impactful feature for turning QueryPat from a "database viewer" into a "knowledge browser."

**Argument against:**
- For popular terms (Christ: 4,853 mentions), the backlinks section would be overwhelming. It needs aggressive grouping (by section type, by year, by relevance) and truncation.
- It duplicates information already shown in the "Linked Segments" and "Related Terms" sections on detail pages.
- On mobile, a long backlinks section pushes important content far down.

**Recommendation:** Implement a compact backlinks section with:
- Grouped by type (Exegesis Summaries, Biography, Dictionary, Archive)
- Show count per group, expand on click
- Maximum 5 items shown per group initially
- Only show on detail pages (TermDetail, SegmentDetail, NameDetail), not on list pages

This avoids clutter while providing the discovery value.

---

## 4. Density Indicators — Logic Explained

**What they are:** The biography page has three density levels that filter events by their `importance` score (1-5):

| Level | Label | Filter | Purpose |
|-------|-------|--------|---------|
| 1 | All Events | importance >= 1 | Full research archive — every documented event, including minor anecdotes (119 events) |
| 2 | Intellectual Biography | importance >= 3 | The story of Dick's intellectual and creative development — major readings, key relationships, significant publications, visionary experiences (101 events) |
| 3 | Major Events Only | importance >= 4 | Defining moments — births, deaths, marriages, breakdowns, 2-3-74, major publications (41 events) |

**How importance is scored (from the pkdbiostyle guide):**
- **5 = Defining event:** Birth, death, 2-3-74 experience, marriage to Tessa
- **4 = Major life event:** Publication of major novels, divorce, move to Fullerton, Hugo Award
- **3 = Intellectual influence:** Reading Plato, encountering Gnosticism, friendship with Bishop Pike
- **2 = Social context:** Participating in fan circles, attending a lecture
- **1 = Minor anecdote:** Small social events, passing references

**Why this matters for users:**
- A **casual reader** wants "Major Events Only" — a 5-minute overview of Dick's life in 41 key moments
- A **student** wants "Intellectual Biography" — the story of how Dick's reading and thinking evolved
- A **scholar** wants "All Events" — every documented detail for cross-referencing

This is the same principle as a map's zoom level: zoom out for highways, zoom in for side streets.

---

## 5. Global Search Results — Study

**Current state:** Search uses Fuse.js with a single flat list of results across segments, terms, archive docs, names, and biography. Results are shown as cards with type badges.

**Problems with current approach:**
1. Results are unranked beyond Fuse.js's fuzzy score, so a dictionary term and a passing mention in a segment have equal visual weight
2. No grouping — users searching for "VALIS" get a mixed list of the dictionary entry, 50+ segments, archive documents, and biography events
3. No preview of why a result matched (no highlighted matching text)

**Proposed search results design:**

### Option A: Grouped results (recommended)
Like Google's Knowledge Panel approach:
```
[Search: "VALIS"]

DICTIONARY (1 result)
  VALIS — Vast Active Living Intelligence System...

BIOGRAPHY (2 results)
  1976: Begins early drafts of VALIS-related material...
  1981: Publication of The Divine Invasion...

EXEGESIS SUMMARIES (47 results, showing top 5)
  Letter to Dorothy, Sep 12 1976 — introduces the term "VALIS"...
  Exegesis entry, Sep 15 1975 — explores Rome Two theory...
  [Show all 47 results]

ARCHIVE (3 results)
  ...
```

**Benefits:** Users immediately find the most relevant result type. The dictionary entry is the "canonical" result; segments provide depth.

### Option B: Unified ranked list with type badges (current, improved)
Keep the flat list but improve ranking: dictionary terms always float to top, followed by biography, then segments. Add match highlighting.

**Recommendation:** Option A (grouped) is more usable and aligns with the relational browser concept. Each group header becomes a navigational affordance.

---

## 6. Tag-Based Filtering vs. Page-Specific Filtering — Explained

**Page-specific filtering (current):**
When you click a category tag on the Biography page, it filters only biography events. When you click a concept tag on the Timeline page, it filters only timeline segments. Each page is an island.

**Cross-site tag filtering (proposed):**
When you click "Gnosticism" anywhere on the site, you see everything related to Gnosticism across all sections: dictionary definition, biography events where Dick encountered Gnostic ideas, Exegesis segments discussing Gnosticism, scholars who write about Dick and Gnosticism, and archive documents on the topic.

**Implementation:** A dedicated "tag results" page at `/tag/:tagname` that queries all data sources. Similar to the search page but pre-filtered to exact entity matches rather than fuzzy text search.

**The difference in user experience:**
- Page-specific: "Show me all biography events tagged 'Gnosticism'" (narrow)
- Cross-site: "Show me everything in this database about Gnosticism" (broad, exploratory)

Cross-site tagging turns entity tags into portals. A user reading about Dick's 1958 interest in Gnosticism can click the tag and immediately see the Exegesis passages where he develops Gnostic theology 16 years later, the scholars who study this thread, and the novels where Gnostic themes appear.

---

## 7. Consistent Template Design — Discussion

**The question:** Should the Psychology topics page, AI & Robots study, and Names in novels page share a common "topic entry" template, or have unique layouts?

**Argument for consistency:**
- Users learn one interface pattern and can navigate any section intuitively
- Development is faster — one component serves all three
- The site feels cohesive rather than like three different websites stitched together
- Mobile layouts are much easier to maintain with one template

**Argument for differentiation:**
- Psychology topics need room for mini-essays with inline citations
- AI & Robots entries are organized by story, not by concept
- Names need character relationship displays that don't apply to concepts

**Recommended approach — shared skeleton, differentiated content zones:**

All three use the same outer layout:
```
[Title]
[Type badge] [Tags]
[Short description — 1-2 sentences]

[Content zone — varies by type]

[Cross-references: Related terms, segments, biography events]
```

The **content zone** varies:
- **Psychology:** Essay text (200-400 words) with inline term links, "Further reading" with page references
- **AI & Robots:** Story-by-story breakdown with character links and thematic analysis
- **Names:** Character profile with novel appearances, relationships, and thematic significance

This gives users a familiar frame while allowing each section to serve its unique purpose.

---

## 8. Related Sidebar / Footer — Study

**The idea:** Every detail page shows a "Related" section with contextually linked items from other sections of the site.

**The clutter problem:**
A term like "Christ" connects to 4,853 segments, dozens of biography events, multiple scholars, and nearly every dictionary term. Showing all connections would bury the actual content.

**Proposed design — "Explore Further" footer with curated connections:**

```
── Explore Further ──────────────────────

In the Dictionary:    Logos, Holy Spirit, Parousia (3 of 28 related)
In the Biography:     1974: Begins writing the Exegesis...  (2 of 8 related)
In the Exegesis:      Letter to Claudia, Feb 27 1975...     (3 of 47 related)
In the Archive:       PKD Exegesis Folder 18...              (1 of 4 related)

[See all connections →]
```

**Selection logic:** Show the 2-3 most relevant items per section, determined by:
1. Direct mention (exact match) over thematic link
2. Higher importance/confidence scores first
3. Chronological diversity (don't show 3 items from 1978; spread across years)

**"Fun trips" approach:** Add a "Rabbit Hole" or "Deep Dive" suggestion — a curated path like: "This term connects to Zebra → which Dick identifies with VALIS → which he discusses in 47 Exegesis entries → and which appears in the novel VALIS (1981)." This gamifies exploration without cluttering the main interface.

---

## 9. Breadcrumb Navigation — Explained

**What it is:** A trail of links showing where you are in the site hierarchy:

```
Home > Dictionary > Valis
Home > Timeline > 1975 > Letter to Claudia, Feb 27 1975
Home > Biography > Early Life (1928-1946)
```

**Why it matters:**
- **Orientation:** Users who arrive via a cross-link (e.g., clicked "Valis" from a biography entry) immediately see they're on a dictionary page, not a biography page
- **Navigation:** One click to go back to the section index instead of using the browser back button
- **Context:** Shows the hierarchy — this segment is part of the 1975 timeline, which is part of the Exegesis Timeline

**Implementation:** A small component below the nav bar, above the page header. Uses React Router's current path to generate crumbs. Subtle styling — small text, muted color, not visually dominant.

**For mobile:** Breadcrumbs compress to show only the parent (e.g., "< Dictionary" as a back link) to save vertical space.

---

## 10. Interactive Features for Scholars — Study

**Potential features, ordered by implementation complexity:**

### Tier 1: Low complexity, high value
- **Bookmarks / Favorites:** Users can star any item (term, segment, biography event). Stored in localStorage. A "My Bookmarks" page lists them all. No backend needed.
- **Reading lists:** Users create named lists ("My VALIS research", "Gnostic theology thread") and add items to them. Also localStorage. Export as JSON or plain text.

### Tier 2: Medium complexity
- **Annotations:** Users can attach private notes to any item. Stored in localStorage. Shown as a small note icon on bookmarked items. Export as Markdown.
- **Citation export:** Each page has a "Cite" button that copies a formatted citation (Chicago, MLA, APA) for the source material referenced on that page.

### Tier 3: High complexity (future)
- **Shared annotations:** Multiple scholars can see each other's annotations. Requires a backend (database, authentication).
- **Collaborative reading paths:** Scholars create guided tours through the material and share them via URL. Requires backend.
- **Search history and "recently viewed":** Track browsing patterns to suggest related items. Privacy-sensitive.

**Recommendation for v1.0:** Implement Tier 1 (bookmarks + reading lists) using localStorage. These are zero-infrastructure features that provide immediate value to repeat visitors. The "Start Here" page can explain how to use them.

---

## Summary of Immediate Actions (v1.1 after push)

| Feature | Priority | Complexity | Status |
|---------|----------|------------|--------|
| Dark mode toggle | High | Low | Ready to implement |
| Linked panes (hover preview first) | Medium | Medium | Needs design |
| Global search (grouped results) | High | Medium | Ready to implement |
| Cross-site tag filtering | High | Medium | Ready to implement |
| "Start Here" guide page | High | Low | Ready to implement |
| Mobile-first responsive design | High | Medium | Partially done |
| Breadcrumb navigation | Medium | Low | Ready to implement |
| Compact backlinks footer | Medium | Medium | Needs design |
| Bookmarks (localStorage) | Medium | Low | Ready to implement |
| Consistent topic template | Medium | Low | Wait for content |
| Local graph widget | Low | High | Defer to v2 |
| Full graph view | Low | Very High | Defer to v2+ |
