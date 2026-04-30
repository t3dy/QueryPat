# Writing Audit — Dashboard + Exegesis landing (P1 deliverables, 2026-04-29)

Scope: the prose written in the P1 redesign — [Dashboard.tsx](site/src/pages/Dashboard.tsx) (hero, intro paragraphs, "What's inside" list, two captions) and [Exegesis.tsx](site/src/pages/Exegesis.tsx) (hero, intro paragraphs, browse-by-year and recurring-vocabulary captions, scholar list).

Audited against the five enforced editorial rules in [PKDontology.md §5.4](PKDontology.md) (state lane, attribute interpretations, surface contradictions, cross-link, distinguish fact from self-report) plus the templates' style requirements (verbs over adjectives; no vague praise; link integrity).

---

## A. Factual errors — must fix

### A1. Erik Davis is not a co-editor of the published *Exegesis* {#a1}

[site/src/pages/Exegesis.tsx:23](site/src/pages/Exegesis.tsx:23):
```
{ slug: 'erik-davis', name: 'Erik Davis', note: 'Co-editor of the published Exegesis (2011) ...' }
```

Per [scholars.json](site/public/data/scholars.json), Davis's role is "Cultural critic, esoteric historian." His Exegesis contribution is `'Annotations on the published Exegesis (HMH, 2011)'` — he was an annotator, not a co-editor. The co-editors were Pamela Jackson and Jonathan Lethem.

**Fix:** "Annotator on the published *Exegesis* (2011); *TechGnosis* (1998); *High Weirdness* (2019)."

### A2. Simon Critchley — wrong book title {#a2}

[site/src/pages/Exegesis.tsx:27](site/src/pages/Exegesis.tsx:27):
```
'Philosophy and the Tragic — engages 2-3-74 as philosophical event'
```

There is no Critchley book by that title. Per [scholars.json](site/public/data/scholars.json), his PKD-relevant works are *How to Stop Living and Start Worrying* (Polity, 2010 — chapter on PKD), *The Faith of the Faithless* (Verso, 2012), and his annotations on the Exegesis (HMH, 2011).

**Fix:** "Annotator on the *Exegesis* (2011); chapter on PKD in *How to Stop Living and Start Worrying* (2010)."

### A3. Jeffrey Kripal — "The Flip" is not PKD-relevant; slug is wrong {#a3}

[site/src/pages/Exegesis.tsx:26](site/src/pages/Exegesis.tsx:26):
```
{ slug: 'jeffrey-kripal', ... 'Mutants and Mystics; The Flip — places PKD within visionary religious studies' }
```

Two issues. First, Kripal's [scholars.json](site/public/data/scholars.json) entry lists *Authors of the Impossible* (2010) and *Mutants and Mystics* (2011) as the PKD-relevant works; *The Flip* (2019) is a Kripal book but not where his PKD engagement lives. Second, his scholar_id in the database is `jeffrey-j-kripal`, not `jeffrey-kripal` — the link will hit `/scholars` cleanly but the anchor is dead either way (see B1).

**Fix:** "Annotator on the *Exegesis* (2011); *Mutants and Mystics* (2011); *Authors of the Impossible* (2010)." Update slug to `jeffrey-j-kripal`.

---

## B. Link integrity — must fix

### B1. Anchor links to `/scholars#slug` don't resolve {#b1}

[site/src/pages/Exegesis.tsx:134](site/src/pages/Exegesis.tsx:134) generates `<Link to={`/scholars#${slug}`}>`. [Scholars.tsx](site/src/pages/Scholars.tsx) does not render `id={scholar_id}` on its cards (cards are tracked only by internal expanded-state). The hash is dropped silently — every "key scholars" link lands on `/scholars` with no scroll target and no preselection.

