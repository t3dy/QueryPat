# Handover — End of Session (2026-04-29)

A self-contained brief for picking up this project in a new conversation window. Read this first, then [QueryPatOverview.md](QueryPatOverview.md) for methodology and [CONTENT_PLAN_V3.md](CONTENT_PLAN_V3.md) for the writing roadmap.

---

## Where we are

**Deployed and live:** [t3dy.github.io/QueryPat](https://t3dy.github.io/QueryPat/) — main is at commit `d98336c` after merging v3 (editorial frame) and v4 (topic studies + AI scenes pipeline).

**Branches:** `main` is the only one anyone needs to care about. `claude/goofy-williams-cff64c` is the worktree branch from this session — already merged into main via [PR #1](https://github.com/t3dy/QueryPat/pull/1).

**Git workflow preference (confirmed in this session):** the user wants everything on main. Direct commits to main are fine; long-lived feature branches are unnecessary overhead for a solo project. PR #1 was created defensively because main had uncommitted work; once that landed it was merged.

**External-source convention:** large copyrighted source materials live outside git. Already excluded via `.gitignore`: `PKD LLM Chats/`, `PKD stuff to add/`, `PaulPKDarchive/`. Archive document JSON entries reference paths inside these external folders.

---

## What landed in this session

### v3 — Editorial frame, ontology, scholar density, corpus integration

**New methodology documents** (committed, on main):
- [PKDontology.md](PKDontology.md) — the data ontology. Ten core entity domains, four standing researcher questions, evidentiary lanes (A: Fiction, B: Exegesis, C: Scholarship, D: Synthesis, E: Primary), the contradiction registry of nine known dispute zones, and the fact-vs-interpretation editorial line.
- [CONTENT_PLAN_V3.md](CONTENT_PLAN_V3.md) — the writing roadmap that succeeds [IMPROVEMENT_PLAN.md](IMPROVEMENT_PLAN.md). Ten phases, scholar profile expansion targets, document summary triage.
- [QueryPatOverview.md](QueryPatOverview.md) — end-to-end methodology: provenance, data model, build pipeline, editorial system, JSON contract, site architecture, AI-vs-human boundary.
- [scripts/overrides/templates/](scripts/overrides/templates/) — 10 style-guide templates (scholarship, biography, interview, primary, fan, newspaper, finding aid, scholar, dictionary, biography event).

**Scholar profile expansion** (105 → 119; 37 with rich profiles):
- Tier-1 biographers fully expanded: Sutin, Anne Dick, Arnold, Peake, Tessa Dick, Rickman, **Pamela Jackson** (promoted Tier 3 → Tier 1 after recovering her 1999 UC Berkeley dissertation)
- Tier-2 academic monograph authors: Robinson, Fitting, Rossi, Palmer, Freedman, Butler, Burton, Lem, Suvin, Jameson, Csicsery-Ronay Jr., Kripal, McKee, DiTommaso, Warrick, Umland, Dunst, Davis, Angus Taylor
- 14 new scholars added: J.K. Thomas, Ken Simpson, Perry Kinman, Michael Levy, Lejla Kucukalic, Eric Carl Link, Jason Vest, Hazel Pierce, Douglas Mackey, David Gill, Roger Luckhurst, Simon Critchley, N. Katherine Hayles, Scott Bukatman
- New `Scholars.tsx` UI fields rendered: **Key Arguments**, **Scholarly Lineage**, **Disputes**, **Quotable Lines**

**Document summary rewrites** (Tier-1 biographies — six-section page summaries per the scholarship template):
- Sutin's *Divine Invasions* (1989), Anne Dick's *Search* (1995/2010), Arnold's *Divine Madness* (2016), Peake's *A Life of PKD* (2013), Robinson's *The Novels of PKD* (1984)

**New archive documents** (228 → 237) integrated from `C:\QueryPat\PKD stuff to add\`:
- Pamela Jackson 1999 UC Berkeley dissertation *The World Philip K. Dick Made* (UMI #9931275)
- Erik Davis ASE conference talk *The Hymn of Philip K. Dick*
- David Gill 2006 MA thesis on PKD's paranoia
- J.K. Thomas, *Coin-Operated Doors and God: A Gnostic Reading of Philip K. Dick* (2014)
- Ken Simpson, *The Aesthetics of Garbage in Martian Time-Slip* (CRAS 44.2, 2014)
- Angus Taylor, *Philip K. Dick and the Umbrella of Light* (T-K Graphics, 1975) — one of the very earliest book-length PKD essays
- Music in PKD research spreadsheet (2,076-row catalog)
- Erik Davis SPIN 1989 / Sonic Youth quotation excerpts
- Rouzleweave #2 (May 2002, Perry Kinman, fan publication digitized by Frank Hollander 2017)

### v4 — Topic studies pipeline, AI scenes feature

(This was the user's pre-existing in-progress work, present as uncommitted on main when this session began. Committed and shipped.)

- `Documentation/STUDIES_BLUEPRINT.md` — design document for topic studies as a new top-level entity type
- `database/scenes_schema.sql` — `ai_interaction_types`, `ai_scene_candidates` tables
- 241-line addition to `database/unified_schema.sql` for studies support
- `scripts/studies/` — full pipeline (~30 scripts, lexicons, prompts)
- 5 new pages: `StudiesIndex`, `StudyIndex`, `TopicDetail`, `ScenesIndex`, `SceneDetail` with routes `/studies`, `/studies/:studyId`, `/studies/:studyId/:slug`, `/studies/ai/scenes`, `/studies/ai/scenes/:sceneId`
- 8 new components in `site/src/components/studies/`
- 4.8 MB of pre-built JSON exports in `site/public/data/studies/`
- Homeopape research: `site/public/homeopape.html`, `homeopape_report.md`, `Documentation/perry_kinman_homeopape_malfunction.md`
- `AIpassages.md` (1.1 MB) and `PSYpassages.md` (2.3 MB) — extracted-text corpora for the studies pipeline

---

## Direction tweaks made in this conversation

These are the editorial/architectural shifts the user established. The system files have been updated to reflect them; the implementation work below is **outstanding**.

### Tweak 1 — Project scope is broader than the Exegesis

The site is **a knowledge portal about Philip K. Dick the author**, not just a viewer for the *Exegesis*. The Exegesis is one (very important) source within a larger PKD studies frame that includes biography, fiction, letters, interviews, scholarship, fan reception, adaptations, and visual/musical reception.

**Implication for naming:** the user wants the title changed from "QueryPat - Exegesis Knowledge Portal" to **"Philip K. Dick Knowledge Portal"**.

**Implication for IA:** the *Exegesis* should be **its own tab**, not the centerpiece of the dashboard. The dashboard should be PKD-as-author, with the Exegesis prominent but discrete.

### Tweak 2 — Timeline must include publications, not just Exegesis writings

Currently the timeline shows Exegesis segments by year (1975, 1976, 1978, 1981 are the only populated years) plus biography events. **Publications should be on the timeline** — novels published, stories sold, contracts signed, drafts written. This would naturally fill out the 1950s and 1960s, currently barren on the timeline.

The user explicitly noted: *"I don't understand why so many of the years cannot be clicked in the 'Browse by Year' section. That whole design needs to be rethought."* The current Dashboard `Browse by Year` greys out years with `count + bio_events == 0`, which is most of the 1950s and 1960s — even though PKD wrote and published prolifically those decades.

### Tweak 3 — Scholar profiles articulate contributions, not provide vague praise

This was the foundational v3 editorial commitment: scholar profiles must articulate **the specific contributions** scholars make to PKD studies (key arguments, scholarly lineage, disputes), rather than vague "important / fascinating" prose. The [scholar template](scripts/overrides/templates/template_scholar.md) and the 37 rewrites are the implementation. **Status: substantially complete** (37 of 119 with rich profiles; 82 still to expand per [CONTENT_PLAN_V3 §4](CONTENT_PLAN_V3.md)).

### Tweak 4 — Document summaries capture "all the key contributions both academic and fan"

The other foundational v3 commitment, also reflected in the [scholarship template](scripts/overrides/templates/template_doc_scholarship.md). Six required sections; the Robinson, Sutin, Anne Dick, Arnold, Peake rewrites are the demonstrations. **Status: 5 of ~130 needing rewrite are done.**

### Tweak 5 — The `PKD stuff to add/` integration pattern

When the user adds source materials to a `PKD stuff to add/` folder in the project root, those should be:
1. Integrated into the database (new archive doc JSON entries, scholar profile expansions, dictionary additions as relevant)
2. Cross-linked per [PKDontology §6](PKDontology.md)
3. The folder itself is gitignored — only the resulting database entries are tracked

This pattern was established mid-session and used to integrate the 9 new archive documents listed above.

### Tweak 6 — All work goes to main (no feature branches)

The user prefers direct-to-main commits. Use PRs only when there's already-uncommitted unrelated work on main that needs to be preserved before merging.

---

## Outstanding work (queued for next session)

In priority order, with concrete action items:

### P1 — Rebrand and IA restructure (the user's last directive before this handover)

1. **Change site title** from `QueryPat - Exegesis Knowledge Portal` to `Philip K. Dick Knowledge Portal`. Files to edit:
   - [site/index.html](site/index.html) — `<title>` element
   - [site/src/pages/Dashboard.tsx](site/src/pages/Dashboard.tsx) — `<h1>` and subtitle
   - [README.md](README.md) — top-level heading (keep "QueryPat" as repo name; site name becomes "Philip K. Dick Knowledge Portal")

2. **Redesign the Dashboard** as a PKD-as-author portal. The current dashboard centers the Exegesis (counts headlined as "Exegesis Summaries", subtitle says "scholarly reference for Philip K. Dick's *Exegesis*"). The redesign should:
   - Lead with PKD-as-author: a brief biographical orientation, dates (1928–1982), what the portal contains and how to navigate it
   - Surface the breadth — fiction, letters, interviews, scholarship, fan publications, the Exegesis, adaptations
   - Demote the Exegesis to one prominent tile among several rather than the center
   - Keep the entry-point links (Timeline, Dictionary, Archive, Biography, Names, Scholars, Studies) but rebalance their visual weight

3. **Add an `/exegesis` route** or rename the current Timeline tab so the Exegesis has its own clear home. Decision needed: is "Exegesis" its own tab in the nav, or does Timeline remain the home for it? My recommendation: rename "Timeline" → "Exegesis" if Timeline is in fact mostly Exegesis content, *or* keep "Timeline" as the unified chronology (Exegesis + biography + publications, after the data fix in P2) and add a separate "Exegesis" tab that surfaces the full *Exegesis* manuscript holdings and the editorial / annotation context.

### P2 — Timeline data fix (publications on the timeline)

Why so many years aren't clickable: `analytics.json` defines `has_content = true` only when `count + bio_events > 0`. For most pre-1974 years that's false. The fix is **add publications to the timeline data**.

1. **Add a `publications` field** to per-year timeline JSON files (`timeline/years/{year}.json`). A publication entry should have at least: title, date_display, date_start, type (novel / story / essay / letter), publisher / venue, and a link to the relevant document or work entity.
2. **Source the publication data** from one of:
   - The `documents` table where `is_pkd_authored = true` and `category` is novels/short_stories/letters/etc. (the lowest-cost option — uses what's already in the DB)
   - PKD's known bibliography (a more authoritative external list)
   - A new `works` table per [PKDontology §2.2](PKDontology.md) capturing the canonical bibliography
3. **Update `analytics.json`** so `has_content` reflects publications too. The 1950s and 1960s should light up.
4. **Update Dashboard `Browse by Year`** rendering — the current greying logic stays the same but the underlying data fixes the experience.
5. **Update Timeline page** to render a third entry type (publications) alongside segments and biography events, with its own card style and badge.

### P3 — Resume the v3 editorial work

Per [CONTENT_PLAN_V3 §7](CONTENT_PLAN_V3.md) the implementation order continues:

3. **Document rewrite — Tier-1 biographies + major monographs** — 5 of ~30 done (Sutin, Anne Dick, Arnold, Peake, Robinson). Next: the major academic monographs (Palmer's *Exhilaration and Terror*, Freedman's *Critical Theory*, Rossi's *Twisted Worlds*, Burton's *Bergson and Dick*, Butler's Pocket Essentials).
4. **Theme entity table + initial 20 themes** (per [PKDontology §2.6](PKDontology.md)).
5. **Vision-event entity table + initial 10 visions** (per [PKDontology §2.3](PKDontology.md)).
6. **Document rewrite — primaries + interviews + SFS articles**.
7. **Dictionary deepening** (per [CONTENT_PLAN_V3 §6.2](CONTENT_PLAN_V3.md)).
8. **Document rewrite — fan publications + newspapers + finding aids**.
9. **Biography deep extraction** — target 1500+ events from current 646 by mining the Tier-1 biographies more thoroughly.
10. **Segment gap-fill** — 900 of 1107 Exegesis segments lack parsed summaries (longest tail).

### P4 — GitHub Actions deprecation warning

The deploy pipeline is on `actions/checkout@v4`, `actions/setup-node@v4`, `actions/upload-artifact@v4`, all using Node.js 20. GitHub will force Node.js 24 starting June 2, 2026, and remove Node.js 20 from runners on Sept 16, 2026. Bump these before then. Non-blocking but real.

### P5 — v4 (studies / scenes) follow-up — open question

The studies pipeline shipped but I haven't audited the data flow end-to-end. The pipeline produces JSON in `site/public/data/studies/` consumed by the new pages. Worth checking:
- Whether the 5 new pages render on the live site without errors
- Whether the scenes data has the expected shape
- Whether the AIpassages.md / PSYpassages.md inputs are reproducible from a build script (the user's call on whether these stay tracked or get gitignored if they're machine-generated)

---

## Key files to know about

| File | Why it matters |
|------|---------------|
| [QueryPatOverview.md](QueryPatOverview.md) | End-to-end methodology — read first |
| [PKDontology.md](PKDontology.md) | Editorial frame — what the database tracks and why |
| [CONTENT_PLAN_V3.md](CONTENT_PLAN_V3.md) | Writing roadmap — what's queued |
| [scripts/overrides/templates/](scripts/overrides/templates/) | 10 style-guide templates governing all new content |
| [README.md](README.md) | Project surface; counts; site link |
| [site/public/data/scholars.json](site/public/data/scholars.json) | 119 scholars; 37 rich profiles per the new template |
| [site/public/data/archive/index.json](site/public/data/archive/index.json) | 237 archive documents; per-doc summaries in `docs/{slug}.json` |
| [site/public/data/analytics.json](site/public/data/analytics.json) | Dashboard data — `segments_per_year` controls the "Browse by Year" rendering |
| [site/src/pages/Dashboard.tsx](site/src/pages/Dashboard.tsx) | Landing page — slated for redesign per Tweak 1 |
| [site/src/pages/Timeline.tsx](site/src/pages/Timeline.tsx) | Timeline page — slated for publications integration per Tweak 2 |
| [database/unified_schema.sql](database/unified_schema.sql) | Canonical schema, including v4 studies additions |
| [database/scenes_schema.sql](database/scenes_schema.sql) | AI scenes pipeline schema |

---

## How to pick up in a new session

1. **First message to send:** "Read [HANDOVER.md](HANDOVER.md) and [QueryPatOverview.md](QueryPatOverview.md). I want to start on P1: rename the site to 'Philip K. Dick Knowledge Portal' and redesign the dashboard." (or whichever P-priority you want next)
2. **Confirm context:** ask the new session to summarize what it understands the next priority to be before it starts editing — a 30-second sanity check that the handover transferred correctly.
3. **Editorial discipline:** every new entry the session writes should respect [PKDontology.md](PKDontology.md)'s five enforced rules (state lane, attribute interpretations, surface contradictions, cross-link six ways, distinguish fact from self-report) and the relevant template in [scripts/overrides/templates/](scripts/overrides/templates/).

---

## Open questions for you to decide

1. **Repo name vs. site name.** The repo is `t3dy/QueryPat` — do you want to rename the GitHub repo to match the new site name, or keep "QueryPat" as the project codename and use "Philip K. Dick Knowledge Portal" only as the user-visible site title?
2. **Exegesis tab vs. Timeline tab.** Should "Exegesis" be its own top-level tab containing the *Exegesis* manuscript navigator, while "Timeline" becomes a unified chronology of life + publications + Exegesis writings? Or fold the Exegesis under Timeline as currently? My read: separate them.
3. **Publication source-of-truth.** When we put publications on the timeline, do we mine the existing `documents` table where `is_pkd_authored = true`, or build a canonical `works` table from a known PKD bibliography? Latter is cleaner; former is faster.
4. **AIpassages.md / PSYpassages.md.** Are these reproducible from a build script, or hand-curated? If reproducible, gitignore them; if curated, track them.
5. **v4 audit.** Want me to audit the studies pages on the live site before the redesign work, or trust they're working?
