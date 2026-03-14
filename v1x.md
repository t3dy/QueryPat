# QueryPat v1.x — From Database Viewer to Knowledge Browser

## What Changed

Version 1.0 shipped a working viewer for the PKD Exegesis database. Version 1.x reshapes it into a relational knowledge browser — a tool where every page is a starting point for exploration, not just an endpoint for lookup.

Eight features were added across nine new files. None require a backend. None add new dependencies. All degrade gracefully on mobile.

---

## The Eight Features

### 1. Entity Page Template

**Component:** `EntityLayout.tsx`

Every detail page in QueryPat — terms, segments, names, archive documents — now shares a common skeleton. The layout provides a title row with a bookmark star, type badges and tags, a one-line summary, a content zone that varies by entity type, and footer slots for cross-references and backlinks.

The content zone is a React `children` prop, so each page controls what goes inside while the frame stays consistent. A user who learns to read a dictionary entry can immediately navigate a segment page or a name page without reorienting.

Adopted by TermDetail, SegmentDetail, NameDetail, and ArchiveDetail.

### 2. Breadcrumb Navigation

**Component:** `Breadcrumbs.tsx`

A breadcrumb trail now appears below the navigation bar on every page, generated automatically from the current React Router path. On desktop, it renders the full chain — Home > Dictionary > VALIS. On mobile, it collapses to a single back link: < Dictionary.

The breadcrumbs serve two purposes. First, orientation: a user who arrives at VALIS via a cross-link from a biography event immediately sees they are on a dictionary page. Second, escape: one click returns them to the section index without reaching for the browser back button.

Segment breadcrumbs use `formatSegmentTitle` to display human-readable names rather than raw filenames.

### 3. Grouped Search Results

**Page:** `Search.tsx` (rewritten)

The flat list of search results has been replaced with results grouped by entity type, displayed in a fixed priority order: Dictionary first, then Biography, Exegesis Summaries, Names, and Archive Documents.

Dictionary terms appear first because they represent canonical definitions. When a user searches for "VALIS," the dictionary entry is the anchor; the fifty Exegesis segments that mention it are the depth.

Each group shows its top five results and can be expanded. The Fuse.js configuration now weights title matches three times higher than body text, so exact hits on entity names surface above incidental mentions. Snippets show context around the matched term rather than truncating from the start. The page accepts a `?q=` URL parameter, enabling deep links from other parts of the site.

### 4. Cross-Site Tag Filtering

**Page:** `TagResults.tsx` | **Route:** `/tag/:tagname`

Tags have been transformed from page-specific filters into global concept portals. Clicking "Gnosticism" on a dictionary page, a segment page, or a biography card now navigates to the same destination: a tag results page that gathers everything in the database related to that concept.

The tag page groups results using the same visual pattern as the search page. It draws from the existing search index, so no new data pipeline is needed. Tags have been wired into TermDetail (category and thematic tags), SegmentDetail (recurring concepts), NameDetail (allusion types), and ArchiveDetail (document category).

A user reading about Dick's 1958 encounter with Gnosticism can click the tag and immediately see the Exegesis passages where he develops Gnostic theology sixteen years later, the scholars who study this thread, and the novels where Gnostic motifs appear.

### 5. Explore Further Footer

**Component:** `ExploreFooter.tsx`

At the bottom of each entity page, a curated "Explore Further" section offers two or three related items from other parts of the site: dictionary terms, biography events, Exegesis entries, and archive documents.

The footer answers the question a reader asks after finishing a page: "Where do I go next?" Rather than presenting every connection (VALIS links to fifty segments), it shows a small, diverse selection — enough to suggest a path without overwhelming the reader. Total counts and "See all" links are available for those who want the full picture.

The footer renders in a responsive grid that collapses to a single column on narrow screens.

### 6. Backlinks Panel

**Component:** `BacklinksPanel.tsx`

Below the Explore Further section, a "What Links Here" panel reveals the relational structure of the database. It lists every page that references the current item, grouped by entity type, with a count badge and the first five entries shown per group.

Each group is expandable. The panel for VALIS, for instance, shows 50 Exegesis summaries, 3 biography events, and 8 related dictionary terms. A researcher studying Dick's use of the concept can see at a glance how densely it is woven through the corpus.

Backlinks are computed from data already loaded for the detail page, so no additional fetches are needed.

### 7. User Bookmarks

**Hook:** `useBookmarks.ts` | **Component:** `BookmarkButton.tsx` | **Page:** `Bookmarks.tsx`