**Fix options, ordered by effort:**
1. Drop the hash — link to `/scholars` plainly. The user can search/scroll. (lowest effort, what I'll do for P1)
2. Add `id={s.scholar_id}` to the scholar card root in [Scholars.tsx:151](site/src/pages/Scholars.tsx:151), and a `useEffect` that opens the matching card and scrolls to it. (correct fix, queue for follow-up)

### B2. "Evidentiary lane" and "scholarly frame" link to /scholars; lanes aren't explained there {#b2}

[Dashboard.tsx:59](site/src/pages/Dashboard.tsx:59) links the phrase "evidentiary lane" to `/scholars`. [Exegesis.tsx:60](site/src/pages/Exegesis.tsx:60) links "scholarly frame" to `/scholars`. Neither phrase is about scholars per se — they're about the A/B/C/D/E lane scheme defined in [PKDontology.md §3](PKDontology.md). Lanes are visualized as colored badges on `/archive` and `/archive/:slug`, but there's no on-site explainer page.

**Fix:** point both links at `/archive` (where the lane badges actually appear). Defer creating a methodology/about page to a later phase.

---

## C. Voice and concision — should fix

### C1. "Scholarly research portal" is redundant {#c1}

[Dashboard.tsx:42-44](site/src/pages/Dashboard.tsx:42). "Scholarly research portal" doubles up — the second word doesn't add anything. "Scholarly portal" is enough. Companion phrase "single research surface" later in the same passage (line 58) compounds the issue.

**Fix:** "scholarly portal"; "into a single site."

### C2. "Drug-induced cognition" is awkward {#c2}

[Dashboard.tsx:52](site/src/pages/Dashboard.tsx:52). "Drug-induced cognition" implies the drugs *cause* the cognition, which is a narrower claim than the prose intends and not what PKD's fiction is mostly *about* (his work explores altered states, perceptual fragility, and amphetamine-driven productivity rather than cognition-induced-by-drugs as a theme).

**Fix:** "drugs and altered states."

### C3. "Registered disputes" is opaque {#c3}

[Dashboard.tsx:121](site/src/pages/Dashboard.tsx:121). Insider phrasing — readers won't know what a "registered" dispute is. The plain word is "documented."

**Fix:** "documented disputes" — or, since the scholar template calls them simply "disputes," just "disputes."

### C4. Parenthetical "(Publications coming.)" leaks roadmap into front-of-house copy {#c4}

[Dashboard.tsx:101](site/src/pages/Dashboard.tsx:101). Front-of-house copy that announces its own incompleteness is a maintenance liability — easy to forget to remove once P2 lands. The empty 1950s/60s in the year grid below already signal this (and the Browse-by-year caption already says publications are queued). Drop the parenthetical.

**Fix:** remove "(Publications coming.)".

### C5. "Reliability tier" — minor jargon {#c5}

[Dashboard.tsx:97](site/src/pages/Dashboard.tsx:97). The phrase is fine in the data dictionary but a casual reader sees "tier" without explanation. Mild — could go either way. Keep, since the Biography page itself surfaces the tiers visibly.

**Decision:** keep.

---

## D. Editorial-discipline checks (the five rules)

| Rule | Dashboard | Exegesis page |
|------|-----------|---------------|
| State lane | Implicit only — invokes "evidentiary lane" but doesn't model it. Acceptable for hero copy. | **Yes** — "Treat segments as Lane B evidence" with a contradiction-aware gloss ("not necessarily what was true"). |
| Attribute interpretations | N/A in pure descriptive copy — no contested claims made. | **Yes** — "experiences he interpreted variously" attributes the four explanations (revelation/illness/KGB/satellite) to PKD's own self-report rather than asserting them. |
| Surface contradictions | N/A. | **Yes** — Lane B caveat surfaces the autobiographical-by-unreliable-narrator framing. |
| Cross-link | **Yes** — every "What's inside" entry is a link; six routes referenced. | **Yes** — links to /timeline, /dictionary, /scholars, year pages. |
| Fact vs self-report | N/A. | **Yes** — "what PKD theorized about himself, not necessarily what was true" is the explicit move. |

No editorial-rule violations. The Exegesis intro is the strongest piece of writing in the P1 set; the Dashboard intro is descriptive (no contested claims) and thus passes vacuously.

---

## E. Numbers — verified

| Claim | Source | OK? |
|------|--------|-----|
| 1928–1982 | well-attested | ✓ |
| Forty-four novels | common count | ✓ |
| Over a hundred short stories | actual count ~121 | ✓ (could be more specific) |
| ~8,000 manuscript pages (Exegesis) | Sutin 1989; Lethem/Jackson 2011 introduction | ✓ |
| 944-page selection (2011 published Exegesis) | HMH 2011 first printing | ✓ |
| 646 biography events | [biography/index.json](site/public/data/biography/index.json) total field | ✓ (live-fetched) |
| 1,107 segments | [analytics.json](site/public/data/analytics.json) totals.segments | ✓ (live-fetched) |
| 207 with parsed summaries | analytics totals.segments_with_summary | ✓ (live-fetched) |
| 882 with raw text | analytics totals.segments_with_raw_text | ✓ (live-fetched) |
| Four years populated (1975, 1976, 1978, 1981) | [QueryPatOverview.md §9.1](QueryPatOverview.md), confirmed against timeline/index | ✓ |
| 228+ archive documents | analytics totals.archive_docs (228); [README.md](README.md) says 237; [HANDOVER.md](HANDOVER.md) says 237. Worth flagging. | ⚠ — see F1 |
| 191 fiction characters (in 592 names) | [README.md](README.md) v2.1 entry | ✓ |
| 119 scholars | scholars.json length (live-fetched) | ✓ |
| 310 dictionary terms | analytics totals.terms_public | ✓ |

---

## F. Data-vs-prose drift to flag

### F1. Archive document count: 228 vs 237 {#f1}

`analytics.json` reports 228 archive documents (the count baked into the build at the time analytics was generated). `README.md` and `HANDOVER.md` claim 237 (after the v3 corpus integration of nine new documents). The Dashboard "What's inside" hard-codes "228+" and the stat tile pulls 228 from analytics. The "+" hedge papers over the drift but doesn't fix it.

**Fix in this audit:** none — the prose number tracks `analytics.json` correctly. Real fix is to rebuild analytics.json from the post-v3 database. Out of scope for P1; flag for whoever reruns `python scripts/build_all.py --export-only`.

### F2. The "44 novels / 121 stories" specificity question {#f2}

"Forty-four novels and over a hundred short stories" undercounts the stories. Actual short-story count is ~121 (commonly cited; the Citadel five-volume *Collected Stories* runs to 118 stories with several uncollected). "Over a hundred" is technically correct but reads as soft. Acceptable for hero copy; keep.

---

## Summary of fixes to apply

| # | Where | Change |
|---|-------|--------|
| A1 | Exegesis.tsx — Davis | "Co-editor" → "Annotator"; tighten note |
| A2 | Exegesis.tsx — Critchley | Replace "Philosophy and the Tragic" with actual works |
| A3 | Exegesis.tsx — Kripal | Replace "The Flip" with *Authors of the Impossible*; fix slug to `jeffrey-j-kripal` |
| B1 | Exegesis.tsx — scholar links | Drop `#slug` anchor (anchors are dead); link cleanly to `/scholars` |
| B2 | Dashboard.tsx + Exegesis.tsx | Repoint "evidentiary lane" / "scholarly frame" to `/archive` |
| C1 | Dashboard.tsx | "scholarly research portal" → "scholarly portal"; "research surface" → "site" |
| C2 | Dashboard.tsx | "drug-induced cognition" → "drugs and altered states" |
| C3 | Dashboard.tsx | "registered disputes" → "disputes" |
| C4 | Dashboard.tsx | Drop "(Publications coming.)" |

Deferred (out of P1 scope):
- B1 proper fix (add anchor IDs + scroll-into-view) — queue for next session.
- F1 (rebuild analytics) — needs `python scripts/build_all.py --export-only`.