A star icon now appears beside the title on every entity page. Clicking it saves the item to a personal bookmark list stored in the browser's localStorage. A dedicated Bookmarks page, accessible from the navigation bar, lists all saved items grouped by entity type with timestamps and one-click removal.

Bookmarks persist between sessions and require no backend. Cross-component synchronization is handled through a lightweight listener pattern — starring an item on one page immediately updates the Bookmarks page if both are open.

This is the simplest version of a feature that matters: scholars working through the Exegesis over multiple sessions need a way to mark where they have been and what they want to return to.

### 8. Hover Previews

**Component:** `HoverPreview.tsx`

Hovering over any internal link — a related term, a linked segment, a name reference — now displays a small preview card showing the entity's type, title, and a short description.

The preview loads data directly from JSON without navigating away from the current page. An in-memory cache prevents redundant fetches. The card positions itself above or below the link depending on available viewport space, with a 300ms delay to avoid distracting flicker.

On mobile, where hover is not available, the previews are hidden entirely. This provides most of the benefit of split-pane navigation without any of the routing complexity.

---

## Files Modified

| File | Change |
|------|--------|
| `site/src/App.tsx` | Added routes for `/bookmarks` and `/tag/:tagname` |
| `site/src/components/Layout.tsx` | Integrated Breadcrumbs component; added Bookmarks to navigation bar |
| `site/src/pages/Search.tsx` | Rewritten with grouped results, weighted ranking, expandable groups, `?q=` deep linking |
| `site/src/pages/TermDetail.tsx` | Wrapped in EntityLayout; added ExploreFooter, BacklinksPanel, HoverPreview; tags linked to `/tag/` |
| `site/src/pages/SegmentDetail.tsx` | Wrapped in EntityLayout; added ExploreFooter, BacklinksPanel, HoverPreview; concept tags linked to `/tag/` |
| `site/src/pages/NameDetail.tsx` | Wrapped in EntityLayout; added ExploreFooter, BacklinksPanel, HoverPreview |
| `site/src/pages/ArchiveDetail.tsx` | Wrapped in EntityLayout; category tag linked to `/tag/` |
| `site/src/App.css` | Added styles for breadcrumbs, entity layout, bookmarks, explore footer, backlinks, hover previews, search groups, and responsive overrides |

## Files Created

| File | Purpose |
|------|---------|
| `site/src/components/EntityLayout.tsx` | Shared detail page layout with title, badges, tags, bookmark, content slot, footer slot |
| `site/src/components/Breadcrumbs.tsx` | Path-derived breadcrumb navigation with mobile back-link fallback |
| `site/src/components/BookmarkButton.tsx` | Star toggle for bookmarking entities |
| `site/src/components/ExploreFooter.tsx` | Curated cross-references grouped by section |
| `site/src/components/BacklinksPanel.tsx` | Expandable backlinks grouped by entity type |
| `site/src/components/HoverPreview.tsx` | Preview cards for internal links with caching and positioning |
| `site/src/hooks/useBookmarks.ts` | localStorage-backed bookmark state with cross-component sync |
| `site/src/pages/Bookmarks.tsx` | Saved items listing grouped by entity type |
| `site/src/pages/TagResults.tsx` | Cross-site tag results with grouped display |

---

## Architecture Decisions

**No global state library.** Bookmarks use localStorage with a simple listener pattern for cross-component sync. Everything else is local state or derived from the URL. React Context was considered and rejected as unnecessary for a single shared concern.

**No new dependencies.** Every feature is built with React, React Router, and Fuse.js, all already in the project. HoverPreview uses native `fetch` with an in-memory `Map` for caching. The total bundle size increased by under 3 KB gzipped.

**Mobile-first responsive design.** Breadcrumbs collapse to back links. Hover previews are hidden. The Explore Further grid stacks to a single column. All card grids remain single-column on narrow viewports. Nothing breaks; the experience simplifies.

**Incremental adoption.** EntityLayout wraps existing page content without requiring changes to the data schema or the JSON export pipeline. Tags link to `/tag/` routes using the existing search index. Backlinks and explore items are computed from data already fetched for the detail page.

**Performance.** Hover preview data is cached in memory after the first fetch. Backlinks and explore items add no network requests — they are derived from the entity's own JSON payload. The tag page reuses the search index already loaded by the Search page. On a dataset with 1,107 segments and 310 terms, all pages render instantly.

---

## Deferred to v2

- Graph visualizations (local graph widget, full network view)
- Collaborative features (shared annotations, reading paths)
- Dark mode toggle
- "Start Here" guided introduction
- Citation export (Chicago, MLA, APA)
- Search history and recently viewed items
